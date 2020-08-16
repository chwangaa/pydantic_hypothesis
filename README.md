Consider the following pydantic dataclass (see tests/contract.py for full code)

```python
@dataclass
class Contract:
    name: str
    description: str
    contractors: List[str]
    start_date: date
    end_date: date

    @validator("name", "description")
    def name_must_not_be_empty(cls, name):
        pass

    @validator("contractors")
    def must_have_at_least_one_contractor(cls, contractors):
        pass

    @validator("end_date")
    def end_date_must_not_before_start_date(cls, end_date, values):
        pass
```

One can not easily use `hypothesis.from_type(Contractor)` for it given the three validations.

One solution candidate is to code up a customized hypothesis strategies builder for this `Contractor` type, something like this:

```python
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
```

Run it in `tests/test_with_explicit_builder` to see

Another solution will be to just use `from_type` as it is, but add an extra layer so that if one generation fails the validation, try again. e.g.

```python

def from_pydantic_type(type_name):
    x = strategies.from_type(type_name)
    old_do_draw = x.do_draw

    def do_draw(data):
        try:
            return old_do_draw(data)
        except ValueError as e:
            print(e)
            raise UnsatisfiedAssumption()

    x.do_draw = do_draw

    return x

@given(contract=from_pydantic_type(Contract))
def test_with_pydantic_type_syntax(contract):
    pass
```