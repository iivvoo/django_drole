from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Base(object):
    """
        A singletonish (based on id) type with additional
        equality functionality
    """
    _registry = None  ## should be overridden, don't share through base

    def __init__(self, id, name="", description=""):
        self.id = id
        self.name = name or id
        self.description = description

    def __eq__(self, other):
        return other and self.__class__ is other.__class__ and \
               self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def create(cls, id, name="", description=""):
        p = cls._registry.get(id)
        if not p:
            p = cls(id, name, description)
            cls._registry[id] = p
        return p

class _Permission(Base):
    _registry = {}

        
def Permission(id, name="", description=""):
    return _Permission.create(id, name, description)

class _Role(Base):
    _registry = {}
        

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

    @classmethod
    def assignments(cls, obj):  # XXX make this a manager?
        """ return all assignments for a specific object """
        model_ct = ContentType.objects.get_for_model(obj)
        return cls.objects.filter(content_type=model_ct, object_id=obj.id).all()


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
