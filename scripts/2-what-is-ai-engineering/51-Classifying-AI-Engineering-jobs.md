# Classifying AI Engineering Job Postings with an LLM

## Introduction
In the last video, we scraped some job postings seeking an “AI Engineer”. 
The result of this scrape is displayed here in this table. 

We also had a closer look at some of these job postings, we reviewed their descriptions, and agreed that, for these job posts, the definition of “AI Engineer” matches ours. So the companies of these Job Postings were looking for an Engineer that builds applications on top of pre-trained models. 

One thing however I noticed while analysing lots of  AI Engineering job postings is that the term **AI Engineer** is not used consistently across the market.

And that is important to understand, because sometimes companies use the title, but they actually mean something slightly different from what we mean in this course.

## Actually ML Engineering
TODO: use current job postings
For instance, when we take a look at this job posting: [InterImage hiring AI Engineer in Annapolis Junction, MD](https://www.linkedin.com/jobs/view/4395309456/), then the focus is more on developing, training, evaluating and fine-tuning machine learning, and deep learning models, instead of integrating such models into applications. 

## Actually MLOps
In an other job posting, - this one here -  key responsibilities of the role is about: https://www.linkedin.com/jobs/view/4395041804/ Operations. 

In my experience, there are **three common types of mismatch**.

The first one is what I would call **traditional ML roles**.

In these cases, the company advertises an AI Engineer role, but if you look more closely, they are really looking for a **Machine Learning Engineer**. That usually means they want someone who trains models, fine-tunes models deeply, or works directly on model development, rather than someone who mainly builds applications on top of pre-trained foundation models.

So the title says *AI Engineer*, but the actual work is much closer to classic ML Engineering.

The second mismatch is that some companies are actually looking for an **MLOps Engineer**.

MLOps is basically **DevOps for Machine Learning**. The focus there is less on building the end-user application and more on the surrounding platform: deploying models, monitoring them in production, managing infrastructure, maintaining training and serving pipelines, and making sure ML systems operate reliably at scale.

So again, the job may be labeled *AI Engineer*, but the real focus is platform, operations, and infrastructure for machine learning systems.

And the third mismatch is that sometimes the role is really more of a **leadership role**.

In that case, the title may still sound hands-on, but the actual job contains much less development work and much more leadership: setting direction, coordinating teams, making strategic decisions, and driving AI initiatives across the company.

So when you read AI Engineer job postings, you have to look beyond the title.

Because sometimes *AI Engineer* means **application builder on top of foundation models**, sometimes it really means **ML Engineer**, sometimes **MLOps Engineer**, and sometimes even a **leadership position**.

That is just the reality of an emerging job role: the market has not fully settled on one single definition yet.

## So we need to filter them out

Before we continue with analyzing jobs for AI engineers further, we want to filter out these kinds of jobs that have a different definition of an AI engineer.

But how can we do this? Should we search for certain words in the job description and if these words are contained we just filter them out? 

Well this doesn't sound too reliable and probably doesn't give us good results.

What about using an LLM to decide if a job posting matches with our definition of AI engineering? Let's implement such a classification now.

Such a classification task was very hard or near impossible to do before LLMs but now with the power of strong foundational models we can implement this difficult task in a pretty easy way.

### On screen
- `4-classify-job-postings.ipynb`

So in this lesson, we are going to clean that dataset by adding an LLM-based filtering step.

The goal is simple. We will read the scraped job postings from disk, send each posting to an LLM, ask the model whether this is truly an AI engineering role, and then save only the accepted jobs into a new JSONL file.

This matters because every later analysis depends on the quality of this dataset. If we keep irrelevant jobs in the file, then our insights about responsibilities, tools, and skills will be noisy. So before we analyze the market, we first want to improve the quality of the data.

A keyword filter would not be enough here. A posting can mention AI or machine learning without the actual role being AI engineering, and before modern LLMs this kind of semantic filtering usually required much more custom NLP work, labeled examples, or a dedicated classifier.

One important detail before we start: this notebook assumes that the previous notebook has already created `jobs/1-scraped_jobs.jsonl`. So this step builds directly on the output from the scraping workflow.

By the end of this lesson, you will understand a very practical AI engineering pattern: use an LLM as a classifier, enforce a structured output format, and turn raw unstructured data into a more reliable dataset for downstream analysis.

## Section 1: Imports and Notebook Goal

### On screen
- Import cell
- `json`
- `Path`
- `pandas`
- `OpenAI`
- `HTML` and `display`

### Narration
Let’s start with the imports.

There is nothing special here, so we do not need to spend much time on this cell.

The key idea here is that this workflow is mostly regular Python data processing with one LLM call inside the loop. That is a very common AI engineering pattern. You take an existing software or data workflow, and then you add a model call at the point where judgment is needed.

That is the main thing to remember from this section: the overall structure stays simple, and the LLM becomes one component inside a larger pipeline.

## Section 2: Load the Scraped Jobs from File

### On screen
- The cell that defines `scraped_jobs_path`
- The existence check
- The empty-file check
- The success message with the number of entries

### Narration
Now we load the scraped job postings from the previous lesson.

We load `jobs/1-scraped_jobs.jsonl`, make sure the file exists and is not empty, and then read it into a dataframe.

At the end, we print the number of entries as a quick sanity check before we start making model calls.

## Section 3: Define the Instructions

### On screen
- The `client = OpenAI()` line
- The full `instructions` string
- The AI engineering definition and decision rules

### Narration
Next, we define the instructions for the model.

This is one of the most important parts of the notebook, because the quality of the classification depends heavily on the quality of these instructions.

We start by creating the OpenAI client. Then we define a multi-line instruction string that explains exactly how the model should think about the task.

Notice what we are doing here. We are not only saying, classify this job posting. We are also defining what we mean by AI engineering in the context of this course.

In these instructions, AI engineering means building applications on top of foundation models. In other words, integrating models like LLMs into products and software systems.

Then we contrast that with nearby roles that should not be accepted. For example, traditional machine learning engineering can focus on training or tuning models. MLOps and platform engineering can focus on infrastructure. Standard software engineering, analytics, and research roles may mention AI, but that does not automatically make them AI engineering roles.

We also add an important rule for ambiguity: if the posting is unclear, classify it as false.

That conservative rule is useful because in data filtering, false positives are often more damaging than false negatives. If we accidentally keep many irrelevant jobs, the later analysis becomes less trustworthy. It is usually better to end up with a smaller but cleaner dataset.

This cell also introduces a new concept: `instructions`.

In the Responses API, `instructions` are the high-level task rules we want the model to follow consistently across calls. You can think of this as the stable behavior we want from the model.

Later, for each individual job posting, we will pass the specific job title and description as the `input`. So the instructions define the role and decision criteria, while the input contains the actual example to classify.

That distinction is important and comes up all the time in AI engineering. Stable policy goes into the instructions. Case-specific data goes into the input.

## Section 4: Define the Schema

### On screen
- The `schema` dictionary
- `is_ai_engineering_role`
- `reason`
- `required`
- `additionalProperties: False`

### Narration
After defining the instructions, we define the schema for the model output.

This tells the model exactly what shape the response should have.

In this case, the schema is intentionally very small. We want two fields.

The first field is `is_ai_engineering_role`, which is a boolean. That is the core classification result.

The second field is `reason`, which is a string. That gives us a short explanation for the decision.

We also mark both fields as required, and we set `additionalProperties` to `False`. That means we only want these fields and nothing else.

Why is this useful?

Because free-form text is harder to process reliably in code. If the model replied in plain prose, we would need to parse that text ourselves, and that becomes brittle very quickly.

With a schema, we make the output predictable. That means our downstream code can safely read the boolean decision and the explanation without guessing about formatting.

Structured output is a broader topic, and we will cover it in more depth later in the course. For now, the important point is that schemas help us turn model output into something software can consume reliably.

That is a major part of real AI engineering. We are not only trying to get a good answer from the model. We are also trying to get an answer in a format that fits cleanly into an application or data pipeline.

## Section 5: Make the LLM Calls

### On screen
- The `results = []` line
- The loop over `jobs_df.iterrows()`
- The progress print statement
- The `client.responses.create(...)` call
- The `instructions`, `input`, and `text.format` arguments
- Parsing `response.output_text`

### Narration
Now we get to the core of the notebook: making one model call for each job posting.

We start with an empty list called `results`. Then we loop over the dataframe row by row.

For each job, we extract the title and description. We also print a progress message like `Screening job 3 out of 25`. That is helpful because model-based loops can take time, and progress output makes the notebook feel much more transparent while it runs.

Then we call `client.responses.create`.

There are a few important pieces in this call.

First, we choose the model, here `gpt-5.4-mini`. That is a practical choice for a classification task like this. We do not need a huge amount of creativity. We need reasonably good judgment, structured output, and efficient execution across multiple rows.

Second, we pass the `instructions` we defined earlier. These stay constant for every job posting.

Third, we pass the job-specific content through `input`. This input includes the job title and the full job description. So again, the instructions define the rules, and the input provides the specific example to classify.

Fourth, inside the `text` argument, we define the output format. We tell the model to use a JSON schema named `ai_engineering_job_screening`, and we pass the schema object we created earlier. We also set `strict` to `True`, which means we want the output to follow the schema exactly.

There is also a `verbosity` setting of `low`. That makes sense here because we only need a short reason, not a long essay.

Once the response comes back, we parse `response.output_text` using `json.loads`, extract the boolean field and the reason, and append both values to our `results` list.

There is an important engineering lesson in this section.

The LLM is not the entire application. The LLM is one step inside a loop, and the rest of the program still matters. We still control the prompt, the schema, the iteration logic, the parsing, and how the result gets stored.

That is how you should think about production AI systems as well. The model call is important, but it sits inside a larger software workflow that you design.

## Section 6: Combine the Results and Save the Accepted Jobs

### On screen
- The cell that creates `classified_jobs_path`
- `results_df = pd.DataFrame(results)`
- `screened_jobs = pd.concat(...)`
- Filtering rows where `is_ai_engineering_role` is true
- Writing `2-classified-jobs.jsonl`

### Narration
Once all model calls are finished, we combine the classification results with the original job postings.

We turn the `results` list into a dataframe, join it back to the original jobs, and then filter for the rows where `is_ai_engineering_role` is true.

Those accepted jobs are written to `jobs/2-classified-jobs.jsonl`, which becomes the cleaned dataset for the next lessons.

That is the pattern to remember: raw data comes in, the LLM adds judgment, and we save the improved result for downstream use.

## Section 7: Display the Results

### On screen
- The print statements with the output path and counts
- The dataframe with `title`, `is_ai_engineering_role`, `llm_reason`, and `job_url`
- Clickable job links in the notebook output

### Narration
In the final step, we display the results so we can inspect what happened.

We print the saved file path and the main counts, so we can immediately see how strong the filtering effect was.

Then we render a small table with the title, the classification, the model's reason, and the job URL.

This is also a quick quality check. We can scan a few examples and see whether the model decisions match our definition of AI engineering.

## Recap

### On screen
- Notebook summary
- Input file: `jobs/1-scraped_jobs.jsonl`
- Output file: `jobs/2-classified-jobs.jsonl`

### Narration
Let’s recap what we built in this notebook.

We started with scraped job postings from the previous lesson.

Then we defined a clear set of instructions for what counts as an AI engineering role.

After that, we defined a strict output schema so the model would return structured data that our Python code could use reliably.

Then we looped over every job posting, sent the title and description to the model, parsed the structured result, and stored the classification.

Finally, we combined the model output with the original data, kept only the accepted jobs, saved them into a new JSONL file, and displayed the results for inspection.

The big lesson here is that LLMs are not only for chat interfaces. They are also very useful as judgment components inside data and software pipelines.

In the next lessons, we will use this cleaned dataset to analyze what AI engineering jobs actually look like in practice.

## Optional Closing

### On screen
- The saved output file
- Transition to the next notebook

### Narration
At this point, we now have a cleaner set of AI engineering job postings, and that gives us a much better foundation for the rest of the analysis.

So in the next lesson, we can move from data collection and filtering to actual market insights, because now we are analyzing the right set of roles.

## Additional Lecture Ideas

- Helpful analogy or intuition:
  Describe the model here as a junior research assistant that reads each posting and applies a written rubric. The code provides the rubric, the model applies judgment, and the pipeline stores the result.
- Common mistake to warn about:
  Students may assume that if a role mentions machine learning, generative AI, or data science, it should automatically count as AI engineering. Reinforce that this course uses a narrower definition centered on building applications with foundation models.
- Common mistake to warn about:
  Students may treat the model output as ground truth. Point out that this is still a probabilistic system, so we should inspect examples and refine the instructions if the decisions do not match our intent.
- Production extension:
  Mention that in a production setting, you would likely batch requests where possible.
- Portfolio extension:
  A strong follow-up project would be to build a small job-market analysis pipeline that scrapes roles every week, classifies them automatically, tracks trends over time, and exposes the results in a dashboard.

## Inferred Context Added to This Script

- The notebook assumes the earlier scraping notebook has already produced `jobs/1-scraped_jobs.jsonl`.
- The script explicitly frames the displayed table as a lightweight evaluation step, even though the notebook itself only shows the results.
- The explanation of why schemas matter and why ambiguous cases are classified as false is expanded for teaching clarity.
