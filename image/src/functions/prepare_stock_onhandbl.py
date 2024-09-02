from functions.additional_functions import *
import decimal
from models import Htparam, L_artikel, L_bestand, L_lager

def prepare_stock_onhandbl(s_artnr:int):
    price_decimal = 0
    artnr = ""
    bezeich = ""
    output_list_list = []
    long_digit:bool = False
    htparam = l_artikel = l_bestand = l_lager = None

    output_list = l_oh = None

    output_list_list, Output_list = create_model("Output_list", {"l_bezeich":str, "str":str})

    L_oh = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, artnr, bezeich, output_list_list, long_digit, htparam, l_artikel, l_bestand, l_lager
        nonlocal l_oh


        nonlocal output_list, l_oh
        nonlocal output_list_list
        return {"price_decimal": price_decimal, "artnr": artnr, "bezeich": bezeich, "output-list": output_list_list}

    def soh_list():

        nonlocal price_decimal, artnr, bezeich, output_list_list, long_digit, htparam, l_artikel, l_bestand, l_lager
        nonlocal l_oh


        nonlocal output_list, l_oh
        nonlocal output_list_list

        qty:decimal = 0
        val:decimal = 0
        t_init_qty:decimal = 0
        t_init_val:decimal = 0
        t_in_qty:decimal = 0
        t_in_val:decimal = 0
        t_out_qty:decimal = 0
        t_out_val:decimal = 0
        t_end_qty:decimal = 0
        t_end_val:decimal = 0
        t_qty:decimal = 0
        t_wert:decimal = 0
        adjust:decimal = 0
        value_in:decimal = 0
        value_out:decimal = 0
        L_oh = L_bestand

        l_oh = db_session.query(L_oh).filter(
                (L_oh.artnr == s_artnr) &  (L_oh.lager_nr == 0)).first()

        if l_oh:
            t_qty = l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang
            t_wert = l_oh.val_anf_best + l_oh.wert_eingang - l_oh.wert_ausgang

        elif not l_oh:

            return

        l_lager_obj_list = []
        for l_lager, l_bestand in db_session.query(L_lager, L_bestand).join(L_bestand,(L_bestand.artnr == s_artnr) &  (L_bestand.lager_nr == L_lager.lager_nr)).all():
            if l_lager._recid in l_lager_obj_list:
                continue
            else:
                l_lager_obj_list.append(l_lager._recid)


            qty = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            t_end_qty = t_end_qty + qty

            if t_qty != 0:
                val = t_wert * qty / t_qty
            else:
                val = 0
            adjust = val - l_bestand.val_anf_best - l_bestand.wert_eingang +\
                    l_bestand.wert_ausgang
            value_in = l_bestand.wert_eingang
            value_out = l_bestand.wert_ausgang


            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.l_bezeich = l_lager.bezeich
            STR = to_string(l_lager.lager_nr, "99")

            if l_bestand.anf_best_dat != None:
                STR = STR + to_string(l_bestand.anf_best_dat, "99/99/99")
            else:
                STR = STR + "        "

            if long_digit:
                STR = STR + to_string(l_bestand.anz_anf_best, "->,>>>,>>9.99") + to_string(l_bestand.val_anf_best, "->,>>>,>>>,>>9") + to_string(l_bestand.anz_eingang, "->,>>>,>>9.99") + to_string(value_in, "->,>>>,>>>,>>9") + to_string(l_bestand.anz_ausgang, "->,>>>,>>9.99") + to_string(value_out, "->,>>>,>>>,>>9") + to_string(adjust, " ->>>,>>>,>>9") + to_string(qty, "->,>>>,>>9.99") + to_string(val, "->,>>>,>>>,>>9")
            else:
                STR = STR + to_string(l_bestand.anz_anf_best, "->,>>>,>>9.99") + to_string(l_bestand.val_anf_best, "->>,>>>,>>9.99") + to_string(l_bestand.anz_eingang, "->,>>>,>>9.99") + to_string(value_in, "->>,>>>,>>9.99") + to_string(l_bestand.anz_ausgang, "->,>>>,>>9.99") + to_string(value_out, "->>,>>>,>>9.99") + to_string(adjust, "->,>>>,>>9.99") + to_string(qty, "->,>>>,>>9.99") + to_string(val, "->>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)


        if long_digit:
            STR = to_string("", "x(2)") + to_string("TOTAL", "x(8)") + to_string(l_oh.anz_anf_best, "->,>>>,>>9.99") + to_string(l_oh.val_anf_best, "->,>>>,>>>,>>9") + to_string(l_oh.anz_eingang, "->,>>>,>>9.99") + to_string(l_oh.wert_eingang, "->,>>>,>>>,>>9") + to_string(l_oh.anz_ausgang, "->,>>>,>>9.99") + to_string(l_oh.wert_ausgang, "->,>>>,>>>,>>9") + to_string(0, "->,>>>,>>9.99") + to_string(t_qty, "->,>>>,>>9.99") + to_string(t_wert, "->,>>>,>>>,>>9")
        else:
            STR = to_string("", "x(2)") + to_string("TOTAL", "x(8)") + to_string(l_oh.anz_anf_best, "->,>>>,>>9.99") + to_string(l_oh.val_anf_best, "->>,>>>,>>9.99") + to_string(l_oh.anz_eingang, "->,>>>,>>9.99") + to_string(l_oh.wert_eingang, "->>,>>>,>>9.99") + to_string(l_oh.anz_ausgang, "->,>>>,>>9.99") + to_string(l_oh.wert_ausgang, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(t_qty, "->,>>>,>>9.99") + to_string(t_wert, "->>,>>>,>>9.99")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if not l_artikel:

        return generate_output()
    artnr = to_string(l_artikel.artnr, "9999999")
    bezeich = l_artikel.bezeich


    soh_list()

    return generate_output()