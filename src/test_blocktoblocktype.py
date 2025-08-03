import unittest
from markdowntoblocks import markdown_to_blocks
from blocktoblocktype import block_to_blocktype, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_ideal_case(self):
        example = """### This is the heading of an example document

## Section 1

This is an example of a markdown document, for the purpose of testing.

## Section 2

Following is an example of a code block.

```Some code
blablabla
etc```

Following is an example of an unordered list.

- list item 1
- list item 2
- list item 3

Following is an example of an ordered list.

1. list item 1
2. list item 2
3. list item 3

## A quote from poetry

> Leaves are falling
> western winds are blowing
> always remember."""
        blocks = markdown_to_blocks(example)
        blocktypes = list(map(block_to_blocktype, blocks))
        self.assertListEqual(blocktypes, [BlockType.HEADING,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.CODE,
                                      BlockType.PARAGRAPH,
                                      BlockType.UNORDERED_LIST,
                                      BlockType.PARAGRAPH,
                                      BlockType.ORDERED_LIST,
                                      BlockType.HEADING,
                                      BlockType.QUOTE])
    def test_incorrect_case(self):
        example = """### This is the heading of an example document

## Section 1

This is an example of a markdown document, for the purpose of testing.

## Section 2

Following is an example of a code block.

```Some code
blablabla
etc```and some more text

Following is an example of an unordered list.

- list item 1
-list item 2
- list item 3

Following is an example of an ordered list.

1. list item 1
2 list item 2
3. list item 3

## A quote from poetry

Leaves are falling
> western winds are blowing
> always remember."""
        blocks = markdown_to_blocks(example)
        blocktypes = list(map(block_to_blocktype, blocks))
        self.assertListEqual(blocktypes, [BlockType.HEADING,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.PARAGRAPH,
                                      BlockType.HEADING,
                                      BlockType.PARAGRAPH])