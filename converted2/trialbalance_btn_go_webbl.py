#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpchar import htpchar
from models import Gl_acct, Gl_jouhdr, Gl_journal, Gl_jhdrhis, Gl_jourhis, Gl_main, Htparam, Gl_accthis

def trialbalance_btn_go_webbl(acct_type:int, from_fibu:string, to_fibu:string, sorttype:int, from_dept:int, from_date:date, to_date:date, close_month:int, close_date:date, pnl_acct:string, close_year:date, prev_month:int, show_longbal:bool, pbal_flag:bool, asremoteflag:bool):

    prepare_cache ([Gl_acct, Gl_jouhdr, Gl_journal, Gl_jhdrhis, Gl_jourhis, Gl_main, Htparam, Gl_accthis])

    output_list_data = []
    num_acctype:int = 0
    sales:Decimal = to_decimal("0.0")
    cost:Decimal = to_decimal("0.0")
    gop_credit:Decimal = to_decimal("0.0")
    gop_debit:Decimal = to_decimal("0.0")
    tot_diff:Decimal = to_decimal("0.0")
    curr_i:int = 0
    in_procedure:bool = False
    numsend:int = 30
    last_acct_close_priod:date = None
    t_from_date:date = None
    t_to_date:date = None
    t_strgrp:string = ""
    t_str:string = ""
    t_int:int = 0
    t_date:date = None
    from_datehis:date = None
    to_datehis:date = None
    readflag:int = 0
    coa_format:string = ""
    counter:int = 0
    tt_pbal2:Decimal = to_decimal("0.0")
    gl_acct = gl_jouhdr = gl_journal = gl_jhdrhis = gl_jourhis = gl_main = htparam = gl_accthis = None

    output_list = output_listhis = result_list = t_res_list = t_res_listhis = g_list = g_listpre = g_listhis = None

    output_list_data, Output_list = create_model("Output_list", {"gop_flag":bool, "nr":int, "str":string, "budget":Decimal, "proz":Decimal, "mark":bool, "ch":string})
    output_listhis_data, Output_listhis = create_model("Output_listhis", {"gop_flag":bool, "nr":int, "str":string, "budget":Decimal, "proz":Decimal, "mark":bool, "ch":string})
    result_list_data, Result_list = create_model("Result_list", {"gop_flag":bool, "nr":int, "str":string, "budget":Decimal, "proz":Decimal, "mark":bool, "ch":string})
    t_res_list_data, T_res_list = create_model("T_res_list", {"grp_nr":string, "acc_no":string, "t_date":date, "f1":string, "f2":string, "f3":int, "f4":int, "f5":int, "f6":int, "f7":int, "f8":int, "f9":int, "f10":int, "note":string})
    t_res_listhis_data, T_res_listhis = create_model("T_res_listhis", {"grp_nr":string, "acc_no":string, "t_date":date, "f1":string, "f2":string, "f3":int, "f4":int, "f5":int, "f6":int, "f7":int, "f8":int, "f9":int, "f10":int, "note":string})
    g_list_data, G_list = create_model("G_list", {"datum":date, "grecid":int, "fibu":string}, {"datum": None})
    g_listpre_data, G_listpre = create_model("G_listpre", {"datum":date, "grecid":int, "fibu":string}, {"datum": None})
    g_listhis_data, G_listhis = create_model("G_listhis", {"datum":date, "grecid":int, "fibu":string}, {"datum": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        return {"output-list": output_list_data}

    def get_bemerk(bemerk:string):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1


    def lastday(d:date):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data


        return add_interval(date_mdy(get_month(d) , 1, get_year(d)) , 1, "month") - 1


    def create_glist():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

            for gl_journal in db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal.fibukonto >= (from_fibu).lower()) & (Gl_journal.fibukonto <= (to_fibu).lower())).order_by(Gl_journal.fibukonto).all():
                g_list = G_list()
                g_list_data.append(g_list)

                g_list.datum = gl_jouhdr.datum
                g_list.grecid = gl_journal._recid
                g_list.fibu = gl_journal.fibukonto


    def create_glisthis():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter(
                 (Gl_jhdrhis.datum >= from_datehis) & (Gl_jhdrhis.datum <= to_datehis)).order_by(Gl_jhdrhis.datum).all():

            for gl_jourhis in db_session.query(Gl_jourhis).filter(
                     (Gl_jourhis.jnr == gl_jhdrhis.jnr) & (Gl_jourhis.fibukonto >= (from_fibu).lower()) & (Gl_jourhis.fibukonto <= (to_fibu).lower())).order_by(Gl_jourhis.fibukonto).all():
                g_list = G_list()
                g_list_data.append(g_list)

                g_list.datum = gl_jhdrhis.datum
                g_list.grecid = gl_jourhis._recid
                g_list.fibu = gl_jourhis.fibukonto


    def create_list1():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        konto:string = ""
        i:int = 0
        c:string = ""
        ind:int = 0
        n:int = 0
        curr_month:int = 0
        do_it:bool = False
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        y_bal:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        prev_bal:Decimal = to_decimal("0.0")
        tot_bal:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        to_bal:Decimal = to_decimal("0.0")
        curr_tbal:Decimal = to_decimal("0.0")
        curr_totbal:Decimal = to_decimal("0.0")
        curr_ttbal:Decimal = to_decimal("0.0")
        curr_month = close_month
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")
        act_flag = 0

        if to_date <= date_mdy(get_month(close_date) , 1, get_year(close_date)) - 1:
            act_flag = 1
        output_list_data.clear()

        if sorttype == 1:

            if acct_type == 0:

                for gl_acct in db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower())).order_by(Gl_acct.fibukonto).all():
                    konto = gl_acct.fibukonto
                    do_it = True

                    if from_dept > 0 and gl_acct.deptnr != from_dept:
                        do_it = False

                    if do_it:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        counter = counter + 1
                        output_list.nr = counter


                        c = convert_fibu(gl_acct.fibukonto)
                        str = " " + to_string(c, "x(16)") + substring(gl_acct.bezeich, 0, 20)

                        if length(gl_acct.bezeich) > 20:
                            str = str + substring(gl_acct.bezeich, 20, 18)
                        t_debit =  to_decimal("0")
                        t_credit =  to_decimal("0")
                        p_bal =  to_decimal("0")
                        t_bal =  to_decimal("0")
                        curr_tbal =  to_decimal("0")
                        curr_totbal =  to_decimal("0")
                        curr_ttbal =  to_decimal("0")

                        if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:
                            p_bal, to_bal = calc_prevbalance(konto)
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
                            t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(p_bal) + to_decimal(to_bal)

                        for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto), sort_by=[("fibu",False),("datum",False)]):
                            pass
                            t_date = g_list.datum

                            if g_list.grecid != 0:

                                if t_date >= from_date and t_date <= to_date:

                                    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_journal:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        else:
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        output_list = Output_list()
                                        output_list_data.append(output_list)

                                        counter = counter + 1
                                        output_list.nr = counter


                                        str = to_string(gl_jouhdr.datum) + to_string(gl_jouhdr.refno, "x(16)")
                                        for i in range(1,22 + 1) :
                                            str = str + " "

                                        if gl_journal.debit >= 0:
                                            str = str + to_string(gl_journal.debit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_journal.debit, "->>,>>>,>>>,>>>,>>9.99")

                                        if gl_journal.credit >= 0:
                                            str = str + to_string(gl_journal.credit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_journal.credit, "->>,>>>,>>>,>>>,>>9.99")
                                        str = str + to_string("", "x(44) ") + to_string(get_bemerk (gl_journal.bemerk) , "x(62)")

                                if t_date >= from_datehis and t_date <= to_datehis:

                                    gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_jourhis:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_jourhis.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_jourhis.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_jourhis.credit) - to_decimal(gl_jourhis.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        else:
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        output_list = Output_list()
                                        output_list_data.append(output_list)

                                        counter = counter + 1
                                        output_list.nr = counter


                                        str = to_string(gl_jhdrhis.datum) + to_string(gl_jhdrhis.refno, "x(13)")
                                        for i in range(1,22 + 1) :
                                            str = str + " "

                                        if gl_jourhis.debit >= 0:
                                            str = str + to_string(gl_jourhis.debit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_jourhis.debit, "->>,>>>,>>>,>>>,>>9.99")

                                        if gl_jourhis.credit >= 0:
                                            str = str + to_string(gl_jourhis.credit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_jourhis.credit, "->>,>>>,>>>,>>>,>>9.99")
                                        str = str + to_string("", "x(44)") + to_string(get_bemerk (gl_jourhis.bemerk) , "x(62)")
                        p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                        if gl_acct.acc_type != 3 and gl_acct.acc_type != 4:
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

                        if p_bal != 0 or t_debit != 0 or t_credit != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            counter = counter + 1
                            output_list.nr = counter


                            str = " " + "T O T A L "
                            c = convert_balance(p_bal)
                            str = str + to_string(c, "x(22)")

                            if t_debit >= 0:
                                str = str + to_string(t_debit, ">>>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                            if t_credit >= 0:
                                str = str + to_string(t_credit, ">>>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                            if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                diff =  to_decimal(t_credit) - to_decimal(t_debit)
                                tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                            else:
                                diff =  to_decimal(t_debit) - to_decimal(t_credit)
                                tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                            c = convert_balance(diff)
                            str = str + to_string(c, "x(22)")
                            c = convert_balance(t_bal)
                            str = str + to_string(c, "x(22)")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            counter = counter + 1
                            output_list.nr = counter


                        else:
                            output_list_data.remove(output_list)

            elif acct_type != 0:

                for gl_acct in db_session.query(Gl_acct).filter(
                         (Gl_acct.acc_type == to_int(acct_type)) & (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower())).order_by(Gl_acct.fibukonto).all():
                    konto = gl_acct.fibukonto
                    do_it = True

                    if from_dept > 0 and gl_acct.deptnr != from_dept:
                        do_it = False

                    if do_it:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        counter = counter + 1
                        output_list.nr = counter


                        c = convert_fibu(gl_acct.fibukonto)
                        str = " " + to_string(c, "x(16)") + substring(gl_acct.bezeich, 0, 20)

                        if length(gl_acct.bezeich) > 20:
                            str = str + substring(gl_acct.bezeich, 20, 18)
                        t_debit =  to_decimal("0")
                        t_credit =  to_decimal("0")
                        p_bal =  to_decimal("0")
                        t_bal =  to_decimal("0")
                        curr_tbal =  to_decimal("0")
                        curr_totbal =  to_decimal("0")
                        curr_ttbal =  to_decimal("0")

                        if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:
                            p_bal, to_bal = calc_prevbalance(konto)
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
                            t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(t_bal) + to_decimal(to_bal)

                        for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto), sort_by=[("fibu",False),("datum",False)]):
                            pass
                            t_date = g_list.datum

                            if g_list.grecid != 0:

                                if t_date >= from_date and t_date <= to_date:

                                    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_journal:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        else:
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        output_list = Output_list()
                                        output_list_data.append(output_list)

                                        counter = counter + 1
                                        output_list.nr = counter


                                        str = to_string(gl_jouhdr.datum) + to_string(gl_jouhdr.refno, "x(16)")
                                        for i in range(1,22 + 1) :
                                            str = str + " "

                                        if gl_journal.debit >= 0:
                                            str = str + to_string(gl_journal.debit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_journal.debit, "->>,>>>,>>>,>>>,>>9.99")

                                        if gl_journal.credit >= 0:
                                            str = str + to_string(gl_journal.credit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_journal.credit, "->>,>>>,>>>,>>>,>>9.99")
                                        str = str + to_string("", "x(44) ") + to_string(get_bemerk (gl_journal.bemerk) , "x(62)")

                                if t_date >= from_datehis and t_date <= to_datehis:

                                    gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_jourhis:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_jourhis.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_jourhis.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_jourhis.credit) - to_decimal(gl_jourhis.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        else:
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        output_list = Output_list()
                                        output_list_data.append(output_list)

                                        counter = counter + 1
                                        output_list.nr = counter


                                        str = to_string(gl_jhdrhis.datum) + to_string(gl_jhdrhis.refno, "x(13)")
                                        for i in range(1,22 + 1) :
                                            str = str + " "

                                        if gl_jourhis.debit >= 0:
                                            str = str + to_string(gl_jourhis.debit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_jourhis.debit, "->>,>>>,>>>,>>>,>>9.99")

                                        if gl_jourhis.credit >= 0:
                                            str = str + to_string(gl_jourhis.credit, ">>>,>>>,>>>,>>>,>>9.99")
                                        else:
                                            str = str + to_string(gl_jourhis.credit, "->>,>>>,>>>,>>>,>>9.99")
                                        str = str + to_string("", "x(44)") + to_string(get_bemerk (gl_jourhis.bemerk) , "x(62)")
                        p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                        if gl_acct.acc_type != 3 and gl_acct.acc_type != 4:
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

                        if p_bal != 0 or t_debit != 0 or t_credit != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            counter = counter + 1
                            output_list.nr = counter


                            str = " " + "T O T A L "
                            c = convert_balance(p_bal)
                            str = str + to_string(c, "x(22)")

                            if t_debit >= 0:
                                str = str + to_string(t_debit, ">>>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                            if t_credit >= 0:
                                str = str + to_string(t_credit, ">>>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                            if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                diff =  to_decimal(t_credit) - to_decimal(t_debit)
                                tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                            else:
                                diff =  to_decimal(t_debit) - to_decimal(t_credit)
                                tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                            c = convert_balance(diff)
                            str = str + to_string(c, "x(22)")
                            c = convert_balance(t_bal)
                            str = str + to_string(c, "x(22)")
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            counter = counter + 1
                            output_list.nr = counter


                        else:
                            output_list_data.remove(output_list)

            if prev_bal != 0 or tot_debit != 0 or tot_credit != 0:
                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter


                str = " " + "Grand TOTAL "
                c = convert_balance(prev_bal)
                str = str + to_string(c, "x(22)")

                if tot_debit >= 0:
                    str = str + to_string(tot_debit, ">>>,>>>,>>>,>>>,>>9.99")
                else:
                    str = str + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")

                if tot_credit >= 0:
                    str = str + to_string(tot_credit, ">>>,>>>,>>>,>>>,>>9.99")
                else:
                    str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                c = convert_balance(tot_diff)
                str = str + to_string(c, "x(22)")
                c = convert_balance(tot_bal)
                str = str + to_string(c, "x(22)")

            if to_date == close_date:
                prof_loss_acct11()


    def create_list2():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        konto:string = ""
        i:int = 0
        c:string = ""
        ind:int = 0
        curr_month:int = 0
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        y_bal:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        t_ybal:Decimal = to_decimal("0.0")
        tt_ybal:Decimal = to_decimal("0.0")
        prev_bal:Decimal = to_decimal("0.0")
        tot_bal:Decimal = to_decimal("0.0")
        tot_budget:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        tt_debit:Decimal = to_decimal("0.0")
        tt_credit:Decimal = to_decimal("0.0")
        tt_pbal:Decimal = to_decimal("0.0")
        tt_bal:Decimal = to_decimal("0.0")
        tt_diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        n:int = 0
        to_bal:Decimal = to_decimal("0.0")
        curr_tbal:Decimal = to_decimal("0.0")
        curr_totbal:Decimal = to_decimal("0.0")
        curr_ttbal:Decimal = to_decimal("0.0")
        gl_account = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        in_procedure = True
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")
        act_flag = 0

        if to_date <= date_mdy(get_month(close_date) , 1, get_year(close_date)) - 1:
            act_flag = 1
        output_list_data.clear()
        curr_month = close_month

        if sorttype == 2:

            if acct_type == 0:

                gl_main_obj_list = {}
                gl_main = Gl_main()
                gl_account = Gl_acct()
                for gl_main.code, gl_main.bezeich, gl_main.nr, gl_main._recid, gl_account.fibukonto, gl_account.bezeich, gl_account.acc_type, gl_account.budget, gl_account.ly_budget, gl_account.actual, gl_account.last_yr, gl_account.deptnr, gl_account._recid in db_session.query(Gl_main.code, Gl_main.bezeich, Gl_main.nr, Gl_main._recid, Gl_account.fibukonto, Gl_account.bezeich, Gl_account.acc_type, Gl_account.budget, Gl_account.ly_budget, Gl_account.actual, Gl_account.last_yr, Gl_account.deptnr, Gl_account._recid).join(Gl_account,(Gl_account.main_nr == Gl_main.nr) & (Gl_account.fibukonto >= (from_fibu).lower()) & (Gl_account.fibukonto <= (to_fibu).lower())).order_by(Gl_main.code).all():
                    if gl_main_obj_list.get(gl_main._recid):
                        continue
                    else:
                        gl_main_obj_list[gl_main._recid] = True


                    prev_bal =  to_decimal("0")
                    tot_debit =  to_decimal("0")
                    tot_credit =  to_decimal("0")
                    t_ybal =  to_decimal("0")
                    tot_bal =  to_decimal("0")
                    tot_budget =  to_decimal("0")
                    diff =  to_decimal("0")
                    tot_diff =  to_decimal("0")
                    curr_tbal =  to_decimal("0")
                    curr_totbal =  to_decimal("0")
                    curr_ttbal =  to_decimal("0")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter


                    str = to_string(to_string(gl_main.code) , "x(16)") + substring(gl_main.bezeich, 0, 38)

                    for gl_acct in db_session.query(Gl_acct).filter(
                             (Gl_acct.main_nr == gl_main.nr) & (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower())).order_by(Gl_acct.fibukonto).all():
                        konto = gl_acct.fibukonto
                        t_debit =  to_decimal("0")
                        t_credit =  to_decimal("0")
                        p_bal =  to_decimal("0")
                        t_bal =  to_decimal("0")
                        y_bal =  to_decimal("0")

                        if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:
                            p_bal, to_bal = calc_prevbalance(konto)
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
                            t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(p_bal) + to_decimal(to_bal)


                            tt_pbal =  to_decimal(tt_pbal) + to_decimal(p_bal)
                            tt_bal =  to_decimal(tt_bal) + to_decimal(p_bal) + to_decimal(to_bal)

                        for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):
                            t_date = g_list.datum
                            pass

                            if g_list.grecid != 0:

                                if t_date >= from_datehis and t_date <= to_datehis:

                                    gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_jourhis:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_jourhis.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_jourhis.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_jourhis.credit) - to_decimal(gl_jourhis.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                                        tt_debit =  to_decimal(tt_debit) + to_decimal(gl_jourhis.debit)
                                        tt_credit =  to_decimal(tt_credit) + to_decimal(gl_jourhis.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                            tt_bal =  to_decimal(tt_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                            tt_bal =  to_decimal(tt_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

                                elif t_date >= from_date and t_date <= to_date:

                                    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_journal:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
                                        tt_debit =  to_decimal(tt_debit) + to_decimal(gl_journal.debit)
                                        tt_credit =  to_decimal(tt_credit) + to_decimal(gl_journal.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                            tt_bal =  to_decimal(tt_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                            tt_bal =  to_decimal(tt_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                        if gl_acct.acc_type != 3 and gl_acct.acc_type != 4:
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

                        if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            counter = counter + 1
                            output_list.nr = counter


                            c = convert_fibu(gl_acct.fibukonto)
                            str = to_string(c, "x(16)") + to_string(gl_acct.bezeich, "x(38)")
                            c = convert_balance(p_bal)

                            if t_debit >= 0:
                                str = str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                            if t_credit >= 0:
                                str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                            if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                diff =  - to_decimal(t_debit) + to_decimal(t_credit)
                                tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                                tt_diff =  to_decimal(tt_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                            else:
                                diff =  to_decimal(t_debit) - to_decimal(t_credit)
                                tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                                tt_diff =  to_decimal(tt_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                            c = convert_balance(diff)
                            str = str + to_string(c, "x(22)")
                            c = convert_balance(t_bal)
                            str = str + to_string(c, "x(22)")
                            c = convert_balance(y_bal)
                            str = str + to_string(c, "x(22)")
                            t_ybal =  to_decimal(t_ybal) + to_decimal(y_bal)
                            tt_ybal =  to_decimal(tt_ybal) + to_decimal(y_bal)

                            if get_year(close_year) == get_year(to_date):

                                if gl_acct.acc_type == 1:
                                    output_list.budget =  - to_decimal(gl_acct.budget[get_month(to_date) - 1])

                                elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                    output_list.budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])

                            elif get_year(close_year) == get_year(to_date) + 1:

                                if gl_acct.acc_type == 1:
                                    output_list.budget =  - to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])

                                elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                    output_list.budget =  to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])
                            tot_budget =  to_decimal(tot_budget) + to_decimal(output_list.budget)

                            if output_list.budget != 0:
                                output_list.proz =  to_decimal(t_bal) / to_decimal(output_list.budget) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter


                    str = " " + to_string("s U B T O T A L", "x(38)")
                    c = convert_balance(prev_bal)
                    tt_pbal2 =  to_decimal(tt_pbal2) + to_decimal(prev_bal)

                    if tot_debit >= 0:
                        str = str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                    else:
                        str = str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")

                    if tot_credit >= 0:
                        str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    else:
                        str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    c = convert_balance(tot_diff)
                    str = str + to_string(c, "x(22)")
                    c = convert_balance(tot_bal)
                    str = str + to_string(c, "x(22)")
                    c = convert_balance(t_ybal)
                    str = str + to_string(c, "x(22)")
                    output_list.budget =  to_decimal(tot_budget)

                    if output_list.budget != 0:
                        output_list.proz =  to_decimal(tot_bal) / to_decimal(output_list.budget) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter


            else:

                gl_main_obj_list = {}
                gl_main = Gl_main()
                gl_account = Gl_acct()
                for gl_main.code, gl_main.bezeich, gl_main.nr, gl_main._recid, gl_account.fibukonto, gl_account.bezeich, gl_account.acc_type, gl_account.budget, gl_account.ly_budget, gl_account.actual, gl_account.last_yr, gl_account.deptnr, gl_account._recid in db_session.query(Gl_main.code, Gl_main.bezeich, Gl_main.nr, Gl_main._recid, Gl_account.fibukonto, Gl_account.bezeich, Gl_account.acc_type, Gl_account.budget, Gl_account.ly_budget, Gl_account.actual, Gl_account.last_yr, Gl_account.deptnr, Gl_account._recid).join(Gl_account,(Gl_account.acc_type == acct_type) & (Gl_account.main_nr == Gl_main.nr) & (Gl_account.fibukonto >= (from_fibu).lower()) & (Gl_account.fibukonto <= (to_fibu).lower())).order_by(Gl_main.code).all():
                    if gl_main_obj_list.get(gl_main._recid):
                        continue
                    else:
                        gl_main_obj_list[gl_main._recid] = True


                    prev_bal =  to_decimal("0")
                    tot_debit =  to_decimal("0")
                    tot_credit =  to_decimal("0")
                    t_ybal =  to_decimal("0")
                    tot_bal =  to_decimal("0")
                    tot_budget =  to_decimal("0")
                    diff =  to_decimal("0")
                    tot_diff =  to_decimal("0")
                    curr_tbal =  to_decimal("0")
                    curr_totbal =  to_decimal("0")
                    curr_ttbal =  to_decimal("0")


                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter


                    str = to_string(to_string(gl_main.code) , "x(16)") + substring(gl_main.bezeich, 0, 38)

                    for gl_acct in db_session.query(Gl_acct).filter(
                             (Gl_acct.acc_type == acct_type) & (Gl_acct.main_nr == gl_main.nr) & (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower())).order_by(Gl_acct.fibukonto).all():
                        konto = gl_acct.fibukonto
                        t_debit =  to_decimal("0")
                        t_credit =  to_decimal("0")
                        p_bal =  to_decimal("0")
                        t_bal =  to_decimal("0")
                        y_bal =  to_decimal("0")

                        if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:
                            p_bal, to_bal = calc_prevbalance(konto)
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
                            t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(p_bal) + to_decimal(to_bal)


                            tt_pbal =  to_decimal(tt_pbal) + to_decimal(p_bal)
                            tt_bal =  to_decimal(tt_bal) + to_decimal(p_bal) + to_decimal(to_bal)

                        for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):
                            t_date = g_list.datum
                            pass

                            if g_list.grecid != 0:

                                if t_date >= from_datehis and t_date <= to_datehis:

                                    gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_jourhis:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_jourhis.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_jourhis.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_jourhis.credit) - to_decimal(gl_jourhis.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                                        tt_debit =  to_decimal(tt_debit) + to_decimal(gl_jourhis.debit)
                                        tt_credit =  to_decimal(tt_credit) + to_decimal(gl_jourhis.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                            tt_bal =  to_decimal(tt_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                            tt_bal =  to_decimal(tt_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

                                elif t_date >= from_date and t_date <= to_date:

                                    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                                    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                                    g_list_data.remove(g_list)

                                    if gl_journal:

                                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                                        if gl_acct.acc_type == 1:
                                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
                                        tt_debit =  to_decimal(tt_debit) + to_decimal(gl_journal.debit)
                                        tt_credit =  to_decimal(tt_credit) + to_decimal(gl_journal.credit)

                                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                            tt_bal =  to_decimal(tt_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        else:
                                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                            tt_bal =  to_decimal(tt_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                        if gl_acct.acc_type != 3 and gl_acct.acc_type != 4:
                            prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

                        if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            counter = counter + 1
                            output_list.nr = counter


                            c = convert_fibu(gl_acct.fibukonto)
                            str = to_string(c, "x(16)") + to_string(gl_acct.bezeich, "x(38)")
                            c = convert_balance(p_bal)

                            if t_debit >= 0:
                                str = str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                            if t_credit >= 0:
                                str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                            else:
                                str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                            if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                diff =  - to_decimal(t_debit) + to_decimal(t_credit)
                                tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                                tt_diff =  to_decimal(tt_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                            else:
                                diff =  to_decimal(t_debit) - to_decimal(t_credit)
                                tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                                tt_diff =  to_decimal(tt_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                            c = convert_balance(diff)
                            str = str + to_string(c, "x(22)")
                            c = convert_balance(t_bal)
                            str = str + to_string(c, "x(22)")
                            c = convert_balance(y_bal)
                            str = str + to_string(c, "x(22)")
                            t_ybal =  to_decimal(t_ybal) + to_decimal(y_bal)
                            tt_ybal =  to_decimal(tt_ybal) + to_decimal(y_bal)

                            if get_year(close_year) == get_year(to_date):

                                if gl_acct.acc_type == 1:
                                    output_list.budget =  - to_decimal(gl_acct.budget[get_month(to_date) - 1])

                                elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                    output_list.budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])

                            elif get_year(close_year) == get_year(to_date) + 1:

                                if gl_acct.acc_type == 1:
                                    output_list.budget =  - to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])

                                elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                    output_list.budget =  to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])
                            tot_budget =  to_decimal(tot_budget) + to_decimal(output_list.budget)

                            if output_list.budget != 0:
                                output_list.proz =  to_decimal(t_bal) / to_decimal(output_list.budget) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter


                    str = " " + to_string("s U B T O T A L", "x(38)")
                    c = convert_balance(prev_bal)
                    tt_pbal2 =  to_decimal(tt_pbal2) + to_decimal(prev_bal)

                    if tot_debit >= 0:
                        str = str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                    else:
                        str = str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")

                    if tot_credit >= 0:
                        str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    else:
                        str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    c = convert_balance(tot_diff)
                    str = str + to_string(c, "x(22)")
                    c = convert_balance(tot_bal)
                    str = str + to_string(c, "x(22)")
                    c = convert_balance(t_ybal)
                    str = str + to_string(c, "x(22)")
                    output_list.budget =  to_decimal(tot_budget)

                    if output_list.budget != 0:
                        output_list.proz =  to_decimal(tot_bal) / to_decimal(output_list.budget) * to_decimal("100")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            str = " " + to_string("T O T A L", "x(38)")
            c = convert_balance(tt_pbal2)

            if tt_debit >= 0:
                str = str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")

            if tt_credit >= 0:
                str = str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            c = convert_balance(tt_diff)
            str = str + to_string(c, "x(22)")
            c = convert_balance(tt_bal)
            str = str + to_string(c, "x(22)")

        if from_dept == 0:
            prof_loss_acct21()


    def create_list2d():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        konto:string = ""
        i:int = 0
        c:string = ""
        ind:int = 0
        curr_month:int = 0
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        y_bal:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        t_ybal:Decimal = to_decimal("0.0")
        tt_ybal:Decimal = to_decimal("0.0")
        prev_bal:Decimal = to_decimal("0.0")
        tot_bal:Decimal = to_decimal("0.0")
        tot_budget:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        tt_debit:Decimal = to_decimal("0.0")
        tt_credit:Decimal = to_decimal("0.0")
        tt_pbal:Decimal = to_decimal("0.0")
        tt_bal:Decimal = to_decimal("0.0")
        tt_diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        n:int = 0
        to_bal:Decimal = to_decimal("0.0")
        curr_tbal:Decimal = to_decimal("0.0")
        curr_totbal:Decimal = to_decimal("0.0")
        curr_ttbal:Decimal = to_decimal("0.0")
        gl_account = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        in_procedure = True
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")
        act_flag = 0

        if to_date <= date_mdy(get_month(close_date) , 1, get_year(close_date)) - 1:
            act_flag = 1
        output_list_data.clear()
        curr_month = close_month

        if sorttype == 2:

            gl_main_obj_list = {}
            gl_main = Gl_main()
            gl_account = Gl_acct()
            for gl_main.code, gl_main.bezeich, gl_main.nr, gl_main._recid, gl_account.fibukonto, gl_account.bezeich, gl_account.acc_type, gl_account.budget, gl_account.ly_budget, gl_account.actual, gl_account.last_yr, gl_account.deptnr, gl_account._recid in db_session.query(Gl_main.code, Gl_main.bezeich, Gl_main.nr, Gl_main._recid, Gl_account.fibukonto, Gl_account.bezeich, Gl_account.acc_type, Gl_account.budget, Gl_account.ly_budget, Gl_account.actual, Gl_account.last_yr, Gl_account.deptnr, Gl_account._recid).join(Gl_account,(Gl_account.main_nr == Gl_main.nr) & (Gl_account.fibukonto >= (from_fibu).lower()) & (Gl_account.fibukonto <= (to_fibu).lower()) & (Gl_account.deptnr == from_dept)).order_by(Gl_main.code).all():
                if gl_main_obj_list.get(gl_main._recid):
                    continue
                else:
                    gl_main_obj_list[gl_main._recid] = True


                prev_bal =  to_decimal("0")
                tot_debit =  to_decimal("0")
                tot_credit =  to_decimal("0")
                t_ybal =  to_decimal("0")
                tot_bal =  to_decimal("0")
                tot_budget =  to_decimal("0")
                diff =  to_decimal("0")
                tot_diff =  to_decimal("0")
                curr_tbal =  to_decimal("0")
                curr_totbal =  to_decimal("0")
                curr_ttbal =  to_decimal("0")


                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter


                str = to_string(to_string(gl_main.code) , "x(16)") + substring(gl_main.bezeich, 0, 38)

                for gl_acct in db_session.query(Gl_acct).filter(
                         (Gl_acct.main_nr == gl_main.nr) & (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower()) & (Gl_acct.deptnr == from_dept)).order_by(Gl_acct.fibukonto).all():
                    konto = gl_acct.fibukonto
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    p_bal =  to_decimal("0")
                    t_bal =  to_decimal("0")
                    y_bal =  to_decimal("0")

                    if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:
                        p_bal, to_bal = calc_prevbalance(konto)
                        prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
                        t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(p_bal) + to_decimal(to_bal)


                        tt_pbal =  to_decimal(tt_pbal) + to_decimal(p_bal)
                        tt_bal =  to_decimal(tt_bal) + to_decimal(p_bal) + to_decimal(to_bal)

                    for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):
                        t_date = g_list.datum
                        pass

                        if g_list.grecid != 0:

                            if t_date >= from_datehis and t_date <= to_datehis:

                                gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                                gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                                g_list_data.remove(g_list)

                                if gl_jourhis:

                                    if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                        gop_credit =  to_decimal(gop_credit) + to_decimal(gl_jourhis.credit)
                                        gop_debit =  to_decimal(gop_debit) + to_decimal(gl_jourhis.debit)

                                    if gl_acct.acc_type == 1:
                                        sales =  to_decimal(sales) + to_decimal(gl_jourhis.credit) - to_decimal(gl_jourhis.debit)

                                    elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                        cost =  to_decimal(cost) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                    t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
                                    t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
                                    tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
                                    tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
                                    tt_debit =  to_decimal(tt_debit) + to_decimal(gl_jourhis.debit)
                                    tt_credit =  to_decimal(tt_credit) + to_decimal(gl_jourhis.credit)

                                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                        t_bal =  to_decimal(t_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        tot_bal =  to_decimal(tot_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                        tt_bal =  to_decimal(tt_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
                                    else:
                                        t_bal =  to_decimal(t_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        tot_bal =  to_decimal(tot_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
                                        tt_bal =  to_decimal(tt_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

                            elif t_date >= from_date and t_date <= to_date:

                                gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                                gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                                g_list_data.remove(g_list)

                                if gl_journal:

                                    if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                                        gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                                        gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                                    if gl_acct.acc_type == 1:
                                        sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                                    elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                        cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                    t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                                    t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                                    tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                                    tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
                                    tt_debit =  to_decimal(tt_debit) + to_decimal(gl_journal.debit)
                                    tt_credit =  to_decimal(tt_credit) + to_decimal(gl_journal.credit)

                                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                                        t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                        tt_bal =  to_decimal(tt_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                                    else:
                                        t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                                        tt_bal =  to_decimal(tt_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                    p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                    if gl_acct.acc_type != 3 and gl_acct.acc_type != 4:
                        prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

                    if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        counter = counter + 1
                        output_list.nr = counter


                        c = convert_fibu(gl_acct.fibukonto)
                        str = to_string(c, "x(16)") + to_string(gl_acct.bezeich, "x(38)")
                        c = convert_balance(p_bal)

                        if t_debit >= 0:
                            str = str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                        else:
                            str = str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                        if t_credit >= 0:
                            str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                        else:
                            str = str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff =  - to_decimal(t_debit) + to_decimal(t_credit)
                            tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                            tt_diff =  to_decimal(tt_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                        else:
                            diff =  to_decimal(t_debit) - to_decimal(t_credit)
                            tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                            tt_diff =  to_decimal(tt_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                        c = convert_balance(diff)
                        str = str + to_string(c, "x(22)")
                        c = convert_balance(t_bal)
                        str = str + to_string(c, "x(22)")
                        c = convert_balance(y_bal)
                        str = str + to_string(c, "x(22)")
                        t_ybal =  to_decimal(t_ybal) + to_decimal(y_bal)
                        tt_ybal =  to_decimal(tt_ybal) + to_decimal(y_bal)

                        if get_year(close_year) == get_year(to_date):

                            if gl_acct.acc_type == 1:
                                output_list.budget =  - to_decimal(gl_acct.budget[get_month(to_date) - 1])

                            elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                output_list.budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])

                        elif get_year(close_year) == get_year(to_date) + 1:

                            if gl_acct.acc_type == 1:
                                output_list.budget =  - to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])

                            elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                                output_list.budget =  to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])
                        tot_budget =  to_decimal(tot_budget) + to_decimal(output_list.budget)

                        if output_list.budget != 0:
                            output_list.proz =  to_decimal(t_bal) / to_decimal(output_list.budget) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter


                str = " " + to_string("s U B T O T A L", "x(38)")
                c = convert_balance(prev_bal)

                if tot_debit >= 0:
                    str = str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                else:
                    str = str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")

                if tot_credit >= 0:
                    str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                else:
                    str = str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                c = convert_balance(tot_diff)
                str = str + to_string(c, "x(22)")
                c = convert_balance(tot_bal)
                str = str + to_string(c, "x(22)")
                c = convert_balance(t_ybal)
                str = str + to_string(c, "x(22)")
                output_list.budget =  to_decimal(tot_budget)

                if output_list.budget != 0:
                    output_list.proz =  to_decimal(tot_bal) / to_decimal(output_list.budget) * to_decimal("100")
                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            str = " " + to_string("T O T A L", "x(38)")
            c = convert_balance(tt_pbal)

            if tt_debit >= 0:
                str = str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")

            if tt_credit >= 0:
                str = str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            c = convert_balance(tt_diff)
            str = str + to_string(c, "x(22)")
            c = convert_balance(tt_bal)
            str = str + to_string(c, "x(22)")


    def convert_fibu(konto:string):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()


    def calc_prevbalance(fibu:string):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        p_bal = to_decimal("0.0")
        to_bal = to_decimal("0.0")
        gbuff = None

        def generate_inner_output():
            return (p_bal, to_bal)

        Gbuff =  create_buffer("Gbuff",Gl_acct)

        gbuff = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})

        if gbuff.acc_type != 3 and gbuff.acc_type != 4:

            return generate_inner_output()

        if get_year(close_year) == get_year(t_from_date) and get_month(t_from_date) >= 2:
            p_bal =  to_decimal(gbuff.actual[prev_month - 1])


        else:

            if get_month(t_from_date) >= 2:

                gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, fibu)],"year": [(eq, get_year(t_from_date))]})
            else:

                gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, fibu)],"year": [(eq, get_year(t_from_date) - 1)]})

            if gl_accthis:
                p_bal =  to_decimal(gl_accthis.actual[prev_month - 1])

        if gbuff.acc_type == 4:
            p_bal =  -1 * to_decimal(p_bal)

        if p_bal != 0:

            return generate_inner_output()

        if get_day(t_to_date + 1) != 1:

            return generate_inner_output()

        g_list = query(g_list_data, filters=(lambda g_list: g_list.fibu.lower()  == (fibu).lower()), first=True)

        if g_list:

            return generate_inner_output()

        if get_year(t_to_date) == get_year(close_date):
            to_bal =  to_decimal(gbuff.actual[get_month(t_to_date) - 1])
        else:

            gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, fibu)],"year": [(eq, get_year(t_to_date))]})

            if gl_accthis:
                to_bal =  to_decimal(gl_accthis.actual[get_month(t_to_date) - 1])

        if gbuff.acc_type == 4:
            to_bal =  -1 * to_decimal(to_bal)

        return generate_inner_output()


    def convert_balance(balance:Decimal):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        if balance >= 0:

            if not show_longbal:
                s = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            else:
                s = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
        else:
            balance =  - to_decimal(balance)

            if balance >= 0:

                if not show_longbal:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
                else:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
            else:

                if not show_longbal:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
                else:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
            s = "(" + ch + ")"
            for i in range(1,20 - length(ch)  + 1) :
                s = " " + s

        return generate_inner_output()


    def prof_loss_acct11():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        m:int = 0
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        c:string = ""

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, pnl_acct)]})

        if gl_acct:

            if get_year(close_year) == get_year(t_to_date):
                m = close_month - 1

                if m >= 1:
                    p_bal =  - to_decimal(gl_acct.actual[m - 1])
                else:
                    p_bal =  - to_decimal(gl_acct.last_yr[11])

            elif get_year(close_year) == (get_year(t_to_date) + 1):
                m = close_month - 1

                if m >= 1:
                    p_bal =  - to_decimal(gl_acct.last_yr[m - 1])
            t_bal =  to_decimal(p_bal) + to_decimal(sales) - to_decimal(cost) + to_decimal(gop_credit) - to_decimal(gop_debit)
            diff =  to_decimal(gop_credit) + to_decimal(sales) - to_decimal(gop_debit) - to_decimal(cost)
            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            str = " " + "Expected GOP "
            c = convert_balance(p_bal)
            str = str + to_string(c, "x(22)")

            if (gop_credit + sales) >= 0:
                str = str + to_string((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99") + to_string((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99") + to_string((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            c = convert_balance(diff)
            str = str + to_string(c, "x(22)")
            c = convert_balance(t_bal)
            str = str + to_string(c, "x(22)")


    def calcrevcost(t_bal:Decimal, p_bal:Decimal, y_bal:Decimal):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        p_sign:int = 1
        n:int = 0

        def generate_inner_output():
            return (p_bal, y_bal)


        if gl_acct.acc_typ == 3 or gl_acct.acc_type == 4:
            y_bal =  to_decimal(t_bal)

            return generate_inner_output()

        if gl_acct.acc_type == 1:
            p_sign = -1

        if pbal_flag and get_month(from_date) > 1:

            if get_year(close_year) == get_year(from_date):
                for n in range(1,get_month(from_date) - 1 + 1) :
                    p_bal =  to_decimal(p_bal) + to_decimal(p_sign) * to_decimal(gl_acct.actual[n - 1])
            else:

                gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, gl_acct.fibukonto)],"year": [(eq, get_year(from_date))]})

                if gl_accthis:
                    for n in range(1,get_month(from_date) - 1 + 1) :
                        p_bal =  to_decimal(p_bal) + to_decimal(p_sign) * to_decimal(gl_accthis.actual[n - 1])

        if get_year(close_year) == get_year(from_date):
            for n in range(1,get_month(to_date)  + 1) :
                y_bal =  to_decimal(y_bal) + to_decimal(p_sign) * to_decimal(gl_acct.actual[n - 1])
        else:

            gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, gl_acct.fibukonto)],"year": [(eq, get_year(from_date))]})

            if gl_accthis:
                for n in range(1,get_month(to_date)  + 1) :
                    y_bal =  to_decimal(y_bal) + to_decimal(p_sign) * to_decimal(gl_accthis.actual[n - 1])

        return generate_inner_output()


    def prof_loss_acct21():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        m:int = 0
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        c:string = ""
        hbuff = None
        Hbuff =  create_buffer("Hbuff",Gl_accthis)

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, pnl_acct)]})

        if gl_acct:

            gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, pnl_acct)],"year": [(eq, (get_year(t_to_date) - 1))]})

            if get_year(close_year) == get_year(t_to_date):
                m = close_month - 1

                if m >= 1:
                    p_bal =  - to_decimal(gl_acct.actual[m - 1])
                else:

                    if gl_accthis:
                        p_bal =  - to_decimal(gl_accthis.actual[11])
                    else:
                        p_bal =  - to_decimal(gl_acct.last_yr[11])
            else:

                hbuff = get_cache (Gl_accthis, {"fibukonto": [(eq, pnl_acct)],"year": [(eq, get_year(t_to_date))]})

                if hbuff:
                    m = close_month - 1

                    if m >= 1:
                        p_bal =  - to_decimal(hbuff.actual[m - 1])
                    else:

                        if gl_accthis:
                            p_bal =  - to_decimal(gl_accthis.actual[11])
                        else:
                            p_bal =  - to_decimal(hbuff.last_yr[11])
            t_bal =  to_decimal(p_bal) + to_decimal(sales) - to_decimal(cost) + to_decimal(gop_credit) - to_decimal(gop_debit)
            diff =  to_decimal(gop_credit) + to_decimal(sales) - to_decimal(gop_debit) - to_decimal(cost)
            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            str = " " + to_string("balance - " + gl_acct.bezeich, "x(38)")
            c = convert_balance(p_bal)
            str = str + to_string(c, "x(22)")

            if (gop_debit + cost) >= 0:
                str = str + to_string((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99")

            if (gop_credit + sales) >= 0:
                str = str + to_string((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            else:
                str = str + to_string((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            c = convert_balance(diff)
            str = str + to_string(c, "x(22)")
            c = convert_balance(t_bal)
            str = str + to_string(c, "x(22)")
            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


    def sendnextrecords():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        def generate_inner_output():
            return (result_list_data)

        result_list_data.clear()
        curr_i = 1

        output_list = query(output_list_data, next=True)
        while None != output_list and curr_i <= numsend:
            result_list = Result_list()
            result_list_data.append(result_list)

            buffer_copy(output_list, result_list)
            curr_i = curr_i + 1

            if curr_i <= numsend:

                output_list = query(output_list_data, next=True)

        return generate_inner_output()


    def delete_procedure():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

    last_acct_close_priod = get_output(htpdate(795))
    coa_format = get_output(htpchar(977))
    num_acctype = 0

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower()) & ((Gl_acct.acc_type == 1) | (Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 5))).first()

    if gl_acct:
        num_acctype = 1

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(ge, from_fibu),(le, to_fibu)],"acc_type": [(eq, 3)]})

    if gl_acct:
        num_acctype = num_acctype + 1

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(ge, from_fibu),(le, to_fibu)],"acc_type": [(eq, 4)]})

    if gl_acct:
        num_acctype = num_acctype + 1
    t_from_date = from_date
    t_to_date = to_date
    from_date = None
    t_date = None


    g_list_data.clear()

    gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, lastday (t_from_date))]})

    if gl_jouhdr:
        from_date = t_from_date
        to_date = t_to_date


        create_glist()
    else:

        gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, t_to_date)]})

        if gl_jouhdr:
            for t_date in date_range(t_from_date,t_to_date) :

                gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, t_date)]})

                if gl_jouhdr:
                    from_datehis = t_from_date
                    to_datehis = t_date - timedelta(days=1)


                    create_glisthis()
                    from_date = t_date
                    to_date = t_to_date


                    create_glist()
                    break
        else:
            from_datehis = t_from_date
            to_datehis = t_to_date


            create_glisthis()

    if sorttype == 1:
        create_list1()
    else:

        if from_dept == 0:
            create_list2()
        else:
            create_list2d()

    return generate_output()