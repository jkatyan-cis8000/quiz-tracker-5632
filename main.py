import json
import os
from question import Question, QuestionType
from quiz import Quiz
from interface import QuizInterface
from loader import load_questions_from_json


def load_config(config_path: str = "config.json") -> dict:
    """Load configuration from JSON file or use defaults."""
    defaults = {
        "question_file": "questions.json",
        "default_points": 10,
        "show_correct_answers_default": False
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                defaults.update(config)
        except (json.JSONDecodeError, IOError):
            pass
    
    return defaults


def main():
    # Load configuration
    config = load_config()
    
    # Create quiz
    quiz = Quiz()
    quiz.show_correct_answers = config.get("show_correct_answers_default", False)
    
    # Load questions from file
    question_file = config.get("question_file", "questions.json")
    
    try:
        questions = load_questions_from_json(question_file)
        for q in questions:
            quiz.add_question(q)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("No questions loaded. Exiting.")
        return
    except ValueError as e:
        print(f"Error loading questions: {e}")
        return
    
    # Run the quiz
    interface = QuizInterface(quiz)
    interface.run()


if __name__ == "__main__":
    main()
