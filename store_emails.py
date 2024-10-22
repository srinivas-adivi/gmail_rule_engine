import os.path

from sqlalchemy.exc import IntegrityError, PendingRollbackError
import yaml

import smm.data_models
import smm.provider
import smm.serializer
import smm.rules_engine
import db_lib


def read_config(path_to_config):
    if not os.path.exists(path_to_config):
        raise ValueError(f"configuration file not found: `{path_to_config}`")

    with open(path_to_config) as of:
        config_content = yaml.safe_load(of.read()) or {}
        config_info = smm.data_models.Config(**config_content)
        return config_info

def main(path_to_config='config.yaml'):
    try:
        config_data = read_config(path_to_config)
        if config_data:
            db_info = config_data.db_config or {}
            db_type = db_info.db_type.name
            db_config = getattr(db_info, db_type)
            print(f"{db_type}, {db_config}")

            service_info = config_data.service_config or {}
            service_name = service_info.service.name
            service_config = getattr(service_info, service_name)
            print(f"{service_name}, {service_config}")
            try:
                provider = smm.provider.EmailServiceProvider(service_name, service_config)
                email_srv = provider.get_email_service()
                emails = email_srv.emails()
            except AttributeError as error:
                print(f"Failed: {error}")
                return

            # Get payload manager
            payload_manager = provider.get_payload_manager()

            # Create table
            db_lib.Base.metadata.create_all(db_lib.engine)

            for email in emails:
                msg_id = email['id']
                print(f"store: msg_id: {msg_id}")

                msg_data = email_srv.get_email(msg_id)
                msg_data_obj = smm.data_models.GmailMessage(**msg_data)
                email_payload = payload_manager.api_parser(msg_data_obj)

                serializer = smm.serializer.GmailSerializer()
                email_schema = serializer.to_email_schema(email_payload)
                email_data = serializer.to_email_model(email_schema)

                try:
                    email = db_lib.Message(**email_data)
                    db_lib.session.add(email)
                    db_lib.session.commit()
                except IntegrityError as error:
                    print(error)
                except PendingRollbackError as error:
                    print(error)
                    break

    except ValueError as e:
        print(f"ERROR: {path_to_config}: {e}")

if __name__ == "__main__":
    main()
