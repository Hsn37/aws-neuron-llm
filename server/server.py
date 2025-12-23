from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import os
from pathlib import Path
import uvicorn
from prompt import processor_prompt, extract_json
from openai import OpenAI


client = OpenAI(
    api_key="EMPTY",
    base_url="https://e0b2fdd67be4.ngrok-free.app/v1"
)

app = FastAPI(title="Transcript Processing API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
TRANSCRIPTS_DIR = BASE_DIR / "test_transcripts"


class ProcessRequest(BaseModel):
    template: Dict[str, Any]
    transcript: str


@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    with open(BASE_DIR / "index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/templates")
async def get_templates() -> Dict[str, Any]:
    """Get all available templates"""
    templates = {}
    
    if not TEMPLATES_DIR.exists():
        raise HTTPException(status_code=404, detail="Templates directory not found")
    
    for template_file in TEMPLATES_DIR.glob("*.json"):
        try:
            with open(template_file, "r") as f:
                template_name = template_file.stem
                templates[template_name] = json.load(f)
        except Exception as e:
            print(f"Error loading template {template_file}: {e}")
    
    return templates


@app.get("/api/transcripts")
async def get_transcripts() -> Dict[str, str]:
    """Get all available test transcripts"""
    transcripts = {}
    
    if not TRANSCRIPTS_DIR.exists():
        raise HTTPException(status_code=404, detail="Transcripts directory not found")
    
    for transcript_file in TRANSCRIPTS_DIR.glob("*.txt"):
        try:
            with open(transcript_file, "r") as f:
                transcript_name = transcript_file.stem
                transcripts[transcript_name] = f.read()
        except Exception as e:
            print(f"Error loading transcript {transcript_file}: {e}")
    
    return transcripts


@app.post("/api/process")
async def process_transcript(request: ProcessRequest) -> Dict[str, Any]:
    try:
        formatted_template = json.dumps(request.template, indent=2)
        prompt = processor_prompt.format(
            template=formatted_template,
            transcript=request.transcript
        )
        
        response = client.chat.completions.create(
            model="Qwen/Qwen3-4B-Instruct-2507",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        processed_transcript = extract_json(response.choices[0].message.content)
        
        result = {
            "status": "processed",
            "result": processed_transcript
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
