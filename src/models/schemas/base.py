import datetime
import re

from pydantic import BaseModel, Field, field_validator

import pydantic

from src.utilities.formatters.datetime_formatter import (
    format_datetime_into_isoformat,
)
from src.utilities.formatters.field_formatter import (
    format_dict_key_to_camel_case,
)


# The above class is a base schema model in Python that includes various
# configuration options for validation, population, JSON encoding, alias
# generation, and attribute conversion.
class BaseSchemaModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        json_encoders={datetime.datetime: format_datetime_into_isoformat},
        alias_generator=format_dict_key_to_camel_case,
        from_attributes=True,
    )

    @field_validator('username', check_fields=False)
    def phone_number_validate(cls, v: str):
        regex = r"^(254|0)?(7|1)\d{8}$"
        if not re.match(regex, v):
            raise ValueError("Invalid phone number format")
        return v
