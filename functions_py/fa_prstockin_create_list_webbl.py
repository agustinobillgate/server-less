#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 28/7/2025
# if available
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Mathis, Fa_op

def fa_prstockin_create_list_webbl(lief_nr:int, to_date:date, docu_nr:string):

    prepare_cache ([L_lieferant, Mathis, Fa_op])

    firma = ""
    str_list_data = []
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    d_purchase:bool = False
    l_lieferant = mathis = fa_op = None

    str_list = None

    str_list_data, Str_list = create_model("Str_list", {"qty":Decimal, "warenwert":Decimal, "bezeich":string, "price":Decimal, "lscheinnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal firma, str_list_data, tot_anz, tot_amount, d_purchase, l_lieferant, mathis, fa_op
        nonlocal lief_nr, to_date, docu_nr


        nonlocal str_list
        nonlocal str_list_data

        return {"firma": firma, "str-list": str_list_data}

    def create_list():

        nonlocal firma, str_list_data, tot_anz, tot_amount, d_purchase, l_lieferant, mathis, fa_op
        nonlocal lief_nr, to_date, docu_nr


        nonlocal str_list
        nonlocal str_list_data

        i:int = 0
        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")
        i = 0
        d_purchase = False
        firma = l_lieferant.firma

        fa_op_obj_list = {}
        fa_op = Fa_op()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.anzahl, fa_op.warenwert, fa_op.einzelpreis, fa_op.docu_nr, fa_op._recid, mathis.name, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.anzahl, Fa_op.warenwert, Fa_op.einzelpreis, Fa_op.docu_nr, Fa_op._recid, Mathis.name, Mathis._recid).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.datum == to_date) & (Fa_op.lief_nr == lief_nr) & (Fa_op.loeschflag <= 1) & (Fa_op.anzahl != 0) & (Fa_op.lscheinnr == (docu_nr).lower())).order_by(Mathis.name).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            i = i + 1

            if fa_op.docu_nr == fa_op.lscheinnr:
                d_purchase = True
            tot_anz =  to_decimal(tot_anz) + to_decimal(fa_op.anzahl)
            tot_amount =  to_decimal(tot_amount) + to_decimal(fa_op.warenwert)
            str_list = Str_list()
            str_list_data.append(str_list)

            str_list.qty =  to_decimal(fa_op.anzahl)
            str_list.warenwert =  to_decimal(fa_op.warenwert)
            str_list.bezeich = mathis.name
            str_list.price =  to_decimal(fa_op.einzelpreis)
            str_list.lscheinnr = fa_op.lscheinnr


        str_list = Str_list()
        str_list_data.append(str_list)

        str_list.bezeich = "T O T A L"
        str_list.qty =  to_decimal(tot_anz)
        str_list.warenwert =  to_decimal(tot_amount)


    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    # Rd 28/7/2025
    # if available
    if l_lieferant:
        create_list()

    return generate_output()