#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Guestseg, Guest, Segment

def create_gcfbl(gnat:string, gland:string, def_natcode:string, gastid:string, name:string, fname:string, ftitle:string, user_init:string, gphone:string, gastno:int, selected_gastnr:int):

    prepare_cache ([Guestseg, Segment])

    guestseg = guest = segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestseg, guest, segment
        nonlocal gnat, gland, def_natcode, gastid, name, fname, ftitle, user_init, gphone, gastno, selected_gastnr

        return {"gnat": gnat, "gland": gland, "selected_gastnr": selected_gastnr}

    def create_gcf():

        nonlocal guestseg, guest, segment
        nonlocal gnat, gland, def_natcode, gastid, name, fname, ftitle, user_init, gphone, gastno, selected_gastnr

        curr_gastnr:int = 0
        del_gastnr:int = 0
        gastsegm = None
        Gastsegm =  create_buffer("Gastsegm",Guestseg)
        curr_gastnr = 0

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr < 0)).first()

        if guest:
            curr_gastnr = - guest.gastnr
            db_session.delete(guest)

            guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)]})

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


        pass

        # guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})
        guestseg = db_session.query(Gastsegm).filter(
                 (Gastsegm.gastnr == guest.gastnr),
                 (Gastsegm.reihenfolge == 1)).with_for_update().first()

        if not guestseg:
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = guest.gastnr
            guestseg.reihenfolge = 1

        gastsegm = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

        if not gastsegm:

            gastsegm = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})

        if gastsegm:
            guestseg.segmentcode = gastsegm.segmentcode


        else:

            segment = db_session.query(Segment).first()

            if segment:
                guestseg.segmentcode = segment.segmentcode
        pass
        pass


    create_gcf()

    return generate_output()