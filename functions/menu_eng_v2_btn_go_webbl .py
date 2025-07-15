from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_artikel, Hoteldpt, Artikel, H_cost, H_umsatz, H_journal, Wgrpdep

subgr_list_list, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":str}, {"selected": True})

def menu_eng_v2_btn_go_webbl (subgr_list_list:[Subgr_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):
    output_list2_list = []
    t_anz:int = 0
    t_sales:decimal = to_decimal("0.0")
    t_cost:decimal = to_decimal("0.0")
    t_margin:decimal = to_decimal("0.0")
    st_sales:decimal = 0 FORMAT ">>,>>>,>>9.99"
    st_cost:decimal = 0 FORMAT ">>,>>>,>>9.99"
    st_margin:decimal = 0 FORMAT "->,>>>,>>9.99"
    st_proz2:decimal = 0 FORMAT ">>9.99"
    s_anzahl:int = 0 FORMAT "->>>>>9"
    s_proz1:decimal = 0 FORMAT ">>9.99"
    gtotal_sold:decimal = to_decimal("0.0")
    gtotal_sold_perc:decimal = to_decimal("0.0")
    gtotal_cost:decimal = to_decimal("0.0")
    gtotal_revenue:decimal = to_decimal("0.0")
    gtotal_profit:decimal = to_decimal("0.0")
    avrg_item_profit:decimal = to_decimal("0.0")
    food_cost:decimal = to_decimal("0.0")
    menu_pop_factor:decimal = to_decimal("0.0")
    count_foodcost:decimal = to_decimal("0.0")
    h_artikel = hoteldpt = artikel = h_cost = h_umsatz = h_journal = wgrpdep = None

    subgr_list = output_list = h_list = fb_cost_analyst = output_list2 = ph_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "bezeich":str, "s":str})
    h_list_list, H_list = create_model("H_list", {"flag":str, "artnr":int, "dept":int, "bezeich":str, "zknr":int, "grpname":str, "anzahl":int, "proz1":decimal, "epreis":decimal, "cost":decimal, "margin":decimal, "t_sales":decimal, "t_cost":decimal, "t_margin":decimal, "proz2":decimal})
    fb_cost_analyst_list, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":int, "bezeich":str, "qty":int, "proz1":decimal, "epreis":decimal, "cost":decimal, "margin":decimal, "t_sales":decimal, "t_cost":decimal, "t_margin":decimal, "proz2":decimal, "item_profit":decimal, "total_profit":decimal, "profit_category":str, "popularity_category":str, "menu_item_class":str})
    output_list2_list, Output_list2 = create_model("Output_list2", {"flag":int, "artnr":int, "dept":str, "bezeich":str, "zknr":int, "grpname":str, "anzahl":int, "proz1":decimal, "epreis":decimal, "cost":decimal, "margin":decimal, "item_prof":decimal, "t_sales":decimal, "t_cost":decimal, "t_margin":decimal, "profit":decimal, "proz2":decimal, "profit_cat":str, "popularity_cat":str, "menu_item_class":str, "s":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list
        return {"output-list2": output_list2_list}

    def create_h_umsatz1():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        do_it:bool = False
        cost:decimal = to_decimal("0.0")
        anz:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        Ph_list = H_list
        ph_list_list = h_list_list
        output_list_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

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

            h_artikel_obj_list = []
            for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) & (Artikel.endkum != disc_nr)).filter(
                     (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                if h_artikel._recid in h_artikel_obj_list:
                    continue
                else:
                    h_artikel_obj_list.append(h_artikel._recid)


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:

                    h_cost = db_session.query(H_cost).filter(
                             (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == to_date) & (H_cost.flag == 1)).first()
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

                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum == datum)).first()

                        if h_umsatz:
                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")

                            h_cost = db_session.query(H_cost).filter(
                                     (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == datum) & (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                h_journal = db_session.query(H_journal).filter(
                                         (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == datum)).first()

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

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        do_it:bool = False
        cost:decimal = to_decimal("0.0")
        anz:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        output_list_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

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

            h_artikel_obj_list = []
            for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 6) & (Artikel.endkum != disc_nr)).filter(
                     (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                if h_artikel._recid in h_artikel_obj_list:
                    continue
                else:
                    h_artikel_obj_list.append(h_artikel._recid)


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:

                    h_cost = db_session.query(H_cost).filter(
                             (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == to_date) & (H_cost.flag == 1)).first()
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

                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum == datum)).first()

                        if h_umsatz:
                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")

                            h_cost = db_session.query(H_cost).filter(
                                     (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == datum) & (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                h_journal = db_session.query(H_journal).filter(
                                         (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == datum)).first()

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

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

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
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(75)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")


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

    def create_list1(pos:bool):

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        curr_grp:int = 0

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                 (Wgrpdep.departement == h_list.dept) & (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(75)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(75)")

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                add_sub()


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                 (Wgrpdep.departement == h_list.dept) & (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(75)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(75)")

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                add_sub()


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                 (Wgrpdep.departement == h_list.dept) & (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(75)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(75)")

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                add_sub()


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                 (Wgrpdep.departement == h_list.dept) & (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(75)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(75)")

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                add_sub()


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                 (Wgrpdep.departement == h_list.dept) & (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(75)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(75)")

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                add_sub()


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                 (Wgrpdep.departement == h_list.dept) & (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(75)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(75)")

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
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->,>>>,>>9.9") + to_string(h_list.cost, "->,>>>,>>9.9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->>>,>>>,>>9.9") + to_string(h_list.t_cost, " ->>>,>>>,>>9.9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>9") + to_string(h_list.bezeich, "x(75)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.9") + to_string(h_list.epreis, "->>>,>>>,>>9") + to_string(h_list.cost, "->>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, " ->,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>>,>>>,>>9") + to_string(h_list.t_margin, " ->>>,>>9.99 ") + to_string(h_list.proz2, "->>9.9")
                add_sub()

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

    def create_sub(curr_grp:int):

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

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


            s_anzahl = 0
            s_proz1 =  to_decimal("0")
            st_sales =  to_decimal("0")
            st_cost =  to_decimal("0")
            st_margin =  to_decimal("0")
            st_proz2 =  to_decimal("0")


    def add_sub():

        nonlocal output_list2_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal subgr_list_list, output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)


    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    for output_list in query(output_list_list):
        fb_cost_analyst = Fb_cost_analyst()
        fb_cost_analyst_list.append(fb_cost_analyst)

        fb_cost_analyst.flag = output_list.flag
        fb_cost_analyst.bezeich = output_list.bezeich
        fb_cost_analyst.artnr = to_int(substring(output_list.s, 0, 5))
        fb_cost_analyst.qty = to_int(substring(output_list.s, 29, 6))
        fb_cost_analyst.proz1 = to_decimal(substring(output_list.s, 35, 6))
        fb_cost_analyst.epreis = to_decimal(substring(output_list.s, 41, 12))
        fb_cost_analyst.cost = to_decimal(substring(output_list.s, 53, 12))
        fb_cost_analyst.margin = to_decimal(substring(output_list.s, 65, 12))
        fb_cost_analyst.t_sales = to_decimal(substring(output_list.s, 77, 15))
        fb_cost_analyst.t_cost = to_decimal(substring(output_list.s, 92, 15))
        fb_cost_analyst.t_margin = to_decimal(substring(output_list.s, 107, 13))
        fb_cost_analyst.proz2 = to_decimal(substring(output_list.s, 120, 6))
        fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
        fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        gtotal_sold =  to_decimal(gtotal_sold) + to_decimal(fb_cost_analyst.qty)
        gtotal_sold_perc =  to_decimal(gtotal_sold_perc) + to_decimal(fb_cost_analyst.proz1)
        gtotal_cost =  to_decimal(gtotal_cost) + to_decimal(fb_cost_analyst.t_cost)
        gtotal_revenue =  to_decimal(gtotal_revenue) + to_decimal(fb_cost_analyst.t_sales)
        gtotal_profit =  to_decimal(gtotal_profit) + to_decimal(fb_cost_analyst.total_profit)

        if fb_cost_analyst.artnr != 0:
            count_foodcost =  to_decimal(count_foodcost) + to_decimal("1")
    avrg_item_profit =  to_decimal(gtotal_profit) / to_decimal(gtotal_sold)
    menu_pop_factor = ( to_decimal((1) / to_decimal(count_foodcost)) * to_decimal(0.8))

    for fb_cost_analyst in query(fb_cost_analyst_list):

        if fb_cost_analyst.item_profit < avrg_item_profit:
            fb_cost_analyst.profit_category = "LOW"
        else:
            fb_cost_analyst.profit_category = "HIGH"

        if fb_cost_analyst.proz1 < menu_pop_factor:
            fb_cost_analyst.popularity_category = "LOW"
        else:
            fb_cost_analyst.popularity_category = "HIGH"

        if profit_category.lower()  == ("LOW").lower()  and popularity_category.lower()  == ("LOW").lower() :
            fb_cost_analyst.menu_item_class = "DOG"

        elif profit_category.lower()  == ("LOW").lower()  and popularity_category.lower()  == ("HIGH").lower() :
            fb_cost_analyst.menu_item_class = "WORKHORSE"

        elif profit_category.lower()  == ("HIGH").lower()  and popularity_category.lower()  == ("LOW").lower() :
            fb_cost_analyst.menu_item_class = "CHALLENGE"

        elif profit_category.lower()  == ("HIGH").lower()  and popularity_category.lower()  == ("HIGH").lower() :
            fb_cost_analyst.menu_item_class = "STAR"

    for fb_cost_analyst in query(fb_cost_analyst_list):
        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.artnr = fb_cost_analyst.artnr
        output_list2.bezeich = to_string(fb_cost_analyst.bezeich)
        output_list2.anzahl = fb_cost_analyst.qty
        output_list2.proz1 =  to_decimal(fb_cost_analyst.proz1)
        output_list2.epreis =  to_decimal(fb_cost_analyst.epreis)
        output_list2.cost =  to_decimal(fb_cost_analyst.cost)
        output_list2.margin =  to_decimal(fb_cost_analyst.margin)
        output_list2.item_prof =  to_decimal(fb_cost_analyst.item_profit)
        output_list2.t_sales =  to_decimal(fb_cost_analyst.t_sales)
        output_list2.t_cost =  to_decimal(fb_cost_analyst.t_cost)
        output_list2.t_margin =  to_decimal(fb_cost_analyst.t_margin)
        output_list2.profit =  to_decimal(fb_cost_analyst.total_profit)
        output_list2.proz2 =  to_decimal(fb_cost_analyst.proz2)
        output_list2.profit_cat = to_string(fb_cost_analyst.profit_category)
        output_list2.popularity_cat = to_string(fb_cost_analyst.popularity_category)
        output_list2.menu_item_class = to_string(fb_cost_analyst.menu_item_class)

    for output_list2 in query(output_list2_list):

        if output_list2.artnr == 0 and output_list2.bezeich.lower()  != ("T o t a l").lower() :
            output_list2.artnr = 0
            output_list2.bezeich = output_list2.bezeich
            output_list2.anzahl = 0
            output_list2.proz1 =  to_decimal("0")
            output_list2.epreis =  to_decimal("0")
            output_list2.cost =  to_decimal("0")
            output_list2.margin =  to_decimal("0")
            output_list2.item_prof =  to_decimal("0")
            output_list2.t_sales =  to_decimal("0")
            output_list2.t_cost =  to_decimal("0")
            output_list2.t_margin =  to_decimal("0")
            output_list2.profit =  to_decimal("0")
            output_list2.proz2 =  to_decimal("0")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

        elif output_list2.bezeich.lower()  == ("T o t a l").lower() :
            output_list2.artnr = 0
            output_list2.bezeich = output_list2.bezeich
            output_list2.anzahl = output_list2.anzahl
            output_list2.proz1 =  to_decimal("100")
            output_list2.epreis =  to_decimal("0")
            output_list2.cost =  to_decimal("0")
            output_list2.margin =  to_decimal("0")
            output_list2.item_prof =  to_decimal("0")
            output_list2.t_sales =  to_decimal(output_list2.t_sales)
            output_list2.t_cost =  to_decimal(output_list2.t_cost)
            output_list2.t_margin =  to_decimal(output_list2.t_margin)
            output_list2.profit =  to_decimal("0")
            output_list2.proz2 =  to_decimal("100")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

        elif output_list2.bezeich == "":
            output_list2.artnr = 0
            output_list2.bezeich = to_string("")
            output_list2.anzahl = 0
            output_list2.proz1 =  to_decimal("0")
            output_list2.epreis =  to_decimal("0")
            output_list2.cost =  to_decimal("0")
            output_list2.margin =  to_decimal("0")
            output_list2.item_prof =  to_decimal("0")
            output_list2.t_sales =  to_decimal("0")
            output_list2.t_cost =  to_decimal("0")
            output_list2.t_margin =  to_decimal("0")
            output_list2.profit =  to_decimal("0")
            output_list2.proz2 =  to_decimal("0")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

    return generate_output()