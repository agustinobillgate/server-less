# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        remark: - fix python indentation
                - fix AppServer connection
                - fix log & errormsg 
"""
from functions.additional_functions import *
from decimal import Decimal
from functions.get_data_elearningbl_hdesk import get_data_elearningbl_hdesk


def get_data_faq_elearningbl(keysearch: str, module: int):
    errormsg = ""
    tlist_data = []
    happparam = ""
    lreturn_hdesk: bool = False

    tlist = None

    tlist_data, Tlist = create_model(
        "Tlist",
        {
            "number": int,
            "ttitle": string,
            "url_video": string,
            "module": string,
            "sub_module": string
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal errormsg, tlist_data, happparam, lreturn_hdesk
        nonlocal keysearch, module

        nonlocal tlist
        nonlocal tlist_data

        return {
            "errormsg": errormsg,
            "tlist": tlist_data
        }

    happparam = " -H hdesk.e1-vhp.com -S 3099 -DirectConnect -sessionModel Session-free"

    # CREATE SERVER hServer-hdesk.
    class AppServer:
        def connect(self, params):
            return True, ""
        
        def disconect(self):
            pass
        
    hServer_hdesk = AppServer()
    # lreturn_hdesk = hServer_hdesk: CONNECT(happparam, None, None, None)
    lreturn_hdesk, err = hServer_hdesk.connect(happparam)


    # if ERROR_STATUS:
        # GET_MESSAGE(1) != '':
        # errormsg = "ERROR|" + ERROR_STATUS: GET_MESSAGE(1)
    if err != '':
        errormsg = f"ERROR|{err}"

    if not lreturn_hdesk:
    #     errormsg = errormsg + " ERROR|Can not connect to the AppServer."
        errormsg += " ERROR|Can not connect to the AppServer."

    if errormsg != "":
        print(f"LOG: {errormsg}")

    if lreturn_hdesk:
        tlist_data.clear()

        if keysearch is None:
            keysearch = ""

        local_storage.combo_flag = True
        tlist_data = get_output(get_data_elearningbl_hdesk(keysearch, module))
        local_storage.combo_flag = False

    # lreturn_hdesk = hServer_hdesk: DISCONNECT()
    lreturn_hdesk = hServer_hdesk.disconect()

    return generate_output()
