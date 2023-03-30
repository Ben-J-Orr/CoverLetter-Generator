# IMPORTS #
import os
import openai
import time
start_time = time.time()
# API KEY #
openai.api_key = "API-KEY"
count = 1
# READ RESUME # 
with open('resume/experience.txt', encoding="utf8") as f:
    experience = f.read()

# LOOP THROUGH JOBS # 
for i in os.listdir("Adverts/"): 
    # READ PERSPECTIVE JOB AD # 
    print (f"Current Job [{count}]: {i}")
    with open(f'adverts/{i}') as f:
        job_ad = f.read()

    # API CALL #
    content = ("This is the content of my resume: " + experience + "Write a cover letter for the following job advert: " + 
               job_ad + " Keep it short. And make reference to my above resume. Include my name at the end. When referencing the job advert, Dont be too literal or too wordy.")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": content}])
    chat_response = completion.choices[0].message.content

    # DUMP OUTPUT TO FILE #
    with open(f'outputs/{i}_Output.txt', 'w') as file:
        file.write(chat_response)
    count = count + 1 

# END MESSAGE + ELAPSED TIME #
input(f"\nCompleted all jobs [{count-1}] in {round((time.time() - start_time),2)} seconds.")
