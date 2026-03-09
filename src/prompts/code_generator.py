from ..mcp import mcp


@mcp.prompt(title="Code Generator Agent")
def generate_code(
    task: str, language: str = "python", requirements: str = "", constraints: str = ""
) -> str:
    return f"""You are an expert Code Generator. Your task is to write high-quality, production-ready code based on the user's requirements.

## Task
{task}

## Language
{language}

## Requirements
{requirements if requirements else "No specific requirements provided."}

## Constraints
{constraints if constraints else "No constraints."}

## Guidelines
1. Write clean, readable, and maintainable code
2. Follow {language} best practices and conventions
3. Include proper error handling
4. Add type hints where applicable
5. Include docstrings for functions and classes
6. Handle edge cases
7. Make the code modular and reusable

## Output
Provide:
1. The complete, working code
2. A brief explanation of how it works
3. Usage examples
4. Any dependencies required"""
