from django.db import models
from django.contrib.auth.models import User

class stock_info(models.Model):  # Class names should be in CamelCase
    symbol = models.CharField(max_length=50)
    price = models.FloatField()
    no_of_shares = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(default=0)
    flag= models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        # Calculate the total value
        if self.flag==0:
            self.total = self.price * self.no_of_shares
        else:
            pass
        # Call the parent class's save method
        super(stock_info, self).save(*args, **kwargs)
    def __str__(self):
        return self.symbol
