from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.read_gl_journalbl import read_gl_journalbl
from functions.delete_debitorbl import delete_debitorbl
from functions.delete_gl_jouhdrbl import delete_gl_jouhdrbl
from functions.delete_gl_journalbl import delete_gl_journalbl
from models import Gl_journal, Debitor

def delete_manual_arbl(pvilanguage:int, rechnr:int, ar_recid:int):
    success_flag = False
    msg_str = ""
    acc_close:date = None
    ar_gl:date = None
    lvcarea:str = "delete_manual_ar"
    gl_journal = debitor = None

    t_gl_journal = None

    t_gl_journal_list, T_gl_journal = create_model_like(Gl_journal, {"b_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, acc_close, ar_gl, lvcarea, gl_journal, debitor


        nonlocal t_gl_journal
        nonlocal t_gl_journal_list
        return {"success_flag": success_flag, "msg_str": msg_str}


    acc_close = get_output(htpdate(558))
    ar_gl = get_output(htpdate(1014))
    t_gl_journal_list = get_output(read_gl_journalbl(3, None, None, None, None, None, rechnr, "", "", None, None))

    t_gl_journal = query(t_gl_journal_list, first=True)

    if t_gl_journal:

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == ar_recid)).first()

        if debitor.zahlkonto == 0 and debitor.counter == 0:

            if debitor.rgdatum > acc_close and debitor.rgdatum > ar_gl:
                success_flag = get_output(delete_debitorbl(1, ar_recid))
                success_flag = get_output(delete_gl_jouhdrbl(3, t_gl_journal.jnr, None, "", None))
                success_flag = get_output(delete_gl_journalbl(2, None, to_string(rechnr)))
            else:
                success_flag = False


                msg_str = translateExtended ("The transaction has closed", lvcarea, "")

                return generate_output()
        else:
            success_flag = False


            msg_str = translateExtended ("The transaction has paid", lvcarea, "")

            return generate_output()
    else:

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == ar_recid)).first()

        if debitor.zahlkonto == 0 and debitor.counter == 0:

            if debitor.rgdatum > acc_close and debitor.rgdatum > ar_gl:
                success_flag = get_output(delete_debitorbl(1, ar_recid))
            else:
                success_flag = False


                msg_str = translateExtended ("The transaction has closed", lvcarea, "")

                return generate_output()
        else:
            success_flag = False


            msg_str = translateExtended ("The transaction has paid", lvcarea, "")

            return generate_output()