#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, Artikel, Bediener

def prepare_view_apitembl(ap_recid:int):

    prepare_cache ([L_kredit, Artikel, Bediener])

    counter = 0
    invoice = ""
    q1_list_data = []
    l_kredit = artikel = bediener = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"netto":Decimal, "zahlkonto":int, "bezeich":string, "rgdatum":date, "saldo":Decimal, "username":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, invoice, q1_list_data, l_kredit, artikel, bediener
        nonlocal ap_recid


        nonlocal q1_list
        nonlocal q1_list_data

        return {"counter": counter, "invoice": invoice, "q1-list": q1_list_data}

    l_kredit = get_cache (L_kredit, {"_recid": [(eq, ap_recid)]})

    if l_kredit:
        counter = l_kredit.counter
        invoice = l_kredit.name

    if counter != 0:

        l_kredit_obj_list = {}
        l_kredit = L_kredit()
        artikel = Artikel()
        bediener = Bediener()
        for l_kredit.counter, l_kredit.name, l_kredit.netto, l_kredit.zahlkonto, l_kredit.rgdatum, l_kredit.saldo, l_kredit._recid, artikel.bezeich, artikel._recid, bediener.username, bediener._recid in db_session.query(L_kredit.counter, L_kredit.name, L_kredit.netto, L_kredit.zahlkonto, L_kredit.rgdatum, L_kredit.saldo, L_kredit._recid, Artikel.bezeich, Artikel._recid, Bediener.username, Bediener._recid).join(Artikel,(Artikel.artnr == L_kredit.zahlkonto) & (Artikel.departement == 0)).join(Bediener,(Bediener.nr == L_kredit.bediener_nr)).filter(
                 (L_kredit.counter == counter) & (L_kredit.opart >= 0) & (L_kredit.zahlkonto > 0)).order_by(L_kredit.rgdatum, L_kredit.zahlkonto).all():
            if l_kredit_obj_list.get(l_kredit._recid):
                continue
            else:
                l_kredit_obj_list[l_kredit._recid] = True


            q1_list = Q1_list()
            q1_list_data.append(q1_list)

            q1_list.netto =  to_decimal(l_kredit.netto)
            q1_list.zahlkonto = l_kredit.zahlkonto
            q1_list.bezeich = artikel.bezeich
            q1_list.rgdatum = l_kredit.rgdatum
            q1_list.saldo =  to_decimal(l_kredit.saldo)
            q1_list.username = bediener.username


    return generate_output()