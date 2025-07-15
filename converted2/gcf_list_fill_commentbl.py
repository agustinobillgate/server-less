#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Mc_guest

def gcf_list_fill_commentbl(pvilanguage:int, gastno:int):

    prepare_cache ([Guest])

    comments = ""
    lvcarea:string = "gcf-list"
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

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastno)],"activeflag": [(eq, True)]})

        if mc_guest:
            comments = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr_unicode(10)


        comments = comments + guest.bemerkung

        if guest.master_gastnr > 0:

            mguest = get_cache (Guest, {"gastnr": [(eq, guest.master_gastnr)]})

            if mguest:

                if comments == "":
                    comments = mguest.name + ", " + mguest.anredefirma
                else:
                    comments = mguest.name + ", " + mguest.anredefirma + chr_unicode(10) + comments


    fill_gcf_comments()

    return generate_output()