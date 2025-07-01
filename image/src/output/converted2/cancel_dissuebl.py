#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_ophdr, Htparam, L_op, L_bestand, Gl_acct, L_kredit, Ap_journal

def cancel_dissuebl(lief_nr:int, docu_nr:string, user_init:string):

    prepare_cache ([Bediener, Htparam, L_op, L_bestand, Ap_journal])

    wert:Decimal = to_decimal("0.0")
    billdate:date = None
    closedate:date = None
    anzahl:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    tot_anz:Decimal = to_decimal("0.0")
    tot_wert:Decimal = to_decimal("0.0")
    lscheinnr:string = ""
    bediener = l_ophdr = htparam = l_op = l_bestand = gl_acct = l_kredit = ap_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal wert, billdate, closedate, anzahl, t_amount, tot_anz, tot_wert, lscheinnr, bediener, l_ophdr, htparam, l_op, l_bestand, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init

        return {}

    def update_ap():

        nonlocal wert, billdate, closedate, anzahl, t_amount, tot_anz, tot_wert, lscheinnr, bediener, l_ophdr, htparam, l_op, l_bestand, gl_acct, l_kredit, ap_journal
        nonlocal lief_nr, docu_nr, user_init

        ap_license:bool = False
        ap_acct:string = ""
        do_it:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})

        if not htparam.flogical:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})
        ap_acct = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ap_acct)]})

        if not gl_acct:
            do_it = False

        if not do_it:

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
        ap_journal.bemerk = "Cancel Direct Issueing"

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    lscheinnr = docu_nr

    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "stt")]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    closedate = htparam.fdate

    for l_op in db_session.query(L_op).filter(
             (L_op.lief_nr == lief_nr) & (L_op.lscheinnr == (docu_nr).lower()) & ((L_op.op_art == 1) | (L_op.op_art == 3)) & (L_op.flag) & (L_op.loeschflag == 0) & (L_op.pos > 0)).order_by(L_op._recid).all():
        l_op.loeschflag = 2
        billdate = l_op.datum
        wert =  - to_decimal(l_op.warenwert)

        if l_op.op_art == 1:
            t_amount =  to_decimal(t_amount) + to_decimal(wert)

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op.lager_nr)],"artnr": [(eq, l_op.artnr)]})

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op.warenwert)
                pass

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_op.artnr)]})

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op.warenwert)
                pass
    update_ap()

    return generate_output()