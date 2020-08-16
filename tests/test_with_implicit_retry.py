from tests.contract import Contract

from hypothesis_pydantic.from_pydantic_type import from_pydantic_type
from hypothesis import given


@given(contract=from_pydantic_type(Contract))
def test_with_pydantic_type_syntax(contract):
    pass
