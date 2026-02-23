# Python Text Editor Project

Welcome to the Python Text Editor project! This repository contains a fully functional, desktop-based GUI text editor built entirely using Python and the `tkinter` library. 

This project is split into two progressively advanced versions:
1. **`SimpleTextEditor.py`**: A robust, single-document text editor.
2. **`Advanced_TextEditor.py`**: A multi-tabbed, modern text editor capable of handling multiple files simultaneously.

---

## 🚀 Features & Capabilities

### Core Functionality
- **File Management**: Create New, Open, Save, and Exit files seamlessly. 
- **Edit Tools**: Full support for Undo, Redo, Cut, Copy, Paste, and Select All.
- **Find & Replace**: A dedicated popup window to search for specific terms (which highlights all matches in yellow) and replace them individually or all at once.

### Developer & UX Features
- **Live Status Bar**: Real-time tracking of the cursor's Line and Column, alongside Word and Character counts.
- **Python Syntax Highlighting**: Automatically detects Python keywords (`def`, `class`, `if`, etc.) and colors them dynamically based on the active theme.
- **Dark & Light Mode**: A fully integrated theming system. Toggle between a sleek Dark Mode (`#1e1e1e` background) and a clean Light Mode (`#ffffff` background).
- **Dynamic Font Resizing**: Change the font size on the fly (from 12pt up to 32pt) to suit your reading preferences.
- **Keyboard Shortcuts**: Complete hotkey mapping for power users (e.g., `Ctrl+S` to save, `Ctrl+H` for Find & Replace, `Ctrl+D` to toggle Dark Mode).

### Advanced Tabs (`Advanced_TextEditor.py` only)
- **Multi-Document Interface**: Open multiple files in independent tabs using `ttk.Notebook`.
- **Isolated Contexts**: Each tab maintains its own Undo/Redo history and tracks its own unsaved changes (indicated by a `*` in the tab title).
- **Safe Closing**: Attempts to close a tab with unsaved modifications will prompt a confirmation dialog to prevent data loss.

---

## 🛠️ Code Snippet Highlights

Here are some interesting implementation details from the codebase for those looking to learn or improve the project!

### 1. Non-Blocking Find & Replace Highlight
The editor searches through the text widget and applies a `found` tag to every match, allowing for easy visual identification without freezing the app.

```python
def find_text():
    text.tag_remove("found", "1.0", tk.END) # Clear old searches
    search_term = find_entry.get()
    
    if search_term:
        start = "1.0"
        while True:
            # text.search returns the position (e.g., "1.4") of the match
            pos = text.search(search_term, start, stopindex=tk.END)
            if not pos: break
            
            end = f"{pos}+{len(search_term)}c"
            text.tag_add("found", pos, end)
            start = end # Keep searching from the end of the last match
            
        # Apply yellow background to all "found" tags
        text.tag_config("found", background="yellow", foreground="black")
```

### 2. Live Syntax Highlighting
Whenever a key is released, the editor rapidly scans for Python keywords and applies colors based on the current Light/Dark theme setting.

```python
import keyword

def apply_syntax_highlighting(event=None):
    text.tag_remove("keyword", "1.0", tk.END)
    keyword_color = "orange" if is_dark_mode else "blue"
    text.tag_config("keyword", foreground=keyword_color)
    
    for kw in keyword.kwlist:
        start = "1.0"
        while True:
            pos = text.search(kw, start, stopindex=tk.END)
            if not pos: break
            end = f"{pos}+{len(kw)}c"
            text.tag_add("keyword", pos, end)
            start = end

# Bind the function to trigger on every key stroke
text.bind("<KeyRelease>", lambda event: apply_syntax_highlighting())
```

### 3. Tab Management System (Advanced Editor)
Using `ttk.Notebook`, the advanced editor dynamically generates new frames and text widgets inside tabs. A helper function retrieves the currently active widget so commands (like Save or Copy) always affect the correct file.

```python
def get_current_text_widget():
    tab_id = notebook.select()      # Get ID of the active tab
    if not tab_id: return None
    
    tab_frame = notebook.nametowidget(tab_id) # Convert ID to Frame object
    
    # Search the frame's children to find the tk.Text widget
    for child in tab_frame.winfo_children():
        if isinstance(child, tk.Text):
            return child
    return None
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + N` | New File / New Tab |
| `Ctrl + O` | Open File |
| `Ctrl + S` | Save File |
| `Ctrl + W` | Close Current Tab *(Advanced only)* |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Ctrl + A` | Select All |
| `Ctrl + H` | Find & Replace |
| `Ctrl + D` | Toggle Dark/Light Mode |

---

## 🚀 How to Run
Ensure you have Python installed (version 3.x recommended). No external `pip` dependencies are required for the core application as `tkinter` is built into the standard library!

To run the simple editor:
```bash
python SimpleTextEditor.py
```

To run the advanced multi-tab editor:
```bash
python Advanced_TextEditor.py
```

## 🤝 Areas for Improvement
For anyone looking to fork or study this code, here are great next steps for feature expansion:
1. **Full Word Match Check**: Currently, syntax highlighting triggers on partial words (e.g., `define` highlights `def`). Expanding the highlighting logic using Regex boundaries would improve accuracy.
2. **Current Line Highlighting**: Adding a subtle background color to the line the cursor is currently on.
3. **Auto-Indentation**: Make the enter key automatically match the indentation level of the previous line.
4. **Line Numbers**: Add a dedicated gutter frame on the left side to display standard file line numbers.
