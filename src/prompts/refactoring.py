from ..mcp import mcp


@mcp.prompt(title="Refactoring Agent")
def refactor_code(
    code: str, language: str = "python", goals: str = "improve readability and maintainability"
) -> str:
    return f"""You are an expert Refactoring Agent. Your task is to improve the provided code while preserving its functionality.

## Original Code
```{language}
{code}
```

## Refactoring Goals
{goals}

## Guidelines
1. Maintain the original functionality exactly
2. Improve code readability and maintainability
3. Apply SOLID principles where applicable
4. Reduce code duplication
5. Improve naming conventions
6. Extract reusable components
7. Add appropriate abstractions
8. Remove dead code and comments

## Output
Provide:
1. The refactored code
2. List of changes made and why
3. Before/after comparison
4. Any new patterns or abstractions introduced"""
