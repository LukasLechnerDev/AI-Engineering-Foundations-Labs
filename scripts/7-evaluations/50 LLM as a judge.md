# LLM-as-a-Judge

## Learning goals
- Understand why deterministic evals can't evaluate free-text / open-ended outputs like the job summary
- Know the LLM-as-a-judge pattern: one model produces output, a second evaluates it against a rubric
- Write a judge prompt with a concrete rubric
- Understand the trade-offs: cost, latency, and judge bias

## Notes
- Anchor on the `summary` field from the summarizer in `step_4_summarize.py` — students already know this field exists
- The existing `test_summary_eval.py` is the implementation to walk through
- Use the spectrum table (code-based → human-graded → LLM-as-a-judge) as the motivating frame
- Use a capable model as judge; cheaper/faster models can work but need calibration first
- LLM judges can be lenient toward outputs from the same model family — worth mentioning

## Script

### The gap deterministic evals can't fill

We already built a test that checks classification accuracy. We compare the model's True/False output against a human label and get a number. Clean and cheap.

But the summarizer returns a `summary` field — a 2-3 sentence overview of the job posting.

How do you test if a summary is good?

You can't write `assert summary == "..."` — the text is different every run. A regex won't tell you whether the summary accurately reflects the job description. You need something that understands language.

### The judge pattern

LLM-as-a-judge means using a second LLM to evaluate the output of the first.

The judge gets three things:
- The original input (job title + description)
- The model's output (the summary)
- A rubric that defines what "good" looks like

And it returns a structured verdict: pass or fail, and why.

The rubric is everything. A vague prompt like "is this a good summary?" produces vague, inconsistent judgments. A concrete rubric produces reliable signal. For our summary field, the rubric has three criteria:

1. **Concise** — is the summary 2-3 sentences, no more, no less?
2. **Accurate** — is every claim supported by text in the job description?
3. **No hallucinations** — does the summary avoid introducing technologies or responsibilities not in the original?

The judge only passes if all three are met.

### Walking through test_summary_eval.py

Open `tests/test_summary_eval.py`. A few things to notice:

**The judge gets the summarizer's own instructions.** The `judge_instructions` string includes the original `instructions` variable from `step_4_summarize.py`. The judge knows exactly what the summarizer was supposed to do — so it can check whether the summary actually follows those rules.

**The judge uses a stronger model.** The summarizer uses `gpt-4o-mini`. The judge uses a more capable model. You want your judge to be smarter than — or at least as smart as — the model being judged.

**Structured output makes the verdict machine-readable.** The judge returns `passes` (bool) and `feedback` (string). The bool lets the test calculate a pass rate. The feedback string tells you *why* something failed — that's what you actually use to improve your prompt.

**The test only samples 20 jobs.** Running a strong model as judge on every output adds cost. A representative sample is enough to detect regressions in prompt quality.

### Where this fits

| Type | What it evaluates | How |
|---|---|---|
| Code-based | Classification (True/False) | Compare against human label |
| Human-graded | Any output | Human fills in CSV |
| LLM-as-a-judge | Free-text quality (summary) | Judge LLM scores against rubric |

Each level catches things the previous one misses. LLM-as-a-judge is the only practical option for evaluating free-text quality at scale.

### Trade-offs

**Cost and latency.** Running a strong judge model on every output adds up. Sample strategically — 20 jobs is enough to detect a regression in reason quality without burning your budget on every test run.

**Judge bias.** A model may be lenient toward outputs from its own family. Before trusting your judge, manually check 5-10 verdicts against your own judgment. If the judge keeps passing things you'd fail, tighten the rubric.

## Sources
- https://developers.openai.com/api/docs/guides/evaluation-best-practices
- https://hamel.dev/blog/posts/evals-faq/
