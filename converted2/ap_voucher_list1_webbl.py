#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, L_lieferant, Bediener

input_paylist_data, Input_paylist = create_model("Input_paylist", {"fdate":string, "tdate":string, "excl_pay":bool})

def ap_voucher_list1_webbl(input_paylist_data:[Input_paylist]):

    prepare_cache ([L_kredit, L_lieferant, Bediener])

    pay_flag:bool = False
    tot_debit:Decimal = to_decimal("0.0")
    tot_credit:Decimal = to_decimal("0.0")
    tot_balance:Decimal = to_decimal("0.0")
    from_date:date = None
    to_date:date = None
    age_list_data = []
    l_kredit = l_lieferant = bediener = None

    age_list = input_paylist = b_kredit = None

    age_list_data, Age_list = create_model("Age_list", {"supplier":string, "invoice":int, "datum":date, "counter":int, "debit":Decimal, "credit":Decimal, "balance":Decimal, "user_init":string})

    B_kredit = create_buffer("B_kredit",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pay_flag, tot_debit, tot_credit, tot_balance, from_date, to_date, age_list_data, l_kredit, l_lieferant, bediener
        nonlocal b_kredit


        nonlocal age_list, input_paylist, b_kredit
        nonlocal age_list_data

        return {"age-list": age_list_data}


    input_paylist = query(input_paylist_data, first=True)
    if input_paylist.fdate is None or input_paylist.tdate is None:
        return generate_output
    
    from_date = date_mdy(input_paylist.fdate)
    to_date = date_mdy(input_paylist.tdate)

    l_kredit_obj_list = {}
    l_kredit = L_kredit()
    l_lieferant = L_lieferant()
    for l_kredit.rechnr, l_kredit.counter, l_kredit.rgdatum, l_kredit.saldo, l_kredit.bediener_nr, l_kredit.zahlkonto, l_kredit._recid, l_lieferant.firma, l_lieferant.anredefirma, l_lieferant._recid in db_session.query(L_kredit.rechnr, L_kredit.counter, L_kredit.rgdatum, L_kredit.saldo, L_kredit.bediener_nr, L_kredit.zahlkonto, L_kredit._recid, L_lieferant.firma, L_lieferant.anredefirma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
             (L_kredit.rechnr != 0) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date)).order_by(L_kredit.rechnr, L_lieferant.firma, L_kredit.rgdatum, L_kredit.zahlkonto).all():
        if l_kredit_obj_list.get(l_kredit._recid):
            continue
        else:
            l_kredit_obj_list[l_kredit._recid] = True

        age_list = query(age_list_data, filters=(lambda age_list: age_list.invoice == l_kredit.rechnr), first=True)

        if not age_list:
            age_list = Age_list()
            age_list_data.append(age_list)

            age_list.supplier = l_lieferant.firma + ", " + l_lieferant.anredefirma
            age_list.invoice = l_kredit.rechnr
            age_list.counter = l_kredit.counter
            age_list.datum = l_kredit.rgdatum
            pay_flag = False

        if l_kredit.zahlkonto == 0 and l_kredit.saldo > 0:

            bediener = get_cache (Bediener, {"nr": [(eq, l_kredit.bediener_nr)]})

            if bediener:
                age_list.user_init = bediener.userinit
            age_list.credit =  to_decimal(age_list.credit) + to_decimal(l_kredit.saldo)
            age_list.balance =  to_decimal(age_list.balance) + to_decimal(l_kredit.saldo)
            tot_credit =  to_decimal(tot_credit) + to_decimal(l_kredit.saldo)
            tot_balance =  to_decimal(tot_balance) + to_decimal(l_kredit.saldo)

        elif l_kredit.zahlkonto != 0 and l_kredit.saldo < 0:
            age_list.debit =  to_decimal(age_list.debit) + to_decimal(l_kredit.saldo)
            age_list.balance =  to_decimal(age_list.balance) + to_decimal(l_kredit.saldo)
            tot_debit =  to_decimal(tot_debit) + to_decimal(l_kredit.saldo)
            tot_balance =  to_decimal(tot_balance) + to_decimal(l_kredit.saldo)

        if input_paylist.excl_pay:

            b_kredit = db_session.query(B_kredit).filter(
                     (B_kredit.rechnr == age_list.invoice) & (B_kredit.counter == age_list.counter) & ((get_year(B_kredit.rgdatum) < get_year(from_date)) | ((get_year(B_kredit.rgdatum) == get_year(from_date)) & (get_month(B_kredit.rgdatum) < get_month(from_date))))).first()

            if b_kredit and b_kredit.zahlkonto != l_kredit.zahlkonto:

                if not pay_flag:

                    if l_kredit.saldo < 0:
                        tot_debit =  to_decimal(tot_debit) - to_decimal(l_kredit.saldo)
                        tot_balance =  to_decimal(tot_balance) - to_decimal(l_kredit.saldo)

                    elif l_kredit.saldo > 0:
                        tot_credit =  to_decimal(tot_credit) - to_decimal(l_kredit.saldo)
                        tot_balance =  to_decimal(tot_balance) - to_decimal(l_kredit.saldo)
                    pay_flag = True
                    age_list_data.remove(age_list)
                else:
                    pay_flag = False
                    age_list_data.remove(age_list)
    age_list = Age_list()
    age_list_data.append(age_list)

    age_list.supplier = "T O T A L "
    age_list.debit =  to_decimal(tot_debit)
    age_list.credit =  to_decimal(tot_credit)
    age_list.balance =  to_decimal(tot_balance)

    for age_list in query(age_list_data):
        pass

    return generate_output()