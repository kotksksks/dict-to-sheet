import sv_ttk
from tkinter import ttk, font
from utils import load_data, insert_data, input_text, output_text, generate_random_output, number_frame, number_entry

sv_ttk.set_theme('light')


def create_gui(root):
    default_font = font.nametofont('TkDefaultFont')
    default_font.configure(size=12)

    input_label = ttk.Label(root, text='Type words and cats, e.g. "word 2"')
    input_label.grid(pady=5, padx=10, sticky='n')

    input_text.grid(pady=5, padx=10, sticky='n')

    button_frame = ttk.Frame(root)
    button_frame.grid(sticky='n')

    file_button = ttk.Button(button_frame, text='Open file...', command=load_data)
    file_button.grid(row=4, column=0, sticky='ew', padx=10)

    load_button = ttk.Button(button_frame, text='Record data', command=insert_data)
    load_button.grid(row=4, column=1, sticky='ew', padx=10)

    number_frame.grid(pady=50, sticky='n')

    number_label = ttk.Label(number_frame, text='Enter num')
    number_label.grid(row=5, column=1, padx=10, sticky='e')

    number_entry.grid(row=5, column=3, padx=10, sticky='w')

    ok_button = ttk.Button(number_frame, text='OK', command=generate_random_output, width=6)
    ok_button.grid(row=5, column=5, padx=10, sticky='w')

    output_label = ttk.Label(root, text='Enjoy the result')
    output_label.grid(padx=10, sticky='n')

    output_text.grid(pady=5, padx=10, sticky='n')

    root.mainloop()