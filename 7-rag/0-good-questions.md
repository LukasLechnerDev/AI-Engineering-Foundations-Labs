# Good Questions to Show RAG in Action

Good demo questions can't be answered by the LLM without the knowledge base. The examples below are based on the knowledge base run from 2026-09-14, so adapt company names to your own run.

## 1. The Model Doesn't Know This Without RAG

Ask these to the plain LLM first, then to the RAG chatbot.

- Which companies are currently hiring AI engineers in San Francisco?
- Is Anthropic hiring right now? What's the role about?
- What does the AI Engineer role at T12 Technologies involve?

## 2. Search by Meaning, Not Keywords

The question uses different words than the documents, which shows the strength of embeddings.

- Are there roles for someone who just graduated? (should find "Early Career" and "campus hire")
- Which jobs involve building AI agents?
- I'm a lawyer turned developer. Is there a job that fits me? (should find Aderant)

## 3. Answers That Need Both Jobs and Companies

One answer needs chunks from both the `jobs/` and the `companies/` folder.

- What does the company behind the Aderant role actually sell, and what would I build there?
- Which of these jobs are at venture-backed startups vs. large public companies?
- Is the Embedding VC posting from the VC firm itself or from one of its startups?
- Which postings are from recruiting agencies rather than the actual employer?

## 4. Comparing and Advising

- Compare the Optum role and the Thomson Reuters role. Which one is more about LLMs?
- What skills come up most in these postings, and how should I prepare?
- Write me a short cover letter intro for the OpenAI GTM Growth role.

## 5. Questions That Show Limits

- **How many jobs mention Python?** Counting fails, because retrieval only returns the top k chunks, not all documents.
- **What's the salary at Google?** Google isn't in the knowledge base. A well-grounded chatbot says it doesn't know instead of making something up.
- **What does the Optum job require?** There are two Optum postings, so retrieval can mix chunks from both. This shows why citing sources matters.
- **Tell me about the benefits.** If the benefits section ended up in its own chunk, it loses its context. This connects back to chunking.

## Suggested Demo Flow

1. Ask a category 1 question without RAG. The model can't answer or makes something up.
2. Ask the same question with RAG, and show the retrieved chunks and their sources.
3. Ask a category 3 question to show that jobs and companies work together.
4. End with the counting question to show a limit of RAG.
