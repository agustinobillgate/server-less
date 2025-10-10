#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Wgrpdep

input_list_data, Input_list = create_model("Input_list", {"dept_num":int, "subgrp_name":string})

def prepare_outlet_subgrp_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Hoteldpt, Wgrpdep])

    output_list_data = []
    wgrpdep_list_data = []
    dept:int = 0
    subgrp_name:string = ""
    dpttype:int = 0
    hoteldpt = wgrpdep = None

    input_list = output_list = wgrpdep_list = None

    output_list_data, Output_list = create_model("Output_list", {"depart":string, "num":int, "dpttype":string, "msg_str":string, "success_flag":bool})
    wgrpdep_list_data, Wgrpdep_list = create_model("Wgrpdep_list", {"departement":int, "zknr":int, "bezeich":string, "isselected":bool, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, wgrpdep_list_data, dept, subgrp_name, dpttype, hoteldpt, wgrpdep


        nonlocal input_list, output_list, wgrpdep_list
        nonlocal output_list_data, wgrpdep_list_data

        return {"output-list": output_list_data, "wgrpdep-list": wgrpdep_list_data}


    output_list = Output_list()
    output_list_data.append(output_list)


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        dept = input_list.dept_num
        subgrp_name = trim(input_list.subgrp_name)

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    if hoteldpt:
        output_list.num = hoteldpt.num
        output_list.depart = hoteldpt.depart
        dpttype = hoteldpt.departtyp

    if subgrp_name == "" or subgrp_name == None:

        for wgrpdep in db_session.query(Wgrpdep).filter(
                 (Wgrpdep.departement == dept)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr).all():
            wgrpdep_list = Wgrpdep_list()
            wgrpdep_list_data.append(wgrpdep_list)

            wgrpdep_list.departement = wgrpdep.departement
            wgrpdep_list.zknr = wgrpdep.zknr
            wgrpdep_list.bezeich = wgrpdep.bezeich
            wgrpdep_list.isselected = False
            wgrpdep_list.rec_id = wgrpdep._recid


    else:

        for wgrpdep in db_session.query(Wgrpdep).filter(
                 (Wgrpdep.departement == dept) & (get_index(Wgrpdep.bezeich, subgrp_name) > 0)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr).all():
            wgrpdep_list = Wgrpdep_list()
            wgrpdep_list_data.append(wgrpdep_list)

            wgrpdep_list.departement = wgrpdep.departement
            wgrpdep_list.zknr = wgrpdep.zknr
            wgrpdep_list.bezeich = wgrpdep.bezeich
            wgrpdep_list.isselected = False
            wgrpdep_list.rec_id = wgrpdep._recid

    if dpttype == 1:
        output_list.dpttype = "Food & Beverage"
    elif dpttype == 2:
        output_list.dpttype = "Minibar"
    elif dpttype == 3:
        output_list.dpttype = "Laundry"
    elif dpttype == 4:
        output_list.dpttype = "Banquet"
    elif dpttype == 5:
        output_list.dpttype = "Drug Store"
    elif dpttype == 6:
        output_list.dpttype = "Others"
    elif dpttype == 7:
        output_list.dpttype = "Spa"
    elif dpttype == 8:
        output_list.dpttype = "Boutique"
    else:
        ""

    return generate_output()