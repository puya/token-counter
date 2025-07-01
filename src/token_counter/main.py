import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from typing import Optional

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
    file_path: str = typer.Argument(..., help="The path to the text file to count tokens in."),
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
    """Counts the tokens in a text file and displays the result."""

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

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]Processing {file_path}[/cyan]", total=None)
        token_count = count_tokens(file_path, progress, task, encoding_name=selected_encoding)

    if token_count == -1:
        console.print(f"[bold red]Error:[/] File not found at [cyan]{file_path}[/cyan]", style="bold")
        raise typer.Exit(code=1)
    elif token_count == -3:
        console.print(f"[bold red]Error:[/] Invalid encoding name: [cyan]{selected_encoding}[/cyan]", style="bold")
        raise typer.Exit(code=1)
    elif token_count == -2:
        console.print(f"[bold red]Error:[/] An error occurred while processing the file.", style="bold")
        raise typer.Exit(code=1)

    table = Table(title="Token Count Result")
    table.add_column("File Path", justify="left", style="cyan", no_wrap=True)
    table.add_column("Token Count", justify="right", style="magenta")
    table.add_column("Encoding", justify="left", style="green")

    table.add_row(file_path, str(token_count), selected_encoding)

    console.print(table)

if __name__ == "__main__":
    app()
