from ..mcp import mcp


@mcp.prompt(title="Documentation Agent")
def generate_docs(code: str, language: str = "python", doc_format: str = "google") -> str:
    return f"""You are an expert Documentation Agent. Your task is to generate comprehensive documentation for the provided code.

## Code to Document
```{language}
{code}
```

## Documentation Format
{doc_format.capitalize()} style (Google, NumPy, or Sphinx)

## Guidelines
1. Write clear, concise documentation
2. Follow {doc_format} style conventions
3. Include descriptions for all public APIs
4. Document parameters, return values, and exceptions
5. Add usage examples
6. Include edge cases and limitations
7. Document dependencies

## Output
Provide:
1. Module-level docstring
2. Class/function docstrings with all sections
3. Usage examples
4. Any additional documentation needed"""
