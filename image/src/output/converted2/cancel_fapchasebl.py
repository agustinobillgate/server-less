from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_artikel, Bediener, Htparam, Fa_op, L_kredit, Ap_journal

def cancel_fapchasebl(lief_nr:int, docu_nr:str, user_init:str):
    lscheinnr:str = ""
    billdate:date = None
    t_amount:decimal = to_decimal("0.0")
    fa_artikel = bediener = htparam = fa_op = l_kredit = ap_journal = None

    fa_art = None

    Fa_art = create_buffer("Fa_art",Fa_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lscheinnr, billdate, t_amount, fa_artikel, bediener, htparam, fa_op, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init
        nonlocal fa_art


        nonlocal fa_art
        return {}

    def update_ap():

        nonlocal lscheinnr, billdate, t_amount, fa_artikel, bediener, htparam, fa_op, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init
        nonlocal fa_art


        nonlocal fa_art

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 1016)).first()

        if not htparam.flogical:

            return

        l_kredit = db_session.query(L_kredit).filter(
                 (func.lower(L_kredit.name) == (docu_nr).lower()) & (L_kredit.saldo == - t_amount) & (L_kredit.lief_nr == lief_nr) & (L_kredit.rgdatum == billdate)).first()

        if l_kredit:
            db_session.delete(l_kredit)
        else:
            l_kredit = L_kredit()
            db_session.add(l_kredit)

            l_kredit.name = docu_nr
            l_kredit.lief_nr = lief_nr
            l_kredit.lscheinnr = lscheinnr
            l_kredit.rgdatum = billdate
            l_kredit.datum = None
            l_kredit.saldo =  to_decimal(t_amount)
            l_kredit.ziel = 0
            l_kredit.netto =  to_decimal(t_amount)
            l_kredit.bediener_nr = bediener.nr


        ap_journal = Ap_journal()
        db_session.add(ap_journal)

        ap_journal.lief_nr = lief_nr
        ap_journal.docu_nr = docu_nr
        ap_journal.lscheinnr = docu_nr
        ap_journal.rgdatum = billdate
        ap_journal.saldo =  to_decimal(t_amount)
        ap_journal.netto =  to_decimal(t_amount)
        ap_journal.userinit = bediener.userinit
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.bemerk = "Cancel Fixed Asset Receiving"


    lscheinnr = docu_nr

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    for fa_op in db_session.query(Fa_op).filter(
             (Fa_op.lief_nr == lief_nr) & (func.lower(Fa_op.lscheinnr) == (lscheinnr).lower()) & (Fa_op.loeschflag <= 1)).order_by(Fa_op._recid).all():

        fa_artikel = db_session.query(Fa_artikel).filter(
                 (Fa_artikel.nr == fa_op.nr)).first()

        if fa_artikel.p_nr != 0:

            fa_art = db_session.query(Fa_art).filter(
                     (Fa_art.nr == fa_artikel.p_nr)).first()

            if fa_art:
                fa_art.warenwert =  to_decimal(fa_art.warenwert) - to_decimal(fa_artikel.warenwert)
                fa_art.book_wert =  to_decimal(fa_art.book_wert) - to_decimal(fa_artikel.warenwert)
        fa_artikel.posted = False
        fa_artikel.next_depn = None
        fa_artikel.anzahl = 0
        fa_artikel.warenwert =  to_decimal("0")
        fa_artikel.book_wert =  to_decimal("0")
        fa_op.loeschflag = 2
        t_amount =  to_decimal(t_amount) - to_decimal(fa_op.warenwert)
    update_ap()

    return generate_output()