from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation, Prmarket, Guest, Htparam

def nation_admin_check1bl(pvilanguage:int, rec_id:int, kurzbez:str, nationnr:int, natbez:str, untergruppe:int, hauptgruppe:int, language:int, marksegm:str):
    msg_str = ""
    lvcarea:str = "nation_admin_check"
    nation = prmarket = guest = htparam = None

    gbuff = None

    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, nation, prmarket, guest, htparam
        nonlocal gbuff


        nonlocal gbuff
        return {"msg_str": msg_str}

    def fill_new_nation():

        nonlocal msg_str, lvcarea, nation, prmarket, guest, htparam
        nonlocal gbuff


        nonlocal gbuff


        nationnr = nationnr
        nation.kurzbez = kurzbez
        nation.bezeich = natbez
        nation.untergruppe = untergruppe
        nation.hauptgruppe = hauptgruppe
        nation.language = language

        prmarket = db_session.query(Prmarket).filter(
                (func.lower(Prmarket.bezeich) == (marksegm).lower())).first()

        if prmarket:
            nation.bezeich = nation.bezeich + ";" + to_string(prmarket.nr)

    def update_nationcode():

        nonlocal msg_str, lvcarea, nation, prmarket, guest, htparam
        nonlocal gbuff


        nonlocal gbuff

        curr_gastnr:int = 0
        Gbuff = Guest

        guest = db_session.query(Guest).filter(
                ((Guest.gastnr > curr_gastnr)) &  (((Guest.nation1 == nation.kurzbez)) |  ((Guest.land == nation.kurzbez)))).first()
        while None != guest:
            curr_gastnr = guest.gastnr

            gbuff = db_session.query(Gbuff).filter(
                        (Gbuff._recid == guest._recid)).first()

            if guest.nation1 == nation.kurzbez:
                gbuff.nation1 = kurzbez

            if guest.land == nation.kurzbez:
                gbuff.land = kurzbez

            gbuff = db_session.query(Gbuff).first()

            guest = db_session.query(Guest).filter(
                    ((Guest.gastnr > curr_gastnr)) &  (((Guest.nation1 == nation.kurzbez)) |  ((Guest.land == nation.kurzbez)))).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 153)).first()

        if htparam.fchar == nation.kurzbez:

            htparam = db_session.query(Htparam).first()
            htparam.fchar = kurzbez

            htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 276)).first()

        if htparam.fchar == nation.kurzbez:

            htparam = db_session.query(Htparam).first()
            htparam.fchar = kurzbez

            htparam = db_session.query(Htparam).first()


    nation = db_session.query(Nation).filter(
            (func.lower(Nation.(kurzbez).lower()) == (kurzbez).lower()) &  (Nation.natcode == 0) &  (Nation._recid != rec_id)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr(2) + translateExtended ("Nation code already exists, use other code.", lvcarea, "")

        return generate_output()

    nation = db_session.query(Nation).filter(
            (func.lower(Nation.(kurzbez).lower()) == (kurzbez).lower()) &  (Nation.natcode > 0)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr(2) + translateExtended ("nation code used for a region code, use other code.", lvcarea, "")

        return generate_output()

    if msg_str == "":

        nation = db_session.query(Nation).filter(
                (Nation._recid == rec_id)).first()

        if nation.(kurzbez).lower().lower()  != (kurzbez).lower() :
            update_nationcode()

        nation = db_session.query(Nation).first()
        fill_new_nation()

    return generate_output()