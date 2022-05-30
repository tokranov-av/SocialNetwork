from rest_framework.generics import CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from .models import Posts, UserReactions
from .serialisers import (
    UserRegistrationSerializer, PostsSerializer, PostDetailSerializer,
    PostAddSerializer
)
from django.contrib.auth import get_user_model
from .pagination import PostsPagination
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class RegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class PostsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    pagination_class = PostsPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        instance.view_count += 1
        instance.save(update_fields=['view_count', ])
        serializer.context['request'] = request
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def vote(self, request, *args, **kwargs):

        value = request.GET.get('value', None)
        if value not in ['-1', '0', '1']:
            return Response(
                {'error': 'value должен быть равен -1, 0, или 1.'}, 400
            )
        current_post = self.get_object()
        current_user = request.user

        user_reaction = UserReactions.objects.filter(
            user=current_user, post=current_post).first()

        if value == '-1':
            message = 'Вы поставили Dislike!'
        elif value == '1':
            message = 'Вы поставили Like!'
        else:
            message = 'Вы удалили оценку.'

        if not user_reaction:
            UserReactions.objects.create(
                user=current_user, post=current_post, reaction=value)
            if value == '0':
                message = 'Оценка не изменилась.'
        elif user_reaction.reaction != value:
            user_reaction.reaction = value
            user_reaction.save(update_fields=['reaction'])
        else:
            message = 'Оценка не изменилась.'

        return Response(
            {'message': message}, 200
        )


class AddPostAPIView(CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostAddSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
