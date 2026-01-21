# R1

![TextEdit Screenshot](images/image.png)

## Core Editing Features

The text editor is built on PyQt6's `QPlainTextEdit` widget, which provides a solid foundation for plain text editing. All the essential editing features work correctly: typing text, undo/redo (Ctrl+Z and Ctrl+Shift+Z), cut/copy/paste (Ctrl+X/C/V), and text selection. I added several useful line manipulation commands that you'd find in modern editors like VS Code: duplicate line (Ctrl+Shift+D), delete line (Ctrl+Shift+K), and move line up/down (Alt+Up/Down). The editor uses the Menlo monospace font at 12pt with 4-space tab stops, which makes it suitable for code editing.

The `TextEditor` class is designed to be self-contained and reusable. It handles its own file I/O through `load_file()` and `save_file()` methods, tracks its modification state, and emits Qt signals when the cursor position or document changes. This signal-based architecture keeps the editor decoupled from the UI—the tab widget and status bar just listen for these signals rather than polling the editor's state. This made testing much easier since we can test the editor in isolation without needing to create the entire UI. The `TestEditorBasics` and `TestLineOperations` test classes in `tests/test_editor.py` verify that text insertion, modification tracking, and all line operations work correctly through programmatic testing.

## Opening and Saving Files

File operations work reliably using UTF-8 encoding, which ensures compatibility with code files and international text. The editor displays a ● (bullet) symbol in the tab title when a file has unsaved changes, providing clear visual feedback. When you try to close a modified file, a dialog prompts you with three options: Save, Discard, or Cancel, preventing accidental data loss.

The architecture cleanly separates concerns: the `TextEditor` class handles the low-level file reading and writing, while the `EditorTabWidget` manages the user-facing file dialogs and prompts. One nice feature I implemented is that if you try to open a file that's already open in another tab, the editor switches to that existing tab instead of opening it twice—this prevents confusion about which tab contains which version of a file. Additionally, when you open a file and have an empty "Untitled" tab, it reuses that tab rather than creating a new one. The `TestFileOperations` test class covers save/load round-trips, error handling for nonexistent files, and edge cases like attempting to save without specifying a path.

## Multi-file Support with Tabs and Split Views

This was one of the two advanced features I chose to implement. The tab system allows you to work with multiple files simultaneously, with tabs that can be dragged to reorder and keyboard shortcuts (Ctrl+Tab and Ctrl+Shift+Tab) to cycle through them. The split view system is more interesting—you can split the window horizontally (Ctrl+\\) for side-by-side editing or vertically (Ctrl+Shift+\\) for top-and-bottom layout. Splits can be nested infinitely in any direction, creating complex layouts for viewing multiple files at once.

The implementation uses Qt's `QSplitter` widget with a tree structure where each split can contain either tab widgets or more splits. The tricky part was managing which split is "active" for operations like opening files or saving—I solved this by tracking focus events on tab widgets and maintaining an `_active_tabs` reference in the `SplitContainer` class. When you close the last tab in a split pane, the split automatically removes itself and rebalances the layout. The splitter handles are now styled to be visible (gray bars that turn blue on hover) and are 4 pixels wide, making them easy to click and drag to resize panes. Because the split functionality is complex and involves dynamic UI manipulation, I validated it through manual testing with the running application, while the underlying tab and editor functionality is covered by the automated test suite.

## Find and Replace

This was the second advanced feature I implemented. The find/replace bar appears at the bottom of the window and provides all the essential search functionality: find next and previous (F3 and Shift+F3), case-sensitive search toggle, whole-word matching, replace single occurrence, and replace all. It displays a real-time match counter showing the total number of matches, and when you open it, it automatically populates with the current selection if any text is selected. The search wraps around the document boundaries, so pressing "find next" at the end of the file continues from the beginning.

The implementation uses Qt's `QTextDocument.find()` method with appropriate flags for case sensitivity and whole-word matching. I made the replace-all operation use Qt's edit blocks (beginEditBlock/endEditBlock), which makes the entire replace-all operation a single undo action—so if you accidentally replace 100 occurrences, one Ctrl+Z reverts all of them. One implementation detail I'm particularly happy with: the match counter recalculates on every keystroke by scanning the entire document. This could be slow for huge files, but it provides instant feedback as you type, which improves the user experience significantly. The `TestFindFunctionality` and `TestReplaceFunctionality` test classes in `tests/test_find_replace.py` provide 12 comprehensive tests covering search directions, wrap-around behavior, case-sensitive and case-insensitive searching, whole-word matching with punctuation boundaries, replace operations, and edge cases like empty strings and no matches.

## Software Architecture

The editor follows a modular architecture with clear separation of concerns. The `TextEditor` class is the core editing widget that handles file I/O and text manipulation. The `EditorTabWidget` manages multiple editor instances in tabs and handles tab-related UI operations. The `SplitContainer` manages the split view system with its dynamic nested layout. The `FindReplaceWidget` provides search and replace functionality. The `MainWindow` ties everything together with menus, keyboard shortcuts, and signal connections. All components communicate through Qt's signal/slot mechanism, which keeps coupling loose and makes it easy to test components in isolation or add new features without breaking existing code.

## Selected Advanced Features

For this assignment, I implemented two of the required advanced features:

1. **Multi-file support, tabs, and split views** - Fully functional with drag-to-reorder tabs, smart duplicate file prevention, horizontal and vertical splits with arbitrary nesting, automatic split cleanup, and visible draggable split handles.

2. **Find and replace** - Complete implementation with case-sensitive matching, whole-word search, replace single and replace all operations, live match counting, wrap-around navigation, and comprehensive test coverage.

Both features are fully functional, well-tested, and integrated seamlessly with the rest of the editor.

---

# R2

*Coming soon*

---

# R3

*Coming soon*
