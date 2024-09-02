from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, L_lager, L_artikel, L_op, H_compli, Hoteldpt, Gl_acct, H_artikel, Exrate, Artikel, H_cost, L_ophdr, Umsatz

def fb_flash1_btn_go_webbl(pvilanguage:int, from_grp:int, food:int, main_storage:int, f_store:int, t_store:int, date1:date, date2:date, foreign_nr:int, exchg_rate:decimal, double_currency:bool):
    fb_flash_list = []
    lvcarea:str = "fb_flash1"
    done:bool = False
    dstore:int = 0
    curr_store:int = 0
    long_digit:bool = False
    f_sales:decimal = 0
    b_sales:decimal = 0
    tf_sales:decimal = 0
    tb_sales:decimal = 0
    bev_food:str = ""
    food_bev:str = ""
    coa_format:str = ""
    htparam = l_lager = l_artikel = l_op = h_compli = hoteldpt = gl_acct = h_artikel = exrate = artikel = h_cost = l_ophdr = umsatz = None

    s_list = fb_flash = l_store = h_art = gl_acc1 = gl_acct1 = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "reihenfolge":int, "lager_nr":int, "fibukonto":str, "bezeich":str, "flag":int, "betrag":decimal, "t_betrag":decimal}, {"reihenfolge": 1, "flag": 2})
    fb_flash_list, Fb_flash = create_model("Fb_flash", {"flag":int, "bezeich":str, "c_alloc":str, "t_consumed":decimal, "mtd_consumed":decimal})

    L_store = L_lager
    H_art = H_artikel
    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list
        return {"fb-flash": fb_flash_list}

    def create_food():

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        betrag:decimal = 0
        t_betrag1:decimal = 0
        t_betrag2:decimal = 0
        d_betrag:decimal = 0
        m_betrag:decimal = 0
        d1_betrag:decimal = 0
        m1_betrag:decimal = 0
        flag:int = 0
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        amount:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        fl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        bl_eknr = finteger
        fb_flash = Fb_flash()
        fb_flash_list.append(fb_flash)

        fb_flash = Fb_flash()
        fb_flash_list.append(fb_flash)

        fb_flash.c_alloc = "** food **"
        fb_flash = Fb_flash()
        fb_flash_list.append(fb_flash)


        for l_store in db_session.query(L_store).filter(
                (L_store.lager_nr != main_storage) &  (L_store.lager_nr >= f_store) &  (L_store.lager_nr <= t_store) &  (L_store.betriebsnr > 0)).all():
            s_list_list.clear()
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

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
            food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr, l_store.lager_nr)
            d_betrag = 0
            m_betrag = 0
            d1_betrag = 0
            m1_betrag = 0
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 1)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d_betrag = d_betrag + s_list.betrag
                m_betrag = m_betrag + s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed = s_list.betrag
                fb_flash.mtd_consumed = s_list.t_betrag


            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 2)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d_betrag = d_betrag + s_list.betrag
                m_betrag = m_betrag + s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed = betrag
                fb_flash.mtd_consumed = t_betrag

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
            d_betrag = d_betrag + s_list.betrag
            m_betrag = m_betrag + s_list.t_betrag
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = s_list.bezeich
            fb_flash.t_consumed = betrag
            fb_flash.mtd_consumed = t_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "GROSS CONSUMPTION cost"
            fb_flash.t_consumed = d_betrag
            fb_flash.mtd_consumed = m_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "LESS BY:"
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "COMPLIMENT cost"
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 4)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d1_betrag = d1_betrag + s_list.betrag
                m1_betrag = m1_betrag + s_list.t_betrag
                d_betrag = d_betrag - s_list.betrag
                m_betrag = m_betrag - s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed = s_list.betrag
                fb_flash.mtd_consumed = s_list.t_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.flag = 1
            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed = betrag
            fb_flash.mtd_consumed = t_betrag1


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "DEPARTMENT EXPENSES"
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 5)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d1_betrag = d1_betrag + s_list.betrag
                m1_betrag = m1_betrag + s_list.t_betrag
                d_betrag = d_betrag - s_list.betrag
                m_betrag = m_betrag - s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed = betrag
                fb_flash.mtd_consumed = t_betrag

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d1_betrag = d1_betrag + s_list.betrag
            m1_betrag = m1_betrag + s_list.t_betrag
            d_betrag = d_betrag - s_list.betrag
            m_betrag = m_betrag - s_list.t_betrag
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = s_list.bezeich
            fb_flash.t_consumed = s_list.betrag
            fb_flash.mtd_consumed = s_list.t_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.flag = 1
            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed = betrag
            fb_flash.mtd_consumed = t_betrag1


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "TOTAL EXPENSES"
            fb_flash.t_consumed = d1_betrag
            fb_flash.mtd_consumed = m1_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "NET CONSUMPTION cost"
            fb_flash.t_consumed = d_betrag
            fb_flash.mtd_consumed = m_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = "Nett food Sales"
            fb_flash.t_consumed = f_sales
            fb_flash.mtd_consumed = tf_sales


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.flag = 99
            fb_flash.c_alloc = "R a t i o  cost:Sales (%)"

            if f_sales != 0:
                fb_flash.t_consumed = (d_betrag / f_sales * 100)
            else:
                fb_flash.t_consumed = 0

            if tf_sales != 0:
                fb_flash.mtd_consumed = (m_betrag / tf_sales) * 100
            else:
                fb_flash.mtd_consumed = 0
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

        done = True

    def create_bev():

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        betrag:decimal = 0
        t_betrag1:decimal = 0
        t_betrag2:decimal = 0
        d_betrag:decimal = 0
        m_betrag:decimal = 0
        d1_betrag:decimal = 0
        m1_betrag:decimal = 0
        flag:int = 0
        f_eknr:int = 0
        b_eknr:int = 0
        fl_eknr:int = 0
        bl_eknr:int = 0
        h_service:decimal = 0
        h_mwst:decimal = 0
        amount:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 862)).first()
        f_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 892)).first()
        b_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 257)).first()
        fl_eknr = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 258)).first()
        bl_eknr = finteger
        fb_flash = Fb_flash()
        fb_flash_list.append(fb_flash)

        fb_flash = Fb_flash()
        fb_flash_list.append(fb_flash)

        fb_flash.c_alloc = "** BEVERAGE **"
        fb_flash = Fb_flash()
        fb_flash_list.append(fb_flash)


        for l_store in db_session.query(L_store).filter(
                (L_store.lager_nr != main_storage) &  (L_store.lager_nr >= f_store) &  (L_store.lager_nr <= t_store) &  (L_store.betriebsnr > 0)).all():
            s_list_list.clear()
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

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
            food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr, l_store.lager_nr)
            d_betrag = 0
            m_betrag = 0
            d1_betrag = 0
            m1_betrag = 0
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 1)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d_betrag = d_betrag + s_list.betrag
                m_betrag = m_betrag + s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed = s_list.betrag
                fb_flash.mtd_consumed = s_list.t_betrag


            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 2)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d_betrag = d_betrag + s_list.betrag
                m_betrag = m_betrag + s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.bezeich = s_list.bezeich
                fb_flash.t_consumed = s_list.betrag
                fb_flash.mtd_consumed = s_list.t_betrag

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
            d_betrag = d_betrag + s_list.betrag
            m_betrag = m_betrag + s_list.t_betrag
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = s_list.bezeich
            fb_flash.t_consumed = s_list.betrag
            fb_flash.mtd_consumed = s_list.t_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "GROSS CONSUMPTION cost"
            fb_flash.t_consumed = d_betrag
            fb_flash.mtd_consumed = m_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "LESS BY:"


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "COMPLIMENT cost"


            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 4)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d1_betrag = d1_betrag + s_list.betrag
                m1_betrag = m1_betrag + s_list.t_betrag
                d_betrag = d_betrag - s_list.betrag
                m_betrag = m_betrag - s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed = s_list.betrag
                fb_flash.mtd_consumed = s_list.t_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed = betrag
            fb_flash.mtd_consumed = t_betrag1


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "DEPARTMENT EXPENSES"
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 5)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d1_betrag = d1_betrag + s_list.betrag
                m1_betrag = m1_betrag + s_list.t_betrag
                d_betrag = d_betrag - s_list.betrag
                m_betrag = m_betrag - s_list.t_betrag
                fb_flash = Fb_flash()
                fb_flash_list.append(fb_flash)

                fb_flash.c_alloc = s_list.bezeich
                fb_flash.t_consumed = s_list.betrag
                fb_flash.mtd_consumed = s_list.t_betrag

            s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d1_betrag = d1_betrag + s_list.betrag
            m1_betrag = m1_betrag + s_list.t_betrag
            d_betrag = d_betrag - s_list.betrag
            m_betrag = m_betrag - s_list.t_betrag
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = s_list.bezeich
            fb_flash.t_consumed = s_list.betrag
            fb_flash.mtd_consumed = s_list.t_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.flag = 1
            fb_flash.c_alloc = "SUB TOTAL"
            fb_flash.t_consumed = betrag
            fb_flash.mtd_consumed = t_betrag1


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "TOTAL EXPENSES"
            fb_flash.t_consumed = d1_betrag
            fb_flash.mtd_consumed = m1_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.bezeich = "NET CONSUMPTION cost"
            fb_flash.t_consumed = d_betrag
            fb_flash.mtd_consumed = m_betrag


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.c_alloc = "Nett Beverage Sales"
            fb_flash.t_consumed = b_sales
            fb_flash.mtd_consumed = tb_sales


            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

            fb_flash.flag = 99
            fb_flash.c_alloc = "R a t i o  cost:Sales (%)"

            if b_sales != 0:
                fb_flash.t_consumed = d_betrag / b_sales * 100

            if tb_sales != 0:
                fb_flash.mtd_consumed = (m_betrag / tb_sales) * 100
            fb_flash = Fb_flash()
            fb_flash_list.append(fb_flash)

        done = True

    def step_food1(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 1

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_store)).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 1
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("TRANSFER TO SIDE STORE", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (L_op.loeschflag <= 1) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1) &  ((L_op.lager_nr == curr_store) |  (L_op.pos == curr_store)) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.lager_nr == curr_store:
                s_list.t_betrag = s_list.t_betrag - l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag - l_op.warenwert

            if l_op.pos == curr_store:
                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def step_food1a():

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        curr_dept:int = 0
        flag:int = 1

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_store)).first()
        curr_dept = l_lager.betriebsnr
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 2
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER IN", lvcarea, "")
        s_list.flag = flag
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 3
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER OUT", lvcarea, "")
        s_list.flag = flag

        for h_compli in db_session.query(H_compli).filter(
                (H_compli.datum >= date1) &  (H_compli.datum <= date2) &  (H_compli.betriebsnr > 0) &  (H_compli.p_artnr == 1)).all():

            hoteldpt = db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num == h_compli.betriebsnr)).first()

            if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nr == 2), first=True)
                s_list.t_betrag = s_list.t_betrag + h_compli.epreis

                if h_compli.datum == date2:
                    s_list.betrag = s_list.betrag + h_compli.epreis
            else:

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == h_compli.departement)).first()

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.nr == 3), first=True)
                    s_list.t_betrag = s_list.t_betrag - h_compli.epreis

                    if h_compli.datum == date2:
                        s_list.betrag = s_list.betrag - h_compli.epreis

    def step_bev1(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 2

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_store)).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 1
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("TRANSFER TO SIDE STORE", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (L_op.loeschflag <= 1) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1) &  ((L_op.lager_nr == curr_store) |  (L_op.pos == curr_store)) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.lager_nr == curr_store:
                s_list.t_betrag = s_list.t_betrag - l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag - l_op.warenwert

            if l_op.pos == curr_store:
                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def step_bev1a():

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        curr_dept:int = 0
        flag:int = 2

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_store)).first()
        curr_dept = l_lager.betriebsnr
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 2
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER IN", lvcarea, "")
        s_list.flag = flag
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.nr = 3
        s_list.reihenfolge = 1
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("KITCHEN TRANSFER OUT", lvcarea, "")
        s_list.flag = flag

        for h_compli in db_session.query(H_compli).filter(
                (H_compli.datum >= date1) &  (H_compli.datum <= date2) &  (H_compli.betriebsnr > 0) &  (H_compli.p_artnr == 2)).all():

            hoteldpt = db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num == h_compli.betriebsnr)).first()

            if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nr == 2), first=True)
                s_list.t_betrag = s_list.t_betrag + h_compli.epreis

                if h_compli.datum == date2:
                    s_list.betrag = s_list.betrag + h_compli.epreis
            else:

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == h_compli.departement)).first()

                if hoteldpt and hoteldpt.betriebsnr == l_lager.lager_nr:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.nr == 3), first=True)
                    s_list.t_betrag = s_list.t_betrag - h_compli.epreis

                    if h_compli.datum == date2:
                        s_list.betrag = s_list.betrag - h_compli.epreis

    def step_food2(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 1

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_store)).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("DIRECT PURCHASED", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  (L_op.lager_nr == curr_store)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            s_list.t_betrag = s_list.t_betrag + l_op.warenwert

            if l_op.datum == date2:
                s_list.betrag = s_list.betrag + l_op.warenwert

    def step_bev2(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 2

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_store)).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 2
        s_list.lager_nr = l_lager.lager_nr
        s_list.bezeich = translateExtended ("DIRECT PURCHASED", lvcarea, "")
        s_list.flag = flag

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  (L_op.lager_nr == curr_store)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            s_list.t_betrag = s_list.t_betrag + l_op.warenwert

            if l_op.datum == date2:
                s_list.betrag = s_list.betrag + l_op.warenwert

    def beverage_to_food():

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 272)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fchar)).first()
        bev_food = fchar
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 3
        s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                gl_acct.bezeich.upper()
        s_list.flag = 1

    def food_to_beverage():

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 275)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fchar)).first()
        food_bev = fchar
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 3
        s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                gl_acct.bezeich.upper()
        s_list.flag = 2

    def step_two(f_endkum:int, b_endkum:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 0
        cost_account:str = ""
        cost_value:decimal = 0
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        com_artnr:int = 0
        com_bezeich:str = ""
        com_fibu:str = ""
        H_art = H_artikel
        Gl_acc1 = Gl_acct

        if dstore == 0:

            return

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num > 0) &  ((Hoteldpt.num == l_store.betriebsnr) |  (Hoteldpt.betriebsnr == l_store.lager_nr))).all():

            h_compli_obj_list = []
            for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                    (H_compli.datum >= date1) &  (H_compli.datum <= date2) &  (H_compli.departement == hoteldpt.num) &  (H_compli.betriebsnr == 0)).all():
                if h_compli._recid in h_compli_obj_list:
                    continue
                else:
                    h_compli_obj_list.append(h_compli._recid)

                if double_currency and curr_datum != h_compli.datum:
                    curr_datum = h_compli.datum

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_datum)).first()
                    else:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.datum == curr_datum)).first()

                    if exrate:
                        rate = exrate.betrag
                    else:
                        rate = exchg_rate

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == 0)).first()

                gl_acct = db_session.query(Gl_acct).filter(
                        (Gl_acct.fibukonto == artikel.fibukonto)).first()
                com_artnr = artikel.artnr
                com_bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                        gl_acct.bezeich.upper()
                com_fibu = gl_acct.fibukonto

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_compli.artnr) &  (H_artikel.departement == h_compli.departement)).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                flag = 0

                if artikel.endkum == f_endkum:
                    flag = 1

                elif artikel.endkum == b_endkum:
                    flag = 2

                s_list = query(s_list_list, filters=(lambda s_list :s_list.fibukonto.lower()  == (com_fibu).lower()  and s_list.reihenfolge == 4 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 4
                    s_list.lager_nr = com_artnr
                    s_list.fibukonto = com_fibu
                    s_list.bezeich = com_bezeich
                    s_list.flag = flag
                cost = 0

                h_cost = db_session.query(H_cost).filter(
                        (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                if h_cost and h_cost.betrag != 0:
                    cost = h_compli.anzahl * h_cost.betrag

                elif not h_cost or (h_cost and h_cost.betrag == 0):
                    cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate
                s_list.t_betrag = s_list.t_betrag + cost

                if h_compli.datum == date2:
                    s_list.betrag = s_list.betrag + cost

    def step_three_food(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 1
        fibukonto:str = ""
        bezeich:str = ""
        Gl_acct1 = Gl_acct

        l_op_obj_list = []
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto) &  ((Gl_acct.acc_type == 5) |  (Gl_acct.acc_type == 3) |  (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.lager_nr == curr_store) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto
                    bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                        gl_acct1.bezeich.upper()

            if fibukonto.lower()  == (food_bev).lower() :
                pass

            elif fibukonto.lower()  == (bev_food).lower() :
                pass
            else:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and s_list.reihenfolge == 5 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 5
                    s_list.fibukonto = fibukonto
                    s_list.bezeich = bezeich
                    s_list.flag = flag
                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def step_three_bev(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        flag:int = 2
        fibukonto:str = ""
        bezeich:str = ""
        Gl_acct1 = Gl_acct

        l_op_obj_list = []
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto) &  ((Gl_acct.acc_type == 5) |  (Gl_acct.acc_type == 3) |  (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.lager_nr == curr_store) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()

                if gl_acct1:
                    fibukonto = gl_acct1.fibukonto
                    bezeich = to_string(gl_acct1.fibukonto, coa_format) + " " +\
                        gl_acct1.bezeich.upper()

            if fibukonto.lower()  == (food_bev).lower() :
                pass

            elif fibukonto.lower()  == (bev_food).lower() :
                pass
            else:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.(fibukonto).lower().lower()  == (fibukonto).lower()  and s_list.reihenfolge == 5 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 5
                    s_list.fibukonto = fibukonto
                    s_list.bezeich = bezeich
                    s_list.flag = flag
                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def food_bev(fl_eknr:int, bl_eknr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                (L_op.op_art == 3) &  (L_op.loeschflag <= 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  ((func.lower(L_op.stornogrund) == (bev_food).lower()) |  (func.lower(L_op.stornogrund) == food_bev)) &  (L_op.lager_nr == curr_store)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.stornogrund.lower()  == (food_bev).lower() :

                s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 3 and s_list.flag == 2), first=True)
                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

            elif l_op.stornogrund.lower()  == (bev_food).lower() :

                s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 3 and s_list.flag == 1), first=True)
                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def step_four(f_eknr:int, b_eknr:int, store_nr:int):

        nonlocal fb_flash_list, lvcarea, done, dstore, curr_store, long_digit, f_sales, b_sales, tf_sales, tb_sales, bev_food, food_bev, coa_format, htparam, l_lager, l_artikel, l_op, h_compli, hoteldpt, gl_acct, h_artikel, exrate, artikel, h_cost, l_ophdr, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal s_list, fb_flash, l_store, h_art, gl_acc1, gl_acct1
        nonlocal s_list_list, fb_flash_list

        h_service:decimal = 0
        h_mwst:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        amount:decimal = 0
        serv_taxable:bool = False
        f_sales = 0
        b_sales = 0
        tf_sales = 0
        tb_sales = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_taxable = htparam.flogical

        if dstore == 0:

            return

        for hoteldpt in db_session.query(Hoteldpt).filter(
                ((Hoteldpt.num == dstore) |  (Hoteldpt.betriebsnr == store_nr))).all():

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.artart == 0) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == f_eknr) |  (Artikel.endkum == b_eknr) |  (Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5) |  (Artikel.umsatzart == 6))).all():

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.datum >= date1) &  (Umsatz.datum <= date2) &  (Umsatz.departement == artikel.departement) &  (Umsatz.artnr == artikel.artnr)).all():
                    h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                    h_mwst = h_mwst + vat2


                    amount = umsatz.betrag / fact

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales = f_sales + amount
                        tf_sales = tf_sales + amount

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales = b_sales + amount
                        tb_sales = tb_sales + amount


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 977)).first()
    coa_format = htparam.fchar

    if from_grp == food:
        create_food()
    else:
        create_bev()

    return generate_output()