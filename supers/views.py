from unicodedata import name
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from super_types.models import SuperType
from .serializers import SuperSerializer
from .models import Super

@api_view(['GET', 'POST'])
def supers_list(request):
    if request.method == 'GET':
        supers_type_param = request.query_params.get('type')
        supers = Super.objects.all()
        custom_response_dictionary = {}
        if supers_type_param:
            supers = supers.filter(super_type__type=supers_type_param)
            serializer = SuperSerializer(supers, many=True)
            return Response(serializer.data)
        heroes_list = []
        villains_list = []
        custom_response_dictionary = {
            "Heroes": heroes_list,
            "Villains": villains_list
        }
        for super in supers:             #I need a serializer in here somewhere
            if SuperType.type == "Hero":
                heroes_list.append(super)
            elif SuperType.type == "Villain":
                villains_list.append(super)
        return Response(custom_response_dictionary)
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def supers_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(super);
        return Response(serializer.data)
    elif request.method == 'PUT':    
        serializer = SuperSerializer(super, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)