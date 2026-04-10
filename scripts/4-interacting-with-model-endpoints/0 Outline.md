# Outline

## Teaching goal
- Students should learn how to turn model calls into reliable software behavior.
- This module stays focused on raw API fundamentals.

## What to cover
- Responses API as the default interface for the course
  - https://www.youtube.com/watch?v=0pGxoubWI6s
  - when to use it instead of Chat Completions
- request and response mental model
- instructions vs input vs message roles
- conversation state
  - manual conversation history
  - a LLM doesn't have memory by default, every call is stateless
  - conversation history including tool calls
- stream responses with a Gradio chat interface
- temperature and response settings
- structured output
- multi-modality
  - upload and analyze an image
  - generate an image
- tool calling
  - custom tools
  - built-in tools as a short extension
  - batch mode?
  - Basic Overview of Inference Services

## Keep out of this module
- costs, latency, and model routing
- retries, rate limits, fallbacks, and defensive parsing
- framework comparisons like LangChain or PydanticAI
- MCP
- workflows and agent definitions

### OpenAI API Deep Dive

https://model-spec.openai.com/2025-12-18.html
https://developers.openai.com/api/docs/guides/text
https://www.youtube.com/watch?v=0pGxoubWI6s
