from functions.additional_functions import *
import decimal
from models import Guestseg, Reservation, Guest, Segment

def create_gcfbl(gnat:str, gland:str, def_natcode:str, gastid:str, name:str, fname:str, ftitle:str, user_init:str, gphone:str, gastno:int, selected_gastnr:int):
    guestseg = reservation = guest = segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestseg, reservation, guest, segment
        nonlocal gnat, gland, def_natcode, gastid, name, fname, ftitle, user_init, gphone, gastno, selected_gastnr


        return {"gnat": gnat, "gland": gland, "selected_gastnr": selected_gastnr}

    def create_gcf():

        nonlocal guestseg, reservation, guest, segment
        nonlocal gnat, gland, def_natcode, gastid, name, fname, ftitle, user_init, gphone, gastno, selected_gastnr

        curr_gastnr:int = 0
        del_gastnr:int = 0
        gastsegm = None
        Gastsegm =  create_buffer("Gastsegm",Guestseg)

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == resnr)).first()
        curr_gastnr = 0

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr < 0)).first()

        if guest:
            curr_gastnr = - guest.gastnr
            db_session.delete(guest)

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == curr_gastnr)).first()

            if guest:
                curr_gastnr = 0

        if curr_gastnr == 0:

            guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

            if guest:
                curr_gastnr = guest.gastnr + 1
            else:
                curr_gastnr = 1

        if gnat == "":
            gnat = def_natcode

        if gland == "":
            gland = def_natcode
        guest = Guest()
        db_session.add(guest)

        guest.gastnr = curr_gastnr
        selected_gastnr = guest.gastnr
        guest.karteityp = 0
        guest.ausweis_nr1 = gastid
        guest.nation1 = gnat
        guest.land = gland
        guest.name = name
        guest.vorname1 = fname
        guest.anrede1 = ftitle
        guest.char1 = user_init
        guest.telefon = gphone

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

        if not guestseg:
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = guest.gastnr
            guestseg.reihenfolge = 1

        if reservation and reservation.segmentcode != 0:
            guestseg.segmentcode = reservation.segmentcode
        else:

            gastsegm = db_session.query(Gastsegm).filter(
                     (Gastsegm.gastnr == guest.gastnr) & (Gastsegm.reihenfolge == 1)).first()

            if not gastsegm:

                gastsegm = db_session.query(Gastsegm).filter(
                         (Gastsegm.gastnr == guest.gastnr)).first()

            if gastsegm:
                guestseg.segmentcode = gastsegm.segmentcode


            else:

                segment = db_session.query(Segment).first()
                guestseg.segmentcode = segment.segmentcode
        pass


    create_gcf()

    return generate_output()