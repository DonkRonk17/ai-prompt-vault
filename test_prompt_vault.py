#!/usr/bin/env python3
"""
Test Suite for AI Prompt Vault
===============================
Comprehensive tests for all vault operations.

Author: Atlas (Team Brain)
For: Logan Smith / Metaphy LLC
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import prompt_vault


class TestVaultOperations(unittest.TestCase):
    """Test core vault operations."""
    
    def setUp(self):
        """Create a temporary vault for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_dir = Path(self.temp_dir) / ".prompt-vault"
        self.vault_file = self.vault_dir / "prompts.json"
        self.config_file = self.vault_dir / "config.json"
        
        # Override vault paths
        prompt_vault.VAULT_DIR = self.vault_dir
        prompt_vault.VAULT_FILE = self.vault_file
        prompt_vault.CONFIG_FILE = self.config_file
        
        # Initialize vault
        prompt_vault.init_vault()
    
    def tearDown(self):
        """Clean up temporary vault."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_01_init_vault(self):
        """Test vault initialization."""
        self.assertTrue(self.vault_dir.exists())
        self.assertTrue(self.vault_file.exists())
        self.assertTrue(self.config_file.exists())
        
        # Check vault structure
        vault = prompt_vault.load_vault()
        self.assertIn("prompts", vault)
        self.assertIn("version", vault)
        self.assertEqual(vault["prompts"], [])
    
    def test_02_add_prompt_basic(self):
        """Test adding a basic prompt."""
        result = prompt_vault.add_prompt(
            "test-prompt",
            "This is a test prompt",
            category="testing"
        )
        self.assertTrue(result)
        
        # Verify prompt was added
        vault = prompt_vault.load_vault()
        self.assertEqual(len(vault["prompts"]), 1)
        
        prompt = vault["prompts"][0]
        self.assertEqual(prompt["name"], "test-prompt")
        self.assertEqual(prompt["content"], "This is a test prompt")
        self.assertEqual(prompt["category"], "testing")
    
    def test_03_add_prompt_with_tags(self):
        """Test adding a prompt with tags."""
        result = prompt_vault.add_prompt(
            "tagged-prompt",
            "Tagged content",
            category="coding",
            tags=["python", "testing", "example"]
        )
        self.assertTrue(result)
        
        prompt = prompt_vault.get_prompt("tagged-prompt")
        self.assertIsNotNone(prompt)
        self.assertEqual(len(prompt["tags"]), 3)
        self.assertIn("python", prompt["tags"])
    
    def test_04_add_duplicate_prompt(self):
        """Test that duplicate prompt names are rejected."""
        prompt_vault.add_prompt("duplicate", "Content 1")
        result = prompt_vault.add_prompt("duplicate", "Content 2")
        self.assertFalse(result)
        
        # Verify only one prompt exists
        vault = prompt_vault.load_vault()
        self.assertEqual(len(vault["prompts"]), 1)
    
    def test_05_get_prompt_by_name(self):
        """Test retrieving a prompt by name."""
        prompt_vault.add_prompt("findme", "Content", category="general")
        
        prompt = prompt_vault.get_prompt("findme")
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt["name"], "findme")
        self.assertEqual(prompt["content"], "Content")
    
    def test_06_get_prompt_by_id(self):
        """Test retrieving a prompt by ID."""
        prompt_vault.add_prompt("test", "Content")
        vault = prompt_vault.load_vault()
        prompt_id = vault["prompts"][0]["id"]
        
        prompt = prompt_vault.get_prompt(prompt_id)
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt["name"], "test")
    
    def test_07_get_nonexistent_prompt(self):
        """Test getting a prompt that doesn't exist."""
        prompt = prompt_vault.get_prompt("nonexistent")
        self.assertIsNone(prompt)
    
    def test_08_use_prompt_increments_counter(self):
        """Test that using a prompt increments the use counter."""
        prompt_vault.add_prompt("counter-test", "Content")
        
        # Use prompt twice
        prompt_vault.use_prompt("counter-test", copy_to_clipboard=False)
        prompt_vault.use_prompt("counter-test", copy_to_clipboard=False)
        
        prompt = prompt_vault.get_prompt("counter-test")
        self.assertEqual(prompt["uses"], 2)
    
    def test_09_list_prompts_all(self):
        """Test listing all prompts."""
        prompt_vault.add_prompt("prompt1", "Content 1", category="coding")
        prompt_vault.add_prompt("prompt2", "Content 2", category="writing")
        prompt_vault.add_prompt("prompt3", "Content 3", category="coding")
        
        prompts = prompt_vault.list_prompts()
        self.assertEqual(len(prompts), 3)
    
    def test_10_list_prompts_by_category(self):
        """Test listing prompts filtered by category."""
        prompt_vault.add_prompt("code1", "Content", category="coding")
        prompt_vault.add_prompt("write1", "Content", category="writing")
        prompt_vault.add_prompt("code2", "Content", category="coding")
        
        coding_prompts = prompt_vault.list_prompts(category="coding")
        self.assertEqual(len(coding_prompts), 2)
        
        writing_prompts = prompt_vault.list_prompts(category="writing")
        self.assertEqual(len(writing_prompts), 1)
    
    def test_11_list_prompts_by_tag(self):
        """Test listing prompts filtered by tag."""
        prompt_vault.add_prompt("p1", "Content", tags=["python", "testing"])
        prompt_vault.add_prompt("p2", "Content", tags=["javascript"])
        prompt_vault.add_prompt("p3", "Content", tags=["python", "coding"])
        
        python_prompts = prompt_vault.list_prompts(tag="python")
        self.assertEqual(len(python_prompts), 2)
    
    def test_12_search_prompts_by_name(self):
        """Test searching prompts by name."""
        prompt_vault.add_prompt("debug-python", "Debug content")
        prompt_vault.add_prompt("test-code", "Test content")
        prompt_vault.add_prompt("debug-js", "Debug JS")
        
        results = prompt_vault.list_prompts(search="debug")
        self.assertEqual(len(results), 2)
    
    def test_13_search_prompts_by_content(self):
        """Test searching prompts by content."""
        prompt_vault.add_prompt("p1", "This contains keyword special")
        prompt_vault.add_prompt("p2", "This does not")
        prompt_vault.add_prompt("p3", "Also has special keyword")
        
        results = prompt_vault.list_prompts(search="special")
        self.assertEqual(len(results), 2)
    
    def test_14_delete_prompt(self):
        """Test deleting a prompt."""
        prompt_vault.add_prompt("to-delete", "Content")
        
        result = prompt_vault.delete_prompt("to-delete")
        self.assertTrue(result)
        
        # Verify deletion
        prompt = prompt_vault.get_prompt("to-delete")
        self.assertIsNone(prompt)
    
    def test_15_delete_nonexistent_prompt(self):
        """Test deleting a prompt that doesn't exist."""
        result = prompt_vault.delete_prompt("nonexistent")
        self.assertFalse(result)
    
    def test_16_update_prompt_content(self):
        """Test updating prompt content."""
        prompt_vault.add_prompt("updatable", "Old content")
        
        result = prompt_vault.update_prompt("updatable", new_content="New content")
        self.assertTrue(result)
        
        prompt = prompt_vault.get_prompt("updatable")
        self.assertEqual(prompt["content"], "New content")
    
    def test_17_update_prompt_category(self):
        """Test updating prompt category."""
        prompt_vault.add_prompt("categorized", "Content", category="coding")
        
        prompt_vault.update_prompt("categorized", new_category="testing")
        
        prompt = prompt_vault.get_prompt("categorized")
        self.assertEqual(prompt["category"], "testing")
    
    def test_18_update_prompt_tags(self):
        """Test updating prompt tags."""
        prompt_vault.add_prompt("tagged", "Content", tags=["old"])
        
        prompt_vault.update_prompt("tagged", new_tags=["new", "tags"])
        
        prompt = prompt_vault.get_prompt("tagged")
        self.assertEqual(prompt["tags"], ["new", "tags"])
    
    def test_19_update_prompt_name(self):
        """Test updating prompt name."""
        prompt_vault.add_prompt("old-name", "Content")
        
        result = prompt_vault.update_prompt("old-name", new_name="new-name")
        self.assertTrue(result)
        
        # Old name should not exist
        self.assertIsNone(prompt_vault.get_prompt("old-name"))
        
        # New name should exist
        prompt = prompt_vault.get_prompt("new-name")
        self.assertIsNotNone(prompt)


class TestImportExport(unittest.TestCase):
    """Test import/export functionality."""
    
    def setUp(self):
        """Create a temporary vault for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_dir = Path(self.temp_dir) / ".prompt-vault"
        self.vault_file = self.vault_dir / "prompts.json"
        self.config_file = self.vault_dir / "config.json"
        
        # Override vault paths
        prompt_vault.VAULT_DIR = self.vault_dir
        prompt_vault.VAULT_FILE = self.vault_file
        prompt_vault.CONFIG_FILE = self.config_file
        
        prompt_vault.init_vault()
    
    def tearDown(self):
        """Clean up temporary vault."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_20_export_all_prompts(self):
        """Test exporting all prompts."""
        prompt_vault.add_prompt("p1", "Content 1", category="coding")
        prompt_vault.add_prompt("p2", "Content 2", category="writing")
        
        export_file = Path(self.temp_dir) / "export.json"
        result = prompt_vault.export_prompts(str(export_file))
        self.assertTrue(result)
        self.assertTrue(export_file.exists())
        
        # Verify export contents
        data = json.loads(export_file.read_text())
        self.assertEqual(len(data["prompts"]), 2)
        self.assertEqual(data["count"], 2)
    
    def test_21_export_by_category(self):
        """Test exporting prompts by category."""
        prompt_vault.add_prompt("code1", "Content", category="coding")
        prompt_vault.add_prompt("write1", "Content", category="writing")
        prompt_vault.add_prompt("code2", "Content", category="coding")
        
        export_file = Path(self.temp_dir) / "coding-export.json"
        prompt_vault.export_prompts(str(export_file), category="coding")
        
        data = json.loads(export_file.read_text())
        self.assertEqual(len(data["prompts"]), 2)
    
    def test_22_import_prompts(self):
        """Test importing prompts."""
        # Create import file
        import_data = {
            "prompts": [
                {"name": "imported1", "content": "Content 1", "category": "coding"},
                {"name": "imported2", "content": "Content 2", "category": "testing"}
            ]
        }
        import_file = Path(self.temp_dir) / "import.json"
        import_file.write_text(json.dumps(import_data))
        
        result = prompt_vault.import_prompts(str(import_file))
        self.assertTrue(result)
        
        # Verify import
        vault = prompt_vault.load_vault()
        self.assertEqual(len(vault["prompts"]), 2)
    
    def test_23_import_skip_duplicates(self):
        """Test that import skips duplicates by default."""
        prompt_vault.add_prompt("existing", "Original content")
        
        import_data = {
            "prompts": [
                {"name": "existing", "content": "New content"},
                {"name": "new-prompt", "content": "Content"}
            ]
        }
        import_file = Path(self.temp_dir) / "import.json"
        import_file.write_text(json.dumps(import_data))
        
        prompt_vault.import_prompts(str(import_file), overwrite=False)
        
        # Original should be unchanged
        prompt = prompt_vault.get_prompt("existing")
        self.assertEqual(prompt["content"], "Original content")
        
        # New prompt should be added
        vault = prompt_vault.load_vault()
        self.assertEqual(len(vault["prompts"]), 2)
    
    def test_24_import_with_overwrite(self):
        """Test import with overwrite enabled."""
        prompt_vault.add_prompt("overwrite-me", "Old content")
        
        import_data = {
            "prompts": [
                {"name": "overwrite-me", "content": "New content"}
            ]
        }
        import_file = Path(self.temp_dir) / "import.json"
        import_file.write_text(json.dumps(import_data))
        
        prompt_vault.import_prompts(str(import_file), overwrite=True)
        
        # Content should be updated
        prompt = prompt_vault.get_prompt("overwrite-me")
        self.assertEqual(prompt["content"], "New content")


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_25_generate_id_consistency(self):
        """Test that generate_id produces consistent results."""
        id1 = prompt_vault.generate_id("test content")
        id2 = prompt_vault.generate_id("test content")
        self.assertEqual(id1, id2)
    
    def test_26_generate_id_uniqueness(self):
        """Test that different content produces different IDs."""
        id1 = prompt_vault.generate_id("content 1")
        id2 = prompt_vault.generate_id("content 2")
        self.assertNotEqual(id1, id2)
    
    def test_27_generate_id_length(self):
        """Test that generated IDs are 8 characters."""
        id = prompt_vault.generate_id("any content")
        self.assertEqual(len(id), 8)


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestVaultOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestImportExport))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
