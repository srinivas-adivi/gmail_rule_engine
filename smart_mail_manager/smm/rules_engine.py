from datetime import datetime, timedelta

import smm.data_models
import smm.lib


class Rule:
    def __init__(self, field, predicate, value):
        self.field = field
        self.predicate = predicate
        self.value = value

    def criteria(self, db_model):
        fields = smm.data_models.GmailMessageSchema.model_fields
        db_field, field_type = next((key, value.annotation.__name__)
                                    for key, value in fields.items()
                                    if value.alias == self.field)
        print(f"{field_type}, {db_field}")
        if field_type == "str":
            return self._string_criteria(db_model, db_field)
        elif field_type == "datetime":
            return self._date_criteria(db_model, db_field)

    def _string_criteria(self, db_model, db_field):
        predicate = self.predicate.lower()
        if predicate == "contains":
            print(f"{getattr(db_model, db_field).like(f'%{self.value}')}"
                  f" {self.value}")
            return getattr(db_model, db_field).like(f"%{self.value}%")
        elif predicate == "does not contains":
            print(f"{getattr(db_model, db_field).notlike(f'%{self.value}')}"
                  f" {self.value}")
            return getattr(db_model, db_field).notlike(f"%{self.value}%")
        elif predicate == "equals":
            return getattr(db_model, db_field) == self.value
        elif predicate == "does not equals":
            return not getattr(db_model, db_field) == self.value

        return None

    def _date_criteria(self, db_model, db_field):

        result, msg = smm.lib.validate_and_extract(self.value)
        if result:
            if len(result) == 2:
                days, months = result
            else:
                days, months = result[0], 0

            rule_date = datetime.now() - timedelta(days=(days + months*30))

            predicate = self.predicate.lower()
            if rule_date:
                print(f"{predicate} {rule_date}")
                if predicate == "is less than":
                    return getattr(db_model, db_field) < rule_date
                elif predicate == "is greater than":

                    return getattr(db_model, db_field) > rule_date
        else:
            print(f"date criteria: {msg}")

        return None


class RuleEngine:
    def __init__(self, conditions, predicate="All"):
        self.rules = conditions
        self.predicate = predicate

    def criteria(self, db_model):
        result = [rule.criteria(db_model) for rule in self.rules]
        return result
