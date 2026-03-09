from mcp.server.fastmcp.prompts import base

from ..mcp import mcp


@mcp.prompt(title="Debug Assistant Agent")
def debug_error(error: str, code: str = "", context: str = "") -> list[base.Message]:
    system_prompt = """You are an expert Debug Assistant. Your role is to help users diagnose and fix bugs in their code.

## Debugging Approach
1. First, understand the error message and stack trace
2. Ask clarifying questions if needed
3. Identify potential root causes
4. Provide step-by-step solutions with code examples
5. Suggest prevention strategies

## Communication Style
- Be methodical and systematic
- Explain your reasoning
- Provide actionable fixes
- Consider edge cases"""

    messages = [base.Message(role="system", content=system_prompt)]

    if code:
        messages.append(
            base.Message(
                role="user",
                content=f"I'm seeing this error:\n\n{error}\n\nHere is the relevant code:\n```\n{code}\n```",
            )
        )
    else:
        messages.append(base.Message(role="user", content=f"I'm seeing this error:\n\n{error}"))

    if context:
        messages.append(base.Message(role="user", content=f"Additional context:\n{context}"))

    messages.append(
        base.Message(
            role="assistant",
            content="I'll help you debug this. Let me analyze the error and provide solutions.\n\nCould you also tell me:\n1. What have you tried so far?\n2. Is this happening consistently or only in specific conditions?",
        )
    )

    return messages
