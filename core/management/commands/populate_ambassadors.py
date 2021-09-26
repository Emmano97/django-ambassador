from django.core.management import BaseCommand
from faker import Faker
from faker.providers import profile

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker('en_US')
        fake.add_provider(profile)

        for i in range(30):
            user = User.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password='',
                is_ambassador=True
            )

            user.set_password("password")
            user.save()