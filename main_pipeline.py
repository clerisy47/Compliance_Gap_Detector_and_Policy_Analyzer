from parsers.parse_docs import (
    parse_answer_library,
    parse_frameworks,
    parse_policy_folder,
)

from summarizer.summarize import summarize_sections
from embedder.generate_embeddings import embed_texts
from matcher.semantic_match import match_requirements
from recommender.generate_recommendations import suggest_fixes
from dashboard.report_generator import generate_report

frameworks = parse_frameworks("data/frameworks.xlsx")
policies = parse_policy_folder("data/policies/")
answer_library_entry = parse_answer_library("data/answer_library_entry.xlsx")

internal_policy_summaries = summarize_sections([doc["content"] for doc in policies])
qa_descriptions = [entry["details"] for entry in answer_library_entry]

framework_embeddings = embed_texts(frameworks)
internal_embeddings = embed_texts(internal_policy_summaries + qa_descriptions)
internal_texts = internal_policy_summaries + qa_descriptions

matches = match_requirements(
    frameworks, framework_embeddings, internal_texts, internal_embeddings
)

gaps_with_recs = suggest_fixes(matches)

generate_report(frameworks, matches, gaps_with_recs)

print("Pipeline completed. Open the dashboard to view results.")

print(answer_library_entry)
