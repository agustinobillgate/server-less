from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Fbstat, H_umsatz, Htparam, Queasy, Hoteldpt, H_journal, H_bill, H_artikel, Artikel, H_cost

def nt_fbstat():
    bill_date:date = None
    belegung:int = 0
    i:int = 0
    curr_rechnr:int = 0
    curr_dept:int = 0
    shift:int = 0
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    cost:decimal = to_decimal("0.0")
    serv_taxable:bool = False
    fbstat = h_umsatz = htparam = queasy = hoteldpt = h_journal = h_bill = h_artikel = artikel = h_cost = None

    t_list = s_list = sbuff = tbuff = fbuff = hbuff = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "rechnr":int, "billno":int, "food":[decimal,4], "bev":[decimal,4], "other":[decimal,4], "f_cost":[decimal,4], "b_cost":[decimal,4], "o_cost":[decimal,4], "f_pax":[int,4], "b_pax":[int,4], "o_pax":[int,4], "gpax":[int,4], "wpax":[int,4], "beleg":int, "pay":decimal, "rmtrans":decimal, "compli":decimal, "coupon":decimal})
    s_list_list, S_list = create_model("S_list", {"shift":int, "ftime":int, "ttime":int})

    Sbuff = S_list
    sbuff_list = s_list_list

    Tbuff = T_list
    tbuff_list = t_list_list

    Fbuff = create_buffer("Fbuff",Fbstat)
    Hbuff = create_buffer("Hbuff",H_umsatz)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, belegung, i, curr_rechnr, curr_dept, shift, serv, vat, vat2, fact, netto, cost, serv_taxable, fbstat, h_umsatz, htparam, queasy, hoteldpt, h_journal, h_bill, h_artikel, artikel, h_cost
        nonlocal sbuff, tbuff, fbuff, hbuff


        nonlocal t_list, s_list, sbuff, tbuff, fbuff, hbuff
        nonlocal t_list_list, s_list_list

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 > 4)).first()

    if queasy:

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 5) & (Queasy.number3 >= 1) & (Queasy.number3 <= 4)).order_by(Queasy._recid).all():
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.shift = queasy.number3
        s_list.ftime = to_int(substring(to_string(queasy.number1, "9999") , 0, 2)) * 3600 +\
                to_int(substring(to_string(queasy.number1, "9999") , 2, 2)) * 60
        s_list.ttime = to_int(substring(to_string(queasy.number2, "9999") , 0, 2)) * 3600 +\
                to_int(substring(to_string(queasy.number2, "9999") , 2, 2)) * 60

        if s_list.ftime > s_list.ttime:
            sbuff = Sbuff()
            sbuff_list.append(sbuff)

            sbuff.shift = s_list.shift
            sbuff.ftime = 0
            sbuff.ttime = s_list.ttime
            s_list.ttime = 24 * 3600

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    curr_dept = 0
    curr_rechnr = 0

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 1)).order_by(Hoteldpt._recid).all():

        h_umsatz = db_session.query(H_umsatz).filter(
                 (H_umsatz.artnr == 0) & (H_umsatz.departement == hoteldpt.num) & (H_umsatz.betriebsnr == hoteldpt.num) & (H_umsatz.datum == bill_date)).first()

        if h_umsatz:

            hbuff = db_session.query(Hbuff).filter(
                     (Hbuff._recid == h_umsatz._recid)).first()
            hbuff.betrag =  to_decimal("0")
            hbuff.nettobetrag =  to_decimal("0")


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

                s_list = query(s_list_list, filters=(lambda s_list: s_list.h_journal.zeit >= s_list.ftime and h_journal.zeit <= s_list.ttime), first=True)

                if s_list and s_list.shift <= 4:
                    shift = s_list.shift
                else:
                    shift = 3

        t_list = query(t_list_list, filters=(lambda t_list: t_list.dept == h_journal.departement and t_list.rechnr == h_journal.rechnr and t_list.billno == h_journal.waehrungsnr), first=True)

        if not t_list:

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.rechnr == h_journal.rechnr) & (H_bill.departement == h_journal.departement)).first()
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.billno = h_journal.waehrungsnr
            t_list.dept = h_journal.departement
            t_list.rechnr = h_journal.rechnr
            t_list.beleg = h_bill.belegung

        if h_journal.artnr == 0:

            if re.match(r".*RmNo.*",h_journal.bezeich, re.IGNORECASE):
                t_list.rmtrans =  to_decimal(t_list.rmtrans) + to_decimal(h_journal.betrag)
            else:
                t_list.pay =  to_decimal(t_list.pay) + to_decimal(h_journal.betrag)
        else:

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.artnr == h_journal.artnr) & (H_artikel.departement == h_journal.departement)).first()

            if h_artikel.artart == 0:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                netto =  to_decimal(h_journal.betrag) / to_decimal(fact)
                cost =  to_decimal("0")

                h_cost = db_session.query(H_cost).filter(
                         (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == bill_date) & (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag)
                else:
                    cost =  to_decimal(netto) * to_decimal(h_artikel.prozent) / to_decimal("100")

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.departement == h_journal.departement) & (H_bill.rechnr == h_journal.rechnr)).first()

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

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

    for t_list in query(t_list_list, filters=(lambda t_list: t_list.billno > 0)):
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

    for t_list in query(t_list_list, filters=(lambda t_list: t_list.billno == 0)):
        for i in range(1,4 + 1) :

            if t_list.food[i - 1] != 0:
                belegung = t_list.beleg

                if t_list.food[i - 1] < 0 and belegung > 0:
                    belegung = - belegung

                for tbuff in query(tbuff_list, filters=(lambda tbuff: tbuff.rechnr == t_list.rechnr and tbuff.dept == t_list.dept and tbuff.billno > 0)):
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

                for tbuff in query(tbuff_list, filters=(lambda tbuff: tbuff.rechnr == t_list.rechnr and tbuff.dept == t_list.dept and tbuff.billno > 0)):
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

                for tbuff in query(tbuff_list, filters=(lambda tbuff: tbuff.rechnr == t_list.rechnr and tbuff.dept == t_list.dept and tbuff.billno > 0)):
                    belegung = belegung - tbuff.o_pax[i - 1]

                if t_list.other[i - 1] > 0 and belegung <= 0:
                    belegung = 1

                elif t_list.other[i - 1] < 0 and belegung >= 0:
                    belegung = -1
                t_list.o_pax[i - 1] = belegung

    for t_list in query(t_list_list):
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

    for t_list in query(t_list_list, filters=(lambda t_list: t_list.pay != 0 or t_list.rmTrans != 0)):

        h_umsatz = db_session.query(H_umsatz).filter(
                 (H_umsatz.artnr == 0) & (H_umsatz.departement == t_list.dept) & (H_umsatz.betriebsnr == t_list.dept) & (H_umsatz.datum == bill_date)).first()

        if not h_umsatz:
            h_umsatz = H_umsatz()
            db_session.add(h_umsatz)

            h_umsatz.artnr = 0
            h_umsatz.departement = t_list.dept
            h_umsatz.betriebsnr = t_list.dept
            h_umsatz.datum = bill_date

        fbstat = db_session.query(Fbstat).filter(
                 (Fbstat.datum == bill_date) & (Fbstat.departement == t_list.dept)).first()

        if not fbstat:
            fbstat = Fbstat()
            db_session.add(fbstat)

            fbstat.datum = bill_date
            fbstat.departement = t_list.dept

        fbuff = db_session.query(Fbuff).filter(
                 (Fbuff.datum == bill_date) & (Fbuff.departement == (t_list.dept + 100))).first()

        if not fbuff:
            fbuff = Fbuff()
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