#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Reslin_queasy, Res_line

def flag_report_create_listbl(user_init:string, f_date:date, t_date:date, sorttype:int, alldept_flag:bool):

    prepare_cache ([Bediener, Reslin_queasy, Res_line])

    s_list_list = []
    bediener = reslin_queasy = res_line = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"frdate":date, "date":date, "name":string, "zinr":string, "flag":bool, "ci":bool, "co":bool, "ankunft":date, "abreise":date, "urgent":bool, "done":bool, "id":string, "dept":string, "bemerk":string, "resnr":int, "reslinnr":int, "ind":int, "s_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, bediener, reslin_queasy, res_line
        nonlocal user_init, f_date, t_date, sorttype, alldept_flag


        nonlocal s_list
        nonlocal s_list_list

        return {"s-list": s_list_list}

    def create_list():

        nonlocal s_list_list, bediener, reslin_queasy, res_line
        nonlocal user_init, f_date, t_date, sorttype, alldept_flag


        nonlocal s_list
        nonlocal s_list_list

        do_it:bool = False
        ci_flag:bool = False
        dept_str:string = ""
        frdate:date = None

        for s_list in query(s_list_list):
            s_list_list.remove(s_list)
            pass

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.date1 >= f_date)).order_by(Reslin_queasy.date1).all():
            do_it, ci_flag, dept_str, frdate = check_do_it(reslin_queasy.char1, reslin_queasy.date1, logical(reslin_queasy.deci1))

            if do_it:

                if reslin_queasy.date1 <= f_date and reslin_queasy.date1 > t_date:

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)],"active_flag": [(le, 1)]})
                else:

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)],"active_flag": [(le, 2)],"resstatus": [(ne, 9),(ne, 10)]})

                if res_line:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.date = reslin_queasy.date1
                    s_list.name = res_line.name
                    s_list.zinr = res_line.zinr
                    s_list.flag = (res_line.active_flag == 1)
                    s_list.co = (res_line.active_flag == 2)
                    s_list.ankunft = res_line.ankunft
                    s_list.abreise = res_line.abreise
                    s_list.id = entry(1, reslin_queasy.char1, chr_unicode(2))
                    s_list.bemerk = entry(0, reslin_queasy.char1, chr_unicode(2))
                    s_list.resnr = reslin_queasy.resnr
                    s_list.reslinnr = reslin_queasy.reslinnr
                    s_list.urgent = (reslin_queasy.number1 == 1)
                    s_list.done = (reslin_queasy.deci1 == 1)
                    s_list.ind = 1
                    s_list.ci = ci_flag
                    s_list.frdate = frdate
                    s_list.dept = dept_str
                    s_list.s_recid = reslin_queasy._recid

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.date2 >= f_date)).order_by(Reslin_queasy.date2).all():
            do_it, ci_flag, dept_str, frdate = check_do_it(reslin_queasy.char2, reslin_queasy.date2, logical(reslin_queasy.deci2))

            if do_it:

                if reslin_queasy.date2 <= f_date and reslin_queasy.date2 > t_date:

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)],"active_flag": [(le, 1)]})
                else:

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)],"active_flag": [(le, 2)],"resstatus": [(ne, 9),(ne, 10)]})

                if res_line:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.date = reslin_queasy.date2
                    s_list.name = res_line.name
                    s_list.zinr = res_line.zinr
                    s_list.flag = (res_line.active_flag == 1)
                    s_list.co = (res_line.active_flag == 2)
                    s_list.ankunft = res_line.ankunft
                    s_list.abreise = res_line.abreise
                    s_list.id = entry(1, reslin_queasy.char2, chr_unicode(2))
                    s_list.bemerk = entry(0, reslin_queasy.char2, chr_unicode(2))
                    s_list.resnr = reslin_queasy.resnr
                    s_list.reslinnr = reslin_queasy.reslinnr
                    s_list.urgent = (reslin_queasy.number2 == 1)
                    s_list.done = (reslin_queasy.deci2 == 1)
                    s_list.ind = 2
                    s_list.ci = ci_flag
                    s_list.frdate = frdate
                    s_list.dept = dept_str
                    s_list.s_recid = reslin_queasy._recid

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.date3 >= f_date)).order_by(Reslin_queasy.date3).all():
            do_it, ci_flag, dept_str, frdate = check_do_it(reslin_queasy.char3, reslin_queasy.date3, logical(reslin_queasy.deci3))

            if do_it:

                if reslin_queasy.date3 <= f_date and reslin_queasy.date3 > t_date:

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)],"active_flag": [(le, 1)]})
                else:

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)],"active_flag": [(le, 2)],"resstatus": [(ne, 9),(ne, 10)]})

                if res_line:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.date = reslin_queasy.date3
                    s_list.name = res_line.name
                    s_list.zinr = res_line.zinr
                    s_list.flag = (res_line.active_flag == 1)
                    s_list.co = (res_line.active_flag == 2)
                    s_list.ankunft = res_line.ankunft
                    s_list.abreise = res_line.abreise
                    s_list.id = entry(1, reslin_queasy.char3, chr_unicode(2))
                    s_list.bemerk = entry(0, reslin_queasy.char3, chr_unicode(2))
                    s_list.resnr = reslin_queasy.resnr
                    s_list.reslinnr = reslin_queasy.reslinnr
                    s_list.urgent = (reslin_queasy.number3 == 1)
                    s_list.done = (reslin_queasy.deci3 == 1)
                    s_list.ind = 3
                    s_list.ci = ci_flag
                    s_list.frdate = frdate
                    s_list.dept = dept_str
                    s_list.s_recid = reslin_queasy._recid


    def check_do_it(inp_char:string, todate:date, done_flag:bool):

        nonlocal s_list_list, bediener, reslin_queasy, res_line
        nonlocal user_init, f_date, t_date, sorttype, alldept_flag


        nonlocal s_list
        nonlocal s_list_list

        do_it = True
        ci_flag = False
        dept_str = ""
        frdate = None
        curr_i:int = 0
        mesvalue:string = ""
        usrdept_str:string = ""

        def generate_inner_output():
            return (do_it, ci_flag, dept_str, frdate)


        if (sorttype == 1 and not done_flag) or (sorttype == 2 and done_flag):
            do_it = False

            return generate_inner_output()
        frdate = todate

        if num_entries(inp_char, chr_unicode(2)) <= 2:

            if frdate > t_date:
                do_it = False

            return generate_inner_output()
        for curr_i in range(3,num_entries(inp_char, chr_unicode(2))  + 1) :

            if curr_i == 3:
                mesvalue = entry(2, inp_char, chr_unicode(2))
                frdate = date_mdy(to_int(substring(mesvalue, 0, 2)) , to_int(substring(mesvalue, 2, 2)) , to_int(substring(mesvalue, 4)))

            elif curr_i == 4:
                dept_str = entry(3, inp_char, chr_unicode(2))

            elif curr_i == 5:
                mesvalue = entry(4, inp_char, chr_unicode(2))
                ci_flag = logical(to_int(mesvalue))

        if alldept_flag:

            return generate_inner_output()

        if dept_str == "":

            return generate_inner_output()
        usrdept_str = to_string(bediener.user_group) + ","

        if matches(dept_str,r"*," + usrdept_str + r"*"):

            return generate_inner_output()

        if substring(dept_str, 0, length((usrdept_str).lower() )) == (usrdept_str).lower() :

            return generate_inner_output()
        do_it = False

        return generate_inner_output()


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    create_list()

    return generate_output()