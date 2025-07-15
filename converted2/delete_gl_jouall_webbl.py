#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Gl_jouhdr, Gl_journal, Bediener, Res_history

def delete_gl_jouall_webbl(refno:string, idnr:string):

    prepare_cache ([Htparam, Bediener, Res_history])

    flag = False
    msg = ""
    fb_close:date = None
    mat_close:date = None
    gl_close:date = None
    tdate:string = ""
    iday:int = 0
    imon:int = 0
    iyear:int = 0
    queasy = htparam = gl_jouhdr = gl_journal = bediener = res_history = None

    t_lop = queasy_buff = None

    t_lop_data, T_lop = create_model("T_lop", {"lscheinnr":string})

    Queasy_buff = create_buffer("Queasy_buff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, msg, fb_close, mat_close, gl_close, tdate, iday, imon, iyear, queasy, htparam, gl_jouhdr, gl_journal, bediener, res_history
        nonlocal refno, idnr
        nonlocal queasy_buff


        nonlocal t_lop, queasy_buff
        nonlocal t_lop_data

        return {"flag": flag, "msg": msg}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    fb_close = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    mat_close = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    gl_close = htparam.fdate

    gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, refno)]})

    if gl_jouhdr:

        if gl_jouhdr.activeflag == 0:

            if gl_jouhdr.jtype == 3 or gl_jouhdr.jtype == 6:

                if gl_jouhdr.datum >= date_mdy(get_month(fb_close) , 1, get_year(fb_close)) or gl_jouhdr.datum >= date_mdy(get_month(mat_close) , 1, get_year(mat_close)):

                    for gl_journal in db_session.query(Gl_journal).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                        db_session.delete(gl_journal)
                    pass
                    db_session.delete(gl_jouhdr)
                    flag = True

                    queasy = get_cache (Queasy, {"key": [(eq, 348)],"date1": [(eq, gl_jouhdr.datum)]})

                    if queasy:

                        for queasy_buff in db_session.query(Queasy_buff).filter(
                                 (Queasy_buff.key == 348) & (Queasy_buff.date1 == gl_jouhdr.datum)).order_by(Queasy_buff._recid).all():
                            db_session.delete(queasy_buff)
                else:
                    flag = False


                    msg = "GL has been closed. Can not delete journal"

                    return generate_output()
            else:

                if gl_jouhdr.datum >= date_mdy(get_month(gl_close) , 1, get_year(gl_close)):

                    for gl_journal in db_session.query(Gl_journal).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                        db_session.delete(gl_journal)
                    pass
                    db_session.delete(gl_jouhdr)
                    flag = True

                    queasy = get_cache (Queasy, {"key": [(eq, 348)],"date1": [(eq, gl_jouhdr.datum)]})

                    if queasy:

                        for queasy_buff in db_session.query(Queasy_buff).filter(
                                 (Queasy_buff.key == 348) & (Queasy_buff.date1 == gl_jouhdr.datum)).order_by(Queasy_buff._recid).all():
                            db_session.delete(queasy_buff)
                else:
                    flag = False


                    msg = "GL has been closed. Can not delete journal"

                    return generate_output()
        else:
            flag = False
            msg = "Closed journal can not be deleted"

            return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, idnr)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.resnr = 0
    res_history.reslinnr = 0
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Journal Transaction & Detail Delete - Reference no " + refno + " by " + bediener.username
    res_history.betriebsnr = bediener.nr
    res_history.action = "JournalTransactionDelete"


    pass

    return generate_output()