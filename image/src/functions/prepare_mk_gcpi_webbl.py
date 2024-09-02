from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gc_pibline, Gc_pi, Gc_pitype, Htparam, Gl_acct, Gc_giro, Bediener, Gc_piacct, Queasy

def prepare_mk_gcpi_webbl(pvilanguage:int, pi_number:str, user_init:str):
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
    pay_amount = 0
    pbuff_list = []
    t_gc_pitype_list = []
    t_gc_pibline_list = []
    s_list_list = []
    bankname = ""
    i:int = 0
    lvcarea:str = "mk_gcPI"
    gc_pibline = gc_pi = gc_pitype = htparam = gl_acct = gc_giro = bediener = gc_piacct = queasy = None

    t_gc_pibline = pbuff = t_gc_pitype = s_list = None

    t_gc_pibline_list, T_gc_pibline = create_model_like(Gc_pibline, {"rec_id":int})
    pbuff_list, Pbuff = create_model_like(Gc_pi)
    t_gc_pitype_list, T_gc_pitype = create_model_like(Gc_pitype)
    s_list_list, S_list = create_model("S_list", {"reihe":int, "bezeich":str, "amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_list, t_gc_pitype_list, t_gc_pibline_list, s_list_list, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_list, pbuff_list, t_gc_pitype_list, s_list_list
        return {"pi_acctno": pi_acctno, "giro_tempacct": giro_tempacct, "pi_mode": pi_mode, "pi_status": pi_status, "pi_type1": pi_type1, "fl_temp": fl_temp, "fl_err": fl_err, "p_110": p_110, "bemerk": bemerk, "rcvname": rcvname, "pay_acctno": pay_acctno, "department": department, "pay_amount": pay_amount, "pbuff": pbuff_list, "t-gc-pitype": t_gc_pitype_list, "t-gc-PIbline": t_gc_pibline_list, "s-list": s_list_list, "bankname": bankname}

    def enable1a():

        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_list, t_gc_pitype_list, t_gc_pibline_list, s_list_list, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_list, pbuff_list, t_gc_pitype_list, s_list_list

        gc_piacct = db_session.query(Gc_piacct).filter(
                (Gc_piacct.fibukonto == gc_pi.credit_fibu)).first()

        if gc_piacct:
            pay_acctno = gc_piacct.fibukonto

        bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == gc_pi.rcvID)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == bediener.user_group)).first()

        if queasy:
            department = queasy.char3
        bemerk = pbuff.bemerk
        rcvname = bediener.username

    def enable2():

        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_list, t_gc_pitype_list, t_gc_pibline_list, s_list_list, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_list, pbuff_list, t_gc_pitype_list, s_list_list

        for gc_pibline in db_session.query(Gc_pibline).filter(
                (gc_PIbline.docu_nr == pbuff.docu_nr)).all():
            t_gc_pibline = T_gc_pibline()
            t_gc_pibline_list.append(t_gc_pibline)

            buffer_copy(gc_PIbline, t_gc_pibline)
            t_gc_PIbline.rec_id = gc_PIbline._recid

        gc_piacct = db_session.query(Gc_piacct).filter(
                (Gc_piacct.fibukonto == gc_pi.credit_fibu)).first()

        if gc_piacct:
            pay_acctno = gc_piacct.fibukonto

        bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == gc_pi.rcvID)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == bediener.user_group)).first()

        if queasy:
            department = queasy.char3
        bemerk = pbuff.bemerk
        rcvname = bediener.username
        pay_amount = pbuff.betrag

    def enable3():

        nonlocal pi_acctno, giro_tempacct, pi_mode, pi_status, pi_type1, fl_temp, fl_err, p_110, bemerk, rcvname, pay_acctno, department, pay_amount, pbuff_list, t_gc_pitype_list, t_gc_pibline_list, s_list_list, bankname, i, lvcarea, gc_pibline, gc_pi, gc_pitype, htparam, gl_acct, gc_giro, bediener, gc_piacct, queasy


        nonlocal t_gc_pibline, pbuff, t_gc_pitype, s_list
        nonlocal t_gc_pibline_list, pbuff_list, t_gc_pitype_list, s_list_list

        for gc_pibline in db_session.query(Gc_pibline).filter(
                (gc_PIbline.docu_nr == pbuff.docu_nr)).all():
            t_gc_pibline = T_gc_pibline()
            t_gc_pibline_list.append(t_gc_pibline)

            buffer_copy(gc_PIbline, t_gc_pibline)
            t_gc_PIbline.rec_id = gc_PIbline._recid

        gc_piacct = db_session.query(Gc_piacct).filter(
                (Gc_piacct.fibukonto == gc_pi.credit_fibu)).first()

        if gc_piacct:
            pay_acctno = gc_piacct.fibukonto

        bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == gc_pi.rcvID)).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 19) &  (Queasy.number1 == bediener.user_group)).first()

        if queasy:
            department = queasy.char3
        bemerk = pbuff.bemerk
        rcvname = bediener.username
        pay_amount = pbuff.betrag


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 931)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == htparam.fchar)).first()

    if not gl_acct:
        fl_err = True

        return generate_output()
    pi_acctno = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1018)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == htparam.fchar)).first()

    if gl_acct:
        giro_tempacct = htparam.fchar


    pbuff = Pbuff()
    pbuff_list.append(pbuff)

    for i in range(1,10 + 1) :
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.reihe = i

    if pi_number == "":
        pi_mode = "new"
    else:

        gc_pi = db_session.query(Gc_pi).filter(
                (func.lower(Gc_pi.docu_nr) == (pi_number).lower())).first()
        buffer_copy(gc_pi, pbuff)

        gc_giro = db_session.query(Gc_giro).filter(
                (Gc_giro.gironum == gc_pi.chequeNo)).first()

        if gc_giro:
            bankname = gc_giro.bankname
        for i in range(1,10 + 1) :

            s_list = query(s_list_list, filters=(lambda s_list :s_list.reihe == i), first=True)
            s_list.bezeich = pbuff.bez_array[i - 1]
            s_list.amount = pbuff.amount_array[i - 1]

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

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if not gc_pi or (gc_pi and gc_pi.pi_type == 0):
        fl_temp = 1

        for gc_pitype in db_session.query(Gc_pitype).all():
            t_gc_pitype = T_gc_pitype()
            t_gc_pitype_list.append(t_gc_pitype)

            buffer_copy(gc_pitype, t_gc_pitype)
    else:
        fl_temp = 2

        gc_pitype = db_session.query(Gc_pitype).filter(
                (Gc_pitype.nr == gc_pi.pi_type)).first()
        pi_type1 = gc_pitype.bezeich

        for gc_pitype in db_session.query(Gc_pitype).filter(
                (Gc_pitype.nr != gc_pi.pi_type)).all():
            t_gc_pitype = T_gc_pitype()
            t_gc_pitype_list.append(t_gc_pitype)

            buffer_copy(gc_pitype, t_gc_pitype)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    p_110 = htparam.fdate

    if pi_mode.lower()  == "new1":
        enable1a()

    elif pi_mode.lower()  == "open":
        enable2()

    elif pi_mode.lower()  == "closed":
        enable3()

    return generate_output()