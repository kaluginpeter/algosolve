from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from algorithm import models as algorithm_models
from structure import models as structure_models


class FullUserSerializer(ModelSerializer):

    class Meta:
        model = algorithm_models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(FullUserSerializer, self).update(instance, validated_data)

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = algorithm_models.User
        fields = ('username', 'first_name', 'last_name', )
        read_only_fields = ('password', 'username', 'first_name', 'last_name')


class AlgortihmsToCategorySertializer(ModelSerializer):
    class Meta:
        model = algorithm_models.Algorithm
        fields = ('id', 'title', 'slug')


class CategoryAlgorithmSerializer(ModelSerializer):
    algorithms = AlgortihmsToCategorySertializer(many=True, required=False)

    class Meta:
        model = algorithm_models.Category
        fields = (
            'id', 'is_published', 'created_at',
            'title', 'slug', 'algorithms'
        )


class FullCategoryAlgorithmSerializer(ModelSerializer):
    algorithms = AlgortihmsToCategorySertializer(many=True, required=False)

    class Meta:
        model = algorithm_models.Category
        fields = (
            'id', 'is_published', 'created_at',
            'title', 'description', 'slug', 'algorithms'
        )


class UrlToTheoryAlgorithmSerializer(ModelSerializer):
    algorithm = SerializerMethodField()

    class Meta:
        model = algorithm_models.UrlAlgorithm
        fields = (
            'id', 'is_published', 'created_at',
            'algorithm', 'title', 'url'
        )

    def get_algorithm(self, obj):
        return obj.algorithm.slug


class UrlToOnlineTaskAlgorithmSerializer(ModelSerializer):
    algorithm = SerializerMethodField()

    class Meta:
        model = algorithm_models.UrlTaskAlgorithm
        fields = (
            'id', 'is_published', 'created_at',
            'algorithm', 'title', 'url'
        )

    def get_algorithm(self, obj):
        return obj.algorithm.slug


class TaskToAlgorithmSerializer(ModelSerializer):
    algorithm = SerializerMethodField()

    class Meta:
        model = algorithm_models.TaskAlgorithm
        fields = ('id', 'algorithm', 'text')

    def get_algorithm(self, obj):
        return obj.algorithm.slug


class ImageToAlgorithmSerializer(ModelSerializer):
    algorithm = SerializerMethodField()

    class Meta:
        model = algorithm_models.ImageAlgorithm
        fields = (
            'id', 'is_published', 'created_at',
            'algorithm', 'image', 'caption', 'alt'
        )

    def get_algorithm(self, obj):
        return obj.algorithm.slug


class CommentToAlgorithmSerializer(ModelSerializer):
    algorithm = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = algorithm_models.Comment
        fields = ('id', 'author', 'algorithm', 'text', 'created_at')

    def get_algorithm(self, obj):
        return obj.algorithm.slug

    def get_author(self, obj):
        return obj.author.username


class AlgorithmSerializer(ModelSerializer):
    category = SerializerMethodField()

    class Meta:
        model = algorithm_models.Algorithm
        fields = (
            'id', 'is_published', 'created_at',
            'category', 'title', 'slug'
        )

    def get_category(self, obj):
        return obj.category.slug


class FullAlgorithmSerializer(ModelSerializer):
    category = SerializerMethodField()
    url_to_theory_algorithm = UrlToTheoryAlgorithmSerializer(
        many=True, required=False
    )
    url_to_online_tasks = UrlToOnlineTaskAlgorithmSerializer(
        many=True, required=False
    )
    task_to_algorithm = TaskToAlgorithmSerializer(many=True, required=False)
    photo_algorithm = ImageToAlgorithmSerializer(many=True, required=False)
    comments = CommentToAlgorithmSerializer(many=True, required=False)

    class Meta:
        model = algorithm_models.Algorithm
        fields = ('id', 'is_published', 'created_at', 'category', 'title',
                  'description', 'theory', 'realization', 'example', 'slug',
                  'url_to_online_tasks', 'url_to_theory_algorithm',
                  'task_to_algorithm', 'photo_algorithm', 'comments')

    def get_category(self, obj):
        return obj.category.slug


class CommentAlgorithmSerializer(ModelSerializer):
    algorithm = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = algorithm_models.Comment
        fields = ('id', 'created_at', 'algorithm', 'author', 'text')
        read_only_fields = ('id', 'created_at', 'algorithm', 'author')

    def get_algorithm(self, obj):
        return obj.algorithm.slug

    def get_author(self, obj):
        return obj.author.username


class DataStructureToCategorySertializer(ModelSerializer):

    class Meta:
        model = structure_models.DataStructure
        fields = ('id', 'title', 'slug')


class CategoryDataStructureSerializer(ModelSerializer):
    data_structures = DataStructureToCategorySertializer(
        many=True, required=False
    )

    class Meta:
        model = structure_models.CategoryDateStructure
        fields = (
            'id', 'is_published', 'created_at',
            'title', 'slug', 'data_structures'
        )


class FullCategoryDataStructureSerializer(ModelSerializer):
    data_structures = DataStructureToCategorySertializer(
        many=True, required=False
    )

    class Meta:
        model = structure_models.CategoryDateStructure
        fields = (
            'id', 'is_published', 'created_at',
            'title', 'description', 'slug', 'data_structures'
        )


class UrlToTheoryDataStructureSerializer(ModelSerializer):
    data_structure = SerializerMethodField()

    class Meta:
        model = structure_models.UrlDataStructure
        fields = (
            'id', 'is_published', 'created_at',
            'data_structure', 'title', 'url'
        )

    def get_data_structures(self, obj):
        return obj.data_structure.slug


class TaskToDataStructureSerializer(ModelSerializer):
    data_structure = SerializerMethodField()

    class Meta:
        model = structure_models.TaskDataStructure
        fields = ('id', 'data_structure', 'text')

    def get_data_structure(self, obj):
        return obj.data_structure.slug


class ImageToDataStructureSerializer(ModelSerializer):
    data_structure = SerializerMethodField()

    class Meta:
        model = structure_models.ImageDataStructure
        fields = (
            'id', 'is_published', 'created_at',
            'data_structure', 'image', 'caption', 'alt'
        )

    def get_algorithm(self, obj):
        return obj.data_structure.slug


class CommentToDataStructureSerializer(ModelSerializer):
    data_structure = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = structure_models.CommentDataStructure
        fields = (
            'id', 'author', 'data_structure',
            'text', 'created_at'
        )

    def get_algorithm(self, obj):
        return obj.data_structure.slug

    def get_author(self, obj):
        return obj.author.username


class DataStructureSerializer(ModelSerializer):
    category = SerializerMethodField()

    class Meta:
        model = structure_models.DataStructure
        fields = (
            'id', 'is_published', 'created_at',
            'category', 'title', 'slug'
        )

    def get_category(self, obj):
        return obj.category.slug


class FullDataStructureSerializer(ModelSerializer):
    category = SerializerMethodField()
    url_to_theory_data_structure = UrlToTheoryDataStructureSerializer(
        many=True, required=False
    )
    task_to_data_structure = TaskToDataStructureSerializer(
        many=True, required=False
    )
    photo_data_structure = ImageToDataStructureSerializer(
        many=True, required=False
    )
    comments = CommentToDataStructureSerializer(many=True, required=False)

    class Meta:
        model = structure_models.DataStructure
        fields = ('id', 'is_published', 'created_at', 'category', 'title',
                  'description', 'theory', 'realization', 'example', 'slug',
                  'url_to_theory_data_structure', 'task_to_data_structure',
                  'photo_data_structure', 'comments')

    def get_category(self, obj):
        return obj.category.slug


class CommentDataStructureSerializer(ModelSerializer):
    data_structure = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = structure_models.CommentDataStructure
        fields = ('id', 'created_at', 'data_structure', 'author', 'text')
        read_only_fields = ('id', 'created_at', 'data_structure', 'author')

    def get_data_structure(self, obj):
        return obj.data_structure.slug

    def get_author(self, obj):
        return obj.author.username
