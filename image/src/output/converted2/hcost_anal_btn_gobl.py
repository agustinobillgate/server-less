#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Artikel, H_cost, L_artikel, H_rezept, H_rezlin, L_op, L_ophdr, Gl_acct

def hcost_anal_btn_gobl(sorttype:int, incl_bf:bool, incl_fb:bool, from_date:date, to_date:date, f_eknr:int, b_eknr:int, fl_eknr:int, bl_eknr:int, preis_typ:int, food_bev:string, bev_food:string):

    prepare_cache ([H_artikel, Artikel, H_cost, L_artikel, H_rezlin, L_op, L_ophdr])

    s_list_list = []
    h_artikel = artikel = h_cost = l_artikel = h_rezept = h_rezlin = l_op = l_ophdr = gl_acct = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"flag":int, "artnr":int, "bezeich":string, "munit":string, "qty1":Decimal, "val1":Decimal, "qty2":Decimal, "val2":Decimal, "d_qty":Decimal, "d_val":Decimal, "s_qty1":string, "s_qty2":string, "s_qty3":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        return {"s-list": s_list_list}

    def create_list1():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        datum:date = None
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        s_list_list.clear()
        for datum in date_range(from_date,to_date) :

            h_cost_obj_list = {}
            h_cost = H_cost()
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_cost.anzahl, h_cost.betrag, h_cost._recid, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel._recid, artikel.endkum, artikel._recid in db_session.query(H_cost.anzahl, H_cost.betrag, H_cost._recid, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel._recid, Artikel.endkum, Artikel._recid).join(H_artikel,(H_artikel.artnr == H_cost.artnr) & (H_artikel.departement == H_cost.departement) & ((H_artikel.artnrlager != 0) | (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                     (H_cost.datum == datum) & (H_cost.flag == 1)).order_by(H_artikel.bezeich).all():
                if h_cost_obj_list.get(h_cost._recid):
                    continue
                else:
                    h_cost_obj_list[h_cost._recid] = True

                if h_artikel.artnrlager != 0 and artikel.endkum == f_eknr:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 =  to_decimal(s_list.qty1) + to_decimal(h_cost.anzahl)
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag)

                elif h_artikel.artnrrezept != 0:

                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                    if h_rezept:
                        recipe_bdown(h_rezept.artnrrezept, h_cost.anzahl)
        create_food()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty =  to_decimal(s_list.qty2) - to_decimal(s_list.qty1)
                s_list.d_val =  to_decimal(s_list.val2) - to_decimal(s_list.val1)
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 =  to_decimal(t_val1) + to_decimal(s_list.val1)
                t_val2 =  to_decimal(t_val2) + to_decimal(s_list.val2)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 =  to_decimal(t_val1)
        s_list.val2 =  to_decimal(t_val2)
        s_list.d_val =  to_decimal(t_val2) - to_decimal(t_val1)


    def create_list11():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        datum:date = None
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        s_list_list.clear()
        for datum in date_range(from_date,to_date) :

            h_cost_obj_list = {}
            h_cost = H_cost()
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_cost.anzahl, h_cost.betrag, h_cost._recid, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel._recid, artikel.endkum, artikel._recid in db_session.query(H_cost.anzahl, H_cost.betrag, H_cost._recid, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel._recid, Artikel.endkum, Artikel._recid).join(H_artikel,(H_artikel.artnr == H_cost.artnr) & (H_artikel.departement == H_cost.departement) & ((H_artikel.artnrlager != 0) | (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.endkum == f_eknr)).filter(
                     (H_cost.datum == datum) & (H_cost.flag == 1)).order_by(H_artikel.bezeich).all():
                if h_cost_obj_list.get(h_cost._recid):
                    continue
                else:
                    h_cost_obj_list[h_cost._recid] = True

                if h_artikel.artnrlager != 0:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 =  to_decimal(s_list.qty1) + to_decimal(h_cost.anzahl)
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag)

                elif h_artikel.artnrrezept != 0:

                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                    if h_rezept:
                        recipe_bdown1(h_rezept.artnrrezept, h_cost.anzahl)
        create_food1()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty =  to_decimal(s_list.qty2) - to_decimal(s_list.qty1)
                s_list.d_val =  to_decimal(s_list.val2) - to_decimal(s_list.val1)
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 =  to_decimal(t_val1) + to_decimal(s_list.val1)
                t_val2 =  to_decimal(t_val2) + to_decimal(s_list.val2)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 =  to_decimal(t_val1)
        s_list.val2 =  to_decimal(t_val2)
        s_list.d_val =  to_decimal(t_val2) - to_decimal(t_val1)


    def create_list2():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        datum:date = None
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        s_list_list.clear()
        for datum in date_range(from_date,to_date) :

            h_cost_obj_list = {}
            h_cost = H_cost()
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_cost.anzahl, h_cost.betrag, h_cost._recid, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel._recid, artikel.endkum, artikel._recid in db_session.query(H_cost.anzahl, H_cost.betrag, H_cost._recid, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel._recid, Artikel.endkum, Artikel._recid).join(H_artikel,(H_artikel.artnr == H_cost.artnr) & (H_artikel.departement == H_cost.departement) & ((H_artikel.artnrlager != 0) | (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                     (H_cost.datum == datum) & (H_cost.flag == 1)).order_by(H_artikel.bezeich).all():
                if h_cost_obj_list.get(h_cost._recid):
                    continue
                else:
                    h_cost_obj_list[h_cost._recid] = True

                if h_artikel.artnrlager != 0 and artikel.endkum == b_eknr:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 =  to_decimal(s_list.qty1) + to_decimal(h_cost.anzahl)
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag)

                elif h_artikel.artnrrezept != 0:

                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                    if h_rezept:
                        recipe_bdown(h_rezept.artnrrezept, h_cost.anzahl)
        create_beverage()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty =  to_decimal(s_list.qty2) - to_decimal(s_list.qty1)
                s_list.d_val =  to_decimal(s_list.val2) - to_decimal(s_list.val1)
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 =  to_decimal(t_val1) + to_decimal(s_list.val1)
                t_val2 =  to_decimal(t_val2) + to_decimal(s_list.val2)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 =  to_decimal(t_val1)
        s_list.val2 =  to_decimal(t_val2)
        s_list.d_val =  to_decimal(t_val2) - to_decimal(t_val1)


    def create_list22():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        datum:date = None
        t_val1:Decimal = to_decimal("0.0")
        t_val2:Decimal = to_decimal("0.0")
        s_list_list.clear()
        for datum in date_range(from_date,to_date) :

            h_cost_obj_list = {}
            h_cost = H_cost()
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_cost.anzahl, h_cost.betrag, h_cost._recid, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel._recid, artikel.endkum, artikel._recid in db_session.query(H_cost.anzahl, H_cost.betrag, H_cost._recid, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel._recid, Artikel.endkum, Artikel._recid).join(H_artikel,(H_artikel.artnr == H_cost.artnr) & (H_artikel.departement == H_cost.departement) & ((H_artikel.artnrlager != 0) | (H_artikel.artnrrezept != 0))).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.endkum == b_eknr)).filter(
                     (H_cost.datum == datum) & (H_cost.flag == 1)).order_by(H_artikel.bezeich).all():
                if h_cost_obj_list.get(h_cost._recid):
                    continue
                else:
                    h_cost_obj_list[h_cost._recid] = True

                if h_artikel.artnrlager != 0:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                    if l_artikel:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.artnr = l_artikel.artnr
                            s_list.bezeich = l_artikel.bezeich
                            s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                        s_list.qty1 =  to_decimal(s_list.qty1) + to_decimal(h_cost.anzahl)
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag)

                elif h_artikel.artnrrezept != 0:

                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                    if h_rezept:
                        recipe_bdown1(h_rezept.artnrrezept, h_cost.anzahl)
        create_beverage1()

        for s_list in query(s_list_list):

            if s_list.qty1 == 0 and s_list.qty2 == 0:
                s_list_list.remove(s_list)
            else:
                s_list.d_qty =  to_decimal(s_list.qty2) - to_decimal(s_list.qty1)
                s_list.d_val =  to_decimal(s_list.val2) - to_decimal(s_list.val1)
                s_list.s_qty1 = to_string(s_list.qty1, "->,>>>,>>9.99")
                s_list.s_qty2 = to_string(s_list.qty2, "->,>>>,>>9.99")
                s_list.s_qty3 = to_string(s_list.d_qty, "->,>>>,>>9.99")
                t_val1 =  to_decimal(t_val1) + to_decimal(s_list.val1)
                t_val2 =  to_decimal(t_val2) + to_decimal(s_list.val2)
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.flag = 2
        s_list.bezeich = "T O T A L"
        s_list.val1 =  to_decimal(t_val1)
        s_list.val2 =  to_decimal(t_val2)
        s_list.d_val =  to_decimal(t_val2) - to_decimal(t_val1)


    def recipe_bdown(p_artnr:int, menge:Decimal):

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        inh:Decimal = to_decimal("0.0")
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                recipe_bdown(h_rezlin.artnrlager, inh)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if l_artikel and (((l_artikel.endkum == fl_eknr) and (sorttype == 1)) or ((l_artikel.endkum == bl_eknr) and (sorttype == 2))):

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.bezeich = l_artikel.bezeich
                        s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                    s_list.qty1 =  to_decimal(s_list.qty1) + to_decimal(inh) / to_decimal(l_artikel.inhalt)

                    if preis_typ == 0 or l_artikel.ek_aktuell == 0:
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                    else:
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))


    def create_food():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == (food_bev).lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto != (food_bev).lower()) & (L_ophdr.fibukonto != ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)],"acc_type": [(eq, 2)]})

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
                s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)


    def recipe_bdown1(p_artnr:int, menge:Decimal):

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        inh:Decimal = to_decimal("0.0")
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                recipe_bdown1(h_rezlin.artnrlager, inh)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if l_artikel:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                    if not s_list:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.bezeich = l_artikel.bezeich
                        s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                    s_list.qty1 =  to_decimal(s_list.qty1) + to_decimal(inh) / to_decimal(l_artikel.inhalt)

                    if preis_typ == 0 or l_artikel.ek_aktuell == 0:
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                    else:
                        s_list.val1 =  to_decimal(s_list.val1) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))


    def create_beverage1():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr and s_list.flag == 0), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == (food_bev).lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr and s_list.flag == 1), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.flag = 1
                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto != (food_bev).lower()) & (L_ophdr.fibukonto != ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)],"acc_type": [(eq, 2)]})

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
                s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)


    def create_food1():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr and s_list.flag == 0), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == (bev_food).lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr and s_list.flag == 1), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.flag = 1
                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto != (bev_food).lower()) & (L_ophdr.fibukonto != ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)],"acc_type": [(eq, 2)]})

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
                s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)


    def create_beverage():

        nonlocal s_list_list, h_artikel, artikel, h_cost, l_artikel, h_rezept, h_rezlin, l_op, l_ophdr, gl_acct
        nonlocal sorttype, incl_bf, incl_fb, from_date, to_date, f_eknr, b_eknr, fl_eknr, bl_eknr, preis_typ, food_bev, bev_food


        nonlocal s_list
        nonlocal s_list_list

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == bl_eknr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == fl_eknr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto == (bev_food).lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.artnr = l_artikel.artnr
                s_list.bezeich = l_artikel.bezeich
                s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
            s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
            s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)

        l_ophdr_obj_list = {}
        l_ophdr = L_ophdr()
        l_op = L_op()
        l_artikel = L_artikel()
        for l_ophdr.fibukonto, l_ophdr._recid, l_op.anzahl, l_op.warenwert, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.endkum, l_artikel.ek_aktuell, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_ophdr.fibukonto, L_ophdr._recid, L_op.anzahl, L_op.warenwert, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.endkum, L_artikel.ek_aktuell, L_artikel.vk_preis, L_artikel._recid).join(L_op,(L_op.lscheinnr == L_ophdr.lscheinnr) & (L_op.loeschflag <= 1) & (L_op.op_art == 3)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_ophdr.op_typ == ("STT").lower()) & (L_ophdr.datum >= from_date) & (L_ophdr.datum <= to_date) & (L_ophdr.fibukonto != (bev_food).lower()) & (L_ophdr.fibukonto != ("0000000000").lower())).order_by(L_ophdr._recid).all():
            if l_ophdr_obj_list.get(l_ophdr._recid):
                continue
            else:
                l_ophdr_obj_list[l_ophdr._recid] = True

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophdr.fibukonto)],"acc_type": [(eq, 2)]})

            if gl_acct:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == l_artikel.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = l_artikel.artnr
                    s_list.bezeich = l_artikel.bezeich
                    s_list.munit = trim(to_string(l_artikel.inhalt, ">>,>>9")) + " " + l_artikel.masseinheit
                s_list.qty2 =  to_decimal(s_list.qty2) + to_decimal(l_op.anzahl)
                s_list.val2 =  to_decimal(s_list.val2) + to_decimal(l_op.warenwert)


    if sorttype == 1 and not incl_bf:
        create_list1()

    elif sorttype == 1 and incl_bf:
        create_list11()

    elif sorttype == 2 and not incl_fb:
        create_list2()

    elif sorttype == 2 and incl_fb:
        create_list22()

    return generate_output()