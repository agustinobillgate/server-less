#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 21-10-2025 
# Issue : New compile program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Fbstat, H_umsatz, H_journal, H_artikel, Htparam, Queasy, Hoteldpt, H_bill, Artikel, H_cost

def nt_fbstat():

    prepare_cache ([Fbstat, H_umsatz, H_journal, H_artikel, Htparam, Queasy, Hoteldpt, H_bill, Artikel, H_cost])

    bill_date:date = None
    belegung:int = 0
    i:int = 0
    curr_rechnr:int = 0
    curr_dept:int = 0
    shift:int = 0
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    cost:Decimal = to_decimal("0.0")
    serv_taxable:bool = False
    found_compli:bool = False
    fbstat = h_umsatz = h_journal = h_artikel = htparam = queasy = hoteldpt = h_bill = artikel = h_cost = None

    t_list = s_list = sbuff = tbuff = fbuff = hbuff = buf_hjourn = buf_hart = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "rechnr":int, "billno":int, "food":[Decimal,4], "bev":[Decimal,4], "other":[Decimal,4], "f_cost":[Decimal,4], "b_cost":[Decimal,4], "o_cost":[Decimal,4], "f_pax":[int,4], "b_pax":[int,4], "o_pax":[int,4], "gpax":[int,4], "wpax":[int,4], "beleg":int, "pay":Decimal, "rmtrans":Decimal, "compli":Decimal, "coupon":Decimal})
    s_list_data, S_list = create_model("S_list", {"shift":int, "ftime":int, "ttime":int})

    Sbuff = S_list
    sbuff_data = s_list_data

    Tbuff = T_list
    tbuff_data = t_list_data

    Fbuff = create_buffer("Fbuff",Fbstat)
    Hbuff = create_buffer("Hbuff",H_umsatz)
    Buf_hjourn = create_buffer("Buf_hjourn",H_journal)
    Buf_hart = create_buffer("Buf_hart",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, belegung, i, curr_rechnr, curr_dept, shift, serv, vat, vat2, fact, netto, cost, serv_taxable, found_compli, fbstat, h_umsatz, h_journal, h_artikel, htparam, queasy, hoteldpt, h_bill, artikel, h_cost
        nonlocal sbuff, tbuff, fbuff, hbuff, buf_hjourn, buf_hart


        nonlocal t_list, s_list, sbuff, tbuff, fbuff, hbuff, buf_hjourn, buf_hart
        nonlocal t_list_data, s_list_data

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_taxable = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 5)],"number3": [(gt, 4)]})

    if queasy:

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 >= 1) & (Queasy.number3 <= 4)).order_by(Queasy._recid).all():
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.shift = queasy.number3
        s_list.ftime = to_int(substring(to_string(queasy.number1, "9999") , 0, 2)) * 3600 +\
                to_int(substring(to_string(queasy.number1, "9999") , 2, 2)) * 60
        s_list.ttime = to_int(substring(to_string(queasy.number2, "9999") , 0, 2)) * 3600 +\
                to_int(substring(to_string(queasy.number2, "9999") , 2, 2)) * 60

        if s_list.ftime > s_list.ttime:
            sbuff = Sbuff()
            sbuff_data.append(sbuff)

            sbuff.shift = s_list.shift
            sbuff.ftime = 0
            sbuff.ttime = s_list.ttime
            s_list.ttime = 24 * 3600


    curr_dept = 0
    curr_rechnr = 0

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1)).order_by(Hoteldpt._recid).all():

        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, hoteldpt.num)],"betriebsnr": [(eq, hoteldpt.num)],"datum": [(eq, bill_date)]})

        if h_umsatz:

            hbuff = get_cache (H_umsatz, {"_recid": [(eq, h_umsatz._recid)]})
            hbuff.betrag =  to_decimal("0")
            hbuff.nettobetrag =  to_decimal("0")


            pass
            pass

    for h_journal in db_session.query(H_journal).filter(
             (H_journal.bill_datum == bill_date)).order_by(H_journal.departement, H_journal.rechnr, H_journal.zeit).all():

        if curr_dept != h_journal.departement:
            curr_dept = h_journal.departement
            curr_rechnr = 0

        if curr_rechnr != h_journal.rechnr:
            curr_rechnr = h_journal.rechnr
            shift = h_journal.betriebsnr

            if shift == 0:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.h_journal.zeit >= s_list.ftime and h_journal.zeit <= s_list.ttime), first=True)

                if s_list and s_list.shift <= 4:
                    shift = s_list.shift
                else:
                    shift = 3

        t_list = query(t_list_data, filters=(lambda t_list: t_list.dept == h_journal.departement and t_list.rechnr == h_journal.rechnr and t_list.billno == h_journal.waehrungsnr), first=True)

        if not t_list:

            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.billno = h_journal.waehrungsnr
            t_list.dept = h_journal.departement
            t_list.rechnr = h_journal.rechnr
            t_list.beleg = h_bill.belegung

        if h_journal.artnr == 0:

            if matches(h_journal.bezeich,r"*RmNo*"):
                t_list.rmtrans =  to_decimal(t_list.rmtrans) + to_decimal(h_journal.betrag)
            else:
                t_list.pay =  to_decimal(t_list.pay) + to_decimal(h_journal.betrag)
        else:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)]})

            if h_artikel.artart == 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                netto =  to_decimal(h_journal.betrag) / to_decimal(fact)
                found_compli = False

                buf_hjourn_obj_list = {}
                buf_hjourn = H_journal()
                buf_hart = H_artikel()
                for buf_hjourn.departement, buf_hjourn.rechnr, buf_hjourn.betriebsnr, buf_hjourn.zeit, buf_hjourn.waehrungsnr, buf_hjourn.betrag, buf_hjourn.artnr, buf_hjourn.bill_datum, buf_hjourn.anzahl, buf_hjourn._recid, buf_hart.artnrfront, buf_hart.departement, buf_hart.artnr, buf_hart.artart, buf_hart._recid in db_session.query(Buf_hjourn.departement, Buf_hjourn.rechnr, Buf_hjourn.betriebsnr, Buf_hjourn.zeit, Buf_hjourn.waehrungsnr, Buf_hjourn.betrag, Buf_hjourn.artnr, Buf_hjourn.bill_datum, Buf_hjourn.anzahl, Buf_hjourn._recid, Buf_hart.artnrfront, Buf_hart.departement, Buf_hart.artnr, Buf_hart.artart, Buf_hart._recid).join(Buf_hart,(Buf_hart.artnr == Buf_hjourn.artnr) & (Buf_hart.departement == Buf_hjourn.departement) & ((Buf_hart.artart == 11) | (Buf_hart.artart == 12))).filter(
                         (Buf_hjourn.rechnr == h_journal.rechnr) & (Buf_hjourn.departement == h_journal.departement) & (Buf_hjourn.bill_datum == h_journal.bill_datum)).order_by(Buf_hjourn.zeit.desc()).all():
                    if buf_hjourn_obj_list.get(buf_hjourn._recid):
                        continue
                    else:
                        buf_hjourn_obj_list[buf_hjourn._recid] = True


                    found_compli = True
                    break

                if not found_compli:
                    t_list.pay =  to_decimal(t_list.pay) + to_decimal(netto)
                cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, bill_date)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag)
                    cost = to_decimal(round(cost , 2))

                h_bill = get_cache (H_bill, {"departement": [(eq, h_journal.departement)],"rechnr": [(eq, h_journal.rechnr)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel:

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        t_list.food[shift - 1] = t_list.food[shift - 1] + netto
                        t_list.f_cost[shift - 1] = t_list.f_cost[shift - 1] + cost

                    elif artikel.umsatzart == 6:
                        t_list.bev[shift - 1] = t_list.bev[shift - 1] + netto
                        t_list.b_cost[shift - 1] = t_list.b_cost[shift - 1] + cost

                    elif artikel.umsatzart == 4:
                        t_list.other[shift - 1] = t_list.other[shift - 1] + netto
                        t_list.o_cost[shift - 1] = t_list.o_cost[shift - 1] + cost


            else:

                if h_artikel.artart <= 7:
                    t_list.pay =  to_decimal(t_list.pay) + to_decimal(netto)

                elif h_artikel.artart == 11:
                    t_list.compli =  to_decimal(t_list.compli) + to_decimal(netto)

                elif h_artikel.artart == 12:
                    t_list.coupon =  to_decimal(t_list.coupon) + to_decimal(netto)

    for t_list in query(t_list_data, filters=(lambda t_list: t_list.billno > 0)):
        for i in range(1,4 + 1) :

            if t_list.food[i - 1] != 0 and t_list.beleg > 0:
                t_list.f_pax[i - 1] = 1

            elif t_list.food[i - 1] != 0 and t_list.beleg < 0:
                t_list.f_pax[i - 1] = -1

            if t_list.bev[i - 1] != 0 and t_list.beleg > 0:
                t_list.b_pax[i - 1] = 1

            elif t_list.bev[i - 1] != 0 and t_list.beleg < 0:
                t_list.b_pax[i - 1] = -1

            if t_list.other[i - 1] != 0 and t_list.beleg > 0:
                t_list.o_pax[i - 1] = 1

            elif t_list.other[i - 1] != 0 and t_list.beleg < 0:
                t_list.o_pax[i - 1] = -1

    for t_list in query(t_list_data, filters=(lambda t_list: t_list.billno == 0)):
        for i in range(1,4 + 1) :

            if t_list.food[i - 1] != 0:
                belegung = t_list.beleg

                if t_list.food[i - 1] < 0 and belegung > 0:
                    belegung = - belegung

                for tbuff in query(tbuff_data, filters=(lambda tbuff: tbuff.rechnr == t_list.rechnr and tbuff.dept == t_list.dept and tbuff.billno > 0)):
                    belegung = belegung - tbuff.f_pax[i - 1]

                if t_list.food[i - 1] > 0 and belegung <= 0:
                    belegung = 1

                elif t_list.food[i - 1] < 0 and belegung >= 0:
                    belegung = -1
                t_list.f_pax[i - 1] = belegung

            if t_list.bev[i - 1] != 0:
                belegung = t_list.beleg

                if t_list.bev[i - 1] < 0 and belegung > 0:
                    belegung = - belegung

                for tbuff in query(tbuff_data, filters=(lambda tbuff: tbuff.rechnr == t_list.rechnr and tbuff.dept == t_list.dept and tbuff.billno > 0)):
                    belegung = belegung - tbuff.b_pax[i - 1]

                if t_list.bev[i - 1] > 0 and belegung <= 0:
                    belegung = 1

                elif t_list.bev[i - 1] < 0 and belegung >= 0:
                    belegung = -1
                t_list.b_pax[i - 1] = belegung

            if t_list.other[i - 1] != 0:
                belegung = t_list.beleg

                if t_list.other[i - 1] < 0 and belegung > 0:
                    belegung = - belegung

                for tbuff in query(tbuff_data, filters=(lambda tbuff: tbuff.rechnr == t_list.rechnr and tbuff.dept == t_list.dept and tbuff.billno > 0)):
                    belegung = belegung - tbuff.o_pax[i - 1]

                if t_list.other[i - 1] > 0 and belegung <= 0:
                    belegung = 1

                elif t_list.other[i - 1] < 0 and belegung >= 0:
                    belegung = -1
                t_list.o_pax[i - 1] = belegung

    for t_list in query(t_list_data):
        for i in range(1,4 + 1) :

            if t_list.rmTrans != 0:

                if t_list.f_pax[i - 1] != 0:
                    t_list.gpax[i - 1] = t_list.f_pax[i - 1]

                elif t_list.b_pax[i - 1] != 0:
                    t_list.gpax[i - 1] = t_list.b_pax[i - 1]

                elif t_list.o_pax[i - 1] != 0:
                    t_list.gpax[i - 1] = t_list.o_pax[i - 1]

            elif t_list.pay != 0:

                if t_list.f_pax[i - 1] != 0:
                    t_list.wpax[i - 1] = t_list.f_pax[i - 1]

                elif t_list.b_pax[i - 1] != 0:
                    t_list.wpax[i - 1] = t_list.b_pax[i - 1]

                elif t_list.o_pax[i - 1] != 0:
                    t_list.wpax[i - 1] = t_list.o_pax[i - 1]

    for t_list in query(t_list_data, filters=(lambda t_list: t_list.pay != 0 or t_list.rmTrans != 0)):

        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, 0)],"departement": [(eq, t_list.dept)],"betriebsnr": [(eq, t_list.dept)],"datum": [(eq, bill_date)]})

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = 0
            h_umsatz.departement = t_list.dept
            h_umsatz.betriebsnr = t_list.dept
            h_umsatz.datum = bill_date

        fbstat = get_cache (Fbstat, {"datum": [(eq, bill_date)],"departement": [(eq, t_list.dept)]})

        if not fbstat:
            fbstat = Fbstat()
            db_session.add(fbstat)

            fbstat.datum = bill_date
            fbstat.departement = t_list.dept

        fbuff = get_cache (Fbstat, {"datum": [(eq, bill_date)],"departement": [(eq, (t_list.dept + 100))]})

        if not fbuff:
            fbuff = Fbstat()
            db_session.add(fbuff)

            fbuff.datum = bill_date
            fbuff.departement = t_list.dept + 100

        if t_list.rmTrans != 0:
            for i in range(1,4 + 1) :
                fbstat.food_grev[i - 1] = fbstat.food_grev[i - 1] + t_list.food[i - 1]
                fbstat.bev_grev[i - 1] = fbstat.bev_grev[i - 1] + t_list.bev[i - 1]
                fbstat.other_grev[i - 1] = fbstat.other_grev[i - 1] + t_list.other[i - 1]
                fbstat.food_gcost[i - 1] = fbstat.food_gcost[i - 1] + t_list.f_cost[i - 1]
                fbstat.bev_gcost[i - 1] = fbstat.bev_gcost[i - 1] + t_list.b_cost[i - 1]
                fbstat.other_gcost[i - 1] = fbstat.other_gcost[i - 1] + t_list.o_cost[i - 1]
                fbstat.food_gpax[i - 1] = fbstat.food_gpax[i - 1] + t_list.f_pax[i - 1]
                fbstat.bev_gpax[i - 1] = fbstat.bev_gpax[i - 1] + t_list.b_pax[i - 1]
                fbstat.other_gpax[i - 1] = fbstat.other_gpax[i - 1] + t_list.o_pax[i - 1]
                h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(t_list.f_pax[i - 1])
                h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(t_list.b_pax[i - 1])

        elif t_list.pay != 0:
            for i in range(1,4 + 1) :
                fbstat.food_wrev[i - 1] = fbstat.food_wrev[i - 1] + t_list.food[i - 1]
                fbstat.bev_wrev[i - 1] = fbstat.bev_wrev[i - 1] + t_list.bev[i - 1]
                fbstat.other_wrev[i - 1] = fbstat.other_wrev[i - 1] + t_list.other[i - 1]
                fbstat.food_wcost[i - 1] = fbstat.food_wcost[i - 1] + t_list.f_cost[i - 1]
                fbstat.bev_wcost[i - 1] = fbstat.bev_wcost[i - 1] + t_list.b_cost[i - 1]
                fbstat.other_wcost[i - 1] = fbstat.other_wcost[i - 1] + t_list.o_cost[i - 1]
                fbstat.food_wpax[i - 1] = fbstat.food_wpax[i - 1] + t_list.f_pax[i - 1]
                fbstat.bev_wpax[i - 1] = fbstat.bev_wpax[i - 1] + t_list.b_pax[i - 1]
                fbstat.other_wpax[i - 1] = fbstat.other_wpax[i - 1] + t_list.o_pax[i - 1]
                h_umsatz.betrag =  to_decimal(h_umsatz.betrag) + to_decimal(t_list.f_pax[i - 1])
                h_umsatz.nettobetrag =  to_decimal(h_umsatz.nettobetrag) + to_decimal(t_list.b_pax[i - 1])


        for i in range(1,4 + 1) :
            fbuff.food_gpax[i - 1] = fbuff.food_gpax[i - 1] + t_list.gpax[i - 1]
            fbuff.food_wpax[i - 1] = fbuff.food_wpax[i - 1] + t_list.wpax[i - 1]

    return generate_output()