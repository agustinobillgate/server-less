#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_untergrup, L_op, Gl_acct, Queasy

def inv_adjustlist_btn_go_webbl(sorttype:int, curr_lager:int, from_grp:int, transdate:date, flag_cost:bool):

    prepare_cache ([L_artikel, L_untergrup, L_op, Gl_acct, Queasy])

    tot_amount = to_decimal("0.0")
    tot_avrg_amount = to_decimal("0.0")
    c_list_list = []
    l_artikel = l_untergrup = l_op = gl_acct = queasy = None

    c_list = bc_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":Decimal, "zwkum":int, "endkum":int, "qty":Decimal, "qty1":Decimal, "amount":Decimal, "avrg_amount":Decimal, "fibukonto":string, "cost_center":string, "variance":Decimal, "lscheinnr":string, "id":string, "chg_id":string, "chg_date":date}, {"fibukonto": "0000000000"})
    bc_list_list, Bc_list = create_model("Bc_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":Decimal, "zwkum":int, "endkum":int, "qty":Decimal, "qty1":Decimal, "amount":Decimal, "avrg_amount":Decimal, "fibukonto":string, "cost_center":string, "variance":Decimal, "lscheinnr":string, "id":string, "chg_id":string, "chg_date":date}, {"fibukonto": "0000000000"})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amount, tot_avrg_amount, c_list_list, l_artikel, l_untergrup, l_op, gl_acct, queasy
        nonlocal sorttype, curr_lager, from_grp, transdate, flag_cost


        nonlocal c_list, bc_list
        nonlocal c_list_list, bc_list_list

        return {"tot_amount": tot_amount, "tot_avrg_amount": tot_avrg_amount, "c-list": c_list_list}

    def journal_list1():

        nonlocal tot_amount, tot_avrg_amount, c_list_list, l_artikel, l_untergrup, l_op, gl_acct, queasy
        nonlocal sorttype, curr_lager, from_grp, transdate, flag_cost


        nonlocal c_list, bc_list
        nonlocal c_list_list, bc_list_list


        c_list_list.clear()

        if sorttype == 1:

            if flag_cost:

                if from_grp == 0:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             ((trim(L_op.stornogrund) == ("0").lower()) | (trim(L_op.stornogrund) == ("00").lower()) | (trim(L_op.stornogrund) == ("000").lower()) | (trim(L_op.stornogrund) == ("0000").lower()) | (trim(L_op.stornogrund) == ("00000").lower()) | (trim(L_op.stornogrund) == ("000000").lower()) | (trim(L_op.stornogrund) == ("0000000").lower()) | (trim(L_op.stornogrund) == ("00000000").lower()) | (trim(L_op.stornogrund) == ("000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000").lower()) | (trim(L_op.stornogrund) == ("00000000000").lower()) | (trim(L_op.stornogrund) == ("000000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000000").lower())) & (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.artnr, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             ((trim(L_op.stornogrund) == ("0").lower()) | (trim(L_op.stornogrund) == ("00").lower()) | (trim(L_op.stornogrund) == ("000").lower()) | (trim(L_op.stornogrund) == ("0000").lower()) | (trim(L_op.stornogrund) == ("00000").lower()) | (trim(L_op.stornogrund) == ("000000").lower()) | (trim(L_op.stornogrund) == ("0000000").lower()) | (trim(L_op.stornogrund) == ("00000000").lower()) | (trim(L_op.stornogrund) == ("000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000").lower()) | (trim(L_op.stornogrund) == ("00000000000").lower()) | (trim(L_op.stornogrund) == ("000000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000000").lower())) & (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.artnr, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


            else:

                if from_grp == 0:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.artnr, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.artnr, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

        elif sorttype == 2:

            if flag_cost:

                if from_grp == 0:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             ((trim(L_op.stornogrund) == ("0").lower()) | (trim(L_op.stornogrund) == ("00").lower()) | (trim(L_op.stornogrund) == ("000").lower()) | (trim(L_op.stornogrund) == ("0000").lower()) | (trim(L_op.stornogrund) == ("00000").lower()) | (trim(L_op.stornogrund) == ("000000").lower()) | (trim(L_op.stornogrund) == ("0000000").lower()) | (trim(L_op.stornogrund) == ("00000000").lower()) | (trim(L_op.stornogrund) == ("000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000").lower()) | (trim(L_op.stornogrund) == ("00000000000").lower()) | (trim(L_op.stornogrund) == ("000000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000000").lower())) & (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result"),(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             ((trim(L_op.stornogrund) == ("0").lower()) | (trim(L_op.stornogrund) == ("00").lower()) | (trim(L_op.stornogrund) == ("000").lower()) | (trim(L_op.stornogrund) == ("0000").lower()) | (trim(L_op.stornogrund) == ("00000").lower()) | (trim(L_op.stornogrund) == ("000000").lower()) | (trim(L_op.stornogrund) == ("0000000").lower()) | (trim(L_op.stornogrund) == ("00000000").lower()) | (trim(L_op.stornogrund) == ("000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000").lower()) | (trim(L_op.stornogrund) == ("00000000000").lower()) | (trim(L_op.stornogrund) == ("000000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000000").lower())) & (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result"),(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


            else:

                if from_grp == 0:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2

        elif sorttype == 3:

            if flag_cost:

                if from_grp == 0:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             ((trim(L_op.stornogrund) == ("0").lower()) | (trim(L_op.stornogrund) == ("00").lower()) | (trim(L_op.stornogrund) == ("000").lower()) | (trim(L_op.stornogrund) == ("0000").lower()) | (trim(L_op.stornogrund) == ("00000").lower()) | (trim(L_op.stornogrund) == ("000000").lower()) | (trim(L_op.stornogrund) == ("0000000").lower()) | (trim(L_op.stornogrund) == ("00000000").lower()) | (trim(L_op.stornogrund) == ("000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000").lower()) | (trim(L_op.stornogrund) == ("00000000000").lower()) | (trim(L_op.stornogrund) == ("000000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000000").lower())) & (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.zwkum, L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             ((trim(L_op.stornogrund) == ("0").lower()) | (trim(L_op.stornogrund) == ("00").lower()) | (trim(L_op.stornogrund) == ("000").lower()) | (trim(L_op.stornogrund) == ("0000").lower()) | (trim(L_op.stornogrund) == ("00000").lower()) | (trim(L_op.stornogrund) == ("000000").lower()) | (trim(L_op.stornogrund) == ("0000000").lower()) | (trim(L_op.stornogrund) == ("00000000").lower()) | (trim(L_op.stornogrund) == ("000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000").lower()) | (trim(L_op.stornogrund) == ("00000000000").lower()) | (trim(L_op.stornogrund) == ("000000000000").lower()) | (trim(L_op.stornogrund) == ("0000000000000").lower())) & (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.zwkum, L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


            else:

                if from_grp == 0:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.zwkum, L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


                else:

                    l_op_obj_list = {}
                    l_op = L_op()
                    l_artikel = L_artikel()
                    l_untergrup = L_untergrup()
                    for l_op.deci1, l_op.anzahl, l_op.stornogrund, l_op.warenwert, l_op.lscheinnr, l_op.artnr, l_op._recid, l_artikel.endkum, l_artikel.zwkum, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.deci1, L_op.anzahl, L_op.stornogrund, L_op.warenwert, L_op.lscheinnr, L_op.artnr, L_op._recid, L_artikel.endkum, L_artikel.zwkum, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                             (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum <= transdate) & ((substring(L_op.lscheinnr, 0, 3) == ("INV").lower()) | (substring(L_op.lscheinnr, 0, 3) == ("SRD").lower())) & (L_op.loeschflag <= 1)).order_by(L_artikel.zwkum, L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                        if l_op_obj_list.get(l_op._recid):
                            continue
                        else:
                            l_op_obj_list[l_op._recid] = True

                        c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                        if not c_list:
                            c_list = C_list()
                            c_list_list.append(c_list)

                            c_list.artnr = 0
                            c_list.fibukonto = ""
                            c_list.endkum = l_artikel.endkum
                            c_list.zwkum = l_artikel.zwkum
                            c_list.bezeich = l_untergrup.bezeich


                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = l_artikel.artnr
                        c_list.bezeich = l_artikel.bezeich
                        c_list.munit = l_artikel.masseinheit
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)
                        c_list.zwkum = l_artikel.zwkum
                        c_list.endkum = l_artikel.endkum
                        c_list.qty =  to_decimal(l_op.deci1[0])
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)
                        c_list.variance =  to_decimal(c_list.qty) - to_decimal(c_list.qty1)
                        c_list.lscheinnr = l_op.lscheinnr


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, c_list.fibukonto)]})

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment inv")]})

                        if queasy:
                            c_list.id = queasy.char2

                        queasy = get_cache (Queasy, {"key": [(eq, 334)],"char1": [(eq, l_op.lscheinnr)],"char3": [(eq, "adjusment result")],"number1": [(eq, l_op.artnr)]})

                        if queasy:
                            c_list.chg_id = queasy.char2
                            c_list.chg_date = queasy.date2


    journal_list1()

    return generate_output()