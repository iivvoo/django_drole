from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class _Permission(object):
    _perms = {}

    def __init__(self, id, name="", description=""):
        self.id = id
        self.name = name or id
        self.description = description

    @classmethod
    def create(cls, id, name, description):
        p = cls._perms.get(id)
        if not p:
            p = _Permission(id, name, description)
            cls._perms[id] = p
        return p
        
def Permission(id, name="", description=""):
    return _Permission.create(id, name, description)

class _Role(object):
    _roles = {}

    def __init__(self, id, name="", description=""):
        self.id = id
        self.name = name or id
        self.description = description

    @classmethod
    def create(cls, id, name, description):
        p = cls._roles.get(id)
        if not p:
            p = _Role(id, name, description)
            cls._roles[id] = p
        return p

    def has_access(self, obj, permission):
        model_ct = ContentType.objects.get_for_model(obj)
        return RolePermission.objects.filter(content_type=model_ct,
                                             object_id=obj.id,
                                             role=self.id,
                                             permission=permission.id).exists()
        
def Role(id, name="", description=""):
    return _Role.create(id, name, description)


class RolePermission(models.Model):
    permission = models.CharField(max_length=255, blank=False, db_index=True)
    role = models.CharField(max_length=255, blank=False, db_index=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    @classmethod
    def assign(cls, obj, role, permission):
        r = cls(content_object=obj,
                permission=permission.id,
                role=role.id)
        r.save()
        return r

    def __unicode__(self):
        return u"<Permission {0} for role {1}>".format(self.permission,
                                                      self.role)
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
