from pydantic import BaseModel, ConfigDict, field_validator

class BaseDto(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )
    @field_validator("*", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        return None if v == "" else v
