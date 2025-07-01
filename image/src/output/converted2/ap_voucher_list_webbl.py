#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, L_kredit, Bediener

def ap_voucher_list_webbl(fdate:date, tdate:date):

    prepare_cache ([L_lieferant, L_kredit, Bediener])

    age_list_list = []
    l_lieferant = l_kredit = bediener = None

    age_list = None

    age_list_list, Age_list = create_model("Age_list", {"supplier":string, "invoice":int, "datum":date, "counter":int, "debit":Decimal, "credit":Decimal, "balance":Decimal, "user_init":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal age_list_list, l_lieferant, l_kredit, bediener
        nonlocal fdate, tdate


        nonlocal age_list
        nonlocal age_list_list

        return {"age-list": age_list_list}

    l_kredit_obj_list = {}
    l_kredit = L_kredit()
    l_lieferant = L_lieferant()
    for l_kredit.rechnr, l_kredit.counter, l_kredit.rgdatum, l_kredit.bediener_nr, l_kredit.saldo, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant._recid in db_session.query(L_kredit.rechnr, L_kredit.counter, L_kredit.rgdatum, L_kredit.bediener_nr, L_kredit.saldo, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
             (L_kredit.rechnr != 0) & (L_kredit.rgdatum >= fdate) & (L_kredit.rgdatum <= tdate)).order_by(L_kredit.rechnr, L_lieferant.firma, L_kredit.rgdatum, L_kredit.zahlkonto).all():
        if l_kredit_obj_list.get(l_kredit._recid):
            continue
        else:
            l_kredit_obj_list[l_kredit._recid] = True

        age_list = query(age_list_list, filters=(lambda age_list: age_list.invoice == l_kredit.rechnr), first=True)

        if not age_list:
            age_list = Age_list()
            age_list_list.append(age_list)

            age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
            age_list.invoice = l_kredit.rechnr
            age_list.counter = l_kredit.counter
            age_list.datum = l_kredit.rgdatum

        if l_kredit.zahlkonto == 0:

            bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

            if bediener:
                age_list.user_init = bediener.userinit
            age_list.credit =  to_decimal(age_list.credit) + to_decimal(l_kredit.saldo)
            age_list.balance =  to_decimal(age_list.balance) + to_decimal(l_kredit.saldo)


        else:
            age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.saldo)
            age_list.balance =  to_decimal(age_list.balance) + to_decimal(l_kredit.saldo)

    return generate_output()