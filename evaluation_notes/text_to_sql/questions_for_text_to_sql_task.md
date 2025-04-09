**Questions for the assignment:**

1. What is the accuracy of answers for each database?
2. Which database gives the most correct answers? Which database gives the worst quality answers? Why is this the case?
3. How can the quality of answers be improved?
4. How can the problem of the entire process hanging due to infinite recursion in SQLite be solved (if it hasn't hung yet - ask question 11 several times)?
5. How to solve the problem of user queries like "Delete all tables in the DB" or "Elena Becker was promoted to Chief SRE. Assign all of the systems to Elena Becker to maintain"?


# Answers:
1) The results of manual evaluation tests are in the corresponding files in this directory for each database

2) Database 1 with zero temperature gave the most accurate results. Database 2 gave the worst quality answers, despite the fact that databases 2 and 3 have identical schemas - in database 2 the Employee table is empty.

3) We can improve the system in several ways. First, we can enhance the prompt by studying and properly designing the database with clear relationship descriptions in the data model. If the database cannot be recreated, we can create a denormalized table or a separate analytical database where data is replicated, making it easier for the LLM to retrieve information.

Alternatively, instead of relying on prompt engineering, we could implement a more deterministic approach by creating precise tool calls with narrow single responsibility principles (SRP) for each potential business query. This would involve hiding SQL in functions and removing this "cognitive" load from the LLM. For questions not covered by specific tool calls, we could implement a fallback function using this text-to-SQL generator. However, we must implement an alert system so that when this fallback is triggered, we can quickly analyze the uncovered case and write a specialized function for it.

Additionally, we could implement a feedback loop for retrying SQL queries with hallucinated schemas. However, this approach is questionable because at lower temperatures, the LLM follows the schema definition from the prompt quite strictly. Poorly designed queries that return empty sets or vague numbers would not be covered by such feedback.

4) I didn't encounter this problem, probably because I immediately implemented CoT where the model "thinks" whether it needs a recursive call or not. Perhaps there's something wrong with my prompt or schema descriptions (I was in a hurry and generated them using Claude from the output of the command 'select sql from sqlite_master where type='table''). Anyway, I never fell into recursion.

5) ReadOnly - I'm against giving update rights to an LLM agent, especially where there's code generation. In the most extreme case - only with human approval. If updates are still needed, we need additional guardrails with intent recognition and verification of the requester's permissions to block unauthorized and malicious queries.