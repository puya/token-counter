import tiktoken
import os
from rich.progress import Progress
from typing import Optional

def count_tokens(
    file_path: Optional[str] = None,
    text_content: Optional[str] = None,
    progress: Optional[Progress] = None,
    task_id = None,
    encoding_name: str = "cl100k_base",
    chunk_size: int = 8192  # 8KB chunks
) -> int:
    """Counts the number of tokens in a file or string, updating a progress bar."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        total_tokens = 0

        if text_content is not None:
            total_tokens = len(encoding.encode(text_content))
            if progress and task_id:
                progress.update(task_id, total=len(text_content.encode('utf-8')), advance=len(text_content.encode('utf-8')))
        elif file_path is not None:
            file_size = os.path.getsize(file_path)
            if progress and task_id:
                progress.update(task_id, total=file_size)

            with open(file_path, "r") as f:
                while chunk := f.read(chunk_size):
                    total_tokens += len(encoding.encode(chunk))
                    if progress and task_id:
                        progress.update(task_id, advance=len(chunk.encode('utf-8')))
        else:
            return -4 # No input provided
        
        return total_tokens
    except FileNotFoundError:
        return -1
    except ValueError:
        return -3 # Invalid encoding name
    except Exception as e:
        return -2 # Using a different code for other errors