from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from module.models import Module
from userprofile.models import BaseTimestamp

from ckeditor.fields import RichTextField

User = get_user_model()


class Quiz(BaseTimestamp):
    """
    Quiz model.
    """
    teacher = models.ForeignKey(User, related_name='quizzes', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    due = models.DateField()
    allowed_attempts = models.PositiveIntegerField()
    time_limit_mins = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        # Return title.
        return f"{self.title}"

    def get_absolute_url(self):
        # Return absolute url of quiz by its id.
        return reverse("quiz:quiz-detail", kwargs={"course_slug": self.module.course.slug, "quiz_id": self.id})

    def get_add_question_absolute_url(self):
        # Return add question absolute url of quiz by its id.
        return reverse("quiz:add-question", kwargs={"course_slug": self.module.course.slug, "quiz_id": self.id})

    def get_take_quiz_absolute_url(self):
        # Return take quiz absolute url of course by its id.
        return reverse("quiz:take-quiz", kwargs={"course_slug": self.module.course.slug, "quiz_id": self.id})    

    def get_submit_attempt_absolute_url(self):
        # Return submit attempt absolute url of quiz by its id.
        return reverse("quiz:submit-attempt", kwargs={"course_slug": self.module.course.slug, "quiz_id": self.id})


class QuizQuestion(BaseTimestamp):
    """
    Quiz Question model.
    """
    teacher = models.ForeignKey(User, related_name='quiz_questions', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=900)
    points = models.PositiveIntegerField()

    def __str__(self):
        # Return question's text.
        return f"{self.question_text}"


class QuizAnswer(BaseTimestamp):
    """
    Quiz Answer model.
    """
    question = models.ForeignKey(QuizQuestion, related_name='quiz_answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=900)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        # Return answer's text.
        return f"{self.answer_text}"


class Attempt(BaseTimestamp):
    """
    Attempter model.
    """
    student = models.ForeignKey(User, related_name='attempters', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='attempters', on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    question = models.ManyToManyField(QuizQuestion, related_name='attempts')
    answer = models.ManyToManyField(QuizAnswer, related_name='attempts')

    def __str__(self):
        # Return student's fullname and quiz's title.
        return f"{self.student.full_name} | {self.quiz.title}"

    def get_absolute_url(self):
        # Return absolute url of attempt by its id.
        return reverse("quiz:attempt-detail", kwargs={"course_slug": self.quiz.module.course.slug, "quiz_id": self.quiz.id, "attempt_id": self.id})


# class Attempt(BaseTimestamp):
#     """
#     Attempt model.
#     """
#     quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
#     attempter = models.ForeignKey(Attempter, related_name='attempts', on_delete=models.CASCADE)
#     question = models.ManyToManyField(Question, related_name='attempts')
#     answer = models.ManyToManyField(Answer, related_name='attempts')

#     def __str__(self):
#         # Return attempter's fullname and answer's text.
#         return f"{self.attempter.student.full_name}"

#     def get_absolute_url(self):
#         # Return absolute url of attempt by its id.
#         return reverse("quiz:attempt-detail", kwargs={"course_slug": self.quiz.module.course.slug, "quiz_id": self.quiz.id, "attempt_id": self.id})    