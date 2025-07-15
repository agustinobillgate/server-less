from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fobill_vatlistbl import fobill_vatlistbl
from sqlalchemy import func
from models import Guest, Res_line, Htparam, Paramtext, Bill, Mc_guest, Artikel, Bill_line, Reservation, Bediener, Arrangement, Waehrung, Zimmer, Queasy, Exrate

t_spbill_list_list, T_spbill_list = create_model("T_spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})

def web_interface_print_bill_lnl_selectedbl(t_spbill_list_list:[T_spbill_list], pvilanguage:int, curr_status:str, briefnr:int, resnr:int, reslinnr:int, inv_type:int, rechnr:int, curr_program:str, gastnr:int, spbill_flag:bool, user_init:str, lnldelimeter:str, for_curr:decimal, conv_wabkurz:str, curr_bezeich:str):
    str1 = ""
    str2 = ""
    str3 = ""
    t_str3_list = []
    lvcarea:str = "print-bill-lnl"
    briefnr2:int = 0
    briefnr21:int = 0
    htl_name:str = ""
    htl_adr1:str = ""
    htl_adr2:str = ""
    htl_adr3:str = ""
    htl_tel:str = ""
    htl_fax:str = ""
    htl_email:str = ""
    resv_name:str = ""
    username:str = ""
    bill_recv:str = ""
    bill_no:str = ""
    bl_descript:str = ""
    bl_descript0:str = ""
    bl_voucher:str = ""
    bl0_balance:decimal = 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99"
    bl0_balance1:decimal = 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99"
    bl_balance:decimal = 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99"
    bl_balance1:decimal = 0 FORMAT "->>>,>>>,>>>,>>>,>>9.99"
    sum_anz:decimal = 0 FORMAT "->>>"
    address1:str = ""
    address2:str = ""
    address3:str = ""
    email:str = ""
    hp_no:str = ""
    acc:str = ""
    adult:str = ""
    child1:str = ""
    child2:str = ""
    complgst:str = ""
    room_no:str = ""
    room_price:str = ""
    arrival:str = ""
    departure:str = ""
    bl_guest:str = ""
    l_guest:str = ""
    bl_instruct:str = ""
    resno:str = ""
    in_word:str = ""
    room_cat:str = ""
    city:str = ""
    country:str = ""
    zip:str = ""
    hp_guest:str = ""
    phone:str = ""
    bl_accom:str = ""
    sstr1:str = ""
    sstr2:str = ""
    sstr3:str = ""
    w_length:int = 40
    progname:str = ""
    temp_amt:decimal = to_decimal("0.0")
    wi_gastnr:int = 0
    ind_gastnr:int = 0
    select_flag:bool = False
    g_comment:str = ""
    bill_comment:str = ""
    ma_gst_amount:decimal = to_decimal("0.0")
    ma_gst_tot_sales_artikel:decimal = to_decimal("0.0")
    ma_gst_tot_non_taxable:decimal = to_decimal("0.0")
    ma_gst_tot_taxable:decimal = to_decimal("0.0")
    ma_gst_gtot_tax:decimal = to_decimal("0.0")
    curr_guest:str = ""
    tot_service_code:decimal = to_decimal("0.0")
    serv1:decimal = to_decimal("0.0")
    vat1:decimal = to_decimal("0.0")
    vat3:decimal = to_decimal("0.0")
    fact1:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    guest_taxcode:str = ""
    tot_inclvat:decimal = to_decimal("0.0")
    net_amount:decimal = to_decimal("0.0")
    serv_code:decimal = to_decimal("0.0")
    acc_tax:decimal = to_decimal("0.0")
    vat_cam:decimal = to_decimal("0.0")
    do_it:bool = False
    membernumber:str = ""
    mgst:decimal = to_decimal("0.0")
    artnr_1001:decimal = to_decimal("0.0")
    selected_room:str = ""
    paidout:int = 0
    frate:decimal = 1
    rm_serv:bool = False
    rm_vat:bool = False
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    amount_bef_tax:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = 1
    guest = res_line = htparam = paramtext = bill = mc_guest = artikel = bill_line = reservation = bediener = arrangement = waehrung = zimmer = queasy = exrate = None

    bline_list = sum_tbl = t_str3 = t_spbill_list = bl_guest = bline_vatlist = guest1 = resline = None

    bline_list_list, Bline_list = create_model("Bline_list", {"bl_recid":int, "artnr":int, "dept":int, "anzahl":int, "massnr":int, "billin_nr":int, "zeit":int, "mwst_code":int, "vatproz":decimal, "epreis":decimal, "netto":decimal, "fsaldo":decimal, "saldo":decimal, "orts_tax":decimal, "voucher":str, "bezeich":str, "zinr":str, "gname":str, "origin_id":str, "userinit":str, "ankunft":date, "abreise":date, "datum":date}, {"origin_id": ""})
    sum_tbl_list, Sum_tbl = create_model("Sum_tbl", {"mwst_code":int, "sum_date":str, "sum_roomnr":str, "sum_desc":str, "sum_amount":decimal, "sum_id":str, "sum_amount_bef_tax":decimal}, {"sum_date": "", "sum_roomnr": "", "sum_desc": "", "sum_id": ""})
    t_str3_list, T_str3 = create_model("T_str3", {"str3":str})
    bl_guest_list, bl_guest = create_model("bl_guest", {"zinr":str, "curr_guest":str})
    bline_vatlist_list, Bline_vatlist = create_model("Bline_vatlist", {"seqnr":int, "vatnr":int, "bezeich":str, "betrag":decimal})

    Guest1 = create_buffer("Guest1",Guest)
    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str1, str2, str3, t_str3_list, lvcarea, briefnr2, briefnr21, htl_name, htl_adr1, htl_adr2, htl_adr3, htl_tel, htl_fax, htl_email, resv_name, username, bill_recv, bill_no, bl_descript, bl_descript0, bl_voucher, bl0_balance, bl0_balance1, bl_balance, bl_balance1, sum_anz, address1, address2, address3, email, hp_no, acc, adult, child1, child2, complgst, room_no, room_price, arrival, departure, bl_guest, l_guest, bl_instruct, resno, in_word, room_cat, city, country, zip, hp_guest, phone, bl_accom, sstr1, sstr2, sstr3, w_length, progname, temp_amt, wi_gastnr, ind_gastnr, select_flag, g_comment, bill_comment, ma_gst_amount, ma_gst_tot_sales_artikel, ma_gst_tot_non_taxable, ma_gst_tot_taxable, ma_gst_gtot_tax, curr_guest, tot_service_code, serv1, vat1, vat3, fact1, netto, guest_taxcode, tot_inclvat, net_amount, serv_code, acc_tax, vat_cam, do_it, membernumber, mgst, artnr_1001, selected_room, paidout, frate, rm_serv, rm_vat, service, vat, amount_bef_tax, vat2, fact, guest, res_line, htparam, paramtext, bill, mc_guest, artikel, bill_line, reservation, bediener, arrangement, waehrung, zimmer, queasy, exrate
        nonlocal pvilanguage, curr_status, briefnr, resnr, reslinnr, inv_type, rechnr, curr_program, gastnr, spbill_flag, user_init, lnldelimeter, for_curr, conv_wabkurz, curr_bezeich
        nonlocal guest1, resline


        nonlocal bline_list, sum_tbl, t_str3, t_spbill_list, bl_guest, bline_vatlist, guest1, resline
        nonlocal bline_list_list, sum_tbl_list, t_str3_list, t_spbill_list_list, bl_guest_list, bline_vatlist_list
        return {"str1": str1, "str2": str2, "str3": str3, "t-str3": t_str3_list}

    def calc_bl_balance1(datum:date, betrag:decimal, fremdwbetrag:decimal, fbetrag:decimal):

        nonlocal str1, str2, str3, t_str3_list, lvcarea, briefnr2, briefnr21, htl_name, htl_adr1, htl_adr2, htl_adr3, htl_tel, htl_fax, htl_email, resv_name, username, bill_recv, bill_no, bl_descript, bl_descript0, bl_voucher, bl0_balance, bl0_balance1, bl_balance, bl_balance1, sum_anz, address1, address2, address3, email, hp_no, acc, adult, child1, child2, complgst, room_no, room_price, arrival, departure, bl_guest, l_guest, bl_instruct, resno, in_word, room_cat, city, country, zip, hp_guest, phone, bl_accom, sstr1, sstr2, sstr3, w_length, progname, temp_amt, wi_gastnr, ind_gastnr, select_flag, g_comment, bill_comment, ma_gst_amount, ma_gst_tot_sales_artikel, ma_gst_tot_non_taxable, ma_gst_tot_taxable, ma_gst_gtot_tax, curr_guest, tot_service_code, serv1, vat1, vat3, fact1, netto, guest_taxcode, tot_inclvat, net_amount, serv_code, acc_tax, vat_cam, do_it, membernumber, mgst, artnr_1001, selected_room, paidout, frate, rm_serv, rm_vat, service, vat, amount_bef_tax, vat2, fact, guest, res_line, htparam, paramtext, bill, mc_guest, artikel, bill_line, reservation, bediener, arrangement, waehrung, zimmer, queasy, exrate
        nonlocal pvilanguage, curr_status, briefnr, resnr, reslinnr, inv_type, rechnr, curr_program, gastnr, spbill_flag, user_init, lnldelimeter, for_curr, conv_wabkurz, curr_bezeich
        nonlocal guest1, resline


        nonlocal bline_list, sum_tbl, t_str3, t_spbill_list, bl_guest, bline_vatlist, guest1, resline
        nonlocal bline_list_list, sum_tbl_list, t_str3_list, t_spbill_list_list, bl_guest_list, bline_vatlist_list

        billdate:date = None
        resline_exrate:decimal = to_decimal("0.0")
        rline = None

        def generate_inner_output():
            return (fbetrag)

        Rline =  create_buffer("Rline",Res_line)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate

        if resnr == 0:
            fbetrag =  to_decimal(fbetrag) + to_decimal(fremdwbetrag)

            return generate_inner_output()

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == resnr) & ((Rline.resstatus == 6) | (Rline.resstatus == 8)) & (Rline.reserve_dec > 0)).first()

        if not rline:
            fbetrag =  to_decimal(fbetrag) + to_decimal(fremdwbetrag)
        else:

            if rline.reserve_dec != 0:

                if rline.ankunft == billdate:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.waehrungsnr == rline.betriebsnr)).first()

                    if waehrung:
                        resline_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                    else:
                        resline_exrate =  to_decimal(rline.reserve_dec)
                else:

                    exrate = db_session.query(Exrate).filter(
                             (Exrate.datum == rline.ankunft) & (Exrate.artnr == rline.betriebsnr)).first()

                    if exrate:
                        resline_exrate =  to_decimal(exrate.betrag)
                    else:
                        resline_exrate =  to_decimal(rline.reserve_dec)

            if resline_exrate != 0:
                fbetrag =  to_decimal(fbetrag) + to_decimal(betrag) / to_decimal(resline_exrate)
            else:
                fbetrag =  to_decimal(fbetrag) + to_decimal(betrag) / to_decimal(rline.reserve_dec)

        return generate_inner_output()

    if inv_type == 9 and num_entries(curr_program, ";") > 1:
        selected_room = entry(1, curr_program, ";")
        curr_program = entry(0, curr_program, ";")

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 415)).first()
    briefnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 495)).first()
    briefnr21 = htparam.finteger

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()
    htl_adr1 = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 202)).first()
    htl_adr2 = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 203)).first()
    htl_adr3 = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()
    htl_tel = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 205)).first()
    htl_fax = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 206)).first()
    htl_email = paramtext.ptexte

    bill = db_session.query(Bill).filter(
             (Bill.rechnr == rechnr)).first()
    bill_comment = bill.vesrdepot

    if curr_program.lower()  == ("ns-invoice").lower() :

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastnr)).first()

        if guest:

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == gastnr)).first()

            if mc_guest:
                membernumber = mc_guest.cardnum
            bill_recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            city = trim(guest.wohnort)
            country = trim(guest.land)
            zip = trim(guest.plz)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
            phone = to_string(guest.telefon, "x(16)")
            g_comment = guest.bemerkung

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == bill.resnr) & (Res_line.resnr == bill.reslinnr)).first()

        if res_line:

            guest1 = db_session.query(Guest1).filter(
                     (Guest1.gastnr == res_line.gastnrmember)).first()

            if guest1:
                hp_guest = to_string(guest.mobil_telefon, "x(16)")

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")
        ma_gst_amount =  to_decimal("0")
        ma_gst_tot_sales_artikel =  to_decimal("0")
        ma_gst_tot_non_taxable =  to_decimal("0")
        ma_gst_tot_taxable =  to_decimal("0")
        tot_service_code =  to_decimal("0")

        if not spbill_flag:

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                    bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)


                serv1 =  to_decimal("0")
                vat1 =  to_decimal("0")
                vat3 =  to_decimal("0")
                fact1 =  to_decimal("0")

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                         (Htparam.paramnr == artikel.mwst_code)).first()

                            if htparam:
                                ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                        elif artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:

                                    htparam = db_session.query(Htparam).filter(
                                                 (Htparam.paramnr == artikel.mwst_code)).first()

                                    if htparam:
                                        ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                                elif artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

                    if artikel.service_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        tot_service_code =  to_decimal(tot_service_code) + to_decimal((netto) * to_decimal(serv1) )

                    if artnr_1001 == 0 and ma_gst_amount == 0 and artikel.mwst_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        mgst =  to_decimal(mgst) + to_decimal((netto) * to_decimal((vat1) + to_decimal(vat3)) )

        else:

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)

                t_spbill_list = query(t_spbill_list_list, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                         (Htparam.paramnr == artikel.mwst_code)).first()

                            if htparam:
                                ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                        elif artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:

                                    htparam = db_session.query(Htparam).filter(
                                                 (Htparam.paramnr == artikel.mwst_code)).first()

                                    if htparam:
                                        ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                                elif artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

                    if artikel.service_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        tot_service_code =  to_decimal(tot_service_code) + to_decimal((netto) * to_decimal(serv1) )

                    if artnr_1001 == 0 and ma_gst_amount == 0 and artikel.mwst_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        mgst =  to_decimal(mgst) + to_decimal((netto) * to_decimal((vat1) + to_decimal(vat3)) )


        if ma_gst_amount != 0:
            ma_gst_amount = ( to_decimal(ma_gst_amount) * to_decimal("6") / to_decimal(100)) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        elif artnr_1001 != 0:
            ma_gst_amount =  to_decimal(artnr_1001)
            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(artnr_1001) - to_decimal(ma_gst_tot_non_taxable) )


            ma_gst_gtot_tax =  to_decimal(artnr_1001) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)
        else:
            ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 416)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 410)).first()
        progname = htparam.fchar

        if (progname != ""):

            if progname.lower()  == ("word_chinese.p").lower() :

                if briefnr == briefnr2:
                    sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr3)
            else:

                if briefnr == briefnr2 or briefnr == briefnr21:
                    sstr1, sstr2 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2:
                        sstr1, sstr2 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr1) + " " + trim(sstr2)
        do_it = False

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 271)).first()

        if htparam.flogical:
            bline_vatlist_list = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_list, first=True)

            if bline_vatlist:
                do_it = True

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == bill.resnr)).first()

        if reservation:
            resv_name = reservation.name

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            username = bediener.username
        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if email == None:
                email = ""

            if hp_no == None:
                hp_no = ""

            if acc == None:
                acc = ""

            if adult == None:
                adult = ""

            if child1 == None:
                child1 = ""

            if child2 == None:
                child2 = ""

            if complgst == None:
                complgst = ""

            if room_no == None:
                room_no = ""

            if room_price == None:
                room_price = ""

            if arrival == None:
                arrival = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if bl_guest == None:
                bl_guest = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bl_instruct == None:
                bl_instruct = ""

            if user_init == None:
                user_init = ""

            if room_cat == None:
                room_cat = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if resv_name == None:
                resv_name = ""

            if guest_taxcode == None:
                guest_taxcode = ""

            if in_word == None:
                in_word = ""

            if bl_accom == None:
                bl_accom = ""

            if username == None:
                username = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM")
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$city" + city + lnldelimeter + "$country" + country + lnldelimeter + "$zip" + zip + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$resv-name" + resv_name + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$acc-guest" + bl_accom + lnldelimeter + "$bl-username" + username + lnldelimeter + "$g-comment" + g_comment + lnldelimeter + "$bill-comment" + bill_comment
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("RoomNo", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if inv_type == 2:

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == rechnr)).first()

                if bill_line:
                    bl_voucher = ""
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:

                        if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                            if num_entries(bl_descript, "/") > 2:
                                bl_voucher = entry(2, bl_descript, "/")
                        else:
                            bl_voucher = entry(1, bl_descript, "/")

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                    if res_line:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()

                        if guest:
                            curr_guest = guest.name


                    else:
                        curr_guest = " "


                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                if do_it:

                    bline_vatlist = query(bline_vatlist_list, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_list, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
            else:

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == rechnr)).first()

                if bill_line:
                    bl_voucher = ""
                    bl_descript = bill_line.bezeich
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:

                        if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                            if num_entries(bl_descript, "/") > 2:
                                bl_voucher = entry(2, bl_descript, "/")
                        else:
                            bl_voucher = entry(1, bl_descript, "/")

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                    if res_line:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()

                        if guest:
                            curr_guest = guest.name


                    else:
                        curr_guest = " "


                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                if do_it:

                    bline_vatlist = query(bline_vatlist_list, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_list, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if email == None:
                email = ""

            if hp_no == None:
                hp_no = ""

            if acc == None:
                acc = ""

            if adult == None:
                adult = ""

            if child1 == None:
                child1 = ""

            if child2 == None:
                child2 = ""

            if complgst == None:
                complgst = ""

            if room_no == None:
                room_no = ""

            if room_price == None:
                room_price = ""

            if arrival == None:
                arrival = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if bl_guest == None:
                bl_guest = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bl_instruct == None:
                bl_instruct = ""

            if user_init == None:
                user_init = ""

            if room_cat == None:
                room_cat = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if resv_name == None:
                resv_name = ""

            if guest_taxcode == None:
                guest_taxcode = ""

            if in_word == None:
                in_word = ""

            if bl_accom == None:
                bl_accom = ""

            if username == None:
                username = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM")
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$city" + city + lnldelimeter + "$country" + country + lnldelimeter + "$zip" + zip + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$resv-name" + resv_name + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$acc-guest" + bl_accom + lnldelimeter + "$bl-username" + username + lnldelimeter + "$g-comment" + g_comment + lnldelimeter + "$bill-comment" + bill_comment
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("RoomNo", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if not spbill_flag:

                if inv_type == 2:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        sum_tbl = query(sum_tbl_list, filters=(lambda sum_tbl: sum_tbl.mwst_code == artikel.mwst_code), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_list.append(sum_tbl)

                            sum_tbl.mwst_code = artikel.mwst_code
                            sum_tbl.sum_desc = bl_descript
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_list):
                        sum_anz =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == rechnr) & (Bill_line.artnr == sum_tbl.mwst_code)).order_by(Bill_line._recid).all():
                            sum_anz =  to_decimal(sum_anz) + to_decimal(bill_line.anzahl)
                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + bl_descript + lnldelimeter + to_string(sum_anz, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest

                elif inv_type == 3:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        sum_tbl = query(sum_tbl_list, filters=(lambda sum_tbl: sum_tbl.sum_desc == bill_line.bezeich), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_list.append(sum_tbl)

                            sum_tbl.sum_date = to_string(bill_line.bill_datum)
                            sum_tbl.sum_desc = bill_line.bezeich
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        sum_tbl = query(sum_tbl_list, filters=(lambda sum_tbl: sum_tbl.sum_desc == bill_line.bezeich), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_list.append(sum_tbl)

                            sum_tbl.sum_desc = bill_line.bezeich
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_list):
                        sum_anz =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == rechnr) & (Bill_line.bezeich == sum_tbl.sum_desc)).order_by(Bill_line._recid).all():
                            sum_anz =  to_decimal(sum_anz) + to_decimal(bill_line.anzahl)
                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = sum_tbl.sum_date + lnldelimeter + bl_descript + lnldelimeter + to_string(sum_anz, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3


                else:

                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3


            else:

                if inv_type == 2:

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)


                        bl_descript0 = entry(0, bl_descript, "/")
                        bl_voucher = ""

                        if num_entries(bl_descript, "/") > 1:

                            if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3

                elif inv_type == 3:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit, Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                        str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.bezeich + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3


                else:

                    bill_line_obj_list = []
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        t_spbill_list = query(t_spbill_list_list, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if re.match(r".*c/i.*",bl_descript, re.IGNORECASE) or re.match(r".*c/o.*",bl_descript, re.IGNORECASE):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == bill_line.massnr) & (Res_line.reslinnr == bill_line.billin_nr) & (Res_line.zinr == bill_line.zinr)).first()

                        if res_line:

                            guest = db_session.query(Guest).filter(
                                     (Guest.gastnr == res_line.gastnrmember)).first()

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = str3

    elif curr_program.lower()  == ("fo-invoice").lower() :

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

        if not res_line:

            return generate_output()

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 242)).first()
        paidout = htparam.finteger
        bline_list_list.clear()

        if not spbill_flag:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()

                if not artikel:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == bill_line.artnr) & (Artikel.departement == 0)).first()
                bline_list = Bline_list()
                bline_list_list.append(bline_list)

                buffer_copy(bill_line, bline_list)
                bline_list.bl_recid = bill_line._recid
                bline_list.dept = bill_line.departement
                bline_list.datum = bill_line.bill_datum
                bline_list.fsaldo =  to_decimal("0")
                bline_list.saldo =  to_decimal(bill_line.betrag)
                bline_list.epreis =  to_decimal(bill_line.epreis)


                bline_list.fsaldo = calc_bl_balance1(bill_line.bill_datum, bill_line.betrag, bill_line.fremdwbetrag, bline_list.fsaldo)

        else:

            bill_line_obj_list = []
            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)

                t_spbill_list = query(t_spbill_list_list, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()

                if not artikel:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == bill_line.artnr) & (Artikel.departement == 0)).first()
                bline_list = Bline_list()
                bline_list_list.append(bline_list)

                buffer_copy(bill_line, bline_list)
                bline_list.bl_recid = bill_line._recid
                bline_list.dept = bill_line.departement
                bline_list.datum = bill_line.bill_datum
                bline_list.fsaldo =  to_decimal("0")
                bline_list.saldo =  to_decimal(bill_line.betrag)
                bline_list.epreis =  to_decimal(bill_line.epreis)


                bline_list.fsaldo = calc_bl_balance1(bill_line.bill_datum, bill_line.betrag, bill_line.fremdwbetrag, bline_list.fsaldo)


        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 127)).first()
        rm_vat = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 128)).first()
        rm_serv = htparam.flogical

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == arrangement.artnr_logis) & (Artikel.departement == 0)).first()

        if res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        service =  to_decimal("0")
        vat =  to_decimal("0")

        if rm_serv:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.service_code)).first()

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if rm_vat:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 479)).first()

            if htparam.flogical:
                vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrpay)).first()

        if guest:

            if guest.karteityp == 0:

                if guest.anrede1 != "":
                    bill_recv = guest.anrede1 + ". "

                elif guest.vorname1 != "":
                    bill_recv = bill_recv + guest.vorname1 + " "
                bill_recv = bill_recv + guest.name
            else:

                if guest.anredefirma != "":
                    bill_recv = guest.anredefirma + ". "
                bill_recv = bill_recv + guest.name
            bill_recv = trim(bill_recv)
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            email = trim(guest.email_adr)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
            phone = to_string(guest.telefon, "x(16)")
            guest_taxcode = to_string(guest.firmen_nr)

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 109)).first()
            wi_gastnr = htparam.finteger

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 123)).first()
            ind_gastnr = htparam.finteger

            if guest.karteityp == 0 or guest.gastnr == wi_gastnr or guest.gastnr == ind_gastnr:
                room_price = to_string(res_line.zipreis, ">>>,>>>,>>9.99")

            elif res_line.gastnrmember == res_line.gastnrpay:
                room_price = to_string(res_line.zipreis, ">>>,>>>,>>9.99")

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == bill.resnr) & (Res_line.resnr == bill.reslinnr)).first()

        if res_line:

            guest1 = db_session.query(Guest1).filter(
                     (Guest1.gastnr == res_line.gastnrmember)).first()

            if guest1:
                hp_guest = to_string(guest1.mobil_telefon, "x(16)")


        ma_gst_amount =  to_decimal("0")
        ma_gst_tot_sales_artikel =  to_decimal("0")
        ma_gst_tot_non_taxable =  to_decimal("0")
        ma_gst_tot_taxable =  to_decimal("0")
        mgst =  to_decimal("0")
        tot_service_code =  to_decimal("0")

        bill_line_obj_list = []
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                 (Bill_line._recid.in_(list(set([bline_list.bl_recid for bline_list in bline_list_list]))))).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
            if bill_line._recid in bill_line_obj_list:
                continue
            else:
                bill_line_obj_list.append(bill_line._recid)


            bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
            bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
            bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

            if (artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9):
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

            elif artikel.artart == 6 and artikel.zwkum == paidout:
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                serv1 =  to_decimal("0")
                vat1 =  to_decimal("0")
                vat3 =  to_decimal("0")
                fact1 =  to_decimal("0")


                ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                if bill_line.bill_datum <= 08/31/18:

                    if artikel.mwst_code != 0:

                        htparam = db_session.query(Htparam).filter(
                                     (Htparam.paramnr == artikel.mwst_code)).first()

                        if htparam:
                            ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                    elif artikel.mwst_code == 0:
                        ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                else:

                    if artikel.artnr == 1001 or artikel.artnr == 1002:

                        if bill_line.betrag > 0:
                            artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)
                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)


                    else:

                        if artikel.artnr != 1001:

                            if artikel.mwst_code != 0:

                                htparam = db_session.query(Htparam).filter(
                                             (Htparam.paramnr == artikel.mwst_code)).first()

                                if htparam:
                                    ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                            elif artikel.mwst_code == 0:
                                ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

                if artikel.service_code != 0:
                    serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                    netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                    tot_service_code =  to_decimal(tot_service_code) + to_decimal((netto) * to_decimal(serv1) )

                if artnr_1001 == 0 and ma_gst_amount == 0 and artikel.mwst_code != 0:
                    serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                    netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                    mgst =  to_decimal(mgst) + to_decimal((netto) * to_decimal((vat1) + to_decimal(vat3)) )

        if ma_gst_amount != 0:
            ma_gst_amount = ( to_decimal(ma_gst_amount) * to_decimal("6") / to_decimal(100)) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        elif artnr_1001 != 0:
            ma_gst_amount =  to_decimal(artnr_1001)
            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(artnr_1001) - to_decimal(ma_gst_tot_non_taxable) )


            ma_gst_gtot_tax =  to_decimal(artnr_1001) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)
        else:
            ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 416)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 410)).first()
        progname = htparam.fchar

        if (progname != ""):

            if progname.lower()  == ("word_chinese.p").lower() :

                if briefnr == briefnr2:
                    sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr3)
            else:

                if briefnr == briefnr2 or briefnr == briefnr21:
                    sstr1, sstr2 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2 or spbill_flag:
                        sstr1, sstr2 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr1) + " " + trim(sstr2)

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

        if res_line:

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == res_line.zinr)).first()

            if zimmer:
                room_cat = zimmer.bezeich
            room_no = trim(res_line.zinr)

            if bill and bill.resnr > 0 and bill.reslinnr == 0:

                if res_line.resstatus >= 6 and res_line.resstatus <= 8:
                    arrival = to_string(res_line.ankunft)
                    departure = to_string(res_line.abreise)
            else:
                arrival = to_string(res_line.ankunft)

                if res_line.ankzeit != 0:
                    arrival = to_string(res_line.ankunft) + " " + to_string(res_line.ankzeit, "HH:MM")
                    departure = to_string(res_line.abreise) + " " + to_string(res_line.abreisezeit, "HH:MM")

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:
                bl_guest = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == guest.gastnr)).first()

                if mc_guest:
                    membernumber = mc_guest.cardnum

            if res_line.code != "":

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

                if queasy:
                    bl_instruct = trim(queasy.char1)

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.l_zuordnung[inc_value(2)] != 0)).first()

            if resline:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == resline.gastnrmember)).first()

                if guest:
                    bl_accom = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name


            acc = to_string(res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis)
            adult = to_string(res_line.erwachs)
            child1 = to_string(res_line.kind1)
            child2 = to_string(res_line.kind2)
            complgst = to_string(res_line.gratis)
            resno = to_string(resnr)

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 271)).first()

        if htparam.flogical:
            bline_vatlist_list = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_list, first=True)

            if bline_vatlist:
                do_it = True

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == bill.resnr)).first()

        if reservation:
            resv_name = reservation.name

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            username = bediener.username

        if address1 == None:
            address1 = ""

        if address2 == None:
            address2 = ""

        if address3 == None:
            address3 = ""

        if email == None:
            email = ""

        if hp_no == None:
            hp_no = ""

        if acc == None:
            acc = ""

        if adult == None:
            adult = ""

        if child1 == None:
            child1 = ""

        if child2 == None:
            child2 = ""

        if complgst == None:
            complgst = ""

        if room_no == None:
            room_no = ""

        if room_price == None:
            room_price = ""

        if arrival == None:
            arrival = ""

        if arrival == None:
            arrival = ""

        if departure == None:
            departure = ""

        if bl_guest == None:
            bl_guest = ""

        if resno == None:
            resno = ""

        if bl_guest == None:
            bl_guest = ""

        if htl_adr1 == None:
            htl_adr1 = ""

        if htl_adr2 == None:
            htl_adr2 = ""

        if htl_adr3 == None:
            htl_adr3 = ""

        if bl_instruct == None:
            bl_instruct = ""

        if user_init == None:
            user_init = ""

        if room_cat == None:
            room_cat = ""

        if htl_tel == None:
            htl_tel = ""

        if htl_fax == None:
            htl_fax = ""

        if htl_email == None:
            htl_email = ""

        if hp_guest == None:
            hp_guest = ""

        if phone == None:
            phone = ""

        if membernumber == None:
            membernumber = ""

        if resv_name == None:
            resv_name = ""

        if guest_taxcode == None:
            guest_taxcode = ""

        if in_word == None:
            in_word = ""

        if bl_accom == None:
            bl_accom = ""

        if username == None:
            username = ""
        str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$email" + email + lnldelimeter + "$hp-no" + hp_no + lnldelimeter + "$acc" + acc + lnldelimeter + "$adult" + adult + lnldelimeter + "$child1" + child1 + lnldelimeter + "$child2" + child2 + lnldelimeter + "$complgst" + complgst + lnldelimeter + "$room-no" + room_no + lnldelimeter + "$room-price" + room_price + lnldelimeter + "$arrival" + arrival + lnldelimeter + "$arrival0" + arrival + lnldelimeter + "$departure" + departure + lnldelimeter + "$departure0" + departure + lnldelimeter + "$bl-guest" + trim(bl_guest) + lnldelimeter + "$bl-instruct" + bl_instruct + lnldelimeter + "$resno" + resno + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter + "$room-cat" + room_cat + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$resv-name" + resv_name + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$guest-taxcode" + guest_taxcode + lnldelimeter + "$in-word" + in_word + lnldelimeter + "$acc-guest" + bl_accom + lnldelimeter + "$bl-username" + username
        str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("Description/Voucher", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("RmNo", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("ID", lvcarea, "") + lnldelimeter + translateExtended ("Guest Name", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("Amount Before Tax", lvcarea, "") + lnldelimeter + translateExtended ("Foreign Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("In Word", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "") + lnldelimeter + translateExtended ("Convert Currency", lvcarea, "") + lnldelimeter + translateExtended ("Currency", lvcarea, "") + lnldelimeter + translateExtended ("Description Currency", lvcarea, "")
        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            bline_list = query(bline_list_list, first=True)

            if not bline_list:

                return generate_output()
            bl_descript = bline_list.bezeich
            bl_descript0 = entry(0, bl_descript, "/")

            if num_entries(bl_descript, "/") > 1:
                bl_voucher = entry(1, bl_descript, "/")
            amount_bef_tax =  to_decimal(bline_list.saldo)
            amount_bef_tax =  to_decimal(amount_bef_tax) / to_decimal((1) + to_decimal(service) + to_decimal(vat))
            bl_balance =  to_decimal(bl_balance) + to_decimal(bline_list.saldo)
            ma_gst_amount =  to_decimal("0")
            str3 = to_string(bline_list.datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bline_list.anzahl, "->>>") + lnldelimeter + bline_list.zinr + lnldelimeter + to_string(bline_list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bline_list.userinit + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(amount_bef_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bline_list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(for_curr, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + conv_wabkurz + lnldelimeter + curr_bezeich
            t_str3 = T_str3()
            t_str3_list.append(t_str3)

            t_str3.str3 = str3

            if do_it:

                bline_vatlist = query(bline_vatlist_list, first=True)

                if bline_vatlist:
                    str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                    t_str3 = query(t_str3_list, first=True)

                    if t_str3:
                        t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            for bline_list in query(bline_list_list, sort_by=[("datum",False)]):
                bl_voucher = ""
                bl_descript = bline_list.bezeich
                bl_descript0 = entry(0, bl_descript, "/")

                if num_entries(bl_descript, "/") > 1:
                    bl_voucher = entry(1, bl_descript, "/")
                fact =  to_decimal("1")

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line._recid == bline_list.bl_recid)).first()

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()

                if artikel.mwst_code != 0 or artikel.service_code != 0 or artikel.prov_code != 0:
                    service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                vat =  to_decimal(vat) + to_decimal(vat2)


                amount_bef_tax =  to_decimal(bline_list.saldo)
                amount_bef_tax =  to_decimal(amount_bef_tax) / to_decimal(fact)
                bl_balance =  to_decimal(bl_balance) + to_decimal(bline_list.saldo)
                str3 = to_string(bline_list.datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bline_list.anzahl, "->>>") + lnldelimeter + bline_list.zinr + lnldelimeter + to_string(bline_list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bline_list.userinit + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(amount_bef_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bline_list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(for_curr, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + conv_wabkurz + lnldelimeter + curr_bezeich + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")
                t_str3 = T_str3()
                t_str3_list.append(t_str3)

                t_str3.str3 = str3

            if do_it:

                for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                    str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                    t_str3 = T_str3()
                    t_str3_list.append(t_str3)

                    t_str3.str3 = str3

    elif curr_program.lower()  == ("master-inv").lower() :

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastnr)).first()

        if guest:

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == res_line.gastnrmember)).first()

            if mc_guest:
                membernumber = mc_guest.cardnum
            bill_recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
            phone = to_string(guest.telefon, "x(16)")

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == bill.resnr)).first()

        if reservation:
            resv_name = reservation.name

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr)).first()

        if res_line:
            room_no = trim(res_line.zinr)

            if bill and bill.resnr > 0 and bill.reslinnr == 0:

                if res_line.resstatus >= 6 and res_line.resstatus <= 8:
                    arrival = to_string(res_line.ankunft)
                    departure = to_string(res_line.abreise)
            else:
                arrival = to_string(res_line.ankunft)

                if res_line.ankzeit != 0:
                    arrival = to_string(res_line.ankunft) + " " + to_string(res_line.ankzeit, "HH:MM")
                    departure = to_string(res_line.abreise) + " " + to_string(res_line.abreisezeit, "HH:MM")

            guest1 = db_session.query(Guest1).filter(
                     (Guest1.gastnr == res_line.gastnrmember)).first()

            if guest1:
                hp_guest = to_string(guest.mobil_telefon, "x(16)")

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).order_by(Res_line.name, Res_line.zinr).all():

                if res_line.name != " ":
                    bl_guest = bl_guest + res_line.name + " # " + res_line.zinr + chr(10)

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")
        ma_gst_amount =  to_decimal("0")
        ma_gst_tot_sales_artikel =  to_decimal("0")
        ma_gst_tot_non_taxable =  to_decimal("0")
        ma_gst_tot_taxable =  to_decimal("0")
        tot_service_code =  to_decimal("0")

        if not spbill_flag:

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                    bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                elif artikel.artart == 6 and artikel.zwkum == paidout:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    serv1 =  to_decimal("0")
                    vat1 =  to_decimal("0")
                    vat3 =  to_decimal("0")
                    fact1 =  to_decimal("0")


                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                         (Htparam.paramnr == artikel.mwst_code)).first()

                            if htparam:
                                ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                        elif artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)
                                mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)


                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:

                                    htparam = db_session.query(Htparam).filter(
                                                 (Htparam.paramnr == artikel.mwst_code)).first()

                                    if htparam:
                                        ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                                elif artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

                    if artikel.service_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        tot_service_code =  to_decimal(tot_service_code) + to_decimal((netto) * to_decimal(serv1) )

                    if artnr_1001 == 0 and ma_gst_amount == 0 and artikel.mwst_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        mgst =  to_decimal(mgst) + to_decimal((netto) * to_decimal((vat1) + to_decimal(vat3)) )

        else:

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)

                t_spbill_list = query(t_spbill_list_list, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                if (artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9):
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

                elif artikel.artart == 6 and artikel.zwkum == paidout:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    serv1 =  to_decimal("0")
                    vat1 =  to_decimal("0")
                    vat3 =  to_decimal("0")
                    fact1 =  to_decimal("0")


                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:

                            htparam = db_session.query(Htparam).filter(
                                         (Htparam.paramnr == artikel.mwst_code)).first()

                            if htparam:
                                ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                        elif artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)
                                mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)


                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:

                                    htparam = db_session.query(Htparam).filter(
                                                 (Htparam.paramnr == artikel.mwst_code)).first()

                                    if htparam:
                                        ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal((1) + to_decimal((htparam.fdecimal) / to_decimal(100))) )

                                elif artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

                    if artikel.service_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        tot_service_code =  to_decimal(tot_service_code) + to_decimal((netto) * to_decimal(serv1) )

                    if artnr_1001 == 0 and ma_gst_amount == 0 and artikel.mwst_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        mgst =  to_decimal(mgst) + to_decimal((netto) * to_decimal((vat1) + to_decimal(vat3)) )


        if ma_gst_amount != 0:
            ma_gst_amount = ( to_decimal(ma_gst_amount) * to_decimal("6") / to_decimal(100)) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        elif artnr_1001 != 0:
            ma_gst_amount =  to_decimal(artnr_1001)
            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(artnr_1001) - to_decimal(ma_gst_tot_non_taxable) )
            ma_gst_gtot_tax =  to_decimal(artnr_1001) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)


        else:
            ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 416)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 410)).first()
        progname = htparam.fchar

        if (progname != ""):

            if progname.lower()  == ("word_chinese.p").lower() :

                if briefnr == briefnr2:
                    sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr3)
            else:

                if briefnr == briefnr2 or briefnr == briefnr21:
                    sstr1, sstr2 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2:
                        sstr1, sstr2 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr1) + " " + trim(sstr2)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 271)).first()

        if htparam.flogical:
            bline_vatlist_list = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_list, first=True)

            if bline_vatlist:
                do_it = True


        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if email == None:
                email = ""

            if hp_no == None:
                hp_no = ""

            if acc == None:
                acc = ""

            if adult == None:
                adult = ""

            if child1 == None:
                child1 = ""

            if child2 == None:
                child2 = ""

            if complgst == None:
                complgst = ""

            if room_no == None:
                room_no = ""

            if room_price == None:
                room_price = ""

            if arrival == None:
                arrival = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if bl_guest == None:
                bl_guest = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bl_instruct == None:
                bl_instruct = ""

            if user_init == None:
                user_init = ""

            if room_cat == None:
                room_cat = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if resv_name == None:
                resv_name = ""

            if guest_taxcode == None:
                guest_taxcode = ""

            if in_word == None:
                in_word = ""

            if bl_accom == None:
                bl_accom = ""

            if username == None:
                username = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$hp-no" + hp_no + lnldelimeter + "$room-no" + room_no + lnldelimeter + "$arrival" + arrival + lnldelimeter + "$arrival0" + arrival + lnldelimeter + "$departure" + departure + lnldelimeter + "$departure0" + departure + lnldelimeter + "$bl-guest" + bl_guest + lnldelimeter + "$resno" + resno + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$resv-name" + resv_name + lnldelimeter + "$bl-username" + username
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$acc-guest" + bl_accom
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("RmNo", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("ID", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if inv_type == 2:

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == rechnr)).first()

                if bill_line:

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                    if res_line:
                        l_guest = res_line.name


                    bl_voucher = ""
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:
                        bl_voucher = entry(1, bl_descript, "/")
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bill_line.bezeich + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest

                if do_it:

                    bline_vatlist = query(bline_vatlist_list, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_list, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
            else:

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.rechnr == rechnr)).first()

                if bill_line:

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                    if res_line:
                        l_guest = res_line.name


                    bl_voucher = ""
                    bl_descript = bill_line.bezeich
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:
                        bl_voucher = entry(1, bl_descript, "/")
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bill_line.bezeich + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest

                if do_it:

                    bline_vatlist = query(bline_vatlist_list, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_list, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if email == None:
                email = ""

            if hp_no == None:
                hp_no = ""

            if acc == None:
                acc = ""

            if adult == None:
                adult = ""

            if child1 == None:
                child1 = ""

            if child2 == None:
                child2 = ""

            if complgst == None:
                complgst = ""

            if room_no == None:
                room_no = ""

            if room_price == None:
                room_price = ""

            if arrival == None:
                arrival = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if bl_guest == None:
                bl_guest = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bl_instruct == None:
                bl_instruct = ""

            if user_init == None:
                user_init = ""

            if room_cat == None:
                room_cat = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if resv_name == None:
                resv_name = ""

            if guest_taxcode == None:
                guest_taxcode = ""

            if in_word == None:
                in_word = ""

            if bl_accom == None:
                bl_accom = ""

            if username == None:
                username = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$hp-no" + hp_no + lnldelimeter + "$room-no" + room_no + lnldelimeter + "$arrival" + arrival + lnldelimeter + "$arrival0" + arrival + lnldelimeter + "$departure" + departure + lnldelimeter + "$departure0" + departure + lnldelimeter + "$bl-guest" + bl_guest + lnldelimeter + "$resno" + resno + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$resv-name" + resv_name + lnldelimeter + "$acc-guest" + bl_accom + lnldelimeter + "$bl-username" + username
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$acc-guest" + bl_accom
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("RmNo", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("ID", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if not spbill_flag:

                if inv_type == 2:

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        sum_tbl = query(sum_tbl_list, filters=(lambda sum_tbl: sum_tbl.mwst_code == artikel.mwst_code), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_list.append(sum_tbl)

                            sum_tbl.mwst_code = artikel.mwst_code
                            sum_tbl.sum_desc = bl_descript
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_list):
                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + "" + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "" + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3

                elif inv_type == 4:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        sum_tbl = query(sum_tbl_list, filters=(lambda sum_tbl: sum_tbl.sum_desc == bill_line.bezeich and sum_tbl.sum_roomnr == bill_line.zinr), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_list.append(sum_tbl)

                            sum_tbl.sum_date = to_string(bill_line.bill_datum)
                            sum_tbl.sum_desc = bill_line.bezeich
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)
                            sum_tbl.sum_roomnr = bill_line.zinr
                            sum_tbl.sum_id = bill_line.userinit


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_list):
                        sum_anz =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == rechnr) & (Bill_line.bezeich == sum_tbl.sum_desc)).order_by(Bill_line._recid).all():
                            sum_anz =  to_decimal(sum_anz) + to_decimal(bill_line.anzahl)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == resnr) & (Res_line.zinr == sum_tbl.sum_roomnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                        if res_line:
                            l_guest = res_line.name


                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(sum_tbl.sum_date) + lnldelimeter + sum_tbl.sum_roomnr + lnldelimeter + bl_descript + lnldelimeter + to_string(sum_anz, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + sum_tbl.sum_id + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3


                else:

                    t_spbill_list = query(t_spbill_list_list, filters=(lambda t_spbill_list: t_spbill_list.selected), first=True)
                select_flag = None != t_spbill_list

                if select_flag :

                    bill_line_obj_list = []
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                        if res_line:
                            l_guest = res_line.name


                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")
                else:

                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                        if res_line:
                            l_guest = res_line.name

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                if do_it:

                    for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = str3


            else:

                if inv_type == 2:

                    bill_line_obj_list = []
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)


                        bl_voucher = ""
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                        if res_line:
                            l_guest = res_line.name


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + "" + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "" + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_list.append(t_str3)

                            t_str3.str3 = str3

                elif inv_type == 4:

                    bill_line_obj_list = []
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit, Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        t_spbill_list = query(t_spbill_list_list, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                        if res_line:
                            l_guest = res_line.name


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = str3


                else:

                    bill_line_obj_list = []
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_list if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line._recid in bill_line_obj_list:
                            continue
                        else:
                            bill_line_obj_list.append(bill_line._recid)

                        t_spbill_list = query(t_spbill_list_list, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == resnr) & (Res_line.zinr == bill_line.zinr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).first()

                        if res_line:
                            l_guest = res_line.name


                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_list.append(t_str3)

                        t_str3.str3 = str3

    if curr_program.lower()  == ("master-inv-room").lower() :

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastnr)).first()

        if guest:
            bill_recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            city = trim(guest.wohnort)
            country = trim(guest.land)
            zip = trim(guest.plz)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
        bline_list_list.clear()

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == rechnr) & (func.lower(Bill_line.zinr) == (selected_room).lower())).order_by(Bill_line._recid).all():
            bline_list = Bline_list()
            bline_list_list.append(bline_list)

            buffer_copy(bill_line, bline_list)
            bline_list.bl_recid = bill_line._recid
            bline_list.dept = bill_line.departement
            bline_list.datum = bill_line.bill_datum
            bline_list.fsaldo =  to_decimal("0")
            bline_list.saldo =  to_decimal(bill_line.betrag)
            bline_list.epreis =  to_decimal(bill_line.epreis)


            bline_list.fsaldo = calc_bl_balance1(bill_line.bill_datum, bill_line.betrag, bill_line.fremdwbetrag, bline_list.fsaldo)

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.resstatus != 12) & (func.lower(Res_line.zinr) == (selected_room).lower())).first()

        if res_line:
            reslinnr = res_line.reslinnr

            if bill and bill.resnr > 0 and bill.reslinnr == 0:

                if res_line.resstatus >= 6 and res_line.resstatus <= 8:
                    arrival = to_string(res_line.ankunft)
                    departure = to_string(res_line.abreise)
            else:
                arrival = to_string(res_line.ankunft)

                if res_line.ankzeit != 0:
                    arrival = to_string(res_line.ankunft) + " " + to_string(res_line.ankzeit, "HH:MM")
                    departure = to_string(res_line.abreise) + " " + to_string(res_line.abreisezeit, "HH:MM")

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:
                bl_guest = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.l_zuordnung[inc_value(2)] != 0)).first()

            if resline:

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == resline.gastnrmember)).first()

                if guest:
                    bl_accom = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name


            acc = to_string(res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis)
            adult = to_string(res_line.erwachs)
            child1 = to_string(res_line.kind1)
            child2 = to_string(res_line.kind2)
            complgst = to_string(res_line.gratis)
            resno = to_string(resnr)

        zimmer = db_session.query(Zimmer).filter(
                 (func.lower(Zimmer.zinr) == (selected_room).lower())).first()

        if zimmer:
            room_cat = zimmer.bezeich

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")

        bill_line_obj_list = []
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                 (Bill_line._recid.in_(list(set([bline_list.bl_recid for bline_list in bline_list_list]))))).order_by(Bill_line._recid).all():
            if bill_line._recid in bill_line_obj_list:
                continue
            else:
                bill_line_obj_list.append(bill_line._recid)


            bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
            bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
            bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

            if (artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9):
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

            elif artikel.artart == 6 and artikel.zwkum == paidout:
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 416)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 410)).first()
        progname = htparam.fchar

        if (progname != ""):

            if progname.lower()  == ("word_chinese.p").lower() :

                if briefnr == briefnr2:
                    sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2, sstr3 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr3)
            else:

                if briefnr == briefnr2 or briefnr == briefnr21:
                    sstr1, sstr2 = get_output(run_program(progname,(bl0_balance1, w_length)))
                else:

                    if bl0_balance != 0:
                        sstr1, sstr2 = get_output(run_program(progname,(bl0_balance, w_length)))

                    elif inv_type == 2 or spbill_flag:
                        sstr1, sstr2 = get_output(run_program(progname,(bl_balance, w_length)))
                    else:
                        sstr1, sstr2 = get_output(run_program(progname,(bill.saldo, w_length)))
                in_word = trim(sstr1) + " " + trim(sstr2)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 271)).first()

        if htparam.flogical:
            bline_vatlist_list = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_list, first=True)

            if bline_vatlist:
                do_it = True


        room_no = selected_room

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")
        str1 = "$bill-recv" + bill_recv + lnldelimeter +\
                "$bill-no" + bill_no + lnldelimeter +\
                "$address1" + address1 + lnldelimeter +\
                "$address2" + address2 + lnldelimeter +\
                "$address3" + address3 + lnldelimeter +\
                "$city" + city + lnldelimeter +\
                "$country" + country + lnldelimeter +\
                "$zip" + zip + lnldelimeter +\
                "$email" + email + lnldelimeter +\
                "$hp-no" + hp_no + lnldelimeter +\
                "$acc" + acc + lnldelimeter +\
                "$adult" + adult + lnldelimeter +\
                "$child1" + child1 + lnldelimeter +\
                "$child2" + child2 + lnldelimeter +\
                "$complgst" + complgst + lnldelimeter +\
                "$room-no" + room_no + lnldelimeter +\
                "$room-price" + room_price + lnldelimeter +\
                "$arrival" + arrival + lnldelimeter +\
                "$arrival0" + arrival + lnldelimeter +\
                "$departure" + departure + lnldelimeter +\
                "$departure0" + departure + lnldelimeter +\
                "$bl-guest" + trim(bl_guest) + lnldelimeter +\
                "$bl-instruct" + bl_instruct + lnldelimeter +\
                "$resno" + resno + lnldelimeter +\
                "$bl-id" + user_init + lnldelimeter +\
                "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter +\
                "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter +\
                "$room-cat" + room_cat + lnldelimeter +\
                "$htl-name" + htl_name + lnldelimeter +\
                "$htl-adr1" + htl_adr1 + lnldelimeter +\
                "$htl-adr2" + htl_adr2 + lnldelimeter +\
                "$htl-adr3" + htl_adr3 + lnldelimeter +\
                "$htl-tel" + htl_tel + lnldelimeter +\
                "$htl-fax" + htl_fax + lnldelimeter +\
                "$htl-email" + htl_email + lnldelimeter +\
                "$reslinnr" + to_string(reslinnr)
        str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter +\
                translateExtended ("Description/Voucher", lvcarea, "") + lnldelimeter +\
                translateExtended ("Qty", lvcarea, "") + lnldelimeter +\
                translateExtended ("RmNo", lvcarea, "") + lnldelimeter +\
                translateExtended ("Amount", lvcarea, "") + lnldelimeter +\
                translateExtended ("ID", lvcarea, "") + lnldelimeter +\
                translateExtended ("Guest Name", lvcarea, "") + lnldelimeter +\
                translateExtended ("Description", lvcarea, "") + lnldelimeter +\
                translateExtended ("Voucher", lvcarea, "") + lnldelimeter +\
                translateExtended ("Amount Before Tax", lvcarea, "") + lnldelimeter +\
                translateExtended ("Foreign Amount", lvcarea, "") + lnldelimeter +\
                translateExtended ("Balance", lvcarea, "") + lnldelimeter +\
                translateExtended ("In Word", lvcarea, "")
        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            bline_list = query(bline_list_list, first=True)

            if not bline_list:

                return generate_output()
            bl_descript = bline_list.bezeich
            bl_descript0 = entry(0, bl_descript, "/")

            if num_entries(bl_descript, "/") > 1:
                bl_voucher = entry(1, bl_descript, "/")
            amount_bef_tax =  to_decimal(bline_list.saldo)
            amount_bef_tax =  to_decimal(amount_bef_tax) / to_decimal((1) + to_decimal(service) + to_decimal(vat))
            bl_balance =  to_decimal(bl_balance) + to_decimal(bline_list.saldo)
            str3 = to_string(bline_list.datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bline_list.anzahl, "->>>") + lnldelimeter + bline_list.zinr + lnldelimeter + to_string(bline_list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bline_list.userinit + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(amount_bef_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bline_list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word
            t_str3 = T_str3()
            t_str3_list.append(t_str3)

            t_str3.str3 = str3

            if do_it:

                bline_vatlist = query(bline_vatlist_list, first=True)

                if bline_vatlist:
                    str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                    t_str3 = query(t_str3_list, first=True)

                    if t_str3:
                        t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            for bline_list in query(bline_list_list):

                if num_entries(bline_list.bezeich, "/") > 1:
                    bl_voucher = entry(1, bline_list.bezeich, "/")
                bl_descript = bline_list.bezeich
                bl_descript0 = entry(0, bl_descript, "/")
                amount_bef_tax =  to_decimal(bline_list.saldo)
                amount_bef_tax =  to_decimal(amount_bef_tax) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                bl_balance =  to_decimal(bl_balance) + to_decimal(bline_list.saldo)
                str3 = to_string(bline_list.datum) + lnldelimeter +\
                        bl_descript + lnldelimeter +\
                        to_string(bline_list.anzahl, "->>>") + lnldelimeter +\
                        bline_list.zinr + lnldelimeter +\
                        to_string(bline_list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter +\
                        bline_list.userinit + lnldelimeter +\
                        bl_guest + lnldelimeter +\
                        bl_descript0 + lnldelimeter +\
                        bl_voucher + lnldelimeter +\
                        to_string(amount_bef_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter +\
                        to_string(bline_list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter +\
                        to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter +\
                        in_word + lnldelimeter +\
                        to_string(" ") + lnldelimeter +\
                        to_string(" ")


                t_str3 = T_str3()
                t_str3_list.append(t_str3)

                t_str3.str3 = str3

            if do_it:

                for bline_vatlist in query(bline_vatlist_list, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                    str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                    t_str3 = T_str3()
                    t_str3_list.append(t_str3)

                    t_str3.str3 = str3

    return generate_output()