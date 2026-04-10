# 20 - Next-token prediction

## Teaching goal
- Give students the simplest correct mental model for what an LLM does.

## Content to learn
- during pretraining the model learns patterns from lots of text
- a useful mental model is: the model learns by predicting the next token again and again
- when we use the model, it generates one token at a time
- each new token depends on the previous tokens in the context
- the model works with probabilities, so outputs are not always identical
- temperature makes the output more stable or more varied

## Keep this light
- no math
- no transformer internals
- no top-k or top-p in the MVP
