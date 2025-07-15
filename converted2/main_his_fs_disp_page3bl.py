#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def main_his_fs_disp_page3bl():

    prepare_cache ([Queasy])

    strktext = ""
    i:int = 0
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal strktext, i, queasy

        return {"strktext": strktext}

    strktext = ""
    for i in range(1,12 + 1) :

        queasy = get_cache (Queasy, {"key": [(eq, 148)],"char3": [(ne, "")],"number1": [(eq, i)]})

        if queasy:
            strktext = strktext + "[" + to_string(i) + "] " + queasy.char3 + chr_unicode(2)
        else:

            if i == 1:
                strktext = strktext + "[1] Banquet Instructions" + chr_unicode(2)

            if i == 2:
                strktext = strktext + "[2] F/O Instructions" + chr_unicode(2)

            if i == 3:
                strktext = strktext + "[3] Kitchen Instructions" + chr_unicode(2)

            if i == 4:
                strktext = strktext + "[4] House-Keeping Instructions" + chr_unicode(2)

            if i == 5:
                strktext = strktext + "[5] Steward Instructions" + chr_unicode(2)

            if i == 6:
                strktext = strktext + "[6] Engineering Instructions" + chr_unicode(2)

            if i == 7:
                strktext = strktext + "[7] Restaurant Instructions" + chr_unicode(2)

            if i == 8:
                strktext = strktext + "[8] Security Instructions" + chr_unicode(2)

            if i == 9:
                strktext = strktext + "[9] Bar Instructions" + chr_unicode(2)

            if i == 10:
                strktext = strktext + "[10] MCM Instructions" + chr_unicode(2)

            if i == 11:
                strktext = strktext + "[11] Sales & Marketing" + chr_unicode(2)

            if i == 12:
                strktext = strktext + "[12] Order Taken By" + chr_unicode(2)

    return generate_output()