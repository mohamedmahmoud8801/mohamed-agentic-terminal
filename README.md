# Mohamed Agentic Terminal

**Turn AI agents into coding assistants that can execute commands, write Python code, manage files, and explore codebases through the Model Context Protocol (MCP).**

`mohamed-agentic-terminal` is an MCP server that gives AI applications access to terminal execution, Python scripting, file management, and code search tools.

Connect it to an MCP-compatible client and let AI agents perform practical development tasks instead of only generating code as text.

## ✨ Features

The package exposes nine tools:

| Tool | Description |
|---|---|
| `bash` | Execute shell commands. |
| `python_code` | Execute Python code directly. |
| `python_file` | Create and execute Python scripts. |
| `glob` | Find files using glob patterns. |
| `grep` | Search file contents for matching text. |
| `read_file` | Read file contents. |
| `write_file` | Create or update files. |
| `create_folder` | Create directories. |
| `delete_folder` | Delete directories. |

## 📦 Installation

### Option 1: Run with `uvx`

You can run the MCP server without manually installing it into your project.

First, install [uv](https://docs.astral.sh/uv/) if you haven't already.

Then run:

```bash
uvx --from mohamed-agentic-terminal agentic_terminal
```

### Option 2: Install in a Python project

If your project uses `uv`, run:

```bash
uv add mohamed-agentic-terminal
```

## 🔌 Connect to an MCP Client

Configure your MCP-compatible client to launch the server using `uvx`.

Example configuration:

```json
{
  "mcpServers": {
    "agentic_terminal": {
      "transport": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "mohamed-agentic-terminal",
        "agentic_terminal"
      ]
    }
  }
}
```

The configuration format may differ between MCP clients. Adapt the settings to your client's requirements if necessary.

## 🤖 Usage with LangChain and Ollama

This example demonstrates how to connect the MCP server to a LangChain agent using a local language model through Ollama.

### Step 1: Create a project

```bash
uv init agentic-terminal-demo
cd agentic-terminal-demo
uv add langchain langchain-mcp-adapters langchain-ollama
```

### Step 2: Install and prepare Ollama

Install [Ollama](https://ollama.com/) if it isn't already installed.

Download the model:

```bash
ollama pull qwen2.5:7b-instruct
```

Make sure Ollama is running before executing the example.

### Step 3: Create `agent.py`

```python
import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama


async def main():
    # Connect to the MCP server
    client = MultiServerMCPClient(
        {
            "terminal": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                    "--from",
                    "mohamed-agentic-terminal",
                    "agentic_terminal",
                ],
            }
        }
    )

    # Discover the available MCP tools
    tools = await client.get_tools()

    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}")

    # Initialize the local LLM
    model = ChatOllama(
        model="qwen2.5:7b-instruct",
        temperature=0,
    )

    # Create the AI agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a coding assistant. "
            "Use the available tools to create, inspect, "
            "and execute code when needed."
        ),
    )

    # Define a coding task
    task = """
    Create a Python file named calculator.py with functions for:
    - Addition
    - Subtraction
    - Multiplication
    - Division

    Handle division by zero.
    Include a small demonstration in the script.
    Run the script and verify that it works.
    """

    # Execute the task
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": task,
                }
            ]
        }
    )

    print("\nAgent response:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 4: Run the agent

```bash
uv run python agent.py
```

The agent discovers the available MCP tools and can call them to complete the requested task.

In this example, the agent is asked to create a calculator script, execute it, and verify the result.

After execution, inspect the generated `calculator.py` file and run it independently if needed:

```bash
cat calculator.py
python calculator.py
```

**Note:** The example uses a local Ollama model, but you can adapt it to another model supported by your LangChain integration.

## 💡 Use Cases

### 1. AI Coding Assistants

Build agents that can:
- Generate Python scripts.
- Execute code and inspect the results.
- Read error messages and attempt corrections.
- Modify existing source files.

### 2. Codebase Exploration

Allow agents to:
- Search for files by pattern.
- Find matching text in source code.
- Read files to understand an existing project.
- Explore project structures.

### 3. File Management

Enable agents to:
- Create project directories.
- Generate new files.
- Update existing files.
- Organize development workflows.

### 4. Development Automation

Combine shell commands, Python execution, and file operations to automate repetitive programming tasks.

### 5. Local AI Agents

Connect local LLMs to MCP tools through frameworks such as LangChain, without requiring a hosted LLM API for inference.

## ⚙️ How It Works

```text
              User Request
                   |
                   v
              AI Agent (LLM)
                   |
                   v
                MCP Client
                   |
                   v
        Agentic Terminal MCP Server
                   |
          +--------+--------+
          |        |        |
          v        v        v
         Bash    Python   File Tools
          |        |        |
          +--------+--------+
                   |
                   v
             Tool Results
                   |
                   v
              AI Agent
```

The LLM determines which tools to call based on the task. The MCP server exposes the available capabilities and returns tool results to the client.

## 🛠️ Technology Stack

- Python
- Model Context Protocol (MCP)
- FastMCP
- LangChain integration
- Ollama-compatible local LLM workflows

## ⚠️ Important Notes

- This package provides tools to AI applications; it does not include or host an LLM.
- An MCP-compatible client is required to interact with the server.
- Shell commands and file operations run in the environment where the MCP server executes.
- AI-generated code and command results should be reviewed and tested.
- Use an appropriately controlled environment when allowing an agent to execute commands or modify files.

## 🔗 Links

- **PyPI:** https://pypi.org/project/mohamed-agentic-terminal/
- **Model Context Protocol:** https://modelcontextprotocol.io/
- **uv Documentation:** https://docs.astral.sh/uv/
- **Ollama:** https://ollama.com/

## 📄 License

See the project repository for license information.
---

# MCP Gateway

A Dockerized gateway that connects multiple MCP servers through one Streamable HTTP endpoint.

## Architecture

- DuckDuckGo MCP Server
- Agentic Terminal MCP Server
- Streamable HTTP transport

## Run with Docker

Pull the image:

    docker pull mmahmoud15901/mcp-gateway:0.1.2

Run the Gateway locally:

    docker run -d --name mcp-gateway -p 127.0.0.1:8001:8001 mmahmoud15901/mcp-gateway:0.1.2

View logs:

    docker logs -f mcp-gateway

## MCP Endpoint

    http://127.0.0.1:8001/mcp

Use Streamable HTTP transport.

## Security

The Agentic Terminal server can execute shell commands and Python code and modify files. Keep the Gateway bound to localhost. Do not expose it publicly without authentication and access controls.

Never commit credentials or `.env` files.

## Docker Image

https://hub.docker.com/r/mmahmoud15901/mcp-gateway

Image tag: `0.1.2`