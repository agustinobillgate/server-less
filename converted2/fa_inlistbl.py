#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Mathis, Fa_op

def fa_inlistbl(lief_nr:int, docu_nr:string, from_date:date, to_date:date):

    prepare_cache ([L_lieferant, Mathis, Fa_op])

    t_firma = ""
    output_list_data = []
    l_lieferant = mathis = fa_op = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"datum":date, "nr":int, "name":string, "anzahl":int, "einzelpreis":Decimal, "warenwert":Decimal, "lscheinnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_firma, output_list_data, l_lieferant, mathis, fa_op
        nonlocal lief_nr, docu_nr, from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        return {"t_firma": t_firma, "output-list": output_list_data}

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    t_firma = l_lieferant.firma

    fa_op_obj_list = {}
    fa_op = Fa_op()
    mathis = Mathis()
    for fa_op.datum, fa_op.anzahl, fa_op.einzelpreis, fa_op.warenwert, fa_op.lscheinnr, fa_op._recid, mathis.nr, mathis.name, mathis._recid in db_session.query(Fa_op.datum, Fa_op.anzahl, Fa_op.einzelpreis, Fa_op.warenwert, Fa_op.lscheinnr, Fa_op._recid, Mathis.nr, Mathis.name, Mathis._recid).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
             (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date) & (Fa_op.loeschflag == 0) & (Fa_op.lief_nr == lief_nr) & (Fa_op.docu_nr == (docu_nr).lower())).order_by(Fa_op.datum, Fa_op.nr).all():
        if fa_op_obj_list.get(fa_op._recid):
            continue
        else:
            fa_op_obj_list[fa_op._recid] = True


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.datum = fa_op.datum
        output_list.nr = mathis.nr
        output_list.name = mathis.name
        output_list.anzahl = fa_op.anzahl
        output_list.einzelpreis =  to_decimal(fa_op.einzelpreis)
        output_list.warenwert =  to_decimal(fa_op.warenwert)
        output_list.lscheinnr = fa_op.lscheinnr

    return generate_output()