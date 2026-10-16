from django.db import models
from django.contrib.auth.models import User





class Vendor(models.Model):

    name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    logo = models.ImageField(
        upload_to='vendors/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    

    def __str__(self):
        return self.name



class Product(models.Model):

    CATEGORY_CHOICES = [
        ('phones', 'Phones'),
        ('audio', 'Audio'),
        ('watch', 'Watch'),
        ('accessories', 'Accessories'),
        ('cmf', 'CMF Products'),
    ]

    vendor = models.ForeignKey(
    Vendor,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    image = models.ImageField(upload_to='products/')

    stock = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    processor_score = models.IntegerField(default=50)

    camera_score = models.IntegerField(default=50)

    battery_score = models.IntegerField(default=50)

    display_score = models.IntegerField(default=50)

    def __str__(self):
        return self.name




class Wishlist(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name




    

class Order(models.Model):

    full_name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    payment_method = models.CharField(max_length=50)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True
)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.product.name
    

