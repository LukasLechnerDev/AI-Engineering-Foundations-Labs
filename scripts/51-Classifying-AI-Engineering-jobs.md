## LLM Classification / Filtering

- open `4-classify-job-postings.ipynb`
- What we are now going to do is to read the scraped jobs, use an LLM to classify whether each role is truly an AI engineering role, and only write the accepted jobs into a different jsonl file. 

### Import
- no special imports

### Load scraped jobs from file
- load scraped jobs from last lecture
- makes sure the file exists and is not empty
- reads it into a pandas dataframe

### Define the prompt
- new concept: define instructions (in the completions endpoint: system prompt)

### Define the schema
- give a short explanation, why we use a schema here
- mention that structured output will be covered in one of the next modules

### Make the LLM Calls
- shortly explain loop
- explain difference between instructions and input
- explain text / structured output
- shortly explain rest of the code

### Combine and display the result
- quickly explain code