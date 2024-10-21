import clang.cindex as clang
import json
import uuid
import re
import pydot
from IPython.display import Image, display


# ~~~~~~~~~~~~~~~~~~ PARSING C++ AST TO JSON ~~~~~~~~~~~~~~~~~~


def parse_cpp_code(code):
    """Parse C++ code using Clang to create an AST."""
    index = clang.Index.create()
    tu = index.parse('temp.cpp', args=['-std=c++11'], unsaved_files=[('temp.cpp', code)])
    return tu.cursor


def json_cpp_ast(cursor):
    """Recursively parse a Clang cursor into JSON."""
    def node_to_dict(node):
        result = {"kind": node.kind.name, "spelling": node.spelling, "location": str(node.location)}
        result['children'] = [node_to_dict(c) for c in node.get_children()]
        return result

    return json.dumps(node_to_dict(cursor), indent=4)


# ~~~~~~~~~~~~~~~~~~~~~~~~ DRAWING AST ~~~~~~~~~~~~~~~~~~~~~~~~~


def grapher(graph, ast_nodes, parent_node="", node_hash="__init__"):
    """Recursively parse JSON-AST object into a tree."""
    if isinstance(ast_nodes, dict):
        for key, node in ast_nodes.items():
            if not parent_node:
                parent_node = node
                continue
            if key == "kind":
                node = graph_detail(node, ast_nodes)  # get node detail for graph
                node_hash = draw(parent_node, node, graph=graph, parent_hash=node_hash)
                parent_node = node  # once a child, now parent
                continue
            # parse recursively
            if isinstance(node, dict):
                grapher(graph, node, parent_node=parent_node, node_hash=node_hash)
            if isinstance(node, list):
                [
                    grapher(graph, item, parent_node=parent_node, node_hash=node_hash)
                    for item in node
                ]


def graph_detail(value, ast_scope):
    """Retrieve node details for C++ AST nodes."""
    detail_keys = ("spelling", "location")
    for key in detail_keys:
        if not isinstance(ast_scope.get(key), type(None)):
            value = f"{value}\n{key}: {ast_scope[key]}"

    return value


def clean_node(method):
    """Decorator to eliminate illegal characters, check type, and
    shorten lengthy child and parent nodes."""
    def wrapper(*args, **kwargs):
        parent_name, child_name = tuple(
            "_node" if node == "node" else node for node in args
        )
        illegal_char = re.compile(r"[,\\/]$")  # Remove illegal chars from node names
        illegal_char.sub("*", child_name)
        if not child_name:
            return
        if len(child_name) > 2500:
            child_name = "~~~DOCS: too long to fit on graph~~~"
        args = (parent_name, child_name)

        return method(*args, **kwargs)

    return wrapper


@clean_node
def draw(parent_name, child_name, graph, parent_hash):
    """Draw parent and child nodes. Create and return new hash
    key declared to a child node."""
    parent_node = pydot.Node(parent_hash, label=parent_name, shape="box")
    child_hash = str(uuid.uuid4())  # create hash key
    child_node = pydot.Node(child_hash, label=child_name, shape="box")

    graph.add_node(parent_node)
    graph.add_node(child_node)
    graph.add_edge(pydot.Edge(parent_node, child_node))

    return child_hash


# For Jupyter notebooks
def view_tree(pdot):
    """Display the tree in the notebook."""
    tree = Image(pdot.create_png())
    display(tree)


# ~~~~~~~~~~~~~~~~~~~~~~~~ MAIN FUNCTION ~~~~~~~~~~~~~~~~~~~~~~~~~


def main():
    """Take user input and draw a C++ AST. Save file as PNG."""
    graph = pydot.Dot(
        graph_type="digraph",
        strict=True,
        constraint=True,
        concentrate=True,
        splines="polyline",
    )
    cpp_code = input("Input C++ code:\n")

    ast_cursor = parse_cpp_code(cpp_code)
    ast_json = json_cpp_ast(ast_cursor)

    print("JSON AST:\n", ast_json)

    grapher(graph, json.loads(ast_json))

    if graph.write_png("cpp_astree.png"):
        print("C++ AST graph created successfully.")


if __name__ == "__main__":
    main()
