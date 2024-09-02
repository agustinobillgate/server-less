from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_artikel, Hoteldpt, Artikel, H_cost, H_umsatz, H_journal, Wgrpdep

def menu_eng_btn_go_webbl(subgr_list:[Subgr_list], sorttype:int, from_dept:int, to_dept:int, dstore:int, ldry_dept:int, all_sub:bool, from_date:date, to_date:date, fact1:int, exchg_rate:decimal, vat_included:bool, mi_subgrp:bool, detailed:bool, curr_sort:int, short_flag:bool):
    fb_cost_analyst_list = []
    t_anz:int = 0
    t_sales:decimal = 0
    t_cost:decimal = 0
    t_margin:decimal = 0
    st_sales:decimal = 0
    st_cost:decimal = 0
    st_margin:decimal = 0
    st_proz2:decimal = 0
    s_anzahl:int = 0
    s_proz1:decimal = 0
    h_artikel = hoteldpt = artikel = h_cost = h_umsatz = h_journal = wgrpdep = None

    subgr_list = h_list = fb_cost_analyst = h_art = None

    subgr_list_list, Subgr_list = create_model("Subgr_list", {"selected":bool, "zknr":int, "bezeich":str}, {"selected": True})
    h_list_list, H_list = create_model("H_list", {"flag":str, "artnr":int, "dept":int, "bezeich":str, "zknr":int, "grpname":str, "anzahl":int, "proz1":decimal, "epreis":decimal, "cost":decimal, "margin":decimal, "t_sales":decimal, "t_cost":decimal, "t_margin":decimal, "proz2":decimal})
    fb_cost_analyst_list, Fb_cost_analyst = create_model("Fb_cost_analyst", {"flag":int, "artnr":str, "bezeich":str, "qty":str, "proz1":str, "epreis":str, "cost":str, "margin":str, "t_sales":str, "t_cost":str, "t_margin":str, "proz2":str})

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list
        return {"fb-cost-analyst": fb_cost_analyst_list}

    def create_h_umsatz1():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        do_it:bool = False
        cost:decimal = 0
        anz:int = 0
        H_art = H_artikel
        fb_cost_analyst_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept) &  (Hoteldpt.num != dstore) &  (Hoteldpt.num != ldry_dept)).all():

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = []
            for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_Artikel.artnrfront) &  (Artikel.departement == H_Artikel.departement) &  ((Artikel.umsatzart == 3) |  (Artikel.umsatzart == 5)) &  (Artikel.endkum != disc_nr)).filter(
                    (H_artikel.artart == 0) &  (H_artikel.departement == hoteldpt.num)).all():
                if h_artikel._recid in h_artikel_obj_list:
                    continue
                else:
                    h_artikel_obj_list.append(h_artikel._recid)


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list :subgr_list.zknr == h_artikel.zwkum and subgr_list.SELECTED), first=True)
                    do_it = None != subgr_list

                if do_it:

                    h_cost = db_session.query(H_cost).filter(
                            (H_cost.artnr == h_artikel.artnr) &  (H_cost.departement == h_artikel.departement) &  (H_cost.datum == to_date) &  (H_cost.flag == 1)).first()
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat = vat + vat2


                    h_list = H_list()
                    h_list_list.append(h_list)


                    if h_cost and h_cost.betrag != 0:
                        h_list.cost = h_cost.betrag
                    else:
                        h_list.cost = h_artikel.epreis1 * h_artikel.prozent / 100 * exchg_rate
                    h_list.cost = h_list.cost / fact1
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / fact
                    else:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / fact1
                    for datum in range(from_date,to_date + 1) :
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                        vat = vat + vat2

                        h_umsatz = db_session.query(H_umsatz).filter(
                                (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.departement == h_artikel.departement) &  (H_umsatz.datum == datum)).first()

                        if h_umsatz:
                            anz = h_umsatz.anzahl
                            cost = 0

                            h_cost = db_session.query(H_cost).filter(
                                    (H_cost.artnr == h_artikel.artnr) &  (H_cost.departement == h_artikel.departement) &  (H_cost.datum == datum) &  (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost = anz * h_cost.betrag
                                h_list.cost = h_cost.betrag
                            else:

                                h_journal = db_session.query(H_journal).filter(
                                        (H_journal.artnr == h_artikel.artnr) &  (H_journal.departement == h_artikel.departement) &  (H_journal.bill_datum == datum)).first()

                                if h_journal:
                                    cost = anz * h_journal.epreis * h_artikel.prozent / 100
                                else:
                                    cost = anz * h_artikel.epreis1 * h_artikel.prozent / 100 * exchg_rate
                                h_list.cost = h_artikel.epreis1 * h_artikel.prozent / 100 * exchg_rate
                            cost = cost / fact1
                            h_list.anzahl = h_list.anzahl + anz
                            h_list.t_cost = h_list.t_cost + cost
                            h_list.t_sales = h_list.t_sales + h_umsatz.betrag / fact
                            t_cost = t_cost + cost
                            t_anz = t_anz + anz
                            t_sales = t_sales + h_umsatz.betrag / fact

                    if h_list.epreis != 0:
                        h_list.margin = h_list.cost / h_list.epreis * 100
            create_list(pos)
            t_anz = 0
            t_sales = 0
            t_cost = 0

    def create_h_umsatz2():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list

        disc_flag:bool = False
        disc_nr:int = 0
        dept:int = -1
        pos:bool = False
        datum:date = None
        vat:decimal = 0
        serv:decimal = 0
        vat2:decimal = 0
        serv_vat:bool = False
        fact:decimal = 0
        do_it:bool = False
        cost:decimal = 0
        anz:int = 0
        H_art = H_artikel
        fb_cost_analyst_list.clear()
        h_list_list.clear()

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept) &  (Hoteldpt.num != dstore) &  (Hoteldpt.num != ldry_dept)).all():

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.departement == hoteldpt.num)).first()

            if h_artikel:
                pos = True
            else:
                pos = False

            if pos:
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)

                fb_cost_analyst.bezeich = to_string(hoteldpt.num, "99 ") + to_string(hoteldpt.depart, "x(21)")
            dept = hoteldpt.num

            h_artikel_obj_list = []
            for h_artikel, artikel in db_session.query(H_artikel, Artikel).join(Artikel,(Artikel.artnr == H_Artikel.artnrfront) &  (Artikel.departement == H_Artikel.departement) &  (Artikel.umsatzart == 6) &  (Artikel.endkum != disc_nr)).filter(
                    (H_artikel.artart == 0) &  (H_artikel.departement == hoteldpt.num)).all():
                if h_artikel._recid in h_artikel_obj_list:
                    continue
                else:
                    h_artikel_obj_list.append(h_artikel._recid)


                do_it = False

                if all_sub:
                    do_it = True
                else:

                    subgr_list = query(subgr_list_list, filters=(lambda subgr_list :subgr_list.zknr == h_artikel.zwkum and subgr_list.SELECTED), first=True)
                    do_it = None != subgr_list

                if do_it:

                    h_cost = db_session.query(H_cost).filter(
                            (H_cost.artnr == h_artikel.artnr) &  (H_cost.departement == h_artikel.departement) &  (H_cost.datum == to_date) &  (H_cost.flag == 1)).first()
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                    vat = vat + vat2


                    h_list = H_list()
                    h_list_list.append(h_list)


                    if h_cost and h_cost.betrag != 0:
                        h_list.cost = h_cost.betrag
                    else:
                        h_list.cost = h_artikel.epreis1 * h_artikel.prozent / 100 * exchg_rate
                    h_list.cost = h_list.cost / fact1
                    h_list.dept = h_artikel.departement
                    h_list.artnr = h_artikel.artnr
                    h_list.dept = h_artikel.departement
                    h_list.bezeich = h_artikel.bezeich
                    h_list.zknr = h_artikel.zwkum

                    if vat_included:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / fact
                    else:
                        h_list.epreis = h_artikel.epreis1 * exchg_rate / fact1
                    for datum in range(from_date,to_date + 1) :
                        serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))
                        vat = vat + vat2

                        h_umsatz = db_session.query(H_umsatz).filter(
                                (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.departement == h_artikel.departement) &  (H_umsatz.datum == datum)).first()

                        if h_umsatz:
                            anz = h_umsatz.anzahl
                            cost = 0

                            h_cost = db_session.query(H_cost).filter(
                                    (H_cost.artnr == h_artikel.artnr) &  (H_cost.departement == h_artikel.departement) &  (H_cost.datum == datum) &  (H_cost.flag == 1)).first()

                            if h_cost and h_cost.betrag != 0:
                                cost = anz * h_cost.betrag
                                h_list.cost = h_cost.betrag
                            else:

                                h_journal = db_session.query(H_journal).filter(
                                        (H_journal.artnr == h_artikel.artnr) &  (H_journal.departement == h_artikel.departement) &  (H_journal.bill_datum == datum)).first()

                                if h_journal:
                                    cost = anz * h_journal.epreis * h_artikel.prozent / 100
                                else:
                                    cost = anz * h_artikel.epreis1 * h_artikel.prozent / 100 * exchg_rate
                                h_list.cost = h_artikel.epreis1 * h_artikel.prozent / 100 * exchg_rate
                            cost = cost / fact1
                            h_list.anzahl = h_list.anzahl + anz
                            h_list.t_cost = h_list.t_cost + cost
                            h_list.t_sales = h_list.t_sales + h_umsatz.betrag / fact
                            t_cost = t_cost + cost
                            t_anz = t_anz + anz
                            t_sales = t_sales + h_umsatz.betrag / fact

                    if h_list.epreis != 0:
                        h_list.margin = h_list.cost / h_list.epreis * 100
            create_list(pos)
            t_anz = 0
            t_sales = 0
            t_cost = 0

    def create_list(pos:bool):

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list

        if mi_subgrp:
            create_list1(pos)

            return

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num)):

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num)):

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num)):

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")

        if pos and t_sales != 0:
            t_margin = 0

            if t_sales != 0:
                t_margin = t_cost / t_sales * 100
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)


            if short_flag:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, ">>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "  ->>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(t_cost, "  ->>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(t_margin, "->>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, ">>9.99")


            else:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, ">>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(t_cost, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(t_margin, "->>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, ">>9.99")


            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)


    def create_list1(pos:bool):

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list

        curr_grp:int = 0

        if detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num)):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.departement == h_list.dept) &  (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                add_sub()

        elif detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num)):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.departement == h_list.dept) &  (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                add_sub()

        elif detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num)):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.departement == h_list.dept) &  (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                add_sub()

        elif not detailed and curr_sort == 1:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.departement == h_list.dept) &  (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                add_sub()

        elif not detailed and curr_sort == 2:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.departement == h_list.dept) &  (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                add_sub()

        elif not detailed and curr_sort == 3:

            for h_list in query(h_list_list, filters=(lambda h_list :h_list.dept == hoteldpt.num and (h_list.t_sales != 0 or h_list.anzahl != 0))):

                if curr_grp != h_list.zknr:
                    create_sub(curr_grp)

                    wgrpdep = db_session.query(Wgrpdep).filter(
                                (Wgrpdep.departement == h_list.dept) &  (Wgrpdep.zknr == h_list.zknr)).first()
                    curr_grp = h_list.zknr
                    fb_cost_analyst = Fb_cost_analyst()
                    fb_cost_analyst_list.append(fb_cost_analyst)

                    fb_cost_analyst.flag = 1
                    fb_cost_analyst.bezeich = to_string(wgrpdep.bezeich, "x(24)")

                if t_anz != 0:
                    h_list.proz1 = h_list.anzahl / t_anz * 100

                if h_list.t_sales != 0:
                    h_list.t_margin = h_list.t_cost / h_list.t_sales * 100

                if t_sales != 0:
                    h_list.proz2 = h_list.t_sales / t_sales * 100
                fb_cost_analyst = Fb_cost_analyst()
                fb_cost_analyst_list.append(fb_cost_analyst)


                if short_flag:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->,>>>,>>9.9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->,>>>,>>9.9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->>>,>>>,>>9.9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                else:
                    fb_cost_analyst.artnr = to_string(h_list.artnr, ">>>>>9")
                    fb_cost_analyst.bezeich = to_string(h_list.bezeich, "x(24)")
                    fb_cost_analyst.qty = to_string(h_list.anzahl, "->>>>9")
                    fb_cost_analyst.proz1 = to_string(h_list.proz1, "->>9.9")
                    fb_cost_analyst.epreis = to_string(h_list.epreis, "->>>,>>>,>>9")
                    fb_cost_analyst.cost = to_string(h_list.cost, "->>>,>>>,>>9")
                    fb_cost_analyst.margin = to_string(h_list.margin, "->>>,>>9.99")
                    fb_cost_analyst.t_sales = to_string(h_list.t_sales, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_cost = to_string(h_list.t_cost, "->,>>>,>>>,>>9")
                    fb_cost_analyst.t_margin = to_string(h_list.t_margin, "->>>,>>9.99")
                    fb_cost_analyst.proz2 = to_string(h_list.proz2, "->>9.9")


                add_sub()
        create_sub(curr_grp)

        if pos and t_sales != 0:
            t_margin = 0

            if t_sales != 0:
                t_margin = t_cost / t_sales * 100
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)


            if short_flag:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, ">>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "  ->>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(t_cost, "  ->>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(t_margin, "->>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, ">>9.99")


            else:
                fb_cost_analyst.artnr = to_string("")
                fb_cost_analyst.bezeich = to_string("T o t a l")
                fb_cost_analyst.qty = to_string(t_anz, ">>,>>9")
                fb_cost_analyst.proz1 = to_string(100, ">>9.99")
                fb_cost_analyst.epreis = to_string("")
                fb_cost_analyst.cost = to_string("")
                fb_cost_analyst.margin = to_string("")
                fb_cost_analyst.t_sales = to_string(t_sales, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_cost = to_string(t_cost, "->,>>>,>>>,>>9")
                fb_cost_analyst.t_margin = to_string(t_margin, "->>>,>>9.99")
                fb_cost_analyst.proz2 = to_string(100, ">>9.99")


            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)


    def create_sub(curr_grp:int):

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list

        if curr_grp != 0:

            if st_sales != 0:
                st_margin = st_cost / st_sales * 100
            fb_cost_analyst = Fb_cost_analyst()
            fb_cost_analyst_list.append(fb_cost_analyst)

            fb_cost_analyst.flag = 2
            fb_cost_analyst.artnr = to_string("")
            fb_cost_analyst.bezeich = to_string("S u b T o t a l")
            fb_cost_analyst.qty = to_string(s_anzahl, "->>>>9")
            fb_cost_analyst.proz1 = to_string(s_proz1, "->>9.9")
            fb_cost_analyst.epreis = to_string("")
            fb_cost_analyst.cost = to_string("")
            fb_cost_analyst.margin = to_string("")
            fb_cost_analyst.t_sales = to_string(st_sales, "->,>>>,>>>,>>9")
            fb_cost_analyst.t_cost = to_string(st_cost, "->,>>>,>>>,>>9")
            fb_cost_analyst.t_margin = to_string(st_margin, "->>>,>>9.99")
            fb_cost_analyst.proz2 = to_string(st_proz2, "->>9.9")


            s_anzahl = 0
            s_proz1 = 0
            st_sales = 0
            st_cost = 0
            st_margin = 0
            st_proz2 = 0

    def add_sub():

        nonlocal fb_cost_analyst_list, t_anz, t_sales, t_cost, t_margin, st_sales, st_cost, st_margin, st_proz2, s_anzahl, s_proz1, h_artikel, hoteldpt, artikel, h_cost, h_umsatz, h_journal, wgrpdep
        nonlocal h_art


        nonlocal subgr_list, h_list, fb_cost_analyst, h_art
        nonlocal subgr_list_list, h_list_list, fb_cost_analyst_list


        s_anzahl = s_anzahl + h_list.anzahl
        st_sales = st_sales + h_list.t_sales
        st_cost = st_cost + h_list.t_cost
        s_proz1 = s_proz1 + h_list.proz1
        st_proz2 = st_proz2 + h_list.proz2

    if sorttype == 1:
        create_h_umsatz1()

    elif sorttype == 2:
        create_h_umsatz2()

    return generate_output()