from openai import OpenAI
import time

with open(".apikey", "r") as f:
    OPEN_AI_API_KEY = f.read().strip()
client = OpenAI(api_key=OPEN_AI_API_KEY)

THREAD = None


# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body, topic=None, side=None):
    global THREAD

    if THREAD is None:
        THREAD = client.beta.threads.create()
        message = client.beta.threads.messages.create(
            thread_id=THREAD.id,
            role="assistant",
            content=f"The topic of debate is: {topic}. The side you are arguing for is: {side}.",
        )

    thread_id = THREAD.id

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    print(message)

    # Run the assistant and get the new message
    new_message = run_assistant(THREAD)
    return new_message


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve("asst_7X2vrM6FZKF7J5rtK40Xe2Rc")

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        print("waiting...")
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    print(f"Generated message: {new_message}")
    return new_message


if __name__ == "__main__":

    # Test assistant
    new_message = generate_response(
        "I think it is a great idea which has emerged in recent times.",
        "Is LGBTQ+ a good ideology for the society?",
        "against",
    )
