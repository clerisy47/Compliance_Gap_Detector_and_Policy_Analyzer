from parsers.parse_docs import parse_answer_library, parse_frameworks, parse_policy_folder
from summarizer.summarize import summarize_sections
from embedder.generate_embeddings import embed_texts
from matcher.semantic_match import match_requirements
from recommender.generate_recommendations import suggest_fixes
from dashboard.report_generator import generate_report

framework_reqs = parse_frameworks("data/compliance_docs/frameworks.csv")
internal_policies = parse_policy_folder("data/internal_policies/")
answer_library = parse_answer_library("data/internal_qa/answer_library_entry.csv")

internal_policy_summaries = summarize_sections([doc["content"] for doc in internal_policies])
qa_descriptions = [entry["details"] for entry in answer_library]

framework_embeddings = embed_texts(framework_reqs)
internal_embeddings = embed_texts(internal_policy_summaries + qa_descriptions)
internal_texts = internal_policy_summaries + qa_descriptions

matches = match_requirements(framework_reqs, framework_embeddings, internal_texts, internal_embeddings)

gaps_with_recs = suggest_fixes(matches)

generate_report(framework_reqs, matches, gaps_with_recs)

print("Pipeline completed. Open the dashboard to view results.")
