from re import split as re_split

def markdown_to_blocks(markdown):
    lst = [m.strip() for m in re_split(r"\n\s*\n",markdown)]
    return list(filter(lambda m: m!="", lst))
