from django.urls import path
from goals import views

urlpatterns = [
    path('goal_category/create/', views.GoalCategoryCreateAPIVIew.as_view()),
    path('goal_category/list/', views.GoalCategoryListView.as_view()),
    path('goal_category/<pk>/', views.GoalCategoryAPIView.as_view()),
    path('goal/create/', views.GoalCreateAPIView.as_view()),
    path('goal/<pk>/', views.GoalAPIView.as_view()),
    path('goal/list/', views.GoalListAPIView.as_view())
]