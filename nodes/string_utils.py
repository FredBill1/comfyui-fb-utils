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


@register_node("FB Multiline String List")
class FBMultilineStringList:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "value": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
        }
    }
    RETURN_TYPES = ("STRING_LIST",)
    FUNCTION = "execute"

    def execute(self, value: str) -> tuple[list[str]]:
        return ([line.strip() for line in value.split("\n")],)


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


@register_node("FB String Replace")
class FBStringReplace:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "value": ("STRING", {"forceInput": True}),
            "olds": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
            "news": ("STRING", {"default": "", "multiline": True, "dynamicPrompts": False}),
            "recursive": ("BOOLEAN", {"default": True}),
        }
    }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    def execute(self, value: str, olds: str, news: str, recursive: bool) -> tuple[str]:
        olds = [line for line in olds.split("\n")]
        news = [line for line in news.split("\n")]
        assert len(olds) == len(news), "The number of old and new strings must be the same."
        while True:
            old_value = value
            for old, new in zip(olds, news):
                value = value.replace(old, new)
            if not (recursive and old_value != value):
                break
        return (value,)


@register_node("FB String Strip")
class FBStringStrip:
    CATEGORY = "FredBill1"
    INPUT_TYPES = lambda: {
        "required": {
            "value": ("STRING", {"forceInput": True}),
            "chars": ("STRING", {"default": ""}),
            "chars_as_raw_str": ("BOOLEAN", {"default": False}),
            "left": ("BOOLEAN", {"default": True}),
            "right": ("BOOLEAN", {"default": True}),
        }
    }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    def execute(self, value: str, chars: str, chars_as_raw_str: bool, left: bool, right: bool) -> tuple[str]:
        if chars and not chars_as_raw_str:
            chars = codecs.decode(chars, "unicode_escape")
        if not chars:
            chars = None
        if left and right:
            value = value.strip(chars)
        elif left:
            value = value.lstrip(chars)
        elif right:
            value = value.rstrip(chars)
        return (value,)
