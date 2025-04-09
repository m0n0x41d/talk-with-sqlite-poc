# LLM agent with SQL task with some constraints.

## Task 1
We need to draft a small program that takes a question for an LLM, converts it to an SQL query, executes it in a database, and returns the answer. 

There are three SQLite databases with different versions of the same data: DB1, DB2, DB3

### Constraints:

- No more than 100 lines of code, not counting prompts
- No need to synthesize an answer. It's ok to output just the query result
- We're not solving the issue of environment freezing due to infinite recursion. Manual reloading in such cases is good enough

Questions:

- What is the accuracy of answers for each database?
- Which database provides the most correct answers? Which database gives the worst quality answers? Why is this the case?
- How can the quality of answers be improved?
- How can we solve the problem of the entire process freezing due to infinite recursion in SQLite (if it's not freezing yet - ask question #11 several times)?
- How to handle user queries like "Delete all tables in the database" or "Elena Becker was promoted to Chief SRE. Assign all of the systems to Elena Becker to maintain"?


## Task 2
Take the script from the first task and any version of the database, then write a script for text-to-code instead of text-to-sql. That is, instead of generating SQL and executing a database query, we need to generate Python code and execute it.

The goal is to be able to ask questions about the organizational structure, and have the system output code that builds charts or displays tables.

### Constraints:

For simplicity of implementation, let the script just output Python code that you can copy and run manually (you can automate this if desired)
If desired, you can even skip writing a script for Python code generation and package the entire prompt into an Anthropic Claude Project or OpenAI Custom GPT.

### Additional questions:

- What functions should be written in the "things that are available to the LLM and are already pre-written for it" section? Why write anything in advance for the LLM at all?
- What can be done when the LLM-generated code produces an error?
- How can additional data sources be added to such a system?