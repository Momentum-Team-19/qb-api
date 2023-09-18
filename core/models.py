from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


class User(AbstractUser):
    photo = models.ImageField(upload_to="user_profile_photos", null=True, blank=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    accepted = models.BooleanField(null=True)

    def __str__(self):
        return self.text


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        null=True,
        blank=True,
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(question__isnull=False) & models.Q(answer__isnull=True)
                    | models.Q(answer__isnull=False) & models.Q(question__isnull=True)
                ),
                name="one_of_two_fields_null_constraint",
            )
        ]

    def __str__(self):
        return f"{self.user} bookmarks"
