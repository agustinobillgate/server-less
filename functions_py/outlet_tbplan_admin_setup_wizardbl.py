#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Tisch, Queasy

input_list_data, Input_list = create_model("Input_list", {"new_tisch":int, "dept_num":int, "case_type":int})
t_list_data, T_list = create_model("T_list", {"departement":int, "tischnr":int, "tisch_recid":int, "isselected":bool, "x_coordinate":Decimal, "y_coordinate":Decimal})

def outlet_tbplan_admin_setup_wizardbl(input_list_data:[Input_list], t_list_data:[T_list]):
    output_list_data = []
    new_tisch:int = 0
    total_tisch:int = 0
    dept_num:int = 0
    case_type:int = 0
    looping:int = 0
    init_table:int = 0
    num_table:int = 0
    init_x:Decimal = to_decimal("0.0")
    init_y:Decimal = to_decimal("0.0")
    increment_x:int = 0
    increment_y:int = 0
    tisch = queasy = None

    input_list = t_list = output_list = None

    output_list_data, Output_list = create_model("Output_list", {"msg_str":string, "success_flag":bool}, {"success_flag": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, new_tisch, total_tisch, dept_num, case_type, looping, init_table, num_table, init_x, init_y, increment_x, increment_y, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def add_tisch():

        nonlocal output_list_data, new_tisch, total_tisch, dept_num, case_type, looping, init_table, num_table, init_x, init_y, increment_x, increment_y, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal output_list_data


        num_table = 1
        init_table = 0

        for tisch in db_session.query(Tisch).filter(
                 (Tisch.departement == dept_num)).order_by(Tisch.tischnr.desc()).all():

            if tisch.tischnr >= num_table:
                num_table = tisch.tischnr + 1
            init_table = init_table + 1
        total_tisch = new_tisch + init_table

        if total_tisch > 100:
            output_list.msg_str = "Can't add more table on this department, Total table existing are higher than allowed number"
            output_list.success_flag = False

            return

        if init_table == 0:
            for looping in range(1,new_tisch  + 1) :

                tisch = get_cache (Tisch, {"departement": [(eq, dept_num)],"tischnr": [(eq, num_table)]})

                if not tisch:
                    tisch = Tisch()
                    db_session.add(tisch)

                    tisch.tischnr = num_table
                    tisch.departement = dept_num
                    tisch.bezeich = "TABLE " + trim(to_string(num_table, ">>>>>>99"))
                    tisch.normalbeleg = 2
                    tisch.roomcharge = False
                    tisch.betriebsnr = 0
                    num_table = num_table + 1


            init_x =  to_decimal(37.5)
            init_y =  to_decimal(97.4) - to_decimal(56.25)
            increment_x = 11
            increment_y = 0

            for tisch in db_session.query(Tisch).filter(
                     (Tisch.departement == dept_num)).order_by(Tisch.tischnr).all():

                if increment_x == 11 and increment_y < 9:
                    increment_x = 1
                    increment_y = increment_y + 1
                    init_x =  to_decimal(37.5)
                    init_y =  to_decimal(init_y) + to_decimal(56.25)

                elif increment_x == 11 and increment_y == 9:
                    increment_x = -1
                    increment_y = -1
                    init_x =  to_decimal("975")
                    init_y =  to_decimal(584.9)

                elif increment_x == -1 and increment_y == -1:
                    output_list.msg_str = "Error table creation, Total table are higher than allowed number"
                    output_list.success_flag = False

                    return
                else:
                    increment_x = increment_x + 1
                    init_x =  to_decimal(init_x) + to_decimal(90.00)

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if queasy:
                    pass
                    queasy.number2 = tisch.tischnr
                    queasy.deci1 =  to_decimal(init_x)
                    queasy.deci2 =  to_decimal(init_y)


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 31
                    queasy.number1 = dept_num
                    queasy.number2 = tisch.tischnr
                    queasy.deci1 =  to_decimal(init_x)
                    queasy.deci2 =  to_decimal(init_y)
                    queasy.deci3 =  to_decimal("0")


                pass
                pass
        else:
            for looping in range(1,new_tisch  + 1) :

                tisch = get_cache (Tisch, {"departement": [(eq, dept_num)],"tischnr": [(eq, num_table)]})

                if not tisch:
                    tisch = Tisch()
                    db_session.add(tisch)

                    tisch.tischnr = num_table
                    tisch.departement = dept_num
                    tisch.bezeich = "TABLE " + trim(to_string(num_table, ">>>>>>99"))
                    tisch.normalbeleg = 2
                    tisch.roomcharge = False
                    tisch.betriebsnr = 0
                    num_table = num_table + 1

            for tisch in db_session.query(Tisch).filter(
                     (Tisch.departement == dept_num)).order_by(Tisch.tischnr).all():

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 31
                    queasy.number1 = dept_num
                    queasy.number2 = tisch.tischnr
                    queasy.deci1 =  to_decimal("0")
                    queasy.deci2 =  to_decimal("0")
                    queasy.deci3 =  to_decimal("0")


        output_list.msg_str = "Table created succesfully"
        output_list.success_flag = True


    def mod_tisch():

        nonlocal output_list_data, new_tisch, total_tisch, dept_num, case_type, looping, init_table, num_table, init_x, init_y, increment_x, increment_y, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal output_list_data

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.isSelected)):

            if t_list.tischnr <= 0:
                output_list.msg_str = "Error modify table.. invalid input table number" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

            tisch = get_cache (Tisch, {"_recid": [(ne, t_list.tisch_recid)],"tischnr": [(eq, t_list.tischnr)],"departement": [(eq, t_list.departement)]})

            if tisch:
                output_list.msg_str = "Error modify table.. table with the same number already exist" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)]})

            if tisch:

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if not queasy:
                    output_list.msg_str = "Error modify table.. table not yet exist in floor plan" +\
                            chr_unicode(10) +\
                            "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                    output_list.success_flag = False

                    return

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.isSelected)):

            if t_list.tischnr <= 0:
                output_list.msg_str = "Error modify table.. invalid input table number" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)]})

            if tisch:

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if queasy:
                    pass
                    queasy.number2 = t_list.tischnr


                    pass
                    pass
                pass
                tisch.tischnr = t_list.tischnr
                tisch.bezeich = "TABLE " + trim(to_string(t_list.tischnr, ">>>>>>99"))


                pass
                pass
        output_list.msg_str = "Table Modified succesfully"
        output_list.success_flag = True


    def del_tisch():

        nonlocal output_list_data, new_tisch, total_tisch, dept_num, case_type, looping, init_table, num_table, init_x, init_y, increment_x, increment_y, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal output_list_data

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.isSelected)):

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)]})

            if tisch:

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if not queasy:
                    output_list.msg_str = "Error delete table.. table not exist in floor plan" +\
                            chr_unicode(10) +\
                            "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                    output_list.success_flag = False

                    return
            else:
                output_list.msg_str = "Error delete table.. table not recorded yet" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.isSelected)):

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)]})

            if tisch:

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if queasy:
                    pass
                    db_session.delete(queasy)
                else:
                    output_list.msg_str = "Error modify table.. table not exist in floor plan" +\
                            chr_unicode(10) +\
                            "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                    output_list.success_flag = False

                    return
                pass
                db_session.delete(tisch)
        output_list.msg_str = "Table Deleted Succesfully"
        output_list.success_flag = True


    def save_tisch_position():

        nonlocal output_list_data, new_tisch, total_tisch, dept_num, case_type, looping, init_table, num_table, init_x, init_y, increment_x, increment_y, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal output_list_data

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.isSelected)):

            if (t_list.x_coordinate < 0 or t_list.x_coordinate > 975 or t_list.y_coordinate < 59.9 or t_list.Y_coordinate > 584.9) and not (t_list.x_coordinate == 0 and t_list.x_coordinate == 0):
                output_list.msg_str = "Error modify table plan.. out of range" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)],"tischnr": [(ne, t_list.tischnr)]})

            if tisch:
                output_list.msg_str = "Error modify table plan.. discrepancy table number" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)]})

            if tisch:

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if not queasy:
                    output_list.msg_str = "Error modify table plan.. table not exist in floor plan" +\
                            chr_unicode(10) +\
                            "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                    output_list.success_flag = False

                    return

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.isSelected)):

            if (t_list.x_coordinate < 0 or t_list.x_coordinate > 975 or t_list.y_coordinate < 59.9 or t_list.Y_coordinate > 584.9) and not (t_list.x_coordinate == 0 and t_list.x_coordinate == 0):
                output_list.msg_str = "Error modify table plan.. out of range" +\
                        chr_unicode(10) +\
                        "TABLE " + trim(to_string(t_list.tischnr, ">>>>>99"))
                output_list.success_flag = False

                return

            tisch = get_cache (Tisch, {"_recid": [(eq, t_list.tisch_recid)]})

            if tisch:

                queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)]})

                if queasy:
                    pass
                    queasy.deci1 =  to_decimal(t_list.x_coordinate)
                    queasy.deci2 =  to_decimal(t_list.y_coordinate)


                    pass
                    pass
                pass
                pass
        output_list.msg_str = "Table Position Saved"
        output_list.success_flag = True


    def create_section(pos_num:int):

        nonlocal output_list_data, new_tisch, total_tisch, dept_num, case_type, looping, init_table, num_table, init_x, init_y, increment_x, increment_y, tisch, queasy


        nonlocal input_list, t_list, output_list
        nonlocal output_list_data

        queasy = get_cache (Queasy, {"key": [(eq, 357)],"number1": [(eq, 2)],"number2": [(eq, pos_num)],"deci1": [(eq, 2.4)],"char1": [(eq, "outlet administration")],"char2": [(eq, "table layout setup")],"logi1": [(eq, True)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 2
            queasy.number2 = pos_num
            queasy.deci1 =  to_decimal(2.4)
            queasy.char1 = "OUTLET ADMINISTRATION"
            queasy.char2 = "TABLE LAYOUT SETUP"
            queasy.logi1 = True


        output_list.msg_str = "Progress saved successfully"
        output_list.success_flag = True

    output_list = Output_list()
    output_list_data.append(output_list)


    input_list = query(input_list_data, first=True)

    if not input_list:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()
    else:
        new_tisch = input_list.new_tisch
        dept_num = input_list.dept_num
        case_type = input_list.case_type

    if new_tisch > 100 or new_tisch < 0:
        output_list.msg_str = "Invalid input, Total table are higher than allowed number"
        output_list.success_flag = False

        return generate_output()

    if case_type == 1:
        add_tisch()
    elif case_type == 2:
        mod_tisch()
    elif case_type == 3:
        del_tisch()
    elif case_type == 4:
        save_tisch_position()
    elif case_type == 5:
        create_section(dept_num)
    else:
        output_list.msg_str = "Error loading.. please contact our Customer Service"
        output_list.success_flag = False

        return generate_output()

    return generate_output()