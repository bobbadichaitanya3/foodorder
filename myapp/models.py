from django.db import models
from django .contrib.auth.models import User
class Category(models.Model):
    title=models.CharField(max_length=50)
    img=models.ImageField(upload_to='')
    slug=models.SlugField()
    def _str_(self):
        return self.title
class Product(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    slug=models.SlugField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    img=models.ImageField(upload_to='')
    product_available=models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.title 
class Cart(models.Model):
    cart_id=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.IntegerField()
    timestamp=models.DateTimeField(auto_now=True)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    def __str__(self):
        return self.product.title
    def update_quantity(self,quantity):
        self.quantity+=quantity
        self.save()
    def total(self):
        return self.quantity*self.price
class Buy(models.Model):
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product.title+'_'+str(self.id)

class TimeStamp(models.Model):
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User,on_delete = models.CASCADE)

	class Meta:
		abstract = True

class Review(TimeStamp):
	post = models.ForeignKey(Product,on_delete = models.CASCADE)
	review = models.TextField()

	def _str_(self):
		return self.review 

