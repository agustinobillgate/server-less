#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy, Paramtext

def prepare_setup_roombl():
    rmcat_list = []
    bed_setup_list = []
    rmtype_list = []
    t_queasy_list = []
    t_paramtext_list = []
    guest_pref_list = []
    zimkateg = queasy = paramtext = None

    rmcat = bed_setup = rmtype = t_queasy = t_paramtext = guest_pref = None

    rmcat_list, Rmcat = create_model("Rmcat", {"nr":int, "code":string})
    bed_setup_list, Bed_setup = create_model("Bed_setup", {"nr":int, "bezeich":string, "bed_code":string})
    rmtype_list, Rmtype = create_model_like(Zimkateg)
    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_paramtext_list, T_paramtext = create_model_like(Paramtext)
    guest_pref_list, Guest_pref = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_list, bed_setup_list, rmtype_list, t_queasy_list, t_paramtext_list, guest_pref_list, zimkateg, queasy, paramtext


        nonlocal rmcat, bed_setup, rmtype, t_queasy, t_paramtext, guest_pref
        nonlocal rmcat_list, bed_setup_list, rmtype_list, t_queasy_list, t_paramtext_list, guest_pref_list

        return {"rmcat": rmcat_list, "bed-setup": bed_setup_list, "rmtype": rmtype_list, "t-queasy": t_queasy_list, "t-paramtext": t_paramtext_list, "guest-pref": guest_pref_list}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy._recid).all():
        rmcat = Rmcat()
        rmcat_list.append(rmcat)

        rmcat.nr = queasy.number1
        rmcat.code = queasy.char1

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
        bed_setup = Bed_setup()
        bed_setup_list.append(bed_setup)

        bed_setup.nr = paramtext.txtnr - 9200
        bed_setup.bezeich = paramtext.ptexte
        bed_setup.bed_code = paramtext.notes

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        rmtype = Rmtype()
        rmtype_list.append(rmtype)

        buffer_copy(zimkateg, rmtype)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 189) & (Queasy.logi2)).order_by(Queasy._recid).all():
        guest_pref = Guest_pref()
        guest_pref_list.append(guest_pref)

        buffer_copy(queasy, guest_pref)

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 230) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
        t_paramtext = T_paramtext()
        t_paramtext_list.append(t_paramtext)

        buffer_copy(paramtext, t_paramtext)

    return generate_output()