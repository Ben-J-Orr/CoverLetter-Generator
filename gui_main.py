import os
import tkinter as tk

from GUI.cover_letter_gui import CLGui

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    form = tk.Tk()

    cfg_path = os.path.join(PROJ_DIR, "config.json")

    app = CLGui(default_cfg_file_path=cfg_path, parent=form)
    app.add_letter_generator_page()
    app.add_experience_page()
    app.add_settings_page()

    form.mainloop()
