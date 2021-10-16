from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from . import views


urlpatterns = [
    path('', csrf_exempt(never_cache(views.get_tasks)), name='get_tasks'),
    path('<int:task_id>', csrf_exempt(never_cache(views.specific_task)), name='specific_task'),
    path('new-task', csrf_exempt(never_cache(views.create_task)), name='create_task'),
]
