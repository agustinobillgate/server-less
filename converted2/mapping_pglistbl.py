#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Queasy, Artikel, H_artikel

def mapping_pglistbl(case_type:int, load_type:int, pg_number:int, pg_name:string, art_dept:int, art_name:string):

    prepare_cache ([Artikel, H_artikel])

    payment_gateway_list_data = []
    vhp_payment_list_data = []
    hoteldpt = queasy = artikel = h_artikel = None

    payment_gateway_list = vhp_payment_list = t_hoteldpt = None

    payment_gateway_list_data, Payment_gateway_list = create_model("Payment_gateway_list", {"pg_art_no":int, "pg_art_name":string, "pg_grp_no":int, "pg_grp_name":string, "pg_art_activate":bool, "vhp_art_no":int, "vhp_art_name":string, "vhp_art_dept":int})
    vhp_payment_list_data, Vhp_payment_list = create_model("Vhp_payment_list", {"vhp_art_no":int, "vhp_art_name":string})
    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session
    pg_name = pg_name.strip()
    art_name = art_name.strip()

    def generate_output():
        nonlocal payment_gateway_list_data, vhp_payment_list_data, hoteldpt, queasy, artikel, h_artikel
        nonlocal case_type, load_type, pg_number, pg_name, art_dept, art_name

        nonlocal payment_gateway_list, vhp_payment_list, t_hoteldpt
        nonlocal payment_gateway_list_data, vhp_payment_list_data, t_hoteldpt_data

        return {"payment-gateway-list": payment_gateway_list_data, "vhp-payment-list": vhp_payment_list_data}

    def create_queasy():

        nonlocal payment_gateway_list_data, vhp_payment_list_data, hoteldpt, queasy, artikel, h_artikel
        nonlocal case_type, load_type, pg_number, pg_name, art_dept, art_name

        nonlocal payment_gateway_list, vhp_payment_list, t_hoteldpt
        nonlocal payment_gateway_list_data, vhp_payment_list_data, t_hoteldpt_data

        for t_hoteldpt in query(t_hoteldpt_data, sort_by=[("num",False)]):

            if pg_number == 1:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1-QRIS"
                queasy.char2 = "4-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "15-Debit/Credit Card Payment"
                queasy.char2 = "1-Debit/Credit Card"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "16-Credit Card Authorization"
                queasy.char2 = "2-Credit Card Authorization"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "22-Sinarmas VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "29-BCA VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "32-CIMB VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "33-Danamon VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "34-BRI VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "36-Permata VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "38-BNI VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "41-Mandiri VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "42-QNB VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "43-BTN VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "44-Maybank VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "47-Arta Jasa VA"
                queasy.char2 = "3-Virtual Account"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "50-LinkAja!"
                queasy.char2 = "4-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "51-Jenius Pay"
                queasy.char2 = "4-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "53-OVO"
                queasy.char2 = "4-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999

            elif pg_number == 2:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1-CREDIT_CARD"
                queasy.char2 = "1-Debit/Credit Card"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "2-GOPAY"
                queasy.char2 = "2-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "3-QRIS"
                queasy.char2 = "2-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "4-SHOPEEPAY"
                queasy.char2 = "2-Digital Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "5-BANK_transFER|PERMATA"
                queasy.char2 = "6-Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "6-BANK_transFER|BCA"
                queasy.char2 = "6-Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "7-BANK_transFER|BNI"
                queasy.char2 = "6-Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "8-BANK_transFER|BRI"
                queasy.char2 = "6-Bank Transfer"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "9-ECHANNEL"
                queasy.char2 = "3-Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "10-BCA_KLIKPAY"
                queasy.char2 = "3-Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "11-BCA_KLIKBCA"
                queasy.char2 = "3-Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "12-CIMB_CLICKS"
                queasy.char2 = "3-Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "13-DANAMON_ONLINE"
                queasy.char2 = "3-Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "14-BRI_EPAY"
                queasy.char2 = "3-Internet Banking"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "15-CSTORE|INDOMARET"
                queasy.char2 = "4-Other Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "16-CSTORE|ALFAMART"
                queasy.char2 = "4-Other Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "17-AKULAKU"
                queasy.char2 = "4-Other Payment"
                queasy.logi1 = False
                queasy.betriebsnr = 999

            elif pg_number == 3:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1-BRI"
                queasy.char2 = "1-BANK_transFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "2-BNI"
                queasy.char2 = "1-BANK_transFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "3-MANDIRI"
                queasy.char2 = "1-BANK_transFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "4-PERMATA"
                queasy.char2 = "1-BANK_transFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "5-BCA"
                queasy.char2 = "1-BANK_transFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1-SHOPEEPAY"
                queasy.char2 = "2-EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "2-DANA"
                queasy.char2 = "2-EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "3-OVO"
                queasy.char2 = "2-EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "4-LINKAJA"
                queasy.char2 = "2-EWALLET"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1-CREDIT_CARD"
                queasy.char2 = "3-CREDIT_CARD"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "1-QRIS"
                queasy.char2 = "4-DIGITAL PAYMENT"
                queasy.logi1 = False
                queasy.betriebsnr = 999


                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 224
                queasy.number1 = pg_number
                queasy.number2 = t_hoteldpt.num
                queasy.char1 = "6-BJB"
                queasy.char2 = "1-BANK_transFER"
                queasy.logi1 = False
                queasy.betriebsnr = 999


    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    if case_type == 1:

        if load_type == 1:

            queasy = get_cache (Queasy, {"key": [(eq, 224)],"number1": [(eq, pg_number)]})

            if not queasy:
                create_queasy()

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 224) & (Queasy.number1 == pg_number)).order_by(Queasy._recid).all():
                payment_gateway_list = Payment_gateway_list()
                payment_gateway_list_data.append(payment_gateway_list)

                payment_gateway_list.pg_art_no = to_int(entry(0, queasy.char1, "-"))
                payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

                if queasy.number1 == 2:
                    payment_gateway_list.pg_grp_no = to_int(entry(0, queasy.char2, "-"))
                    payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
                payment_gateway_list.pg_art_activate = queasy.logi1

                if num_entries(queasy.char3, "-") >= 2:
                    payment_gateway_list.vhp_art_no = to_int(entry(0, queasy.char3, "-"))
                    payment_gateway_list.vhp_art_name = entry(1, queasy.char3, "-")
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

                for h_artikel in db_session.query(H_artikel).filter(
                         (H_artikel.departement == art_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 5) | (H_artikel.artart == 6) | (H_artikel.artart == 7)) & (H_artikel.activeflag)).order_by(H_artikel.artnr).all():
                    vhp_payment_list = Vhp_payment_list()
                    vhp_payment_list_data.append(vhp_payment_list)

                    vhp_payment_list.vhp_art_no = h_artikel.artnr
                    vhp_payment_list.vhp_art_name = h_artikel.bezeich

        elif load_type == 3:

            queasy = get_cache (Queasy, {"key": [(eq, 224)],"number1": [(eq, pg_number)]})

            if not queasy:
                create_queasy()
            else:

                for queasy in db_session.query(Queasy).filter(
                         (Queasy.key == 224) & (Queasy.number1 == pg_number)).order_by(Queasy._recid).with_for_update().all():
                    db_session.delete(queasy)
                create_queasy()

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 224) & (Queasy.number1 == pg_number)).order_by(Queasy._recid).all():
                payment_gateway_list = Payment_gateway_list()
                payment_gateway_list_data.append(payment_gateway_list)

                payment_gateway_list.pg_art_no = to_int(entry(0, queasy.char1, "-"))
                payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

                if queasy.number1 == 2:
                    payment_gateway_list.pg_grp_no = to_int(entry(0, queasy.char2, "-"))
                    payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
                payment_gateway_list.pg_art_activate = queasy.logi1

                if num_entries(queasy.char3, "-") >= 2:
                    payment_gateway_list.vhp_art_no = to_int(entry(0, queasy.char3, "-"))
                    payment_gateway_list.vhp_art_name = entry(1, queasy.char3, "-")
                payment_gateway_list.vhp_art_dept = queasy.number2
    else:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 224) & (Queasy.number1 == pg_number) & (Queasy.number2 == art_dept)).order_by(Queasy._recid).all():
            payment_gateway_list = Payment_gateway_list()
            payment_gateway_list_data.append(payment_gateway_list)

            payment_gateway_list.pg_art_no = to_int(entry(0, queasy.char1, "-"))
            payment_gateway_list.pg_art_name = entry(1, queasy.char1, "-")

            if queasy.number1 == 2:
                payment_gateway_list.pg_grp_no = to_int(entry(0, queasy.char2, "-"))
                payment_gateway_list.pg_grp_name = entry(1, queasy.char2, "-")
            payment_gateway_list.pg_art_activate = queasy.logi1

            if num_entries(queasy.char3, "-") >= 2:
                payment_gateway_list.vhp_art_no = to_int(entry(0, queasy.char3, "-"))
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

            for h_artikel in db_session.query(H_artikel).filter(
                     (H_artikel.departement == art_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 5) | (H_artikel.artart == 6) | (H_artikel.artart == 7)) & (H_artikel.activeflag)).order_by(H_artikel.artnr).all():
                vhp_payment_list = Vhp_payment_list()
                vhp_payment_list_data.append(vhp_payment_list)

                vhp_payment_list.vhp_art_no = h_artikel.artnr
                vhp_payment_list.vhp_art_name = h_artikel.bezeich

    return generate_output()