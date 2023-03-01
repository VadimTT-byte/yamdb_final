from django.db.models import Avg
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title
from users.permissions import (IsAdministrator, IsAuthorOrReadOnly,
                               IsModerator, ReadOnly)

from .filters import FilterForTitle
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


class CreateListModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = PageNumberPagination
    permission_classes = [IsAdministrator | ReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    pass


class CategoryViewSet(CreateListModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdministrator | ReadOnly]
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleSerializer


class ParentReviewCommentViewSet(viewsets.ModelViewSet):
    ...
    pagination_class = PageNumberPagination
    permission_classes = [IsAdministrator | IsAuthorOrReadOnly | IsModerator]


class ReviewViewSet(ParentReviewCommentViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ParentReviewCommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
