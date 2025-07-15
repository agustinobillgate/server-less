from functions.additional_functions import *
import decimal
from datetime import date
from models import Kresline

def check_reservation(type:str, from_date:date, to_date:date, nr:int):
    ok_flag = False
    kresline = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, kresline
        nonlocal type, from_date, to_date, nr

        return {"ok_flag": ok_flag}

    ok_flag = False

    if type.lower()  == ("kabin").lower() :

        kresline = db_session.query(Kresline).filter(
                 ((Kresline.datum >= from_date) & (Kresline.datum <= to_date)) & (Kresline.kabnr == nr) & (Kresline.betriebsnr != 9)).first()

        if not kresline:
            ok_flag = True
        else:
            ok_flag = False

    elif type.lower()  == ("masseur").lower() :

        kresline = db_session.query(Kresline).filter(
                 ((Kresline.datum >= from_date) & (Kresline.datum <= to_date)) & (Kresline.massnr == nr) & (Kresline.betriebsnr != 9)).first()

        if not kresline:
            ok_flag = True
        else:
            ok_flag = False

    elif type.lower()  == ("treatment").lower() :

        kresline = db_session.query(Kresline).filter(
                 ((Kresline.datum >= from_date) & (Kresline.datum <= to_date)) & (Kresline.artnr == nr) & (Kresline.betriebsnr != 9)).first()

        if not kresline:
            ok_flag = True
        else:
            ok_flag = False

    elif type.lower()  == ("equipment").lower() :

        kresline = db_session.query(Kresline).filter(
                 ((Kresline.datum >= from_date) & (Kresline.datum <= to_date)) & (Kresline.buchart == nr) & (Kresline.betriebsnr != 9)).first()

        if not kresline:
            ok_flag = True
        else:
            ok_flag = False

    return generate_output()