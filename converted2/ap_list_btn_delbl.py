#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, Gl_jouhdr, Gl_journal, Ap_journal

def ap_list_btn_delbl(pvilanguage:int, ap_recid:int, user_init:string):

    prepare_cache ([Ap_journal])

    msg_str = ""
    lvcarea:string = "ap-list"
    saldo:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    l_kredit = gl_jouhdr = gl_journal = ap_journal = None

    apbuff = None

    Apbuff = create_buffer("Apbuff",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, saldo, netto, l_kredit, gl_jouhdr, gl_journal, ap_journal
        nonlocal pvilanguage, ap_recid, user_init
        nonlocal apbuff


        nonlocal apbuff

        return {"msg_str": msg_str}


    # l_kredit = get_cache (L_kredit, {"_recid": [(eq, ap_recid)]})
    l_kredit = db_session.query(Apbuff).filter(
             (Apbuff._recid == ap_recid)).with_for_update().first()

    if l_kredit:

        if l_kredit.counter > 0:

            apbuff = db_session.query(Apbuff).filter(
                     (Apbuff.counter == l_kredit.counter) & (Apbuff.zahlkonto > 0)).first()

            if apbuff:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("A/P Payment exists, deleting not possible.", lvcarea, "")

                return generate_output()

        # gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, l_kredit.name)],"datum": [(eq, l_kredit.rgdatum)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.refno == l_kredit.name) & (Gl_jouhdr.datum == l_kredit.rgdatum)).with_for_update().first()

        if gl_jouhdr and gl_jouhdr.activeflag == 1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("The related journals are no longer active.", lvcarea, "")

            return generate_output()

        if gl_jouhdr:

            for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).with_for_update().all():
                db_session.delete(gl_journal)
            pass
            pass
            db_session.delete(gl_jouhdr)
            pass
        saldo =  to_decimal(saldo) - to_decimal(l_kredit.saldo)
        netto =  to_decimal(netto) - to_decimal(l_kredit.netto)


        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = l_kredit.lief_nr
        ap_journal.docu_nr = l_kredit.name
        ap_journal.lscheinnr = l_kredit.lscheinnr
        ap_journal.rgdatum = l_kredit.rgdatum
        ap_journal.saldo =  to_decimal(saldo)
        ap_journal.netto =  to_decimal(netto)
        ap_journal.userinit = user_init
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.betriebsnr = l_kredit.betriebsnr


        pass
        db_session.delete(l_kredit)

    return generate_output()