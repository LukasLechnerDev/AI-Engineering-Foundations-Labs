# Maintaining the RAG eval dataset

The golden test set lives in `eval_dataset.csv`. Domain experts should edit that
file; they do not need to change `evals.py`.

## Why CSV

- It opens directly in Excel and Google Sheets.
- Each row is one test case, so reviewing and assigning rows is straightforward.
- It is easy to version in Git and load with Python's standard library.
- The current data is flat. JSONL would add complexity without providing a benefit.

If the evals later need multi-turn conversations, lists of acceptable answers, or
structured grading rubrics, JSONL would be a better fit.

## Columns

- `id`: A short, stable identifier. Do not reuse an ID for a different question.
- `category`: The behavior being tested, such as `direct_fact`, `comparison`, or
  `out_of_scope`.
- `question`: A realistic user question.
- `reference_answer`: The facts and behavior a good answer must contain. It is a
  grading reference, not text the application must reproduce word for word.
- `source_documents`: The documents that support the reference answer. Separate
  multiple paths with semicolons. This can be blank for an out-of-scope case.

## Review workflow

1. Add questions that represent real user needs, common failures, and important
   edge cases.
2. Have a domain expert write the reference answer from the source documents.
3. Have a second reviewer verify factual claims and source paths.
4. Run the eval suite before and after changing retrieval, prompts, or models.
5. Inspect failures individually. A score alone does not explain what broke.
6. Add useful production failures to the dataset so fixed problems stay fixed.

Keep the set balanced across normal questions, comparisons, ambiguous questions,
and questions the application should refuse. When the dataset grows, keep a small
development subset for prompt iteration and a held-out subset for final checks.

Include plenty of `discovery` cases where users describe their experience, goals,
or constraints without naming a company or job title. These better represent a
large knowledge base whose contents are unknown to users. Reference answers should
identify the best-supported matches and preserve important caveats such as
location, seniority, clearance requirements, and uncertainty. Avoid requiring an
exhaustive list unless the application is designed to search the full corpus.

Export the sheet as UTF-8 CSV after editing it in Excel or Google Sheets. Do not
manually remove quotes around cells that contain commas.
