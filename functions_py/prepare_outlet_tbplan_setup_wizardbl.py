#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Tisch, Queasy

input_list_data, Input_list = create_model("Input_list", {"dept_num":int, "case_type":int})

def prepare_outlet_tbplan_setup_wizardbl(input_list_data:[Input_list]):

    prepare_cache ([Hoteldpt, Tisch, Queasy])

    t_list_data = []
    output_list_data = []
    dept_num:int = 0
    case_type:int = 0
    total_tisch:int = 0
    dpttype:int = 0
    hoteldpt = tisch = queasy = None

    input_list = t_list = output_list = None

    t_list_data, T_list = create_model("T_list", {"departement":int, "tischnr":int, "tisch_recid":int, "isselected":bool, "x_coordinate":Decimal, "y_coordinate":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"depart":string, "num":int, "dpttype":string, "total_tisch":int, "msg_str":string, "success_flag":bool}, {"success_flag": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_data, output_list_data, dept_num, case_type, total_tisch, dpttype, hoteldpt, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal t_list_data, output_list_data

        return {"t-list": t_list_data, "output-list": output_list_data}


    output_list = Output_list()
    output_list_data.append(output_list)


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        dept_num = input_list.dept_num
        case_type = input_list.case_type

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept_num)]})

    if hoteldpt:
        output_list.num = hoteldpt.num
        output_list.depart = hoteldpt.depart
        dpttype = hoteldpt.departtyp

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
    total_tisch = 0

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == dept_num)).order_by(Tisch.tischnr).all():
        total_tisch = total_tisch + 1

        if case_type != 2:

            queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

            if queasy:
                t_list = T_list()
                t_list_data.append(t_list)

                t_list.departement = queasy.number1
                t_list.tischnr = queasy.number2
                t_list.tisch_recid = tisch._recid
                t_list.isselected = False

                if case_type == 1:
                    t_list.x_coordinate =  to_decimal(queasy.deci1)
                    t_list.y_coordinate =  to_decimal(queasy.deci2)


                else:
                    t_list.x_coordinate =  to_decimal("0")
                    t_list.y_coordinate =  to_decimal("0")


            else:

                if output_list.msg_str == "":
                    output_list.msg_str = "The following table plan were not set up properly: " +\
                            chr_unicode(10) +\
                            "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                    output_list.success_flag = False


                else:
                    output_list.msg_str = output_list.msg_str + ", " + to_string(tisch.tischnr)
    output_list.total_tisch = total_tisch

    return generate_output()