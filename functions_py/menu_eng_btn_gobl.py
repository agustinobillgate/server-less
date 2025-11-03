#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rulita, 19/08/2025
# Recompile program e1-vhp desktop
# ticket: 0CA6DD
#--------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import Htparam, Waehrung, H_artikel, Hoteldpt, Artikel, L_artikel, H_rezept, H_umsatz, H_cost, Wgrpdep

subgr_list_data, Subgr_list = create_model("Subgr_list", {"selected":bool, "subnr":int, "bezeich":string}, {"selected": True})

def menu_eng_btn_gobl(subgr_list_data:[Subgr_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:Decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):

    prepare_cache ([Htparam, Waehrung, H_artikel, Hoteldpt, Artikel, L_artikel, H_rezept, H_cost, Wgrpdep])

    output_list_data = []
    t_anz:int = 0
    t_sales:Decimal = to_decimal("0.0")
    t_cost:Decimal = to_decimal("0.0")
    t_margin:Decimal = to_decimal("0.0")
    tt_anz:int = 0
    tt_sales:Decimal = to_decimal("0.0")
    tt_cost:Decimal = to_decimal("0.0")
    tt_margin:Decimal = to_decimal("0.0")
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
    bill_date:date = None
    htparam = waehrung = h_artikel = hoteldpt = artikel = l_artikel = h_rezept = h_umsatz = h_cost = wgrpdep = None

    subgr_list = output_list = h_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":int, "bezeich":string, "s":string})
    h_list_data, H_list = create_model("H_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "zknr":int, "grpname":string, "anzahl":int, "proz1":Decimal, "epreis":Decimal, "cost":Decimal, "margin":Decimal, "t_sales":Decimal, "t_cost":Decimal, "t_margin":Decimal, "proz2":Decimal, "tt_sales":Decimal, "tt_cost":Decimal, "tt_margin":Decimal, "proz3":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

        return {"output-list": output_list_data}

    def create_h_umsatz1():

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, price_type, double_currency, incl_service, incl_mwst, exrate, bill_date, htparam, waehrung, h_artikel, hoteldpt, artikel, l_artikel, h_rezept, h_umsatz, h_cost, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

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
        price:Decimal = to_decimal("0.0")
        h_art = None
        H_art =  create_buffer("H_art",H_artikel)
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
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                output_list.s = " " + to_string(hoteldpt.num, " 99") + to_string(hoteldpt.depart, "x(21)")
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

                    subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, to_date)],"flag": [(eq, 1)]})
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_data.append(h_list)


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

                    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    while None != h_umsatz:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                            h_list.cost =  to_decimal(h_cost.betrag)
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
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                        tt_sales =  to_decimal(tt_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        tt_anz = tt_anz + anz

                        curr_recid = h_umsatz._recid
                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = to_string("GRAND TOTAL", "x(24)")

        if short_flag:
            output_list.s = " " + to_string("GRAND TOTAL", "x(24)") + to_string(tt_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + " " + to_string("", "x(42)") + to_string(tt_sales, "->>>,>>>,>>>,>>9.99") + to_string(tt_cost, "->>>,>>>,>>>,>>9.99") + to_string(tt_margin, " >>>9.99") + to_string(100, ">>9.99")
        else:
            output_list.s = " " + to_string("GRAND TOTAL", "x(24)") + to_string(tt_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(tt_sales, " ->>,>>>,>>>,>>9") + to_string(tt_cost, "->,>>>,>>>,>>9") + " " + to_string(tt_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

    def create_h_umsatz2():

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

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
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                output_list.s = " " + to_string(hoteldpt.num, " 99") + to_string(hoteldpt.depart, "x(21)")
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

                    subgr_list = query(subgr_list_data, filters=(lambda subgr_list: subgr_list.subnr == h_artikel.zwkum and subgr_list.selected), first=True)
                    do_it = None != subgr_list

                if do_it:

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, to_date)],"flag": [(eq, 1)]})
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_data.append(h_list)


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

                    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    while None != h_umsatz:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                            h_list.cost =  to_decimal(h_cost.betrag)
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
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                        tt_sales =  to_decimal(tt_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        tt_anz = tt_anz + anz

                        curr_recid = h_umsatz._recid
                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = to_string("GRAND TOTAL", "x(24)")

        if short_flag:
            output_list.s = " " + to_string("GRAND TOTAL", "x(24)") + to_string(tt_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + " " + to_string("", "x(42)") + to_string(tt_sales, "->>>,>>>,>>>,>>9.99") + to_string(tt_cost, "->>>,>>>,>>>,>>9.99") + to_string(tt_margin, " >>>9.99") + to_string(100, ">>9.99")
        else:
            output_list.s = " " + to_string("GRAND TOTAL", "x(24)") + to_string(tt_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(tt_sales, " ->>,>>>,>>>,>>9") + to_string(tt_cost, "->,>>>,>>>,>>9") + " " + to_string(tt_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

    def create_list(pos:bool):

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

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
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("anzahl",True),("t_sales",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("t_sales",True),("anzahl",True),("bezeich",False)]):

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = to_string("T o t a l", "x(24)")

            if short_flag:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(42)") + to_string(t_sales, " ->>>,>>>,>>>,>>9.99") + to_string(t_cost, "->>>,>>>,>>>,>>9.99") + to_string(t_margin, " >>>9.99") + to_string(100, ">>9.99")
            else:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(t_sales, "->>>,>>>,>>>,>>9.99") + to_string(t_cost, "->>>,>>>,>>>,>>9.99") + " " + to_string(t_margin, " >>>9.99") + to_string(100, ">>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)


        if pos and tt_sales != 0:
            tt_margin =  to_decimal("0")

            if tt_sales != 0:
                tt_margin =  to_decimal(tt_cost) / to_decimal(tt_sales) * to_decimal("100")


    def create_list1(pos:bool):

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

        curr_grp:int = 0

        if detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = 1
                    output_list.s = " "
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                add_sub()


        elif detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = 1
                    output_list.s = " "
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                add_sub()


        elif detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = 1
                    output_list.s = " "
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                add_sub()


        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = 1
                    output_list.s = " "
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                add_sub()


        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("anzahl",True),("t_sales",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = 1
                    output_list.s = " "
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                add_sub()


        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_data, filters=(lambda h_list: h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0)), sort_by=[("zknr",False),("t_sales",True),("anzahl",True),("bezeich",False)]):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, h_list.dept)],"zknr": [(eq, h_list.zknr)]})
                    curr_grp = h_list.zknr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = 1
                    output_list.s = " "
                    output_list.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 =  to_decimal(h_list.anzahl) / to_decimal(t_anz) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_margin =  to_decimal(h_list.t_cost) / to_decimal(h_list.t_sales) * to_decimal("100")

                if t_sales != 0:
                    h_list.proz2 =  to_decimal(h_list.t_sales) / to_decimal(t_sales) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(h_list.bezeich, "x(24)")

                if short_flag:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, ">>>,>>>,>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->,>>>,>>>,>>9.99") + to_string(h_list.cost, "->>,>>>,>>9.99") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                else:
                    output_list.s = to_string(h_list.artnr, ">>>>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(h_list.anzahl, "->>>>9") + to_string(h_list.proz1, "->>9.99") + to_string(h_list.epreis, "->>>,>>>,>>>,>>9") + to_string(h_list.cost, "->,>>>,>>>,>>9") + to_string(h_list.margin, "->>>,>>9.99 ") + to_string(h_list.t_sales, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "->>>,>>>,>>>,>>9.99") + to_string(h_list.t_margin, " >>>9.99") + to_string(h_list.proz2, "->>9.99")
                add_sub()

        create_sub(curr_grp)

        if pos and t_sales != 0:
            t_margin =  to_decimal("0")

            if t_sales != 0:
                t_margin =  to_decimal(t_cost) / to_decimal(t_sales) * to_decimal("100")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = to_string("T o t a l", "x(24)")

            if short_flag:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(42)") + to_string(t_sales, " ->>>,>>>,>>>,>>9.99") + to_string(t_cost, "->>>,>>>,>>>,>>9.99") + to_string(t_margin, " >>>9.99") + to_string(100, ">>9.99")
            else:
                output_list.s = " " + to_string("T o t a l", "x(24)") + to_string(t_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(t_sales, "->>>,>>>,>>>,>>9.99") + to_string(t_cost, "->>>,>>>,>>>,>>9.99") + " " + to_string(t_margin, " >>>9.99") + to_string(100, ">>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)


        if pos and tt_sales != 0:
            tt_margin =  to_decimal("0")

            if tt_sales != 0:
                tt_margin =  to_decimal(tt_cost) / to_decimal(tt_sales) * to_decimal("100")


    def create_sub(curr_grp:int):

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

        if curr_grp != 0:

            if st_sales != 0:
                st_margin =  to_decimal(st_cost) / to_decimal(st_sales) * to_decimal("100")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = 2
            output_list.bezeich = "S u b T o t a l"
            output_list.s = to_string(" ", "x(9)") +\
                    to_string("S u b T o t a l", "x(24)") +\
                    to_string(s_anzahl, ">>>,>>>,>>9") + " " +\
                    to_string(s_proz1, ">>9.99") +\
                    to_string(" ", "x(42)") +\
                    to_string(st_sales, " ->>>,>>>,>>>,>>9.99") +\
                    to_string(st_cost, "->>>,>>>,>>>,>>9.99") +\
                    to_string(st_margin, " ->>>,>>9.99") + " " +\
                    to_string(st_proz2, "->>9.99")


            s_anzahl = 0
            s_proz1 =  to_decimal("0")
            st_sales =  to_decimal("0")
            st_cost =  to_decimal("0")
            st_margin =  to_decimal("0")
            st_proz2 =  to_decimal("0")


    def add_sub():

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales =  to_decimal(st_sales) + to_decimal(h_list.t_sales)
        st_cost =  to_decimal(st_cost) + to_decimal(h_list.t_cost)
        s_proz1 =  to_decimal(s_proz1) + to_decimal(h_list.proz1)
        st_proz2 =  to_decimal(st_proz2) + to_decimal(h_list.proz2)


    def create_h_umsatz3():

        nonlocal output_list_data, t_anz, t_sales, t_cost, t_margin, tt_anz, tt_sales, tt_cost, tt_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal sorttype, from_dept, to_dept, dstore, ldry_dept, all_sub, from_date, to_date, fact1, exchg_rate, vat_included, mi_subgrp, detailed, curr_sort, short_flag


        nonlocal subgr_list, output_list, h_list
        nonlocal output_list_data, h_list_data

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
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
                output_list.s = " "
            dept = hoteldpt.num

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.zwkum, h_artikel.artnr, h_artikel.departement, h_artikel.epreis1, h_artikel.prozent, h_artikel.bezeich, h_artikel._recid, artikel.artnr, artikel.departement, artikel._recid in db_session.query(H_artikel.zwkum, H_artikel.artnr, H_artikel.departement, H_artikel.epreis1, H_artikel.prozent, H_artikel.bezeich, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.umsatzart == 4) & (Artikel.endkum != disc_nr)).filter(
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

                    h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, to_date)],"flag": [(eq, 1)]})
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat =  to_decimal(vat) + to_decimal(vat2)


                    h_list = H_list()
                    h_list_data.append(h_list)


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

                    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(ge, from_date),(le, to_date)]})
                    while None != h_umsatz:
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)


                        anz = h_umsatz.anzahl
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(anz) * to_decimal(h_cost.betrag)
                            h_list.cost =  to_decimal(h_cost.betrag)
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
                        tt_cost =  to_decimal(tt_cost) + to_decimal(cost)
                        tt_sales =  to_decimal(tt_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        tt_anz = tt_anz + anz

                        curr_recid = h_umsatz._recid
                        h_umsatz = db_session.query(H_umsatz).filter(
                                 (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date) & (H_umsatz._recid > curr_recid)).first()

                    if h_list.epreis != 0:
                        h_list.margin =  to_decimal(h_list.cost) / to_decimal(h_list.epreis) * to_decimal("100")
            create_list(pos)
            t_anz = 0
            t_sales =  to_decimal("0")
            t_cost =  to_decimal("0")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = to_string("GRAND TOTAL", "x(24)")

        if short_flag:
            output_list.s = " " + to_string("GRAND TOTAL", "x(24)") + to_string(tt_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + " " + to_string("", "x(42)") + to_string(tt_sales, "->>>,>>>,>>>,>>9.99") + to_string(tt_cost, "->>>,>>>,>>>,>>9.99") + to_string(tt_margin, " >>>9.99") + to_string(100, ">>9.99")
        else:
            output_list.s = " " + to_string("GRAND TOTAL", "x(24)") + to_string(tt_anz, ">>>,>>>,>>9") + " " + to_string(100, ">>9.99") + to_string("", "x(36)") + " " + to_string(tt_sales, " ->>,>>>,>>>,>>9") + to_string(tt_cost, "->,>>>,>>>,>>9") + " " + to_string(tt_margin, " ->>>,>>9.99 ") + to_string(100, ">>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    elif sorttype == 3:
        create_h_umsatz3()

    return generate_output()