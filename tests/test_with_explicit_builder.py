from tests.contract import Contract
from datetime import date


from hypothesis import given, strategies as st


def get_contract():
    return st.builds(
        Contract,
        name=st.from_regex(".* .*"),
        description=st.from_regex(".* .*"),
        contractors=st.lists(st.text(), min_size=1),
        start_date=st.dates(max_value=date(2010, 12, 31)),
        end_date=st.dates(min_value=date(2011, 1, 1)),
    )


@given(contract=get_contract())
def test_with_explicit_registeration(contract):
    pass
    # testing logic build on top of the given contract
