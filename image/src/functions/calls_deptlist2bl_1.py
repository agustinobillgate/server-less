from functions.additional_functions import *
import decimal
from datetime import date
from functions.calls_deptlistbl import calls_deptlistbl

cost_list_list, Cost_list = create_model("Cost_list", {"num":int, "name":str})
str_list_list, Str_list = create_model("Str_list", {"nebenstelle":str, "zero_rate":bool, "local":decimal, "ldist":decimal, "ovsea":decimal, "s":str})
output_list_list, Output_list = create_model("Output_list", {"ext":str, "datum":str, "zeit":str, "dialed":str, "dest":str, "pabx_rate":str, "guest_rate":str, "duration":str, "zinr":str, "pulse":str, "lin":str, "print":str, "ref_no":str, "username":str})

def calls_deptlist2bl(cost_list_list:[Cost_list], sorttype:int, cost_center:int, to_cc:int, price_decimal:int, from_date:date, to_date:date, double_currency:bool):
    stattype = 0
    output_list_list = []

    str_list = cost_list = output_list = None
    db_session = local_storage.db_session
    # print("CostList:", cost_list_list)

    def generate_output():
        nonlocal stattype, output_list_list
        nonlocal sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency
        nonlocal str_list, cost_list, output_list
        nonlocal str_list_list, cost_list_list, output_list_list
        return {"cost-list": cost_list_list, "str-list": str_list_list, "stattype": stattype, "output-list": output_list_list}

    output_list_list.clear()
    # print("CostList1:", cost_list_list)
    cost_list_listb, stattype, str_list_list = get_output(calls_deptlistbl(cost_list_list, sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency))
    # print("CostList1b:", cost_list_listb)
    # print("StrList:", str_list_list)
    for str_list in query(str_list_list):
        output_list = Output_list()
        output_list_list.append(output_list)
        # print("Str:", str_list.s)
        if str_list is not None :
            output_list.ext = substring(str_list.s, 0, 6)
            output_list.datum = substring(str_list.s, 6, 8)
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


    return generate_output()