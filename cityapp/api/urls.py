from django.urls import path
from api.user_views import *
from api.community_view import *
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Community API')

app_name = "api"

urlpatterns = [
    path('users/register', UserRegistrationAPIView.as_view(), name="register"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),

    path('community/swagger/', schema_view),

    path('community/create/', CreateCommunityAPIView.as_view(), name="create-community"),
    path('community/join/', JoinCommunityAPIView.as_view(), name="join-community"),
    path('community/search/', SearchCommunitiesAPIView.as_view(), name="search-community"),
    path('community/latest-posts/', UsersLatestPostsListAPIView.as_view(), name="latest-posts"),

    path('comment/create/', CommentCreateAPIView.as_view(), name="comment-create"),
    path('comment/create/<pk>/', CommentCreateAPIView_ForSpecificPost.as_view(), name="comment-create-post"),

    path('comment/list/', CommentListAPIView.as_view(), name="comment-list"),
    path('comment/delete/<pk>/', CommentDeleteAPIView.as_view(), name="comment-delete"),
    path('comment/update/<pk>/', CommentUpdateAPIView.as_view(), name="comment-update"),

]
