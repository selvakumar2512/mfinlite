# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:55:21 2021

@author: Abinesh
"""

from __future__ import unicode_literals

# from .models import LoanMaster, LoanAsset, LoanTransactions

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL     # Typically /static/
    #static Root
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def generate_pdf(template_src,context_dict={}):
    
    template = get_template(template_src)
    html     = template.render(context_dict)
    result   = BytesIO()
    pdf      = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)

    if not pdf.err:
        return result.getvalue()
    
    return None
    