# using conversion tools version: 1.0.0.119
"""_yusufwijasena_18/11/2025

    Ticket ID: 20FD2B
        remark: - fix python indentation
                - fix AppServer connection
                - fix log & errormsg 
"""
from functions.additional_functions import *
from decimal import Decimal
from functions.prepare_get_elearningbl_hdesk import prepare_get_elearningbl_hdesk


def prepare_get_faq_elearningbl():
    happparam: string = ""
    lreturn_hdesk: bool = False
    tot_video = 0
    errormsg = ""
    module_list_data = []

    module_list = None

    module_list_data, Module_list = create_model(
        "Module_list",
        {
            "module_no": int,
            "module_name": string
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal happparam, lreturn_hdesk, tot_video, errormsg, module_list_data

        nonlocal module_list
        nonlocal module_list_data

        return {
            "tot_video": tot_video,
            "errormsg": errormsg,
            "module-list": module_list_data
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
    #     GET_MESSAGE(1) != '':
    #     errormsg = "ERROR|" + ERROR_STATUS: GET_MESSAGE(1)

    if err != "":
        errormsg = f"ERROR|{err}"
        
    if not lreturn_hdesk:
        errormsg = errormsg + " ERROR|Can not connect to the AppServer."

    if errormsg != "":
        # logmess(errormsg)
        print(f"LOG: {errormsg}")

    if lreturn_hdesk:
        local_storage.combo_flag = True
        tot_video, module_list_data = get_output(
            prepare_get_elearningbl_hdesk())
        local_storage.combo_flag = False

    lreturn_hdesk = hServer_hdesk.disconect()

    return generate_output()
