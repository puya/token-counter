import tiktoken
import os
from rich.progress import Progress

def count_tokens(
    file_path: str,
    progress: Progress,
    task_id,
    encoding_name: str = "cl100k_base",
    chunk_size: int = 8192  # 8KB chunks
) -> int:
    """Counts the number of tokens in a file, updating a progress bar."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        total_tokens = 0
        file_size = os.path.getsize(file_path)
        progress.update(task_id, total=file_size)

        with open(file_path, "r") as f:
            while chunk := f.read(chunk_size):
                total_tokens += len(encoding.encode(chunk))
                progress.update(task_id, advance=len(chunk.encode('utf-8')))
        
        return total_tokens
    except FileNotFoundError:
        return -1
    except Exception as e:
        # In case of other errors, like permission denied
        return -2 # Using a different code for other errors