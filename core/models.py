from django.db import models
from django.contrib.auth.models import User

# Категорія для меню
class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

# Пункти меню
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_items")

    def __str__(self):
        return self.title

# Кошик користувача
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Cart: {self.user.username} - {self.menu_item.title}"

# Замовлення
class Order(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order: {self.user.username} - {self.status}"
