import os
import time

from ai import GptService
from fileutil import read_config_from_file


# Main function to process job advertisements and generate cover letters
def main():
    # Set the API key for OpenAI
    global config, s
    # Define the directories for job advertisements and output
    ADVERTS_DIR = "Adverts/"
    OUTPUT_DIR = "outputs/"

    # Read the user's experience from a text file
    with open('resume/experience.txt', encoding="utf8") as f:
        experience = f.read()

    # Start the timer to measure the time taken to process all job ads
    start_time = time.time()

    # Create a list of job advertisement filenames in the Adverts directory
    job_ads = [(count, filename) for count, filename in enumerate(os.listdir(ADVERTS_DIR), start=1)]

    # Iterate through each job advertisement and generate a cover letter
    for count, filename in job_ads:
        print(f"Current Job [{count}]: {filename}")

        # Read the content of the job advertisement
        with open(os.path.join(ADVERTS_DIR, filename)) as f:
            job_ad = f.read()

        # Generate a cover letter using the experience and job advertisement
        additional_prompt_options = config['additional_prompt_options']
        cover_letter = s.generate_cover_letter(experience, job_ad, additional_prompt_options)

        # Save the generated cover letter in the output directory
        with open(os.path.join(OUTPUT_DIR, f'{filename}_Output.txt'), 'w') as file:
            file.write(cover_letter)

    # Calculate and display the elapsed time taken to process all job ads
    elapsed_time = round(time.time() - start_time, 2)
    input(f"\nCompleted all jobs [{count}] in {elapsed_time} seconds.")


# Run the main function
if __name__ == "__main__":
    config = read_config_from_file()
    s = GptService(
        key=config['api-key'],
        model="gpt-3.5-turbo"
    )
    main()
