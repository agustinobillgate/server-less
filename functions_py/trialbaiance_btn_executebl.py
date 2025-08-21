#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 21/8/20225
# data tidak tampil semua
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.trialbalance_btn_go_cld_1bl import trialbalance_btn_go_cld_1bl

def trialbaiance_btn_executebl(acct_type:int, from_fibu:string, to_fibu:string, sorttype:int, from_dept:int, from_date:date, to_date:date, close_month:int, close_date:date, pnl_acct:string, close_year:date, prev_month:int, show_longbal:bool, pbal_flag:bool, asremoteflag:bool):
    msg_str = ""
    tb_list_detail_data = []
    tb_list_summary_data = []
    refno:string = ""
    begining_bal:string = ""
    tot_debit:string = ""
    tot_credit:string = ""
    net_change:string = ""
    ending_bal:string = ""
    ytd_balance:string = ""

    output_list = tb_list_summary = tb_list_detail = None

    output_list_data, Output_list = create_model("Output_list", {"gop_flag":bool, "nr":int, "str":string, "budget":Decimal, "proz":Decimal, "mark":bool, "ch":string, "ref_no":string, "begin_bal":string, "tot_debit":string, "tot_credit":string, "net_change":string, "ending_bal":string, "ytd_bal":string, "dept_nr":int, "dept_name":string, "is_show_depart":bool})
    tb_list_summary_data, Tb_list_summary = create_model("Tb_list_summary", {"account_no":string, "description":string, "beginingbal":string, "tot_debit":string, "tot_credit":string, "net_change":string, "ending_bal":string, "ytd_balance":string, "budget":Decimal, "proz":Decimal, "dept_nr":string, "dept_name":string})
    tb_list_detail_data, Tb_list_detail = create_model("Tb_list_detail", {"marks":string, "date":date, "ref_no":string, "begining_bal":string, "tot_debit":string, "tot_credit":string, "net_change":string, "ending_bal":string, "note":string, "dept_nr":string, "dept_name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, tb_list_detail_data, tb_list_summary_data, refno, begining_bal, tot_debit, tot_credit, net_change, ending_bal, ytd_balance
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, tb_list_summary, tb_list_detail
        nonlocal output_list_data, tb_list_summary_data, tb_list_detail_data

        return {"msg_str": msg_str, "tb-list-detail": tb_list_detail_data, "tb-list-summary": tb_list_summary_data}


    output_list_data = get_output(trialbalance_btn_go_cld_1bl(acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag))

    if sorttype == 1:

        for output_list in query(output_list_data):
            # print(output_list.str)
            refno = output_list.ref_no
            begining_bal = output_list.begin_bal
            tot_debit = output_list.tot_debit
            tot_credit = output_list.tot_credit
            net_change = output_list.net_change
            ending_bal = output_list.ending_bal

            if matches(begining_bal,r"*(*"):
                begining_bal = replace_str(begining_bal, "(", "-")

            if matches(begining_bal,r"*)*"):
                begining_bal = replace_str(begining_bal, ")", "")

            if matches(tot_debit,r"*(*"):
                tot_debit = replace_str(tot_debit, "(", "-")

            if matches(tot_debit,r"*)*"):
                tot_debit = replace_str(tot_debit, ")", "")

            if matches(tot_credit,r"*(*"):
                tot_credit = replace_str(tot_credit, "(", "-")

            if matches(tot_credit,r"*)*"):
                tot_credit = replace_str(tot_credit, ")", "")

            if matches(net_change,r"*(*"):
                net_change = replace_str(net_change, "(", "-")

            if matches(net_change,r"*)*"):
                net_change = replace_str(net_change, ")", "")

            if matches(ending_bal,r"*(*"):
                ending_bal = replace_str(ending_bal, "(", "-")

            if matches(ending_bal,r"*)*"):
                ending_bal = replace_str(ending_bal, ")", "")
            tb_list_detail = Tb_list_detail()
            tb_list_detail_data.append(tb_list_detail)

            tb_list_detail.marks = output_list.ch
            tb_list_detail.date = date_mdy(trim(substring(output_list.str, 0, 8)))
            tb_list_detail.ref_no = refno
            tb_list_detail.begining_bal = begining_bal
            tb_list_detail.tot_debit = tot_debit
            tb_list_detail.tot_credit = tot_credit
            tb_list_detail.net_change = net_change
            tb_list_detail.ending_bal = ending_bal
            tb_list_detail.note = substring(output_list.str, 134, 62)

            if output_list.is_show_depart :
                tb_list_detail.dept_nr = to_string(output_list.dept_nr)
                tb_list_detail.dept_name = output_list.dept_name
            else:
                tb_list_detail.dept_nr = ""
                tb_list_detail.dept_name = ""
    else:

        for output_list in query(output_list_data):
            # print(output_list.str)
            refno = substring(output_list.str, 0, 16)
            begining_bal = (replace_str(substring(output_list.str, 54, 22) , ",", ""))
            tot_debit = (replace_str(substring(output_list.str, 76, 22) , ",", ""))
            tot_credit = (replace_str(substring(output_list.str, 98, 22) , ",", ""))
            net_change = (replace_str(substring(output_list.str, 120, 22) , ",", ""))
            ending_bal = (replace_str(substring(output_list.str, 142, 22) , ",", ""))
            ytd_balance = (replace_str(substring(output_list.str, 164, 22) , ",", ""))

            if matches(begining_bal,r"*(*"):
                begining_bal = replace_str(begining_bal, "(", "-")

            if matches(begining_bal,r"*)*"):
                begining_bal = replace_str(begining_bal, ")", "")

            if matches(tot_debit,r"*(*"):
                tot_debit = replace_str(tot_debit, "(", "-")

            if matches(tot_debit,r"*)*"):
                tot_debit = replace_str(tot_debit, ")", "")

            if matches(tot_credit,r"*(*"):
                tot_credit = replace_str(tot_credit, "(", "-")

            if matches(tot_credit,r"*)*"):
                tot_credit = replace_str(tot_credit, ")", "")

            if matches(net_change,r"*(*"):
                net_change = replace_str(net_change, "(", "-")

            if matches(net_change,r"*)*"):
                net_change = replace_str(net_change, ")", "")

            if matches(ending_bal,r"*(*"):
                ending_bal = replace_str(ending_bal, "(", "-")

            if matches(ending_bal,r"*)*"):
                ending_bal = replace_str(ending_bal, ")", "")

            if matches(ytd_balance,r"*(*"):
                ytd_balance = replace_str(ytd_balance, "(", "-")

            if matches(ytd_balance,r"*)*"):
                ytd_balance = replace_str(ytd_balance, ")", "")
            tb_list_summary = Tb_list_summary()
            tb_list_summary_data.append(tb_list_summary)

            tb_list_summary.account_no = trim(refno)
            tb_list_summary.description = trim(substring(output_list.str, 16, 38))
            tb_list_summary.beginingbal = begining_bal
            tb_list_summary.tot_debit = tot_debit
            tb_list_summary.tot_credit = tot_credit
            tb_list_summary.net_change = net_change
            tb_list_summary.ending_bal = ending_bal
            tb_list_summary.ytd_balance = ytd_balance
            tb_list_summary.budget =  to_decimal(output_list.budget)
            tb_list_summary.proz =  to_decimal(output_list.proz)

            if output_list.is_show_depart :
                tb_list_summary.dept_nr = to_string(output_list.dept_nr)
                tb_list_summary.dept_name = output_list.dept_name
            else:
                tb_list_summary.dept_nr = ""
                tb_list_summary.dept_name = ""

    return generate_output()