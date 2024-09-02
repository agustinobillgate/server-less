from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Parameters, L_artikel, Htparam, L_orderhdr

def prepare_pr_list_1bl():
    billdate = None
    long_digit = False
    cost_list_list = []
    t_parameters_list = []
    t_l_artikel_list = []
    parameters = l_artikel = htparam = l_orderhdr = None

    t_parameters = cost_list = t_l_artikel = lbuff = None

    t_parameters_list, T_parameters = create_model_like(Parameters)
    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":str})
    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "traubensort":str, "lief_einheit":decimal, "bezeich":str, "jahrgang":int, "ek_aktuell":decimal, "min_bestand":decimal, "anzverbrauch":decimal})

    Lbuff = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, long_digit, cost_list_list, t_parameters_list, t_l_artikel_list, parameters, l_artikel, htparam, l_orderhdr
        nonlocal lbuff


        nonlocal t_parameters, cost_list, t_l_artikel, lbuff
        nonlocal t_parameters_list, cost_list_list, t_l_artikel_list
        return {"billdate": billdate, "long_digit": long_digit, "cost-list": cost_list_list, "t-parameters": t_parameters_list, "t-l-artikel": t_l_artikel_list}

    def create_costlist():

        nonlocal billdate, long_digit, cost_list_list, t_parameters_list, t_l_artikel_list, parameters, l_artikel, htparam, l_orderhdr
        nonlocal lbuff


        nonlocal t_parameters, cost_list, t_l_artikel, lbuff
        nonlocal t_parameters_list, cost_list_list, t_l_artikel_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname > "")).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring

    def check_appr():

        nonlocal billdate, long_digit, cost_list_list, t_parameters_list, t_l_artikel_list, parameters, l_artikel, htparam, l_orderhdr
        nonlocal lbuff


        nonlocal t_parameters, cost_list, t_l_artikel, lbuff
        nonlocal t_parameters_list, cost_list_list, t_l_artikel_list

        approve_str:str = ""
        Lbuff = L_orderhdr

        for l_orderhdr in db_session.query(L_orderhdr).all():

            if re.match(".*;.*",lief_fax[1]):
                1
            else:

                lbuff = db_session.query(Lbuff).filter(
                        (Lbuff._recid == l_orderhdr._recid)).first()

                if lbuff:
                    approve_str = lbuff.lief_fax[1]

                    if lbuff.lief_fax[1] == "":
                        lbuff.lief_fax[1] = " ; ; ; "


                    else:
                        lbuff.lief_fax[1] = approve_str + ";" +\
                            approve_str + ";" + approve_str + ";" + approve_str

                    lbuff = db_session.query(Lbuff).first()


    create_costlist()
    check_appr()

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    for l_artikel in db_session.query(L_artikel).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.traubensort = l_artikel.traubensort
        t_l_artikel.lief_einheit = l_artikel.lief_einheit
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.jahrgang = l_artikel.jahrgang
        t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
        t_l_artikel.min_bestand = l_artikel.min_bestand
        t_l_artikel.anzverbrauch = l_artikel.anzverbrauch

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    return generate_output()