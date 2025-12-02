#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Rd, 28/11/2025, with_for_update added
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep, H_artikel, Queasy

input_list_data, Input_list = create_model("Input_list", {"case_type":int, "dept_num":int})
wgrpdep_list_data, Wgrpdep_list = create_model("Wgrpdep_list", {"departement":int, "zknr":int, "bezeich":string, "isselected":bool, "rec_id":int})

def save_outlet_subgrp_setup_wizardbl(input_list_data:[Input_list], wgrpdep_list_data:[Wgrpdep_list]):

    prepare_cache ([Queasy])

    output_list_data = []
    case_type:int = 0
    departement:int = 0
    wgrpdep = h_artikel = queasy = None

    wgrpdep_list = input_list = output_list = None

    output_list_data, Output_list = create_model("Output_list", {"msg_str":string, "success_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, case_type, departement, wgrpdep, h_artikel, queasy


        nonlocal wgrpdep_list, input_list, output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def add_subgrp():

        nonlocal output_list_data, case_type, departement, wgrpdep, h_artikel, queasy


        nonlocal wgrpdep_list, input_list, output_list
        nonlocal output_list_data

        zknr:int = 0
        zknr = 0

        wgrpdep_list = query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id == -1 and wgrpdep_list.departement != 0 and wgrpdep_list.bezeich != ""), first=True)

        if not wgrpdep_list:
            output_list.msg_str = "No new subgroup inserted, please check your input"
            output_list.success_flag = False

            return

        for wgrpdep in db_session.query(Wgrpdep).order_by(Wgrpdep._recid).all():

            if zknr < wgrpdep.zknr:
                zknr = wgrpdep.zknr

        for wgrpdep_list in query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id == -1)):

            wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, wgrpdep_list.departement)],"bezeich": [(eq, wgrpdep_list.bezeich)]})

            if wgrpdep:
                output_list.msg_str = "Subgroup already exists"
                output_list.success_flag = False

                return
            wgrpdep = Wgrpdep()
            db_session.add(wgrpdep)

            wgrpdep.departement = wgrpdep_list.departement
            wgrpdep.bezeich = wgrpdep_list.bezeich
            wgrpdep.betriebsnr = 0
            wgrpdep.fibukonto = to_string(0) + ";" +\
                    to_string(0) + ";"

            if wgrpdep_list.zknr == 0:
                zknr = zknr + 1
                wgrpdep.zknr = zknr
            else:
                wgrpdep.zknr = wgrpdep_list.zknr
        output_list.msg_str = "Add data success"
        output_list.success_flag = True


    def chg_subgrp():

        nonlocal output_list_data, case_type, departement, wgrpdep, h_artikel, queasy


        nonlocal wgrpdep_list, input_list, output_list
        nonlocal output_list_data

        wgrpdep_list = query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id > 0), first=True)

        if not wgrpdep_list:
            output_list.msg_str = "Invalid Procedure, please contact our Customer Service"
            output_list.success_flag = False

            return

        for wgrpdep_list in query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id > 0)):

            wgrpdep = db_session.query(Wgrpdep).filter(
                     (Wgrpdep._recid != wgrpdep_list.rec_id) & (Wgrpdep.departement == wgrpdep_list.departement) & ((Wgrpdep.bezeich == wgrpdep_list.bezeich) | (Wgrpdep.zknr == wgrpdep_list.zknr))).first()

            if wgrpdep:

                if wgrpdep.zknr == wgrpdep_list.zknr:
                    output_list.msg_str = "Subgroup Number already exists, modify not possible"
                    output_list.success_flag = False


                else:
                    output_list.msg_str = "Subgroup already exists, modify not possible"
                    output_list.success_flag = False

                return

            if wgrpdep_list.zknr == 0:
                output_list.msg_str = "Invalid Subgroup Number, modify not possible"
                output_list.success_flag = False

                return

        for wgrpdep_list in query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id > 0)):

            wgrpdep = db_session.query(Wgrpdep).filter(
                     (Wgrpdep._recid != wgrpdep_list.rec_id) & (Wgrpdep.departement == wgrpdep_list.departement) & ((Wgrpdep.bezeich == wgrpdep_list.bezeich) | (Wgrpdep.zknr == wgrpdep_list.zknr))).first()

            if wgrpdep:

                if wgrpdep.zknr == wgrpdep_list.zknr:
                    output_list.msg_str = "Subgroup Number already exists, modify not possible"
                    output_list.success_flag = False


                else:
                    output_list.msg_str = "Subgroup already exists, modify not possible"
                    output_list.success_flag = False

                return

            if wgrpdep_list.zknr == 0:
                output_list.msg_str = "Invalid Subgroup Number, modify not possible"
                output_list.success_flag = False

                return

            # wgrpdep = get_cache (Wgrpdep, {"_recid": [(eq, wgrpdep_list.rec_id)]})
            wgrpdep = db_session.query(Wgrpdep).filter(
                     (Wgrpdep._recid == wgrpdep_list.rec_id)).with_for_update().first()

            if wgrpdep:
                wgrpdep.bezeich = wgrpdep_list.bezeich
                wgrpdep.zknr = wgrpdep_list.zknr


                pass
        output_list.msg_str = "Modify data success"
        output_list.success_flag = True


    def del_subgrp():

        nonlocal output_list_data, case_type, departement, wgrpdep, h_artikel, queasy


        nonlocal wgrpdep_list, input_list, output_list
        nonlocal output_list_data

        zknr:int = 0

        wgrpdep_list = query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id > 0 and wgrpdep_list.isSelected), first=True)

        if not wgrpdep_list:
            output_list.msg_str = "No existing subgroup selected.. please select at least 1 to delete"
            output_list.success_flag = False

            return
        else:
            departement = wgrpdep_list.departement
            zknr = wgrpdep_list.zknr

        h_artikel = get_cache (H_artikel, {"departement": [(eq, departement)],"zwkum": [(eq, zknr)]})

        if h_artikel:
            output_list.msg_str = "Article exists, delete not possible."
            output_list.success_flag = False

            return
        else:

            for wgrpdep_list in query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id > 0 and wgrpdep_list.isSelected)):

                wgrpdep = get_cache (Wgrpdep, {"_recid": [(eq, wgrpdep_list.rec_id)]})

                if not wgrpdep:
                    output_list.msg_str = "Subgroup does not exists, delete not possible."
                    output_list.success_flag = False

                    return

            for wgrpdep_list in query(wgrpdep_list_data, filters=(lambda wgrpdep_list: wgrpdep_list.rec_id > 0 and wgrpdep_list.isSelected)):

                # wgrpdep = get_cache (Wgrpdep, {"_recid": [(eq, wgrpdep_list.rec_id)]})
                wgrpdep = db_session.query(Wgrpdep).filter(
                         (Wgrpdep._recid == wgrpdep_list.rec_id)).with_for_update().first()

                if not wgrpdep:
                    output_list.msg_str = "Subgroup does not exists, delete not possible."
                    output_list.success_flag = False

                    return
                else:
                    pass
                    db_session.delete(wgrpdep)
        output_list.msg_str = "Delete success"
        output_list.success_flag = True


    def create_section(pos_num:int):

        nonlocal output_list_data, case_type, departement, wgrpdep, h_artikel, queasy


        nonlocal wgrpdep_list, input_list, output_list
        nonlocal output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 2)],"number2": [(eq, pos_num)],"deci1": [(eq, 2.2)],"char1": [(eq, "outlet administration")],"char2": [(eq, "subgroup setup")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 2
            queasy.number2 = pos_num
            queasy.deci1 =  to_decimal(2.2)
            queasy.char1 = "OUTLET ADMINISTRATION"
            queasy.char2 = "SUBGROUP SETUP"
            queasy.logi1 = True


        output_list.msg_str = "Progress saved successfully"
        output_list.success_flag = True


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        case_type = input_list.case_type
        departement = input_list.dept_num


    output_list = Output_list()
    output_list_data.append(output_list)


    if case_type == 1:
        add_subgrp()
    elif case_type == 2:
        chg_subgrp()
    elif case_type == 3:
        del_subgrp()
    elif case_type == 4:
        create_section(departement)
    else:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()

    return generate_output()