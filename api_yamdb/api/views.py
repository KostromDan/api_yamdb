from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from reviews.models import Category, Genre, Title
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer


class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete']
#    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete']
#    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]


#class TitleViewset(viewsets.ModelViewSet):

#  permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin]
