from typing import List, Tuple, Optional
from question import Question


class Quiz:
    def __init__(self):
        self.questions: List[Question] = []
        self.current_question_index: int = 0
        self.score: int = 0
        self.user_answers: List[Tuple[Question, str, bool]] = []
        self.show_correct_answers: bool = False

    def add_question(self, question: Question) -> None:
        self.questions.append(question)

    def get_current_question(self) -> Optional[Question]:
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def answer_current(self, user_answer: str) -> bool:
        question = self.get_current_question()
        if question is None:
            return False
        is_correct = question.is_correct(user_answer)
        self.user_answers.append((question, user_answer, is_correct))
        if is_correct:
            self.score += question.points
        return is_correct

    def has_next(self) -> bool:
        return self.current_question_index < len(self.questions) - 1
    
    def get_total_questions(self) -> int:
        return len(self.questions)

    def next_question(self) -> None:
        self.current_question_index += 1

    def get_summary(self) -> dict:
        return {
            "score": self.score,
            "total": len(self.questions),
            "answered": len(self.user_answers)
        }

    def finish(self) -> dict:
        summary = self.get_summary()
        summary["show_correct_answers"] = self.show_correct_answers
        if self.show_correct_answers:
            summary["correct_answers"] = [
                {"question": q.question_text, "correct": q.correct_answer}
                for q in self.questions
            ]
        return summary
