from functions.additional_functions import *
import decimal
from models import L_kredit, Gl_jouhdr, Gl_journal, Ap_journal

def ap_list_btn_delbl(pvilanguage:int, ap_recid:int, user_init:str):
    msg_str = ""
    lvcarea:str = "ap_list"
    saldo:decimal = 0
    netto:decimal = 0
    l_kredit = gl_jouhdr = gl_journal = ap_journal = None

    apbuff = None

    Apbuff = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, saldo, netto, l_kredit, gl_jouhdr, gl_journal, ap_journal
        nonlocal apbuff


        nonlocal apbuff
        return {"msg_str": msg_str}


    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit._recid == ap_recid)).first()

    if l_kredit.counter > 0:

        apbuff = db_session.query(Apbuff).filter(
                (Apbuff.counter == l_kredit.counter) &  (Apbuff.zahlkonto > 0)).first()

        if apbuff:
            msg_str = msg_str + chr(2) + translateExtended ("A/P Payment exists, deleting not possible.", lvcarea, "")

            return generate_output()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.refno == l_kredit.name) &  (Gl_jouhdr.datum == l_kredit.rgdatum)).first()

    if gl_jouhdr and gl_jouhdr.activeflag == 1:
        msg_str = msg_str + chr(2) + translateExtended ("The related journals are no longer active.", lvcarea, "")

        return generate_output()

    if gl_jouhdr:

        for gl_journal in db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == gl_jouhdr.jnr)).all():
            db_session.delete(gl_journal)

        gl_jouhdr = db_session.query(Gl_jouhdr).first()
        db_session.delete(gl_jouhdr)
    saldo = saldo - l_kredit.saldo
    netto = netto - l_kredit.netto


    ap_journal = Ap_journal()
    db_session.add(ap_journal)

    ap_journal.lief_nr = l_kredit.lief_nr
    ap_journal.docu_nr = l_kredit.name
    ap_journal.lscheinnr = l_kredit.lscheinnr
    ap_journal.rgdatum = l_kredit.rgdatum
    ap_journal.saldo = saldo
    ap_journal.netto = netto
    ap_journal.userinit = user_init
    ap_journal.zeit = get_current_time_in_seconds()
    ap_journal.betriebsnr = l_kredit.betriebsnr

    l_kredit = db_session.query(L_kredit).first()
    db_session.delete(l_kredit)


    return generate_output()