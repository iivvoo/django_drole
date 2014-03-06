from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Permission(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

class Role(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def has_access(self, obj, permission):
        model_ct = ContentType.objects.get_for_model(obj)
        return self.rolepermissions.filter(content_type=model_ct,
                                           object_id=obj.id,
                                           permission=permission).exists()

class RolePermission(models.Model):
    permission = models.ForeignKey(Permission, related_name="permissionroles")
    role = models.ForeignKey(Role, related_name="rolepermissions")

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    @classmethod
    def assign(cls, obj, role, permission):
        r = cls(content_object=obj,
                permission=permission,
                role=role)
        r.save()
        return r
"""
def do_generic_stuff(func, obj):
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(obj.__class__)
    object_id = getattr(obj, obj.__class__._meta.pk.column)
    return func(content_type=content_type, object_id=object_id)

from django.contrib.contenttypes.models import ContentType
type = ContentType.objects.get_for_model(object)
vote, created = Vote.objects.get_or_create(user_voted=user_voted, content_type=type, object_id=object.id)
"""
