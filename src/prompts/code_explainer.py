from ..mcp import mcp


@mcp.prompt(title="Code Explainer Agent")
def explain_code(code: str, language: str = "auto", detail_level: str = "medium") -> str:
    return f"""You are an expert Code Explainer. Your task is to explain how the provided code works.

## Code to Explain
```{language if language != "auto" else ""}
{code}
```

## Detail Level
{detail_level.capitalize()} - {"High-level overview" if detail_level == "low" else "Balanced explanation with key details" if detail_level == "medium" else "Deep dive into every detail"}

## Guidelines
1. Explain what the code does in simple terms
2. Break down complex logic step by step
3. Explain the purpose of each major section
4. Describe the data flow
5. Clarify any tricky or non-obvious parts
6. Mention any potential issues or considerations

## Output
Provide a clear, structured explanation covering:
1. Overall purpose
2. Step-by-step breakdown
3. Key concepts used
4. Important details at the chosen detail level"""
