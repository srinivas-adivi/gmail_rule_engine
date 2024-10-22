import os.path
import json

from sqlalchemy import and_, or_
import yaml

import smm.data_models
import smm.provider
import smm.serializer
import smm.rules_engine
import db_lib


def read_rules(path_to_rules):
    if not os.path.exists(path_to_rules):
        raise ValueError(f"rules file not found: `{path_to_rules}`")

    with open(path_to_rules) as of:
        rules_content = json.load(of) or {}
        rules_info = smm.data_models.Rules(**rules_content)
        return rules_info

def read_config(path_to_config):
    if not os.path.exists(path_to_config):
        raise ValueError(f"configuration file not found: `{path_to_config}`")

    with open(path_to_config) as of:
        config_content = yaml.safe_load(of.read()) or {}
        config_info = smm.data_models.Config(**config_content)
        return config_info

def main(path_to_config='config.yaml', path_to_rules='rules.json'):
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

            provider = smm.provider.EmailServiceProvider(service_name, service_config)

        rules_info = read_rules(path_to_rules)
        if rules_info:
            rules = rules_info.rules or []

            for rule_info in rules:
                conditions_info = rule_info.conditions
                predicate = rule_info.predicate
                actions_info = rule_info.actions

                print(f"{conditions_info}, \n {predicate}, \n{actions_info}")

                conditions = [smm.rules_engine.Rule(**condition.model_dump())
                              for condition in conditions_info]

                # Initialize RuleEngine
                rule_engine = smm.rules_engine.RuleEngine(conditions, predicate)

                query = db_lib.session.query(db_lib.Message)
                if predicate == 'All':
                    filters = and_(*rule_engine.criteria(db_lib.Message))
                else:
                    filters = or_(*rule_engine.criteria(db_lib.Message))

                query = query.filter(filters)
                emails = query.all()
                rule_executor = provider.get_rule_executor()
                for email in emails:
                    print(f"{email.sender}, {email.received_date}")
                    rule_executor.apply_actions(email.msg_id, actions_info)

    except ValueError as e:
        print(f"ERROR: {path_to_rules}: {e}")

if __name__ == "__main__":
    main()
