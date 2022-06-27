from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title

from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          RegistrationSerializer, TitleSerializer,
                          UserMeSerializer, UserSerializer
                          )

User = get_user_model()


@permission_classes([IsAdmin])
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    queryset = User.objects.all()


class CreateListDeleteViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenreViewset(CreateListDeleteViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoryViewset(CreateListDeleteViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]


@api_view(['PATCH', 'GET'])
@permission_classes([IsAuthenticated])
def user_me_view(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserMeSerializer(instance=user, )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    serializer = UserMeSerializer(data=request.data, instance=user)
    if serializer.is_valid():
        role = request.data.get('role')
        if (role is not None
                and 'user' == user.role != role):
            json_error = {
                'role': user.role
            }
            return Response(json_error, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.validated_data)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    serializer = RegistrationSerializer(data=request.data, )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    json_err = {}
    if username is None:
        json_err['username'] = 'Имя пользователя не указано!'
    if confirmation_code is None:
        json_err[
            'confirmation_code'] = 'Код подтверждения не указан!'
    if len(json_err) != 0:
        return Response(json_err, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        json_err = {
            'username': f'Пользователя <{username}> не существует!'
        }
        return Response(json_err, status=status.HTTP_404_NOT_FOUND)
    if user.confirmation_code != confirmation_code:
        json_err = {
            'confirmation_code': 'Код подтверждения не верен!'
        }
        return Response(json_err, status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    json_ans = {
        'token': str(refresh.access_token),
    }
    return Response(json_ans, status=status.HTTP_200_OK)
