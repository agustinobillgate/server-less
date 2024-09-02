from functions.additional_functions import *
import decimal
from models import H_rezept, Htparam, H_rezlin, L_artikel

def prepare_recipe_listbl():
    cost_list_list = []
    t_h_rezept_list = []
    price_type:int = 0
    curr_i:int = 0
    h_rezept = htparam = h_rezlin = l_artikel = None

    cost_list = t_h_rezept = r_list = r1_list = h_recipe = hrecipe = None

    cost_list_list, Cost_list = create_model("Cost_list", {"artnrrezept":int, "cost":decimal})
    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept)
    r_list_list, R_list = create_model("R_list", {"max_n":int, "recipe_nr":[int, 99]})

    R1_list = R_list
    r1_list_list = r_list_list

    H_recipe = H_rezept
    Hrecipe = H_rezept

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, t_h_rezept_list, price_type, curr_i, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal r1_list, h_recipe, hrecipe


        nonlocal cost_list, t_h_rezept, r_list, r1_list, h_recipe, hrecipe
        nonlocal cost_list_list, t_h_rezept_list, r_list_list
        return {"cost-list": cost_list_list, "t-h-rezept": t_h_rezept_list}

    def calculate_cost():

        nonlocal cost_list_list, t_h_rezept_list, price_type, curr_i, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal r1_list, h_recipe, hrecipe


        nonlocal cost_list, t_h_rezept, r_list, r1_list, h_recipe, hrecipe
        nonlocal cost_list_list, t_h_rezept_list, r_list_list

        amount:decimal = 0

        for h_rezept in db_session.query(H_rezept).all():
            buffer_copy(r1_list, r_list)
            curr_i = 0

            cost_list = query(cost_list_list, filters=(lambda cost_list :cost_list.artnrrezept == h_rezept.artnrrezept), first=True)

            if not cost_list:
                cost_list = Cost_list()
                cost_list_list.append(cost_list)

                cost_list.artnrrezept = h_rezept.artnrrezept
                amount = 0
                amount = cal_cost(h_rezept.artnrrezept, 1, amount)
                cost_list.cost = amount

    def cal_cost(p_artnr:int, menge:decimal, cost:decimal):

        nonlocal cost_list_list, t_h_rezept_list, price_type, curr_i, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal r1_list, h_recipe, hrecipe


        nonlocal cost_list, t_h_rezept, r_list, r1_list, h_recipe, hrecipe
        nonlocal cost_list_list, t_h_rezept_list, r_list_list

        inh:decimal = 0
        i:int = 0
        H_recipe = H_rezept
        Hrecipe = H_rezept

        h_recipe = db_session.query(H_recipe).filter(
                (H_recipe.artnrrezept == p_artnr)).first()

        if h_recipe:

            for h_rezlin in db_session.query(H_rezlin).filter(
                    (H_rezlin.artnrrezept == p_artnr)).all():

                if h_rezlin.recipe_flag :

                    hrecipe = db_session.query(Hrecipe).filter(
                            (Hrecipe.artnrrezept == h_rezlin.artnrlager)).first()

                    if hrecipe:

                        if hrecipe.portion > 1:
                            inh = menge * h_rezlin.menge / hrecipe.portion


                        else:
                            inh = menge * h_rezlin.menge
                        cost = cal_cost(h_rezlin.artnrlager, inh, cost)
                else:
                    inh = menge * h_rezlin.menge

                    l_artikel = db_session.query(L_artikel).filter(
                            (L_artikel.artnr == h_rezlin.artnrlager)).first()

                    if price_type == 0 or l_artikel.ek_aktuell == 0:
                        cost = cost + inh / l_artikel.inhalt * l_artikel.vk_preis / (1 - h_rezlin.lostfact / 100)
                    else:
                        cost = cost + inh / l_artikel.inhalt * l_artikel.ek_aktuell / (1 - h_rezlin.lostfact / 100)


    r1_list = R1_list()
    r1_list_list.append(r1_list)

    r_list = R_list()
    r_list_list.append(r_list)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1024)).first()
    price_type = htparam.finteger
    calculate_cost()

    for h_rezept in db_session.query(H_rezept).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_list.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    return generate_output()