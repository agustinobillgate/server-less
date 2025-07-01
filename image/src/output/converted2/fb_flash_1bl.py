#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Waehrung, L_lager, L_artikel, L_bestand, L_op, Gl_acct, H_artikel, H_compli, Exrate, Artikel, H_cost, L_ophdr, Hoteldpt, Umsatz

def fb_flash_1bl(pvilanguage:int, from_grp:int, food:int, bev:int, date1:date, date2:date, incl_initoh:bool, incl_streq:bool):

    prepare_cache ([Htparam, Waehrung, L_lager, L_bestand, L_op, Gl_acct, H_artikel, H_compli, Exrate, Artikel, H_cost, Hoteldpt, Umsatz])

    fbflash_list_list = []
    done = False
    beg_oh:Decimal = to_decimal("0.0")
    betrag:Decimal = to_decimal("0.0")
    t_betrag1:Decimal = to_decimal("0.0")
    t_betrag2:Decimal = to_decimal("0.0")
    d_betrag:Decimal = to_decimal("0.0")
    m_betrag:Decimal = to_decimal("0.0")
    d1_betrag:Decimal = to_decimal("0.0")
    m1_betrag:Decimal = to_decimal("0.0")
    flag:int = 0
    f_eknr:int = 0
    b_eknr:int = 0
    fl_eknr:int = 0
    bl_eknr:int = 0
    main_storage:int = 1
    bev_food:string = ""
    food_bev:string = ""
    ldry:int = 0
    dstore:int = 0
    foreign_nr:int = 0
    exchg_rate:Decimal = 1
    double_currency:bool = False
    f_sales:Decimal = to_decimal("0.0")
    b_sales:Decimal = to_decimal("0.0")
    tf_sales:Decimal = to_decimal("0.0")
    tb_sales:Decimal = to_decimal("0.0")
    anf_store:int = 1
    long_digit:bool = False
    coa_format:string = ""
    lvcarea:string = "fb-flash"
    htparam = waehrung = l_lager = l_artikel = l_bestand = l_op = gl_acct = h_artikel = h_compli = exrate = artikel = h_cost = l_ophdr = hoteldpt = umsatz = None

    fbflash_list = s_list = None

    fbflash_list_list, Fbflash_list = create_model("Fbflash_list", {"flag":int, "trans_to_storage":string, "cost_alloc":string, "day_cons":string, "mtd_cons":string})
    s_list_list, S_list = create_model("S_list", {"reihenfolge":int, "lager_nr":int, "fibukonto":string, "bezeich":string, "flag":int, "betrag":Decimal, "t_betrag":Decimal, "betrag1":Decimal, "t_betrag1":Decimal}, {"reihenfolge": 1, "flag": 2})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        return {"fbflash-list": fbflash_list_list, "done": done}

    def step_food1(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 1
        l_store = None
        L_store =  create_buffer("L_store",L_lager)

        l_op_obj_list = {}
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_op.op_art == 4) & (L_op.loeschflag <= 1) & (L_op.herkunftflag == 1) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.lager_nr != main_storage:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag =  to_decimal(s_list.t_betrag) - to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

            if l_op.pos != main_storage:

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.pos and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_store.lager_nr
                    s_list.bezeich = l_store.bezeich
                    s_list.flag = flag


                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_bev1(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 2
        l_store = None
        L_store =  create_buffer("L_store",L_lager)

        l_op_obj_list = {}
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_op.op_art == 4) & (L_op.loeschflag <= 1) & (L_op.herkunftflag == 1) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.lager_nr != main_storage:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag =  to_decimal(s_list.t_betrag) - to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

            if l_op.pos != main_storage:

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.pos and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_store.lager_nr
                    s_list.bezeich = l_store.bezeich
                    s_list.flag = flag


                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_food2(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 1

        l_op_obj_list = {}
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_op.op_art == 1) & (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.lager_nr != main_storage) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 2 and s_list.flag == flag), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.reihenfolge = 2
                s_list.lager_nr = l_lager.lager_nr
                s_list.bezeich = l_lager.bezeich
                s_list.flag = flag


            s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

            if l_op.datum == date2:
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_bev2(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 2

        l_op_obj_list = {}
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_op.op_art == 1) & (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.lager_nr != main_storage) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 2 and s_list.flag == flag), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.reihenfolge = 2
                s_list.lager_nr = l_lager.lager_nr
                s_list.bezeich = l_lager.bezeich
                s_list.flag = flag


            s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

            if l_op.datum == date2:
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def beverage_to_food():

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acct:
            bev_food = htparam.fchar
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 3
            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 1


    def food_to_beverage():

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if gl_acct:
            food_bev = htparam.fchar
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.reihenfolge = 3
            s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            s_list.flag = 2


    def step_two(f_endkum:int, b_endkum:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        h_art = None
        gl_acc1 = None
        flag:int = 0
        cost_account:string = ""
        cost_value:Decimal = to_decimal("0.0")
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        com_artnr:int = 0
        com_bezeich:string = ""
        com_fibu:string = ""
        H_art =  create_buffer("H_art",H_artikel)
        Gl_acc1 =  create_buffer("Gl_acc1",Gl_acct)

        h_compli_obj_list = {}
        h_compli = H_compli()
        h_art = H_artikel()
        for h_compli.datum, h_compli.artnr, h_compli.departement, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art._recid in db_session.query(H_compli.datum, H_compli.artnr, H_compli.departement, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                 (H_compli.datum >= date1) & (H_compli.datum <= date2) & (H_compli.departement != ldry) & (H_compli.departement != dstore) & (H_compli.betriebsnr == 0)).order_by(H_compli.datum, H_compli.rechnr).all():
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
            com_artnr = artikel.artnr
            com_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            com_fibu = gl_acct.fibukonto

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
            flag = 0

            if artikel.endkum == f_endkum or artikel.umsatzart == 3 or artikel.umsatzart == 5:
                flag = 1

            elif artikel.endkum == b_endkum or artikel.umsatzart == 6:
                flag = 2

            s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto.lower()  == (com_fibu).lower()  and s_list.reihenfolge == 4 and s_list.flag == flag), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.reihenfolge = 4
                s_list.lager_nr = com_artnr
                s_list.fibukonto = com_fibu
                s_list.bezeich = com_bezeich
                s_list.flag = flag


            cost =  to_decimal("0")

            h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

            if h_cost and h_cost.betrag != 0:
                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)

            elif not h_cost or (h_cost and h_cost.betrag == 0):
                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)
            s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(cost)

            if h_compli.datum == date2:
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(cost)


    def step_three_food(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 1
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        type_of_acct:int = 0
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        l_op_obj_list = {}
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto) & ((Gl_acct.acc_type == 5) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.datum >= date1) & (L_op.datum <= date2) & (L_op.lager_nr != main_storage)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            type_of_acct = gl_acct.acc_type

            if l_op.stornogrund != "":

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if gl_acct1:
                    type_of_acct = gl_acct1.acc_type
                    fibukonto = gl_acct1.fibukonto
                    bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                        gl_acct1.bezeich.upper()

            if fibukonto.lower()  == (food_bev).lower() :
                pass

            elif fibukonto.lower()  == (bev_food).lower() :
                pass
            else:

                if type_of_acct == 3 or type_of_acct == 4 or type_of_acct == 5:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == 5 and s_list.flag == flag), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.reihenfolge = 5
                        s_list.fibukonto = fibukonto
                        s_list.bezeich = bezeich
                        s_list.flag = flag


                    s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                    if l_op.datum == date2:
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_three_bev(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 2
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        type_of_acct:int = 0
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        l_op_obj_list = {}
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto) & ((Gl_acct.acc_type == 5) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.datum >= date1) & (L_op.datum <= date2) & (L_op.lager_nr != main_storage)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            type_of_acct = gl_acct.acc_type

            if l_op.stornogrund != "":

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto
                    bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                            gl_acct1.bezeich.upper()
                    type_of_acct = gl_acct1.acc_type

            if fibukonto.lower()  == (food_bev).lower() :
                pass

            elif fibukonto.lower()  == (bev_food).lower() :
                pass
            else:

                if type_of_acct == 3 or type_of_acct == 4 or type_of_acct == 5:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == 5 and s_list.flag == flag), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.reihenfolge = 5
                        s_list.fibukonto = fibukonto
                        s_list.bezeich = bezeich
                        s_list.flag = flag


                    s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                    if l_op.datum == date2:
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def func_food_to_bev(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        l_op_obj_list = {}
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                 (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.datum >= date1) & (L_op.datum <= date2) & ((L_op.stornogrund == (bev_food).lower()) | (L_op.stornogrund == (food_bev).lower()))).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.stornogrund.lower()  == (food_bev).lower() :

                s_list = query(s_list_list, filters=(lambda s_list: s_list.reihenfolge == 3 and s_list.flag == 2), first=True)

                if l_op.lager_nr >= 1:
                    s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                    if l_op.datum == date2:
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
                else:
                    s_list.t_betrag1 =  to_decimal(s_list.t_betrag1) + to_decimal(l_op.warenwert)

                    if l_op.datum == date2:
                        s_list.betrag1 =  to_decimal(s_list.betrag1) + to_decimal(l_op.warenwert)

            elif l_op.stornogrund.lower()  == (bev_food).lower() :

                s_list = query(s_list_list, filters=(lambda s_list: s_list.reihenfolge == 3 and s_list.flag == 1), first=True)

                if l_op.lager_nr >= 1:
                    s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                    if l_op.datum == date2:
                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)
                else:
                    s_list.t_betrag1 =  to_decimal(s_list.t_betrag1) + to_decimal(l_op.warenwert)

                    if l_op.datum == date2:
                        s_list.betrag1 =  to_decimal(s_list.betrag1) + to_decimal(l_op.warenwert)


    def step_four(f_eknr:int, b_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        serv_taxable:bool = False
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
                    h_service, h_mwst = get_output(calc_servvat(artikel.departement, artikel.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    amount =  to_decimal(umsatz.betrag) / to_decimal((1) + to_decimal(h_service) + to_decimal(h_mwst))

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales =  to_decimal(f_sales) + to_decimal(amount)
                        tf_sales =  to_decimal(tf_sales) + to_decimal(amount)

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales =  to_decimal(b_sales) + to_decimal(amount)
                        tb_sales =  to_decimal(tb_sales) + to_decimal(amount)


    def step_five(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, f_eknr, b_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal pvilanguage, from_grp, food, bev, date1, date2, incl_initoh, incl_streq


        nonlocal fbflash_list, s_list
        nonlocal fbflash_list_list, s_list_list

        flag:int = 0
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        type_of_acct:int = 0
        qty:Decimal = to_decimal("0.0")
        qty1:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_qty1:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)
        qty =  to_decimal("0")
        val =  to_decimal("0")
        qty1 =  to_decimal("0")

        if from_grp == food:
            flag = 1

            l_op_obj_list = {}
            for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("REQ").lower()) & (L_ophdr.docu_nr == L_op.lscheinnr)).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto) & ((Gl_acct.acc_type == 5) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                     (L_op.datum >= date1) & (L_op.datum <= date2) & (L_op.op_art >= 13) & (L_op.op_art <= 14) & (L_op.herkunftflag <= 2) & (L_op.loeschflag <= 1)).order_by(L_op.reorgflag, L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 6 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 6
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

        elif from_grp == bev:
            flag = 2

            l_op_obj_list = {}
            for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("REQ").lower()) & (L_ophdr.docu_nr == L_op.lscheinnr)).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto) & ((Gl_acct.acc_type == 5) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                     (L_op.datum >= date1) & (L_op.datum <= date2) & (L_op.op_art >= 13) & (L_op.op_art <= 14) & (L_op.herkunftflag <= 2) & (L_op.loeschflag <= 1)).order_by(L_op.reorgflag, L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                s_list = query(s_list_list, filters=(lambda s_list: s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 6 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 6
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

    if incl_initoh:
        anf_store = 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
    ldry = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
    dstore = htparam.finteger

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
    f_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
    b_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    fl_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    bl_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    coa_format = htparam.fchar

    if incl_streq == False:

        if from_grp == food:
            step_food1(fl_eknr, bl_eknr)
            step_food2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_food(fl_eknr, bl_eknr)
            func_food_to_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)

        elif from_grp == bev:
            step_bev1(fl_eknr, bl_eknr)
            step_bev2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_bev(fl_eknr, bl_eknr)
            func_food_to_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)
    else:

        if from_grp == food:
            step_food1(fl_eknr, bl_eknr)
            step_food2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_food(fl_eknr, bl_eknr)
            func_food_to_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)
            step_five(fl_eknr, bl_eknr)

        elif from_grp == bev:
            step_bev1(fl_eknr, bl_eknr)
            step_bev2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_bev(fl_eknr, bl_eknr)
            func_food_to_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)
            step_five(fl_eknr, bl_eknr)

    if from_grp == food or from_grp == 0:
        d_betrag =  to_decimal("0")
        m_betrag =  to_decimal("0")
        d1_betrag =  to_decimal("0")
        m1_betrag =  to_decimal("0")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.cost_alloc = translateExtended ("** food **", lvcarea, "")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        t_betrag1 =  to_decimal("0")
        beg_oh =  to_decimal("0")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("OPENING INVENTORY", lvcarea, "")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= anf_store)).order_by(L_lager._recid).all():
            betrag =  to_decimal("0")

            l_bestand_obj_list = {}
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == 1)).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                betrag =  to_decimal(betrag) + to_decimal(l_bestand.val_anf_best)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(l_bestand.val_anf_best)

                if l_lager.lager_nr > 1:
                    beg_oh =  to_decimal(beg_oh) + to_decimal(l_bestand.val_anf_best)

                    if incl_initoh:
                        m_betrag =  to_decimal(m_betrag) + to_decimal(l_bestand.val_anf_best)

            if betrag > 0:
                fbflash_list = Fbflash_list()
                fbflash_list_list.append(fbflash_list)


                if not long_digit:
                    fbflash_list.cost_alloc = l_lager.bezeich
                    fbflash_list.mtd_cons = to_string(betrag, "->,>>>,>>>,>>9.99")


                else:
                    fbflash_list.cost_alloc = l_lager.bezeich
                    fbflash_list.mtd_cons = to_string(betrag, "->>>>,>>>,>>>,>>9")

        if t_betrag1 > 0:
            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)

            fbflash_list.flag = 1

            if not long_digit:
                fbflash_list.trans_to_storage = translateExtended ("T o t a l", lvcarea, "")
                fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.flag = 1
                fbflash_list.trans_to_storage = translateExtended ("T o t a l", lvcarea, "")
                fbflash_list.mtd_cons = to_string(t_betrag1, "->>>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("transFER TO SIDE STORE", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 1), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("DIRECT PURCHASED", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 2), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if incl_streq :
            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)

            fbflash_list.trans_to_storage = translateExtended ("STORE REQUISITION", lvcarea, "")
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 6), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)

                fbflash_list = Fbflash_list()
                fbflash_list_list.append(fbflash_list)


                if not long_digit:
                    fbflash_list.cost_alloc = s_list.bezeich
                    fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                    fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


                else:
                    fbflash_list.cost_alloc = s_list.bezeich
                    fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                    fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


                fbflash_list = Fbflash_list()
                fbflash_list_list.append(fbflash_list)

            fbflash_list.flag = 1

            if not long_digit:
                fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
                fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
                fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


        s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
        d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag) + to_decimal(s_list.betrag1)
        m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag) + to_decimal(s_list.t_betrag1)


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.cost_alloc = s_list.bezeich
            fbflash_list.day_cons = to_string((s_list.betrag + s_list.betrag1) , "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string((s_list.t_betrag + s_list.t_betrag1) , "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.cost_alloc = s_list.bezeich
            fbflash_list.day_cons = to_string((s_list.betrag + s_list.betrag1) , " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string((s_list.t_betrag + s_list.t_betrag1) , " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("GROSS CONSUMPTION cost", lvcarea, "")
            fbflash_list.day_cons = to_string(d_betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(m_betrag, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("GROSS CONSUMPTION cost", lvcarea, "")
            fbflash_list.day_cons = to_string(d_betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(m_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("LESS BY:", lvcarea, "")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("COMPLIMENT cost", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 4), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
            m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("DEPARTMENT EXPENSES", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 5), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
            m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
        betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
        t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
        d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
        m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
        d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
        m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)

        if s_list.t_betrag != 0:
            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string((s_list.betrag) , "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string((s_list.t_betrag) , "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string((s_list.betrag) , " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string((s_list.t_betrag) , " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("TOTAL EXPENSES", lvcarea, "")
            fbflash_list.day_cons = to_string(d1_betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(m1_betrag, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("TOTAL EXPENSES", lvcarea, "")
            fbflash_list.day_cons = to_string(d1_betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(m1_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("NET CONSUMPTION cost", lvcarea, "")
            fbflash_list.day_cons = to_string(d_betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(m_betrag, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("NET CONSUMPTION cost", lvcarea, "")
            fbflash_list.day_cons = to_string(d_betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(m_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.cost_alloc = translateExtended ("Nett food Sales", lvcarea, "")
            fbflash_list.day_cons = to_string(f_sales, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(tf_sales, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.cost_alloc = translateExtended ("Nett food Sales", lvcarea, "")
            fbflash_list.day_cons = to_string(f_sales, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(tf_sales, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.cost_alloc = translateExtended ("R a t i o cost:Sales (%)", lvcarea, "")

        if f_sales != 0:
            fbflash_list.day_cons = to_string((d_betrag / f_sales * 100) , "->,>>>,>>>,>>9.99")
        else:
            fbflash_list.day_cons = to_string(0, "->,>>>,>>>,>>9.99")

        if tf_sales != 0:
            fbflash_list.mtd_cons = to_string((m_betrag / tf_sales) * 100, "->,>>>,>>>,>>9.99")
        else:
            fbflash_list.mtd_cons = to_string(0, "->,>>>,>>>,>>9.99")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

    done = True

    if from_grp == bev:
        d_betrag =  to_decimal("0")
        m_betrag =  to_decimal("0")
        d1_betrag =  to_decimal("0")
        m1_betrag =  to_decimal("0")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.cost_alloc = translateExtended ("** BEVERAGE **", lvcarea, "")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        t_betrag1 =  to_decimal("0")
        beg_oh =  to_decimal("0")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("OPENING INVENTORY", lvcarea, "")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= anf_store)).order_by(L_lager._recid).all():
            betrag =  to_decimal("0")

            l_bestand_obj_list = {}
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == 2)).filter(
                     (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                betrag =  to_decimal(betrag) + to_decimal(l_bestand.val_anf_best)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(l_bestand.val_anf_best)

                if l_lager.lager_nr > 1:
                    beg_oh =  to_decimal(beg_oh) + to_decimal(l_bestand.val_anf_best)

                    if incl_initoh:
                        m_betrag =  to_decimal(m_betrag) + to_decimal(l_bestand.val_anf_best)

            if betrag > 0:
                fbflash_list = Fbflash_list()
                fbflash_list_list.append(fbflash_list)


                if not long_digit:
                    fbflash_list.cost_alloc = l_lager.bezeich
                    fbflash_list.mtd_cons = to_string(betrag, "->,>>>,>>>,>>9.99")


                else:
                    fbflash_list.cost_alloc = l_lager.bezeich
                    fbflash_list.mtd_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")

        if t_betrag1 > 0:
            fbflash_list.flag = 1
            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.trans_to_storage = translateExtended ("T o t a l", lvcarea, "")
                fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.trans_to_storage = translateExtended ("T o t a l", lvcarea, "")
                fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("transFER TO SIDE STORE", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 1), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("DIRECT PURCHASED", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 2), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if incl_streq :
            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)

            fbflash_list.trans_to_storage = translateExtended ("STORE REQUISITION", lvcarea, "")
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 6), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)

                fbflash_list = Fbflash_list()
                fbflash_list_list.append(fbflash_list)


                if not long_digit:
                    fbflash_list.cost_alloc = s_list.bezeich
                    fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                    fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


                else:
                    fbflash_list.cost_alloc = s_list.bezeich
                    fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                    fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


                fbflash_list = Fbflash_list()
                fbflash_list_list.append(fbflash_list)

            fbflash_list.flag = 1

            if not long_digit:
                fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
                fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
                fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


        s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
        d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag) + to_decimal(s_list.betrag1)
        m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag) + to_decimal(s_list.t_betrag1)


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.cost_alloc = s_list.bezeich
            fbflash_list.day_cons = to_string((s_list.betrag + s_list.betrag1) , "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string((s_list.t_betrag + s_list.t_betrag1) , "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.cost_alloc = s_list.bezeich
            fbflash_list.day_cons = to_string((s_list.betrag + s_list.betrag1) , " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string((s_list.t_betrag + s_list.t_betrag1) , " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("GROSS CONSUMPTION cost", lvcarea, "")
            fbflash_list.day_cons = to_string(d_betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(m_betrag, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("GROSS CONSUMPTION cost", lvcarea, "")
            fbflash_list.day_cons = to_string(d_betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(m_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("LESS BY:", lvcarea, "")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("COMPLIMENT cost", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 4), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
            m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("DEPARTMENT EXPENSES", lvcarea, "")
        betrag =  to_decimal("0")
        t_betrag1 =  to_decimal("0")

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 5), sort_by=[("bezeich",False)]):
            betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
            t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
            d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
            m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
            d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
            m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)


            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string(s_list.betrag, " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string(s_list.t_betrag, " ->>>,>>>,>>>,>>9")

        s_list = query(s_list_list, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
        betrag =  to_decimal(betrag) + to_decimal(s_list.betrag) + to_decimal(s_list.betrag1)
        t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag) + to_decimal(s_list.t_betrag1)
        d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag) + to_decimal(s_list.betrag1)
        m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag) + to_decimal(s_list.t_betrag1)
        d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag) - to_decimal(s_list.betrag1)
        m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag) - to_decimal(s_list.t_betrag1)

        if s_list.t_betrag != 0:
            fbflash_list = Fbflash_list()
            fbflash_list_list.append(fbflash_list)


            if not long_digit:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string((s_list.betrag) , "->,>>>,>>>,>>9.99")
                fbflash_list.mtd_cons = to_string((s_list.t_betrag) , "->,>>>,>>>,>>9.99")


            else:
                fbflash_list.cost_alloc = s_list.bezeich
                fbflash_list.day_cons = to_string((s_list.betrag) , " ->>>,>>>,>>>,>>9")
                fbflash_list.mtd_cons = to_string((s_list.t_betrag) , " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.flag = 1

        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(t_betrag1, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("Sub T o t a l", lvcarea, "")
            fbflash_list.day_cons = to_string(betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(t_betrag1, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = translateExtended ("TOTAL EXPENSES", lvcarea, "")
            fbflash_list.day_cons = to_string(d1_betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(m1_betrag, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = translateExtended ("TOTAL EXPENSES", lvcarea, "")
            fbflash_list.day_cons = to_string(d1_betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(m1_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.trans_to_storage = to_string(translateExtended ("NET CONSUMPTION cost", lvcarea, "") , "x(24)")
            fbflash_list.day_cons = to_string(d_betrag, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(m_betrag, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.trans_to_storage = to_string(translateExtended ("NET CONSUMPTION cost", lvcarea, "") , "x(24)")
            fbflash_list.day_cons = to_string(d_betrag, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(m_betrag, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)


        if not long_digit:
            fbflash_list.cost_alloc = translateExtended ("Nett Beverage Sales", lvcarea, "")
            fbflash_list.day_cons = to_string(b_sales, "->,>>>,>>>,>>9.99")
            fbflash_list.mtd_cons = to_string(tb_sales, "->,>>>,>>>,>>9.99")


        else:
            fbflash_list.cost_alloc = translateExtended ("Nett Beverage Sales", lvcarea, "")
            fbflash_list.day_cons = to_string(b_sales, " ->>>,>>>,>>>,>>9")
            fbflash_list.mtd_cons = to_string(tb_sales, " ->>>,>>>,>>>,>>9")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.cost_alloc = translateExtended ("R a t i o cost:Sales (%)", lvcarea, "")

        if b_sales != 0:
            fbflash_list.day_cons = to_string((d_betrag / b_sales * 100) , "->,>>>,>>>,>>9.99")
        else:
            fbflash_list.day_cons = to_string(0, "->,>>>,>>>,>>9.99")

        if tb_sales != 0:
            fbflash_list.mtd_cons = to_string((m_betrag / tb_sales) * 100, "->,>>>,>>>,>>9.99")
        else:
            fbflash_list.mtd_cons = to_string(0, "->,>>>,>>>,>>9.99")
    done = True

    return generate_output()