#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 25/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_accthis, Htparam, Gl_jouhdr, Gl_journal, Gl_jourhis, Gl_jhdrhis, Bediener, Res_history
from sqlalchemy.orm import flag_modified

def closeyear2bl(curr_yr:int, curr_date:date, user_init:string):

    prepare_cache ([Gl_acct, Gl_accthis, Htparam, Gl_jourhis, Bediener, Res_history])

    t_gl_acct_data = []
    i:int = 0
    last_2yr:date = None
    yy:int = 0
    gl_acct = gl_accthis = htparam = gl_jouhdr = gl_journal = gl_jourhis = gl_jhdrhis = bediener = res_history = None

    t_gl_acct = gl_acc1 = gl_hbuff = gl_acct1 = gbuff = gbuff1 = None

    t_gl_acct_data, T_gl_acct = create_model_like(Gl_acct)

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_hbuff = create_buffer("Gl_hbuff",Gl_accthis)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gbuff = create_buffer("Gbuff",Gl_accthis)
    Gbuff1 = create_buffer("Gbuff1",Gl_accthis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_data, i, last_2yr, yy, gl_acct, gl_accthis, htparam, gl_jouhdr, gl_journal, gl_jourhis, gl_jhdrhis, bediener, res_history
        nonlocal curr_yr, curr_date, user_init
        nonlocal gl_acc1, gl_hbuff, gl_acct1, gbuff, gbuff1


        nonlocal t_gl_acct, gl_acc1, gl_hbuff, gl_acct1, gbuff, gbuff1
        nonlocal t_gl_acct_data

        return {"t-gl-acct": t_gl_acct_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})
    htparam.flogical = True

    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        t_gl_acct = T_gl_acct()
        t_gl_acct_data.append(t_gl_acct)

        buffer_copy(gl_acct, t_gl_acct)

    # gl_accthis = get_cache (Gl_accthis, {"year": [(eq, curr_yr)]})
    # while None != gl_accthis:

    #     gl_hbuff = get_cache (Gl_accthis, {"_recid": [(eq, gl_accthis._recid)]})
    #     db_session.delete(gl_hbuff)
    #     pass

    #     curr_recid = gl_accthis._recid
    #     gl_accthis = db_session.query(Gl_accthis).filter(
    #              (Gl_accthis.year == curr_yr) & (Gl_accthis._recid > curr_recid)).first()

    for gl_accthis in db_session.query(Gl_accthis).filter(
                 (Gl_accthis.year == curr_yr)).order_by(Gl_accthis._recid)().all():
        gl_hbuff = db_session.query(Gl_accthis).filter(
                     (Gl_accthis._recid == gl_accthis._recid)).with_for_update().first()
        db_session.delete(gl_hbuff)
        pass

    gl_acct = db_session.query(Gl_acct).first()
    while None != gl_acct:
        gl_accthis = Gl_accthis()
        db_session.add(gl_accthis)

        buffer_copy(gl_acct, gl_accthis)
        gl_accthis.year = curr_yr

        # Rd, 25/11/2025, with_for_update added
        # gl_acc1 = get_cache (Gl_acct, {"_recid": [(eq, gl_acct._recid)]})
        gl_acc1 = db_session.query(Gl_acct).filter(
                     (Gl_acct._recid == gl_acct._recid)).with_for_update().first()
        for i in range(1,12 + 1) :
            gl_acc1.last_yr[i - 1] = gl_acc1.actual[i - 1]
            gl_acc1.actual[i - 1] = 0
            gl_acc1.ly_budget[i - 1] = gl_acc1.budget[i - 1]
            gl_acc1.budget[i - 1] = gl_acc1.debit[i - 1]
            gl_acc1.debit[i - 1] = 0
        
        pass

        curr_recid = gl_acct._recid
        gl_acct = db_session.query(Gl_acct).filter(Gl_acct._recid > curr_recid).first()

    flag_modified(gl_acc1, "last_yr")
    flag_modified(gl_acc1, "actual")
    flag_modified(gl_acc1, "ly_budget")
    flag_modified(gl_acc1, "budget")
    flag_modified(gl_acc1, "debit")

    last_2yr = date_mdy(1, 1, (curr_yr - timedelta(days=1)))

    # Rd, 25/11/2025, with_for_update added
    # gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(lt, last_2yr)]})
    # while None != gl_jouhdr:
    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum < last_2yr)).order_by(Gl_jouhdr._recid).with_for_update().all():
        # Rd, 25/11/2025,
        for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).with_for_update().all():
            gl_jourhis = Gl_jourhis()
            db_session.add(gl_jourhis)

            buffer_copy(gl_journal, gl_jourhis)
            gl_jourhis.datum = gl_jouhdr.datum
            pass
            db_session.delete(gl_journal)
        gl_jhdrhis = Gl_jhdrhis()
        db_session.add(gl_jhdrhis)
        buffer_copy(gl_jouhdr, gl_jhdrhis)
        pass
        db_session.delete(gl_jouhdr)

        # curr_recid = gl_jouhdr._recid
        # gl_jouhdr = db_session.query(Gl_jouhdr).filter(
        #              (Gl_jouhdr.datum < last_2yr) & (Gl_jouhdr._recid > curr_recid)).first()
    pass
    pass

    # htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})
    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).with_for_update().first()
    htparam.flogical = False
    pass

    # htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 795)).with_for_update().first()
    curr_date = htparam.fdate
    yy = get_year(curr_date) + 1
    htparam.fdate = date_mdy(get_month(curr_date) , get_day(curr_date) , yy)
    htparam.lupdate = get_current_date()
    htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 599)]})

    if htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 979)]})

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})
        gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == htparam.fchar)).with_for_update().first()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 612)]})

        # gl_acct1 = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})
        gl_acct1 = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == htparam.fchar)).with_for_update().first()

        # gbuff = get_cache (Gl_accthis, {"fibukonto": [(eq, gl_acct.fibukonto)],"year": [(eq, curr_yr)]})
        gbuff = db_session.query(Gl_accthis).filter(
                     (Gl_accthis.fibukonto == gl_acct.fibukonto) & (Gl_accthis.year == curr_yr)).with_for_update().first()

        # gbuff1 = get_cache (Gl_accthis, {"fibukonto": [(eq, gl_acct1.fibukonto)],"year": [(eq, curr_yr)]})
        gbuff1 = db_session.query(Gl_accthis).filter(
                     (Gl_accthis.fibukonto == gl_acct1.fibukonto) & (Gl_accthis.year == curr_yr)).with_for_update().first()
        for i in range(1,12 + 1) :
            gl_acct1.last_yr[i - 1] = gl_acct1.last_yr[i - 1] + gl_acct.last_yr[i - 1]
            gl_acct.last_yr[i - 1] = 0
            gbuff1.actual[i - 1] = gl_acct1.last_yr[i - 1]
            gbuff.actual[i - 1] = 0
        flag_modified(gl_acct1, "last_yr")
        flag_modified(gl_acct, "last_yr")
        flag_modified(gbuff1, "actual")
        flag_modified(gbuff, "actual")

        pass
        pass
        pass
        pass

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Closing Year - " + to_string(yy - 1)
    res_history.action = "G/L"


    pass
    pass

    return generate_output()