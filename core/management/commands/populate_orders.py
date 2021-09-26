from random import randrange, randint
from django.core.management import BaseCommand
from faker import Faker
from faker.providers import profile
from core.models import Order, User, OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker('en_US')
        fake.add_provider(profile)
        users_count = User.objects.all().count()

        for _ in range(3):
            order = Order.objects.create(
                user_id=randint(1, users_count),
                code='code',
                ambassador_email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                complete=True
            )

            for _ in range(randrange(1, 5)):
                price = randrange(10, 100)
                quantity = randrange(1, 5)
                OrderItem.objects.create(
                    order_id=order.id,
                    product_title=fake.name(),
                    price=price,
                    quantity=quantity,
                    admin_revenue=.9 * price * quantity,
                    ambassador_revenue=.1 * price * quantity
                )