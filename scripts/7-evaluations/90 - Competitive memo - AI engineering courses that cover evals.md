# Competitive memo: AI engineering courses that cover evals

## Executive summary

- The strongest dedicated evals courses treat evals as a primary workflow, not as a side topic. Anthropic, DeepLearning.AI, Reforge, and Evidently all make eval design, grading strategy, or iteration loops the center of the course.
- The market splits into two clear lanes. One lane is technical and builder-focused, covering deterministic checks, LLM-as-judge, datasets, tracing, and production monitoring. The other lane is product/PM-focused, emphasizing rubrics, golden datasets, trace analysis, and eval-driven roadmaps.
- This course's current stance in [0 Outline.md](./0%20Outline.md) is directionally strong and still differentiated. Most competitors either go broader into platforms and observability, or they assume a more advanced or more product-heavy audience. There is still room for a beginner-friendly, code-first module that starts local and stays tied to one concrete app.
- The biggest gap in the current outline is not "more theory." It is sharper sequencing and clearer examples. The strongest competitor courses all organize evals around concrete artifacts: test cases, graders, traces, and repeated experiments.
- Broad AI engineering bootcamps still tend to mention evaluation as one topic among many rather than teaching it as an operational habit. That creates a good positioning opportunity for this course: evals as a practical software engineering skill for shipping reliable AI apps.

## Comparison table

| Bucket | Course | Audience | Format | Exact eval coverage from official source | Eval emphasis | Depth | Relevance to this repo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dedicated evals | [Anthropic Courses: Prompt evaluations](https://github.com/anthropics/courses/tree/master/prompt_evaluations) | Developers working with Claude and prompts | Free, self-paced, GitHub notebooks | Anthropic says this course teaches "production prompt evaluations" and the prompt evaluations course spans nine lessons, including human-graded evals, simple code-graded evals, classification evals, promptfoo, model-graded evals, and custom model-graded evals. | Human grading, code grading, promptfoo, model grading | Course centerpiece | High. This is the closest match to a code-first evals module for developers. |
| Dedicated evals | [DeepLearning.AI: Evaluating AI Agents](https://learn.deeplearning.ai/courses/evaluating-ai-agents/information) | Beginner builders with basic Python | Free enrollment, short course, 2h 16m, 15 lessons, 6 code examples | The course teaches learners to add observability, set up evaluations for agent components, choose between code-based and LLM-as-a-judge evaluators, run structured experiments, and monitor agent performance in production. | Agent decomposition, component evals, traces, LLM-as-judge, production monitoring | Course centerpiece | Medium. Strong for later agents content, but less aligned to the MVP because it assumes an agent architecture. |
| Dedicated evals | [Reforge: AI Evals](https://www.reforge.com/courses/ai-evals) | PMs, senior PMs, product leaders | Paid membership, live course, current page shows start date April 9, 2026 | Reforge frames the course as an eval-driven playbook for AI agents, covering AI PRDs, golden datasets, eval rubrics, trace analysis, automated evaluators, code-based and LLM-as-judge evaluation, and evaluating agent architectures. | Product workflow, roadmaps, rubrics, trace analysis, automated evaluators | Course centerpiece | Medium-low for the MVP student, high as positioning input. It shows how strongly evals are becoming a PM and product quality topic. |
| Dedicated evals | [Evidently AI: LLM evaluation for builders](https://www.evidentlyai.com/llm-evaluation-course-practice) | AI/ML engineers, data scientists, technical PMs, hands-on builders | Free, 3-week video course, 10 hands-on code tutorials | Evidently explicitly covers automated quality checks "from deterministic validations to model-based scoring," custom LLM judges, RAG evaluation, adversarial testing, test datasets, prompt/model comparison, tracing outputs, and evaluating summarization, classification, content generation, and basic agents. | Deterministic checks, model-based scoring, LLM judges, RAG evals, adversarial testing, tracing | Course centerpiece | Very high. This is the nearest external example of a modern, practical builder curriculum. |
| Dedicated evals | [Evidently AI: LLM evaluations for AI product teams](https://www.evidentlyai.com/llm-evaluations-course) | AI product managers and AI leaders | Free, 7-day email course, no coding required | Evidently positions this as a gentle introduction covering evaluation methods, benchmarks, guardrails, custom LLM judges, and "evaluations at different stages of LLM app lifecycle: from experiments to production monitoring." | PM-friendly lifecycle view, quality systems, monitoring, guardrails | Course centerpiece | Medium. Useful as a signal that non-technical audiences are now being taught eval literacy. |
| Broader AI engineering | [LunarTech: AI Engineering Bootcamp](https://www.lunartech.ai/bootcamp/ai-engineering-bootcamp) | Aspiring or advanced AI engineers | Paid, self-paced bootcamp, 400+ learning hours | LunarTech presents evaluation as part of a much broader AI engineering curriculum. The page says students learn the "complete lifecycle of generative AI" and one LLM section explicitly lists "Evaluation" alongside pre-training, optimization, fine-tuning, pruning, and LLM Ops. | Broad model/LLM lifecycle, evaluation as one curriculum item | Light mention | Low-medium. It validates that evaluation is table stakes in broad AI engineering training, but it does not appear to teach evals with the same depth as dedicated offerings. |

## Notes on evidence

- Anthropic evidence:
  - Main courses README says `Prompt evaluations` teaches "production prompt evaluations" to measure prompt quality.
  - The dedicated course README lists nine lessons, including human-graded evals, code-graded evals, classification evals, promptfoo-based evals, model-graded evals, and custom model-graded evals.
- DeepLearning.AI evidence:
  - The official course page says learners add observability, prepare testing examples, choose code-based vs. LLM-as-a-judge evaluators, create structured experiments, and monitor agents in production.
- Reforge evidence:
  - The official course page positions evals as a practical introduction for PMs and lists a syllabus of evaluation gap, eval-driven roadmaps, trace analysis, automated evaluation, and agent architecture evaluation.
- Evidently builders evidence:
  - The official course page explicitly lists deterministic validations, model-based scoring, custom LLM judges, RAG evaluation, adversarial testing, tracing outputs, and hands-on testing of summarization, classification, content generation, and basic agents.
- Evidently product teams evidence:
  - The official course page explicitly lists evaluation methods, benchmarks, guardrails, custom LLM judges, and evaluation across the lifecycle from experiments to production monitoring.
- LunarTech evidence:
  - The official bootcamp page explicitly includes `Evaluation` in an LLM curriculum list, but it does not expose a detailed evaluation syllabus on the page. The "light mention" depth rating is an inference from that limited evidence.

## Positioning implications for this course

- Keep module 7 anchored on the current local-first stance. The current outline already says to start with deterministic checks, add model-graded checks later, and keep evaluation platforms out of the main module. That is still a good beginner path.
- Position the module as "evals for one real app" rather than "survey of evaluation methods." Competitor courses that land well all organize the topic around a concrete workflow. For this repo, the classification and extraction steps in `ai-engineer-job-digest` are the obvious backbone.
- Lean into the software engineering framing. Reforge shows the PM angle, while Evidently and DeepLearning.AI show observability- and platform-heavy variants. This course can stay simpler and more differentiated by teaching evals as repeatable checks, regression protection, and iteration loops inside a real Python app.
- Treat tracing and platform tooling as a later layer, not the first layer. DeepLearning.AI and Evidently go quickly into observability and monitoring. That is useful later, but it would dilute the MVP if introduced before students can run local evals in code.
- Add slightly more explicit "experiment loop" language. Several competitors frame evals not only as graders, but as a way to compare prompts, models, or logic changes. That concept fits the existing project and can be taught without adding much complexity.

## Recommendations for module 7

- Tighten the module around a three-step progression:
  1. Deterministic checks on classification and extraction outputs.
  2. Human-labeled or manually reviewed examples to create a small trusted dataset.
  3. One carefully scoped LLM-as-a-judge example for a subjective field such as summary quality or reasoning quality.
- Make the core artifacts explicit:
  - a test dataset
  - one deterministic grader
  - one model-based grader
  - one simple score report students can interpret
- Teach evals through repeated comparisons:
  - baseline prompt vs. revised prompt
  - stronger model vs. cheaper model
  - before vs. after a code or prompt change
- Keep platforms out of the main learning path in this module.
  - Mention promptfoo briefly only if it helps visualize the eval loop.
  - Do not make Langfuse, LangSmith, Braintrust, or similar tools a dependency for understanding the fundamentals.
- Add one explicit lesson beat on failure analysis:
  - not just "what score did we get?"
  - but "which examples failed, why did they fail, and what do we change next?"

## Recommendations for later production modules

- In the Langfuse or productionizing modules, introduce tracing and observability as a second layer on top of the local eval suite, not as a replacement.
- If agents stay in scope for later modules, borrow the strongest pattern from DeepLearning.AI:
  - evaluate components separately
  - then evaluate end-to-end behavior
- If product thinking gets more explicit later, borrow selectively from Reforge:
  - define what "good" means
  - maintain a golden dataset
  - use evals to decide whether a change should ship
- Consider a later optional extension inspired by Evidently:
  - RAG evaluation
  - adversarial testing
  - monitoring evals in production
  - but only after the MVP project is already reliable locally

## Suggested decisions

- Decision 1: Keep module 7 code-first and local-first. Do not move platform-based evaluation workflows into the core evals module.
- Decision 2: Strengthen the module around concrete eval artifacts and comparison loops, not broader theory coverage.
- Decision 3: Reserve observability, trace inspection, and production monitoring for later modules where students already understand local evals.
- Decision 4: Position evals as a core software engineering skill for reliable AI products. This is the clearest differentiation against broad bootcamps and PM-oriented courses.

## Sources

- Internal course context:
  - [scripts/7-evaluations/0 Outline.md](./0%20Outline.md)
  - [scripts/0-preview/0-preview.md](../0-preview/0-preview.md)
- External sources:
  - Anthropic Courses README: [github.com/anthropics/courses](https://github.com/anthropics/courses/tree/master/prompt_evaluations)
  - Anthropic raw README for `prompt_evaluations`: [raw.githubusercontent.com/anthropics/courses/master/prompt_evaluations/README.md](https://raw.githubusercontent.com/anthropics/courses/master/prompt_evaluations/README.md)
  - DeepLearning.AI `Evaluating AI Agents`: [learn.deeplearning.ai/courses/evaluating-ai-agents/information](https://learn.deeplearning.ai/courses/evaluating-ai-agents/information)
  - Reforge `AI Evals`: [reforge.com/courses/ai-evals](https://www.reforge.com/courses/ai-evals)
  - Evidently `LLM evaluation for builders`: [evidentlyai.com/llm-evaluation-course-practice](https://www.evidentlyai.com/llm-evaluation-course-practice)
  - Evidently `LLM evaluations for AI product teams`: [evidentlyai.com/llm-evaluations-course](https://www.evidentlyai.com/llm-evaluations-course)
  - LunarTech `AI Engineering Bootcamp`: [lunartech.ai/bootcamp/ai-engineering-bootcamp](https://www.lunartech.ai/bootcamp/ai-engineering-bootcamp)
