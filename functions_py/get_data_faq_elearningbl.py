#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from functions.get_data_elearningbl_hdesk import get_data_elearningbl_hdesk

def get_data_faq_elearningbl(keysearch:string, module:int):
    errormsg = ""
    tlist_data = []
    happparam:string = ""
    lreturn_hdesk:bool = False

    tlist = None

    tlist_data, Tlist = create_model("Tlist", {"number":int, "ttitle":string, "url_video":string, "module":string, "sub_module":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal errormsg, tlist_data, happparam, lreturn_hdesk
        nonlocal keysearch, module


        nonlocal tlist
        nonlocal tlist_data

        return {"errormsg": errormsg, "tlist": tlist_data}


    happparam = " -H hdesk.e1-vhp.com -S 3099" + " -DirectConnect -sessionModel Session-free"


    lreturn_hdesk = hServer_hdesk:CONNECT (happparam, None , None , None)

    if ERROR_STATUS:GET_MESSAGE (1) != '':
        errormsg = "ERROR|" + ERROR_STATUS:GET_MESSAGE (1)

    if not lreturn_hdesk:
        errormsg = errormsg + " ERROR|Can not connect to the AppServer."

    if errormsg != "":
        logmess(errormsg)

    if lreturn_hdesk:
        tlist_data.clear()

        if keysearch == None:
            keysearch = ""


        local_storage.combo_flag = True
        tlist_data = get_output(get_data_elearningbl_hdesk(keysearch, module))
        local_storage.combo_flag = False

    lreturn_hdesk = hServer_hdesk:DISCONNECT()


    return generate_output()