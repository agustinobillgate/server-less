#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_journal, Artikel, Parameters

def delacct_allowedbl(pvilanguage:int, from_acct:string, mess_it:bool):

    prepare_cache ([Gl_acct, Artikel])

    do_it = False
    msg_str = ""
    lvcarea:string = "gl-export-import-journal"
    gl_acct = gl_journal = artikel = parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, msg_str, lvcarea, gl_acct, gl_journal, artikel, parameters
        nonlocal pvilanguage, from_acct, mess_it

        return {"do_it": do_it, "msg_str": msg_str}

    def delacct_allowed():

        nonlocal do_it, msg_str, lvcarea, gl_acct, gl_journal, artikel, parameters
        nonlocal pvilanguage, from_acct, mess_it

        gl_journal = get_cache (Gl_journal, {"fibukonto": [(eq, gl_acct.fibukonto)]})

        if gl_journal:

            if mess_it:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("G/L Journal entry exists, deleting not possible.", lvcarea, "")

            return

        artikel = get_cache (Artikel, {"fibukonto": [(eq, gl_acct.fibukonto)]})

        if artikel:

            if mess_it:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Front-office Article exists, deleting not possible", lvcarea, "") + chr_unicode(10) + to_string(artikel.artnr) + " - " + artikel.bezeich

            return

        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "alloc")],"vtype": [(eq, 1)],"vstring": [(eq, gl_acct.fibukonto)]})

        if parameters:

            if mess_it:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Cost Allocation exists, deleting not possible.", lvcarea, "")

            return
        do_it = True

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, from_acct)]})

    if not gl_acct:
        msg_str = translateExtended ("No such Account Number:", lvcarea, "") + " " + from_acct

        return generate_output()
    delacct_allowed()

    return generate_output()