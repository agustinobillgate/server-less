from functions.additional_functions import *
import decimal
from datetime import date
from functions.mobile_prepare_hk_statadminbl import mobile_prepare_hk_statadminbl
from models import Zimkateg, Queasy, Bediener

def hk_get_statusbl():
    ci_date = None
    z_list_list = []
    om_list_list = []
    bline_list_list = []
    setup_list_list = []
    t_zimkateg_list = []
    zimkateg = queasy = bediener = None

    t_zimkateg = t_z_list = z_list = om_list = bline_list = setup_list = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    t_z_list_list, T_z_list = create_model("T_z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})
    z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str, "id":str, "pic":str})
    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
    bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, z_list_list, om_list_list, bline_list_list, setup_list_list, t_zimkateg_list, zimkateg, queasy, bediener


        nonlocal t_zimkateg, t_z_list, z_list, om_list, bline_list, setup_list
        nonlocal t_zimkateg_list, t_z_list_list, z_list_list, om_list_list, bline_list_list, setup_list_list
        return {"ci_date": ci_date, "z-list": z_list_list, "om-list": om_list_list, "bline-list": bline_list_list, "setup-list": setup_list_list, "t-zimkateg": t_zimkateg_list}

    ci_date, t_z_list_list, om_list_list, bline_list_list, setup_list_list, t_zimkateg_list = get_output(mobile_prepare_hk_statadminbl("", 0, 0, 0))

    for t_z_list in query(t_z_list_list):
        z_list = Z_list()
        z_list_list.append(z_list)

        buffer_copy(t_z_list, z_list)

        # if not queasy or not(queasy.key == 196 and queasy.date1 == ci_date and entry (0, queasy.char1, ";") == z_list.zinr):
        #     queasy = db_session.query(Queasy).filter(
        #         (Queasy.key == 196) &  
        #         (Queasy.date1 == ci_date) &  
        #         (entry (0, Queasy.char1, ";") == z_list.zinr)
        #         ).first()
        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 196) &  
                (Queasy.date1 == ci_date) 
                # & ((entry (0, Queasy.char1, ";")) == z_list.zinr)
                ).first()
        if queasy:
            local_storage.debugging = local_storage.debugging + ","+ queasy.char1
            if ((entry (0, queasy.char1, ";")) == z_list.zinr):
                z_list.id = entry(1, queasy.char1, ";")

                if not bediener or not(bediener.userinit == z_list.id):
                    bediener = db_session.query(Bediener).filter(
                        (Bediener.userinit == z_list.id)).first()

                if bediener:
                    z_list.pic = bediener.username

    return generate_output()