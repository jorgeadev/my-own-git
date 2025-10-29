"""Git object handling: blob, tree, and commit objects."""

import hashlib
import zlib
from pathlib import Path
from typing import Optional


class GitObject:
    """Base class for Git objects."""
    
    def __init__(self, data: bytes):
        self.data = data
    
    def serialize(self) -> bytes:
        """Serialize the object data."""
        return self.data
    
    def get_type(self) -> str:
        """Return the object type."""
        raise NotImplementedError


class GitBlob(GitObject):
    """Represents a Git blob object (file content)."""
    
    def get_type(self) -> str:
        return "blob"


class GitTree(GitObject):
    """Represents a Git tree object (directory)."""
    
    def get_type(self) -> str:
        return "tree"


class GitCommit(GitObject):
    """Represents a Git commit object."""
    
    def get_type(self) -> str:
        return "commit"


def hash_object(data: bytes, obj_type: str = "blob", write: bool = False, git_dir: Optional[Path] = None) -> str:
    """
    Hash an object and optionally write it to the object database.
    
    Args:
        data: The object data to hash
        obj_type: The type of object (blob, tree, commit)
        write: If True, write the object to the database
        git_dir: Path to the .git directory
    
    Returns:
        The SHA-1 hash of the object as a hex string
    """
    # Create the object header
    header = f"{obj_type} {len(data)}\x00".encode()
    full_data = header + data
    
    # Compute SHA-1 hash
    sha1 = hashlib.sha1(full_data).hexdigest()
    
    if write and git_dir:
        # Compress the data
        compressed = zlib.compress(full_data)
        
        # Create object path: .git/objects/xx/yyyy...
        obj_dir = git_dir / "objects" / sha1[:2]
        obj_dir.mkdir(parents=True, exist_ok=True)
        
        obj_file = obj_dir / sha1[2:]
        
        # Write the object file
        with open(obj_file, 'wb') as f:
            f.write(compressed)
    
    return sha1


def read_object(sha1: str, git_dir: Path) -> tuple[str, bytes]:
    """
    Read an object from the object database.
    
    Args:
        sha1: The SHA-1 hash of the object
        git_dir: Path to the .git directory
    
    Returns:
        A tuple of (object_type, object_data)
    """
    # Construct object path
    obj_path = git_dir / "objects" / sha1[:2] / sha1[2:]
    
    if not obj_path.exists():
        raise FileNotFoundError(f"Object {sha1} not found")
    
    # Read and decompress the object
    with open(obj_path, 'rb') as f:
        compressed = f.read()
    
    data = zlib.decompress(compressed)
    
    # Parse the header
    null_pos = data.index(b'\x00')
    header = data[:null_pos].decode()
    obj_type, size_str = header.split(' ')
    
    # Extract the object data
    obj_data = data[null_pos + 1:]
    
    return obj_type, obj_data
