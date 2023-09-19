from rest_framework import serializers
from .models import Question, Answer, User, Bookmark
from taggit.serializers import TagListSerializerField, TaggitSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "email", "photo"]

    def update(self, instance, validated_data):
        if "file" in self.initial_data:
            file = self.initial_data.get("file")
            instance.photo.save(file.name, file, save=True)
            return instance
        # this call to super is to make sure that update still works for other fields
        return super().update(instance, validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Answer
        fields = ["id", "text", "author", "accepted"]


class AnswerDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Answer
        fields = ["id", "text", "accepted", "author"]


class AnswerWritableSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Answer
        fields = ["text", "author", "accepted"]


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    answers = AnswerSerializer(many=True, required=False)
    tags = TagListSerializerField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "title", "body", "author", "tags", "answers"]


class QuestionWritableSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Question
        fields = ["title", "body", "author", "tags"]


class QuestionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "title",
        ]


class AnswerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "question"]


class BookmarkListSerializer(serializers.ModelSerializer):
    question = QuestionNestedSerializer(required=False)
    answer = AnswerNestedSerializer(required=False)

    class Meta:
        model = Bookmark
        fields = ["question", "answer"]
