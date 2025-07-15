#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy, Paramtext

def prepare_setup_roombl():
    rmcat_data = []
    bed_setup_data = []
    rmtype_data = []
    t_queasy_data = []
    t_paramtext_data = []
    guest_pref_data = []
    zimkateg = queasy = paramtext = None

    rmcat = bed_setup = rmtype = t_queasy = t_paramtext = guest_pref = None

    rmcat_data, Rmcat = create_model("Rmcat", {"nr":int, "code":string})
    bed_setup_data, Bed_setup = create_model("Bed_setup", {"nr":int, "bezeich":string, "bed_code":string})
    rmtype_data, Rmtype = create_model_like(Zimkateg)
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_paramtext_data, T_paramtext = create_model_like(Paramtext)
    guest_pref_data, Guest_pref = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmcat_data, bed_setup_data, rmtype_data, t_queasy_data, t_paramtext_data, guest_pref_data, zimkateg, queasy, paramtext


        nonlocal rmcat, bed_setup, rmtype, t_queasy, t_paramtext, guest_pref
        nonlocal rmcat_data, bed_setup_data, rmtype_data, t_queasy_data, t_paramtext_data, guest_pref_data

        return {"rmcat": rmcat_data, "bed-setup": bed_setup_data, "rmtype": rmtype_data, "t-queasy": t_queasy_data, "t-paramtext": t_paramtext_data, "guest-pref": guest_pref_data}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy._recid).all():
        rmcat = Rmcat()
        rmcat_data.append(rmcat)

        rmcat.nr = queasy.number1
        rmcat.code = queasy.char1

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
        bed_setup = Bed_setup()
        bed_setup_data.append(bed_setup)

        bed_setup.nr = paramtext.txtnr - 9200
        bed_setup.bezeich = paramtext.ptexte
        bed_setup.bed_code = paramtext.notes

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        rmtype = Rmtype()
        rmtype_data.append(rmtype)

        buffer_copy(zimkateg, rmtype)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 189) & (Queasy.logi2)).order_by(Queasy._recid).all():
        guest_pref = Guest_pref()
        guest_pref_data.append(guest_pref)

        buffer_copy(queasy, guest_pref)

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 230) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
        t_paramtext = T_paramtext()
        t_paramtext_data.append(t_paramtext)

        buffer_copy(paramtext, t_paramtext)

    return generate_output()