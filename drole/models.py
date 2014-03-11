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

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, id, name="", description=""):
        p = cls._registry.get(id)
        if not p:
            p = cls(id, name, description)
            cls._registry[id] = p
        return p

    @classmethod
    def all(cls):
        return cls._registry.values()

class Permission(Base):
    _registry = {}

    def __unicode__(self):
        return u"<Permission {0} ({1})>".format(self.id, self.name)

class Role(Base):
    _registry = {}

    def has_access(self, obj, permission):
        model_ct = ContentType.objects.get_for_model(obj)
        return RolePermission.objects.filter(content_type=model_ct,
                                             object_id=obj.id,
                                             role=self,
                                             permission=permission).exists()

    def __unicode__(self):
        return u"<Role {0} ({1})>".format(self.id, self.name)

class RoleField(models.CharField):

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None:
            return None

        if isinstance(value, (str, unicode)):
            return Role(value)

        return value

    def get_prep_value(self, value):
        if isinstance(value, Role):
            return value.id
        return value

    def xget_db_prep_save(self, value, connection):
        return super(RoleField, self).get_db_prep_save(value.id, connection)

class PermissionField(models.CharField):

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None:
            return None

        if isinstance(value, (str, unicode)):
            return Permission(value)

        return value

    def get_prep_value(self, value):
        if isinstance(value, Permission):
            return value.id
        return value

    def xget_db_prep_save(self, value, connection):
        return super(PermissionField, self).get_db_prep_save(value.id, connection)

class RolePermission(models.Model):
    permission = PermissionField(max_length=255, blank=False, db_index=True)
    role = RoleField(max_length=255, blank=False, db_index=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    @classmethod
    def assign(cls, obj, role, permission):
        model_ct = ContentType.objects.get_for_model(obj)
        r, _ = cls.objects.get_or_create(content_type=model_ct,
                                         object_id=obj.id,
                                         permission=permission,
                                         role=role)
        return r

    @classmethod
    def assignments(cls, obj):  # XXX make this a manager?
        """ return all assignments for a specific object """
        model_ct = ContentType.objects.get_for_model(obj)
        return cls.objects.filter(content_type=model_ct, object_id=obj.id).all()


    def __unicode__(self):
        return u"<Permission {0} for role {1}>".format(self.permission,
                                                      self.role)
