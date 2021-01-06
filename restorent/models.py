from django.db import models
  

class Customer(models.Model):
    userid=models.EmailField(max_length=254)
    time=models.TextField(max_length=122)
    name=models.CharField(max_length=122)
    mobile=models.CharField(max_length=12)
    amount=models.IntegerField()
    class Meta:  
        db_table = "customer"  
    def __str__(self): 
        return self.title 

class Dish(models.Model):
    oid=models.IntegerField()
    dname=models.TextField(max_length=122)
    dquantity=models.IntegerField()
    damount=models.IntegerField()
    class Meta:  
        db_table = "dish"  
    def __str__(self): 
        return self.title 

class Menu(models.Model):
    userid=models.EmailField(max_length=254)
    dishname=models.TextField(max_length=200)
    dishprice=models.IntegerField()
    dishtype=models.TextField(max_length=200)
    class Meta:
        db_table="menu"



