#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import Htparam, H_artikel, Hoteldpt, Artikel, H_umsatz, H_journal, Wgrpdep

subgr_list_list, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":string}, {"selected": True})

def menu_eng_btn_go_webbl(subgr_list_list:[Subgr_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:Decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):

    prepare_cache ([Htparam, H_artikel, Hoteldpt, Artikel, H_journal, Wgrpdep])

    fb_cost_analyst_list = []
    t_anz:int = 0
    t_sales:Decimal = to_decimal("0.0")
    t_cost:Decimal = to_decimal("0.0")
    t_margin:Decimal = to_decimal("0.0")
    st_sales:Decimal = 0
    st_cost:Decimal = 0
    st_margin:Decimal = 0
    st_proz2:Decimal = 0
    s_anzahl:int = 0
    s_proz1:Decimal = 0
    price_type:int = 0
    htparam = h_artikel = hoteldpt = artikel = h_umsatz = h_journal = wgrpdep = None

    subgr_list = h_list = fb_cost_analyst = None

    h_list_list, H_list = create_model("H_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal})
    fb_cost_analyst_list, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":string, "bezeich":string, "qty":string, "proz1":string, "epreis":string, "cost":string, "margin":string, "t_sales":string, "t_cost":string, "t_margin":string, "proz2":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        return {"fb-cost-analyst": fb_cost_analyst_list}

    def create_h_umsatz1():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        do_it:bool = False
        tmp_anzahl:int = 0
        cost:Decimal = to_decimal("0.0")
        anz:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        fb_cost_analyst_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.artnrrezept, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel.epreis1, h_artikel.prozent, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnrrezept, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel.epreis1, H_artikel.prozent, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) & (Artikel.endkum != disc_nr)).filter(
                     (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                if h_artikel_obj_list.get(h_artikel._recid):
                    continue
                else:
                    h_artikel_obj_list[h_artikel._recid] = True


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.cost =  to_decimal("0")
                    h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))
                    h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                    else:
                        h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)

                    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    while None != h_umsatz:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")
                        h_list.cost =  to_decimal("0")
                        h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                        if h_list.cost != 0:
                            cost =  to_decimal(anz) * to_decimal(h_list.cost)
                        else:

                            h_journal = get_cache (H_journal, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"bill_datum": [(eq, h_umsatz.datum)]})

                            if h_journal:
                                cost =  to_decimal(anz) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                h_list.cost =  to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")


                            else:
                                cost =  to_decimal(anz) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)


                        cost =  to_decimal(cost) / to_decimal(fact1)
                        h_list.anzahl = h_list.anzahl + anz
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        t_cost =  to_decimal(t_cost) + to_decimal(cost)
                        t_anz = t_anz + anz
                        t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                        if h_list.anzahl != 0 and h_list.anzahl != None:
                            tmp_anzahl = 0
                        else:
                            tmp_anzahl = h_list.anzahl

                        if vat_included and tmp_anzahl != 0:
                            h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                        elif tmp_anzahl != 0:
                            h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)
                        else:
                            h_list.epreis =  to_decimal("0")

                        curr_recid = h_umsatz._recid
                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_h_umsatz2():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        do_it:bool = False
        cost:Decimal = to_decimal("0.0")
        anz:int = 0
        tmp_anzahl:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        fb_cost_analyst_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.artnrrezept, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel.epreis1, h_artikel.prozent, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnrrezept, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel.epreis1, H_artikel.prozent, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 6) & (Artikel.endkum != disc_nr)).filter(
                     (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                if h_artikel_obj_list.get(h_artikel._recid):
                    continue
                else:
                    h_artikel_obj_list[h_artikel._recid] = True


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.cost =  to_decimal("0")
                    h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))
                    h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                    else:
                        h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)

                    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    while None != h_umsatz:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")
                        h_list.cost =  to_decimal("0")
                        h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                        if h_list.cost != 0:
                            cost =  to_decimal(anz) * to_decimal(h_list.cost)
                        else:

                            h_journal = get_cache (H_journal, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"bill_datum": [(eq, h_umsatz.datum)]})

                            if h_journal:
                                cost =  to_decimal(anz) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                h_list.cost =  to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")


                            else:
                                cost =  to_decimal(anz) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)


                        cost =  to_decimal(cost) / to_decimal(fact1)
                        h_list.anzahl = h_list.anzahl + anz
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        t_cost =  to_decimal(t_cost) + to_decimal(cost)
                        t_anz = t_anz + anz
                        t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                        if h_list.anzahl != 0 and h_list.anzahl != None:
                            tmp_anzahl = 0
                        else:
                            tmp_anzahl = h_list.anzahl

                        if vat_included and tmp_anzahl != 0:
                            h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                        elif tmp_anzahl != 0:
                            h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)
                        else:
                            h_list.epreis =  to_decimal("0")

                        curr_recid = h_umsatz._recid
                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_h_umsatz3():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        do_it:bool = False
        cost:Decimal = to_decimal("0.0")
        anz:int = 0
        tmp_anzahl:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        fb_cost_analyst_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.artnrrezept, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel.epreis1, h_artikel.prozent, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnrrezept, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel.epreis1, H_artikel.prozent, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 4) & (Artikel.endkum != disc_nr)).filter(
                     (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                if h_artikel_obj_list.get(h_artikel._recid):
                    continue
                else:
                    h_artikel_obj_list[h_artikel._recid] = True


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.cost =  to_decimal("0")
                    h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))
                    h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                    else:
                        h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)

                    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    while None != h_umsatz:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")
                        h_list.cost =  to_decimal("0")
                        h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                        if h_list.cost != 0:
                            cost =  to_decimal(anz) * to_decimal(h_list.cost)
                        else:

                            h_journal = get_cache (H_journal, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"bill_datum": [(eq, h_umsatz.datum)]})

                            if h_journal:
                                cost =  to_decimal(anz) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                h_list.cost =  to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")


                            else:
                                cost =  to_decimal(anz) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)


                        cost =  to_decimal(cost) / to_decimal(fact1)
                        h_list.anzahl = h_list.anzahl + anz
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        t_cost =  to_decimal(t_cost) + to_decimal(cost)
                        t_anz = t_anz + anz
                        t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                        if h_list.anzahl != 0 and h_list.anzahl != None:
                            tmp_anzahl = 0
                        else:
                            tmp_anzahl = h_list.anzahl

                        if vat_included and tmp_anzahl != 0:
                            h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                        elif tmp_anzahl != 0:
                            h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)
                        else:
                            h_list.epreis =  to_decimal("0")

                        curr_recid = h_umsatz._recid
                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_list(pos:bool):

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        if mi_subgrp:
            create_list1(pos)

            return

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num)):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)


            if short_flag:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, "->>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "->>,>>>,>>>,>>9.99")
                fb_cost_analyst.t_cost = to_string(t_cost, "->>,>>>,>>>,>>9.99")
                fb_cost_analyst.t_margin = to_string(t_margin, "->>,>>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, "->>9.99")


            else:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, "->>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "->>>,>>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(t_cost, "->>>,>>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(t_margin, "->,>>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, "->>9.99")


            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)

    def create_list1(pos:bool):

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        curr_grp:int = 0

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                add_sub()

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                add_sub()

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                add_sub()

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                add_sub()

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                add_sub()

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->,>>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>>>>9")
                    fb_cost_analyst.bezeich = h_list.bezeich
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.99")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.99")


                add_sub()
        create_sub(curr_grp)

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)


            if short_flag:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, "->>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "->>,>>>,>>>,>>9.99")
                fb_cost_analyst.t_cost = to_string(t_cost, "->>,>>>,>>>,>>9.99")
                fb_cost_analyst.t_margin = to_string(t_margin, "->>,>>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, "->>9.99")


            else:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, "->>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(t_cost, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(t_margin, "->,>>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, "->>9.99")


            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)

    def create_sub(curr_grp:int):

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list

        if curr_grp != 0:

            if st_sales != 0:
                st_margin =  to_decimal(st_cost) / to_decimal(st_sales) * to_decimal("100")

            if short_flag:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.flag = 2
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("S u b T o t a l")
                fb_cost_analyst.qty = to_string(s_anzahl, "->>>>9")
                fb_cost_analyst.proz1 = to_string(s_proz1, "->>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(st_sales, "->,>>>,>>>,>>9.99")
                fb_cost_analyst.t_cost = to_string(st_cost, "->,>>>,>>>,>>9.99")
                fb_cost_analyst.t_margin = to_string(st_margin, "->,>>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(st_proz2, "->>9.9")


            else:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.flag = 2
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("S u b T o t a l")
                fb_cost_analyst.qty = to_string(s_anzahl, "->>>>9")
                fb_cost_analyst.proz1 = to_string(s_proz1, "->>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(st_sales, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(st_cost, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(st_margin, "->>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(st_proz2, "->>9.9")


            s_anzahl = 0
            s_proz1 =  to_decimal("0")
            st_sales =  to_decimal("0")
            st_cost =  to_decimal("0")
            st_margin =  to_decimal("0")
            st_proz2 =  to_decimal("0")


    def add_sub():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_list, fb_cost_analyst_list


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    elif sorttype == 3:
        create_h_umsatz3()

    return generate_output()