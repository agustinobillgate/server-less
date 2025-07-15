#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit

def select_ap_deliverynotebl(lief_nr:int, from_date:date, to_date:date):

    prepare_cache ([L_kredit])

    b1_list_data = []
    l_kredit = None

    b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"rgdatum":date, "name":string, "lscheinnr":string, "saldo":Decimal, "opart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_data, l_kredit
        nonlocal lief_nr, from_date, to_date


        nonlocal b1_list
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    for l_kredit in db_session.query(L_kredit).filter(
             (L_kredit.lief_nr == lief_nr) & (L_kredit.zahlkonto == 0) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date)).order_by(L_kredit.rgdatum, L_kredit.name).all():
        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.rgdatum = l_kredit.rgdatum
        b1_list.name = l_kredit.name
        b1_list.lscheinnr = l_kredit.lscheinnr
        b1_list.saldo =  to_decimal(l_kredit.saldo)
        b1_list.opart = l_kredit.opart

    return generate_output()