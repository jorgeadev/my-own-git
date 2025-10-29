"""Tests for Git object handling."""

import unittest
import tempfile
import shutil
from pathlib import Path

from mygit.objects import (
    GitBlob, GitTree, GitCommit,
    hash_object, read_object
)
from mygit.repository import init_repository


class TestGitObjects(unittest.TestCase):
    """Test Git object operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        self.git_dir = init_repository(self.test_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_git_blob(self):
        """Test GitBlob object."""
        data = b"Hello, World!"
        blob = GitBlob(data)
        
        self.assertEqual(blob.get_type(), "blob")
        self.assertEqual(blob.serialize(), data)
    
    def test_git_tree(self):
        """Test GitTree object."""
        data = b"tree data"
        tree = GitTree(data)
        
        self.assertEqual(tree.get_type(), "tree")
        self.assertEqual(tree.serialize(), data)
    
    def test_git_commit(self):
        """Test GitCommit object."""
        data = b"commit data"
        commit = GitCommit(data)
        
        self.assertEqual(commit.get_type(), "commit")
        self.assertEqual(commit.serialize(), data)
    
    def test_hash_object_without_write(self):
        """Test hashing an object without writing to database."""
        data = b"test content"
        sha1 = hash_object(data, "blob", write=False)
        
        # Verify it's a valid SHA-1 hash (40 hex characters)
        self.assertEqual(len(sha1), 40)
        self.assertTrue(all(c in "0123456789abcdef" for c in sha1))
        
        # Verify the hash is deterministic
        sha1_2 = hash_object(data, "blob", write=False)
        self.assertEqual(sha1, sha1_2)
    
    def test_hash_object_with_write(self):
        """Test hashing an object and writing to database."""
        data = b"test content for writing"
        sha1 = hash_object(data, "blob", write=True, git_dir=self.git_dir)
        
        # Verify object file was created
        obj_path = self.git_dir / "objects" / sha1[:2] / sha1[2:]
        self.assertTrue(obj_path.exists())
    
    def test_read_object(self):
        """Test reading an object from database."""
        data = b"test content for reading"
        sha1 = hash_object(data, "blob", write=True, git_dir=self.git_dir)
        
        # Read the object back
        obj_type, obj_data = read_object(sha1, self.git_dir)
        
        self.assertEqual(obj_type, "blob")
        self.assertEqual(obj_data, data)
    
    def test_read_nonexistent_object(self):
        """Test reading an object that doesn't exist."""
        fake_sha1 = "a" * 40
        
        with self.assertRaises(FileNotFoundError):
            read_object(fake_sha1, self.git_dir)
    
    def test_hash_different_types(self):
        """Test that different object types produce different hashes."""
        data = b"same data"
        
        blob_hash = hash_object(data, "blob", write=False)
        tree_hash = hash_object(data, "tree", write=False)
        commit_hash = hash_object(data, "commit", write=False)
        
        # All hashes should be different
        self.assertNotEqual(blob_hash, tree_hash)
        self.assertNotEqual(blob_hash, commit_hash)
        self.assertNotEqual(tree_hash, commit_hash)


if __name__ == "__main__":
    unittest.main()
