from transformers import pipeline
import google.generativeai as genai

GOOGLE_API_KEY = ""


def generate_answer(policy, top_k_framework):
    genai.configure(api_key=GOOGLE_API_KEY)
    print(top_k_framework)
    system_instruction = """
    You are a cybersecurity assistant.
    1) First write the requirement at the beginning of the answer.
    2) Given the evidence, find if the requirement is: 'Satisfied' or 'Not Satisfied' and explain in short why.
    """

    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest", system_instruction=system_instruction
    )

    top_k_text = "\n\n".join(
        [f"Passage {i+1}: {c}" for i, c in enumerate(top_k_framework)]
    )

    prompt = f"""
    Requirement:
    {top_k_text}

    Evidence:
    {policy}
    """

    result = model.generate_content(prompt)
    return result.text.strip()
