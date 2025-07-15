#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_pibline, Gc_pi, Gc_pitype, Htparam, Gl_acct, Gc_giro, Bediener, Gc_piacct, Queasy

def prepare_mk_gcpi_webbl(pvilanguage:int, pi_number:string, user_init:string):

    prepare_cache ([Htparam, Gc_giro, Bediener, Gc_piacct, Queasy])

    pi_acctno = ""
    giro_tempacct = ""
    pi_mode = ""
    pi_status = ""
    pi_type1 = ""
    fl_temp = 0
    fl_err = False
    p_110 = None
    bemerk = ""
    rcvname = ""
    pay_acctno = ""
    department = ""
    pay_amount = to_decimal("0.0")
    pbuff_data = []
    t_gc_pitype_data = []
    t_gc_pibline_data = []
    s_list_data = []
    bankname = ""
    i:int = 0
    lvcarea:string = "mk-gcPI"
    gc_pibline = gc_pi = gc_pitype = htparam = gl_acct = gc_giro = bediener = gc_piacct = queasy = None

    t_gc_pibline = pbuff = t_gc_pitype = s_list = None

    t_gc_pibline_data, T_gc_pibline = create_model_like(Gc_pibline, {"rec_id":int})
    pbuff_data, Pbuff = create_model_like(Gc_pi)
    t_gc_pitype_data, T_gc_pitype = create_model_like(Gc_pitype)
    s_list_data, S_list = create_model("S_list", {"reihe":int, "bezeich":string, "amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_data, t_gc_pitype_data, t_gc_pibline_data, s_list_data, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy
        nonlocal pvilanguage, pi_number, user_init


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_data, pbuff_data, t_gc_pitype_data, s_list_data

        return {"pi_acctno": pi_acctno, "giro_tempacct": giro_tempacct, "pi_mode": pi_mode, "pi_status": pi_status, "pi_type1": pi_type1, "fl_temp": fl_temp, "fl_err": fl_err, "p_110": p_110, "bemerk": bemerk, "rcvname": rcvname, "pay_acctno": pay_acctno, "department": department, "pay_amount": pay_amount, "pbuff": pbuff_data, "t-gc-pitype": t_gc_pitype_data, "t-gc-PIbline": t_gc_pibline_data, "s-list": s_list_data, "bankname": bankname}

    def enable1a():

        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_data, t_gc_pitype_data, t_gc_pibline_data, s_list_data, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy
        nonlocal pvilanguage, pi_number, user_init


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_data, pbuff_data, t_gc_pitype_data, s_list_data

        gc_piacct = get_cache (Gc_piacct, {"fibukonto": [(eq, gc_pi.credit_fibu)]})

        if gc_piacct:
            pay_acctno = gc_piacct.fibukonto

        bediener = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, bediener.user_group)]})

        if queasy:
            department = queasy.char3
        bemerk = pbuff.bemerk
        rcvname = bediener.username


    def enable2():

        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_data, t_gc_pitype_data, t_gc_pibline_data, s_list_data, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy
        nonlocal pvilanguage, pi_number, user_init


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_data, pbuff_data, t_gc_pitype_data, s_list_data

        for gc_pibline in db_session.query(Gc_pibline).filter(
                 (gc_pibline.docu_nr == pbuff.docu_nr)).order_by(Gc_pibline._recid).all():
            t_gc_pibline = T_gc_pibline()
            t_gc_pibline_data.append(t_gc_pibline)

            buffer_copy(gc_pibline, t_gc_pibline)
            t_gc_pibline.rec_id = gc_pibline._recid

        gc_piacct = get_cache (Gc_piacct, {"fibukonto": [(eq, gc_pi.credit_fibu)]})

        if gc_piacct:
            pay_acctno = gc_piacct.fibukonto

        bediener = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, bediener.user_group)]})

        if queasy:
            department = queasy.char3
        bemerk = pbuff.bemerk
        rcvname = bediener.username
        pay_amount =  to_decimal(pbuff.betrag)


    def enable3():

        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_data, t_gc_pitype_data, t_gc_pibline_data, s_list_data, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy
        nonlocal pvilanguage, pi_number, user_init


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_data, pbuff_data, t_gc_pitype_data, s_list_data

        for gc_pibline in db_session.query(Gc_pibline).filter(
                 (gc_pibline.docu_nr == pbuff.docu_nr)).order_by(Gc_pibline._recid).all():
            t_gc_pibline = T_gc_pibline()
            t_gc_pibline_data.append(t_gc_pibline)

            buffer_copy(gc_pibline, t_gc_pibline)
            t_gc_pibline.rec_id = gc_pibline._recid

        gc_piacct = get_cache (Gc_piacct, {"fibukonto": [(eq, gc_pi.credit_fibu)]})

        if gc_piacct:
            pay_acctno = gc_piacct.fibukonto

        bediener = get_cache (Bediener, {"userinit": [(eq, gc_pi.rcvid)]})

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, bediener.user_group)]})

        if queasy:
            department = queasy.char3
        bemerk = pbuff.bemerk
        rcvname = bediener.username
        pay_amount =  to_decimal(pbuff.betrag)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 931)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

    if not gl_acct:
        fl_err = True

        return generate_output()
    pi_acctno = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1018)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

    if gl_acct:
        giro_tempacct = htparam.fchar


    pbuff = Pbuff()
    pbuff_data.append(pbuff)

    for i in range(1,10 + 1) :
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.reihe = i

    if pi_number == "":
        pi_mode = "new"
    else:

        gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, pi_number)]})

        if gc_pi:
            buffer_copy(gc_pi, pbuff)

            gc_giro = get_cache (Gc_giro, {"gironum": [(eq, gc_pi.chequeno)]})

            if gc_giro:
                bankname = gc_giro.bankname
            for i in range(1,10 + 1) :

                s_list = query(s_list_data, filters=(lambda s_list: s_list.reihe == i), first=True)
                s_list.bezeich = pbuff.bez_array[i - 1]
                s_list.amount =  to_decimal(pbuff.amount_array[i - 1])

            if gc_pi.pi_status == 0:
                pi_status = "0 - " + translateExtended ("APPLY", lvcarea, "")
                pi_mode = "new1"

            elif gc_pi.pi_status == 1:
                pi_status = "1 - " + translateExtended ("POSTED", lvcarea, "")
                pi_mode = "open"

            elif gc_pi.pi_status == 2:
                pi_status = "2 - " + translateExtended ("CLOSED", lvcarea, "")
                pi_mode = "closed"

            elif gc_pi.pi_status == 9:
                pi_status = "9 - " + translateExtended ("CANCELLED", lvcarea, "")
                pi_mode = "cancelled"

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if not gc_pi or (gc_pi and gc_pi.pi_type == 0):
        fl_temp = 1

        for gc_pitype in db_session.query(Gc_pitype).order_by(Gc_pitype.nr).all():
            t_gc_pitype = T_gc_pitype()
            t_gc_pitype_data.append(t_gc_pitype)

            buffer_copy(gc_pitype, t_gc_pitype)
    else:
        fl_temp = 2

        gc_pitype = get_cache (Gc_pitype, {"nr": [(eq, gc_pi.pi_type)]})
        pi_type1 = gc_pitype.bezeich

        for gc_pitype in db_session.query(Gc_pitype).filter(
                 (Gc_pitype.nr != gc_pi.pi_type)).order_by(Gc_pitype.nr).all():
            t_gc_pitype = T_gc_pitype()
            t_gc_pitype_data.append(t_gc_pitype)

            buffer_copy(gc_pitype, t_gc_pitype)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    p_110 = htparam.fdate

    if pi_mode.lower()  == ("new1").lower() :
        enable1a()

    elif pi_mode.lower()  == ("open").lower() :
        enable2()

    elif pi_mode.lower()  == ("closed").lower() :
        enable3()

    return generate_output()