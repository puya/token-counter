import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from token_counter.counter import count_tokens

app = typer.Typer()
console = Console()

@app.command()
def main(file_path: str = typer.Argument(..., help="The path to the text file to count tokens in.")):
    """Counts the tokens in a text file and displays the result."""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]Processing {file_path}[/cyan]", total=None)
        token_count = count_tokens(file_path, progress, task)

    if token_count == -1:
        console.print(f"[bold red]Error:[/] File not found at [cyan]{file_path}[/cyan]", style="bold")
        raise typer.Exit(code=1)
    elif token_count == -2:
        console.print(f"[bold red]Error:[/] An error occurred while processing the file.", style="bold")
        raise typer.Exit(code=1)

    table = Table(title="Token Count Result")
    table.add_column("File Path", justify="left", style="cyan", no_wrap=True)
    table.add_column("Token Count", justify="right", style="magenta")

    table.add_row(file_path, str(token_count))

    console.print(table)

if __name__ == "__main__":
    app()