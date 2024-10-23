from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import IdeaForm
from .models import Idea
from .serializers import IdeaSerializer


@api_view(['GET'])
def idea_list(request):
    ideas = Idea.objects.all()
    serializer = IdeaSerializer(ideas, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def idea_create(request):
    form = IdeaForm(request.data)
    if form.is_valid():
        idea = form.save(commit=False)
        idea.created_by = request.user
        idea.save()
        serializer = IdeaSerializer(idea)
        return JsonResponse(serializer.data, safe=False)
    else:
        errors = form.errors.as_text()
        return JsonResponse({'error': errors})