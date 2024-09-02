from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.ns_inv_attach_cashless_codebl import ns_inv_attach_cashless_codebl
from functions.read_bk_veranbl import read_bk_veranbl
from functions.read_bk_reserbl import read_bk_reserbl
from functions.read_reservationbl import read_reservationbl
from models import Reservation, Bk_reser, Bk_veran

def ns_inv_attach_cashless_code_webbl(sorttype:int, gastname:str, dept:int, rechnr:int):
    resname = ""
    address = ""
    city = ""
    comments = ""
    b1_list_list = []
    ba_dept:int = 0
    fr_name:str = ""
    to_name:str = ""
    stat:str = ""
    reservation = bk_reser = bk_veran = None

    b1_list = t_reservation = t_bk_reser = t_bk_veran = None

    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "rechnr":int, "name":str, "vorname1":str, "anrede1":str, "saldo":decimal, "printnr":int, "datum":date, "b_recid":int, "adresse1":str, "wohnort":str, "bemerk":str, "plz":str, "bill_datum":date, "qr_code":str})
    t_reservation_list, T_reservation = create_model_like(Reservation)
    t_bk_reser_list, T_bk_reser = create_model_like(Bk_reser)
    t_bk_veran_list, T_bk_veran = create_model_like(Bk_veran)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, comments, b1_list_list, ba_dept, fr_name, to_name, stat, reservation, bk_reser, bk_veran


        nonlocal b1_list, t_reservation, t_bk_reser, t_bk_veran
        nonlocal b1_list_list, t_reservation_list, t_bk_reser_list, t_bk_veran_list
        return {"resname": resname, "address": address, "city": city, "comments": comments, "b1-list": b1_list_list}

    ba_dept = get_output(htpint(900))
    b1_list_list = get_output(ns_inv_attach_cashless_codebl(0, sorttype, gastname, dept, ba_dept, rechnr))

    b1_list = query(b1_list_list, first=True)

    if b1_list:
        resname = b1_list.name
        address = b1_list.adresse1
        city = b1_list.wohnort + " " + b1_list.plz

        if dept == ba_dept and b1_list.rechnr != 0:
            t_bk_veran_list = get_output(read_bk_veranbl(2, None, None, b1_list.rechnr, None))

            t_bk_veran = query(t_bk_veran_list, first=True)

            if t_bk_veran:
                comments = "RefNo: " + to_string(t_bk_veran.veran_nr) + chr(10)
                t_bk_reser_list = get_output(read_bk_reserbl(5, t_bk_veran.veran_nr, None, 9, None))

                for t_bk_reser in query(t_bk_reser_list):
                    comments = comments + to_string(t_bk_reser.veran_resnr) + ": " + stat[t_bk_reser.resstatus - 1] + " " + to_string(t_bk_reser.datum) + chr(10) + t_bk_reser.raum + " " + to_string(t_bk_reser.von_zeit, "99:99") + " - " + to_string(t_bk_reser.bis_zeit, "99:99") + chr(10)
        comments = comments + b1_list.bemerk
        t_reservation_list = get_output(read_reservationbl(1, b1_list.resnr, None, ""))

        t_reservation = query(t_reservation_list, first=True)

        if t_reservation and t_reservation.bemerk != "":
            comments = comments + chr(10) + t_reservation.bemerk

    return generate_output()