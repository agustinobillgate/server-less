#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 25/7/2025
# gitlab: 653
# if availabe s_list
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, L_lager, L_artikel, L_op, H_compli, Hoteldpt, Gl_acct, H_artikel, Exrate, Artikel, H_cost, L_ophdr, Umsatz

def fb_flash1_btn_go_webbl(pvilanguage:int, from_grp:int, food:int, main_storage:int, f_store:int, t_store:int, date1:date, date2:date, foreign_nr:int, exchg_rate:Decimal, double_currency:bool):

    prepare_cache ([Htparam, L_lager, L_op, H_compli, Hoteldpt, Gl_acct, H_artikel, Exrate, Artikel, H_cost, Umsatz])

    fb_flash_data = []
    lvcarea:string = "fb-flash1"
    done:bool = False
    dstore:int = 0
    curr_store:int = 0
    long_digit:bool = False
    f_sales:Decimal = to_decimal("0.0")
    b_sales:Decimal = to_decimal("0.0")
    tf_sales:Decimal = to_decimal("0.0")
    tb_sales:Decimal = to_decimal("0.0")
    bev_food:string = ""
    food_bev:string = ""
    coa_format:string = ""
    htparam = l_lager = l_artikel = l_op = h_compli = hoteldpt = gl_acct = h_artikel = exrate = artikel = h_cost = l_ophdr = umsatz = None

    s_list = fb_flash = l_store = None

    s_list_data, S_list = create_model("S_list", {"nr":int, "reihenfolge":int, "lager_nr":int, "fibukonto":string, "bezeich":string, "flag":int, "betrag":Decimal, "t_betrag":Decimal}, {"reihenfolge": 1, "flag": 2})
    fb_flash_data, Fb_flash = create_model("Fb_flash", {"flag":int, "bezeich":string, "c_alloc":string, "t_consumed":Decimal, "mtd_consumed":Decimal})

    L_store = create_buffer("L_store",L_lager)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        return {"fb-flash": fb_flash_data}

    def create_food():

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

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
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})

        if htparam:
            f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})

        if htparam:
            b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})

        if htparam:
            fl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})

        if htparam:
            bl_eknr = htparam.finteger
        fb_flash = Fb_flash()
        fb_flash_data.append(fb_flash)

        fb_flash = Fb_flash()
        fb_flash_data.append(fb_flash)

        fb_flash.c_alloc = "** food **"
        fb_flash = Fb_flash()
        fb_flash_data.append(fb_flash)


        for l_store in db_session.query(L_store).filter(
                 (L_store.lager_nr != main_storage) & (L_store.lager_nr >= f_store) & (L_store.lager_nr <= t_store) & (L_store.betriebsnr > 0)).order_by(L_store.lager_nr).all():
            s_list_data.clear()
            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.c_alloc = l_store.bezeich
            dstore = l_store.betriebsnr
            curr_store = l_store.lager_nr
            step_food1(fl_eknr, bl_eknr)

            if l_store.betriebsnr > 0:
                step_food1a()
            step_food2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_food(fl_eknr, bl_eknr)
            func_food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr, l_store.lager_nr)
            d_betrag =  to_decimal("0")
            m_betrag =  to_decimal("0")
            d1_betrag =  to_decimal("0")
            m1_betrag =  to_decimal("0")
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 1), sort_by=[("nr",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 2), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)

            s_list = query(s_list_data, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
            # Rd, 25/7/2025
            # if available
            if s_list:
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "GROSS CONSUMPTION cost"
            fb_flash.t_consumed =  to_decimal(d_betrag)
            fb_flash.mtd_consumed =  to_decimal(m_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "LESS BY:"
            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "COMPLIMENT cost"
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 4), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
                m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.flag = 1
            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed =  to_decimal(betrag)
            fb_flash.mtd_consumed =  to_decimal(t_betrag1)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "DEPARTMENT EXPENSES"
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 5), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
                m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)

            s_list = query(s_list_data, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
            # Rd, 25/7/2025
            # if available
            if s_list:
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
                m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.flag = 1
            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed =  to_decimal(betrag)
            fb_flash.mtd_consumed =  to_decimal(t_betrag1)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "TOTAL EXPENSES"
            fb_flash.t_consumed =  to_decimal(d1_betrag)
            fb_flash.mtd_consumed =  to_decimal(m1_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "NET CONSUMPTION cost"
            fb_flash.t_consumed =  to_decimal(d_betrag)
            fb_flash.mtd_consumed =  to_decimal(m_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.c_alloc = "Nett food Sales"
            fb_flash.t_consumed =  to_decimal(f_sales)
            fb_flash.mtd_consumed =  to_decimal(tf_sales)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.flag = 99
            fb_flash.c_alloc = "R a t i o cost:Sales (%)"

            if f_sales != 0:
                fb_flash.t_consumed = ( to_decimal(d_betrag) / to_decimal(f_sales) * to_decimal(100))
            else:
                fb_flash.t_consumed =  to_decimal("0")

            if tf_sales != 0:
                fb_flash.mtd_consumed = ( to_decimal(m_betrag) / to_decimal(tf_sales)) * to_decimal("100")
            else:
                fb_flash.mtd_consumed =  to_decimal("0")
            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

        done = True


    def create_bev():

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

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
        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        fl_eknr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        bl_eknr = htparam.finteger
        fb_flash = Fb_flash()
        fb_flash_data.append(fb_flash)

        fb_flash = Fb_flash()
        fb_flash_data.append(fb_flash)

        fb_flash.c_alloc = "** BEVERAGE **"
        fb_flash = Fb_flash()
        fb_flash_data.append(fb_flash)


        for l_store in db_session.query(L_store).filter(
                 (L_store.lager_nr != main_storage) & (L_store.lager_nr >= f_store) & (L_store.lager_nr <= t_store) & (L_store.betriebsnr > 0)).order_by(L_store.lager_nr).all():
            s_list_data.clear()
            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.c_alloc = l_store.bezeich
            dstore = l_store.betriebsnr
            curr_store = l_store.lager_nr
            step_bev1(fl_eknr, bl_eknr)

            if l_store.betriebsnr > 0:
                step_bev1a()
            step_bev2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_bev(fl_eknr, bl_eknr)
            func_food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr, l_store.lager_nr)
            d_betrag =  to_decimal("0")
            m_betrag =  to_decimal("0")
            d1_betrag =  to_decimal("0")
            m1_betrag =  to_decimal("0")
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 1), sort_by=[("nr",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 2), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)

            s_list = query(s_list_data, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
            # Rd, 25/7/2025
            # if available
            if s_list:
                d_betrag =  to_decimal(d_betrag) + to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) + to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "GROSS CONSUMPTION cost"
            fb_flash.t_consumed =  to_decimal(d_betrag)
            fb_flash.mtd_consumed =  to_decimal(m_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "LESS BY:"


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "COMPLIMENT cost"


            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 4), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
                m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed =  to_decimal(betrag)
            fb_flash.mtd_consumed =  to_decimal(t_betrag1)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "DEPARTMENT EXPENSES"
            betrag =  to_decimal("0")
            t_betrag1 =  to_decimal("0")

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.flag == 2 and s_list.reihenfolge == 5), sort_by=[("bezeich",False)]):
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
                m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)

            s_list = query(s_list_data, filters=(lambda s_list: s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
            # Rd, 25/7/2025
            # if available
            if s_list:
                betrag =  to_decimal(betrag) + to_decimal(s_list.betrag)
                t_betrag1 =  to_decimal(t_betrag1) + to_decimal(s_list.t_betrag)
                d1_betrag =  to_decimal(d1_betrag) + to_decimal(s_list.betrag)
                m1_betrag =  to_decimal(m1_betrag) + to_decimal(s_list.t_betrag)
                d_betrag =  to_decimal(d_betrag) - to_decimal(s_list.betrag)
                m_betrag =  to_decimal(m_betrag) - to_decimal(s_list.t_betrag)
                fb_flash = Fb_flash()
                fb_flash_data.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed =  to_decimal(s_list.betrag)
                fb_flash.mtd_consumed =  to_decimal(s_list.t_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.flag = 1
            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed =  to_decimal(betrag)
            fb_flash.mtd_consumed =  to_decimal(t_betrag1)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "TOTAL EXPENSES"
            fb_flash.t_consumed =  to_decimal(d1_betrag)
            fb_flash.mtd_consumed =  to_decimal(m1_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.bezeich = "NET CONSUMPTION cost"
            fb_flash.t_consumed =  to_decimal(d_betrag)
            fb_flash.mtd_consumed =  to_decimal(m_betrag)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.c_alloc = "Nett Beverage Sales"
            fb_flash.t_consumed =  to_decimal(b_sales)
            fb_flash.mtd_consumed =  to_decimal(tb_sales)


            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

            fb_flash.flag = 99
            fb_flash.c_alloc = "R a t i o cost:Sales (%)"

            if b_sales != 0:
                fb_flash.t_consumed =  to_decimal(d_betrag) / to_decimal(b_sales) * to_decimal("100")

            if tb_sales != 0:
                fb_flash.mtd_consumed = ( to_decimal(m_betrag) / to_decimal(tb_sales)) * to_decimal("100")
            fb_flash = Fb_flash()
            fb_flash_data.append(fb_flash)

        done = True


    def step_food1(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        flag:int = 1

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_store)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = 1
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("TRANSFER TO SIDE STORE", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = {}
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_op.loeschflag <= 1) & (L_op.op_art == 4) & (L_op.herkunftflag == 1) & ((L_op.lager_nr == curr_store) | (L_op.pos == curr_store)) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.lager_nr == curr_store:
                s_list.t_betrag =  to_decimal(s_list.t_betrag) - to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

            if l_op.pos == curr_store:
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_food1a():

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        curr_dept:int = 0
        flag:int = 1

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_store)]})
        curr_dept = l_lager.betriebsnr
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = 2
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER IN", lvcarea, "")
        s_list.flag = flag
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = 3
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER OUT", lvcarea, "")
        s_list.flag = flag

        for h_compli in db_session.query(H_compli).filter(
                 (H_compli.datum >= date1) & (H_compli.datum <= date2) & (H_compli.betriebsnr > 0) & (H_compli.p_artnr == 1)).order_by(H_compli.departement).all():

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.betriebsnr)]})

            if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nr == 2), first=True)
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(h_compli.epreis)

                if h_compli.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(h_compli.epreis)
            else:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.departement)]})

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.nr == 3), first=True)
                    s_list.t_betrag =  to_decimal(s_list.t_betrag) - to_decimal(h_compli.epreis)

                    if h_compli.datum == date2:
                        s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(h_compli.epreis)


    def step_bev1(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        flag:int = 2

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_store)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = 1
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("TRANSFER TO SIDE STORE", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = {}
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_op.loeschflag <= 1) & (L_op.op_art == 4) & (L_op.herkunftflag == 1) & ((L_op.lager_nr == curr_store) | (L_op.pos == curr_store)) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.lager_nr == curr_store:
                s_list.t_betrag =  to_decimal(s_list.t_betrag) - to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(l_op.warenwert)

            if l_op.pos == curr_store:
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_bev1a():

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        curr_dept:int = 0
        flag:int = 2

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_store)]})
        curr_dept = l_lager.betriebsnr
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = 2
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER IN", lvcarea, "")
        s_list.flag = flag
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = 3
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER OUT", lvcarea, "")
        s_list.flag = flag

        for h_compli in db_session.query(H_compli).filter(
                 (H_compli.datum >= date1) & (H_compli.datum <= date2) & (H_compli.betriebsnr > 0) & (H_compli.p_artnr == 2)).order_by(H_compli.departement).all():

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.betriebsnr)]})

            if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nr == 2), first=True)
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(h_compli.epreis)

                if h_compli.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(h_compli.epreis)
            else:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, h_compli.departement)]})

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_data, filters=(lambda s_list: s_list.nr == 3), first=True)
                    s_list.t_betrag =  to_decimal(s_list.t_betrag) - to_decimal(h_compli.epreis)

                    if h_compli.datum == date2:
                        s_list.betrag =  to_decimal(s_list.betrag) - to_decimal(h_compli.epreis)


    def step_food2(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        flag:int = 1

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_store)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("DIRECT PURCHASED", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = {}
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.datum >= date1) & (L_op.datum <= date2) & (L_op.lager_nr == curr_store)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

            if l_op.datum == date2:
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_bev2(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        flag:int = 2

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_store)]})
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("DIRECT PURCHASED", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = {}
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1) & (L_op.datum >= date1) & (L_op.datum <= date2) & (L_op.lager_nr == curr_store)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

            if l_op.datum == date2:
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def beverage_to_food():

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})

        if htparam:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

            if gl_acct:
                bev_food = htparam.fchar
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.reihenfolge = 3
                s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                        gl_acct.bezeich.upper()
                s_list.flag = 1


    def food_to_beverage():

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})

        if htparam:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

            if gl_acct:
                food_bev = htparam.fchar
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.reihenfolge = 3
                s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                        gl_acct.bezeich.upper()
                s_list.flag = 2


    def step_two(f_endkum:int, b_endkum:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

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

        if dstore == 0:

            return

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num > 0) & ((Hoteldpt.num == l_store.betriebsnr) | (Hoteldpt.betriebsnr == l_store.lager_nr))).order_by(Hoteldpt.num).all():

            h_compli_obj_list = {}
            h_compli = H_compli()
            h_art = H_artikel()
            for h_compli.betriebsnr, h_compli.epreis, h_compli.departement, h_compli.datum, h_compli.artnr, h_compli.anzahl, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art._recid in db_session.query(H_compli.betriebsnr, H_compli.epreis, H_compli.departement, H_compli.datum, H_compli.artnr, H_compli.anzahl, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                     (H_compli.datum >= date1) & (H_compli.datum <= date2) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0)).order_by(H_compli.datum, H_compli.rechnr).all():
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

                if artikel.endkum == f_endkum:
                    flag = 1

                elif artikel.endkum == b_endkum:
                    flag = 2

                s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (com_fibu).lower()  and s_list.reihenfolge == 4 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

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

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        flag:int = 1
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        l_op_obj_list = {}
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto) & ((Gl_acct.acc_type == 5) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.lager_nr == curr_store) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()

            if l_op.stornogrund != "":

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto
                    bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                        gl_acct1.bezeich.upper()

            if fibukonto.lower()  == (food_bev).lower() :
                pass

            elif fibukonto.lower()  == (bev_food).lower() :
                pass
            else:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == 5 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = 5
                    s_list.fibukonto = fibukonto
                    s_list.bezeich = bezeich
                    s_list.flag = flag
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_three_bev(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        flag:int = 2
        fibukonto:string = ""
        bezeich:string = ""
        gl_acct1 = None
        Gl_acct1 =  create_buffer("Gl_acct1",Gl_acct)

        l_op_obj_list = {}
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) & (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == L_ophdr.fibukonto) & ((Gl_acct.acc_type == 5) | (Gl_acct.acc_type == 3) | (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_op.pos > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 3) & (L_op.lager_nr == curr_store) & (L_op.datum >= date1) & (L_op.datum <= date2)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()

            if l_op.stornogrund != "":

                gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, l_op.stornogrund)]})

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto
                    bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                        gl_acct1.bezeich.upper()

            if fibukonto.lower()  == (food_bev).lower() :
                pass

            elif fibukonto.lower()  == (bev_food).lower() :
                pass
            else:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.fibukonto.lower()  == (fibukonto).lower()  and s_list.reihenfolge == 5 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.reihenfolge = 5
                    s_list.fibukonto = fibukonto
                    s_list.bezeich = bezeich
                    s_list.flag = flag
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def func_food_bev(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        l_op_obj_list = {}
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) & ((L_artikel.endkum == fl_eknr) | (L_artikel.endkum == bl_eknr))).filter(
                 (L_op.op_art == 3) & (L_op.loeschflag <= 1) & (L_op.datum >= date1) & (L_op.datum <= date2) & ((L_op.stornogrund == (bev_food).lower()) | (L_op.stornogrund == (food_bev).lower())) & (L_op.lager_nr == curr_store)).order_by(L_op._recid).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.stornogrund.lower()  == (food_bev).lower() :

                s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 3 and s_list.flag == 2), first=True)
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)

            elif l_op.stornogrund.lower()  == (bev_food).lower() :

                s_list = query(s_list_data, filters=(lambda s_list: s_list.reihenfolge == 3 and s_list.flag == 1), first=True)
                s_list.t_betrag =  to_decimal(s_list.t_betrag) + to_decimal(l_op.warenwert)

                if l_op.datum == date2:
                    s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(l_op.warenwert)


    def step_four(f_eknr:int, b_eknr:int, store_nr:int):

        nonlocal fb_flash_data, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal pvilanguage, from_grp, food, main_storage, f_store, t_store, date1, date2, foreign_nr, exchg_rate, double_currency
        nonlocal l_store


        nonlocal s_list, fb_flash, l_store
        nonlocal s_list_data, fb_flash_data

        h_service:Decimal = to_decimal("0.0")
        h_mwst:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        serv_taxable:bool = False
        f_sales =  to_decimal("0")
        b_sales =  to_decimal("0")
        tf_sales =  to_decimal("0")
        tb_sales =  to_decimal("0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_taxable = htparam.flogical

        if dstore == 0:

            return

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 ((Hoteldpt.num == dstore) | (Hoteldpt.betriebsnr == store_nr))).order_by(Hoteldpt.num).all():

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    coa_format = htparam.fchar

    if from_grp == food:
        create_food()
    else:
        create_bev()

    return generate_output()