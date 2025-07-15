#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.mobile_prepare_hk_statadminbl import mobile_prepare_hk_statadminbl
from models import Zimkateg, Queasy, Bediener

def hk_get_statusbl():

    prepare_cache ([Queasy, Bediener])

    ci_date = None
    z_list_data = []
    om_list_data = []
    bline_list_data = []
    setup_list_data = []
    t_zimkateg_data = []
    zimkateg = queasy = bediener = None

    t_zimkateg = t_z_list = z_list = om_list = bline_list = setup_list = None

    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)
    t_z_list_data, T_z_list = create_model("T_z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string})
    z_list_data, Z_list = create_model("Z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string, "id":string, "pic":string})
    om_list_data, Om_list = create_model("Om_list", {"zinr":string, "ind":int})
    bline_list_data, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, z_list_data, om_list_data, bline_list_data, setup_list_data, t_zimkateg_data, zimkateg, queasy, bediener


        nonlocal t_zimkateg, t_z_list, z_list, om_list, bline_list, setup_list
        nonlocal t_zimkateg_data, t_z_list_data, z_list_data, om_list_data, bline_list_data, setup_list_data

        return {"ci_date": ci_date, "z-list": z_list_data, "om-list": om_list_data, "bline-list": bline_list_data, "setup-list": setup_list_data, "t-zimkateg": t_zimkateg_data}

    ci_date, t_z_list_data, om_list_data, bline_list_data, setup_list_data, t_zimkateg_data = get_output(mobile_prepare_hk_statadminbl("", 0, 0, 0))

    for t_z_list in query(t_z_list_data):
        z_list = Z_list()
        z_list_data.append(z_list)

        buffer_copy(t_z_list, z_list)

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 196) & (Queasy.date1 == ci_date) & (entry (0, Queasy.char1, ";") == z_list.zinr)).first()

        if queasy:
            z_list.id = entry(1, queasy.char1, ";")

            bediener = get_cache (Bediener, {"userinit": [(eq, z_list.id)]})

            if bediener:
                z_list.pic = bediener.username

    return generate_output()