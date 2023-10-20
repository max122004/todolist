from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.permission import IsAuthorOrReadOnly
from goals.serializer import GoalCategorySerializer, GoalListSerializer, GoalSerializer, GoalCategoryCreateSerializer, \
    GoalCreateSerializer


class GoalCategoryCreateAPIVIew(CreateAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalCategoryListView(ListAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategorySerializer
    # pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_delete=False
        )

    def get(self, request, *args, **kwargs):
        goal_title = request.GET.get('title', None)
        if goal_title:
            self.queryset = self.queryset.filter(
                title__icontains=goal_title
            )
        return super().get(request, *args, **kwargs)


class GoalCategoryAPIView(RetrieveUpdateDestroyAPIView):
    queryset = GoalCategory.objects.all()
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_delete=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalListAPIView(ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend
    ]
    filter_class = GoalDateFilter

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_delete=False
        )

    def get(self, request, *args, **kwargs):
        title_goals = request.GET.get('title', None)
        if title_goals:
            self.queryset = self.queryset.filter(
                title__icontains=title_goals
            )
        return super().get(request, *args, **kwargs)


class GoalAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_delete=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateAPIView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_delete=False
        )