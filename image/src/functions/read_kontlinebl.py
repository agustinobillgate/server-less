from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kontline

def read_kontlinebl(case_type:int, kontignr:int, konstat:int, gastno:int, kontcode:str, datum:date):
    t_kontline_list = []
    curr_kontig:int = 0
    kontline = None

    t_kontline = None

    t_kontline_list, T_kontline = create_model_like(Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontline_list, curr_kontig, kontline


        nonlocal t_kontline
        nonlocal t_kontline_list
        return {"t-kontline": t_kontline_list}

    if kontignr < 0:
        curr_kontig = - kontignr
    else:
        curr_kontig = kontignr

    if case_type == 1:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == curr_kontig) &  (Kontline.kontstatus == konstat)).first()
    elif case_type == 2:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontstatus == konstat) &  (Kontline.datum >= Kontline.ankunft) &  (Kontline.datum <= Kontline.abreise)).first()
    elif case_type == 3:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == curr_kontig) &  (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontstatus == konstat)).first()
    elif case_type == 4:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (Kontline.kontignr == curr_kontig) &  (Kontline.kontstatus == konstat)).first()
    elif case_type == 5:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == curr_kontig) &  (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontstatus == konstat)).first()
    elif case_type == 6:

        if curr_kontig != 0 and curr_kontig != None:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.gastnr == gastno) &  (Kontline.kontignr == curr_kontig) &  (Kontline.kontstatus == konstat) &  (Kontline.betriebsnr == 1)).first()
        else:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.gastnr == gastno) &  (Kontline.kontignr > 0) &  (Kontline.kontstatus == konstat) &  (Kontline.betriebsnr == 1)).first()
    elif case_type == 7:

        if curr_kontig != 0 and curr_kontig != None:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.gastnr == gastno) &  (Kontline.kontignr == curr_kontig) &  (Kontline.kontstatus == konstat) &  (Kontline.betriebsnr == 0)).first()
        else:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.gastnr == gastno) &  (Kontline.kontignr > 0) &  (Kontline.kontstatus == konstat) &  (Kontline.betriebsnr == 0)).first()
    elif case_type == 8:

        kontline = db_session.query(Kontline).filter(
                (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.betriebsnr == 0) &  (Kontline.gastnr != gastno) &  (Kontline.gastnr > 0) &  (Kontline.kontstat == 1)).first()
    elif case_type == 9:

        kontline = db_session.query(Kontline).filter(
                (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.gastnr == gastno)).first()
    elif case_type == 10:

        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == kontignr) &  (Kontline.gastnr == gastno)).first()
    elif case_type == 11:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (Kontline.kontignr == kontignr) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).first()
    elif case_type == 12:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (Kontline.kontignr == kontignr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()
    elif case_type == 13:

        kontline = db_session.query(Kontline).filter(
                (Kontline.gastnr == gastno) &  (Kontline.betriebsnr == 1) &  (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.kontignr != kontignr) &  (Kontline.zikatnr != konstat) &  (Kontline.kontstat == 1)).first()
    elif case_type == 14:

        kontline = db_session.query(Kontline).filter(
                (func.lower(Kontline.(kontcode).lower()) == (kontcode).lower()) &  (Kontline.betriebsnr == 1) &  (Kontline.gastnr != gastno) &  (Kontline.gastnr > 0) &  (Kontline.kontstat == 1)).first()

    if kontline:
        t_kontline = T_kontline()
        t_kontline_list.append(t_kontline)

        buffer_copy(kontline, t_kontline)

    return generate_output()