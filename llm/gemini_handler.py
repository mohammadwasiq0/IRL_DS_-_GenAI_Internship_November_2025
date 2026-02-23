# from langchain_google_genai import ChatGoogleGenerativeAI
# from config import Config
# from utils.logger import logger

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=Config.GEMINI_API_KEY
# )

# def generate_response(prompt):
#     try:
#         response = llm.invoke(prompt)
#         return response.content
#     except Exception as e:
#         logger.error(f"Gemini Error: {e}")
#         return "Sorry, something went wrong."


from euriai import EuriaiClient
from config import Config
from utils.logger import logger


# Initialize client once (singleton style)
client = EuriaiClient(
    api_key=Config.EURI_API_KEY,
    model="gpt-4.1-nano"  # Fast + cost-efficient
)


def generate_response(prompt: str) -> str:
    try:
        response = client.generate_completion(
            prompt=prompt,
            temperature=0.5,
            max_tokens=100
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        logger.error(f"Euriai Error: {str(e)}")
        return f"Error: {str(e)}"
