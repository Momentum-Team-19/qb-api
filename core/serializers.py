from rest_framework import serializers
from .models import Question, Answer, User, Bookmark
from taggit.serializers import TagListSerializerField, TaggitSerializer
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "photo",
            "phone",
            "first_name",
            "last_name",
        ]

    def update(self, instance, validated_data):
        if "file" in self.initial_data:
            file = self.initial_data.get("file")
            instance.photo.save(file.name, file, save=True)
            return instance
        # this call to super is to make sure that update still works for other fields
        return super().update(instance, validated_data)


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "photo",
        ]


class AnswerSerializer(serializers.ModelSerializer):
    author = UserNestedSerializer(read_only=True)
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "text", "author", "accepted", "question"]


class AnswerDetailSerializer(serializers.ModelSerializer):
    author = UserNestedSerializer(read_only=True)
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "text", "accepted", "author", "question"]


class AnswerWritableSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Answer
        fields = ["text", "author", "accepted"]


class QuestionSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = UserNestedSerializer(read_only=True)
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


class UserProfileSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True, read_only=True)
    answers = AnswerNestedSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "photo",
            "phone",
            "first_name",
            "last_name",
            "questions",
            "answers",
        ]

    def create(self, validated_data):
        # Get the nested data for question and answer
        question_data = validated_data.pop('question', None)
        answer_data = validated_data.pop('answer', None)

        # Initialize variables
        question = None
        answer = None

        # Retrieve Question and Answer instances if they exist in the database
        if question_data:
            question = Question.objects.get(id=question_data['id'])
        
        if answer_data:
            answer = Answer.objects.get(id=answer_data['id'])

        # Create the Bookmark object
        bookmark = Bookmark.objects.create(question=question, answer=answer, **validated_data)
        
        return bookmark

