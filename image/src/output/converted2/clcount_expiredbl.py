#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Cl_memtype, Cl_member, Mc_fee

def clcount_expiredbl(code_num:string):

    prepare_cache ([Cl_memtype, Cl_member, Mc_fee])

    exp_date = None
    memtype:int = 0
    fdate:date = None
    dauer:int = 0
    i:int = 0
    dd:int = 0
    mm:int = 0
    yy:int = 0
    total_days:int = 0
    count_month:int = 0
    curr_month:int = 0
    sum_day:List[int] = create_empty_list(12,0)
    cl_memtype = cl_member = mc_fee = None

    tbuff = None

    Tbuff = create_buffer("Tbuff",Cl_memtype)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exp_date, memtype, fdate, dauer, i, dd, mm, yy, total_days, count_month, curr_month, sum_day, cl_memtype, cl_member, mc_fee
        nonlocal code_num
        nonlocal tbuff


        nonlocal tbuff

        return {"exp_date": exp_date}


    cl_member = get_cache (Cl_member, {"codenum": [(eq, code_num)]})

    if cl_member.memstatus == 0:
        exp_date = cl_member.expired_date

        return generate_output()

    mc_fee = get_cache (Mc_fee, {"key": [(eq, 2)],"nr": [(eq, cl_member.membertype)],"gastnr": [(eq, cl_member.gastnr)],"activeflag": [(eq, 0)]})

    if mc_fee:
        exp_date = mc_fee.bis_datum

        return generate_output()
    memtype = cl_member.membertype
    fdate = cl_member.expired_date
    dauer = cl_member.num1


    sum_day[0] = 31

    if (get_year(fdate) % 4) == 0:
        sum_day[1] = 29
    else:
        sum_day[1] = 28
    sum_day[2] = 31
    sum_day[3] = 30
    sum_day[4] = 31
    sum_day[5] = 30
    sum_day[6] = 31
    sum_day[7] = 31
    sum_day[8] = 30
    sum_day[9] = 31
    sum_day[10] = 30
    sum_day[11] = 31

    tbuff = get_cache (Cl_memtype, {"nr": [(eq, memtype)]})

    if tbuff:

        if dauer == 0:
            dauer = tbuff.dauer
        dd = get_day(fdate)
        mm = get_month(fdate)
        yy = get_year(fdate)
        total_days = sum_day[mm - 1] - dd
        count_month = 1
        curr_month = mm + 1

        if curr_month == 13:
            curr_month = 1
        while True:

            if count_month == dauer:
                break
            total_days = total_days + sum_day[curr_month - 1]
            count_month = count_month + 1
            curr_month = curr_month + 1

            if curr_month == 13:
                curr_month = 1

            if curr_month == 0:
                curr_month = 12
        exp_date = fdate + total_days + dd - timedelta(days=1)

    return generate_output()