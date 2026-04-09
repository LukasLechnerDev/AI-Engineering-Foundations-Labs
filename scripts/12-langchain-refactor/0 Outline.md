# Outline

## Teaching goal
- Show students how a higher-level framework changes a working AI project after they already understand the raw SDK.
- Keep this module practical by refactoring familiar parts of project 1 instead of introducing a new product.

## Why this module lives here
- Students already built `ai-engineer-job-digest` with the raw OpenAI SDK, so they can now judge abstractions instead of memorizing them.
- LangChain appears often enough in AI engineering job postings and tutorials that students should be able to read and extend LangChain-based code.
- Teaching LangChain before RAG makes later retrieval codebases easier to follow without making frameworks the foundation of the course.

## What to cover
1. Why the course taught the raw SDK first
2. What LangChain abstracts over and what it does not
3. Refactor one or two familiar project-1 stages to LangChain
4. Use LangChain for:
   - model setup
   - prompt templates
   - structured output or output parsing
   - simple chain composition
5. Compare the raw SDK and LangChain versions side by side
6. Show where LangChain reduces boilerplate
7. Show where LangChain hides important details or adds indirection
8. Define a rule of thumb for when to stay with the raw SDK vs when to use a framework
9. End with a short bridge to RAG
   - document loaders
   - text splitters
   - retrievers
   - vector store integrations

## Keep out of this module
- full RAG implementation details
- agents and LangGraph
- deep framework internals
- long surveys of alternative frameworks
- rewriting the whole project just because a framework exists

## Note
- This should stay short and opinionated.
- The goal is framework literacy, not framework dependence.
