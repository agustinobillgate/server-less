#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_lager, L_artikel, L_op, L_ophis

def stock_transformlist_create_listbl(from_date:date, to_date:date, from_art:int, to_art:int):

    prepare_cache ([Htparam, L_lager, L_artikel, L_op, L_ophis])

    it_exist = False
    t_list_data = []
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_op = l_ophis = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"datum":date, "lscheinnr":string, "f_bezeich":string, "t_bezeich":string, "artnr":string, "bezeich":string, "einheit":string, "content":Decimal, "price":string, "qty":Decimal, "s_qty":string, "op_art":int, "val":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_data, long_digit, htparam, l_lager, l_artikel, l_op, l_ophis
        nonlocal from_date, to_date, from_art, to_art


        nonlocal t_list
        nonlocal t_list_data

        return {"it_exist": it_exist, "t-list": t_list_data}

    def create_list():

        nonlocal it_exist, t_list_data, long_digit, htparam, l_lager, l_artikel, l_op, l_ophis
        nonlocal from_date, to_date, from_art, to_art


        nonlocal t_list
        nonlocal t_list_data

        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        it_exist = False
        t_list_data.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        lscheinnr = ""

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.op_art, l_op._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.op_art, L_op._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art >= 2) & (L_op.op_art <= 4) & (L_op.herkunftflag == 3) & (L_op.loeschflag <= 1)).order_by(L_op.datum, L_op.lscheinnr, L_op.op_art, L_op.zeit).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            it_exist = True

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

            l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

            if lscheinnr != l_op.lscheinnr and qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.price = "Total"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                qty =  to_decimal("0")
                val =  to_decimal("0")
            lscheinnr = l_op.lscheinnr
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.datum = l_op.datum
            t_list.lscheinnr = lscheinnr
            t_list.f_bezeich = l_lager.bezeich

            if l_store:
                t_list.t_bezeich = l_store.bezeich
            t_list.artnr = to_string(l_op.artnr, "9999999")
            t_list.bezeich = l_artikel.bezeich
            t_list.einheit = l_artikel.masseinheit
            t_list.content =  to_decimal(l_artikel.inhalt)

            if l_op.anzahl != 0:

                if not long_digit:
                    t_list.price = to_string((l_op.warenwert / l_op.anzahl) , "->>,>>>,>>9.99")
                else:
                    t_list.price = to_string((l_op.warenwert / l_op.anzahl) , "->,>>>,>>>,>>9")
            t_list.qty =  to_decimal(l_op.anzahl)
            t_list.val =  to_decimal(l_op.warenwert)
            t_list.s_qty = to_string(t_list.qty, "->>>,>>9.999")
            t_list.op_art = l_op.op_art

            if l_op.op_art == 2:
                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)

        l_ophis_obj_list = {}
        l_ophis = L_ophis()
        l_artikel = L_artikel()
        for l_ophis.lager_nr, l_ophis.lscheinnr, l_ophis.datum, l_ophis.artnr, l_ophis.warenwert, l_ophis.anzahl, l_ophis.op_art, l_ophis._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid in db_session.query(L_ophis.lager_nr, L_ophis.lscheinnr, L_ophis.datum, L_ophis.artnr, L_ophis.warenwert, L_ophis.anzahl, L_ophis.op_art, L_ophis._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                 (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr >= from_art) & (L_ophis.artnr <= to_art) & (L_ophis.op_art >= 2) & (L_ophis.op_art <= 4) & (not_(matches(L_ophis.fibukonto,"*CANCELLED*")))).order_by(L_ophis.datum, L_ophis.lscheinnr, L_ophis.op_art).all():
            if l_ophis_obj_list.get(l_ophis._recid):
                continue
            else:
                l_ophis_obj_list[l_ophis._recid] = True

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_ophis.lager_nr)]})
            it_exist = False

            if lscheinnr != l_ophis.lscheinnr and qty != 0:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.price = "Total"
                t_list.qty =  to_decimal(qty)
                t_list.val =  to_decimal(val)
                qty =  to_decimal("0")
                val =  to_decimal("0")
            lscheinnr = l_ophis.lscheinnr
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.datum = l_ophis.datum
            t_list.lscheinnr = lscheinnr
            t_list.f_bezeich = l_lager.bezeich
            t_list.t_bezeich = ""
            t_list.artnr = to_string(l_ophis.artnr, "9999999")
            t_list.bezeich = l_artikel.bezeich
            t_list.einheit = l_artikel.masseinheit
            t_list.content =  to_decimal(l_artikel.inhalt)

            if l_ophis.anzahl != 0:

                if not long_digit:
                    t_list.price = to_string((l_ophis.warenwert / l_ophis.anzahl) , "->>,>>>,>>9.99")
                else:
                    t_list.price = to_string((l_ophis.warenwert / l_ophis.anzahl) , "->,>>>,>>>,>>9")
            t_list.qty =  to_decimal(l_ophis.anzahl)
            t_list.val =  to_decimal(l_ophis.warenwert)
            t_list.s_qty = to_string(t_list.qty, "->>>,>>9.999")
            t_list.op_art = l_ophis.op_art

            if l_ophis.op_art == 2:
                val =  to_decimal(val) + to_decimal(l_ophis.warenwert)
                t_val =  to_decimal(t_val) + to_decimal(l_ophis.warenwert)

        if val != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)

        if t_val != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty =  to_decimal(t_qty)
            t_list.val =  to_decimal(t_val)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    create_list()

    return generate_output()