

def extract_title(markdown):
    markdown_rows = markdown.split("\n")
    for row in markdown_rows:
        if row[0] == "#"
        return row
    raise Exception("No h1 header found. All pages need a single h1 header")