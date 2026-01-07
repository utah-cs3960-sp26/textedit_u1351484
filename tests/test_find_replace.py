"""Tests for the FindReplaceWidget."""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.editor import TextEditor
from src.find_replace import FindReplaceWidget


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


@pytest.fixture
def find_replace(app, editor):
    """Create a FindReplaceWidget instance."""
    widget = FindReplaceWidget()
    widget.set_editor(editor)
    yield widget
    widget.deleteLater()


class TestFindFunctionality:
    """Test find functionality."""
    
    def test_find_next_basic(self, editor, find_replace):
        """Test basic find next."""
        editor.setPlainText("Hello World Hello")
        find_replace.find_input.setText("Hello")
        
        assert find_replace.find_next()
        assert editor.textCursor().selectedText() == "Hello"
        assert editor.textCursor().position() == 5
    
    def test_find_next_wraps(self, editor, find_replace):
        """Test that find wraps around."""
        editor.setPlainText("Hello World Hello")
        find_replace.find_input.setText("Hello")
        
        find_replace.find_next()
        find_replace.find_next()
        
        assert find_replace.find_next()
        assert editor.textCursor().position() == 5
    
    def test_find_previous(self, editor, find_replace):
        """Test find previous."""
        editor.setPlainText("Hello World Hello")
        cursor = editor.textCursor()
        cursor.setPosition(len("Hello World Hello"))
        editor.setTextCursor(cursor)
        
        find_replace.find_input.setText("Hello")
        
        assert find_replace.find_previous()
        assert editor.textCursor().selectedText() == "Hello"
    
    def test_find_case_sensitive(self, editor, find_replace):
        """Test case sensitive search."""
        editor.setPlainText("Hello hello HELLO")
        find_replace.find_input.setText("hello")
        find_replace.case_sensitive_cb.setChecked(True)
        
        assert find_replace.find_next()
        assert editor.textCursor().position() == 11
    
    def test_find_whole_word(self, editor, find_replace):
        """Test whole word search."""
        editor.setPlainText("Hello HelloWorld Hello")
        find_replace.find_input.setText("Hello")
        find_replace.whole_word_cb.setChecked(True)
        
        find_replace.find_next()
        first_pos = editor.textCursor().position()
        
        find_replace.find_next()
        second_pos = editor.textCursor().position()
        
        assert first_pos == 5
        assert second_pos == 22
    
    def test_find_no_match(self, editor, find_replace):
        """Test find with no match."""
        editor.setPlainText("Hello World")
        find_replace.find_input.setText("xyz")
        
        assert not find_replace.find_next()
    
    def test_find_empty_search(self, editor, find_replace):
        """Test find with empty search text."""
        editor.setPlainText("Hello World")
        find_replace.find_input.setText("")
        
        assert not find_replace.find_next()


class TestReplaceFunctionality:
    """Test replace functionality."""
    
    def test_replace_single(self, editor, find_replace):
        """Test single replacement."""
        editor.setPlainText("Hello World Hello")
        find_replace.find_input.setText("Hello")
        find_replace.replace_input.setText("Hi")
        
        find_replace.find_next()
        find_replace.replace()
        
        assert "Hi World" in editor.toPlainText()
    
    def test_replace_all(self, editor, find_replace):
        """Test replace all."""
        editor.setPlainText("Hello World Hello Hello")
        find_replace.find_input.setText("Hello")
        find_replace.replace_input.setText("Hi")
        
        count = find_replace.replace_all()
        
        assert count == 3
        assert editor.toPlainText() == "Hi World Hi Hi"
    
    def test_replace_all_case_sensitive(self, editor, find_replace):
        """Test case sensitive replace all."""
        editor.setPlainText("Hello hello HELLO")
        find_replace.find_input.setText("hello")
        find_replace.replace_input.setText("hi")
        find_replace.case_sensitive_cb.setChecked(True)
        
        count = find_replace.replace_all()
        
        assert count == 1
        assert editor.toPlainText() == "Hello hi HELLO"
    
    def test_replace_empty_replacement(self, editor, find_replace):
        """Test replacing with empty string (deletion)."""
        editor.setPlainText("Hello World")
        find_replace.find_input.setText(" World")
        find_replace.replace_input.setText("")
        
        find_replace.replace_all()
        
        assert editor.toPlainText() == "Hello"
    
    def test_replace_no_match(self, editor, find_replace):
        """Test replace with no matches."""
        editor.setPlainText("Hello World")
        find_replace.find_input.setText("xyz")
        find_replace.replace_input.setText("abc")
        
        count = find_replace.replace_all()
        
        assert count == 0
        assert editor.toPlainText() == "Hello World"


class TestFindReplaceUI:
    """Test find/replace UI behavior."""
    
    def test_show_find_focuses_input(self, editor, find_replace):
        """Test that showing find bar focuses the input."""
        find_replace.show_find()
        assert find_replace.isVisible()
    
    def test_show_find_uses_selection(self, editor, find_replace):
        """Test that showing find uses current selection."""
        editor.setPlainText("Hello World")
        cursor = editor.textCursor()
        cursor.setPosition(0)
        cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
        editor.setTextCursor(cursor)
        
        find_replace.show_find()
        
        assert find_replace.find_input.text() == "Hello"
