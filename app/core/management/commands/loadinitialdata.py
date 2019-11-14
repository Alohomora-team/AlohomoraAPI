"""
Utils commands for the projects
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
	"""
	Load all fixtures in a comfortable way
	"""
    help = 'load initial data'

    def handle(self, **options):
		"""
		Call for all fixtures her
		"""
        call_command("loaddata", "condos.json", verbosity=0)
        call_command("loaddata", "accounts.json", verbosity=0)
