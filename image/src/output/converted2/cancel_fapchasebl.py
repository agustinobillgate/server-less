#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_artikel, Bediener, Htparam, Fa_op, L_kredit, Ap_journal

def cancel_fapchasebl(lief_nr:int, docu_nr:string, user_init:string):

    prepare_cache ([Fa_artikel, Bediener, Htparam, Fa_op, Ap_journal])

    lscheinnr:string = ""
    billdate:date = None
    t_amount:Decimal = to_decimal("0.0")
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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})

        if not htparam.flogical:

            return

        l_kredit = get_cache (L_kredit, {"name": [(eq, docu_nr)],"saldo": [(eq, - t_amount)],"lief_nr": [(eq, lief_nr)],"rgdatum": [(eq, billdate)]})

        if l_kredit:
            pass
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

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    for fa_op in db_session.query(Fa_op).filter(
             (Fa_op.lief_nr == lief_nr) & (Fa_op.lscheinnr == (lscheinnr).lower()) & (Fa_op.loeschflag <= 1)).order_by(Fa_op._recid).all():

        fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, fa_op.nr)]})

        if fa_artikel.p_nr != 0:

            fa_art = get_cache (Fa_artikel, {"nr": [(eq, fa_artikel.p_nr)]})

            if fa_art:
                fa_art.warenwert =  to_decimal(fa_art.warenwert) - to_decimal(fa_artikel.warenwert)
                fa_art.book_wert =  to_decimal(fa_art.book_wert) - to_decimal(fa_artikel.warenwert)
                pass
        fa_artikel.posted = False
        fa_artikel.next_depn = None
        fa_artikel.anzahl = 0
        fa_artikel.warenwert =  to_decimal("0")
        fa_artikel.book_wert =  to_decimal("0")
        pass
        fa_op.loeschflag = 2
        t_amount =  to_decimal(t_amount) - to_decimal(fa_op.warenwert)
    update_ap()

    return generate_output()