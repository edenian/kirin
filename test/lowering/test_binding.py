import inspect

from kirin import lowering
from kirin.prelude import basic_no_opt
from kirin.dialects import math


@lowering.wraps(math.stmts.sin)
def sin(value: float) -> float: ...


@lowering.wraps(math.stmts.sin)
def documented_sin(value: float) -> float:
    """Compute the sine of a floating point value."""


@basic_no_opt
def main(x: float):
    return sin(x)


def test_binding():
    stmt = main.callable_region.blocks[0].stmts.at(0)

    assert isinstance(stmt, math.stmts.sin)


def test_binding_preserves_wrapped_signature():
    assert inspect.signature(sin) == inspect.signature(sin.__wrapped__)
    assert str(inspect.signature(sin)) == "(value: float) -> float"


def test_binding_preserves_wrapped_docstring():
    assert (
        inspect.getdoc(documented_sin) == "Compute the sine of a floating point value."
    )
    assert documented_sin.__doc__ == "Compute the sine of a floating point value."


def test_binding_preserves_wrapped_metadata():
    assert documented_sin.__wrapped__.__name__ == "documented_sin"
    assert documented_sin.__name__ == "documented_sin"
    assert documented_sin.__module__ == documented_sin.__wrapped__.__module__
    assert documented_sin.__annotations__ == documented_sin.__wrapped__.__annotations__
