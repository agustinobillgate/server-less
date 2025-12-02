#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Nation, Prmarket, Guest, Htparam

def nation_admin_check1bl(pvilanguage:int, rec_id:int, kurzbez:string, nationnr:int, natbez:string, untergruppe:int, hauptgruppe:int, language:int, marksegm:string):

    prepare_cache ([Nation, Prmarket, Guest, Htparam])

    msg_str = ""
    lvcarea:string = "nation-admin-check"
    nation = prmarket = guest = htparam = None

    db_session = local_storage.db_session
    kurzbez = kurzbez.strip()
    natbez = natbez.strip()
    marksegm = marksegm.strip()

    def generate_output():
        nonlocal msg_str, lvcarea, nation, prmarket, guest, htparam
        nonlocal pvilanguage, rec_id, kurzbez, nationnr, natbez, untergruppe, hauptgruppe, language, marksegm

        return {"msg_str": msg_str}

    def fill_new_nation():

        nonlocal msg_str, lvcarea, nation, prmarket, guest, htparam
        nonlocal pvilanguage, rec_id, kurzbez, nationnr, natbez, untergruppe, hauptgruppe, language, marksegm

        nation.nationnr = nationnr
        nation.kurzbez = kurzbez
        nation.bezeich = natbez
        nation.untergruppe = untergruppe
        nation.hauptgruppe = hauptgruppe
        nation.language = language

        prmarket = get_cache (Prmarket, {"bezeich": [(eq, marksegm)]})

        if prmarket:
            nation.bezeich = nation.bezeich + ";" + to_string(prmarket.nr)


    def update_nationcode():

        nonlocal msg_str, lvcarea, nation, prmarket, guest, htparam
        nonlocal pvilanguage, rec_id, kurzbez, nationnr, natbez, untergruppe, hauptgruppe, language, marksegm

        curr_gastnr:int = 0
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)

        guest = db_session.query(Guest).filter(
                 ((Guest.gastnr > curr_gastnr)) & (((Guest.nation1 == nation.kurzbez)) | ((Guest.land == nation.kurzbez)))).first()
        while None != guest:
            curr_gastnr = guest.gastnr

            # gbuff = get_cache (Guest, {"_recid": [(eq, guest._recid)]})
            gbuff = db_session.query(Guest).filter(
                     (Guest._recid == guest._recid)).with_for_update().first()

            if guest.nation1 == nation.kurzbez:
                gbuff.nation1 = kurzbez

            if guest.land == nation.kurzbez:
                gbuff.land = kurzbez
            pass
            pass

            curr_recid = guest._recid
            guest = db_session.query(Guest).filter(
                     ((Guest.gastnr > curr_gastnr)) & (((Guest.nation1 == nation.kurzbez)) | ((Guest.land == nation.kurzbez))) & (Guest._recid > curr_recid)).first()

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})
        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 153)).with_for_update().first()

        if htparam.fchar == nation.kurzbez:
            pass
            htparam.fchar = kurzbez


            pass

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 276)]})
        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 276)).with_for_update().first()

        if htparam.fchar == nation.kurzbez:
            pass
            htparam.fchar = kurzbez


            pass

    nation = get_cache (Nation, {"kurzbez": [(eq, kurzbez)],"natcode": [(eq, 0)],"_recid": [(ne, rec_id)]})

    if nation and kurzbez != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Nation code already exists, use other code.", lvcarea, "")

        return generate_output()

    nation = db_session.query(Nation).filter(
             (Nation.kurzbez == (kurzbez).lower()) & (Nation.natcode > 0)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("nation code used for a region code, use other code.", lvcarea, "")

        return generate_output()

    if msg_str == "":

        # nation = get_cache (Nation, {"_recid": [(eq, rec_id)]})
        nation = db_session.query(Nation).filter(
                 (Nation._recid == rec_id)).with_for_update().first()

        if nation.kurzbez.lower()  != (kurzbez).lower() :
            update_nationcode()
        pass
        fill_new_nation()

    return generate_output()