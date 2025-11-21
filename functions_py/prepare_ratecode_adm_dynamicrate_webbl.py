#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.load_ratecode1bl import load_ratecode1bl
from functions.ratecode_admin_fill_dynarate_counterbl import ratecode_admin_fill_dynarate_counterbl
from models import Ratecode

def prepare_ratecode_adm_dynamicrate_webbl(prcode1:string):
    dynarate_list_data = []
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    curr_counter:int = 0
    ratecode = None

    t_ratecode1 = dynarate_list = None

    t_ratecode1_data, T_ratecode1 = create_model_like(Ratecode, {"s_recid":int})
    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"s_recid":int, "counter":int, "w_day":int, "rmType":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rCode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dynarate_list_data, tokcounter, iftask, mestoken, mesvalue, curr_counter, ratecode
        nonlocal prcode1


        nonlocal t_ratecode1, dynarate_list
        nonlocal t_ratecode1_data, dynarate_list_data

        return {"dynaRate-list": dynarate_list_data}

    t_ratecode1_data = get_output(load_ratecode1bl(2, None, prcode1, None, None, None, None, None, None, None, None, None))

    for t_ratecode1 in query(t_ratecode1_data):
        dynarate_list = Dynarate_list()
        dynarate_list_data.append(dynarate_list)

        dynarate_list.s_recid = t_ratecode1.s_recid


        iftask = t_ratecode1.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

            if mestoken == "CN":
                dynarate_list.counter = to_int(mesvalue)
            elif mestoken == "RT":
                dynarate_list.rmType = mesvalue
            elif mestoken == "WD":
                dynarate_list.w_day = to_int(mesvalue)
            elif mestoken == "FR":
                dynarate_list.fr_room = to_int(mesvalue)
            elif mestoken == "TR":
                dynarate_list.to_room = to_int(mesvalue)
            elif mestoken == "D1":
                dynarate_list.days1 = to_int(mesvalue)
            elif mestoken == "D2":
                dynarate_list.days2 = to_int(mesvalue)
            elif mestoken == "RC":
                dynarate_list.rCode = mesvalue

        if dynarate_list.counter == 0:
            curr_counter = get_output(ratecode_admin_fill_dynarate_counterbl(t_ratecode1.code, dynarate_list.rmType, dynarate_list.rCode, dynarate_list.w_day))
            dynarate_list.counter = curr_counter

    return generate_output()