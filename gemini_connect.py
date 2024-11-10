import google.generativeai as genai

with open(".apikey", "r") as file:
    api_key = file.read().strip()
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

first_call = True


def generate_response(user_message, topic=None, side=None):
    global first_call
    if first_call:
        first_call = False
        chat_session.send_message(
            f"""You are debate specialist and you are here to debate on the topic "{topic}" from the {side} side. Accept the user's prompt, analyze the user's arguments, and provide counterarguments. Avoid very long arguments and try to give short and simple arguments to hold the opponents interest. You can also provide additional arguments to support the user's side."""
        )
    response = chat_session.send_message(user_message)
    return response.text


if __name__ == "__main__":
    response = chat_session.send_message("INSERT_INPUT_HERE")

    print(response.text)
