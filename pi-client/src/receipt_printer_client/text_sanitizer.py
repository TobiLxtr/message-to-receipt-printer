# src/receipt_printer_client/text_sanitizer.py

import re
import emoji


MAX_TEXT_LENGTH = 500 # Maximum total characters allowed in message text
MAX_LINES = 30 # Maximum number of lines allowed in message text
MAX_NAME_LENGTH = 36 # Maximum characters allowed in name field

MAX_EMOJI_REPEAT = 3 # Maximum identical emojis allowed consecutively

# Mapping of specific emojis to ASCII replacements
EMOJI_REPLACEMENTS = {

    # smiles
    "😊": ":)", "😀": ":)", "🙂": ":)", "☺": ":)",

    # laughing
    "😄": ":D", "😁": ":D", "😆": ":D",

    # laughing crying
    "😂": ":'D",

    # sweat laugh
    "😅": "':D",

    # wink
    "😉": ";)",

    # kiss
    "😘": ":*", "😚": ":*", "😙": ":*",

    # neutral
    "😐": ":-|", "😑": ":-|",

    # cool
    "😎": "8-)",

    # sad
    "😓": "':(", "😔": ":(", "😕": ":(", "😞": ":(", "🙁": ":(",

    # crying
    "😢": ":'(", "😥": ":'(", "😭": ":'(",

    # tongue
    "😛": ":P", "😝": ":P",

    # wink tongue
    "😜": ";P",

    # angel
    "😇": "O:-)",

    # upside down
    "🙃": "(:",

    # classic heart symbol
    "♥": "<3",

    # broken heart
    "💔": "</3",
}

# Regex
# Invisible unicode characters (direction markers etc.)
INVISIBLE_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")

# Zero-width characters often present in emoji sequences
ZERO_WIDTH_RE = re.compile(r"[\u200d\ufe0f]")

# Limit excessive line breaks
MULTI_NEWLINE_RE = re.compile(r"\n{4,}")

# Collapse multiple spaces
MULTI_SPACE_RE = re.compile(r"\s{2,}")


def replace_and_limit_emojis(text: str) -> str:
    """
    Replace supported emojis with ASCII equivalents,
    detect heart emojis automatically,
    and limit repeated emojis.

    """

    matches = emoji.emoji_list(text)

    if not matches:
        return text

    result = []
    last_emoji = None
    count = 0
    i = 0
    match_index = 0

    while i < len(text):

        # Check if an emoji starts at this position
        if match_index < len(matches) and matches[match_index]["match_start"] == i:

            e = matches[match_index]["emoji"]

            # Limit repeated identical emojis
            if e == last_emoji:
                count += 1
            else:
                last_emoji = e
                count = 1

            if count <= MAX_EMOJI_REPEAT:

                replacement = None

                # Direct mapping replacement
                if e in EMOJI_REPLACEMENTS:
                    replacement = EMOJI_REPLACEMENTS[e]

                else:
                    # Detect heart emojis automatically
                    data = emoji.EMOJI_DATA.get(e)

                    if data:
                        name = data.get("en", "")

                        if "heart" in name:
                            replacement = "<3"

                # Append replacement with spacing for readability
                if replacement is not None:
                    result.append(replacement + " ")
                else:
                    # Keep placeholder space for removed emoji
                    result.append(" ")

            # Move index past this emoji
            i = matches[match_index]["match_end"]
            match_index += 1

        else:
            result.append(text[i])
            last_emoji = None
            count = 0
            i += 1

    return "".join(result)


def limit_lines(text: str) -> str:
    """
    Limit the maximum number of lines in the text.
    """

    lines = text.splitlines()

    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES]

    return "\n".join(lines)


def sanitize_text(text: str) -> str:
    """
    Sanitize message text before printing.
    """

    if not text:
        return ""

    # Limit excessive line breaks
    text = MULTI_NEWLINE_RE.sub("\n\n\n", text)

    # Limit total text length
    text = text[:MAX_TEXT_LENGTH]

    # Remove invisible unicode characters
    text = INVISIBLE_RE.sub("", text)

    # Remove zero-width emoji helpers
    text = ZERO_WIDTH_RE.sub("", text)

    # Replace and limit emojis
    text = replace_and_limit_emojis(text)

    # Remove any remaining emojis
    text = emoji.replace_emoji(text, replace="")

    # Normalize whitespace
    text = MULTI_SPACE_RE.sub(" ", text)

    # Limit number of lines
    text = limit_lines(text)

    return text.strip()


def sanitize_name(name: str) -> str:
    """
    Sanitize a name field.
    """

    if not name:
        return ""

    # Apply main sanitizer
    name = sanitize_text(name)

    # Remove line breaks
    name = name.replace("\n", " ").replace("\r", " ")

    # Collapse multiple spaces
    name = MULTI_SPACE_RE.sub(" ", name)

    # Trim whitespace
    name = name.strip()

    # Limit name length
    name = name[:MAX_NAME_LENGTH]

    return name