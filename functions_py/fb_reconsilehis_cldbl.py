#using conversion tools version: 1.0.0.119
#-----------------------------------------
# Rd 25/7/2025
# gitlab: 
#
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from functions.calc_servvat import calc_servvat
from models import Htparam, Waehrung, H_artikel, L_besthis, Gl_acct, L_lager, L_ophis, L_ophhis, Hoteldpt, H_compli, Exrate, Artikel, Gl_main, H_cost, L_artikel, H_rezept, Umsatz

def fb_reconsilehis_cldbl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, ldry:int, dstore:int, double_currency:bool, foreign_nr:int, exchg_rate:Decimal, mi_opt_chk:bool, date1:date, date2:date):

    prepare_cache ([Htparam, Waehrung, H_artikel, L_besthis, Gl_acct, L_lager, L_ophis, Hoteldpt, H_compli, Exrate, Artikel, Gl_main, H_cost, L_artikel, H_rezept, Umsatz])

    done = False
    output_list_data = []
    lvcarea:string = "fb-reconsilehis"
    type_of_acct:int = 0
    counter:int = 0
    curr_nr:int = 0
    curr_reihe:int = 0
    coa_format:string = ""
    betrag:Decimal = to_decimal("0.0")
    bill_date:date = date(1,1,1)
    cost:Decimal = to_decimal("0.0")
    price:Decimal = to_decimal("0.0")
    exchange_val:int = 0
    price_type:int = 0
    incl_service:bool = False
    incl_mwst:bool = False
    long_digit:bool = False
    htparam = waehrung = h_artikel = l_besthis = gl_acct = l_lager = l_ophis = l_ophhis = hoteldpt = h_compli = exrate = artikel = gl_main = h_cost = l_artikel = h_rezept = umsatz = None
    

    output_list = s_list = None

    output_list_data, Output_list = create_model("Output_list", {"nr":int, "code":int, "bezeich":string, "s":string})
    s_list_data, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":string, "fibukonto":string, "bezeich":string, "flag":int, "anf_wert":Decimal, "end_wert":Decimal, "betrag":Decimal}, {"reihenfolge": 1, "flag": 2})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, output_list_data, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, bill_date, cost, price, exrate, price_type, incl_service, incl_mwst, long_digit, htparam, waehrung, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, h_rezept, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2


        nonlocal output_list, s_list
        nonlocal output_list_data, s_list_data

        return {"done": done, "output-list": output_list_data}

    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def formatting_int(data, format):
        if type(data) == str:
            data = int(data)

        digit_count = format.count('9')
    
        number_str = str(data)
        
        if len(number_str) > digit_count:
            raise ValueError(f"Number has too many digits for the given mask ({len(number_str)} > {digit_count})")
 
        number_str = number_str.zfill(digit_count)
        
        result = ''
        digit_index = 0

        for char in format:
            if char == '9':
                result += number_str[digit_index]
                digit_index += 1
            else:
                result += char
        return result

    def create_list():

        nonlocal done, output_list_data, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, bill_date, cost, price, exrate, price_type, incl_service, incl_mwst, long_digit, htparam, waehrung, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, h_rezept, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2


        nonlocal output_list, s_list
        nonlocal output_list_data, s_list_data

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
        L_oh =  create_buffer("L_oh",L_besthis)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        s_list_data.clear()
        output_list_data.clear()
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
            # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
            s_list.l_bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

        s_list.flag = 0

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
            s_list.l_bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

        s_list.flag = 0

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_besthis_obj_list = {}
            l_besthis = L_besthis()
            l_oh = L_besthis()

            for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.artnr, l_besthis._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.artnr, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.artnr, L_besthis._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.artnr, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid).join(L_oh,(L_oh.anf_best_dat == from_date) & (L_oh.lager_nr == 0) & (L_oh.artnr == L_besthis.artnr)).filter((L_besthis.anf_best_dat == from_date) & (L_besthis.lager_nr == l_lager.lager_nr) & (L_besthis.artnr <= 2999999)).order_by(L_besthis._recid).all():

                # if l_besthis_obj_list.get(l_besthis._recid):
                #     continue
                # else:
                #     l_besthis_obj_list[l_besthis._recid] = True

                if l_besthis.artnr <= 1999999:
                    flag = 1
                else:
                    flag = 2

                qty1 =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)
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

                s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_besthis.val_anf_best)

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_ophis in db_session.query(L_ophis).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_besthis.artnr) & (L_ophis.op_art == 1) & (L_ophis.lager_nr == l_lager.lager_nr) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():

                    l_ophhis = get_cache (L_ophhis, {"lscheinnr": [(eq, l_ophis.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_ophis.anzahl >= 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11

                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

                    elif l_ophis.anzahl < 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12

                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

                l_ophis_obj_list = {}
                for l_ophis, l_ophhis, gl_acct in db_session.query(L_ophis, L_ophhis, Gl_acct).join(L_ophhis,(L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.op_typ == ("STT").lower())).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_besthis.artnr) & (L_ophis.op_art == 3) & (L_ophis.lager_nr == l_lager.lager_nr) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    type_of_acct = gl_acct.acc_type
                    fibukonto = gl_acct.fibukonto
                    # bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                    bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

                    if l_ophis.fibukonto != "":

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type
                            fibukonto = gl_acct1.fibukonto
                            # bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()
                            bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")


                    if flag == 1 and fibukonto.lower()  == (food_bev).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_ophis.warenwert)

                    elif flag == 2 and fibukonto.lower()  == (bev_food).lower() :

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                        s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_ophis.warenwert)
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
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()

            for h_compli.datum, h_compli.departement, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.artnrlager, h_art.artnrrezept, h_art.prozent, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.artnrlager, H_art.artnrrezept, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter((H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():

                # if h_compli_obj_list.get(h_compli._recid):
                #     continue
                # else:
                #     h_compli_obj_list[h_compli._recid] = True

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

                cost = to_decimal("0")
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:

                    if h_cost.betrag == 1:
                        betrag =  to_decimal("0")
                    else:
                        betrag =  to_decimal(h_cost.betrag)

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(betrag)
                    elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(betrag)

                else:

                    if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                        if h_artikel.artnrlager != 0 :

                            l_artikel = db_session.query(L_artikel).filter(l_artikel.artnr == h_artikel.artnrlager).first()

                            if l_artikel:
                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    cost = l_artikel.vk_preis

                                else:
                                    cost = l_artikel.ek_aktuell

                                if artikel.umsatzart == 6:
                                    b_cost = h_compli.anzahl * cost

                                elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                                    f_cost = h_compli.anzahl * cost
                        
                        elif h_artikel.artnrrezept != 0:
                            h_rezept = db_session.query(H_rezept).filter(h_rezept.artnrrezept == h_artikel.artnrrezept)

                            if h_rezept:
                                cost = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost))

                                if artikel.umsatzart == 6:
                                    b_cost = h_compli.anzahl * cost
                                elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                                    f_cost = h_compli.anzahl * cost
                        else:

                            if artikel.umsatzart == 6:
                                b_cost = to_decimal(h_artikel.prozent) / 100 * to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * rate
                            elif artikel.umsatzart == 3 or artikel.umsatzart == 5:
                                f_cost = to_decimal(h_artikel.prozent) / 100 * to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * rate

                if f_cost != 0:

                    if mi_opt_chk == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.fibukonto = gl_acct.fibukonto
                            # s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")
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

                    if mi_opt_chk == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.fibukonto = gl_acct.fibukonto
                            # s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")
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
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** food **", lvcarea, "") , "x(50)")
            output_list.s = to_string("", "x(24)") + format_fixed_length(translateExtended ("** FOOD **", lvcarea, "") , 50)
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            i = 0
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("1. Opening Inventory", lvcarea, "") , 24)

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

                if i > 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:

                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                else:

                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")
                
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            i = 0
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("2. Incoming Stocks", lvcarea, "") , 24)

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if i > 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                else:
                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            i = 0
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("3. Returned Stocks", lvcarea, "") , 24)

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

                if i > 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                else:
                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string(("4. " + fb_str[0]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = format_fixed_length(("4. " + fb_str[0]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string(("4. " + fb_str[0]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = format_fixed_length(("4. " + fb_str[0]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
                output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")
                output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            i = 0
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("6. Closing Inventory", lvcarea, "") , 24)

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

                if i > 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_nr = curr_nr + 1
                    output_list.nr = curr_nr
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
                else:
                    # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")
                    output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")
                output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

            if not long_digit:
                # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
                output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")
                output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("8. Credits", lvcarea, "") , 24)

            if mi_opt_chk == False:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                # output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
                output_list.s = format_fixed_length(translateExtended ("- Compliment Cost", lvcarea, "") , 24)
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.nr = curr_nr

                    if s_list.code > 0:
                        output_list.code = s_list.code
                    else:
                        output_list.code = counter
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                else:
                    # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                    output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

            if mi_opt_chk == False:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                # output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
                output_list.s = format_fixed_length(translateExtended ("- Department Expenses", lvcarea, "") , 24)
                counter = 0
            else:
                counter = 1

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.nr = curr_nr

                    if s_list.code > 0:
                        output_list.code = s_list.code
                    else:
                        output_list.code = counter
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                else:
                    # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                    output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

            s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

            if mi_opt_chk == False:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr

                if not long_digit:
                    # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
                    output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
                else:
                    # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")
                    output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")

            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

            if not long_digit:
                # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
                output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")
                output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")
                
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            f_ratio =  to_decimal("0")

            if tf_sales != 0:
                f_ratio =  to_decimal(consume2) / to_decimal(tf_sales) * to_decimal("100")

            if not long_digit:
                # output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(f_ratio, "->,>>>,>>9.99 %")
                output_list.s = format_fixed_length(translateExtended ("Net Food Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(f_ratio, "->,>>>,>>9.99")} %"
            else:
                # output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(f_ratio, "->,>>>,>>9.99 %")
                output_list.s = format_fixed_length(translateExtended ("Net Food Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(f_ratio, "->,>>>,>>9.99")} %"

        if from_grp == 1:
            return

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(50)")
        output_list.s = to_string("", "x(24)") + format_fixed_length(translateExtended ("** BEVERAGE **", lvcarea, "") , 50)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        betrag1 =  to_decimal("0")
        # output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("1. Opening Inventory", lvcarea, "") , 24)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("2. Incoming Stocks", lvcarea, "") , 24)
        betrag2 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("3. Returned Stocks", lvcarea, "") , 24)
        betrag3 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(("4. " + fb_str[1]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(("4. " + fb_str[1]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(("4. " + fb_str[1]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(("4. " + fb_str[1]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()

        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("6. Closing Inventory", lvcarea, "") , 24)
        betrag5 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("8. Credits", lvcarea, "") , 24)
        betrag6 =  to_decimal("0")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("- Compliment Cost", lvcarea, "") , 24)
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("- Department Expenses", lvcarea, "") , 24)
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("lager_nr",False)]):
            counter = counter + 1
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)

            if counter > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)")

        if not long_digit:
            # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        b_ratio =  to_decimal("0")

        if tb_sales != 0:
            b_ratio =  to_decimal(consume2) / to_decimal(tb_sales) * to_decimal("100")

        if not long_digit:
            # output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(b_ratio, "->,>>>,>>9.99 %")
            output_list.s = format_fixed_length(translateExtended ("Net Beverage Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(b_ratio, "->,>>>,>>9.99")} %"
        else:
            # output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(b_ratio, "->,>>>,>>9.99 %")
            output_list.s = format_fixed_length(translateExtended ("Net Beverage Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(b_ratio, "->,>>>,>>9.99")} %"


        done = True


    def create_food():

        nonlocal done, output_list_data, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, bill_date, cost, price, exrate, price_type, incl_service, incl_mwst, long_digit, htparam, waehrung, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, h_rezept, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2


        nonlocal output_list, s_list
        nonlocal output_list_data, s_list_data

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
        fb_str:List[string] = ["Beverage TO food", "food to Beverage"]
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
        fb_str[0] = translateExtended ("Beverage to food", lvcarea, "")
        fb_str[1] = translateExtended ("food to Beverage", lvcarea, "")
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_besthis)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        s_list_data.clear()
        output_list_data.clear()
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
            # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
            s_list.l_bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

        s_list.flag = 0

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
            s_list.l_bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

        s_list.flag = 0
        flag = 1

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_besthis_obj_list = {}
            l_besthis = L_besthis()
            l_oh = L_besthis()

            for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.artnr, l_besthis._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.artnr, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.artnr, L_besthis._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.artnr, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid).join(L_oh,(L_oh.anf_best_dat == from_date) & (L_oh.lager_nr == 0) & (L_oh.artnr == L_besthis.artnr)).filter((L_besthis.anf_best_dat == from_date) & (L_besthis.lager_nr == l_lager.lager_nr) & (L_besthis.artnr >= 1000001) & (L_besthis.artnr <= 1999999)).order_by(L_besthis._recid).all():

                # if l_besthis_obj_list.get(l_besthis._recid):
                #     continue
                # else:
                #     l_besthis_obj_list[l_besthis._recid] = True

                qty1 =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)
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

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_besthis.anz_anf_best) * to_decimal(l_oh.val_anf_best) / to_decimal(l_oh.anz_anf_best)

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_ophis in db_session.query(L_ophis).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_besthis.artnr) & (L_ophis.op_art == 1) & (L_ophis.lager_nr == l_lager.lager_nr) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():

                    l_ophhis = get_cache (L_ophhis, {"lscheinnr": [(eq, l_ophis.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_ophis.anzahl >= 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11

                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

                    elif l_ophis.anzahl < 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12
                            
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

                l_ophis_obj_list = {}
                l_ophis = L_ophis()
                gl_acct = Gl_acct()

                for l_ophis.lscheinnr, l_ophis.warenwert, l_ophis.fibukonto, l_ophis.artnr, l_ophis.anzahl, l_ophis._recid, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.main_nr, gl_acct._recid in db_session.query(L_ophis.lscheinnr, L_ophis.warenwert, L_ophis.fibukonto, L_ophis.artnr, L_ophis.anzahl, L_ophis._recid, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.main_nr, Gl_acct._recid).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_besthis.artnr) & (L_ophis.op_art == 3) & (L_ophis.lager_nr == l_lager.lager_nr) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():

                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True

                    type_of_acct = gl_acct.acc_type
                    fibukonto = gl_acct.fibukonto
                    # bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                    bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")
                    gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})

                    if fibukonto.lower()  == (food_bev).lower() :
                        pass
                    elif fibukonto.lower()  == (bev_food).lower() :
                        pass
                    else:
                        if mi_opt_chk == False:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == 1 and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = 1
                                s_list.fibukonto = fibukonto
                                s_list.bezeich = bezeich
                                s_list.flag = 5
                        else:

                            s_list = query(s_list_data, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_data.append(s_list)

                                s_list.reihenfolge = 1
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich
                                s_list.flag = 5

                        if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

        l_ophis_obj_list = {}
        for l_ophis, l_artikel, l_ophhis, gl_acct in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).join(L_ophhis,(L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.op_typ == ("STT").lower())).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((L_ophis.fibukonto == (bev_food).lower()) | (L_ophis.fibukonto == (food_bev).lower())) & (L_ophis.op_art == 3) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():

            # if l_ophis_obj_list.get(l_ophis._recid):
            #     continue
            # else:
            #     l_ophis_obj_list[l_ophis._recid] = True

            fibukonto = gl_acct.fibukonto

            if l_ophis.fibukonto != "":

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto

            if fibukonto.lower()  == (food_bev).lower()  and l_ophis.artnr >= 1000001 and l_ophis.artnr <= 1999999:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_ophis.warenwert)

            elif fibukonto.lower()  == (bev_food).lower()  and l_ophis.artnr > 1999999:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_ophis.warenwert)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            # TODO
            for h_compli.datum, h_compli.departement, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.artnrlager, h_art.artnrrezept, h_art.prozent, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.artnrlager, H_art.artnrrezept, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter((H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():
                
                # if h_compli_obj_list.get(h_compli._recid):
                #     continue
                # else:
                #     h_compli_obj_list[h_compli._recid] = True

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

                cost = to_decimal("0")
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:

                    if h_cost.betrag == 1:
                        betrag =  to_decimal("0")
                    else:
                        betrag =  to_decimal(h_cost.betrag)

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                        f_cost =  to_decimal(h_compli.anzahl) * to_decimal(betrag)

                else:
                    if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                        if artikel.umsatzart == 3 or artikel.umsatzart == 5:
                            if h_artikel.artnrlager != 0:

                                l_artikel = db_session.query(L_artikel).filter(l_artikel.artnr == h_artikel.artnrlager).first()

                                if l_artikel:
                                    
                                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                                        cost = l_artikel.vk_preis
                                    else:
                                        cost = l_artikel.ek_aktuell

                                    f_cost = h_compli.anzahl * cost
                            
                            elif h_artikel.artnrrezept != 0:

                                h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                if h_rezept:
                                    cost = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost))

                                    f_cost = h_compli.anzahl * cost

                            else:
                                f_cost = to_decimal(h_artikel.prozent) / 100 * to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * rate

                    
                if f_cost != 0:

                    if mi_opt_chk == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 1
                            s_list.fibukonto = gl_acct.fibukonto
                            # s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")
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
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** food **", lvcarea, "") , "x(50)")
        output_list.s = to_string("", "x(24)") + format_fixed_length(translateExtended ("** FOOD **", lvcarea, "") , 50)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("1. Opening Inventory", lvcarea, "") , 24)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("2. Incoming Stocks", lvcarea, "") , 24)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("3. Returned Stocks", lvcarea, "") , 24)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 1), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(("4. " + fb_str[0]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(("4. " + fb_str[0]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(("4. " + fb_str[0]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(("4. " + fb_str[0]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("6. Closing Inventory", lvcarea, "") , 24)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 1 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("8. Credits", lvcarea, "") , 24)

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("- Compliment Cost", lvcarea, "") , 24)
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("- Department Expenses", lvcarea, "") , 24)
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 1 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)")

        if not long_digit:
            # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")
            
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        f_ratio =  to_decimal("0")

        if tf_sales != 0:
            f_ratio =  to_decimal(consume2) / to_decimal(tf_sales) * to_decimal("100")

        if not long_digit:
            # output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(f_ratio, "->,>>>,>>9.99 %")
            output_list.s = format_fixed_length(translateExtended ("Net Food Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(f_ratio, "->,>>>,>>9.99")} %"
        else:
            # output_list.s = to_string(translateExtended ("Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(f_ratio, "->,>>>,>>9.99 %")
            output_list.s = format_fixed_length(translateExtended ("Net Food Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(f_ratio, "->,>>>,>>9.99")} %"

        done = True


    def create_beverage():

        nonlocal done, output_list_data, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, bill_date, cost, price, exrate, price_type, incl_service, incl_mwst, long_digit, htparam, waehrung, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, h_rezept, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2


        nonlocal output_list, s_list
        nonlocal output_list_data, s_list_data

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
        fb_str:List[string] = ["Beverage TO food", "food to Beverage"]
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
        fb_str[0] = translateExtended ("Beverage to food", lvcarea, "")
        fb_str[1] = translateExtended ("food to Beverage", lvcarea, "")
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_besthis)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        s_list_data.clear()
        output_list_data.clear()
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
            # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
            s_list.l_bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

        s_list.flag = 0

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = 9999
        # Rd 30/7/2025
        # if available
        if gl_acct:
            # s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
            s_list.l_bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

        s_list.flag = 0
        flag = 2

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            l_besthis_obj_list = {}
            l_besthis = L_besthis()
            l_oh = L_besthis()
            for l_besthis.anz_anf_best, l_besthis.anz_eingang, l_besthis.anz_ausgang, l_besthis.val_anf_best, l_besthis.artnr, l_besthis._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh.anz_ausgang, l_oh.val_anf_best, l_oh.artnr, l_oh.wert_eingang, l_oh.wert_ausgang, l_oh._recid in db_session.query(L_besthis.anz_anf_best, L_besthis.anz_eingang, L_besthis.anz_ausgang, L_besthis.val_anf_best, L_besthis.artnr, L_besthis._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh.anz_ausgang, L_oh.val_anf_best, L_oh.artnr, L_oh.wert_eingang, L_oh.wert_ausgang, L_oh._recid).join(L_oh,(L_oh.anf_best_dat == from_date) & (L_oh.lager_nr == 0) & (L_oh.artnr == L_besthis.artnr)).filter((L_besthis.anf_best_dat == from_date) & (L_besthis.lager_nr == l_lager.lager_nr) & (L_besthis.artnr >= 2000001) & (L_besthis.artnr <= 2999999)).order_by(L_besthis._recid).all():

                # if l_besthis_obj_list.get(l_besthis._recid):
                #     continue
                # else:
                #     l_besthis_obj_list[l_besthis._recid] = True


                qty1 =  to_decimal(l_besthis.anz_anf_best) + to_decimal(l_besthis.anz_eingang) - to_decimal(l_besthis.anz_ausgang)
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

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_besthis.anz_anf_best) * to_decimal(l_oh.val_anf_best) / to_decimal(l_oh.anz_anf_best)

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_ophis in db_session.query(L_ophis).filter(
                         (L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_besthis.artnr) & (L_ophis.op_art == 1) & (L_ophis.lager_nr == l_lager.lager_nr) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():

                    l_ophhis = get_cache (L_ophhis, {"lscheinnr": [(eq, l_ophis.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_ophis.anzahl >= 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 11

                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

                    elif l_ophis.anzahl < 0:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich
                            s_list.flag = 12

                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

                l_ophis_obj_list = {}
                
                for l_ophis, l_ophhis, gl_acct in db_session.query(L_ophis, L_ophhis, Gl_acct).join(L_ophhis,(L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.op_typ == ("STT").lower()) & (L_ophhis.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & (L_ophis.artnr == l_besthis.artnr) & (L_ophis.op_art == 3) & (L_ophis.lager_nr == l_lager.lager_nr) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():
                    # if l_ophis_obj_list.get(l_ophis._recid):
                    #     continue
                    # else:
                    #     l_ophis_obj_list[l_ophis._recid] = True


                    type_of_acct = gl_acct.acc_type
                    fibukonto = gl_acct.fibukonto
                    # bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                    bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")
                    gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})

                    if l_ophis.fibukonto != "":

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                        if gl_acct1:
                            type_of_acct = gl_acct1.acc_type

                            gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct1.main_nr)]})
                            fibukonto = gl_acct1.fibukonto
                            # bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " + gl_acct1.bezeich.upper()
                            bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")

                    if fibukonto.lower()  == (food_bev).lower() :
                        pass
                    elif fibukonto.lower()  == (bev_food).lower() :
                        pass
                    else:
                        if mi_opt_chk == False:

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
                            s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_ophis.warenwert)

        l_ophis_obj_list = {}
        for l_ophis, l_artikel, l_ophhis, gl_acct in db_session.query(L_ophis, L_artikel, L_ophhis, Gl_acct).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).join(L_ophhis,(L_ophhis.lscheinnr == L_ophis.lscheinnr) & (L_ophhis.op_typ == ("STT").lower())).join(Gl_acct,(Gl_acct.fibukonto == L_ophis.fibukonto)).filter((L_ophis.datum >= from_date) & (L_ophis.datum <= to_date) & ((L_ophis.fibukonto == (bev_food).lower()) | (L_ophis.fibukonto == (food_bev).lower())) & (L_ophis.op_art == 3) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.lscheinnr).all():
            # if l_ophis_obj_list.get(l_ophis._recid):
            #     continue
            # else:
            #     l_ophis_obj_list[l_ophis._recid] = True

            fibukonto = gl_acct.fibukonto

            if l_ophis.fibukonto != "":

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto
            if fibukonto.lower()  == (food_bev).lower()  and l_ophis.artnr >= 1000001 and l_ophis.artnr <= 1999999:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_ophis.warenwert)

            elif fibukonto.lower()  == (bev_food).lower()  and l_ophis.artnr > 1999999:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_ophis.warenwert)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()

            for h_compli.datum, h_compli.departement, h_compli.artnr, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.artnrlager, h_art.artnrrezept, h_art.prozent, h_art._recid in db_session.query(H_compli.datum, H_compli.departement, H_compli.artnr, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.artnrlager, H_art.artnrrezept, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter((H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.rechnr).all():

                # if h_compli_obj_list.get(h_compli._recid):
                #     continue
                # else:
                #     h_compli_obj_list[h_compli._recid] = True

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

                cost = to_decimal("0")
                f_cost =  to_decimal("0")
                b_cost =  to_decimal("0")

                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:

                    if h_cost.betrag == 1:
                        betrag =  to_decimal("0")
                    else:
                        betrag =  to_decimal(h_cost.betrag)

                    if artikel.umsatzart == 6:
                        b_cost =  to_decimal(h_compli.anzahl) * to_decimal(betrag)
                else:
                    if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):

                        if artikel.umsatzart == 6:

                            if h_artikel.artnrlager != 0:
                                
                                l_artikel = db_session.query(L_artikel).filter(l_artikel.artnr == h_artikel.artnrlager).first()

                                if l_artikel:
                                    
                                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                                        cost = l_artikel.vk_preis
                                    else:
                                        cost = l_artikel.ek_aktuell

                                    b_cost = h_compli.anzahl * cost

                            elif h_artikel.artnrrezept != 0:

                                h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                if h_rezept:
                                    cost = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost))

                                    b_cost = h_compli.anzahl * cost

                            else:
                                b_cost = to_decimal(h_artikel.prozent) / 100 * to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * rate

                if b_cost != 0:

                    if mi_opt_chk == False:

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.reihenfolge = 2
                            s_list.fibukonto = gl_acct.fibukonto
                            # s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper()
                            s_list.bezeich = formatting_int(gl_acct.fibukonto, coa_format) + " " + gl_acct.bezeich.upper().replace("\\N", "\n")
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
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(50)")
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(50)")
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        betrag1 =  to_decimal("0")
        # output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("1. Opening Inventory", lvcarea, "") , 24)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.anf_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(s_list.anf_wert)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag1, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("2. Incoming Stocks", lvcarea, "") , 24)
        betrag2 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag2, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("3. Returned Stocks", lvcarea, "") , 24)
        betrag3 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == 2), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(s_list.betrag)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag3, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        s_list = query(s_list_data, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(("4. " + fb_str[1]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(("4. " + fb_str[1]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(("4. " + fb_str[1]) , "x(24)") + to_string(s_list.l_bezeich, "x(50)") + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(("4. " + fb_str[1]) , 24) + format_fixed_length(s_list.l_bezeich, 50) + to_string("", "x(18)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("5. Inventory Available", lvcarea, "") , "x(24)") + to_string("(1 + 2 + 3 + 4)", "x(50)") + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("5. Inventory Available", lvcarea, "") , 24) + format_fixed_length("(1 + 2 + 3 + 4)", 50) + to_string("", "x(18)") + to_string(betrag4, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        i = 0
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("6. Closing Inventory", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("6. Closing Inventory", lvcarea, "") , 24)
        betrag5 =  to_decimal("0")

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == 2 and s_list.lager_nr != 9999 and s_list.end_wert != 0), sort_by=[("lager_nr",False)]):
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(s_list.end_wert)

            if i > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_nr = curr_nr + 1
                output_list.nr = curr_nr
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.end_wert, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag5, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)

        if not long_digit:
            # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("7. Gross Consumption", lvcarea, "") , "x(24)") + to_string("(5 - 6)", "x(50)") + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("7. Gross Consumption", lvcarea, "") , 24) + format_fixed_length("(5 - 6)", 50) + to_string("", "x(18)") + to_string(betrag56, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        # output_list.s = to_string(translateExtended ("8. Credits", lvcarea, "") , "x(24)")
        output_list.s = format_fixed_length(translateExtended ("8. Credits", lvcarea, "") , 24)
        betrag6 =  to_decimal("0")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("- Compliment Cost", lvcarea, "") , 24)
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("bezeich",False)]):
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
            counter = counter + 1

            if counter > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            # output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            output_list.s = format_fixed_length(translateExtended ("- Department Expenses", lvcarea, "") , 24)
            counter = 0
        else:
            counter = 1

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == 2 and s_list.betrag != 0), sort_by=[("lager_nr",False)]):
            counter = counter + 1
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)

            if counter > 1:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.nr = curr_nr

                if s_list.code > 0:
                    output_list.code = s_list.code
                else:
                    output_list.code = counter
                output_list.s = to_string("", "x(24)")

            if not long_digit:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->>,>>>,>>>,>>9.99")
            else:
                # output_list.s = output_list.s + to_string(s_list.bezeich, "x(50)") + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")
                output_list.s = output_list.s + format_fixed_length(s_list.bezeich, 50) + to_string(s_list.betrag, "->,>>>,>>>,>>>,>>9")

        s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list.s = to_string("", "x(24)")

        if not long_digit:
            # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
            output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(50)") + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")
            output_list.s = output_list.s + format_fixed_length(s_list.l_bezeich, 50) + to_string(s_list.anf_wert, "->,>>>,>>>,>>>,>>9")

        betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)

        if mi_opt_chk == False:
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_nr = curr_nr + 1
            output_list.nr = curr_nr
            
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")
            output_list.s = to_string("", "x(24)") + to_string("", "x(41)") + format_fixed_length(translateExtended ("SUB TOTAL", lvcarea, "") , 9) + to_string("", "x(18)") + to_string(betrag6, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr

        if not long_digit:
            # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
            output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->>,>>>,>>>,>>9.99")
        else:
            # output_list.s = to_string(translateExtended ("9. Net Consumption", lvcarea, "") , "x(24)") + to_string("(7 - 8)", "x(50)") + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")
            output_list.s = format_fixed_length(translateExtended ("9. Net Consumption", lvcarea, "") , 24) + format_fixed_length("(7 - 8)", 50) + to_string("", "x(18)") + to_string(consume2, "->,>>>,>>>,>>>,>>9")

        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_nr = curr_nr + 1
        output_list.nr = curr_nr
        b_ratio =  to_decimal("0")

        if tb_sales != 0:
            b_ratio =  to_decimal(consume2) / to_decimal(tb_sales) * to_decimal("100")

        if not long_digit:
            # output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(b_ratio, "->,>>>,>>9.99 %")
            output_list.s = format_fixed_length(translateExtended ("Net Beverage Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(b_ratio, "->,>>>,>>9.99")} %"
        else:
            # output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(33)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(18)") + to_string(b_ratio, "->,>>>,>>9.99 %")
            output_list.s = format_fixed_length(translateExtended ("Net Beverage Sales", lvcarea, "") , 24) + to_string("", "x(33)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + format_fixed_length(translateExtended (" Cost:Sales", lvcarea, "") , 18) + f"{to_string(b_ratio, "->,>>>,>>9.99")} %"


        done = True


    def fb_sales(f_eknr:int, b_eknr:int):

        nonlocal done, output_list_data, lvcarea, type_of_acct, counter, curr_nr, curr_reihe, coa_format, betrag, bill_date, cost, price, exrate, price_type, incl_service, incl_mwst, long_digit, htparam, waehrung, h_artikel, l_besthis, gl_acct, l_lager, l_ophis, l_ophhis, hoteldpt, h_compli, exrate, artikel, gl_main, h_cost, l_artikel, h_rezept, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, ldry, dstore, double_currency, foreign_nr, exchg_rate, mi_opt_chk, date1, date2


        nonlocal output_list, s_list
        nonlocal output_list_data, s_list_data

        tf_sales = to_decimal("0.0")
        tb_sales = to_decimal("0.0")
        f_sales:Decimal = to_decimal("0.0")
        b_sales:Decimal = to_decimal("0.0")
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
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
                    h_service =  to_decimal("0")
                    h_mwst =  to_decimal("0")
                    h_service, h_mwst = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    amount =  to_decimal(umsatz.betrag) / to_decimal((1) + to_decimal(h_service) + to_decimal(h_mwst))

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales =  to_decimal(f_sales) + to_decimal(amount)
                        tf_sales =  to_decimal(tf_sales) + to_decimal(amount)

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales =  to_decimal(b_sales) + to_decimal(amount)
                        tb_sales =  to_decimal(tb_sales) + to_decimal(amount)

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    coa_format = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    if htparam:
        price_type = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
    if waehrung:
        exchange_val = waehrung.ankauf / waehrung.einheit

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    if htparam:
        incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    if htparam:
        incl_mwst = htparam.flogical

    if from_grp == 0:
        create_list()

    elif from_grp == food:
        create_food()

    elif from_grp == bev:
        create_beverage()

    return generate_output()