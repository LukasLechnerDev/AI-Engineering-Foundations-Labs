# Maintaining the RAG eval dataset

The source of truth is the `rag/ai-engineering-jobs` dataset in Langfuse. Add and
review test cases in Langfuse; the repository no longer keeps a separate copy.

## Dataset items

- `Input`: A realistic user question.
- `Expected output`: The facts and behavior a good answer must contain. It is a
  grading reference, not text the application must reproduce word for word.
- `Metadata.id`: A short, stable identifier. Do not reuse an ID for a different
  question.
- `Metadata.category`: The behavior being tested, such as `direct_fact`,
  `comparison`, or `out_of_scope`.
- `Metadata.source_documents`: The documents that support the reference answer.

Langfuse creates a new dataset version when items change. The experiment runner
uses the latest version by default.

## Review workflow

1. Add or edit a dataset item in Langfuse.
2. Have a domain expert review the expected output against the source documents.
3. Have a second reviewer verify factual claims and metadata.
4. Run `uv run --locked python 7-rag/evals.py` before and after changing
   retrieval, prompts, or models.
5. Inspect failures individually. A score alone does not explain what broke.
6. Compare experiment runs in Langfuse and add useful production failures to the
   dataset so fixed problems stay fixed.

Keep the set balanced across normal questions, comparisons, ambiguous questions,
and questions the application should refuse. When the dataset grows, keep a small
development subset for prompt iteration and a held-out subset for final checks.

Include plenty of `discovery` cases where users describe their experience, goals,
or constraints without naming a company or job title. These better represent a
large knowledge base whose contents are unknown to users. Reference answers should
identify the best-supported matches and preserve important caveats such as
location, seniority, clearance requirements, and uncertainty. Avoid requiring an
exhaustive list unless the application is designed to search the full corpus.

See the [Langfuse dataset documentation](https://langfuse.com/docs/evaluation/experiments/datasets)
for dataset management and versioning details.
