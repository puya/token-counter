# Token Counter

A simple, fast, and user-friendly command-line tool to count the number of tokens in a text file. It provides a progress bar for large files and displays the output in a clean, readable format.

This tool uses the `tiktoken` library, which is the same tokenizer used by OpenAI for its large language models.

## Features

-   **Fast Tokenization:** Leverages `tiktoken` for high-performance token counting.
-   **Progress Bar:** A `rich`-powered progress bar shows the status of large files.
-   **Styled Output:** Displays results in a clean, formatted table.
-   **Flexible Encoding Selection:** Choose specific `tiktoken` encodings via a flag or an interactive menu.
-   **Multiple File/Directory Support:** Count tokens across multiple specified files or all supported files within a directory.
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
    # Count tokens using the default 'cl100k_base' encoding
    token-counter my_document.txt

    # Count tokens using a specific encoding (e.g., 'p50k_base')
    token-counter my_document.txt --encoding p50k_base

    # Interactively select the encoding from a list
    token-counter my_document.txt --select-encoding
    # or
    token-counter my_document.txt -s

    # Count tokens from stdin
    echo "Your text here" | token-counter

    # Count tokens in multiple files
    token-counter file1.txt file2.md

    # Count tokens in all supported files within a directory
    token-counter my_project_folder/
    ```

    For example:

    ```bash
    token-counter test_article.txt
    token-counter test_article.txt -e p50k_base
    token-counter test_article.txt -s
    echo "Hello world" | token-counter
    token-counter README.md test_article.txt
    token-counter src/
    ```

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