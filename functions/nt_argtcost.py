from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Queasy, H_artikel, H_bill_line, Artikel, H_cost, H_bill, Res_line, Argtcost

def nt_argtcost():
    bill_date:date = None
    shift:int = 0
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    cost:decimal = to_decimal("0.0")
    serv_taxable:bool = False
    do_it:bool = False
    htparam = queasy = h_artikel = h_bill_line = artikel = h_cost = h_bill = res_line = argtcost = None

    m_list = s_list = sbuff = None

    m_list_list, M_list = create_model("M_list", {"artnr":int, "dept":int, "rechnr":int, "betrag":decimal})
    s_list_list, S_list = create_model("S_list", {"shift":int, "ftime":int, "ttime":int})

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, shift, serv, vat, vat2, fact, netto, cost, serv_taxable, do_it, htparam, queasy, h_artikel, h_bill_line, artikel, h_cost, h_bill, res_line, argtcost
        nonlocal sbuff


        nonlocal m_list, s_list, sbuff
        nonlocal m_list_list, s_list_list

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

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

    h_bill_line_obj_list = []
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 12)).filter(
             (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line._recid).all():
        if h_bill_line._recid in h_bill_line_obj_list:
            continue
        else:
            h_bill_line_obj_list.append(h_bill_line._recid)

        m_list = query(m_list_list, filters=(lambda m_list: m_list.artnr == h_bill_line.artnr and m_list.dept == h_bill_line.departement and m_list.rechnr == h_bill_line.rechnr), first=True)

        if not m_list:
            m_list = M_list()
            m_list_list.append(m_list)

            m_list.artnr = h_bill_line.artnr
            m_list.dept = h_bill_line.departement
            m_list.rechnr = h_bill_line.rechnr


        m_list.betrag =  to_decimal(m_list.betrag) - to_decimal(h_bill_line.betrag)

    for m_list in query(m_list_list, filters=(lambda m_list: m_list.betrag == 0)):
        m_list_list.remove(m_list)

    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.bill_datum == bill_date) & (H_bill_line.artnr != 0)).order_by(H_bill_line.departement, H_bill_line.rechnr, H_bill_line.zeit).all():

        m_list = query(m_list_list, filters=(lambda m_list: m_list.dept == h_bill_line.departement and m_list.rechnr == h_bill_line.rechnr), first=True)
        do_it = None != m_list

        if do_it:
            shift = h_bill_line.betriebsnr

            if shift == 0:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.h_bill_line.zeit >= s_list.ftime and h_bill_line.zeit <= s_list.ttime), first=True)

                if s_list and s_list.shift <= 4:
                    shift = s_list.shift
                else:
                    shift = 3

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.artnr == h_bill_line.artnr) & (H_artikel.departement == h_bill_line.departement)).first()

            if h_artikel.artart == 0:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                netto =  to_decimal(h_bill_line.betrag) / to_decimal(fact)
                cost =  to_decimal("0")

                h_cost = db_session.query(H_cost).filter(
                         (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == bill_date) & (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_bill_line.anzahl) * to_decimal(h_cost.betrag)
                else:
                    cost =  to_decimal(netto) * to_decimal(h_artikel.prozent) / to_decimal("100")

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.departement == h_bill_line.departement) & (H_bill.rechnr == h_bill_line.rechnr)).first()
                pass

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

                if res_line:

                    argtcost = db_session.query(Argtcost).filter(
                             (Argtcost.datum == bill_date) & (Argtcost.gastnrmember == res_line.gastnrmember) & (Argtcost.zinr == res_line.zinr) & (Argtcost.artnr == h_bill_line.artnr) & (Argtcost.departement == h_bill_line.departement) & (Argtcost.mealcoupon == m_list.artnr) & (Argtcost.shift == shift)).first()
                else:

                    argtcost = db_session.query(Argtcost).filter(
                             (Argtcost.datum == bill_date) & (Argtcost.gastnrmember == 0) & (Argtcost.zinr == "") & (Argtcost.artnr == h_bill_line.artnr) & (Argtcost.departement == h_bill_line.departement) & (Argtcost.mealcoupon == m_list.artnr) & (Argtcost.shift == shift)).first()

                if not argtcost:
                    argtcost = Argtcost()
                    db_session.add(argtcost)

                    argtcost.datum = bill_date
                    argtcost.artnr = h_bill_line.artnr
                    argtcost.departement = h_bill_line.departement
                    argtcost.mealcoupon = m_list.artnr
                    argtcost.shift = shift

                    if res_line:
                        argtcost.gastnrmember = res_line.gastnrmember
                        argtcost.zinr = res_line.zinr

                    if artikel:
                        argtcost.artnrfront = artikel.artnr
                argtcost.anzahl = argtcost.anzahl + h_bill_line.anzahl
                argtcost.costbetrag =  to_decimal(argtcost.costbetrag) + to_decimal(cost)
                argtcost.nettobetrag =  to_decimal(argtcost.nettobetrag) + to_decimal(netto)

    return generate_output()