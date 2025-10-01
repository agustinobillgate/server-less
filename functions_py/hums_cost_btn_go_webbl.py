#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_artikel, Hoteldpt, Umsatz, Artikel, H_compli, H_cost, H_journal, H_umsatz, Exrate

def hums_cost_btn_go_webbl(sorttype:int, detailed:bool, from_dept:int, to_dept:int, from_date:date, to_date:date, fact1:int, mi_compli_checked:bool):

    prepare_cache ([Htparam, Waehrung, H_artikel, Hoteldpt, Umsatz, Artikel, H_compli, H_cost, H_journal, H_umsatz, Exrate])

    output_list_data = []
    exchg_rate:Decimal = 1
    double_currency:bool = False
    foreign_nr:int = 0
    dd_gsales:Decimal = to_decimal("0.0")
    dd_gcompli:Decimal = to_decimal("0.0")
    dd_gcost:Decimal = to_decimal("0.0")
    dd_ncost:Decimal = to_decimal("0.0")
    tot_gsales:Decimal = to_decimal("0.0")
    tot_gcompli:Decimal = to_decimal("0.0")
    tot_gcost:Decimal = to_decimal("0.0")
    tot_ncost:Decimal = to_decimal("0.0")
    dd_anz:int = 0
    dd_comanz:int = 0
    tm_anz:int = 0
    tm_comanz:int = 0
    htparam = waehrung = h_artikel = hoteldpt = umsatz = artikel = h_compli = h_cost = h_journal = h_umsatz = exrate = None

    h_list = output_list = None

    h_list_data, H_list = create_model("H_list", {"artnr":int, "dept":int, "num":int, "depart":string, "anz":int, "m_anz":int, "sales":Decimal, "t_sales":Decimal, "comanz":int, "compli":Decimal, "t_compli":Decimal, "t_comanz":int, "cost":Decimal, "t_cost":Decimal, "ncost":Decimal, "t_ncost":Decimal, "proz":Decimal, "t_proz":Decimal, "anz_cost":int, "manz_cost":int})
    output_list_data, Output_list = create_model("Output_list", {"num":int, "bezeich":string, "anz":int, "sales":Decimal, "ncost":Decimal, "comanz":int, "compli":Decimal, "cost":Decimal, "proz":Decimal, "m_anz":int, "t_sales":Decimal, "t_ncost":Decimal, "m_comanz":int, "t_compli":Decimal, "t_cost":Decimal, "t_proz":Decimal, "anz_cost":int, "manz_cost":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, dd_anz, dd_comanz, tm_anz, tm_comanz, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        return {"output-list": output_list_data}


    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)


    def create_h_umsatz1():

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, dd_anz, dd_comanz, tm_anz, tm_comanz, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        gsales:Decimal = to_decimal("0.0")
        t_gsales:Decimal = to_decimal("0.0")
        gcompli:Decimal = to_decimal("0.0")
        t_gcompli:Decimal = to_decimal("0.0")
        gcost:Decimal = to_decimal("0.0")
        t_gcost:Decimal = to_decimal("0.0")
        ncost:Decimal = to_decimal("0.0")
        t_ncost:Decimal = to_decimal("0.0")
        proz:Decimal = to_decimal("0.0")
        t_proz:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        m_endkum:int = 0
        t_anz:int = 0
        t_m_anz:int = 0
        t_comanz:int = 0
        t_m_comanz:int = 0
        t_anz_cost:int = 0
        t_manz_cost:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        dd_gsales =  to_decimal("0")
        dd_gcompli =  to_decimal("0")
        dd_gcost =  to_decimal("0")
        dd_ncost =  to_decimal("0")
        tot_gsales =  to_decimal("0")
        tot_gcompli =  to_decimal("0")
        tot_gcost =  to_decimal("0")
        tot_ncost =  to_decimal("0")
        output_list_data.clear()
        h_list_data.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "** Food **"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 273)]})
        m_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True

            if pos:
                for curr_datum in date_range(from_date,to_date) :

                    if double_currency:
                        find_exrate(curr_datum)

                        if exrate:
                            rate =  to_decimal(exrate.betrag)
                        else:
                            rate =  to_decimal(exchg_rate)
                    rate =  to_decimal(rate) / to_decimal(fact1)

                    if curr_datum == from_date:
                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = {}
                    artikel = Artikel()
                    umsatz = Umsatz()
                    for artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid, umsatz.datum, umsatz.anzahl, umsatz.betrag, umsatz._recid in db_session.query(Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid, Umsatz.datum, Umsatz.anzahl, Umsatz.betrag, Umsatz._recid).join(Umsatz,(Umsatz.artnr == Artikel.artnr) & (Umsatz.departement == Artikel.departement) & (Umsatz.datum == curr_datum)).filter(
                             (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).order_by(Artikel._recid).all():
                        if artikel_obj_list.get(artikel._recid):
                            continue
                        else:
                            artikel_obj_list[artikel._recid] = True


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if umsatz.datum == to_date:
                            h_list.anz = h_list.anz + umsatz.anzahl
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            gsales =  to_decimal(gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        h_list.m_anz = h_list.m_anz + umsatz.anzahl
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        t_gsales =  to_decimal(t_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    h_compli_obj_list = {}
                    h_compli = H_compli()
                    h_art = H_artikel()
                    for h_compli.departement, h_compli.artnr, h_compli.datum, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid in db_session.query(H_compli.departement, H_compli.artnr, H_compli.datum, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == hoteldpt.num) & (H_compli.datum == curr_datum) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli_obj_list.get(h_compli._recid):
                            continue
                        else:
                            h_compli_obj_list[h_compli._recid] = True

                        h_artikel = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)]})

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                        if (artikel.endkum == f_endkum or artikel.endkum == m_endkum or artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                            else:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                            if h_compli.datum == to_date:
                                h_list.compli =  to_decimal(h_list.compli) + to_decimal(cost)
                                h_list.comanz = h_list.comanz + h_compli.anzahl
                                gcompli =  to_decimal(gcompli) + to_decimal(cost)
                                dd_gcompli =  to_decimal(dd_gcompli) + to_decimal(cost)
                            h_list.t_compli =  to_decimal(h_list.t_compli) + to_decimal(cost)
                            h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                            t_gcompli =  to_decimal(t_gcompli) + to_decimal(cost)
                            tot_gcompli =  to_decimal(tot_gcompli) + to_decimal(cost)

                    h_journal_obj_list = {}
                    h_journal = H_journal()
                    h_art = H_artikel()
                    artikel = Artikel()
                    for h_journal.artnr, h_journal.departement, h_journal.bill_datum, h_journal.anzahl, h_journal.epreis, h_journal._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid, artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid in db_session.query(H_journal.artnr, H_journal.departement, H_journal.bill_datum, H_journal.anzahl, H_journal.epreis, H_journal._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid, Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid).join(H_art,(H_art.artnr == H_journal.artnr) & (H_art.departement == H_journal.departement) & (H_art.artart == 0)).join(Artikel,(Artikel.artnr == H_art.artnrfront) & (Artikel.departement == H_art.departement) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).filter(
                             (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_datum)).order_by(H_journal._recid).all():
                        if h_journal_obj_list.get(h_journal._recid):
                            continue
                        else:
                            h_journal_obj_list[h_journal._recid] = True


                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"datum": [(eq, h_journal.bill_datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(rate) * to_decimal(h_art.prozent) / to_decimal("100")

                        if h_journal.bill_datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            h_list.anz_cost = h_list.anz_cost + h_journal.anzahl
                            gcost =  to_decimal(gcost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        h_list.manz_cost = h_list.manz_cost + h_journal.anzahl
                        t_gcost =  to_decimal(t_gcost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

        for h_list in query(h_list_data):
            h_list.ncost =  to_decimal(h_list.cost) - to_decimal(h_list.compli)
            ncost =  to_decimal(ncost) + to_decimal(h_list.ncost)
            dd_ncost =  to_decimal(dd_ncost) + to_decimal(h_list.ncost)
            h_list.t_ncost =  to_decimal(h_list.t_cost) - to_decimal(h_list.t_compli)
            t_ncost =  to_decimal(t_ncost) + to_decimal(h_list.t_ncost)
            tot_ncost =  to_decimal(tot_ncost) + to_decimal(h_list.t_ncost)

            if h_list.sales != 0:
                h_list.proz =  to_decimal(h_list.ncost) / to_decimal(h_list.sales) * to_decimal("100")

            if h_list.t_sales != 0:
                h_list.t_proz =  to_decimal(h_list.t_ncost) / to_decimal(h_list.t_sales) * to_decimal("100")
            t_anz = t_anz + h_list.anz
            t_m_anz = t_m_anz + h_list.m_anz
            t_comanz = t_comanz + h_list.comanz
            t_m_comanz = t_m_comanz + h_list.t_comanz
            t_anz_cost = t_anz_cost + h_list.anz_cost
            t_manz_cost = t_manz_cost + h_list.manz_cost


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.num = h_list.num
            # output_list.bezeich = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
            output_list.bezeich = to_string(h_list.num, "99") + " " + format_fixed_length(h_list.depart, 20)
            output_list.anz = h_list.anz
            output_list.sales =  to_decimal(h_list.sales)
            output_list.ncost =  to_decimal(h_list.ncost)
            output_list.comanz = h_list.comanz
            output_list.compli =  to_decimal(h_list.compli)
            output_list.cost =  to_decimal(h_list.cost)
            output_list.proz =  to_decimal(h_list.proz)
            output_list.m_anz = h_list.m_anz
            output_list.t_sales =  to_decimal(h_list.t_sales)
            output_list.t_ncost =  to_decimal(h_list.t_ncost)
            output_list.m_comanz = h_list.t_comanz
            output_list.t_compli =  to_decimal(h_list.t_compli)
            output_list.t_cost =  to_decimal(h_list.t_cost)
            output_list.t_proz =  to_decimal(h_list.t_proz)
            output_list.anz_cost = h_list.anz_cost
            output_list.manz_cost = h_list.manz_cost

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "T O T A L"
        output_list.sales =  to_decimal(gsales)
        output_list.ncost =  to_decimal(ncost)
        output_list.compli =  to_decimal(gcompli)
        output_list.cost =  to_decimal(gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_sales =  to_decimal(t_gsales)
        output_list.t_ncost =  to_decimal(t_ncost)
        output_list.t_compli =  to_decimal(t_gcompli)
        output_list.t_cost =  to_decimal(t_gcost)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = t_anz
        output_list.m_anz = t_m_anz
        output_list.comanz = t_comanz
        output_list.m_comanz = t_m_comanz
        output_list.anz_cost = t_anz_cost
        output_list.manz_cost = t_manz_cost


        dd_anz = dd_anz + t_anz
        dd_comanz = dd_comanz + t_comanz
        tm_anz = tm_anz + t_m_anz
        tm_comanz = tm_comanz + t_m_comanz


    def create_h_umsatz2():

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, dd_anz, dd_comanz, tm_anz, tm_comanz, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        gsales:Decimal = to_decimal("0.0")
        t_gsales:Decimal = to_decimal("0.0")
        gcompli:Decimal = to_decimal("0.0")
        t_gcompli:Decimal = to_decimal("0.0")
        gcost:Decimal = to_decimal("0.0")
        t_gcost:Decimal = to_decimal("0.0")
        ncost:Decimal = to_decimal("0.0")
        t_ncost:Decimal = to_decimal("0.0")
        proz:Decimal = to_decimal("0.0")
        t_proz:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        t_anz:int = 0
        t_m_anz:int = 0
        t_comanz:int = 0
        t_m_comanz:int = 0
        t_anz_cost:int = 0
        t_manz_cost:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_data.clear()
        h_list_data.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "** Beverage **"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True

            if pos:
                for curr_datum in date_range(from_date,to_date) :

                    if double_currency:
                        find_exrate(curr_datum)

                        if exrate:
                            rate =  to_decimal(exrate.betrag)
                        else:
                            rate =  to_decimal(exchg_rate)
                    rate =  to_decimal(rate) / to_decimal(fact1)

                    if curr_datum == from_date:
                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = {}
                    artikel = Artikel()
                    umsatz = Umsatz()
                    for artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid, umsatz.datum, umsatz.anzahl, umsatz.betrag, umsatz._recid in db_session.query(Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid, Umsatz.datum, Umsatz.anzahl, Umsatz.betrag, Umsatz._recid).join(Umsatz,(Umsatz.artnr == Artikel.artnr) & (Umsatz.departement == Artikel.departement) & (Umsatz.datum == curr_datum)).filter(
                             (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).order_by(Artikel._recid).all():
                        if artikel_obj_list.get(artikel._recid):
                            continue
                        else:
                            artikel_obj_list[artikel._recid] = True


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if umsatz.datum == to_date:
                            h_list.anz = h_list.anz + umsatz.anzahl
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            gsales =  to_decimal(gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        h_list.m_anz = h_list.m_anz + umsatz.anzahl
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        t_gsales =  to_decimal(t_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    h_compli_obj_list = {}
                    h_compli = H_compli()
                    h_art = H_artikel()
                    for h_compli.departement, h_compli.artnr, h_compli.datum, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid in db_session.query(H_compli.departement, H_compli.artnr, H_compli.datum, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == hoteldpt.num) & (H_compli.datum == curr_datum) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli_obj_list.get(h_compli._recid):
                            continue
                        else:
                            h_compli_obj_list[h_compli._recid] = True

                        h_artikel = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)]})

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                        if (artikel.endkum == b_endkum or artikel.umsatzart == 6):
                            cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                            else:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                            if h_compli.datum == to_date:
                                h_list.compli =  to_decimal(h_list.compli) + to_decimal(cost)
                                h_list.comanz = h_list.comanz + h_compli.anzahl
                                gcompli =  to_decimal(gcompli) + to_decimal(cost)
                                dd_gcompli =  to_decimal(dd_gcompli) + to_decimal(cost)
                            h_list.t_compli =  to_decimal(h_list.t_compli) + to_decimal(cost)
                            h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                            t_gcompli =  to_decimal(t_gcompli) + to_decimal(cost)
                            tot_gcompli =  to_decimal(tot_gcompli) + to_decimal(cost)

                    h_journal_obj_list = {}
                    h_journal = H_journal()
                    h_art = H_artikel()
                    artikel = Artikel()
                    for h_journal.artnr, h_journal.departement, h_journal.bill_datum, h_journal.anzahl, h_journal.epreis, h_journal._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid, artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid in db_session.query(H_journal.artnr, H_journal.departement, H_journal.bill_datum, H_journal.anzahl, H_journal.epreis, H_journal._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid, Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid).join(H_art,(H_art.artnr == H_journal.artnr) & (H_art.departement == H_journal.departement) & (H_art.artart == 0)).join(Artikel,(Artikel.artnr == H_art.artnrfront) & (Artikel.departement == H_art.departement) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).filter(
                             (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_datum)).order_by(H_journal._recid).all():
                        if h_journal_obj_list.get(h_journal._recid):
                            continue
                        else:
                            h_journal_obj_list[h_journal._recid] = True


                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"datum": [(eq, h_journal.bill_datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(rate) * to_decimal(h_art.prozent) / to_decimal("100")

                        if h_journal.bill_datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            h_list.anz_cost = h_list.anz_cost + h_journal.anzahl
                            gcost =  to_decimal(gcost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.manz_cost = h_list.manz_cost + h_journal.anzahl
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        t_gcost =  to_decimal(t_gcost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

        for h_list in query(h_list_data):
            h_list.ncost =  to_decimal(h_list.cost) - to_decimal(h_list.compli)
            ncost =  to_decimal(ncost) + to_decimal(h_list.ncost)
            dd_ncost =  to_decimal(dd_ncost) + to_decimal(h_list.ncost)
            h_list.t_ncost =  to_decimal(h_list.t_cost) - to_decimal(h_list.t_compli)
            t_ncost =  to_decimal(t_ncost) + to_decimal(h_list.t_ncost)
            tot_ncost =  to_decimal(tot_ncost) + to_decimal(h_list.t_ncost)

            if h_list.sales != 0:
                h_list.proz =  to_decimal(h_list.ncost) / to_decimal(h_list.sales) * to_decimal("100")

            if h_list.t_sales != 0:
                h_list.t_proz =  to_decimal(h_list.t_ncost) / to_decimal(h_list.t_sales) * to_decimal("100")
            t_anz = t_anz + h_list.anz
            t_m_anz = t_m_anz + h_list.m_anz
            t_comanz = t_comanz + h_list.comanz
            t_m_comanz = t_m_comanz + h_list.t_comanz
            t_anz_cost = t_anz_cost + h_list.anz_cost
            t_manz_cost = t_manz_cost + h_list.manz_cost


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.num = h_list.num
            # output_list.bezeich = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
            output_list.bezeich = to_string(h_list.num, "99") + " " + format_fixed_length(h_list.depart, 20)
            output_list.anz = h_list.anz
            output_list.sales =  to_decimal(h_list.sales)
            output_list.ncost =  to_decimal(h_list.ncost)
            output_list.comanz = h_list.comanz
            output_list.compli =  to_decimal(h_list.compli)
            output_list.cost =  to_decimal(h_list.cost)
            output_list.proz =  to_decimal(h_list.proz)
            output_list.m_anz = h_list.m_anz
            output_list.t_sales =  to_decimal(h_list.t_sales)
            output_list.t_ncost =  to_decimal(h_list.t_ncost)
            output_list.m_comanz = h_list.t_comanz
            output_list.t_compli =  to_decimal(h_list.t_compli)
            output_list.t_cost =  to_decimal(h_list.t_cost)
            output_list.t_proz =  to_decimal(h_list.t_proz)
            output_list.anz_cost = h_list.anz_cost
            output_list.manz_cost = h_list.manz_cost

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "T O T A L"
        output_list.sales =  to_decimal(gsales)
        output_list.ncost =  to_decimal(ncost)
        output_list.compli =  to_decimal(gcompli)
        output_list.cost =  to_decimal(gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_sales =  to_decimal(t_gsales)
        output_list.t_ncost =  to_decimal(t_ncost)
        output_list.t_compli =  to_decimal(t_gcompli)
        output_list.t_cost =  to_decimal(t_gcost)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = t_anz
        output_list.m_anz = t_m_anz
        output_list.comanz = t_comanz
        output_list.m_comanz = t_m_comanz
        output_list.anz_cost = t_anz_cost
        output_list.manz_cost = t_manz_cost


        dd_anz = dd_anz + t_anz
        dd_comanz = dd_comanz + t_comanz
        tm_anz = tm_anz + t_m_anz
        tm_comanz = tm_comanz + t_m_comanz


    def create_h_umsatz3():

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, dd_anz, dd_comanz, tm_anz, tm_comanz, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        gsales:Decimal = to_decimal("0.0")
        t_gsales:Decimal = to_decimal("0.0")
        gcompli:Decimal = to_decimal("0.0")
        t_gcompli:Decimal = to_decimal("0.0")
        gcost:Decimal = to_decimal("0.0")
        t_gcost:Decimal = to_decimal("0.0")
        ncost:Decimal = to_decimal("0.0")
        t_ncost:Decimal = to_decimal("0.0")
        proz:Decimal = to_decimal("0.0")
        t_proz:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        t_anz:int = 0
        t_m_anz:int = 0
        t_comanz:int = 0
        t_m_comanz:int = 0
        t_anz_cost:int = 0
        t_manz_cost:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_data.clear()
        h_list_data.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "** Others **"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                pos = True

            if pos:
                for curr_datum in date_range(from_date,to_date) :

                    if double_currency:
                        find_exrate(curr_datum)

                        if exrate:
                            rate =  to_decimal(exrate.betrag)
                        else:
                            rate =  to_decimal(exchg_rate)
                    rate =  to_decimal(rate) / to_decimal(fact1)

                    if curr_datum == from_date:
                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = {}
                    artikel = Artikel()
                    umsatz = Umsatz()
                    for artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid, umsatz.datum, umsatz.anzahl, umsatz.betrag, umsatz._recid in db_session.query(Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid, Umsatz.datum, Umsatz.anzahl, Umsatz.betrag, Umsatz._recid).join(Umsatz,(Umsatz.artnr == Artikel.artnr) & (Umsatz.departement == Artikel.departement) & (Umsatz.datum == curr_datum)).filter(
                             (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & (Artikel.umsatzart == 4)).order_by(Artikel._recid).all():
                        if artikel_obj_list.get(artikel._recid):
                            continue
                        else:
                            artikel_obj_list[artikel._recid] = True


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if umsatz.datum == to_date:
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            h_list.anz = h_list.anz + umsatz.anzahl
                            gsales =  to_decimal(gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        h_list.m_anz = h_list.m_anz + umsatz.anzahl
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        t_gsales =  to_decimal(t_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    h_compli_obj_list = {}
                    h_compli = H_compli()
                    h_art = H_artikel()
                    for h_compli.departement, h_compli.artnr, h_compli.datum, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid in db_session.query(H_compli.departement, H_compli.artnr, H_compli.datum, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == hoteldpt.num) & (H_compli.datum == curr_datum) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli_obj_list.get(h_compli._recid):
                            continue
                        else:
                            h_compli_obj_list[h_compli._recid] = True

                        h_artikel = get_cache (H_artikel, {"departement": [(eq, h_compli.departement)],"artnr": [(eq, h_compli.artnr)]})

                        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                        if artikel.umsatzart == 4:
                            cost =  to_decimal("0")

                            h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                            if h_cost and h_cost.betrag != 0:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                            else:
                                cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                            if h_compli.datum == to_date:
                                h_list.compli =  to_decimal(h_list.compli) + to_decimal(cost)
                                h_list.comanz = h_list.comanz + h_compli.anzahl
                                gcompli =  to_decimal(gcompli) + to_decimal(cost)
                                dd_gcompli =  to_decimal(dd_gcompli) + to_decimal(cost)
                            h_list.t_compli =  to_decimal(h_list.t_compli) + to_decimal(cost)
                            h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                            t_gcompli =  to_decimal(t_gcompli) + to_decimal(cost)
                            tot_gcompli =  to_decimal(tot_gcompli) + to_decimal(cost)

                    h_journal_obj_list = {}
                    h_journal = H_journal()
                    h_art = H_artikel()
                    artikel = Artikel()
                    for h_journal.artnr, h_journal.departement, h_journal.bill_datum, h_journal.anzahl, h_journal.epreis, h_journal._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid, artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid in db_session.query(H_journal.artnr, H_journal.departement, H_journal.bill_datum, H_journal.anzahl, H_journal.epreis, H_journal._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid, Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid).join(H_art,(H_art.artnr == H_journal.artnr) & (H_art.departement == H_journal.departement) & (H_art.artart == 0)).join(Artikel,(Artikel.artnr == H_art.artnrfront) & (Artikel.departement == H_art.departement) & (Artikel.umsatzart == 4)).filter(
                             (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_datum)).order_by(H_journal._recid).all():
                        if h_journal_obj_list.get(h_journal._recid):
                            continue
                        else:
                            h_journal_obj_list[h_journal._recid] = True


                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"datum": [(eq, h_journal.bill_datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(rate) * to_decimal(h_art.prozent) / to_decimal("100")

                        if h_journal.bill_datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            h_list.anz_cost = h_list.anz_cost + h_journal.anzahl
                            gcost =  to_decimal(gcost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        h_list.manz_cost = h_list.manz_cost + h_journal.anzahl
                        t_gcost =  to_decimal(t_gcost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

        for h_list in query(h_list_data):
            h_list.ncost =  to_decimal(h_list.cost) - to_decimal(h_list.compli)
            ncost =  to_decimal(ncost) + to_decimal(h_list.ncost)
            dd_ncost =  to_decimal(dd_ncost) + to_decimal(h_list.ncost)
            h_list.t_ncost =  to_decimal(h_list.t_cost) - to_decimal(h_list.t_compli)
            t_ncost =  to_decimal(t_ncost) + to_decimal(h_list.t_ncost)
            tot_ncost =  to_decimal(tot_ncost) + to_decimal(h_list.t_ncost)

            if h_list.sales != 0:
                h_list.proz =  to_decimal(h_list.ncost) / to_decimal(h_list.sales) * to_decimal("100")

            if h_list.t_sales != 0:
                h_list.t_proz =  to_decimal(h_list.t_ncost) / to_decimal(h_list.t_sales) * to_decimal("100")
            t_anz = t_anz + h_list.anz
            t_m_anz = t_m_anz + h_list.m_anz
            t_comanz = t_comanz + h_list.comanz
            t_m_comanz = t_m_comanz + h_list.t_comanz
            t_anz_cost = t_anz_cost + h_list.anz_cost
            t_manz_cost = t_manz_cost + h_list.manz_cost


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.num = h_list.num
            # output_list.bezeich = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
            output_list.bezeich = to_string(h_list.num, "99") + " " + format_fixed_length(h_list.depart, 20)
            output_list.anz = h_list.anz
            output_list.sales =  to_decimal(h_list.sales)
            output_list.ncost =  to_decimal(h_list.ncost)
            output_list.comanz = h_list.comanz
            output_list.compli =  to_decimal(h_list.compli)
            output_list.cost =  to_decimal(h_list.cost)
            output_list.proz =  to_decimal(h_list.proz)
            output_list.m_anz = h_list.m_anz
            output_list.t_sales =  to_decimal(h_list.t_sales)
            output_list.t_ncost =  to_decimal(h_list.t_ncost)
            output_list.m_comanz = h_list.t_comanz
            output_list.t_compli =  to_decimal(h_list.t_compli)
            output_list.t_cost =  to_decimal(h_list.t_cost)
            output_list.t_proz =  to_decimal(h_list.t_proz)
            output_list.anz_cost = h_list.anz_cost
            output_list.manz_cost = h_list.manz_cost

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "T O T A L"
        output_list.sales =  to_decimal(gsales)
        output_list.ncost =  to_decimal(ncost)
        output_list.compli =  to_decimal(gcompli)
        output_list.cost =  to_decimal(gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_sales =  to_decimal(t_gsales)
        output_list.t_ncost =  to_decimal(t_ncost)
        output_list.t_compli =  to_decimal(t_gcompli)
        output_list.t_cost =  to_decimal(t_gcost)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = t_anz
        output_list.m_anz = t_m_anz
        output_list.comanz = t_comanz
        output_list.m_comanz = t_m_comanz
        output_list.anz_cost = t_anz_cost
        output_list.manz_cost = t_manz_cost


        dd_anz = dd_anz + t_anz
        dd_comanz = dd_comanz + t_comanz
        tm_anz = tm_anz + t_m_anz
        tm_comanz = tm_comanz + t_m_comanz

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "GRAND TOTAL"
            output_list.sales =  to_decimal(dd_gsales)
            output_list.ncost =  to_decimal(dd_ncost)
            output_list.compli =  to_decimal(dd_gcompli)
            output_list.cost =  to_decimal(dd_gcost)
            output_list.t_sales =  to_decimal(tot_gsales)
            output_list.t_ncost =  to_decimal(tot_ncost)
            output_list.t_compli =  to_decimal(tot_gcompli)
            output_list.t_cost =  to_decimal(tot_gcost)
            output_list.anz = dd_anz
            output_list.comanz = dd_comanz
            output_list.m_anz = tm_anz
            output_list.m_comanz = tm_comanz


    def create_h_umsatz11():

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        gsales:Decimal = to_decimal("0.0")
        t_gsales:Decimal = to_decimal("0.0")
        gcompli:Decimal = to_decimal("0.0")
        t_gcompli:Decimal = to_decimal("0.0")
        gcost:Decimal = to_decimal("0.0")
        t_gcost:Decimal = to_decimal("0.0")
        ncost:Decimal = to_decimal("0.0")
        t_ncost:Decimal = to_decimal("0.0")
        proz:Decimal = to_decimal("0.0")
        t_proz:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        m_endkum:int = 0
        dd_gsales:Decimal = to_decimal("0.0")
        dd_gcompli:Decimal = to_decimal("0.0")
        dd_gcost:Decimal = to_decimal("0.0")
        dd_ncost:Decimal = to_decimal("0.0")
        tot_gsales:Decimal = to_decimal("0.0")
        tot_gcompli:Decimal = to_decimal("0.0")
        tot_gcost:Decimal = to_decimal("0.0")
        tot_ncost:Decimal = to_decimal("0.0")
        dd_anz:int = 0
        dd_comanz:int = 0
        tm_anz:int = 0
        tm_comanz:int = 0
        t_anz:int = 0
        t_m_anz:int = 0
        t_comanz:int = 0
        t_m_comanz:int = 0
        t_anz_cost:int = 0
        t_manz_cost:int = 0
        ind:int = 0
        price_decimal:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        output_list_data.clear()
        h_list_data.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "** Food **"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 273)]})
        m_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                h_list = H_list()
                h_list_data.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.artnrfront, h_artikel.departement, h_artikel.prozent, h_artikel.bezeich, h_artikel.artnr, h_artikel._recid, artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid in db_session.query(H_artikel.artnrfront, H_artikel.departement, H_artikel.prozent, H_artikel.bezeich, H_artikel.artnr, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.depart = h_artikel.bezeich

                    for h_umsatz in db_session.query(H_umsatz).filter(
                             (H_umsatz.departement == h_artikel.departement) & (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).order_by(H_umsatz._recid).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if double_currency:
                            find_exrate(h_umsatz.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        rate =  to_decimal(rate) / to_decimal(fact1)

                        if h_umsatz.datum == to_date:

                            if mi_compli_checked:
                                h_list.anz = h_list.anz + h_umsatz.anzahl
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                        if mi_compli_checked:
                            h_list.m_anz = h_list.m_anz + h_umsatz.anzahl
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_umsatz.artnr)],"departement": [(eq, h_umsatz.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)

                            if not mi_compli_checked:

                                if h_umsatz.datum == to_date:
                                    h_list.anz = h_list.anz + h_cost.anzahl
                                h_list.m_anz = h_list.m_anz + h_cost.anzahl
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                     (H_journal.artnr == h_umsatz.artnr) & (H_journal.departement == h_umsatz.departement) & (H_journal.bill_datum == h_umsatz.datum)).order_by(H_journal._recid).all():
                                cost =  to_decimal(cost) + to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) * to_decimal(rate) / to_decimal("100")

                                if not mi_compli_checked:

                                    if h_umsatz.datum == to_date:
                                        h_list.anz = h_list.anz + h_journal.anzahl
                                    h_list.m_anz = h_list.m_anz + h_journal.anzahl

                        if h_umsatz.datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

                    h_compli_obj_list = {}
                    h_compli = H_compli()
                    h_art = H_artikel()
                    for h_compli.departement, h_compli.artnr, h_compli.datum, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid in db_session.query(H_compli.departement, H_compli.artnr, H_compli.datum, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == h_artikel.departement) & (H_compli.artnr == h_artikel.artnr) & (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli_obj_list.get(h_compli._recid):
                            continue
                        else:
                            h_compli_obj_list[h_compli._recid] = True

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                        if h_compli.datum == to_date:
                            h_list.compli =  to_decimal(h_list.compli) + to_decimal(cost)
                            h_list.comanz = h_list.comanz + h_compli.anzahl
                            dd_gcompli =  to_decimal(dd_gcompli) + to_decimal(cost)

                            if not mi_compli_checked:
                                h_list.anz = h_list.anz - h_compli.anzahl
                        h_list.t_compli =  to_decimal(h_list.t_compli) + to_decimal(cost)
                        h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                        tot_gcompli =  to_decimal(tot_gcompli) + to_decimal(cost)

                        if not mi_compli_checked:
                            h_list.m_anz = h_list.m_anz - h_compli.anzahl

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger
        ind = 0
        gsales =  to_decimal("0")
        ncost =  to_decimal("0")
        gcompli =  to_decimal("0")
        gcost =  to_decimal("0")
        t_gsales =  to_decimal("0")
        t_gcompli =  to_decimal("0")
        t_gcost =  to_decimal("0")
        t_ncost =  to_decimal("0")
        t_proz =  to_decimal("0")

        for h_list in query(h_list_data, filters=(lambda h_list: h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

                    if t_gsales != 0:
                        t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.bezeich = "T O T A L"
                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz
                    output_list.sales =  to_decimal(gsales)
                    output_list.ncost =  to_decimal(ncost)
                    output_list.compli =  to_decimal(gcompli)
                    output_list.cost =  to_decimal(gcost)
                    output_list.proz =  to_decimal(proz)
                    output_list.t_proz =  to_decimal(t_proz)
                    output_list.anz = t_anz
                    output_list.m_anz = t_m_anz
                    output_list.comanz = t_comanz
                    output_list.m_comanz = t_m_comanz
                    output_list.anz_cost = t_anz_cost
                    output_list.manz_cost = t_manz_cost

                    if t_gsales >= 0:
                        output_list.t_sales =  to_decimal(t_gsales)
                        output_list.t_ncost =  to_decimal(t_ncost)
                        output_list.t_compli =  to_decimal(t_gcompli)
                        output_list.t_cost =  to_decimal(t_gcost)


                ncost =  to_decimal("0")
                gsales =  to_decimal("0")
                gcompli =  to_decimal("0")
                gcost =  to_decimal("0")
                t_gsales =  to_decimal("0")
                t_gcompli =  to_decimal("0")
                t_gcost =  to_decimal("0")
                t_ncost =  to_decimal("0")
                t_proz =  to_decimal("0")
                dd_anz = dd_anz + t_anz
                dd_comanz = dd_comanz + t_comanz
                tm_anz = tm_anz + t_m_anz
                tm_comanz = tm_comanz + t_m_comanz


                t_anz = 0
                t_m_anz = 0
                t_comanz = 0
                t_m_comanz = 0
                t_anz_cost = 0
                t_manz_cost = 0


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.num = h_list.num
                output_list.bezeich = h_list.depart
                output_list.anz = h_list.anz
                output_list.comanz = h_list.comanz
                output_list.m_anz = h_list.m_anz
                output_list.m_comanz = h_list.comanz


            else:
                gsales =  to_decimal(gsales) + to_decimal(h_list.sales)
                gcost =  to_decimal(gcost) + to_decimal(h_list.cost)
                gcompli =  to_decimal(gcompli) + to_decimal(h_list.compli)
                t_gsales =  to_decimal(t_gsales) + to_decimal(h_list.t_sales)
                t_gcost =  to_decimal(t_gcost) + to_decimal(h_list.t_cost)
                t_gcompli =  to_decimal(t_gcompli) + to_decimal(h_list.t_compli)
                h_list.ncost =  to_decimal(h_list.cost) - to_decimal(h_list.compli)
                ncost =  to_decimal(ncost) + to_decimal(h_list.ncost)
                h_list.t_ncost =  to_decimal(h_list.t_cost) - to_decimal(h_list.t_compli)
                t_ncost =  to_decimal(t_ncost) + to_decimal(h_list.t_ncost)
                tot_ncost =  to_decimal(tot_ncost) + to_decimal(h_list.t_ncost)

                if h_list.sales != 0:
                    h_list.proz =  to_decimal(h_list.ncost) / to_decimal(h_list.sales) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_proz =  to_decimal(h_list.t_ncost) / to_decimal(h_list.t_sales) * to_decimal("100")
                t_anz = t_anz + h_list.anz
                t_m_anz = t_m_anz + h_list.m_anz
                t_comanz = t_comanz + h_list.comanz
                t_m_comanz = t_m_comanz + h_list.t_comanz
                t_anz_cost = t_anz_cost + h_list.anz_cost
                t_manz_cost = t_manz_cost + h_list.manz_cost


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.num = h_list.num
                output_list.bezeich = h_list.depart
                output_list.sales =  to_decimal(h_list.sales)
                output_list.ncost =  to_decimal(h_list.ncost)
                output_list.compli =  to_decimal(h_list.compli)
                output_list.cost =  to_decimal(h_list.cost)
                output_list.proz =  to_decimal(h_list.proz)
                output_list.t_proz =  to_decimal(h_list.t_proz)
                output_list.anz_cost = h_list.anz_cost
                output_list.manz_cost = h_list.manz_cost

                if h_list.t_sales >= 0:
                    output_list.t_sales =  to_decimal(h_list.t_sales)
                    output_list.t_ncost =  to_decimal(h_list.t_ncost)
                    output_list.t_compli =  to_decimal(h_list.t_compli)
                    output_list.t_cost =  to_decimal(h_list.t_cost)


        proz =  to_decimal("0")
        t_proz =  to_decimal("0")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        dd_anz = dd_anz + t_anz
        dd_comanz = dd_comanz + t_comanz
        tm_anz = tm_anz + t_m_anz
        tm_comanz = tm_comanz + t_m_comanz


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "T O T A L"
        output_list.sales =  to_decimal(gsales)
        output_list.ncost =  to_decimal(ncost)
        output_list.compli =  to_decimal(gcompli)
        output_list.cost =  to_decimal(gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = t_anz
        output_list.m_anz = t_m_anz
        output_list.comanz = t_comanz
        output_list.m_comanz = t_m_comanz
        output_list.anz_cost = t_anz_cost
        output_list.manz_cost = t_manz_cost

        if t_gsales >= 0:
            output_list.t_sales =  to_decimal(t_gsales)
            output_list.t_ncost =  to_decimal(t_ncost)
            output_list.t_compli =  to_decimal(t_gcompli)
            output_list.t_cost =  to_decimal(t_gcost)


        proz =  to_decimal("0")
        t_proz =  to_decimal("0")
        dd_ncost =  to_decimal(dd_gcost) - to_decimal(dd_gcompli)

        if dd_gsales != 0:
            proz =  to_decimal(dd_ncost) / to_decimal(dd_gsales) * to_decimal("100")

        if tot_gsales != 0:
            t_proz =  to_decimal(tot_ncost) / to_decimal(tot_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "GRAND TOTAL"
        output_list.sales =  to_decimal(dd_gsales)
        output_list.ncost =  to_decimal(dd_ncost)
        output_list.compli =  to_decimal(dd_gcompli)
        output_list.cost =  to_decimal(dd_gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = dd_anz
        output_list.comanz = dd_comanz
        output_list.m_anz = tm_anz
        output_list.m_comanz = tm_comanz

        if tot_gsales >= 0:
            output_list.t_sales =  to_decimal(tot_gsales)
            output_list.t_ncost =  to_decimal(tot_ncost)
            output_list.t_compli =  to_decimal(tot_gcompli)
            output_list.t_cost =  to_decimal(tot_gcost)


    def create_h_umsatz22():

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        gsales:Decimal = to_decimal("0.0")
        t_gsales:Decimal = to_decimal("0.0")
        gcompli:Decimal = to_decimal("0.0")
        t_gcompli:Decimal = to_decimal("0.0")
        gcost:Decimal = to_decimal("0.0")
        t_gcost:Decimal = to_decimal("0.0")
        ncost:Decimal = to_decimal("0.0")
        t_ncost:Decimal = to_decimal("0.0")
        proz:Decimal = to_decimal("0.0")
        t_proz:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        dd_gsales:Decimal = to_decimal("0.0")
        dd_gcompli:Decimal = to_decimal("0.0")
        dd_gcost:Decimal = to_decimal("0.0")
        dd_ncost:Decimal = to_decimal("0.0")
        tot_gsales:Decimal = to_decimal("0.0")
        tot_gcompli:Decimal = to_decimal("0.0")
        tot_gcost:Decimal = to_decimal("0.0")
        tot_ncost:Decimal = to_decimal("0.0")
        dd_anz:int = 0
        dd_comanz:int = 0
        tm_anz:int = 0
        tm_comanz:int = 0
        t_anz:int = 0
        t_m_anz:int = 0
        t_comanz:int = 0
        t_m_comanz:int = 0
        t_anz_cost:int = 0
        t_manz_cost:int = 0
        ind:int = 0
        price_decimal:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_data.clear()
        h_list_data.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "** Beverage **"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                h_list = H_list()
                h_list_data.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.artnrfront, h_artikel.departement, h_artikel.prozent, h_artikel.bezeich, h_artikel.artnr, h_artikel._recid, artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid in db_session.query(H_artikel.artnrfront, H_artikel.departement, H_artikel.prozent, H_artikel.bezeich, H_artikel.artnr, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.depart = h_artikel.bezeich

                    for h_umsatz in db_session.query(H_umsatz).filter(
                             (H_umsatz.departement == h_artikel.departement) & (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).order_by(H_umsatz._recid).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if double_currency:
                            find_exrate(h_umsatz.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        rate =  to_decimal(rate) / to_decimal(fact1)

                        if h_umsatz.datum == to_date:

                            if mi_compli_checked:
                                h_list.anz = h_list.anz + h_umsatz.anzahl
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                        if mi_compli_checked:
                            h_list.m_anz = h_list.m_anz + h_umsatz.anzahl
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_umsatz.artnr)],"departement": [(eq, h_umsatz.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)

                            if not mi_compli_checked:

                                if h_umsatz.datum == to_date:
                                    h_list.anz = h_list.anz + h_cost.anzahl
                                h_list.m_anz = h_list.m_anz + h_cost.anzahl
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                     (H_journal.artnr == h_umsatz.artnr) & (H_journal.departement == h_umsatz.departement) & (H_journal.bill_datum == h_umsatz.datum)).order_by(H_journal._recid).all():
                                cost =  to_decimal(cost) + to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) * to_decimal(rate) / to_decimal("100")

                                if not mi_compli_checked:

                                    if h_umsatz.datum == to_date:
                                        h_list.anz = h_list.anz + h_journal.anzahl
                                    h_list.m_anz = h_list.m_anz + h_journal.anzahl

                        if h_umsatz.datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

                    h_compli_obj_list = {}
                    h_compli = H_compli()
                    h_art = H_artikel()
                    for h_compli.departement, h_compli.artnr, h_compli.datum, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid in db_session.query(H_compli.departement, H_compli.artnr, H_compli.datum, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == h_artikel.departement) & (H_compli.artnr == h_artikel.artnr) & (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli_obj_list.get(h_compli._recid):
                            continue
                        else:
                            h_compli_obj_list[h_compli._recid] = True

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                        if h_compli.datum == to_date:
                            h_list.compli =  to_decimal(h_list.compli) + to_decimal(cost)
                            h_list.comanz = h_list.comanz + h_compli.anzahl
                            dd_gcompli =  to_decimal(dd_gcompli) + to_decimal(cost)

                            if not mi_compli_checked:
                                h_list.anz = h_list.anz - h_compli.anzahl
                        h_list.t_compli =  to_decimal(h_list.t_compli) + to_decimal(cost)
                        h_list.t_comanz = h_list.t_comanz + h_compli.anzahl

                        if not mi_compli_checked:
                            h_list.m_anz = h_list.m_anz - h_compli.anzahl
                        tot_gcompli =  to_decimal(tot_gcompli) + to_decimal(cost)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger
        ind = 0
        gsales =  to_decimal("0")
        ncost =  to_decimal("0")
        gcompli =  to_decimal("0")
        gcost =  to_decimal("0")
        t_gsales =  to_decimal("0")
        t_gcompli =  to_decimal("0")
        t_gcost =  to_decimal("0")
        t_ncost =  to_decimal("0")
        t_proz =  to_decimal("0")
        t_anz = 0
        t_m_anz = 0
        t_comanz = 0
        t_m_comanz = 0
        t_anz_cost = 0
        t_manz_cost = 0

        for h_list in query(h_list_data, filters=(lambda h_list: h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

                    if t_gsales != 0:
                        t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.bezeich = "T O T A L"
                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz
                    output_list.sales =  to_decimal(gsales)
                    output_list.ncost =  to_decimal(ncost)
                    output_list.compli =  to_decimal(gcompli)
                    output_list.cost =  to_decimal(gcost)
                    output_list.proz =  to_decimal(proz)
                    output_list.t_proz =  to_decimal(t_proz)
                    output_list.anz = t_anz
                    output_list.m_anz = t_m_anz
                    output_list.comanz = t_comanz
                    output_list.m_comanz = t_m_comanz
                    output_list.anz_cost = t_anz_cost
                    output_list.manz_cost = t_manz_cost

                    if t_gsales >= 0:
                        output_list.t_sales =  to_decimal(t_gsales)
                        output_list.t_ncost =  to_decimal(t_ncost)
                        output_list.t_compli =  to_decimal(t_gcompli)
                        output_list.t_cost =  to_decimal(t_gcost)


                gsales =  to_decimal("0")
                gcompli =  to_decimal("0")
                gcost =  to_decimal("0")
                ncost =  to_decimal("0")
                t_gsales =  to_decimal("0")
                t_gcompli =  to_decimal("0")
                t_gcost =  to_decimal("0")
                t_ncost =  to_decimal("0")
                t_proz =  to_decimal("0")
                dd_anz = dd_anz + t_anz
                dd_comanz = dd_comanz + t_comanz
                tm_anz = tm_anz + t_m_anz
                tm_comanz = tm_comanz + t_m_comanz


                t_anz = 0
                t_m_anz = 0
                t_comanz = 0
                t_m_comanz = 0
                t_anz_cost = 0
                t_manz_cost = 0


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.num = h_list.num
                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.bezeich = h_list.depart


            else:
                gsales =  to_decimal(gsales) + to_decimal(h_list.sales)
                gcost =  to_decimal(gcost) + to_decimal(h_list.cost)
                gcompli =  to_decimal(gcompli) + to_decimal(h_list.compli)
                t_gsales =  to_decimal(t_gsales) + to_decimal(h_list.t_sales)
                t_gcost =  to_decimal(t_gcost) + to_decimal(h_list.t_cost)
                t_gcompli =  to_decimal(t_gcompli) + to_decimal(h_list.t_compli)
                h_list.ncost =  to_decimal(h_list.cost) - to_decimal(h_list.compli)
                ncost =  to_decimal(ncost) + to_decimal(h_list.ncost)
                h_list.t_ncost =  to_decimal(h_list.t_cost) - to_decimal(h_list.t_compli)
                t_ncost =  to_decimal(t_ncost) + to_decimal(h_list.t_ncost)
                tot_ncost =  to_decimal(tot_ncost) + to_decimal(h_list.t_ncost)

                if h_list.sales != 0:
                    h_list.proz =  to_decimal(h_list.ncost) / to_decimal(h_list.sales) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_proz =  to_decimal(h_list.t_ncost) / to_decimal(h_list.t_sales) * to_decimal("100")
                t_anz = t_anz + h_list.anz
                t_m_anz = t_m_anz + h_list.m_anz
                t_comanz = t_comanz + h_list.comanz
                t_m_comanz = t_m_comanz + h_list.t_comanz
                t_anz_cost = t_anz_cost + h_list.anz_cost
                t_manz_cost = t_manz_cost + h_list.manz_cost


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.num = h_list.num
                output_list.bezeich = h_list.depart
                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.sales =  to_decimal(h_list.sales)
                output_list.ncost =  to_decimal(h_list.ncost)
                output_list.compli =  to_decimal(h_list.compli)
                output_list.cost =  to_decimal(h_list.cost)
                output_list.proz =  to_decimal(h_list.proz)
                output_list.t_proz =  to_decimal(h_list.t_proz)
                output_list.anz_cost = h_list.anz_cost
                output_list.manz_cost = h_list.manz_cost

                if h_list.t_sales >= 0:
                    output_list.t_sales =  to_decimal(h_list.t_sales)
                    output_list.t_ncost =  to_decimal(h_list.t_ncost)
                    output_list.t_compli =  to_decimal(h_list.t_compli)
                    output_list.t_cost =  to_decimal(h_list.t_cost)


        proz =  to_decimal("0")
        t_proz =  to_decimal("0")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        dd_anz = dd_anz + t_anz
        dd_comanz = dd_comanz + t_comanz
        tm_anz = tm_anz + t_m_anz
        tm_comanz = tm_comanz + t_m_comanz


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "T O T A L"
        output_list.sales =  to_decimal(gsales)
        output_list.ncost =  to_decimal(ncost)
        output_list.compli =  to_decimal(gcompli)
        output_list.cost =  to_decimal(gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = t_anz
        output_list.m_anz = t_m_anz
        output_list.comanz = t_comanz
        output_list.m_comanz = t_m_comanz
        output_list.anz_cost = t_anz_cost
        output_list.manz_cost = t_manz_cost

        if t_gsales >= 0:
            output_list.t_sales =  to_decimal(t_gsales)
            output_list.t_ncost =  to_decimal(t_ncost)
            output_list.t_compli =  to_decimal(t_gcompli)
            output_list.t_cost =  to_decimal(t_gcost)


        proz =  to_decimal("0")
        t_proz =  to_decimal("0")
        dd_ncost =  to_decimal(dd_gcost) - to_decimal(dd_gcompli)

        if dd_gsales != 0:
            proz =  to_decimal(dd_ncost) / to_decimal(dd_gsales) * to_decimal("100")

        if tot_gsales != 0:
            t_proz =  to_decimal(tot_ncost) / to_decimal(tot_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "GRAND TOTAL"
        output_list.sales =  to_decimal(dd_gsales)
        output_list.ncost =  to_decimal(dd_ncost)
        output_list.compli =  to_decimal(dd_gcompli)
        output_list.cost =  to_decimal(dd_gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = dd_anz
        output_list.comanz = dd_comanz
        output_list.m_anz = tm_anz
        output_list.m_comanz = tm_comanz

        if tot_gsales >= 0:
            output_list.t_sales =  to_decimal(tot_gsales)
            output_list.t_ncost =  to_decimal(tot_ncost)
            output_list.t_compli =  to_decimal(tot_gcompli)
            output_list.t_cost =  to_decimal(tot_gcost)


    def create_h_umsatz33():

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:Decimal = 1
        curr_datum:date = None
        cost:Decimal = to_decimal("0.0")
        gsales:Decimal = to_decimal("0.0")
        t_gsales:Decimal = to_decimal("0.0")
        gcompli:Decimal = to_decimal("0.0")
        t_gcompli:Decimal = to_decimal("0.0")
        gcost:Decimal = to_decimal("0.0")
        t_gcost:Decimal = to_decimal("0.0")
        ncost:Decimal = to_decimal("0.0")
        t_ncost:Decimal = to_decimal("0.0")
        proz:Decimal = to_decimal("0.0")
        t_proz:Decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        dd_gsales:Decimal = to_decimal("0.0")
        dd_gcompli:Decimal = to_decimal("0.0")
        dd_gcost:Decimal = to_decimal("0.0")
        dd_ncost:Decimal = to_decimal("0.0")
        tot_gsales:Decimal = to_decimal("0.0")
        tot_gcompli:Decimal = to_decimal("0.0")
        tot_gcost:Decimal = to_decimal("0.0")
        tot_ncost:Decimal = to_decimal("0.0")
        dd_anz:int = 0
        dd_comanz:int = 0
        tm_anz:int = 0
        tm_comanz:int = 0
        t_anz:int = 0
        t_m_anz:int = 0
        t_comanz:int = 0
        t_m_comanz:int = 0
        t_anz_cost:int = 0
        t_manz_cost:int = 0
        ind:int = 0
        price_decimal:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_data.clear()
        h_list_data.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.bezeich = "** Others **"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
        f_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
        b_endkum = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = get_cache (H_artikel, {"departement": [(eq, hoteldpt.num)]})

            if h_artikel:
                h_list = H_list()
                h_list_data.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = {}
                h_artikel = H_artikel()
                artikel = Artikel()
                for h_artikel.artnrfront, h_artikel.departement, h_artikel.prozent, h_artikel.bezeich, h_artikel.artnr, h_artikel._recid, artikel.artnr, artikel.departement, artikel.endkum, artikel.umsatzart, artikel._recid in db_session.query(H_artikel.artnrfront, H_artikel.departement, H_artikel.prozent, H_artikel.bezeich, H_artikel.artnr, H_artikel._recid, Artikel.artnr, Artikel.departement, Artikel.endkum, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == hoteldpt.num) & (Artikel.umsatzart == 4)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel_obj_list.get(h_artikel._recid):
                        continue
                    else:
                        h_artikel_obj_list[h_artikel._recid] = True


                    h_list = H_list()
                    h_list_data.append(h_list)

                    h_list.depart = h_artikel.bezeich

                    for h_umsatz in db_session.query(H_umsatz).filter(
                             (H_umsatz.departement == h_artikel.departement) & (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).order_by(H_umsatz._recid).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if double_currency:
                            find_exrate(h_umsatz.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        rate =  to_decimal(rate) / to_decimal(fact1)

                        if h_umsatz.datum == to_date:

                            if mi_compli_checked:
                                h_list.anz = h_list.anz + h_umsatz.anzahl
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)

                        if mi_compli_checked:
                            h_list.m_anz = h_list.m_anz + h_umsatz.anzahl
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_umsatz.artnr)],"departement": [(eq, h_umsatz.departement)],"datum": [(eq, h_umsatz.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)

                            if not mi_compli_checked:

                                if h_umsatz.datum == to_date:
                                    h_list.anz = h_list.anz + h_cost.anzahl
                                h_list.m_anz = h_list.m_anz + h_cost.anzahl
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                     (H_journal.artnr == h_umsatz.artnr) & (H_journal.departement == h_umsatz.departement) & (H_journal.bill_datum == h_umsatz.datum)).order_by(H_journal._recid).all():
                                cost =  to_decimal(cost) + to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(h_artikel.prozent) * to_decimal(rate) / to_decimal("100")

                                if not mi_compli_checked:

                                    if h_umsatz.datum == to_date:
                                        h_list.anz = h_list.anz + h_journal.anzahl
                                    h_list.m_anz = h_list.m_anz + h_journal.anzahl

                        if h_umsatz.datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

                    h_compli_obj_list = {}
                    h_compli = H_compli()
                    h_art = H_artikel()
                    for h_compli.departement, h_compli.artnr, h_compli.datum, h_compli.anzahl, h_compli.epreis, h_compli._recid, h_art.artnrfront, h_art.departement, h_art.prozent, h_art.bezeich, h_art.artnr, h_art._recid in db_session.query(H_compli.departement, H_compli.artnr, H_compli.datum, H_compli.anzahl, H_compli.epreis, H_compli._recid, H_art.artnrfront, H_art.departement, H_art.prozent, H_art.bezeich, H_art.artnr, H_art._recid).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == h_artikel.departement) & (H_compli.artnr == h_artikel.artnr) & (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli_obj_list.get(h_compli._recid):
                            continue
                        else:
                            h_compli_obj_list[h_compli._recid] = True

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        cost =  to_decimal("0")

                        h_cost = get_cache (H_cost, {"artnr": [(eq, h_compli.artnr)],"departement": [(eq, h_compli.departement)],"datum": [(eq, h_compli.datum)],"flag": [(eq, 1)]})

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_compli.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_compli.anzahl) * to_decimal(h_compli.epreis) * to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(rate)

                        if h_compli.datum == to_date:
                            h_list.compli =  to_decimal(h_list.compli) + to_decimal(cost)
                            h_list.comanz = h_list.comanz + h_compli.anzahl
                            dd_gcompli =  to_decimal(dd_gcompli) + to_decimal(cost)

                            if not mi_compli_checked:
                                h_list.anz = h_list.anz - h_compli.anzahl
                        h_list.t_compli =  to_decimal(h_list.t_compli) + to_decimal(cost)
                        h_list.t_comanz = h_list.t_comanz + h_compli.anzahl

                        if not mi_compli_checked:
                            h_list.m_anz = h_list.m_anz - h_compli.anzahl
                        tot_gcompli =  to_decimal(tot_gcompli) + to_decimal(cost)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger
        ind = 0
        gsales =  to_decimal("0")
        ncost =  to_decimal("0")
        gcompli =  to_decimal("0")
        gcost =  to_decimal("0")
        t_gsales =  to_decimal("0")
        t_gcompli =  to_decimal("0")
        t_gcost =  to_decimal("0")
        t_ncost =  to_decimal("0")
        t_proz =  to_decimal("0")

        for h_list in query(h_list_data, filters=(lambda h_list: h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

                    if t_gsales != 0:
                        t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.bezeich = "T O T A L"
                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz
                    output_list.sales =  to_decimal(gsales)
                    output_list.ncost =  to_decimal(ncost)
                    output_list.compli =  to_decimal(gcompli)
                    output_list.cost =  to_decimal(gcost)
                    output_list.proz =  to_decimal(proz)
                    output_list.t_proz =  to_decimal(t_proz)
                    output_list.anz = t_anz
                    output_list.m_anz = t_m_anz
                    output_list.comanz = t_comanz
                    output_list.m_comanz = t_m_comanz
                    output_list.anz_cost = t_anz_cost
                    output_list.manz_cost = t_manz_cost

                    if t_gsales >= 0:
                        output_list.t_sales =  to_decimal(t_gsales)
                        output_list.t_ncost =  to_decimal(t_ncost)
                        output_list.t_compli =  to_decimal(t_gcompli)
                        output_list.t_cost =  to_decimal(t_gcost)


                gsales =  to_decimal("0")
                gcompli =  to_decimal("0")
                gcost =  to_decimal("0")
                ncost =  to_decimal("0")
                t_gsales =  to_decimal("0")
                t_gcompli =  to_decimal("0")
                t_gcost =  to_decimal("0")
                t_ncost =  to_decimal("0")
                t_proz =  to_decimal("0")
                dd_anz = dd_anz + t_anz
                dd_comanz = dd_comanz + t_comanz
                tm_anz = tm_anz + t_m_anz
                tm_comanz = tm_comanz + t_m_comanz


                t_anz = 0
                t_m_anz = 0
                t_comanz = 0
                t_m_comanz = 0
                t_anz_cost = 0
                t_manz_cost = 0


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.num = h_list.num
                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.bezeich = h_list.depart


            else:
                gsales =  to_decimal(gsales) + to_decimal(h_list.sales)
                gcost =  to_decimal(gcost) + to_decimal(h_list.cost)
                gcompli =  to_decimal(gcompli) + to_decimal(h_list.compli)
                t_gsales =  to_decimal(t_gsales) + to_decimal(h_list.t_sales)
                t_gcost =  to_decimal(t_gcost) + to_decimal(h_list.t_cost)
                t_gcompli =  to_decimal(t_gcompli) + to_decimal(h_list.t_compli)
                h_list.ncost =  to_decimal(h_list.cost) - to_decimal(h_list.compli)
                ncost =  to_decimal(ncost) + to_decimal(h_list.ncost)
                h_list.t_ncost =  to_decimal(h_list.t_cost) - to_decimal(h_list.t_compli)
                t_ncost =  to_decimal(t_ncost) + to_decimal(h_list.t_ncost)
                tot_ncost =  to_decimal(tot_ncost) + to_decimal(h_list.t_ncost)

                if h_list.sales != 0:
                    h_list.proz =  to_decimal(h_list.ncost) / to_decimal(h_list.sales) * to_decimal("100")

                if h_list.t_sales != 0:
                    h_list.t_proz =  to_decimal(h_list.t_ncost) / to_decimal(h_list.t_sales) * to_decimal("100")
                t_anz = t_anz + h_list.anz
                t_m_anz = t_m_anz + h_list.m_anz
                t_comanz = t_comanz + h_list.comanz
                t_m_comanz = t_m_comanz + h_list.t_comanz
                t_anz_cost = t_anz_cost + h_list.anz_cost
                t_manz_cost = t_manz_cost + h_list.manz_cost


                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.num = h_list.num
                output_list.bezeich = h_list.depart
                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.sales =  to_decimal(h_list.sales)
                output_list.ncost =  to_decimal(h_list.ncost)
                output_list.compli =  to_decimal(h_list.compli)
                output_list.cost =  to_decimal(h_list.cost)
                output_list.proz =  to_decimal(h_list.proz)
                output_list.t_proz =  to_decimal(h_list.t_proz)
                output_list.anz_cost = h_list.anz_cost
                output_list.manz_cost = h_list.manz_cost

                if h_list.t_sales >= 0:
                    output_list.t_sales =  to_decimal(h_list.t_sales)
                    output_list.t_ncost =  to_decimal(h_list.t_ncost)
                    output_list.t_compli =  to_decimal(h_list.t_compli)
                    output_list.t_cost =  to_decimal(h_list.t_cost)


        proz =  to_decimal("0")
        t_proz =  to_decimal("0")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        dd_anz = dd_anz + t_anz
        dd_comanz = dd_comanz + t_comanz
        tm_anz = tm_anz + t_m_anz
        tm_comanz = tm_comanz + t_m_comanz


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "T O T A L"
        output_list.sales =  to_decimal(gsales)
        output_list.ncost =  to_decimal(ncost)
        output_list.compli =  to_decimal(gcompli)
        output_list.cost =  to_decimal(gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = t_anz
        output_list.m_anz = t_m_anz
        output_list.comanz = t_comanz
        output_list.m_comanz = t_m_comanz
        output_list.anz_cost = t_anz_cost
        output_list.manz_cost = t_manz_cost

        if t_gsales >= 0:
            output_list.t_sales =  to_decimal(t_gsales)
            output_list.t_ncost =  to_decimal(t_ncost)
            output_list.t_compli =  to_decimal(t_gcompli)
            output_list.t_cost =  to_decimal(t_gcost)


        proz =  to_decimal("0")
        t_proz =  to_decimal("0")
        dd_ncost =  to_decimal(dd_gcost) - to_decimal(dd_gcompli)

        if dd_gsales != 0:
            proz =  to_decimal(dd_ncost) / to_decimal(dd_gsales) * to_decimal("100")

        if tot_gsales != 0:
            t_proz =  to_decimal(tot_ncost) / to_decimal(tot_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = "GRAND TOTAL"
        output_list.sales =  to_decimal(dd_gsales)
        output_list.ncost =  to_decimal(dd_ncost)
        output_list.compli =  to_decimal(dd_gcompli)
        output_list.cost =  to_decimal(dd_gcost)
        output_list.proz =  to_decimal(proz)
        output_list.t_proz =  to_decimal(t_proz)
        output_list.anz = dd_anz
        output_list.comanz = dd_comanz
        output_list.m_anz = tm_anz
        output_list.m_comanz = tm_comanz

        if tot_gsales >= 0:
            output_list.t_sales =  to_decimal(tot_gsales)
            output_list.t_ncost =  to_decimal(tot_ncost)
            output_list.t_compli =  to_decimal(tot_gcompli)
            output_list.t_cost =  to_decimal(tot_gcost)


    def find_exrate(curr_date:date):

        nonlocal output_list_data, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, dd_anz, dd_comanz, tm_anz, tm_comanz, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_data, output_list_data

        if foreign_nr != 0:

            exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            exrate = get_cache (Exrate, {"datum": [(eq, curr_date)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if sorttype == 1:

        if not detailed:
            create_h_umsatz1()
        else:
            create_h_umsatz11()

    elif sorttype == 2:

        if not detailed:
            create_h_umsatz2()
        else:
            create_h_umsatz22()

    elif sorttype == 3:

        if not detailed:
            create_h_umsatz3()
        else:
            create_h_umsatz33()

    elif sorttype == 4:

        if not detailed:
            create_h_umsatz1()
            create_h_umsatz2()
            create_h_umsatz3()
        else:
            create_h_umsatz11()
            create_h_umsatz22()
            create_h_umsatz33()

    return generate_output()