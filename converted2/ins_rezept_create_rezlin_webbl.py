#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezlin, H_rezept, L_artikel, Queasy

def ins_rezept_create_rezlin_webbl(artnr:int, h_artnr:int, s_artnr:int, qty:Decimal, recipetype:int, price_type:int, inhalt:Decimal, descript:string, lostfact:Decimal, cost_percent:Decimal, poten_sell_price:Decimal):

    prepare_cache ([H_rezlin, H_rezept, L_artikel, Queasy])

    warn_flag = 0
    vk_preis = to_decimal("0.0")
    inh:Decimal = to_decimal("0.0")
    s_rezlin_data = []
    curr_pos:int = 0
    recipe_cost:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    portion:int = 0
    h_rezlin = h_rezept = l_artikel = queasy = None

    s_rezlin = h_rezlin1 = hrecipe = None

    s_rezlin_data, S_rezlin = create_model("S_rezlin", {"new_created":bool, "h_recid":int, "pos":int, "artnr":int, "bezeich":string, "masseinheit":string, "inhalt":Decimal, "vk_preis":Decimal, "cost":Decimal, "menge":Decimal, "lostfact":Decimal, "recipe_flag":bool, "s_unit":string})

    H_rezlin1 = create_buffer("H_rezlin1",H_rezlin)
    Hrecipe = create_buffer("Hrecipe",H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal warn_flag, vk_preis, inh, s_rezlin_data, curr_pos, recipe_cost, amount, portion, h_rezlin, h_rezept, l_artikel, queasy
        nonlocal artnr, h_artnr, s_artnr, qty, recipetype, price_type, inhalt, descript, lostfact, cost_percent, poten_sell_price
        nonlocal h_rezlin1, hrecipe


        nonlocal s_rezlin, h_rezlin1, hrecipe
        nonlocal s_rezlin_data

        return {"warn_flag": warn_flag, "vk_preis": vk_preis, "s-rezlin": s_rezlin_data}

    def create_amount():

        nonlocal warn_flag, inh, s_rezlin_data, curr_pos, recipe_cost, amount, portion, h_rezlin, h_rezept, l_artikel, queasy
        nonlocal artnr, h_artnr, s_artnr, qty, recipetype, price_type, inhalt, descript, lostfact, cost_percent, poten_sell_price
        nonlocal h_rezlin1, hrecipe


        nonlocal s_rezlin, h_rezlin1, hrecipe
        nonlocal s_rezlin_data

        cost:Decimal = to_decimal("0.0")
        cost2:Decimal = to_decimal("0.0")
        h_recipe = None
        vk_preis:Decimal = to_decimal("0.0")
        H_recipe =  create_buffer("H_recipe",H_rezept)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == h_artnr)).order_by(H_rezlin._recid).all():
            curr_pos = curr_pos + 1

            if h_rezlin.recipe_flag == False:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost2 =  to_decimal(h_rezlin.menge) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

            elif h_rezlin.recipe_flag :
                cost = cal_cost(h_rezlin1.artnrlager, inh, cost)
                cost2 =  to_decimal(cost2) + to_decimal(cost)
            amount =  to_decimal(amount) + to_decimal(cost2)


    def create_rezlin():

        nonlocal warn_flag, vk_preis, inh, s_rezlin_data, curr_pos, recipe_cost, amount, portion, h_rezlin, h_rezept, l_artikel, queasy
        nonlocal artnr, h_artnr, s_artnr, qty, recipetype, price_type, inhalt, descript, lostfact, cost_percent, poten_sell_price
        nonlocal h_rezlin1, hrecipe


        nonlocal s_rezlin, h_rezlin1, hrecipe
        nonlocal s_rezlin_data

        cost:Decimal = to_decimal("0.0")
        curr_pos = curr_pos + 1
        s_rezlin = S_rezlin()
        s_rezlin_data.append(s_rezlin)

        s_rezlin.pos = curr_pos
        s_rezlin.artnr = s_artnr
        s_rezlin.bezeich = descript
        s_rezlin.menge =  to_decimal(qty)
        s_rezlin.lostfact =  to_decimal(lostfact)
        s_rezlin.new_created = True

        if recipetype == 1:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

            if price_type == 0 or l_artikel.ek_aktuell == 0:
                vk_preis =  to_decimal(l_artikel.vk_preis)
            else:
                vk_preis =  to_decimal(l_artikel.ek_aktuell)
            s_rezlin.masseinheit = to_string(l_artikel.masseinheit, "x(3)")
            s_rezlin.inhalt =  to_decimal(l_artikel.inhalt)
            s_rezlin.vk_preis =  to_decimal(vk_preis)
            s_rezlin.cost =  to_decimal(qty) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(s_rezlin.lostfact) / to_decimal(100))
            amount =  to_decimal(amount) + to_decimal(s_rezlin.cost)

            if num_entries(l_artikel.herkunft, ";") > 1:
                s_rezlin.s_unit = entry(1, l_artikel.herkunft, ";")

            if s_rezlin.s_unit == " ":
                s_rezlin.s_unit = l_artikel.masseinheit

            if s_rezlin.cost == 0:
                warn_flag = 1
            poten_sell_price =  to_decimal("100") / to_decimal(cost_percent) * to_decimal(amount) / to_decimal(portion)

            queasy = get_cache (Queasy, {"key": [(eq, 252)],"number1": [(eq, h_artnr)]})

            if queasy:
                queasy.deci1 =  to_decimal(cost_percent)
                queasy.deci2 =  to_decimal(poten_sell_price)


                pass
                pass
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 252
                queasy.number1 = h_artnr
                queasy.date1 = get_current_date()
                queasy.deci1 =  to_decimal(cost_percent)
                queasy.deci2 =  to_decimal(poten_sell_price)


                pass

        elif recipetype == 2:

            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, artnr)]})

            if h_rezept:

                for h_rezlin1 in db_session.query(H_rezlin1).filter(
                         (H_rezlin1.artnrrezept == artnr)).order_by(H_rezlin1._recid).all():

                    hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin1.artnrrezept)]})

                    if hrecipe.portion > 1:
                        inh =  to_decimal(qty) * to_decimal(h_rezlin1.menge) / to_decimal(hrecipe.portion)


                    else:
                        inh =  to_decimal(qty) * to_decimal(h_rezlin1.menge)

                    if h_rezlin1.recipe_flag :
                        cost = cal_cost(h_rezlin1.artnrlager, inh, cost)
                    else:

                        l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin1.artnrlager)]})

                        if price_type == 0 or l_artikel.ek_aktuell == 0:
                            vk_preis =  to_decimal(l_artikel.vk_preis)
                        else:
                            vk_preis =  to_decimal(l_artikel.ek_aktuell)
                        cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin1.lostfact) / to_decimal(100))
                s_rezlin.recipe_flag = True
                s_rezlin.inhalt =  to_decimal(inhalt)
                s_rezlin.cost =  to_decimal(cost)

                if s_rezlin.cost == 0:
                    warn_flag = 2
                amount =  to_decimal(amount) + to_decimal(s_rezlin.cost)
                poten_sell_price =  to_decimal("100") / to_decimal(cost_percent) * to_decimal(amount) / to_decimal(portion)

                queasy = get_cache (Queasy, {"key": [(eq, 252)],"number1": [(eq, h_artnr)]})

                if queasy:
                    queasy.deci1 =  to_decimal(cost_percent)
                    queasy.deci2 =  to_decimal(poten_sell_price)


                    pass
                    pass
                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 252
                    queasy.number1 = h_artnr
                    queasy.date1 = get_current_date()
                    queasy.deci1 =  to_decimal(cost_percent)
                    queasy.deci2 =  to_decimal(poten_sell_price)


                    pass
        h_rezlin = H_rezlin()
        db_session.add(h_rezlin)

        h_rezlin.artnrrezept = h_artnr
        h_rezlin.artnrlager = s_rezlin.artnr
        h_rezlin.menge =  to_decimal(s_rezlin.menge)
        h_rezlin.lostfact =  to_decimal(s_rezlin.lostfact)
        h_rezlin.recipe_flag = s_rezlin.recipe_flag
        pass
        s_rezlin.h_recid = h_rezlin._recid


    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal warn_flag, s_rezlin_data, curr_pos, recipe_cost, amount, portion, h_rezlin, h_rezept, l_artikel, queasy
        nonlocal artnr, h_artnr, s_artnr, qty, recipetype, price_type, inhalt, descript, lostfact, cost_percent, poten_sell_price
        nonlocal h_rezlin1, hrecipe


        nonlocal s_rezlin, h_rezlin1, hrecipe
        nonlocal s_rezlin_data

        inh:Decimal = to_decimal("0.0")
        vk_preis:Decimal = to_decimal("0.0")
        h_rezlin1 = None
        hrecipe = None

        def generate_inner_output():
            return (cost)

        H_rezlin1 =  create_buffer("H_rezlin1",H_rezlin)
        Hrecipe =  create_buffer("Hrecipe",H_rezept)

        for h_rezlin1 in db_session.query(H_rezlin1).filter(
                 (H_rezlin1.artnrrezept == p_artnr)).order_by(H_rezlin1._recid).all():

            hrecipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin1.artnrrezept)]})

            if hrecipe.portion > 1:
                inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge) / to_decimal(hrecipe.portion)


            else:
                inh =  to_decimal(menge) * to_decimal(h_rezlin1.menge)

            if h_rezlin1.recipe_flag :
                cost = cal_cost(h_rezlin1.artnrlager, inh, cost)
            else:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin1.artnrlager)]})

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    vk_preis =  to_decimal(l_artikel.vk_preis)
                else:
                    vk_preis =  to_decimal(l_artikel.ek_aktuell)
                cost =  to_decimal(cost) + to_decimal(inh) / to_decimal(l_artikel.inhalt) * to_decimal(vk_preis) / to_decimal((1) - to_decimal(h_rezlin1.lostfact) / to_decimal(100))

        return generate_inner_output()


    if lostfact == None:
        lostfact =  to_decimal(0.00)
    else:
        lostfact =  to_decimal(lostfact)

    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artnr)]})

    if h_rezept:
        portion = h_rezept.portion
    create_amount()
    create_rezlin()

    return generate_output()