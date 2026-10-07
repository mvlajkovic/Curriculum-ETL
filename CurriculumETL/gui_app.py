import time
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from gui.lesson_info_loader import load_lesson_info

from database.db import get_connection, sanitize
from database.transaction import TransactionManager
from database.repositories.lesson import search_lessons

WINDOW_TITLE: str     = "Lesson Search"
WINDOW_SIZE: str      = "1000x600"
WINDOW_ICON_PATH: str = "icon.png"
THEME: str            = "alt"

class GuiApp:
    def __init__(self):
        ### GUI WINDOW INIT ###
        self.root: tk.Tk = tk.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title(WINDOW_TITLE)
        self.root.bind("<Return>", lambda x: self.search())

        if THEME in ttk.Style().theme_names():
            ttk.Style().theme_use(THEME)

        # Window icon.
        if Path(WINDOW_ICON_PATH).is_file():
            self.root.iconphoto(
                True, tk.PhotoImage(file=WINDOW_ICON_PATH)
            )

        main_frame = tk.Frame(self.root, bd=4, relief=tk.GROOVE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ### SEARCH PANEL ###
        search_frame = tk.Frame(main_frame, bd=4, relief=tk.GROOVE)
        search_frame.pack(side=tk.LEFT, anchor="n", padx=5, pady=5, ipadx=5, ipady=5)

        # Course code input.
        tk.Label(search_frame, anchor="w", width=14, text="COURSE CODE").grid(row=0, column=0)
        self.course_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.course_sterm
        ).grid(row=0, column=1)

        # Title input.
        tk.Label(search_frame, anchor="w", width=14, text="TITLE").grid(row=1, column=0)
        self.title_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.title_sterm
        ).grid(row=1, column=1)

        # Lesson number input.
        tk.Label(search_frame, anchor="w", width=14, text="LESSON NUMBER").grid(row=2, column=0)
        self.lesson_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.lesson_sterm
        ).grid(row=2, column=1)

        # Year input.
        tk.Label(search_frame, anchor="w", width=14, text="YEAR").grid(row=3, column=0)
        self.year_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.year_sterm
        ).grid(row=3, column=1)

        # Author input.
        tk.Label(search_frame, anchor="w", width=14, text="AUTHOR").grid(row=4, column=0)
        self.author_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.author_sterm
        ).grid(row=4, column=1)

        # File ID input.
        tk.Label(search_frame, anchor="w", width=14, text="FILE ID").grid(row=5, column=0)
        self.file_id_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.file_id_sterm
        ).grid(row=5, column=1)

        # Clear button.
        tk.Button(
            search_frame,
            text="CLEAR",
            command=lambda: self.clear_input(),
            width=15
        ).grid(row=6, column=1, pady=(10, 0))

        # Search button.
        tk.Button(
            search_frame,
            text="SEARCH",
            command=lambda: self.search(),
            fg="white", bg="sea green",
            width=15
        ).grid(row=7, column=1, pady=(5, 0))

        ### SEARCH RESULTS LABEL ###
        self.info_label = tk.Label(
            main_frame, anchor="center", width=100, text=""
        )
        self.info_label.pack(side=tk.BOTTOM)

        ### TREEVIEW PANEL ###
        self.tree = ttk.Treeview(main_frame, show="tree")
        self.tree.bind("<Control-c>", self.handle_copy)
        self.tree.tag_bind("lesson", "<<TreeviewOpen>>", self.on_row_expand)
        self.tree.tag_bind("lesson", "<<TreeviewClose>>", self.on_row_collapse)
        self.tree.tag_configure("lesson", foreground="maroon")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    # Run the application and show the window.
    def run(self):
        self.root.mainloop()

    # Called when user presses enter or the search button.
    def search(self):
        start_time = time.perf_counter()
        conn = get_connection()

        self.tree.delete(*self.tree.get_children())

        if not conn:
            self.tree.insert("", "end", text="Couldn't connect to the database.")
            return

        try:
            with TransactionManager(conn) as cursor:
                result = search_lessons(
                    cursor,
                    self.course_sterm.get(),
                    self.title_sterm.get(),
                    self.lesson_sterm.get(),
                    self.year_sterm.get(),
                    self.author_sterm.get(),
                    self.file_id_sterm.get()
                )

                if len(result) < 1:
                    self.tree.insert("", "end", text="No results.")

                for row in result:
                    id = row.id
                    if not id:
                        continue

                    course_code = sanitize(row.course_code)
                    lesson_number = sanitize(row.lesson_number)
                    academic_year = sanitize(row.academic_year)
                    title = sanitize(row.title, True)

                    self.tree.insert(
                        "", "end", id,
                        tags=["lesson"],
                        text=f"#{id} - {course_code} - {lesson_number} - {academic_year} - {title}"
                    )

                    self.tree.insert(id, "end", text="Loading...")

                self.info_label.config(
                    text=f"Found {len(result)} results in {round(time.perf_counter() - start_time, 2)} seconds."
                )
        finally:
            conn.close()

    # Load all lesson data when user expands a lesson item.
    # Called when user expands a lesson item.
    def on_row_expand(self, event):
        focus: str = self.tree.focus()
        if not focus:
            return

        lesson_id: int = 0
        try:
            lesson_id = int(focus)
        except ValueError:
            return

        conn = get_connection()
        if conn:
            try:
                with TransactionManager(conn) as cursor:
                    load_lesson_info(
                        cursor, lesson_id, self.tree
                    )
            finally:
                conn.close()

    # Unload all additional info for a loaded lesson item.
    # Called when user closes an opened lesson item.
    def on_row_collapse(self, event):
        focus: str = self.tree.focus()
        if not focus:
            return
        
        self.tree.delete(*self.tree.get_children(focus))
        self.tree.insert(focus, "end", text="Loading...")

    # Copy the focused item in the Treeview.
    # Called when user presses Ctrl+C.
    def handle_copy(self, event):
        focus: str = self.tree.focus()
        if not focus:
            return

        text: str = self.tree.item(focus, "text")
        if not text:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    # Called when user presses the clear button.
    # Clears all search fields.
    def clear_input(self):
        self.course_sterm.set("")
        self.title_sterm.set("")
        self.lesson_sterm.set("")
        self.year_sterm.set("")
        self.author_sterm.set("")
        self.file_id_sterm.set("")

def main():
    app = GuiApp()
    app.run()

if __name__ == "__main__":
    main()
