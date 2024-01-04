from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Tạo lễ cưới minh họa"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("[+]Done..."))
