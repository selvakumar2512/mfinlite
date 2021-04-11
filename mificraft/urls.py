"""mificraft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
#from django.urls import path
#from django.conf.urls import url,include
#from authentication import views

#urlpatterns = [
#    path('admin/', admin.site.urls),
#    url(r'^$',views.user_login,name='user_login'),
#    url(r'^authentication/',include('authentication.urls')),
#    url(r'^logout/$', views.user_logout, name='logout'),
#]

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),               # Django admin route
    path('customers/', include("customer.urls"),),
    path('loans/', include("loan.urls"),),
    path("", include("authentication.urls")),      # Auth routes - login / register
    path("", include("app.urls")),                 # UI Kits Html files
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

