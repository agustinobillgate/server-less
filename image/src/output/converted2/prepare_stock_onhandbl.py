#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, L_artikel, L_bestand, L_lager

def prepare_stock_onhandbl(s_artnr:int):

    prepare_cache ([Htparam, L_artikel, L_bestand, L_lager])

    price_decimal = 0
    artnr = ""
    bezeich = ""
    output_list_list = []
    long_digit:bool = False
    htparam = l_artikel = l_bestand = l_lager = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"l_bezeich":string, "str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, artnr, bezeich, output_list_list, long_digit, htparam, l_artikel, l_bestand, l_lager
        nonlocal s_artnr


        nonlocal output_list
        nonlocal output_list_list

        return {"price_decimal": price_decimal, "artnr": artnr, "bezeich": bezeich, "output-list": output_list_list}

    def soh_list():

        nonlocal price_decimal, artnr, bezeich, output_list_list, long_digit, htparam, l_artikel, l_bestand, l_lager
        nonlocal s_artnr


        nonlocal output_list
        nonlocal output_list_list

        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_init_qty:Decimal = to_decimal("0.0")
        t_init_val:Decimal = to_decimal("0.0")
        t_in_qty:Decimal = to_decimal("0.0")
        t_in_val:Decimal = to_decimal("0.0")
        t_out_qty:Decimal = to_decimal("0.0")
        t_out_val:Decimal = to_decimal("0.0")
        t_end_qty:Decimal = to_decimal("0.0")
        t_end_val:Decimal = to_decimal("0.0")
        l_oh = None
        t_qty:Decimal = to_decimal("0.0")
        t_wert:Decimal = to_decimal("0.0")
        adjust:Decimal = to_decimal("0.0")
        value_in:Decimal = to_decimal("0.0")
        value_out:Decimal = to_decimal("0.0")
        L_oh =  create_buffer("L_oh",L_bestand)

        l_oh = get_cache (L_bestand, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, 0)]})

        if l_oh:
            t_qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
            t_wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

        elif not l_oh:

            return

        l_lager_obj_list = {}
        l_lager = L_lager()
        l_bestand = L_bestand()
        for l_lager.bezeich, l_lager.lager_nr, l_lager._recid, l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand.wert_eingang, l_bestand.wert_ausgang, l_bestand.anf_best_dat, l_bestand._recid in db_session.query(L_lager.bezeich, L_lager.lager_nr, L_lager._recid, L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand.wert_eingang, L_bestand.wert_ausgang, L_bestand.anf_best_dat, L_bestand._recid).join(L_bestand,(L_bestand.artnr == s_artnr) & (L_bestand.lager_nr == L_lager.lager_nr)).order_by(L_lager._recid).all():
            if l_lager_obj_list.get(l_lager._recid):
                continue
            else:
                l_lager_obj_list[l_lager._recid] = True


            qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            t_end_qty =  to_decimal(t_end_qty) + to_decimal(qty)

            if t_qty != 0:
                val =  to_decimal(t_wert) * to_decimal(qty) / to_decimal(t_qty)
            else:
                val =  to_decimal("0")
            adjust =  to_decimal(val) - to_decimal(l_bestand.val_anf_best) - to_decimal(l_bestand.wert_eingang) +\
                    l_bestand.wert_ausgang
            value_in =  to_decimal(l_bestand.wert_eingang)
            value_out =  to_decimal(l_bestand.wert_ausgang)


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.l_bezeich = l_lager.bezeich
            str = to_string(l_lager.lager_nr, "99")

            if l_bestand.anf_best_dat != None:
                str = str + to_string(l_bestand.anf_best_dat, "99/99/99")
            else:
                str = str + " "

            if long_digit:
                str = str + to_string(l_bestand.anz_anf_best, "->,>>>,>>9.99") + to_string(l_bestand.val_anf_best, "->,>>>,>>>,>>9") + to_string(l_bestand.anz_eingang, "->,>>>,>>9.99") + to_string(value_in, "->,>>>,>>>,>>9") + to_string(l_bestand.anz_ausgang, "->,>>>,>>9.99") + to_string(value_out, "->,>>>,>>>,>>9") + to_string(adjust, " ->>>,>>>,>>9") + to_string(qty, "->,>>>,>>9.99") + to_string(val, "->,>>>,>>>,>>9")
            else:
                str = str + to_string(l_bestand.anz_anf_best, "->,>>>,>>9.99") + to_string(l_bestand.val_anf_best, "->>,>>>,>>9.99") + to_string(l_bestand.anz_eingang, "->,>>>,>>9.99") + to_string(value_in, "->>,>>>,>>9.99") + to_string(l_bestand.anz_ausgang, "->,>>>,>>9.99") + to_string(value_out, "->>,>>>,>>9.99") + to_string(adjust, "->,>>>,>>9.99") + to_string(qty, "->,>>>,>>9.99") + to_string(val, "->>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)


        if long_digit:
            str = to_string("", "x(2)") + to_string("TOTAL", "x(8)") + to_string(l_oh.anz_anf_best, "->,>>>,>>9.99") + to_string(l_oh.val_anf_best, "->,>>>,>>>,>>9") + to_string(l_oh.anz_eingang, "->,>>>,>>9.99") + to_string(l_oh.wert_eingang, "->,>>>,>>>,>>9") + to_string(l_oh.anz_ausgang, "->,>>>,>>9.99") + to_string(l_oh.wert_ausgang, "->,>>>,>>>,>>9") + to_string(0, "->,>>>,>>9.99") + to_string(t_qty, "->,>>>,>>9.99") + to_string(t_wert, "->,>>>,>>>,>>9")
        else:
            str = to_string("", "x(2)") + to_string("TOTAL", "x(8)") + to_string(l_oh.anz_anf_best, "->,>>>,>>9.99") + to_string(l_oh.val_anf_best, "->>,>>>,>>9.99") + to_string(l_oh.anz_eingang, "->,>>>,>>9.99") + to_string(l_oh.wert_eingang, "->>,>>>,>>9.99") + to_string(l_oh.anz_ausgang, "->,>>>,>>9.99") + to_string(l_oh.wert_ausgang, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(t_qty, "->,>>>,>>9.99") + to_string(t_wert, "->>,>>>,>>9.99")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if not l_artikel:

        return generate_output()
    artnr = to_string(l_artikel.artnr, "9999999")
    bezeich = l_artikel.bezeich


    soh_list()

    return generate_output()