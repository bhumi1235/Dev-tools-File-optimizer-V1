import re


def chunk_markdown(text):

    pattern = r'^(#+)\s+(.*)$'

    lines = text.splitlines()

    chunks = []

    current_heading = None
    current_content = []

    for line in lines:

        match = re.match(pattern, line)

        if match:

            if current_heading and current_content:

                content = "\n".join(current_content).strip()

                if len(content.split()) >= 5:

                    chunks.append({
                        "heading": current_heading,
                        "content": content
                    })

            current_heading = match.group(2)
            current_content = []

        else:

            if line.strip():
                current_content.append(line)

    if current_heading and current_content:

        content = "\n".join(current_content).strip()

        if len(content.split()) >= 5:

            chunks.append({
                "heading": current_heading,
                "content": content
            })

    return chunks