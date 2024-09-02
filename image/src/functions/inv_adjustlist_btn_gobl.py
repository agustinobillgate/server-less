from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, L_untergrup, L_op, Gl_acct

def inv_adjustlist_btn_gobl(sorttype:int, curr_lager:int, from_grp:int, transdate:date):
    tot_amount = 0
    tot_avrg_amount = 0
    c_list_list = []
    l_artikel = l_untergrup = l_op = gl_acct = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":str, "munit":str, "inhalt":decimal, "zwkum":int, "endkum":int, "qty":decimal, "qty1":decimal, "amount":decimal, "avrg_amount":decimal, "fibukonto":str, "cost_center":str, "variance":decimal}, {"fibukonto": "0000000000"})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amount, tot_avrg_amount, c_list_list, l_artikel, l_untergrup, l_op, gl_acct


        nonlocal c_list
        nonlocal c_list_list
        return {"tot_amount": tot_amount, "tot_avrg_amount": tot_avrg_amount, "c-list": c_list_list}

    def journal_list1():

        nonlocal tot_amount, tot_avrg_amount, c_list_list, l_artikel, l_untergrup, l_op, gl_acct


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype == 1:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == curr_lager) &  (L_op.op_art == 3) &  (L_op.datum <= transdate) &  ((substring(L_op.lscheinnr, 0, 3) == "INV") |  (substring(L_op.lscheinnr, 0, 3) == "SRD")) &  (L_op.loeschflag <= 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                c_list = query(c_list_list, filters=(lambda c_list :c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

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
                c_list.inhalt = l_artikel.inhalt
                c_list.zwkum = l_artikel.zwkum
                c_list.endkum = l_artikel.endkum
                c_list.qty = l_op.deci1[0]
                c_list.qty1 = l_op.deci1[0] - l_op.anzahl
                c_list.fibukonto = l_op.stornogrund
                c_list.amount = l_op.warenwert
                c_list.avrg_amount = l_op.warenwert / l_op.anzahl
                c_list.variance = c_list.qty - c_list.qty1


                tot_amount = tot_amount + l_op.warenwert
                tot_avrg_amount = tot_avrg_amount + (l_op.warenwert / l_op.anzahl)

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == c_list.fibukonto)).first()

                if gl_acct:
                    c_list.cost_center = gl_acct.bezeich


        elif sorttype == 2:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == curr_lager) &  (L_op.op_art == 3) &  (L_op.datum <= transdate) &  ((substring(L_op.lscheinnr, 0, 3) == "INV") |  (substring(L_op.lscheinnr, 0, 3) == "SRD")) &  (L_op.loeschflag <= 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                c_list = query(c_list_list, filters=(lambda c_list :c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

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
                c_list.inhalt = l_artikel.inhalt
                c_list.zwkum = l_artikel.zwkum
                c_list.endkum = l_artikel.endkum
                c_list.qty = l_op.deci1[0]
                c_list.qty1 = l_op.deci1[0] - l_op.anzahl
                c_list.fibukonto = l_op.stornogrund
                c_list.amount = l_op.warenwert
                c_list.avrg_amount = l_op.warenwert / l_op.anzahl
                c_list.variance = c_list.qty - c_list.qty1


                tot_amount = tot_amount + l_op.warenwert
                tot_avrg_amount = tot_avrg_amount + (l_op.warenwert / l_op.anzahl)

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == c_list.fibukonto)).first()

                if gl_acct:
                    c_list.cost_center = gl_acct.bezeich


        elif sorttype == 3:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == curr_lager) &  (L_op.op_art == 3) &  (L_op.datum <= transdate) &  ((substring(L_op.lscheinnr, 0, 3) == "INV") |  (substring(L_op.lscheinnr, 0, 3) == "SRD")) &  (L_op.loeschflag <= 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                c_list = query(c_list_list, filters=(lambda c_list :c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

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
                c_list.inhalt = l_artikel.inhalt
                c_list.zwkum = l_artikel.zwkum
                c_list.endkum = l_artikel.endkum
                c_list.qty = l_op.deci1[0]
                c_list.qty1 = l_op.deci1[0] - l_op.anzahl
                c_list.fibukonto = l_op.stornogrund
                c_list.amount = l_op.warenwert
                c_list.avrg_amount = l_op.warenwert / l_op.anzahl
                c_list.variance = c_list.qty - c_list.qty1


                tot_amount = tot_amount + l_op.warenwert
                tot_avrg_amount = tot_avrg_amount + (l_op.warenwert / l_op.anzahl)

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == c_list.fibukonto)).first()

                if gl_acct:
                    c_list.cost_center = gl_acct.bezeich

    journal_list1()

    return generate_output()