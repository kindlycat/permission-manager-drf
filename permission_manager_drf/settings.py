from django.conf import settings
from django.utils.module_loading import import_string


# Path to the function for getting a permission manager class for a model
PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER = getattr(
    settings,
    'PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER',
    'permission_manager_drf.utils.get_permission_manager_class_for_model',
)

# Import the permission manager getter function dynamically
permission_manager_getter = import_string(
    PERMISSION_MANAGER_DRF_FOR_MODEL_GETTER,
)
