def markdown_to_blocks(text):
    splittext = text.split("\n\n")
    # Remove leading and trailing whitespace from each item
    splittext = list(map(lambda s: s.strip(), splittext))
    # Remove empty items that might appear when there are too many newlines between paragraphs
    splittext = list(filter(lambda s: len(s) > 0, splittext))
    return splittext

