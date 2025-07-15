#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Akt_kont

def read_akt_kontbl(case_type:int, gastno:int, userno:int, gname:string):
    t_akt_kont_data = []
    akt_kont = None

    t_akt_kont = None

    t_akt_kont_data, T_akt_kont = create_model_like(Akt_kont)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_kont_data, akt_kont
        nonlocal case_type, gastno, userno, gname


        nonlocal t_akt_kont
        nonlocal t_akt_kont_data

        return {"t-akt-kont": t_akt_kont_data}

    if case_type == 1:

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastno)],"kontakt_nr": [(eq, userno)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 2:

        for akt_kont in db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastno) & (Akt_kont.kontakt_nr >= 1)).order_by(Akt_kont.name).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 3:

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastno)],"hauptkontakt": [(eq, False)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 4:

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastno)],"hauptkontakt": [(eq, True)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 5:

        for akt_kont in db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastno) & (Akt_kont.kontakt_nr > 0) & (Akt_kont.name >= (gname).lower())).order_by(Akt_kont.name).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 6:

        for akt_kont in db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastno)).order_by(Akt_kont._recid).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 7:

        akt_kont = db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastno) & (Akt_kont.name == (gname).lower()) | ((Akt_kont.name + ", " + Akt_kont.anrede) == (gname).lower())).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 8:

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastno)],"name": [(eq, gname)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 9:

        akt_kont = db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastno) & (matches(gname,("*" + Akt_kont.name + "*"))) & (matches(gname,("*" + Akt_kont.vorname + "*")))).first()

        if not akt_kont:

            akt_kont = db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == gastno) & (matches(gname,("*" + Akt_kont.name + "*")))).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 10:

        akt_kont = get_cache (Akt_kont, {"betrieb_gast": [(eq, gastno)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 11:

        for akt_kont in db_session.query(Akt_kont).filter(
                 (Akt_kont.betrieb_gast == gastno)).order_by(Akt_kont._recid).all():
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 12:

        akt_kont = db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastno) & (substring(Akt_kont.abteilung, 0, 3) == (gname).lower())).first()

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)
    elif case_type == 13:

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastno)]})

        if akt_kont:
            t_akt_kont = T_akt_kont()
            t_akt_kont_data.append(t_akt_kont)

            buffer_copy(akt_kont, t_akt_kont)

    return generate_output()