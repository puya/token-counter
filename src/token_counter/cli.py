import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from typing import Optional, List
import sys
import os
from pathlib import Path
import fnmatch
import json

from token_counter.counter import count_tokens

app = typer.Typer()
console = Console()

ENCODING_OPTIONS = {
    "cl100k_base": "Used by GPT-4, GPT-3.5-Turbo, text-embedding-ada-002",
    "p50k_base": "Used by CodeX models, text-davinci-002, text-davinci-003",
    "r50k_base": "Used by GPT-3 models like davinci (older)",
    "gpt2": "Used by GPT-2 models (older)",
}

LLM_LIMITS = {}
FILE_EXTENSIONS = ()

try:
    with open(Path(__file__).parent / "config" / "llm_limits.json", "r") as f:
        LLM_LIMITS = json.load(f)
except FileNotFoundError:
    console.print("[bold red]Error:[/] llm_limits.json not found. LLM limit comparison will not be available.", style="bold")
except json.JSONDecodeError:
    console.print("[bold red]Error:[/] Could not decode llm_limits.json. LLM limit comparison will not be available.", style="bold")

try:
    with open(Path(__file__).parent / "config" / "allowed_extensions.json", "r") as f:
        FILE_EXTENSIONS = tuple(json.load(f).get("default_extensions", []))
except FileNotFoundError:
    console.print("[bold red]Error:[/] allowed_extensions.json not found. Defaulting to a limited set of file extensions.", style="bold")
    FILE_EXTENSIONS = ('.txt', '.md', '.py', '.js', '.ts', '.json', '.html', '.css', '.log')
except json.JSONDecodeError:
    console.print("[bold red]Error:[/] Could not decode allowed_extensions.json. Defaulting to a limited set of file extensions.", style="bold")
    FILE_EXTENSIONS = ('.txt', '.md', '.py', '.js', '.ts', '.json', '.html', '.css', '.log')

def is_excluded(path: str, exclude_patterns: List[str]) -> bool:
    """Checks if a path matches any of the exclusion patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        # Handle directory patterns like 'node_modules/'
        if pattern.endswith('/') and fnmatch.fnmatch(path + '/', pattern):
            return True
    return False

def format_number_with_separators(num: int) -> str:
    """Format number with thousand separators (commas)."""
    return f"{num:,}"

def format_number_compact(num: int) -> str:
    """Format number in compact form using K/M suffixes for better readability."""
    if num >= 1_000_000:
        if num % 1_000_000 == 0:
            return f"{num // 1_000_000}M"
        else:
            return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        if num % 1_000 == 0:
            return f"{num // 1_000}K"
        else:
            return f"{num / 1_000:.1f}K"
    else:
        return str(num)

def group_models_by_provider(llm_limits: dict) -> dict:
    """Group models by their providers for organized output."""
    providers = {
        "OpenAI": [],
        "Anthropic": [],
        "Google": [],
        "Meta": [],
        "xAI": [],
        "Mistral": [],
        "Cohere": []
    }
    
    for model, limit in llm_limits.items():
        model_lower = model.lower()
        if model_lower.startswith('gpt'):
            providers["OpenAI"].append((model, limit))
        elif model_lower.startswith('claude'):
            providers["Anthropic"].append((model, limit))
        elif model_lower.startswith('gemini'):
            providers["Google"].append((model, limit))
        elif model_lower.startswith('llama'):
            providers["Meta"].append((model, limit))
        elif model_lower.startswith('grok'):
            providers["xAI"].append((model, limit))
        elif model_lower.startswith('mistral'):
            providers["Mistral"].append((model, limit))
        elif model_lower.startswith('command'):
            providers["Cohere"].append((model, limit))
    
    # Remove empty providers
    return {provider: models for provider, models in providers.items() if models}

def discover_extensions_in_directory(directory_path: str, max_files: int = 1000, recursive: bool = False) -> List[str]:
    """Discover all unique file extensions in a directory."""
    extensions = set()
    file_count = 0
    try:
        directory = Path(directory_path)
        if not directory.is_dir():
            return []
        
        if recursive:
            # Recursive scan using os.walk
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = Path(root) / filename
                    if file_path.suffix:
                        extensions.add(file_path.suffix.lower())
                        file_count += 1
                        # Safety limit to prevent processing too many files
                        if file_count > max_files:
                            console.print(f"[bold yellow]Warning:[/] Stopped after scanning {max_files} files in {directory_path}")
                            return sorted(list(extensions))
        else:
            # Non-recursive scan
            for file_path in directory.iterdir():
                if file_path.is_file() and file_path.suffix:
                    extensions.add(file_path.suffix.lower())
                    file_count += 1
                    # Safety limit to prevent processing too many files
                    if file_count > max_files:
                        console.print(f"[bold yellow]Warning:[/] Stopped after scanning {max_files} files in {directory_path}")
                        break
        
        return sorted(list(extensions))
    except (OSError, PermissionError):
        return []

@app.command()
def main(
    paths: Optional[List[str]] = typer.Argument(None, help="One or more file paths or directory paths to count tokens in. If not provided, reads from stdin."),
    model: Optional[str] = typer.Option(
        None, 
        "--model", 
        "-m", 
        help="Specify the encoding model (e.g., 'cl100k_base')."
    ),
    select_encoding: bool = typer.Option(
        False, 
        "--select-encoding", 
        "-s", 
        help="Interactively select the encoding model from a list."
    ),
    exclude: Optional[List[str]] = typer.Option(
        None, 
        "--exclude", 
        "-x", 
        help="Glob patterns to exclude files/directories (e.g., '*.log', 'node_modules/'). Can be used multiple times."
    ),
    check_limits: bool = typer.Option(
        False, 
        "--check-limits", 
        "-c", 
        help="Compare the token count against common LLM context window limits."
    ),
    extension: Optional[List[str]] = typer.Option(
        None, 
        "--extension", 
        "-e", 
        help="""Comma-separated list of file extensions to include (e.g., '.xml,.yaml'). This will override the default allowed extensions."""
    ),
    add_extensions: Optional[List[str]] = typer.Option(
        None, 
        "--add-extensions", 
        "-a", 
        help="""Comma-separated list of file extensions to add to the default allowed extensions (e.g., '.log,.temp'). Use '*' to discover all extensions in the target directory."""
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively scan subdirectories when processing directories."
    )
):
    """Counts the tokens in text files or stdin and displays the result."""

    selected_encoding = "cl100k_base" # Default encoding

    if select_encoding:
        encoding_choices = [
            {"name": f"{name} - {desc}", "value": name}
            for name, desc in ENCODING_OPTIONS.items()
        ]
        selected_encoding = inquirer.select(
            message="Select an encoding model:",
            choices=encoding_choices,
            default="cl100k_base",
            validate=EmptyInputValidator(),
            qmark="[?]",
            pointer="->",
        ).execute()
    elif model is not None:
        selected_encoding = model # Use the provided model value

    files_to_process = []
    exclude_patterns = exclude or []
    
    current_file_extensions = list(FILE_EXTENSIONS) # Start with a mutable list of default extensions
    
    if extension and add_extensions:
        console.print("[bold yellow]Warning:[/] Both --extension and --add-extensions were provided. --extension will take precedence.", style="bold")
        # Process --extension as it takes precedence
        processed_extensions = []
        for ext_arg in extension:
            processed_extensions.extend([e.strip() if e.strip().startswith('.') else '.' + e.strip() for e in ext_arg.split(',')])
        current_file_extensions = processed_extensions
    elif extension:
        processed_extensions = []
        for ext_arg in extension:
            processed_extensions.extend([e.strip() if e.strip().startswith('.') else '.' + e.strip() for e in ext_arg.split(',')])
        current_file_extensions = processed_extensions
    elif add_extensions:
        processed_extensions = []
        for ext_arg in add_extensions:
            # Handle wildcard for auto-discovery
            if ext_arg.strip() == '*':
                # Discover extensions from target directories
                if paths:
                    for path in paths:
                        path_obj = Path(path)
                        if path_obj.is_dir():
                            discovered = discover_extensions_in_directory(str(path_obj), recursive=recursive)
                            processed_extensions.extend(discovered)
                            if discovered:
                                recursive_msg = " (recursive)" if recursive else ""
                                console.print(f"[bold green]Discovered extensions in {path}{recursive_msg}:[/] {', '.join(discovered)}")
                        elif path_obj.parent.is_dir():
                            # If it's a file, discover from its parent directory
                            discovered = discover_extensions_in_directory(str(path_obj.parent), recursive=False)
                            processed_extensions.extend(discovered)
                            if discovered:
                                console.print(f"[bold green]Discovered extensions in {path_obj.parent}:[/] {', '.join(discovered)}")
                else:
                    # If no paths provided, discover from current directory
                    console.print("[bold yellow]Warning:[/] Using wildcard (*) without specifying a path will scan the current directory.")
                    discovered = discover_extensions_in_directory(".", recursive=recursive)
                    processed_extensions.extend(discovered)
                    if discovered:
                        recursive_msg = " (recursive)" if recursive else ""
                        console.print(f"[bold green]Discovered extensions in current directory{recursive_msg}:[/] {', '.join(discovered)}")
                        # Show a warning if many extensions were found
                        if len(discovered) > 10:
                            console.print(f"[bold yellow]Warning:[/] Found {len(discovered)} different extensions. This may process many files.")
            else:
                # Handle regular extension list
                processed_extensions.extend([e.strip() if e.strip().startswith('.') else '.' + e.strip() for e in ext_arg.split(',')])
        current_file_extensions.extend(processed_extensions)

    current_file_extensions = tuple(sorted(list(set(current_file_extensions)))) # Remove duplicates and convert to tuple

    if paths:
        for p in paths:
            path_obj = Path(p)
            if path_obj.is_file():
                if not is_excluded(str(path_obj), exclude_patterns):
                    if path_obj.suffix in current_file_extensions:
                        files_to_process.append(str(path_obj))
            elif path_obj.is_dir():
                if recursive:
                    # Recursive directory traversal
                    for root, dirs, filenames in os.walk(path_obj):
                        # Filter out excluded directories from traversal
                        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclude_patterns)]
                        for filename in filenames:
                            file_full_path = os.path.join(root, filename)
                            if not is_excluded(file_full_path, exclude_patterns): # Exclude files
                                if Path(file_full_path).suffix in current_file_extensions:
                                    files_to_process.append(file_full_path)
                else:
                    # Non-recursive: only scan the immediate directory
                    try:
                        for file_path in path_obj.iterdir():
                            if file_path.is_file():
                                file_full_path = str(file_path)
                                if not is_excluded(file_full_path, exclude_patterns):
                                    if file_path.suffix in current_file_extensions:
                                        files_to_process.append(file_full_path)
                    except (OSError, PermissionError):
                        console.print(f"[bold red]Error:[/] Permission denied or error accessing directory: [cyan]{path_obj}[/cyan]", style="bold")
            else:
                console.print(f"[bold red]Error:[/] Path not found or not a file/directory: [cyan]{p}[/cyan]", style="bold")
                raise typer.Exit(code=1)
    else:
        if not sys.stdin.isatty(): # Check if stdin is being piped
            text_content = sys.stdin.read()
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task(f"[cyan]Processing stdin[/cyan]", total=None)
                token_count = count_tokens(text_content=text_content, progress=progress, task_id=task, encoding_name=selected_encoding)
            
            table = Table(title="Token Count Result")
            table.add_column("Input Source", justify="left", style="cyan", no_wrap=True)
            table.add_column("Token Count", justify="right", style="magenta")
            table.add_column("Encoding", justify="left", style="green")
            table.add_row("stdin", format_number_with_separators(token_count), selected_encoding)
            console.print(table)

            if check_limits and LLM_LIMITS:
                console.print("\n[bold yellow]LLM Context Window Limits:[/bold yellow]")
                grouped_models = group_models_by_provider(LLM_LIMITS)
                
                for provider, models in grouped_models.items():
                    console.print(f"\n[bold cyan]{provider}:[/bold cyan]")
                    for model, limit in models:
                        percentage = (token_count / limit) * 100
                        color = "green" if percentage <= 100 else "red"
                        token_display = format_number_compact(token_count)
                        limit_display = format_number_compact(limit)
                        console.print(f"  - [bold]{model}:[/bold] {token_display}/{limit_display} tokens ([{color}]{percentage:.2f}%[/])")

            raise typer.Exit(code=0)
        else:
            console.print("[bold red]Error:[/] No input file(s) provided and no data piped from stdin.", style="bold")
            raise typer.Exit(code=1)

    if not files_to_process:
        console.print("[bold red]Error:[/] No text files found to process in the provided path(s) or all files were excluded.", style="bold")
        raise typer.Exit(code=1)

    total_tokens_overall = 0
    results_table = Table(title="Token Count Results")
    results_table.add_column("File Path", justify="left", style="cyan", no_wrap=True)
    results_table.add_column("Token Count", justify="right", style="magenta")
    results_table.add_column("Encoding", justify="left", style="green")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        for file_path in files_to_process:
            task = progress.add_task(f"[cyan]Processing {file_path}[/cyan]", total=None)
            token_count = count_tokens(file_path=file_path, progress=progress, task_id=task, encoding_name=selected_encoding)

            if token_count == -1:
                console.print(f"[bold red]Error:[/] File not found at [cyan]{file_path}[/cyan]", style="bold")
                # Continue to next file, don't exit
            elif token_count == -3:
                console.print(f"[bold red]Error:[/] Invalid encoding name: [cyan]{selected_encoding}[/cyan] for file [cyan]{file_path}[/cyan]", style="bold")
                # Continue to next file, don't exit
            elif token_count == -2:
                console.print(f"[bold red]Error:[/] An error occurred while processing [cyan]{file_path}[/cyan].", style="bold")
                # Continue to next file, don't exit
            else:
                results_table.add_row(file_path, format_number_with_separators(token_count), selected_encoding)
                total_tokens_overall += token_count

    console.print(results_table)
    if len(files_to_process) > 1:
        console.print(f"\n[bold green]Total Tokens Across All Files:[/bold green] [bold magenta]{format_number_with_separators(total_tokens_overall)}[/bold magenta]")

    if check_limits and LLM_LIMITS:
        console.print("\n[bold yellow]LLM Context Window Limits:[/bold yellow]")
        tokens_to_check = total_tokens_overall if len(files_to_process) > 1 else (token_count if 'token_count' in locals() else 0)
        
        if tokens_to_check == 0 and len(files_to_process) == 1 and 'token_count' not in locals():
            # This case handles when a single file was processed but resulted in an error
            pass # No limits to check if there was an error and no tokens counted
        else:
            grouped_models = group_models_by_provider(LLM_LIMITS)
            
            for provider, models in grouped_models.items():
                console.print(f"\n[bold cyan]{provider}:[/bold cyan]")
                for model, limit in models:
                    percentage = (tokens_to_check / limit) * 100
                    color = "green" if percentage <= 100 else "red"
                    token_display = format_number_compact(tokens_to_check)
                    limit_display = format_number_compact(limit)
                    console.print(f"  - [bold]{model}:[/bold] {token_display}/{limit_display} tokens ([{color}]{percentage:.2f}%[/])")

if __name__ == "__main__":
    app()