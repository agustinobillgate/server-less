#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_pprice, L_lieferant, L_artikel, Htparam, L_order

def pchase_book_printbl(sorttype:int, s_artnr:int):

    prepare_cache ([L_pprice, Htparam, L_order])

    output_list_data = []
    total_anzahl:int = 0
    total_einzelpreis:Decimal = to_decimal("0.0")
    total_warenwert:Decimal = to_decimal("0.0")
    i:int = 0
    long_digit:bool = False
    curr_remark:string = ""
    l_pprice = l_lieferant = l_artikel = htparam = l_order = None

    output_list = l_price1 = l_supply = l_art1 = None

    output_list_data, Output_list = create_model("Output_list", {"counter":int, "str":string, "pos":int}, {"pos": 1})

    L_price1 = create_buffer("L_price1",L_pprice)
    L_supply = create_buffer("L_supply",L_lieferant)
    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, total_anzahl, total_einzelpreis, total_warenwert, i, long_digit, curr_remark, l_pprice, l_lieferant, l_artikel, htparam, l_order
        nonlocal sorttype, s_artnr
        nonlocal l_price1, l_supply, l_art1


        nonlocal output_list, l_price1, l_supply, l_art1
        nonlocal output_list_data

        return {"output-list": output_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if sorttype == 1:

        l_price1_obj_list = {}
        for l_price1, l_art1, l_supply in db_session.query(L_price1, L_art1, L_supply).join(L_art1,(L_art1.artnr == L_price1.artnr)).join(L_supply,(L_supply.lief_nr == L_price1.lief_nr)).filter(
                 (L_price1.artnr == s_artnr)).order_by(L_price1.bestelldatum.desc(), L_price1.einzelpreis).all():
            if l_price1_obj_list.get(l_price1._recid):
                continue
            else:
                l_price1_obj_list[l_price1._recid] = True


            i = i + 1
            output_list = Output_list()
            output_list_data.append(output_list)

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
                total_einzelpreis =  to_decimal(total_einzelpreis) + to_decimal(l_price1.einzelpreis)
                total_warenwert =  to_decimal(total_warenwert) + to_decimal(l_price1.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_price1.docu_nr)],"lief_nr": [(eq, l_price1.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr_unicode(10) , ";")
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
                total_einzelpreis =  to_decimal(total_einzelpreis) + to_decimal(l_price1.einzelpreis)
                total_warenwert =  to_decimal(total_warenwert) + to_decimal(l_price1.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_price1.docu_nr)],"lief_nr": [(eq, l_price1.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr_unicode(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")


    elif sorttype == 2:

        l_price1_obj_list = {}
        for l_price1, l_art1, l_supply in db_session.query(L_price1, L_art1, L_supply).join(L_art1,(L_art1.artnr == L_price1.artnr)).join(L_supply,(L_supply.lief_nr == L_price1.lief_nr)).filter(
                 (L_price1.artnr == s_artnr)).order_by(L_supply.firma, L_price1.bestelldatum.desc()).all():
            if l_price1_obj_list.get(l_price1._recid):
                continue
            else:
                l_price1_obj_list[l_price1._recid] = True


            i = i + 1
            output_list = Output_list()
            output_list_data.append(output_list)

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
                total_einzelpreis =  to_decimal(total_einzelpreis) + to_decimal(l_price1.einzelpreis)
                total_warenwert =  to_decimal(total_warenwert) + to_decimal(l_price1.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_price1.docu_nr)],"lief_nr": [(eq, l_price1.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr_unicode(10) , ";")
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
                total_einzelpreis =  to_decimal(total_einzelpreis) + to_decimal(l_price1.einzelpreis)
                total_warenwert =  to_decimal(total_warenwert) + to_decimal(l_price1.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_price1.docu_nr)],"lief_nr": [(eq, l_price1.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr_unicode(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")


    elif sorttype == 3:

        l_price1_obj_list = {}
        for l_price1, l_art1, l_supply in db_session.query(L_price1, L_art1, L_supply).join(L_art1,(L_art1.artnr == L_price1.artnr)).join(L_supply,(L_supply.lief_nr == L_price1.lief_nr)).filter(
                 (L_price1.artnr == s_artnr)).order_by(L_price1.einzelpreis, L_price1.bestelldatum).all():
            if l_price1_obj_list.get(l_price1._recid):
                continue
            else:
                l_price1_obj_list[l_price1._recid] = True


            i = i + 1
            output_list = Output_list()
            output_list_data.append(output_list)

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
                total_einzelpreis =  to_decimal(total_einzelpreis) + to_decimal(l_price1.einzelpreis)
                total_warenwert =  to_decimal(total_warenwert) + to_decimal(l_price1.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_price1.docu_nr)],"lief_nr": [(eq, l_price1.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr_unicode(10) , ";")
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
                total_einzelpreis =  to_decimal(total_einzelpreis) + to_decimal(l_price1.einzelpreis)
                total_warenwert =  to_decimal(total_warenwert) + to_decimal(l_price1.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_price1.docu_nr)],"lief_nr": [(eq, l_price1.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    curr_remark = replace_str(l_order.besteller, chr_unicode(10) , ";")
                    output_list.str = output_list.str + " " + to_string(curr_remark, "x(32)")

    output_list = Output_list()
    output_list_data.append(output_list)

    output_list.str = '~n' + "T o t a l" + to_string(" ", "x(60)") + to_string(total_anzahl, "9999") + to_string(total_einzelpreis, "->>,>>>,>>9.99") + to_string(" ", "x(1)") + to_string(total_warenwert, "->>,>>>,>>9.99")
    output_list.counter = i

    return generate_output()