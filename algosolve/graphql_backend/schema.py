import graphene
from graphene_django import DjangoObjectType

from algorithm import models as algorithm_models
from structure import models as structure_models


class UserType(DjangoObjectType):
    class Meta:
        model = algorithm_models.User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'password')


class CategoryAlgorithmType(DjangoObjectType):
    class Meta:
        model = algorithm_models.Category
        fields = ('id', 'description', 'is_published',
                  'created_at', 'title', 'slug', 'algorithms')


class CategoryDataStructureType(DjangoObjectType):
    class Meta:
        model = structure_models.CategoryDateStructure
        fields = ('id', 'title', 'description', 'slug',
                  'is_published', 'created_at', 'data_structures')


class AlgorithmType(DjangoObjectType):
    class Meta:
        model = algorithm_models.Algorithm
        fields = ('id', 'is_published', 'created_at', 'category', 'title',
                  'description', 'theory', 'realization', 'example', 'slug',
                  'task_to_algorithm', 'photo_algorithm',
                  'url_to_theory_algorithm',
                  'url_to_online_tasks', 'comments')


class DataStructureType(DjangoObjectType):
    class Meta:
        model = structure_models.DataStructure
        fields = (
            'id', 'category', 'title', 'description',
            'theory', 'realization', 'example',
            'slug', 'is_published', 'created_at',
            'photo_data_structure', 'task_to_data_structure',
            'url_to_theory_data_structure', 'comments')


class ImageAlgorithmType(DjangoObjectType):
    class Meta:
        model = algorithm_models.ImageAlgorithm
        fields = ('id', 'algorithm', 'image', 'caption',
                  'alt', 'is_published', 'created_at')


class ImageDataStructureType(DjangoObjectType):
    class Meta:
        model = structure_models.ImageDataStructure
        fields = ('id', 'data_structure', 'image', 'caption',
                  'alt', 'is_published', 'created_at')


class TaskAlgorithmType(DjangoObjectType):
    class Meta:
        model = algorithm_models.TaskAlgorithm
        fields = ('id', 'text', 'algorithm')


class TaskDataStructureType(DjangoObjectType):
    class Meta:
        model = structure_models.TaskDataStructure
        fields = ('id', 'data_structure', 'text', 'is_published', 'created_at')


class UrlAlgorithmType(DjangoObjectType):
    class Meta:
        model = algorithm_models.UrlAlgorithm
        fields = ('id', 'title', 'algorithm',
                  'url', 'is_published', 'created_at')


class UrlDataStructureType(DjangoObjectType):
    class Meta:
        model = structure_models.UrlDataStructure
        fields = ('id', 'data_structure', 'title',
                  'is_published', 'created_at')


class UrlTaskAlgorithm(DjangoObjectType):
    class Meta:
        model = algorithm_models.UrlTaskAlgorithm
        fields = ('id', 'algorithm', 'title',
                  'url', 'is_published', 'created_at')


class CommentAlgorithmType(DjangoObjectType):
    class Meta:
        model = algorithm_models.Comment
        fields = ('id', 'algorithm', 'text', 'author', 'created_at')


class CommentDataStructureType(DjangoObjectType):
    class Meta:
        model = structure_models.CommentDataStructure
        fields = ('id', 'text', 'author', 'data_structure', 'created_at')


class Query(graphene.ObjectType):
    all_categories_algorithms = graphene.List(CategoryAlgorithmType)
    all_categories_data_structures = graphene.List(CategoryDataStructureType)
    category_algorithm_by_slug = graphene.Field(
        CategoryAlgorithmType,
        category_algorithm_slug=graphene.String(required=True)
    )
    category_data_structure_by_slug = graphene.Field(
        CategoryDataStructureType,
        category_data_structure_slug=graphene.String(required=True)
    )
    all_algorithms = graphene.List(AlgorithmType)
    all_data_structures = graphene.List(DataStructureType)
    algorithm_by_slug = graphene.Field(
        AlgorithmType,
        algorithm_slug=graphene.String(required=True)
    )
    data_structure_by_slug = graphene.Field(
        DataStructureType,
        data_structure_slug=graphene.String(required=True)
    )
    all_comments_algorithms = graphene.List(CommentAlgorithmType)
    all_comments_data_structures = graphene.List(CommentDataStructureType)
    algorithm_comment_by_id = graphene.Field(
        CommentAlgorithmType,
        algorithm_slug=graphene.String(required=True),
        comment_id=graphene.Int(required=True)
    )
    data_structure_comment_by_id = graphene.Field(
        CommentDataStructureType,
        data_structure_slug=graphene.String(required=True),
        comment_id=graphene.Int(required=True)
    )

    def resolve_all_categories_algorithms(root, info):
        return algorithm_models.Category.objects.all() \
            .prefetch_related('algorithms')

    def resolve_all_categories_data_structures(root, info):
        return structure_models.CategoryDateStructure.objects.all() \
            .prefetch_related('data_structures')

    def resolve_category_algorithm_by_slug(
            root, info, category_algorithm_slug
    ):
        try:
            return algorithm_models.Category.objects.prefetch_related(
                'algorithms').get(slug=category_algorithm_slug)
        except algorithm_models.Category.DoesNotExist:
            return None

    def resolve_category_data_structure_by_slug(
            root, info, category_data_structure_slug
    ):
        try:
            return structure_models.CategoryDateStructure.objects \
                .prefetch_related('data_structures') \
                .get(slug=category_data_structure_slug)
        except structure_models.CategoryDateStructure.DoesNotExist:
            return None

    def resolve_all_algorithms(root, info):
        return algorithm_models.Algorithm.objects.all()

    def resolve_all_data_structures(root, info):
        return structure_models.DataStructure.objects.all()

    def resolve_algorithm_by_slug(root, info, algorithm_slug):
        try:
            return algorithm_models.Algorithm.objects \
                .select_related('category').prefetch_related(
                    'photo_algorithm', 'task_to_algorithm',
                    'url_to_theory_algorithm',
                    'url_to_online_tasks', 'comments').get(slug=algorithm_slug)
        except algorithm_models.Algorithm.DoesNotExist:
            return None

    def resolve_data_structure_by_slug(root, info, data_structure_slug):
        try:
            return structure_models.DataStructure.objects \
                .select_related('category').prefetch_related(
                    'data_structures_images', 'task_to_data_structure',
                    'url_to_theory_data_structure', 'comments'
                ).get(slug=data_structure_slug)
        except structure_models.DataStructure.DoesNotExist:
            return None

    def resolve_all_comments_algorithms(root, info):
        return algorithm_models.Comment.objects.all()

    def resolve_all_comments_data_structures(root, info):
        return structure_models.CommentDataStructure.objects.all()

    def resolve_algorithm_comment_by_id(
            root, info, algorithm_slug, comment_id):
        try:
            return algorithm_models.Comment.objects.get(
                algorithm__slug=algorithm_slug,
                id=comment_id
            )
        except algorithm_models.Comment.DoesNotExist:
            return None

    def resolve_data_structure_comment_by_id(
            root, info, data_structure_slug, comment_id):
        try:
            return structure_models.CommentDataStructure.objects.get(
                data_structure__slug=data_structure_slug,
                id=comment_id
            )
        except structure_models.CommentDataStructure.DoesNotExist:
            return None


class CreateCommentAlgorithmMutation(graphene.Mutation):
    class Arguments:
        algorithm_slug = graphene.String()
        author = graphene.String()
        text = graphene.String()

    created_comment_algorithm = graphene.Field(CommentAlgorithmType)
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    @classmethod
    def mutate(cls, info, root, algorithm_slug, author, text):
        try:
            algorithm = algorithm_models.Algorithm.objects.get(
                slug=algorithm_slug
            )
        except algorithm_models.Algorithm.DoesNotExist:
            return CreateCommentAlgorithmMutation(
                ok=False, errors=['algorithm does not exist']
            )
        try:
            user = algorithm_models.User.objects.get(username=author)
        except algorithm_models.User.DoesNotExist:
            return CreateCommentAlgorithmMutation(
                ok=False, errors=['user not exist']
            )
        if len(text) < 2:
            return CreateCommentAlgorithmMutation(
                ok=False, errors=['text of comment should be greater than 1']
            )
        comment = algorithm_models.Comment(
            algorithm=algorithm, author=user, text=text
        )
        comment.save()
        return CreateCommentAlgorithmMutation(
            created_comment_algorithm=comment, ok=True, errors=[]
        )


class UpdateCommentAlgorithmMutation(graphene.Mutation):
    class Arguments:
        algorithm_slug = graphene.String()
        comment_id = graphene.ID()
        author = graphene.String()
        text = graphene.String()

    updated_comment_algorithm = graphene.Field(CommentAlgorithmType)
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    @classmethod
    def mutate(cls, info, root, algorithm_slug, author, text, comment_id):
        try:
            algorithm = algorithm_models.Algorithm.objects.get(
                slug=algorithm_slug
            )
        except algorithm_models.Algorithm.DoesNotExist:
            return UpdateCommentAlgorithmMutation(
                ok=False, errors=['algorithm does not exist']
            )
        try:
            comment = algorithm_models.Comment.objects.get(id=comment_id)
        except algorithm_models.Comment.DoesNotExist:
            return UpdateCommentAlgorithmMutation(
                ok=False, errors=['comment not exist']
            )
        if len(text) < 2:
            return UpdateCommentAlgorithmMutation(
                ok=False, errors=['text of comment should be greater than 1']
            )
        comment.text = text
        comment.save()
        return UpdateCommentAlgorithmMutation(
            updated_comment_algorithm=comment, ok=True, errors=[]
        )


class DeleteCommentAlgorithmMutation(graphene.Mutation):
    class Arguments:
        algorithm_slug = graphene.String()
        comment_id = graphene.ID()
        author = graphene.String()

    deleted_comment_algorithm = graphene.Field(CommentAlgorithmType)
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    @classmethod
    def mutate(cls, info, root, algorithm_slug, author, comment_id):
        try:
            algorithm = algorithm_models.Algorithm.objects.get(
                slug=algorithm_slug
            )
        except algorithm_models.Algorithm.DoesNotExist:
            return DeleteCommentAlgorithmMutation(
                ok=False, errors=['algorithm does not exist']
            )
        try:
            comment = algorithm_models.Comment.objects.get(id=comment_id)
        except algorithm_models.Comment.DoesNotExist:
            return DeleteCommentAlgorithmMutation(
                ok=False, errors=['comment not exist']
            )
        comment.delete()
        return DeleteCommentAlgorithmMutation(
            deleted_comment_algorithm=comment, ok=True, errors=[]
        )


class CreateCommentDataStructureMutation(graphene.Mutation):
    class Arguments:
        data_structure_slug = graphene.String()
        author = graphene.String()
        text = graphene.String()

    created_comment_data_structure = graphene.Field(CommentDataStructureType)

    @classmethod
    def mutate(cls, root, info, data_structure_slug, author, text):
        try:
            data_structure = structure_models.DataStructure.objects.get(
                slug=data_structure_slug
            )
        except structure_models.DataStructure.DoesNotExist:
            return CreateCommentDataStructureMutation(
                ok=False, errors=['data_structure not exist']
            )
        try:
            user = algorithm_models.User.objects.get(username=author)
        except algorithm_models.User.DoesNotExist:
            return CreateCommentDataStructureMutation(
                ok=False, errors=['user not exist']
            )
        comment = structure_models.CommentDataStructure(
            data_structure=data_structure, author=user, text=text
        )
        comment.save()
        return CreateCommentDataStructureMutation(
            created_comment_data_structure=comment
        )


class UpdateCommentDataStructureMutation(graphene.Mutation):
    class Arguments:
        data_structure_slug = graphene.String()
        comment_id = graphene.ID()
        author = graphene.String()
        text = graphene.String()

    updated_comment_data_structure = graphene.Field(CommentDataStructureType)
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    @classmethod
    def mutate(cls, info, root, data_structure_slug, author, text, comment_id):
        try:
            data_structure = structure_models.DataStructure.objects.get(
                slug=data_structure_slug
            )
        except structure_models.DataStructure.DoesNotExist:
            return UpdateCommentDataStructureMutation(
                ok=False, errors=['data structure does not exist']
            )
        try:
            comment = structure_models.CommentDataStructure.objects.get(
                id=comment_id
            )
        except structure_models.CommentDataStructure.DoesNotExist:
            return UpdateCommentDataStructureMutation(
                ok=False, errors=['comment not exist']
            )
        if len(text) < 2:
            return UpdateCommentDataStructureMutation(
                ok=False, errors=['text of comment should be greater than 1']
            )
        comment.text = text
        comment.save()
        return UpdateCommentDataStructureMutation(
            updated_comment_data_structure=comment, ok=True, errors=[]
        )


class DeleteCommentDataStructureMutation(graphene.Mutation):
    class Arguments:
        data_structure_slug = graphene.String()
        comment_id = graphene.ID()
        author = graphene.String()

    deleted_comment_data_structure = graphene.Field(CommentDataStructureType)
    ok = graphene.Boolean(required=True)
    errors = graphene.List(graphene.String, required=True)

    @classmethod
    def mutate(cls, info, root, data_structure_slug, author, comment_id):
        try:
            data_stucture = structure_models.DataStructure.objects.get(
                slug=data_structure_slug
            )
        except structure_models.DataStructure.DoesNotExist:
            return DeleteCommentDataStructureMutation(
                ok=False, errors=['data structure does not exist']
            )
        try:
            comment = structure_models.CommentDataStructure.objects.get(
                id=comment_id
            )
        except structure_models.CommentDataStructure.DoesNotExist:
            return DeleteCommentDataStructureMutation(
                ok=False, errors=['comment not exist']
            )
        comment.delete()
        return DeleteCommentDataStructureMutation(
            deleted_comment_data_structure=comment, ok=True, errors=[]
        )


class Mutation(graphene.ObjectType):
    add_comment_in_algorithm = CreateCommentAlgorithmMutation.Field()
    add_comment_in_data_structure = CreateCommentDataStructureMutation.Field()
    update_comment_in_algorithm = UpdateCommentAlgorithmMutation.Field()
    delete_comment_in_algorithm = DeleteCommentAlgorithmMutation.Field()
    update_comment_in_data_structure = UpdateCommentDataStructureMutation.Field()
    delete_comment_in_data_structure = DeleteCommentDataStructureMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
