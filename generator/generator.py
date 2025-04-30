
# import google.generativeai as genai

# GOOGLE_API_KEY = "AIzaSyDI5ZZdfTV28Y2CCODEdh661p3dcc5CYcU"


# def generate_answer(policy, top_k_framework):
#     genai.configure(api_key=GOOGLE_API_KEY)
#     print(top_k_framework)
#     system_instruction = """
#     You are a cybersecurity assistant.
#     1) First write the requirement at the beginning of the answer.
#     2) Given the evidence, find if the requirement is: 'Satisfied' or 'Not Satisfied' and explain in short why.
#     """

#     model = genai.GenerativeModel(
#         "gemini-1.5-pro-latest", system_instruction=system_instruction
#     )

#     top_k_text = "\n\n".join(
#         [f"Passage {i+1}: {c}" for i, c in enumerate(top_k_framework)]
#     )

#     prompt = f"""
#     Requirement:
#     {top_k_text}

#     Evidence:
#     {policy}
#     """

#     result = model.generate_content(prompt)
#     return result.text.strip()



# '''
import requests

def generate_answer(requirement, evidence_chunks):
    """
    Use Flan-T5 (text2text-generation) to classify requirement satisfaction.
    Returns a string with [Satisfied/Not Satisfied/Missing] and an explanation.
    """
    # Load the Flan-T5 small model in a text2text-generation pipeline
    # generator = pipeline("text2text-generation", model="google/flan-t5-small")
    # Build a prompt that includes the requirement and bullet-pointed evidence
    # prompt = f"Requirement: {requirement}\nEvidence:\n"
    big_chunk = ""
    for chunk in evidence_chunks:
        big_chunk += chunk
    # prompt = ""
    # # print("---------------------------------------------------------------------------")
    # # print(big_chunk)
    # # print("----------------------------------------------------------------------------")
    # prompt += ("This is the requirement \n " + requirement + "\n this is the evidence \n" + big_chunk +
    #            "Answer with 'Satisfied', 'Not Satisfied', or 'Missing' and provide a brief explanation.")
    # # Generate the answer (deterministic output with do_sample=False)
    # print("------------------------------------------------------------------------------")
    # print(prompt)
    # print("-------------------------------------------------------------------------------")
    # result = generator(prompt)
    # print(result)
    prompt = (
    "You are a compliance assistant.\n"
    "1) First write the requirement at the beggining of the answer"
    "2) given the evidence, find if the requirement is: 'Satisfied' or 'Not Satisfied' and explain in short why.\n"
    "Requirement: \n"
    f"{requirement}\n\n"
    "Evidence:\n"
    f"{big_chunk}\n\n"
    )
    #print(prompt)
    
    print("***"*20)
    response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",       # Use the same name you use in the CLI
        "prompt": prompt,
        "stream": False          # Set to True if you want to stream output
    }
)

    print("***"*20)
    # Extract and print the generated response
    print(response.json()["response"])
    

    return response.json()["response"]
# '''

# import time
# import requests

# def generate_answer(policy, top_k_framework):
#     start = time.time()
#     """
#     Use locally running LLaMA 3.2 model to evaluate if cybersecurity requirements are satisfied.
#     Returns a string: 'Satisfied' or 'Not Satisfied' with a short explanation.
#     """

#     # Combine evidence passages into one block of text
#     top_k_text = "\n\n".join(
#         [f"Passage {i+1}: {chunk}" for i, chunk in enumerate(top_k_framework)]
#     )

#     # Build the full prompt with system instruction
#     prompt = (
#         "You are a cybersecurity assistant.\n"
#         "1) First write the requirement at the beginning of the answer.\n"
#         "2) Given the evidence, find if the requirement is: 'Satisfied' or 'Not Satisfied' and explain in short why.\n\n"
#         "Requirement:\n"
#         f"{top_k_text}\n\n"
#         "Evidence:\n"
#         f"{policy}\n"
#     )

#     # Send request to local LLaMA server
#     print("*** SENDING PROMPT TO LLaMA 3.2 ***")
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3.2",
#             "prompt": prompt,
#             "stream": False
#         }
#     )
#     print("*** RESPONSE RECEIVED ***")
#     print(time.time()-start)

#     # Extract and return the generated response
#     return response.json().get("response", "No response from model.")

