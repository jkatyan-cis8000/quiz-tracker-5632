# Quiz Tracker Architecture

## Overview
A configurable trivia quiz program that supports multiple-choice and short-answer questions, tracks scores, and optionally displays correct answers after completion.

## Module Structure

### 1. `question.py` - Core Question Classes
**Responsibility:** Define data structures for questions and their answers.

**Classes:**
- `QuestionType` (Enum): `MULTIPLE_CHOICE`, `SHORT_ANSWER`
- `Question`: 
  - `id`: str
  - `question_text`: str
  - `options`: List[str] (for multiple-choice)
  - `correct_answer`: str (normalized for comparison)
  - `question_type`: QuestionType
  - `points`: int

**Methods:**
- `is_correct(user_answer: str) -> bool`: Normalize and compare answers

### 2. `quiz.py` - Quiz Engine
**Responsibility:** Manage the quiz flow, scoring, and question tracking.

**Classes:**
- `Quiz`:
  - `questions`: List[Question]
  - `current_question_index`: int
  - `score`: int
  - `user_answers`: List[Tuple[Question, str, bool]]
  - `show_correct_answers`: bool (configurable)

**Methods:**
- `add_question(question: Question)`: Add question to quiz
- `get_current_question() -> Question`: Get current question
- `answer_current(user_answer: str) -> bool`: Record answer, update score
- `has_next() -> bool`: Check if more questions remain
- `next_question()`: Advance to next question
- `get_summary() -> dict`: Return quiz results (score, total, answers)
- `finish() -> dict`: End quiz and return full summary with correct answers if enabled

### 3. `loader.py` - Question Bank Loader
**Responsibility:** Load questions from JSON files with configurable format.

**Functions:**
- `load_questions_from_json(filepath: str) -> List[Question]`: Parse JSON and create Question objects
  - Supports both single question format and array format
  - Validates required fields
  - Normalizes answer formats

**JSON Format Example:**
```json
{
  "questions": [
    {
      "id": "q1",
      "question": "What is 2+2?",
      "type": "multiple_choice",
      "options": ["3", "4", "5", "6"],
      "correct_answer": "4",
      "points": 10
    },
    {
      "id": "q2",
      "question": "Capital of France?",
      "type": "short_answer",
      "correct_answer": "Paris",
      "points": 10
    }
  ]
}
```

### 4. `interface.py` - Interactive UI
**Responsibility:** Handle user interaction, input, and output display.

**Classes:**
- `QuizInterface`:
  - `quiz`: Quiz instance
  - `show_correct_after`: bool

**Methods:**
- `display_question(question: Question)`: Print question and options
- `get_user_answer() -> str`: Get and validate user input
- `display_feedback(is_correct: bool, correct_answer: str)`: Show immediate feedback
- `display_summary(summary: dict)`: Show final results
- `prompt_show_correct_answers() -> bool`: Ask user if they want to see correct answers
- `run()`: Main game loop

### 5. `main.py` - Entry Point
**Responsibility:** Wire everything together and run the application.

**Functions:**
- `main()`: Load config, create quiz, run interface

**Configuration Options (config.json):**
```json
{
  "question_file": "questions.json",
  "default_points": 10,
  "show_correct_answers_default": false
}
```

## Module Dependencies
```
main.py
   ├── interface.py
   │      ├── quiz.py
   │      └── loader.py
   ├── quiz.py
   │      └── question.py
   └── loader.py
          └── question.py
```

## File Ownership
- `question.py`: Core data structures (shared, read-only after creation)
- `quiz.py`: Quiz engine logic (shared)
- `loader.py`: JSON parsing and loading (shared)
- `interface.py`: User interface (shared)
- `main.py`: Entry point (shared)
- `questions.json`: Sample question bank (sample data)
- `config.json`: Configuration file (sample config)

## Interfaces (Contracts)

**Question API:**
- `is_correct(user_answer)` must normalize both strings (lowercase, strip whitespace)

**Quiz API:**
- `answer_current()` returns `True` if correct, `False` otherwise
- `get_summary()` returns: `{score: int, total: int, answered: List[Tuple[Question, str, bool]]}`
- `finish()` returns full summary including correct answers for each question

**Loader API:**
- Returns list of `Question` objects
- Raises `FileNotFoundError` or `ValueError` on invalid data

**Interface API:**
- `run()` is the main method that handles the entire quiz flow
