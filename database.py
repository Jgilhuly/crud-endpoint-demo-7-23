"""Database module for in-memory product storage."""
from typing import List, Optional
from datetime import datetime

from models import Product, ProductCreate, ProductUpdate


class InMemoryDatabase:
    """In-memory database for storing and managing products."""

    def __init__(self):
        self.products: List[Product] = []
        self.next_id = 1
        self._init_sample_data()

    def _init_sample_data(self):
        """Initialize the database with sample product data."""
        sample_products = [
            ProductCreate(
                name="Wireless Headphones",
                description="High-quality wireless headphones with noise cancellation",
                price=199.99,
                category="Electronics",
                tags=["audio", "wireless", "premium"]
            ),
            ProductCreate(
                name="Coffee Maker",
                description="Programmable coffee maker with built-in grinder",
                price=89.99,
                category="Appliances",
                tags=["kitchen", "coffee", "automatic"]
            ),
            ProductCreate(
                name="Laptop Stand",
                description="Adjustable aluminum laptop stand for ergonomic work",
                price=45.99,
                category="Accessories",
                tags=["ergonomic", "aluminum", "adjustable"]
            ),
            ProductCreate(
                name="Bluetooth Speaker",
                description="Portable waterproof Bluetooth speaker with 12-hour battery",
                price=79.99,
                category="Electronics",
                tags=["audio", "bluetooth", "portable", "waterproof"]
            ),
            ProductCreate(
                name="Office Chair",
                description="Ergonomic office chair with lumbar support and mesh back",
                price=299.99,
                category="Furniture",
                tags=["ergonomic", "office", "lumbar", "mesh"]
            ),
            ProductCreate(
                name="Smart Watch",
                description="Fitness tracking smart watch with heart rate monitor",
                price=249.99,
                category="Electronics",
                tags=["fitness", "smart", "health", "wearable"]
            )
        ]

        for product_data in sample_products:
            self.create_product(product_data)

    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product in the database."""
        product = Product(
            id=self.next_id,
            **product_data.dict(),
            created_at=datetime.now()
        )
        self.products.append(product)
        self.next_id += 1
        return product

    def get_all_products(self) -> List[Product]:
        """Get all products from the database."""
        return self.products

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a specific product by ID."""
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def update_product(self, product_id: int, update_data: ProductUpdate) -> Optional[Product]:
        """Update an existing product in the database."""
        product = self.get_product(product_id)
        if not product:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(product, field, value)

        return product

    def delete_product(self, product_id: int) -> bool:
        """Delete a product from the database."""
        for i, product in enumerate(self.products):
            if product.id == product_id:
                del self.products[i]
                return True
        return False

    def search_products(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        tags: Optional[List[str]] = None
    ) -> List[Product]:
        """
        Search products based on various criteria.
        
        Args:
            query: Search term to match against name and description
            category: Filter by category
            min_price: Minimum price filter
            max_price: Maximum price filter
            in_stock: Filter by stock status
            tags: List of tags to match (any tag match)
        
        Returns:
            List of products matching the search criteria
        """
        results = self.products.copy()
        
        # Text search in name and description
        if query:
            query_lower = query.lower()
            results = [
                product for product in results
                if (query_lower in product.name.lower() or 
                    query_lower in product.description.lower())
            ]
        
        # Category filter
        if category:
            results = [
                product for product in results
                if product.category.lower() == category.lower()
            ]
        
        # Price range filter
        if min_price is not None:
            results = [
                product for product in results
                if product.price >= min_price
            ]
        
        if max_price is not None:
            results = [
                product for product in results
                if product.price <= max_price
            ]
        
        # Stock status filter
        if in_stock is not None:
            results = [
                product for product in results
                if product.in_stock == in_stock
            ]
        
        # Tags filter (any tag match)
        if tags:
            tag_set = set(tag.lower() for tag in tags)
            results = [
                product for product in results
                if any(tag.lower() in tag_set for tag in product.tags)
            ]
        
        return results

    def get_categories(self) -> List[str]:
        """Get all unique categories from products."""
        categories = set(product.category for product in self.products)
        return sorted(list(categories))

    def get_all_tags(self) -> List[str]:
        """Get all unique tags from products."""
        all_tags = set()
        for product in self.products:
            all_tags.update(product.tags)
        return sorted(list(all_tags))


# Global database instance
db = InMemoryDatabase()
