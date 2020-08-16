from hypothesis import strategies
from hypothesis.errors import UnsatisfiedAssumption


def from_pydantic_type(type_name):
    """
    Returns a strategy that guarantees to generate a instance that passes the pydantic validation

    if the type strategy generate some raw data which cannot be used to parse
    a valid pydantic dataclass, re-try the strategy by raising a
    UnsatisfiedAssumption
    """
    x = strategies.from_type(type_name)
    old_do_draw = x.do_draw

    def do_draw(data):
        try:
            return old_do_draw(data)
        # this naive implementation is based on the assumption that all
        # validation error should raise ValueError
        # which is advised by the pydantic official doc
        except ValueError as e:
            print(e)
            raise UnsatisfiedAssumption()

    x.do_draw = do_draw

    return x
