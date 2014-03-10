from drole.models import Permission, _Permission

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

    def test_equality(self):
        """ ordinary comparison. Will succeed since it will be the same
            objects """
        assert Permission("foo") == Permission("foo")

    def test_forced_equality(self):
        """ if somehow different permissions get created with the same
            identifier, they should still be equal """
        assert _Permission("foo") == _Permission("foo")

    def test_forced_inequality(self):
        """ if somehow different permissions get created with different
            identifiers, they shouldn't be equal """
        assert _Permission("foo") != _Permission("bar")

    def test_forced_identity(self):
        """ if somehow different permissions get created with the same
            identifier, they are equal but not identical """
        assert _Permission("foo") is not _Permission("foo")

    def test_in(self):
        """ a common case """
        assert Permission("foo") in [Permission("bar"),
                                     Permission("foo"), Permission("hello")]
