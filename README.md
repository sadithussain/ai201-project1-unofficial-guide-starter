# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

My domain is student-written reviews of Computer Science professors at my college, RIT. This knowledge is hard to find otherwise because it's not listed on the official RIT website or documents. This is experience gathered from students which are individual to every professor. This knowledge is valuable because it is written from the experience of a student which is useful to other students compared to material provided by the professor or school. For example, we will be able to figure out which professors are more rigorous, provide more coursework, have better policies, etc.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professor | Student-written reviews for Maria Jose Cepeda Garcia | https://www.ratemyprofessors.com/professor/2556028 |
| 2 | Rate My Professor | Student-written reviews for Sean Strout | https://www.ratemyprofessors.com/professor/127294 |
| 3 | Rate My Professor | Student-written reviews for Jansen Orfan | https://www.ratemyprofessors.com/professor/2299490 |
| 4 | Rate My Professor | Student-written reviews for Yuan Liao | https://www.ratemyprofessors.com/professor/2979160 |
| 5 | Rate My Professor | Student-written reviews for Ting Cao | https://www.ratemyprofessors.com/professor/2585840 |
| 6 | Rate My Professor | Student-written reviews for Thomas Borrelli | https://www.ratemyprofessors.com/professor/1105257 |
| 7 | Rate My Professor | Student-written reviews for Abeer Ahmad | https://www.ratemyprofessors.com/professor/2954361 |
| 8 | Rate My Professor | Student-written reviews for Arthur Nunes | https://www.ratemyprofessors.com/professor/1037287 |
| 9 | Rate My Professor | Student-written reviews for Xumin Liu | https://www.ratemyprofessors.com/professor/1410469 |
| 10 | Rate My Professor | Student-written reviews for Mohan Kumar | https://www.ratemyprofessors.com/professor/2094090 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500

**Overlap:** 100

**Why these choices fit your documents:** Rate My Professor reviews are usually short and on average it seems like they are around 300 characters in length. However, we also need to take into account other information that comes along with the review such as the class, attendance, 'would take again', grade, and textbook answers. We also want to take into account the fact that we may cut off reviews in the middle which is why I decided to go for 100 characters of overlap.

**Final chunk count:** 410

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** Although this is a very lightweight and fast model, the embedding is satisfactory for the job that we are doing. However, more complicated queries may cause problems.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** I passed the retrieved context into the Groq API with the following strict instruction: 
*"CRITICAL RULES: 1. You must answer the user's question USING ONLY the context provided below. 2. If the answer cannot be determined from the provided context, you MUST output exactly: 'I do not have enough information in the provided documents to answer this question.' Do not make up an answer."*

**How source attribution is surfaced in the response:** Source attribution is surfaced in the response because it is attached to our embeds. We used the name of the files that were associated with the raw text in order to attach a professor's name to it and we know that all of this raw data is from Rate My Professor.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How strict are Maria Cepeda's deadline policies? | She is very strict about these policies and there are almost always no extensions. | Detailed her "insane missed exam policy" (showing up late results in a 0 with no makeups), but noted assignment due dates are clear and more reasonable. | Relevant | Accurate |
| 2 | What does Jansen Orfan do for students who are struggling in his class? | Jansen has many resources to help students who are struggling. He is very helpful during office hours and gives students many extra credit opportunities. | Described him as caring, patient, and responsive outside of class. However, the system did not mention "extra credit opportunities" due to missing context. | Partially relevant | Partially accurate |
| 3 | What are some complaints and praises of Thomas Borelli's teaching style? | He is very energetic and makes the class exciting. However, many students say that his lecture is absolutely mandatory. | Praised him as enthusiastic, passionate, and clear with a good sense of humor. Complained that he relies heavily on slides and moves too fast, but missed the mandatory attendance point. | Partially relevant | Partially accurate |
| 4 | As someone who may not go to class often, what is something I should watch out for if I take Abeer Ahmad? | Although Abeer's lectures are highly reviewed, many students say that he doesn't post lecture materials often and takes long to respond to emails. | Warned that missing class means missing vital whiteboard notes, and noted that lectures do not always align perfectly with the tough homework and projects. | Partially relevant | Partially accurate |
| 5 | As someone who takes notes during lectures to succeed, what is one thing that I should be worried about when taking Yuan Liao? | One thing you should watch out for is that many students say his lectures are very boring. | Explicitly warned that lectures are boring, unengaging, cause students to fall asleep, and force you to do most learning outside of the classroom. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What are some complaints and praises of Thomas Borelli's teaching style?

**What the system returned:** The system successfully synthesized praises (enthusiastic, passionate, clear) and complaints (relies heavily on slides, moves too fast). However, it completely missed the expected complaint that his lecture attendance is mandatory.

**Root cause (tied to a specific pipeline stage):** This failure is tied to the Retrieval Stage because the information that was retieved left out some context because we are only keeping the top 5 relevant vector stores.

**What you would change to fix it:** We could increase our top-k to a higher value like 8.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The spec helped me during implementation because it was an outline of what I needed to get done, in order which helped with how I was going to prompt AI to generate code.

**One way your implementation diverged from the spec, and why:** I had intially planned to use a top-k of 4 but increased that value to 5 prior to implementation.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I provided the raw, messy copy-pasted Rate My Professor text alongside my strict chunking parameters and asked for an ingestion script.
- *What it produced:* It provided a sliding window script that created chunks of text from the raw data based on the parameters provided. The script also removed common repetitive UI phrases that were inside of the data.
- *What I changed or overrode:* N/A

**Instance 2**

- *What I gave the AI:* I provided my completed ChromaDB retriever.py module and asked the AI to wire it to the Groq llama-3.3-70b-versatile model within a Gradio web interface.
- *What it produced:* It generated a standard chatbot interface that appended a weak instruction to the system prompt asking the LLM to "please cite your sources at the end."
- *What I changed or overrode:* I discarded the citation method suggested by the AI and instead opted in for 100% accurate citations by using the file name of the original data to recognize where chunks were being sourced from.
