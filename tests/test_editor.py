"""Tests for the TextEditor widget."""

import pytest
import tempfile
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QTextCursor

from src.editor import TextEditor


@pytest.fixture(scope="session")
def app():
    """Create a QApplication instance for the test session."""
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    yield application


@pytest.fixture
def editor(app):
    """Create a TextEditor instance."""
    ed = TextEditor()
    yield ed
    ed.deleteLater()


class TestEditorBasics:
    """Test basic editor functionality."""
    
    def test_initial_state(self, editor):
        """Test editor initial state."""
        assert editor.file_path is None
        assert not editor.is_modified
        assert editor.toPlainText() == ""
    
    def test_text_insertion(self, editor):
        """Test basic text insertion."""
        editor.setPlainText("Hello, World!")
        assert editor.toPlainText() == "Hello, World!"
    
    def test_modification_tracking(self, editor):
        """Test modification state tracking."""
        editor.setPlainText("Test")
        editor.set_modified(False)
        assert not editor.is_modified
        
        cursor = editor.textCursor()
        cursor.insertText("a")
        assert editor.is_modified
    
    def test_display_name_untitled(self, editor):
        """Test display name for untitled file."""
        assert editor.get_display_name() == "Untitled"
    
    def test_display_name_with_file(self, editor):
        """Test display name with file path."""
        editor.file_path = "/path/to/test.txt"
        assert editor.get_display_name() == "test.txt"


class TestFileOperations:
    """Test file save/load operations."""
    
    def test_save_and_load_file(self, editor):
        """Test saving and loading a file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            editor.setPlainText("Test content\nLine 2")
            assert editor.save_file(temp_path)
            assert editor.file_path == temp_path
            assert not editor.is_modified
            
            editor2 = TextEditor()
            assert editor2.load_file(temp_path)
            assert editor2.toPlainText() == "Test content\nLine 2"
            assert editor2.file_path == temp_path
            assert not editor2.is_modified
            editor2.deleteLater()
        finally:
            os.unlink(temp_path)
    
    def test_load_nonexistent_file(self, editor):
        """Test loading a file that doesn't exist."""
        assert not editor.load_file("/nonexistent/path/file.txt")
    
    def test_save_without_path(self, editor):
        """Test saving without a path."""
        editor.setPlainText("Test")
        assert not editor.save_file()


class TestLineOperations:
    """Test line manipulation operations."""
    
    def test_duplicate_line(self, editor):
        """Test line duplication."""
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        cursor = editor.textCursor()
        cursor.setPosition(0)
        editor.setTextCursor(cursor)
        
        editor.duplicate_line()
        lines = editor.toPlainText().split('\n')
        assert len(lines) == 4
        assert lines[0] == "Line 1"
        assert lines[1] == "Line 1"
    
    def test_delete_line(self, editor):
        """Test line deletion."""
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        cursor = editor.textCursor()
        cursor.setPosition(7)
        editor.setTextCursor(cursor)
        
        editor.delete_line()
        lines = editor.toPlainText().split('\n')
        assert len(lines) == 2
        assert lines[0] == "Line 1"
        assert lines[1] == "Line 3"
    
    def test_move_line_down(self, editor):
        """Test moving line down."""
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        cursor = editor.textCursor()
        cursor.setPosition(0)
        editor.setTextCursor(cursor)
        
        editor.move_line_down()
        lines = editor.toPlainText().split('\n')
        assert lines[0] == "Line 2"
        assert lines[1] == "Line 1"
        assert lines[2] == "Line 3"
    
    def test_move_line_up(self, editor):
        """Test moving line up."""
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        cursor = editor.textCursor()
        cursor.setPosition(7)
        editor.setTextCursor(cursor)
        
        editor.move_line_up()
        lines = editor.toPlainText().split('\n')
        assert lines[0] == "Line 2"
        assert lines[1] == "Line 1"
        assert lines[2] == "Line 3"
    
    def test_move_first_line_up_noop(self, editor):
        """Test that moving the first line up does nothing."""
        editor.setPlainText("Line 1\nLine 2")
        cursor = editor.textCursor()
        cursor.setPosition(0)
        editor.setTextCursor(cursor)
        
        editor.move_line_up()
        assert editor.toPlainText() == "Line 1\nLine 2"
    
    def test_move_last_line_down_noop(self, editor):
        """Test that moving the last line down does nothing."""
        editor.setPlainText("Line 1\nLine 2")
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        editor.setTextCursor(cursor)
        
        editor.move_line_down()
        assert editor.toPlainText() == "Line 1\nLine 2"


class TestSelection:
    """Test selection operations."""
    
    def test_select_word(self, editor):
        """Test word selection."""
        editor.setPlainText("Hello World")
        cursor = editor.textCursor()
        cursor.setPosition(2)
        editor.setTextCursor(cursor)
        
        editor.select_word()
        assert editor.textCursor().selectedText() == "Hello"
    
    def test_select_line(self, editor):
        """Test line selection."""
        editor.setPlainText("Line 1\nLine 2")
        cursor = editor.textCursor()
        cursor.setPosition(0)
        editor.setTextCursor(cursor)
        
        editor.select_line()
        assert editor.textCursor().selectedText() == "Line 1"
    
    def test_select_all(self, editor):
        """Test select all."""
        editor.setPlainText("Line 1\nLine 2")
        editor.select_all()
        assert editor.textCursor().selectedText() == "Line 1\u2029Line 2"


class TestNavigation:
    """Test navigation operations."""
    
    def test_go_to_line(self, editor):
        """Test go to line."""
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        editor.go_to_line(2)
        
        cursor = editor.textCursor()
        assert cursor.blockNumber() == 1
    
    def test_go_to_invalid_line(self, editor):
        """Test go to invalid line number."""
        editor.setPlainText("Line 1\nLine 2")
        editor.go_to_line(999)
        pass
