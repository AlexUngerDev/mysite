from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from .models import Task
from tasks.serializers import TaskSerializer

# Create your views here.


@api_view(['GET'])
def get_tasks(request):
    output = [
        {
            'name': task.name,
            'completed': task.completed,
            'task_description': task.task_description,
        } for task in Task.objects.all()
    ]
    return JsonResponse(output, safe=False)


def specific_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except ObjectDoesNotExist as err:
        print(err)
        return HttpResponseNotFound()
    except Exception as err:
        print(err)
        return HttpResponse(status=500)

    if request.method == 'GET':
        output = {
            'name': task.name,
            'completed': task.completed,
            'task_description': task.task_description,
        }
        return JsonResponse(output, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Task was updated successfully"})
        return HttpResponse()

    elif request.method == 'DELETE':
        task.delete()
        # task.save()
        return JsonResponse({'message': 'The task was deleted successfully'}, status=204)


@api_view(['POST'])
def create_task(request):
    data = JSONParser().parse(request)
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)
