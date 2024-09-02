from functions.additional_functions import *
import decimal
from models import L_kredit, Artikel, Bediener

def prepare_view_apitembl(ap_recid:int):
    counter = 0
    invoice = ""
    q1_list_list = []
    l_kredit = artikel = bediener = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"netto":decimal, "zahlkonto":int, "bezeich":str, "rgdatum":date, "saldo":decimal, "username":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, invoice, q1_list_list, l_kredit, artikel, bediener


        nonlocal q1_list
        nonlocal q1_list_list
        return {"counter": counter, "invoice": invoice, "q1-list": q1_list_list}

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit._recid == ap_recid)).first()
    counter = l_kredit.counter
    invoice = l_kredit.name

    if counter != 0:

        l_kredit_obj_list = []
        for l_kredit, artikel, bediener in db_session.query(L_kredit, Artikel, Bediener).join(Artikel,(Artikel.artnr == L_kredit.zahlkonto) &  (Artikel.departement == 0)).join(Bediener,(Bediener.nr == L_kredit.bediener_nr)).filter(
                (L_kredit.counter == counter) &  (L_kredit.opart >= 0) &  (L_kredit.zahlkonto > 0)).all():
            if l_kredit._recid in l_kredit_obj_list:
                continue
            else:
                l_kredit_obj_list.append(l_kredit._recid)


            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.netto = l_kredit.netto
            q1_list.zahlkonto = l_kredit.zahlkonto
            q1_list.bezeich = artikel.bezeich
            q1_list.rgdatum = l_kredit.rgdatum
            q1_list.saldo = l_kredit.saldo
            q1_list.username = bediener.username


    return generate_output()