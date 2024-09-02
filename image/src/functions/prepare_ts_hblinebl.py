from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Kellner, Htparam, Bediener, H_artikel, H_bill_line, Wgrpdep

def prepare_ts_hblinebl(user_init:str, dept:int, curr_rechnr:int):
    zero_flag = False
    billdate = None
    balance = 0
    max_gpos = 0
    menu_list_list = []
    grp_list_list = []
    curr_zwkum:int = 0
    fgcol_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    kellner = htparam = bediener = h_artikel = h_bill_line = wgrpdep = None

    menu_list = grp_list = kbuff = None

    menu_list_list, Menu_list = create_model("Menu_list", {"request":str, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "price":decimal, "betrag":decimal, "voucher":str}, {"anzahl": 1})
    grp_list_list, Grp_list = create_model("Grp_list", {"pos":int, "dept":int, "zknr":int, "bezeich":str, "grp_bgcol":int, "grp_fgcol":int}, {"grp_bgcol": 1, "grp_fgcol": 15})

    Kbuff = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zero_flag, billdate, balance, max_gpos, menu_list_list, grp_list_list, curr_zwkum, fgcol_array, kellner, htparam, bediener, h_artikel, h_bill_line, wgrpdep
        nonlocal kbuff


        nonlocal menu_list, grp_list, kbuff
        nonlocal menu_list_list, grp_list_list
        return {"zero_flag": zero_flag, "billdate": billdate, "balance": balance, "max_gpos": max_gpos, "menu-list": menu_list_list, "grp-list": grp_list_list}

    def build_bline():

        nonlocal zero_flag, billdate, balance, max_gpos, menu_list_list, grp_list_list, curr_zwkum, fgcol_array, kellner, htparam, bediener, h_artikel, h_bill_line, wgrpdep
        nonlocal kbuff


        nonlocal menu_list, grp_list, kbuff
        nonlocal menu_list_list, grp_list_list

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_artikel.artnr) &  (H_artikel.departement == dept) &  (H_artikel.artart == 0)).filter(
                (H_bill_line.departement == dept) &  (H_bill_line.rechnr == curr_rechnr)).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            menu_list = Menu_list()
            menu_list_list.append(menu_list)

            menu_list.nr = 0
            menu_list.posted = True
            menu_list.REQUEST = ""
            menu_list.artnr = h_bill_line.artnr
            menu_list.bezeich = h_bill_line.bezeich
            menu_list.anzahl = h_bill_line.anzahl
            balance = balance + h_bill_line.betrag

    def build_glist():

        nonlocal zero_flag, billdate, balance, max_gpos, menu_list_list, grp_list_list, curr_zwkum, fgcol_array, kellner, htparam, bediener, h_artikel, h_bill_line, wgrpdep
        nonlocal kbuff


        nonlocal menu_list, grp_list, kbuff
        nonlocal menu_list_list, grp_list_list

        i:int = 0
        w_fibukonto:int = 0

        if not zero_flag:

            wgrpdep_obj_list = []
            for wgrpdep, h_artikel in db_session.query(Wgrpdep, H_artikel).join(H_artikel,(H_artikel.departement == dept) &  (H_artikel.zwkum == Wgrpdep.zknr) &  (H_artikel.artart == 0) &  (H_artikel.epreis1 != 0) &  (H_artikel.activeflag)).filter(
                    (Wgrpdep.departement == dept)).all():
                if wgrpdep._recid in wgrpdep_obj_list:
                    continue
                else:
                    wgrpdep_obj_list.append(wgrpdep._recid)


                w_fibukonto = 0
                i = i + 1
                grp_list = Grp_list()
                grp_list_list.append(grp_list)

                grp_list.pos = i
                grp_list.dept = dept
                grp_list.zknr = wgrpdep.zknr
                grp_list.bezeich = wgrpdep.bezeich

                if i == 1:
                    curr_zwkum = wgrpdep.zknr
                w_fibukonto = to_int(entry(0, wgrpdep.fibukonto, ";"))

                if w_fibukonto != 0:
                    grp_list.grp_bgcol = w_fibukonto
                    grp_list.grp_fgcol = fgcol_array[grp_list.grp_bgcol + 1 - 1]

        else:

            wgrpdep_obj_list = []
            for wgrpdep, h_artikel in db_session.query(Wgrpdep, H_artikel).join(H_artikel,(H_artikel.departement == dept) &  (H_artikel.zwkum == Wgrpdep.zknr) &  (H_artikel.artart == 0) &  (H_artikel.activeflag)).filter(
                    (Wgrpdep.departement == dept)).all():
                if wgrpdep._recid in wgrpdep_obj_list:
                    continue
                else:
                    wgrpdep_obj_list.append(wgrpdep._recid)


                w_fibukonto = 0
                i = i + 1
                grp_list = Grp_list()
                grp_list_list.append(grp_list)

                grp_list.pos = i
                grp_list.dept = dept
                grp_list.zknr = wgrpdep.zknr
                grp_list.bezeich = wgrpdep.bezeich

                if i == 1:
                    curr_zwkum = wgrpdep.zknr
                w_fibukonto = to_int(entry(0, wgrpdep.fibukonto, ";"))

                if w_fibukonto != 0:
                    grp_list.grp_bgcol = w_fibukonto
                    grp_list.grp_fgcol = fgcol_array[grp_list.grp_bgcol + 1 - 1]

        max_gpos = i


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 869)).first()
    zero_flag = htparam.flogical

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:

        kbuff = db_session.query(Kbuff).filter(
                (Kbuff.departement == dept) &  (Kbuff.kellner_nr == to_int(bediener.userinit))).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:

        kbuff = db_session.query(Kbuff).filter(
                (Kbuff.departement == dept) &  (Kbuff.kellner_nr == to_int(bediener.userinit))).first()
    build_bline()
    build_glist()

    return generate_output()