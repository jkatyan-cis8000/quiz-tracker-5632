import json
from typing import List
from question import Question, QuestionType


def load_questions_from_json(filepath: str) -> List[Question]:
    """
    Load questions from a JSON file.
    
    Supports both single question object and array of questions format.
    Validates required fields and normalizes answers.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        List of Question objects
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the JSON is invalid or missing required fields
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Question file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filepath}: {e}")
    
    # Handle both single object and array format
    if isinstance(data, dict):
        if 'questions' in data:
            questions_data = data['questions']
        else:
            questions_data = [data]
    elif isinstance(data, list):
        questions_data = data
    else:
        raise ValueError(f"Invalid JSON structure in {filepath}: expected object or array")
    
    if not questions_data:
        raise ValueError(f"No questions found in {filepath}")
    
    questions = []
    for idx, q_data in enumerate(questions_data):
        # Validate required fields
        if 'id' not in q_data:
            raise ValueError(f"Question {idx + 1} missing required field 'id'")
        if 'question' not in q_data and 'question_text' not in q_data:
            raise ValueError(f"Question {idx + 1} missing required field 'question' or 'question_text'")
        if 'correct_answer' not in q_data and 'correctAnswer' not in q_data:
            raise ValueError(f"Question {idx + 1} missing required field 'correct_answer' or 'correctAnswer'")
        if 'type' not in q_data and 'question_type' not in q_data:
            raise ValueError(f"Question {idx + 1} missing required field 'type' or 'question_type'")
        
        # Get question text (support both field names)
        question_text = q_data.get('question') or q_data.get('question_text', '')
        
        # Get correct answer (support both field names)
        correct_answer = q_data.get('correct_answer') or q_data.get('correctAnswer', '')
        
        # Get question type
        question_type_str = q_data.get('type') or q_data.get('question_type', '').lower()
        if question_type_str == 'multiple_choice' or question_type_str == 'multiple-choice':
            q_type = QuestionType.MULTIPLE_CHOICE
        elif question_type_str == 'short_answer' or question_type_str == 'short-answer':
            q_type = QuestionType.SHORT_ANSWER
        else:
            raise ValueError(f"Invalid question type '{question_type_str}' in question {idx + 1}")
        
        # Get options (only for multiple-choice)
        options = q_data.get('options')
        if q_type == QuestionType.MULTIPLE_CHOICE and not options:
            raise ValueError(f"Question {idx + 1} is multiple-choice but has no options")
        
        # Get points (optional, default 10)
        points = q_data.get('points', 10)
        
        # Normalize correct answer to lowercase
        question = Question(
            id=str(q_data['id']),
            question_text=question_text,
            options=options,
            correct_answer=correct_answer.lower().strip(),
            question_type=q_type,
            points=points
        )
        questions.append(question)
    
    return questions
