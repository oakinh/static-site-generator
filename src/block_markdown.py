import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            blocks.remove(block)
        else:
            new_blocks.append(block.strip())
    return new_blocks


def block_to_block_type(markdown_block):
    if (
        markdown_block.startswith("# ")
        or markdown_block.startswith("## ")
        or markdown_block.startswith("### ")
        or markdown_block.startswith("#### ")
        or markdown_block.startswith("##### ")
        or markdown_block.startswith("###### ")
        ):
        return block_type_heading
    elif markdown_block.startswith("```"):
        if not markdown_block.endswith("```"):
            raise ValueError("Invalid markdown, code block must be properly closed")
        return block_type_code
    elif markdown_block.startswith(">"):
        splits = markdown_block.splitlines()
        for split in splits:
            if not split.startswith(">"):
                raise ValueError("Invalid markdown, each line in a quote block must start with a '>' character")
        return block_type_quote
    elif markdown_block.startswith("*") or markdown_block.startswith("-"):
        splits = markdown_block.splitlines()
        for split in splits:
            if not (split.startswith("*") or split.startswith("-")):
                raise ValueError("Invalid markdown, each line in an unordered list block must start with a '*' or '-' character")
        return block_type_unordered_list
    elif markdown_block.startswith("1."):
        splits = markdown_block.splitlines()
        base_pattern = "{}."
        line_number = 0
        for split in splits:
            line_number += 1
            pattern = base_pattern.format(line_number)
            if not bool(re.match(pattern, split)):
                raise ValueError("Invalid markdown, each line in an ordered list must start first with '1.' and increment by 1 thereafter")
        return block_type_ordered_list
    return block_type_paragraph









