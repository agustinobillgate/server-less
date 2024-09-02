from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_kont

def read_akt_kontbl(case_type:int, gastno:int, userno:int, gname:str):
    t_akt_kont_list = []
    akt_kont = None

    t_akt_kont = None

    t_akt_kont_list, T_akt_kont = create_model_like(Akt_kont)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_kont_list, akt_kont


        nonlocal t_akt_kont
        nonlocal t_akt_kont_list
        return {"t-akt-kont": t_akt_kont_list}

    if case_type == 1:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (Akt_kont.kontakt_nr == userno)).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 2:

        for akt_kont in db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (Akt_kont.kontakt_nr >= 1)).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 3:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (Akt_kont.hauptkontakt == False)).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 4:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (Akt_kont.hauptkontakt)).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 5:

        for akt_kont in db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (Akt_kont.kontakt_nr > 0) &  (func.lower(Akt_kont.name) >= (gname).lower())).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 6:

        for akt_kont in db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno)).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 7:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (func.lower(Akt_kont.name) == (gname).lower()) |  ((func.lower(Akt_kont.name) + ", " + Akt_kont.anrede) == (gname).lower())).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 8:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (func.lower(Akt_kont.name) == (gname).lower())).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 9:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (gname.op("~")(".*" + Akt_kont.name + ".*")) &  (gname.op("~")(".*" + Akt_kont.vorname + ".*"))).first()

        if not akt_kont:

            akt_kont = db_session.query(Akt_kont).filter(
                    (Akt_kont.gastnr == gastno) &  (gname.op("~")(".*" + Akt_kont.name + ".*"))).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 10:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.betrieb_gast == gastno)).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 11:

        for akt_kont in db_session.query(Akt_kont).filter(
                (Akt_kont.betrieb_gast == gastno)).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 12:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno) &  (substring(Akt_kont.abteilung, 0, 3) == (gname).lower())).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 13:

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastno)).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_list.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)

    return generate_output()