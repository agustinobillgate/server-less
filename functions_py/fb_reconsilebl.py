#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 30/7/2025
# gitlab: 
# if available gl_acct
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_artikel, L_bestand, L_besthis, Gl_acct, L_lager, L_artikel, L_op, L_ophdr, Hoteldpt, H_compli, Exrate, Artikel, Gl_main, H_cost, Umsatz, H_bill_line

def fb_reconsilebl(pvilanguage:int, case_type:int, from_date:date, to_date:date, from_grp:int, mi_opt:bool, date1:date, date2:date):

    prepare_cache ([Htparam, Waehrung, H_artikel, L_bestand, Gl_acct, L_lager, L_artikel, L_op, Hoteldpt, H_compli, Exrate, Artikel, Gl_main, H_cost, Umsatz, H_bill_line])

    done = False
    fbreconsile_list_data = []
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
    htparam = waehrung = h_artikel = l_bestand = l_besthis = gl_acct = l_lager = l_artikel = l_op = l_ophdr = hoteldpt = h_compli = exrate = artikel = gl_main = h_cost = umsatz = h_bill_line = None

    fbreconsile_list = s_list = None

    fbreconsile_list_data, Fbreconsile_list = create_model("Fbreconsile_list", {"nr":int, "code":int, "bezeich":string, "col1":string, "col2":string, "col3":string, "col4":string, "col5":string})
    s_list_data, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":string, "fibukonto":string, "bezeich":string, "flag":int, "anf_wert":Decimal, "end_wert":Decimal, "betrag":Decimal}, {"reihenfolge": 1, "flag": 2})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, fbreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal pvilanguage, case_type, from_date, to_date, from_grp, mi_opt, date1, date2


        nonlocal fbreconsile_list, s_list
        nonlocal fbreconsile_list_data, s_list_data

        return {"done": done, "fbreconsile-list": fbreconsile_list_data}

    def create_list():

        nonlocal done, fbreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal pvilanguage, case_type, from_date, to_date, from_grp, mi_opt, date1, date2


        nonlocal fbreconsile_list, s_list
        nonlocal fbreconsile_list_data, s_list_data

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
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        f_sales:Decimal = to_decimal("0.0")
        b_sales:Decimal = to_decimal("0.0")
        tf_sales:Decimal = to_decimal("0.0")
        tb_sales:Decimal = to_decimal("0.0")
        f_ratio:Decimal = to_decimal("0.0")
        b_ratio:Decimal = to_decimal("0.0")
        fibu:string = ""
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        i:int = 0
        bev_food:string = ""
        food_bev:string = ""
        fb_str:List[string] = ["Beverage TO Food", "Food to Beverage"]
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        qty1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_oh = None
        l_ohist = None
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        fb_str[0] = translateExtended ("Beverage to Food", lvcarea, "")
        fb_str[1] = translateExtended ("Food to Beverage", lvcarea, "")
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_bestand)
        L_ohist =  create_buffer("L_ohist",L_besthis)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        s_list_data.clear()
        fbreconsile_list_data.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        fl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        bl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})
        bev_food = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})
        food_bev = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, bev_food)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 1
        s_list.lager_nr = 9999
        
        # Rd 30/7/2025
        # if available
        # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        if gl_acct:
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

        s_list.flag = 0

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        if gl_acct:
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

        s_list.flag = 0

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_oh = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh._recid, l_artikel.artnr, l_artikel.endkum, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh._recid, L_artikel.artnr, L_artikel.endkum, L_artikel._recid).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

                if l_artikel.endkum == fl_eknr:
                    flag = 1

                elif l_artikel.endkum == bl_eknr:
                    flag = 2
                qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
                wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                if l_bestand.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) * to_decimal(l_bestand.val_anf_best) / to_decimal(l_bestand.anz_anf_best)

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                l_op_obj_list = {}
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto)).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True


                    type_of_acct = gl_acct.acc_type
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_op.stornogrund != "":

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)
                    else:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.fibukonto = fibukonto
                            s_list.bezeich = bezeich
                            s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.departement, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli.rechnr, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli.rechnr, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                artikel = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, 0)]})

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

                gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})

                h_artikel = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    f_cost = cost_correction(f_cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                if f_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(f_cost)

                if b_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(b_cost)
        tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)

        if from_grp == 0 or from_grp == 1:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col2 = to_string(translateExtended ("** FOOD **", lvcarea, "") , "x(50)")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_data.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:

                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                else:

                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_data.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:

                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                else:

                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9.99")
            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")
            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_data.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:

                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                else:

                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9.99")
            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

            s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col1 = to_string(("4. " + fb_str[0]) , "x(24)")
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            else:
                fbreconsile_list.col1 = to_string(("4. " + fb_str[0]) , "x(24)")
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
                fbreconsile_list.col3 = to_string("", "x(15)")
                fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9.99")
            else:
                fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
                fbreconsile_list.col3 = to_string("", "x(15)")
                fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            i = 0
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

                if i > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_data.append(fbreconsile_list)

                    curr_nr = curr_nr + 1
                    fbreconsile_list.nr = curr_nr
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9.99")
            else:
                fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
                fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9.99")
            else:
                fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
                fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")

            if mi_opt == False:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_data.append(fbreconsile_list)

                    fbreconsile_list.nr = curr_nr

                    if s_list.code > 0:
                        fbreconsile_list.code = s_list.code
                    else:
                        fbreconsile_list.code = counter
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            if mi_opt == False:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    fbreconsile_list = Fbreconsile_list()
                    fbreconsile_list_data.append(fbreconsile_list)

                    fbreconsile_list.nr = curr_nr

                    if s_list.code > 0:
                        fbreconsile_list.code = s_list.code
                    else:
                        fbreconsile_list.code = counter
                    fbreconsile_list.col1 = to_string("", "x(24)")

                if not long_digit:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                    fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

            if mi_opt == False:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr

                if not long_digit:
                    fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                    fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9.99")


                else:
                    fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
                    fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
                fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
                fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            f_ratio =  to_decimal("0")

            if tf_sales != 0:
                f_ratio = to_decimal(round(consume2 , 2) / round(tf_sales , 2) * 100)

            if f_ratio == None:
                f_ratio =  to_decimal("0")

            if not long_digit:
                fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99")
                fbreconsile_list.col3 = to_string(translateExtended (" cost:Sales", lvcarea, "") , "x(15)")
                fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")


            else:
                fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
                fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9")
                fbreconsile_list.col3 = to_string(translateExtended (" cost:Sales", lvcarea, "") , "x(15)")
                fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")

        if from_grp == 1:

            return
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col2 = to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(50)")
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        betrag1 =  to_decimal("0")
        fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + translateExtended ("SUB TOTAL", lvcarea, "")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        betrag3 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col4 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col4 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(("4. " + fb_str[1]) , "x(24)")
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(("4. " + fb_str[1]) , "x(24)")
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")


        betrag5 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        betrag6 =  to_decimal("0")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("lager_nr",False)]):
            counter = counter + 1
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string("", "x(24)")

        if not long_digit:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        b_ratio =  to_decimal("0")

        if tb_sales != 0:
            b_ratio =  to_decimal(consume2) / to_decimal(tb_sales) * to_decimal("100")

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99")
            fbreconsile_list.col3 = to_string(translateExtended (" cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9")
            fbreconsile_list.col3 = to_string(translateExtended (" cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        done = True


    def create_food():

        nonlocal done, fbreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal pvilanguage, case_type, from_date, to_date, from_grp, mi_opt, date1, date2


        nonlocal fbreconsile_list, s_list
        nonlocal fbreconsile_list_data, s_list_data

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
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        f_sales:Decimal = to_decimal("0.0")
        b_sales:Decimal = to_decimal("0.0")
        tf_sales:Decimal = to_decimal("0.0")
        tb_sales:Decimal = to_decimal("0.0")
        f_ratio:Decimal = to_decimal("0.0")
        b_ratio:Decimal = to_decimal("0.0")
        fibu:string = ""
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        i:int = 0
        bev_food:string = ""
        food_bev:string = ""
        fb_str:List[string] = ["Beverage TO Food", "Food to Beverage"]
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        qty1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_oh = None
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        fb_str[0] = translateExtended ("Beverage to Food", lvcarea, "")
        fb_str[1] = translateExtended ("Food to Beverage", lvcarea, "")
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_bestand)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        curr_nr = 0
        curr_reihe = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        fl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        bl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})
        bev_food = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})
        food_bev = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, bev_food)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 1
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0
        flag = 1

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_oh = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh._recid, l_artikel.artnr, l_artikel.endkum, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh._recid, L_artikel.artnr, L_artikel.endkum, L_artikel._recid).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

                if l_artikel.endkum == fl_eknr:
                    flag = 1

                elif l_artikel.endkum == bl_eknr:
                    flag = 2
                qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
                wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                if l_bestand.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) * to_decimal(l_bestand.val_anf_best) / to_decimal(l_bestand.anz_anf_best)

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                l_op_obj_list = {}
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto)).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True


                    type_of_acct = gl_acct.acc_type

                    gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_op.stornogrund != "":

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                            gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct1.main_nr)]})

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)
                    else:

                        if mi_opt == False:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.fibukonto = fibukonto
                                s_list.bezeich = bezeich
                                s_list.flag = 5
                        else:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich
                                s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.departement, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli.rechnr, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli.rechnr, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                artikel = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, 0)]})

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

                gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})

                h_artikel = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    f_cost = cost_correction(f_cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                if f_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(f_cost)
        tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col2 = to_string(translateExtended ("** FOOD **", lvcarea, "") , "x(50)")
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(("4. " + fb_str[0]) , "x(24)")
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(("4. " + fb_str[0]) , "x(24)")
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string("", "x(24)")

        if not long_digit:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        f_ratio =  to_decimal("0")

        if tf_sales != 0:
            f_ratio = to_decimal(round(consume2 , 2) / round(tf_sales , 2) * 100)

        if f_ratio == None:
            f_ratio =  to_decimal("0")

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99")
            fbreconsile_list.col3 = to_string(translateExtended (" cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Food Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9")
            fbreconsile_list.col3 = to_string(translateExtended (" cost:Sales", lvcarea, "") , "x(15)")
            fbreconsile_list.col4 = to_string(f_ratio, "->,>>>,>>9.99 %")


        done = True


    def create_beverage():

        nonlocal done, fbreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal pvilanguage, case_type, from_date, to_date, from_grp, mi_opt, date1, date2


        nonlocal fbreconsile_list, s_list
        nonlocal fbreconsile_list_data, s_list_data

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
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        f_sales:Decimal = to_decimal("0.0")
        b_sales:Decimal = to_decimal("0.0")
        tf_sales:Decimal = to_decimal("0.0")
        tb_sales:Decimal = to_decimal("0.0")
        f_ratio:Decimal = to_decimal("0.0")
        b_ratio:Decimal = to_decimal("0.0")
        fibu:string = ""
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        i:int = 0
        bev_food:string = ""
        food_bev:string = ""
        fb_str:List[string] = ["Beverage TO Food", "Food to Beverage"]
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        qty1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_oh = None
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        fb_str[0] = translateExtended ("Beverage to Food", lvcarea, "")
        fb_str[1] = translateExtended ("Food to Beverage", lvcarea, "")
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_bestand)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        s_list_data.clear()
        fbreconsile_list_data.clear()
        curr_nr = 0
        curr_reihe = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        fl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        bl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})
        bev_food = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})
        food_bev = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, bev_food)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 1
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
        s_list.flag = 0
        flag = 2

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_oh = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand.val_anf_best, l_bestand._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh._recid, l_artikel.artnr, l_artikel.endkum, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand.val_anf_best, L_bestand._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh._recid, L_artikel.artnr, L_artikel.endkum, L_artikel._recid).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

                if l_artikel.endkum == fl_eknr:
                    flag = 1

                elif l_artikel.endkum == bl_eknr:
                    flag = 2
                qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)
                wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                if l_bestand.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) * to_decimal(l_bestand.val_anf_best) / to_decimal(l_bestand.anz_anf_best)

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                l_op_obj_list = {}
                for l_op, l_ophdr, gl_acct in db_session.query(L_op, L_ophdr, Gl_acct).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto)).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():
                    if l_op_obj_list.get(l_op._recid):
                        continue
                    else:
                        l_op_obj_list[l_op._recid] = True


                    type_of_acct = gl_acct.acc_type

                    gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})
                    fibukonto = gl_acct.fibukonto
                    bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()

                    if l_op.stornogrund != "":

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type

                            gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct1.main_nr)]})
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()

                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)
                    else:

                        if mi_opt == False:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.fibukonto = fibukonto
                                s_list.bezeich = bezeich
                                s_list.flag = 5
                        else:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = flag
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich
                                s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.datum, h_compli.departement, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli.rechnr, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.epreis1, h_art.artart, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli.rechnr, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.epreis1, H_art.artart, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                if h_compli_obj_list.get(h_compli._recid):
                    continue
                else:
                    h_compli_obj_list[h_compli._recid] = True

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_datum)]})
                    else:

                        exrate = get_cache (Exrate, {"datum": [(eq, curr_datum)]})

                    if exrate:
                        rate =  to_decimal(exrate.betrag)
                    else:
                        rate =  to_decimal(exchg_rate)

                artikel = get_cache (Artikel, {"artnr": [(eq, h_art.artnrfront)],"departement": [(eq, 0)]})

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

                gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})

                h_artikel = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                    f_cost = cost_correction(f_cost)

                elif not h_cost or (h_cost and h_cost.betrag == 0):

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                if b_cost != 0:

                    if mi_opt == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.fibukonto = gl_acct.fibukonto
                            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.flag = 4
                    else:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.code = gl_main.code
                            s_list.bezeich = gl_main.bezeich
                            s_list.flag = 4
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(b_cost)
        tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col2 = to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(50)")
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        betrag1 =  to_decimal("0")
        fbreconsile_list.col1 = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag1, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        betrag2 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag2, "->>,>>>,>>>,>>9")


        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        betrag3 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag3, "->>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(("4. " + fb_str[1]) , "x(24)")
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(("4. " + fb_str[1]) , "x(24)")
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col4 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(1 + 2 + 3 + 4)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag4, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        i = 0
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        betrag5 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                curr_nr = curr_nr + 1
                fbreconsile_list.nr = curr_nr
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.end_wert, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag5, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(5 - 6)", "x(50)")
            fbreconsile_list.col4 = to_string(betrag56, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        betrag6 =  to_decimal("0")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Compliment cost", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
            fbreconsile_list.col1 = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("lager_nr",False)]):
            counter = counter + 1
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)

            if counter > 1:
                fbreconsile_list = Fbreconsile_list()
                fbreconsile_list_data.append(fbreconsile_list)

                fbreconsile_list.nr = curr_nr

                if s_list.code > 0:
                    fbreconsile_list.code = s_list.code
                else:
                    fbreconsile_list.code = counter
                fbreconsile_list.col1 = to_string("", "x(24)")

            if not long_digit:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")


            else:
                fbreconsile_list.col2 = to_string(s_list.bezeich, "x(50)")
                fbreconsile_list.col3 = to_string(s_list.betrag, "->>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list.col1 = to_string("", "x(24)")

        if not long_digit:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string(s_list.l_bezeich, "x(50)")
            fbreconsile_list.col3 = to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")


        betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

        if mi_opt == False:
            fbreconsile_list = Fbreconsile_list()
            fbreconsile_list_data.append(fbreconsile_list)

            curr_nr = curr_nr + 1
            fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col2 = to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)")
            fbreconsile_list.col4 = to_string(betrag6, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9.99")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("(7 - 8)", "x(50)")
            fbreconsile_list.col4 = to_string(consume2, "->>,>>>,>>>,>>9")


        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        fbreconsile_list = Fbreconsile_list()
        fbreconsile_list_data.append(fbreconsile_list)

        curr_nr = curr_nr + 1
        fbreconsile_list.nr = curr_nr
        b_ratio =  to_decimal("0")

        if tb_sales != 0:
            b_ratio =  to_decimal(consume2) / to_decimal(tb_sales) * to_decimal("100")

        if not long_digit:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99")
            fbreconsile_list.col3 = to_string(" cost:Sales", "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        else:
            fbreconsile_list.col1 = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)")
            fbreconsile_list.col2 = to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9")
            fbreconsile_list.col3 = to_string(" cost:Sales", "x(15)")
            fbreconsile_list.col4 = to_string(b_ratio, "->,>>>,>>9.99 %")


        done = True


    def fb_sales(f_eknr:int, b_eknr:int):

        nonlocal done, fbreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal pvilanguage, case_type, from_date, to_date, from_grp, mi_opt, date1, date2


        nonlocal fbreconsile_list, s_list
        nonlocal fbreconsile_list_data, s_list_data

        tf_sales = to_decimal("0.0")
        tb_sales = to_decimal("0.0")
        f_sales:Decimal = to_decimal("0.0")
        b_sales:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        serv_taxable:bool = False

        def generate_inner_output():
            return (tf_sales, tb_sales)

        f_sales =  to_decimal("0")
        b_sales =  to_decimal("0")
        tf_sales =  to_decimal("0")
        tb_sales =  to_decimal("0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_taxable = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == f_eknr) | (Artikel.endkum == b_eknr) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5) | (Artikel.umsatzart == 6))).order_by(Artikel._recid).all():

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.datum >= date1) & (Umsatz.datum <= date2) & (Umsatz.departement == artikel.departement) & (Umsatz.artnr == artikel.artnr)).order_by(Umsatz._recid).all():
                    h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                    h_mwst =  to_decimal(h_mwst) + to_decimal(vat2)


                    amount =  to_decimal(umsatz.betrag) / to_decimal(fact)

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales =  to_decimal(f_sales) + to_decimal(amount)
                        tf_sales =  to_decimal(tf_sales) + to_decimal(amount)

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales =  to_decimal(b_sales) + to_decimal(amount)
                        tb_sales =  to_decimal(tb_sales) + to_decimal(amount)

        return generate_inner_output()


    def cost_correction(cost:Decimal):

        nonlocal done, fbreconsile_list_data, curr_nr, curr_reihe, ldry, dstore, long_digit, foreign_nr, exchg_rate, double_currency, type_of_acct, counter, coa_format, f_date, lvcarea, htparam, waehrung, h_artikel, l_bestand, l_besthis, gl_acct, l_lager, l_artikel, l_op, l_ophdr, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, umsatz, h_bill_line
        nonlocal pvilanguage, case_type, from_date, to_date, from_grp, mi_opt, date1, date2


        nonlocal fbreconsile_list, s_list
        nonlocal fbreconsile_list_data, s_list_data

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

    if case_type == 0:
        create_list()

    elif case_type == 1:
        create_food()

    elif case_type == 2:
        create_beverage()

    return generate_output()