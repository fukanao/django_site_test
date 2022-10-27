from django.db import models

# myapp/models.py

class Blog(models.Model):
    #title = models.CharField(blank=False, null=False, max_length=150)
    id_num = models.IntegerField(primary_key=True)
    title = models.CharField(blank=True, max_length=150)
    text  = models.TextField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    product = models.CharField(max_length=200, blank=True)
    '''
    def __str__(self):
        return self.title
        #return self.str(id_num)
    '''

class Products(models.Model):
    #id_num = models.IntegerField(primary_key=True, blank=False, null=False)
    product = models.CharField(blank=False, max_length=100)
    #mst_id = models.FloatField(blank=False, null=False)
    mst_id = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.product


