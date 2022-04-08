from rest_framework import routers

from taskban_backend.boards.api.views import (
    BoardViewSet,
    ColumnViewSet,
    LabelViewSet,
    TaskViewSet,
    CommentViewSet,
)

app_name = "boards"

router = routers.DefaultRouter()
router.register(r"", BoardViewSet)
router.register(r"columns", ColumnViewSet)
router.register(r"labels", LabelViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = router.urls
