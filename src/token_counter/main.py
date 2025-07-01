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

from token_counter.counter import count_tokens

app = typer.Typer()
console = Console()

ENCODING_OPTIONS = {
    "cl100k_base": "Used by GPT-4, GPT-3.5-Turbo, text-embedding-ada-002",
    "p50k_base": "Used by CodeX models, text-davinci-002, text-davinci-003",
    "r50k_base": "Used by GPT-3 models like davinci (older)",
    "gpt2": "Used by GPT-2 models (older)",
}

@app.command()
def main(
    paths: Optional[List[str]] = typer.Argument(None, help="One or more file paths or directory paths to count tokens in. If not provided, reads from stdin."),
    encoding: Optional[str] = typer.Option(
        None, 
        "--encoding", 
        "-e", 
        help="Specify the encoding model (e.g., 'cl100k_base')."
    ),
    select_encoding: bool = typer.Option(
        False, 
        "--select-encoding", 
        "-s", 
        help="Interactively select the encoding model from a list."
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
    elif encoding is not None:
        selected_encoding = encoding # Use the provided encoding value

    files_to_process = []
    if paths:
        for p in paths:
            path_obj = Path(p)
            if path_obj.is_file():
                files_to_process.append(str(path_obj))
            elif path_obj.is_dir():
                for root, _, filenames in os.walk(path_obj):
                    for filename in filenames:
                        if filename.endswith(('.txt', '.md', '.py', '.js', '.ts', '.json', '.html', '.css')):
                            files_to_process.append(os.path.join(root, filename))
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
            table.add_row("stdin", str(token_count), selected_encoding)
            console.print(table)
            raise typer.Exit(code=0)
        else:
            console.print("[bold red]Error:[/] No input file(s) provided and no data piped from stdin.", style="bold")
            raise typer.Exit(code=1)

    if not files_to_process:
        console.print("[bold red]Error:[/] No text files found to process in the provided path(s).", style="bold")
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
                results_table.add_row(file_path, str(token_count), selected_encoding)
                total_tokens_overall += token_count

    console.print(results_table)
    if len(files_to_process) > 1:
        console.print(f"\n[bold green]Total Tokens Across All Files:[/bold green] [bold magenta]{total_tokens_overall}[/bold magenta]")

if __name__ == "__main__":
    app()
