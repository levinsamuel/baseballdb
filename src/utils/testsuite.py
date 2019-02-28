from django.test import TransactionTestCase
try:
    from django.test.runner import DiscoverRunner as BaseRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as BaseRunner


class NoDatabaseMixin:

    def build_suite(self, *args, **kwargs):
        """Build a suite like normal, but make a note of whether
        any tests require the DB"""
        # This has no parent. So why the call to super? because you'll see
        # below that this is going to be declared as the first parent of
        # another subclass that will use the base runner, which does have
        # this method, as its later parent
        suite = super(NoDatabaseMixin, self).build_suite(*args, **kwargs)
        self._needs_db = any([isinstance(test, TransactionTestCase)
                              for test in suite])
        return suite

    def setup_databases(self, *args, **kwargs):
        """Use the '_needs_db' property assigned in 'build_suite' to decide
        whether to create a new database or not"""

        if self._needs_db:
            return super().setup_databases(*args, **kwargs)
        if self.verbosity >= 1:
            print("No DB tests detected, skipping DB creation")
        return None

    def teardown_databases(self, *args, **kwargs):

        if self._needs_db:
            return super().teardown_databases(*args, **kwargs)
        return None


class FastTestRunner(NoDatabaseMixin, BaseRunner):
    """Empty class that just mixes the DB check class with the base runner"""
