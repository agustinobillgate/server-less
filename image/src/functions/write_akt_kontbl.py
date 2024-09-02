from functions.additional_functions import *
import decimal
from models import Akt_kont

def write_akt_kontbl(case_type:int, t_akt_kont:[T_akt_kont]):
    success_flag = False
    akt_kont = None

    t_akt_kont = None

    t_akt_kont_list, T_akt_kont = create_model_like(Akt_kont)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akt_kont


        nonlocal t_akt_kont
        nonlocal t_akt_kont_list
        return {"success_flag": success_flag}

    if case_type == 1:

        t_akt_kont = query(t_akt_kont_list, first=True)

        if not t_akt_kont:

            return generate_output()

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == t_Akt_kont.gastnr) &  (Akt_kont.kontakt_nr == t_Akt_kont.kontakt_nr)).first()

        if not akt_kont:
            akt_kont = Akt_kont()
        db_session.add(akt_kont)

        buffer_copy(t_akt_kont, akt_kont)

        akt_kont = db_session.query(Akt_kont).first()
        success_flag = True
    elif case_type == 2:

        t_akt_kont = query(t_akt_kont_list, first=True)

        if not t_akt_kont:

            return generate_output()

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == t_Akt_kont.gastnr) &  (Akt_kont.kontakt_nr == t_Akt_kont.kontakt_nr)).first()

        if akt_kont:
            db_session.delete(akt_kont)

            success_flag = True
    elif case_type == 3:

        t_akt_kont = query(t_akt_kont_list, first=True)

        if not t_akt_kont:

            return generate_output()
        akt_kont = Akt_kont()
        db_session.add(akt_kont)

        buffer_copy(t_akt_kont, akt_kont)
        success_flag = True

    return generate_output()