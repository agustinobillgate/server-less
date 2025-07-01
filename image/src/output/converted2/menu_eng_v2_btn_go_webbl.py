#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_artikel, Hoteldpt, Artikel, H_cost, H_umsatz, H_journal, Wgrpdep

subgr_list_list, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":string}, {"selected": True})

def menu_eng_v2_btn_go_webbl(subgr_list_list:[Subgr_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:Decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):

    prepare_cache ([H_artikel, Hoteldpt, Artikel, H_cost, H_umsatz, H_journal, Wgrpdep])

    output_list2_list = []
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
    gtotal_sold:Decimal = to_decimal("0.0")
    gtotal_sold_perc:Decimal = to_decimal("0.0")
    gtotal_cost:Decimal = to_decimal("0.0")
    gtotal_revenue:Decimal = to_decimal("0.0")
    gtotal_profit:Decimal = to_decimal("0.0")
    avrg_item_profit:Decimal = to_decimal("0.0")
    food_cost:Decimal = to_decimal("0.0")
    menu_pop_factor:Decimal = to_decimal("0.0")
    count_foodcost:Decimal = to_decimal("0.0")
    curr_grp:int = 0
    grp_bez:string = ""
    h_artikel = hoteldpt = artikel = h_cost = h_umsatz = h_journal = wgrpdep = None

    subgr_list = output_list = h_list = fb_cost_analyst = output_list2 = ph_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "bezeich":string, "s":string})
    h_list_list, H_list = create_model("H_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal})
    fb_cost_analyst_list, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":int, "bezeich":string, "qty":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal, "item_profit":Decimal, "total_profit":Decimal, "profit_category":string, "popularity_category":string, "menu_item_class":string})
    output_list2_list, Output_list2 = create_model("Output_list2", {"flag":int, "artnr":int, "dept":string, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "item_prof":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "profit":Decimal, "proz2":Decimal, "profit_cat":string, "popularity_cat":string, "menu_item_class":string, "s":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        return {"output-list2": output_list2_list}

    def create_h_umsatz1():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

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
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        Ph_list = H_list
        ph_list_list = h_list_list
        output_list_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                output_list.s = " " + to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.epreis1, h_artikel.prozent, h_artikel.bezeich, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.epreis1, H_artikel.prozent, H_artikel.bezeich, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) & (Artikel.endkum != disc_nr)).filter(
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

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, to_date)],"flag": [(eq, 1)]})
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_list.append(h_list)


                    if h_cost and h_cost.betrag != 0:
                        h_list.cost =  to_decimal(h_cost.betrag)
                    else:
                        h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
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
                    for datum in date_range(from_date,to_date) :
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, datum)]})

                        if h_umsatz:
                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                h_journal = get_cache (H_journal, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"bill_datum": [(eq, datum)]})

                                if h_journal:
                                    cost =  to_decimal(anz) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
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

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_h_umsatz2():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

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
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        output_list_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                output_list.s = " " + to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.epreis1, h_artikel.prozent, h_artikel.bezeich, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.epreis1, H_artikel.prozent, H_artikel.bezeich, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 6) & (Artikel.endkum != disc_nr)).filter(
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

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, to_date)],"flag": [(eq, 1)]})
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_list.append(h_list)


                    if h_cost and h_cost.betrag != 0:
                        h_list.cost =  to_decimal(h_cost.betrag)
                    else:
                        h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
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
                    for datum in date_range(from_date,to_date) :
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, datum)]})

                        if h_umsatz:
                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                h_journal = get_cache (H_journal, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"bill_datum": [(eq, datum)]})

                                if h_journal:
                                    cost =  to_decimal(anz) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
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

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_list(pos:bool):

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        if mi_subgrp:
            create_list1(pos)

            return

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num)):
                do_create_list()

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):
                do_create_list()

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):
                do_create_list()

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):
                do_create_list()

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):
                do_create_list()

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):
                do_create_list()

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.bezeich = to_string("T o t a l", "x(24)")

            if short_flag:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>,>>9") + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(t_sales, " ->>>,>>>,>>9") + " " + to_string(t_cost, " ->>>,>>>,>>9") + to_string(t_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
            else:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>,>>9") + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(t_sales, " ->,>>>,>>>,>>9") + " " + to_string(t_cost, " ->>>,>>>,>>9") + to_string(t_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            output_list2.bezeich = "T o t a l"
            output_list2.anzahl = t_anz
            output_list2.proz1 =  to_decimal("100")
            output_list2.t_sales =  to_decimal(t_sales)
            output_list2.t_cost =  to_decimal(t_cost)
            output_list2.t_margin =  to_decimal(t_margin)
            output_list2.proz2 =  to_decimal("100")


            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

    def create_list1(pos:bool):

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):
                do_create_list1()

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):
                do_create_list1()

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):
                do_create_list1()

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):
                do_create_list1()

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):
                do_create_list1()

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):
                do_create_list1()
        create_sub(curr_grp)

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.bezeich = to_string("T o t a l", "x(24)")

            if short_flag:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>,>>9") + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(t_sales, " ->>>,>>>,>>9") + " " + to_string(t_cost, " ->>>,>>>,>>9") + to_string(t_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
            else:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>,>>9") + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(t_sales, " ->,>>>,>>>,>>9") + " " + to_string(t_cost, " ->>>,>>>,>>9") + to_string(t_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            output_list2.bezeich = "T o t a l"
            output_list2.anzahl = t_anz
            output_list2.proz1 =  to_decimal("100")
            output_list2.t_sales =  to_decimal(t_sales)
            output_list2.t_cost =  to_decimal(t_cost)
            output_list2.t_margin =  to_decimal(t_margin)
            output_list2.proz2 =  to_decimal("100")


            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

    def create_outlist():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list


        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.artnr = h_list.artnr
        output_list2.bezeich = h_list.bezeich
        output_list2.anzahl = h_list.anzahl
        output_list2.proz1 =  to_decimal(h_list.proz1)
        output_list2.epreis =  to_decimal(h_list.epreis)
        output_list2.cost =  to_decimal(h_list.cost)
        output_list2.margin =  to_decimal(h_list.margin)
        output_list2.t_sales =  to_decimal(h_list.t_sales)
        output_list2.t_cost =  to_decimal(h_list.t_cost)
        output_list2.t_margin =  to_decimal(h_list.t_margin)
        output_list2.proz2 =  to_decimal(h_list.proz2)
        output_list2.item_prof =  to_decimal(output_list2.epreis) - to_decimal(output_list2.cost)
        output_list2.profit =  to_decimal(output_list2.t_sales) - to_decimal(output_list2.t_cost)


    def do_create_list():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        if t_anz != 0:
            h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

        if h_list.t_sales != 0:
            h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

        if t_sales != 0:
            h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.bezeich = to_string(h_list.bezeich, "x(75)")

        if short_flag:
            output_list.s = to_string(h_list.artnr, ">>>>9") +\
                    to_string(h_list.bezeich, "x(75)") +\
                    to_string(h_list.anzahl, "->>>>9") +\
                    to_string(h_list.proz1, "->>9.9") +\
                    to_string(h_list.epreis, "->,>>>,>>9.9") +\
                    to_string(h_list.cost, "->,>>>,>>9.9") +\
                    to_string(h_list.margin, "->>>,>>9.99 ") +\
                    to_string(h_list.t_sales, " ->>>,>>>,>>9.9") +\
                    to_string(h_list.t_cost, " ->>>,>>>,>>9.9") +\
                    to_string(h_list.t_margin, " ->>>,>>9.99 ") +\
                    to_string(h_list.proz2, "->>9.9")


        else:
            output_list.s = to_string(h_list.artnr, ">>>>9") +\
                    to_string(h_list.bezeich, "x(75)") +\
                    to_string(h_list.anzahl, "->>>>9") +\
                    to_string(h_list.proz1, "->>9.9") +\
                    to_string(h_list.epreis, "->>>,>>>,>>9") +\
                    to_string(h_list.cost, "->>>,>>>,>>9") +\
                    to_string(h_list.margin, "->>>,>>9.99 ") +\
                    to_string(h_list.t_sales, " ->,>>>,>>>,>>9") +\
                    to_string(h_list.t_cost, " ->>>,>>>,>>9") +\
                    to_string(h_list.t_margin, " ->>>,>>9.99 ") +\
                    to_string(h_list.proz2, "->>9.9")


        create_outlist()


    def do_create_list1():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        if curr_grp != h_list.zknr:
            create_sub(curr_grp)

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})

            if wgrpdep:
                grp_bez = wgrpdep.bezeich
            else:
                grp_bez = ""
            curr_grp = h_list.zknr
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 1
            output_list.s = " " + to_string(grp_bez, "x(75)")
            output_list.bezeich = to_string(grp_bez, "x(75)")

        if t_anz != 0:
            h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

        if h_list.t_sales != 0:
            h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

        if t_sales != 0:
            h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.bezeich = to_string(h_list.bezeich, "x(75)")

        if short_flag:
            output_list.s = to_string(h_list.artnr, ">>>>9") +\
                    to_string(h_list.bezeich, "x(75)") +\
                    to_string(h_list.anzahl, "->>>>9") +\
                    to_string(h_list.proz1, "->>9.9") +\
                    to_string(h_list.epreis, "->,>>>,>>9.9") +\
                    to_string(h_list.cost, "->,>>>,>>9.9") +\
                    to_string(h_list.margin, "->>>,>>9.99 ") +\
                    to_string(h_list.t_sales, " ->>>,>>>,>>9.9") +\
                    to_string(h_list.t_cost, " ->>>,>>>,>>9.9") +\
                    to_string(h_list.t_margin, " ->>>,>>9.99 ") +\
                    to_string(h_list.proz2, "->>9.9")


        else:
            output_list.s = to_string(h_list.artnr, ">>>>9") +\
                    to_string(h_list.bezeich, "x(75)") +\
                    to_string(h_list.anzahl, "->>>>9") +\
                    to_string(h_list.proz1, "->>9.9") +\
                    to_string(h_list.epreis, "->>>,>>>,>>9") +\
                    to_string(h_list.cost, "->>>,>>>,>>9") +\
                    to_string(h_list.margin, "->>>,>>9.99 ") +\
                    to_string(h_list.t_sales, " ->,>>>,>>>,>>9") +\
                    to_string(h_list.t_cost, " ->>>,>>>,>>9") +\
                    to_string(h_list.t_margin, " ->>>,>>9.99 ") +\
                    to_string(h_list.proz2, "->>9.9")


        add_sub()
        create_outlist()


    def create_sub(curr_grp:int):

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        if curr_grp != 0:

            if st_sales != 0:
                st_margin =  to_decimal(st_cost) / to_decimal(st_sales) * to_decimal("100")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = 2
            output_list.bezeich = "S u b T o t a l"
            output_list.s = to_string(" ", "x(5)") +\
                    to_string("S u b T o t a l", "x(24)") +\
                    to_string(s_anzahl, "->>>>9") +\
                    to_string(s_proz1, "->>9.9") +\
                    to_string(" ", "x(36)") +\
                    to_string(st_sales, " ->,>>>,>>>,>>9") +\
                    to_string(st_cost, " ->>>,>>>,>>9") +\
                    to_string(st_margin, " ->>>,>>9.99 ") +\
                    to_string(st_proz2, "->>9.9")


            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            output_list2.bezeich = "S u b T o t a l"
            output_list2.anzahl = s_anzahl
            output_list2.proz1 =  to_decimal(s_proz1)
            output_list2.t_sales =  to_decimal(st_sales)
            output_list2.t_cost =  to_decimal(st_cost)
            output_list2.t_margin =  to_decimal(st_margin)
            output_list2.proz2 =  to_decimal(st_proz2)


            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            s_anzahl = 0
            s_proz1 =  to_decimal("0")
            st_sales =  to_decimal("0")
            st_cost =  to_decimal("0")
            st_margin =  to_decimal("0")
            st_proz2 =  to_decimal("0")


    def add_sub():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, curr_grp, grp_bez, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)


    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    for output_list2 in query(output_list2_list):
        gtotal_sold =  to_decimal(gtotal_sold) + to_decimal(output_list2.anzahl)
        gtotal_sold_perc =  to_decimal(gtotal_sold_perc) + to_decimal(output_list2.proz1)
        gtotal_cost =  to_decimal(gtotal_cost) + to_decimal(output_list2.t_cost)
        gtotal_revenue =  to_decimal(gtotal_revenue) + to_decimal(output_list2.t_sales)
        gtotal_profit =  to_decimal(gtotal_profit) + to_decimal(output_list2.profit)

        if output_list2.artnr != 0:
            count_foodcost =  to_decimal(count_foodcost) + to_decimal("1")
    avrg_item_profit =  to_decimal(gtotal_profit) / to_decimal(gtotal_sold)
    menu_pop_factor = ( to_decimal((1) / to_decimal(count_foodcost)) * to_decimal(0.8))

    for output_list2 in query(output_list2_list):

        if output_list2.item_prof < avrg_item_profit:
            output_list2.profit_cat = "LOW"
        else:
            output_list2.profit_cat = "HIGH"

        if output_list2.proz1 < menu_pop_factor:
            output_list2.popularity_cat = "LOW"
        else:
            output_list2.popularity_cat = "HIGH"

        if output_list2.profit_cat.lower()  == ("LOW").lower()  and output_list2.popularity_cat.lower()  == ("LOW").lower() :
            output_list2.menu_item_class = "DOG"

        elif output_list2.profit_cat.lower()  == ("LOW").lower()  and output_list2.popularity_cat.lower()  == ("HIGH").lower() :
            output_list2.menu_item_class = "WORKHORSE"

        elif output_list2.profit_cat.lower()  == ("HIGH").lower()  and output_list2.popularity_cat.lower()  == ("LOW").lower() :
            output_list2.menu_item_class = "CHALLENGE"

        elif output_list2.profit_cat.lower()  == ("HIGH").lower()  and output_list2.popularity_cat.lower()  == ("HIGH").lower() :
            output_list2.menu_item_class = "STAR"

    return generate_output()