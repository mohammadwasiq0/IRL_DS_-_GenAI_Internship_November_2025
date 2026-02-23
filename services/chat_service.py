from prompts.prompt_manager import build_prompt
from llm.gemini_handler import generate_response
from memory.memory_manager import save_message

def process_chat(user_id, user_input):
    prompt = build_prompt(user_input)
    response = generate_response(prompt)

    save_message(user_id, "user", user_input)
    save_message(user_id, "assistant", response)

    return response
