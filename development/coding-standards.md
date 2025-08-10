coding-standards.md

```markdown
# Coding Standards & Best Practices – Tender Insight Hub

## 1. Overview

This document defines coding conventions and quality standards to ensure consistency, readability, and maintainability across the Tender Insight Hub codebase.


## 2. Python Backend Standards

### 2.1 Style Guide  
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code formatting.  
- Use [Black](https://black.readthedocs.io/en/stable/) as the autoformatter.  
- Use meaningful, descriptive names for variables, functions, and classes.  
- Keep lines under 79 characters where possible.  

### 2.2 Imports  
- Standard library imports first, then third-party, then local imports.  
- Use absolute imports for clarity.

### 2.3 Type Annotations  
- All functions must have type hints for parameters and return types.  
- Use `typing` module as needed (`List`, `Optional`, `Dict`, etc.).

### 2.4 Docstrings  
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).  
- Document purpose, arguments, return types, and exceptions.

### 2.5 Error Handling  
- Use explicit exception handling with specific exception types.  
- Avoid bare `except:` blocks.

### 2.6 Logging  
- Use Python’s `logging` module instead of `print()`.  
- Configure log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).


## 3. Frontend Standards (React + Tailwind CSS)

### 3.1 Code Style  
- Use ES6+ syntax and features (arrow functions, destructuring, template literals).  
- Use Prettier for auto-formatting and ESLint for linting.

### 3.2 Component Structure  
- Functional components with hooks preferred.  
- Separate presentational and container components.  

### 3.3 Styling  
- Use Tailwind CSS utility classes exclusively. Avoid inline styles unless unavoidable.  

### 3.4 File Naming  
- Use `PascalCase` for components, `camelCase` for variables/functions.


## 4. Git Workflow

- Use **feature branches** for new work: `feature/short-description`.  
- Pull requests must be reviewed before merge.  
- Write clear, concise commit messages using conventional commits style:


## 5. Testing Practices

- Write tests for all new features before merging.  
- Keep tests isolated and independent.  
- Use descriptive test names that explain the behavior being tested.


## 6. Documentation

- Keep code comments minimal and focused on _why_, not _what_.  
- Update `.md` docs with every significant feature change.  
- Maintain accurate Swagger/OpenAPI specs.


## 7. Code Review Checklist

- Adherence to coding standards.  
- No obvious bugs or security flaws.  
- Proper test coverage and passing tests.  
- Clean, understandable code.  
- Proper documentation and comments.


End of Coding Standards.


