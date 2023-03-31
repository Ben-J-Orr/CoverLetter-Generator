# IMPORTS
import os
import openai
import time

# Function to generate a cover letter using the GPT-3.5 API
def generate_cover_letter(experience, job_ad):
    # Combine resume experience and job ad to form content for the AI
    content = ("This is the content of my resume: " + experience + 
               "Write a cover letter for the following job advert: " + 
               job_ad + " Keep it short. And make reference to my above resume. Include my name at the end. When referencing the job advert, Dont be too literal or too wordy.")
    
    # Make an API call to generate the cover letter
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    )
    return completion.choices[0].message.content

# Main function
def main():
    # CONSTANTS
    API_KEY = "API-KEY"
    RESUME_PATH = 'resume/experience.txt'
    ADVERTS_DIR = "Adverts/"
    OUTPUT_DIR = "outputs/"

    # Set API key for OpenAI
    openai.api_key = API_KEY

    # Read resume from the specified file
    with open(RESUME_PATH, encoding="utf8") as f:
        experience = f.read()

    # Loop through all job ads in the specified directory
    start_time = time.time()
    for count, filename in enumerate(os.listdir(ADVERTS_DIR), start=1):
        print(f"Current Job [{count}]: {filename}")

        # Read content of the current job ad
        with open(os.path.join(ADVERTS_DIR, filename)) as f:
            job_ad = f.read()

        # Call generate_cover_letter() function to create a cover letter
        chat_response = generate_cover_letter(experience, job_ad)

        # Write the generated cover letter to the output directory
        with open(os.path.join(OUTPUT_DIR, f'{filename}_Output.txt'), 'w') as file:
            file.write(chat_response)

    # Print completion message and total time taken
    input(f"\nCompleted all jobs [{count}] in {round((time.time() - start_time),2)} seconds.")

# Execute main function
if __name__ == "__main__":
    main()
