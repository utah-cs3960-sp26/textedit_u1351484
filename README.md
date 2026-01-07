# TextEdit

A cross-platform text editor built with PyQt6.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

## Running Tests

```bash
pytest tests/ -v
```

---

# R1

## Core Editor

The text editor is built on PyQt6's `QPlainTextEdit`, providing a solid foundation for plain text editing. The editor supports:

- **Text editing**: Full text input with undo/redo support (Ctrl+Z, Ctrl+Shift+Z)
- **Selection**: Select word (Ctrl+D), select line (Ctrl+L), select all (Ctrl+A)
- **Clipboard**: Cut (Ctrl+X), copy (Ctrl+C), paste (Ctrl+V)
- **Line manipulation**: Duplicate line (Ctrl+Shift+D), delete line (Ctrl+Shift+K), move line up/down (Alt+Up/Down)

The editor uses a monospace font (Menlo) with 4-space tab stops for code-friendly editing. Each editor instance tracks its own file path and modification state, emitting signals when the cursor position or modification state changes.

Validation: The `TestEditorBasics` and `TestLineOperations` test classes verify text insertion, modification tracking, and all line operations work correctly.

## Opening and Saving Files

File I/O is handled through `load_file()` and `save_file()` methods on the TextEditor class. The implementation:

- Uses UTF-8 encoding for all files
- Tracks the file path and updates the modification state after save
- Provides visual feedback through tab titles (● prefix for unsaved changes)
- Prompts to save before closing modified files

The tab widget handles the file dialogs via `QFileDialog`, supporting both "Save" and "Save As" workflows. When opening a file that's already open, it switches to the existing tab instead of opening a duplicate.

Validation: `TestFileOperations` tests cover save/load round-trips, error handling for nonexistent files, and edge cases like saving without a path.

## Multi-file Support with Tabs

The `EditorTabWidget` class extends `QTabWidget` to manage multiple editor instances:

- **Closable tabs**: Each tab has a close button; prompts to save unsaved changes
- **Movable tabs**: Drag to reorder tabs
- **Tab navigation**: Ctrl+Tab and Ctrl+Shift+Tab cycle through tabs
- **Smart file opening**: Reuses empty untitled tabs, avoids duplicate tabs for the same file
- **Modification indicators**: Tab title shows ● prefix for unsaved files

The architecture keeps the editor widget simple and stateless regarding multi-file concerns—the tab widget handles all tab lifecycle management.

Validation: Tab functionality is validated manually through the running application. The underlying editor tests ensure each tab's editor instance works correctly.

## Find and Replace

The `FindReplaceWidget` provides comprehensive search functionality:

- **Find next/previous**: Navigate through matches with F3/Shift+F3 or arrow buttons
- **Replace single**: Replace current match and advance to next
- **Replace all**: Replace all occurrences in one operation
- **Options**: Case sensitive and whole word matching
- **Match counter**: Shows total number of matches
- **Keyboard-friendly**: Enter to find next, Escape to close

The find bar appears at the bottom of the window and automatically populates with the current selection when opened. The search wraps around the document when reaching the end.

Validation: `TestFindFunctionality` and `TestReplaceFunctionality` provide 14 tests covering basic search, wrap-around, case sensitivity, whole word matching, replace operations, and edge cases.

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New | Ctrl+N |
| Open | Ctrl+O |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Close Tab | Ctrl+W |
| Undo/Redo | Ctrl+Z / Ctrl+Shift+Z |
| Find | Ctrl+F |
| Replace | Ctrl+H |
| Go to Line | Ctrl+G |
| Select Word | Ctrl+D |
| Select Line | Ctrl+L |
| Duplicate Line | Ctrl+Shift+D |
| Delete Line | Ctrl+Shift+K |
| Move Line Up/Down | Alt+Up/Down |

---

# R2

*Coming soon*

---

# R3

*Coming soon*
