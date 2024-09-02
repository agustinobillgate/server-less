from functions.additional_functions import *
import decimal
from models import H_rezept, Htparam, H_rezlin, L_artikel

def prepare_view_recitembl(artnr:int, curr_i:int):
    t_str = ""
    o_portion = 0
    price_type = 0
    amount = 0
    amount1 = 0
    h_list_list = []
    curr_artnr:int = 0
    h_rezept = htparam = h_rezlin = l_artikel = None

    h_list = h_recipe = hrecipe = t_h_rezlin = None

    h_list_list, H_list = create_model("H_list", {"str":str, "portion":int, "artnr":int, "bezeich":str, "lostfact":decimal, "menge":decimal, "cost":decimal, "r_artnr":int, "r_flag":bool, "costportion":decimal})

    H_recipe = H_rezept
    Hrecipe = H_rezept
    T_h_rezlin = H_rezlin

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_str, o_portion, price_type, amount, amount1, h_list_list, curr_artnr, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal h_recipe, hrecipe, t_h_rezlin


        nonlocal h_list, h_recipe, hrecipe, t_h_rezlin
        nonlocal h_list_list
        return {"t_str": t_str, "o_portion": o_portion, "price_type": price_type, "amount": amount, "amount1": amount1, "h-list": h_list_list}

    def create_list(p_artnr:int, menge:decimal):

        nonlocal t_str, o_portion, price_type, amount, amount1, h_list_list, curr_artnr, h_rezept, htparam, h_rezlin, l_artikel
        nonlocal h_recipe, hrecipe, t_h_rezlin


        nonlocal h_list, h_recipe, hrecipe, t_h_rezlin
        nonlocal h_list_list

        c_artnr:int = 0
        cost:decimal = 0
        i:int = 0
        H_recipe = H_rezept
        Hrecipe = H_rezept
        T_h_rezlin = H_rezlin

        for h_rezlin in db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == p_artnr)).all():

            if h_rezlin.recipe_flag :
                curr_artnr = p_artnr
                h_list = H_list()
                h_list_list.append(h_list)

                h_list.r_artnr = p_artnr

                h_recipe = db_session.query(H_recipe).filter(
                        (H_recipe.artnrrezept == h_rezlin.artnrlager)).first()
                h_list.artnr = h_recipe.artnrrezept
                h_list.bezeich = h_recipe.bezeich
                h_list.menge = h_rezlin.menge
                h_list.portion = h_recipe.portion
                h_list.r_flag = True
                h_list.str = to_string(h_list.artnr, ">>>>>>9") + to_string(h_list.bezeich, "x(24)") + to_string(" ", "x(12)") + to_string(h_list.menge, ">>>,>>9.999")
                create_list(h_rezlin.artnrlager, menge * h_rezlin.menge / h_recipe.portion)
            else:
                h_list = H_list()
                h_list_list.append(h_list)


                h_recipe = db_session.query(H_recipe).filter(
                        (H_recipe.artnrrezept == p_artnr)).first()

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == h_rezlin.artnrlager)).first()

                t_h_rezlin = db_session.query(T_h_rezlin).filter(
                        (T_h_rezlin.artnrrezept == curr_artnr) &  (T_h_rezlin.artnrlager == p_artnr)).first()

                if price_type == 0 or l_artikel.ek_aktuell == 0:
                    cost = (menge * h_rezlin.menge / l_artikel.inhalt * l_artikel.vk_preis) / (1 - h_rezlin.lostfact / 100)
                else:
                    cost = (menge * h_rezlin.menge / l_artikel.inhalt * l_artikel.ek_aktuell) / (1 - h_rezlin.lostfact / 100)
                amount = amount + cost
                h_list.r_artnr = p_artnr
                h_list.artnr = l_artikel.artnr
                h_list.bezeich = l_artikel.bezeich
                h_list.lostfact = h_rezlin.lostfact
                h_list.menge = h_rezlin.menge * menge
                h_list.cost = cost

                if t_h_rezlin and t_h_rezlin.recipe_flag :
                    h_list.costportion = cost / o_portion
                else:
                    h_list.costportion = cost / o_portion
                h_list.str = to_string(h_list.artnr, "9999999") + to_string(h_list.bezeich, "x(31)") + to_string(h_list.lostfact, "99.99") + to_string(h_list.menge, ">>>,>>9.999") + to_string(h_list.cost, ">,>>>,>>>,>>9.99") + to_string(h_list.costportion, ">,>>>,>>>,>>9.99")

    h_rezept = db_session.query(H_rezept).filter(
            (H_rezept.artnrrezept == artnr)).first()
    t_str = "Recipe Items - " + to_string(artnr) + " " + trim(substring(h_rezept.bezeich, 0, 24)) + " (Portion " + to_string(h_rezept.portion) + ")"
    o_portion = h_rezept.portion

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1024)).first()
    price_type = htparam.finteger
    amount = 0
    create_list(artnr, curr_i)
    amount1 = amount / o_portion

    return generate_output()