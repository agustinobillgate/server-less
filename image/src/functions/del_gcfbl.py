from functions.additional_functions import *
import decimal
import re
from functions.delete_guestbookbl import delete_guestbookbl
from models import Guest, Res_line, Debitor, Akt_cust, Bill, Billhis, Kontline, Zimmer, Bk_veran, Mc_guest, Cl_member, Akt_kont, Htparam, Guestseg, History, Guest_pr, Gk_notes, Guestbud, Queasy

def del_gcfbl(gastnr:int):
    error_code = 0
    answer:bool = False
    gastno:str = ""
    guest = res_line = debitor = akt_cust = bill = billhis = kontline = zimmer = bk_veran = mc_guest = cl_member = akt_kont = htparam = guestseg = history = guest_pr = gk_notes = guestbud = queasy = None

    guest1 = None

    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, answer, gastno, guest, res_line, debitor, akt_cust, bill, billhis, kontline, zimmer, bk_veran, mc_guest, cl_member, akt_kont, htparam, guestseg, history, guest_pr, gk_notes, guestbud, queasy
        nonlocal guest1


        nonlocal guest1
        return {"error_code": error_code}

    def check_global_allotment():

        nonlocal error_code, answer, gastno, guest, res_line, debitor, akt_cust, bill, billhis, kontline, zimmer, bk_veran, mc_guest, cl_member, akt_kont, htparam, guestseg, history, guest_pr, gk_notes, guestbud, queasy
        nonlocal guest1


        nonlocal guest1

        error_code = 0
        tokcounter:int = 0
        mesvalue:str = ""

        def generate_inner_output():
            return error_code

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 147)).all():
            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if mesvalue != "" and to_int(mesvalue) == gastnr:
                    error_code = 66
                    break


        return generate_inner_output()


    res_line = db_session.query(Res_line).filter(
            (Res_line.gastnr == gastnr)).first()

    if res_line:
        error_code = 1

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.gastnrmember == gastnr)).first()

    if res_line:
        error_code = 1

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.gastnrpay == gastnr)).first()

    if res_line:
        error_code = 1

        return generate_output()

    debitor = db_session.query(Debitor).filter(
            (Debitor.gastnr == gastnr) &  (Debitor.zahlkonto == 0)).first()

    if debitor:
        error_code = 2

        return generate_output()

    debitor = db_session.query(Debitor).filter(
            (Debitor.gastnrmember == gastnr) &  (Debitor.zahlkonto == 0)).first()

    if debitor:
        error_code = 2

        return generate_output()

    guest1 = db_session.query(Guest1).filter(
            (Guest1.master_gastnr == gastnr) &  (Guest1.gastnr > 0)).first()

    if guest1:
        error_code = 3

        return generate_output()

    akt_cust = db_session.query(Akt_cust).filter(
            (Akt_cust.gastnr == gastnr)).first()

    if akt_cust:
        error_code = 4

        return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill.gastnr == gastnr)).first()

    if bill:
        error_code = 5

        return generate_output()

    billhis = db_session.query(Billhis).filter(
            (Billhis.gastnr == gastnr)).first()

    if billhis:
        error_code = 5

        return generate_output()

    kontline = db_session.query(Kontline).filter(
            (Kontline.gastnr == gastnr)).first()

    if kontline:
        error_code = 6

        return generate_output()
    error_code = check_global_allotment()

    if error_code > 0:

        return generate_output()

    zimmer = db_session.query(Zimmer).filter(
            (Zimmer.owner_nr == gastnr)).first()

    if zimmer:
        error_code = 7

        return generate_output()

    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.gastnr == gastnr)).first()

    if bk_veran:
        error_code = 8

        return generate_output()

    mc_guest = db_session.query(Mc_guest).filter(
            (Mc_guest.gastnr == gastnr)).first()

    if mc_guest:
        error_code = 9

        return generate_output()

    cl_member = db_session.query(Cl_member).filter(
            (Cl_member.gastnr == gastnr)).first()

    if cl_member:
        error_code = 10

        return generate_output()

    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.betrieb_gast == gastnr)).first()

    if akt_kont:
        error_code = 11

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 615)).first()

    if htparam:
        gastno = "*" + to_string(gastnr) + "*"

        if re.match(gastno,htparam.fchar):
            error_code = 12

            return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    guest = db_session.query(Guest).first()

    for guestseg in db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr)).all():
        db_session.delete(guestseg)

    for history in db_session.query(History).filter(
                (History.gastnr == guest.gastnr)).all():
        db_session.delete(history)

    for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == guest.gastnr)).all():
        db_session.delete(guest_pr)

    for gk_notes in db_session.query(Gk_notes).filter(
                (Gk_notes.gastnr == guest.gastnr)).all():
        db_session.delete(gk_notes)

    for guestbud in db_session.query(Guestbud).filter(
                (Guestbud.gastnr == guest.gastnr)).all():
        db_session.delete(guestbud)

    for akt_kont in db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == guest.gastnr)).all():
        db_session.delete(akt_kont)

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 472)).first()

    if htparam.flogical:
        get_output(delete_guestbookbl(guest.gastnr))
    db_session.delete(guest)

    return generate_output()