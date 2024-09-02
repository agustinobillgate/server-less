from functions.additional_functions import *
import decimal
from datetime import date
from functions.rm_productrate_create_umsatz1bl import rm_productrate_create_umsatz1bl

def rm_productrate_create_umsatz1_listbl(disptype:int, mi_ftd:bool, f_date:date, t_date:date, to_date:date, cardtype:int, incl_comp:bool, sales_id:str):
    out_list_list = []

    to_list = output_list2 = out_list = None

    to_list_list, To_list = create_model("To_list", {"gastnr":int, "name":str, "room":int, "c_room":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "ratecode":str, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal})
    output_list2_list, Output_list2 = create_model("Output_list2", {"flag":int, "name":str, "rmnite1":int, "rmrev1":decimal, "rmnite":int, "rmrev":decimal, "str2":str, "rate":str})
    out_list_list, Out_list = create_model("Out_list", {"name":str, "rate":str, "room":str, "pax":str, "logis":str, "proz":str, "avrgrate":str, "m_room":str, "m_pax":str, "m_logis":str, "m_proz":str, "m_avrgrate":str, "y_room":str, "y_pax":str, "y_logis":str, "y_proz":str, "y_avrgrate":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_list


        nonlocal to_list, output_list2, out_list
        nonlocal to_list_list, output_list2_list, out_list_list
        return {"out-list": out_list_list}


    output_list2_list, to_list_list = get_output(rm_productrate_create_umsatz1bl(disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id))

    for out_list in query(out_list_list):
        out_list_list.remove(out_list)

    for output_list2 in query(output_list2_list):
        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.rate = substring(output_list2.str2, 179, 15)
        out_list.name = substring(output_list2.str2, 0, 24)
        out_list.room = substring(output_list2.str2, 24, 7)
        out_list.pax = substring(output_list2.str2, 31, 7)
        out_list.logis = substring(output_list2.str2, 38, 15)
        out_list.proz = substring(output_list2.str2, 53, 7)
        out_list.avrgrate = substring(output_list2.str2, 60, 14)
        out_list.m_room = substring(output_list2.str2, 74, 7)
        out_list.m_pax = substring(output_list2.str2, 81, 7)
        out_list.m_logis = substring(output_list2.str2, 88, 15)
        out_list.m_proz = substring(output_list2.str2, 103, 7)
        out_list.m_avrgrate = substring(output_list2.str2, 110, 14)
        out_list.y_room = substring(output_list2.str2, 124, 8)
        out_list.y_pax = substring(output_list2.str2, 132, 8)
        out_list.y_logis = substring(output_list2.str2, 140, 18)
        out_list.y_proz = substring(output_list2.str2, 158, 7)
        out_list.y_avrgrate = substring(output_list2.str2, 165, 14)

    return generate_output()