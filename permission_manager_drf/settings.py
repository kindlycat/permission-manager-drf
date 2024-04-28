from django.conf import settings
from django.utils.module_loading import import_string


PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER = getattr(
    settings,
    'PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER',
    'permission_manager_drf.utils.get_permission_manager_class_for_model',
)

permission_manager_getter = import_string(
    PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER,
)
