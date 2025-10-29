#using conversion tools version: 1.0.0.117

#===================================================================
#Rulita, 27/28/2025
#From fb_cost_analyst.qty = to_int(substring(output_list.s, 9, 6))
#TO fb_cost_analyst.qty = to_decimal(substring(output_list.s, 9, 6))
#added safe devide 
#===================================================================

#------------------------------------------
# Rd, 28/8/2025
# safe_divide, reslin -> reslin_queasy
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import Htparam, Waehrung, H_artikel, Hoteldpt, Artikel, H_menu, H_mjourn, L_artikel, H_rezept, H_umsatz, H_cost, H_compli, Wgrpdep

subgr_list_data, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":string}, {"selected": True})
payload_list_data, Payload_list = create_model("Payload_list", {"include_compliment":bool, "compliment_only":bool, "include_package":bool, "package_only":bool})

def safe_divide(numerator, denominator):
    numerator, denominator = to_decimal(numerator), to_decimal(denominator)
    return (numerator / denominator) if denominator not in (0, None) else to_decimal("0")

def menu_eng_v2_list1_webbl(subgr_list_data:[Subgr_list], payload_list_data:[Payload_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:Decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):

    prepare_cache ([Htparam, Waehrung, H_artikel, Hoteldpt, Artikel, H_mjourn, L_artikel, H_rezept, H_cost, H_compli, Wgrpdep])

    output_list2_data = []
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
    double_currency:bool = False
    incl_service:bool = False
    incl_mwst:bool = False
    exrate:Decimal = 1
    bill_date:date = None
    food_disc:int = 0
    bev_disc:int = 0
    other_disc:int = 0
    price_type:int = 0
    htparam = waehrung = h_artikel = hoteldpt = artikel = h_menu = h_mjourn = l_artikel = h_rezept = h_umsatz = h_cost = h_compli = wgrpdep = None

    subgr_list = payload_list = output_list = h_list = fb_cost_analyst = output_list2 = ph_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":int, "bezeich":string, "s":string})
    h_list_data, H_list = create_model("H_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal, "sub_menu_qty":[int,15], "sub_menu_bezeich":[string,15], "isparent":bool})
    fb_cost_analyst_data, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":int, "bezeich":string, "qty":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal, "item_profit":Decimal, "total_profit":Decimal, "profit_category":string, "popularity_category":string, "menu_item_class":string, "dept":int})
    output_list2_data, Output_list2 = create_model("Output_list2", {"flag":string, "artnr":string, "dept":string, "bezeich":string, "zknr":string, "grpname":string, "anzahl":string, "proz1":string, "epreis":string, "cost":string, "margin":string, "item_prof":string, "t_sales":string, "t_cost":string, "t_margin":string, "profit":string, "proz2":string, "profit_cat":string, "popularity_cat":string, "menu_item_class":string, "s":string, "deb":Decimal, "isparent":bool, "sub_menu_qty":[int,15], "sub_menu_bezeich":[string,15]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

        return {"output-list2": output_list2_data}

    def create_h_umsatz1():

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

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
        cost_todate:Decimal = to_decimal("0.0")
        cost_compli:Decimal = to_decimal("0.0")
        cost_open_price:Decimal = to_decimal("0.0")
        t_cost_open_price:Decimal = to_decimal("0.0")
        cost_sales_compli:Decimal = to_decimal("0.0")
        price:Decimal = to_decimal("0.0")
        tmp_anzahl:int = 0
        isparent:bool = False
        curr_date:date = None
        i:int = 0
        h_art = None
        h_artikel_buff = None
        H_art =  create_buffer("H_art",H_artikel)
        Ph_list = H_list
        ph_list_data = h_list_data
        H_artikel_buff =  create_buffer("H_artikel_buff",H_artikel)
        output_list_data.clear()
        h_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99") + " " + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            if payload_list.compliment_only or payload_list.include_compliment:

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.bezeich, h_artikel.betriebsnr, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.bezeich, H_artikel.betriebsnr, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) & (Artikel.endkum != disc_nr)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    do_it = False

                    if all_sub:
                        do_it = True
                    else:

                        subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                        do_it = None != subgr_list

                    if do_it:

                        if payload_list.package_only:

                            if h_artikel.betriebsnr == 0:
                                continue
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.cost =  to_decimal("0")
                        h_list.artnr = h_artikel.artnr
                        h_list.dept = h_artikel.departement
                        h_list.bezeich = h_artikel.bezeich
                        h_list.zknr = h_artikel.zwkum
                        isparent = False

                        if (payload_list.include_package or payload_list.package_only) and h_artikel.betriebsnr > 0:
                            i = 0

                            h_menu_obj_list = {}
                            for h_menu, h_artikel_buff in db_session.query(H_menu, H_artikel_buff).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr)).filter(
                                     (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
                                if h_menu_obj_list.get(h_menu._recid):
                                    continue
                                else:
                                    h_menu_obj_list[h_menu._recid] = True


                                i = i + 1
                                h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                            i = 0
                            for curr_date in date_range(from_date,to_date) :

                                h_mjourn_obj_list = {}
                                h_mjourn = H_mjourn()
                                h_artikel_buff = H_artikel()
                                for h_mjourn.anzahl, h_mjourn._recid, h_artikel_buff.zwkum, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff.bezeich, h_artikel_buff.betriebsnr, h_artikel_buff.epreis1, h_artikel_buff.artnrlager, h_artikel_buff.artnrrezept, h_artikel_buff.prozent, h_artikel_buff.artnrfront, h_artikel_buff._recid in db_session.query(H_mjourn.anzahl, H_mjourn._recid, H_artikel_buff.zwkum, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff.bezeich, H_artikel_buff.betriebsnr, H_artikel_buff.epreis1, H_artikel_buff.artnrlager, H_artikel_buff.artnrrezept, H_artikel_buff.prozent, H_artikel_buff.artnrfront, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr)).filter(
                                         (H_mjourn.departement == h_artikel.departement) & (H_mjourn.h_artnr == h_artikel.artnr) & (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.bill_datum >= curr_date) & (H_mjourn.bill_datum <= curr_date)).order_by(H_mjourn._recid).all():
                                    if h_mjourn_obj_list.get(h_mjourn._recid):
                                        continue
                                    else:
                                        h_mjourn_obj_list[h_mjourn._recid] = True


                                    for i in range(1,15 + 1) :

                                        if h_list.sub_menu_bezeich[i - 1] == h_artikel_buff.bezeich and h_list.sub_menu_bezeich[i - 1] != "":
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break

                                        elif h_list.sub_menu_bezeich[i - 1] == "" and h_artikel_buff.bezeich != "":
                                            h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break
                                    isparent = True

                        if isparent:
                            h_list.isparent = True

                        if vat_included:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                        else:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)

                        if h_artikel.artnrlager != 0:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                            if l_artikel:

                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    h_list.cost =  to_decimal(l_artikel.vk_preis)
                                else:
                                    h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                        elif h_artikel.artnrrezept != 0:

                            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                            if h_rezept:
                                cost_todate =  to_decimal("0")
                                cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                h_list.cost =  to_decimal(cost_todate)
                        else:
                            price =  to_decimal(h_artikel.epreis1)

                            if price != 0:
                                price = calculate_price(price)

                            if price == None:
                                price =  to_decimal("0")
                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                        h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                        h_list.cost = to_decimal(round(h_list.cost , 2))

                        if not payload_list.compliment_only:

                            h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                            while None != h_umsatz:
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                anz = h_umsatz.anzahl
                                cost =  to_decimal("0")
                                h_list.cost =  to_decimal("0")

                                h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                                if h_cost and h_cost.betrag != 0:
                                    cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                    h_list.cost =  to_decimal(h_cost.betrag)
                                else:

                                    if h_artikel.artnrlager != 0:

                                        l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                                        if l_artikel:

                                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                                h_list.cost =  to_decimal(l_artikel.vk_preis)
                                            else:
                                                h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                                    elif h_artikel.artnrrezept != 0:

                                        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                        if h_rezept:
                                            cost_todate =  to_decimal("0")
                                            cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                            h_list.cost =  to_decimal(cost_todate)
                                    else:

                                        if h_artikel.epreis1 != 0:
                                            price =  to_decimal(h_artikel.epreis1)

                                            if price != 0:
                                                price = calculate_price(price)

                                            if price == None:
                                                price =  to_decimal("0")
                                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                                    cost =  to_decimal(anz) * to_decimal(h_list.cost)
                                cost =  to_decimal(cost) / to_decimal(fact1)
                                cost = to_decimal(round(cost , 2))
                                h_list.anzahl = h_list.anzahl + anz
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                                t_cost =  to_decimal(t_cost) + to_decimal(cost)
                                t_anz = t_anz + anz
                                t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                                if h_list.anzahl != 0 and h_list.anzahl != None:
                                    tmp_anzahl = h_list.anzahl
                                else:
                                    tmp_anzahl = 0

                                #Rulita added safe devide
                                if vat_included and tmp_anzahl != 0:
                                    # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                    h_list.epreis = ( safe_divide(to_decimal(h_list.t_sales) , to_decimal(tmp_anzahl))) * to_decimal(exchg_rate) / to_decimal(fact)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                                elif tmp_anzahl != 0:
                                    h_list.epreis = ( safe_divide(to_decimal(h_list.t_sales) , to_decimal(tmp_anzahl))) * to_decimal(exchg_rate) / to_decimal(fact1)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                else:
                                    h_list.epreis =  to_decimal("0")
                                    h_list.cost =  to_decimal("0")

                                curr_recid = h_umsatz._recid
                                h_umsatz = db_session.query(H_umsatz).filter(
                                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")

                            if payload_list.include_compliment:
                                cost_open_price =  to_decimal("0")
                                cost_sales_compli =  to_decimal("0")

                                for h_compli in db_session.query(H_compli).filter(
                                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                    h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                    h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)

                                    cost_sales_compli =  to_decimal(cost_sales_compli) + to_decimal(h_compli.epreis)
                                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                    vat =  to_decimal(vat) + to_decimal(vat2)


                                    cost =  to_decimal("0")
                                    cost_compli =  to_decimal("0")

                                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                                    if h_cost and h_cost.betrag != 0:
                                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                                    else:

                                        if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                                            cost_compli =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(h_compli.epreis) * to_decimal(exchg_rate)
                                            cost =  to_decimal(h_compli.anzahl) * to_decimal(cost_compli)

                                    if h_artikel.epreis1 != 0:
                                        cost =  to_decimal(cost) / to_decimal(fact1)
                                        cost = to_decimal(round(cost , 2))
                                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)

                                    if h_list.anzahl != 0 and h_list.anzahl != None:
                                        tmp_anzahl = h_list.anzahl
                                    else:
                                        tmp_anzahl = 0

                                    if vat_included and tmp_anzahl != 0:
                                        h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                        if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                            if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                                h_list.cost =  to_decimal("0")
                                                h_list.t_cost =  to_decimal("0")
                                                cost_open_price =  to_decimal("0")
                                            else:
                                                h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                cost_open_price =  to_decimal(cost_sales_compli) * to_decimal(h_artikel.prozent) / to_decimal("100")

                                    elif tmp_anzahl != 0:
                                        h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                        if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                            if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                                h_list.cost =  to_decimal("0")
                                                h_list.t_cost =  to_decimal("0")
                                                cost_open_price =  to_decimal("0")
                                            else:
                                                h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                cost_open_price =  to_decimal(cost_sales_compli) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                    else:
                                        h_list.epreis =  to_decimal("0")
                                        h_list.cost =  to_decimal("0")
                                    t_anz = t_anz + h_compli.anzahl
                                    t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)
                                t_cost =  to_decimal(t_cost) + to_decimal(cost_open_price)
                        else:

                            for h_compli in db_session.query(H_compli).filter(
                                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                cost =  to_decimal("0")
                                cost_compli =  to_decimal("0")

                                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                                if h_cost and h_cost.betrag != 0:
                                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                                else:

                                    if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                                        cost_compli =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(h_compli.epreis) * to_decimal(exchg_rate)
                                        cost =  to_decimal(h_compli.anzahl) * to_decimal(cost_compli)
                                cost =  to_decimal(cost) / to_decimal(fact1)
                                cost = to_decimal(round(cost , 2))
                                h_list.cost =  to_decimal(cost)
                                h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                                t_anz = t_anz + h_compli.anzahl
                                t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)

                                if h_list.anzahl != 0 and h_list.anzahl != None:
                                    tmp_anzahl = h_list.anzahl

                                if vat_included and tmp_anzahl != 0:
                                    # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                elif tmp_anzahl != 0:
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                else:
                                    h_list.epreis =  to_decimal("0")
                                    h_list.cost =  to_decimal("0")

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
                                t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                create_list(pos)
                t_anz = 0
                t_sales =  to_decimal("0")
                t_cost =  to_decimal("0")
            else:

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.bezeich, h_artikel.betriebsnr, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.bezeich, H_artikel.betriebsnr, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) & (Artikel.endkum != disc_nr)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    do_it = False

                    if all_sub:
                        do_it = True
                    else:

                        subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                        do_it = None != subgr_list

                    if do_it:

                        if payload_list.package_only:

                            if h_artikel.betriebsnr == 0:
                                continue
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.cost =  to_decimal("0")
                        h_list.dept = h_artikel.departement
                        h_list.artnr = h_artikel.artnr
                        h_list.dept = h_artikel.departement
                        h_list.bezeich = h_artikel.bezeich
                        h_list.zknr = h_artikel.zwkum

                        if vat_included:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                        else:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)
                        isparent = False

                        if (payload_list.include_package or payload_list.package_only) and h_artikel.betriebsnr > 0:
                            i = 0

                            h_menu_obj_list = {}
                            for h_menu, h_artikel_buff in db_session.query(H_menu, H_artikel_buff).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr)).filter(
                                     (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
                                if h_menu_obj_list.get(h_menu._recid):
                                    continue
                                else:
                                    h_menu_obj_list[h_menu._recid] = True


                                i = i + 1
                                h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                            i = 0
                            for curr_date in date_range(from_date,to_date) :

                                h_mjourn_obj_list = {}
                                h_mjourn = H_mjourn()
                                h_artikel_buff = H_artikel()
                                for h_mjourn.anzahl, h_mjourn._recid, h_artikel_buff.zwkum, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff.bezeich, h_artikel_buff.betriebsnr, h_artikel_buff.epreis1, h_artikel_buff.artnrlager, h_artikel_buff.artnrrezept, h_artikel_buff.prozent, h_artikel_buff.artnrfront, h_artikel_buff._recid in db_session.query(H_mjourn.anzahl, H_mjourn._recid, H_artikel_buff.zwkum, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff.bezeich, H_artikel_buff.betriebsnr, H_artikel_buff.epreis1, H_artikel_buff.artnrlager, H_artikel_buff.artnrrezept, H_artikel_buff.prozent, H_artikel_buff.artnrfront, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr)).filter(
                                         (H_mjourn.departement == h_artikel.departement) & (H_mjourn.h_artnr == h_artikel.artnr) & (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.bill_datum >= curr_date) & (H_mjourn.bill_datum <= curr_date)).order_by(H_mjourn._recid).all():
                                    if h_mjourn_obj_list.get(h_mjourn._recid):
                                        continue
                                    else:
                                        h_mjourn_obj_list[h_mjourn._recid] = True


                                    for i in range(1,15 + 1) :

                                        if h_list.sub_menu_bezeich[i - 1] == h_artikel_buff.bezeich and h_list.sub_menu_bezeich[i - 1] != "":
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break

                                        elif h_list.sub_menu_bezeich[i - 1] == "" and h_artikel_buff.bezeich != "":
                                            h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break
                                    isparent = True

                        if isparent:
                            h_list.isparent = True

                        if h_artikel.artnrlager != 0:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                            if l_artikel:

                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    h_list.cost =  to_decimal(l_artikel.vk_preis)
                                else:
                                    h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                        elif h_artikel.artnrrezept != 0:

                            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                            if h_rezept:
                                cost_todate =  to_decimal("0")
                                cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                h_list.cost =  to_decimal(cost_todate)
                        else:
                            price =  to_decimal(h_artikel.epreis1)

                            if price != 0:
                                price = calculate_price(price)

                            if price == None:
                                price =  to_decimal("0")
                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                        h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                        h_list.cost = to_decimal(round(h_list.cost , 2))

                        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                        while None != h_umsatz:
                            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                            vat =  to_decimal(vat) + to_decimal(vat2)


                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")
                            h_list.cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                if h_artikel.artnrlager != 0:

                                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                                    if l_artikel:

                                        if price_type == 0 or l_artikel.ek_aktuell == 0:
                                            h_list.cost =  to_decimal(l_artikel.vk_preis)
                                        else:
                                            h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                                elif h_artikel.artnrrezept != 0:

                                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                    if h_rezept:
                                        cost_todate =  to_decimal("0")
                                        cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                        h_list.cost =  to_decimal(cost_todate)
                                else:

                                    if h_artikel.epreis1 != 0:
                                        price =  to_decimal(h_artikel.epreis1)

                                        if price != 0:
                                            price = calculate_price(price)

                                        if price == None:
                                            price =  to_decimal("0")
                                        h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                                cost =  to_decimal(anz) * to_decimal(h_list.cost)
                            cost =  to_decimal(cost) / to_decimal(fact1)
                            cost = to_decimal(round(cost , 2))
                            h_list.anzahl = h_list.anzahl + anz
                            h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                            h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                            t_cost =  to_decimal(t_cost) + to_decimal(cost)
                            t_anz = t_anz + anz
                            t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                            if h_list.anzahl != 0 and h_list.anzahl != None:
                                tmp_anzahl = h_list.anzahl
                            else:
                                tmp_anzahl = 0

                            if vat_included and tmp_anzahl != 0:
                                # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                    if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                        h_list.cost =  to_decimal("0")
                                        h_list.t_cost =  to_decimal("0")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                    else:
                                        h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                            elif tmp_anzahl != 0:
                                h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                    if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                        h_list.cost =  to_decimal("0")
                                        h_list.t_cost =  to_decimal("0")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                    else:
                                        h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                            else:
                                h_list.epreis =  to_decimal("0")
                                h_list.cost =  to_decimal("0")

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

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

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
        cost_todate:Decimal = to_decimal("0.0")
        cost_compli:Decimal = to_decimal("0.0")
        cost_open_price:Decimal = to_decimal("0.0")
        cost_sales_compli:Decimal = to_decimal("0.0")
        price:Decimal = to_decimal("0.0")
        tmp_anzahl:int = 0
        isparent:bool = False
        curr_date:date = None
        i:int = 0
        h_art = None
        h_artikel_buff = None
        H_art =  create_buffer("H_art",H_artikel)
        H_artikel_buff =  create_buffer("H_artikel_buff",H_artikel)
        output_list_data.clear()
        h_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != dstore) & (Hoteldpt.num != ldry_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            if payload_list.compliment_only or payload_list.include_compliment:

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.bezeich, h_artikel.betriebsnr, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.bezeich, H_artikel.betriebsnr, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 6) & (Artikel.endkum != disc_nr)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    do_it = False

                    if all_sub:
                        do_it = True 
                    else:

                        subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                        do_it = None != subgr_list

                    if do_it:

                        if payload_list.package_only:

                            if h_artikel.betriebsnr == 0:
                                continue
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.cost =  to_decimal("0")
                        h_list.dept = h_artikel.departement
                        h_list.artnr = h_artikel.artnr
                        h_list.dept = h_artikel.departement
                        h_list.bezeich = h_artikel.bezeich
                        h_list.zknr = h_artikel.zwkum

                        if vat_included:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                        else:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)
                        isparent = False

                        if (payload_list.include_package or payload_list.package_only) and h_artikel.betriebsnr > 0:
                            i = 0

                            h_menu_obj_list = {}
                            for h_menu, h_artikel_buff in db_session.query(H_menu, H_artikel_buff).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr)).filter(
                                     (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
                                if h_menu_obj_list.get(h_menu._recid):
                                    continue
                                else:
                                    h_menu_obj_list[h_menu._recid] = True


                                i = i + 1
                                h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                            i = 0
                            for curr_date in date_range(from_date,to_date) :

                                h_mjourn_obj_list = {}
                                h_mjourn = H_mjourn()
                                h_artikel_buff = H_artikel()
                                for h_mjourn.anzahl, h_mjourn._recid, h_artikel_buff.zwkum, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff.bezeich, h_artikel_buff.betriebsnr, h_artikel_buff.epreis1, h_artikel_buff.artnrlager, h_artikel_buff.artnrrezept, h_artikel_buff.prozent, h_artikel_buff.artnrfront, h_artikel_buff._recid in db_session.query(H_mjourn.anzahl, H_mjourn._recid, H_artikel_buff.zwkum, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff.bezeich, H_artikel_buff.betriebsnr, H_artikel_buff.epreis1, H_artikel_buff.artnrlager, H_artikel_buff.artnrrezept, H_artikel_buff.prozent, H_artikel_buff.artnrfront, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr)).filter(
                                         (H_mjourn.departement == h_artikel.departement) & (H_mjourn.h_artnr == h_artikel.artnr) & (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.bill_datum >= curr_date) & (H_mjourn.bill_datum <= curr_date)).order_by(H_mjourn._recid).all():
                                    if h_mjourn_obj_list.get(h_mjourn._recid):
                                        continue
                                    else:
                                        h_mjourn_obj_list[h_mjourn._recid] = True


                                    for i in range(1,15 + 1) :

                                        if h_list.sub_menu_bezeich[i - 1] == h_artikel_buff.bezeich and h_list.sub_menu_bezeich[i - 1] != "":
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break

                                        elif h_list.sub_menu_bezeich[i - 1] == "" and h_artikel_buff.bezeich != "":
                                            h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break
                                    isparent = True

                        if isparent:
                            h_list.isparent = True

                        if h_artikel.artnrlager != 0:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                            if l_artikel:

                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    h_list.cost =  to_decimal(l_artikel.vk_preis)
                                else:
                                    h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                        elif h_artikel.artnrrezept != 0:

                            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                            if h_rezept:
                                cost_todate =  to_decimal("0")
                                cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                h_list.cost =  to_decimal(cost_todate)
                        else:
                            price =  to_decimal(h_artikel.epreis1)

                            if price != 0:
                                price = calculate_price(price)

                            if price == None:
                                price =  to_decimal("0")
                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                        h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                        h_list.cost = to_decimal(round(h_list.cost , 2))

                        if not payload_list.compliment_only:

                            h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                            while None != h_umsatz:
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                anz = h_umsatz.anzahl
                                cost =  to_decimal("0")
                                h_list.cost =  to_decimal("0")

                                h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                                if h_cost and h_cost.betrag != 0:
                                    cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                    h_list.cost =  to_decimal(h_cost.betrag)
                                else:

                                    if h_artikel.artnrlager != 0:

                                        l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                                        if l_artikel:

                                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                                h_list.cost =  to_decimal(l_artikel.vk_preis)
                                            else:
                                                h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                                    elif h_artikel.artnrrezept != 0:

                                        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                        if h_rezept:
                                            cost_todate =  to_decimal("0")
                                            cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                            h_list.cost =  to_decimal(cost_todate)
                                    else:

                                        if h_artikel.epreis1 != 0:
                                            price =  to_decimal(h_artikel.epreis1)

                                            if price != 0:
                                                price = calculate_price(price)

                                            if price == None:
                                                price =  to_decimal("0")
                                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                                    cost =  to_decimal(anz) * to_decimal(h_list.cost)
                                cost =  to_decimal(cost) / to_decimal(fact1)
                                cost = to_decimal(round(cost , 2))
                                h_list.anzahl = h_list.anzahl + anz
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                                t_cost =  to_decimal(t_cost) + to_decimal(cost)
                                t_anz = t_anz + anz
                                t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                                if h_list.anzahl != 0 and h_list.anzahl != None:
                                    tmp_anzahl = h_list.anzahl
                                else:
                                    tmp_anzahl = 0

                                if vat_included and tmp_anzahl != 0:
                                    # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                                elif tmp_anzahl != 0:
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)


                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                else:
                                    h_list.epreis =  to_decimal("0")
                                    h_list.cost =  to_decimal("0")

                                curr_recid = h_umsatz._recid
                                h_umsatz = db_session.query(H_umsatz).filter(
                                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")

                            if payload_list.include_compliment:
                                cost_open_price =  to_decimal("0")
                                cost_sales_compli =  to_decimal("0")

                                for h_compli in db_session.query(H_compli).filter(
                                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                    h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                    h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)

                                    cost_sales_compli =  to_decimal(cost_sales_compli) + to_decimal(h_compli.epreis)
                                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                    vat =  to_decimal(vat) + to_decimal(vat2)


                                    cost =  to_decimal("0")
                                    cost_compli =  to_decimal("0")

                                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                                    if h_cost and h_cost.betrag != 0:
                                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                                    else:

                                        if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                                            cost_compli =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(h_compli.epreis) * to_decimal(exchg_rate)
                                            cost =  to_decimal(h_compli.anzahl) * to_decimal(cost_compli)

                                    if h_artikel.epreis1 != 0:
                                        cost =  to_decimal(cost) / to_decimal(fact1)
                                        cost = to_decimal(round(cost , 2))
                                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)

                                    if h_list.anzahl != 0 and h_list.anzahl != None:
                                        tmp_anzahl = h_list.anzahl
                                    else:
                                        tmp_anzahl = 0

                                    if vat_included and tmp_anzahl != 0:
                                        h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                        if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                            if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                                h_list.cost =  to_decimal("0")
                                                h_list.t_cost =  to_decimal("0")
                                                cost_open_price =  to_decimal("0")
                                            else:
                                                h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                cost_open_price =  to_decimal(cost_sales_compli) * to_decimal(h_artikel.prozent) / to_decimal("100")

                                    elif tmp_anzahl != 0:
                                        h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                        if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                            if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                                h_list.cost =  to_decimal("0")
                                                h_list.t_cost =  to_decimal("0")
                                                cost_open_price =  to_decimal("0")
                                            else:
                                                h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                cost_open_price =  to_decimal(cost_sales_compli) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                    else:
                                        h_list.epreis =  to_decimal("0")
                                        h_list.cost =  to_decimal("0")
                                    t_anz = t_anz + h_compli.anzahl
                                    t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)
                                t_cost =  to_decimal(t_cost) + to_decimal(cost_open_price)
                        else:

                            for h_compli in db_session.query(H_compli).filter(
                                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                cost =  to_decimal("0")
                                cost_compli =  to_decimal("0")

                                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                                if h_cost and h_cost.betrag != 0:
                                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                                else:

                                    if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                                        cost_compli =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(h_compli.epreis) * to_decimal(exchg_rate)
                                        cost =  to_decimal(h_compli.anzahl) * to_decimal(cost_compli)
                                cost =  to_decimal(cost) / to_decimal(fact1)
                                cost = to_decimal(round(cost , 2))
                                h_list.cost =  to_decimal(cost)
                                h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                                t_anz = t_anz + h_compli.anzahl
                                t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)

                                if h_list.anzahl != 0 and h_list.anzahl != None:
                                    tmp_anzahl = h_list.anzahl
                                else:
                                    tmp_anzahl = 0

                                if vat_included and tmp_anzahl != 0:
                                    # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                                elif tmp_anzahl != 0:
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                else:
                                    h_list.epreis =  to_decimal("0")
                                    h_list.cost =  to_decimal("0")

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
                                t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                create_list(pos)
                t_anz = 0
                t_sales =  to_decimal("0")
                t_cost =  to_decimal("0")
            else:

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.bezeich, h_artikel.betriebsnr, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.bezeich, H_artikel.betriebsnr, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 6) & (Artikel.endkum != disc_nr)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    do_it = False

                    if all_sub:
                        do_it = True
                    else:

                        subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                        do_it = None != subgr_list

                    if do_it:

                        if payload_list.package_only:

                            if h_artikel.betriebsnr == 0:
                                continue
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.cost =  to_decimal("0")
                        h_list.dept = h_artikel.departement
                        h_list.artnr = h_artikel.artnr
                        h_list.dept = h_artikel.departement
                        h_list.bezeich = h_artikel.bezeich
                        h_list.zknr = h_artikel.zwkum

                        if vat_included:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                        else:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)
                        isparent = False

                        if (payload_list.include_package or payload_list.package_only) and h_artikel.betriebsnr > 0:
                            i = 0

                            h_menu_obj_list = {}
                            for h_menu, h_artikel_buff in db_session.query(H_menu, H_artikel_buff).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr)).filter(
                                     (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
                                if h_menu_obj_list.get(h_menu._recid):
                                    continue
                                else:
                                    h_menu_obj_list[h_menu._recid] = True


                                i = i + 1
                                h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                            i = 0
                            for curr_date in date_range(from_date,to_date) :

                                h_mjourn_obj_list = {}
                                h_mjourn = H_mjourn()
                                h_artikel_buff = H_artikel()
                                for h_mjourn.anzahl, h_mjourn._recid, h_artikel_buff.zwkum, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff.bezeich, h_artikel_buff.betriebsnr, h_artikel_buff.epreis1, h_artikel_buff.artnrlager, h_artikel_buff.artnrrezept, h_artikel_buff.prozent, h_artikel_buff.artnrfront, h_artikel_buff._recid in db_session.query(H_mjourn.anzahl, H_mjourn._recid, H_artikel_buff.zwkum, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff.bezeich, H_artikel_buff.betriebsnr, H_artikel_buff.epreis1, H_artikel_buff.artnrlager, H_artikel_buff.artnrrezept, H_artikel_buff.prozent, H_artikel_buff.artnrfront, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr)).filter(
                                         (H_mjourn.departement == h_artikel.departement) & (H_mjourn.h_artnr == h_artikel.artnr) & (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.bill_datum >= curr_date) & (H_mjourn.bill_datum <= curr_date)).order_by(H_mjourn._recid).all():
                                    if h_mjourn_obj_list.get(h_mjourn._recid):
                                        continue
                                    else:
                                        h_mjourn_obj_list[h_mjourn._recid] = True


                                    for i in range(1,15 + 1) :

                                        if h_list.sub_menu_bezeich[i - 1] == h_artikel_buff.bezeich and h_list.sub_menu_bezeich[i - 1] != "":
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break

                                        elif h_list.sub_menu_bezeich[i - 1] == "" and h_artikel_buff.bezeich != "":
                                            h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break
                                    isparent = True

                        if isparent:
                            h_list.isparent = True

                        if h_artikel.artnrlager != 0:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                            if l_artikel:

                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    h_list.cost =  to_decimal(l_artikel.vk_preis)
                                else:
                                    h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                        elif h_artikel.artnrrezept != 0:

                            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                            if h_rezept:
                                cost_todate =  to_decimal("0")
                                cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                h_list.cost =  to_decimal(cost_todate)
                        else:
                            price =  to_decimal(h_artikel.epreis1)

                            if price != 0:
                                price = calculate_price(price)

                            if price == None:
                                price =  to_decimal("0")
                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                        h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                        h_list.cost = to_decimal(round(h_list.cost , 2))

                        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                        while None != h_umsatz:
                            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                            vat =  to_decimal(vat) + to_decimal(vat2)


                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")
                            h_list.cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                if h_artikel.artnrlager != 0:

                                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                                    if l_artikel:

                                        if price_type == 0 or l_artikel.ek_aktuell == 0:
                                            h_list.cost =  to_decimal(l_artikel.vk_preis)
                                        else:
                                            h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                                elif h_artikel.artnrrezept != 0:

                                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                    if h_rezept:
                                        cost_todate =  to_decimal("0")
                                        cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                        h_list.cost =  to_decimal(cost_todate)
                                else:

                                    if h_artikel.epreis1 != 0:
                                        price =  to_decimal(h_artikel.epreis1)

                                        if price != 0:
                                            price = calculate_price(price)

                                        if price == None:
                                            price =  to_decimal("0")
                                        h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                                cost =  to_decimal(anz) * to_decimal(h_list.cost)
                            cost =  to_decimal(cost) / to_decimal(fact1)
                            cost = to_decimal(round(cost , 2))
                            h_list.anzahl = h_list.anzahl + anz
                            h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                            h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                            t_cost =  to_decimal(t_cost) + to_decimal(cost)
                            t_anz = t_anz + anz
                            t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                            if h_list.anzahl != 0 and h_list.anzahl != None:
                                tmp_anzahl = h_list.anzahl
                            else:
                                tmp_anzahl = 0

                            #Rulita added safe devide
                            if vat_included and tmp_anzahl != 0:
                                # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                    if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                        h_list.cost =  to_decimal("0")
                                        h_list.t_cost =  to_decimal("0")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                    else:
                                        h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                            elif tmp_anzahl != 0:
                                h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                    if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                        h_list.cost =  to_decimal("0")
                                        h_list.t_cost =  to_decimal("0")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                    else:
                                        h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                            else:
                                h_list.epreis =  to_decimal("0")
                                h_list.cost =  to_decimal("0")

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

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

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
        cost_todate:Decimal = to_decimal("0.0")
        cost_compli:Decimal = to_decimal("0.0")
        cost_open_price:Decimal = to_decimal("0.0")
        cost_sales_compli:Decimal = to_decimal("0.0")
        price:Decimal = to_decimal("0.0")
        tmp_anzahl:int = 0
        isparent:bool = False
        curr_date:date = None
        i:int = 0
        h_art = None
        h_artikel_buff = None
        H_art =  create_buffer("H_art",H_artikel)
        H_artikel_buff =  create_buffer("H_artikel_buff",H_artikel)
        output_list_data.clear()
        h_list_data.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            if payload_list.compliment_only or payload_list.include_compliment:

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.bezeich, h_artikel.betriebsnr, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.bezeich, H_artikel.betriebsnr, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 4) & (Artikel.endkum != disc_nr)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    do_it = False

                    if all_sub:
                        do_it = True
                    else:

                        subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                        do_it = None != subgr_list

                    if do_it:

                        if payload_list.package_only:

                            if h_artikel.betriebsnr == 0:
                                continue
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.cost =  to_decimal("0")
                        h_list.dept = h_artikel.departement
                        h_list.artnr = h_artikel.artnr
                        h_list.dept = h_artikel.departement
                        h_list.bezeich = h_artikel.bezeich
                        h_list.zknr = h_artikel.zwkum

                        if vat_included:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                        else:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)
                        isparent = False

                        if (payload_list.include_package or payload_list.package_only) and h_artikel.betriebsnr > 0:
                            i = 0

                            h_menu_obj_list = {}
                            for h_menu, h_artikel_buff in db_session.query(H_menu, H_artikel_buff).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr)).filter(
                                     (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
                                if h_menu_obj_list.get(h_menu._recid):
                                    continue
                                else:
                                    h_menu_obj_list[h_menu._recid] = True


                                i = i + 1
                                h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                            i = 0
                            for curr_date in date_range(from_date,to_date) :

                                h_mjourn_obj_list = {}
                                h_mjourn = H_mjourn()
                                h_artikel_buff = H_artikel()
                                for h_mjourn.anzahl, h_mjourn._recid, h_artikel_buff.zwkum, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff.bezeich, h_artikel_buff.betriebsnr, h_artikel_buff.epreis1, h_artikel_buff.artnrlager, h_artikel_buff.artnrrezept, h_artikel_buff.prozent, h_artikel_buff.artnrfront, h_artikel_buff._recid in db_session.query(H_mjourn.anzahl, H_mjourn._recid, H_artikel_buff.zwkum, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff.bezeich, H_artikel_buff.betriebsnr, H_artikel_buff.epreis1, H_artikel_buff.artnrlager, H_artikel_buff.artnrrezept, H_artikel_buff.prozent, H_artikel_buff.artnrfront, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr)).filter(
                                         (H_mjourn.departement == h_artikel.departement) & (H_mjourn.h_artnr == h_artikel.artnr) & (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.bill_datum >= curr_date) & (H_mjourn.bill_datum <= curr_date)).order_by(H_mjourn._recid).all():
                                    if h_mjourn_obj_list.get(h_mjourn._recid):
                                        continue
                                    else:
                                        h_mjourn_obj_list[h_mjourn._recid] = True


                                    for i in range(1,15 + 1) :

                                        if h_list.sub_menu_bezeich[i - 1] == h_artikel_buff.bezeich and h_list.sub_menu_bezeich[i - 1] != "":
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break

                                        elif h_list.sub_menu_bezeich[i - 1] == "" and h_artikel_buff.bezeich != "":
                                            h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break
                                    isparent = True

                        if isparent:
                            h_list.isparent = True

                        if h_artikel.artnrlager != 0:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                            if l_artikel:

                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    h_list.cost =  to_decimal(l_artikel.vk_preis)
                                else:
                                    h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                        elif h_artikel.artnrrezept != 0:

                            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                            if h_rezept:
                                cost_todate =  to_decimal("0")
                                cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                h_list.cost =  to_decimal(cost_todate)
                        else:
                            price =  to_decimal(h_artikel.epreis1)

                            if price != 0:
                                price = calculate_price(price)

                            if price == None:
                                price =  to_decimal("0")
                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                        h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                        h_list.cost = to_decimal(round(h_list.cost , 2))

                        if not payload_list.compliment_only:

                            h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                            while None != h_umsatz:
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                anz = h_umsatz.anzahl
                                cost =  to_decimal("0")
                                h_list.cost =  to_decimal("0")

                                h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                                if h_cost and h_cost.betrag != 0:
                                    cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                    h_list.cost =  to_decimal(h_cost.betrag)
                                else:

                                    if h_artikel.artnrlager != 0:

                                        l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                                        if l_artikel:

                                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                                h_list.cost =  to_decimal(l_artikel.vk_preis)
                                            else:
                                                h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                                    elif h_artikel.artnrrezept != 0:

                                        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                        if h_rezept:
                                            cost_todate =  to_decimal("0")
                                            cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                            h_list.cost =  to_decimal(cost_todate)
                                    else:

                                        if h_artikel.epreis1 != 0:
                                            price =  to_decimal(h_artikel.epreis1)

                                            if price != 0:
                                                price = calculate_price(price)

                                            if price == None:
                                                price =  to_decimal("0")
                                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                                    cost =  to_decimal(anz) * to_decimal(h_list.cost)
                                cost =  to_decimal(cost) / to_decimal(fact1)
                                cost = to_decimal(round(cost , 2))
                                h_list.anzahl = h_list.anzahl + anz
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                                t_cost =  to_decimal(t_cost) + to_decimal(cost)
                                t_anz = t_anz + anz
                                t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                                if h_list.anzahl != 0 and h_list.anzahl != None:
                                    tmp_anzahl = h_list.anzahl
                                else:
                                    tmp_anzahl = 0

                                if vat_included and tmp_anzahl != 0:
                                    # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                                elif tmp_anzahl != 0:
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                else:
                                    h_list.epreis =  to_decimal("0")
                                    h_list.cost =  to_decimal("0")

                                curr_recid = h_umsatz._recid
                                h_umsatz = db_session.query(H_umsatz).filter(
                                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")

                            if payload_list.include_compliment:
                                cost_open_price =  to_decimal("0")
                                cost_sales_compli =  to_decimal("0")

                                for h_compli in db_session.query(H_compli).filter(
                                         (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                    h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                    h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                    
                                    cost_sales_compli =  to_decimal(cost_sales_compli) + to_decimal(h_compli.epreis)
                                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                    vat =  to_decimal(vat) + to_decimal(vat2)


                                    cost =  to_decimal("0")
                                    cost_compli =  to_decimal("0")

                                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                                    if h_cost and h_cost.betrag != 0:
                                        cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                                    else:

                                        if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                                            cost_compli =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(h_compli.epreis) * to_decimal(exchg_rate)
                                            cost =  to_decimal(h_compli.anzahl) * to_decimal(cost_compli)

                                    if h_artikel.epreis1 != 0:
                                        cost =  to_decimal(cost) / to_decimal(fact1)
                                        cost = to_decimal(round(cost , 2))
                                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)

                                    if h_list.anzahl != 0 and h_list.anzahl != None:
                                        tmp_anzahl = h_list.anzahl
                                    else:
                                        tmp_anzahl = 0

                                    if vat_included and tmp_anzahl != 0:
                                        h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                        if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                            if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                                h_list.cost =  to_decimal("0")
                                                h_list.t_cost =  to_decimal("0")
                                                cost_open_price =  to_decimal("0")
                                            else:
                                                h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                cost_open_price =  to_decimal(cost_sales_compli) * to_decimal(h_artikel.prozent) / to_decimal("100")

                                    elif tmp_anzahl != 0:
                                        h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                        if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                            if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                                h_list.cost =  to_decimal("0")
                                                h_list.t_cost =  to_decimal("0")
                                                cost_open_price =  to_decimal("0")
                                            else:
                                                h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                                cost_open_price =  to_decimal(cost_sales_compli) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                    else:
                                        h_list.epreis =  to_decimal("0")
                                        h_list.cost =  to_decimal("0")
                                    t_anz = t_anz + h_compli.anzahl
                                    t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)
                                t_cost =  to_decimal(t_cost) + to_decimal(cost_open_price)
                        else:

                            for h_compli in db_session.query(H_compli).filter(
                                     (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.departement == hoteldpt.num) & (H_compli.betriebsnr == 0) & (H_compli.artnr == h_artikel.artnr)).order_by(H_compli._recid).all():
                                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_compli.datum))
                                vat =  to_decimal(vat) + to_decimal(vat2)


                                cost =  to_decimal("0")
                                cost_compli =  to_decimal("0")

                                h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                                if h_cost and h_cost.betrag != 0:
                                    cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag)
                                else:

                                    if (not h_cost and h_compli.datum < bill_date) or (h_cost and h_cost.betrag == 0):
                                        cost_compli =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(h_compli.epreis) * to_decimal(exchg_rate)
                                        cost =  to_decimal(h_compli.anzahl) * to_decimal(cost_compli)
                                cost =  to_decimal(cost) / to_decimal(fact1)
                                cost = to_decimal(round(cost , 2))
                                h_list.cost =  to_decimal(cost)
                                h_list.anzahl = h_list.anzahl + h_compli.anzahl
                                h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_compli.epreis)
                                h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                                t_anz = t_anz + h_compli.anzahl
                                t_sales =  to_decimal(t_sales) + to_decimal(h_compli.epreis)

                                if h_list.anzahl != 0 and h_list.anzahl != None:
                                    tmp_anzahl = h_list.anzahl
                                else:
                                    tmp_anzahl = 0

                                if vat_included and tmp_anzahl != 0:
                                    # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                                elif tmp_anzahl != 0:
                                    h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                    if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                        if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                            h_list.cost =  to_decimal("0")
                                            h_list.t_cost =  to_decimal("0")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                        else:
                                            h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                            t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                else:
                                    h_list.epreis =  to_decimal("0")
                                    h_list.cost =  to_decimal("0")

                            if h_list.epreis != 0:
                                h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
                                t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                create_list(pos)
                t_anz = 0
                t_sales =  to_decimal("0")
                t_cost =  to_decimal("0")
            else:

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.bezeich, h_artikel.betriebsnr, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.bezeich, H_artikel.betriebsnr, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 4) & (Artikel.endkum != disc_nr)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    do_it = False

                    if all_sub:
                        do_it = True
                    else:

                        subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                        do_it = None != subgr_list

                    if do_it:

                        if payload_list.package_only:

                            if h_artikel.betriebsnr == 0:
                                continue
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.cost =  to_decimal("0")
                        h_list.dept = h_artikel.departement
                        h_list.artnr = h_artikel.artnr
                        h_list.dept = h_artikel.departement
                        h_list.bezeich = h_artikel.bezeich
                        h_list.zknr = h_artikel.zwkum

                        if vat_included:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact)
                        else:
                            h_list.epreis =  to_decimal(h_artikel.epreis1) * to_decimal(exchg_rate) / to_decimal(fact1)
                        isparent = False

                        if (payload_list.include_package or payload_list.package_only) and h_artikel.betriebsnr > 0:
                            i = 0

                            h_menu_obj_list = {}
                            for h_menu, h_artikel_buff in db_session.query(H_menu, H_artikel_buff).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr)).filter(
                                     (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
                                if h_menu_obj_list.get(h_menu._recid):
                                    continue
                                else:
                                    h_menu_obj_list[h_menu._recid] = True


                                i = i + 1
                                h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                            i = 0
                            for curr_date in date_range(from_date,to_date) :

                                h_mjourn_obj_list = {}
                                h_mjourn = H_mjourn()
                                h_artikel_buff = H_artikel()
                                for h_mjourn.anzahl, h_mjourn._recid, h_artikel_buff.zwkum, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff.bezeich, h_artikel_buff.betriebsnr, h_artikel_buff.epreis1, h_artikel_buff.artnrlager, h_artikel_buff.artnrrezept, h_artikel_buff.prozent, h_artikel_buff.artnrfront, h_artikel_buff._recid in db_session.query(H_mjourn.anzahl, H_mjourn._recid, H_artikel_buff.zwkum, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff.bezeich, H_artikel_buff.betriebsnr, H_artikel_buff.epreis1, H_artikel_buff.artnrlager, H_artikel_buff.artnrrezept, H_artikel_buff.prozent, H_artikel_buff.artnrfront, H_artikel_buff._recid).join(H_artikel_buff,(H_artikel_buff.artnr == H_mjourn.artnr)).filter(
                                         (H_mjourn.departement == h_artikel.departement) & (H_mjourn.h_artnr == h_artikel.artnr) & (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.bill_datum >= curr_date) & (H_mjourn.bill_datum <= curr_date)).order_by(H_mjourn._recid).all():
                                    if h_mjourn_obj_list.get(h_mjourn._recid):
                                        continue
                                    else:
                                        h_mjourn_obj_list[h_mjourn._recid] = True


                                    for i in range(1,15 + 1) :

                                        if h_list.sub_menu_bezeich[i - 1] == h_artikel_buff.bezeich and h_list.sub_menu_bezeich[i - 1] != "":
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break

                                        elif h_list.sub_menu_bezeich[i - 1] == "" and h_artikel_buff.bezeich != "":
                                            h_list.sub_menu_bezeich[i - 1] = h_artikel_buff.bezeich
                                            h_list.sub_menu_qty[i - 1] = h_list.sub_menu_qty[i - 1] + h_mjourn.anzahl
                                            break
                                    isparent = True

                        if isparent:
                            h_list.isparent = True

                        if h_artikel.artnrlager != 0:

                            l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                            if l_artikel:

                                if price_type == 0 or l_artikel.ek_aktuell == 0:
                                    h_list.cost =  to_decimal(l_artikel.vk_preis)
                                else:
                                    h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                        elif h_artikel.artnrrezept != 0:

                            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                            if h_rezept:
                                cost_todate =  to_decimal("0")
                                cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                h_list.cost =  to_decimal(cost_todate)
                        else:
                            price =  to_decimal(h_artikel.epreis1)

                            if price != 0:
                                price = calculate_price(price)

                            if price == None:
                                price =  to_decimal("0")
                            h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                        h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                        h_list.cost = to_decimal(round(h_list.cost , 2))

                        h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                        while None != h_umsatz:
                            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                            vat =  to_decimal(vat) + to_decimal(vat2)


                            anz = h_umsatz.anzahl
                            cost =  to_decimal("0")
                            h_list.cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                                h_list.cost =  to_decimal(h_cost.betrag)
                            else:

                                if h_artikel.artnrlager != 0:

                                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                                    if l_artikel:

                                        if price_type == 0 or l_artikel.ek_aktuell == 0:
                                            h_list.cost =  to_decimal(l_artikel.vk_preis)
                                        else:
                                            h_list.cost =  to_decimal(l_artikel.ek_aktuell)

                                elif h_artikel.artnrrezept != 0:

                                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                                    if h_rezept:
                                        cost_todate =  to_decimal("0")
                                        cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                        h_list.cost =  to_decimal(cost_todate)
                                else:

                                    if h_artikel.epreis1 != 0:
                                        price =  to_decimal(h_artikel.epreis1)

                                        if price != 0:
                                            price = calculate_price(price)

                                        if price == None:
                                            price =  to_decimal("0")
                                        h_list.cost =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
                                cost =  to_decimal(anz) * to_decimal(h_list.cost)
                            cost =  to_decimal(cost) / to_decimal(fact1)
                            cost = to_decimal(round(cost , 2))
                            h_list.anzahl = h_list.anzahl + anz
                            h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                            h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                            t_cost =  to_decimal(t_cost) + to_decimal(cost)
                            t_anz = t_anz + anz
                            t_sales =  to_decimal(t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                            if h_list.anzahl != 0 and h_list.anzahl != None:
                                tmp_anzahl = h_list.anzahl
                            else:
                                tmp_anzahl = 0

                            if vat_included and tmp_anzahl != 0:
                                # h_list.epreis = ( to_decimal(h_list.t_sales) / to_decimal(h_list.anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)
                                h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact)

                                if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                    if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                        h_list.cost =  to_decimal("0")
                                        h_list.t_cost =  to_decimal("0")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                    else:
                                        h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)

                            elif tmp_anzahl != 0:
                                h_list.epreis = ( safe_divide(h_list.t_sales, tmp_anzahl)) * to_decimal(exchg_rate) / to_decimal(fact1)

                                if h_artikel.epreis1 == 0 and (not h_cost or (h_cost and h_cost.betrag == 0)):

                                    if (h_artikel.artnr == food_disc or h_artikel.artnr == bev_disc or h_artikel.artnr == other_disc) and h_artikel.prozent != 0:
                                        h_list.cost =  to_decimal("0")
                                        h_list.t_cost =  to_decimal("0")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                                    else:
                                        h_list.cost =  to_decimal(h_list.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        h_list.t_cost =  to_decimal(h_list.t_sales) * to_decimal(h_artikel.prozent) / to_decimal("100")
                                        t_cost =  to_decimal(t_cost) + to_decimal(h_list.t_cost)
                            else:
                                h_list.epreis =  to_decimal("0")
                                h_list.cost =  to_decimal("0")

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

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

        if mi_subgrp:
            create_list1(pos)

            return

        if detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num)):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_data.append(fb_cost_analyst)

            fb_cost_analyst.bezeich = "T o t a l"
            fb_cost_analyst.qty = t_anz
            fb_cost_analyst.proz1 =  to_decimal("100")
            fb_cost_analyst.t_sales =  to_decimal(t_sales)
            fb_cost_analyst.t_cost =  to_decimal(t_cost)
            fb_cost_analyst.t_margin =  to_decimal(t_margin)
            fb_cost_analyst.proz2 =  to_decimal("100")


            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_data.append(fb_cost_analyst)

    def create_list1(pos:bool):

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

        curr_grp:int = 0
        wgrpdep_bezeich:string = ""

        if detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = wgrpdep.bezeich

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


                add_sub()


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})

                    if wgrpdep:
                        wgrpdep_bezeich = wgrpdep.bezeich
                    else:
                        wgrpdep_bezeich = ""
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = wgrpdep.bezeich

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


                add_sub()


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = wgrpdep.bezeich

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


                add_sub()


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = wgrpdep.bezeich

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


                add_sub()


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = wgrpdep.bezeich

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


                add_sub()


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = wgrpdep.bezeich

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = h_list.bezeich
                fb_cost_analyst.artnr = h_list.artnr
                fb_cost_analyst.qty = h_list.anzahl
                fb_cost_analyst.proz1 =  to_decimal(h_list.proz1)
                fb_cost_analyst.epreis =  to_decimal(h_list.epreis)
                fb_cost_analyst.cost =  to_decimal(h_list.cost)
                fb_cost_analyst.margin =  to_decimal(h_list.margin)
                fb_cost_analyst.t_sales =  to_decimal(h_list.t_sales)
                fb_cost_analyst.t_cost =  to_decimal(h_list.t_cost)
                fb_cost_analyst.t_margin =  to_decimal(h_list.margin)
                fb_cost_analyst.proz2 =  to_decimal(h_list.proz2)
                fb_cost_analyst.dept = h_list.dept
                fb_cost_analyst.item_profit =  to_decimal(fb_cost_analyst.epreis) - to_decimal(fb_cost_analyst.cost)
                fb_cost_analyst.total_profit =  to_decimal(fb_cost_analyst.t_sales) - to_decimal(fb_cost_analyst.t_cost)


                add_sub()

        create_sub(curr_grp)

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_data.append(fb_cost_analyst)

            fb_cost_analyst.bezeich = "T o t a l"
            fb_cost_analyst.qty = t_anz
            fb_cost_analyst.proz1 =  to_decimal("100")
            fb_cost_analyst.t_sales =  to_decimal(t_sales)
            fb_cost_analyst.t_cost =  to_decimal(t_cost)
            fb_cost_analyst.t_margin =  to_decimal(t_margin)
            fb_cost_analyst.proz2 =  to_decimal("100")


            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_data.append(fb_cost_analyst)

    def create_sub(curr_grp:int):

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

        if curr_grp != 0:

            if st_sales != 0:
                st_margin =  to_decimal(st_cost) / to_decimal(st_sales) * to_decimal("100")
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_data.append(fb_cost_analyst)

            fb_cost_analyst.flag = 2
            fb_cost_analyst.bezeich = "S u b T o t a l"
            fb_cost_analyst.qty = s_anzahl
            fb_cost_analyst.proz1 =  to_decimal(s_proz1)
            fb_cost_analyst.t_sales =  to_decimal(st_sales)
            fb_cost_analyst.t_cost =  to_decimal(st_cost)
            fb_cost_analyst.t_margin =  to_decimal(st_margin)
            fb_cost_analyst.proz2 =  to_decimal(st_proz2)
            s_anzahl = 0
            s_proz1 =  to_decimal("0")
            st_sales =  to_decimal("0")
            st_cost =  to_decimal("0")
            st_margin =  to_decimal("0")
            st_proz2 =  to_decimal("0")


    def add_sub():

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)


    def calculate_price(price:Decimal):

        nonlocal output_list2_data, t_anz, t_anz_deb, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, gtotal_sold, gtotal_sold_perc, gtotal_cost, gtotal_revenue, gtotal_profit, avrg_item_profit, food_cost, menu_pop_factor, count_foodcost, double_currency, incl_service, incl_mwst, exrate, bill_date, food_disc, bev_disc, other_disc, price_type, htparam, waehrung, h_artikel, hoteldpt, artikel, h_menu, h_mjourn, l_artikel, h_rezept, h_umsatz, h_cost, h_compli, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, payload_list, output_list, h_list, fb_cost_analyst, output_list2, ph_list
        nonlocal output_list_data, h_list_data, fb_cost_analyst_data, output_list2_data

        artikel1 = None
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = 1

        def generate_inner_output():
            return (price)

        Artikel1 =  create_buffer("Artikel1",Artikel)

        artikel1 = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

        if artikel1 and artikel1.pricetab and not double_currency:
            price =  to_decimal(price) * to_decimal(exrate)

        if incl_mwst or incl_service:
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(3, artikel1.artnr, artikel1.departement, to_date))

            if serv != 0:
                fact =  to_decimal(serv) + to_decimal((1) + to_decimal(serv)) * to_decimal((vat) + to_decimal(vat2)) / to_decimal("100")
            else:
                fact =  to_decimal(serv) + to_decimal((vat) + to_decimal(vat2)) / to_decimal("100")
            fact =  to_decimal("1") + to_decimal(fact)
        price =  to_decimal(price) / to_decimal(fact)
        price = to_decimal(round(price , 2))

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        food_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        other_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        bev_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    payload_list = query(payload_list_data, first=True)

    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    elif sorttype == 3:
        create_h_umsatz3()

    for fb_cost_analyst in query(fb_cost_analyst_data):
        gtotal_sold =  to_decimal(gtotal_sold) + to_decimal(fb_cost_analyst.qty)
        gtotal_sold_perc =  to_decimal(gtotal_sold_perc) + to_decimal(fb_cost_analyst.proz1)
        gtotal_cost =  to_decimal(gtotal_cost) + to_decimal(fb_cost_analyst.t_cost)
        gtotal_revenue =  to_decimal(gtotal_revenue) + to_decimal(fb_cost_analyst.t_sales)
        gtotal_profit =  to_decimal(gtotal_profit) + to_decimal(fb_cost_analyst.total_profit)

        if fb_cost_analyst.artnr != 0:
            count_foodcost =  to_decimal(count_foodcost) + to_decimal("1")
    avrg_item_profit =  to_decimal(gtotal_profit) / to_decimal(gtotal_sold)
    menu_pop_factor = ( to_decimal((1) / to_decimal(count_foodcost)) * to_decimal(0.8))

    for fb_cost_analyst in query(fb_cost_analyst_data):

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
        output_list2 = Output_list2()
        output_list2_data.append(output_list2)


        if fb_cost_analyst.artnr != 0:
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
            output_list2.t_margin = to_string(fb_cost_analyst.t_margin , "->,>>>,>>>,>>9.99")
            output_list2.profit = to_string(fb_cost_analyst.total_profit , "->,>>>,>>>,>>9.99")
            output_list2.proz2 = to_string(fb_cost_analyst.proz2 , "->>9.99")
            output_list2.profit_cat = to_string(fb_cost_analyst.profit_category)
            output_list2.popularity_cat = to_string(fb_cost_analyst.popularity_category)
            output_list2.menu_item_class = to_string(fb_cost_analyst.menu_item_class)
            output_list2.dept = to_string(fb_cost_analyst.dept)

        elif fb_cost_analyst.bezeich.lower()  == ("T o t a l").lower() :
            output_list2.artnr = to_string("")
            output_list2.bezeich = fb_cost_analyst.bezeich
            output_list2.anzahl = to_string(fb_cost_analyst.qty , "->>>>9")
            output_list2.proz1 = to_string(100, "->>9.99")
            output_list2.epreis = to_string("")
            output_list2.cost = to_string("")
            output_list2.margin = to_string("")
            output_list2.item_prof = to_string("")
            output_list2.t_sales = to_string(fb_cost_analyst.t_sales , "->,>>>,>>>,>>9.99")
            output_list2.t_cost = to_string(fb_cost_analyst.t_cost , "->,>>>,>>>,>>9.99")
            output_list2.t_margin = to_string(fb_cost_analyst.t_margin , "->,>>>,>>>,>>9.99")
            output_list2.profit = to_string("")
            output_list2.proz2 = to_string(100, "->>9.99")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")

        elif fb_cost_analyst.bezeich.lower()  == ("S u b T o t a l").lower() :
            output_list2.artnr = to_string("")
            output_list2.bezeich = fb_cost_analyst.bezeich
            output_list2.anzahl = to_string(fb_cost_analyst.qty , "->>>>9")
            output_list2.proz1 = to_string(fb_cost_analyst.proz1 , "->>9.99")
            output_list2.epreis = to_string("")
            output_list2.cost = to_string("")
            output_list2.margin = to_string("")
            output_list2.item_prof = to_string("")
            output_list2.t_sales = to_string(fb_cost_analyst.t_sales , "->,>>>,>>>,>>9.99")
            output_list2.t_cost = to_string(fb_cost_analyst.t_cost , "->,>>>,>>>,>>9.99")
            output_list2.t_margin = to_string(fb_cost_analyst.t_margin , "->,>>>,>>>,>>9.99")
            output_list2.profit = to_string("")
            output_list2.proz2 = to_string(fb_cost_analyst.proz2 , "->>9.99")
            output_list2.profit_cat = to_string("")
            output_list2.popularity_cat = to_string("")
            output_list2.menu_item_class = to_string("")


        else:
            output_list2.artnr = to_string("")
            output_list2.bezeich = fb_cost_analyst.bezeich
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

    if payload_list.include_package or payload_list.package_only:

        for output_list2 in query(output_list2_data):

            h_list = query(h_list_data, filters=(lambda h_list: h_list.artnr == to_int(output_list2.artnr) and h_list.dept == to_int(output_list2.dept)), first=True)

            if h_list:
                output_list2.isparent = h_list.isparent
                output_list2.sub_menu_bezeich = h_list.sub_menu_bezeich
                output_list2.sub_menu_qty = h_list.sub_menu_qty

    return generate_output()