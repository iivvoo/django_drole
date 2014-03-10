from drole.models import Role

class TestRole(object):
    """
        Role is a simple wrapper around a string identifier
        with some singleton-ish behaviour
    """
    def test_create(self):
        """ Role are implicitly created """
        assert Role("foo") is not None

    def test_uniqueness_id(self):
        """ Different instances with same identifier are identical """
        assert Role("foo") is Role("foo")

    def test_uniqueness_attrs(self):
        """ Different instances with same identifier are identical, even
            if other attributes differ """
        assert Role("foo", "bar", "bla") is \
               Role("foo", "this", "that")

    def test_uniqueness_differ(self):
        """ 
            Role with different identifier are not equal
        """
        assert Role("foo") != Role("bar")

