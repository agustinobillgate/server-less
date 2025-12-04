"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        _remark_:   - only converted to python
"""

from functions.additional_functions import *
import decimal
from models import H_bill, H_bill_line


def ts_splitbill_build_lmenubl(rec_id: int, dept: int):
    max_lapos = 0
    menu_list = []
    lhbline_list = []
    h_bill = h_bill_line = None

    menu = lhbline = None

    menu_list, Menu = create_model(
        "Menu",
        {
            "pos": int,
            "bezeich": str,
            "artnr": int
        })
    lhbline_list, Lhbline = create_model(
        "Lhbline",
        {
            "nr": int,
            "rid": int
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_lapos, menu_list, lhbline_list, h_bill, h_bill_line
        nonlocal rec_id, dept

        nonlocal menu, lhbline
        nonlocal menu_list, lhbline_list
        return {
            "max_lapos": max_lapos,
            "menu": menu_list,
            "Lhbline": lhbline_list
        }

    def build_lmenu():

        nonlocal max_lapos, menu_list, lhbline_list, h_bill, h_bill_line
        nonlocal rec_id, dept

        nonlocal menu, lhbline
        nonlocal menu_list, lhbline_list

        curr_lapos: int = 1
        i: int = 0
        menu_list.clear()
        lhbline_list.clear()
        curr_lapos = 1
        max_lapos = 0

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept) & (H_bill_line.waehrungsnr == 0)).order_by(H_bill_line.bezeich).all():
            i = i + 1
            menu = Menu()
            menu_list.append(menu)

            menu.pos = i
            menu.artnr = h_bill_line.artnr
            menu.bezeich = to_string(
                h_bill_line.anzahl) + " " + h_bill_line.bezeich
            lhbline = Lhbline()
            lhbline_list.append(lhbline)

            lhbline.nr = i
            lhbline.rid = h_bill_line._recid
        max_lapos = i

    h_bill = db_session.query(H_bill).filter(
        (H_bill._recid == rec_id)).first()
    build_lmenu()

    return generate_output()
