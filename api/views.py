from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item

@api_view(['GET'])
def get_items(request):
    items = Item.objects.all().values('id', 'name', 'description', 'price')
    return Response(items)
