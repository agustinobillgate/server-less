from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_lieferant, Mathis, Fa_op

def prepare_fa_stockinbl(ponum:str):
    price_decimal = 0
    billdate = None
    heute = None
    todate = None
    beg_date = None
    q2_list_list = []
    htparam = l_lieferant = mathis = fa_op = None

    q2_list = None

    q2_list_list, Q2_list = create_model("Q2_list", {"lscheinnr":str, "name":str, "location":str, "einzelpreis":decimal, "anzahl":int, "warenwert":decimal, "firma":str, "datum":date, "docu_nr":str, "lief_nr":int, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, billdate, heute, todate, beg_date, q2_list_list, htparam, l_lieferant, mathis, fa_op


        nonlocal q2_list
        nonlocal q2_list_list
        return {"price_decimal": price_decimal, "billdate": billdate, "heute": heute, "todate": todate, "beg_date": beg_date, "q2-list": q2_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate
    heute = billdate
    todate = billdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    beg_date = date_mdy(get_month(fdate) , 1, get_year(fdate))

    if ponum == "":

        fa_op_obj_list = []
        for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                (Fa_op.opart == 1) &  (func.lower(Fa_op.lscheinnr) >= (ponum).lower()) &  (Fa_op.datum >= billdate) &  (Fa_op.datum <= todate) &  (Fa_op.loeschflag <= 1)).all():
            if fa_op._recid in fa_op_obj_list:
                continue
            else:
                fa_op_obj_list.append(fa_op._recid)


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.lscheinnr = fa_op.lscheinnr
            q2_list.name = mathis.name
            q2_list.location = mathis.location
            q2_list.einzelpreis = fa_op.einzelpreis
            q2_list.anzahl = fa_op.anzahl
            q2_list.warenwert = fa_op.warenwert
            q2_list.firma = l_lieferant.firma
            q2_list.datum = fa_op.datum
            q2_list.docu_nr = fa_op.docu_nr
            q2_list.lief_nr = fa_op.lief_nr
            q2_list.rec_id = fa_op._recid


    else:

        fa_op_obj_list = []
        for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                (Fa_op.opart == 1) &  (func.lower(Fa_op.lscheinnr) == (ponum).lower()) &  (Fa_op.datum >= billdate) &  (Fa_op.datum <= todate) &  (Fa_op.loeschflag <= 1)).all():
            if fa_op._recid in fa_op_obj_list:
                continue
            else:
                fa_op_obj_list.append(fa_op._recid)


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.lscheinnr = fa_op.lscheinnr
            q2_list.name = mathis.name
            q2_list.location = mathis.location
            q2_list.einzelpreis = fa_op.einzelpreis
            q2_list.anzahl = fa_op.anzahl
            q2_list.warenwert = fa_op.warenwert
            q2_list.firma = l_lieferant.firma
            q2_list.datum = fa_op.datum
            q2_list.docu_nr = fa_op.docu_nr
            q2_list.lief_nr = fa_op.lief_nr
            q2_list.rec_id = fa_op._recid

    return generate_output()