from django.core.management.base import BaseCommand
from faker import Faker
from Product_Lists.models import Product, UpComingProducts, Category
from random import choice

class Command(BaseCommand):
    help = 'Seed the Product and UpComingProducts models in the Product_Lists app with fake data'

    CATEGORIES = [
        'Sports Accessories',
        'Fitness Equipment',
        'Training Gear',
        'Running Shoes',
        'Sports Equipment',
        "Men's Jerseys",
        "Women's Jerseys"
    ]

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, help='The number of fake products to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        number = kwargs['number'] if 'number' in kwargs else 10

        # Ensure the categories exist in the database
        for category_name in self.CATEGORIES:
            Category.objects.get_or_create(name=category_name)

        # Create fake products
        for _ in range(number):
            category = choice(Category.objects.all())
            product = Product.objects.create(
                name=fake.name()[:10],
                description=fake.text(max_nb_chars=100),
                price=fake.random_number(digits=2),
                image='images/product_icon.png',
                digital=fake.boolean()
            )
            product.categories.add(category)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {number} fake products'))

        # Create fake upcoming products
        for _ in range(number):
            UpComingProducts.objects.create(
                name=fake.name()[:10],
                image='product_images/upcoming/default.jpg'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {number} fake upcoming products'))
