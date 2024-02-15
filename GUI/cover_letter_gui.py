import json
import os
import tkinter as tk
from tkinter import ttk, scrolledtext

import appdirs

from GUI.cfg import GuiSettings
from GUI.snackbar import GuiSnackbar
from ai import GptService
from fileutil import read_config_from_file


class CLGui:
    CONFIG_NAME = "cfg.json"

    def __init__(self, parent: tk.Tk = None, default_cfg_file_path: str = None):
        self._parent = parent
        self._root_dir = os.path.dirname(os.path.abspath(__file__))
        self._default_cfg_file_path = default_cfg_file_path
        self._cfg = self._init_cfg()

        self._parent.title("CoverLetter-Generator")

        self._init_widows_size()
        geometry_str = self._get_geometry_str()
        self._parent.geometry(geometry_str)

        self._notebook = ttk.Notebook(self._parent)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._snackbar = GuiSnackbar(self._parent)

    def add_letter_generator_page(self):
        lg_frame = ttk.Frame(self._notebook)
        self._notebook.add(lg_frame, text='Letter generator')

        generate_button = ttk.Button(
            lg_frame,
            text="Generate",
            command=lambda: self.generate_handler(result_input, vacancy_input),
        )
        generate_button.pack(side=tk.RIGHT, padx=5, pady=5)

        vacancy_input = self._get_text_input(
            lg_frame,
            "Insert vacancy description here.",
            height=int(self._window_height * 0.45)
        )

        result_input = self._get_text_input(lg_frame, readonly=True)

    def add_experience_page(self):
        exp_frame = ttk.Frame(self._notebook)
        self._notebook.add(exp_frame, text='Experience')
        self._add_settings_text_input_field(
            parent=exp_frame,
            value=self._cfg.experience,
            update_func=self._update_settings_experience,
        )

    def add_settings_page(self):
        settings_frame = ttk.Frame(self._notebook)
        self._notebook.add(settings_frame, text='Settings')
        self._add_input_field(
            parent=settings_frame,
            value=self._cfg.gpt_api_key,
            label_text='Gpt api-key',
            update_func=self._update_settings_api_key
        )
        self._add_input_field(
            parent=settings_frame,
            value=self._cfg.gpt_prompt,
            label_text='Gpt Extra Prompts:',
            update_func=self._update_settings_prompt
        )
        self._add_input_field(
            parent=settings_frame,
            value=self._cfg.gpt_model,
            label_text='Gpt Model:',
            update_func=self._update_settings_gpt_model
        )

    def _add_settings_text_input_field(self, parent, value, update_func):
        input_ = self._get_text_input(parent, value)

        def update_settings(_):
            update_func(input_.get("1.0", tk.END).strip())
            self._snackbar.show("Settings updated successfully!")

        input_.bind("<KeyRelease>", update_settings)

        line_size = input_.tk.call("font", "metrics", input_.cget("font"), "-linespace")
        viewport_height = int(self._window_height / line_size)

        input_.config(height=viewport_height)

    def generate_handler(self, res: scrolledtext.ScrolledText, vacancy: scrolledtext.ScrolledText):
        def _update_res_msg(text):
            res.config(state=tk.NORMAL)
            res.delete('1.0', tk.END)
            res.insert(tk.END, text)
            res.config(state=tk.DISABLED)

        def _get_gpt_answer():
            gpt_service = GptService(
                key=self._cfg.gpt_api_key
            )
            answer = gpt_service.generate_cover_letter(
                experience=self._cfg.experience,
                job_ad=vacancy_input_value
            )
            _update_res_msg(answer)

        _update_res_msg("Generating a cover letter, please wait...")

        vacancy_input_value = vacancy.get("1.0", tk.END).strip()
        res.after(500, _get_gpt_answer)

    def _get_text_input(self, parent, value="", readonly=False, height=-1):
        if readonly:
            input_ = scrolledtext.ScrolledText(parent, wrap=tk.WORD, state=tk.DISABLED, bg='gainsboro')
        else:
            input_ = scrolledtext.ScrolledText(parent, wrap=tk.WORD)

        input_.insert(tk.END, value)
        input_.pack(fill=tk.BOTH, padx=5, pady=5)

        if height > 0:
            line_size = input_.tk.call("font", "metrics", input_.cget("font"), "-linespace")
            viewport_height_lines = int(height / line_size)
            input_.config(height=viewport_height_lines)

        return input_

    def _init_widows_size(self):
        self._window_width = int(self._parent.winfo_screenwidth() * 0.5)
        self._window_height = int(self._parent.winfo_screenheight() * 0.5)

    def _get_geometry_str(self):
        screen_width = self._parent.winfo_screenwidth()
        screen_height = self._parent.winfo_screenheight()

        return f"{self._window_width}x{self._window_height}+{screen_width // 2 - self._window_width // 2}+{screen_height // 2 - self._window_height // 2}"

    def _add_input_field(self, parent, value, label_text, update_func):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=5, pady=5)

        label = ttk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=5)

        input_ = tk.StringVar()
        input_.set(value)

        def update_settings(_):
            update_func(input_.get())
            self._snackbar.show("Settings updated successfully!")

        file_entry_frame = ttk.Frame(frame)
        file_entry_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        file_entry = ttk.Entry(file_entry_frame, textvariable=input_, width=1)
        file_entry.pack(fill=tk.X, padx=5, pady=5, expand=True)

        file_entry.bind("<KeyRelease>", update_settings)

    def _update_settings_api_key(self, value):
        self._cfg.gpt_api_key = value
        self._dump_config()

    def _update_settings_experience(self, value):
        self._cfg.experience = value
        self._dump_config()

    def _update_settings_prompt(self, value):
        self._cfg.gpt_prompt = value
        self._dump_config()

    def _update_settings_gpt_model(self, value):
        self._cfg.gpt_model = value
        self._dump_config()

    def _dump_config(self):
        # not the best way to save, for now ok
        json_val = json.dumps(vars(self._cfg), indent=2)
        with open(self._cfg_path, "w") as f:
            f.write(json_val)

    def _init_cfg(self):
        os_config_dir = appdirs.user_config_dir(appname='.cl_generator')
        os.makedirs(os_config_dir, exist_ok=True)
        self._cfg_path = os.path.join(os_config_dir, self.CONFIG_NAME)
        cfg = GuiSettings()

        if os.path.exists(self._cfg_path) and os.path.isfile(self._cfg_path):
            # hooray duplication :)
            # if continue to grow make some middlaware remapper or something
            file_cfg = read_config_from_file(self._cfg_path)

            cfg.gpt_api_key = file_cfg.get("gpt_api_key", "<insert your key>")
            cfg.gpt_prompt = file_cfg.get("gpt_prompt", cfg.gpt_prompt)
            cfg.experience = file_cfg.get("experience", "<insert your experience>")
            cfg.gpt_model = file_cfg.get("gpt_model", cfg.gpt_model)
        else:
            file_cfg = read_config_from_file(self._default_cfg_file_path)
            cfg.gpt_api_key = file_cfg.get("api-key", "<insert your key>")
            cfg.gpt_prompt = file_cfg.get("additional_prompt_options", cfg.gpt_prompt)
            cfg.experience = "<insert your experience>"

        return cfg
