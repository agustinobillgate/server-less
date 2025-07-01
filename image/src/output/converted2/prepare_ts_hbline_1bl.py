#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdec import htpdec
from models import Kellner, Htparam, Bediener, H_artikel, H_bill_line, Wgrpdep

def prepare_ts_hbline_1bl(user_init:string, dept:int, curr_rechnr:int):

    prepare_cache ([Htparam, Bediener, H_bill_line, Wgrpdep])

    zero_flag = False
    billdate = None
    balance = to_decimal("0.0")
    max_gpos = 0
    cashless_license = False
    cashless_minsaldo = to_decimal("0.0")
    menu_list_list = []
    grp_list_list = []
    curr_zwkum:int = 0
    fgcol_array:List[int] = [15, 15, 15, 15, 15, 15, 15, 15, 0, 15, 0, 0, 15, 15, 0, 0, 15]
    kellner = htparam = bediener = h_artikel = h_bill_line = wgrpdep = None

    menu_list = grp_list = kbuff = None

    menu_list_list, Menu_list = create_model("Menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1})
    grp_list_list, Grp_list = create_model("Grp_list", {"pos":int, "dept":int, "zknr":int, "bezeich":string, "grp_bgcol":int, "grp_fgcol":int}, {"grp_bgcol": 1, "grp_fgcol": 15})

    Kbuff = create_buffer("Kbuff",Kellner)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zero_flag, billdate, balance, max_gpos, cashless_license, cashless_minsaldo, menu_list_list, grp_list_list, curr_zwkum, fgcol_array, kellner, htparam, bediener, h_artikel, h_bill_line, wgrpdep
        nonlocal user_init, dept, curr_rechnr
        nonlocal kbuff


        nonlocal menu_list, grp_list, kbuff
        nonlocal menu_list_list, grp_list_list

        return {"zero_flag": zero_flag, "billdate": billdate, "balance": balance, "max_gpos": max_gpos, "cashless_license": cashless_license, "cashless_minsaldo": cashless_minsaldo, "menu-list": menu_list_list, "grp-list": grp_list_list}

    def build_bline():

        nonlocal zero_flag, billdate, balance, max_gpos, cashless_license, cashless_minsaldo, menu_list_list, grp_list_list, curr_zwkum, fgcol_array, kellner, htparam, bediener, h_artikel, h_bill_line, wgrpdep
        nonlocal user_init, dept, curr_rechnr
        nonlocal kbuff


        nonlocal menu_list, grp_list, kbuff
        nonlocal menu_list_list, grp_list_list

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_artikel.artnr) & (H_artikel.departement == dept) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.departement == dept) & (H_bill_line.rechnr == curr_rechnr)).order_by(H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            menu_list = Menu_list()
            menu_list_list.append(menu_list)

            menu_list.nr = 0
            menu_list.posted = True
            menu_list.request = ""
            menu_list.artnr = h_bill_line.artnr
            menu_list.bezeich = h_bill_line.bezeich
            menu_list.anzahl = h_bill_line.anzahl
            balance =  to_decimal(balance) + to_decimal(h_bill_line.betrag)


    def build_glist():

        nonlocal zero_flag, billdate, balance, max_gpos, cashless_license, cashless_minsaldo, menu_list_list, grp_list_list, curr_zwkum, fgcol_array, kellner, htparam, bediener, h_artikel, h_bill_line, wgrpdep
        nonlocal user_init, dept, curr_rechnr
        nonlocal kbuff


        nonlocal menu_list, grp_list, kbuff
        nonlocal menu_list_list, grp_list_list

        i:int = 0
        w_fibukonto:int = 0

        if not zero_flag:

            wgrpdep_obj_list = {}
            for wgrpdep, h_artikel in db_session.query(Wgrpdep, H_artikel).join(H_artikel,(H_artikel.departement == dept) & (H_artikel.zwkum == Wgrpdep.zknr) & (H_artikel.artart == 0) & (H_artikel.epreis1 != 0) & (H_artikel.activeflag)).filter(
                     (Wgrpdep.departement == dept)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.bezeich).all():
                if wgrpdep_obj_list.get(wgrpdep._recid):
                    continue
                else:
                    wgrpdep_obj_list[wgrpdep._recid] = True


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

            wgrpdep_obj_list = {}
            for wgrpdep, h_artikel in db_session.query(Wgrpdep, H_artikel).join(H_artikel,(H_artikel.departement == dept) & (H_artikel.zwkum == Wgrpdep.zknr) & (H_artikel.artart == 0) & (H_artikel.activeflag)).filter(
                     (Wgrpdep.departement == dept)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.bezeich).all():
                if wgrpdep_obj_list.get(wgrpdep._recid):
                    continue
                else:
                    wgrpdep_obj_list[wgrpdep._recid] = True


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
             (Htparam.paramnr == 1022) & (Htparam.bezeichnung != ("not used").lower()) & (Htparam.flogical)).first()

    if htparam:
        cashless_license = True
    cashless_minsaldo = get_output(htpdec(586))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 869)]})
    zero_flag = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        kbuff = db_session.query(Kbuff).filter(
                 (Kbuff.departement == dept) & (Kbuff.kellner_nr == to_int(bediener.userinit))).first()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        kbuff = db_session.query(Kbuff).filter(
                 (Kbuff.departement == dept) & (Kbuff.kellner_nr == to_int(bediener.userinit))).first()
    build_bline()
    build_glist()

    return generate_output()