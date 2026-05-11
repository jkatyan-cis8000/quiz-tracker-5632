from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"


@dataclass
class Question:
    id: str
    question_text: str
    options: Optional[List[str]]
    correct_answer: str
    question_type: QuestionType
    points: int = 10

    def is_correct(self, user_answer: str) -> bool:
        normalized_user = user_answer.lower().strip()
        normalized_correct = self.correct_answer.lower().strip()
        return normalized_user == normalized_correct
