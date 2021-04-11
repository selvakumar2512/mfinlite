from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from .models import Customer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime

def is_valid(param):
    return param != '' and param is not None

@login_required(login_url="/login/")
def customer_view(request):
    
    msg          = ''
    new_customer = 0
    
### create object of form 
    if request.method == "POST":
        form        = CustomerForm(request.POST) 
        # idform      = IDForm(request.POST)
        # addressform = AddressForm(request.POST)
### Save Customer         
        if form.is_valid():
            customer = Customer(
                client_id         = form.cleaned_data.get("client_id"),
                customer_id       = form.cleaned_data.get("customer_id"),
                external_id       = form.cleaned_data.get("external_id"),
                title             = form.cleaned_data.get("title"),
                first_name        = form.cleaned_data.get("first_name"),
                middle_name       = form.cleaned_data.get("middle_name"),
                last_name         = form.cleaned_data.get("last_name"),
                name_at_birth     = form.cleaned_data.get("name_at_birth"),
                full_name         = form.cleaned_data.get("full_name"),
                nick_name         = form.cleaned_data.get("nick_name"),
                gender            = form.cleaned_data.get("gender"),
                birth_place       = form.cleaned_data.get("birth_place"),
                marital_status    = form.cleaned_data.get("marital_status"),
                occupation        = form.cleaned_data.get("occupation"),
                nationality       = form.cleaned_data.get("nationality"),
                date_of_birth     = form.cleaned_data.get("date_of_birth"),
                date_of_marriage  = form.cleaned_data.get("date_of_marriage"),
                date_of_death     = form.cleaned_data.get("date_of_death"),
                valid_from        = form.cleaned_data.get("valid_from"),
                valid_to          = form.cleaned_data.get("valid_to"),
                status            = form.cleaned_data.get("status"),
                id_type           = form.cleaned_data.get("id_type"),
                id_number         = form.cleaned_data.get("id_number"),
                perm_house        = form.cleaned_data.get("perm_house"),
                perm_building     = form.cleaned_data.get("perm_building"),
                perm_street_1     = form.cleaned_data.get("perm_street_1"),
                perm_street_2     = form.cleaned_data.get("perm_street_2"),
                perm_village      = form.cleaned_data.get("perm_village"),
                perm_taluk        = form.cleaned_data.get("perm_taluk"),
                perm_district     = form.cleaned_data.get("perm_district"),
                perm_city         = form.cleaned_data.get("perm_city"),
                perm_postal_code  = form.cleaned_data.get("perm_postal_code"),
                perm_region       = form.cleaned_data.get("perm_region"),
                perm_country      = form.cleaned_data.get("perm_country"),
                cont_house        = form.cleaned_data.get("cont_house"),
                cont_building     = form.cleaned_data.get("cont_building"),
                cont_street_1     = form.cleaned_data.get("cont_street_1"),
                cont_street_2     = form.cleaned_data.get("cont_street_2"),
                cont_village      = form.cleaned_data.get("cont_village"),
                cont_taluk        = form.cleaned_data.get("cont_taluk"),
                cont_district     = form.cleaned_data.get("cont_district"),
                cont_city         = form.cleaned_data.get("cont_city"),
                cont_postal_code  = form.cleaned_data.get("cont_postal_code"),
                cont_region       = form.cleaned_data.get("cont_region"),
                cont_country      = form.cleaned_data.get("cont_country"),
                telephone         = form.cleaned_data.get("telephone"),
                mobile_phone      = form.cleaned_data.get("mobile_phone"),
                alternate_contact = form.cleaned_data.get("alternate_contact"),
                email_id          = form.cleaned_data.get("email_id"),
                rel_type          = form.cleaned_data.get("rel_type"),
                rel_title         = form.cleaned_data.get("rel_title"),
                rel_first_name    = form.cleaned_data.get("rel_first_name"),
                rel_middle_name   = form.cleaned_data.get("rel_middle_name"),
                rel_last_name     = form.cleaned_data.get("rel_last_name"),
                rel_full_name     = form.cleaned_data.get("rel_full_name"),
                rel_mobile        = form.cleaned_data.get("rel_mobile"),
                created_on        = datetime.now(),
                created_by        = str(request.user),
                changed_on        = datetime.now(),
                changed_by        = str(request.user),
                )
            # new_customer = customer.save(request)
            new_customer = customer.save()
            msg          = 'Customer ' + str(new_customer) + ' Created Successfully'    
### Save Address
#             if addressform.is_valid():
#                 address = CusomterAddress(
#                     client_id         = form.cleaned_data.get("client_id"),
#                     customer_id       = Customer.objects.get(customer_id=new_customer),
#                     address_type      = addressform.cleaned_data.get("address_type"),
#                     unit_number       = addressform.cleaned_data.get("unit_number"),
#                     building          = addressform.cleaned_data.get("building"),
#                     street_1          = addressform.cleaned_data.get("street_1"),
#                     street_2          = addressform.cleaned_data.get("street_2"),
#                     street_3          = addressform.cleaned_data.get("street_3"),
#                     street_4          = addressform.cleaned_data.get("street_4"),
#                     street_5          = addressform.cleaned_data.get("street_5"),
#                     city              = addressform.cleaned_data.get("city"),
#                     postal_code       = addressform.cleaned_data.get("postal_code"),
#                     region            = addressform.cleaned_data.get("region"),
#                     country           = addressform.cleaned_data.get("country"),
#                     telephone         = addressform.cleaned_data.get("telephone"),
#                     mobile_phone      = addressform.cleaned_data.get("mobile_phone"),                
#                     alternate_contact = addressform.cleaned_data.get("alternate_contact"),
#                     email_id          = addressform.cleaned_data.get("email_id"),
#                     created_on        = datetime.now(),
#                     created_by        = str(request.user),
#                     changed_on        = datetime.now(),
#                     changed_by        = str(request.user),
#                     )
#                 # address.save(request)
#                 address.save()
#             else:
#                 msg = addressform.errors
# ### Identification        
#             if idform.is_valid():
#                 id = CustomerIdentification(
#                     client_id   = form.cleaned_data.get("client_id"),
#                     customer_id = Customer.objects.get(customer_id=new_customer),
#                     id_type     = idform.cleaned_data.get("id_type"),
#                     id_number   = idform.cleaned_data.get("id_number"),
#                     created_on  = datetime.now(),
#                     created_by  = str(request.user),
#                     changed_on  = datetime.now(),
#                     changed_by  = str(request.user),                    
#                     )
#                 # id.save(request)
#                 id.save()
#             else:
#                 msg = idform.errors           
        else:
            msg = form.errors
    else:
        form = CustomerForm() 
        # idform = IDForm()
        # addressform = AddressForm()

    context = {
        'form': form,
        # 'addressform': addressform,
        # 'idform': idform,
        'msg': msg,
        'new_customer': new_customer,
        'segment': 'customer'
        }
 
    return render(request, 'customers/customer.html', context)

@login_required(login_url="/login/")
def custsearch_view(request):

    # customers =  CustomerIdentification.objects.none()
    customers = Customer.objects.none()
    # customers = Customer.objects.all()

    customer_id = request.GET.get("customer_id")
    first_name  = request.GET.get("first_name")
    last_name   = request.GET.get("last_name")
    id_number   = request.GET.get("id_number")
    # village     = request.GET.get("street_3")
    # taluk       = request.GET.get("street_4")
    # district    = request.GET.get("street_5")
    village     = request.GET.get("village")
    taluk       = request.GET.get("taluk")
    district    = request.GET.get("district")
    city        = request.GET.get("city")
    postal_code = request.GET.get("postal_code")
    region      = request.GET.get("region")
    
    if  ( is_valid(customer_id) | is_valid(last_name)   | 
          is_valid(first_name)  | is_valid(id_number)   | 
          is_valid(village)     | is_valid(taluk)       | 
          is_valid(district)    | is_valid(city)        | 
          is_valid(postal_code) | is_valid(region) ):
        
        customers = Customer.objects.all()
        # customers = CustomerIdentification.objects.all()
        # ad = CusomterAddress.objects.filter(customer_id__in=Subquery(
        #                     customers.values("customer_id")))
        # customers = customers.annotate(
        #             village=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                        ).values('street_3')),
        #             taluk=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                      ).values('street_4')),
        #             district=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                         ).values('street_5')),
        #             city=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                     ).values('city')),
        #             postal_code=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                            ).values('postal_code')),
        #             region=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                       ).values('region')),
        #             mobile=Subquery(ad.filter(customer_id=OuterRef('customer_id')
        #                                       ).values('mobile_phone'),
        #             ))
    
    if is_valid(customer_id):
        customers = customers.filter(Q(customer_id__icontains=customer_id)
                                     ).distinct()
    if is_valid(first_name):
        customers = customers.filter(Q(first_name__icontains=first_name)
                                     ).distinct()
    if is_valid(last_name):
        customers = customers.filter(Q(last_name__icontains=last_name)
                                     ).distinct()
    if is_valid(id_number):
        customers = customers.filter(Q(id_number__icontains=id_number))
    if is_valid(village):
        # customers = customers.filter(Q(village__icontains=village)).distinct()
        customers = customers.filter(Q(perm_village__icontains=village) | Q(cont_village__icontains=village)).distinct()
    if is_valid(taluk):
        # customers = customers.filter(Q(taluk__icontains=taluk)).distinct()
        customers = customers.filter(Q(perm_taluk__icontains=taluk) | Q(cont_taluk__icontains=taluk)).distinct()
    if is_valid(district):
        # customers = customers.filter(Q(district__icontains=district)).distinct()
        customers = customers.filter(Q(perm_district__icontains=district) | Q(cont_district__icontains=district)).distinct()
    if is_valid(city):
        # customers = customers.filter(Q(city__icontains=city)).distinct()
        customers = customers.filter(Q(perm_city__icontains=city) | Q(cont_city__icontains=city)).distinct()
    if is_valid(postal_code):
        # customers = customers.filter(Q(postal_code__icontains=postal_code)).distinct()
        customers = customers.filter(Q(perm_postal_code__icontains=postal_code) | Q(cont_postal_code__icontains=postal_code)).distinct()
    if is_valid(region):
        # customers = customers.filter(Q(region__icontains=region)).distinct()
        customers = customers.filter(Q(perm_region__icontains=region) | Q(cont_region__icontains=region)).distinct()

    context = { 
        'customers': customers,
        'segment': 'customer-search',
        }
    return render(request, 'customers/customer-search.html', context)

@login_required(login_url="/login/")
def custmanage_view(request):
       
    cust_id = request.GET.get("customer_id")
    # address_type = request.GET.get("add_type")
    # context = {}
    
    form = CustomerForm() 
    # idform = IDForm()
    # addressform = AddressForm()
    
    event = None
    # tab = 'personal_tab'
 
### Get Submit Event
    if 'get_customer' in request.GET:
        event = 'get_customer'
    
    if 'update_customer' in request.POST:
        event = 'update_customer'
    
### Get Active Tab
    # tab = request.GET.get('activeTab')
    
    if request.method =='GET':
        form = CustomerForm(request.GET)
        if is_valid(cust_id):
            customer = get_object_or_404(Customer, customer_id=cust_id)
            if customer:
                form = CustomerForm(initial={
                            'client_id':        customer.client_id, 
                            'customer_id':      customer.customer_id,
                            'external_id':      customer.external_id,
                            'title':            customer.title,
                            'first_name':       customer.first_name,
                            'middle_name':      customer.middle_name,
                            'last_name':        customer.last_name,
                            'name_at_birth':    customer.name_at_birth,
                            'full_name':        customer.full_name,
                            'nick_name':        customer.nick_name,
                            'gender':           customer.gender,
                            'birth_place':      customer.birth_place,
                            'marital_status':   customer.marital_status,
                            'occupation':       customer.occupation,
                            'nationality':      customer.nationality,
                            'date_of_birth':    customer.date_of_birth,
                            'date_of_marriage': customer.date_of_marriage,
                            'date_of_death':    customer.date_of_death,
                            'valid_from':       customer.valid_from,
                            'valid_to':         customer.valid_to,
                            'status':           customer.status,
                            'id_type':          customer.id_type,
                            'id_number':        customer.id_number,
                            'perm_house':       customer.perm_house,
                            'perm_building':    customer.perm_building,
                            'perm_street_1':    customer.perm_street_1,
                            'perm_street_2':    customer.perm_street_2,
                            'perm_village':     customer.perm_village,
                            'perm_taluk':       customer.perm_taluk,
                            'perm_district':    customer.perm_district,
                            'perm_city':        customer.perm_city,
                            'perm_postal_code': customer.perm_postal_code,
                            'perm_region':      customer.perm_region,
                            'perm_country':     customer.perm_country,
                            'cont_house':       customer.cont_house,
                            'cont_building':    customer.cont_building,
                            'cont_street_1':    customer.cont_street_1,
                            'cont_street_2':    customer.cont_street_2,
                            'cont_village':     customer.cont_village,
                            'cont_taluk':       customer.cont_taluk,
                            'cont_district':    customer.cont_district,
                            'cont_city':        customer.cont_city,
                            'cont_postal_code': customer.cont_postal_code,
                            'cont_region':      customer.cont_region,
                            'cont_country':     customer.cont_country,
                            'telephone':        customer.telephone,
                            'mobile_phone':     customer.mobile_phone,
                            'alternate_contact':customer.alternate_contact,
                            'email_id':         customer.email_id,
                            'rel_type':         customer.rel_type,
                            'rel_title':        customer.rel_title,
                            'rel_first_name':   customer.rel_first_name,
                            'rel_middle_name':  customer.rel_middle_name,
                            'rel_last_name':    customer.rel_last_name,
                            'rel_full_name':    customer.rel_full_name,
                            'rel_mobile':       customer.rel_mobile,
                            })                
            # if tab == 'personal_tab':
            #     customer = get_object_or_404(Customer, customer_id=cust_id)
            #     if customer:
            #         form = CustomerForm(initial={
            #                 'client_id':customer.client_id, 
            #                 'customer_id':customer.customer_id,
            #                 'external_id':customer.external_id,
            #                 'title':customer.title,
            #                 'first_name':customer.first_name,
            #                 'middle_name':customer.middle_name,
            #                 'last_name':customer.last_name,
            #                 'name_at_birth':customer.name_at_birth,
            #                 'full_name':customer.full_name,
            #                 'nick_name':customer.nick_name,
            #                 'gender':customer.gender,
            #                 'birth_place':customer.birth_place,
            #                 'marital_status':customer.marital_status,
            #                 'occupation':customer.occupation,
            #                 'nationality':customer.nationality,
            #                 'date_of_birth':customer.date_of_birth,
            #                 'date_of_marriage':customer.date_of_marriage,
            #                 'date_of_death':customer.date_of_death,
            #                 'valid_from':customer.valid_from,
            #                 'valid_to':customer.valid_to,
            #                 'status':customer.status,
            #                 })
            # elif tab == 'address_tab':
            #     if is_valid(address_type):
            #         address = CusomterAddress.objects.filter(customer_id=cust_id,
            #                                                  address_type=address_type)
            #         addressform = AddressForm(initial={
            #             'client_id': address.client_id,
            #             'customer_id': address.customer_id,
            #             'address_type': address.address_type,
            #             'unit_number': address.unit_number,                     
            #             })
            #         context["addresses"] = address
    else:
        # if event == 'update_customer':
        form = CustomerForm(request.POST) 
### Save Customer      
        cust_id = request.POST.get('customer_id')   
        if is_valid(cust_id):
            customer = get_object_or_404(Customer, customer_id=cust_id)
            if form.is_valid():
                customer.client_id          = form.cleaned_data.get("client_id")
                customer.customer_id        = form.cleaned_data.get("customer_id")
                customer.external_id        = form.cleaned_data.get("external_id")
                customer.title              = form.cleaned_data.get("title")
                customer.first_name         = form.cleaned_data.get("first_name")
                customer.middle_name        = form.cleaned_data.get("middle_name")
                customer.last_name          = form.cleaned_data.get("last_name")
                customer.name_at_birth      = form.cleaned_data.get("name_at_birth")
                customer.full_name          = form.cleaned_data.get("full_name")
                customer.nick_name          = form.cleaned_data.get("nick_name")
                customer.gender             = form.cleaned_data.get("gender")
                customer.birth_place        = form.cleaned_data.get("birth_place")
                customer.marital_status     = form.cleaned_data.get("marital_status")
                customer.occupation         = form.cleaned_data.get("occupation")
                customer.nationality        = form.cleaned_data.get("nationality")
                customer.date_of_birth      = form.cleaned_data.get("date_of_birth")
                customer.date_of_marriage   = form.cleaned_data.get("date_of_marriage")
                customer.date_of_death      = form.cleaned_data.get("date_of_death")
                customer.valid_from         = form.cleaned_data.get("valid_from")
                customer.valid_to           = form.cleaned_data.get("valid_to")
                customer.status             = form.cleaned_data.get("status")
                customer.id_type            = form.cleaned_data.get('id_type')
                customer.id_number          = form.cleaned_data.get('id_number')
                customer.perm_house         = form.cleaned_data.get('perm_house')
                customer.perm_building      = form.cleaned_data.get('perm_building')
                customer.perm_street_1      = form.cleaned_data.get('perm_street_1')
                customer.perm_street_2      = form.cleaned_data.get('perm_street_2')
                customer.perm_village       = form.cleaned_data.get('perm_village')
                customer.perm_taluk         = form.cleaned_data.get('perm_taluk')
                customer.perm_district      = form.cleaned_data.get('perm_district')
                customer.perm_city          = form.cleaned_data.get('perm_city')
                customer.perm_postal_code   = form.cleaned_data.get('perm_postal_code')
                customer.perm_region        = form.cleaned_data.get('perm_region')
                customer.perm_country       = form.cleaned_data.get('perm_country')
                customer.cont_house         = form.cleaned_data.get('cont_house')
                customer.cont_building      = form.cleaned_data.get('cont_building')
                customer.cont_street_1      = form.cleaned_data.get('cont_street_1')
                customer.cont_street_2      = form.cleaned_data.get('cont_street_2')
                customer.cont_village       = form.cleaned_data.get('cont_village')
                customer.cont_taluk         = form.cleaned_data.get('cont_taluk')
                customer.cont_district      = form.cleaned_data.get('cont_district')
                customer.cont_city          = form.cleaned_data.get('cont_city')
                customer.cont_postal_code   = form.cleaned_data.get('cont_postal_code')
                customer.cont_region        = form.cleaned_data.get('cont_region')
                customer.cont_country       = form.cleaned_data.get('cont_country')
                customer.telephone          = form.cleaned_data.get('telephone')
                customer.mobile_phone       = form.cleaned_data.get('mobile_phone')
                customer.alternate_contact  = form.cleaned_data.get('alternate_contact')
                customer.email_id           = form.cleaned_data.get('email_id')
                customer.rel_type           = form.cleaned_data.get('rel_type')
                customer.rel_title          = form.cleaned_data.get('rel_title')
                customer.rel_first_name     = form.cleaned_data.get('rel_first_name')
                customer.rel_middle_name    = form.cleaned_data.get('rel_middle_name')
                customer.rel_last_name      = form.cleaned_data.get('rel_last_name')
                customer.rel_full_name      = form.cleaned_data.get('rel_full_name')
                customer.rel_middle_name    = form.cleaned_data.get('rel_middle_name')
                customer.rel_last_name      = form.cleaned_data.get('rel_last_name')
                customer.rel_full_name      = form.cleaned_data.get('rel_full_name')
                customer.rel_mobile         = form.cleaned_data.get('rel_mobile')
                customer.changed_on         = datetime.now()
                customer.changed_by         = str(request.user)
                customer.update()
            
    context = {
        'form': form,
        'segment': 'customer-manage',
        'event': event
        }

    return render(request, 'customers/customer-manage.html', context)