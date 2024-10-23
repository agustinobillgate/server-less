from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Htparam, H_bill_line, H_artikel, Artikel, L_artikel, H_rezept, H_rezlin, L_lager, Hoteldpt, L_ophdr, L_op, L_bestand

def direct_autodeductbl(bill_date:date):
    inv_closedate:date = None
    food_closedate:date = None
    transdate:date = None
    deductflag:bool = True
    mm1:int = 0
    yy1:int = 0
    mm2:int = 0
    yy2:int = 0
    deduct_compli:bool = False
    to_date:date = None
    from_date:date = None
    main_grp1:int = 0
    main_grp2:int = 0
    main_grp3:int = 0
    htparam = h_bill_line = h_artikel = artikel = l_artikel = h_rezept = h_rezlin = l_lager = hoteldpt = l_ophdr = l_op = l_bestand = None

    s_list = t_list = sbuff = None

    s_list_list, S_list = create_model("S_list", {"dept":int, "store":int, "artnr":int, "price":decimal, "qty":decimal, "fibukonto":str}, {"fibukonto": "0000000000"})
    t_list_list, T_list = create_model("T_list", {"dept":int, "rechnr":int, "pay":decimal, "rmtrans":decimal, "compli":decimal, "coupon":decimal, "fibukonto":str}, {"fibukonto": "0000000000"})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list
        return {}

    def create_list():

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.bill_datum == bill_date)).order_by(H_bill_line.departement, H_bill_line.rechnr).all():

            t_list = query(t_list_list, filters=(lambda t_list: t_list.dept == h_bill_line.departement and t_list.rechnr == h_bill_line.rechnr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.dept = h_bill_line.departement
                t_list.rechnr = h_bill_line.rechnr

            if h_bill_line.artnr == 0:

                if re.match(r".*RmNo.*",h_bill_line.bezeich, re.IGNORECASE):
                    t_list.rmtrans =  to_decimal(t_list.rmtrans) + to_decimal(h_bill_line.betrag)
                else:
                    t_list.pay =  to_decimal(t_list.pay) + to_decimal(h_bill_line.betrag)
            else:

                h_artikel = db_session.query(H_artikel).filter(
                         (H_artikel.artnr == h_bill_line.artnr) & (H_artikel.departement == h_bill_line.departement)).first()

                if not h_artikel:
                    pass

                elif h_artikel:

                    if h_artikel.artart == 0:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel:
                            t_list.fibukonto = artikel.bezeich1


                    else:

                        if h_artikel.artart <= 7:
                            t_list.pay =  to_decimal(t_list.pay) - to_decimal(h_bill_line.betrag)

                        elif h_artikel.artart == 11:
                            t_list.compli =  to_decimal(t_list.compli) - to_decimal(h_bill_line.betrag)

                        elif h_artikel.artart == 12:
                            t_list.coupon =  to_decimal(t_list.coupon) - to_decimal(h_bill_line.betrag)


    def get_l_artikels():

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        do_it:bool = False

        for t_list in query(t_list_list, filters=(lambda t_list: t_list.pay >= 0 or t_list.rmTrans != 0 or t_list.compli != 0 or t_list.coupon != 0)):

            if t_list.compli != 0:
                do_it = deduct_compli
            else:
                do_it = True

            if t_list.coupon != 0:
                do_it = deduct_compli
            else:
                do_it = True

            if do_it:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.departement == t_list.dept) & (H_bill_line.rechnr == t_list.rechnr) & (H_bill_line.steuercode != 99999)).order_by(H_bill_line._recid).all():

                    if h_bill_line.artnr == 0:
                        pass
                    else:

                        h_artikel = db_session.query(H_artikel).filter(
                                 (H_artikel.artnr == h_bill_line.artnr) & (H_artikel.departement == h_bill_line.departement)).first()

                        if not h_artikel:
                            pass

                        elif h_artikel.artart == 0:

                            if h_artikel.artnrlager != 0:

                                l_artikel = db_session.query(L_artikel).filter(
                                         (L_artikel.artnr == h_artikel.artnrlager)).first()

                                if l_artikel:

                                    s_list = query(s_list_list, filters=(lambda s_list: s_list.dept == t_list.dept and s_list.artnr == l_artikel.artnr and s_list.fibukonto == t_list.fibukonto), first=True)

                                    if not s_list:
                                        s_list = S_list()
                                        s_list_list.append(s_list)

                                        s_list.dept = t_list.dept
                                        s_list.artnr = l_artikel.artnr
                                        s_list.price =  to_decimal(l_artikel.vk_preis)
                                        s_list.store = h_artikel.lagernr

                                        artikel = db_session.query(Artikel).filter(
                                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                                        if artikel:
                                            s_list.fibukonto = artikel.bezeich1


                                    s_list.qty =  to_decimal(s_list.qty) + to_decimal(h_bill_line.anzahl)

                            elif h_artikel.artnrrezept != 0:

                                h_rezept = db_session.query(H_rezept).filter(
                                         (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                                if h_rezept:
                                    get_recipe(h_rezept.artnrrezept, 1)

    def get_recipe(p_artnr:int, menge:decimal):

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe2(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.dept == t_list.dept and s_list.artnr == l_artikel.artnr and s_list.fibukonto == t_list.fibukonto), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.dept = t_list.dept
                        s_list.artnr = l_artikel.artnr
                        s_list.price =  to_decimal(l_artikel.vk_preis)

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel:
                            s_list.fibukonto = artikel.bezeich1

                        if h_artikel.lagernr != 0:

                            l_lager = db_session.query(L_lager).filter(
                                     (L_lager.lager_nr == h_artikel.lagernr)).first()

                            if l_lager:
                                store_found = True
                                s_list.store = h_artikel.lagernr

                        if not store_found:

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == s_list.dept)).first()
                            s_list.store = hoteldpt.betriebsnr


                    inh =  to_decimal(inh) / to_decimal(l_art.inhalt)
                    s_list.qty =  to_decimal(s_list.qty) + to_decimal(h_bill_line.anzahl) * to_decimal(inh)


    def get_recipe2(p_artnr:int, menge:decimal):

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe3(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.dept == t_list.dept and s_list.artnr == l_artikel.artnr and s_list.fibukonto == t_list.fibukonto), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.dept = t_list.dept
                        s_list.artnr = l_artikel.artnr
                        s_list.price =  to_decimal(l_artikel.vk_preis)

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel:
                            s_list.fibukonto = artikel.bezeich1

                        if h_artikel.lagernr != 0:

                            l_lager = db_session.query(L_lager).filter(
                                     (L_lager.lager_nr == h_artikel.lagernr)).first()

                            if l_lager:
                                store_found = True
                                s_list.store = h_artikel.lagernr

                        if not store_found:

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == s_list.dept)).first()
                            s_list.store = hoteldpt.betriebsnr


                    inh =  to_decimal(inh) / to_decimal(l_art.inhalt)
                    s_list.qty =  to_decimal(s_list.qty) + to_decimal(h_bill_line.anzahl) * to_decimal(inh)


    def get_recipe3(p_artnr:int, menge:decimal):

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe4(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.dept == t_list.dept and s_list.artnr == l_artikel.artnr and s_list.fibukonto == t_list.fibukonto), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.dept = t_list.dept
                        s_list.artnr = l_artikel.artnr
                        s_list.price =  to_decimal(l_artikel.vk_preis)

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel:
                            s_list.fibukonto = artikel.bezeich1

                        if h_artikel.lagernr != 0:

                            l_lager = db_session.query(L_lager).filter(
                                     (L_lager.lager_nr == h_artikel.lagernr)).first()

                            if l_lager:
                                store_found = True
                                s_list.store = h_artikel.lagernr

                        if not store_found:

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == s_list.dept)).first()
                            s_list.store = hoteldpt.betriebsnr


                    inh =  to_decimal(inh) / to_decimal(l_art.inhalt)
                    s_list.qty =  to_decimal(s_list.qty) + to_decimal(h_bill_line.anzahl) * to_decimal(inh)


    def get_recipe4(p_artnr:int, menge:decimal):

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe5(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.dept == t_list.dept and s_list.artnr == l_artikel.artnr and s_list.fibukonto == t_list.fibukonto), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.dept = t_list.dept
                        s_list.artnr = l_artikel.artnr
                        s_list.price =  to_decimal(l_artikel.vk_preis)

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel:
                            s_list.fibukonto = artikel.bezeich1

                        if h_artikel.lagernr != 0:

                            l_lager = db_session.query(L_lager).filter(
                                     (L_lager.lager_nr == h_artikel.lagernr)).first()

                            if l_lager:
                                store_found = True
                                s_list.store = h_artikel.lagernr

                        if not store_found:

                            hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == s_list.dept)).first()
                            s_list.store = hoteldpt.betriebsnr


                    inh =  to_decimal(inh) / to_decimal(l_art.inhalt)
                    s_list.qty =  to_decimal(s_list.qty) + to_decimal(h_bill_line.anzahl) * to_decimal(inh)


    def get_recipe5(p_artnr:int, menge:decimal):

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

            if l_artikel:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.dept == t_list.dept and s_list.artnr == l_artikel.artnr and s_list.fibukonto == t_list.fibukonto), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.dept = t_list.dept
                    s_list.artnr = l_artikel.artnr
                    s_list.price =  to_decimal(l_artikel.vk_preis)

                    artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                    if artikel:
                        s_list.fibukonto = artikel.bezeich1

                    if h_artikel.lagernr != 0:

                        l_lager = db_session.query(L_lager).filter(
                                     (L_lager.lager_nr == h_artikel.lagernr)).first()

                        if l_lager:
                            store_found = True
                            s_list.store = h_artikel.lagernr

                    if not store_found:

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                     (Hoteldpt.num == s_list.dept)).first()
                        s_list.store = hoteldpt.betriebsnr


                inh =  to_decimal(inh) / to_decimal(l_art.inhalt)
                s_list.qty =  to_decimal(s_list.qty) + to_decimal(h_bill_line.anzahl) * to_decimal(inh)


    def create_outgoing():

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        curr_dept:int = -1
        lscheinnr:str = ""
        curr_lager:int = 0
        curr_onhand:decimal = to_decimal("0.0")
        Sbuff = S_list
        sbuff_list = s_list_list

        s_list = query(s_list_list, filters=(lambda s_list: s_list.store == 0), first=True)
        while None != s_list:

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == s_list.dept)).first()
            curr_lager = hoteldpt.betriebsnr

            if curr_lager == 0:
                pass
            else:
                s_list.store = curr_lager

            s_list = query(s_list_list, filters=(lambda s_list: s_list.store == 0), next=True)

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.store == 0 or s_list.qty == 0)):
            s_list_list.remove(s_list)

        if mm1 == mm2:

            for s_list in query(s_list_list, sort_by=[("store",False)]):

                l_ophdr = db_session.query(L_ophdr).filter(
                         (func.lower(L_ophdr.op_typ) == ("STT").lower()) & (substring(L_ophdr.lscheinnr, 0, 3) == ("INV").lower()) & (L_ophdr.datum >= bill_date) & (L_ophdr.lager_nr == s_list.store)).first()

                if l_ophdr:

                    for sbuff in query(sbuff_list, filters=(lambda sbuff: sbuff.store == s_list.store)):
                        sbuff_list.remove(sbuff)

        for s_list in query(s_list_list, sort_by=[("dept",False)]):

            if curr_dept != s_list.dept:
                lscheinnr = "SAD" + substring(to_string(get_year(transdate)) , 2, 2) + to_string(get_month(transdate) , "99") + to_string(get_day(transdate) , "99") + "-" + to_string(s_list.dept, "99")
                l_ophdr = L_ophdr()
                db_session.add(l_ophdr)

                l_ophdr.datum = transdate
                l_ophdr.lager_nr = s_list.store
                l_ophdr.docu_nr = lscheinnr
                l_ophdr.lscheinnr = lscheinnr
                l_ophdr.op_typ = "STT"
                l_ophdr.fibukonto = s_list.fibukonto
                curr_dept = s_list.dept


            l_op = L_op()
            db_session.add(l_op)

            l_op.datum = transdate
            l_op.lager_nr = s_list.store
            l_op.artnr = s_list.artnr
            l_op.zeit = get_current_time_in_seconds()
            l_op.anzahl =  to_decimal(s_list.qty)
            l_op.einzelpreis =  to_decimal(s_list.price)
            l_op.warenwert =  to_decimal(s_list.qty) * to_decimal(s_list.price)
            l_op.op_art = 3
            l_op.herkunftflag = 4
            l_op.lscheinnr = lscheinnr
            l_op.pos = 1
            l_op.fuellflag = 0

            if to_decimal(s_list.fibukonto) != 0:
                l_op.stornogrund = s_list.fibukonto

        if deductflag:
            init_onhand()

            for l_op in db_session.query(L_op).filter(
                     ((L_op.op_art == 1) | (L_op.op_art == 2)) & (L_op.loeschflag < 2) & ((L_op.datum >= from_date) & (L_op.datum <= to_date)) & (L_op.pos >= 1) & (L_op.lager_nr > 0)).order_by(L_op.artnr).all():

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == l_op.artnr)).first()

                if l_artikel:
                    update_eingang()

            for l_op in db_session.query(L_op).filter(
                     ((L_op.op_art == 3) | (L_op.op_art == 4)) & (L_op.loeschflag < 2) & ((L_op.datum >= from_date) & (L_op.datum <= to_date)) & (L_op.pos >= 1) & (L_op.lager_nr > 0)).order_by(L_op.artnr).all():

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == l_op.artnr)).first()

                if l_artikel:
                    update_ausgang()


    def init_onhand():

        nonlocal inv_closedate, food_closedate, transdate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        l_oh = None
        buf_lart = None
        L_oh =  create_buffer("L_oh",L_bestand)
        Buf_lart =  create_buffer("Buf_lart",L_artikel)

        l_oh = db_session.query(L_oh).filter(
                 (L_oh.lager_nr == 0)).first()
        while None != l_oh:

            buf_lart = db_session.query(Buf_lart).filter(
                         (Buf_lart.artnr == l_oh.artnr)).first()

            if buf_lart:

                l_bestand = db_session.query(L_bestand).filter(
                             (L_bestand._recid == l_oh._recid)).first()
                l_bestand.anz_eingang =  to_decimal("0")
                l_bestand.wert_eingang =  to_decimal("0")
                l_bestand.anz_ausgang =  to_decimal("0")
                l_bestand.wert_ausgang =  to_decimal("0")


            curr_recid = l_oh._recid
            l_oh = db_session.query(L_oh).filter(
                     (L_oh.lager_nr == 0)).filter(L_oh._recid > curr_recid).first()

        l_lager = db_session.query(L_lager).first()
        while None != l_lager:

            l_oh = db_session.query(L_oh).filter(
                     (L_oh.lager_nr == l_lager.lager_nr)).first()
            while None != l_oh:

                buf_lart = db_session.query(Buf_lart).filter(
                             (Buf_lart.artnr == l_oh.artnr)).first()

                if buf_lart:

                    l_bestand = db_session.query(L_bestand).filter(
                                 (L_bestand._recid == l_oh._recid)).first()
                    l_bestand.anz_eingang =  to_decimal("0")
                    l_bestand.wert_eingang =  to_decimal("0")
                    l_bestand.anz_ausgang =  to_decimal("0")
                    l_bestand.wert_ausgang =  to_decimal("0")

                curr_recid = l_oh._recid
                l_oh = db_session.query(L_oh).filter(
                             (L_oh.lager_nr == l_lager.lager_nr)).filter(L_oh._recid > curr_recid).first()


            curr_recid = l_lager._recid
            l_lager = db_session.query(L_lager).filter(L_lager._recid > curr_recid).first()


    def update_eingang():

        nonlocal inv_closedate, food_closedate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        s_artnr:int = 0
        anzahl:decimal = to_decimal("0.0")
        wert:decimal = to_decimal("0.0")
        transdate:date = None
        curr_lager:int = 0
        tot_anz:decimal = to_decimal("0.0")
        tot_wert:decimal = to_decimal("0.0")
        avrg_price:decimal = to_decimal("0.0")
        s_artnr = l_op.artnr
        anzahl =  to_decimal(l_op.anzahl)
        wert =  to_decimal(l_op.warenwert)
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        if l_op.op_art == 1 or (l_op.op_art == 2 and l_op.herkunftflag == 3):

            l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = transdate


            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)

        l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate


        l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) + to_decimal(anzahl)
        l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(wert)

    def update_ausgang():

        nonlocal inv_closedate, food_closedate, deductflag, mm1, yy1, mm2, yy2, deduct_compli, to_date, from_date, main_grp1, main_grp2, main_grp3, htparam, h_bill_line, h_artikel, artikel, l_artikel, h_rezept, h_rezlin, l_lager, hoteldpt, l_ophdr, l_op, l_bestand
        nonlocal bill_date


        nonlocal s_list, t_list, sbuff
        nonlocal s_list_list, t_list_list

        s_artnr:int = 0
        anzahl:decimal = to_decimal("0.0")
        wert:decimal = to_decimal("0.0")
        transdate:date = None
        curr_lager:int = 0
        s_artnr = l_op.artnr
        anzahl =  to_decimal(l_op.anzahl)
        wert =  to_decimal(l_op.warenwert)
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        if l_op.op_art == 3 or (l_op.op_art == 4 and l_op.herkunftflag == 3):

            l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.lager_nr == 0) & (L_bestand.artnr == s_artnr)).first()

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = transdate


            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

        l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == curr_lager) & (L_bestand.artnr == s_artnr)).first()

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate


        l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
        l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)

    inv_closedate = get_output(htpdate(224))
    food_closedate = get_output(htpdate(221))
    deduct_compli = get_output(htplogic(947))

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 257)).first()
    main_grp1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 258)).first()
    main_grp2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 268)).first()
    main_grp3 = htparam.finteger

    if main_grp1 == 1 or main_grp2 == 2:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 224)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 221)).first()
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    transdate = bill_date
    mm1 = get_month(bill_date)
    yy1 = get_year(bill_date)
    mm2 = get_month(inv_closedate)
    yy2 = get_year(inv_closedate)

    if (mm1 < mm2) or (yy1 < yy2):
        transdate = date_mdy(mm2, 1, yy2)

    if (mm1 > mm2) or (yy1 > yy2):
        deductflag = False


    create_list()
    get_l_artikels()
    create_outgoing()

    return generate_output()