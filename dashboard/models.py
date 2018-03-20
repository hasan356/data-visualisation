from django.db import models

class Revenue(models.Model):
    MonthlyRevenue = models.CharField(max_length=50)
    Month = models.CharField(max_length=50)

    def __str__(self):
        return self.MonthlyRevenue + '-' + self.Month