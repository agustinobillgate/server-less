#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, H_artikel, Gl_acct, L_bestand, L_lager, L_artikel, L_op, L_ophdr, Gl_main, H_compli, Hoteldpt, Exrate, Artikel, H_cost, Umsatz

def fb_reconsile1bl(pvilanguage:int, from_grp:int, food:int, bev:int, from_date:date, to_date:date, date1:date, date2:date, mi_opt_chk:bool, double_currency:bool, exchg_rate:Decimal, foreign_nr:int):

    prepare_cache ([Htparam, H_artikel, Gl_acct, L_bestand, L_lager, L_artikel, L_op, Gl_main, H_compli, Hoteldpt, Exrate, Artikel, H_cost, Umsatz])

    done = False
    output_list_list = []
    counter:int = 0
    output_counter:int = 0
    coa_format:string = ""
    lvcarea:string = "fb-reconsile1"
    type_of_acct:int = 0
    long_digit:bool = False
    htparam = h_artikel = gl_acct = l_bestand = l_lager = l_artikel = l_op = l_ophdr = gl_main = h_compli = hoteldpt = exrate = artikel = h_cost = umsatz = None

    s_list = s1_list = output_list = None

    s_list_list, S_list = create_model("S_list", {"code":int, "reihenfolge":int, "lager_nr":int, "l_bezeich":string, "fibukonto":string, "bezeich":string, "flag":int, "anf_wert":Decimal, "end_wert":Decimal, "betrag":Decimal}, {"reihenfolge": 1, "flag": 2})
    output_list_list, Output_list = create_model("Output_list", {"curr_counter":int, "nr":int, "store":int, "amount":Decimal, "bezeich":string, "s":string})

    S1_list = S_list
    s1_list_list = s_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr
        nonlocal s1_list


        nonlocal s_list, s1_list, output_list
        nonlocal s_list_list, output_list_list

        return {"done": done, "output-list": output_list_list}

    def create_food():

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr
        nonlocal s1_list


        nonlocal s_list, s1_list, output_list
        nonlocal s_list_list, output_list_list

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
        net_cost:Decimal = to_decimal("0.0")
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
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        qty1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        onhand:Decimal = to_decimal("0.0")
        fibukonto:string = ""
        bezeich:string = ""
        netcost_flag:bool = False
        gl_acct1 = None
        l_oh = None
        l_oh1 = None
        tot_foodcost:Decimal = to_decimal("0.0")
        H_art =  create_buffer("H_art",H_artikel)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        L_oh =  create_buffer("L_oh",L_bestand)
        L_oh1 =  create_buffer("L_oh1",L_bestand)
        output_list_list.clear()

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
        create_output_list()
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** food **", lvcarea, "") , "x(33)")
        flag = 1

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.betriebsnr > 0)).order_by(L_lager._recid).all():
            s_list_list.clear()
            betrag1 =  to_decimal("0")
            betrag2 =  to_decimal("0")
            betrag3 =  to_decimal("0")
            betrag4 =  to_decimal("0")
            betrag5 =  to_decimal("0")
            betrag6 =  to_decimal("0")
            net_cost =  to_decimal("0")

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, bev_food)]})
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 1
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 2
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0


            create_output_list()
            create_output_list()
            output_list.s = to_string("", "x(24)") + to_string(l_lager.lager_nr, "99 ") + to_string(l_lager.bezeich, "x(30)")

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_oh = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh._recid, l_artikel.artnr, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh._recid, L_artikel.artnr, L_artikel._recid).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) -\
                        l_bestand.anz_ausgang
                qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) -\
                        l_oh.anz_ausgang
                wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) -\
                        l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                s1_list = query(s1_list_list, filters=(lambda s1_list: s1_list.lager_nr == l_lager.lager_nr and s1_list.reihenfolge == flag and s1_list.flag == 1), first=True)

                if not s1_list:
                    s1_list = S1_list()
                    s1_list_list.append(s1_list)

                    s1_list.flag = 1
                    s1_list.reihenfolge = flag
                    s1_list.lager_nr = l_lager.lager_nr
                    s1_list.l_bezeich = l_lager.bezeich

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) *\
                            l_oh.val_anf_best / to_decimal(l_oh.anz_anf_best)
                    s1_list.anf_wert =  to_decimal(s1_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) *\
                        (l_artikel.vk_preis - to_decimal(l_oh.val_anf_best) / to_decimal(l_oh.anz_anf_best) )

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.flag = 11
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.flag = 12
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.pos > 0) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    if substring(l_op.stornogrund, 0, 8) == ("00000000").lower() :
                        net_cost =  to_decimal(net_cost) + to_decimal(l_op.warenwert)
                    else:

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                        if gl_acct1:
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                                    gl_acct1.bezeich.upper()
                            type_of_acct = gl_acct1.acc_type

                            gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct1.main_nr)]})

                        if fibukonto.lower()  == (food_bev).lower() :
                            pass

                        elif fibukonto.lower()  == (bev_food).lower() :
                            pass
                        else:

                            if mi_opt_chk == False:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.fibukonto = fibukonto
                                    s_list.bezeich = bezeich


                            else:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.code = gl_main.code
                                    s_list.bezeich = gl_main.bezeich

                            if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 111
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.l_bezeich = l_lager.bezeich

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.warenwert, l_op.stornogrund, l_op.anzahl, l_op.lager_nr, l_op.pos, l_op._recid, l_artikel.artnr, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.warenwert, L_op.stornogrund, L_op.anzahl, L_op.lager_nr, L_op.pos, L_op._recid, L_artikel.artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.loeschflag <= 1) & (L_op.op_art == 4) & (L_op.herkunftflag == 1) & ((L_op.lager_nr == l_lager.lager_nr) | (L_op.pos == l_lager.lager_nr))).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if l_op.lager_nr == l_lager.lager_nr:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

                if l_op.pos == l_lager.lager_nr:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 112
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN transFER IN"


            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 113
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN transFER OUT"

            for h_compli in db_session.query(H_compli).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr > 0) & (H_compli.p_artnr == 1)).order_by(H_compli.departement).all():

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.betriebsnr)]})

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 112), first=True)
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(h_compli.epreis)
                else:

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.departement)]})

                    if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 113), first=True)
                        s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(h_compli.epreis)

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.warenwert, l_op.stornogrund, l_op.anzahl, l_op.lager_nr, l_op.pos, l_op._recid, l_artikel.artnr, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.warenwert, L_op.stornogrund, L_op.anzahl, L_op.lager_nr, L_op.pos, L_op._recid, L_artikel.artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                     (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.datum >= date1) & (L_op.datum <= date2) & ((L_op.stornogrund == (bev_food).lower()) | (L_op.stornogrund == (food_bev).lower())) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if l_op.stornogrund.lower()  == (food_bev).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

                elif l_op.stornogrund.lower()  == (bev_food).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

            for hoteldpt in db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num > 0) & ((Hoteldpt.num == l_lager.betriebsnr) | (Hoteldpt.betriebsnr == l_lager.lager_nr))).order_by(Hoteldpt.num).all():

                h_compli_obj_list = {}
                h_compli = H_compli()
                h_art = H_artikel()
                for h_compli.betriebsnr, h_compli.epreis, h_compli.departement, h_compli.datum, h_compli.artnr, h_compli.anzahl, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art._recid in db_session.query(H_compli.betriebsnr, H_compli.epreis, H_compli.departement, H_compli.datum, H_compli.artnr, H_compli.anzahl, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
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

                        if artikel.endkum == b_eknr:
                            b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                        elif artikel.endkum == f_eknr:
                            f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                        if artikel.endkum == f_eknr:
                            tot_foodcost =  to_decimal(tot_foodcost) + to_decimal(f_cost)

                    elif not h_cost or (h_cost and h_cost.betrag == 0):

                        if artikel.endkum == b_eknr:
                            b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                        elif artikel.endkum == f_eknr:
                            f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                        if artikel.endkum == f_eknr:
                            tot_foodcost =  to_decimal(tot_foodcost) + to_decimal(f_cost)

                    if f_cost != 0:

                        if mi_opt_chk == False:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = flag
                                s_list.fibukonto = gl_acct.fibukonto
                                s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                                        gl_acct.bezeich.upper()


                        else:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == 1 and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = 1
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(f_cost)

            if l_lager.betriebsnr != 0:
                tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand =  to_decimal(s_list.anf_wert)
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand =  to_decimal(s_list.anf_wert)
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(onhand)
            create_output_list()
            output_list.s = to_string(translateExtended (" OpenInv Adjustment", lvcarea, "") , "x(24)") +\
                    to_string("", "x(33)")
            output_list.nr = 1
            output_list.store = l_lager.lager_nr
            output_list.amount =  to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand =  to_decimal(s_list.betrag)
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand =  to_decimal(s_list.betrag)
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("4. Store Transfer", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 111 and s_list.reihenfolge == flag), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("5. Kitchen Transfer In", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 112 and s_list.reihenfolge == flag), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended (" Kitchen Transfer Out", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 113 and s_list.reihenfolge == flag), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == flag), first=True)
            create_output_list()
            output_list.s = to_string(("6. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
            create_output_list()
            output_list.s = to_string(translateExtended ("7. Inventory Available", lvcarea, "") , "x(24)") +\
                    to_string("(1 + 2 + 3 + 4 + 5 + 6)", "x(33)") +\
                    to_string("", "x(15)")
            output_list.nr = 2
            output_list.store = l_lager.lager_nr
            output_list.amount =  to_decimal(betrag4)

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag4, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag4, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("8. Closing Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.end_wert != 0), first=True)

            if s_list:
                onhand =  to_decimal(s_list.end_wert)
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string("", "x(15)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            create_output_list()
            betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)
            output_list.s = to_string(translateExtended ("9. Tot. Cost Consumption", lvcarea, "") , "x(24)") +\
                    to_string("(7 - 8)", "x(33)") + to_string("", "x(15)")
            output_list.nr = 3
            output_list.store = l_lager.lager_nr
            output_list.amount =  to_decimal(betrag56)

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag56, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag56, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("10 Less by Expenses", lvcarea, "") , "x(24)")
            create_output_list()
            output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == flag and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == flag and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.reihenfolge == 2 and s_list.lager_nr == 9999), first=True)
            create_output_list()
            output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)
            create_output_list()

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string(translateExtended ("SUB TOTAL", lvcarea, "") , "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
            consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
            create_output_list()

            if not long_digit:
                output_list.s = to_string(translateExtended ("11 Net Cost Consumed", lvcarea, "") , "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("11 Net Cost Consumed", "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
            create_output_list()
            f_ratio =  to_decimal("0")

            if tf_sales != 0:
                f_ratio =  to_decimal(consume2) / to_decimal(tf_sales) * to_decimal("100")

            if not long_digit:
                output_list.s = to_string(translateExtended (">> Net food Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tf_sales, "->,>>>,>>>,>>9.99") + to_string(" Cost:Sales", "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
            else:
                output_list.s = to_string("Net food Sales", "x(24)") + to_string("", "x(16)") + to_string(tf_sales, " ->>>,>>>,>>>,>>9") + to_string(" Cost:Sales", "x(15)") + to_string(f_ratio, "->,>>>,>>9.99 %")
        done = True


    def create_beverage():

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr
        nonlocal s1_list


        nonlocal s_list, s1_list, output_list
        nonlocal s_list_list, output_list_list

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
        net_cost:Decimal = to_decimal("0.0")
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
        curr_datum:date = None
        rate:Decimal = 1
        h_art = None
        qty1:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        l_oh = None
        l_oh1 = None
        onhand:Decimal = to_decimal("0.0")
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        H_art =  create_buffer("H_art",H_artikel)
        L_oh =  create_buffer("L_oh",L_bestand)
        L_oh1 =  create_buffer("L_oh1",L_bestand)
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        output_list_list.clear()

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
        create_output_list()
        output_list.s = to_string("", "x(24)") + to_string(translateExtended ("** BEVERAGE **", lvcarea, "") , "x(33)")
        flag = 2

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.betriebsnr > 0)).order_by(L_lager._recid).all():
            s_list_list.clear()
            betrag1 =  to_decimal("0")
            betrag2 =  to_decimal("0")
            betrag3 =  to_decimal("0")
            betrag4 =  to_decimal("0")
            betrag5 =  to_decimal("0")
            betrag6 =  to_decimal("0")
            net_cost =  to_decimal("0")

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, bev_food)]})
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 1
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, food_bev)]})
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 2
            s_list.lager_nr = 9999
            s_list.l_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 0


            create_output_list()
            create_output_list()
            output_list.s = to_string("", "x(24)") + to_string(l_lager.lager_nr, "99 ") + to_string(l_lager.bezeich, "x(30)")

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_oh = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand._recid, l_oh.anz_anf_best, l_oh.anz_eingang, l_oh._recid, l_artikel.artnr, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand._recid, L_oh.anz_anf_best, L_oh.anz_eingang, L_oh._recid, L_artikel.artnr, L_artikel._recid).join(L_oh,(L_oh.artnr == L_bestand.artnr) & (L_oh.lager_nr == 0)).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) -\
                        l_bestand.anz_ausgang
                qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) -\
                        l_oh.anz_ausgang
                wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) -\
                        l_oh.wert_ausgang

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 0), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = flag
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.l_bezeich = l_lager.bezeich
                    s_list.flag = 0

                s1_list = query(s1_list_list, filters=(lambda s1_list: s1_list.lager_nr == l_lager.lager_nr and s1_list.reihenfolge == flag and s1_list.flag == 1), first=True)

                if not s1_list:
                    s1_list = S1_list()
                    s1_list_list.append(s1_list)

                    s1_list.flag = 1
                    s1_list.reihenfolge = flag
                    s1_list.lager_nr = l_lager.lager_nr
                    s1_list.l_bezeich = l_lager.bezeich

                if l_oh.anz_anf_best != 0:
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) *\
                            l_oh.val_anf_best / to_decimal(l_oh.anz_anf_best)
                    s1_list.anf_wert =  to_decimal(s1_list.anf_wert) + to_decimal(l_bestand.anz_anf_best) *\
                        (l_artikel.vk_preis - to_decimal(l_oh.val_anf_best) / to_decimal(l_oh.anz_anf_best) )

                if qty != 0:
                    s_list.end_wert =  to_decimal(s_list.end_wert) + to_decimal(wert) * to_decimal(qty1) / to_decimal(qty)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.op_art == 1) & (L_op.loeschflag <= 1) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, l_op.lscheinnr)],"op_typ": [(eq, "sti")]})

                    if l_op.anzahl >= 0:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 11), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.flag = 11
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                    elif l_op.anzahl < 0:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_lager.lager_nr and s_list.reihenfolge == flag and s_list.flag == 12), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.flag = 12
                            s_list.reihenfolge = flag
                            s_list.lager_nr = l_lager.lager_nr
                            s_list.l_bezeich = l_lager.bezeich


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

                for l_op in db_session.query(L_op).filter(
                         (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr == l_artikel.artnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.pos > 0) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op.lscheinnr).all():

                    if substring(l_op.stornogrund, 0, 8) == ("00000000").lower() :
                        net_cost =  to_decimal(net_cost) + to_decimal(l_op.warenwert)
                    else:

                        gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                        if gl_acct1:
                            fibukonto = gl_acct1.fibukonto
                            bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                                    gl_acct1.bezeich.upper()
                            type_of_acct = gl_acct1.acc_type


                            gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct1.main_nr)]})

                        if fibukonto.lower()  == (food_bev).lower() :
                            pass

                        elif fibukonto.lower()  == (bev_food).lower() :
                            pass
                        else:

                            if mi_opt_chk == False:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.fibukonto = fibukonto
                                    s_list.bezeich = bezeich


                            else:

                                s_list = query(s_list_list, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == flag and s_list.flag == 5), first=True)

                                if not s_list:
                                    s_list = S_list()
                                    s_list_list.append(s_list)

                                    s_list.flag = 5
                                    s_list.reihenfolge = flag
                                    s_list.code = gl_main.code
                                    s_list.bezeich = gl_main.bezeich

                            if type_of_acct == 5 or type_of_acct == 3 or type_of_acct == 4:
                                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 111
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.l_bezeich = l_lager.bezeich

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.warenwert, l_op.stornogrund, l_op.anzahl, l_op.lager_nr, l_op.pos, l_op._recid, l_artikel.artnr, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.warenwert, L_op.stornogrund, L_op.anzahl, L_op.lager_nr, L_op.pos, L_op._recid, L_artikel.artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.loeschflag <= 1) & (L_op.op_art == 4) & (L_op.herkunftflag == 1) & ((L_op.lager_nr == l_lager.lager_nr) | (L_op.pos == l_lager.lager_nr))).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if l_op.lager_nr == l_lager.lager_nr:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

                if l_op.pos == l_lager.lager_nr:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.flag = 112
            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN transFER IN"


            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = flag
            s_list.lager_nr = l_lager.lager_nr
            s_list.bezeich = "KITCHEN transFER OUT"
            s_list.flag = 113

            for h_compli in db_session.query(H_compli).filter(
                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr > 0) & (H_compli.p_artnr == 2)).order_by(H_compli.departement).all():

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.betriebsnr)]})

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 112), first=True)
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(h_compli.epreis)
                else:

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.departement)]})

                    if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 113), first=True)
                        s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(h_compli.epreis)

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.warenwert, l_op.stornogrund, l_op.anzahl, l_op.lager_nr, l_op.pos, l_op._recid, l_artikel.artnr, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.warenwert, L_op.stornogrund, L_op.anzahl, L_op.lager_nr, L_op.pos, L_op._recid, L_artikel.artnr, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                     (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.datum >= date1) & (L_op.datum <= date2) & ((L_op.stornogrund == (bev_food).lower()) | (L_op.stornogrund == (food_bev).lower())) & (L_op.lager_nr == l_lager.lager_nr)).order_by(L_op._recid).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                if l_op.stornogrund.lower()  == (food_bev).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

                elif l_op.stornogrund.lower()  == (bev_food).lower() :

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 1), first=True)
                    s_list.anf_wert =  to_decimal(s_list.anf_wert) + to_decimal(l_op.warenwert)

            for hoteldpt in db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num > 0) & ((Hoteldpt.num == l_lager.betriebsnr) | (Hoteldpt.betriebsnr == l_lager.lager_nr))).order_by(Hoteldpt.num).all():

                h_compli_obj_list = {}
                h_compli = H_compli()
                h_art = H_artikel()
                for h_compli.betriebsnr, h_compli.epreis, h_compli.departement, h_compli.datum, h_compli.artnr, h_compli.anzahl, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art._recid in db_session.query(H_compli.betriebsnr, H_compli.epreis, H_compli.departement, H_compli.datum, H_compli.artnr, H_compli.anzahl, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
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

                        if artikel.endkum == b_eknr:
                            b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                        elif artikel.endkum == f_eknr:
                            f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

                    elif not h_cost or (h_cost and h_cost.betrag == 0):

                        if artikel.endkum == b_eknr:
                            b_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                        elif artikel.endkum == f_eknr:
                            f_cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                    if b_cost != 0:

                        if mi_opt_chk == False:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto == gl_acct.fibukonto and s_list.reihenfolge == flag and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = flag
                                s_list.fibukonto = gl_acct.fibukonto
                                s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                                        gl_acct.bezeich.upper()


                        else:

                            s_list = query(s_list_list, filters=(lambda s_list: s_list.code == gl_main.code and s_list.reihenfolge == 2 and s_list.flag == 4), first=True)

                            if not s_list:
                                s_list = S_list()
                                s_list_list.append(s_list)

                                s_list.flag = 4
                                s_list.reihenfolge = 2
                                s_list.code = gl_main.code
                                s_list.bezeich = gl_main.bezeich


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(b_cost)

            if l_lager.betriebsnr != 0:
                tf_sales, tb_sales = fb_sales(f_eknr, b_eknr)
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("1. Opening Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand =  to_decimal(s_list.anf_wert)
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.anf_wert != 0), first=True)

            if s_list:
                onhand =  to_decimal(s_list.anf_wert)
            i = i + 1
            betrag1 =  to_decimal(betrag1) + to_decimal(onhand)
            create_output_list()
            output_list.s = to_string(translateExtended (" OpenInv Adjustment", lvcarea, "") , "x(24)") +\
                    to_string("", "x(33)")
            output_list.nr = 1
            output_list.store = l_lager.lager_nr
            output_list.amount =  to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("2. Incoming Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 11 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand =  to_decimal(s_list.betrag)
            i = i + 1
            betrag2 =  to_decimal(betrag2) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("3. Returned Stocks", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 12 and s_list.reihenfolge == flag), first=True)

            if s_list:
                onhand =  to_decimal(s_list.betrag)
            i = i + 1
            betrag3 =  to_decimal(betrag3) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("4. Store Transfer", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 111 and s_list.reihenfolge == flag), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended ("5. Kitchen Transfer In", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 112 and s_list.reihenfolge == flag), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            i = 0
            create_output_list()
            output_list.s = to_string(translateExtended (" Kitchen Transfer Out", lvcarea, "") , "x(24)")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 113 and s_list.reihenfolge == flag), sort_by=[("lager_nr",False)]):
                i = i + 1
                betrag2 =  to_decimal(betrag2) + to_decimal(s_list.betrag)

                if not long_digit:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string("", "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == 9999 and s_list.reihenfolge == 2), first=True)
            create_output_list()
            output_list.s = to_string(("6. " + s_list.l_bezeich) , "x(24)") + to_string("", "x(33)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag4 =  to_decimal(betrag1) + to_decimal(betrag2) + to_decimal(betrag3) + to_decimal(s_list.anf_wert)
            create_output_list()
            output_list.s = to_string(translateExtended ("7. Inventory Available", lvcarea, "") , "x(24)") +\
                    to_string("(1 + 2 + 3 + 4 + 5 + 6)", "x(33)") +\
                    to_string("", "x(15)")
            output_list.nr = 2
            output_list.store = l_lager.lager_nr
            output_list.amount =  to_decimal(betrag4)

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag4, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag4, "->>,>>>,>>>,>>9")
            i = 0
            onhand =  to_decimal("0")
            create_output_list()
            output_list.s = to_string(translateExtended ("8. Closing Inventory", lvcarea, "") , "x(24)")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 0 and s_list.reihenfolge == flag and s_list.lager_nr != 9999 and s_list.end_wert != 0), first=True)

            if s_list:
                onhand =  to_decimal(s_list.end_wert)
            i = i + 1
            betrag5 =  to_decimal(betrag5) + to_decimal(onhand)

            if not long_digit:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string("", "x(15)") + to_string(onhand, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string("", "x(33)") + to_string(onhand, "->>,>>>,>>>,>>9")
            create_output_list()
            betrag56 =  to_decimal(betrag4) - to_decimal(betrag5)
            output_list.s = to_string(translateExtended ("9. Tot. Cost Consumption", lvcarea, "") , "x(24)") +\
                    to_string("(7 - 8)", "x(33)") + to_string("", "x(15)")
            output_list.nr = 3
            output_list.store = l_lager.lager_nr
            output_list.amount =  to_decimal(betrag56)

            if not long_digit:
                output_list.s = output_list.s + to_string(betrag56, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(betrag56, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("10 Less by Expenses", lvcarea, "") , "x(24)")
            create_output_list()
            output_list.s = to_string(translateExtended ("- Compliment Cost", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 4 and s_list.reihenfolge == flag and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")
            create_output_list()
            output_list.s = to_string(translateExtended ("- Department Expenses", lvcarea, "") , "x(24)")
            counter = 0

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 5 and s_list.reihenfolge == flag and s_list.betrag != 0), sort_by=[("bezeich",False)]):
                betrag6 =  to_decimal(betrag6) + to_decimal(s_list.betrag)
                counter = counter + 1

                if counter > 1:
                    create_output_list()
                    output_list.s = to_string("", "x(24)")

                if not long_digit:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>>,>>>,>>9.99")
                else:
                    output_list.s = output_list.s + to_string(s_list.bezeich, "x(33)") + to_string(s_list.betrag, "->>,>>>,>>>,>>9")

            s_list = query(s_list_list, filters=(lambda s_list: s_list.reihenfolge == 1 and s_list.lager_nr == 9999), first=True)
            create_output_list()
            output_list.s = to_string("", "x(24)")

            if not long_digit:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>>,>>>,>>9.99")
            else:
                output_list.s = output_list.s + to_string(s_list.l_bezeich, "x(33)") + to_string(s_list.anf_wert, "->>,>>>,>>>,>>9")
            betrag6 =  to_decimal(betrag6) + to_decimal(s_list.anf_wert)
            create_output_list()

            if not long_digit:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string("SUB TOTAL", "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string("", "x(24)") + to_string("", "x(24)") + to_string("SUB TOTAL", "x(9)") + to_string("", "x(15)") + to_string(betrag6, "->>,>>>,>>>,>>9")
            consume2 =  to_decimal(betrag56) - to_decimal(betrag6)
            create_output_list()

            if not long_digit:
                output_list.s = to_string(translateExtended ("11 Net Cost Consumed", lvcarea, "") , "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>>,>>>,>>9.99")
            else:
                output_list.s = to_string(translateExtended ("11 Net Cost Consumed", lvcarea, "") , "x(24)") + to_string("(9 - 10)", "x(33)") + to_string("", "x(15)") + to_string(consume2, "->>,>>>,>>>,>>9")
            create_output_list()
            b_ratio =  to_decimal("0")

            if tb_sales != 0:
                b_ratio =  to_decimal(consume2) / to_decimal(tb_sales) * to_decimal("100")

            if not long_digit:
                output_list.s = to_string(translateExtended (">> Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, "->,>>>,>>>,>>9.99") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
            else:
                output_list.s = to_string(translateExtended ("Net Beverage Sales", lvcarea, "") , "x(24)") + to_string("", "x(16)") + to_string(tb_sales, " ->>>,>>>,>>>,>>9") + to_string(translateExtended (" Cost:Sales", lvcarea, "") , "x(15)") + to_string(b_ratio, "->,>>>,>>9.99 %")
        done = True


    def fb_sales(f_eknr:int, b_eknr:int):

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr
        nonlocal s1_list


        nonlocal s_list, s1_list, output_list
        nonlocal s_list_list, output_list_list

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
                 ((Hoteldpt.num == l_lager.betriebsnr) | (Hoteldpt.betriebsnr == l_lager.lager_nr))).order_by(Hoteldpt.num).all():

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


    def create_output_list():

        nonlocal done, output_list_list, counter, output_counter, coa_format, lvcarea, type_of_acct, long_digit, htparam, h_artikel, gl_acct, l_bestand, l_lager, l_artikel, l_op, l_ophdr, gl_main, h_compli, hoteldpt, exrate, artikel, h_cost, umsatz
        nonlocal pvilanguage, from_grp, food, bev, from_date, to_date, date1, date2, mi_opt_chk, double_currency, exchg_rate, foreign_nr
        nonlocal s1_list


        nonlocal s_list, s1_list, output_list
        nonlocal s_list_list, output_list_list


        output_counter = output_counter + 1
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.curr_counter = output_counter

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    coa_format = htparam.fchar

    if from_grp == food:
        create_food()

    elif from_grp == bev:
        create_beverage()

    return generate_output()