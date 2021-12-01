from django.urls import path

from base import views

urlpatterns = [
    path('', views.BanksListAPI.as_view(), name='banks_list'),
    path('branches/', views.BranchesListAPI.as_view(), name='branches_list'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

]