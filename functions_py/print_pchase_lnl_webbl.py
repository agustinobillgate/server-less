# using conversion tools version: 1.0.0.119
# -----------------------------------------
# Rd, 25/7/2025
# po_nr -> op_list.po_nr

# yusufwijasena, 11/11/2025 (F6D79E)
# - update Dzikri: 508B79
# - already latest
# - fix ("string").lower()
# Rd, 01/12/2025, with_for_update added
# -----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Paramtext, Htparam, L_orderhdr, L_lieferant, L_order, Parameters, Waehrung, Guestbook, L_artikel
from sqlalchemy.orm.attributes import flag_modified

def print_pchase_lnl_webbl(pvilanguage: int, lnldelimeter: string, docunr: string, stattype: int, curr_status: string):
    prepare_cache([Queasy, Paramtext, Htparam, L_orderhdr, L_lieferant, L_order, Parameters, Waehrung, Guestbook, L_artikel])

    str3_list_data = []
    esign_print_data = []
    str1_data = []
    str3_data = []
    lvcarea: string = "print-pchase-lnl"
    long_digit: bool = False
    foreign_currency: bool = False
    price_decimal: int = 0
    bill_recv: string = ""
    address1: string = ""
    address2: string = ""
    cp_name: string = ""
    telp: string = ""
    fax_no: string = ""
    bill_no: string = ""
    bill_date: string = ""
    refer: string = ""
    po_source: string = ""
    dep_date: string = ""
    arr_date: string = ""
    delivery_date: string = ""
    bl_descript: string = ""
    bl_qty: string = ""
    d_unit: string = ""
    bl_price: string = ""
    bl_amount: string = ""
    c_exrate: string = ""
    bl_balance: string = ""
    balance: Decimal = to_decimal("0.0")
    remark: string = ""
    bank_name: string = ""
    account: string = ""
    rekening: string = ""
    i: int = 0
    globaldisc: Decimal = to_decimal("0.0")
    companytitle: string = ""
    bl_vat: string = ""
    po_number: string = ""
    bl_amount_add_vat: string = ""
    htl_name: string = ""
    htl_adr: string = ""
    htl_tel: string = ""
    created_by: string = ""
    vat_code: string = ""
    vat1: Decimal = to_decimal("0.0")
    vat2: Decimal = to_decimal("0.0")
    p_app: bool = False
    img_id_name: List[string] = create_empty_list(4, "")
    img_id_date: List[string] = create_empty_list(4, "")
    img_id_pos: List[string] = create_empty_list(4, "")
    tmp_liefnr: int = 0
    iscreated: bool = False
    queasy = paramtext = htparam = l_orderhdr = l_lieferant = l_order = parameters = waehrung = guestbook = l_artikel = None

    str3_list = esign_print = str1 = str3 = op_list = b_queasy = None

    str3_list_data, Str3_list = create_model(
        "Str3_list",
        {
            "str": string
        })
    esign_print_data, Esign_print = create_model(
        "Esign_print",
        {
            "sign_nr": int,
            "sign_name": string,
            "sign_img": bytes,
            "sign_date": string,
            "sign_position": string
        })
    str1_data, Str1 = create_model(
        "Str1",
        {
            "bill_recv": string,
            "address1": string,
            "address2": string,
            "cp_name": string,
            "telp": string,
            "fax_no": string,
            "bill_no": string,
            "bill_date": date,
            "refer": string,
            "po_source": string,
            "po_number": string,
            "dep_date": int,
            "arr_date": date,
            "created_by": string,
            "delivery_date": date,
            "remark": string,
            "globaldisc": Decimal,
            "bank_name": string,
            "account": string,
            "rekening": string,
            "companytitle": string,
            "vat_code": string,
            "afterdisc": Decimal,
            "htl_name": string,
            "htl_adr": string,
            "htl_tel": string
        })
    str3_data, Str3 = create_model(
        "Str3",
        {
            "bl_descript": string,
            "arr_date": string,
            "bl_qty": string,
            "d_unit": string,
            "bl_price": string,
            "bl_amount": string,
            "c_exrate": string,
            "bl_balance": string,
            "remark": string,
            "konto": string,
            "disc": Decimal,
            "disc2": Decimal,
            "vat": Decimal,
            "disc_value": Decimal,
            "disc2_value": Decimal,
            "epreis0": Decimal,
            "bl_vat": string,
            "artnr": int,
            "brutto": Decimal,
            "po_nr": string,
            "po_source": string,
            "vat1": Decimal,
            "vat2": Decimal,
            "add_vat": Decimal,
            "bl_amount_add_vat": string
        })
    op_list_data, Op_list = create_model(
        "Op_list",
        {
            "artnr": int,
            "anzahl": Decimal,
            "bezeich": string,
            "bez_aend": bool,
            "disc": Decimal,
            "disc2": Decimal,
            "vat": Decimal,
            "epreis": Decimal,
            "epreis0": Decimal,
            "warenwert": Decimal,
            "konto": string,
            "warenwert0": Decimal,
            "remark": string,
            "disc_value": Decimal,
            "disc2_value": Decimal,
            "brutto": Decimal,
            "vat_value": Decimal,
            "po_nr": string,
            "vat_code": string,
            "vat1": Decimal,
            "vat2": Decimal,
            "add_vat": Decimal,
            "warenwert_add_vat": Decimal
        })

    B_queasy = create_buffer("B_queasy", Queasy)

    db_session = local_storage.db_session
    docunr = docunr.strip()
    curr_status = curr_status.strip()

    def generate_output():
        nonlocal str3_list_data, esign_print_data, str1_data, str3_data, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, bl_amount_add_vat, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, tmp_liefnr, iscreated, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal pvilanguage, lnldelimeter, docunr, stattype, curr_status
        nonlocal b_queasy
        nonlocal str3_list, esign_print, str1, str3, op_list, b_queasy
        nonlocal str3_list_data, esign_print_data, str1_data, str3_data, op_list_data

        return {
            "str3-list": str3_list_data,
            "esign-print": esign_print_data,
            "str1": str1_data,
            "str3": str3_data
        }

    def decode_string(in_str: string):
        nonlocal str3_list_data, esign_print_data, str1_data, str3_data, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, bl_amount_add_vat, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, tmp_liefnr, iscreated, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal pvilanguage, lnldelimeter, docunr, stattype, curr_status
        nonlocal b_queasy
        nonlocal str3_list, esign_print, str1, str3, op_list, b_queasy
        nonlocal str3_list_data, esign_print_data, str1_data, str3_data, op_list_data

        out_str = ""
        s: string = ""
        j: int = 0
        len_: int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1, length(s) + 1):
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    def do_billline():
        nonlocal str3_list_data, esign_print_data, str1_data, str3_data, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, bl_amount_add_vat, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, tmp_liefnr, iscreated, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal pvilanguage, lnldelimeter, docunr, stattype, curr_status
        nonlocal b_queasy
        nonlocal str3_list, esign_print, str1, str3, op_list, b_queasy
        nonlocal str3_list_data, esign_print_data, str1_data, str3_data, op_list_data

        l_art = None
        create_it: bool = False
        curr_bez: string = ""
        bez_aend: bool = False
        disc: Decimal = to_decimal("0.0")
        disc2: Decimal = to_decimal("0.0")
        disc_value: Decimal = to_decimal("0.0")
        disc2_value: Decimal = to_decimal("0.0")
        price0: Decimal = to_decimal("0.0")
        brutto: Decimal = to_decimal("0.0")
        tot_qty: Decimal = to_decimal("0.0")
        vat: Decimal = to_decimal("0.0")
        vat_val: Decimal = to_decimal("0.0")
        loeschflag: int = 0
        L_art = create_buffer("L_art", L_artikel)
        op_list_data.clear()

        if stattype == 0:
            loeschflag = 0

        elif stattype == 1:
            loeschflag = 1

        elif stattype == 2:
            loeschflag = 0

        elif stattype == 3:
            loeschflag = 2

        if stattype == 0 or stattype == 2:
            for l_order in db_session.query(L_order).filter(
                    (L_order.docu_nr == (docunr).lower()) & (L_order.loeschflag == loeschflag) & (L_order.pos > 0)).order_by(L_order.pos).all():
                create_it = False
                bez_aend = False

                l_art = get_cache(L_artikel, {"artnr": [(eq, l_order.artnr)]})

                if l_art:
                    curr_bez = l_art.bezeich
                    disc = to_decimal("0")
                    disc2 = to_decimal("0")
                    disc_value = to_decimal("0")
                    disc2_value = to_decimal("0")
                    vat_val = to_decimal("0")
                    price0 = to_decimal("0")
                    brutto = to_decimal("0")

                    if l_order.quality != "":
                        if num_entries(l_order.quality, " ") == 6:
                            disc = to_int(substring(entry(0, l_order.quality, " "), 0, 2)) + to_int(
                                substring(entry(0, l_order.quality, " "), 3, 2)) * 0.01
                            disc_value = to_decimal(to_decimal(
                                entry(3, l_order.quality, " ")))
                            disc2 = to_int(substring(entry(2, l_order.quality, " "), 151)) + to_int(
                                substring(entry(2, l_order.quality, " "), 3, 2)) * 0.01
                            disc2_value = to_decimal(to_decimal(
                                entry(4, l_order.quality, " ")))
                            vat_val = to_decimal(to_decimal(
                                entry(5, l_order.quality, " ")))

                        elif num_entries(l_order.quality, " ") >= 6:
                            disc = to_int(substring(l_order.quality, 0, 2)) + \
                                to_int(substring(l_order.quality, 3, 2)) * 0.01
                            disc_value = to_decimal(
                                substring(l_order.quality, 18, 18))

                            if length(l_order.quality) > 12:
                                disc2 = to_int(substring(
                                    l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                                disc2_value = to_decimal(
                                    substring(l_order.quality, 36, 18))
                                vat_val = to_decimal(
                                    substring(l_order.quality, 54, 18))
                                price0 = to_decimal(
                                    substring(l_order.quality, 72, 18))
                                brutto = to_decimal(
                                    substring(l_order.quality, 90, 18))

                    if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:
                        op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich ==
                                        l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund and op_list.remark == l_order.besteller), first=True)
                    else:
                        curr_bez = substring(
                            l_order.stornogrund, 12, length(l_order.stornogrund))
                        create_it = True
                        bez_aend = True

                    if length(l_order.stornogrund) > 12:
                        curr_bez = substring(l_order.stornogrund, 12)

                    if not op_list or create_it:
                        vat = to_decimal("0")
                        op_list = Op_list()
                        op_list_data.append(op_list)

                        op_list.artnr = l_order.artnr
                        op_list.bezeich = curr_bez
                        op_list.bez_aend = bez_aend
                        op_list.epreis = to_decimal(l_order.einzelpreis)
                        op_list.epreis0 = to_decimal(l_order.einzelpreis)
                        op_list.konto = l_order.stornogrund
                        op_list.remark = l_order.besteller
                        op_list.po_nr = po_number
                        op_list.vat_code = vat_code
                        op_list.vat1 = to_decimal(vat1)
                        op_list.vat2 = to_decimal(vat2)

                        queasy = get_cache(
                            Queasy, {"key": [(eq, 304)], "char1": [(eq, l_order.docu_nr)], "number1": [(eq, l_order.artnr)]})

                        if queasy:
                            op_list.add_vat = (to_decimal(
                                1.0) + to_decimal((queasy.deci1) / to_decimal(100)))
                        else:
                            op_list.add_vat = to_decimal("1")

                        if l_order.quality != "":
                            vat = to_int(substring(l_order.quality, 6, 2)) + \
                                to_int(substring(l_order.quality, 9, 2)) * 0.01
                            op_list.disc = to_decimal(disc)
                            op_list.disc2 = to_decimal(disc2)
                            op_list.disc_value = to_decimal(disc_value)
                            op_list.disc2_value = to_decimal(disc2_value)
                            op_list.vat = to_decimal(vat)
                            op_list.vat_value = to_decimal(vat_val)
                            disc = to_decimal(disc) / to_decimal("100")
                            disc2 = to_decimal(disc2) / to_decimal("100")
                            vat = to_decimal(vat) / to_decimal("100")

                    op_list.anzahl = to_decimal(
                        op_list.anzahl) + to_decimal(l_order.anzahl)
                    op_list.warenwert = to_decimal(
                        op_list.warenwert) + to_decimal(l_order.warenwert)
                    op_list.warenwert_add_vat = to_decimal(
                        op_list.warenwert_add_vat) + to_decimal((l_order.warenwert) * to_decimal(op_list.add_vat))

                    if op_list.warenwert == op_list.warenwert_add_vat:
                        if brutto == 0:
                            op_list.brutto = (to_decimal(op_list.warenwert) + to_decimal(
                                op_list.disc_value) + to_decimal(op_list.disc2_value)) - to_decimal(op_list.vat_value)
                        else:
                            op_list.brutto = to_decimal(brutto)

                        if price0 == 0:
                            op_list.epreis0 = to_decimal(
                                round((op_list.brutto / op_list.anzahl), 2))
                        else:
                            op_list.epreis0 = to_decimal(price0)
                        op_list.warenwert0 = to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal(
                            (1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                    else:
                        if brutto == 0:
                            op_list.brutto = (to_decimal(op_list.warenwert_add_vat) + to_decimal(op_list.disc_value) + to_decimal(
                                op_list.disc2_value)) - to_decimal(op_list.vat_value) - (to_decimal(op_list.warenwert_add_vat) - to_decimal(op_list.warenwert))
                        else:
                            op_list.brutto = to_decimal(brutto)

                        if price0 == 0:
                            op_list.epreis0 = to_decimal(
                                round((op_list.brutto / op_list.anzahl), 2))
                        else:
                            op_list.epreis0 = to_decimal(price0)
                        op_list.warenwert0 = to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal(
                            (1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                    tot_qty = to_decimal(tot_qty) + to_decimal(l_order.anzahl)

        elif stattype == 1 or stattype == 3:
            for l_order in db_session.query(L_order).filter(
                    (L_order.docu_nr == (docunr).lower()) & (L_order.loeschflag == loeschflag) & (L_order.pos > 0)).order_by(L_order.pos).all():
                create_it = False
                bez_aend = False

                l_art = get_cache(L_artikel, {"artnr": [(eq, l_order.artnr)]})
                curr_bez = l_art.bezeich
                disc = to_decimal("0")
                disc2 = to_decimal("0")
                disc_value = to_decimal("0")
                disc2_value = to_decimal("0")
                vat_val = to_decimal("0")
                price0 = to_decimal("0")
                brutto = to_decimal("0")

                if l_order.quality != "":
                    if num_entries(l_order.quality, " ") == 6:
                        disc = to_int(substring(entry(0, l_order.quality, " "), 0, 2)) + \
                            to_int(
                                substring(entry(0, l_order.quality, " "), 3, 2)) * 0.01
                        disc_value = to_decimal(to_decimal(
                            entry(3, l_order.quality, " ")))
                        disc2 = to_int(substring(entry(2, l_order.quality, " "), 151)) + to_int(
                            substring(entry(2, l_order.quality, " "), 3, 2)) * 0.01
                        disc2_value = to_decimal(to_decimal(
                            entry(4, l_order.quality, " ")))
                        vat_val = to_decimal(to_decimal(
                            entry(5, l_order.quality, " ")))

                    elif num_entries(l_order.quality, " ") >= 6:
                        disc = to_int(substring(l_order.quality, 0, 2)) + \
                            to_int(substring(l_order.quality, 3, 2)) * 0.01
                        disc_value = to_decimal(
                            substring(l_order.quality, 18, 18))

                        if length(l_order.quality) > 12:
                            disc2 = to_int(substring(
                                l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                            disc2_value = to_decimal(
                                substring(l_order.quality, 36, 18))
                            vat_val = to_decimal(
                                substring(l_order.quality, 54, 18))
                            price0 = to_decimal(
                                substring(l_order.quality, 72, 18))
                            brutto = to_decimal(
                                substring(l_order.quality, 90, 18))

                if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:
                    op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich ==
                                    l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund and op_list.remark == l_order.besteller), first=True)
                else:
                    curr_bez = substring(
                        l_order.stornogrund, 12, length(l_order.stornogrund))
                    create_it = True
                    bez_aend = True

                if length(l_order.stornogrund) > 12:
                    curr_bez = substring(l_order.stornogrund, 12)

                if not op_list or create_it:
                    vat = to_decimal("0")
                    op_list = Op_list()
                    op_list_data.append(op_list)

                    op_list.artnr = l_order.artnr
                    op_list.bezeich = curr_bez
                    op_list.bez_aend = bez_aend
                    op_list.epreis = to_decimal(l_order.einzelpreis)
                    op_list.epreis0 = to_decimal(l_order.einzelpreis)
                    op_list.konto = l_order.stornogrund
                    op_list.remark = l_order.besteller
                    op_list.po_nr = po_number
                    op_list.vat_code = vat_code
                    op_list.vat1 = to_decimal(vat1)
                    op_list.vat2 = to_decimal(vat2)

                    queasy = get_cache(
                        Queasy, {"key": [(eq, 304)], "char1": [(eq, l_order.docu_nr)], "number1": [(eq, l_order.artnr)]})

                    if queasy:
                        op_list.add_vat = (to_decimal(
                            1.0) + to_decimal((queasy.deci1) / to_decimal(100)))
                    else:
                        op_list.add_vat = to_decimal("1")

                    if l_order.quality != "":
                        vat = to_int(substring(l_order.quality, 6, 2)) + \
                            to_int(substring(l_order.quality, 9, 2)) * 0.01
                        op_list.disc = to_decimal(disc)
                        op_list.disc2 = to_decimal(disc2)
                        op_list.disc_value = to_decimal(disc_value)
                        op_list.disc2_value = to_decimal(disc2_value)
                        op_list.vat = to_decimal(vat)
                        op_list.vat_value = to_decimal(vat_val)
                        disc = to_decimal(disc) / to_decimal("100")
                        disc2 = to_decimal(disc2) / to_decimal("100")
                        vat = to_decimal(vat) / to_decimal("100")

                op_list.anzahl = to_decimal(
                    op_list.anzahl) + to_decimal(l_order.anzahl)
                op_list.warenwert = to_decimal(
                    op_list.warenwert) + to_decimal(l_order.warenwert)
                op_list.warenwert_add_vat = to_decimal(
                    op_list.warenwert_add_vat) + to_decimal((l_order.warenwert) * to_decimal(op_list.add_vat))

                if op_list.warenwert == op_list.warenwert_add_vat:
                    if brutto == 0:
                        op_list.brutto = (to_decimal(op_list.warenwert) + to_decimal(
                            op_list.disc_value) + to_decimal(op_list.disc2_value)) - to_decimal(op_list.vat_value)
                    else:
                        op_list.brutto = to_decimal(brutto)

                    if price0 == 0:
                        op_list.epreis0 = to_decimal(
                            round((op_list.brutto / op_list.anzahl), 2))
                    else:
                        op_list.epreis0 = to_decimal(price0)
                    op_list.warenwert0 = to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal(
                        (1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                else:
                    if brutto == 0:
                        op_list.brutto = (to_decimal(op_list.warenwert_add_vat) + to_decimal(op_list.disc_value) + to_decimal(
                            op_list.disc2_value)) - to_decimal(op_list.vat_value) - (to_decimal(op_list.warenwert_add_vat) - to_decimal(op_list.warenwert))
                    else:
                        op_list.brutto = to_decimal(brutto)

                    if price0 == 0:
                        op_list.epreis0 = to_decimal(
                            round((op_list.brutto / op_list.anzahl), 2))
                    else:
                        op_list.epreis0 = to_decimal(price0)
                    op_list.warenwert0 = to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal(
                        (1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                tot_qty = to_decimal(tot_qty) + to_decimal(l_order.anzahl)

        elif stattype == None:
            for l_order in db_session.query(L_order).filter(
                    (L_order.docu_nr == (docunr).lower()) & (L_order.pos > 0)).order_by(L_order.pos).all():
                create_it = False
                bez_aend = False

                l_art = get_cache(L_artikel, {"artnr": [(eq, l_order.artnr)]})
                curr_bez = l_art.bezeich
                disc = to_decimal("0")
                disc2 = to_decimal("0")
                disc_value = to_decimal("0")
                disc2_value = to_decimal("0")
                vat_val = to_decimal("0")
                price0 = to_decimal("0")
                brutto = to_decimal("0")

                if l_order.quality != "":
                    if num_entries(l_order.quality, " ") == 6:
                        disc = to_int(substring(entry(0, l_order.quality, " "), 0, 2)) + \
                            to_int(
                                substring(entry(0, l_order.quality, " "), 3, 2)) * 0.01
                        disc_value = to_decimal(to_decimal(
                            entry(3, l_order.quality, " ")))
                        disc2 = to_int(substring(entry(2, l_order.quality, " "), 151)) + to_int(
                            substring(entry(2, l_order.quality, " "), 3, 2)) * 0.01
                        disc2_value = to_decimal(to_decimal(
                            entry(4, l_order.quality, " ")))
                        vat_val = to_decimal(to_decimal(
                            entry(5, l_order.quality, " ")))

                    elif num_entries(l_order.quality, " ") >= 6:
                        disc = to_int(substring(l_order.quality, 0, 2)) + \
                            to_int(substring(l_order.quality, 3, 2)) * 0.01
                        disc_value = to_decimal(
                            substring(l_order.quality, 18, 18))

                        if length(l_order.quality) > 12:
                            disc2 = to_int(substring(
                                l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                            disc2_value = to_decimal(
                                substring(l_order.quality, 36, 18))
                            vat_val = to_decimal(
                                substring(l_order.quality, 54, 18))
                            price0 = to_decimal(
                                substring(l_order.quality, 72, 18))
                            brutto = to_decimal(
                                substring(l_order.quality, 90, 18))

                if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:
                    op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich ==
                                    l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund and op_list.remark == l_order.besteller), first=True)
                else:
                    curr_bez = substring(
                        l_order.stornogrund, 12, length(l_order.stornogrund))
                    create_it = True
                    bez_aend = True

                if length(l_order.stornogrund) > 12:
                    curr_bez = substring(l_order.stornogrund, 12)

                if not op_list or create_it:
                    vat = to_decimal("0")
                    op_list = Op_list()
                    op_list_data.append(op_list)

                    op_list.artnr = l_order.artnr
                    op_list.bezeich = curr_bez
                    op_list.bez_aend = bez_aend
                    op_list.epreis = to_decimal(l_order.einzelpreis)
                    op_list.epreis0 = to_decimal(l_order.einzelpreis)
                    op_list.konto = l_order.stornogrund
                    op_list.remark = l_order.besteller
                    op_list.po_nr = po_number
                    op_list.vat_code = vat_code
                    op_list.vat1 = to_decimal(vat1)
                    op_list.vat2 = to_decimal(vat2)

                    queasy = get_cache(
                        Queasy, {"key": [(eq, 304)], "char1": [(eq, l_order.docu_nr)], "number1": [(eq, l_order.artnr)]})

                    if queasy:
                        op_list.add_vat = (to_decimal(
                            1.0) + to_decimal((queasy.deci1) / to_decimal(100)))
                    else:
                        op_list.add_vat = to_decimal("1")

                    if l_order.quality != "":
                        vat = to_int(substring(l_order.quality, 6, 2)) + \
                            to_int(substring(l_order.quality, 9, 2)) * 0.01
                        op_list.disc = to_decimal(disc)
                        op_list.disc2 = to_decimal(disc2)
                        op_list.disc_value = to_decimal(disc_value)
                        op_list.disc2_value = to_decimal(disc2_value)
                        op_list.vat = to_decimal(vat)
                        op_list.vat_value = to_decimal(vat_val)
                        disc = to_decimal(disc) / to_decimal("100")
                        disc2 = to_decimal(disc2) / to_decimal("100")
                        vat = to_decimal(vat) / to_decimal("100")

                op_list.anzahl = to_decimal(
                    op_list.anzahl) + to_decimal(l_order.anzahl)
                op_list.warenwert = to_decimal(
                    op_list.warenwert) + to_decimal(l_order.warenwert)
                op_list.warenwert_add_vat = to_decimal(
                    op_list.warenwert_add_vat) + to_decimal((l_order.warenwert) * to_decimal(op_list.add_vat))

                if op_list.warenwert == op_list.warenwert_add_vat:
                    if brutto == 0:
                        op_list.brutto = (to_decimal(op_list.warenwert) + to_decimal(
                            op_list.disc_value) + to_decimal(op_list.disc2_value)) - to_decimal(op_list.vat_value)
                    else:
                        op_list.brutto = to_decimal(brutto)

                    if price0 == 0:
                        op_list.epreis0 = to_decimal(
                            round((op_list.brutto / op_list.anzahl), 2))
                    else:
                        op_list.epreis0 = to_decimal(price0)
                    op_list.warenwert0 = to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal(
                        (1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                else:
                    if brutto == 0:
                        op_list.brutto = (to_decimal(op_list.warenwert_add_vat) + to_decimal(op_list.disc_value) + to_decimal(
                            op_list.disc2_value)) - to_decimal(op_list.vat_value) - (to_decimal(op_list.warenwert_add_vat) - to_decimal(op_list.warenwert))
                    else:
                        op_list.brutto = to_decimal(brutto)

                    if price0 == 0:
                        op_list.epreis0 = to_decimal(
                            round((op_list.brutto / op_list.anzahl), 2))
                    else:
                        op_list.epreis0 = to_decimal(price0)
                    op_list.warenwert0 = to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal(
                        (1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                tot_qty = to_decimal(tot_qty) + to_decimal(l_order.anzahl)

        for op_list in query(op_list_data):
            if op_list.anzahl == 0:
                op_list_data.remove(op_list)

    htl_name = ""

    paramtext = get_cache(Paramtext, {"txtnr": [(eq, 240)]})

    if paramtext and paramtext.ptexte != "":
        htl_name = decode_string(paramtext.ptexte)
    htl_adr = ""

    paramtext = get_cache(Paramtext, {"txtnr": [(eq, 201)]})

    if paramtext:
        htl_adr = paramtext.ptexte
    htl_tel = ""

    paramtext = get_cache(Paramtext, {"txtnr": [(eq, 204)]})

    if paramtext:
        htl_tel = paramtext.ptexte

    htparam = get_cache(Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 71)]})
    p_app = htparam.flogical

    l_orderhdr = db_session.query(L_orderhdr).filter(
        (L_orderhdr.docu_nr == (docunr).lower()) & (L_orderhdr.lief_nr > 0)).first()

    if l_orderhdr:
        tmp_liefnr = l_orderhdr.lief_nr
    else:
        l_orderhdr = get_cache(
            L_orderhdr, {"docu_nr": [(eq, docunr)], "lief_nr": [(eq, 0)]})

        if l_orderhdr:
            tmp_liefnr = l_orderhdr.lief_nr
        else:
            tmp_liefnr = None

    if tmp_liefnr is not None:
        l_lieferant = get_cache(
            L_lieferant, {"lief_nr": [(eq, l_orderhdr.lief_nr)]})

        if l_lieferant:
            for i in range(1, length(l_lieferant.bank) + 1):
                if matches(substring(l_lieferant.bank, i - 1, 3), r"a/n"):
                    break
            bill_recv = l_lieferant.firma
            address1 = l_lieferant.adresse1
            address2 = l_lieferant.adresse2
            cp_name = l_lieferant.namekontakt + ", " + l_lieferant.vorname1 +\
                " " + l_lieferant.anrede1
            telp = l_lieferant.telefon
            fax_no = l_lieferant.fax
            bank_name = substring(l_lieferant.bank, 0, i - 2)
            account = substring(l_lieferant.bank, i + 4 -
                                1, length(l_lieferant.bank))
            rekening = l_lieferant.kontonr
            companytitle = l_lieferant.anredefirma

            str1 = Str1()
            str1_data.append(str1)

            str1.bill_recv = l_lieferant.firma
            str1.address1 = l_lieferant.adresse1
            str1.address2 = l_lieferant.adresse2
            str1.cp_name = l_lieferant.namekontakt + ", " + \
                l_lieferant.vorname1 + " " + l_lieferant.anrede1
            str1.telp = l_lieferant.telefon
            str1.fax_no = l_lieferant.fax
            str1.bank_name = substring(l_lieferant.bank, 0, i - 2)
            str1.account = substring(
                l_lieferant.bank, i + 4 - 1, length(l_lieferant.bank))
            str1.rekening = l_lieferant.kontonr
            str1.companytitle = l_lieferant.anredefirma

            iscreated = True

            queasy = get_cache(
                Queasy, {"key": [(eq, 219)], "number1": [(eq, l_lieferant.lief_nr)]})

            if queasy:
                vat_code = queasy.char1
                vat1 = to_decimal(queasy.deci1)
                vat2 = to_decimal(queasy.deci2)

                str1.vat_code = queasy.char1

    if l_orderhdr:
        bill_no = docunr

        l_order = get_cache(
            L_order, {"lief_nr": [(eq, l_orderhdr.lief_nr)], "docu_nr": [(eq, docunr)], "pos": [(eq, 0)]})

        if l_order:
            if l_order.zeit > 0:
                if curr_status.lower() == "design":
                    bill_no = docunr + "-REPRINT"
                else:
                    queasy = get_cache(
                        Queasy, {"key": [(eq, 240)], "char1": [(eq, l_order.docu_nr)]})

                    if not queasy:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 240
                        queasy.char1 = l_order.docu_nr

                        bill_no = docunr
                    else:
                        queasy.number1 = queasy.number1 + 1
                        bill_no = docunr + "-REPRINT" + \
                            to_string(queasy.number1)
            refer = to_string(l_order.lief_fax[0])
            globaldisc = to_decimal(l_order.warenwert)

            str1.refer = refer
            str1.globaldisc = to_decimal(globaldisc)
            str1.bill_no = bill_no

        bill_date = to_string(l_orderhdr.bestelldatum)
        dep_date = to_string(l_orderhdr.angebot_lief[1])
        remark = l_orderhdr.lief_fax[2]
        arr_date = to_string(l_orderhdr.lieferdatum)
        delivery_date = to_string(l_orderhdr.lieferdatum)
        po_number = l_order.docu_nr
        created_by = to_string(l_orderhdr.besteller)

        str1.bill_date = l_orderhdr.bestelldatum
        str1.dep_date = l_orderhdr.angebot_lief[1]
        str1.remark = remark
        str1.arr_date = l_orderhdr.lieferdatum
        str1.delivery_date = l_orderhdr.lieferdatum
        str1.po_number = po_number
        str1.created_by = l_orderhdr.besteller

        parameters = db_session.query(Parameters).filter(
            (Parameters.progname == "costcenter") & (Parameters.section == "name") & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

        if parameters:
            po_source = parameters.vstring

        waehrung = get_cache(
            Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

        if waehrung:
            htparam = get_cache(Htparam, {"paramnr": [(eq, 152)]})

            if htparam.fchar != "" and (htparam.fchar != waehrung.wabkurz):
                foreign_currency = True
            c_exrate = to_string(waehrung.wabkurz)

        if p_app:
            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 245) & (Queasy.char1 == (docunr).lower())).order_by(Queasy._recid).all():

                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number2) & (Guestbook.reserve_logic[inc_value(1)])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_data.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(
                        3, guestbook.infostr, "|")
                    img_id_name[queasy.number1 -
                                1] = entry(1, guestbook.infostr, "|")
                    img_id_date[queasy.number1 -
                                1] = entry(1, queasy.char3, "|")
                    img_id_pos[queasy.number1 -
                                1] = entry(3, guestbook.infostr, "|")

    do_billline()

    for op_list in query(op_list_data):
        bl_descript = op_list.bezeich

        if op_list.anzahl >= 10000 or (- op_list.anzahl >= 10000):
            bl_qty = to_string(op_list.anzahl, "->>>,>>9")

        elif op_list.anzahl >= 1000 or (- op_list.anzahl >= 1000):
            if op_list.anzahl >= 0:
                bl_qty = to_string(op_list.anzahl, ">,>>9.99")
            else:
                bl_qty = to_string(op_list.anzahl, "->,>>9.9")
        else:
            bl_qty = to_string(op_list.anzahl, "->>9.99")

        l_artikel = get_cache(L_artikel, {"artnr": [(eq, op_list.artnr)]})

        if l_artikel:
            d_unit = l_artikel.traubensorte

        if op_list.warenwert == op_list.warenwert_add_vat:
            balance = to_decimal(balance) + to_decimal(op_list.warenwert)
        else:
            balance = to_decimal(balance) + \
                to_decimal(op_list.warenwert_add_vat)
        bl_amount = to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.99")
        bl_balance = to_string(balance, "->,>>>,>>>,>>>,>>9.99")
        bl_amount_add_vat = to_string(
            op_list.warenwert_add_vat, "->>>,>>>,>>>,>>9.99")

        if op_list.epreis >= 10000000:
            bl_price = to_string(op_list.epreis, " >>,>>>,>>>,>>>,>>9.99")
        else:
            bl_price = to_string(op_list.epreis, ">>>,>>>,>>>,>>9.99")
        bl_vat = to_string(op_list.vat_value, "->,>>>,>>>,>>9.99")

        str3_list = Str3_list()
        str3_list_data.append(str3_list)

        # Rd, 25/7/2025
        # po_nr -> op_list.po_nr
        str3_list.str = bl_descript + lnldelimeter + \
            arr_date + lnldelimeter + \
            bl_qty + lnldelimeter + \
            d_unit + lnldelimeter + \
            bl_price + lnldelimeter + \
            bl_amount + lnldelimeter + \
            c_exrate + lnldelimeter + \
            bl_balance + lnldelimeter + \
            op_list.remark + lnldelimeter + \
            op_list.konto + lnldelimeter + \
            to_string(op_list.disc, "->>9.99") + lnldelimeter + \
            to_string(op_list.disc2, "->>9.99") + lnldelimeter + \
            to_string(op_list.vat, "->>9.99") + lnldelimeter + \
            to_string(op_list.disc_value, "->>>,>>>,>>>,>>9.99") + lnldelimeter + \
            to_string(op_list.disc2_value, "->>>,>>>,>>>,>>9.99") + lnldelimeter + \
            to_string(op_list.epreis0, ">>,>>>,>>>,>>>,>>9.99") + lnldelimeter + \
            bl_vat + lnldelimeter + \
            to_string(op_list.artnr, ">>>>>>>9") + lnldelimeter + \
            to_string(op_list.brutto, ">>>,>>>,>>>,>>9.99") + lnldelimeter + \
            op_list.po_nr + lnldelimeter + \
            po_source + lnldelimeter + \
            to_string(vat1, "->,>>>,>>>,>>>,>>9.99") + lnldelimeter + \
            to_string(vat2, "->,>>>,>>>,>>>,>>9.99") + lnldelimeter + \
            to_string(((op_list.add_vat - 1) * 100), "->>9.99") + lnldelimeter + \
            bl_amount_add_vat
        str3 = Str3()
        str3_data.append(str3)

        str3.bl_descript = bl_descript
        str3.arr_date = arr_date
        str3.bl_qty = bl_qty
        str3.d_unit = d_unit
        str3.bl_price = bl_price
        str3.bl_amount = bl_amount
        str3.c_exrate = c_exrate
        str3.bl_balance = bl_balance
        str3.remark = op_list.remark
        str3.konto = op_list.konto
        str3.disc = to_decimal(op_list.disc)
        str3.disc2 = to_decimal(op_list.disc2)
        str3.vat = to_decimal(op_list.vat)
        str3.disc_value = to_decimal(op_list.disc_value)
        str3.disc2_value = to_decimal(op_list.disc2_value)
        str3.epreis0 = to_decimal(op_list.epreis0)
        str3.bl_vat = bl_vat
        str3.artnr = op_list.artnr
        str3.brutto = to_decimal(op_list.brutto)
        str3.po_nr = op_list.po_nr
        str3.po_source = po_source
        str3.vat1 = to_decimal(vat1)
        str3.vat2 = to_decimal(vat2)
        str3.add_vat = (to_decimal((op_list.add_vat) -
                        to_decimal(1)) * to_decimal("100"))
        str3.bl_amount_add_vat = bl_amount_add_vat

    if iscreated:
        str1.afterdisc = to_decimal(balance) - to_decimal(globaldisc)
        str1.htl_name = htl_name
        str1.htl_adr = htl_adr
        str1.htl_tel = htl_tel

    if tmp_liefnr is not None:
        # l_order = get_cache(L_order, {"lief_nr": [(eq, l_orderhdr.lief_nr)], "docu_nr": [
        #                     (eq, docunr)], "pos": [(eq, 0)]})
        l_order = db_session.query(L_order).filter(
            (L_order.lief_nr == l_orderhdr.lief_nr) & (L_order.docu_nr == (docunr).lower()) & (L_order.pos == 0)).with_for_update().first()
        l_order.gedruckt = get_current_date()
        l_order.zeit = get_current_time_in_seconds()

    return generate_output()
