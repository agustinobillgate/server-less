#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Parameters, L_artikel, Htparam, L_orderhdr
from sqlalchemy.orm import flag_modified

def prepare_pr_list_1bl():

    prepare_cache ([L_artikel, Htparam, L_orderhdr])

    billdate = None
    long_digit = False
    cost_list_data = []
    t_parameters_data = []
    t_l_artikel_data = []
    parameters = l_artikel = htparam = l_orderhdr = None

    t_parameters = cost_list = t_l_artikel = None

    t_parameters_data, T_parameters = create_model_like(Parameters)
    cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    t_l_artikel_data, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "traubensort":string, "lief_einheit":Decimal, "bezeich":string, "jahrgang":int, "ek_aktuell":Decimal, "min_bestand":Decimal, "anzverbrauch":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, long_digit, cost_list_data, t_parameters_data, t_l_artikel_data, parameters, l_artikel, htparam, l_orderhdr


        nonlocal t_parameters, cost_list, t_l_artikel
        nonlocal t_parameters_data, cost_list_data, t_l_artikel_data

        return {"billdate": billdate, "long_digit": long_digit, "cost-list": cost_list_data, "t-parameters": t_parameters_data, "t-l-artikel": t_l_artikel_data}

    def create_costlist():

        nonlocal billdate, long_digit, cost_list_data, t_parameters_data, t_l_artikel_data, parameters, l_artikel, htparam, l_orderhdr


        nonlocal t_parameters, cost_list, t_l_artikel
        nonlocal t_parameters_data, cost_list_data, t_l_artikel_data

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_data.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    def check_appr():

        nonlocal billdate, long_digit, cost_list_data, t_parameters_data, t_l_artikel_data, parameters, l_artikel, htparam, l_orderhdr


        nonlocal t_parameters, cost_list, t_l_artikel
        nonlocal t_parameters_data, cost_list_data, t_l_artikel_data

        approve_str:string = ""
        lbuff = None
        Lbuff =  create_buffer("Lbuff",L_orderhdr)

        for l_orderhdr in db_session.query(L_orderhdr).order_by(L_orderhdr._recid).all():

            if matches(l_orderhdr.lief_fax[1],r"*;*"):
                pass
            else:

                # lbuff = get_cache (L_orderhdr, {"_recid": [(eq, l_orderhdr._recid)]})
                lbuff = db_session.query(L_orderhdr).filter(
                          (L_orderhdr._recid == l_orderhdr._recid)).with_for_update

                if lbuff:
                    approve_str = lbuff.lief_fax[1]

                    if lbuff.lief_fax[1] == "":
                        lbuff.lief_fax[1] = " ; ; ; "


                    else:
                        lbuff.lief_fax[1] = approve_str + ";" +\
                            approve_str + ";" + approve_str + ";" + approve_str


                    pass
        flag_modified(lbuff, "lief_fax")

    create_costlist()
    check_appr()

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).with_for_update().all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.traubensort = l_artikel.traubensorte
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.jahrgang = l_artikel.jahrgang
        t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        t_l_artikel.min_bestand =  to_decimal(l_artikel.min_bestand)
        t_l_artikel.anzverbrauch =  to_decimal(l_artikel.anzverbrauch)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    return generate_output()