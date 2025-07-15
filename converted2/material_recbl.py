#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, H_artikel, L_bestand, L_besthis, Gl_acct, L_lager, L_artikel, L_untergrup, L_op, H_bill_line

def material_recbl(pvilanguage:int, from_date:date, to_date:date, from_grp:int, lager_no:int, from_main:int, to_main:int):

    prepare_cache ([Htparam, Waehrung, H_artikel, L_bestand, L_lager, L_artikel, L_untergrup, L_op, H_bill_line])

    mtreconsile_list_data = []
    curr_nr:int = 0
    curr_reihe:int = 0
    ldry:int = 0
    dstore:int = 0
    long_digit:bool = False
    foreign_nr:int = 0
    exchg_rate:Decimal = 1
    double_currency:bool = False
    type_of_acct:int = 0
    counter:int = 0
    coa_format:string = ""
    f_date:date = None
    lvcarea:string = "fb-reconsile"
    htparam = waehrung = h_artikel = l_bestand = l_besthis = gl_acct = l_lager = l_artikel = l_untergrup = l_op = h_bill_line = None

    mtreconsile_list = s_list = None

    mtreconsile_list_data, Mtreconsile_list = create_model("Mtreconsile_list", {"nr":int, "code":int, "bezeich":string, "col1":string, "col2":string, "col3":string, "col4":string, "col5":string})
    s_list_data, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":string, "fibukonto":string, "bezeich":string, "flag":int, "anf_wert":Decimal, "end_wert":Decimal, "betrag":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mtreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_untergrup, l_op, h_bill_line
        nonlocal pvilanguage, from_date, to_date, from_grp, lager_no, from_main, to_main


        nonlocal mtreconsile_list, s_list
        nonlocal mtreconsile_list_data, s_list_data

        return {"mtreconsile-list": mtreconsile_list_data}

    def create_list():

        nonlocal mtreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_untergrup, l_op, h_bill_line
        nonlocal pvilanguage, from_date, to_date, from_grp, lager_no, from_main, to_main


        nonlocal mtreconsile_list, s_list
        nonlocal mtreconsile_list_data, s_list_data

        betrag1:Decimal = to_decimal("0.0")
        betrag2:Decimal = to_decimal("0.0")
        betrag3:Decimal = to_decimal("0.0")
        betrag4:Decimal = to_decimal("0.0")
        betrag5:Decimal = to_decimal("0.0")
        betrag6:Decimal = to_decimal("0.0")
        betrag61:Decimal = to_decimal("0.0")
        betrag62:Decimal = to_decimal("0.0")
        betrag56:Decimal = to_decimal("0.0")
        consume2:Decimal = to_decimal("0.0")
        flag:int = 0
        m_cost:Decimal = to_decimal("0.0")
        m_ratio:Decimal = to_decimal("0.0")
        fibu:string = ""
        m_sales:Decimal = to_decimal("0.0")
        mm_sales:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        i:int = 0
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        qty1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        j:int = 0
        qty0:Decimal = to_decimal("0.0")
        val0:Decimal = to_decimal("0.0")
        l_oh = None
        l_ohist = None
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_bestand)
        L_ohist =  create_buffer("L_ohist",L_besthis)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        s_list_data.clear()
        mtreconsile_list_data.clear()
        curr_nr = 0
        curr_reihe = 0
        flag = 1

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, lager_no)]})

        if l_lager:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_bestand.artnr, l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand._recid, l_artikel.artnr, l_artikel.vk_preis, l_artikel._recid, l_untergrup.fibukonto, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_bestand.artnr, L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand._recid, L_artikel.artnr, L_artikel.vk_preis, L_artikel._recid, L_untergrup.fibukonto, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum >= from_main) & (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_untergrup.fibukonto, L_artikel.artnr).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                l_oh = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_bestand.artnr)]})
                qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                qty0 =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
                val0 =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

                if qty0 != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal((qty) / to_decimal(qty0)) * to_decimal(val0)
                s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.val_anf_best)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art <= 2) & (L_op.lager_nr == lager_no) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                    if l_op.op_art == 1:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == l_untergrup.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.fibukonto = l_untergrup.fibukonto
                    s_list.bezeich = l_untergrup.bezeich
                    s_list.flag = 4

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art >= 3) & (L_op.op_art <= 4) & (L_op.lager_nr == l_lager.lager_nr) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                    if l_op.op_art == 3:
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
                    else:
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
        else:

            for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

                l_bestand_obj_list = {}
                l_bestand = L_bestand()
                l_artikel = L_artikel()
                l_untergrup = L_untergrup()
                for l_bestand.artnr, l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand._recid, l_artikel.artnr, l_artikel.vk_preis, l_artikel._recid, l_untergrup.fibukonto, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_bestand.artnr, L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand._recid, L_artikel.artnr, L_artikel.vk_preis, L_artikel._recid, L_untergrup.fibukonto, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum >= from_main) & (L_artikel.endkum <= to_main)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_untergrup.fibukonto, L_artikel.artnr).all():
                    if l_bestand_obj_list.get(l_bestand._recid):
                        continue
                    else:
                        l_bestand_obj_list[l_bestand._recid] = True

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.reihenfolge = flag
                        s_list.lager_nr = l_lager.lager_nr
                        s_list.l_bezeich = l_lager.bezeich
                        s_list.flag = 0

                    l_oh = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_bestand.artnr)]})
                    qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                    qty0 =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
                    val0 =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

                    if qty0 != 0:
                        s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal((qty) / to_decimal(qty0)) * to_decimal(val0)
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.val_anf_best)

                    for l_op in db_session.query(L_op).filter(
                             (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art <= 2) & (L_op.lager_nr == l_lager.lager_nr) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                        if l_op.op_art == 1:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.lager_nr = l_lager.lager_nr
                                s_list.l_bezeich = l_lager.bezeich
                                s_list.flag = 11
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == l_untergrup.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.reihenfolge = 1
                        s_list.fibukonto = l_untergrup.fibukonto
                        s_list.bezeich = l_untergrup.bezeich
                        s_list.flag = 4

                    for l_op in db_session.query(L_op).filter(
                             (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art >= 3) & (L_op.op_art <= 4) & (L_op.lager_nr == l_lager.lager_nr) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                        if l_op.op_art == 3:
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
                        else:
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.anzahl) * to_decimal(l_artikel.vk_preis)
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list.col2 = to_string(translateExtended ("** MATERIAL **", lvcarea, "") , "x(33)")
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        i = 0
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        betrag1 =  to_decimal("0")
        mtreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                mtreconsile_list = Mtreconsile_list()
                mtreconsile_list_data.append(mtreconsile_list)

                curr_nr = curr_nr + 1
                mtreconsile_list.nr = curr_nr
                mtreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                mtreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.anf_wert, " ->>>,>>>,>>9.99")


            else:
                mtreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.anf_wert, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr

        if not long_digit:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag1, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag1, " ->>,>>>,>>>,>>9")


        i = 0
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                mtreconsile_list = Mtreconsile_list()
                mtreconsile_list_data.append(mtreconsile_list)

                curr_nr = curr_nr + 1
                mtreconsile_list.nr = curr_nr
                mtreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                mtreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.betrag, " ->>>,>>>,>>9.99")


            else:
                mtreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.betrag, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr

        if not long_digit:
            mtreconsile_list.col2 = to_string("", "x(24)") + translateExtended ("SUB TOTAL", lvcarea, "")
            mtreconsile_list.col4 = to_string(betrag2, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag2, " ->>,>>>,>>>,>>9")


        i = 0
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag4)

        if not long_digit:
            mtreconsile_list.col1 = to_string(translateExtended ("3. Inventory Available", lvcarea, "") , "x(24)")
            mtreconsile_list.col2 = to_string("(1 + 2)", "x(33)")
            mtreconsile_list.col4 = to_string(betrag4, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col1 = to_string(translateExtended ("3. Inventory Available", lvcarea, "") , "x(24)")
            mtreconsile_list.col2 = to_string("(1 + 2)", "x(33)")
            mtreconsile_list.col4 = to_string(betrag4, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        i = 0
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list.col1 = to_string(translateExtended ("4. Closing Inventory", lvcarea, "") , "x(24)")


        betrag5 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                mtreconsile_list = Mtreconsile_list()
                mtreconsile_list_data.append(mtreconsile_list)

                curr_nr = curr_nr + 1
                mtreconsile_list.nr = curr_nr
                mtreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                mtreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.end_wert, " ->>>,>>>,>>9.99")


            else:
                mtreconsile_list.col2 = to_string(s_list.l_bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.end_wert, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr

        if not long_digit:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag5, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag5, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            mtreconsile_list.col1 = to_string(translateExtended ("5. Gross Consumption", lvcarea, "") , "x(24)")
            mtreconsile_list.col2 = to_string("(3 - 4)", "x(33)")
            mtreconsile_list.col4 = to_string(betrag56, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col1 = to_string(translateExtended ("5. Gross Consumption", lvcarea, "") , "x(24)")
            mtreconsile_list.col2 = to_string("(3 - 4)", "x(33)")
            mtreconsile_list.col4 = to_string(betrag56, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        mtreconsile_list.col1 = to_string(translateExtended ("6. Consumed", lvcarea, "") , "x(24)")
        betrag6 =  to_decimal("0")
        counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                mtreconsile_list = Mtreconsile_list()
                mtreconsile_list_data.append(mtreconsile_list)

                mtreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    mtreconsile_list.code = s_list.code
                else:
                    mtreconsile_list.code = counter
                mtreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                mtreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.betrag, " ->>>,>>>,>>9.99")


            else:
                mtreconsile_list.col2 = to_string(s_list.bezeich, "x(33)")
                mtreconsile_list.col3 = to_string(s_list.betrag, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr

        if not long_digit:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag6, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            mtreconsile_list.col4 = to_string(betrag6, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr

        if not long_digit:
            mtreconsile_list.col1 = to_string(translateExtended ("7. Net Consumption", lvcarea, "") , "x(24)")
            mtreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            mtreconsile_list.col4 = to_string(consume2, " ->>>,>>>,>>9.99")


        else:
            mtreconsile_list.col1 = to_string(translateExtended ("7. Net Consumption", lvcarea, "") , "x(24)")
            mtreconsile_list.col2 = to_string("(5 - 6)", "x(33)")
            mtreconsile_list.col4 = to_string(consume2, " ->>,>>>,>>>,>>9")


        mtreconsile_list = Mtreconsile_list()
        mtreconsile_list_data.append(mtreconsile_list)

        curr_nr = curr_nr + 1
        mtreconsile_list.nr = curr_nr


    def cost_correction(cost:Decimal):

        nonlocal mtreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_untergrup, l_op, h_bill_line
        nonlocal pvilanguage, from_date, to_date, from_grp, lager_no, from_main, to_main


        nonlocal mtreconsile_list, s_list
        nonlocal mtreconsile_list_data, s_list_data

        def generate_inner_output():
            return (cost)


        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_compli.rechnr)],"bill_datum": [(eq, h_compli.datum)],"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)],"epreis": [(eq, h_compli.epreis)]})

        if h_bill_line and substring(h_bill_line.bezeich, length(h_bill_line.bezeich) - 1, 1) == ("*").lower()  and h_bill_line.epreis != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if h_artikel and h_artikel.artart == 0 and h_artikel.epreis1 > h_bill_line.epreis:
                cost =  to_decimal(cost) * to_decimal(h_bill_line.epreis) / to_decimal(h_artikel.epreis1)

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
    ldry = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
    dstore = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    coa_format = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam.flogical:
        double_currency = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")
    create_list()

    return generate_output()