#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_transf_headoffice2bl import gl_transf_headoffice2bl
from models import Gl_jouhdr, Gl_journal, Paramtext, Gl_acct, Htparam

def gl_transf_headoffice1bl(pvilanguage:int, curr_date:date):

    prepare_cache ([Paramtext, Gl_acct, Htparam])

    success_flag = False
    msg_str = ""
    first_date:date = None
    lreturn:bool = False
    map_acct:string = ""
    hoappparam:string = ""
    vhost:string = ""
    vservice:string = ""
    lic_nr:string = ""
    lvcarea:string = "closemonth"
    gl_jouhdr = gl_journal = paramtext = gl_acct = htparam = None

    t_gl_jouhdr = t_gl_journal = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)
    t_gl_journal_list, T_gl_journal = create_model_like(Gl_journal)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, first_date, lreturn, map_acct, hoappparam, vhost, vservice, lic_nr, lvcarea, gl_jouhdr, gl_journal, paramtext, gl_acct, htparam
        nonlocal pvilanguage, curr_date


        nonlocal t_gl_jouhdr, t_gl_journal
        nonlocal t_gl_jouhdr_list, t_gl_journal_list

        return {"success_flag": success_flag, "msg_str": msg_str}

    def decode_string(in_str:string):

        nonlocal success_flag, msg_str, first_date, lreturn, map_acct, hoappparam, vhost, vservice, lic_nr, lvcarea, gl_jouhdr, gl_journal, paramtext, gl_acct, htparam
        nonlocal pvilanguage, curr_date


        nonlocal t_gl_jouhdr, t_gl_journal
        nonlocal t_gl_jouhdr_list, t_gl_journal_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)


        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if not paramtext:
        msg_str = translateExtended ("parmtext[243] was not available.", lvcarea, "")

        return generate_output()
    lic_nr = decode_string(paramtext.ptexte)
    first_date = date_mdy(get_month(curr_date) , 1, get_year(curr_date))

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).order_by(Gl_jouhdr.jnr).all():
        t_gl_jouhdr = T_gl_jouhdr()
        t_gl_jouhdr_list.append(t_gl_jouhdr)

        buffer_copy(gl_jouhdr, t_gl_jouhdr)

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)]})
            map_acct = ""
            map_acct = trim(entry(1, gl_acct.userinit, ";"))

            if map_acct != "":
                t_gl_journal.fibukonto = map_acct

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2843)]})
    vhost = entry(0, htparam.fchar, ":")
    vservice = entry(1, htparam.fchar, ":")
    hoappparam = " -H " + vhost + " -s " + vservice + " -DirectConnect -sessionModel Session-free"


    lreturn = set_combo_session(hoappparam, None , None , None)

    if not lreturn:
        msg_str = translateExtended ("Failed to connect to HO server", lvcarea, "") + chr_unicode(10) + translateExtended ("Journals could not be transferred to the Heaad Office DB.", lvcarea, "")


        return generate_output()
    local_storage.combo_flag = True
    get_output(gl_transf_headoffice2bl(lic_nr, t_gl_jouhdr_list, t_gl_journal_list))
    local_storage.combo_flag = False

    success_flag = True
    msg_str = translateExtended ("Journals have been transferred to the Heaad Office DB.", lvcarea, "")

    lreturn = reset_combo_session()


    return generate_output()