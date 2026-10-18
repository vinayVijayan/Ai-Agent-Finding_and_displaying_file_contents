import os
import json
from typing import List, Dict, Any
from litellm import completion
from dotenv import load_dotenv

load_dotenv()


def list_files(directory: str = ".") -> List[str]:
    """Lists all files in the given directory path."""
    try:
        target_path = os.path.abspath(directory)
        if not os.path.exists(target_path):
            return [f"Error: Path '{directory}' does not exist."]
        
        return os.listdir(target_path)
    except Exception as e:
        return [f"Error listing directory '{directory}': {str(e)}"]

def read_file(file_name: str) -> str:
    """Reads the content of a specific file."""
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{file_name}': {str(e)}"



def parse_action(response_text: str) -> Dict[str, Any]:
    """Extracts and parses JSON action from the LLM's output."""
    try:
        text = response_text.strip()
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                try:
                    return json.loads(part)
                except json.JSONDecodeError:
                    continue
        return json.loads(text)
    except Exception as e:
        return {
            "tool_name": "error",
            "args": {"message": f"Failed to parse JSON. Raw output: {response_text}"}
        }


SYSTEM_RULES = """You are a file system AI agent. You can inspect files and directories to answer user queries.

AVAILABLE TOOLS:
1. list_files
   Description: Lists all files and directories in a given path. Pass "." for current directory or ".." to look at the parent directory.
   Format: {"tool_name": "list_files", "args": {"directory": "<path_string>"}}

2. read_file
   Description: Reads the raw text content of a specific file.
   Format: {"tool_name": "read_file", "args": {"file_name": "<filename_path>"}}

3. terminate
   Description: Delivers the final answer to the user and stops the loop.
   Format: {"tool_name": "terminate", "args": {"message": "<your full final answer>"}}

RULES:
- You MUST respond with ONLY a single valid JSON object per turn. Do not add conversational text outside the JSON.
- Take one step at a time.
- Once you have gathered enough information to answer the user's question, call the 'terminate' tool.
"""


def run_agent(user_query: str, max_iterations: int = 10): # Increased max_iterations to give it time to search
    memory: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_RULES},
        {"role": "user", "content": user_query}
    ]

    iterations = 0

    while iterations < max_iterations:
        print(f"\n--- Iteration {iterations + 1} ---")
        print("Agent thinking...")

        max_retries = 3
        response_text = ""
        
        for attempt in range(max_retries):
            try:
                llm_response = completion(
                    model="gemini/gemini-3.8-flash",
                    messages=memory
                )
                response_text = llm_response.choices[0].message.content
                break  # If successful, break out of the retry loop
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Waits 1s, 2s, then 4s
                    print(f"⚠️ API busy (Error 503/429). Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"\n❌ API Failed after {max_retries} attempts. Error: {str(e)}")
                    return  # Exit the agent entirely if the API is completely down

        if not response_text:
            break

        print(f"Agent response:\n{response_text}")

        action = parse_action(response_text)
        tool_name = action.get("tool_name")
        args = action.get("args", {})

        result: Any = "Action executed"

        # Execute Action
        if tool_name == "list_files":
            directory_path = args.get("directory", ".")
            files = list_files(directory_path)
            result = {"result": files}

        elif tool_name == "read_file":
            file_name = args.get("file_name", "")
            content = read_file(file_name)
            result = {"result": content}

        elif tool_name == "error":
            result = {"error": args.get("message", "Parsing error occurred")}

        elif tool_name == "terminate":
            print(f"\n[Agent Final Answer]:\n{args.get('message')}")
            break

        else:
            result = {"error": f"Unknown action: {tool_name}"}

        print(f"Action result: {result}")

        # Update Memory
        memory.extend([
            {"role": "assistant", "content": response_text},
            {"role": "user", "content": json.dumps(result)}
        ])

        if tool_name == "terminate":
            break

        iterations += 1

if __name__ == "__main__":
    task = input("Enter a task: ")
    run_agent(task)