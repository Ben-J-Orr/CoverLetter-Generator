from dataclasses import dataclass


@dataclass
class GuiSettings:
    gpt_api_key: str = ""
    gpt_prompt: str = "Keep it short. And make reference to my above resume. Include my name at the end. When referencing the job advert, Dont be too literal or too wordy."
    gpt_model: str = "gpt-4"
    experience: str = "default value ha?"
