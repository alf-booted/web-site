from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(md_block):
    if re.match(r"#{1,6} ",md_block):
        return BlockType.HEADING
    if re.match(r"```\n.*```$",md_block,re.DOTALL):
        return BlockType.CODE
    rows = md_block.split("\n")
    if re.match(r">",md_block):
        if all([re.match(r">",row) for row in rows]):
            return BlockType.QUOTE
    if re.match(r"- ",md_block):
        if all([re.match(r"- ",row) for row in rows]):
            return BlockType.UNORDERED_LIST
    if re.match(r"1\. ",md_block):
        if all([re.match(fr"{i+1}\. ",rows[i]) for i in range(len(rows))]):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

