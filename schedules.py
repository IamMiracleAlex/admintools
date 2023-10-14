import sys
from django.core.management import call_command

class Runner:
    def __getattr__(self, attr):
        return lambda: call_command(attr)

sys.modules[__name__] = Runner()