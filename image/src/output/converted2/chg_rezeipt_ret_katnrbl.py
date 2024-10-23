from functions.additional_functions import *
import decimal
from models import H_rezept

def chg_rezeipt_ret_katnrbl(katnr:int):
    avail_h_rez = False
    o_bezeich = ""
    h_rezept = None

    h_rez = None

    H_rez = create_buffer("H_rez",H_rezept)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_rez, o_bezeich, h_rezept
        nonlocal katnr
        nonlocal h_rez


        nonlocal h_rez
        return {"avail_h_rez": avail_h_rez, "o_bezeich": o_bezeich}


    h_rez = db_session.query(H_rez).filter(
             (H_rez.kategorie == katnr)).first()

    if h_rez:
        avail_h_rez = True
        o_bezeich = h_rez.bezeich

    return generate_output()