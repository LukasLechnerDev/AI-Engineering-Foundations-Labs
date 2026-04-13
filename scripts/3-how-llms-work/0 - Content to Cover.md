# 0 - Content to Cover

## Teaching goal
- Give students the smallest useful mental model for how LLMs work.
- Keep this module short so we can get back to building quickly.

## What to cover
- what a foundation model is at a high level
- tokens
  - text gets split into tokens
  - models read and generate tokens, not words
- pretraining and next-token prediction
  - the model learns patterns from lots of text
  - at runtime it generates one token at a time
- probabilistic output - why not deterministic?
  - the model predicts probabilities, not one guaranteed answer
  - temperature changes how stable or varied the output is
  
  This is a useful mental model for the course:
- accuracy: is the output good enough?
- cost: can this scale economically?
- latency: is the response fast enough for the use case?

## Keep out of this module?
- supervised vs unsupervised taxonomy
- parameters and parameter count
- top-k and top-p
- open source vs open weight
- token pricing and cost calculators
- context windows and max output tokens in detail
- knowledge cutoff
- reasoning vs non-reasoning models
- deeper architecture details

## Note
- Teach only enough theory to support the `ai-engineer-job-digest` project.
- Move the deferred topics to the end-of-course advanced module.

### Ressources: 
- AIE Book Chapter 2
- Patterns Book pg7+
- ~[https://www.youtube.com/watch?v=zjkBMFhNj_g](https://www.youtube.com/watch?v=zjkBMFhNj_g)~ => Karpathy on LLMs
* https://openai.com/index/chatgpt/ Introducing ChatGPT
* Ed Donners Videos on YT
  
