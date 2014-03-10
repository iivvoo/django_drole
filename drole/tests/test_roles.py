from drole.models import Role, _Role

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

    def test_equality(self):
        """ ordinary comparison. Will succeed since it will be the same
            objects """
        assert Role("foo") == Role("foo")

    def test_forced_equality(self):
        """ if somehow different roles get created with the same identifier,
            they should still be equal """
        assert _Role("foo") == _Role("foo")

    def test_forced_inequality(self):
        """ if somehow different roles get created with different identifiers,
            they should not be equal """
        assert _Role("foo") != _Role("bar")

    def test_forced_identity(self):
        """ if somehow different roles get created with the same identifier,
            they are equal but not identical """
        assert _Role("foo") is not _Role("foo")

    def test_in(self):
        """ a common case """
        assert Role("foo") in [Role("bar"), Role("foo"), Role("hello")]
