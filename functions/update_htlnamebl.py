#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def update_htlnamebl(htl_name:string, htl_adr1:string, htl_adr2:string, htl_adr3:string, htl_tel:string, htl_fax:string, htl_email:string):

    prepare_cache ([Paramtext])

    paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal paramtext
        nonlocal htl_name, htl_adr1, htl_adr2, htl_adr3, htl_tel, htl_fax, htl_email

        return {}

    def update_it():

        nonlocal paramtext
        nonlocal htl_name, htl_adr1, htl_adr2, htl_adr3, htl_tel, htl_fax, htl_email

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
        paramtext.ptexte = htl_name

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
        paramtext.ptexte = htl_adr1

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 202)]})
        paramtext.ptexte = htl_adr2

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
        paramtext.ptexte = htl_adr3

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
        paramtext.ptexte = htl_tel

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 205)]})
        paramtext.ptexte = htl_fax

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 206)]})
        paramtext.ptexte = htl_email


    update_it()

    return generate_output()