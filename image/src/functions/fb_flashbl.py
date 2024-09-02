from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from models import Htparam, Waehrung, L_lager, L_artikel, L_bestand, L_op, Gl_acct, H_artikel, H_compli, Exrate, Artikel, H_cost, L_ophdr, Hoteldpt, Umsatz

def fb_flashbl(pvilanguage:int, from_grp:int, food:int, bev:int, date1:date, date2:date, incl_initoh:bool, incl_streq:bool):
    fbflash_list_list = []
    done = False
    beg_oh:decimal = 0
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
    main_storage:int = 1
    bev_food:str = ""
    food_bev:str = ""
    ldry:int = 0
    dstore:int = 0
    foreign_nr:int = 0
    exchg_rate:decimal = 1
    double_currency:bool = False
    f_sales:decimal = 0
    b_sales:decimal = 0
    tf_sales:decimal = 0
    tb_sales:decimal = 0
    anf_store:int = 1
    long_digit:bool = False
    coa_format:str = ""
    lvcarea:str = "fb_flash"
    htparam = waehrung = l_lager = l_artikel = l_bestand = l_op = gl_acct = h_artikel = h_compli = exrate = artikel = h_cost = l_ophdr = hoteldpt = umsatz = None

    fbflash_list = s_list = l_store = h_art = gl_acc1 = gl_acct1 = None

    fbflash_list_list, Fbflash_list = create_model("Fbflash_list", {"flag":int, "trans_to_storage":str, "cost_alloc":str, "day_cons":str, "mtd_cons":str})
    s_list_list, S_list = create_model("S_list", {"reihenfolge":int, "lager_nr":int, "fibukonto":str, "bezeich":str, "flag":int, "betrag":decimal, "t_betrag":decimal, "betrag1":decimal, "t_betrag1":decimal}, {"reihenfolge": 1, "flag": 2})

    L_store = L_lager
    H_art = H_artikel
    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list
        return {"fbflash-list": fbflash_list_list, "done": done}

    def step_food1(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 1
        L_store = L_lager

        l_op_obj_list = []
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (L_op.op_art == 4) &  (L_op.loeschflag <= 1) &  (L_op.herkunftflag == 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.lager_nr != main_storage:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag = s_list.t_betrag - l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag - l_op.warenwert

            if l_op.pos != main_storage:

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.pos and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_store.lager_nr
                    s_list.bezeich = l_store.bezeich
                    s_list.flag = flag


                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def step_bev1(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 2
        L_store = L_lager

        l_op_obj_list = []
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (L_op.op_art == 4) &  (L_op.loeschflag <= 1) &  (L_op.herkunftflag == 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.lager_nr != main_storage:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag = s_list.t_betrag - l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag - l_op.warenwert

            if l_op.pos != main_storage:

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.pos and s_list.reihenfolge == 1 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 1
                    s_list.lager_nr = l_store.lager_nr
                    s_list.bezeich = l_store.bezeich
                    s_list.flag = flag


                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

    def step_food2(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 1

        l_op_obj_list = []
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (L_op.op_art == 1) &  (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.lager_nr != main_storage) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 2 and s_list.flag == flag), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.reihenfolge = 2
                s_list.lager_nr = l_lager.lager_nr
                s_list.bezeich = l_lager.bezeich
                s_list.flag = flag


            s_list.t_betrag = s_list.t_betrag + l_op.warenwert

            if l_op.datum == date2:
                s_list.betrag = s_list.betrag + l_op.warenwert

    def step_bev2(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 2

        l_op_obj_list = []
        for l_op, l_lager, l_artikel in db_session.query(L_op, L_lager, L_artikel).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (L_op.op_art == 1) &  (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.lager_nr != main_storage) &  (L_op.datum >= date1) &  (L_op.datum <= date2)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 2 and s_list.flag == flag), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.reihenfolge = 2
                s_list.lager_nr = l_lager.lager_nr
                s_list.bezeich = l_lager.bezeich
                s_list.flag = flag


            s_list.t_betrag = s_list.t_betrag + l_op.warenwert

            if l_op.datum == date2:
                s_list.betrag = s_list.betrag + l_op.warenwert

    def beverage_to_food():

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 272)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fchar)).first()
        bev_food = htparam.fchar
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 3
        s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                gl_acct.bezeich.upper()
        s_list.flag = 1

    def food_to_beverage():

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 275)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fchar)).first()
        food_bev = htparam.fchar
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihenfolge = 3
        s_list.bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                gl_acct.bezeich.upper()
        s_list.flag = 2

    def step_two(f_endkum:int, b_endkum:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

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

        h_compli_obj_list = []
        for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                (H_compli.datum >= date1) &  (H_compli.datum <= date2) &  (H_compli.departement != ldry) &  (H_compli.departement != dstore) &  (H_compli.betriebsnr == 0)).all():
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

            if artikel.endkum == f_endkum or artikel.umsatzart == 3 or artikel.umsatzart == 5:
                flag = 1

            elif artikel.endkum == b_endkum or artikel.umsatzart == 6:
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

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 1
        fibukonto:str = ""
        bezeich:str = ""
        type_of_acct:int = 0
        Gl_acct1 = Gl_acct

        l_op_obj_list = []
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto) &  ((Gl_acct.acc_type == 5) |  (Gl_acct.acc_type == 3) |  (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  (L_op.lager_nr != main_storage)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            type_of_acct = gl_acct.acc_type

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()

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

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 2
        fibukonto:str = ""
        bezeich:str = ""
        type_of_acct:int = 0
        Gl_acct1 = Gl_acct

        l_op_obj_list = []
        for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.fibukonto != "")).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto) &  ((Gl_acct.acc_type == 5) |  (Gl_acct.acc_type == 3) |  (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (L_op.pos > 0) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  (L_op.lager_nr != main_storage)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            fibukonto = gl_acct.fibukonto
            bezeich = to_string(gl_acct.fibukonto, coa_format) + " " +\
                    gl_acct.bezeich.upper()
            type_of_acct = gl_acct.acc_type

            if l_op.stornogrund != "":

                gl_acct1 = db_session.query(Gl_acct1).filter(
                        (Gl_acct1.fibukonto == l_op.stornogrund)).first()

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

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  ((L_artikel.endkum == fl_eknr) |  (L_artikel.endkum == bl_eknr))).filter(
                (L_op.op_art == 3) &  (L_op.loeschflag <= 1) &  (L_op.datum >= date1) &  (L_op.datum <= date2) &  ((func.lower(L_op.stornogrund) == (bev_food).lower()) |  (func.lower(L_op.stornogrund) == food_bev))).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            if l_op.stornogrund.lower()  == (food_bev).lower() :

                s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 3 and s_list.flag == 2), first=True)

                if l_op.lager_nr >= 1:
                    s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                    if l_op.datum == date2:
                        s_list.betrag = s_list.betrag + l_op.warenwert
                else:
                    s_list.t_betrag1 = s_list.t_betrag1 + l_op.warenwert

                    if l_op.datum == date2:
                        s_list.betrag1 = s_list.betrag1 + l_op.warenwert

            elif l_op.stornogrund.lower()  == (bev_food).lower() :

                s_list = query(s_list_list, filters=(lambda s_list :s_list.reihenfolge == 3 and s_list.flag == 1), first=True)

                if l_op.lager_nr >= 1:
                    s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                    if l_op.datum == date2:
                        s_list.betrag = s_list.betrag + l_op.warenwert
                else:
                    s_list.t_betrag1 = s_list.t_betrag1 + l_op.warenwert

                    if l_op.datum == date2:
                        s_list.betrag1 = s_list.betrag1 + l_op.warenwert

    def step_four(f_eknr:int, b_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, fl_eknr, bl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        h_service:decimal = 0
        h_mwst:decimal = 0
        amount:decimal = 0
        serv_taxable:bool = False
        f_sales = 0
        b_sales = 0
        tf_sales = 0
        tb_sales = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_taxable = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num != ldry) &  (Hoteldpt.num != dstore)).all():

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.artart == 0) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == f_eknr) |  (Artikel.endkum == b_eknr) |  (Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5) |  (Artikel.umsatzart == 6))).all():

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.datum >= date1) &  (Umsatz.datum <= date2) &  (Umsatz.departement == artikel.departement) &  (Umsatz.artnr == artikel.artnr)).all():
                    h_service = 0
                    h_mwst = 0
                    h_service, h_mwst = get_output(calc_servvat(artikel.departement, artikel.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    amount = umsatz.betrag / (1 + h_service + h_mwst)

                    if artikel.endkum == f_eknr or artikel.umsatzart == 3 or artikel.umsatzart == 5:

                        if umsatz.datum == date2:
                            f_sales = f_sales + amount
                        tf_sales = tf_sales + amount

                    elif artikel.endkum == b_eknr or artikel.umsatzart == 6:

                        if umsatz.datum == date2:
                            b_sales = b_sales + amount
                        tb_sales = tb_sales + amount

    def step_five(fl_eknr:int, bl_eknr:int):

        nonlocal fbflash_list_list, done, beg_oh, betrag, t_betrag1, t_betrag2, d_betrag, m_betrag, d1_betrag, m1_betrag, flag, f_eknr, b_eknr, fl_eknr, main_storage, bev_food, food_bev, ldry, dstore, foreign_nr, exchg_rate, double_currency, f_sales, b_sales, tf_sales, tb_sales, anf_store, long_digit, coa_format, lvcarea, htparam, waehrung, l_lager, l_artikel, l_bestand, l_op, gl_acct, h_artikel, h_compli, exrate, artikel, h_cost, l_ophdr, hoteldpt, umsatz
        nonlocal l_store, h_art, gl_acc1, gl_acct1


        nonlocal fbflash_list, s_list, l_store, h_art, gl_acc1, gl_acct1
        nonlocal fbflash_list_list, s_list_list

        flag:int = 0
        fibukonto:str = ""
        bezeich:str = ""
        type_of_acct:int = 0
        qty:decimal = 0
        qty1:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_qty1:decimal = 0
        t_val:decimal = 0
        Gl_acct1 = Gl_acct
        qty = 0
        val = 0
        qty1 = 0

        if from_grp == food:
            flag = 1

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "REQ") &  (L_ophdr.docu_nr == L_op.lscheinnr)).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto) &  ((Gl_acct.acc_type == 5) |  (Gl_acct.acc_type == 3) |  (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                    (L_op.datum >= date1) &  (L_op.datum <= date2) &  (L_op.op_art >= 13) &  (L_op.op_art <= 14) &  (L_op.herkunftflag <= 2) &  (L_op.loeschflag <= 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 6 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 6
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert

        elif from_grp == bev:
            flag = 2

            l_op_obj_list = []
            for l_op, l_ophdr, gl_acct, l_lager, l_artikel in db_session.query(L_op, L_ophdr, Gl_acct, L_lager, L_artikel).join(L_ophdr,(L_ophdr.lscheinnr == L_op.lscheinnr) &  (func.lower(L_ophdr.op_typ) == "REQ") &  (L_ophdr.docu_nr == L_op.lscheinnr)).join(Gl_acct,(Gl_acct.fibukonto == l_ophdr.fibukonto) &  ((Gl_acct.acc_type == 5) |  (Gl_acct.acc_type == 3) |  (Gl_acct.acc_type == 4))).join(L_lager,(L_lager.lager_nr == L_op.lager_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                    (L_op.datum >= date1) &  (L_op.datum <= date2) &  (L_op.op_art >= 13) &  (L_op.op_art <= 14) &  (L_op.herkunftflag <= 2) &  (L_op.loeschflag <= 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                s_list = query(s_list_list, filters=(lambda s_list :s_list.lager_nr == l_op.lager_nr and s_list.reihenfolge == 6 and s_list.flag == flag), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.reihenfolge = 6
                    s_list.lager_nr = l_lager.lager_nr
                    s_list.bezeich = l_lager.bezeich
                    s_list.flag = flag


                s_list.t_betrag = s_list.t_betrag + l_op.warenwert

                if l_op.datum == date2:
                    s_list.betrag = s_list.betrag + l_op.warenwert


    if incl_initoh:
        anf_store = 2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1081)).first()
    ldry = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1082)).first()
    dstore = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        double_currency = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit
        else:
            exchg_rate = 1

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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 977)).first()
    coa_format = htparam.fchar

    if incl_streq == False:

        if from_grp == food:
            step_food1(fl_eknr, bl_eknr)
            step_food2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_food(fl_eknr, bl_eknr)
            food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)

        elif from_grp == bev:
            step_bev1(fl_eknr, bl_eknr)
            step_bev2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_bev(fl_eknr, bl_eknr)
            food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)
    else:

        if from_grp == food:
            step_food1(fl_eknr, bl_eknr)
            step_food2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_food(fl_eknr, bl_eknr)
            food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)
            step_five(fl_eknr, bl_eknr)

        elif from_grp == bev:
            step_bev1(fl_eknr, bl_eknr)
            step_bev2(fl_eknr, bl_eknr)
            beverage_to_food()
            food_to_beverage()
            step_two(f_eknr, b_eknr)
            step_three_bev(fl_eknr, bl_eknr)
            food_bev(fl_eknr, bl_eknr)
            step_four(f_eknr, b_eknr)
            step_five(fl_eknr, bl_eknr)

    if from_grp == food or from_grp == 0:
        d_betrag = 0
        m_betrag = 0
        d1_betrag = 0
        m1_betrag = 0


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.cost_alloc = translateExtended ("** food **", lvcarea, "")


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        t_betrag1 = 0
        beg_oh = 0
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("OPENING INVENTORY", lvcarea, "")

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= anf_store)).all():
            betrag = 0

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == 1)).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                betrag = betrag + l_bestand.val_anf_best
                t_betrag1 = t_betrag1 + l_bestand.val_anf_best

                if l_lager.lager_nr > 1:
                    beg_oh = beg_oh + l_bestand.val_anf_best

                    if incl_initoh:
                        m_betrag = m_betrag + l_bestand.val_anf_best

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

        fbflash_list.trans_to_storage = translateExtended ("TRANSFER TO SIDE STORE", lvcarea, "")
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 1)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d_betrag = d_betrag + s_list.betrag
            m_betrag = m_betrag + s_list.t_betrag


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
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 2)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d_betrag = d_betrag + s_list.betrag
            m_betrag = m_betrag + s_list.t_betrag


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
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 6)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d_betrag = d_betrag + s_list.betrag
                m_betrag = m_betrag + s_list.t_betrag


                pass
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


        s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
        d_betrag = d_betrag + s_list.betrag + s_list.betrag1
        m_betrag = m_betrag + s_list.t_betrag + s_list.t_betrag1


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
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 4)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d1_betrag = d1_betrag + s_list.betrag
            m1_betrag = m1_betrag + s_list.t_betrag
            d_betrag = d_betrag - s_list.betrag
            m_betrag = m_betrag - s_list.t_betrag


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
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 5)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d1_betrag = d1_betrag + s_list.betrag
            m1_betrag = m1_betrag + s_list.t_betrag
            d_betrag = d_betrag - s_list.betrag
            m_betrag = m_betrag - s_list.t_betrag


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

        s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
        betrag = betrag + s_list.betrag
        t_betrag1 = t_betrag1 + s_list.t_betrag
        d1_betrag = d1_betrag + s_list.betrag
        m1_betrag = m1_betrag + s_list.t_betrag
        d_betrag = d_betrag - s_list.betrag
        m_betrag = m_betrag - s_list.t_betrag

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

        fbflash_list.cost_alloc = translateExtended ("R a t i o  cost:Sales (%)", lvcarea, "")

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
        d_betrag = 0
        m_betrag = 0
        d1_betrag = 0
        m1_betrag = 0


        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.cost_alloc = translateExtended ("** BEVERAGE **", lvcarea, "")
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        t_betrag1 = 0
        beg_oh = 0
        fbflash_list = Fbflash_list()
        fbflash_list_list.append(fbflash_list)

        fbflash_list.trans_to_storage = translateExtended ("OPENING INVENTORY", lvcarea, "")

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= anf_store)).all():
            betrag = 0

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == 2)).filter(
                    (L_bestand.lager_nr == l_lager.lager_nr)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                betrag = betrag + l_bestand.val_anf_best
                t_betrag1 = t_betrag1 + l_bestand.val_anf_best

                if l_lager.lager_nr > 1:
                    beg_oh = beg_oh + l_bestand.val_anf_best

                    if incl_initoh:
                        m_betrag = m_betrag + l_bestand.val_anf_best

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

        fbflash_list.trans_to_storage = translateExtended ("TRANSFER TO SIDE STORE", lvcarea, "")
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 1)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d_betrag = d_betrag + s_list.betrag
            m_betrag = m_betrag + s_list.t_betrag


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
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 2)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d_betrag = d_betrag + s_list.betrag
            m_betrag = m_betrag + s_list.t_betrag


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
            betrag = 0
            t_betrag1 = 0

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 6)):
                betrag = betrag + s_list.betrag
                t_betrag1 = t_betrag1 + s_list.t_betrag
                d_betrag = d_betrag + s_list.betrag
                m_betrag = m_betrag + s_list.t_betrag


                pass
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


        s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 3), first=True)
        d_betrag = d_betrag + s_list.betrag + s_list.betrag1
        m_betrag = m_betrag + s_list.t_betrag + s_list.t_betrag1


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
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 4)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d1_betrag = d1_betrag + s_list.betrag
            m1_betrag = m1_betrag + s_list.t_betrag
            d_betrag = d_betrag - s_list.betrag
            m_betrag = m_betrag - s_list.t_betrag


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
        betrag = 0
        t_betrag1 = 0

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.flag == 2 and s_list.reihenfolge == 5)):
            betrag = betrag + s_list.betrag
            t_betrag1 = t_betrag1 + s_list.t_betrag
            d1_betrag = d1_betrag + s_list.betrag
            m1_betrag = m1_betrag + s_list.t_betrag
            d_betrag = d_betrag - s_list.betrag
            m_betrag = m_betrag - s_list.t_betrag


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

        s_list = query(s_list_list, filters=(lambda s_list :s_list.flag == 1 and s_list.reihenfolge == 3), first=True)
        betrag = betrag + s_list.betrag + s_list.betrag1
        t_betrag1 = t_betrag1 + s_list.t_betrag + s_list.t_betrag1
        d1_betrag = d1_betrag + s_list.betrag + s_list.betrag1
        m1_betrag = m1_betrag + s_list.t_betrag + s_list.t_betrag1
        d_betrag = d_betrag - s_list.betrag - s_list.betrag1
        m_betrag = m_betrag - s_list.t_betrag - s_list.t_betrag1

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

        fbflash_list.cost_alloc = translateExtended ("R a t i o  cost:Sales (%)", lvcarea, "")

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