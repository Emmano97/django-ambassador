from random import randrange

from django.core.management import BaseCommand
from faker import Faker
from faker.providers import profile

from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker('en_US')
        fake.add_provider(profile)

        for i in range(30):
            product = Product.objects.create(
                title=fake.name(),
                description=fake.text(100),
                image=fake.image_url(),
                price=randrange(10, 1000)
            )
            product.save()