from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'load initial data'

    def handle(self, **options):
        call_command("loaddata", "condos.json", verbosity=0)
        call_command("loaddata", "accounts.json", verbosity=0)
