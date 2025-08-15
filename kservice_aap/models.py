from django.db import models

class KserviceRecords(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    t_date = models.DateField(blank=True, null=True)
    akuser_id = models.IntegerField(blank=True, null=True)
    portfolio_lender = models.CharField(max_length=255, blank=True, null=True)
    borrower_name = models.CharField(max_length=255, blank=True, null=True)
    origination_date = models.DateField(blank=True, null=True)
    maturity_date = models.DateField(blank=True, null=True)
    origination_amount = models.CharField(max_length=100, blank=True, null=True)
    salesforce_ticket_number = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    business_structure = models.CharField(max_length=255, blank=True, null=True)
    kore = models.CharField(max_length=255, blank=True, null=True)
    inscribe = models.CharField(db_column='Inscribe', max_length=255, blank=True, null=True)  # Field name made lowercase.
    google_search = models.CharField(max_length=255, blank=True, null=True)
    tlo = models.CharField(max_length=255, blank=True, null=True)
    case_status = models.CharField(max_length=45, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    application_loan_number = models.IntegerField(blank=True, null=True)

   

class ChangeLog(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    case_id = models.IntegerField(blank=True, null=True)
    numner_old = models.CharField(max_length=45, blank=True, null=True)
    numner_new = models.IntegerField(blank=True, null=True)
    comment_old = models.TextField(blank=True, null=True)
    comment_new = models.TextField(blank=True, null=True)
    kore_old = models.CharField(max_length=255, blank=True, null=True)
    kore_new = models.CharField(max_length=255, blank=True, null=True)
    inscribe_old = models.CharField(db_column='Inscribe_old', max_length=255, blank=True, null=True)  # Field name made lowercase.
    google_search = models.CharField(max_length=255, blank=True, null=True)
    tlo_old = models.CharField(max_length=255, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

   
