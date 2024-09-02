from functions.additional_functions import *
import decimal
from functions.load_ratecode1bl import load_ratecode1bl
from functions.ratecode_admin_fill_dynarate_counterbl import ratecode_admin_fill_dynarate_counterbl
from models import Ratecode

def prepare_ratecode_adm_dynamicrate_webbl(prcode1:str):
    dynarate_list_list = []
    tokcounter:int = 0
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    curr_counter:int = 0
    ratecode = None

    t_ratecode1 = dynarate_list = None

    t_ratecode1_list, T_ratecode1 = create_model_like(Ratecode, {"s_recid":int})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"s_recid":int, "counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dynarate_list_list, tokcounter, iftask, mestoken, mesvalue, curr_counter, ratecode


        nonlocal t_ratecode1, dynarate_list
        nonlocal t_ratecode1_list, dynarate_list_list
        return {"dynaRate-list": dynarate_list_list}

    t_ratecode1_list = get_output(load_ratecode1bl(2, None, prcode1, None, None, None, None, None, None, None, None, None))

    for t_ratecode1 in query(t_ratecode1_list):
        dynarate_list = Dynarate_list()
        dynarate_list_list.append(dynarate_list)

        dynaRate_list.s_recid = t_ratecode1.s_recid


        iftask = t_ratecode1.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

            if mestoken == "CN":
                dynaRate_list.counter = to_int(mesvalue)
            elif mestoken == "RT":
                dynaRate_list.rmType = mesvalue
            elif mestoken == "WD":
                dynaRate_list.w_day = to_int(mesvalue)
            elif mestoken == "FR":
                dynaRate_list.fr_room = to_int(mesvalue)
            elif mestoken == "TR":
                dynaRate_list.to_room = to_int(mesvalue)
            elif mestoken == "D1":
                dynaRate_list.days1 = to_int(mesvalue)
            elif mestoken == "D2":
                dynaRate_list.days2 = to_int(mesvalue)
            elif mestoken == "RC":
                dynaRate_list.rCode = mesvalue

    if dynaRate_list.counter == 0:
        curr_counter = get_output(ratecode_admin_fill_dynarate_counterbl(t_ratecode1.code, dynaRate_list.rmType, dynaRate_list.rCode, dynarate_list.w_day))
        dynaRate_list.counter = curr_counter

    return generate_output()