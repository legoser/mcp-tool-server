from ..mcp import mcp


@mcp.prompt(title="Test Generator Agent")
def generate_tests(
    code: str,
    language: str = "python",
    test_framework: str = "pytest",
    coverage_level: str = "basic",
) -> str:
    return f"""You are an expert Test Generator. Your task is to create comprehensive test cases for the provided code.

## Code to Test
```{language}
{code}
```

## Test Framework
{test_framework}

## Coverage Level
{coverage_level.capitalize()} - {"Focus on critical paths and edge cases" if coverage_level == "basic" else "Include edge cases, error handling, and boundary conditions" if coverage_level == "comprehensive" else "Maximum coverage including performance and integration tests"}

## Guidelines
1. Write tests that are readable and self-documenting
2. Cover happy path and error scenarios
3. Use descriptive test names that explain what is being tested
4. Include both positive and negative test cases
5. Mock external dependencies where appropriate
6. Follow the testing conventions of {test_framework}

## Output
Provide:
1. Complete test code with proper imports
2. Brief explanation of each test case
3. Any setup/teardown if needed"""
