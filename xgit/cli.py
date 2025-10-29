#!/usr/bin/env python3
"""Command-line interface for My Own Git."""

import sys
import argparse
from pathlib import Path

from mygit.repository import init_repository, find_git_directory
from mygit.objects import hash_object, read_object


def cmd_init(args):
    """Initialize a new repository."""
    try:
        git_dir = init_repository(args.path)
        print(f"Initialized empty Git repository in {git_dir.parent.resolve()}")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_hash_object(args):
    """Hash an object and optionally write it to the database."""
    try:
        # Read the file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File {args.file} not found", file=sys.stderr)
            sys.exit(1)
        
        data = file_path.read_bytes()
        
        # Find git directory if we need to write
        git_dir = None
        if args.write:
            git_dir = find_git_directory()
            if git_dir is None:
                print("Error: Not a git repository", file=sys.stderr)
                sys.exit(1)
        
        # Hash the object
        sha1 = hash_object(data, args.type, args.write, git_dir)
        print(sha1)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_cat_file(args):
    """Display the contents of an object."""
    try:
        # Find git directory
        git_dir = find_git_directory()
        if git_dir is None:
            print("Error: Not a git repository", file=sys.stderr)
            sys.exit(1)
        
        # Read the object
        obj_type, obj_data = read_object(args.object, git_dir)
        
        if args.pretty_print:
            # For pretty print, just output the content
            sys.stdout.buffer.write(obj_data)
        elif args.type:
            # Show the type
            print(obj_type)
        elif args.size:
            # Show the size
            print(len(obj_data))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="My Own Git - A basic Python implementation of Git"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new repository")
    init_parser.add_argument(
        "path", 
        nargs="?", 
        default=None,
        help="Path to initialize repository (default: current directory)"
    )
    init_parser.set_defaults(func=cmd_init)
    
    # hash-object command
    hash_parser = subparsers.add_parser(
        "hash-object", 
        help="Compute object ID and optionally create a blob"
    )
    hash_parser.add_argument("file", help="File to hash")
    hash_parser.add_argument(
        "-t", "--type",
        default="blob",
        choices=["blob", "tree", "commit"],
        help="Object type (default: blob)"
    )
    hash_parser.add_argument(
        "-w", "--write",
        action="store_true",
        help="Write the object to the database"
    )
    hash_parser.set_defaults(func=cmd_hash_object)
    
    # cat-file command
    cat_parser = subparsers.add_parser(
        "cat-file",
        help="Provide content or type and size information for repository objects"
    )
    cat_parser.add_argument("object", help="Object hash to display")
    cat_parser.add_argument(
        "-p", "--pretty-print",
        action="store_true",
        help="Pretty-print the object content"
    )
    cat_parser.add_argument(
        "-t", "--type",
        action="store_true",
        help="Show the object type"
    )
    cat_parser.add_argument(
        "-s", "--size",
        action="store_true",
        help="Show the object size"
    )
    cat_parser.set_defaults(func=cmd_cat_file)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the command
    args.func(args)


if __name__ == "__main__":
    main()
