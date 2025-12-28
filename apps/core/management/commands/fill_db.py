from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal

from apps.core.models import Category, Product, Cart, CartItem, Order, OrderItem, Payment

User = get_user_model()


class Command(BaseCommand):
    """Management command to fill database with test data."""
    help = 'Fill database with test data'

    def handle(self, *args, **options) -> None:
        """Execute the command."""
        self.stdout.write(self.style.SUCCESS('Starting to fill database...'))

        # Create users
        self.stdout.write('Creating users...')
        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Admin user already exists'))

        user1, created = User.objects.get_or_create(
            email='user1@example.com',
            defaults={'username': 'user1'}
        )
        if created:
            user1.set_password('user123')
            user1.save()
            self.stdout.write(self.style.SUCCESS('✓ User1 created'))
        else:
            self.stdout.write(self.style.WARNING('⚠ User1 already exists'))

        user2, created = User.objects.get_or_create(
            email='user2@example.com',
            defaults={'username': 'user2'}
        )
        if created:
            user2.set_password('user123')
            user2.save()
            self.stdout.write(self.style.SUCCESS('✓ User2 created'))
        else:
            self.stdout.write(self.style.WARNING('⚠ User2 already exists'))

        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            'Electronics',
            'Books',
            'Clothing',
            'Home & Garden',
            'Sports',
            'Toys',
        ]
        categories = []
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories.append(cat)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Category "{cat_name}" created'))

        # Create products
        self.stdout.write('Creating products...')
        products_data = [
            # Electronics
            ('iPhone 14 Pro', 'Latest Apple smartphone', Decimal('999.99'), 50, categories[0]),
            ('MacBook Pro', 'Professional laptop', Decimal('2499.99'), 30, categories[0]),
            ('AirPods Pro', 'Wireless earbuds', Decimal('249.99'), 100, categories[0]),
            ('iPad Air', 'Tablet computer', Decimal('599.99'), 40, categories[0]),
            
            # Books
            ('Python Programming', 'Learn Python from scratch', Decimal('39.99'), 200, categories[1]),
            ('Django for Beginners', 'Web development with Django', Decimal('44.99'), 150, categories[1]),
            ('Clean Code', 'A Handbook of Agile Software Craftsmanship', Decimal('34.99'), 180, categories[1]),
            
            # Clothing
            ('T-Shirt', 'Cotton t-shirt', Decimal('19.99'), 500, categories[2]),
            ('Jeans', 'Blue denim jeans', Decimal('59.99'), 300, categories[2]),
            ('Sneakers', 'Running shoes', Decimal('89.99'), 200, categories[2]),
            
            # Home & Garden
            ('Coffee Maker', 'Automatic coffee machine', Decimal('129.99'), 80, categories[3]),
            ('Blender', 'High-speed blender', Decimal('79.99'), 100, categories[3]),
            
            # Sports
            ('Yoga Mat', 'Non-slip yoga mat', Decimal('29.99'), 150, categories[4]),
            ('Dumbbells Set', '20kg dumbbells', Decimal('149.99'), 60, categories[4]),
            
            # Toys
            ('LEGO Set', 'Building blocks set', Decimal('49.99'), 120, categories[5]),
            ('Board Game', 'Family board game', Decimal('34.99'), 90, categories[5]),
        ]
        
        products = []
        for title, desc, price, stock, category in products_data:
            product, created = Product.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc,
                    'price': price,
                    'stock': stock,
                    'category': category
                }
            )
            products.append(product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Product "{title}" created'))

        # Create carts with items
        self.stdout.write('Creating carts...')
        cart1, created = Cart.objects.get_or_create(user=user1)
        if created or not cart1.items.exists():
            CartItem.objects.get_or_create(
                cart=cart1,
                product=products[0],
                defaults={'quantity': 1}
            )
            CartItem.objects.get_or_create(
                cart=cart1,
                product=products[2],
                defaults={'quantity': 2}
            )
            self.stdout.write(self.style.SUCCESS('✓ Cart for user1 created with items'))

        cart2, created = Cart.objects.get_or_create(user=user2)
        if created or not cart2.items.exists():
            CartItem.objects.get_or_create(
                cart=cart2,
                product=products[1],
                defaults={'quantity': 1}
            )
            self.stdout.write(self.style.SUCCESS('✓ Cart for user2 created with items'))

        # Create orders
        self.stdout.write('Creating orders...')
        order1, created = Order.objects.get_or_create(
            user=user1,
            total_price=Decimal('1499.97'),
            defaults={'total_price': Decimal('1499.97')}
        )
        if created:
            OrderItem.objects.create(
                order=order1,
                product=products[0],
                quantity=1,
                price=products[0].price
            )
            OrderItem.objects.create(
                order=order1,
                product=products[2],
                quantity=2,
                price=products[2].price
            )
            self.stdout.write(self.style.SUCCESS('✓ Order for user1 created'))

        order2, created = Order.objects.get_or_create(
            user=user2,
            total_price=Decimal('2499.99'),
            defaults={'total_price': Decimal('2499.99')}
        )
        if created:
            OrderItem.objects.create(
                order=order2,
                product=products[1],
                quantity=1,
                price=products[1].price
            )
            self.stdout.write(self.style.SUCCESS('✓ Order for user2 created'))

        # Create payments
        self.stdout.write('Creating payments...')
        payment1, created = Payment.objects.get_or_create(
            order=order1,
            defaults={
                'amount': order1.total_price,
                'method': 'card',
                'status': 'completed'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Payment for order1 created'))

        payment2, created = Payment.objects.get_or_create(
            order=order2,
            defaults={
                'amount': order2.total_price,
                'method': 'paypal',
                'status': 'pending'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Payment for order2 created'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database filled successfully!'))
        self.stdout.write(self.style.SUCCESS('\nTest accounts:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin@example.com / admin123'))
        self.stdout.write(self.style.SUCCESS('  User1: user1@example.com / user123'))
        self.stdout.write(self.style.SUCCESS('  User2: user2@example.com / user123'))
