from functions.additional_functions import *
import decimal
from models import Guest, Mc_guest

def gcf_list_fill_commentbl(pvilanguage:int, gastno:int):
    comments = ""
    lvcarea:str = "gcf-list"
    guest = mc_guest = None

    mguest = None

    Mguest = create_buffer("Mguest",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal comments, lvcarea, guest, mc_guest
        nonlocal pvilanguage, gastno
        nonlocal mguest


        nonlocal mguest
        return {"comments": comments}

    def fill_gcf_comments():

        nonlocal comments, lvcarea, guest, mc_guest
        nonlocal pvilanguage, gastno
        nonlocal mguest


        nonlocal mguest


        comments = ""

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastno)).first()

        mc_guest = db_session.query(Mc_guest).filter(
                 (Mc_guest.gastnr == gastno) & (Mc_guest.activeflag)).first()

        if mc_guest:
            comments = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr(10)


        comments = comments + guest.bemerk

        if guest.master_gastnr > 0:

            mguest = db_session.query(Mguest).filter(
                     (Mguest.gastnr == guest.master_gastnr)).first()

            if mguest:

                if comments == "":
                    comments = mguest.name + ", " + mguest.anredefirma
                else:
                    comments = mguest.name + ", " + mguest.anredefirma + chr(10) + comments


    fill_gcf_comments()

    return generate_output()