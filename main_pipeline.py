
from parsers.parse_docs import parse_documents
from summarizer.summarize import summarize_sections
from embedder.generate_embeddings import embed_texts
from matcher.semantic_match import match_requirements
from recommender.generate_recommendations import suggest_fixes
from dashboard.report_generator import generate_report

compliance_docs = parse_documents("data/compliance_docs/")
internal_policies = parse_documents("data/internal_policies/")
qa_pairs = parse_documents("data/internal_qa/")

compliance_reqs = summarize_sections(compliance_docs)
internal_summaries = summarize_sections(internal_policies + qa_pairs)

req_embeddings = embed_texts(compliance_reqs)
internal_embeddings = embed_texts(internal_summaries)

matches = match_requirements(compliance_reqs, req_embeddings, internal_summaries, internal_embeddings)

gaps_with_recs = suggest_fixes(matches)

generate_report(compliance_reqs, matches, gaps_with_recs)

print("✅ Pipeline completed. Open the dashboard to view results.")