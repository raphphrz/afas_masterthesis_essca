
def getOpenAiKey():
    """
    Get the OpenAI API key from the environment variable.
    """
    from dotenv import load_dotenv
    import os
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")
