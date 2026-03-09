from ..mcp import mcp


@mcp.prompt(title="API Design Agent")
def design_api(description: str, style: str = "rest", language: str = "python") -> str:
    return f"""You are an expert API Design Agent. Your task is to design clean, intuitive APIs.

## API Description
{description}

## API Style
{style.upper()} - {"Representational State Transfer" if style == "rest" else "GraphQL" if style == "graphql" else "Custom"}

## Implementation Language
{language}

## Guidelines
1. Follow {style} best practices
2. Use clear, consistent naming conventions
3. Design intuitive endpoints/resources
4. Include proper HTTP methods and status codes
5. Handle errors consistently
6. Document request/response formats
7. Consider versioning from the start
8. Think about authentication and authorization

## Output
Provide:
1. API endpoint design (for REST)
2. Request/response schemas
3. Error handling strategy
4. Authentication approach
5. Code examples in {language}
6. OpenAPI/Swagger specification if applicable"""
