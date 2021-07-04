from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from classroom.models import Course
from userprofile.models import BaseTimestamp

from ckeditor.fields import RichTextField

User = get_user_model()


class Question(BaseTimestamp):
    """
    Question model.
    """
    title = models.CharField(max_length=300)
    content = RichTextField()
    student = models.ForeignKey(User, related_name='course_questions', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)
    has_accepted_answer = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return question's title and student's fullname.
        return f"{self.title} | {self.student.full_name}"

    def get_answers_count(self):
        # Return answer's count.
        return Answer.objects.filter(question=self).count()

    def get_absolute_url(self):
        # Return absolute url of question by its id.
        return reverse("question:question-detail", kwargs={"course_slug": self.course.slug, "question_id": self.id})    

    
class Answer(BaseTimestamp):
    """
    Answer model.
    """
    student = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    content = RichTextField()
    up_votes = models.ManyToManyField(User, related_name='up_votes_answers', blank=True)
    down_votes = models.ManyToManyField(User, related_name='down_votes_answers', blank=True)
    votes = models.IntegerField(default=0)
    is_accepted_answer = models.BooleanField(default=False)

    def __str__(self):
        # Return question's title and student's fullname.
        return f"{self.question.title} | {self.student.full_name}"

    @property
    def calculate_votes(self):
        # Return the substraction of up and down votes.
        u_votes = self.up_votes.count()
        d_votes = self.down_votes.count()
        self.votes = u_votes - d_votes
        self.save()
        return self.votes

    def get_mark_as_answer_absolute_url(self):
        # Return ark answer absolute url of answer by its id.
        return reverse("question:mark-answer", kwargs={"course_slug": self.question.course.slug, "question_id": self.question.id, "answer_id": self.id})