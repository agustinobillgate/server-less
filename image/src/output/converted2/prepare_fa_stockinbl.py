#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lieferant, Mathis, Fa_op

def prepare_fa_stockinbl(ponum:string):

    prepare_cache ([Htparam, L_lieferant, Mathis, Fa_op])

    price_decimal = 0
    billdate = None
    heute = None
    todate = None
    beg_date = None
    q2_list_list = []
    htparam = l_lieferant = mathis = fa_op = None

    q2_list = None

    q2_list_list, Q2_list = create_model("Q2_list", {"lscheinnr":string, "name":string, "location":string, "einzelpreis":Decimal, "anzahl":int, "warenwert":Decimal, "firma":string, "datum":date, "docu_nr":string, "lief_nr":int, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, billdate, heute, todate, beg_date, q2_list_list, htparam, l_lieferant, mathis, fa_op
        nonlocal ponum


        nonlocal q2_list
        nonlocal q2_list_list

        return {"price_decimal": price_decimal, "billdate": billdate, "heute": heute, "todate": todate, "beg_date": beg_date, "q2-list": q2_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate
    heute = billdate
    todate = billdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    beg_date = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate))

    if ponum == "":

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.docu_nr, fa_op.lief_nr, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.docu_nr, Fa_op.lief_nr, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.opart == 1) & (Fa_op.lscheinnr >= (ponum).lower()) & (Fa_op.datum >= billdate) & (Fa_op.datum <= todate) & (Fa_op.loeschflag <= 1)).order_by(Fa_op.datum, Fa_op.docu_nr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.lscheinnr = fa_op.lscheinnr
            q2_list.name = mathis.name
            q2_list.location = mathis.location
            q2_list.einzelpreis =  to_decimal(fa_op.einzelpreis)
            q2_list.anzahl = fa_op.anzahl
            q2_list.warenwert =  to_decimal(fa_op.warenwert)
            q2_list.firma = l_lieferant.firma
            q2_list.datum = fa_op.datum
            q2_list.docu_nr = fa_op.docu_nr
            q2_list.lief_nr = fa_op.lief_nr
            q2_list.rec_id = fa_op._recid


    else:

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.docu_nr, fa_op.lief_nr, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.docu_nr, Fa_op.lief_nr, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.opart == 1) & (Fa_op.lscheinnr == (ponum).lower()) & (Fa_op.datum >= billdate) & (Fa_op.datum <= todate) & (Fa_op.loeschflag <= 1)).order_by(Fa_op.datum, Fa_op.docu_nr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.lscheinnr = fa_op.lscheinnr
            q2_list.name = mathis.name
            q2_list.location = mathis.location
            q2_list.einzelpreis =  to_decimal(fa_op.einzelpreis)
            q2_list.anzahl = fa_op.anzahl
            q2_list.warenwert =  to_decimal(fa_op.warenwert)
            q2_list.firma = l_lieferant.firma
            q2_list.datum = fa_op.datum
            q2_list.docu_nr = fa_op.docu_nr
            q2_list.lief_nr = fa_op.lief_nr
            q2_list.rec_id = fa_op._recid

    return generate_output()