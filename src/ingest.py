import os
import re

def clean_text(text: str) -> str:
    """Removes UI artifacts from the copy-pasted Rate My Professor text."""
    # 1. Strip out specific repetitive UI clutter lines
    clutter_patterns = [
        r"Thumbs up\s*\d*",
        r"Thumbs down\s*\d*",
        r"For Credit:\s*(Yes|No)",
        r"Attendance:\s*(Mandatory|Not Mandatory|N/A)",
        r"Would Take Again:\s*(Yes|No)",
        r"Textbook:\s*(Yes|No|N/A)",
        r"Arrow Icon",
        r"Compare",
        r"I'm Professor .*",
        r"Rating Distribution"
    ]
    
    for pattern in clutter_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # 2. Flatten multiple newlines/tabs into standard spaced prose
    text = re.sub(r'[\s\t\n\r]+', ' ', text)
    
    return text.strip()

def chunk_document(text: str, filename: str, chunk_size: int = 500, overlap: int = 100) -> list:
    """Splits text into sliding window chunks and injects professor metadata."""
    # Extract professor name cleanly from file name
    prof_name = filename.replace("prof_", "").replace(".txt", "").replace("_", " ").title()
    prefix = f"[Professor: {prof_name}] "
    
    chunks = []
    step = chunk_size - overlap
    
    if len(text) <= chunk_size:
        chunks.append({
            "text": prefix + text,
            "metadata": {"source": filename, "professor": prof_name}
        })
        return chunks

    for i in range(0, len(text), step):
        chunk_text = text[i:i + chunk_size]
        if len(chunk_text) < 40 and len(chunks) > 0:
            continue
            
        chunks.append({
            "text": prefix + chunk_text,
            "metadata": {"source": filename, "professor": prof_name}
        })
        
    return chunks

def run_pipeline():
    raw_dir = "data/raw"
    all_chunks = []
    
    if not os.path.exists(raw_dir):
        print(f"Error: Directory '{raw_dir}' not found.")
        return

    files = [f for f in os.listdir(raw_dir) if f.endswith(".txt")]
    print(f"Found {len(files)} raw files. Processing...")

    for file in files:
        with open(os.path.join(raw_dir, file), "r", encoding="utf-8") as f:
            raw_content = f.read()
            
        cleaned_content = clean_text(raw_content)
        file_chunks = chunk_document(cleaned_content, file)
        all_chunks.extend(file_chunks)
        
    print(f"\n✅ Processing complete!")
    print(f"Generated {len(all_chunks)} total chunks across your documents.")
    
    if all_chunks:
        print("\n" + "="*50)
        print("🔍 MILESTONE 3 VERIFICATION: PRINTING 5 SAMPLE CHUNKS")
        print("="*50)
        
        # Take up to 5 sample chunks to inspect
        sample_size = min(5, len(all_chunks))
        for idx in range(sample_size):
            sample = all_chunks[idx]
            print(f"\n[CHUNK {idx + 1}/{sample_size}]")
            print(f"📄 Source File: {sample['metadata']['source']}")
            print(f"👤 Professor:  {sample['metadata']['professor']}")
            print(f"📏 Text Length: {len(sample['text'])} characters")
            print(f"📝 Content preview:\n{sample['text']}")
            print("-" * 40)

if __name__ == "__main__":
    run_pipeline()