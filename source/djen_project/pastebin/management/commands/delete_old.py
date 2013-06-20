import datetime

from django.core.management.base import NoArgsCommand

from pastebin.models import Paste

class Command(NoArgsCommand):
    help = """
            deletes pastes not updated in last 24 hrs

            Use this subcommand in a cron job
            to clear older pastes
           """

    def handle_noargs(self, **options):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(1)
        old_pastes = Paste.objects.filter(updated_on__lte=yesterday)
        old_pastes.delete()

