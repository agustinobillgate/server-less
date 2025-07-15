#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_ophdr, L_artikel, Gl_acct

def stock_outlist_print_outgoingbl(s_op_recid:int, from_grp:int, show_price:bool):

    prepare_cache ([L_op, L_ophdr, L_artikel, Gl_acct])

    tot_amount = to_decimal("0.0")
    l_op1_lscheinnr = ""
    print_list_data = []
    preis:Decimal = to_decimal("0.0")
    wert:Decimal = to_decimal("0.0")
    l_op = l_ophdr = l_artikel = gl_acct = None

    print_list = l_op1 = None

    print_list_data, Print_list = create_model("Print_list", {"datum":date, "lager_nr":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "gl_bezeich":string, "preis":Decimal, "wert":Decimal})

    L_op1 = create_buffer("L_op1",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amount, l_op1_lscheinnr, print_list_data, preis, wert, l_op, l_ophdr, l_artikel, gl_acct
        nonlocal s_op_recid, from_grp, show_price
        nonlocal l_op1


        nonlocal print_list, l_op1
        nonlocal print_list_data

        return {"tot_amount": tot_amount, "l_op1_lscheinnr": l_op1_lscheinnr, "print-list": print_list_data}

    l_op1 = get_cache (L_op, {"_recid": [(eq, s_op_recid)]})

    if l_op1:
        l_op1_lscheinnr = l_op1.lscheinnr

        l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "stt")],"lscheinnr": [(eq, l_op1.lscheinnr)],"fibukonto": [(ne, "")]})

        if from_grp == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.einzelpreis, l_op.warenwert, l_op.stornogrund, l_op.datum, l_op.lager_nr, l_op.artnr, l_op.anzahl, l_op._recid, l_op.lscheinnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.einzelpreis, L_op.warenwert, L_op.stornogrund, L_op.datum, L_op.lager_nr, L_op.artnr, L_op.anzahl, L_op._recid, L_op.lscheinnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum == l_op1.datum) & (L_op.op_art == 3) & (L_op.lscheinnr == l_op1.lscheinnr) & (L_op.loeschflag <= 1)).order_by(l_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)

                if l_op.stornogrund != "":

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if l_op.stornogrund == "" or not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)]})
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.datum = l_op.datum
                print_list.lager_nr = l_op.lager_nr
                print_list.artnr = l_op.artnr
                print_list.bezeich = l_artikel.bezeich
                print_list.anzahl =  to_decimal(l_op.anzahl)
                print_list.preis =  to_decimal(preis)
                print_list.wert =  to_decimal(wert)

                if gl_acct:
                    print_list.gl_bezeich = gl_acct.bezeich
                tot_amount =  to_decimal(tot_amount) + to_decimal(wert)

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.einzelpreis, l_op.warenwert, l_op.stornogrund, l_op.datum, l_op.lager_nr, l_op.artnr, l_op.anzahl, l_op._recid, l_op.lscheinnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.einzelpreis, L_op.warenwert, L_op.stornogrund, L_op.datum, L_op.lager_nr, L_op.artnr, L_op.anzahl, L_op._recid, L_op.lscheinnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_op.datum == l_op1.datum) & (L_op.op_art == 3) & (L_op.lscheinnr == l_op1.lscheinnr) & (L_op.loeschflag <= 1)).order_by(l_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if show_price:
                    preis =  to_decimal(l_op.einzelpreis)
                    wert =  to_decimal(l_op.warenwert)

                if l_op.stornogrund != "":

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if l_op.stornogrund == "" or not gl_acct:

                    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)]})
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.datum = l_op.datum
                print_list.lager_nr = l_op.lager_nr
                print_list.artnr = l_op.artnr
                print_list.bezeich = l_artikel.bezeich
                print_list.anzahl =  to_decimal(l_op.anzahl)
                print_list.preis =  to_decimal(preis)
                print_list.wert =  to_decimal(wert)

                if gl_acct:
                    print_list.gl_bezeich = gl_acct.bezeich
                tot_amount =  to_decimal(tot_amount) + to_decimal(wert)


    return generate_output()