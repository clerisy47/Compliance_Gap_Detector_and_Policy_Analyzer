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
answer_library_entry = parse_answer_library("data/answer_library_entry.xlsx")


def run_rag_pipeline(query):
    embeddings = create_embeddings(policies)
    query_emb = embed_query(query)
    context, scores = retrieve_relevant_context(query_emb, policies, embeddings)
    return generate_answer(query, context)


with open("full_report.txt", "w") as file:
    for framework in frameworks:
        file.write(run_rag_pipeline(framework) + "\n\n\n\n\n")
