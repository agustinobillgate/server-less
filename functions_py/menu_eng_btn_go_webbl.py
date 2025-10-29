#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import Htparam, Waehrung, H_artikel, Hoteldpt, Artikel, L_artikel, H_rezept, H_umsatz, H_cost, Wgrpdep

subgr_list_data, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":string}, {"selected": True})

def menu_eng_btn_go_webbl(subgr_list_data:[Subgr_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:Decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):

    prepare_cache ([Htparam, Waehrung, H_artikel, Hoteldpt, Artikel, L_artikel, H_rezept, H_cost, Wgrpdep])

    fb_cost_analyst_data = []
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
    double_currency:bool = False
    incl_service:bool = False
    incl_mwst:bool = False
    exrate:Decimal = 1
    bill_date:date = date(1,1,1)
    htparam = waehrung = h_artikel = hoteldpt = artikel = l_artikel = h_rezept = h_umsatz = h_cost = wgrpdep = None

    subgr_list = h_list = fb_cost_analyst = None

    h_list_data, H_list = create_model("H_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal})
    fb_cost_analyst_data, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":string, "bezeich":string, "qty":string, "proz1":string, "epreis":string, "cost":string, "margin":string, "t_sales":string, "t_cost":string, "t_margin":string, "proz2":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

        return {"fb-cost-analyst": fb_cost_analyst_data}

    def calculate_price(price:Decimal):

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

        artikel1 = None
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = 1

        def generate_inner_output():
            return (price)
        artikel1 = db_session.query(Artikel).filter((Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()
        
        if artikel1 and artikel1.pricetab and not double_currency:
            price =  to_decimal(price) * to_decimal(exrate)

        if incl_mwst or incl_service:
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(3, artikel1.artnr, artikel1.departement, to_date))

            if serv != 0:
                fact = serv + (1 + serv) * (vat + vat2) / 100
            else:
                fact = serv + (vat + vat2) / 100

            fact = fact + 1

        price = to_decimal(price) / to_decimal(fact)

        price = to_decimal(round(price, 2))

        return generate_inner_output()

    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def create_h_umsatz1():

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

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
        cost_todate:Decimal = to_decimal("0.0")
        cost_open_price:Decimal = to_decimal("0.0")
        price:Decimal = to_decimal("0.0")
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        fb_cost_analyst_data.clear()
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

                # fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99") + " " + format_fixed_length(hoteldpt.depart, 21)

            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & ((Artikel.umsatzart == 3) | (Artikel.umsatzart == 5)) & (Artikel.endkum != disc_nr)).filter(
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
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  vat + vat2

                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.cost =  to_decimal("0")
                    # h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))
                    # h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    # h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / to_decimal(fact)
                    else:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / to_decimal(fact1)

                    if h_artikel.artnrlager != 0:

                        l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == h_artikel.artnrlager).first()

                        if l_artikel:

                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                h_list.cost = l_artikel.vk_preis

                            else:
                                h_list.cost = l_artikel.ek_aktuell

                    elif h_artikel.artnrrezept != 0:

                        h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == h_artikel.artnrrezept).first()

                        if h_rezept:

                            cost_todate = 0

                            cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))

                            h_list.cost = cost_todate

                    else:

                        price = h_artikel.epreis1
                        if price != 0:
                            price = calculate_price(price)

                        if price == None:
                            price = 0

                        h_list.cost = h_artikel.prozent / 100 * price * exchg_rate

                    h_list.cost = h_list.cost / to_decimal(fact1)

                    h_list.cost = h_list.cost

                    # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    # while None != h_umsatz:

                    for h_umsatz in db_session.query(H_umsatz).filter((H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).all():

                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  vat + vat2

                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")

                        h_list.cost =  to_decimal("0")
                        # h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                        h_cost = db_session.query(H_cost).filter((H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == h_umsatz.datum) & (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = anz * h_cost.betrag
                            h_list.cost = h_cost.betrag
                        else:
                            if h_artikel.artnrlager != 0:
                                l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == h_artikel.artnrlager).first()

                                if l_artikel:
                                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                                        h_list.cost = l_artikel.vk_preis

                                    else:
                                        h_list.cost = l_artikel.ek_aktuell

                            elif h_artikel.artnrrezept != 0:
                                h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == h_artikel.artnrrezept).first()

                                if h_rezept:

                                    cost_todate = 0

                                    cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                    h_list.cost = cost_todate
                            else:
                                if h_artikel.epreis1 != 0:
                                    price = h_artikel.epreis1

                                    if price != 0:
                                        price = calculate_price(price)

                                    if price == None:
                                        price = 0

                                    h_list.cost = h_artikel.prozent / 100 * price * exchg_rate

                            cost = anz * h_list.cost
                            
                        cost =  cost / fact1

                        h_list.anzahl = h_list.anzahl + anz
                        h_list.t_cost =  h_list.t_cost + cost
                        h_list.t_sales =  h_list.t_sales + h_umsatz.betrag / fact
                        t_cost = t_cost + cost
                        t_anz = t_anz + anz
                        t_sales =  t_sales + h_umsatz.betrag / fact

                        if h_list.anzahl != 0 and h_list.anzahl != None:
                            tmp_anzahl = h_list.anzahl
                        else:
                            tmp_anzahl = 0

                        if vat_included and tmp_anzahl != 0:
                            h_list.epreis = ( h_list.t_sales / tmp_anzahl) * exchg_rate / fact
                            
                            if h_artikel.epreis1 == 0 and ((not h_cost) or (h_cost and h_cost.betrag == 0)):
                                h_list.cost = h_list.epreis * h_artikel.prozent / 100
                                
                                h_list.t_cost = h_list.t_sales * h_artikel.prozent / 100
                                t_cost = t_cost + h_list.t_cost

                        elif tmp_anzahl != 0:
                            h_list.epreis = ( h_list.t_sales / tmp_anzahl) * exchg_rate / fact1

                            if h_artikel.epreis1 == 0 and ((not h_cost) or (h_cost and h_cost.betrag == 0)):
                                h_list.cost = h_list.epreis * h_artikel.prozent / 100

                                h_list.t_cost = h_list.t_sales * h_artikel.prozent / 100
                                t_cost = t_cost + h_list.t_cost

                        else:
                            h_list.epreis =  to_decimal("0")
                            h_list.cost = to_decimal("0")

                        h_list.t_cost = Decimal(f"{h_list.t_cost}").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                        # curr_recid = h_umsatz._recid
                        # h_umsatz = db_session.query(H_umsatz).filter(
                        #          (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  h_list.cost / h_list.epreis * to_decimal("100")

            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_h_umsatz2():

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

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
        cost_open_price:Decimal = to_decimal("0.0")
        price:Decimal = to_decimal("0.0")
        tmp_anzahl:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        fb_cost_analyst_data.clear()
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

                # fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99") + " " + format_fixed_length(hoteldpt.depart, 21)

            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 6) & (Artikel.endkum != disc_nr)).filter(
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
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  vat + vat2

                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.cost =  to_decimal("0")
                    # h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))
                    # h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    # h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / to_decimal(fact)
                    else:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / to_decimal(fact1)

                    if h_artikel.artnrlager != 0:

                        l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == h_artikel.artnrlager).first()

                        if l_artikel:

                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                h_list.cost = l_artikel.vk_preis

                            else:
                                h_list.cost = l_artikel.ek_aktuell

                    elif h_artikel.artnrrezept != 0:

                        h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == h_artikel.artnrrezept).first()

                        if h_rezept:
                            cost_todate = 0

                            cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                            h_list.cost = cost_todate
                    else:
                        price = h_artikel.epreis1
                        if price != 0:
                            price = calculate_price(price)

                        if price == None:
                            price = 0

                        h_list.cost = h_artikel.prozent / 100 * price * exchg_rate

                    h_list.cost = h_list.cost / to_decimal(fact1)

                    h_list.cost = h_list.cost

                    # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    # while None != h_umsatz:

                    for h_umsatz in db_session.query(H_umsatz).filter((H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).all():

                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  vat + vat2

                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")
                        
                        h_list.cost =  to_decimal("0")
                        # h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                        h_cost = db_session.query(H_cost).filter((H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == h_umsatz.datum) & (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = anz * h_cost.betrag
                            h_list.cost = h_cost.betrag
                        else:
                            if h_artikel.artnrlager != 0:
                                l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == h_artikel.artnrlager).first()

                                if l_artikel:
                                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                                        h_list.cost = l_artikel.vk_preis

                                    else:
                                        h_list.cost = l_artikel.ek_aktuell

                            elif h_artikel.artnrrezept != 0:
                                h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == h_artikel.artnrrezept).first()

                                if h_rezept:

                                    cost_todate = 0

                                    cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                    h_list.cost = cost_todate
                            else:

                                if h_artikel.epreis1 != 0:
                                    price = h_artikel.epreis1

                                    if price != 0:
                                        price = calculate_price(price)

                                    if price == None:
                                        price = 0

                                    h_list.cost = h_artikel.prozent / 100 * price * exchg_rate

                            cost = anz * h_list.cost
                        
                        cost =  cost / fact1

                        h_list.anzahl = h_list.anzahl + anz
                        h_list.t_cost =  h_list.t_cost + cost
                        h_list.t_sales =  h_list.t_sales + h_umsatz.betrag / fact
                        t_cost = t_cost + cost
                        t_anz = t_anz + anz
                        t_sales =  t_sales + h_umsatz.betrag / fact

                        if h_list.anzahl != 0 and h_list.anzahl != None:
                            tmp_anzahl = h_list.anzahl
                        else:
                            tmp_anzahl = 0

                        if vat_included and tmp_anzahl != 0:
                            h_list.epreis = ( h_list.t_sales / tmp_anzahl) * exchg_rate / fact
                            
                            if h_artikel.epreis1 == 0 and ((not h_cost) or (h_cost and h_cost.betrag == 0)):
                                h_list.cost = h_list.epreis * h_artikel.prozent / 100
                                
                                h_list.t_cost = h_list.t_sales * h_artikel.prozent / 100
                                t_cost = t_cost + h_list.t_cost

                        elif tmp_anzahl != 0:
                            h_list.epreis = ( h_list.t_sales / tmp_anzahl) * exchg_rate / fact1

                            if h_artikel.epreis1 == 0 and ((not h_cost) or (h_cost and h_cost.betrag == 0)):
                                h_list.cost = h_list.epreis * h_artikel.prozent / 100

                                h_list.t_cost = h_list.t_sales * h_artikel.prozent / 100
                                t_cost = t_cost + h_list.t_cost

                        else:
                            h_list.epreis =  to_decimal("0")
                            h_list.cost = to_decimal("0")

                        h_list.t_cost = Decimal(f"{h_list.t_cost}").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                        # curr_recid = h_umsatz._recid
                        # h_umsatz = db_session.query(H_umsatz).filter(
                        #          (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  h_list.cost / h_list.epreis * to_decimal("100")

            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")

    def create_h_umsatz3():

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

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
        cost_open_price:Decimal = to_decimal("0.0")
        price:Decimal = to_decimal("0.0")
        tmp_anzahl:int = 0
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
        fb_cost_analyst_data.clear()
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

                # fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99") + " " + format_fixed_length(hoteldpt.depart, 21)

            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.departement, h_artikel.artnr, h_artikel.bezeich, h_artikel.epreis1, h_artikel.artnrlager, h_artikel.artnrrezept, h_artikel.prozent, h_artikel.artnrfront, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.departement, H_artikel.artnr, H_artikel.bezeich, H_artikel.epreis1, H_artikel.artnrlager, H_artikel.artnrrezept, H_artikel.prozent, H_artikel.artnrfront, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 4) & (Artikel.endkum != disc_nr)).filter(
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
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  vat + vat2

                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.cost =  to_decimal("0")
                    # h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))
                    # h_list.cost =  to_decimal(h_list.cost) / to_decimal(fact1)
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    # h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / to_decimal(fact)
                    else:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / to_decimal(fact1)

                    if h_artikel.artnrlager != 0:

                        l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == h_artikel.artnrlager).first()

                        if l_artikel:

                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                h_list.cost = l_artikel.vk_preis

                            else:
                                h_list.cost = l_artikel.ek_aktuell

                    elif h_artikel.artnrrezept != 0:

                        h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == h_artikel.artnrrezept).first()

                        if h_rezept:

                            cost_todate = 0

                            cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))

                            h_list.cost = cost_todate

                    else:

                        price = h_artikel.epreis1
                        if price != 0:
                            price = calculate_price(price)

                        if price == None:
                            price = 0

                        h_list.cost = h_artikel.prozent / 100 * price * exchg_rate

                    h_list.cost = h_list.cost / to_decimal(fact1)

                    h_list.cost = h_list.cost

                    # h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    # while None != h_umsatz:

                    for h_umsatz in db_session.query(H_umsatz).filter((H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).all():

                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  vat + vat2

                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")
                        
                        h_list.cost =  to_decimal("0")
                        # h_list.cost = get_output(fb_cost_count_recipe_costbl(h_artikel.artnrrezept, price_type, h_list.cost))

                        h_cost = db_session.query(H_cost).filter((H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == h_umsatz.datum) & (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = anz * h_cost.betrag
                            h_list.cost = h_cost.betrag
                        else:
                            if h_artikel.artnrlager != 0:
                                l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == h_artikel.artnrlager).first()

                                if l_artikel:
                                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                                        h_list.cost = l_artikel.vk_preis

                                    else:
                                        h_list.cost = l_artikel.ek_aktuell

                            elif h_artikel.artnrrezept != 0:
                                h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == h_artikel.artnrrezept).first()

                                if h_rezept:

                                    cost_todate = 0

                                    cost_todate = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost_todate))
                                    h_list.cost = cost_todate
                            else:
                                if h_artikel.epreis1 != 0:
                                    price = h_artikel.epreis1

                                    if price != 0:
                                        price = calculate_price(price)

                                    if price == None:
                                        price = 0

                                    h_list.cost = h_artikel.prozent / 100 * price * exchg_rate
                            cost = anz * h_list.cost
                        cost =  cost / fact1

                        h_list.anzahl = h_list.anzahl + anz
                        h_list.t_cost =  h_list.t_cost + cost
                        h_list.t_sales =  h_list.t_sales + h_umsatz.betrag / fact
                        t_cost = t_cost + cost
                        t_anz = t_anz + anz
                        t_sales =  t_sales + h_umsatz.betrag / fact

                        if h_list.anzahl != 0 and h_list.anzahl != None:
                            tmp_anzahl = h_list.anzahl
                        else:
                            tmp_anzahl = 0

                        if vat_included and tmp_anzahl != 0:
                            h_list.epreis = ( h_list.t_sales / tmp_anzahl) * exchg_rate / fact

                            if h_artikel.epreis1 == 0 and ((not h_cost) or (h_cost and h_cost.betrag == 0)):
                                h_list.cost = h_list.epreis * h_artikel.prozent / 100
                                
                                h_list.t_cost = h_list.t_sales * h_artikel.prozent / 100
                                t_cost = t_cost + h_list.t_cost

                        elif tmp_anzahl != 0:
                            h_list.epreis = ( h_list.t_sales / tmp_anzahl) * exchg_rate / fact1

                            if h_artikel.epreis1 == 0 and ((not h_cost) or (h_cost and h_cost.betrag == 0)):
                                h_list.cost = h_list.epreis * h_artikel.prozent / 100

                                h_list.t_cost = h_list.t_sales * h_artikel.prozent / 100
                                t_cost = t_cost + h_list.t_cost

                        else:
                            h_list.epreis =  to_decimal("0")
                            h_list.cost = to_decimal("0")
                        
                        h_list.t_cost = Decimal(f"{h_list.t_cost}").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                        # curr_recid = h_umsatz._recid
                        # h_umsatz = db_session.query(H_umsatz).filter(
                        #          (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  h_list.cost / h_list.epreis * to_decimal("100")

            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")


    def create_list(pos:bool):

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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
            fb_cost_analyst_data.append(fb_cost_analyst)


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
            fb_cost_analyst_data.append(fb_cost_analyst)

    def create_list1(pos:bool):

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

        curr_grp:int = 0

        if detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_data.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)


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
            fb_cost_analyst_data.append(fb_cost_analyst)


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
            fb_cost_analyst_data.append(fb_cost_analyst)

    def create_sub(curr_grp:int):

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data

        if curr_grp != 0:

            if st_sales != 0:
                st_margin =  to_decimal(st_cost) / to_decimal(st_sales) * to_decimal("100")

            if short_flag:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_data.append(fb_cost_analyst)

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
                fb_cost_analyst_data.append(fb_cost_analyst)

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

        nonlocal fb_cost_analyst_data, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, h_list, fb_cost_analyst
        nonlocal h_list_data, fb_cost_analyst_data


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exrate = waehrung.ankauf / waehrung.einheit

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    elif sorttype == 3:
        create_h_umsatz3()

    return generate_output()