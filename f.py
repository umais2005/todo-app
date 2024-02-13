import tkinter as tk


def button_click(event):
    # Get the widget ID from the event object
    button_id = event.widget.winfo_id()
    print("Button clicked. ID:", button_id)


root = tk.Tk()

# Define the number of buttons you want to create
num_buttons = 5

# Create buttons in a loop
for i in range(num_buttons):
    button = tk.Button(root, text=f"Button {i + 1}")
    button.grid(row=i, column=0)
    # Bind the button click event to the button_click function
    button.bind("<Button-1>", button_click)

root.mainloop()
