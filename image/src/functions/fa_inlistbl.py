from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, Mathis, Fa_op

def fa_inlistbl(lief_nr:int, docu_nr:str, from_date:date, to_date:date):
    t_firma = ""
    output_list_list = []
    l_lieferant = mathis = fa_op = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"datum":date, "nr":int, "name":str, "anzahl":int, "einzelpreis":decimal, "warenwert":decimal, "lscheinnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_firma, output_list_list, l_lieferant, mathis, fa_op


        nonlocal output_list
        nonlocal output_list_list
        return {"t_firma": t_firma, "output-list": output_list_list}

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    t_firma = l_lieferant.firma

    fa_op_obj_list = []
    for fa_op, mathis in db_session.query(Fa_op, Mathis).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
            (Fa_op.datum >= from_date) &  (Fa_op.datum <= to_date) &  (Fa_op.loeschflag == 0) &  (Fa_op.lief_nr == lief_nr) &  (func.lower(Fa_op.(docu_nr).lower()) == (docu_nr).lower())).all():
        if fa_op._recid in fa_op_obj_list:
            continue
        else:
            fa_op_obj_list.append(fa_op._recid)


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.datum = fa_op.datum
        output_list.nr = mathis.nr
        output_list.name = mathis.name
        output_list.anzahl = fa_op.anzahl
        output_list.einzelpreis = fa_op.einzelpreis
        output_list.warenwert = fa_op.warenwert
        output_list.lscheinnr = fa_op.lscheinnr

    return generate_output()