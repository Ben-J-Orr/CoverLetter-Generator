import openai


class GptService:
    def __init__(self, key, model="gpt-4"):
        self._client = openai.OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=key,
        )
        self._model = model

    def generate_cover_letter(self, experience, job_ad, additional_prompt_options=""):
        try:
            print("Ask  GPT")
            content = (
                f"This is the content of my resume: {experience} " +
                f"Write a cover letter for the following job advert: " +
                f"{job_ad + additional_prompt_options}"
            )
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": content}]
            )
            print("Answer GPT")
            return completion.choices[0].message.content
        except Exception as e:
            return str(e)
