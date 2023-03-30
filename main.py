# IMPORTS
import os
import openai
import time

def generate_cover_letter(experience, job_ad):
    content = ("This is the content of my resume: " + experience + 
               "Write a cover letter for the following job advert: " + 
               job_ad + " Keep it short. And make reference to my above resume. Include my name at the end. When referencing the job advert, Dont be too literal or too wordy.")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    )
    return completion.choices[0].message.content

def main():
    # CONSTANTS
    API_KEY = "API-KEY"
    RESUME_PATH = 'resume/experience.txt'
    ADVERTS_DIR = "Adverts/"
    OUTPUT_DIR = "outputs/"

    # API KEY
    openai.api_key = API_KEY

    # READ RESUME
    with open(RESUME_PATH, encoding="utf8") as f:
        experience = f.read()

    # LOOP THROUGH JOBS
    start_time = time.time()
    for count, filename in enumerate(os.listdir(ADVERTS_DIR), start=1):
        print(f"Current Job [{count}]: {filename}")

        # READ PERSPECTIVE JOB AD
        with open(os.path.join(ADVERTS_DIR, filename)) as f:
            job_ad = f.read()

        # API CALL
        chat_response = generate_cover_letter(experience, job_ad)

        # DUMP OUTPUT TO FILE
        with open(os.path.join(OUTPUT_DIR, f'{filename}_Output.txt'), 'w') as file:
            file.write(chat_response)

    # END MESSAGE + ELAPSED TIME
    input(f"\nCompleted all jobs [{count}] in {round((time.time() - start_time),2)} seconds.")

if __name__ == "__main__":
    main()
