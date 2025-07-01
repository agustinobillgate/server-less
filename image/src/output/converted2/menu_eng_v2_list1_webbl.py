#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import Htparam, H_artikel, Hoteldpt, Artikel, H_umsatz, H_journal, H_compli, Wgrpdep

subgr_list_list, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":string}, {"selected": True})
payload_list_list, Payload_list = create_model("Payload_list", {"include_compliment":bool, "compliment_only":bool})

def menu_eng_v2_list1_webbl(subgr_list_list:[Subgr_list], payload_list_list:[Payload_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:Decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):

    prepare_cache ([Htparam, H_artikel, Hoteldpt, Artikel, H_journal, H_compli, Wgrpdep])

    output_list2_list = []
    t_anz:int = 0
    t_anz_deb:int = 0
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
    price_type:int = 0
    htparam = h_artikel = hoteldpt = artikel = h_umsatz = h_journal = h_compli = wgrpdep = None

    subgr_list = payload_list = output_list = h_list = fb_cost_analyst = output_list2 = ph_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "bezeich":string, "s":string})
    h_list_list, H_list = create_model("H_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal})
    fb_cost_analyst_list, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":int, "bezeich":string, "qty":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal, "item_profit":Decimal, "total_profit":Decimal, "profit_category":string, "popularity_category":string, "menu_item_class":string})
    output_list2_list, Output_list2 = create_model("Output_list2", {"flag":string, "artnr":string, "dept":string, "bezeich":string, "zknr":string, "grpname":string, "anzahl":string, "proz1":string, "epreis":string, "cost":string, "margin":string, "item_prof":string, "t_sales":string, "t_cost":string, "t_margin":string, "profit":string, "proz2":string, "profit_cat":string, "popularity_cat":string, "menu_item_class":string, "s":string, "deb":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        return {"output-list2": output_list2_list}

    def create_h_umsatz1():

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
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
            dept = hoteldpt.num

            if payload_list.compliment_only or payload_list.include_compliment:

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

                        if not payload_list.compliment_only:

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

                                if vat_included:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                else:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                curr_recid = h_umsatz._recid
                                h_umsatz = db_session.query(H_umsatz).filter(
                                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")

                            if payload_list.include_compliment:

                                for h_compli in db_session.query(H_compli).filter(
                                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                    h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                    h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                    h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(h_compli.anzahl) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                    t_anz = t_anz + h_compli.anzahl
                                    t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)
                        else:

                            for h_compli in db_session.query(H_compli).filter(
                                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                h_list.cost =  to_decimal("0")
                                h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                                if h_list.cost != 0:
                                    pass
                                else:
                                    h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(h_compli.anzahl) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                t_anz = t_anz + h_compli.anzahl
                                t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)

                                if vat_included:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                else:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
                create_list(pos)
                t_anz = 0
                t_sales =  to_decimal("0")
                t_cost =  to_decimal("0")
            else:

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

                            if vat_included:
                                h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                            else:
                                h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

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

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
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
            dept = hoteldpt.num

            if payload_list.compliment_only or payload_list.include_compliment:

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

                        if not payload_list.compliment_only:

                            h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                            while None != h_umsatz:
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
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

                                if vat_included:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                else:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                curr_recid = h_umsatz._recid
                                h_umsatz = db_session.query(H_umsatz).filter(
                                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")

                            if payload_list.include_compliment:

                                for h_compli in db_session.query(H_compli).filter(
                                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                    h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                    h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                    h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(h_compli.anzahl) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                    t_anz = t_anz + h_compli.anzahl
                                    t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)
                        else:

                            for h_compli in db_session.query(H_compli).filter(
                                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                vat =  to_decimal(vat) + to_decimal(vat)
                                h_list.cost =  to_decimal("0")


                                h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                                if h_list.cost != 0:
                                    pass
                                else:
                                    h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(h_compli.anzahl) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                t_anz = t_anz + h_compli.anzahl
                                t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)

                                if vat_included:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                else:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
                create_list(pos)
                t_anz = 0
                t_sales =  to_decimal("0")
                t_cost =  to_decimal("0")
            else:

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
                            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
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

                            if vat_included:
                                h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                            else:
                                h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

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

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
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
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            if payload_list.compliment_only or payload_list.include_compliment:

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

                        if not payload_list.compliment_only:

                            h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                            while None != h_umsatz:
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
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

                                if vat_included:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                else:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                curr_recid = h_umsatz._recid
                                h_umsatz = db_session.query(H_umsatz).filter(
                                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")

                            if payload_list.include_compliment:

                                for h_compli in db_session.query(H_compli).filter(
                                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                    h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                    h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                    h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(h_compli.anzahl) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                    t_anz = t_anz + h_compli.anzahl
                                    t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)
                        else:

                            for h_compli in db_session.query(H_compli).filter(
                                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                h_list.cost =  to_decimal("0")
                                h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                                if h_list.cost != 0:
                                    pass
                                else:
                                    h_list.cost =  to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(h_compli.anzahl) * to_decimal(h_artikel.epreis1) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(exchg_rate)
                                t_anz = t_anz + h_compli.anzahl
                                t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)

                                if vat_included:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                else:
                                    h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
                create_list(pos)
                t_anz = 0
                t_sales =  to_decimal("0")
                t_cost =  to_decimal("0")
            else:

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
                            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
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

                            if vat_included:
                                h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                            else:
                                h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

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

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        h_list_artnr:string = ""
        h_list_anzahl:string = ""
        h_list_proz1:string = ""
        h_list_epreis:string = ""
        h_list_cost:string = ""
        h_list_margin:string = ""
        h_list_t_sales:string = ""
        h_list_t_cost:string = ""
        h_list_t_margin:string = ""
        h_list_proz2:string = ""
        h_list_epreis_non_short_flag:string = ""
        h_list_cost_non_short_flag:string = ""
        h_list_t_sales_non_short_flag:string = ""
        h_list_t_cost_non_short_flag:string = ""
        t_anz_tot:string = ""
        hundred_tot:string = ""
        t_sales_tot:string = ""
        t_cost_tot:string = ""
        t_margin_tot:string = ""
        t_sales_tot_non_short_flag:string = ""
        t_cost_tot_non_short_flag:string = ""

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
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")


        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            t_anz_tot = to_string(t_anz, "->>>>9")
            hundred_tot = to_string(100, "->>9.99")
            t_sales_tot = to_string(t_sales, "->,>>>,>>>,>>9.99")
            t_cost_tot = to_string(t_cost, "->,>>>,>>>,>>9.99")
            t_margin_tot = to_string(t_margin, "->,>>>,>>9.99")
            t_sales_tot_non_short_flag = to_string(t_sales, " ->>>,>>>,>>>,>>9")
            t_cost_tot_non_short_flag = to_string(t_cost, " ->>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.bezeich = "T o t a l"

            if short_flag:
                output_list.s = to_string(" ", "x(9)") + to_string(t_anz_tot, "x(6)") + to_string(hundred_tot, "x(7)") + to_string("", "x(47)") + to_string(t_sales_tot, "x(17)") + to_string(t_cost_tot, "x(17)") + to_string(t_margin_tot, "x(13)") + to_string(hundred_tot, "x(7)")
            else:
                output_list.s = to_string(" ", "x(5)") + to_string(t_anz_tot, "x(6)") + to_string(hundred_tot, "x(7)") + to_string("", "x(47)") + to_string(t_sales_tot_non_short_flag, "x(17)") + to_string(t_cost_tot_non_short_flag, "x(17)") + to_string(t_margin_tot, "x(13)") + to_string(hundred_tot, "x(7)")
            output_list = Output_list()
            output_list_list.append(output_list)

    def create_list1(pos:bool):

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        curr_grp:int = 0
        h_list_artnr:string = ""
        h_list_anzahl:string = ""
        h_list_proz1:string = ""
        h_list_epreis:string = ""
        h_list_cost:string = ""
        h_list_margin:string = ""
        h_list_t_sales:string = ""
        h_list_t_cost:string = ""
        h_list_t_margin:string = ""
        h_list_proz2:string = ""
        h_list_epreis_non_short_flag:string = ""
        h_list_cost_non_short_flag:string = ""
        h_list_t_sales_non_short_flag:string = ""
        h_list_t_cost_non_short_flag:string = ""
        t_anz_tot:string = ""
        hundred_tot:string = ""
        t_sales_tot:string = ""
        t_cost_tot:string = ""
        t_margin_tot:string = ""
        t_sales_tot_non_short_flag:string = ""
        t_cost_tot_non_short_flag:string = ""
        wgrpdep_bezeich:string = ""

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                add_sub()


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})

                    if wgrpdep:
                        wgrpdep_bezeich = wgrpdep.bezeich
                    else:
                        wgrpdep_bezeich = ""
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.bezeich = to_string(wgrpdep_bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                add_sub()


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                add_sub()


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.s = " " + to_string(wgrpdep.bezeich, "x(24)")
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                add_sub()


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                add_sub()


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.flag = 1
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                h_list_artnr = to_string(h_list.artnr, ">>>>>>>>9")
                h_list_anzahl = to_string(h_list.anzahl, "->>>>9")
                h_list_proz1 = to_string(h_list.proz1, "->>9.99")
                h_list_epreis = to_string(h_list.epreis, "->,>>>,>>>,>>9.99")
                h_list_cost = to_string(h_list.cost, "->,>>>,>>>,>>9.99")
                h_list_margin = to_string(h_list.margin, "->,>>>,>>9.99")
                h_list_t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9.99")
                h_list_t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9.99")
                h_list_t_margin = to_string(h_list.t_margin, "->,>>>,>>9.99")
                h_list_proz2 = to_string(h_list.proz2, "->>9.99")
                h_list_epreis_non_short_flag = to_string(h_list.epreis, " ->>>,>>>,>>>,>>9")
                h_list_cost_non_short_flag = to_string(h_list.cost, " ->>>,>>>,>>>,>>9")
                h_list_t_sales_non_short_flag = to_string(h_list.t_sales, " ->>>,>>>,>>>,>>9")
                h_list_t_cost_non_short_flag = to_string(h_list.t_cost, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bezeich = h_list.bezeich

                if short_flag:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis, "x(17)") + to_string(h_list_cost, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales, "x(17)") + to_string(h_list_t_cost, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                else:
                    output_list.s = to_string(h_list_artnr, "x(9)") + to_string(h_list_anzahl, "x(6)") + to_string(h_list_proz1, "x(7)") + to_string(h_list_epreis_non_short_flag, "x(17)") + to_string(h_list_cost_non_short_flag, "x(17)") + to_string(h_list_margin, "x(13)") + to_string(h_list_t_sales_non_short_flag, "x(17)") + to_string(h_list_t_cost_non_short_flag, "x(17)") + to_string(h_list_t_margin, "x(13)") + to_string(h_list_proz2, "x(7)")
                add_sub()

        create_sub(curr_grp)

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            t_anz_tot = to_string(t_anz, "->>>>9")
            hundred_tot = to_string(100, "->>9.99")
            t_sales_tot = to_string(t_sales, "->,>>>,>>>,>>9.99")
            t_cost_tot = to_string(t_cost, "->,>>>,>>>,>>9.99")
            t_margin_tot = to_string(t_margin, "->,>>>,>>9.99")
            t_sales_tot_non_short_flag = to_string(t_sales, " ->>>,>>>,>>>,>>9")
            t_cost_tot_non_short_flag = to_string(t_cost, " ->>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.bezeich = "T o t a l"

            if short_flag:
                output_list.s = to_string(" ", "x(9)") + to_string(t_anz_tot, "x(6)") + to_string(hundred_tot, "x(7)") + to_string("", "x(47)") + to_string(t_sales_tot, "x(17)") + to_string(t_cost_tot, "x(17)") + to_string(t_margin_tot, "x(13)") + to_string(hundred_tot, "x(7)")
            else:
                output_list.s = to_string(" ", "x(5)") + to_string(t_anz_tot, "x(6)") + to_string(hundred_tot, "x(7)") + to_string("", "x(47)") + to_string(t_sales_tot_non_short_flag, "x(17)") + to_string(t_cost_tot_non_short_flag, "x(17)") + to_string(t_margin_tot, "x(13)") + to_string(hundred_tot, "x(7)")
            output_list = Output_list()
            output_list_list.append(output_list)

    def create_sub(curr_grp:int):

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list

        s_anzahl_sub_tot:string = ""
        s_proz1_sub_tot:string = ""
        st_sales_sub_tot:string = ""
        st_cost_sub_tot:string = ""
        st_margin_sub_tot:string = ""
        st_proz2_sub_tot:string = ""
        st_sales_sub_tot_non_short_flag:string = ""
        st_cost_sub_tot_non_short_flag:string = ""

        if curr_grp != 0:

            if st_sales != 0:
                st_margin =  to_decimal(st_cost) / to_decimal(st_sales) * to_decimal("100")
            s_anzahl_sub_tot = to_string(s_anzahl, "->>>>9")
            s_proz1_sub_tot = to_string(s_proz1, "->>9.99")
            st_sales_sub_tot = to_string(st_sales, "->,>>>,>>>,>>9.99")
            st_cost_sub_tot = to_string(st_cost, "->,>>>,>>>,>>9.99")
            st_margin_sub_tot = to_string(st_margin, "->,>>>,>>9.99")
            st_proz2_sub_tot = to_string(st_proz2, "->>9.9")
            st_sales_sub_tot_non_short_flag = to_string(st_sales, " ->>>,>>>,>>>,>>9")
            st_cost_sub_tot_non_short_flag = to_string(st_cost, " ->>>,>>>,>>>,>>9")
            output_list = Output_list()
            output_list_list.append(output_list)


            if short_flag:
                output_list.flag = 2
                output_list.bezeich = "S u b T o t a l"
                output_list.s = to_string(" ", "x(9)") +\
                        to_string(s_anzahl_sub_tot, "x(6)") +\
                        to_string(s_proz1_sub_tot, "x(7)") +\
                        to_string(" ", "x(47)") +\
                        to_string(st_sales_sub_tot, "x(17)") +\
                        to_string(st_cost_sub_tot, "x(17)") +\
                        to_string(st_margin_sub_tot, "x(13)") +\
                        to_string(st_proz2_sub_tot, "x(6)")


            else:
                output_list.flag = 2
                output_list.bezeich = "S u b T o t a l"
                output_list.s = to_string(" ", "x(9)") +\
                        to_string(s_anzahl_sub_tot, "x(6)") +\
                        to_string(s_proz1_sub_tot, "x(7)") +\
                        to_string(" ", "x(47)") +\
                        to_string(st_sales_sub_tot_non_short_flag, "x(17)") +\
                        to_string(st_cost_sub_tot_non_short_flag, "x(17)") +\
                        to_string(st_margin_sub_tot, "x(13)") +\
                        to_string(st_proz2_sub_tot, "x(6)")


            s_anzahl = 0
            s_proz1 =  to_decimal("0")
            st_sales =  to_decimal("0")
            st_cost =  to_decimal("0")
            st_margin =  to_decimal("0")
            st_proz2 =  to_decimal("0")


    def add_sub():

        nonlocal output_list2_list, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, price_type, htparam, h_artikel, hoteldpt, artikel, h_umsatz, h_journal, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_list, h_list_list, fb_cost_analyst_list, output_list2_list


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    payload_list = query(payload_list_list, first=True)

    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    elif sorttype == 3:
        create_h_umsatz3()

    for output_list in query(output_list_list):
        fb_cost_analyst = Fb_cost_analyst()
        fb_cost_analyst_list.append(fb_cost_analyst)

        fb_cost_analyst.flag = output_list.flag
        fb_cost_analyst.bezeich = output_list.bezeich
        fb_cost_analyst.artnr = to_int(substring(output_list.s, 0, 9))
        fb_cost_analyst.qty = to_int(substring(output_list.s, 9, 6))
        fb_cost_analyst.proz1 = to_decimal(substring(output_list.s, 15, 7))
        fb_cost_analyst.epreis = to_decimal(substring(output_list.s, 22, 17))
        fb_cost_analyst.cost = to_decimal(substring(output_list.s, 39, 17))
        fb_cost_analyst.margin = to_decimal(substring(output_list.s, 56, 13))
        fb_cost_analyst.t_sales = to_decimal(substring(output_list.s, 69, 17))
        fb_cost_analyst.t_cost = to_decimal(substring(output_list.s, 86, 17))
        fb_cost_analyst.t_margin = to_decimal(substring(output_list.s, 103, 13))
        fb_cost_analyst.proz2 = to_decimal(substring(output_list.s, 116, 7))
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

        if fb_cost_analyst.profit_category.lower()  == ("LOW").lower()  and fb_cost_analyst.popularity_category.lower()  == ("LOW").lower() :
            fb_cost_analyst.menu_item_class = "DOG"

        elif fb_cost_analyst.profit_category.lower()  == ("LOW").lower()  and fb_cost_analyst.popularity_category.lower()  == ("HIGH").lower() :
            fb_cost_analyst.menu_item_class = "WORKHORSE"

        elif fb_cost_analyst.profit_category.lower()  == ("HIGH").lower()  and fb_cost_analyst.popularity_category.lower()  == ("LOW").lower() :
            fb_cost_analyst.menu_item_class = "CHALLENGE"

        elif fb_cost_analyst.profit_category.lower()  == ("HIGH").lower()  and fb_cost_analyst.popularity_category.lower()  == ("HIGH").lower() :
            fb_cost_analyst.menu_item_class = "STAR"

    for fb_cost_analyst in query(fb_cost_analyst_list):
        output_list2 = Output_list2()
        output_list2_list.append(output_list2)

        output_list2.artnr = to_string(fb_cost_analyst.artnr , ">>>>>>>>9")
        output_list2.bezeich = to_string(fb_cost_analyst.bezeich)
        output_list2.anzahl = to_string(fb_cost_analyst.qty , "->>>>9")
        output_list2.proz1 = to_string(fb_cost_analyst.proz1 , "->>9.99")
        output_list2.epreis = to_string(fb_cost_analyst.epreis , "->,>>>,>>>,>>9.99")
        output_list2.cost = to_string(fb_cost_analyst.cost , "->,>>>,>>>,>>9.99")
        output_list2.margin = to_string(fb_cost_analyst.margin , "->,>>>,>>9.99")
        output_list2.item_prof = to_string(fb_cost_analyst.item_profit , "->,>>>,>>>,>>9.99")
        output_list2.t_sales = to_string(fb_cost_analyst.t_sales , "->,>>>,>>>,>>9.99")
        output_list2.t_cost = to_string(fb_cost_analyst.t_cost , "->,>>>,>>>,>>9.99")
        output_list2.t_margin = to_string(fb_cost_analyst.t_margin , "->,>>>,>>9.99")
        output_list2.profit = to_string(fb_cost_analyst.total_profit , "->,>>>,>>>,>>9.99")
        output_list2.proz2 = to_string(fb_cost_analyst.proz2 , "->>9.99")
        output_list2.profit_cat = to_string(fb_cost_analyst.profit_category)
        output_list2.popularity_cat = to_string(fb_cost_analyst.popularity_category)
        output_list2.menu_item_class = to_string(fb_cost_analyst.menu_item_class)

    for output_list2 in query(output_list2_list):

        if trim (output_list2.artnr) == ("0").lower()  and output_list2.bezeich.lower()  != ("T o t a l").lower() :
            output_list2.artnr = to_string("")
            output_list2.bezeich = output_list2.bezeich
            output_list2.anzahl = to_string("")
            output_list2.proz1 = to_string("")
            output_list2.epreis = to_string("")
            output_list2.cost = to_string("")
            output_list2.margin = to_string("")
            output_list2.item_prof = to_string("")
            output_list2.t_sales = to_string("")
            output_list2.t_cost = to_string("")
            output_list2.t_margin = to_string("")
            output_list2.profit = to_string("")
            output_list2.proz2 = to_string("")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

        elif output_list2.bezeich.lower()  == ("T o t a l").lower() :
            output_list2.artnr = to_string("")
            output_list2.bezeich = output_list2.bezeich
            output_list2.anzahl = output_list2.anzahl
            output_list2.proz1 = to_string(100, "->>9.99")
            output_list2.epreis = to_string("")
            output_list2.cost = to_string("")
            output_list2.margin = to_string("")
            output_list2.item_prof = to_string("")
            output_list2.t_sales = output_list2.t_sales
            output_list2.t_cost = output_list2.t_cost
            output_list2.t_margin = output_list2.t_margin
            output_list2.profit = to_string("")
            output_list2.proz2 = to_string(100, "->>9.99")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

        elif output_list2.bezeich == "":
            output_list2.artnr = to_string("")
            output_list2.bezeich = to_string("")
            output_list2.anzahl = to_string("")
            output_list2.proz1 = to_string("")
            output_list2.epreis = to_string("")
            output_list2.cost = to_string("")
            output_list2.margin = to_string("")
            output_list2.item_prof = to_string("")
            output_list2.t_sales = to_string("")
            output_list2.t_cost = to_string("")
            output_list2.t_margin = to_string("")
            output_list2.profit = to_string("")
            output_list2.proz2 = to_string("")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

    return generate_output()