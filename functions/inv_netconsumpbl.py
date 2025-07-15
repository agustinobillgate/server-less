#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_ophis, Gl_acct, L_lager, L_op

def inv_netconsumpbl(sorttype:int, from_date:date, to_date:date, main_grp:int):

    prepare_cache ([Htparam, L_artikel, L_ophis, Gl_acct, L_lager, L_op])

    t_list_data = []
    htparam = l_artikel = l_ophis = gl_acct = l_lager = l_op = None

    t_list = tbuff = None

    t_list_data, T_list = create_model("T_list", {"nr":int, "f_bezeich":string, "t_bezeich":string, "artnr":string, "bezeich":string, "qty":Decimal, "price":Decimal, "val":Decimal, "mess_unit":string, "deliv_unit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, htparam, l_artikel, l_ophis, gl_acct, l_lager, l_op
        nonlocal sorttype, from_date, to_date, main_grp


        nonlocal t_list, tbuff
        nonlocal t_list_data

        return {"t-list": t_list_data}

    def create_list():

        nonlocal t_list_data, htparam, l_artikel, l_ophis, gl_acct, l_lager, l_op
        nonlocal sorttype, from_date, to_date, main_grp


        nonlocal t_list, tbuff
        nonlocal t_list_data

        close_mat:date = None
        close_fb:date = None
        close_date:date = None
        tot_amt:Decimal = to_decimal("0.0")
        tot_qty:int = 0
        i:int = 0
        Tbuff = T_list
        tbuff_data = t_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
        close_mat = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
        close_fb = htparam.fdate

        if close_mat > close_fb:
            close_date = close_mat
        else:
            close_date = close_fb
        t_list_data.clear()

        if sorttype != 3:

            if to_date <= close_date:

                l_ophis_obj_list = {}
                l_ophis = L_ophis()
                l_artikel = L_artikel()
                for l_ophis.artnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.fibukonto, l_ophis.lager_nr, l_ophis._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_ophis.artnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.fibukonto, L_ophis.lager_nr, L_ophis._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == main_grp)).filter(
                         (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.op_art == 3) & (substring(L_ophis.lscheinnr, 0, 3) == ("INV").lower())).order_by(L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():
                    if l_ophis_obj_list.get(l_ophis._recid):
                        continue
                    else:
                        l_ophis_obj_list[l_ophis._recid] = True


                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = to_string(l_ophis.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.qty =  to_decimal(l_ophis.anzahl)
                    t_list.val =  to_decimal(l_ophis.warenwert)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(l_ophis.warenwert)
                    tot_qty = tot_qty + l_ophis.anzahl


                    t_list.mess_unit = l_artikel.masseinheit
                    t_list.deliv_unit = l_artikel.traubensorte

                    if t_list.qty > 0 and t_list.val > 0:
                        t_list.price =  to_decimal(t_list.val) / to_decimal(t_list.qty)

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                    if gl_acct:
                        t_list.t_bezeich = gl_acct.bezeich

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_ophis.lager_nr)]})

                    if l_lager:
                        t_list.f_bezeich = l_lager.bezeich

            else:

                l_op_obj_list = {}
                l_op = L_op()
                l_artikel = L_artikel()
                for l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.lager_nr, l_op._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.lager_nr, L_op._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == main_grp)).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (substring(L_op.lscheinnr, 0, 3) == ("INV").lower())).order_by(L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True


                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.qty =  to_decimal(l_op.anzahl)
                    t_list.val =  to_decimal(l_op.warenwert)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(l_op.warenwert)
                    tot_qty = tot_qty + l_ophis.anzahl


                    t_list.mess_unit = l_artikel.masseinheit
                    t_list.deliv_unit = l_artikel.traubensorte

                    if t_list.qty > 0 and t_list.val > 0:
                        t_list.price =  to_decimal(t_list.val) / to_decimal(t_list.qty)

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                    if l_lager:
                        t_list.f_bezeich = l_lager.bezeich

        else:

            if to_date <= close_date:

                l_ophis_obj_list = {}
                l_ophis = L_ophis()
                l_artikel = L_artikel()
                for l_ophis.artnr, l_ophis.anzahl, l_ophis.warenwert, l_ophis.fibukonto, l_ophis.lager_nr, l_ophis._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_ophis.artnr, L_ophis.anzahl, L_ophis.warenwert, L_ophis.fibukonto, L_ophis.lager_nr, L_ophis._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum >= 3)).filter(
                         (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.op_art == 3) & (substring(L_ophis.lscheinnr, 0, 3) == ("INV").lower())).order_by(L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():
                    if l_ophis_obj_list.get(l_ophis._recid):
                        continue
                    else:
                        l_ophis_obj_list[l_ophis._recid] = True


                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = to_string(l_ophis.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.qty =  to_decimal(l_ophis.anzahl)
                    t_list.val =  to_decimal(l_ophis.warenwert)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(l_ophis.warenwert)
                    tot_qty = tot_qty + l_ophis.anzahl


                    t_list.mess_unit = l_artikel.masseinheit
                    t_list.deliv_unit = l_artikel.traubensorte

                    if t_list.qty > 0 and t_list.val > 0:
                        t_list.price =  to_decimal(t_list.val) / to_decimal(t_list.qty)

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                    if gl_acct:
                        t_list.t_bezeich = gl_acct.bezeich

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_ophis.lager_nr)]})

                    if l_lager:
                        t_list.f_bezeich = l_lager.bezeich

            else:

                l_op_obj_list = {}
                l_op = L_op()
                l_artikel = L_artikel()
                for l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.lager_nr, l_op._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.lager_nr, L_op._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum >= 3)).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (substring(L_op.lscheinnr, 0, 3) == ("INV").lower())).order_by(L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True


                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.qty =  to_decimal(l_op.anzahl)
                    t_list.val =  to_decimal(l_op.warenwert)
                    tot_amt =  to_decimal(tot_amt) + to_decimal(l_op.warenwert)
                    tot_qty = tot_qty + l_ophis.anzahl


                    t_list.mess_unit = l_artikel.masseinheit
                    t_list.deliv_unit = l_artikel.traubensorte

                    if t_list.qty > 0 and t_list.val > 0:
                        t_list.price =  to_decimal(t_list.val) / to_decimal(t_list.qty)

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                    if l_lager:
                        t_list.f_bezeich = l_lager.bezeich

        i = 1

        for tbuff in query(tbuff_data, sort_by=[("f_bezeich",False)]):
            tbuff.nr = i


            i = i + 1
        t_list = T_list()
        t_list_data.append(t_list)

        t_list.bezeich = "T O T A L"
        t_list.qty =  to_decimal(tot_qty)
        t_list.val =  to_decimal(tot_amt)
        t_list.nr = i

    create_list()

    return generate_output()