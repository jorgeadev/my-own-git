# xgit

A basic Python implementation of Git core features. This project implements fundamental Git operations including repository initialization, object storage, and basic commands.

## Features

- **Repository Initialization**: Create a new Git repository with `init`
- **Object Hashing**: Hash and store Git objects (blobs, trees, commits) with `hash-object`
- **Object Reading**: Read and display Git objects with `cat-file`
- **Git Object Database**: Store and retrieve objects using SHA-1 hashing and zlib compression

## Installation

Clone the repository and install in development mode:

```bash
git clone https://github.com/jorgeadev/xgit.git
cd xgit
pip install -e .
```

## Usage

### Initialize a Repository

```bash
# Initialize in current directory
mygit init

# Initialize in a specific directory
mygit init /path/to/directory
```

### Hash an Object

```bash
# Hash a file (displays SHA-1 hash)
mygit hash-object myfile.txt

# Hash and write to object database
mygit hash-object -w myfile.txt

# Hash a specific object type
mygit hash-object -t blob -w myfile.txt
```

### Display Object Contents

```bash
# Display object content
mygit cat-file -p <object-hash>

# Display object type
mygit cat-file -t <object-hash>

# Display object size
mygit cat-file -s <object-hash>
```

## Running Tests

Run the test suite using Python's unittest:

```bash
python -m unittest discover tests
```

## Project Structure

```
xgit/
├── mygit/              # Main package
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # Command-line interface
│   ├── objects.py      # Git object handling
│   └── repository.py   # Repository management
├── tests/              # Test suite
│   ├── __init__.py
│   ├── test_objects.py
│   └── test_repository.py
├── setup.py            # Package setup
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Implementation Details

This implementation includes:

- **Git Objects**: Blob, Tree, and Commit object types
- **Object Storage**: SHA-1 hashing with zlib compression
- **Repository Structure**: Standard Git directory layout (.git/objects, .git/refs, etc.)
- **Command-line Interface**: Basic Git commands

## License

See LICENSE file for details.
