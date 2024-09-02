from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import H_artikel, Artikel, H_cost, L_artikel, H_rezept, H_rezlin, L_op, L_ophdr, Gl_acct

def hcost_anal_btn_gobl(sorttype:int, incl_bf:bool, incl_fb:bool, from_date:date, to_date:date, f_eknr:int, b_eknr:int, fl_eknr:int, bl_eknr:int, preis_typ:int, food_bev:str, bev_food:str):
    s_list_list = []
    h_artikel = artikel = h_cost = l_artikel = h_rezept = h_rezlin = l_op = l_ophdr = gl_acct = None

    s_list = h_recipe = None

    s_list_list, S_list = create_model("S_list", {"flag":int, "artnr":int, "bezeich":str, "munit":str, "qty1":decimal, "val1":decimal, "qty2":decimal, "val2":decimal, "d_qty":decimal, "d_val":decimal, "s_qty1":str, "s_qty2":str, "s_qty3":str})

    H_recipe = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list
        return {"s-list": s_list_list}

    def create_list1():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        datum:date = None
        t_val1:decimal = 0
        t_val2:decimal = 0
        s_list_list.clear()
        for datum in range(from_date,to_date + 1) :

            h_cost_obj_list = []
            for h_cost, h_artikel, artikel in db_session.query(H_cost, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_cost.artnr) &  (H_artikel.departement == H_cost.departement) &  ((H_artikel.artnrlager != 0) |  (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                    (H_cost.datum == datum) &  (H_cost.flag == 1)).all():
                if h_cost._recid in h_cost_obj_list:
                    continue
                else:
                    h_cost_obj_list.append(h_cost._recid)

                if h_artikel.artnrlager != 0 and artikel.endkum == f_eknr:

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == h_artikel.artnrlager)).first()

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 = s_list.qty1 + h_cost.anzahl
                        s_list.val1 = s_list.val1 + h_cost.anzahl * h_cost.betrag

                elif h_artikel.artnrrezept != 0:

                    h_rezept = db_session.query(H_rezept).filter(
                            (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                    if h_rezept:
                        recipe_bdown(h_rezept.artnrrezept, h_cost.anzahl)
        create_food()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty = s_list.qty2 - s_list.qty1
                s_list.d_val = s_list.val2 - s_list.val1
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 = t_val1 + s_list.val1
                t_val2 = t_val2 + s_list.val2
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 = t_val1
        s_list.val2 = t_val2
        s_list.d_val = t_val2 - t_val1

    def create_list11():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        datum:date = None
        t_val1:decimal = 0
        t_val2:decimal = 0
        s_list_list.clear()
        for datum in range(from_date,to_date + 1) :

            h_cost_obj_list = []
            for h_cost, h_artikel, artikel in db_session.query(H_cost, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_cost.artnr) &  (H_artikel.departement == H_cost.departement) &  ((H_artikel.artnrlager != 0) |  (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement) &  (Artikel.endkum == f_eknr)).filter(
                    (H_cost.datum == datum) &  (H_cost.flag == 1)).all():
                if h_cost._recid in h_cost_obj_list:
                    continue
                else:
                    h_cost_obj_list.append(h_cost._recid)

                if h_artikel.artnrlager != 0:

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == h_artikel.artnrlager)).first()

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 = s_list.qty1 + h_cost.anzahl
                        s_list.val1 = s_list.val1 + h_cost.anzahl * h_cost.betrag

                elif h_artikel.artnrrezept != 0:

                    h_rezept = db_session.query(H_rezept).filter(
                            (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                    if h_rezept:
                        recipe_bdown1(h_rezept.artnrrezept, h_cost.anzahl)
        create_food1()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty = s_list.qty2 - s_list.qty1
                s_list.d_val = s_list.val2 - s_list.val1
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 = t_val1 + s_list.val1
                t_val2 = t_val2 + s_list.val2
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 = t_val1
        s_list.val2 = t_val2
        s_list.d_val = t_val2 - t_val1

    def create_list2():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        datum:date = None
        t_val1:decimal = 0
        t_val2:decimal = 0
        s_list_list.clear()
        for datum in range(from_date,to_date + 1) :

            h_cost_obj_list = []
            for h_cost, h_artikel, artikel in db_session.query(H_cost, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_cost.artnr) &  (H_artikel.departement == H_cost.departement) &  ((H_artikel.artnrlager != 0) |  (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                    (H_cost.datum == datum) &  (H_cost.flag == 1)).all():
                if h_cost._recid in h_cost_obj_list:
                    continue
                else:
                    h_cost_obj_list.append(h_cost._recid)

                if h_artikel.artnrlager != 0 and artikel.endkum == b_eknr:

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == h_artikel.artnrlager)).first()

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 = s_list.qty1 + h_cost.anzahl
                        s_list.val1 = s_list.val1 + h_cost.anzahl * h_cost.betrag

                elif h_artikel.artnrrezept != 0:

                    h_rezept = db_session.query(H_rezept).filter(
                            (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                    if h_rezept:
                        recipe_bdown(h_rezept.artnrrezept, h_cost.anzahl)
        create_beverage()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty = s_list.qty2 - s_list.qty1
                s_list.d_val = s_list.val2 - s_list.val1
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 = t_val1 + s_list.val1
                t_val2 = t_val2 + s_list.val2
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 = t_val1
        s_list.val2 = t_val2
        s_list.d_val = t_val2 - t_val1

    def create_list22():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        datum:date = None
        t_val1:decimal = 0
        t_val2:decimal = 0
        s_list_list.clear()
        for datum in range(from_date,to_date + 1) :

            h_cost_obj_list = []
            for h_cost, h_artikel, artikel in db_session.query(H_cost, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_cost.artnr) &  (H_artikel.departement == H_cost.departement) &  ((H_artikel.artnrlager != 0) |  (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement) &  (Artikel.endkum == b_eknr)).filter(
                    (H_cost.datum == datum) &  (H_cost.flag == 1)).all():
                if h_cost._recid in h_cost_obj_list:
                    continue
                else:
                    h_cost_obj_list.append(h_cost._recid)

                if h_artikel.artnrlager != 0:

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == h_artikel.artnrlager)).first()

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 = s_list.qty1 + h_cost.anzahl
                        s_list.val1 = s_list.val1 + h_cost.anzahl * h_cost.betrag

                elif h_artikel.artnrrezept != 0:

                    h_rezept = db_session.query(H_rezept).filter(
                            (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                    if h_rezept:
                        recipe_bdown1(h_rezept.artnrrezept, h_cost.anzahl)
        create_beverage1()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty = s_list.qty2 - s_list.qty1
                s_list.d_val = s_list.val2 - s_list.val1
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 = t_val1 + s_list.val1
                t_val2 = t_val2 + s_list.val2
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 = t_val1
        s_list.val2 = t_val2
        s_list.d_val = t_val2 - t_val1

    def recipe_bdown(p_artnr:int, menge:decimal):

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        inh:decimal = 0
        H_recipe = H_rezept

        h_recipe = db_session.query(H_recipe).filter(
                (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():
            inh = menge * h_rezlin.menge / h_recipe.portion

            if h_rezlin.recipe_flag :
                recipe_bdown(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel and (((l_artikel.endkum == fl_eknr) and (sorttype == 1)) or ((l_artikel.endkum == bl_eknr) and (sorttype == 2))):

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.bezeich = l_artikel.bezeich
                        s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                    s_list.qty1 = s_list.qty1 + inh / l_artikel.inhalt

                    if preis_typ == 0 or l_artikel.ek_aktuell == 0:
                        s_list.val1 = s_list.val1 + inh / l_artikel.inhalt * l_artikel.vk_preis / (1 - h_rezlin.lostfact / 100)
                    else:
                        s_list.val1 = s_list.val1 + inh / l_artikel.inhalt * l_artikel.ek_aktuell / (1 - h_rezlin.lostfact / 100)

    def create_food():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == (food_bev).lower())).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) != (food_bev).lower()) &  (func.lower(L_ophdr.fibukonto) != "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_ophdr.fibukonto) &  (Gl_acct.acc_type == 2)).first()

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 = s_list.qty2 + l_op.anzahl
                s_list.val2 = s_list.val2 + l_op.warenwert

    def recipe_bdown1(p_artnr:int, menge:decimal):

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        inh:decimal = 0
        H_recipe = H_rezept

        h_recipe = db_session.query(H_recipe).filter(
                (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():
            inh = menge * h_rezlin.menge / h_recipe.portion

            if h_rezlin.recipe_flag :
                recipe_bdown1(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel:

                    s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.bezeich = l_artikel.bezeich
                        s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                    s_list.qty1 = s_list.qty1 + inh / l_artikel.inhalt

                    if preis_typ == 0 or l_artikel.ek_aktuell == 0:
                        s_list.val1 = s_list.val1 + inh / l_artikel.inhalt * l_artikel.vk_preis / (1 - h_rezlin.lostfact / 100)
                    else:
                        s_list.val1 = s_list.val1 + inh / l_artikel.inhalt * l_artikel.ek_aktuell / (1 - h_rezlin.lostfact / 100)

    def create_beverage1():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr and s_list.flag == 0), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == (food_bev).lower())).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr and s_list.flag == 1), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.flag = 1
                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) != (food_bev).lower()) &  (func.lower(L_ophdr.fibukonto) != "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_ophdr.fibukonto) &  (Gl_acct.acc_type == 2)).first()

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 = s_list.qty2 + l_op.anzahl
                s_list.val2 = s_list.val2 + l_op.warenwert

    def create_food1():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr and s_list.flag == 0), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == (bev_food).lower())).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr and s_list.flag == 1), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.flag = 1
                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) != (bev_food).lower()) &  (func.lower(L_ophdr.fibukonto) != "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_ophdr.fibukonto) &  (Gl_acct.acc_type == 2)).first()

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 = s_list.qty2 + l_op.anzahl
                s_list.val2 = s_list.val2 + l_op.warenwert

    def create_beverage():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal h_recipe


        nonlocal s_list, h_recipe
        nonlocal s_list_list

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr) &  (L_artikel.endkum == bl_eknr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr) &  (L_artikel.endkum == fl_eknr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) == (bev_food).lower())).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 = s_list.qty2 + l_op.anzahl
            s_list.val2 = s_list.val2 + l_op.warenwert

        l_ophdr_obj_list = []
        for l_ophdr, l_op, l_artikel in db_session.query(L_ophdr, L_op, L_artikel).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) &  (L_op.loeschflag <= 1) &  (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == l_op.artnr)).filter(
                (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.datum >= from_date) &  (L_ophdr.datum <= to_date) &  (func.lower(L_ophdr.fibukonto) != (bev_food).lower()) &  (func.lower(L_ophdr.fibukonto) != "0000000000")).all():
            if l_ophdr._recid in l_ophdr_obj_list:
                continue
            else:
                l_ophdr_obj_list.append(l_ophdr._recid)

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_ophdr.fibukonto) &  (Gl_acct.acc_type == 2)).first()

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 = s_list.qty2 + l_op.anzahl
                s_list.val2 = s_list.val2 + l_op.warenwert

    if sorttype == 1 and not incl_bf:
        create_list1()

    elif sorttype == 1 and incl_bf:
        create_list11()

    elif sorttype == 2 and not incl_fb:
        create_list2()

    elif sorttype == 2 and incl_fb:
        create_list22()

    return generate_output()