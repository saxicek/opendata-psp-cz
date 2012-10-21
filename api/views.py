from djangorestframework.mixins import ReadModelMixin, ListModelMixin
from djangorestframework.views import ModelView

class InstanceModelReadOnlyView(ReadModelMixin, ModelView):
    """
    A view which provides default operations for read against a model instance.
    """
    _suffix = 'Instance'

class ListModelView(ListModelMixin, ModelView):
    """
    A view which provides default operations for list against a model in the database.
    """
    _suffix = 'List'
