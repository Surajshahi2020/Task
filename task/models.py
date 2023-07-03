from django.db import models


class Location(models.Model):
    province = models.TextField()
    district = models.TextField()
    muncipality = models.TextField()
    project_title = models.TextField()
    project_status = models.TextField()
    donor = models.TextField()
    executing_agency = models.TextField()
    implementing_partner = models.TextField()
    counterpart_ministry = models.TextField()
    type_of_assistance = models.TextField()
    budget_type = models.TextField()
    humanitarian = models.TextField()
    sector = models.TextField()
    agreement_date = models.DateField()
    commitments = models.IntegerField()
    disbursement = models.IntegerField()

    def __str__(self):
        return f"{self.province}--{self.commitments}"
