from parsers.parse_docs import (
    parse_answer_library,
    parse_frameworks,
    parse_policy_folder,
)

from embedder.embedder import create_embeddings, embed_query
from retriever.retriever import retrieve_relevant_context
from generator.generator import generate_answer


frameworks = parse_frameworks("data/frameworks.xlsx")
policies = parse_policy_folder("data/policies/")
# answer_library_entry = parse_answer_library("data/answer_library_entry.xlsx")


def run_rag_pipeline(query):
    embeddings = create_embeddings(policies)
    query_emb = embed_query(query)
    context, scores = retrieve_relevant_context(query_emb, policies, embeddings)
    if scores[0] > 0.6:
        return generate_answer(query, context)
    else:
        return f"**Requirement**:\n\n {query} \n\n **Status**: Missing \n\n**Reason**: \n\nThe requirement is missing."



with open("full_report.txt", "w", encoding="utf-8") as file:
    list_of_frameworks = [
        "CCPA",
        "CIS",
        "GDPR",
        "HIPPA",
        "HITRUST",
        "ISO",
        "NIST 800-53",
        "NIST CSF",
        "PCI-DSS",
        "SCF",
    ]

    for x in list_of_frameworks:
        file.write("*" + x + "*" + "\n\n\n")
        frameworks = parse_frameworks(f"data/frameworks/{x}.xlsx")

        for framework in frameworks:
            result = run_rag_pipeline(framework)
            # print("Generated Answer:", result)  # See what’s returned
            file.write(run_rag_pipeline(framework) + "\n\n\n\n\n")
            
