# Token Counter

A simple, fast, and user-friendly command-line tool to count the number of tokens in a text file. It provides a progress bar for large files and displays the output in a clean, readable format.

This tool uses the `tiktoken` library, which is the same tokenizer used by OpenAI for its large language models.

## Features

-   **Fast Tokenization:** Leverages `tiktoken` for high-performance token counting.
-   **Progress Bar:** A `rich`-powered progress bar shows the status of large files.
-   **Styled Output:** Displays results in a clean, formatted table.
-   **Flexible Encoding Selection:** Choose specific `tiktoken` encodings via a flag or an interactive menu.
-   **Multiple File/Directory Support:** Count tokens across multiple specified files or all supported files within a directory.
-   **Exclusion Patterns:** Exclude files or directories using glob patterns.
-   **File Extension Control:** Override default file extensions or add new ones to customize which files are processed.
-   **LLM Context Limit Comparison:** Compare token counts against common Large Language Model context window limits. These limits are loaded from `src/token_counter/llm_limits.json` and can be customized.
-   **Stdin Support:** Process text piped directly to the tool.
-   **Easy to Use:** Simple command-line interface for quick use.

## Installation & Usage

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd token-counter
    ```

2.  **Install dependencies using `uv`:**

    ```bash
    uv init
    uv add typer rich tiktoken InquirerPy
    uv pip install -e .
    ```

3.  **Run the tool:**

    ```bash
    # Basic usage - count tokens using default 'cl100k_base' encoding
    token-counter my_document.txt

    # Count tokens from stdin
    echo "Your text here" | token-counter

    # Count tokens in multiple files
    token-counter file1.txt file2.md

    # Count tokens in all supported files within a directory
    token-counter my_project_folder/
    ```

## Usage Options

### Model Selection
```bash
# Use a specific encoding model
token-counter my_document.txt --model p50k_base
token-counter my_document.txt -m p50k_base

# Interactively select the encoding from a list
token-counter my_document.txt --select-encoding
token-counter my_document.txt -s
```

### File Extension Control
```bash
# Override default extensions (only process specified extensions)
token-counter my_project_folder/ --extension .xml,.yaml,.toml
token-counter my_project_folder/ -e .xml,.yaml,.toml

# Add new extensions to the default list
token-counter my_project_folder/ --add-extensions .log,.temp
token-counter my_project_folder/ -a .log,.temp
```

### File/Directory Exclusion
```bash
# Exclude specific files or directories using glob patterns
token-counter my_project_folder/ --exclude "*.log" --exclude "node_modules/"
token-counter my_project_folder/ -x "*.log" -x "node_modules/"
```

### LLM Context Limit Comparison
```bash
# Compare token count against common LLM context window limits
token-counter my_long_article.txt --check-limits
token-counter my_long_article.txt -c
```

### Combined Options
```bash
# Complex example combining multiple options
token-counter my_project_folder/ -s -x "*.test.py" -c -e .py,.js

# Process only Python files, exclude tests, and check limits
token-counter . --extension .py --exclude "*test*" --check-limits

# Add log files to processing and use specific model
token-counter logs/ --add-extensions .log --model p50k_base
```

## Complete Option Reference

| Option | Short | Description |
|--------|-------|-------------|
| `--model` | `-m` | Specify the encoding model (e.g., 'cl100k_base', 'p50k_base') |
| `--select-encoding` | `-s` | Interactively select the encoding model from a list |
| `--extension` | `-e` | Override default file extensions (comma-separated) |
| `--add-extensions` | `-a` | Add to default file extensions (comma-separated) |
| `--exclude` | `-x` | Exclude files/directories using glob patterns (repeatable) |
| `--check-limits` | `-c` | Compare token count against LLM context window limits |
| `--help` | | Show help message and exit |

### Examples

    ```bash
    token-counter test_article.txt
    token-counter test_article.txt -m p50k_base
    token-counter test_article.txt -s
    echo "Hello world" | token-counter
    token-counter README.md test_article.txt
    token-counter src/
    token-counter . --exclude "*.md" --exclude "src/"
    token-counter test_article.txt -c
    token-counter . --extension .py,.js
    token-counter . -e .py,.js
    token-counter . --add-extensions .log,.xml
    ```

## Customizing File Extensions

By default, the tool processes files with extensions defined in `src/token_counter/allowed_extensions.json`. You can customize which files are processed using command-line options:

-   **`--extension` or `-e`**: Override the default extensions entirely. Only files with the specified extensions will be processed.
-   **`--add-extensions` or `-a`**: Add new extensions to the default list without removing the existing ones.

If both flags are provided, `--extension` takes precedence and a warning will be displayed.

## Customizing LLM Context Limits

The LLM context window limits are stored in `src/token_counter/llm_limits.json`. You can edit this file to add, remove, or modify the models and their corresponding token limits to suit your needs.

## Adding to PATH

To use the `token-counter` command from anywhere in your system, you need to add the virtual environment's `bin` directory to your shell's `PATH`.

1.  **Get the full path to the `bin` directory:**

    ```bash
    pwd
    # Copy the output and append /.venv/bin to it.
    # For example: /Users/you/token-counter/.venv/bin
    ```

2.  **Add the path to your shell's configuration file:**

    -   For **Bash** (usually `~/.bashrc` or `~/.bash_profile`):

        ```bash
        echo 'export PATH="/path/to/your/project/.venv/bin:$PATH"' >> ~/.bashrc
        source ~/.bashrc
        ```

    -   For **Zsh** (usually `~/.zshrc`):

        ```bash
        echo 'export PATH="/path/to/your/project/.venv/bin:$PATH"' >> ~/.zshrc
        source ~/.zshrc
        ```

    Now you can run `token-counter` from any directory.