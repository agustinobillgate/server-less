from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_op, L_ophdr, L_artikel, Gl_acct

def stock_outlist_print_outgoingbl(s_op_recid:int, from_grp:int, show_price:bool):
    tot_amount = 0
    l_op1_lscheinnr = ""
    print_list_list = []
    preis:decimal = 0
    wert:decimal = 0
    l_op = l_ophdr = l_artikel = gl_acct = None

    print_list = l_op1 = None

    print_list_list, Print_list = create_model("Print_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":str, "anzahl":decimal, "gl_bezeich":str, "preis":decimal, "wert":decimal})

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amount, l_op1_lscheinnr, print_list_list, preis, wert, l_op, l_ophdr, l_artikel, gl_acct
        nonlocal l_op1


        nonlocal print_list, l_op1
        nonlocal print_list_list
        return {"tot_amount": tot_amount, "l_op1_lscheinnr": l_op1_lscheinnr, "print-list": print_list_list}

    l_op1 = db_session.query(L_op1).filter(
            (L_op1._recid == s_op_recid)).first()

    l_ophdr = db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lscheinnr == l_op1.lscheinnr) &  (L_ophdr.fibukonto != "")).first()
    l_op1_lscheinnr = l_op1.lscheinnr

    if from_grp == 0:

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(l_artikel.artnr == L_op.artnr)).filter(
                (L_op.datum == l_op1.datum) &  (L_op.op_art == 3) &  (L_op.lscheinnr == l_op1.lscheinnr) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if show_price:
                preis = l_op.einzelpreis
                wert = l_op.warenwert

            if l_op.stornogrund != "":

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_op.stornogrund)).first()

            if l_op.stornogrund == "" or not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_ophdr.fibukonto)).first()
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.datum = l_op.datum
            print_list.lager_nr = l_op.lager_nr
            print_list.artnr = l_op.artnr
            print_list.bezeich = l_artikel.bezeich
            print_list.anzahl = l_op.anzahl
            print_list.preis = preis
            print_list.wert = wert

            if gl_acct:
                print_list.gl_bezeich = gl_acct.bezeich
            tot_amount = tot_amount + wert

    else:

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(l_artikel.artnr == L_op.artnr) &  (l_artikel.endkum == from_grp)).filter(
                (L_op.datum == l_op1.datum) &  (L_op.op_art == 3) &  (L_op.lscheinnr == l_op1.lscheinnr) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if show_price:
                preis = l_op.einzelpreis
                wert = l_op.warenwert

            if l_op.stornogrund != "":

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_op.stornogrund)).first()

            if l_op.stornogrund == "" or not gl_acct:

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == l_ophdr.fibukonto)).first()
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.datum = l_op.datum
            print_list.lager_nr = l_op.lager_nr
            print_list.artnr = l_op.artnr
            print_list.bezeich = l_artikel.bezeich
            print_list.anzahl = l_op.anzahl
            print_list.preis = preis
            print_list.wert = wert

            if gl_acct:
                print_list.gl_bezeich = gl_acct.bezeich
            tot_amount = tot_amount + wert


    return generate_output()