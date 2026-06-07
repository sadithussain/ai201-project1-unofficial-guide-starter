# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My domain is student-written reviews of Computer Science professors at my college, RIT. This knowledge is hard to find otherwise because it's not listed on the official RIT website or documents. This is experience gathered from students which are individual to every professor. This knowledge is valuable because it is written from the experience of a student which is useful to other students compared to material provided by the professor or school. For example, we will be able to figure out which professors are more rigorous, provide more coursework, have better policies, etc.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500

**Overlap:** 100

**Reasoning:** Rate My Professor reviews are usually short and on average it seems like they are around 300 characters in length. However, we also need to take into account other information that comes along with the review such as the class, attendance, 'would take again', grade, and textbook answers. We also want to take into account the fact that we may cut off reviews in the middle which is why I decided to go for 100 characters of overlap.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** Although all-MiniLM-L6-v2 is a very fast and efficient model, it is not as powerful as the other models out there. It might misunderstand some language that is used by students in reviews. In production, we may want to choose a more powerful model but this might increase latency.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How strict are Maria Cepeda's deadline policies? | She is very strict about these policies and there are almost always no extensions. |
| 2 | What does Jansen Orfan do for students who are struggling in his class? | Jansen has many resources to help students who are struggling. He is very helpful during office hours and gives students many extra credit opportunities. |
| 3 | What are some complaints and praises of Thomas Borelli's teaching style? | He is very energetic and makes the class exciting. However, many students say that his lecture is absolutely mandatory. |
| 4 | As someone who may not go to class often, what is something I should watch out for if I take Abeer Ahmad? | Although Abeer's lectures are highly reviewed, many students say that he doesn't post lecture materials often and takes long to respond to emails. |
| 5 | As someone who takes notes during lectures to succeed, what is one thing that I should be worried about when taking Yuan Liao? | One thing you should watch out for is that many students say his lectures are very boring. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Overlapping Courses:** Professors teach multiple courses which means multiple professors may teach the same course. If a student asks about a specific course and doesn't mention the professor, the answer they get may not be exactly what they're looking for if they have a specific professor in mind already.

2. **Not Enough Context:** There are dozens of reviews per professor and bad reviews may be overshadowed by good reviews and vice versa.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
