===============
PermissionField
===============

PermissionField allow you to retrieve permissions for instance.


Usage
-----

Define permission field in serializer:

..  code-block:: Python

    from rest_framework.serializers import ModelSerializer

    class NewsSerializer(ModelSerializer):
        permissions = PermissionField(actions=('update', 'publish'))

        class Meta:
            model = News
            fields = ('permissions',)

Example output:

..  code-block:: JSON

    {
      "permissions": {
        "update": {
          "allow": true,
          "messages": null
        },
        "publish": {
          "allow": false,
          "messages": [
            "Already published"
          ]
        }
      }
    }


Children
--------

If you need to serialize children's permissions,  you can use the ``children``
argument. For example, you may need to know that you can create some related
instances.

.. code-block:: Python

    from permission_manager_drf import PermissionFieldChild

    class NewsSerializer(ModelSerializer):
        permissions = PermissionField(
            actions=('update', 'publish'),
            children=[
                PermissionFieldChild(
                    name='image',
                    manager=ImagePermissionManager,
                    actions=['create'],
                )
            ]
        )

.. code-block:: JSON

    {
      "update": {
        "allow": false,
        "messages": null
      },
      "publish": {
        "allow": false,
        "messages": null
      },
      "image": {
        "create": {
          "allow": false,
          "messages": [
            "Parent is not editable"
          ]
        }
      }
    }
