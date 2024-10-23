from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, Gl_accthis, Htparam, Gl_jouhdr, Gl_journal, Gl_jourhis, Gl_jhdrhis, Bediener, Res_history

def closeyear2bl(curr_yr:int, curr_date:date, user_init:str):
    t_gl_acct_list = []
    i:int = 0
    last_2yr:date = None
    yy:int = 0
    gl_acct = gl_accthis = htparam = gl_jouhdr = gl_journal = gl_jourhis = gl_jhdrhis = bediener = res_history = None

    t_gl_acct = gl_acc1 = gl_hbuff = gl_acct1 = gbuff = gbuff1 = None

    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_hbuff = create_buffer("Gl_hbuff",Gl_accthis)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gbuff = create_buffer("Gbuff",Gl_accthis)
    Gbuff1 = create_buffer("Gbuff1",Gl_accthis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_list, i, last_2yr, yy, gl_acct, gl_accthis, htparam, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis, bediener, res_history
        nonlocal curr_yr, curr_date, user_init
        nonlocal gl_acc1, gl_hbuff, gl_acct1, gbuff, gbuff1


        nonlocal t_gl_acct, gl_acc1, gl_hbuff, gl_acct1, gbuff, gbuff1
        nonlocal t_gl_acct_list
        return {"t-gl-acct": t_gl_acct_list}

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).first()
    htparam.flogical = True


    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        t_gl_acct = T_gl_acct()
        t_gl_acct_list.append(t_gl_acct)

        buffer_copy(gl_acct, t_gl_acct)

    gl_accthis = db_session.query(Gl_accthis).filter(
             (Gl_accthis.year == curr_yr)).first()
    while None != gl_accthis:

        gl_hbuff = db_session.query(Gl_hbuff).filter(
                     (Gl_hbuff._recid == gl_accthis._recid)).first()
        gl_hbuff_list.remove(gl_hbuff)
        pass


        curr_recid = gl_accthis._recid
        gl_accthis = db_session.query(Gl_accthis).filter(
                 (Gl_accthis.year == curr_yr)).filter(Gl_accthis._recid > curr_recid).first()

    gl_acct = db_session.query(Gl_acct).first()
    while None != gl_acct:
        gl_accthis = Gl_accthis()
        db_session.add(gl_accthis)

        buffer_copy(gl_acct, gl_accthis)
        gl_accthis.year = curr_yr


        pass

        gl_acc1 = db_session.query(Gl_acc1).filter(
                     (Gl_acc1._recid == gl_acct._recid)).first()
        for i in range(1,12 + 1) :
            gl_acc1.last_yr[i - 1] = gl_acc1.actual[i - 1]
            gl_acc1.actual[i - 1] = 0
            gl_acc1.ly_budget[i - 1] = gl_acc1.budget[i - 1]
            gl_acc1.budget[i - 1] = gl_acc1.debit[i - 1]
            gl_acc1.debit[i - 1] = 0


        curr_recid = gl_acct._recid
        gl_acct = db_session.query(Gl_acct).filter(Gl_acct._recid > curr_recid).first()
    last_2yr = date_mdy(1, 1, (curr_yr - timedelta(days=1)))

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum < last_2yr)).first()
    while None != gl_jouhdr:

        for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
            gl_jourhis = Gl_jourhis()
            db_session.add(gl_jourhis)

            buffer_copy(gl_journal, gl_jourhis)
            gl_jourhis.datum = gl_jouhdr.datum


            pass
            db_session.delete(gl_journal)
        gl_jhdrhis = Gl_jhdrhis()
        db_session.add(gl_jhdrhis)

        buffer_copy(gl_jouhdr, gl_jhdrhis)
        db_session.delete(gl_jouhdr)

        curr_recid = gl_jouhdr._recid
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum < last_2yr)).filter(Gl_jouhdr._recid > curr_recid).first()

    pass
    pass

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).first()
    htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 795)).first()
    curr_date = htparam.fdate
    yy = get_year(curr_date) + 1
    htparam.fdate = date_mdy(get_month(curr_date) , get_day(curr_date) , yy)
    htparam.lupdate = get_current_date()
    htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 599)).first()

    if htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 979)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == htparam.fchar)).first()

        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 612)).first()

        gl_acct1 = db_session.query(Gl_acct1).filter(
                     (Gl_acct1.fibukonto == htparam.fchar)).first()

        gbuff = db_session.query(Gbuff).filter(
                     (Gbuff.fibukonto == gl_acct.fibukonto) & (Gbuff.year == curr_yr)).first()

        gbuff1 = db_session.query(Gbuff1).filter(
                     (Gbuff1.fibukonto == gl_acct1.fibukonto) & (Gbuff1.year == curr_yr)).first()
        for i in range(1,12 + 1) :
            gl_acct1.last_yr[i - 1] = gl_acct1.last_yr[i - 1] + gl_acct.last_yr[i - 1]
            gl_acct.last_yr[i - 1] = 0
            gbuff1.actual[i - 1] = gl_acct1.last_yr[i - 1]
            gbuff.actual[i - 1] = 0

    bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Closing Year - " + to_string(yy - 1)
    res_history.action = "G/L"


    pass


    return generate_output()