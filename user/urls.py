from django.urls import path, re_path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('list/', views.user_list_view),
    path('item/', views.UserListItemView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('signup/',views.SignupViews.as_view()),
    path('editpro/',views.EditProfileViews.as_view()),
    path('list/',views.UserList.as_view()),
    path('contactlist/',views.ContactList.as_view()),
    path('verify/username/<str:username>/validate/token/<str:token>/',views.GetVerification.as_view()),
    path('usersearch/', views.UserSearch.as_view())
]