from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_artikel, Hoteldpt, Umsatz, Artikel, H_compli, H_cost, H_journal, H_umsatz, Exrate

def hums_cost_btn_gobl(pvilanguage:int, sorttype:int, detailed:bool, from_dept:int, to_dept:int, from_date:date, to_date:date, fact1:int, short_flag:bool, mi_compli_checked:bool):
    output_list_list = []
    exchg_rate:decimal = 1
    double_currency:bool = False
    foreign_nr:int = 0
    dd_gsales:decimal = to_decimal("0.0")
    dd_gcompli:decimal = to_decimal("0.0")
    dd_gcost:decimal = to_decimal("0.0")
    dd_ncost:decimal = to_decimal("0.0")
    tot_gsales:decimal = to_decimal("0.0")
    tot_gcompli:decimal = to_decimal("0.0")
    tot_gcost:decimal = to_decimal("0.0")
    tot_ncost:decimal = to_decimal("0.0")
    lvcarea:str = "hums-cost"
    htparam = waehrung = h_artikel = hoteldpt = umsatz = artikel = h_compli = h_cost = h_journal = h_umsatz = exrate = None

    h_list = output_list = None

    h_list_list, H_list = create_model("H_list", {"artnr":int, "dept":int, "num":int, "depart":str, "anz":int, "m_anz":int, "sales":decimal, "t_sales":decimal, "comanz":int, "compli":decimal, "t_compli":decimal, "t_comanz":int, "cost":decimal, "t_cost":decimal, "ncost":decimal, "t_ncost":decimal, "proz":decimal, "t_proz":decimal})
    output_list_list, Output_list = create_model("Output_list", {"anz":int, "m_anz":int, "comanz":int, "m_comanz":int, "s":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list
        return {"output-list": output_list_list}

    def create_h_umsatz1():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = to_decimal("0.0")
        gsales:decimal = to_decimal("0.0")
        t_gsales:decimal = to_decimal("0.0")
        gcompli:decimal = to_decimal("0.0")
        t_gcompli:decimal = to_decimal("0.0")
        gcost:decimal = to_decimal("0.0")
        t_gcost:decimal = to_decimal("0.0")
        ncost:decimal = to_decimal("0.0")
        t_ncost:decimal = to_decimal("0.0")
        proz:decimal = to_decimal("0.0")
        t_proz:decimal = to_decimal("0.0")
        f_endkum:int = 0
        m_endkum:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        dd_gsales =  to_decimal("0")
        dd_gcompli =  to_decimal("0")
        dd_gcost =  to_decimal("0")
        dd_ncost =  to_decimal("0")
        tot_gsales =  to_decimal("0")
        tot_gcompli =  to_decimal("0")
        tot_gcost =  to_decimal("0")
        tot_ncost =  to_decimal("0")
        output_list_list.clear()
        h_list_list.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.s = to_string(translateExtended ("** Food **", lvcarea, "") , "x(125)")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 862)).first()
        f_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 273)).first()
        m_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

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
                        h_list_list.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = []
                    for artikel, umsatz in db_session.query(Artikel, Umsatz).join(Umsatz,(Umsatz.artnr == Artikel.artnr) & (Umsatz.departement == Artikel.departement) & (Umsatz.datum == curr_datum)).filter(
                             (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).order_by(Artikel._recid).all():
                        if artikel._recid in artikel_obj_list:
                            continue
                        else:
                            artikel_obj_list.append(artikel._recid)


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if umsatz.datum == to_date:
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            gsales =  to_decimal(gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        t_gsales =  to_decimal(t_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == hoteldpt.num) & (H_compli.datum == curr_datum) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        h_artikel = db_session.query(H_artikel).filter(
                                 (H_artikel.departement == h_compli.departement) & (H_artikel.artnr == h_compli.artnr)).first()

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if (artikel.endkum == f_endkum or artikel.endkum == m_endkum or artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            cost =  to_decimal("0")

                            h_cost = db_session.query(H_cost).filter(
                                     (H_cost.artnr == h_compli.artnr) & (H_cost.departement == h_compli.departement) & (H_cost.datum == h_compli.datum) & (H_cost.flag == 1)).first()

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

                    h_journal_obj_list = []
                    for h_journal, h_art, artikel in db_session.query(H_journal, H_art, Artikel).join(H_art,(H_art.artnr == H_journal.artnr) & (H_art.departement == H_journal.departement) & (H_art.artart == 0)).join(Artikel,(Artikel.artnr == H_art.artnrfront) & (Artikel.departement == H_art.departement) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).filter(
                             (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_datum)).order_by(H_journal._recid).all():
                        if h_journal._recid in h_journal_obj_list:
                            continue
                        else:
                            h_journal_obj_list.append(h_journal._recid)


                        cost =  to_decimal("0")

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_journal.artnr) & (H_cost.departement == h_journal.departement) & (H_cost.datum == h_journal.bill_datum) & (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(rate) * to_decimal(h_art.prozent) / to_decimal("100")

                        if h_journal.bill_datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            gcost =  to_decimal(gcost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        t_gcost =  to_decimal(t_gcost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()

        for h_list in query(h_list_list):
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
            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.compli, " ->>,>>>,>>>,>>9") + to_string(h_list.cost, " ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " >>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>,>>>,>>>,>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>>>>>>>>>9") + to_string(h_list.ncost, " ->>>>>>>>>>9") + to_string(h_list.compli, " ->>>>>>>>>>9") + to_string(h_list.cost, " ->>>>>>>>>>9")

                if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " >>>>>>>>>>>>9") + to_string(h_list.t_ncost, " >>>>>>>>>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>>>>>>>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>>>>>>>>>9") + to_string(h_list.t_ncost, " ->>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " ->>>>>>>>>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
            else:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, " ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->>.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->>.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")
            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->>.99")


    def create_h_umsatz2():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = to_decimal("0.0")
        gsales:decimal = to_decimal("0.0")
        t_gsales:decimal = to_decimal("0.0")
        gcompli:decimal = to_decimal("0.0")
        t_gcompli:decimal = to_decimal("0.0")
        gcost:decimal = to_decimal("0.0")
        t_gcost:decimal = to_decimal("0.0")
        ncost:decimal = to_decimal("0.0")
        t_ncost:decimal = to_decimal("0.0")
        proz:decimal = to_decimal("0.0")
        t_proz:decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_list.clear()
        h_list_list.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.s = to_string(translateExtended ("** Beverage **", lvcarea, "") , "x(125)")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 862)).first()
        f_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 892)).first()
        b_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

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
                        h_list_list.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = []
                    for artikel, umsatz in db_session.query(Artikel, Umsatz).join(Umsatz,(Umsatz.artnr == Artikel.artnr) & (Umsatz.departement == Artikel.departement) & (Umsatz.datum == curr_datum)).filter(
                             (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).order_by(Artikel._recid).all():
                        if artikel._recid in artikel_obj_list:
                            continue
                        else:
                            artikel_obj_list.append(artikel._recid)


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if umsatz.datum == to_date:
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            gsales =  to_decimal(gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        t_gsales =  to_decimal(t_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == hoteldpt.num) & (H_compli.datum == curr_datum) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        h_artikel = db_session.query(H_artikel).filter(
                                 (H_artikel.departement == h_compli.departement) & (H_artikel.artnr == h_compli.artnr)).first()

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if (artikel.endkum == b_endkum or artikel.umsatzart == 6):
                            cost =  to_decimal("0")

                            h_cost = db_session.query(H_cost).filter(
                                     (H_cost.artnr == h_compli.artnr) & (H_cost.departement == h_compli.departement) & (H_cost.datum == h_compli.datum) & (H_cost.flag == 1)).first()

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

                    h_journal_obj_list = []
                    for h_journal, h_art, artikel in db_session.query(H_journal, H_art, Artikel).join(H_art,(H_art.artnr == H_journal.artnr) & (H_art.departement == H_journal.departement) & (H_art.artart == 0)).join(Artikel,(Artikel.artnr == H_art.artnrfront) & (Artikel.departement == H_art.departement) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).filter(
                             (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_datum)).order_by(H_journal._recid).all():
                        if h_journal._recid in h_journal_obj_list:
                            continue
                        else:
                            h_journal_obj_list.append(h_journal._recid)


                        cost =  to_decimal("0")

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_journal.artnr) & (H_cost.departement == h_journal.departement) & (H_cost.datum == h_journal.bill_datum) & (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(rate) * to_decimal(h_art.prozent) / to_decimal("100")

                        if h_journal.bill_datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            gcost =  to_decimal(gcost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        t_gcost =  to_decimal(t_gcost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()

        for h_list in query(h_list_list):
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
            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.compli, " ->>,>>>,>>>,>>9") + to_string(h_list.cost, " ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " >>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>,>>>,>>>,>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>>>>>>>>>9") + to_string(h_list.ncost, " ->>>>>>>>>>9") + to_string(h_list.compli, " ->>>>>>>>>>9") + to_string(h_list.cost, " ->>>>>>>>>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " >>>>>>>>>>>>9") + to_string(h_list.t_ncost, " >>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " >>>>>>>>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>>>>>>>>>9") + to_string(h_list.t_ncost, " ->>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " ->>>>>>>>>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
            else:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, " ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.proz, "->>>>9"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, ">>>>>>>>>,>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")


    def create_h_umsatz3():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = to_decimal("0.0")
        gsales:decimal = to_decimal("0.0")
        t_gsales:decimal = to_decimal("0.0")
        gcompli:decimal = to_decimal("0.0")
        t_gcompli:decimal = to_decimal("0.0")
        gcost:decimal = to_decimal("0.0")
        t_gcost:decimal = to_decimal("0.0")
        ncost:decimal = to_decimal("0.0")
        t_ncost:decimal = to_decimal("0.0")
        proz:decimal = to_decimal("0.0")
        t_proz:decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_list.clear()
        h_list_list.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.s = to_string(translateExtended ("** Others **", lvcarea, "") , "x(125)")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 862)).first()
        f_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 892)).first()
        b_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

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
                        h_list_list.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = []
                    for artikel, umsatz in db_session.query(Artikel, Umsatz).join(Umsatz,(Umsatz.artnr == Artikel.artnr) & (Umsatz.departement == Artikel.departement) & (Umsatz.datum == curr_datum)).filter(
                             (Artikel.artart == 0) & (Artikel.departement == hoteldpt.num) & (Artikel.umsatzart == 4)).order_by(Artikel._recid).all():
                        if artikel._recid in artikel_obj_list:
                            continue
                        else:
                            artikel_obj_list.append(artikel._recid)


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat =  to_decimal(vat) + to_decimal(vat2)

                        if umsatz.datum == to_date:
                            h_list.sales =  to_decimal(h_list.sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            gsales =  to_decimal(gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                            dd_gsales =  to_decimal(dd_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        h_list.t_sales =  to_decimal(h_list.t_sales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        t_gsales =  to_decimal(t_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tot_gsales =  to_decimal(tot_gsales) + to_decimal(umsatz.betrag) / to_decimal(fact)

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == hoteldpt.num) & (H_compli.datum == curr_datum) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        h_artikel = db_session.query(H_artikel).filter(
                                 (H_artikel.departement == h_compli.departement) & (H_artikel.artnr == h_compli.artnr)).first()

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel.umsatzart == 4:
                            cost =  to_decimal("0")

                            h_cost = db_session.query(H_cost).filter(
                                     (H_cost.artnr == h_compli.artnr) & (H_cost.departement == h_compli.departement) & (H_cost.datum == h_compli.datum) & (H_cost.flag == 1)).first()

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

                    h_journal_obj_list = []
                    for h_journal, h_art, artikel in db_session.query(H_journal, H_art, Artikel).join(H_art,(H_art.artnr == H_journal.artnr) & (H_art.departement == H_journal.departement) & (H_art.artart == 0)).join(Artikel,(Artikel.artnr == H_art.artnrfront) & (Artikel.departement == H_art.departement) & (Artikel.umsatzart == 4)).filter(
                             (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_datum)).order_by(H_journal._recid).all():
                        if h_journal._recid in h_journal_obj_list:
                            continue
                        else:
                            h_journal_obj_list.append(h_journal._recid)


                        cost =  to_decimal("0")

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_journal.artnr) & (H_cost.departement == h_journal.departement) & (H_cost.datum == h_journal.bill_datum) & (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_cost.betrag) / to_decimal(fact1)
                        else:
                            cost =  to_decimal(h_journal.anzahl) * to_decimal(h_journal.epreis) * to_decimal(rate) * to_decimal(h_art.prozent) / to_decimal("100")

                        if h_journal.bill_datum == to_date:
                            h_list.cost =  to_decimal(h_list.cost) + to_decimal(cost)
                            gcost =  to_decimal(gcost) + to_decimal(cost)
                            dd_gcost =  to_decimal(dd_gcost) + to_decimal(cost)
                        h_list.t_cost =  to_decimal(h_list.t_cost) + to_decimal(cost)
                        t_gcost =  to_decimal(t_gcost) + to_decimal(cost)
                        tot_gcost =  to_decimal(tot_gcost) + to_decimal(cost)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()

        for h_list in query(h_list_list):
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
            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.compli, " ->>,>>>,>>>,>>9") + to_string(h_list.cost, " ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " >>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>,>>>,>>>,>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>>>>>>>>>9") + to_string(h_list.ncost, " ->>>>>>>>>>9") + to_string(h_list.compli, " ->>>>>>>>>>9") + to_string(h_list.cost, " ->>>>>>>>>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " >>>>>>>>>>>>9") + to_string(h_list.t_ncost, " >>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " >>>>>>>>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>>>>>>>>>9") + to_string(h_list.t_ncost, " ->>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " ->>>>>>>>>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
            else:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, " ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, ">>>>>>>>>,>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9") + to_string(dd_ncost, " ->>,>>>,>>>,>>9") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9") + to_string(dd_gcost, " ->>,>>>,>>>,>>9") + to_string(" ")

                if tot_gsales >= 0:
                    output_list.s = output_list.s + to_string(tot_gsales, " >>,>>>,>>>,>>9") + to_string(tot_ncost, " >>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " >>,>>>,>>>,>>9") + to_string(" ")
                else:
                    output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9") + to_string(tot_ncost, " ->>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " ->>,>>>,>>>,>>9") + to_string(" ")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>>>>>>>>>9") + to_string(dd_ncost, " ->>>>>>>>>>9") + to_string(dd_gcompli, " ->>>>>>>>>>9") + to_string(dd_gcost, " ->>>>>>>>>>9") + to_string(" ")

                if t_gsales >= 0:
                    output_list.s = output_list.s + to_string(tot_gsales, ">>>>>>>>>,>>9") + to_string(tot_ncost, " >>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " >>>>>>>>>>9") + to_string(" ")
                else:
                    output_list.s = output_list.s + to_string(tot_gsales, " ->>>>>>>>>>9") + to_string(tot_ncost, " ->>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " ->>>>>>>>>>9") + to_string(" ")
            else:
                output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, " ->>,>>>,>>>,>>9.99") + to_string(" ") + to_string(tot_gsales, " ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99") + to_string(" ")


    def create_h_umsatz11():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = to_decimal("0.0")
        gsales:decimal = to_decimal("0.0")
        t_gsales:decimal = to_decimal("0.0")
        gcompli:decimal = to_decimal("0.0")
        t_gcompli:decimal = to_decimal("0.0")
        gcost:decimal = to_decimal("0.0")
        t_gcost:decimal = to_decimal("0.0")
        ncost:decimal = to_decimal("0.0")
        t_ncost:decimal = to_decimal("0.0")
        proz:decimal = to_decimal("0.0")
        t_proz:decimal = to_decimal("0.0")
        f_endkum:int = 0
        m_endkum:int = 0
        dd_gsales:decimal = to_decimal("0.0")
        dd_gcompli:decimal = to_decimal("0.0")
        dd_gcost:decimal = to_decimal("0.0")
        dd_ncost:decimal = to_decimal("0.0")
        tot_gsales:decimal = to_decimal("0.0")
        tot_gcompli:decimal = to_decimal("0.0")
        tot_gcost:decimal = to_decimal("0.0")
        tot_ncost:decimal = to_decimal("0.0")
        ind:int = 0
        price_decimal:int = 0
        H_art =  create_buffer("H_art",H_artikel)
        output_list_list.clear()
        h_list_list.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.s = to_string(translateExtended ("** Food **", lvcarea, "") , "x(125)")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 862)).first()
        f_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 273)).first()
        m_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = []
                for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == f_endkum) | (Artikel.endkum == m_endkum) | (Artikel.umsatzart == 3) | (Artikel.umsatzart == 5))).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel._recid in h_artikel_obj_list:
                        continue
                    else:
                        h_artikel_obj_list.append(h_artikel._recid)


                    h_list = H_list()
                    h_list_list.append(h_list)

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

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_umsatz.artnr) & (H_cost.departement == h_umsatz.departement) & (H_cost.datum == h_umsatz.datum) & (H_cost.flag == 1)).first()

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

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == h_artikel.departement) & (H_compli.artnr == h_artikel.artnr) & (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        cost =  to_decimal("0")

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_compli.artnr) & (H_cost.departement == h_compli.departement) & (H_cost.datum == h_compli.datum) & (H_cost.flag == 1)).first()

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

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
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

        for h_list in query(h_list_list, filters=(lambda h_list: h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

                    if t_gsales != 0:
                        t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz

                    if price_decimal == 0 and short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")

                    elif price_decimal == 0 and not short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                    else:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")
                        output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                ncost =  to_decimal("0")
                gsales =  to_decimal("0")
                gcompli =  to_decimal("0")
                gcost =  to_decimal("0")
                t_gsales =  to_decimal("0")
                t_gcompli =  to_decimal("0")
                t_gcost =  to_decimal("0")
                t_ncost =  to_decimal("0")
                t_proz =  to_decimal("0")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
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
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz

                if htparam.finteger == 0 and short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.compli, " ->>,>>>,>>>,>>9") + to_string(h_list.cost, " ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.proz, "->>>>9"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " >>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>,>>>,>>>,>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

                elif htparam.finteger == 0 and not short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>>>>>>>>>9") + to_string(h_list.ncost, " ->>>>>>>>>>9") + to_string(h_list.compli, " ->>>>>>>>>>9") + to_string(h_list.cost, " ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.proz, "->>>>9"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " >>>>>>>>>>>>9") + to_string(h_list.t_ncost, " >>>>>>>>>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>>>>>>>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " ->>>>>>>>>>9") + to_string(h_list.t_ncost, " ->>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
                else:
                    output_list.s = to_string(h_list.depart, "x(23)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, " ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(proz, "->>>>9"))) > 3:
                        output_list.s = output_list.s + to_string(proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(proz, "->9.99")
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
        proz =  to_decimal("0")
        t_proz =  to_decimal("0")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9") + to_string(t_proz, "->>.99")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9") + to_string(t_proz, "->>.99")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        proz =  to_decimal("0")
        t_proz =  to_decimal("0")
        dd_ncost =  to_decimal(dd_gcost) - to_decimal(dd_gcompli)

        if dd_gsales != 0:
            proz =  to_decimal(dd_ncost) / to_decimal(dd_gsales) * to_decimal("100")

        if tot_gsales != 0:
            t_proz =  to_decimal(tot_ncost) / to_decimal(tot_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9") + to_string(dd_ncost, " ->>,>>>,>>>,>>9") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9") + to_string(dd_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, " >>,>>>,>>>,>>9") + to_string(tot_ncost, " >>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9") + to_string(tot_ncost, " ->>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>>>>>>>>>9") + to_string(dd_ncost, " ->>>>>>>>>>9") + to_string(dd_gcompli, " ->>>>>>>>>>9") + to_string(dd_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, " >>>>>>>>>>>>9") + to_string(tot_ncost, " >>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, " ->>>>>>>>>>9") + to_string(tot_ncost, " ->>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")


    def create_h_umsatz22():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = to_decimal("0.0")
        gsales:decimal = to_decimal("0.0")
        t_gsales:decimal = to_decimal("0.0")
        gcompli:decimal = to_decimal("0.0")
        t_gcompli:decimal = to_decimal("0.0")
        gcost:decimal = to_decimal("0.0")
        t_gcost:decimal = to_decimal("0.0")
        ncost:decimal = to_decimal("0.0")
        t_ncost:decimal = to_decimal("0.0")
        proz:decimal = to_decimal("0.0")
        t_proz:decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        dd_gsales:decimal = to_decimal("0.0")
        dd_gcompli:decimal = to_decimal("0.0")
        dd_gcost:decimal = to_decimal("0.0")
        dd_ncost:decimal = to_decimal("0.0")
        tot_gsales:decimal = to_decimal("0.0")
        tot_gcompli:decimal = to_decimal("0.0")
        tot_gcost:decimal = to_decimal("0.0")
        tot_ncost:decimal = to_decimal("0.0")
        ind:int = 0
        price_decimal:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_list.clear()
        h_list_list.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.s = to_string(translateExtended ("** Beverage **", lvcarea, "") , "x(125)")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 862)).first()
        f_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 892)).first()
        b_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = []
                for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == hoteldpt.num) & ((Artikel.endkum == b_endkum) | (Artikel.umsatzart == 6))).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel._recid in h_artikel_obj_list:
                        continue
                    else:
                        h_artikel_obj_list.append(h_artikel._recid)


                    h_list = H_list()
                    h_list_list.append(h_list)

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

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_umsatz.artnr) & (H_cost.departement == h_umsatz.departement) & (H_cost.datum == h_umsatz.datum) & (H_cost.flag == 1)).first()

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

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == h_artikel.departement) & (H_compli.artnr == h_artikel.artnr) & (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        cost =  to_decimal("0")

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_compli.artnr) & (H_cost.departement == h_compli.departement) & (H_cost.datum == h_compli.datum) & (H_cost.flag == 1)).first()

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

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
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

        for h_list in query(h_list_list, filters=(lambda h_list: h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

                    if t_gsales != 0:
                        t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz

                    if price_decimal == 0 and short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")

                    elif price_decimal == 0 and not short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                    else:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")
                        output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                gsales =  to_decimal("0")
                gcompli =  to_decimal("0")
                gcost =  to_decimal("0")
                ncost =  to_decimal("0")
                t_gsales =  to_decimal("0")
                t_gcompli =  to_decimal("0")
                t_gcost =  to_decimal("0")
                t_ncost =  to_decimal("0")
                t_proz =  to_decimal("0")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
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
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz

                if htparam.finteger == 0 and short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.compli, " ->>,>>>,>>>,>>9") + to_string(h_list.cost, " ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " >>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>,>>>,>>>,>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

                elif htparam.finteger == 0 and not short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>>>>>>>>>9") + to_string(h_list.ncost, " ->>>>>>>>>>9") + to_string(h_list.compli, " ->>>>>>>>>>9") + to_string(h_list.cost, " ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " >>>>>>>>>>>>9") + to_string(h_list.t_ncost, " >>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " >>>>>>>>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " ->>>>>>>>>>9") + to_string(h_list.t_ncost, " ->>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
                else:
                    output_list.s = to_string(h_list.depart, "x(23)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, " ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9.99")
        proz =  to_decimal("0")
        t_proz =  to_decimal("0")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        proz =  to_decimal("0")
        t_proz =  to_decimal("0")
        dd_ncost =  to_decimal(dd_gcost) - to_decimal(dd_gcompli)

        if dd_gsales != 0:
            proz =  to_decimal(dd_ncost) / to_decimal(dd_gsales) * to_decimal("100")

        if tot_gsales != 0:
            t_proz =  to_decimal(tot_ncost) / to_decimal(tot_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9") + to_string(dd_ncost, " ->>,>>>,>>>,>>9") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9") + to_string(dd_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, " >>,>>>,>>>,>>9") + to_string(tot_ncost, " >>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9") + to_string(tot_ncost, " ->>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>>>>>>>>>9") + to_string(dd_ncost, " ->>>>>>>>>>9") + to_string(dd_gcompli, " ->>>>>>>>>>9") + to_string(dd_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, " >>>>>>>>>>>>9") + to_string(tot_ncost, " >>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, " ->>>>>>>>>>9") + to_string(tot_ncost, " ->>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")


    def create_h_umsatz33():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        vat:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        pos:bool = False
        h_art = None
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = to_decimal("0.0")
        gsales:decimal = to_decimal("0.0")
        t_gsales:decimal = to_decimal("0.0")
        gcompli:decimal = to_decimal("0.0")
        t_gcompli:decimal = to_decimal("0.0")
        gcost:decimal = to_decimal("0.0")
        t_gcost:decimal = to_decimal("0.0")
        ncost:decimal = to_decimal("0.0")
        t_ncost:decimal = to_decimal("0.0")
        proz:decimal = to_decimal("0.0")
        t_proz:decimal = to_decimal("0.0")
        f_endkum:int = 0
        b_endkum:int = 0
        dd_gsales:decimal = to_decimal("0.0")
        dd_gcompli:decimal = to_decimal("0.0")
        dd_gcost:decimal = to_decimal("0.0")
        dd_ncost:decimal = to_decimal("0.0")
        tot_gsales:decimal = to_decimal("0.0")
        tot_gcompli:decimal = to_decimal("0.0")
        tot_gcost:decimal = to_decimal("0.0")
        tot_ncost:decimal = to_decimal("0.0")
        ind:int = 0
        price_decimal:int = 0
        H_art =  create_buffer("H_art",H_artikel)

        if sorttype != 4:
            output_list_list.clear()
        h_list_list.clear()

        if sorttype == 4:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.s = to_string(translateExtended ("** Others **", lvcarea, "") , "x(125)")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 862)).first()
        f_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 892)).first()
        b_endkum = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = []
                for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == hoteldpt.num) & (Artikel.umsatzart == 4)).filter(
                         (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.bezeich).all():
                    if h_artikel._recid in h_artikel_obj_list:
                        continue
                    else:
                        h_artikel_obj_list.append(h_artikel._recid)


                    h_list = H_list()
                    h_list_list.append(h_list)

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

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_umsatz.artnr) & (H_cost.departement == h_umsatz.departement) & (H_cost.datum == h_umsatz.datum) & (H_cost.flag == 1)).first()

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

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) & (H_art.artnr == H_compli.p_artnr) & (H_art.artart == 11)).filter(
                             (H_compli.departement == h_artikel.departement) & (H_compli.artnr == h_artikel.artnr) & (H_compli.datum >= from_date) & (H_compli.datum <= to_date) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate =  to_decimal(exrate.betrag)
                            else:
                                rate =  to_decimal(exchg_rate)
                        cost =  to_decimal("0")

                        h_cost = db_session.query(H_cost).filter(
                                 (H_cost.artnr == h_compli.artnr) & (H_cost.departement == h_compli.departement) & (H_cost.datum == h_compli.datum) & (H_cost.flag == 1)).first()

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

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
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

        for h_list in query(h_list_list, filters=(lambda h_list: h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

                    if t_gsales != 0:
                        t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz

                    if price_decimal == 0 and short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

                        if len(trim(to_string(proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

                        if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")

                    elif price_decimal == 0 and not short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

                        if len(trim(to_string(proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

                        if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                    else:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")
                        output_list.s = output_list.s + to_string(proz, "->>.99") + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                gsales =  to_decimal("0")
                gcompli =  to_decimal("0")
                gcost =  to_decimal("0")
                ncost =  to_decimal("0")
                t_gsales =  to_decimal("0")
                t_gcompli =  to_decimal("0")
                t_gcost =  to_decimal("0")
                t_ncost =  to_decimal("0")
                t_proz =  to_decimal("0")
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
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
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz

                if htparam.finteger == 0 and short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.compli, " ->>,>>>,>>>,>>9") + to_string(h_list.cost, " ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " >>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " >>,>>>,>>>,>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

                elif htparam.finteger == 0 and not short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, " ->>>>>>>>>>9") + to_string(h_list.ncost, " ->>>>>>>>>>9") + to_string(h_list.compli, " ->>>>>>>>>>9") + to_string(h_list.cost, " ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " >>>>>>>>>>>>9") + to_string(h_list.t_ncost, " >>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " >>>>>>>>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, " ->>>>>>>>>>9") + to_string(h_list.t_ncost, " ->>>>>>>>>>9") + to_string(h_list.t_compli, " ->>>>>>>>>>9") + to_string(h_list.t_cost, " ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
                else:
                    output_list.s = to_string(h_list.depart, "x(23)") + to_string(h_list.sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, " ->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + to_string(h_list.t_sales, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, " ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, " ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
        proz =  to_decimal("0")
        t_proz =  to_decimal("0")

        if gsales != 0:
            proz =  to_decimal(ncost) / to_decimal(gsales) * to_decimal("100")

        if t_gsales != 0:
            t_proz =  to_decimal(t_ncost) / to_decimal(t_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9") + to_string(ncost, " ->>,>>>,>>>,>>9") + to_string(gcompli, " ->>,>>>,>>>,>>9") + to_string(gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>,>>>,>>>,>>9") + to_string(t_ncost, " >>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9") + to_string(t_ncost, " ->>,>>>,>>>,>>9") + to_string(t_gcompli, " ->>,>>>,>>>,>>9") + to_string(t_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>>>>>>>>>9") + to_string(ncost, " ->>>>>>>>>>9") + to_string(gcompli, " ->>>>>>>>>>9") + to_string(gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, " >>>>>>>>>>>>9") + to_string(t_ncost, " >>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, " ->>>>>>>>>>9") + to_string(t_ncost, " ->>>>>>>>>>9") + to_string(t_gcompli, " ->>>>>>>>>>9") + to_string(t_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, " ->>,>>>,>>>,>>9.99") + to_string(ncost, " ->>,>>>,>>>,>>9.99") + to_string(gcompli, " ->>,>>>,>>>,>>9.99") + to_string(gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, " ->>,>>>,>>>,>>9.99") + to_string(t_ncost, " ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(t_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        proz =  to_decimal("0")
        t_proz =  to_decimal("0")
        dd_ncost =  to_decimal(dd_gcost) - to_decimal(dd_gcompli)

        if dd_gsales != 0:
            proz =  to_decimal(dd_ncost) / to_decimal(dd_gsales) * to_decimal("100")

        if tot_gsales != 0:
            t_proz =  to_decimal(tot_ncost) / to_decimal(tot_gsales) * to_decimal("100")
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9") + to_string(dd_ncost, " ->>,>>>,>>>,>>9") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9") + to_string(dd_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, " >>,>>>,>>>,>>9") + to_string(tot_ncost, " >>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9") + to_string(tot_ncost, " ->>,>>>,>>>,>>9") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9") + to_string(tot_gcost, " ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>>>>>>>>>9") + to_string(dd_ncost, " ->>>>>>>>>>9") + to_string(dd_gcompli, " ->>>>>>>>>>9") + to_string(dd_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, " >>>>>>>>>>>>9") + to_string(tot_ncost, " >>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, " ->>>>>>>>>>9") + to_string(tot_ncost, " ->>>>>>>>>>9") + to_string(tot_gcompli, " ->>>>>>>>>>9") + to_string(tot_gcost, " ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, " ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
            output_list.s = output_list.s + to_string(tot_gsales, " ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, " ->>,>>>,>>>,>>9.99") + to_string(tot_gcost, " ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")


    def find_exrate(curr_date:date):

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal pvilanguage, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked


        nonlocal h_list, output_list
        nonlocal h_list_list, output_list_list

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                     (Exrate.artnr == foreign_nr) & (Exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(Exrate).filter(
                     (Exrate.datum == curr_date)).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

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