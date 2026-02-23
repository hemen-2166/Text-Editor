import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import keyword 

# Global variable to store the current file path
current_file = None

# Theme configurations
dark_theme = {
    "bg": "#1e1e1e",        # Background: dark gray
    "fg": "#d4d4d4",        # Foreground (text): light gray
    "cursor": "#ffffff",    # Cursor: white
    "select_bg": "#264f78"  # Selection background: blue
}
light_theme = {
    "bg": "#ffffff",        # Background: white
    "fg": "#000000",        # Foreground: black
    "cursor": "#000000",    # Cursor: black
    "select_bg": "#0078d7"  # Selection: blue
}

is_dark_mode = False   # Track theme state

# Create main application window
root = tk.Tk()
root.title("Simple Text Editor")
root.geometry("800x600")

# --- STATUS BAR (Create FIRST so it stays at bottom) ---
# Create a Frame (an invisible container/box) at the bottom
status_bar = tk.Frame(root, height=20)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)
# Create a StringVar — a "smart" variable
status_text = tk.StringVar()
status_text.set("Line: 1 | Column: 0 | Words: 0 | Chars: 0")
# Put a Label inside the Frame, connected to the StringVar
status_label = tk.Label(status_bar, textvariable=status_text, anchor=tk.E, padx=10)
status_label.pack(fill=tk.X)

# --- TABS SETUP (Create SECOND to fill remaining space) ---
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill=tk.BOTH)


# --- FUNCTION TO GET ACTIVE TEXT WIDGET ---
def get_current_text_widget():
    # Get the currently selected tab ID
    tab_id = notebook.select()
    if not tab_id: return None
    
    # Get the widget object from ID
    tab_frame = notebook.nametowidget(tab_id)
    
    # Find the Text widget inside this frame
    for child in tab_frame.winfo_children():
        if isinstance(child, tk.Text):
            return child
    return None


# --- FUNCTION TO CREATE NEW TAB ---
def create_editor_tab(content="", title="Untitled"):
    # 1. Create a frame for the tab
    frame = tk.Frame(notebook)
    # Create a scrollbar for the text widget
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame.pack(expand=True, fill=tk.BOTH)
    # 2. Add the frame to notebook
    notebook.add(frame, text=title)
    

    # 3. Create Text widget inside the frame
    text_widget = tk.Text(
        frame,
        wrap=tk.WORD,
        font=("Helvetica", 18),
        undo=True
    )
    text_widget.pack(expand=True, fill=tk.BOTH)
    
    # 4. Insert content if any
    if content:
        text_widget.insert("1.0", content)
        
    # 5. Make this the active tab
    notebook.select(frame)
    
    # 6. Apply bindings to THIS specific text widget
    text_widget.bind("<KeyRelease>", lambda e: [update_status(), apply_syntax_highlighting()])
    text_widget.bind("<<Modified>>", lambda e: on_text_change())
    # Update status on click/focus
    text_widget.bind("<ButtonRelease-1>", lambda e: update_status())
    text_widget.bind("<FocusIn>", lambda e: update_status())
    
    # Apply current theme to new tab
    theme = dark_theme if is_dark_mode else light_theme
    text_widget.config(
        bg=theme["bg"],
        fg=theme["fg"],
        insertbackground=theme["cursor"],
        selectbackground=theme["select_bg"]
    )
    
    return text_widget


# Function to create a new file
def new_file():
    create_editor_tab()

# Function to close current tab safely
def close_current_tab():
    current_tab = notebook.select()
    if not current_tab: return

    # Check for unsaved changes IN THIS TAB
    text_widget = get_current_text_widget()
    if text_widget and text_widget.edit_modified():
        if not messagebox.askyesno("Unsaved Changes", "Close tab without saving?"):
            return # Cancel closing

    notebook.forget(current_tab)
    
    # If no tabs left, create new one
    if not notebook.tabs():
        create_editor_tab()

# Function to open an existing text file
def open_file():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            # Create NEW TAB
            create_editor_tab(content, title=file_path.split("/")[-1])

# Function to save the current text to a file
def save_file():
    text = get_current_text_widget()
    if not text: return

    # Simple approach: Always Save As for now
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get("1.0", tk.END))
        
        # Update tab title
        current_tab = notebook.select()
        notebook.tab(current_tab, text=file_path.split("/")[-1])
        
        messagebox.showinfo("Success", "File saved successfully!")
        text.edit_modified(False)

# A function that reads cursor position and updates the status bar
def update_status(event=None):
    text = get_current_text_widget()
    if not text: return

    try:
        position = text.index(tk.INSERT)
        line, column = position.split(".")
        content = text.get("1.0", "end-1c")
        word_count = len(content.split()) if content else 0
        char_count = len(content)
        status_text.set(f"Line: {line} | Column: {column} | Words: {word_count} | Chars: {char_count}")
    except:
        pass 

# Function to undo the last action
def undo_text():
    text = get_current_text_widget()
    if text:
        try: text.edit_undo()
        except tk.TclError: pass

# Function to redo the last action
def redo_text():
    text = get_current_text_widget()
    if text:
        try: text.edit_redo()
        except tk.TclError: pass

# Function to mark text as modified (shows * in title)
def on_text_change(event=None):
    text = get_current_text_widget()
    if not text: return
    
    if text.edit_modified():
        # Get current tab index
        current_tab = notebook.select()
        current_title = notebook.tab(current_tab, "text")
        if not current_title.startswith("*"):
            notebook.tab(current_tab, text="*" + current_title)

# Function to handle window close
def on_closing():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

def cut_text():
    text = get_current_text_widget()
    if text: text.event_generate("<<Cut>>")

def copy_text():
    text = get_current_text_widget()
    if text: text.event_generate("<<Copy>>")

def paste_text():
    text = get_current_text_widget()
    if text: text.event_generate("<<Paste>>")

def select_all():
    text = get_current_text_widget()
    if text:
        text.tag_add("sel", "1.0", "end-1c")
        return "break"

# Function to find and replace text window render
def find_replace():
    text = get_current_text_widget()
    if not text: return
    
    find_window = tk.Toplevel(root)
    find_window.title("Find & Replace")
    find_window.geometry("400x150")
    find_window.resizable(False, False)
    
    tk.Label(find_window, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    find_entry = tk.Entry(find_window, width=30)
    find_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(find_window, text="Replace:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    replace_entry = tk.Entry(find_window, width=30)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    def find_text():
        text.tag_remove("found", "1.0", tk.END)
        search_term = find_entry.get()
        if search_term:
            start = "1.0"
            while True:
                pos = text.search(search_term, start, stopindex=tk.END)
                if not pos: break
                end = f"{pos}+{len(search_term)}c"
                text.tag_add("found", pos, end)
                start = end
            text.tag_config("found", background="yellow", foreground="black")

    def replace_all():
        search_term = find_entry.get()
        replace_term = replace_entry.get()
        if search_term:
            content = text.get("1.0", tk.END)
            new_content = content.replace(search_term, replace_term)
            text.delete("1.0", tk.END)
            text.insert("1.0", new_content)

    tk.Button(find_window, text="Find All", command=find_text).grid(row=0, column=2, padx=5)
    tk.Button(find_window, text="Replace All", command=replace_all).grid(row=1, column=2, padx=5)
    tk.Button(find_window, text="Close", command=find_window.destroy).grid(row=2, column=1, pady=10)


# --- Theme toggle function ---
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    theme = dark_theme if is_dark_mode else light_theme

    # Apply to ALL open tabs
    for tab_id in notebook.tabs():
        tab_frame = notebook.nametowidget(tab_id)
        for child in tab_frame.winfo_children():
            if isinstance(child, tk.Text):
                child.config(
                    bg=theme["bg"],
                    fg=theme["fg"],
                    insertbackground=theme["cursor"],
                    selectbackground=theme["select_bg"]
                )
    
    # Re-apply syntax highlighting for CURRENT tab
    apply_syntax_highlighting()

    # Apply to root window and status bar
    root.config(bg=theme["bg"])
    notebook.config() 
    status_bar.config(bg=theme["bg"])
    status_label.config(bg=theme["bg"], fg=theme["fg"])

# Font tags
def change_font_size(size):
    text = get_current_text_widget()
    if not text: return
    
    tag_name = f"size_{size}"
    text.tag_config(tag_name, font=("Helvetica", size))
    try:
        text.tag_add(tag_name, "sel.first", "sel.last")
    except tk.TclError:
        pass 

# Syntax highlighting
def apply_syntax_highlighting(event=None):
    text = get_current_text_widget()
    if not text: return
    
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


#Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

#Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Close Tab", command=close_current_tab)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create an edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo_text)
edit_menu.add_command(label="Redo", command=redo_text)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_separator()
edit_menu.add_command(label="Find & Replace", command=find_replace)

# Create a Format menu
format_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Format", menu=format_menu)
font_size_menu = tk.Menu(format_menu, tearoff=0)
format_menu.add_cascade(label="Font Size", menu=font_size_menu)
for size in [12, 14, 16, 18, 20, 24, 32]:
    font_size_menu.add_command(label=str(size), command=lambda s=size: change_font_size(s))

# Create a View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_theme)

#Keyboard shortcuts
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-z>", lambda event: undo_text())
root.bind("<Control-y>", lambda event: redo_text())
root.bind("<Control-h>", lambda event: find_replace())
root.bind("<Control-d>", lambda event: toggle_theme())
root.bind("<Control-a>", lambda event: select_all())
root.bind("<Control-w>", lambda event: close_current_tab())

root.protocol("WM_DELETE_WINDOW", on_closing)

# Create initial tab
create_editor_tab()

# Handle tab changes
notebook.bind("<<NotebookTabChanged>>", lambda e: update_status())

root.mainloop()