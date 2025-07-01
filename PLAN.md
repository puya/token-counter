# Token Counter CLI - Plan & TODOs

## 1. Project Goal

To create a user-friendly command-line interface (CLI) tool in Python that counts the number of tokens in a given text file. The tool should provide progress feedback and present the final count in a visually appealing format.

## 2. Core Features

- Count tokens from a specified file path.
- Display a progress bar while processing the file.
- Output the total token count, file path, and other relevant info in a styled table.
- Handle potential errors gracefully (e.g., file not found).
- Use a standard, efficient tokenization library.

## 3. Technology Stack

- **Language:** Python 3
- **Package/Venv Management:** `uv`
- **CLI Framework:** `typer`
- **Styled Output & Progress:** `rich`
- **Tokenization:** `tiktoken`

## 4. Project Structure

```
token-counter/
├── .gitignore
├── PLAN.md
├── pyproject.toml
├── README.md
└── src/
    └── token_counter/
        ├── __init__.py
        ├── main.py          # CLI logic using typer and rich
        └── counter.py       # Core token counting functionality
```

## 5. Development Plan & TODOs

- [ ] **1. Setup Project Environment**
    - [ ] Initialize `pyproject.toml` for the project.
    - [ ] Add dependencies: `typer`, `rich`, `tiktoken`.
    - [ ] Create the basic directory structure (`src/token_counter`).

- [ ] **2. Implement Core Logic**
    - [ ] Create `src/token_counter/counter.py`.
    - [ ] Implement a function to read a file and count tokens using `tiktoken`.
    - [ ] The function should be efficient for large files (e.g., reading in chunks).

- [ ] **3. Build the CLI**
    - [ ] Create `src/token_counter/main.py`.
    - [ ] Set up a `typer` application.
    - [ ] Add a CLI command that accepts a file path as an argument.
    - [ ] Integrate the `rich` library for progress tracking (e.g., `rich.progress`).
    - [ ] Call the core counting logic from `counter.py`.

- [ ] **4. Refine Output & UX**
    - [ ] Use `rich.table.Table` to display the final results neatly.
    - [ ] Include: File Path, Token Count, and maybe model/encoding used.
    - [ ] Implement robust error handling (e.g., `FileNotFoundError`) with user-friendly `rich`-styled error messages.

- [ ] **5. Documentation**
    - [ ] Create a `README.md` with installation and usage instructions.
    - [ ] Add a `.gitignore` file.

- [ ] **6. (Optional) Enhancements**
    - [ ] Add an option to specify the `tiktoken` encoding model.
    - [ ] Allow reading from `stdin` so text can be piped to the tool.
    - [ ] Add support for counting tokens in multiple files or directories.
