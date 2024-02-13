from datetime import datetime
import random
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def generate_color():
    r = hex(random.randint(100, 255))[2:]
    g = hex(random.randint(100, 255))[2:]
    b = hex(random.randint(100, 255))[2:]
    return f'#{r}{g}{b}'


conn = sqlite3.connect("todo.db")
cursor = conn.cursor()


# cursor.execute("""DELETE FROM tasks
#         """)
#
# conn.commit()


class Taskitem(ttk.Label):
    def __init__(self, master, category=None, **kwargs):
        super().__init__(master)
        self.kwargs = kwargs
        self.category = category
        color = self.find_color() if category else None
        # print(color)
        if color:
            kwargs.update({"background": color[0]})
        else:
            kwargs.update({"background": "#c7dead"})
        self.configure(**kwargs, font='Arial', borderwidth=10, relief='solid', anchor="center")

    def __repr__(self):
        return f'{self.kwargs["text"]}'

    def find_color(self):
        cursor.execute("SELECT color FROM categories WHERE category = ?", (self.category,))
        # print(cursor.fetchone())
        color = cursor.fetchone()
        if color:
            return color


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x700')
        self.root.title('Todo App')
        # for handling different categories
        cursor.execute("SELECT category FROM categories")
        self.categories = set(cursor.fetchall())

        main_heading = ttk.Label(self.root, text="To Do App", font=('Arial', 30))
        main_heading.pack(padx=10, pady=10)
        options_frame = ttk.Frame(self.root)
        options_frame.pack()
        addbtn = ttk.Button(options_frame, text="Add", command=self.show_input)
        addbtn.grid(row=0, column=0)

        ttk.Label(options_frame, text="SortBy").grid(row=0, column=1)
        self.sortby = tk.StringVar()
        ttk.OptionMenu(options_frame, self.sortby, None, "None", "Category", "Description",
                       "Priority", command=self.show_tasks).grid(row=0, column=2)
        # self.labelframe handles input and the column headers
        self.labelframe = ttk.Frame(self.root)
        self.labelframe.pack(fill='both')
        self.labelframe.columnconfigure((0, 1, 3, 4, 5), weight=1)
        self.labelframe.columnconfigure(3, weight=1)
        ttk.Label(self.labelframe, text="Priority number", anchor="center").grid(row=0, column=0)
        ttk.Label(self.labelframe, text="Task Description", anchor="center").grid(row=0, column=1)
        ttk.Label(self.labelframe, text="Task Category", anchor="center").grid(row=0, column=2)
        ttk.Label(self.labelframe, text="Task added Date", anchor="center").grid(row=0, column=3)

        # The container for the tasks
        self.listitems = ttk.Frame(self.root, style="list.TFrame")
        self.listitems.pack(fill='both', expand=True)
        ttk.Style().configure("list.TFrame", background='#c7dead')
        self.listitems.columnconfigure(0, weight=1)
        self.listitems.columnconfigure(1, weight=3)
        self.listitems.columnconfigure(2, weight=1)
        self.listitems.columnconfigure(3, weight=1)
        self.show_tasks()
        # ttk.Label(self.listitems, text="priorityy number").grid(row=0, column=0, sticky='')
        # ttk.Label(self.listitems, text="Task Description").grid(row=0, column=1, sticky="")
        # ttk.Label(self.listitems, text="Task Category").grid(row=0, column=2)

    def show_tasks(self, criteria=None):
        self.criteria = criteria
        if not criteria or criteria == "None":
            cursor.execute("SELECT * FROM tasks")
        else:
            criteria = criteria.lower()
            cursor.execute(f"SELECT * FROM tasks ORDER BY {criteria}")

        tasks = cursor.fetchall()
        self.id_row_mapping = {}
        for i, task in enumerate(tasks):
            new_row = i + 1
            taskid, priority, desc, category, date = task  # unpacks task tuple/row from the db

            prioritylbl = Taskitem(self.listitems, category=category, text=priority)
            prioritylbl.grid(row=new_row, column=0, sticky='new')

            desclbl = Taskitem(self.listitems, category=category, text=desc)
            desclbl.grid(row=new_row, column=1, sticky='new')

            categorylbl = Taskitem(self.listitems, category=category, text=category)
            categorylbl.grid(row=new_row, column=2, sticky="new")

            datelbl = Taskitem(self.listitems, category=category, text=date)
            datelbl.grid(row=new_row, column=3, sticky='new')

            deletebtn = ttk.Button(self.listitems, text="Delete")
            deletebtn.bind('<Button-1>', self.delete_task)
            deletebtn.grid(row=new_row, column=4, sticky='n')
            updatebtn = ttk.Button(self.listitems, text="Update")
            updatebtn.grid(row=new_row, column=5, sticky='n')
            self.id_row_mapping[deletebtn.winfo_id()] = (
                taskid, new_row)  # this maps the task id and the task row to the button id
            print(self.id_row_mapping[deletebtn.winfo_id()])

    def show_input(self):
        self.task_priority = ttk.Entry(self.labelframe, width=5)
        self.task_priority.grid(row=1, column=0, sticky="ew")
        self.task_desc = ttk.Entry(self.labelframe)
        self.task_desc.grid(row=1, column=1, sticky="we")
        self.task_category = ttk.Entry(self.labelframe)
        self.task_category.grid(row=1, column=2, sticky="ew")
        self.confirmbtn = ttk.Button(self.labelframe, text="Confirm", command=self.refresh)
        self.confirmbtn.grid(row=1, column=3, sticky="ew")
        self.confirmbtn = ttk.Button(self.labelframe, text="Cancel", command=self.destroy_input)
        self.confirmbtn.grid(row=1, column=4, sticky="we")

    def refresh(self):
        record = self.add_record()  # gets the record that is added
        if record:  # True if the entries are validated, and the inputs will be closed and menu will be updated
            self.destroy_input()
            self.show_tasks()  # self.criteria

    def destroy_input(self):
        for child in self.labelframe.grid_slaves():
            if child.grid_info()['row'] == 1:
                child.destroy()

    def delete_task(self, event):
        taskinfo = self.id_row_mapping[event.widget.winfo_id()]
        taskid = taskinfo[0]
        print(taskid)
        cursor.execute(f"DELETE FROM tasks WHERE id = {taskid}")
        conn.commit()
        for taskitem in self.listitems.grid_slaves():
            taskitem.destroy()
        self.show_tasks(self.criteria)

    def add_record(self):
        curr_priority = self.task_priority.get()
        curr_description = self.task_desc.get()
        curr_category = self.task_category.get().lower().strip()
        self.add_category(curr_category)
        curr_date = datetime.utcnow().strftime('%d-%m-%Y')
        # validation
        # check empty
        if "" in (curr_description, curr_priority):
            messagebox.showwarning("Invalid input", "Description and priority cannot be empty")
            return False
        try:
            cursor.execute("INSERT INTO tasks(priority, description, category, date) VALUES (?,?,?,?)",
                           (curr_priority, curr_description, curr_category, curr_date))
        except sqlite3.IntegrityError:
            messagebox.showwarning("Invalid input", f"You already have a task named {curr_description}")
            return False
        conn.commit()
        return True

    # this will add a color only if the color is unique and diff than any other category, hence the while try except
    def add_category(self, curr_category):
        if curr_category not in (self.categories, ""):  # and len(self.categories) < 10:
            while True:
                try:
                    cursor.execute("INSERT INTO categories(category, color) VALUES (?,?)",
                                   (curr_category, generate_color()))
                except sqlite3.IntegrityError:
                    pass
                else:
                    break


def main():
    root = tk.Tk()
    app = GUI(root)
    print(app.id_row_mapping)
    root.mainloop()


if __name__ == "__main__":
    # generate_color()
    main()
