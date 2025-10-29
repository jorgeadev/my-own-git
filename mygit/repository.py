"""Repository initialization and management."""

from pathlib import Path
from typing import Optional


def init_repository(path: Optional[Path] = None) -> Path:
    """
    Initialize a new Git repository.
    
    Args:
        path: The path where to initialize the repository. 
              Defaults to current directory.
    
    Returns:
        Path to the .git directory
    """
    if path is None:
        path = Path.cwd()
    else:
        path = Path(path)
    
    # Create .git directory
    git_dir = path / ".git"
    
    if git_dir.exists():
        raise FileExistsError(f"Repository already exists at {path}")
    
    # Create directory structure
    git_dir.mkdir(parents=True)
    (git_dir / "objects").mkdir()
    (git_dir / "refs" / "heads").mkdir(parents=True)
    (git_dir / "refs" / "tags").mkdir(parents=True)
    
    # Create HEAD file
    head_file = git_dir / "HEAD"
    head_file.write_text("ref: refs/heads/main\n")
    
    # Create description file
    description_file = git_dir / "description"
    description_file.write_text("Unnamed repository; edit this file to name the repository.\n")
    
    return git_dir


def find_git_directory(path: Optional[Path] = None) -> Optional[Path]:
    """
    Find the .git directory starting from the given path.
    
    Args:
        path: The path to start searching from. Defaults to current directory.
    
    Returns:
        Path to the .git directory, or None if not found
    """
    if path is None:
        path = Path.cwd()
    else:
        path = Path(path).resolve()
    
    # Check current directory
    git_dir = path / ".git"
    if git_dir.is_dir():
        return git_dir
    
    # Check parent directories
    for parent in path.parents:
        git_dir = parent / ".git"
        if git_dir.is_dir():
            return git_dir
    
    return None
