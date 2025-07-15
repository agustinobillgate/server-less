#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.delete_guestbookbl import delete_guestbookbl
from models import Guest, Queasy, Guestseg, History, Guest_pr, Gk_notes, Guestbud, Akt_kont, Htparam, Bediener, Res_history

def gcf_deletebl(userinit:string, gastnr:int):

    prepare_cache ([Bediener, Res_history])

    gastno:string = ""
    guest = queasy = guestseg = history = guest_pr = gk_notes = guestbud = akt_kont = htparam = bediener = res_history = None

    guest1 = tqueasy = None

    Guest1 = create_buffer("Guest1",Guest)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastno, guest, queasy, guestseg, history, guest_pr, gk_notes, guestbud, akt_kont, htparam, bediener, res_history
        nonlocal userinit, gastnr
        nonlocal guest1, tqueasy


        nonlocal guest1, tqueasy

        return {}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    pass

    for guestseg in db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == guest.gastnr)).order_by(Guestseg._recid).all():
        db_session.delete(guestseg)

    for history in db_session.query(History).filter(
                 (History.gastnr == guest.gastnr)).order_by(History._recid).all():
        db_session.delete(history)

    for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr._recid).all():
        db_session.delete(guest_pr)

    for gk_notes in db_session.query(Gk_notes).filter(
                 (Gk_notes.gastnr == guest.gastnr)).order_by(Gk_notes._recid).all():
        db_session.delete(gk_notes)

    for guestbud in db_session.query(Guestbud).filter(
                 (Guestbud.gastnr == guest.gastnr)).order_by(Guestbud._recid).all():
        db_session.delete(guestbud)

    for akt_kont in db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == guest.gastnr)).order_by(Akt_kont._recid).all():
        db_session.delete(akt_kont)

    for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 231) & (Queasy.number1 == guest.gastnr)).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    for tqueasy in db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 212) & (Tqueasy.number3 == guest.gastnr)).order_by(Tqueasy._recid).all():
        db_session.delete(tqueasy)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 472)]})

    if htparam.flogical:
        get_output(delete_guestbookbl(guest.gastnr))
    db_session.delete(guest)
    pass

    bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Delete GuestCard: gastno " + to_string(gastnr)
    res_history.action = "GuestFile"


    pass
    pass

    return generate_output()