#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 30/7/2025
# gitlab: 986
# change query.
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, H_rezept, H_rezlin, L_artikel

def export_recipebl(pvilanguage:int, from_artnr:int, to_artnr:int, from_kateg:int, to_kateg:int, detail:bool):

    prepare_cache ([Htparam, H_rezept, H_rezlin, L_artikel])

    h_list_data = []
    price_type:int = 0
    p_artnr:int = 0
    menge:Decimal = 1
    curr_artnr:int = 0
    main_portion:int = 0
    v_total_cost:Decimal = 0
    v_total_portion:Decimal = 0
    v_max_cost:Decimal = 999999.99
    htparam = h_rezept = h_rezlin = l_artikel = None

    h_list = t_h_list = None

    h_list_data, H_list = create_model("H_list", {"cat_nr":int, "cat_name":string, "cat_bezeich":string, "rez_recipe_nr":int, "recipe_nr":int, "artnr":int, "bezeich":string, "portion":int, "qty":Decimal, "cost":Decimal, "loss":Decimal, "cost_port":Decimal, "r_flag":bool, "flag":string, "mass_unit":string})

    T_h_list = H_list
    t_h_list_data = h_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_list_data, price_type, p_artnr, menge, curr_artnr, main_portion, v_total_cost, v_total_portion, v_max_cost, htparam, h_rezept, h_rezlin, l_artikel
        nonlocal pvilanguage, from_artnr, to_artnr, from_kateg, to_kateg, detail
        nonlocal t_h_list


        nonlocal h_list, t_h_list
        nonlocal h_list_data

        return {"h-list": h_list_data}

    def create_list(p_artnr:int, menge:Decimal):

        nonlocal h_list_data, price_type, curr_artnr, main_portion, v_total_cost, v_total_portion, htparam, h_rezept, h_rezlin, l_artikel
        nonlocal pvilanguage, from_artnr, to_artnr, from_kateg, to_kateg, detail
        nonlocal t_h_list


        nonlocal h_list, t_h_list
        nonlocal h_list_data

        cost:Decimal = to_decimal("0.0")
        temp_cost:Decimal = to_decimal("0.0")
        temp_menge:Decimal = to_decimal("0.0")
        v_max_cost:Decimal = 999999.99
        h_recipe = None
        t_h_rezlin = None
        H_recipe =  create_buffer("H_recipe",H_rezept)
        T_h_rezlin =  create_buffer("T_h_rezlin",H_rezlin)

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():

            if detail :

                if h_rezlin.recipe_flag :

                    h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrlager)]})

                    if h_recipe:
                        curr_artnr = p_artnr
                        h_list = H_list()
                        h_list_data.append(h_list)

                        h_list.recipe_nr = p_artnr
                        h_list.rez_recipe_nr = h_recipe.artnrrezept
                        h_list.cat_nr = h_recipe.kategorie
                        h_list.cat_bezeich = substring(h_recipe.bezeich, 0, 24)
                        h_list.cat_name = substring(h_recipe.bezeich, 24, 24)
                        h_list.artnr = h_recipe.artnrrezept
                        h_list.bezeich = h_recipe.bezeich
                        h_list.qty =  to_decimal(h_rezlin.menge)
                        h_list.portion = main_portion
                        h_list.r_flag = True


                    create_list(h_rezlin.artnrlager, menge * h_rezlin.menge / h_recipe.portion)
                else:
                    h_list = H_list()
                    h_list_data.append(h_list)


                    h_recipe = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, h_rezlin.artnrlager)]})

                    t_h_rezlin = get_cache (H_rezlin, {"artnrrezept": [(eq, curr_artnr)],"artnrlager": [(eq, p_artnr)]})
                    temp_menge =  to_decimal(menge) * to_decimal(h_rezlin.menge)

                    if temp_menge > v_max_cost:
                        temp_menge =  to_decimal(v_max_cost)
                    temp_menge =  to_decimal(temp_menge) / to_decimal(l_artikel.inhalt)

                    if temp_menge > v_max_cost:
                        temp_menge =  to_decimal(v_max_cost)

                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                        temp_cost =  to_decimal(temp_menge) * to_decimal(l_artikel.vk_preis)
                    else:
                        temp_cost =  to_decimal(temp_menge) * to_decimal(l_artikel.ek_aktuell)

                    if temp_cost > v_max_cost:
                        temp_cost =  to_decimal(v_max_cost)

                    if h_rezlin.lostfact == 100:
                        cost =  to_decimal(temp_cost)
                    else:
                        cost =  to_decimal(temp_cost) / to_decimal((1) - to_decimal(h_rezlin.lostfact) / to_decimal(100))

                    if cost > v_max_cost:
                        cost =  to_decimal(v_max_cost)
                    h_list.cat_nr = h_recipe.kategorie
                    h_list.cat_bezeich = substring(h_recipe.bezeich, 0, 24)
                    h_list.cat_name = substring(h_recipe.bezeich, 24, 24)
                    h_list.recipe_nr = p_artnr
                    h_list.rez_recipe_nr = h_recipe.artnrrezept
                    h_list.artnr = l_artikel.artnr
                    h_list.bezeich = l_artikel.bezeich
                    h_list.loss =  to_decimal(h_rezlin.lostfact)
                    h_list.qty =  to_decimal(h_rezlin.menge) * to_decimal(menge)
                    h_list.cost =  to_decimal(cost)
                    h_list.mass_unit = l_artikel.masseinheit
                    h_list.portion = main_portion

                    if main_portion > 0:
                        h_list.cost_port =  to_decimal(cost) / to_decimal(main_portion)
                    else:
                        h_list.cost_port =  to_decimal("0")

                    if h_list.cost_port > v_max_cost:
                        h_list.cost_port =  to_decimal(v_max_cost)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger
    for p_artnr in range(from_artnr,to_artnr + 1) :

        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, p_artnr)]})

        if h_rezept:
            main_portion = h_rezept.portion
            h_list = H_list()
            h_list_data.append(h_list)

            h_list.recipe_nr = h_rezept.artnrrezept
            h_list.cat_nr = h_rezept.kategorie
            h_list.cat_bezeich = substring(h_rezept.bezeich, 0, 24)
            h_list.cat_name = substring(h_rezept.bezeich, 24, 24)
            h_list.flag = "**"


            create_list(p_artnr, menge)

        for h_list in query(h_list_data, filters=(lambda h_list: h_list.cost > 0 and h_list.flag == "")):

            if h_list.cost > v_max_cost:
                h_list.cost =  to_decimal(v_max_cost)
            v_total_cost =  to_decimal(v_total_cost) + to_decimal(h_list.cost)

            if v_total_cost > v_max_cost:
                v_total_cost =  to_decimal(v_max_cost)

            if h_list.portion > 0:
                v_total_portion =  to_decimal(h_list.portion)

        for h_list in query(h_list_data, filters=(lambda h_list: h_list.bezeich.lower()  == ("T O T A L").lower())):
            h_list_data.remove(h_list)


        h_list = H_list()
        h_list_data.append(h_list)

        h_list.bezeich = "T O T A L"
        h_list.portion = 0
        h_list.flag = ""
        h_list.cat_nr = 0
        h_list.cat_name = ""
        h_list.cat_bezeich = ""
        h_list.rez_recipe_nr = 0
        h_list.recipe_nr = 0
        h_list.artnr = 0
        h_list.qty =  to_decimal("0")
        h_list.cost =  to_decimal(v_total_cost)
        h_list.loss =  to_decimal("0")

        # Rd, 30/7/2025
        # h_list.cost_port = ( to_decimal(IF v_total_portion > 0 THEN)
        # v_total_cost / v_total_portion
        # ELSE
        # 0)
        # h_list.r_flag = True

        if v_total_portion > 0:
            h_list.cost_port = v_total_cost / v_total_portion
        else:
            h_list.cost_port = 0
        h_list.r_flag = False
        h_list.mass_unit = ""

    return generate_output()