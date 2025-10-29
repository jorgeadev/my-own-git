"""Tests for repository initialization and management."""

import unittest
import tempfile
import shutil
from pathlib import Path

from mygit.repository import init_repository, find_git_directory


class TestRepository(unittest.TestCase):
    """Test repository operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_init_repository(self):
        """Test repository initialization."""
        git_dir = init_repository(self.test_path)
        
        # Check that .git directory was created
        self.assertTrue(git_dir.exists())
        self.assertEqual(git_dir.name, ".git")
        
        # Check directory structure
        self.assertTrue((git_dir / "objects").exists())
        self.assertTrue((git_dir / "refs" / "heads").exists())
        self.assertTrue((git_dir / "refs" / "tags").exists())
        
        # Check HEAD file
        head_file = git_dir / "HEAD"
        self.assertTrue(head_file.exists())
        self.assertEqual(head_file.read_text(), "ref: refs/heads/main\n")
        
        # Check description file
        description_file = git_dir / "description"
        self.assertTrue(description_file.exists())
    
    def test_init_repository_already_exists(self):
        """Test that initializing an existing repository raises an error."""
        init_repository(self.test_path)
        
        with self.assertRaises(FileExistsError):
            init_repository(self.test_path)
    
    def test_find_git_directory(self):
        """Test finding the .git directory."""
        git_dir = init_repository(self.test_path)
        
        # Should find the .git directory from the repository root
        found = find_git_directory(self.test_path)
        self.assertEqual(found, git_dir)
        
        # Should find the .git directory from a subdirectory
        subdir = self.test_path / "subdir" / "nested"
        subdir.mkdir(parents=True)
        found = find_git_directory(subdir)
        self.assertEqual(found, git_dir)
    
    def test_find_git_directory_not_found(self):
        """Test finding .git directory when it doesn't exist."""
        found = find_git_directory(self.test_path)
        self.assertIsNone(found)


if __name__ == "__main__":
    unittest.main()
