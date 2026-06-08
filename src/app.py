import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv
from retriever import retrieve_context

# Load API keys from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_answer(query: str) -> tuple[str, str]:
    """Retrieves context and generates a grounded answer using Groq."""
    
    # 1. Get the top 4 chunks from our ChromaDB vector store
    retrieved_chunks = retrieve_context(query, n_results=4)
    
    if not retrieved_chunks:
        return "System error: Could not connect to the database.", ""

    # 2. Format the chunks into a single string for the LLM to read
    context_text = "\n\n---\n\n".join(retrieved_chunks)
    
    # 3. Extract unique professor names to cite our sources
    sources = set()
    for chunk in retrieved_chunks:
        # Extract the professor name from the tag we injected in Milestone 3
        if chunk.startswith("[Professor:"):
            prof_name = chunk.split("]")[0].replace("[Professor: ", "")
            sources.add(prof_name)
            
    source_list = "\n".join([f"• Rate My Professor: {prof}" for prof in sources])

    # 4. The System Prompt (Strict Grounding Rule)
    system_prompt = """You are 'The Unofficial Guide', an AI assistant designed to help RIT students pick classes based on real student reviews.
    
CRITICAL RULES:
1. You must answer the user's question USING ONLY the context provided below.
2. If the answer cannot be determined from the provided context, you MUST output exactly: "I do not have enough information in the provided documents to answer this question." Do not make up an answer.
3. Synthesize the reviews intelligently. Do not just blindly quote them; summarize the overall student sentiment.
"""

    # 5. Call the Groq LLM (llama-3.3-70b-versatile)
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
            ],
            temperature=0.2, # Low temperature for factual, grounded answers
            max_completion_tokens=500
        )
        answer = completion.choices[0].message.content
        return answer, source_list
        
    except Exception as e:
        return f"An error occurred while generating the response: {e}", ""


# 6. Build the Gradio Web Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 The Unofficial Guide: RIT Professor Intel")
    gr.Markdown("Ask a question about CS/SE professors at RIT based on real student reviews. (e.g., *'Are Sean Strout's exams difficult?'*)")
    
    with gr.Row():
        with gr.Column(scale=2):
            user_input = gr.Textbox(label="Your Question", placeholder="Type your question here...", lines=2)
            submit_btn = gr.Button("Ask the Guide", variant="primary")
            
        with gr.Column(scale=3):
            llm_answer = gr.Textbox(label="AI Answer", lines=6, interactive=False)
            cited_sources = gr.Textbox(label="Retrieved Sources", lines=3, interactive=False)

    # Wire up the button click and the 'Enter' key submission
    submit_btn.click(fn=generate_answer, inputs=user_input, outputs=[llm_answer, cited_sources])
    user_input.submit(fn=generate_answer, inputs=user_input, outputs=[llm_answer, cited_sources])

if __name__ == "__main__":
    print("🚀 Launching the Unofficial Guide Web UI...")
    demo.launch(share=False)