import streamlit as st
from anytree import Node, RenderTree, AsciiStyle

TOKENS = {
    'int': 'KEYWORD',
    'float': 'KEYWORD',
    '=': 'ASSIGNMENT_OPERATOR',
    ';': 'TERMINATOR',
    '(': 'LEFT_PARENTHESIS',
    ')': 'RIGHT_PARENTHESIS',
    '{': 'LEFT_BRACE',
    '}': 'RIGHT_BRACE',
    '<': 'LESS_THAN_OPERATOR',
    '>': 'GREATER_THAN_OPERATOR',
    'for': 'KEYWORD',
    'if': 'KEYWORD',
    'else': 'KEYWORD',
    '+': 'ADD_OPERATOR',
    '-': 'SUB_OPERATOR',
    '*': 'MUL_OPERATOR',
    '/': 'DIV_OPERATOR',
    'i': 'IDENTIFIER',
    'x': 'IDENTIFIER',
    '5': 'INTEGER_LITERAL',
    '0': 'INTEGER_LITERAL'
}

def lexical_analysis(code):
    tokens = []
    words = code.replace('(', ' ( ').replace(')', ' ) ').replace(';', ' ; ').replace('<', ' < ').replace('>', ' > ').split()
    
    for word in words:
        token_type = TOKENS.get(word, 'IDENTIFIER')
        tokens.append((word, token_type))
    
    return tokens

def syntax_analysis(tokens):
    if tokens[0][1] == 'KEYWORD' and tokens[1][1] == 'IDENTIFIER' and tokens[2][1] == 'ASSIGNMENT_OPERATOR':
        return "Valid Syntax"
    elif tokens[0][0] == 'for':
        return "Valid for-loop Syntax"
    else:
        return "Syntax Error"


def semantic_analysis(tokens):
    if tokens[0][0] == 'int' and tokens[1][1] == 'IDENTIFIER' and tokens[3][1] == 'INTEGER_LITERAL':
        return "Semantically Correct: Integer assignment"
    elif tokens[0][0] == 'for':
        return "Semantically Correct: for-loop"
    else:
        return "Semantic Error"

def generate_parse_tree(tokens):
    root = Node("Program")
    if tokens[0][0] == "int":
        var_decl = Node("Declaration", parent=root)
        type_node = Node(f"Type: {tokens[0][0]}", parent=var_decl)
        id_node = Node(f"Identifier: {tokens[1][0]}", parent=type_node)
        assign_node = Node(f"Assignment Operator: {tokens[2][0]}", parent=id_node)
        value_node = Node(f"Value: {tokens[3][0]}", parent=assign_node)
        terminator_node = Node(f"Terminator: {tokens[4][0]}", parent=value_node)
    elif tokens[0][0] == "for":
        loop_decl = Node("For Loop", parent=root)
        keyword_node = Node(f"Keyword: {tokens[0][0]}", parent=loop_decl)
        condition_node = Node("Condition", parent=keyword_node)
        init_node = Node(f"Initialization: {tokens[2][0]}={tokens[4][0]}", parent=condition_node)
        cond_node = Node(f"Condition: {tokens[6][0]} < {tokens[8][0]}", parent=condition_node)
    
    return root


def compile_code(code):
    st.subheader("Lexical Analysis")
    tokens = lexical_analysis(code)
    for token in tokens:
        st.write(f"Lexeme: {token[0]} - Token: {token[1]}")
    
    st.subheader("Syntax Analysis")
    syntax_result = syntax_analysis(tokens)
    st.write(syntax_result)
    
    st.subheader("Semantic Analysis")
    semantic_result = semantic_analysis(tokens)
    st.write(semantic_result)
    
    st.subheader("Parse Tree")
    root = generate_parse_tree(tokens)
    for pre, _, node in RenderTree(root, style=AsciiStyle()):
        st.text(f"{pre}{node.name}")


st.title("Simple C++ Compiler Simulation with Binary-like Parse Tree")

code_input = st.text_area("Enter your C++ code snippet:", "int x = 5;")

if st.button("Compile"):
    compile_code(code_input)
