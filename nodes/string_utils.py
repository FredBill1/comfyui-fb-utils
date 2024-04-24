import codecs

from ..node_mappings import register_node


@register_node("FB Multiline String")
class FBMultilineString:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "value": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
        }
    }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    def execute(self, value: str) -> tuple[str]:
        return (value,)


@register_node("FB String Split")
class FBStringSplit:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "value": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
            "delimiter": ("STRING", {"default": ","}),
            "delimiter_as_raw_str": ("BOOLEAN", {"default": False}),
        }
    }
    RETURN_TYPES = ("STRING_LIST",)
    FUNCTION = "execute"

    def execute(self, value: str, delimiter: str, delimiter_as_raw_str: bool) -> tuple[list[str]]:
        if not delimiter_as_raw_str:
            delimiter = codecs.decode(delimiter, "unicode_escape")
        return (value.split(delimiter),)


@register_node("FB String Join")
class FBStringJoin:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "value": ("STRING_LIST", {"default": []}),
            "delimiter": ("STRING", {"default": ","}),
            "delimiter_as_raw_str": ("BOOLEAN", {"default": False}),
        }
    }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    def execute(self, value: list[str], delimiter: str, delimiter_as_raw_str: bool) -> tuple[str]:
        if not delimiter_as_raw_str:
            delimiter = codecs.decode(delimiter, "unicode_escape")
        return (delimiter.join(value),)
