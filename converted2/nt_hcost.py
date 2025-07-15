from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Waehrung, H_artikel, H_journal, H_cost, L_artikel, H_rezept, H_rezlin, H_compli, H_artcost, Artikel

def nt_hcost():
    bill_date:date = None
    cost:decimal = to_decimal("0.0")
    price:decimal = to_decimal("0.0")
    exchg_rate:decimal = 1
    exrate:decimal = 1
    double_currency:bool = False
    price_type:int = 0
    price_decimal:int = 0
    incl_service:bool = False
    incl_mwst:bool = False
    serv_taxable:bool = False
    i:int = 0
    htparam = waehrung = h_artikel = h_journal = h_cost = l_artikel = h_rezept = h_rezlin = h_compli = h_artcost = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, cost, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, i, htparam, waehrung, h_artikel, h_journal, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel

        return {}

    def cal_cost(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal bill_date, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, i, htparam, waehrung, h_artikel, h_journal, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel

        inh:decimal = to_decimal("0.0")
        h_recipe = None

        def generate_inner_output():
            return (cost)

        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if h_recipe.portion > 1:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)


            else:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

        return generate_inner_output()


    def create_hart_cost1():

        nonlocal bill_date, cost, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, htparam, waehrung, h_artikel, h_journal, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel

        qty:decimal = to_decimal("0.0")
        ind:int = 0
        i:int = 0
        ind = get_day(bill_date)

        for h_cost in db_session.query(H_cost).filter(
                 (H_cost.datum == bill_date)).order_by(H_cost._recid).all():

            if h_cost.flag == 1:
                qty =  to_decimal(h_cost.anzahl)

                h_compli = db_session.query(H_compli).filter(
                         (H_compli.artnr == h_cost.artnr) & (H_compli.departement == h_cost.departement) & (H_compli.betriebsnr == 0)).first()

                if h_compli:
                    qty =  to_decimal(qty) - to_decimal(h_compli.anzahl)

                if qty != 0:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_cost.artnr) & (H_artikel.departement == h_cost.departement)).first()

                    if h_artikel.artnrlager != 0:

                        l_artikel = db_session.query(L_artikel).filter(
                                 (L_artikel.artnr == h_artikel.artnrlager)).first()

                        if l_artikel:

                            h_artcost = db_session.query(H_artcost).filter(
                                     (H_artcost.artnr == l_artikel.artnr)).first()

                            if not h_artcost:
                                h_artcost = H_artcost()
                            db_session.add(h_artcost)

                            h_artcost.artnr = l_artikel.artnr
                            h_artcost.datum = bill_date
                            h_artcost.anzahl[ind - 1] = h_artcost.anzahl[ind - 1] + qty

                            if price_type == 0 or l_artikel.ek_aktuell == 0:
                                h_artcost.cost[ind - 1] = h_artcost.cost[ind - 1] + qty * l_artikel.vk_preis
                            else:
                                h_artcost.cost[ind - 1] = h_artcost.cost[ind - 1] + qty * l_artikel.ek_aktuell

                    elif h_artikel.artnrrezept != 0:

                        h_rezept = db_session.query(H_rezept).filter(
                                 (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                        if h_rezept:
                            cal_cost1(h_rezept.artnrrezept, 1, ind)


    def cal_cost1(p_artnr:int, menge:decimal, ind:int):

        nonlocal bill_date, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, i, htparam, waehrung, h_artikel, h_journal, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel

        cost:decimal = to_decimal("0.0")
        inh:decimal = to_decimal("0.0")
        qty:decimal = to_decimal("0.0")

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()
                qty =  to_decimal(inh) / to_decimal(l_artikel.inhalt)

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost =  to_decimal(cost) + to_decimal(qty) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost =  to_decimal(cost) + to_decimal(qty) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

                h_artcost = db_session.query(H_artcost).filter(
                         (H_artcost.artnr == l_artikel.artnr)).first()

                if not h_artcost:
                    h_artcost = H_artcost()
                db_session.add(h_artcost)

                h_artcost.artnr = l_artikel.artnr
                h_artcost.datum = bill_date
                h_artcost.anzahl[ind - 1] = h_artcost.anzahl[ind - 1] + qty
                h_artcost.cost[ind - 1] = h_artcost.cost[ind - 1] + cost


    def calculate_price(price:decimal):

        nonlocal bill_date, cost, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, i, htparam, waehrung, h_artikel, h_journal, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel

        artikel1 = None
        serv:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")

        def generate_inner_output():
            return (price)

        Artikel1 =  create_buffer("Artikel1",Artikel)

        artikel1 = db_session.query(Artikel1).filter(
                 (Artikel1.artnr == h_artikel.artnrfront) & (Artikel1.departement == h_artikel.departement)).first()

        if artikel1 and artikel1.pricetab and not double_currency:
            price =  to_decimal(price) * to_decimal(exrate)

        if incl_mwst or incl_service:
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(3, artikel1.artnr, artikel1.departement, bill_date))

            if serv != 0:
                fact =  to_decimal(serv) + to_decimal((1) + to_decimal(serv)) * to_decimal((vat) + to_decimal(vat2)) / to_decimal("100")
            else:
                fact =  to_decimal(serv) + to_decimal((vat) + to_decimal(vat2)) / to_decimal("100")
            fact =  to_decimal("1") + to_decimal(fact)
        price =  to_decimal(price) / to_decimal(fact)
        price = to_decimal(round(price , price_decimal))

        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 135)).first()
    incl_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 134)).first()
    incl_mwst = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1024)).first()
    price_type = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
             (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    if double_currency and waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    h_journal_obj_list = []
    for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.departement == H_journal.departement) & (H_artikel.artnr == H_journal.artnr) & (H_artikel.artart == 0)).filter(
             (H_journal.bill_datum == bill_date) & (H_journal.zeit >= 0) & (H_journal.sysdate >= bill_date)).order_by(H_journal.artnr, H_journal.departement).all():
        if h_journal._recid in h_journal_obj_list:
            continue
        else:
            h_journal_obj_list.append(h_journal._recid)

        if h_artikel.artnrlager != 0 or h_artikel.artnrrezept != 0 or h_artikel.prozent != 0:

            h_cost = db_session.query(H_cost).filter(
                     (H_cost.artnr == h_artikel.artnr) & (H_cost.departement == h_artikel.departement) & (H_cost.datum == bill_date) & (H_cost.flag == 1)).first()

            if not h_cost:
                h_cost = H_cost()
                db_session.add(h_cost)

                h_cost.datum = bill_date
                h_cost.departement = h_artikel.departement
                h_cost.artnr = h_artikel.artnr
                h_cost.flag = 1

                if h_artikel.artnrlager != 0:

                    l_artikel = db_session.query(L_artikel).filter(
                             (L_artikel.artnr == h_artikel.artnrlager)).first()

                    if l_artikel:

                        if price_type == 0 or l_artikel.ek_aktuell == 0:
                            h_cost.betrag =  to_decimal(l_artikel.vk_preis)
                        else:
                            h_cost.betrag =  to_decimal(l_artikel.ek_aktuell)

                elif h_artikel.artnrrezept != 0:

                    h_rezept = db_session.query(H_rezept).filter(
                             (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                    if h_rezept:
                        cost =  to_decimal("0")
                        cost = cal_cost(h_rezept.artnrrezept, 1, cost)
                        h_cost.betrag =  to_decimal(cost)
                else:
                    price =  to_decimal(h_artikel.epreis1)

                    if price != 0:
                        price = calculate_price(price)

                    if price == None:
                        price =  to_decimal("0")
                    h_cost.betrag =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
            h_cost.anzahl = h_cost.anzahl + h_journal.anzahl
    create_hart_cost1()
    procedur move_hartcost:

    h_artcost = db_session.query(H_artcost).first()
    while None != h_artcost:

        if h_artcost.datum != bill_date:
            for i in range(1,31 + 1) :
                h_artcost.lm_cost[i - 1] = h_artcost.cost[i - 1]
                h_artcost.lm_anzahl[i - 1] = h_artcost.anzahl[i - 1]
                h_artcost.cost[i - 1] = 0
                h_artcost.anzahl[i - 1] = 0
                h_artcost.datum = bill_date

        curr_recid = h_artcost._recid
        h_artcost = db_session.query(H_artcost).filter(H_artcost._recid > curr_recid).first()

    return generate_output()