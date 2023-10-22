from selenium import webdriver
import os
import tkinter as tk
from tkinter import Entry, Button, Label
from tkinter import ttk

CACHE_FILE = 'gui_cache.txt'

def fetch_rendered_html(url):
    chrome_options = webdriver.ChromeOptions()
    if not os.path.exists("cache"):
        os.makedirs("cache")
    cache_folder_path = os.path.abspath("cache")
    chrome_options.add_argument(r"--user-data-dir="+cache_folder_path)
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    html_content = browser.page_source
    browser.quit()

    return html_content

def fetch_liges(url):
    response = fetch_rendered_html(url)
    liges=response.split(r'Liges</span></span><span class="postprofile-field-content"><div class="field_uneditable">')[1].split(r'</div></span></div><div class="autres_comptes">')[0]
    return liges


def delete_entry(row):
    """Delete a specific row and adjust the remaining rows."""
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) == row:
            widget.destroy()

    for r in range(row + 1, len(entries) + 1):
        for widget in window.grid_slaves(row=r):
            widget.grid(row=r - 1)

    del entries[row - 1]
    update_buttons()


def update_buttons():
    """Update the delete buttons' commands since the row indices change."""
    for i, (_, _, btn) in enumerate(entries):
        btn.config(command=lambda i=i: delete_entry(i + 1))


def add_entry():
    row_num = len(entries) + 1

    new_name_label = Label(window, text="Name:")
    new_name_label.grid(row=row_num, column=0)

    new_name_entry = Entry(window)
    new_name_entry.grid(row=row_num, column=1)

    new_url_label = Label(window, text="URL:")
    new_url_label.grid(row=row_num, column=2)

    new_url_entry = Entry(window)
    new_url_entry.grid(row=row_num, column=3)

    delete_btn = Button(window, text="Delete", command=lambda: delete_entry(row_num))
    delete_btn.grid(row=row_num, column=4, padx=10)

    entries.append((new_name_entry, new_url_entry, delete_btn))
    update_buttons()

def show_popup(message):
    """Display a popup window with the given message."""
    popup = tk.Toplevel(window)
    popup.title("Message")

    label = tk.Label(popup, text=message)
    label.pack(pady=20, padx=20)

    ok_button = tk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=10)

def populate_dict():
    result = {}
    for name_entry, url_entry, _ in entries:
        name = name_entry.get()
        url = url_entry.get()
        if name and url:  # Ensure both name and URL are provided
            result[name] = url

    progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
    progress.grid(row=101, column=1, columnspan=3, pady=10)
    window.update()

    finalstring = ""
    num_keys = len(result.keys())
    for idx, key in enumerate(result.keys()):
        print(key)
        finalstring += key + " : " + fetch_liges(result[key]) + "\n"
        progress['value'] = (idx + 1) / num_keys * 100
        window.update()

    show_popup(finalstring)

def load_cache():
    """Load cached data from the file and populate the GUI."""
    if not os.path.exists(CACHE_FILE):
        return

    with open(CACHE_FILE, 'r') as f:
        for line in f:
            name, url = line.strip().split(',')
            add_entry()
            entries[-1][0].insert(0, name)  # Set name
            entries[-1][1].insert(0, url)  # Set URL

def save_cache():
    """Save the current entries to the cache file."""
    with open(CACHE_FILE, 'w') as f:
        for name_entry, url_entry, _ in entries:
            name = name_entry.get()
            url = url_entry.get()
            f.write(f"{name},{url}\n")


window = tk.Tk()
window.title("Liste Liges par Personnage")

entries = []

if os.path.exists(CACHE_FILE):
    load_cache()
else:
    add_entry()

add_button = Button(window, text="Add Line", command=add_entry)
add_button.grid(row=100, column=1, pady=20)  # Using a high row number to ensure it's always at the bottom

populate_button = Button(window, text="Lister Liges", command=populate_dict)
populate_button.grid(row=100, column=3, pady=20)

window.protocol("WM_DELETE_WINDOW", lambda: (save_cache(), window.destroy()))

window.mainloop()