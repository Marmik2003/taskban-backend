from rest_framework import routers

from taskban_backend.boards.api.views import (
    BoardViewSet,
    ColumnViewSet,
    LabelViewSet,
    TaskViewSet,
    CommentViewSet,
)

app_name = "boards"

board_router = routers.DefaultRouter()
board_router.register(r"boards", BoardViewSet)
column_router = routers.DefaultRouter()
column_router.register(r"columns", ColumnViewSet)
labels_router = routers.DefaultRouter()
labels_router.register(r"labels", LabelViewSet)
tasks_router = routers.DefaultRouter()
tasks_router.register(r"tasks", TaskViewSet)
comments_router = routers.DefaultRouter()
comments_router.register(r"comments", CommentViewSet)

urlpatterns = board_router.urls + column_router.urls + labels_router.urls + tasks_router.urls + comments_router.urls
