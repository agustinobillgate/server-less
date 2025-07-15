#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, L_bestand, Htparam, Parameters

def prepare_dml_list_1bl():

    prepare_cache ([Htparam])

    billdate = None
    nextdate = None
    selected_date = None
    fl_eknr = 0
    bl_eknr = 0
    auto_approve = False
    t_hoteldpt_data = []
    t_parameters_data = []
    t_l_bestand_data = []
    hoteldpt = l_bestand = htparam = parameters = None

    t_hoteldpt = t_parameters = t_l_bestand = None

    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)
    t_parameters_data, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})
    t_l_bestand_data, T_l_bestand = create_model_like(L_bestand)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, nextdate, selected_date, fl_eknr, bl_eknr, auto_approve, t_hoteldpt_data, t_parameters_data, t_l_bestand_data, hoteldpt, l_bestand, htparam, parameters


        nonlocal t_hoteldpt, t_parameters, t_l_bestand
        nonlocal t_hoteldpt_data, t_parameters_data, t_l_bestand_data

        return {"billdate": billdate, "nextdate": nextdate, "selected_date": selected_date, "fl_eknr": fl_eknr, "bl_eknr": bl_eknr, "auto_approve": auto_approve, "t-hoteldpt": t_hoteldpt_data, "t-parameters": t_parameters_data, "t-l-bestand": t_l_bestand_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    nextdate = billdate + timedelta(days=1)
    selected_date = nextdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    fl_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    bl_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 390)]})
    auto_approve = htparam.flogical

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    for l_bestand in db_session.query(L_bestand).filter(
             (L_bestand.lager_nr == 0)).order_by(L_bestand._recid).all():
        t_l_bestand = T_l_bestand()
        t_l_bestand_data.append(t_l_bestand)

        buffer_copy(l_bestand, t_l_bestand)

    return generate_output()