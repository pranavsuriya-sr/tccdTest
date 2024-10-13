# Simple C++ Compiler Simulation with Parse Tree Visualization

This is a basic C++ Compiler Simulation built using **Streamlit** for the user interface and **Anytree** for visualizing the parse tree. The program performs lexical analysis, syntax analysis, and semantic analysis on simple C++ code snippets, and generates a binary-like parse tree in the terminal.

## Features

- **Lexical Analysis**: Converts the input C++ code into a sequence of tokens (keywords, operators, identifiers, literals, etc.).
- **Syntax Analysis**: Validates the structure of the input code based on predefined rules (e.g., assignment statements, loops).
- **Semantic Analysis**: Ensures that the input code is semantically correct (e.g., correct variable types and assignments).
- **Parse Tree Visualization**: Displays a binary-like parse tree structure based on the code's tokens and syntactic structure.

## How It Works

### 1. Lexical Analysis
The input code is broken into lexemes, and each lexeme is classified into a token type (e.g., `KEYWORD`, `ASSIGNMENT_OPERATOR`, `IDENTIFIER`, `INTEGER_LITERAL`, etc.).

### 2. Syntax Analysis
Checks the sequence of tokens against C++ syntax rules, such as variable declarations, assignments, and loops.

### 3. Semantic Analysis
Verifies the semantic correctness, such as ensuring the correct type of values being assigned to variables (e.g., integer to `int`).

### 4. Parse Tree
Generates and visualizes a parse tree representing the structure of the code. The tree is shown as a text-based hierarchical tree in the Streamlit app.

## Example

Input Code:
```cpp
int x = 5;
