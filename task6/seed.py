from database.models import Product, Category
from database.db_connect import Session

session = Session()
#caterories
categories = [
    Category(name='Electronics', description='Devices and gadgets including phones, laptops, and cameras.'),
    Category(name='Books', description='Various genres of books including fiction, non-fiction, and academic.'),
    Category(name='Clothing', description='Apparel for men, women, and children including shirts, pants, and dresses.'),
    Category(name='Home & Kitchen', description='Products for home improvement and kitchen needs including furniture, appliances, and utensils.'),
    Category(name='Sports & Outdoors', description='Equipment and gear for various sports and outdoor activities.'),
    Category(name='Beauty & Personal Care', description='Cosmetics, skincare products, and personal care items.'),
    Category(name='Toys & Games', description='Toys for children and games for all ages.'),
    Category(name='Automotive', description='Car accessories, parts, and maintenance products.'),
    Category(name='Health & Wellness', description='Products for health, fitness, and personal wellness.'),
    Category(name='Office Supplies', description='Stationery, office furniture, and other supplies for work environments.')
]

#categories_id
categories_id = {
    'Electronics': 1,
    'Books': 2,
    'Clothing': 3,
    'Home & Kitchen': 4,
    'Sports & Outdoors': 5,
    'Beauty & Personal Care': 6,
    'Toys & Games': 7,
    'Automotive': 8,
    'Health & Wellness': 9,
    'Office Supplies': 10
}

# Define the products
products = [
    # Electronics
    Product(name='Smartphone X Pro', description='A high-end smartphone with a 6.5-inch display, 5G capability, and a triple-camera system.', price=999.99, stock=50, category_id=categories_id['Electronics']),
    Product(name='4K Ultra HD TV', description='A 55-inch 4K Ultra HD television with smart features and built-in streaming apps.', price=799.99, stock=30, category_id=categories_id['Electronics']),
    Product(name='Wireless Noise-Canceling Headphones', description='Over-ear headphones with active noise-canceling technology and up to 30 hours of battery life.', price=149.99, stock=100, category_id=categories_id['Electronics']),
    Product(name='Laptop UltraBook 14', description='A lightweight laptop with a 14-inch screen, Intel i7 processor, 16GB RAM, and 512GB SSD.', price=1299.99, stock=20, category_id=categories_id['Electronics']),
    Product(name='Digital Camera Z7', description='A 24-megapixel DSLR camera with advanced autofocus and a range of lenses for photography enthusiasts.', price=1499.99, stock=15, category_id=categories_id['Electronics']),
    
    # Books
    Product(name='The Great Gatsby', description='A classic novel by F. Scott Fitzgerald exploring themes of wealth and decadence in 1920s America.', price=12.99, stock=200, category_id=categories_id['Books']),
    Product(name='Educated by Tara Westover', description='A memoir about a woman who grows up in a strict and abusive household in rural Idaho and eventually earns a PhD from Cambridge University.', price=14.99, stock=150, category_id=categories_id['Books']),
    Product(name='Sapiens: A Brief History of Humankind', description='Yuval Noah Harari\'s exploration of the history of humanity from the Stone Age to the present.', price=18.99, stock=120, category_id=categories_id['Books']),
    Product(name='The Silent Patient', description='A psychological thriller about a woman who stops speaking after being accused of her husband\'s murder.', price=16.99, stock=180, category_id=categories_id['Books']),
    Product(name='Becoming by Michelle Obama', description='The former First Lady’s memoir about her life, experiences, and journey to the White House.', price=19.99, stock=140, category_id=categories_id['Books']),
    
    # Clothing
    Product(name='Men’s Casual T-Shirt', description='A comfortable cotton T-shirt available in various colors and sizes.', price=19.99, stock=300, category_id=categories_id['Clothing']),
    Product(name='Women’s Summer Dress', description='A light and breezy dress perfect for warm weather, with floral patterns and adjustable straps.', price=29.99, stock=100, category_id=categories_id['Clothing']),
    Product(name='Children’s Winter Coat', description='A warm, insulated coat for kids, featuring a detachable hood and water-resistant fabric.', price=49.99, stock=80, category_id=categories_id['Clothing']),
    Product(name='Jeans Classic Fit', description='Denim jeans with a classic fit, available in different sizes and washes.', price=39.99, stock=150, category_id=categories_id['Clothing']),
    Product(name='Sports Hoodie', description='A comfortable hoodie with moisture-wicking fabric, ideal for workouts and casual wear.', price=34.99, stock=90, category_id=categories_id['Clothing']),
    
    # Home & Kitchen
    Product(name='Stainless Steel Cookware Set', description='A 12-piece set of high-quality pots and pans, including various sizes and types.', price=159.99, stock=25, category_id=categories_id['Home & Kitchen']),
    Product(name='Smart Vacuum Cleaner', description='A robotic vacuum with automated cleaning modes and a scheduling feature.', price=249.99, stock=40, category_id=categories_id['Home & Kitchen']),
    Product(name='Electric Kettle', description='A quick-boil electric kettle with a 1.7-liter capacity and auto-shutoff feature.', price=29.99, stock=70, category_id=categories_id['Home & Kitchen']),
    Product(name='Memory Foam Mattress', description='A king-sized mattress with memory foam for comfort and support, including a breathable cover.', price=499.99, stock=15, category_id=categories_id['Home & Kitchen']),
    Product(name='Coffee Maker 12-Cup', description='A programmable coffee maker with a built-in timer and a keep-warm function.', price=59.99, stock=35, category_id=categories_id['Home & Kitchen']),
    
    # Sports & Outdoors
    Product(name='Camping Tent 4-Person', description='A spacious and easy-to-set-up tent for camping trips, with waterproof material and ventilation windows.', price=129.99, stock=25, category_id=categories_id['Sports & Outdoors']),
    Product(name='Yoga Mat with Carry Strap', description='A non-slip yoga mat with a carrying strap, perfect for home workouts and studio classes.', price=29.99, stock=60, category_id=categories_id['Sports & Outdoors']),
    Product(name='Bicycle 21-Speed', description='A mountain bike with 21 gears, front suspension, and a sturdy frame for off-road and on-road riding.', price=399.99, stock=15, category_id=categories_id['Sports & Outdoors']),
    Product(name='Fishing Rod and Reel Combo', description='A complete fishing set with a durable rod and smooth-reeling reel for freshwater fishing.', price=89.99, stock=30, category_id=categories_id['Sports & Outdoors']),
    Product(name='Hiking Boots Waterproof', description='Rugged and waterproof hiking boots designed for various terrains with good ankle support.', price=79.99, stock=50, category_id=categories_id['Sports & Outdoors']),
    
    # Beauty & Personal Care
    Product(name='Anti-Aging Face Serum', description='A serum with retinol and hyaluronic acid for reducing wrinkles and improving skin texture.', price=29.99, stock=75, category_id=categories_id['Beauty & Personal Care']),
    Product(name='Organic Lip Balm', description='A moisturizing lip balm made with natural ingredients to protect and hydrate lips.', price=6.99, stock=200, category_id=categories_id['Beauty & Personal Care']),
    Product(name='Men’s Beard Grooming Kit', description='A complete kit with beard oil, balm, and a comb for maintaining and styling facial hair.', price=24.99, stock=40, category_id=categories_id['Beauty & Personal Care']),
    Product(name='Vitamin C Face Cream', description='A face cream with Vitamin C for brightening skin and reducing dark spots.', price=34.99, stock=60, category_id=categories_id['Beauty & Personal Care']),
    Product(name='Hair Straightener', description='A professional hair straightener with adjustable heat settings and ceramic plates.', price=49.99, stock=50, category_id=categories_id['Beauty & Personal Care']),
    
    # Toys & Games
    Product(name='LEGO City Building Set', description='A construction-themed LEGO set with various building pieces and minifigures.', price=59.99, stock=50, category_id=categories_id['Toys & Games']),
    Product(name='Children’s Educational Tablet', description='A tablet designed for children with educational games, apps, and parental controls.', price=119.99, stock=40, category_id=categories_id['Toys & Games']),
    Product(name='Board Game: Settlers of Catan', description='A popular strategy board game where players build and trade to develop the island of Catan.', price=39.99, stock=30, category_id=categories_id['Toys & Games']),
    Product(name='Remote-Control Car', description='A fast and durable remote-control car for kids and hobbyists.', price=49.99, stock=25, category_id=categories_id['Toys & Games']),
    Product(name='Puzzle: 1000-Piece World Map', description='A challenging 1000-piece puzzle featuring a detailed world map.', price=14.99, stock=60, category_id=categories_id['Toys & Games']),
    
    # Automotive
    Product(name='Car Dash Cam 1080p', description='A dashboard camera with high-definition video recording and loop recording capabilities.', price=79.99, stock=35, category_id=categories_id['Automotive']),
    Product(name='Bluetooth Car Kit', description='A device for hands-free calling and streaming music from your phone to your car’s audio system.', price=29.99, stock=50, category_id=categories_id['Automotive']),
    Product(name='Car Vacuum Cleaner', description='A compact and powerful vacuum cleaner for keeping your car’s interior clean.', price=39.99, stock=30, category_id=categories_id['Automotive']),
    Product(name='Car Battery Charger', description='A portable charger with multiple settings for maintaining and charging car batteries.', price=59.99, stock=20, category_id=categories_id['Automotive']),
    Product(name='LED Headlight Bulbs', description='High-performance LED headlight bulbs with a bright and efficient beam for improved visibility.', price=34.99, stock=45, category_id=categories_id['Automotive']),
    
    # Health & Wellness
    Product(name='Fitness Tracker', description='A wearable device that tracks steps, heart rate, and calories burned.', price=49.99, stock=70, category_id=categories_id['Health & Wellness']),
    Product(name='Essential Oils Set', description='A collection of pure essential oils for aromatherapy and relaxation.', price=34.99, stock=45, category_id=categories_id['Health & Wellness']),
    Product(name='Vitamin D Supplements', description='A dietary supplement for supporting bone health and immune function.', price=14.99, stock=80, category_id=categories_id['Health & Wellness']),
    Product(name='Yoga Block and Strap Set', description='A set of yoga props to assist with poses and improve flexibility.', price=19.99, stock=60, category_id=categories_id['Health & Wellness']),
    Product(name='Personal Blender', description='A compact blender for making smoothies, shakes, and other blended drinks.', price=29.99, stock=40, category_id=categories_id['Health & Wellness']),
    
    # Office Supplies
    Product(name='Ergonomic Office Chair', description='A comfortable office chair with adjustable height, lumbar support, and a swivel base.', price=149.99, stock=25, category_id=categories_id['Office Supplies']),
    Product(name='Desk Organizer Set', description='A set of desktop organizers including trays, pen holders, and a drawer organizer.', price=9.99, stock=60, category_id=categories_id['Office Supplies']),
    Product(name='High-Speed Printer', description='A color laser printer with fast printing speeds and high-resolution output.', price=199.99, stock=20, category_id=categories_id['Office Supplies']),
    Product(name='Notebook & Pen Set', description='A set including a high-quality notebook and a smooth-writing pen.', price=14.99, stock=100, category_id=categories_id['Office Supplies']),
    Product(name='Whiteboard Calendar', description='A wall-mounted whiteboard with a calendar layout for tracking schedules and tasks.', price=24.99, stock=45, category_id=categories_id['Office Supplies']),
]
# session.add_all(categories)
# session.add_all(products)
result = session.query(Product).filter(Product.product_id==2).one()
print(type(result.price))
session.commit()
session.close()
