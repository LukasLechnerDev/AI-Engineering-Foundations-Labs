# 90 easy for llms hard for regular programming


LLMs are especially strong at tasks where the rules are fuzzy, contextual, or too expensive to hand-code.

The big category is:

Turning messy human language into useful structure or judgment.

Good examples:

* Semantic matching

* Figuring out that “head of people” and “HR director” are probably similar, even if wording is very different.

* Regular programming usually needs tons of brittle rules or synonym lists.
* Intent detection

* Understanding what a user is really trying to do, even when they say it indirectly or badly.

* Example: “I need to stop getting charged for this” → cancel subscription intent.
* Natural-language-to-structured queries

* Turning “show me customers who bought twice last month but not this month” into SQL, filters, or API calls.

* Hard to do reliably with classic parsing unless the input is very constrained.
* Entity resolution in fuzzy text

* Recognizing that “Open AI”, “OpenAI Inc.”, and “the ChatGPT company” likely refer to the same thing.

* Traditional code struggles when names are inconsistent.
* Tone / sentiment / stance detection

* Not just positive vs negative, but things like: frustrated, hesitant, sarcastic, defensive, urgent.

* Rule-based systems break quickly here.
* Rewriting with constraints

* “Make this friendlier, shorter, clearer, and suitable for a legal audience.”

* Regular programming can template text, but not really rewrite meaningfully.
* Generalization from examples

* You can show an LLM a few examples and it often infers the pattern.

* Classic programming usually needs you to explicitly define the pattern.
* Handling ambiguity gracefully

* LLMs can say, in effect, “this probably means X, but could also mean Y.”

* Normal code usually needs exact inputs or it fails.
* Information synthesis across messy inputs

* Combining multiple documents, emails, notes, and partial facts into one coherent answer.

* Traditional software can retrieve data, but synthesis is the hard part.
* Lightweight reasoning over text

* Comparing policies, spotting contradictions, identifying missing fields, checking whether a document likely satisfies requirements.

* Hard to encode with fixed rules because the wording varies too much.
* Semantic clustering / labeling

* Grouping support tickets, feedback, or reviews by underlying theme without exact keywords.

* Traditional keyword-based grouping is much weaker.
* Code or text transformation from intent

* “Convert this cURL command to Python requests,” or “turn this paragraph into bullet points.”

* Classic programming can do narrow conversions, but LLMs handle many variants.

A good mental model:

Regular programming is great when the rules are explicit.

LLMs are great when humans can do the task easily, but would struggle to write down all the rules.

Where classic programming still wins:

* exact arithmetic
* deterministic business rules
* validation against strict schemas
* high-reliability logic
* anything where being “usually right” is not enough

So the sweet spot for LLMs is not just classification/summarization/extraction, but more broadly:

semantic judgment under fuzzy language.

For an AI engineering course, I’d group the “hard for regular programming, good for LLMs” capabilities into these buckets:

1. Understanding — intent, tone, semantic similarity
2. Structuring — extraction, normalization, mapping messy text to schemas
3. Transforming — rewriting, translating, formatting, converting between representations
4. Synthesizing — combining scattered information into one coherent result
5. Judging — relevance, policy fit, completeness, contradiction detection

⠀
A very punchy line for teaching this:

LLMs shine when the problem is easy to recognize as a human, but painful to formalize as code.

If you want, I can turn this into a clean lecture slide with examples per category.

#courses/ai-engineer-fundamentals/1-what-is-ai-engineering