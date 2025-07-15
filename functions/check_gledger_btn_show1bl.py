#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line, H_artikel, Artikel, Umsatz, Billjournal

def check_gledger_btn_show1bl(currdate:date):

    prepare_cache ([H_bill_line, H_artikel, Artikel, Umsatz, Billjournal])

    s = to_decimal("0.0")
    s1_list_data = []
    h_bill_line = h_artikel = artikel = umsatz = billjournal = None

    t1_list = s1_list = s1buff = None

    t1_list_data, T1_list = create_model("T1_list", {"dept":int, "rechnr":int, "pay":Decimal, "rmtrans":Decimal, "compli":Decimal, "coupon":Decimal})
    s1_list_data, S1_list = create_model("S1_list", {"flag":int, "nr":int, "artnr":int, "bezeich":string, "artart":int, "dept":int, "amt":Decimal, "ums":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s, s1_list_data, h_bill_line, h_artikel, artikel, umsatz, billjournal
        nonlocal currdate


        nonlocal t1_list, s1_list, s1buff
        nonlocal t1_list_data, s1_list_data

        return {"s": s, "s1-list": s1_list_data}

    def show_bill_vs_rev():

        nonlocal s, s1_list_data, h_bill_line, h_artikel, artikel, umsatz, billjournal
        nonlocal currdate


        nonlocal t1_list, s1_list, s1buff
        nonlocal t1_list_data, s1_list_data

        curr_i:int = 0
        curr_dept:int = 0
        tot_billamt:Decimal = to_decimal("0.0")
        tot_revamt:Decimal = to_decimal("0.0")
        S1buff = S1_list
        s1buff_data = s1_list_data
        s1_list_data.clear()
        t1_list_data.clear()

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.bill_datum == currdate)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.zeit).all():

            t1_list = query(t1_list_data, filters=(lambda t1_list: t1_list.rechnr == h_bill_line.rechnr and t1_list.dept == h_bill_line.departement), first=True)

            if not t1_list:
                t1_list = T1_list()
                t1_list_data.append(t1_list)

                t1_list.rechnr = h_bill_line.rechnr
                t1_list.dept = h_bill_line.departement

            if h_bill_line.artnr == 0:
                t1_list.rmtrans =  to_decimal(t1_list.rmtrans) + to_decimal(h_bill_line.betrag)
            else:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                if h_artikel.artart == 11:
                    t1_list.compli =  to_decimal(t1_list.compli) + to_decimal(h_bill_line.betrag)

                elif h_artikel.artart == 12:
                    t1_list.coupon =  to_decimal(t1_list.coupon) + to_decimal(h_bill_line.betrag)

                elif h_artikel.artart != 0:
                    t1_list.pay =  to_decimal(t1_list.pay) + to_decimal(h_bill_line.betrag)

        for t1_list in query(t1_list_data):

            if t1_list.pay != 0 or t1_list.rmtrans != 0:
                pass
            else:
                t1_list_data.remove(t1_list)

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.bill_datum == currdate) & (H_bill_line.artnr != 0)).order_by(H_bill_line._recid).all():

            t1_list = query(t1_list_data, filters=(lambda t1_list: t1_list.rechnr == h_bill_line.rechnr and t1_list.dept == h_bill_line.departement), first=True)

            if t1_list:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                if h_artikel.artart == 0:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                    s1_list = query(s1_list_data, filters=(lambda s1_list: s1_list.artnr == artikel.artnr and s1_list.dept == artikel.departement), first=True)

                    if not s1_list:
                        s1_list = S1_list()
                        s1_list_data.append(s1_list)

                        s1_list.artnr = artikel.artnr
                        s1_list.bezeich = artikel.bezeich
                        s1_list.dept = artikel.departement


                    s1_list.amt =  to_decimal(s1_list.amt) + to_decimal(h_bill_line.betrag)

                elif h_artikel.artart == 6 or h_artikel.artart == 5:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                    s1_list = query(s1_list_data, filters=(lambda s1_list: s1_list.artnr == artikel.artnr and s1_list.dept == 0), first=True)

                    if not s1_list:
                        s1_list = S1_list()
                        s1_list_data.append(s1_list)

                        s1_list.artnr = artikel.artnr
                        s1_list.dept = 0
                        s1_list.bezeich = artikel.bezeich
                        s1_list.artart = artikel.artart


                    s1_list.amt =  to_decimal(s1_list.amt) + to_decimal(h_bill_line.betrag)

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum == currdate)).order_by(Umsatz._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel and artikel.artart != 10:
                s =  to_decimal("0")

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.artnr == umsatz.artnr) & (Billjournal.departement == umsatz.departement) & (Billjournal.bill_datum == currdate) & (Billjournal.anzahl != 0)).order_by(Billjournal._recid).all():
                    s =  to_decimal(s) + to_decimal(billjournal.betrag)

                s1_list = query(s1_list_data, filters=(lambda s1_list: s1_list.artnr == umsatz.artnr and s1_list.dept == umsatz.departement), first=True)

                if not s1_list:

                    artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})
                    s1_list = S1_list()
                    s1_list_data.append(s1_list)

                    s1_list.artnr = artikel.artnr
                    s1_list.dept = artikel.departement
                    s1_list.bezeich = artikel.bezeich
                    s1_list.artart = artikel.artart


                s1_list.amt =  to_decimal(s1_list.amt) + to_decimal(s)
                s1_list.ums =  to_decimal(umsatz.betrag)

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.flag == 0), sort_by=[("dept",False),("artnr",False)]):
            curr_i = curr_i + 1

            if curr_i == 1:
                curr_dept = s1_list.dept

            if curr_dept != s1_list.dept:
                s1buff = S1buff()
                s1buff_data.append(s1buff)

                s1buff.flag = 1
                s1buff.nr = curr_i
                s1buff.dept = curr_dept
                s1buff.bezeich = "T O T A L"
                s1buff.amt =  to_decimal(tot_billamt)
                s1buff.ums =  to_decimal(tot_revamt)
                curr_dept = s1_list.dept
                curr_i = curr_i + 1
                s1_list.nr = curr_i
                tot_billamt =  to_decimal(s1_list.amt)
                tot_revamt =  to_decimal(s1_list.ums)


            else:
                tot_billamt =  to_decimal(tot_billamt) + to_decimal(s1_list.amt)
                tot_revamt =  to_decimal(tot_revamt) + to_decimal(s1_list.ums)
                s1_list.nr = curr_i


        s1buff = S1buff()
        s1buff_data.append(s1buff)

        s1buff.flag = 1
        s1buff.nr = curr_i
        s1buff.dept = curr_dept
        s1buff.bezeich = "T O T A L"
        s1buff.amt =  to_decimal(tot_billamt)
        s1buff.ums =  to_decimal(tot_revamt)
        curr_dept = curr_dept
        curr_i = curr_i + 1


    show_bill_vs_rev()

    return generate_output()