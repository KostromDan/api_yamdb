from django_filters import (FilterSet,
                            NumberFilter,
                            CharFilter,
                            ModelMultipleChoiceFilter)

from reviews.models import Genre, Title


class TitleFilter(FilterSet):
    genre = ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
#    category = ModelChoiceFilter(
#        field_name='category__slug',
#        to_field_name='slug',
#        queryset=Category.objects.all()
#    )
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']