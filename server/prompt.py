import json
import re


processor_prompt = """
# Task
You are a helpful assistant that processes therapy session transcripts and fills out templates based on the transcript.


# Context
## Transcript:
{transcript}


# Instructions
1. Read the transcript and understand the context of the session.
2. Read the template and understand the fields that need to be filled out.
3. Fill out the template based on the transcript.

# Response
You must always respond with JSON only. Do not include any other text or comments. JSON format:
{template}

"""

def extract_json(response):
    """Extract JSON from the LLM response """
    try:
        print(f"Extracting JSON from raw response:\n{response}\n\n-------")
        # First attempt: look for JSON inside code blocks
        code_blocks = re.findall(r'```(?:json)?([\s\S]*?)```', response)
        if code_blocks:
            for block in code_blocks:
                try:
                    return json.loads(block.strip())
                except:
                    continue
        
        # Second attempt: look for JSON enclosed in braces
        json_candidates = re.findall(r'({[\s\S]*?})', response)
        if json_candidates:
            for candidate in json_candidates:
                try:
                    return json.loads(candidate)
                except:
                    continue
        
        # Third attempt: try the entire response as JSON
        return json.loads(response)
    except:
        # If all extraction attempts fail, wrap the response in our expected format
        print(f"Failed to extract json")
        
        return None