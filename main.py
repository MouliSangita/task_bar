import tkinter as tk

# Define a function to add a task to the list
def add_task():
    task = task_entry.get()
    if task != '':
        task_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)

# Define a function to remove the selected task from the list
def remove_task():
    selection = task_list.curselection()
    if len(selection) > 0:
        task_list.delete(selection[0])

# Create a GUI window
window = tk.Tk()
window.title('To-Do List')

# Create task label and entry field
task_label = tk.Label(window, text='Task:')
task_label.pack(padx=10, pady=10)
task_entry = tk.Entry(window)
task_entry.pack(padx=10, pady=10)

# Create add and remove buttons
button_frame = tk.Frame(window)
button_frame.pack(padx=10, pady=10)
add_button = tk.Button(button_frame, text='Add', command=add_task)
add_button.pack(side=tk.LEFT, padx=5)
remove_button = tk.Button(button_frame, text='Remove', command=remove_task)
remove_button.pack(side=tk.LEFT, padx=5)

# Create task list
task_list = tk.Listbox(window)
task_list.pack(padx=10, pady=10)

# Run the GUI loop
window.mainloop()
