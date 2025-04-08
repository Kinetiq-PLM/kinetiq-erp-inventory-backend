from django.urls import path
from .views import CyclicCountList

urlpatterns = [
    path('cyclic_counts/', CyclicCountList.as_view(), name='cyclic_count_list'),
]
