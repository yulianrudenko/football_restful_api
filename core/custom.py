import json

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import SerializerMetaclass
from rest_framework.renderers import JSONRenderer

from django.db.models import QuerySet


class JSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})
        return response 

class APIView(APIView):
    '''
    Base DRF APIView extended with attribute(that should be overriden for each one view) & method used by Swagger
    and custom JSON renderer
    Its task is just to allow handy post requests directly from swagger panel in browser
    '''
    input_serializer_class = None  # MUST BE set for each view
    renderer_classes = [JSONRenderer]

    def get_serializer(self, *args, **kwargs) -> SerializerMetaclass:
        if self.input_serializer_class:
            return self.input_serializer_class(*args, **kwargs)
        return None


def paginate_by_page_number(qs, request) -> list:
    paginator = PageNumberPagination() 
    result_page = paginator.paginate_queryset(queryset=qs, request=request)
    return result_page