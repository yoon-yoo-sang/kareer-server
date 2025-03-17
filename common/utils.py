from rest_framework.exceptions import NotFound

from common.errors import OBJECT_DOES_NOT_EXIST


def get_object_or_404_response(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise NotFound(f"{OBJECT_DOES_NOT_EXIST}: cls name: {model.__name__}, kwargs: {kwargs}")
