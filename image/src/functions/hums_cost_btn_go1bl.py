from functions.additional_functions import *
import decimal
from datetime import date
from functions.hums_cost_btn_gobl import hums_cost_btn_gobl

def hums_cost_btn_go1bl(language_code:int, sorttype:int, detailed:bool, from_dept:int, to_dept:int, from_date:date, to_date:date, fact1:int, short_flag:bool, mi_compli_checked:bool):
    fb_cost_report_list = []

    fb_cost_report = output_list = None

    fb_cost_report_list, Fb_cost_report = create_model("Fb_cost_report", {"departement":str, "qty":str, "sales":str, "cost":str, "qty2":str, "compliment":str, "t_cost":str, "ratio":str, "m_qty":str, "m_sales":str, "m_cost":str, "m_qty2":str, "compliment2":str, "t_cost2":str, "ratio2":str})
    output_list_list, Output_list = create_model("Output_list", {"anz":int, "m_anz":int, "comanz":int, "m_comanz":int, "s":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fb_cost_report_list


        nonlocal fb_cost_report, output_list
        nonlocal fb_cost_report_list, output_list_list
        return {"fb-cost-report": fb_cost_report_list}

    output_list_list = get_output(hums_cost_btn_gobl(language_code, sorttype, detailed, from_dept, to_dept, from_date, to_date, fact1, short_flag, mi_compli_checked))
    fb_cost_report._list.clear()

    for output_list in query(output_list_list):
        fb_cost_report = Fb_cost_report()
        fb_cost_report_list.append(fb_cost_report)

        fb_cost_report.departement = substring(output_list.s, 0, 23)
        fb_cost_report.qty = to_string(output_list.anz, ">>>>>")
        fb_cost_report.sales = substring(output_list.s, 23, 20)
        fb_cost_report.cost = substring(output_list.s, 43, 20)
        fb_cost_report.qty2 = to_string(output_list.comanz, ">>>>>")
        fb_cost_report.compliment = substring(output_list.s, 63, 20)
        fb_cost_report.t_cost = substring(output_list.s, 83, 20)
        fb_cost_report.ratio = substring(output_list.s, 103, 6)
        fb_cost_report.m_qty = to_string(output_list.m_anz, ">>>>>")
        fb_cost_report.m_sales = substring(output_list.s, 109, 20)
        fb_cost_report.m_cost = substring(output_list.s, 129, 20)
        fb_cost_report.m_qty2 = to_string(output_list.m_comanz, ">>>>>")
        fb_cost_report.compliment2 = substring(output_list.s, 149, 20)
        fb_cost_report.t_cost2 = substring(output_list.s, 169, 20)
        fb_cost_report.ratio2 = substring(output_list.s, 189, 6)


        pass

    return generate_output()