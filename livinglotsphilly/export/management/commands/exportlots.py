import sys
import traceback

from django.core.management.base import BaseCommand

from ...resources import LotResource


class Command(BaseCommand):
    help = 'Export lots'

    def handle(self, *args, **options):
        self.stderr.write('exportlots: Starting')

        lot_resource = LotResource()
        try:
            print lot_resource.export().csv
        except Exception:
            traceback.print_exc(file=sys.stderr)
        finally:
            self.stderr.write('exportlots: Finished')
