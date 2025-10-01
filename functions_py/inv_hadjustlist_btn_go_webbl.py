#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_untergrup, L_ophis, Queasy, Gl_acct

from sqlalchemy import func, not_

def inv_hadjustlist_btn_go_webbl(sorttype:int, curr_lager:int, from_grp:int, transdate:date, flag_cost:bool, yy:int, mm:int):

    prepare_cache ([L_artikel, L_untergrup, L_ophis, Queasy, Gl_acct])

    tot_amount = to_decimal("0.0")
    tot_avrg_amount = to_decimal("0.0")
    c_list_data = []
    deci1:Decimal = to_decimal("0.0")
    from_date:date = None
    to_date:date = None
    l_artikel = l_untergrup = l_ophis = queasy = gl_acct = None

    c_list = bc_list = None

    c_list_data, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":Decimal, "zwkum":int, "endkum":int, "qty":Decimal, "qty1":Decimal, "amount":Decimal, "avrg_amount":Decimal, "fibukonto":string, "cost_center":string, "variance":Decimal, "lscheinnr":string, "id":string, "chg_id":string, "chg_date":date}, {"fibukonto": "0000000000"})
    bc_list_data, Bc_list = create_model("Bc_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":Decimal, "zwkum":int, "endkum":int, "qty":Decimal, "qty1":Decimal, "amount":Decimal, "avrg_amount":Decimal, "fibukonto":string, "cost_center":string, "variance":Decimal, "lscheinnr":string, "id":string, "chg_id":string, "chg_date":date}, {"fibukonto": "0000000000"})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amount, tot_avrg_amount, c_list_data, deci1, from_date, to_date, l_artikel, l_untergrup, l_ophis, queasy, gl_acct
        nonlocal sorttype, curr_lager, from_grp, transdate, flag_cost, yy, mm


        nonlocal c_list, bc_list
        nonlocal c_list_data, bc_list_data

        return {"tot_amount": tot_amount, "tot_avrg_amount": tot_avrg_amount, "c-list": c_list_data}

    def journal_list1():

        nonlocal tot_amount, tot_avrg_amount, c_list_data, deci1, from_date, to_date, l_artikel, l_untergrup, l_ophis, queasy, gl_acct
        nonlocal sorttype, curr_lager, from_grp, transdate, flag_cost, yy, mm


        nonlocal c_list, bc_list
        nonlocal c_list_data, bc_list_data


        c_list_data.clear()

        if sorttype == 1:

            if flag_cost:

                if from_grp == 0:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(((func.trim(L_ophis.fibukonto) == ("0").lower()) | (func.trim(L_ophis.fibukonto) == ("00").lower()) | (func.trim(L_ophis.fibukonto) == ("000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000000").lower())) & (L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.artnr, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr

                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

                else:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(((func.trim(L_ophis.fibukonto) == ("0").lower()) | (func.trim(L_ophis.fibukonto) == ("00").lower()) | (func.trim(L_ophis.fibukonto) == ("000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000000").lower())) & (L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.artnr, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

            else:
                if from_grp == 0:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower() ) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower() )) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower() ), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.artnr, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich.replace("\\n", "\n")
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr

                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.artnr, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

        elif sorttype == 2:

            if flag_cost:

                if from_grp == 0:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(((func.trim(L_ophis.fibukonto) == ("0").lower()) | (func.trim(L_ophis.fibukonto) == ("00").lower()) | (func.trim(L_ophis.fibukonto) == ("000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000000").lower())) & (L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr

                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result"),(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

                else:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(((func.trim(L_ophis.fibukonto) == ("0").lower()) | (func.trim(L_ophis.fibukonto) == ("00").lower()) | (func.trim(L_ophis.fibukonto) == ("000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000000").lower())) & (L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result"),(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


            else:

                if from_grp == 0:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

        elif sorttype == 3:

            if flag_cost:

                if from_grp == 0:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(((func.trim(L_ophis.fibukonto) == ("0").lower()) | (func.trim(L_ophis.fibukonto) == ("00").lower()) | (func.trim(L_ophis.fibukonto) == ("000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000000").lower())) & (L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.zwkum, L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(((func.trim(L_ophis.fibukonto) == ("0").lower()) | (func.trim(L_ophis.fibukonto) == ("00").lower()) | (func.trim(L_ophis.fibukonto) == ("000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("00000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("000000000000").lower()) | (func.trim(L_ophis.fibukonto) == ("0000000000000").lower())) & (L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 0, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 0, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.zwkum, L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


            else:

                if from_grp == 0:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, length(L_ophis.fibukonto) - length(("CANCELLED").lower()), length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.zwkum, L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:
                    l_ophis_obj_list = {}
                    l_ophis = L_ophis()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()

                    for l_ophis.docu_nr, l_ophis.lscheinnr, l_ophis.artnr, l_ophis.anzahl, l_ophis.fibukonto, l_ophis.warenwert, l_ophis._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_ophis.docu_nr, L_ophis.lscheinnr, L_ophis.artnr, L_ophis.anzahl, L_ophis.fibukonto, L_ophis.warenwert, L_ophis._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter((L_ophis.lager_nr == curr_lager) & (L_ophis.op_art == 3) & (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((func.substr(L_ophis.lscheinnr, 1, 3) == ("INV").lower()) | (func.substr(L_ophis.lscheinnr, 1, 3) == ("SRD").lower())) & (not_((func.length(L_ophis.fibukonto) > 8) & (func.substr(L_ophis.fibukonto, func.length(L_ophis.fibukonto) - length(("CANCELLED").lower()), func.length(L_ophis.fibukonto)) == ("CANCELLED").lower())))).order_by(L_artikel.zwkum, L_artikel.bezeich, L_ophis.datum, L_ophis.lscheinnr).all():

                        # if l_ophis_obj_list.get(l_ophis._recid):
                        #     continue
                        # else:
                        #     l_ophis_obj_list[l_ophis._recid] = True

                        queasy = get_cache (Queasy, {"key": [(eq, 363)],"char1": [(eq, l_ophis.docu_nr)],"char2": [(eq, l_ophis.lscheinnr)],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            deci1 =  to_decimal(queasy.deci1)

                        c_list = query(c_list_data, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_data.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich

                        c_list = C_list()
                        c_list_data.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(deci1)
                        c_list.qty1 =  to_decimal(deci1) - to_decimal(l_ophis.anzahl)
                        c_list.fibukonto = l_ophis.fibukonto
                        c_list.amount =  to_decimal(l_ophis.warenwert)
                        c_list.avrg_amount =  to_decimal(l_ophis.warenwert) / to_decimal(l_ophis.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_ophis.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_ophis.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_ophis.warenwert) / to_decimal(l_ophis.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_ophis.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_ophis.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

    if mm == 12:
        from_date = date_mdy(mm, 1, yy)
        to_date = date_mdy(1, 1, yy + 1) - timedelta(days=1)
    else:
        from_date = date_mdy(mm, 1, yy)
        to_date = date_mdy(mm + 1, 1, yy) - timedelta(days=1)

    journal_list1()

    return generate_output()