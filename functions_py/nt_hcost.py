#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 21-10-2025 
# Issue : New compile program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_journal, Htparam, Waehrung, H_artikel, H_cost, L_artikel, H_rezept, H_rezlin, H_compli, H_artcost, Artikel

def nt_hcost():

    prepare_cache ([Htparam, Waehrung, H_artikel, H_cost, L_artikel, H_rezept, H_rezlin, H_compli, H_artcost, Artikel])

    bill_date:date = None
    cost:Decimal = to_decimal("0.0")
    price:Decimal = to_decimal("0.0")
    exchg_rate:Decimal = 1
    exrate:Decimal = 1
    double_currency:bool = False
    price_type:int = 0
    price_decimal:int = 0
    incl_service:bool = False
    incl_mwst:bool = False
    serv_taxable:bool = False
    create_it:bool = False
    portion:Decimal = 1
    h_journal = htparam = waehrung = h_artikel = h_cost = l_artikel = h_rezept = h_rezlin = h_compli = h_artcost = artikel = None

    t_hjournal = s_rezlin = None

    t_hjournal_data, T_hjournal = create_model_like(H_journal)
    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"h_recid":int, "pos":int, "artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "vk_preis":Decimal, "cost":Decimal, "menge":Decimal, "lostfact":Decimal, "recipe_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, cost, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, create_it, portion, h_journal, htparam, waehrung, h_artikel, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel


        nonlocal t_hjournal, s_rezlin
        nonlocal t_hjournal_data, s_rezlin_data

        return {}

    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal bill_date, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, create_it, portion, h_journal, htparam, waehrung, h_artikel, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel


        nonlocal t_hjournal, s_rezlin
        nonlocal t_hjournal_data, s_rezlin_data

        inh:Decimal = to_decimal("0.0")
        h_recipe = None

        def generate_inner_output():
            return (cost)

        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if h_recipe.portion > 1:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)


            else:
                inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

        return generate_inner_output()


    def create_hart_cost1():

        nonlocal bill_date, cost, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, create_it, portion, h_journal, htparam, waehrung, h_artikel, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel


        nonlocal t_hjournal, s_rezlin
        nonlocal t_hjournal_data, s_rezlin_data

        qty:Decimal = to_decimal("0.0")
        ind:int = 0
        i:int = 0
        ind = get_day(bill_date)

        for h_cost in db_session.query(H_cost).filter(
                 (H_cost.datum == bill_date)).order_by(H_cost._recid).all():

            if h_cost.flag == 1:
                qty =  to_decimal(h_cost.anzahl)

                h_compli = get_cache (H_compli, {"artnr": [(eq, h_cost.artnr)],"departement": [(eq, h_cost.departement)],"betriebsnr": [(eq, 0)]})

                if h_compli:
                    qty =  to_decimal(qty) - to_decimal(h_compli.anzahl)

                if qty != 0:

                    h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_cost.artnr)],"departement": [(eq, h_cost.departement)]})

                    if h_artikel.artnrlager != 0:

                        l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                        if l_artikel:

                            h_artcost = get_cache (H_artcost, {"artnr": [(eq, l_artikel.artnr)]})

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
                            pass

                    elif h_artikel.artnrrezept != 0:

                        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                        if h_rezept:
                            cal_cost1(h_rezept.artnrrezept, 1, ind)


    def cal_cost1(p_artnr:int, menge:Decimal, ind:int):

        nonlocal bill_date, price, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, create_it, portion, h_journal, htparam, waehrung, h_artikel, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel


        nonlocal t_hjournal, s_rezlin
        nonlocal t_hjournal_data, s_rezlin_data

        cost:Decimal = to_decimal("0.0")
        inh:Decimal = to_decimal("0.0")
        qty:Decimal = to_decimal("0.0")

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge)

            if h_rezlin.recipe_flag :
                cost = cal_cost(h_rezlin.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})
                qty =  to_decimal(inh) / to_decimal(l_artikel.inhalt)

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost =  to_decimal(cost) + to_decimal(qty) * to_decimal(l_artikel.vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))
                else:
                    cost =  to_decimal(cost) + to_decimal(qty) * to_decimal(l_artikel.ek_aktuell) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

                h_artcost = get_cache (H_artcost, {"artnr": [(eq, l_artikel.artnr)]})

                if not h_artcost:
                    h_artcost = H_artcost()
                    db_session.add(h_artcost)

                h_artcost.artnr = l_artikel.artnr
                h_artcost.datum = bill_date
                h_artcost.anzahl[ind - 1] = h_artcost.anzahl[ind - 1] + qty
                h_artcost.cost[ind - 1] = h_artcost.cost[ind - 1] + cost


    def calculate_price(price:Decimal):

        nonlocal bill_date, cost, exchg_rate, exrate, double_currency, price_type, price_decimal, incl_service, incl_mwst, serv_taxable, create_it, portion, h_journal, htparam, waehrung, h_artikel, h_cost, l_artikel, h_rezept, h_rezlin, h_compli, h_artcost, artikel


        nonlocal t_hjournal, s_rezlin
        nonlocal t_hjournal_data, s_rezlin_data

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
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(3, artikel1.artnr, artikel1.departement, bill_date))

            if serv != 0:
                fact =  to_decimal(serv) + to_decimal((1) + to_decimal(serv)) * to_decimal((vat) + to_decimal(vat2)) / to_decimal("100")
            else:
                fact =  to_decimal(serv) + to_decimal((vat) + to_decimal(vat2)) / to_decimal("100")
            fact =  to_decimal("1") + to_decimal(fact)
        price =  to_decimal(price) / to_decimal(fact)
        price = to_decimal(round(price , 2))

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_taxable = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if double_currency and waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    h_journal_obj_list = {}
    for h_journal, h_artikel in db_session.query(H_journal, H_artikel).join(H_artikel,(H_artikel.departement == H_journal.departement) & (H_artikel.artnr == H_journal.artnr) & (H_artikel.artart == 0)).filter(
             (H_journal.bill_datum == bill_date) & (H_journal.zeit >= 0) & (H_journal.sysdate >= bill_date)).order_by(H_journal.departement, H_journal.artnr).all():
        if h_journal_obj_list.get(h_journal._recid):
            continue
        else:
            h_journal_obj_list[h_journal._recid] = True


        create_it = True

        t_hjournal = query(t_hjournal_data, filters=(lambda t_hjournal: t_hjournal.artnr == h_journal.artnr and t_hjournal.departement == h_journal.departement and t_hjournal.betrag == - h_journal.betrag and t_hjournal.bill_datum == h_journal.bill_datum), first=True)

        if t_hjournal:
            t_hjournal_data.remove(t_hjournal)
            create_it = False

        if create_it:
            t_hjournal = T_hjournal()
            t_hjournal_data.append(t_hjournal)

            buffer_copy(h_journal, t_hjournal)

    h_artikel_obj_list = {}
    for h_artikel in db_session.query(H_artikel).filter(
             ((H_artikel.departement.in_(list(set([t_hjournal.departement for t_hjournal in t_hjournal_data if t_hjournal.bill_datum == bill_date] & (t_hjournal.zeit >= 0) & (t_hjournal.sysdate >= bill_date))))) & (H_artikel.artnr == t_hjournal.artnr) & (H_artikel.artart == 0))).order_by(t_hjournal.departement, t_hjournal.artnr).all():
        if h_artikel_obj_list.get(h_artikel._recid):
            continue
        else:
            h_artikel_obj_list[h_artikel._recid] = True

        t_hjournal = query(t_hjournal_data, (lambda t_hjournal: (h_artikel.departement == t_hjournal.departement)), first=True)

        if h_artikel.artnrlager != 0 or h_artikel.artnrrezept != 0 or h_artikel.prozent != 0:

            h_cost = get_cache (H_cost, {"artnr": [(eq, h_artikel.artnr)],"departement": [(eq, h_artikel.departement)],"datum": [(eq, bill_date)],"flag": [(eq, 1)]})

            if not h_cost:
                h_cost = H_cost()
                db_session.add(h_cost)

                h_cost.datum = bill_date
                h_cost.departement = h_artikel.departement
                h_cost.artnr = h_artikel.artnr
                h_cost.flag = 1

                if h_artikel.artnrlager != 0:

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_artikel.artnrlager)]})

                    if l_artikel:

                        if price_type == 0 or l_artikel.ek_aktuell == 0:
                            h_cost.betrag =  to_decimal(l_artikel.vk_preis)
                        else:
                            h_cost.betrag =  to_decimal(l_artikel.ek_aktuell)

                elif h_artikel.artnrrezept != 0:

                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                    if h_rezept:
                        cost =  to_decimal("0")
                        cost = get_output(fb_cost_count_recipe_costbl(h_rezept.artnrrezept, price_type, cost))
                        h_cost.betrag =  to_decimal(cost)
                else:
                    price =  to_decimal(h_artikel.epreis1)

                    if price != 0:
                        price = calculate_price(price)

                    if price == None:
                        price =  to_decimal("0")
                    h_cost.betrag =  to_decimal(h_artikel.prozent) / to_decimal("100") * to_decimal(price) * to_decimal(exchg_rate)
            h_cost.anzahl = h_cost.anzahl + t_hjournal.anzahl
    create_hart_cost1()

    return generate_output()