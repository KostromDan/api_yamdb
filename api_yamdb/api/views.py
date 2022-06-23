from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import RegistrationSerializer, UserSerializer, GenreSerializer, CategorySerializer, TitleSerializer
from reviews.models import Category, Genre, Title

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    def get_queryset(self):
        username = self.kwargs.get('pk')
        if username is None:
            return User.objects.all()
        if username == 'me':
            return self.request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValidationError(f'Пользователя <{username}> не существует!')
        return user

    def get_permissions(self):
        # json = {
        #     'data': self.request.data,
        #     'kwargs': self.kwargs,
        #     'url': self.request.build_absolute_uri(),
        #     'metod': self.request.method
        # }
        # print('\n')
        # pprint(json)
        permission_classes = [IsAuthenticated]
        if self.kwargs.get('pk') != 'me':
            permission_classes.append(IsAdmin)
        return [permission() for permission in permission_classes]


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


@permission_classes([AllowAny, ])
@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data, )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.validated_data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny, ])
@api_view(['POST'])
def token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    json_err = {}
    if username is None:
        json_err['username'] = 'Имя пользователя не указано!'
    if confirmation_code is None:
        json_err[
            'confirmation_code'] = 'Код подтверждения не указан не указан!'
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
