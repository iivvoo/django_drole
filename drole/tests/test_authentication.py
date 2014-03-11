import pytest

from twotest.fixtures import client, django_client
from django.contrib.auth.models import User

from drole.models import Role, Permission, RolePermission
from drole.test_models import TestModel

@pytest.fixture()
def role():
    return Role("test.arole", "A role")

@pytest.fixture()
def anonymous_role():
    return Role("test.anonymous", "Anonymous")

@pytest.fixture()
def permission():
    return Permission("test.permission", "Test Permission")

@pytest.fixture()
def view_permission():
    return Permission("test.view", "View Permission")

class TestAuthentication(object):
    def test_unicode(self, client, role, permission):
        obj = TestModel.objects.get_or_create(name="bla")[0]
        assert isinstance(RolePermission.assign(obj,
                                                role,
                                                permission).__unicode__(),
                          unicode)

    def test_empty(self, client, role, permission):
        """ no assignments at all """
        obj = TestModel.objects.get_or_create(name="bla")[0]

        assert not role.has_access(obj, permission)

    def test_mismatch(self, client, anonymous_role, role, view_permission):
        """ permission assigned to different role """
        obj = TestModel.objects.get_or_create(name="bla")[0]

        RolePermission.assign(obj, role, view_permission)

        assert not anonymous_role.has_access(obj, view_permission)

    def test_cross_mismatch(self, client, anonymous_role, role,
                            view_permission, permission):
        """ cross assignment of two perms and two roles """
        obj1 = TestModel.objects.get_or_create(name="1")[0]
        obj2 = TestModel.objects.get_or_create(name="2")[0]

        RolePermission.assign(obj1, role, permission)
        RolePermission.assign(obj2, anonymous_role, view_permission)

        assert not anonymous_role.has_access(obj1, view_permission)
        assert not anonymous_role.has_access(obj2, permission)
        assert not role.has_access(obj1, view_permission)
        assert not role.has_access(obj2, permission)

    def test_cross_match(self, client, anonymous_role, role,
                         view_permission, permission):
        """ cross assignment of two perms and two roles """
        obj1 = TestModel.objects.get_or_create(name="1")[0]
        obj2 = TestModel.objects.get_or_create(name="2")[0]

        RolePermission.assign(obj1, role, permission)
        RolePermission.assign(obj2, anonymous_role, view_permission)

        assert anonymous_role.has_access(obj2, view_permission)
        assert role.has_access(obj1, permission)

    def test_has_access(self, client, anonymous_role, view_permission):
        """ simple success case: role/perm assignment """
        obj = TestModel.objects.get_or_create(name="bla")[0]

        RolePermission.assign(obj, anonymous_role, view_permission)
        assert anonymous_role.has_access(obj, view_permission)

    def test_assignments_empty(self, client):
        """ by default no assignments """
        obj = TestModel.objects.get_or_create(name="bla")[0]

        assert not RolePermission.assignments(obj).exists()

    def test_assignments(self, client, anonymous_role, view_permission):
        """ simple success case: role/perm assignment """
        obj = TestModel.objects.get_or_create(name="bla")[0]

        RolePermission.assign(obj, anonymous_role, view_permission)
        assert RolePermission.assignments(obj).exists()

    def test_assignments_dup(self, client, anonymous_role, view_permission):
        """ a duplicate assignment should not create duplicate records """
        obj = TestModel.objects.get_or_create(name="bla")[0]

        RolePermission.assign(obj, anonymous_role, view_permission)
        RolePermission.assign(obj, anonymous_role, view_permission)
        assert RolePermission.assignments(obj).count() == 1
