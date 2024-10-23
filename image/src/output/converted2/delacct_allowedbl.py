from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Gl_journal, Artikel, Parameters

def delacct_allowedbl(pvilanguage:int, from_acct:str, mess_it:bool):
    do_it = False
    msg_str = ""
    lvcarea:str = "gl-export-import-journal"
    gl_acct = gl_journal = artikel = parameters = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, msg_str, lvcarea, gl_acct, gl_journal, artikel, parameters
        nonlocal pvilanguage, from_acct, mess_it


        return {"do_it": do_it, "msg_str": msg_str}

    def delacct_allowed():

        nonlocal do_it, msg_str, lvcarea, gl_acct, gl_journal, artikel, parameters
        nonlocal pvilanguage, from_acct, mess_it

        gl_journal = db_session.query(Gl_journal).filter(
                 (Gl_journal.fibukonto == gl_acct.fibukonto)).first()

        if gl_journal:

            if mess_it:
                msg_str = msg_str + chr(2) + translateExtended ("G/L Journal entry exists, deleting not possible.", lvcarea, "")

            return

        artikel = db_session.query(Artikel).filter(
                 (Artikel.fibukonto == gl_acct.fibukonto)).first()

        if artikel:

            if mess_it:
                msg_str = msg_str + chr(2) + translateExtended ("Front-office Article exists, deleting not possible", lvcarea, "") + chr(10) + to_string(artikel.artnr) + " - " + artikel.bezeich

            return

        parameters = db_session.query(Parameters).filter(
                 (func.lower(Parameters.progname) == ("CostCenter").lower()) & (func.lower(Parameters.section) == ("Alloc").lower()) & (Parameters.vtype == 1) & (Parameters.vstring == gl_acct.fibukonto)).first()

        if parameters:

            if mess_it:
                msg_str = msg_str + chr(2) + translateExtended ("Cost Allocation exists, deleting not possible.", lvcarea, "")

            return
        do_it = True

    gl_acct = db_session.query(Gl_acct).filter(
             (func.lower(Gl_acct.fibukonto) == (from_acct).lower())).first()

    if not gl_acct:
        msg_str = translateExtended ("No such Account Number:", lvcarea, "") + " " + from_acct

        return generate_output()
    delacct_allowed()

    return generate_output()