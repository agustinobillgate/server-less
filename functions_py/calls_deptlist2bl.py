#using conversion tools version: 1.0.0.117
# ====================================================
# Rulita, 03-09-2025
# modify output-list.datum format from mdy to dmy
# 
# ====================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calls_deptlistbl import calls_deptlistbl
from functions.read_parametersbl import read_parametersbl
from models import Parameters

cost_list_data, Cost_list = create_model("Cost_list", {"num":int, "name":string})

def calls_deptlist2bl(cost_list_data:[Cost_list], sorttype:int, cost_center:int, to_cc:int, price_decimal:int, from_date:date, to_date:date, double_currency:bool, pr_summary:bool):
    stattype = 0
    output_list_data = []
    print_list_data = []
    read_parameter_str1:string = ""
    read_parameter_str2:string = ""
    substrtr:string = ""
    parameters = None
    tmp_dd:string = ""
    tmp_mm:string = ""
    tmp_yy:string = ""

    str_list = cost_list = output_list = print_list = t_parameters = None

    str_list_data, Str_list = create_model("Str_list", {"nebenstelle":string, "zero_rate":bool, "local":Decimal, "ldist":Decimal, "ovsea":Decimal, "s":string})
    output_list_data, Output_list = create_model("Output_list", {"ext":string, "datum":string, "zeit":string, "dialed":string, "dest":string, "pabx_rate":string, "guest_rate":string, "duration":string, "zinr":string, "pulse":string, "lin":string, "print":string, "ref_no":string, "username":string})
    print_list_data, Print_list = create_model("Print_list", {"flag":int, "ext":string, "datum":string, "zeit":string, "dialed":string, "dest":string, "pabx_rate":string, "guest_rate":string, "duration":string, "local":Decimal, "ldist":Decimal, "ovsea":Decimal})
    t_parameters_data, T_parameters = create_model_like(Parameters)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stattype, output_list_data, print_list_data, read_parameter_str1, read_parameter_str2, substrtr, parameters
        nonlocal sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency, pr_summary


        nonlocal str_list, cost_list, output_list, print_list, t_parameters
        nonlocal str_list_data, output_list_data, print_list_data, t_parameters_data

        return {"cost-list": cost_list_data, "stattype": stattype, "output-list": output_list_data, "print-list": print_list_data}


    output_list_data.clear()
    cost_list_data, stattype, str_list_data = get_output(calls_deptlistbl(cost_list_data, sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency))

    for str_list in query(str_list_data):
        
        # Rulita | fixing format datum report Department Calls from mdy to dmy  
        tmp_dd = substring(str_list.s, 9, 2)
        tmp_mm = substring(str_list.s, 6, 2)
        tmp_yy = substring(str_list.s, 12, 2)

        if substring(str_list.s, 6, 8) != '        ' :
            tmp_datum = tmp_dd + '/' + tmp_mm + '/' + tmp_yy
        else:
            tmp_datum = substring(str_list.s, 6, 8)

        if tmp_datum == '//':
            tmp_datum = ''

        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.ext = substring(str_list.s, 0, 6)
        # output_list.datum = substring(str_list.s, 6, 8)
        output_list.datum = tmp_datum
        output_list.zeit = substring(str_list.s, 14, 5)
        output_list.dialed = substring(str_list.s, 19, 24)
        output_list.dest = substring(str_list.s, 43, 16)
        output_list.pabx_rate = substring(str_list.s, 59, 13)
        output_list.guest_rate = substring(str_list.s, 72, 13)
        output_list.duration = substring(str_list.s, 85, 8)
        output_list.zinr = substring(str_list.s, 93, 6)
        output_list.pulse = substring(str_list.s, 99, 6)
        output_list.lin = substring(str_list.s, 105, 4)
        output_list.print = substring(str_list.s, 109, 3)
        output_list.ref_no = substring(str_list.s, 112, 7)
        output_list.username = substring(str_list.s, 119, 32)

    for str_list in query(str_list_data, filters=(lambda str_list: not str_list.zero_rate)):

        if sorttype == 0:

            if substring(trim(str_list.s) , 0, 10) == ("TOTAL DEPT").lower()  or substring(trim(str_list.s) , 0, 5) == ("GRAND").lower() :
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.flag = 0
                print_list.ext = "---"

            if substring(trim(str_list.s) , 0, 10) == ("TOTAL EXT.").lower()  and not pr_summary:
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.flag = 0
                print_list.ext = "---"

            if not pr_summary:
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.flag = 1
                print_list.ext = substring(str_list.s, 0, 6)
                print_list.datum = substring(str_list.s, 6, 8)
                print_list.zeit = substring(str_list.s, 14, 5)
                print_list.dialed = substring(str_list.s, 19, 24)
                print_list.dest = substring(str_list.s, 43, 16)
                print_list.pabx_rate = substring(str_list.s, 59, 13)
                print_list.duration = substring(str_list.s, 85, 8)

            elif pr_summary and (substring(trim(str_list.s) , 0, 5) == ("TOTAL").lower()  or substring(trim(str_list.s) , 0, 5) == ("GRAND").lower()):

                if substring(trim(str_list.s) , 0, 10) == ("TOTAL EXT.").lower() :
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.flag = 2
                    print_list.ext = substring(trim(str_list.s) , 13, 6)

                elif substring(trim(str_list.s) , 0, 10) == ("TOTAL DEPT").lower() :

                    cost_list = query(cost_list_data, filters=(lambda cost_list: cost_list.num == to_int(substring(trim(str_list.s) , 13, 4))), first=True)

                    if cost_list:
                        print_list = Print_list()
                        print_list_data.append(print_list)

                        print_list.flag = 2
                        print_list.ext = cost_list.name


                else:
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.flag = 2
                    print_list.ext = substring(str_list.s, 19, 24)


                print_list.local =  to_decimal(str_list.local)
                print_list.ldist =  to_decimal(str_list.ldist)
                print_list.ovsea =  to_decimal(str_list.ovsea)
                print_list.pabx_rate = substring(str_list.s, 59, 13)
                print_list.guest_rate = substring(str_list.s, 72, 13)

                if substring(trim(str_list.s) , 0, 10) == ("TOTAL DEPT").lower() :
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.flag = 0


        else:

            if substring(trim(str_list.s) , 0, 10) == ("TOTAL DEPT").lower()  or substring(trim(str_list.s) , 0, 5) == ("GRAND").lower() :
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.flag = 0
                print_list.ext = "---"

            if substring(trim(str_list.s) , 0, 10) == ("TOTAL USER").lower()  and not pr_summary:
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.flag = 0
                print_list.ext = "---"

            if not pr_summary:
                print_list = Print_list()
                print_list_data.append(print_list)

                print_list.flag = 1
                print_list.ext = substring(str_list.s, 0, 6)
                print_list.datum = substring(str_list.s, 6, 8)
                print_list.zeit = substring(str_list.s, 14, 5)
                print_list.dialed = substring(str_list.s, 19, 24)
                print_list.dest = substring(str_list.s, 43, 16)
                print_list.pabx_rate = substring(str_list.s, 59, 13)
                print_list.duration = substring(str_list.s, 85, 8)

            elif pr_summary and (substring(trim(str_list.s) , 0, 5) == ("TOTAL").lower()  or substring(trim(str_list.s) , 0, 5) == ("GRAND").lower()):

                if substring(trim(str_list.s) , 0, 10) == ("TOTAL USER").lower() :
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.ext = substring(trim(str_list.s) , 13, 6)

                elif substring(trim(str_list.s) , 0, 10) == ("TOTAL DEPT").lower() :
                    read_parameter_str1 = "CostCenter"
                    read_parameter_str2 = "Name"
                    substrtr = substring(trim(str_list.s) , 13, 4)


                    t_parameters_data = get_output(read_parametersbl(5, read_parameter_str1, read_parameter_str2, substrtr, None))

                    t_parameters = query(t_parameters_data, first=True)
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.ext = t_parameters.vstring


                else:
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.ext = substring(str_list.s, 19, 24)


                print_list.local =  to_decimal(str_list.local)
                print_list.ldist =  to_decimal(str_list.ldist)
                print_list.ovsea =  to_decimal(str_list.ovsea)
                print_list.pabx_rate = substring(str_list.s, 59, 13)
                print_list.guest_rate = substring(str_list.s, 72, 13)

                if substring(trim(str_list.s) , 0, 10) == ("TOTAL DEPT").lower() :
                    print_list = Print_list()
                    print_list_data.append(print_list)

                    print_list.flag = 0

    return generate_output()