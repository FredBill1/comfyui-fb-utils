from ..node_mappings import register_node
from ..core.types import any

INPUT_COUNT = 8
OUTPUT_COUNT = 8

RETURN_VALUES = "\n".join(f'        "o{i}": i{i},' for i in range(OUTPUT_COUNT))
TEMPLATE = f"""\
def func(*, {", ".join(f"i{i}" for i in range(INPUT_COUNT))}, **kwargs) -> dict:
    return {{
{RETURN_VALUES}
    }}
"""


@register_node("FB Custom Function")
class FBCustomFunction:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "func": ("STRING", {"default": TEMPLATE, "multiline": True, "dynamicPrompts": False}),
        },
        "optional": {f"i{i}": (any,) for i in range(INPUT_COUNT)},
    }
    RETURN_TYPES = tuple(any for _ in range(OUTPUT_COUNT))
    RETURN_NAMES = tuple(f"o{i}" for i in range(OUTPUT_COUNT))
    FUNCTION = "execute"

    def execute(self, func: str, **kwargs) -> tuple:
        kwargs = kwargs.copy()
        for i in range(INPUT_COUNT):
            kwargs.setdefault(f"i{i}", None)

        holder = {}
        exec(func, holder)
        result: dict = holder["func"](**kwargs)
        return tuple(result.get(f"o{i}", None) for i in range(OUTPUT_COUNT))
