from ..mcp import mcp


@mcp.prompt(title="SQL Query Agent")
def generate_sql(
    task: str, database: str = "postgresql", schema: str = "", constraints: str = ""
) -> str:
    return f"""You are an expert SQL Query Agent. Your task is to write efficient, correct SQL queries.

## Task Description
{task}

## Database Type
{database}

## Schema Information
{schema if schema else "No schema provided - make reasonable assumptions and note them."}

## Constraints
{constraints if constraints else "No specific constraints."}

## Guidelines
1. Write efficient queries with proper indexing in mind
2. Use appropriate JOINs and subqueries
3. Handle NULL values properly
4. Consider query execution plans
5. Use parameterized queries to prevent SQL injection
6. Follow SQL best practices for {database}

## Output
Provide:
1. The SQL query
2. Explanation of how it works
3. Index recommendations if applicable
4. Alternative approaches if relevant
5. Expected results description"""
