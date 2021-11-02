from django.db import models

# Describes one record as provided by an external file
class Record(models.Model):
    seq = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)    
    last_name = models.CharField(max_length=30)    
    age = models.IntegerField()
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    ccnumber = models.BigIntegerField()

    class Meta:	
        ordering = ['seq']

    def __str__(self):
        return str(self.seq)
