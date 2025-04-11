1. What functions should be included in the section "things that are available to the LLM and already pre-written for it"? Why write anything in advance for the LLM at all?
2. What can be done in cases where the code written by the LLM produces an error?
3. How can additional data sources be added to such a system?

---

1. 
At minimum, we need to tell the model which libraries are available in the environment where the code will be executed, and provide all necessary variable names (with secrets) and non-secret variables that might be required when executing the code - for example, the database address. We need to tell the LLM in advance what's available to it because an LLM is simply a text-to-text transformer. There is no real intelligence here.

2.
We can pass the error back to the LLM, create a feedback loop, for example to another agent with a similar context (data schema, etc.) and ask it to regenerate the code. However, it seems that we could manage with a single prompt. After all, we can add an additional block to an f-string if an error occurs.

3.
Additional data sources can be attempted to be stuffed into the prompt, for example - "here you also have Elasticsearch available at this address, try to extract something from it." But this can quickly lead to prompt bloat and hallucinations IMHO.
If there are many data sources, I would build a more deterministic system, some kind of router or something similar.