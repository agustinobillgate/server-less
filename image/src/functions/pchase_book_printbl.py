from functions.additional_functions import *
import decimal
from models import L_pprice, L_lieferant, L_artikel, Htparam, L_order

def pchase_book_printbl(sorttype:int, s_artnr:int):
    output_list_list = []
    total_anzahl:int = 0
    total_einzelpreis:decimal = 0
    total_warenwert:decimal = 0
    i:int = 0
    long_digit:bool = False
    curr_remark:str = ""
    l_pprice = l_lieferant = l_artikel = htparam = l_order = None

    output_list = l_price1 = l_supply = l_art1 = None

    output_list_list, Output_list = create_model("Output_list", {"counter":int, "str":str, "pos":int}, {"pos": 1})

    L_price1 = L_pprice
    L_supply = L_lieferant
    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, total_anzahl, total_einzelpreis, total_warenwert, i, long_digit, curr_remark, l_pprice, l_lieferant, l_artikel, htparam, l_order
        nonlocal l_price1, l_supply, l_art1


        nonlocal output_list, l_price1, l_supply, l_art1
        nonlocal output_list_list
        return {"output-list": output_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if sorttype == 1:

        l_price1_obj_list = []
        for l_price1, l_art1, l_supply in db_session.query(L_price1, L_art1, L_supply).join(L_art1,(L_art1.artnr == L_price1.artnr)).join(L_supply,(L_supply.lief_nr == L_price1.lief_nr)).filter(
                (L_price1.artnr == s_artnr)).all():
            if l_price1._recid in l_price1_obj_list:
                continue
            else:
                l_price1_obj_list.append(l_price1._recid)


            i = i + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.counter = i

            if not long_digit:
                output_list.str = \
                        to_string(l_price1.bestelldatum, "99/99/99") + " " +\
                        to_string(l_supply.firma, "x(24)") + " " +\
                        to_string(l_price1.docu_nr, "x(16)") + " " +\
                        to_string(l_art1.traubensort, "x(9)") + " " +\
                        to_string(l_art1.lief_einheit, ">>>,>>9") + " " +\
                        to_string(l_price1.anzahl) + " " +\
                        to_string(l_price1.einzelpreis, "->>,>>>,>>9.99") + " " +\
                        to_string(l_price1.warenwert, "->>,>>>,>>9.99")


                total_anzahl = total_anzahl + l_price1.anzahl
                total_einzelpreis = total_einzelpreis + l_price1.einzelpreis
                total_warenwert = total_warenwert + l_price1.warenwert

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_price1.docu_nr) &  (L_order.lief_nr == l_price1.lief_nr) &  (L_order.artnr == s_artnr)).first()

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")
            else:
                output_list.str = \
                        to_string(l_price1.bestelldatum, "99/99/99") + " " +\
                        to_string(l_supply.firma, "x(24)") + " " +\
                        to_string(l_price1.docu_nr, "x(16)") + " " +\
                        to_string(l_art1.traubensort, "x(9)") + " " +\
                        to_string(l_art1.lief_einheit, ">>>,>>9") + " " +\
                        to_string(l_price1.anzahl) + " " +\
                        to_string(l_price1.einzelpreis, "->,>>>,>>>,>>9") + " " +\
                        to_string(l_price1.warenwert, "->,>>>,>>>,>>9")


                total_anzahl = total_anzahl + l_price1.anzahl
                total_einzelpreis = total_einzelpreis + l_price1.einzelpreis
                total_warenwert = total_warenwert + l_price1.warenwert

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_price1.docu_nr) &  (L_order.lief_nr == l_price1.lief_nr) &  (L_order.artnr == s_artnr)).first()

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")


    elif sorttype == 2:

        l_price1_obj_list = []
        for l_price1, l_art1, l_supply in db_session.query(L_price1, L_art1, L_supply).join(L_art1,(L_art1.artnr == L_price1.artnr)).join(L_supply,(L_supply.lief_nr == L_price1.lief_nr)).filter(
                (L_price1.artnr == s_artnr)).all():
            if l_price1._recid in l_price1_obj_list:
                continue
            else:
                l_price1_obj_list.append(l_price1._recid)


            i = i + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.counter = i

            if not long_digit:
                output_list.str = \
                        to_string(l_price1.bestelldatum, "99/99/99") + " " +\
                        to_string(l_supply.firma, "x(24)") + " " +\
                        to_string(l_price1.docu_nr, "x(16)") + " " +\
                        to_string(l_art1.traubensort, "x(9)") + " " +\
                        to_string(l_art1.lief_einheit, ">>>,>>9") + " " +\
                        to_string(l_price1.anzahl) + " " +\
                        to_string(l_price1.einzelpreis, "->>,>>>,>>9.99") + " " +\
                        to_string(l_price1.warenwert, "->>,>>>,>>9.99")


                total_anzahl = total_anzahl + l_price1.anzahl
                total_einzelpreis = total_einzelpreis + l_price1.einzelpreis
                total_warenwert = total_warenwert + l_price1.warenwert

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_price1.docu_nr) &  (L_order.lief_nr == l_price1.lief_nr) &  (L_order.artnr == s_artnr)).first()

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")
            else:
                output_list.str = \
                        to_string(l_price1.bestelldatum, "99/99/99") + " " +\
                        to_string(l_supply.firma, "x(24)") + " " +\
                        to_string(l_price1.docu_nr, "x(16)") + " " +\
                        to_string(l_art1.traubensort, "x(9)") + " " +\
                        to_string(l_art1.lief_einheit, ">>>,>>9") + " " +\
                        to_string(l_price1.anzahl) + " " +\
                        to_string(l_price1.einzelpreis, "->,>>>,>>>,>>9") + " " +\
                        to_string(l_price1.warenwert, "->,>>>,>>>,>>9")


                total_anzahl = total_anzahl + l_price1.anzahl
                total_einzelpreis = total_einzelpreis + l_price1.einzelpreis
                total_warenwert = total_warenwert + l_price1.warenwert

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_price1.docu_nr) &  (L_order.lief_nr == l_price1.lief_nr) &  (L_order.artnr == s_artnr)).first()

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")


    elif sorttype == 3:

        l_price1_obj_list = []
        for l_price1, l_art1, l_supply in db_session.query(L_price1, L_art1, L_supply).join(L_art1,(L_art1.artnr == L_price1.artnr)).join(L_supply,(L_supply.lief_nr == L_price1.lief_nr)).filter(
                (L_price1.artnr == s_artnr)).all():
            if l_price1._recid in l_price1_obj_list:
                continue
            else:
                l_price1_obj_list.append(l_price1._recid)


            i = i + 1
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.counter = i

            if not long_digit:
                output_list.str = \
                        to_string(l_price1.bestelldatum, "99/99/99") + " " +\
                        to_string(l_supply.firma, "x(24)") + " " +\
                        to_string(l_price1.docu_nr, "x(16)") + " " +\
                        to_string(l_art1.traubensort, "x(9)") + " " +\
                        to_string(l_art1.lief_einheit, ">>>,>>9") + " " +\
                        to_string(l_price1.anzahl) + " " +\
                        to_string(l_price1.einzelpreis, "->>,>>>,>>9.99") + " " +\
                        to_string(l_price1.warenwert, "->>,>>>,>>9.99")


                total_anzahl = total_anzahl + l_price1.anzahl
                total_einzelpreis = total_einzelpreis + l_price1.einzelpreis
                total_warenwert = total_warenwert + l_price1.warenwert

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_price1.docu_nr) &  (L_order.lief_nr == l_price1.lief_nr) &  (L_order.artnr == s_artnr)).first()

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")
            else:
                output_list.str = \
                        to_string(l_price1.bestelldatum, "99/99/99") + " " +\
                        to_string(l_supply.firma, "x(24)") + " " +\
                        to_string(l_price1.docu_nr, "x(16)") + " " +\
                        to_string(l_art1.traubensort, "x(9)") + " " +\
                        to_string(l_art1.lief_einheit, ">>>,>>9") + " " +\
                        to_string(l_price1.anzahl) + " " +\
                        to_string(l_price1.einzelpreis, "->,>>>,>>>,>>9") + " " +\
                        to_string(l_price1.warenwert, "->,>>>,>>>,>>9")


                total_anzahl = total_anzahl + l_price1.anzahl
                total_einzelpreis = total_einzelpreis + l_price1.einzelpreis
                total_warenwert = total_warenwert + l_price1.warenwert

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_price1.docu_nr) &  (L_order.lief_nr == l_price1.lief_nr) &  (L_order.artnr == s_artnr)).first()

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")

    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.str = '~n' + "T o t a l" + to_string(" ", "x(60)") + to_string(total_anzahl, "9999") + to_string(total_einzelpreis, "->>,>>>,>>9.99") + to_string(" ", "x(1)") + to_string(total_warenwert, "->>,>>>,>>9.99")
    output_list.counter = i

    return generate_output()