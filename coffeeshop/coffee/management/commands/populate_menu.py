from django.core.management.base import BaseCommand
from coffee.models import MenuItem

class Command(BaseCommand):
    help = 'Populate the database with comprehensive menu items (8-9 items per category) with GBP pricing'

    def handle(self, *args, **options):
        # Clear existing menu items
        MenuItem.objects.all().delete()
        
        # Comprehensive menu items with GBP pricing (£6.99-£9.99 range)
        menu_items = [
            # Coffee (9 items)
            {
                'name': 'Premium House Blend',
                'description': 'Our signature blend of Ethiopian and Colombian beans, medium roast with notes of chocolate and caramel.',
                'price': 7.49,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=300&fit=crop&crop=center',
                'is_featured': True
            },
            {
                'name': 'Single Origin Guatemala',
                'description': 'Premium single-origin beans from the highlands of Guatemala. Full-bodied with hints of dark chocolate.',
                'price': 8.49,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'French Roast Supreme',
                'description': 'Dark roasted to perfection. Bold, smoky flavor with a rich, full body.',
                'price': 7.99,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Ethiopian Yirgacheffe',
                'description': 'Bright, floral coffee with wine-like acidity and citrus notes.',
                'price': 8.99,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Colombian Supremo',
                'description': 'Rich, well-balanced coffee with nutty undertones and medium body.',
                'price': 7.79,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1497515114629-f71d768fd07c?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Brazilian Santos',
                'description': 'Smooth, low-acid coffee with chocolate and nut flavors.',
                'price': 6.99,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Jamaican Blue Mountain',
                'description': 'Rare, mild coffee with exceptional smoothness and perfect balance.',
                'price': 9.99,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Costa Rican Tarrazú',
                'description': 'Full-bodied with bright acidity and wine-like finish.',
                'price': 8.29,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1521302200778-33500795e128?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Kona Coffee Blend',
                'description': 'Hawaiian Kona blend with smooth, rich flavor and low acidity.',
                'price': 8.89,
                'category': 'coffee',
                'image_url': 'https://images.unsplash.com/photo-1493857671505-72967e2e2760?w=400&h=300&fit=crop&crop=center'
            },
            
            # Espresso (9 items)
            {
                'name': 'Classic Espresso',
                'description': 'Double shot of our premium espresso blend. Rich, bold, and aromatic.',
                'price': 7.49,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=400&h=300&fit=crop&crop=center',
                'is_featured': True
            },
            {
                'name': 'Cappuccino Deluxe',
                'description': 'Perfect balance of espresso, steamed milk, and velvety foam. Dusted with cinnamon.',
                'price': 7.99,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Caramel Macchiato',
                'description': 'Espresso with vanilla syrup, steamed milk, and caramel drizzle.',
                'price': 8.49,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Vanilla Latte Supreme',
                'description': 'Smooth espresso with premium vanilla syrup and steamed milk.',
                'price': 7.79,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Mocha Delight',
                'description': 'Rich espresso with chocolate syrup, steamed milk, and whipped cream.',
                'price': 8.29,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Hazelnut Cappuccino',
                'description': 'Traditional cappuccino with aromatic hazelnut syrup.',
                'price': 7.99,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Americano Premium',
                'description': 'Bold espresso shots with hot water for a rich, smooth coffee.',
                'price': 6.99,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1525385133512-2f3bdd039054?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Cortado Special',
                'description': 'Equal parts espresso and warm steamed milk, perfectly balanced.',
                'price': 7.49,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Affogato Supreme',
                'description': 'Vanilla gelato "drowned" in a shot of hot espresso.',
                'price': 8.89,
                'category': 'espresso',
                'image_url': 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400&h=300&fit=crop&crop=center'
            },
            
            # Cold Drinks (8 items)
            {
                'name': 'Iced Cold Brew Supreme',
                'description': 'Smooth, refreshing cold brew coffee served over ice. Naturally sweet and low in acidity.',
                'price': 7.79,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop&crop=center',
                'is_featured': True
            },
            {
                'name': 'Iced Vanilla Latte',
                'description': 'Chilled espresso with premium vanilla syrup and cold milk over ice.',
                'price': 7.99,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Caramel Frappé',
                'description': 'Blended iced coffee with caramel syrup, whipped cream, and caramel drizzle.',
                'price': 8.49,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Iced Mocha Delight',
                'description': 'Cold espresso with chocolate syrup, milk, and whipped cream.',
                'price': 8.19,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Nitro Cold Brew',
                'description': 'Cold brew infused with nitrogen for a smooth, creamy texture.',
                'price': 8.29,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Iced Americano',
                'description': 'Refreshing iced version of our classic americano.',
                'price': 6.99,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1481833761820-0509d3217039?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Coconut Iced Latte',
                'description': 'Tropical blend with coconut milk and iced espresso.',
                'price': 8.49,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Mint Chocolate Frappé',
                'description': 'Refreshing mint and chocolate blended with ice and topped with whipped cream.',
                'price': 8.79,
                'category': 'cold_drinks',
                'image_url': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400&h=300&fit=crop&crop=center'
            },
        ]
        
        # Add remaining categories data
        pastries_data = [
            # Pastries (9 items)
            {
                'name': 'Chocolate Croissant',
                'description': 'Buttery, flaky croissant filled with rich Belgian dark chocolate.',
                'price': 7.49,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1549888834-3ec93d80a0e3?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Blueberry Muffin Supreme',
                'description': 'Fresh baked muffin bursting with juicy Maine blueberries.',
                'price': 6.99,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Cinnamon Roll Deluxe',
                'description': 'Warm, gooey cinnamon roll with cream cheese frosting and pecans.',
                'price': 7.79,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Almond Danish',
                'description': 'Flaky pastry filled with sweet almond paste and topped with sliced almonds.',
                'price': 7.99,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1534432182912-63863115e106?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Apple Turnover',
                'description': 'Crispy puff pastry filled with spiced apple filling.',
                'price': 7.29,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Lemon Scone',
                'description': 'Light, fluffy scone with fresh lemon zest and glaze.',
                'price': 7.19,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Raspberry Tart',
                'description': 'Delicate pastry shell filled with pastry cream and fresh raspberries.',
                'price': 8.49,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Chocolate Éclairs',
                'description': 'Classic French pastry filled with vanilla cream and chocolate glaze.',
                'price': 8.19,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&h=300&fit=crop&crop=center'
            },
            {
                'name': 'Strawberry Cream Puff',
                'description': 'Light choux pastry filled with strawberry cream.',
                'price': 7.89,
                'category': 'pastries',
                'image_url': 'https://images.unsplash.com/photo-1587241321921-91a834d6d191?w=400&h=300&fit=crop&crop=center'
            },
        ]
        
        sandwiches_data = [
            # Sandwiches (8 items)
            {
                'name': 'Gourmet Breakfast Sandwich',
                'description': 'Fresh scrambled eggs, aged cheddar, and crispy bacon on artisan brioche.',
                'price': 8.49,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Turkey Avocado Panini',
                'description': 'Roasted turkey, avocado, swiss cheese, and pesto on sourdough.',
                'price': 8.99,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Club Sandwich Supreme',
                'description': 'Triple-layered with turkey, ham, bacon, lettuce, tomato, and mayo.',
                'price': 9.29,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/4350489/pexels-photo-4350489.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Grilled Chicken Caesar Wrap',
                'description': 'Grilled chicken, romaine lettuce, parmesan, and caesar dressing in a tortilla.',
                'price': 8.19,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/4226764/pexels-photo-4226764.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Caprese Panini',
                'description': 'Fresh mozzarella, tomatoes, basil, and balsamic glaze on ciabatta.',
                'price': 7.79,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/4109998/pexels-photo-4109998.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'BBQ Pulled Pork Sandwich',
                'description': 'Slow-cooked pulled pork with BBQ sauce and coleslaw on a brioche bun.',
                'price': 8.79,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/4790107/pexels-photo-4790107.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Vegetarian Delight',
                'description': 'Grilled vegetables, hummus, and sprouts on whole grain bread.',
                'price': 7.49,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/4350628/pexels-photo-4350628.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Tuna Melt Deluxe',
                'description': 'Albacore tuna salad with melted cheddar on toasted sourdough.',
                'price': 7.99,
                'category': 'sandwiches',
                'image_url': 'https://images.pexels.com/photos/4226256/pexels-photo-4226256.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
        ]
        
        desserts_data = [
            # Desserts (9 items)
            {
                'name': 'Classic Tiramisu',
                'description': 'Traditional Italian dessert with coffee-soaked ladyfingers and mascarpone cream.',
                'price': 8.89,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/6880219/pexels-photo-6880219.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Belgian Chocolate Brownie',
                'description': 'Rich, fudgy brownie made with Belgian chocolate, topped with vanilla ice cream.',
                'price': 8.29,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/2067396/pexels-photo-2067396.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'New York Cheesecake',
                'description': 'Creamy, rich cheesecake with graham cracker crust and berry compote.',
                'price': 8.49,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4350489/pexels-photo-4350489.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with molten chocolate center, served with ice cream.',
                'price': 7.99,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4226764/pexels-photo-4226764.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Crème Brûlée',
                'description': 'Classic French custard topped with caramelized sugar.',
                'price': 7.79,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4109998/pexels-photo-4109998.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Apple Pie à la Mode',
                'description': 'Traditional apple pie with cinnamon and vanilla ice cream.',
                'price': 7.59,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4790107/pexels-photo-4790107.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Panna Cotta',
                'description': 'Silky Italian dessert with berry coulis and fresh mint.',
                'price': 7.19,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4350628/pexels-photo-4350628.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Banoffee Pie',
                'description': 'Banana and toffee pie with whipped cream and chocolate shavings.',
                'price': 8.09,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4226256/pexels-photo-4226256.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'name': 'Gelato Trio',
                'description': 'Three scoops of artisan gelato: vanilla, chocolate, and strawberry.',
                'price': 6.99,
                'category': 'desserts',
                'image_url': 'https://images.pexels.com/photos/4350489/pexels-photo-4350489.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
        ]
        
        # Combine all menu items (removed sandwiches)
        all_items = menu_items + pastries_data + desserts_data
        
        # Create menu items
        for item_data in all_items:
            MenuItem.objects.create(**item_data)
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(all_items)} menu items across all categories with GBP pricing')
        )