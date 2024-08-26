from openai import AzureOpenAI
import os

# Initialize global variables
chat_history = []
window_size = 3  # Set the size of the conversation window

basic_info = f"""
                You are a job applicant with the following basic information:
                Applying for position: Backend Developer
                Graduated from: Peking University
                Interviewing at: ByteDance
                Professional skills: Java
                Next, I will play the role of an interviewer and ask you questions. Please respond accordingly. For specific questions, try to use my professional skills and select an appropriate analytical method to provide a detailed solution.
                """

def add_to_history(role, content):
    global chat_history
    # Add the message to the conversation history
    chat_history.append({"role": role, "content": content})
    # Ensure the conversation history does not exceed the window size
    if len(chat_history) > window_size:
        chat_history.pop(0)

def generate_response(transcript_text):
    global chat_history
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-02-01"
    )
    
    # Add user input to the conversation history
    add_to_history("user", transcript_text)
    
    # Prepare the messages to be sent, including basic information and conversation history
    messages = [{"role": "system", "content": basic_info}] + chat_history
    
    # Use the Azure OpenAI API to generate a response
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Adjust the model name according to your Azure configuration
        messages=messages,
        max_tokens=600,
        temperature=0.4,
    )
    
    # Extract the model's reply
    reply = response.choices[0].message.content
    
    # Add the model's reply to the conversation history
    add_to_history("assistant", reply)
    
    return reply

if __name__ == "__main__":
    # For debugging
    test_transcript = "How do you implement a linked list reversal?"
    response = generate_response(test_transcript)
    print("Test Input: {}".format(test_transcript))
    print("Generated Response: {}".format(response))