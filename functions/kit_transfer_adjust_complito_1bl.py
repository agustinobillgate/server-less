#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Exrate, Artikel, H_artikel, Gl_acct, H_cost, H_rezept, H_compli, H_rezlin, L_artikel

c_list_data, C_list = create_model("C_list", {"artnr":int, "departement":int, "anzahl":int, "bezeich":string, "epreis":Decimal, "fremdwbetrag":Decimal, "betrag":Decimal, "waehrungsnr":int, "bill_datum":date, "zeit":int})

def kit_transfer_adjust_complito_1bl(c_list_data:[C_list], new_dept:int, transdate:date, double_currency:bool, foreign_nr:int, curr_dept:int, exchg_rate:Decimal):

    prepare_cache ([Htparam, Exrate, Artikel, H_artikel, H_cost, H_rezept, H_compli, H_rezlin, L_artikel])

    msg_str = ""
    htparam = exrate = artikel = h_artikel = gl_acct = h_cost = h_rezept = h_compli = h_rezlin = l_artikel = None

    c_list = c1_list = c2_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, htparam, exrate, artikel, h_artikel, gl_acct, h_cost, h_rezept, h_compli, h_rezlin, l_artikel
        nonlocal new_dept, transdate, double_currency, foreign_nr, curr_dept, exchg_rate


        nonlocal c_list, c1_list, c2_list

        return {"msg_str": msg_str}

    def adjust_complito():

        nonlocal msg_str, htparam, exrate, artikel, h_artikel, gl_acct, h_cost, h_rezept, h_compli, h_rezlin, l_artikel
        nonlocal new_dept, transdate, double_currency, foreign_nr, curr_dept, exchg_rate


        nonlocal c_list, c1_list, c2_list

        f_acct:int = 0
        b_acct:int = 0
        o_acct:int = 0
        f_cost:Decimal = to_decimal("0.0")
        b_cost:Decimal = to_decimal("0.0")
        bill_date:date = None
        curr_date:date = None
        rate:Decimal = 1
        cost:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        C1_list = C_list
        c1_list_data = c_list_data
        C2_list = C_list
        c2_list_data = c_list_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate
        curr_date = htparam.fdate

        if transdate != None:
            bill_date = transdate

        if double_currency:

            if foreign_nr != 0:

                exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, bill_date)]})
            else:

                exrate = get_cache (Exrate, {"datum": [(eq, bill_date)]})

            if exrate:
                rate =  to_decimal(exrate.betrag)
            else:
                rate =  to_decimal(exchg_rate)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})

        artikel = get_cache (Artikel, {"artart": [(eq, 0)],"endkum": [(eq, htparam.finteger)],"bezeich1": [(ne, "")],"departement": [(eq, new_dept)]})

        if not artikel:
            msg_str = "cost Account for food cost not available. Transfer not possible"

            return
        f_acct = artikel.artnr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})

        artikel = get_cache (Artikel, {"artart": [(eq, 0)],"endkum": [(eq, htparam.finteger)],"bezeich1": [(ne, "")],"departement": [(eq, new_dept)]})

        if not artikel:
            msg_str = "cost Account for beverage cost not available. Transfer not possible"

            return
        b_acct = artikel.artnr

        for c1_list in query(c1_list_data):

            if curr_artnr == 0:
                curr_artnr = c1_list.artnr

                c2_list = query(c2_list_data, filters=(lambda c2_list: c2_list.recid (c2_list) == recid (c1_list)), first=True)
            else:

                if c1_list.artnr == curr_artnr:
                    c2_list.anzahl = c2_list.anzahl + c1_list.anzahl
                    c1_list_data.remove(c1_list)
                else:
                    curr_artnr = c1_list.artnr

                    c2_list = query(c2_list_data, filters=(lambda c2_list: c2_list.recid (c2_list) == recid (c1_list)), first=True)

        for c1_list in query(c1_list_data, filters=(lambda c1_list: c1_list.anzahl == 0)):

            for c2_list in query(c2_list_data, filters=(lambda c2_list: c2_list.artnr == c1_list.artnr)):
                c2_list_data.remove(c2_list)

        for c1_list in query(c1_list_data):

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, c1_list.artnr)],"departement": [(eq, c1_list.departement)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, artikel.bezeich1)]})

            if not gl_acct:
                msg_str = "cost Account not defined:" + to_string(artikel.artnr) + " - " + artikel.bezeich + ". Transfer not possible."

                return
            cost =  to_decimal("0")

            if bill_date < curr_date:

                h_cost = get_cache (H_cost, {"artnr": [(eq, c1_list.artnr)],"departement": [(eq, c1_list.departement)],"datum": [(eq, bill_date)],"flag": [(eq, 1)]})

                if h_cost and h_cost.betrag != 0:
                    cost =  to_decimal(h_cost.anzahl) * to_decimal(h_cost.betrag)
                else:

                    if h_artikel.artnrrezept != 0:

                        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                        if h_rezept:
                            cal_cost(h_rezept.artnrrezept, 1, input_output cost)
                    else:
                        cost =  to_decimal(c1_list.anzahl) * to_decimal(c1_list.epreis) * to_decimal(h_artikel.prozent) * to_decimal(rate) / to_decimal("100")
            else:

                if h_artikel.artnrrezept != 0:

                    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_artikel.artnrrezept)]})

                    if h_rezept:
                        cal_cost(h_rezept.artnrrezept, 1, input_output cost)
                    else:
                        cost =  to_decimal(c1_list.anzahl) * to_decimal(c1_list.epreis) * to_decimal(h_artikel.prozent) * to_decimal(rate) / to_decimal("100")
                else:
                    cost =  to_decimal(c1_list.anzahl) * to_decimal(c1_list.epreis) * to_decimal(h_artikel.prozent) * to_decimal(rate) / to_decimal("100")
            f_cost =  to_decimal("0")
            b_cost =  to_decimal("0")

            if artikel.umsatzart == 6:
                b_cost =  to_decimal(cost)
            else:
                f_cost =  to_decimal(cost)

            if f_cost != 0:
                h_compli = H_compli()
                db_session.add(h_compli)

                h_compli.datum = bill_date
                h_compli.departement = curr_dept
                h_compli.artnr = c1_list.artnr
                h_compli.anzahl = c1_list.anzahl
                h_compli.epreis =  to_decimal(f_cost)
                h_compli.p_artnr = 1
                h_compli.betriebsnr = new_dept
                pass

            if b_cost != 0:
                h_compli = H_compli()
                db_session.add(h_compli)

                h_compli.datum = bill_date
                h_compli.departement = curr_dept
                h_compli.artnr = c1_list.artnr
                h_compli.anzahl = c1_list.anzahl
                h_compli.epreis =  to_decimal(b_cost)
                h_compli.p_artnr = 2
                h_compli.betriebsnr = new_dept
                pass


    def cal_cost(p_artnr:int, menge:Decimal, cost:Decimal):

        nonlocal msg_str, htparam, exrate, artikel, h_artikel, gl_acct, h_cost, h_rezept, h_compli, h_rezlin, l_artikel
        nonlocal new_dept, transdate, double_currency, foreign_nr, curr_dept, exchg_rate


        nonlocal c_list, c1_list, c2_list

        inh:Decimal = to_decimal("0.0")
        h_recipe = None
        price_type:int = 0

        def generate_inner_output():
            return (cost)

        H_recipe =  create_buffer("H_recipe",H_rezept)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
        price_type = htparam.finteger

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

    adjust_complito()

    return generate_output()