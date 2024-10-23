from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_jouhdr, Gl_journal, Bediener, Res_history

def delete_gl_jouallbl(refno:str, idnr:str):
    flag = False
    msg = ""
    fb_close:date = None
    mat_close:date = None
    gl_close:date = None
    tdate:str = ""
    iday:int = 0
    imon:int = 0
    iyear:int = 0
    htparam = gl_jouhdr = gl_journal = bediener = res_history = None

    t_lop = None

    t_lop_list, T_lop = create_model("T_lop", {"lscheinnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, msg, fb_close, mat_close, gl_close, tdate, iday, imon, iyear, htparam, gl_jouhdr, gl_journal, bediener, res_history
        nonlocal refno, idnr


        nonlocal t_lop
        nonlocal t_lop_list
        return {"flag": flag, "msg": msg}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 221)).first()
    fb_close = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 224)).first()
    mat_close = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    gl_close = htparam.fdate

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
             (func.lower(Gl_jouhdr.refno) == (refno).lower())).first()

    if gl_jouhdr:

        if gl_jouhdr.activeflag == 0:

            if gl_jouhdr.jtype == 3 or gl_jouhdr.jtype == 6:

                if gl_jouhdr.datum >= date_mdy(get_month(fb_close) , 1, get_year(fb_close)) or gl_jouhdr.datum >= date_mdy(get_month(mat_close) , 1, get_year(mat_close)):

                    for gl_journal in db_session.query(Gl_journal).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                        db_session.delete(gl_journal)
                    db_session.delete(gl_jouhdr)
                    flag = True


                else:
                    flag = False


                    msg = "GL has been closed. Can not delete journal"

                    return generate_output()
            else:

                if gl_jouhdr.datum >= date_mdy(get_month(gl_close) , 1, get_year(gl_close)):

                    for gl_journal in db_session.query(Gl_journal).filter(
                             (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                        db_session.delete(gl_journal)
                    db_session.delete(gl_jouhdr)
                    flag = True


                else:
                    flag = False


                    msg = "GL has been closed. Can not delete journal"

                    return generate_output()
        else:
            flag = False
            msg = "Closed journal can not be deleted"

            return generate_output()

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (idnr).lower())).first()
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