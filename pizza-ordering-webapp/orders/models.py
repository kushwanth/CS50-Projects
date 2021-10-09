from django.db import models

# Create your models here.
SIZES = (
    ('S', 'Small'),
    ('L', 'Large'),
)
TYPES = (
('S', 'Silican'),
('R', 'Regular'),
)
ORDER_STATUS = (
		('Placed', 'Placed'),
		('Not Placed', 'Not Placed'),
		('Penging', 'Cooking'),
        ('Completed', 'Completed'),
)

class Topings(models.Model):
    toping_name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.toping_name}"

class Subs(models.Model):
    subs_name = models.CharField(max_length=32)
    subs_size = models.CharField(max_length=1, choices=SIZES, blank=False)
    subs_price = models.DecimalField(help_text="pice in US$", max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.subs_name} of size {self.subs_size} is priced at {self.subs_price}"

class Pastas(models.Model):
    pasta_name = models.CharField(max_length=32)
    pasta_price = models.DecimalField(help_text="pice in US$", max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.pasta_name} is priced at {self.pasta_price}"

class Salads(models.Model):
    salad_name = models.CharField(max_length=32)
    salad_price = models.DecimalField(help_text="pice in US$", max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.salad_name} is priced at {self.salad_price}"

class DP(models.Model):
    dp_name = models.CharField(max_length=32)
    dp_size = models.CharField(max_length=1, choices=SIZES, blank=False)
    dp_price = models.DecimalField(help_text="price in US$", max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.dp_name} of size {self.dp_size} is priced at {self.dp_price}"

class Pizza(models.Model):
    pizza_name = models.CharField(max_length=32, blank=False)
    pizza_size = models.CharField(max_length=1, choices=SIZES, blank=False)
    pizza_type = models.CharField(max_length=1, choices=TYPES, blank=False)
    pizza_price = models.DecimalField(help_text="price in US$", max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pizza_type} {self.pizza_name} topings of size {self.pizza_size} - {self.pizza_price}"

class orderplaced(models.Model):
    order_number = models.IntegerField(primary_key=True, blank=False)
    order_name = models.CharField(max_length=64,blank=False)
    order_price = models.DecimalField(max_digits=9,decimal_places=2, blank=False)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Not Placed')

    def __str__(self):
        return f"{self.order_number} {self.order_name} has placed an order of {self.order_price} with status {self.order_status}"

class orderitems(models.Model):
    order_id = models.IntegerField(blank=False)
    items = models.CharField(max_length=128, blank=True)
    items_price = models.DecimalField(max_digits=5,decimal_places=2, blank=False)

    def __str__(self):
        return f"{self.order_id}"
