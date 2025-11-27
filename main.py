from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    HAS_SPLITTER = True
except:
    HAS_SPLITTER = False


UPLOAD_ROOT = r"C:\Users\hassa\Desktop\readme_uploads"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.3-70b-versatile"




def ensure_clean_upload_folder():
    """Deletes old uploads and recreates upload folder."""
    if os.path.exists(UPLOAD_ROOT):
        shutil.rmtree(UPLOAD_ROOT)
    os.makedirs(UPLOAD_ROOT, exist_ok=True)


ALLOWED_EXT = {
    ".py", ".js", ".ts", ".html", ".css",
    ".json", ".md", ".txt", ".yml", ".yaml"
}


def get_all_files(folder):
    """Return list of all acceptable file paths in the folder."""
    file_list = []
    for root, dirs, files in os.walk(folder):

        skip_dirs = {".git", "__pycache__", "node_modules", ".idea", ".vscode"}
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXT:
                file_list.append(os.path.join(root, file))

    return file_list



def chunk_code_text(text: str, chunk_size: int = 2500, overlap: int = 200):
    """Use Langchain splitter if available, otherwise fallback."""
    if HAS_SPLITTER:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(text)

   
    chunks = []
    start = 0
    L = len(text)

    while start < L:
        end = min(start + chunk_size, L)
        chunks.append(text[start:end])
        start = end - overlap if (end - overlap) > start else end

    return chunks



def llm_call(messages):
    """Calls Groq API."""
    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=False,
            stop=None
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        return None



app = FastAPI()


@app.get("/")
async def html():
    return FileResponse("index.html")


@app.post("/save")
async def save_folder(files: list[UploadFile] = File(...)):
    """Save uploaded files into the upload directory."""
    ensure_clean_upload_folder()

    saved_files = []
    for file in files:
        fname = file.filename.replace("..", "").lstrip("/\\")
        save_path = os.path.join(UPLOAD_ROOT, fname)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(await file.read())

        saved_files.append(save_path)

    return {"status": "saved", "files": saved_files}


# ----------------------
# LLM SUMMARIES
# ----------------------
@app.post("/llm")
async def llm():
    """Generate summaries for each uploaded file."""
    open("store.txt", "w", encoding="utf-8").close()

    system_prompt = """
SYSTEM PROMPT — PROJECT FILE ANALYZER & README BUILDER
You analyze one file at a time and output structured summaries.

STRICT FORMAT:

FILE: <filename>

TECH STACK USED:
- <item>

WORKING / LOGIC SUMMARY:
- description

IMPORTANT FUNCTIONS:
- <name>: description

IMPORTANT CLASSES:
- <name>: description

ENDPOINTS (if any):
| Method | Route | Description |

NOTES:
- relevant notes

RULES:
- Extract ONLY from the file
- If empty, write "None"
- No hallucination
    """

    files = get_all_files(UPLOAD_ROOT)
    if not files:
        return {"error": "No files found"}

    final_output = []

    for file_path in files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

       
        if len(text) <= 3000:
            chunks = [text]
        else:
            chunks = chunk_code_text(text)

        combined_summary = ""

        for chunk in chunks:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"FILE: {file_path}\n\n{chunk}"}
            ]

            assistant = llm_call(messages)

            if assistant is None:
                return {"error": "Groq API call failed"}

            combined_summary += assistant + "\n"

        final_output.append(combined_summary)

        
        with open("store.txt", "a", encoding="utf-8") as s:
            s.write(combined_summary + "\n\n" + "="*60 + "\n\n")

    return {"summaries": final_output}



@app.post("/generate_readme")
async def generate_readme():
    """Creates README.md using stored summaries."""
    open("README.md", "w", encoding="utf-8").close()

    if not os.path.exists("store.txt"):
        return {"error": "store.txt missing"}

    content = open("store.txt", "r", encoding="utf-8").read()

    readme_prompt = """
You create a clean, professional README.md using ONLY the content of store.txt.

Include EXACT sections:
1. Title  
2. Overview  
3. Tech Stack  
4. Features  
5. Project Structure (tree)  
6. Detailed File Summaries  

RULES:
- Use only data in store.txt  
- No assumptions  
- No hallucination  
- No extra sections  
    """

    messages = [
        {"role": "system", "content": readme_prompt},
        {"role": "user", "content": content}
    ]

    readme_text = llm_call(messages)

    if readme_text is None:
        return {"error": "Groq API call failed for README generation"}

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_text)

    return {"status": "README generated successfully", "preview": readme_text}


@app.post("/generate_docs")
async def generate_docs():
    """Creates DOCUMENTATION.md using stored summaries."""
    open("DOCUMENTATION.md", "w", encoding="utf-8").close()

    if not os.path.exists("store.txt"):
        return {"error": "store.txt missing"}

    content = open("store.txt", "r", encoding="utf-8").read()

    docs_prompt = """
    You create a comprehensive, professional technical documentation (DOCUMENTATION.md) using ONLY the content of store.txt.
    
    Include EXACT sections:
    1. Introduction
    2. Architecture Overview
    3. Module Details (Classes, Functions, Logic)
    4. API Reference (if applicable)
    5. Setup & Installation
    6. Usage Guide
    7. Dependencies
    
    RULES:
    - Use only data in store.txt
    - No assumptions
    - No hallucination
    - Professional tone
    """

    messages = [
        {"role": "system", "content": docs_prompt},
        {"role": "user", "content": content}
    ]

    docs_text = llm_call(messages)

    if docs_text is None:
        return {"error": "Groq API call failed for Documentation generation"}

    with open("DOCUMENTATION.md", "w", encoding="utf-8") as f:
        f.write(docs_text)

    return {"status": "Documentation generated successfully", "preview": docs_text}
