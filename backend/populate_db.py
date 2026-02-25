import os
import django
import shutil
from django.core.files import File
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce.settings')
django.setup()

from products.models import Category, Product

def populate():
    # Define data
    data = [
        {
            "category": "Computer accesories",
            "products": [
                {
                    "name": "laptop bag",
                    "price": 55.00,
                    "stock": 50,
                    "image_src": "bag1.webp"
                }
            ]
        },
        {
            "category": "School Item",
            "products": [
                {
                    "name": "School bag",
                    "price": 80.00,
                    "stock": 45,
                    "image_src": "school_bag.jpg"
                }
            ]
        }
    ]

    print("Starting population script...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_products_dir = os.path.join(base_dir, 'media', 'products')
    
    # Ensure media directory exists
    os.makedirs(media_products_dir, exist_ok=True)

    for cat_data in data:
        category, created = Category.objects.get_or_create(name=cat_data["category"])
        if created:
            print(f"Created Category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")

        for prod_data in cat_data["products"]:
            # Check if product exists
            if Product.objects.filter(name=prod_data["name"]).exists():
                print(f"Product already exists: {prod_data['name']}")
                continue

            product = Product(
                name=prod_data["name"],
                description=f"Description for {prod_data['name']}",
                price=Decimal(prod_data["price"]),
                stock=prod_data["stock"],
                category=category
            )

            # Handle Image
            image_src_path = os.path.join(media_products_dir, prod_data["image_src"])
            if os.path.exists(image_src_path):
                with open(image_src_path, 'rb') as f:
                    product.image.save(prod_data["image_src"], File(f), save=False)
                print(f"Attached image: {prod_data['image_src']}")
            else:
                print(f"Warning: Image file not found: {image_src_path}")

            product.save()
            print(f"Created Product: {product.name}")

    print("Population complete.")

if __name__ == '__main__':
    populate()
