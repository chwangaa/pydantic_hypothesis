from datetime import date
from typing import List

from pydantic import validator
from pydantic.dataclasses import dataclass


@dataclass
class Contract:
    name: str
    description: str
    contractors: List[str]
    start_date: date
    end_date: date

    @validator("name", "description")
    def name_must_not_be_empty(cls, name):
        if name == "":
            raise ValueError("name cannot be empty")
        return name

    @validator("contractors")
    def must_have_at_least_one_contractor(cls, contractors):
        if len(contractors) == 0:
            raise ValueError("must have at least one contractor")
        return contractors

    @validator("end_date")
    def end_date_must_not_before_start_date(cls, end_date, values):
        start_date = values.get("start_date", None)
        if start_date is not None and end_date is not None:
            if end_date < start_date:
                raise ValueError("maturity date must not before start date")
        return end_date
