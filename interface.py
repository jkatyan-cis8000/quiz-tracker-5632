from typing import List


class QuizInterface:
    def __init__(self, quiz):
        self.quiz = quiz

    def display_question(self, question) -> None:
        print(f"\nQuestion {self.quiz.current_question_index + 1}: {question.question_text}")
        if question.options:
            for i, option in enumerate(question.options, 1):
                print(f"  {i}. {option}")

    def get_user_answer(self) -> str:
        return input("Your answer: ")

    def display_feedback(self, is_correct: bool, correct_answer: str) -> None:
        if is_correct:
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer is: {correct_answer}")

    def display_summary(self, summary: dict) -> None:
        print(f"\nFinal Score: {summary['score']} / {summary['total'] * 10}")
        print(f"Questions Answered: {summary['answered']}")

    def display_correct_answers(self, correct_answers: List[dict]) -> None:
        """Display all questions with their correct answers."""
        print("\n" + "=" * 50)
        print("CORRECT ANSWERS:")
        print("=" * 50)
        for i, answer in enumerate(correct_answers, 1):
            print(f"\n{i}. {answer['question']}")
            print(f"   Correct answer: {answer['correct']}")

    def prompt_show_correct_answers(self) -> bool:
        response = input("\nShow correct answers? (y/n): ").lower().strip()
        return response == 'y'

    def run(self) -> None:
        while True:
            question = self.quiz.get_current_question()
            if question is None:
                break
            self.display_question(question)
            user_answer = self.get_user_answer()
            is_correct = self.quiz.answer_current(user_answer)
            self.display_feedback(is_correct, question.correct_answer)
            if not self.quiz.has_next():
                break
            self.quiz.next_question()

        self.quiz.show_correct_answers = self.prompt_show_correct_answers()
        summary = self.quiz.finish()
        self.display_summary(summary)
        
        # Display correct answers if requested
        if summary.get('show_correct_answers') and summary.get('correct_answers'):
            self.display_correct_answers(summary['correct_answers'])
