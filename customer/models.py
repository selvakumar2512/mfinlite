from django.db import models
from masterdata.models import Client #, BankMaster
from datetime import date #, datetime
from django.utils.timezone import now
# from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

# Create your models here.


# alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only characters are allowed.')

class RelationshipType(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    relationship_type = models.CharField(primary_key=True, max_length=12, null=False, blank=False )
    relationship_name = models.CharField(max_length=80, null=True, blank=True)
    
    class Meta:
        ordering = ['client_id', 'relationship_type']
    
    def __str__(self):
        return f'{self.relationship_name}'
    
class IdentificationType(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    id_type = models.CharField(primary_key=True, max_length=12, null=False, blank=False )
    id_name = models.CharField(max_length=80, null=True, blank=True)
    
    class Meta:
        ordering = ['client_id', 'id_type']
    
    def __str__(self):
        return f'{self.id_name}'


class Customer(models.Model):

        
# Generate Customer Number

    # def customer_no():
    #      last_customer = Customer.objects.all().order_by('customer_id').last()
    #      if not last_customer:
    #          return '000000000001'
    #      cust_id = last_customer.customer_id
    #      new_customer = cust_id + 1
    #      return new_customer
     
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    customer_id = models.BigAutoField(primary_key=True, default=1, editable=False, auto_created=True)
    external_id = models.CharField(max_length=15, null=True, blank=True )
    
    TITLE_LIST = (
        ('MR', 'Mr.'),
        ('MS', 'Ms.'),
        ('MRS', 'Mrs.'),
        ('DR', 'Dr.'),
        )
    
    title = models.CharField(max_length=3, choices=TITLE_LIST, blank=True, default='MR', verbose_name="title" )
    first_name = models.CharField(max_length=80, null=False, blank=False, )
    middle_name = models.CharField(max_length=80, default='' )
    last_name = models.CharField(max_length=80, default='' )
    name_at_birth = models.CharField(max_length=80, default='' )
    full_name = models.CharField(max_length=160, default='' )
    nick_name = models.CharField(max_length=80,  default='' )
    
    GENDER_LIST = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Third Gender'),
        ('U', 'Unknown'),
        )
    
    gender = models.CharField(max_length=1, choices=GENDER_LIST, blank=False, default='M' )
    birth_place = models.CharField(max_length=80, blank=True, default='' )
    
    MARITAL_LIST = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('I', 'In a Relationship'),
        ('P', 'Separated'),
        )
    
    marital_status = models.CharField(max_length=1, choices=MARITAL_LIST, blank=False, default='M' )
    occupation = models.CharField(max_length=80, default=''  )
    nationality = models.CharField(max_length=80, default='' )
    date_of_birth = models.DateField()
    date_of_marriage = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField(default='31/12/9999')
    
    id_type = models.ForeignKey('IdentificationType', on_delete=models.SET_NULL, null=True)
    id_number = models.CharField(max_length=80, null=False, blank=False)
    
    perm_house       = models.CharField(max_length=20, null=True, blank=True, help_text='House Number')
    perm_building    = models.CharField(max_length=80, null=True, blank=True, help_text='Building Name')
    perm_street_1    = models.CharField(max_length=80, null=True, blank=True, help_text='Street 1')
    perm_street_2    = models.CharField(max_length=80, null=True, blank=True, help_text='Street 2')
    perm_village     = models.CharField(max_length=80, null=True, blank=True, help_text='Village')
    perm_taluk       = models.CharField(max_length=80, null=True, blank=True, help_text='Taluk')
    perm_district    = models.CharField(max_length=80, null=True, blank=True, help_text='District')
    perm_city        = models.CharField(max_length=40, null=False, blank=False)
    perm_postal_code = models.CharField(max_length=20, null=False, blank=False)
    perm_region      = models.CharField(max_length=40, null=True, blank=True, help_text='Region/State')
    perm_country     = models.CharField(max_length=40, null=True, blank=True)
    
    cont_house       = models.CharField(max_length=20, null=True, blank=True, help_text='House Number')
    cont_building    = models.CharField(max_length=80, null=True, blank=True, help_text='Building Name')
    cont_street_1    = models.CharField(max_length=80, null=True, blank=True, help_text='Street 1')
    cont_street_2    = models.CharField(max_length=80, null=True, blank=True, help_text='Street 2')
    cont_village     = models.CharField(max_length=80, null=True, blank=True, help_text='Village')
    cont_taluk       = models.CharField(max_length=80, null=True, blank=True, help_text='Taluk')
    cont_district    = models.CharField(max_length=80, null=True, blank=True, help_text='District')
    cont_city        = models.CharField(max_length=40, null=True, blank=True,)
    cont_postal_code = models.CharField(max_length=20, null=True, blank=True,)
    cont_region      = models.CharField(max_length=40, null=True, blank=True, help_text='Region/State')
    cont_country     = models.CharField(max_length=40, null=True, blank=True,)
    
    telephone = models.CharField(max_length=15, null=False, blank=False)
    mobile_phone = models.CharField(max_length=15, null=False, blank=False)
    alternate_contact = models.CharField(max_length=15, null=False, blank=False)
    email_id = models.CharField(max_length=80, null=True, blank=True)
    
    rel_type = models.ForeignKey(RelationshipType, on_delete=models.SET_NULL, null=True)   
    rel_title = models.CharField(max_length=3, choices=TITLE_LIST, blank=True, default='MR', verbose_name="title" )
    rel_first_name = models.CharField(max_length=80, null=False, blank=False )
    rel_middle_name = models.CharField(max_length=80, null=True, blank=True )
    rel_last_name = models.CharField(max_length=80, null=True, blank=True )
    rel_full_name = models.CharField(max_length=160, null=True, blank=True )
    rel_mobile = models.CharField(max_length=15, null=False, blank=False)
   
    gua_title = models.CharField(max_length=3, choices=TITLE_LIST, blank=True, default='MR', verbose_name="title" )
    gua_first_name = models.CharField(max_length=80, null=False, blank=True )
    gua_middle_name = models.CharField(max_length=80, null=True, blank=True )
    gua_last_name = models.CharField(max_length=80, null=True, blank=True )
    gua_full_name = models.CharField(max_length=160, null=True, blank=True )
    gua_mobile = models.CharField(max_length=15, null=False, blank=True)    
    
    STATUS_LIST = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('D', 'Deleted'),
        )
    
    status = models.CharField(max_length=1, choices=STATUS_LIST, blank=True, default='A' )
    created_on = models.DateTimeField(verbose_name=_("Created On"), auto_now=True)
    created_by = models.CharField(max_length=20, blank=True, default='' )
    changed_on = models.DateTimeField(verbose_name=_("Changed On"), auto_now_add=True)
    changed_by = models.CharField(max_length=20, blank=True, default='' ) 
    
    class Meta:
        ordering = ['client_id', 'customer_id']    
    
    def __str__(self):
        return f'{self.customer_id}, {self.full_name}'
    
    def save(self):
        # if not self.customer_id:
        #         self.customer_id = '1'
        # else:
        #    self.customer_id+=1 
        if not self.customer_id:
            last_customer = Customer.objects.all().order_by('customer_id').last()
            if last_customer:
                self.customer_id = last_customer.customer_id + 1
            else:
                self.customer_id = '1'
        
        # self.created_on = datetime.now()
        # self.created_by = str(request.user)
        # self.changed_on = datetime.now()
        # self.changed_by = str(request.user)
        super(Customer,self).save()
        return self.customer_id
    
    def update(self):
        super(Customer,self).save()

class CustomerGroup(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    group_id  = models.CharField(primary_key=True, max_length=15, null=False,
                                        blank=False)
    group_name = models.CharField(max_length=80, null=False, blank=False)
    customer = models.ManyToManyField(Customer)
    created_on = models.DateTimeField(verbose_name=_("Created On"), auto_now=True)
    created_by = models.CharField(max_length=20, blank=True, default='' )
    changed_on = models.DateTimeField(verbose_name=_("Changed On"), auto_now_add=True)
    changed_by = models.CharField(max_length=20, blank=True, default='' ) 
    
    class Meta:
        ordering = ['client_id', 'group_id']
    
    def __str__(self):
        return f'{self.group_id}, {self.group_name}'
    
# class AddressType(models.Model):
#     client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
#     address_type = models.CharField(primary_key=True, max_length=1, blank=False)
#     address_name = models.CharField(max_length=80, null=True, blank=True)
    
#     class Meta:
#         ordering = ['client_id', 'address_type']    
    
#     def __str__(self):
#         return f'{self.address_name}'
    
# class CusomterAddress(models.Model):
#     client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)    
#     address_type = models.ForeignKey('AddressType', on_delete=models.SET_NULL, null=True)
#     unit_number = models.CharField(max_length=20, null=True, blank=True, help_text='House Number')
#     building = models.CharField(max_length=80, null=True, blank=True, help_text='Building Name')
#     street_1 = models.CharField(max_length=80, null=True, blank=True, help_text='Street 1')
#     street_2 = models.CharField(max_length=80, null=True, blank=True, help_text='Street 2')
#     street_3 = models.CharField(max_length=80, null=True, blank=True, help_text='Village')
#     street_4 = models.CharField(max_length=80, null=True, blank=True, help_text='Taluk')
#     street_5 = models.CharField(max_length=80, null=True, blank=True, help_text='District')
#     city = models.CharField(max_length=40, null=False, blank=False)
#     postal_code = models.CharField(max_length=20, null=False, blank=False)
#     region = models.CharField(max_length=40, null=True, blank=True, help_text='Region/State')
#     country = models.CharField(max_length=40, null=True, blank=True)
#     telephone = models.CharField(max_length=15, null=False, blank=False)
#     mobile_phone = models.CharField(max_length=15, null=False, blank=False)
#     alternate_contact = models.CharField(max_length=15, null=False, blank=False)
#     email_id = models.CharField(max_length=80, null=False, blank=False)
#     created_on = models.DateTimeField()
#     created_by = models.CharField(max_length=20, null=True, blank=True )
#     changed_on = models.DateTimeField(default=now, editable=False)
#     changed_by = models.CharField(max_length=20, null=True, blank=True )
    
#     class Meta:
#         ordering = ['client_id', 'customer_id']    
    
#     def __str__(self):
#         return f'{self.customer_id}, {self.street_1}, {self.city}, {self.region}, {self.country}'

#     def save(self):
#         # self.created_on = datetime.now()
#         # self.created_by = request.user
#         # self.changed_on = datetime.now()
#         # self.changed_by = request.user
#         super(CusomterAddress,self).save()

# class CustomerIdentification(models.Model):
#     client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
#     id_type = models.ForeignKey('IdentificationType', on_delete=models.SET_NULL, null=True)
#     id_number = models.CharField(max_length=80, null=False, blank=False)
#     created_on = models.DateTimeField()
#     created_by = models.CharField(max_length=20, null=True, blank=True )
#     changed_on = models.DateTimeField(default=now, editable=False)
#     changed_by = models.CharField(max_length=20, null=True, blank=True )
    
#     class Meta:
#         ordering = ['client_id', 'customer_id', 'id_type']
    
#     def __str__(self):
#         return f'{self.customer_id}, {self.id_type}, {self.id_number}'
    
#     def save(self):
#         # self.created_on = datetime.now()
#         # self.created_by = request.user
#         # self.changed_on = datetime.now()
#         # self.changed_by = request.user
#         super(CustomerIdentification,self).save()

# class CustomerRelationship(models.Model):
#     client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
#     relationship_type = models.ForeignKey('RelationshipType', on_delete=models.SET_NULL, null=True)
    
#     TITLE_LIST = (
#         ('1', 'Mr.'),
#         ('2', 'Ms.'),
#         ('3', 'Mrs.'),
#         ('4', 'Dr.'),
#         )
    
#     title = models.CharField(max_length=1, choices=TITLE_LIST, blank=True, default='1' )
#     first_name = models.CharField(max_length=80, null=False, blank=False )
#     middle_name = models.CharField(max_length=80, null=True, blank=True )
#     last_name = models.CharField(max_length=80, null=True, blank=True )
#     full_name = models.CharField(max_length=160, null=True, blank=True )
#     created_on = models.DateTimeField()
#     created_by = models.CharField(max_length=20, null=True, blank=True )
#     changed_on = models.DateTimeField(default=now, editable=False)
#     changed_by = models.CharField(max_length=20, null=True, blank=True )
    
#     class Meta:
#         ordering = ['client_id', 'customer_id', 'relationship_type']
    
#     def __str__(self):
#         return f'{self.customer_id}, {self.relationship_type}, {self.relationship_name}'

# class CustomerBank(models.Model):
#     client_id = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
#     customer_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
#     bank_name = models.ForeignKey(BankMaster, on_delete=models.SET_NULL, null=True)
#     bank_branch = models.CharField(max_length=60, null=False, blank=False)
#     ifsc_code = models.CharField(max_length=60, null=False, blank=False)   
#     name_in_bank = models.CharField(max_length=32, null=False, blank=False )
#     account_number = models.CharField(max_length=20, null=False, blank=False )
#     swift_code = models.CharField(max_length=20, null=True, blank=True )     
#     created_on = models.DateTimeField()
# #    created_at = models.DateTimeField()
#     created_by = models.CharField(max_length=20, null=True, blank=True )
#     changed_on = models.DateTimeField(default=now, editable=False)
# #    changed_at = models.DateTimeField()
#     changed_by = models.CharField(max_length=20, null=True, blank=True )
    
#     class Meta:
#         ordering = ['client_id', 'customer_id', 'bank_name']
    
#     def __str__(self):
#         return f'{self.customer_id}, {self.bank_name}, {self.bank_branch}'
    
    
        