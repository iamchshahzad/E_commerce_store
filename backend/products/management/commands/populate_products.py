from django.core.management.base import BaseCommand
from products.models import Product, Category
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Creating categories...')
        electronics = Category.objects.create(name='Electronics')
        clothing = Category.objects.create(name='Clothing')
        home = Category.objects.create(name='Home & Garden')
        books = Category.objects.create(name='Books')

        self.stdout.write('Creating products...')
        
        products = [
            {
                'name': 'Smartphone X Pro',
                'description': 'Latest smartphone with high-resolution camera and long battery life. Features a stunning 6.5-inch OLED display.',
                'price': Decimal('999.99'),
                'stock': 50,
                'category': electronics
            },
            {
                'name': 'Wireless Noise-Canceling Headphones',
                'description': 'Immersive sound quality with active noise cancellation. 30 hours of battery life and comfortable ear cushions.',
                'price': Decimal('299.50'),
                'stock': 100,
                'category': electronics
            },
            {
                'name': '4K Ultra HD Smart TV',
                'description': '55-inch crystal clear display with built-in smart apps. HDR support and voice control remote.',
                'price': Decimal('650.00'),
                'stock': 20,
                'category': electronics
            },
            {
                'name': 'Classic Denim Jacket',
                'description': 'Timeless design, durable denim fabric. Perfect for casual outings and layering.',
                'price': Decimal('75.00'),
                'stock': 200,
                'category': clothing
            },
            {
                'name': 'Cotton Crew Neck T-Shirt',
                'description': 'Soft and breathable 100% cotton t-shirt. Available in multiple colors.',
                'price': Decimal('25.00'),
                'stock': 500,
                'category': clothing
            },
            {
                'name': 'Modern Coffee Table',
                'description': 'Minimalist design with a glass top and wooden legs. Adds elegance to any living room.',
                'price': Decimal('150.00'),
                'stock': 15,
                'category': home
            },
            {
                'name': 'Ergonomic Office Chair',
                'description': 'Adjustable support for back and arms. Designed for comfort during long working hours.',
                'price': Decimal('220.00'),
                'stock': 30,
                'category': home
            },
            {
                'name': 'The Great Gatsby',
                'description': 'A classic novel by F. Scott Fitzgerald. A story of decadence and excess.',
                'price': Decimal('12.99'),
                'stock': 100,
                'category': books
            },
             {
                'name': 'Python Crash Course',
                'description': 'A hands-on, project-based introduction to programming. Learn to write code and build applications.',
                'price': Decimal('35.00'),
                'stock': 80,
                'category': books
            },
             {
                'name': 'Running Shoes',
                'description': 'Lightweight and durable running shoes with superior cushioning/grip.',
                'price': Decimal('120.00'),
                'stock': 60,
                'category': clothing
            }

        ]

        for p_data in products:
            Product.objects.create(**p_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {len(products)} products'))
