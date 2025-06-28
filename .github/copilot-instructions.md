# Edgar Project Coding Standards

**Note: These standards apply to all code in this project. Reference this document in code reviews and development discussions.**

## Clean Code Principles

### Input Validation & Error Handling
- Validate inputs at function boundaries
- Use guard clauses for early validation
- Handle specific exceptions you can recover from
- Let unexpected exceptions bubble up naturally
- Fail fast when detecting invalid states

### Control Flow
- Use early returns to reduce nesting
- Avoid deep conditional nesting (max 2-3 levels)
- Prefer guard clauses over else statements
- Extract complex conditions into well-named functions

### Function Design
- Single responsibility per function
- Keep functions small and focused
- Use descriptive names that explain intent
- Prefer pure functions when possible

### Code Clarity
- Prefer self-documenting code over comments
- Use comments only for WHY, not WHAT
- Choose meaningful variable and function names
- Avoid redundant comments

## Examples

### Good Patterns
```python
def calculate_discount(price: float, user_type: str, item_count: int) -> float:
    if price <= 0:
        raise ValueError("Price must be positive")
    if not user_type:
        raise ValueError("User type is required")
    if item_count < 0:
        raise ValueError("Item count cannot be negative")
    
    if user_type == "premium":
        return price * 0.2
    
    if item_count >= 10:
        return price * 0.1
    
    return 0.0

def is_eligible_for_promotion(user: User) -> bool:
    return (
        user.is_active and 
        user.account_age_days >= 30 and 
        user.purchase_count > 0
    )
```

### Patterns to Avoid
```python
# Avoid: Deep nesting and unclear intent
def calculate_discount_bad(price, user_type, item_count):
    if price > 0:
        if user_type:
            if user_type == "premium":
                return price * 0.2
            else:
                if item_count >= 10:
                    return price * 0.1
                else:
                    return 0.0
    return 0.0

# Avoid: Generic exception handling
try:
    result = risky_operation()
except Exception:  # Too broad
    pass  # Silently ignoring errors
```

## Development Workflow
- Reference these standards when providing code feedback
- Apply these principles consistently across all modules
- Reference these standards in code reviews
- When in doubt, favor simplicity and clarity
- Refactor existing code to align with these standards

## Tool Configuration
- Use `.editorconfig` for consistent formatting
- Use ruff for linting and formatting
- IDE settings should align with these standards

