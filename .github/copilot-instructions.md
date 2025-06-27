# Edgar Project Coding Standards

**Note: These standards apply to all code in this project. Reference this document in code reviews and development discussions.**

## Comments
- Use comments only when code intent is not obvious
- Avoid redundant comments that restate what code does
- Focus on WHY, not WHAT

## Exception Handling
- Handle only specific exceptions you can meaningfully recover from
- Let unexpected exceptions bubble up naturally
- Avoid generic try/except blocks unless absolutely necessary

## Code Style
- Prefer self-documenting code over comments
- Use descriptive variable and method names
- Keep functions focused and small

## Development Workflow
- Reference these standards when providing code feedback
- Apply these principles consistently across all modules
- When in doubt, favor simplicity and clarity

## Tool Configuration
- Use `.editorconfig` for consistent formatting
- use ruff for linting and formatting
- IDE settings should align with these standards
