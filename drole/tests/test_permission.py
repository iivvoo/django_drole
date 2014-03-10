from drole.models import Permission

class TestPermission(object):
    """
        Permission is a simple wrapper around a string identifier
        with some singleton-ish behaviour
    """
    def test_create(self):
        """ Permissions are implicitly created """
        assert Permission("foo") is not None

    def test_uniqueness_id(self):
        """ Different instances with same identifier are identical """
        assert Permission("foo") is Permission("foo")

    def test_uniqueness_attrs(self):
        """ Different instances with same identifier are identical, even
            if other attributes differ """
        assert Permission("foo", "bar", "bla") is \
               Permission("foo", "this", "that")

    def test_uniqueness_differ(self):
        """ 
            Permissions with different identifier are not equal
        """
        assert Permission("foo") != Permission("bar")

