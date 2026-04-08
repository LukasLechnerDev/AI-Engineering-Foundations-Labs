# Typical AI-powered applications

## Big Picture

from programmierbar podcast (see full notes in IntellJ)

### 1. Most production AI use cases fall into a few recurring patterns

The guest describes three main patterns:

1. Knowledge retrieval chatbots
2. Classification tasks
3. Agentic, multi-step workflow automation

### General
- the amount of applications that can be built on top of foundation models is endless
- talk about most popular apps: ChatGPT, Co-Pilot, Codex coding assistant, NotionAI, Grammarly, Duolingo Max (RolePlay, Video Call)
- lots of popular apps integrate AI features into their applications: GSuite, Evernote, 
- RAG applications are popular (Notion, Internal Knowledge Assistants for companies) - https://rewe-group.at/en/newsroom/2025/08/bot-haidi-bipa-launches-ai-assistant-for-employees-and-sets-new-standards-in-knowledge-transfer
- Agents - Customer support agents are popular
- Workflow Automation
- See Google Deep Research from April 7

### Our Notebook
- Go through notebook and summarize use cases of "our" jobs
- Use Codex to read the classified jobs jsonl and search online for real ai apps that these companies are building

## Slob starts here 

## What Students Learn
- AI engineers do not work on one single kind of product
- Many real-world AI engineer jobs are about enterprise software, not only chatbots
- There are a few recurring application categories that show up again and again
- These categories are useful for understanding the job market and for choosing portfolio projects

## Introduction
When we look at recent AI engineering job postings, one thing becomes very clear:

AI engineers are not only building "an AI app".

Instead, they usually work on a few recurring kinds of applications.

That is important for two reasons.

First, it helps us understand what companies actually mean when they hire AI engineers.

And second, it helps us choose much better portfolio projects, because ideally we want to build things that are similar to what companies are building right now.

## Typical categories

### 1. Knowledge assistants and RAG systems
These are systems that answer questions over internal or private data.

Typical examples:
- internal company knowledge assistants
- document search over policies, contracts, or technical docs
- copilots for regulated or private datasets

Why this matters:
This is one of the most common real-world AI application patterns.

Good portfolio projects:
- a PDF question-answering assistant
- a support knowledge bot
- a legal or policy search assistant

### 2. Internal copilots
These are AI tools that help employees do their work faster.

Typical examples:
- finance copilots
- operations copilots
- support copilots
- internal research assistants

Why this matters:
A lot of enterprise AI is not customer-facing. It is built for internal teams.

Good portfolio projects:
- an internal analyst copilot
- a customer support helper
- a meeting and action-item assistant

### 3. Agentic workflow automation
These systems do not just answer questions. They actually execute steps in a workflow.

Typical examples:
- classifying requests
- routing exceptions
- pulling data from tools
- drafting responses
- handing edge cases to a human

Why this matters:
This is probably one of the most important categories in the current AI engineering market.

Good portfolio projects:
- an intake and triage agent
- an invoice or claims workflow agent
- a multi-step sales or operations assistant

### 4. Customer-facing AI assistants
These are AI systems embedded directly into the customer experience.

Typical examples:
- banking assistants
- support assistants
- personalized product assistants
- AI features inside mobile apps

Why this matters:
These systems are often easier for students to understand because they are visible in the final product.

Good portfolio projects:
- a banking-style assistant
- a customer onboarding assistant
- a shopping or recommendation assistant

### 5. Voice and multimodal interfaces
Some AI engineer roles are about building new interfaces, not only text chat.

Typical examples:
- voice assistants
- conversational audio interfaces
- multimodal assistants with text, speech, and image understanding

Why this matters:
AI engineering is also about interface design and user experience, not only back-end orchestration.

Good portfolio projects:
- a voice note assistant
- a meeting assistant with speech input
- a multimodal research assistant

### 6. Industrial and operational AI systems
Not all AI engineer roles are in SaaS or consumer apps.

Typical examples:
- inspection tools
- maintenance assistants
- operations support systems
- AI systems for logistics or manufacturing workflows

Why this matters:
AI engineering also exists in aerospace, healthcare, manufacturing, and other operational environments.

Good portfolio projects:
- a defect inspection assistant
- a maintenance report analyzer
- an operations dashboard with AI recommendations

## Concrete examples from real companies

### Capital One
Capital One has a public AI assistant called [Eno](https://www.capitalone.com/digital/tools/eno/).

This is a great example of a customer-facing AI assistant in finance.

Students can immediately understand the application:
- fraud and unusual charge alerts
- spending insights
- virtual card numbers
- help with account-related questions

Category:
- customer-facing AI assistant
- finance copilot

### Sandbar
Sandbar is building [Stream](https://www.sandbar.com/stream), a private voice ring and conversational notes app.

This is a strong example of a voice-first AI product.

What makes it interesting:
- voice capture on the go
- conversational interaction
- note organization and memory
- web retrieval through a voice interface

Category:
- voice interface
- personal AI assistant

### GE Aerospace
GE Aerospace publicly describes an [AI-enabled inspection tool](https://www.geaerospace.com/news/press-releases/ge-aerospace-deploys-ai-driven-inspection-tool-maximize-narrowbody-engine-time-wing) for aircraft engine maintenance.

This is a very useful example because it shows that AI engineering is not only about chat interfaces.

What students can learn from it:
- AI can help with inspection workflows
- AI can improve consistency and speed
- AI can support technicians inside real operational systems

Category:
- industrial AI
- operational decision support

### H2O.ai
H2O.ai publicly highlights enterprise AI agents, digital assistants, and industry-specific GenAI applications on its [homepage](https://h2o.ai/).

This is a strong example of enterprise AI systems built on private data.

Typical applications highlighted there include:
- fraud reduction
- call center automation
- enterprise AI agents
- ready-to-use AI apps for business workflows

Category:
- knowledge assistants
- agentic enterprise workflows
- internal copilots

### Varick
Varick describes [enterprise AI systems](https://varickagents.com/) that automate end-to-end business workflows.

This is a very strong example of agentic workflow automation.

The applications they describe are not toy demos. They are things like:
- finance operations
- sales workflows
- procurement and logistics workflows
- agents that work across ERP, CRM, and finance tools

Category:
- agentic workflow automation
- enterprise operations AI

### Cadre AI
Cadre AI presents [AI engineering services](https://www.cadreai.com/ai-engineering) around workflow automation, connected systems, and custom AI agents.

This is another good example of how many AI engineer roles are really about fixing workflow bottlenecks inside companies.

Typical applications:
- document routing
- email triage
- customer inquiry handling
- custom multi-step AI agents

Category:
- workflow automation
- internal copilots
- custom AI agents

## What students should take away
- Many AI engineer jobs are about enterprise workflows and internal tools
- Customer-facing assistants are important, but they are only one part of the market
- Voice, multimodal, and industrial applications are also real AI engineering work
- Good portfolio projects should mirror these categories instead of being generic chatbot demos

## Good portfolio project directions
- build a RAG assistant over private documents
- build an internal copilot for a finance or support workflow
- build an agent that classifies, routes, and escalates requests
- build a customer-facing assistant for a specific domain
- build a voice-first assistant
- build an AI workflow for inspection, reporting, or operations
