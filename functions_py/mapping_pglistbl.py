# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 8DF8B5
        _remark_:   - fix python indentation
                    - only convert to python
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Queasy, Artikel, Htparam, H_artikel


def mapping_pglistbl(case_type: int, load_type: int, pg_number: int, pg_name: str, art_dept: int, art_name: str):

    prepare_cache([Artikel, Htparam, H_artikel])

    payment_gateway_list_data = []
    vhp_payment_list_data = []
    is_banquet: bool = False
    p_900: int = 0
    hoteldpt = queasy = artikel = htparam = h_artikel = None

    payment_gateway_list = vhp_payment_list = t_hoteldpt = mapping_pg = None

    payment_gateway_list_data, Payment_gateway_list = create_model(
        "Payment_gateway_list",
        {
            "pg_art_no": int,
            "pg_art_name": str,
            "pg_grp_no": int,
            "pg_grp_name": str,
            "pg_art_activate": bool,
            "vhp_art_no": int,
            "vhp_art_name": str,
            "vhp_art_dept": int
        })
    vhp_payment_list_data, Vhp_payment_list = create_model(
        "Vhp_payment_list",
        {
            "vhp_art_no": int,
            "vhp_art_name": str
        })
    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    Mapping_pg = create_buffer("Mapping_pg", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_gateway_list_data, vhp_payment_list_data, is_banquet, p_900, hoteldpt, queasy, artikel, htparam, h_artikel
        nonlocal case_type, load_type, pg_number, pg_name, art_dept, art_name
        nonlocal mapping_pg
        nonlocal payment_gateway_list, vhp_payment_list, t_hoteldpt, mapping_pg
        nonlocal payment_gateway_list_data, vhp_payment_list_data, t_hoteldpt_data

        return {
            "payment-gateway-list": payment_gateway_list_data,
            "vhp-payment-list": vhp_payment_list_data
        }

    def create_queasy(pg_num: int, dept: int):
        nonlocal payment_gateway_list_data, vhp_payment_list_data, is_banquet, p_900, hoteldpt, queasy, artikel, htparam, h_artikel
        nonlocal case_type, load_type, pg_number, pg_name, art_dept, art_name
        nonlocal mapping_pg
        nonlocal payment_gateway_list, vhp_payment_list, t_hoteldpt, mapping_pg
        nonlocal payment_gateway_list_data, vhp_payment_list_data, t_hoteldpt_data

        pay_list_xendit = ""
        pay_list_doku = ""
        pay_list_midtrs = ""
        pay_list = ""
        loop_payment: int = 0
        get_value = ""
        value_chr1 = ""
        value_chr2 = ""
        pay_list_xendit = "1-BRI=1-BANK_transFER|2-BNI=1-BANK_transFER|3-MANDIRI=1-BANK_transFER|4-PERMATA=1-BANK_transFER|5-BCA=1-BANK_transFER|6-BJB=1-BANK_transFER|" + \
            "7-BSI=1-BANK_transFER|8-MUAMALAT=1-BANK_transFER|9-SAHABAT_SAMPOERNA=1-BANK_transFER|10-BNC=1-BANK_transFER|11-DD_BRI=1-BANK_transFER|12-DD_MANDIRI=1-BANK_transFER|" + \
            "1-SHOPEEPAY=2-EWALLET|2-DANA=2-EWALLET|3-OVO=2-EWALLET|4-LINKAJA=2-EWALLET|5-GOPAY=2-EWALLET|6-NEXCASH=2-EWALLET|7-JENIUSPAY=2-EWALLET|8-ASTRAPAY=2-EWALLET|" + \
            "1-CREDIT_CARD=3-CREDIT_CARD|1-QRIS=4-DIGITAL PAYMENT"
        pay_list_doku = "1-QRIS=4-Digital Payment|15-Debit/Credit Card Payment=1-Debit/Credit Card|16-Credit Card Authorization=2-Credit Card Authorization|" + \
            "22-Sinarmas VA=3-Virtual Account|29-BCA VA=3-Virtual Account|32-CIMB VA=3-Virtual Account|33-Danamon VA=3-Virtual Account|" + \
            "34-BRI VA=3-Virtual Account|36-Permata VA=3-Virtual Account|38-BNI VA=3-Virtual Account|41-Mandiri VA=3-Virtual Account|42-QNB VA=3-Virtual Account|" + \
            "43-BTN VA=3-Virtual Account|44-Maybank VA=3-Virtual Account|47-Arta Jasa VA=3-Virtual Account|" + \
            "50-LinkAja!=4-Digital Payment|51-Jenius Pay=4-Digital Payment|53-OVO=4-Digital Payment"
        pay_list_midtrs = "1-CREDIT_CARD=1-Debit/Credit Card|2-GOPAY=2-Digital Payment|3-QRIS=2-Digital Payment|4-SHOPEEPAY=2-Digital Payment|" + \
            "5-BANK_transFER PERMATA=6-Bank Transfer|6-BANK_transFER BCA=6-Bank Transfer|7-BANK_transFER BNI=6-Bank Transfer|8-BANK_transFER BRI=6-Bank Transfer|" + \
            "9-ECHANNEL=3-Internet Banking|10-BCA_KLIKPAY=3-Internet Banking|11-BCA_KLIKBCA=3-Internet Banking|12-CIMB_CLICKS=3-Internet Banking|13-DANAMON_ONLINE=3-Internet Banking|" + \
            "14-BRI_EPAY=3-Internet Banking|15-CSTORE INDOMARET=4-Other Payment|16-CSTORE ALFAMART=4-Other Payment|17-AKULAKU=4-Other Payment"

        if pg_num == 1:
            pay_list = pay_list_doku

        elif pg_num == 2:
            pay_list = pay_list_midtrs

        elif pg_num == 3:
            pay_list = pay_list_xendit
        for loop_payment in range(1, num_entries(pay_list, "|") + 1):
            get_value = entry(loop_payment - 1, pay_list, "|")

            if get_value != "":
                value_chr1 = entry(0, get_value, "=")
                value_chr2 = entry(1, get_value, "=")

                mapping_pg = db_session.query(Mapping_pg).filter(
                    (Mapping_pg.key == 224) & (Mapping_pg.number1 == pg_num) & (Mapping_pg.number2 == dept) & (Mapping_pg.char1 == (value_chr1).lower())).first()

                if not mapping_pg:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 224
                    queasy.number1 = pg_num
                    queasy.number2 = dept
                    queasy.char1 = value_chr1
                    queasy.char2 = value_chr2
                    queasy.logi1 = False
                    queasy.betriebsnr = 999

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    if case_type == 1:
        if load_type == 1:
            queasy = get_cache(
                Queasy, {"key": [(eq, 224)], "number1": [(eq, pg_number)], "number2": [(eq, art_dept)]})

            if not queasy:
                create_queasy(pg_number, art_dept)

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 224) & (Queasy.number1 == pg_number) & (Queasy.number2 == art_dept)).order_by(Queasy._recid).all():
                payment_gateway_list = Payment_gateway_list()
                payment_gateway_list_data.append(payment_gateway_list)

                payment_gateway_list.pg_art_no = to_int(
                    entry(0, queasy.char1, "-"))
                payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

                if queasy.number1 == 2:
                    payment_gateway_list.pg_grp_no = to_int(
                        entry(0, queasy.char2, "-"))
                    payment_gateway_list.pg_grp_name = entry(
                        1, queasy.char2, "-")
                payment_gateway_list.pg_art_activate = queasy.logi1

                if num_entries(queasy.char3, "-") >= 2:
                    payment_gateway_list.vhp_art_no = to_int(
                        entry(0, queasy.char3, "-"))
                    payment_gateway_list.vhp_art_name = entry(
                        1, queasy.char3, "-")
                payment_gateway_list.vhp_art_dept = queasy.number2

        elif load_type == 2:
            if art_dept == 0:
                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == art_dept) & ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
                    vhp_payment_list = Vhp_payment_list()
                    vhp_payment_list_data.append(vhp_payment_list)

                    vhp_payment_list.vhp_art_no = artikel.artnr
                    vhp_payment_list.vhp_art_name = artikel.bezeich

            else:
                htparam = get_cache(Htparam, {"paramnr": [(eq, 900)]})
                p_900 = htparam.finteger

                if p_900 == art_dept:
                    is_banquet = True
                else:
                    is_banquet = False

                if is_banquet:
                    for artikel in db_session.query(Artikel).filter(
                            (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7))).order_by(Artikel.artnr).all():
                        vhp_payment_list = Vhp_payment_list()
                        vhp_payment_list_data.append(vhp_payment_list)

                        vhp_payment_list.vhp_art_no = artikel.artnr
                        vhp_payment_list.vhp_art_name = artikel.bezeich

                else:
                    for h_artikel in db_session.query(H_artikel).filter(
                            (H_artikel.departement == art_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 5) | (H_artikel.artart == 6) | (H_artikel.artart == 7)) & (H_artikel.activeflag)).order_by(H_artikel.artnr).all():
                        vhp_payment_list = Vhp_payment_list()
                        vhp_payment_list_data.append(vhp_payment_list)

                        vhp_payment_list.vhp_art_no = h_artikel.artnr
                        vhp_payment_list.vhp_art_name = h_artikel.bezeich

        elif load_type == 3:
            queasy = get_cache(
                Queasy, {"key": [(eq, 224)], "number1": [(eq, pg_number)]})

            if not queasy:
                create_queasy(pg_number, art_dept)
            else:
                for queasy in db_session.query(Queasy).filter(
                        (Queasy.key == 224) & (Queasy.number1 == pg_number)).order_by(Queasy._recid).all():
                    db_session.delete(queasy)
                create_queasy(pg_number, art_dept)

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 224) & (Queasy.number1 == pg_number)).order_by(Queasy._recid).all():
                payment_gateway_list = Payment_gateway_list()
                payment_gateway_list_data.append(payment_gateway_list)

                payment_gateway_list.pg_art_no = to_int(
                    entry(0, queasy.char1, "-"))
                payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

                if queasy.number1 == 2:
                    payment_gateway_list.pg_grp_no = to_int(
                        entry(0, queasy.char2, "-"))
                    payment_gateway_list.pg_grp_name = entry(
                        1, queasy.char2, "-")
                payment_gateway_list.pg_art_activate = queasy.logi1

                if num_entries(queasy.char3, "-") >= 2:
                    payment_gateway_list.vhp_art_no = to_int(
                        entry(0, queasy.char3, "-"))
                    payment_gateway_list.vhp_art_name = entry(
                        1, queasy.char3, "-")
                payment_gateway_list.vhp_art_dept = queasy.number2
    else:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 224) & (Queasy.number1 == pg_number) & (Queasy.number2 == art_dept)).order_by(Queasy._recid).all():
            payment_gateway_list = Payment_gateway_list()
            payment_gateway_list_data.append(payment_gateway_list)

            payment_gateway_list.pg_art_no = to_int(
                entry(0, queasy.char1, "-"))
            payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

            if queasy.number1 == 2:
                payment_gateway_list.pg_grp_no = to_int(
                    entry(0, queasy.char2, "-"))
                payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
            payment_gateway_list.pg_art_activate = queasy.logi1

            if num_entries(queasy.char3, "-") >= 2:
                payment_gateway_list.vhp_art_no = to_int(
                    entry(0, queasy.char3, "-"))
                payment_gateway_list.vhp_art_name = entry(1, queasy.char3, "-")
            payment_gateway_list.vhp_art_dept = queasy.number2

        if art_dept == 0:
            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == art_dept) & ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
                vhp_payment_list = Vhp_payment_list()
                vhp_payment_list_data.append(vhp_payment_list)

                vhp_payment_list.vhp_art_no = artikel.artnr
                vhp_payment_list.vhp_art_name = artikel.bezeich

        else:
            htparam = get_cache(Htparam, {"paramnr": [(eq, 900)]})
            p_900 = htparam.finteger

            if p_900 == art_dept:
                is_banquet = True
            else:
                is_banquet = False

            if is_banquet:
                for artikel in db_session.query(Artikel).filter(
                        (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7))).order_by(Artikel.artnr).all():
                    vhp_payment_list = Vhp_payment_list()
                    vhp_payment_list_data.append(vhp_payment_list)

                    vhp_payment_list.vhp_art_no = artikel.artnr
                    vhp_payment_list.vhp_art_name = artikel.bezeich

            else:
                for h_artikel in db_session.query(H_artikel).filter(
                        (H_artikel.departement == art_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 5) | (H_artikel.artart == 6) | (H_artikel.artart == 7)) & (H_artikel.activeflag)).order_by(H_artikel.artnr).all():
                    vhp_payment_list = Vhp_payment_list()
                    vhp_payment_list_data.append(vhp_payment_list)

                    vhp_payment_list.vhp_art_no = h_artikel.artnr
                    vhp_payment_list.vhp_art_name = h_artikel.bezeich

    return generate_output()
