from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_lager, L_artikel, L_op, L_ophis

def stock_transformlist_create_listbl(from_date:date, to_date:date, from_art:int, to_art:int):
    it_exist = False
    t_list_list = []
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_op = l_ophis = None

    t_list = l_store = None

    t_list_list, T_list = create_model("T_list", {"datum":date, "lscheinnr":str, "f_bezeich":str, "t_bezeich":str, "artnr":str, "bezeich":str, "einheit":str, "content":decimal, "price":str, "qty":decimal, "s_qty":str, "op_art":int, "val":decimal})

    L_store = L_lager

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_list, long_digit, htparam, l_lager, l_artikel, l_op, l_ophis
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list
        return {"it_exist": it_exist, "t-list": t_list_list}

    def create_list():

        nonlocal it_exist, t_list_list, long_digit, htparam, l_lager, l_artikel, l_op, l_ophis
        nonlocal l_store


        nonlocal t_list, l_store
        nonlocal t_list_list

        lscheinnr:str = ""
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        lscheinnr = ""

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art >= 2) &  (L_op.op_art <= 4) &  (L_op.herkunftflag == 3) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            it_exist = True

            l_lager = db_session.query(L_lager).filter(
                    (L_lager.lager_nr == l_op.lager_nr)).first()

            l_store = db_session.query(L_store).filter(
                    (L_store.lager_nr == l_op.pos)).first()

            if lscheinnr != l_op.lscheinnr and qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.price = "Total"
                t_list.qty = qty
                t_list.val = val
                qty = 0
                val = 0
            lscheinnr = l_op.lscheinnr
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.datum = l_op.datum
            t_list.lscheinnr = lscheinnr
            t_list.f_bezeich = l_lager.bezeich

            if l_store:
                t_list.t_bezeich = l_store.bezeich
            t_list.artnr = to_string(l_op.artnr, "9999999")
            t_list.bezeich = l_artikel.bezeich
            t_list.einheit = l_artikel.masseinheit
            t_list.content = l_artikel.inhalt

            if l_op.anzahl != 0:

                if not long_digit:
                    t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>,>>>,>>9.99")
                else:
                    t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">,>>>,>>>,>>9")
            t_list.qty = l_op.anzahl
            t_list.val = l_op.warenwert
            t_list.s_qty = to_string(t_list.qty, ">>>,>>9.999")
            t_list.op_art = l_op.op_art

            if l_op.op_art == 2:
                val = val + l_op.warenwert
                t_val = t_val + l_op.warenwert

        l_ophis_obj_list = []
        for l_ophis, l_artikel in db_session.query(L_ophis, L_artikel).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).filter(
                (L_ophis.datum >= from_date) &  (L_ophis.datum <= to_date) &  (L_ophis.artnr >= from_art) &  (L_ophis.artnr <= to_art) &  (L_ophis.op_art >= 2) &  (L_ophis.op_art <= 4) &  (not (L_ophis.fibukonto.op("~")(".*CANCELLED.*")))).all():
            if l_ophis._recid in l_ophis_obj_list:
                continue
            else:
                l_ophis_obj_list.append(l_ophis._recid)

            l_lager = db_session.query(L_lager).filter(
                    (L_lager.lager_nr == l_ophis.lager_nr)).first()
            it_exist = False

            if lscheinnr != l_ophis.lscheinnr and qty != 0:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.price = "Total"
                t_list.qty = qty
                t_list.val = val
                qty = 0
                val = 0
            lscheinnr = l_ophis.lscheinnr
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.datum = l_ophis.datum
            t_list.lscheinnr = lscheinnr
            t_list.f_bezeich = l_lager.bezeich
            t_list.t_bezeich = ""
            t_list.artnr = to_string(l_ophis.artnr, "9999999")
            t_list.bezeich = l_artikel.bezeich
            t_list.einheit = l_artikel.masseinheit
            t_list.content = l_artikel.inhalt

            if l_ophis.anzahl != 0:

                if not long_digit:
                    t_list.price = to_string((l_ophis.warenwert / l_ophis.anzahl) , ">>,>>>,>>9.99")
                else:
                    t_list.price = to_string((l_ophis.warenwert / l_ophis.anzahl) , ">,>>>,>>>,>>9")
            t_list.qty = l_ophis.anzahl
            t_list.val = l_ophis.warenwert
            t_list.s_qty = to_string(t_list.qty, ">>>,>>9.999")
            t_list.op_art = l_ophis.op_art

            if l_ophis.op_art == 2:
                val = val + l_ophis.warenwert
                t_val = t_val + l_ophis.warenwert

        if val != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.val = val

        if t_val != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty = t_qty
            t_list.val = t_val

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    create_list()

    return generate_output()