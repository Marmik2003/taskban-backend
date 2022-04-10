from django.contrib.auth import get_user_model, login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, mixins, filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from taskban_backend.boards.models import Board
from taskban_backend.users.api.serializers import RegisterSerializer, UserSerializer, UserDetailSerializer, \
    AvatarSerializer, UserSearchSerializer
from taskban_backend.users.models import Avatar
from taskban_backend.users.permissions import IsSelf

User = get_user_model()


class ExcludeBoardMembersFilter(filters.BaseFilterBackend):

    result_limit = 8
    filter_param = "board"

    def filter_queryset(self, request, queryset, view):
        board_id = request.query_params.get(self.filter_param)
        try:
            board = Board.objects.get(id=board_id)
        except (Board.DoesNotExist, ValueError):
            return queryset

        return queryset.exclude(id__in=board.members.all())[: self.result_limit]


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permissions_classes = [permissions.AllowAny]


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsSelf]

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "update":
            return UserDetailSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"])
    def update_avatar(self, request, pk):
        avatar_id = request.data.get("id")
        avatar = Avatar.objects.get(id=avatar_id)
        user = self.get_object()
        user.avatar = avatar
        user.save()
        return Response(AvatarSerializer(instance=avatar).data)


class UserSearchView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter, ExcludeBoardMembersFilter]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["username"]

    def get(self, request, *args, **kwargs):
        params = request.query_params
        board_id = params.get("board", "")
        search = params.get("search", "")
        if not board_id.isdigit() or not Board.objects.filter(id=board_id).exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        if len(search) < 3:
            return Response([])

        return super().get(request, *args, **kwargs)

