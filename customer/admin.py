from django.contrib import admin
from .models import Customer,IdentificationType # AddressType, CusomterAddress, 
from .models import RelationshipType, CustomerGroup #CustomerIdentification, RelationshipType
# from .models import CustomerBank
# from .models import Customer

# Register your models here.

admin.site.register(Customer)
admin.site.register(RelationshipType)
admin.site.register(IdentificationType)
admin.site.register(CustomerGroup)
# admin.site.register(AddressType)
# admin.site.register(CusomterAddress)
# admin.site.register(CustomerIdentification)
# admin.site.register(CustomerRelationship)
# admin.site.register(CustomerBank)
