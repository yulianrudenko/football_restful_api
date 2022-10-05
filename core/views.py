from rest_framework.views import APIView


class APIView(APIView):
    '''
    Base DRF APIView extended with attribute(that should be overriden for each one view) & method used by Swagger
    Its task is just to allow handy post requests directly from swagger panel in browser
    '''
    input_serializer_class = None  # MUST BE set for each view

    def get_serializer(self, *args, **kwargs):
        if self.input_serializer_class:
            return self.input_serializer_class(*args, **kwargs)
        return None
