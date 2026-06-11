from tree_sitter import Language, Parser
import tree_sitter_python


PY_LANGUAGE = Language(
    tree_sitter_python.language()
)

parser = Parser(
    PY_LANGUAGE
)


def chunk_python_code(code):

    tree = parser.parse(
        bytes(code, "utf8")
    )

    root = tree.root_node

    chunks = []

    for child in root.children:

        if child.type in [
            "function_definition",
            "class_definition"
        ]:

            chunks.append(
                code[
                    child.start_byte:
                    child.end_byte
                ]
            )

    return chunks