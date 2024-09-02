from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Hoteldpt, L_bestand, Htparam, Parameters

def prepare_dml_list_1bl():
    billdate = None
    nextdate = None
    selected_date = None
    fl_eknr = 0
    bl_eknr = 0
    auto_approve = False
    t_hoteldpt_list = []
    t_parameters_list = []
    t_l_bestand_list = []
    hoteldpt = l_bestand = htparam = parameters = None

    t_hoteldpt = t_parameters = t_l_bestand = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})
    t_l_bestand_list, T_l_bestand = create_model_like(L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, nextdate, selected_date, fl_eknr, bl_eknr, auto_approve, t_hoteldpt_list, t_parameters_list, t_l_bestand_list, hoteldpt, l_bestand, htparam, parameters


        nonlocal t_hoteldpt, t_parameters, t_l_bestand
        nonlocal t_hoteldpt_list, t_parameters_list, t_l_bestand_list
        return {"billdate": billdate, "nextdate": nextdate, "selected_date": selected_date, "fl_eknr": fl_eknr, "bl_eknr": bl_eknr, "auto_approve": auto_approve, "t-hoteldpt": t_hoteldpt_list, "t-parameters": t_parameters_list, "t-l-bestand": t_l_bestand_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    nextdate = billdate + 1
    selected_date = nextdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    fl_eknr = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    bl_eknr = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 390)).first()
    auto_approve = htparam.flogical

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    for l_bestand in db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == 0)).all():
        t_l_bestand = T_l_bestand()
        t_l_bestand_list.append(t_l_bestand)

        buffer_copy(l_bestand, t_l_bestand)

    return generate_output()