# EeveeLLM Test Suite

This directory contains all test files for the EeveeLLM project.

## Running Tests

All tests can be run from the project root:

```bash
# Run a specific test
python tests/test_name_memory.py

# Run all tests (if you have pytest installed)
pytest tests/
```

## Test Files

### Core Functionality Tests

- **test_brain_council.py** - Tests brain council voting system and decision-making
- **test_api.py** - Tests NanoGPT API client functionality
- **test_natural_language.py** - Tests natural language command detection

### Memory System Tests

- **test_name_memory.py** - Verifies Eevee can remember trainer's name
- **test_personal_info_memory.py** - Tests memory of personal information
- **test_enhanced_working_memory.py** - Tests 100-interaction working memory capacity
- **test_full_brain_council_memory.py** - Tests complete memory flow through brain council
- **test_memory_retrieval_fix.py** - Tests memory retrieval fixes
- **test_memory_fixes.py** - General memory system bug fixes
- **test_remember_fix.py** - Tests remember command functionality

### Command System Tests

- **test_command_responses.py** - Tests Eevee's natural responses to commands

### Bug Fix Tests

- **test_senior_review_fixes.py** - Tests fixes from senior code review:
  - Behavior patterns cleanup
  - Consensus level fix
  - Datetime error handling

### Legacy Tests

- **test_phase6.py** - Legacy test from development phases (can be archived)

## Adding New Tests

When adding new tests:
1. Name the file `test_<feature>.py`
2. Include docstrings explaining what's being tested
3. Add entry to this README
4. Ensure tests can run independently from project root
