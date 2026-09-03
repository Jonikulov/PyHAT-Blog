from django.urls import path

from blog_app.views import (
    # home,
    # create_article,
    ArticleCreateView,
    ArticleDeleteView,
    ArticleListView,
    ArticleUpdateView,
)

urlpatterns = [
    # path("", home, name="home"),
    # path("create/", create_article, name="create_article"),
    path("", ArticleListView.as_view(), name="home"),
    path("create/", ArticleCreateView.as_view(), name="create_article"),
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name="update_article"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete_article"),
]
