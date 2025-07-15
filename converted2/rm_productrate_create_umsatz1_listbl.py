#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rm_productrate_create_umsatz1bl import rm_productrate_create_umsatz1bl

def rm_productrate_create_umsatz1_listbl(disptype:int, mi_ftd:bool, f_date:date, t_date:date, to_date:date, cardtype:int, incl_comp:bool, sales_id:string):
    out_list_data = []

    to_list = output_list2 = out_list = None

    to_list_data, To_list = create_model("To_list", {"gastnr":int, "name":string, "room":int, "c_room":int, "pax":int, "logis":Decimal, "proz":Decimal, "avrgrate":Decimal, "ratecode":string, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":Decimal, "m_proz":Decimal, "m_avrgrate":Decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":Decimal, "y_proz":Decimal, "y_avrgrate":Decimal})
    output_list2_data, Output_list2 = create_model("Output_list2", {"flag":int, "name":string, "rmnite1":int, "rmrev1":Decimal, "rmnite":int, "rmrev":Decimal, "str2":string, "rate":string})
    out_list_data, Out_list = create_model("Out_list", {"name":string, "rate":string, "room":string, "pax":string, "logis":string, "proz":string, "avrgrate":string, "m_room":string, "m_pax":string, "m_logis":string, "m_proz":string, "m_avrgrate":string, "y_room":string, "y_pax":string, "y_logis":string, "y_proz":string, "y_avrgrate":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_data
        nonlocal disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id


        nonlocal to_list, output_list2, out_list
        nonlocal to_list_data, output_list2_data, out_list_data

        return {"out-list": out_list_data}


    output_list2_data, to_list_data = get_output(rm_productrate_create_umsatz1bl(disptype, mi_ftd, f_date, t_date, to_date, cardtype, incl_comp, sales_id))

    for out_list in query(out_list_data):
        out_list_data.remove(out_list)

    for output_list2 in query(output_list2_data):
        out_list = Out_list()
        out_list_data.append(out_list)

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