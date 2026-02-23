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

# Set window title
root.title("Simple Text Editor")

# Set window size
root.geometry("800x600")


# Create text editor area
text = tk.Text(
    root,                    # Parent window
    wrap=tk.WORD,            # Wrap text by words (not characters)
    font=("Helvetica", 18),   # Font style and size
    undo=True               # Enable undo functionality
)

# Make text area fill the entire window
# Rule of thumb: In tkinter pack(), always pack fixed-size widgets first (like status bars), then pack the expanding widget last.
text.pack(expand=True, fill=tk.BOTH)


# Create a Frame (an invisible container/box) at the bottom
status_bar = tk.Frame(root, height=20)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)  #stretches across the full width
# Create a StringVar — a "smart" variable
status_text = tk.StringVar()
status_text.set("Line: 1 | Column: 0")


#Put a Label inside the Frame, connected to the StringVar
status_label = tk.Label(status_bar, textvariable=status_text, anchor=tk.E, padx=10)
status_label.pack(fill=tk.X)


# Function to create a new file
def new_file():
      # Delete all text from the text box (from start to end)
      text.delete("1.0", tk.END)

      # Update the title to show "New Editor"
      root.title("New Editor")

      # Set the current file to None
      global current_file
      current_file = None

# Function to open an existing text file
def open_file():
      # Open a file dialog to select a text file
      file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
      )

      # If a file is selected, open it and display its contents
      if file_path:
            # Update the title to show the file name
            root.title(file_path.split("/")[-1])

            # Set the current file to the selected file
            global current_file
            current_file = file_path    

            # Open the file and display its contents in the text box
            with open(file_path, "r") as file:
                  # Clear the old text from the text box
                  text.delete("1.0", tk.END)
                  # Insert the contents of the file into the text box
                  text.insert(tk.END, file.read())
                
            text.edit_modified(False)
           

# Function to save the current text to a file
def save_file():
    global current_file
    # If there is a current file, save the text to it
    if current_file:
        # Open the file in write mode
        with open(current_file, "w") as file:
            # Write the text from the text box to the file
            file.write(text.get("1.0", tk.END))
        # Show a success message
        messagebox.showinfo("Success", "File saved successfully!")
        text.edit_modified(False)       # Reset the "modified" flag
        root.title(root.title().lstrip("*").split("/")[-1].split(".")[0])  # Remove * from title
    else:
        # open a file dialog to select a file to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",  # Default file extension
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")] # Allow only .txt files
        )

        # If a file is selected, save the text to it
        if file_path:
            # Remember the path!
            current_file = file_path   
            # Update the title to show the file name    
            root.title(file_path) 
            # Open the file in write mode
            with open(file_path, "w") as file:
                # Write the text from the text box to the file
                file.write(text.get("1.0", tk.END))
            # Show a success message
            messagebox.showinfo("Success", "File saved successfully!")
            text.edit_modified(False)       # Reset the "modified" flag
            root.title(root.title().lstrip("*").split("/")[-1].split(".")[0]) # Remove * from title
        else:
            messagebox.showerror("Error", "No file selected!")

# A function that reads cursor position and updates the status bar
def update_status(event=None):
      # 1. Get cursor position (Line & Column)
    position = text.index(tk.INSERT)
    line, column = position.split(".")
    # 2. Get all text content
    # "1.0" = start of text
    # "end-1c" = end of text (minus the automatic trailing newline)
    content = text.get("1.0", "end-1c")
    # 3. Count words
    # .split() splits by whitespace (spaces, tabs, newlines)
    word_count = len(content.split()) if content else 0
    # 4. Count characters
    # Calculate length of the string
    char_count = len(content)
    # 5. Update Status Bar
    status_text.set(
        f"Line: {line} | Column: {column} | Words: {word_count} | Chars: {char_count}"
    )

# Function to undo the last action
def undo_text():
    try:                        # "Try to do this..."
        text.edit_undo()        #   → attempt undo
    except tk.TclError:         # "If it fails with TclError..."
        pass   

# Function to redo the last action
def redo_text():
    try:
        text.edit_redo()
    except tk.TclError:
        pass

# Function to mark text as modified (shows * in title)
def on_text_change(event=None):
    # text.edit_modified() returns True if text has been changed
    if text.edit_modified():
        title = root.title()
        # Add * at the beginning if not already there
        if not title.startswith("*"):
            root.title("*" + title)


# Function to handle window close — asks to save if unsaved changes
def on_closing():
    global current_file
    # Check if there are any unsaved changes
    if text.edit_modified():
        # Show a dialog with 3 buttons: Yes / No / Cancel
        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save before closing?"
        )
        # answer = True (Yes), False (No), None (Cancel)

        if answer is True:       # User clicked "Yes" → save then close
            save_file()
            #root.title((current_file or "Simple Text Editor").split("/")[-1])
            root.destroy()
        else:    # User clicked "No" → close without saving
            #root.title((current_file or "Simple Text Editor").split("/")[-1])
            root.destroy()
        # If answer is None → User clicked "Cancel" → do nothing (stay open)
    else:
        #root.title((current_file or "Simple Text Editor").split("/")[-1])
        root.destroy()           # No changes → just close

def cut_text():
    text.event_generate("<<Cut>>")      # Triggers built-in cut
def copy_text():
    text.event_generate("<<Copy>>")     # Triggers built-in copy
def paste_text():
    text.event_generate("<<Paste>>")    # Triggers built-in paste
def select_all():
    text.tag_add("sel", "1.0", "end-1c")  # Select from start to end
    return "break"      

# Function to find and replace text window render
def find_replace():
    # Create a new popup window
    find_window = tk.Toplevel(root)
    find_window.title("Find & Replace")
    find_window.geometry("400x150")
    find_window.resizable(False, False)
    # --- Find row ---
    tk.Label(find_window, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    find_entry = tk.Entry(find_window, width=30)
    find_entry.grid(row=0, column=1, padx=5, pady=5)
    # --- Replace row ---
    tk.Label(find_window, text="Replace:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    replace_entry = tk.Entry(find_window, width=30)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)

    # --- Buttons ---
    tk.Button(find_window, text="Find All", command=lambda: find_text(find_entry)).grid(row=0, column=2, padx=5)
    tk.Button(find_window, text="Replace All", command=lambda: replace_all(find_entry, replace_entry)).grid(row=1, column=2, padx=5)
    tk.Button(find_window, text="Close", command=find_window.destroy).grid(row=2, column=1, pady=10)


  # --- Find button: highlights all matches ---
def find_text(find_entry):
    # Remove old highlights
    text.tag_remove("found", "1.0", tk.END)
    
    search_term = find_entry.get()
    if search_term:
        start = "1.0"
        while True:
            # Search for the term starting from 'start' position
            pos = text.search(search_term, start, stopindex=tk.END)
            if not pos:
                break   # No more matches
            # Calculate end position
            end = f"{pos}+{len(search_term)}c"
            # Highlight the found text
            text.tag_add("found", pos, end)
            start = end   # Continue searching after this match
        # Style the highlights: yellow background
        text.tag_config("found", background="yellow", foreground="black")


    # --- Replace All button ---
def replace_all(find_entry, replace_entry):
    search_term = find_entry.get()
    replace_term = replace_entry.get()
    if search_term:
        # Get all text, replace, and put it back
        content = text.get("1.0", tk.END)
        new_content = content.replace(search_term, replace_term)
        text.delete("1.0", tk.END)
        text.insert("1.0", new_content)

# --- Theme toggle function ---
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode   # Flip True ↔ False

    # Pick the right theme
    theme = dark_theme if is_dark_mode else light_theme

    # Apply to text widget
    text.config(
        bg=theme["bg"],
        fg=theme["fg"],
        insertbackground=theme["cursor"],         # Cursor color
        selectbackground=theme["select_bg"]       # Selection color
    )

    # Apply to root window and status bar
    root.config(bg=theme["bg"])
    status_bar.config(bg=theme["bg"])
    status_label.config(bg=theme["bg"], fg=theme["fg"])
    # Re-apply syntax highlighting with new theme colors
    apply_syntax_highlighting()

# Create a dictionary to keep track of font tags
# We need to create a new tag for each size, e.g., "size12", "size14"
def change_font_size(size):
    # 1. Create a tag name, e.g., "size_20"
    tag_name = f"size_{size}"
    
    # 2. Configure the tag with the font details
    # We use "Helvetica" as the base font family
    text.tag_config(tag_name, font=("Helvetica", size))
    
    # 3. Apply this tag to the CURRENT SELECTION
    try:
        # "sel.first" to "sel.last" covers the highlighted text
        text.tag_add(tag_name, "sel.first", "sel.last")
        
        # Optional: Remove other size tags from this area so they don't overlap
        # (For a simple start, we can just add the new one, as the newest tag usually wins)
    except tk.TclError:
        # No text selected -> Do nothing (or apply to whole doc if you prefer)
        pass 


# Function to highlight Python keywords
def apply_syntax_highlighting(event=None):
    # 1. Clear existing highlights (remove "keyword" tag from all text)
    text.tag_remove("keyword", "1.0", tk.END)
    
    # 2. Configure the "keyword" tag (e.g., orange or blue)
    # We choose a color that works well in dark/light themes
    keyword_color = "orange" if is_dark_mode else "blue"
    text.tag_config("keyword", foreground=keyword_color)
    
    # 3. Get all Python keywords (def, class, if, else, etc.)
    keywords = keyword.kwlist
    
    # 4. Search and highlight each keyword
    for kw in keywords:
        start = "1.0"
        while True:
            # Search for keyword
            # matches=True -> full word match only
            pos = text.search(kw, start, stopindex=tk.END, count=tk.IntVar())
            
            if not pos:
                break
            
            # Use regex logic-like check to ensure whole word match manually if needed,
            # but simple search is a good start. 
            
            # Simple approach: Find end position
            end = f"{pos}+{len(kw)}c"
            
            # Check if it's a whole word (simple check: precede/succeed by whitespace/punctuation?)
            # For simplicity in Step 10, we'll just highlight all occurrences first.
            text.tag_add("keyword", pos, end)
            start = end


#Create a menu bar
menu_bar = tk.Menu(root)

#Attach the menu bar to the root window
root.config(menu=menu_bar)

#Create a file menu
# Dropdown under File which has options like New, Open, Save, Exit
file_menu = tk.Menu(menu_bar, tearoff=0)

#Add the file menu to the menu bar
menu_bar.add_cascade(label="File", menu=file_menu)

#Add commands to the file menu
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
# Add a separator line in menu
file_menu.add_separator()
# Add Exit option to close the application
file_menu.add_command(label="Exit", command=root.quit)

# Create an edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=text.edit_undo)
edit_menu.add_command(label="Redo", command=text.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)

# In your edit menu section:
edit_menu.add_separator()
edit_menu.add_command(label="Find & Replace", command=find_replace)

# Create a View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_theme)

# Create a Format menu
format_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Format", menu=format_menu)

# Add font size submenu
font_size_menu = tk.Menu(format_menu, tearoff=0)
format_menu.add_cascade(label="Font Size", menu=font_size_menu)

# Add options: 12, 14, 16, 18, 20, 24, 32
# We use lambda to pass the specific size to the function
font_size_menu.add_command(label="12", command=lambda: change_font_size(12))
font_size_menu.add_command(label="14", command=lambda: change_font_size(14))
font_size_menu.add_command(label="16", command=lambda: change_font_size(16))
font_size_menu.add_command(label="18", command=lambda: change_font_size(18))
font_size_menu.add_command(label="20", command=lambda: change_font_size(20))
font_size_menu.add_command(label="24", command=lambda: change_font_size(24))
font_size_menu.add_command(label="32", command=lambda: change_font_size(32))

#Create a help menu
# help_menu = tk.Menu(menu_bar, tearoff=0)
# menu_bar.add_cascade(label="Help", menu=help_menu)
# help_menu.add_command(label="About", command=show_about)

#Keyboard shortcuts
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-z>", lambda event: undo_text())
root.bind("<Control-y>", lambda event: redo_text())
# In your shortcuts section:
root.bind("<Control-h>", lambda event: find_replace())

# Handle window close button (X)
root.protocol("WM_DELETE_WINDOW", on_closing)

root.bind("<Control-d>", lambda event: toggle_theme())


# Call update_status whenever the cursor moves
text.bind("<KeyRelease>", lambda event: update_status())          # After any key press
# text.bind("<ButtonRelease-1>", lambda event: update_status()) # After mouse click
#   ↑ We use "Release" not "Press" because:
#   - On Press: cursor is still at the OLD position
#   - On Release: cursor has MOVED to the NEW position

# Detect when text is modified (<<Modified>> fires when text changes)
text.bind("<<Modified>>", lambda event: on_text_change())

# Re-highlight on every key release (so it updates as you type)
text.bind("<KeyRelease>", lambda event: [update_status(), apply_syntax_highlighting()])


# Run the application continuously
# Starts and keeps the window open
root.mainloop()