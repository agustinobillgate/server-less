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
    dd_gsales:decimal = 0
    dd_gcompli:decimal = 0
    dd_gcost:decimal = 0
    dd_ncost:decimal = 0
    tot_gsales:decimal = 0
    tot_gcompli:decimal = 0
    tot_gcost:decimal = 0
    tot_ncost:decimal = 0
    lvcarea:str = "hums_cost"
    htparam = waehrung = h_artikel = hoteldpt = umsatz = artikel = h_compli = h_cost = h_journal = h_umsatz = exrate = None

    h_list = output_list = h_art = None

    h_list_list, H_list = create_model("H_list", {"artnr":int, "dept":int, "num":int, "depart":str, "anz":int, "m_anz":int, "sales":decimal, "t_sales":decimal, "comanz":int, "compli":decimal, "t_compli":decimal, "t_comanz":int, "cost":decimal, "t_cost":decimal, "ncost":decimal, "t_ncost":decimal, "proz":decimal, "t_proz":decimal})
    output_list_list, Output_list = create_model("Output_list", {"anz":int, "m_anz":int, "comanz":int, "m_comanz":int, "s":str})

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list
        return {"output-list": output_list_list}

    def create_h_umsatz1():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        pos:bool = False
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        gsales:decimal = 0
        t_gsales:decimal = 0
        gcompli:decimal = 0
        t_gcompli:decimal = 0
        gcost:decimal = 0
        t_gcost:decimal = 0
        ncost:decimal = 0
        t_ncost:decimal = 0
        proz:decimal = 0
        t_proz:decimal = 0
        f_endkum:int = 0
        m_endkum:int = 0
        H_art = H_artikel
        dd_gsales = 0
        dd_gcompli = 0
        dd_gcost = 0
        dd_ncost = 0
        tot_gsales = 0
        tot_gcompli = 0
        tot_gcost = 0
        tot_ncost = 0
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
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                pos = True

            if pos:
                for curr_datum in range(from_date,to_date + 1) :

                    if double_currency:
                        find_exrate(curr_datum)

                        if exrate:
                            rate = exrate.betrag
                        else:
                            rate = exchg_rate
                    rate = rate / fact1

                    if curr_datum == from_date:
                        h_list = H_list()
                        h_list_list.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = []
                    for artikel, umsatz in db_session.query(Artikel, Umsatz).join(Umsatz,(Umsatz.artnr == Artikel.artnr) &  (Umsatz.departement == Artikel.departement) &  (Umsatz.datum == curr_datum)).filter(
                            (Artikel.artart == 0) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == f_endkum) |  (Artikel.endkum == m_endkum) |  (Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5))).all():
                        if artikel._recid in artikel_obj_list:
                            continue
                        else:
                            artikel_obj_list.append(artikel._recid)


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat = vat + vat2

                        if umsatz.datum == to_date:
                            h_list.sales = h_list.sales + umsatz.betrag / fact
                            gsales = gsales + umsatz.betrag / fact
                            dd_gsales = dd_gsales + umsatz.betrag / fact
                        h_list.t_sales = h_list.t_sales + umsatz.betrag / fact
                        t_gsales = t_gsales + umsatz.betrag / fact
                        tot_gsales = tot_gsales + umsatz.betrag / fact

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                            (H_compli.departement == hoteldpt.num) &  (H_compli.datum == curr_datum) &  (H_compli.betriebsnr == 0)).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.departement == h_compli.departement) &  (H_artikel.artnr == h_compli.artnr)).first()

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                        if (artikel.endkum == f_endkum or artikel.endkum == m_endkum or artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            cost = 0

                            h_cost = db_session.query(H_cost).filter(
                                    (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost = h_compli.anzahl * h_cost.betrag / fact1
                            else:
                                cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                            if h_compli.datum == to_date:
                                h_list.compli = h_list.compli + cost
                                h_list.comanz = h_list.comanz + h_compli.anzahl
                                gcompli = gcompli + cost
                                dd_gcompli = dd_gcompli + cost
                            h_list.t_compli = h_list.t_compli + cost
                            h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                            t_gcompli = t_gcompli + cost
                            tot_gcompli = tot_gcompli + cost

                    h_journal_obj_list = []
                    for h_journal, h_art, artikel in db_session.query(H_journal, H_art, Artikel).join(H_art,(H_art.artnr == H_journal.artnr) &  (H_art.departement == H_journal.departement) &  (H_art.artart == 0)).join(Artikel,(Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == h_art.departement) &  ((Artikel.endkum == f_endkum) |  (Artikel.endkum == m_endkum) |  (Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5))).filter(
                            (H_journal.departement == hoteldpt.num) &  (H_journal.bill_datum == curr_datum)).all():
                        if h_journal._recid in h_journal_obj_list:
                            continue
                        else:
                            h_journal_obj_list.append(h_journal._recid)


                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_journal.artnr) &  (H_cost.departement == h_journal.departement) &  (H_cost.datum == h_journal.bill_datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_journal.anzahl * h_cost.betrag / fact1
                        else:
                            cost = h_journal.anzahl * h_journal.epreis * rate * h_art.prozent / 100

                        if h_journal.bill_datum == to_date:
                            h_list.cost = h_list.cost + cost
                            gcost = gcost + cost
                            dd_gcost = dd_gcost + cost
                        h_list.t_cost = h_list.t_cost + cost
                        t_gcost = t_gcost + cost
                        tot_gcost = tot_gcost + cost

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()

        for h_list in query(h_list_list):
            h_list.ncost = h_list.cost - h_list.compli
            ncost = ncost + h_list.ncost
            dd_ncost = dd_ncost + h_list.ncost
            h_list.t_ncost = h_list.t_cost - h_list.t_compli
            t_ncost = t_ncost + h_list.t_ncost
            tot_ncost = tot_ncost + h_list.t_ncost

            if h_list.sales != 0:
                h_list.proz = h_list.ncost / h_list.sales * 100

            if h_list.t_sales != 0:
                h_list.t_proz = h_list.t_ncost / h_list.t_sales * 100
            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.cost, "     ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "      >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "      >>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "      >>,>>>,>>>,>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "     ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "        ->>>>>>>>>>9") + to_string(h_list.ncost, "        ->>>>>>>>>>9") + to_string(h_list.compli, "        ->>>>>>>>>>9") + to_string(h_list.cost, "        ->>>>>>>>>>9")

                if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "       >>>>>>>>>>>>9") + to_string(h_list.t_ncost, "         >>>>>>>>>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "         >>>>>>>>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "        ->>>>>>>>>>9") + to_string(h_list.t_ncost, "        ->>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "        ->>>>>>>>>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
            else:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, "  ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                output_list.s = output_list.s + to_string(h_list.t_sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "  ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

        if gsales != 0:
            proz = ncost / gsales * 100

        if t_gsales != 0:
            t_proz = t_ncost / t_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->>.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->>.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")
            output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->>.99")

    def create_h_umsatz2():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        pos:bool = False
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        gsales:decimal = 0
        t_gsales:decimal = 0
        gcompli:decimal = 0
        t_gcompli:decimal = 0
        gcost:decimal = 0
        t_gcost:decimal = 0
        ncost:decimal = 0
        t_ncost:decimal = 0
        proz:decimal = 0
        t_proz:decimal = 0
        f_endkum:int = 0
        b_endkum:int = 0
        H_art = H_artikel

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
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                pos = True

            if pos:
                for curr_datum in range(from_date,to_date + 1) :

                    if double_currency:
                        find_exrate(curr_datum)

                        if exrate:
                            rate = exrate.betrag
                        else:
                            rate = exchg_rate
                    rate = rate / fact1

                    if curr_datum == from_date:
                        h_list = H_list()
                        h_list_list.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = []
                    for artikel, umsatz in db_session.query(Artikel, Umsatz).join(Umsatz,(Umsatz.artnr == Artikel.artnr) &  (Umsatz.departement == Artikel.departement) &  (Umsatz.datum == curr_datum)).filter(
                            (Artikel.artart == 0) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == b_endkum) |  (Artikel.umsatzart == 6))).all():
                        if artikel._recid in artikel_obj_list:
                            continue
                        else:
                            artikel_obj_list.append(artikel._recid)


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat = vat + vat2

                        if umsatz.datum == to_date:
                            h_list.sales = h_list.sales + umsatz.betrag / fact
                            gsales = gsales + umsatz.betrag / fact
                            dd_gsales = dd_gsales + umsatz.betrag / fact
                        h_list.t_sales = h_list.t_sales + umsatz.betrag / fact
                        t_gsales = t_gsales + umsatz.betrag / fact
                        tot_gsales = tot_gsales + umsatz.betrag / fact

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                            (H_compli.departement == hoteldpt.num) &  (H_compli.datum == curr_datum) &  (H_compli.betriebsnr == 0)).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.departement == h_compli.departement) &  (H_artikel.artnr == h_compli.artnr)).first()

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                        if (artikel.endkum == b_endkum or artikel.umsatzart == 6):
                            cost = 0

                            h_cost = db_session.query(H_cost).filter(
                                    (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost = h_compli.anzahl * h_cost.betrag / fact1
                            else:
                                cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                            if h_compli.datum == to_date:
                                h_list.compli = h_list.compli + cost
                                h_list.comanz = h_list.comanz + h_compli.anzahl
                                gcompli = gcompli + cost
                                dd_gcompli = dd_gcompli + cost
                            h_list.t_compli = h_list.t_compli + cost
                            h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                            t_gcompli = t_gcompli + cost
                            tot_gcompli = tot_gcompli + cost

                    h_journal_obj_list = []
                    for h_journal, h_art, artikel in db_session.query(H_journal, H_art, Artikel).join(H_art,(H_art.artnr == H_journal.artnr) &  (H_art.departement == H_journal.departement) &  (H_art.artart == 0)).join(Artikel,(Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == h_art.departement) &  ((Artikel.endkum == b_endkum) |  (Artikel.umsatzart == 6))).filter(
                            (H_journal.departement == hoteldpt.num) &  (H_journal.bill_datum == curr_datum)).all():
                        if h_journal._recid in h_journal_obj_list:
                            continue
                        else:
                            h_journal_obj_list.append(h_journal._recid)


                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_journal.artnr) &  (H_cost.departement == h_journal.departement) &  (H_cost.datum == h_journal.bill_datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_journal.anzahl * h_cost.betrag / fact1
                        else:
                            cost = h_journal.anzahl * h_journal.epreis * rate * h_art.prozent / 100

                        if h_journal.bill_datum == to_date:
                            h_list.cost = h_list.cost + cost
                            gcost = gcost + cost
                            dd_gcost = dd_gcost + cost
                        h_list.t_cost = h_list.t_cost + cost
                        t_gcost = t_gcost + cost
                        tot_gcost = tot_gcost + cost

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()

        for h_list in query(h_list_list):
            h_list.ncost = h_list.cost - h_list.compli
            ncost = ncost + h_list.ncost
            dd_ncost = dd_ncost + h_list.ncost
            h_list.t_ncost = h_list.t_cost - h_list.t_compli
            t_ncost = t_ncost + h_list.t_ncost
            tot_ncost = tot_ncost + h_list.t_ncost

            if h_list.sales != 0:
                h_list.proz = h_list.ncost / h_list.sales * 100

            if h_list.t_sales != 0:
                h_list.t_proz = h_list.t_ncost / h_list.t_sales * 100
            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.cost, "     ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "      >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "      >>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "      >>,>>>,>>>,>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "     ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "        ->>>>>>>>>>9") + to_string(h_list.ncost, "        ->>>>>>>>>>9") + to_string(h_list.compli, "        ->>>>>>>>>>9") + to_string(h_list.cost, "        ->>>>>>>>>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "       >>>>>>>>>>>>9") + to_string(h_list.t_ncost, "         >>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "         >>>>>>>>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "        ->>>>>>>>>>9") + to_string(h_list.t_ncost, "        ->>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "        ->>>>>>>>>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
            else:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, "  ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.proz, "->>>>9"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                output_list.s = output_list.s + to_string(h_list.t_sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "  ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

        if gsales != 0:
            proz = ncost / gsales * 100

        if t_gsales != 0:
            t_proz = t_ncost / t_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, ">>>>>>>>>,>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

    def create_h_umsatz3():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        pos:bool = False
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        gsales:decimal = 0
        t_gsales:decimal = 0
        gcompli:decimal = 0
        t_gcompli:decimal = 0
        gcost:decimal = 0
        t_gcost:decimal = 0
        ncost:decimal = 0
        t_ncost:decimal = 0
        proz:decimal = 0
        t_proz:decimal = 0
        f_endkum:int = 0
        b_endkum:int = 0
        H_art = H_artikel

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
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                pos = True

            if pos:
                for curr_datum in range(from_date,to_date + 1) :

                    if double_currency:
                        find_exrate(curr_datum)

                        if exrate:
                            rate = exrate.betrag
                        else:
                            rate = exchg_rate
                    rate = rate / fact1

                    if curr_datum == from_date:
                        h_list = H_list()
                        h_list_list.append(h_list)

                        h_list.num = hoteldpt.num
                        h_list.depart = hoteldpt.depart

                    artikel_obj_list = []
                    for artikel, umsatz in db_session.query(Artikel, Umsatz).join(Umsatz,(Umsatz.artnr == Artikel.artnr) &  (Umsatz.departement == Artikel.departement) &  (Umsatz.datum == curr_datum)).filter(
                            (Artikel.artart == 0) &  (Artikel.departement == hoteldpt.num) &  (Artikel.umsatzart == 4)).all():
                        if artikel._recid in artikel_obj_list:
                            continue
                        else:
                            artikel_obj_list.append(artikel._recid)


                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))
                        vat = vat + vat2

                        if umsatz.datum == to_date:
                            h_list.sales = h_list.sales + umsatz.betrag / fact
                            gsales = gsales + umsatz.betrag / fact
                            dd_gsales = dd_gsales + umsatz.betrag / fact
                        h_list.t_sales = h_list.t_sales + umsatz.betrag / fact
                        t_gsales = t_gsales + umsatz.betrag / fact
                        tot_gsales = tot_gsales + umsatz.betrag / fact

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                            (H_compli.departement == hoteldpt.num) &  (H_compli.datum == curr_datum) &  (H_compli.betriebsnr == 0)).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.departement == h_compli.departement) &  (H_artikel.artnr == h_compli.artnr)).first()

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                        if artikel.umsatzart == 4:
                            cost = 0

                            h_cost = db_session.query(H_cost).filter(
                                    (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost = h_compli.anzahl * h_cost.betrag / fact1
                            else:
                                cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                            if h_compli.datum == to_date:
                                h_list.compli = h_list.compli + cost
                                h_list.comanz = h_list.comanz + h_compli.anzahl
                                gcompli = gcompli + cost
                                dd_gcompli = dd_gcompli + cost
                            h_list.t_compli = h_list.t_compli + cost
                            h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                            t_gcompli = t_gcompli + cost
                            tot_gcompli = tot_gcompli + cost

                    h_journal_obj_list = []
                    for h_journal, h_art, artikel in db_session.query(H_journal, H_art, Artikel).join(H_art,(H_art.artnr == H_journal.artnr) &  (H_art.departement == H_journal.departement) &  (H_art.artart == 0)).join(Artikel,(Artikel.artnr == h_art.artnrfront) &  (Artikel.departement == h_art.departement) &  (Artikel.umsatzart == 4)).filter(
                            (H_journal.departement == hoteldpt.num) &  (H_journal.bill_datum == curr_datum)).all():
                        if h_journal._recid in h_journal_obj_list:
                            continue
                        else:
                            h_journal_obj_list.append(h_journal._recid)


                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_journal.artnr) &  (H_cost.departement == h_journal.departement) &  (H_cost.datum == h_journal.bill_datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_journal.anzahl * h_cost.betrag / fact1
                        else:
                            cost = h_journal.anzahl * h_journal.epreis * rate * h_art.prozent / 100

                        if h_journal.bill_datum == to_date:
                            h_list.cost = h_list.cost + cost
                            gcost = gcost + cost
                            dd_gcost = dd_gcost + cost
                        h_list.t_cost = h_list.t_cost + cost
                        t_gcost = t_gcost + cost
                        tot_gcost = tot_gcost + cost

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()

        for h_list in query(h_list_list):
            h_list.ncost = h_list.cost - h_list.compli
            ncost = ncost + h_list.ncost
            dd_ncost = dd_ncost + h_list.ncost
            h_list.t_ncost = h_list.t_cost - h_list.t_compli
            t_ncost = t_ncost + h_list.t_ncost
            tot_ncost = tot_ncost + h_list.t_ncost

            if h_list.sales != 0:
                h_list.proz = h_list.ncost / h_list.sales * 100

            if h_list.t_sales != 0:
                h_list.t_proz = h_list.t_ncost / h_list.t_sales * 100
            output_list = Output_list()
            output_list_list.append(output_list)


            if htparam.finteger == 0 and short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.cost, "     ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "      >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "      >>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "      >>,>>>,>>>,>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "     ->>,>>>,>>>,>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "        ->>>>>>>>>>9") + to_string(h_list.ncost, "        ->>>>>>>>>>9") + to_string(h_list.compli, "        ->>>>>>>>>>9") + to_string(h_list.cost, "        ->>>>>>>>>>9")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                if h_list.t_sales >= 0:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "       >>>>>>>>>>>>9") + to_string(h_list.t_ncost, "         >>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "         >>>>>>>>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_sales, "        ->>>>>>>>>>9") + to_string(h_list.t_ncost, "        ->>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "        ->>>>>>>>>>9")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
            else:
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, "  ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                output_list.s = output_list.s + to_string(h_list.t_sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "  ->>,>>>,>>>,>>9.99")

                if len(trim(to_string(h_list.t_proz, "->>>>"))) > 3:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                else:
                    output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

        if gsales != 0:
            proz = ncost / gsales * 100

        if t_gsales != 0:
            t_proz = t_ncost / t_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, ">>>>>>>>>,>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

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
                output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "     ->>,>>>,>>>,>>9") + to_string(dd_ncost, "     ->>,>>>,>>>,>>9") + to_string(dd_gcompli, "     ->>,>>>,>>>,>>9") + to_string(dd_gcost, "     ->>,>>>,>>>,>>9") + to_string("      ")

                if tot_gsales >= 0:
                    output_list.s = output_list.s + to_string(tot_gsales, "      >>,>>>,>>>,>>9") + to_string(tot_ncost, "      >>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "      >>,>>>,>>>,>>9") + to_string("      ")
                else:
                    output_list.s = output_list.s + to_string(tot_gsales, "     ->>,>>>,>>>,>>9") + to_string(tot_ncost, "     ->>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "     ->>,>>>,>>>,>>9") + to_string("      ")

            elif htparam.finteger == 0 and not short_flag:
                output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "        ->>>>>>>>>>9") + to_string(dd_ncost, "        ->>>>>>>>>>9") + to_string(dd_gcompli, "        ->>>>>>>>>>9") + to_string(dd_gcost, "        ->>>>>>>>>>9") + to_string("      ")

                if t_gsales >= 0:
                    output_list.s = output_list.s + to_string(tot_gsales, ">>>>>>>>>,>>9") + to_string(tot_ncost, "         >>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "         >>>>>>>>>>9") + to_string("      ")
                else:
                    output_list.s = output_list.s + to_string(tot_gsales, "        ->>>>>>>>>>9") + to_string(tot_ncost, "        ->>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "        ->>>>>>>>>>9") + to_string("      ")
            else:
                output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, "  ->>,>>>,>>>,>>9.99") + to_string("      ") + to_string(tot_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99") + to_string("      ")

    def create_h_umsatz11():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        pos:bool = False
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        gsales:decimal = 0
        t_gsales:decimal = 0
        gcompli:decimal = 0
        t_gcompli:decimal = 0
        gcost:decimal = 0
        t_gcost:decimal = 0
        ncost:decimal = 0
        t_ncost:decimal = 0
        proz:decimal = 0
        t_proz:decimal = 0
        f_endkum:int = 0
        m_endkum:int = 0
        dd_gsales:decimal = 0
        dd_gcompli:decimal = 0
        dd_gcost:decimal = 0
        dd_ncost:decimal = 0
        tot_gsales:decimal = 0
        tot_gcompli:decimal = 0
        tot_gcost:decimal = 0
        tot_ncost:decimal = 0
        ind:int = 0
        price_decimal:int = 0
        H_art = H_artikel
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
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = []
                for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_Artikel.artnrfront) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == f_endkum) |  (Artikel.endkum == m_endkum) |  (Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5))).filter(
                        (H_artikel.artart == 0) &  (H_artikel.departement == hoteldpt.num)).all():
                    if h_artikel._recid in h_artikel_obj_list:
                        continue
                    else:
                        h_artikel_obj_list.append(h_artikel._recid)


                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.depart = h_artikel.bezeich

                    for h_umsatz in db_session.query(H_umsatz).filter(
                            (H_umsatz.departement == h_artikel.departement) &  (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.datum >= from_date) &  (H_umsatz.datum <= to_date)).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat = vat + vat2

                        if double_currency:
                            find_exrate(h_umsatz.datum)

                            if exrate:
                                rate = exrate.betrag
                            else:
                                rate = exchg_rate
                        rate = rate / fact1

                        if h_umsatz.datum == to_date:

                            if mi_compli_checked:
                                h_list.anz = h_list.anz + h_umsatz.anzahl
                            h_list.sales = h_list.sales + h_umsatz.betrag / fact
                            dd_gsales = dd_gsales + h_umsatz.betrag / fact

                        if mi_compli_checked:
                            h_list.m_anz = h_list.m_anz + h_umsatz.anzahl
                        h_list.t_sales = h_list.t_sales + h_umsatz.betrag / fact
                        tot_gsales = tot_gsales + h_umsatz.betrag / fact
                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_umsatz.artnr) &  (H_cost.departement == h_umsatz.departement) &  (H_cost.datum == h_umsatz.datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_cost.anzahl * h_cost.betrag / fact1

                            if not mi_compli_checked:

                                if h_umsatz.datum == to_date:
                                    h_list.anz = h_list.anz + h_cost.anzahl
                                h_list.m_anz = h_list.m_anz + h_cost.anzahl
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                    (H_journal.artnr == h_umsatz.artnr) &  (H_journal.departement == h_umsatz.departement) &  (H_journal.bill_datum == h_umsatz.datum)).all():
                                cost = cost + h_journal.anzahl * h_journal.epreis * h_artikel.prozent * rate / 100

                                if not mi_compli_checked:

                                    if h_umsatz.datum == to_date:
                                        h_list.anz = h_list.anz + h_journal.anzahl
                                    h_list.m_anz = h_list.m_anz + h_journal.anzahl

                        if h_umsatz.datum == to_date:
                            h_list.cost = h_list.cost + cost
                            dd_gcost = dd_gcost + cost
                        h_list.t_cost = h_list.t_cost + cost
                        tot_gcost = tot_gcost + cost

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                            (H_compli.departement == h_artikel.departement) &  (H_compli.artnr == h_artikel.artnr) &  (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.betriebsnr == 0)).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate = exrate.betrag
                            else:
                                rate = exchg_rate
                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_compli.anzahl * h_cost.betrag / fact1
                        else:
                            cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                        if h_compli.datum == to_date:
                            h_list.compli = h_list.compli + cost
                            h_list.comanz = h_list.comanz + h_compli.anzahl
                            dd_gcompli = dd_gcompli + cost

                            if not mi_compli_checked:
                                h_list.anz = h_list.anz - h_compli.anzahl
                        h_list.t_compli = h_list.t_compli + cost
                        h_list.t_comanz = h_list.t_comanz + h_compli.anzahl
                        tot_gcompli = tot_gcompli + cost

                        if not mi_compli_checked:
                            h_list.m_anz = h_list.m_anz - h_compli.anzahl

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger
        ind = 0
        gsales = 0
        ncost = 0
        gcompli = 0
        gcost = 0
        t_gsales = 0
        t_gcompli = 0
        t_gcost = 0
        t_ncost = 0
        t_proz = 0

        for h_list in query(h_list_list, filters=(lambda h_list :h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz = ncost / gsales * 100

                    if t_gsales != 0:
                        t_proz = t_ncost / t_gsales * 100
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz

                    if price_decimal == 0 and short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")

                    elif price_decimal == 0 and not short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                    else:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")
                        output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                ncost = 0
                gsales = 0
                gcompli = 0
                gcost = 0
                t_gsales = 0
                t_gcompli = 0
                t_gcost = 0
                t_ncost = 0
                t_proz = 0
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
            else:
                gsales = gsales + h_list.sales
                gcost = gcost + h_list.cost
                gcompli = gcompli + h_list.compli
                t_gsales = t_gsales + h_list.t_sales
                t_gcost = t_gcost + h_list.t_cost
                t_gcompli = t_gcompli + h_list.t_compli
                h_list.ncost = h_list.cost - h_list.compli
                ncost = ncost + h_list.ncost
                h_list.t_ncost = h_list.t_cost - h_list.t_compli
                t_ncost = t_ncost + h_list.t_ncost
                tot_ncost = tot_ncost + h_list.t_ncost

                if h_list.sales != 0:
                    h_list.proz = h_list.ncost / h_list.sales * 100

                if h_list.t_sales != 0:
                    h_list.t_proz = h_list.t_ncost / h_list.t_sales * 100
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz

                if htparam.finteger == 0 and short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.cost, "     ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.proz, "->>>>9"))) > 3:
                        output_list.s = OUTPUT_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "      >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "      >>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "      >>,>>>,>>>,>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "     ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                        output_list.s = OUTPUT_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

                elif htparam.finteger == 0 and not short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "        ->>>>>>>>>>9") + to_string(h_list.ncost, "        ->>>>>>>>>>9") + to_string(h_list.compli, "        ->>>>>>>>>>9") + to_string(h_list.cost, "        ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.proz, "->>>>9"))) > 3:
                        output_list.s = OUTPUT_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "       >>>>>>>>>>>>9") + to_string(h_list.t_ncost, "         >>>>>>>>>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "         >>>>>>>>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "        ->>>>>>>>>>9") + to_string(h_list.t_ncost, "        ->>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "        ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                        output_list.s = OUTPUT_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
                else:
                    output_list.s = to_string(h_list.depart, "x(23)") + to_string(h_list.sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, "  ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(proz, "->>>>9"))) > 3:
                        output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(proz, "->9.99")
                    output_list.s = output_list.s + to_string(h_list.t_sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "  ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(h_list.t_proz, "->>>>9"))) > 3:
                        output_list.s = OUTPUT_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
        proz = 0
        t_proz = 0

        if gsales != 0:
            proz = ncost / gsales * 100

        if t_gsales != 0:
            t_proz = t_ncost / t_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9") + to_string(t_proz, "->>.99")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9") + to_string(t_proz, "->>.99")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        proz = 0
        t_proz = 0
        dd_ncost = dd_gcost - dd_gcompli

        if dd_gsales != 0:
            proz = dd_ncost / dd_gsales * 100

        if tot_gsales != 0:
            t_proz = tot_ncost / tot_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "     ->>,>>>,>>>,>>9") + to_string(dd_ncost, "     ->>,>>>,>>>,>>9") + to_string(dd_gcompli, "     ->>,>>>,>>>,>>9") + to_string(dd_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, "      >>,>>>,>>>,>>9") + to_string(tot_ncost, "      >>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, "     ->>,>>>,>>>,>>9") + to_string(tot_ncost, "     ->>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "        ->>>>>>>>>>9") + to_string(dd_ncost, "        ->>>>>>>>>>9") + to_string(dd_gcompli, "        ->>>>>>>>>>9") + to_string(dd_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, "       >>>>>>>>>>>>9") + to_string(tot_ncost, "         >>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, "        ->>>>>>>>>>9") + to_string(tot_ncost, "        ->>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(tot_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

    def create_h_umsatz22():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        pos:bool = False
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        gsales:decimal = 0
        t_gsales:decimal = 0
        gcompli:decimal = 0
        t_gcompli:decimal = 0
        gcost:decimal = 0
        t_gcost:decimal = 0
        ncost:decimal = 0
        t_ncost:decimal = 0
        proz:decimal = 0
        t_proz:decimal = 0
        f_endkum:int = 0
        b_endkum:int = 0
        dd_gsales:decimal = 0
        dd_gcompli:decimal = 0
        dd_gcost:decimal = 0
        dd_ncost:decimal = 0
        tot_gsales:decimal = 0
        tot_gcompli:decimal = 0
        tot_gcost:decimal = 0
        tot_ncost:decimal = 0
        ind:int = 0
        price_decimal:int = 0
        H_art = H_artikel

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
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = []
                for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_Artikel.artnrfront) &  (Artikel.departement == hoteldpt.num) &  ((Artikel.endkum == b_endkum) |  (Artikel.umsatzart == 6))).filter(
                        (H_artikel.artart == 0) &  (H_artikel.departement == hoteldpt.num)).all():
                    if h_artikel._recid in h_artikel_obj_list:
                        continue
                    else:
                        h_artikel_obj_list.append(h_artikel._recid)


                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.depart = h_artikel.bezeich

                    for h_umsatz in db_session.query(H_umsatz).filter(
                            (H_umsatz.departement == h_artikel.departement) &  (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.datum >= from_date) &  (H_umsatz.datum <= to_date)).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat = vat + vat2

                        if double_currency:
                            find_exrate(h_umsatz.datum)

                            if exrate:
                                rate = exrate.betrag
                            else:
                                rate = exchg_rate
                        rate = rate / fact1

                        if h_umsatz.datum == to_date:

                            if mi_compli_checked:
                                h_list.anz = h_list.anz + h_umsatz.anzahl
                            h_list.sales = h_list.sales + h_umsatz.betrag / fact
                            dd_gsales = dd_gsales + h_umsatz.betrag / fact

                        if mi_compli_checked:
                            h_list.m_anz = h_list.m_anz + h_umsatz.anzahl
                        h_list.t_sales = h_list.t_sales + h_umsatz.betrag / fact
                        tot_gsales = tot_gsales + h_umsatz.betrag / fact
                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_umsatz.artnr) &  (H_cost.departement == h_umsatz.departement) &  (H_cost.datum == h_umsatz.datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_cost.anzahl * h_cost.betrag / fact1

                            if not mi_compli_checked:

                                if h_umsatz.datum == to_date:
                                    h_list.anz = h_list.anz + h_cost.anzahl
                                h_list.m_anz = h_list.m_anz + h_cost.anzahl
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                    (H_journal.artnr == h_umsatz.artnr) &  (H_journal.departement == h_umsatz.departement) &  (H_journal.bill_datum == h_umsatz.datum)).all():
                                cost = cost + h_journal.anzahl * h_journal.epreis * h_artikel.prozent * rate / 100

                                if not mi_compli_checked:

                                    if h_umsatz.datum == to_date:
                                        h_list.anz = h_list.anz + h_journal.anzahl
                                    h_list.m_anz = h_list.m_anz + h_journal.anzahl

                        if h_umsatz.datum == to_date:
                            h_list.cost = h_list.cost + cost
                            dd_gcost = dd_gcost + cost
                        h_list.t_cost = h_list.t_cost + cost
                        tot_gcost = tot_gcost + cost

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                            (H_compli.departement == h_artikel.departement) &  (H_compli.artnr == h_artikel.artnr) &  (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.betriebsnr == 0)).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate = exrate.betrag
                            else:
                                rate = exchg_rate
                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_compli.anzahl * h_cost.betrag / fact1
                        else:
                            cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                        if h_compli.datum == to_date:
                            h_list.compli = h_list.compli + cost
                            h_list.comanz = h_list.comanz + h_compli.anzahl
                            dd_gcompli = dd_gcompli + cost

                            if not mi_compli_checked:
                                h_list.anz = h_list.anz - h_compli.anzahl
                        h_list.t_compli = h_list.t_compli + cost
                        h_list.t_comanz = h_list.t_comanz + h_compli.anzahl

                        if not mi_compli_checked:
                            h_list.m_anz = h_list.m_anz - h_compli.anzahl
                        tot_gcompli = tot_gcompli + cost

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger
        ind = 0
        gsales = 0
        ncost = 0
        gcompli = 0
        gcost = 0
        t_gsales = 0
        t_gcompli = 0
        t_gcost = 0
        t_ncost = 0
        t_proz = 0

        for h_list in query(h_list_list, filters=(lambda h_list :h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz = ncost / gsales * 100

                    if t_gsales != 0:
                        t_proz = t_ncost / t_gsales * 100
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz

                    if price_decimal == 0 and short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")

                    elif price_decimal == 0 and not short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                    else:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")
                        output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(t_proz, "->>>>9"))) > 3:
                            output_list.s = OUTPUT_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                gsales = 0
                gcompli = 0
                gcost = 0
                ncost = 0
                t_gsales = 0
                t_gcompli = 0
                t_gcost = 0
                t_ncost = 0
                t_proz = 0
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
            else:
                gsales = gsales + h_list.sales
                gcost = gcost + h_list.cost
                gcompli = gcompli + h_list.compli
                t_gsales = t_gsales + h_list.t_sales
                t_gcost = t_gcost + h_list.t_cost
                t_gcompli = t_gcompli + h_list.t_compli
                h_list.ncost = h_list.cost - h_list.compli
                ncost = ncost + h_list.ncost
                h_list.t_ncost = h_list.t_cost - h_list.t_compli
                t_ncost = t_ncost + h_list.t_ncost
                tot_ncost = tot_ncost + h_list.t_ncost

                if h_list.sales != 0:
                    h_list.proz = h_list.ncost / h_list.sales * 100

                if h_list.t_sales != 0:
                    h_list.t_proz = h_list.t_ncost / h_list.t_sales * 100
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz

                if htparam.finteger == 0 and short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.cost, "     ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "      >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "      >>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "      >>,>>>,>>>,>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "     ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

                elif htparam.finteger == 0 and not short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "        ->>>>>>>>>>9") + to_string(h_list.ncost, "        ->>>>>>>>>>9") + to_string(h_list.compli, "        ->>>>>>>>>>9") + to_string(h_list.cost, "        ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "       >>>>>>>>>>>>9") + to_string(h_list.t_ncost, "         >>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "         >>>>>>>>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "        ->>>>>>>>>>9") + to_string(h_list.t_ncost, "        ->>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "        ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
                else:
                    output_list.s = to_string(h_list.depart, "x(23)") + to_string(h_list.sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, "  ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")
                    output_list.s = output_list.s + to_string(h_list.t_sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "  ->>,>>>,>>>,>>9.99")
        proz = 0
        t_proz = 0

        if gsales != 0:
            proz = ncost / gsales * 100

        if t_gsales != 0:
            t_proz = t_ncost / t_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->>.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        proz = 0
        t_proz = 0
        dd_ncost = dd_gcost - dd_gcompli

        if dd_gsales != 0:
            proz = dd_ncost / dd_gsales * 100

        if tot_gsales != 0:
            t_proz = tot_ncost / tot_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "     ->>,>>>,>>>,>>9") + to_string(dd_ncost, "     ->>,>>>,>>>,>>9") + to_string(dd_gcompli, "     ->>,>>>,>>>,>>9") + to_string(dd_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, "      >>,>>>,>>>,>>9") + to_string(tot_ncost, "      >>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, "     ->>,>>>,>>>,>>9") + to_string(tot_ncost, "     ->>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "        ->>>>>>>>>>9") + to_string(dd_ncost, "        ->>>>>>>>>>9") + to_string(dd_gcompli, "        ->>>>>>>>>>9") + to_string(dd_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, "       >>>>>>>>>>>>9") + to_string(tot_ncost, "         >>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, "        ->>>>>>>>>>9") + to_string(tot_ncost, "        ->>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")
            output_list.s = output_list.s + to_string(tot_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

    def create_h_umsatz33():

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        pos:bool = False
        rate:decimal = 1
        curr_datum:date = None
        cost:decimal = 0
        gsales:decimal = 0
        t_gsales:decimal = 0
        gcompli:decimal = 0
        t_gcompli:decimal = 0
        gcost:decimal = 0
        t_gcost:decimal = 0
        ncost:decimal = 0
        t_ncost:decimal = 0
        proz:decimal = 0
        t_proz:decimal = 0
        f_endkum:int = 0
        b_endkum:int = 0
        dd_gsales:decimal = 0
        dd_gcompli:decimal = 0
        dd_gcost:decimal = 0
        dd_ncost:decimal = 0
        tot_gsales:decimal = 0
        tot_gcompli:decimal = 0
        tot_gcost:decimal = 0
        tot_ncost:decimal = 0
        ind:int = 0
        price_decimal:int = 0
        H_art = H_artikel

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
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept)).all():
            pos = False

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.num = hoteldpt.num
                h_list.depart = hoteldpt.depart

                h_artikel_obj_list = []
                for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_Artikel.artnrfront) &  (Artikel.departement == hoteldpt.num) &  (Artikel.umsatzart == 4)).filter(
                        (H_artikel.artart == 0) &  (H_artikel.departement == hoteldpt.num)).all():
                    if h_artikel._recid in h_artikel_obj_list:
                        continue
                    else:
                        h_artikel_obj_list.append(h_artikel._recid)


                    h_list = H_list()
                    h_list_list.append(h_list)

                    h_list.depart = h_artikel.bezeich

                    for h_umsatz in db_session.query(H_umsatz).filter(
                            (H_umsatz.departement == h_artikel.departement) &  (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.datum >= from_date) &  (H_umsatz.datum <= to_date)).all():
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, h_umsatz.datum))
                        vat = vat + vat2

                        if double_currency:
                            find_exrate(h_umsatz.datum)

                            if exrate:
                                rate = exrate.betrag
                            else:
                                rate = exchg_rate
                        rate = rate / fact1

                        if h_umsatz.datum == to_date:

                            if mi_compli_checked:
                                h_list.anz = h_list.anz + h_umsatz.anzahl
                            h_list.sales = h_list.sales + h_umsatz.betrag / fact
                            dd_gsales = dd_gsales + h_umsatz.betrag / fact

                        if mi_compli_checked:
                            h_list.m_anz = h_list.m_anz + h_umsatz.anzahl
                        h_list.t_sales = h_list.t_sales + h_umsatz.betrag / fact
                        tot_gsales = tot_gsales + h_umsatz.betrag / fact
                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_umsatz.artnr) &  (H_cost.departement == h_umsatz.departement) &  (H_cost.datum == h_umsatz.datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_cost.anzahl * h_cost.betrag / fact1

                            if not mi_compli_checked:

                                if h_umsatz.datum == to_date:
                                    h_list.anz = h_list.anz + h_cost.anzahl
                                h_list.m_anz = h_list.m_anz + h_cost.anzahl
                        else:

                            for h_journal in db_session.query(H_journal).filter(
                                    (H_journal.artnr == h_umsatz.artnr) &  (H_journal.departement == h_umsatz.departement) &  (H_journal.bill_datum == h_umsatz.datum)).all():
                                cost = cost + h_journal.anzahl * h_journal.epreis * h_artikel.prozent * rate / 100

                                if not mi_compli_checked:

                                    if h_umsatz.datum == to_date:
                                        h_list.anz = h_list.anz + h_journal.anzahl
                                    h_list.m_anz = h_list.m_anz + h_journal.anzahl

                        if h_umsatz.datum == to_date:
                            h_list.cost = h_list.cost + cost
                            dd_gcost = dd_gcost + cost
                        h_list.t_cost = h_list.t_cost + cost
                        tot_gcost = tot_gcost + cost

                    h_compli_obj_list = []
                    for h_compli, h_art in db_session.query(H_compli, H_art).join(H_art,(H_art.departement == H_compli.departement) &  (H_art.artnr == H_compli.p_artnr) &  (H_art.artart == 11)).filter(
                            (H_compli.departement == h_artikel.departement) &  (H_compli.artnr == h_artikel.artnr) &  (H_compli.datum >= from_date) &  (H_compli.datum <= to_date) &  (H_compli.betriebsnr == 0)).all():
                        if h_compli._recid in h_compli_obj_list:
                            continue
                        else:
                            h_compli_obj_list.append(h_compli._recid)

                        if double_currency:
                            find_exrate(h_compli.datum)

                            if exrate:
                                rate = exrate.betrag
                            else:
                                rate = exchg_rate
                        cost = 0

                        h_cost = db_session.query(H_cost).filter(
                                (H_cost.artnr == h_compli.artnr) &  (H_cost.departement == h_compli.departement) &  (H_cost.datum == h_compli.datum) &  (H_cost.flag == 1)).first()

                        if h_cost and h_cost.betrag != 0:
                            cost = h_compli.anzahl * h_cost.betrag / fact1
                        else:
                            cost = h_compli.anzahl * h_compli.epreis * h_artikel.prozent / 100 * rate

                        if h_compli.datum == to_date:
                            h_list.compli = h_list.compli + cost
                            h_list.comanz = h_list.comanz + h_compli.anzahl
                            dd_gcompli = dd_gcompli + cost

                            if not mi_compli_checked:
                                h_list.anz = h_list.anz - h_compli.anzahl
                        h_list.t_compli = h_list.t_compli + cost
                        h_list.t_comanz = h_list.t_comanz + h_compli.anzahl

                        if not mi_compli_checked:
                            h_list.m_anz = h_list.m_anz - h_compli.anzahl
                        tot_gcompli = tot_gcompli + cost

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger
        ind = 0
        gsales = 0
        ncost = 0
        gcompli = 0
        gcost = 0
        t_gsales = 0
        t_gcompli = 0
        t_gcost = 0
        t_ncost = 0
        t_proz = 0

        for h_list in query(h_list_list, filters=(lambda h_list :h_list.t_cost != 0 or h_list.num != 0 or h_list.t_sales != 0 or h_list.t_compli != 0)):
            ind = ind + 1

            if h_list.num != 0:

                if ind > 1:

                    if gsales != 0:
                        proz = ncost / gsales * 100

                    if t_gsales != 0:
                        t_proz = t_ncost / t_gsales * 100
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.anz = h_list.anz
                    output_list.m_anz = h_list.m_anz
                    output_list.comanz = h_list.comanz
                    output_list.m_comanz = h_list.t_comanz

                    if price_decimal == 0 and short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

                        if len(trim(to_string(proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

                        if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")

                    elif price_decimal == 0 and not short_flag:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

                        if len(trim(to_string(proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")

                        if t_gsales >= 0:
                            output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

                        if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                    else:
                        output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(proz, "->9.99")
                        output_list.s = output_list.s + to_string(proz, "->>.99") + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

                        if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                            output_list.s = output_list.s + to_string(t_proz, "->>>>9")
                        else:
                            output_list.s = output_list.s + to_string(t_proz, "->9.99")
                gsales = 0
                gcompli = 0
                gcost = 0
                ncost = 0
                t_gsales = 0
                t_gcompli = 0
                t_gcost = 0
                t_ncost = 0
                t_proz = 0
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz
                output_list.s = to_string(h_list.num, "99 ") + to_string(h_list.depart, "x(20)")
            else:
                gsales = gsales + h_list.sales
                gcost = gcost + h_list.cost
                gcompli = gcompli + h_list.compli
                t_gsales = t_gsales + h_list.t_sales
                t_gcost = t_gcost + h_list.t_cost
                t_gcompli = t_gcompli + h_list.t_compli
                h_list.ncost = h_list.cost - h_list.compli
                ncost = ncost + h_list.ncost
                h_list.t_ncost = h_list.t_cost - h_list.t_compli
                t_ncost = t_ncost + h_list.t_ncost
                tot_ncost = tot_ncost + h_list.t_ncost

                if h_list.sales != 0:
                    h_list.proz = h_list.ncost / h_list.sales * 100

                if h_list.t_sales != 0:
                    h_list.t_proz = h_list.t_ncost / h_list.t_sales * 100
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.anz = h_list.anz
                output_list.m_anz = h_list.m_anz
                output_list.comanz = h_list.comanz
                output_list.m_comanz = h_list.t_comanz

                if htparam.finteger == 0 and short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.cost, "     ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "      >>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "      >>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "      >>,>>>,>>>,>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_ncost, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_compli, "     ->>,>>>,>>>,>>9") + to_string(h_list.t_cost, "     ->>,>>>,>>>,>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")

                elif htparam.finteger == 0 and not short_flag:
                    output_list.s = to_string(h_list.num, ">> ") + to_string(h_list.depart, "x(20)") + to_string(h_list.sales, "        ->>>>>>>>>>9") + to_string(h_list.ncost, "        ->>>>>>>>>>9") + to_string(h_list.compli, "        ->>>>>>>>>>9") + to_string(h_list.cost, "        ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.proz, "->9.99")

                    if h_list.t_sales >= 0:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "       >>>>>>>>>>>>9") + to_string(h_list.t_ncost, "         >>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "         >>>>>>>>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_sales, "        ->>>>>>>>>>9") + to_string(h_list.t_ncost, "        ->>>>>>>>>>9") + to_string(h_list.t_compli, "        ->>>>>>>>>>9") + to_string(h_list.t_cost, "        ->>>>>>>>>>9")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
                else:
                    output_list.s = to_string(h_list.depart, "x(23)") + to_string(h_list.sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.cost, "  ->>,>>>,>>>,>>9.99")
                    output_list.s = output_list.s + to_string(h_list.t_sales, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_compli, "  ->>,>>>,>>>,>>9.99") + to_string(h_list.t_cost, "  ->>,>>>,>>>,>>9.99")

                    if len(trim(to_string(h_list.t_proz, "->>>>>"))) > 3:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->>>>9")
                    else:
                        output_list.s = output_list.s + to_string(h_list.t_proz, "->9.99")
        proz = 0
        t_proz = 0

        if gsales != 0:
            proz = ncost / gsales * 100

        if t_gsales != 0:
            t_proz = t_ncost / t_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "     ->>,>>>,>>>,>>9") + to_string(ncost, "     ->>,>>>,>>>,>>9") + to_string(gcompli, "     ->>,>>>,>>>,>>9") + to_string(gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "      >>,>>>,>>>,>>9") + to_string(t_ncost, "      >>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "     ->>,>>>,>>>,>>9") + to_string(t_ncost, "     ->>,>>>,>>>,>>9") + to_string(t_gcompli, "     ->>,>>>,>>>,>>9") + to_string(t_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "        ->>>>>>>>>>9") + to_string(ncost, "        ->>>>>>>>>>9") + to_string(gcompli, "        ->>>>>>>>>>9") + to_string(gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if t_gsales >= 0:
                output_list.s = output_list.s + to_string(t_gsales, "       >>>>>>>>>>>>9") + to_string(t_ncost, "         >>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(t_gsales, "        ->>>>>>>>>>9") + to_string(t_ncost, "        ->>>>>>>>>>9") + to_string(t_gcompli, "        ->>>>>>>>>>9") + to_string(t_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("T O T A L", "x(23)") + to_string(gsales, "  ->>,>>>,>>>,>>9.99") + to_string(ncost, "  ->>,>>>,>>>,>>9.99") + to_string(gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
            output_list.s = output_list.s + to_string(t_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(t_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(t_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        proz = 0
        t_proz = 0
        dd_ncost = dd_gcost - dd_gcompli

        if dd_gsales != 0:
            proz = dd_ncost / dd_gsales * 100

        if tot_gsales != 0:
            t_proz = tot_ncost / tot_gsales * 100
        output_list = Output_list()
        output_list_list.append(output_list)


        if htparam.finteger == 0 and short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "     ->>,>>>,>>>,>>9") + to_string(dd_ncost, "     ->>,>>>,>>>,>>9") + to_string(dd_gcompli, "     ->>,>>>,>>>,>>9") + to_string(dd_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, "      >>,>>>,>>>,>>9") + to_string(tot_ncost, "      >>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "      >>,>>>,>>>,>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, "     ->>,>>>,>>>,>>9") + to_string(tot_ncost, "     ->>,>>>,>>>,>>9") + to_string(tot_gcompli, "     ->>,>>>,>>>,>>9") + to_string(tot_gcost, "     ->>,>>>,>>>,>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

        elif htparam.finteger == 0 and not short_flag:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "        ->>>>>>>>>>9") + to_string(dd_ncost, "        ->>>>>>>>>>9") + to_string(dd_gcompli, "        ->>>>>>>>>>9") + to_string(dd_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(proz, "->9.99")

            if tot_gsales >= 0:
                output_list.s = output_list.s + to_string(tot_gsales, "       >>>>>>>>>>>>9") + to_string(tot_ncost, "         >>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "         >>>>>>>>>>9")
            else:
                output_list.s = output_list.s + to_string(tot_gsales, "        ->>>>>>>>>>9") + to_string(tot_ncost, "        ->>>>>>>>>>9") + to_string(tot_gcompli, "        ->>>>>>>>>>9") + to_string(tot_gcost, "        ->>>>>>>>>>9")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
        else:
            output_list.s = to_string("GRAND TOTAL", "x(23)") + to_string(dd_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(dd_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(dd_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")
            output_list.s = output_list.s + to_string(tot_gsales, "  ->>,>>>,>>>,>>9.99") + to_string(tot_ncost, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcompli, "  ->>,>>>,>>>,>>9.99") + to_string(tot_gcost, "  ->>,>>>,>>>,>>9.99")

            if len(trim(to_string(t_proz, "->>>>>"))) > 3:
                output_list.s = output_list.s + to_string(t_proz, "->>>>9")
            else:
                output_list.s = output_list.s + to_string(t_proz, "->9.99")

    def find_exrate(curr_date:date):

        nonlocal output_list_list, exchg_rate, double_currency, foreign_nr, dd_gsales, dd_gcompli, dd_gcost, dd_ncost, tot_gsales, tot_gcompli, tot_gcost, tot_ncost, lvcarea, htparam, waehrung, h_artikel, hoteldpt, umsatz, artikel, h_compli, h_cost, h_journal, h_umsatz, exrate
        nonlocal h_art


        nonlocal h_list, output_list, h_art
        nonlocal h_list_list, output_list_list

        if foreign_nr != 0:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.artnr == foreign_nr) &  (Exrate.datum == curr_date)).first()
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
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit

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