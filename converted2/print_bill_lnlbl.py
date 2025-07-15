#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.fobill_vatlistbl import fobill_vatlistbl
from models import Guest, Htparam, Paramtext, Bill, Mc_guest, Res_line, Artikel, Bill_line, Arrangement, Waehrung, Zimmer, Queasy, Exrate

t_spbill_list_data, T_spbill_list = create_model("T_spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})

def print_bill_lnlbl(t_spbill_list_data:[T_spbill_list], pvilanguage:int, curr_status:string, briefnr:int, resnr:int, reslinnr:int, inv_type:int, rechnr:int, curr_program:string, gastnr:int, spbill_flag:bool, user_init:string, lnldelimeter:string):

    prepare_cache ([Guest, Htparam, Paramtext, Bill, Mc_guest, Res_line, Artikel, Arrangement, Waehrung, Zimmer, Queasy, Exrate])

    str1 = ""
    str2 = ""
    str3 = ""
    t_str3_data = []
    lvcarea:string = "print-bill-lnl"
    briefnr2:int = 0
    briefnr21:int = 0
    htl_name:string = ""
    htl_adr1:string = ""
    htl_adr2:string = ""
    htl_adr3:string = ""
    htl_tel:string = ""
    htl_fax:string = ""
    htl_email:string = ""
    bill_recv:string = ""
    bill_no:string = ""
    bl_descript:string = ""
    bl_descript0:string = ""
    bl_voucher:string = ""
    bl0_balance:Decimal = 0
    bl0_balance1:Decimal = 0
    bl_balance:Decimal = 0
    bl_balance1:Decimal = 0
    sum_anz:Decimal = 0
    address1:string = ""
    address2:string = ""
    address3:string = ""
    email:string = ""
    hp_no:string = ""
    acc:string = ""
    adult:string = ""
    child1:string = ""
    child2:string = ""
    complgst:string = ""
    room_no:string = ""
    room_price:string = ""
    arrival:string = ""
    departure:string = ""
    bl_guest:string = ""
    l_guest:string = ""
    bl_instruct:string = ""
    resno:string = ""
    in_word:string = ""
    room_cat:string = ""
    city:string = ""
    country:string = ""
    zip:string = ""
    hp_guest:string = ""
    phone:string = ""
    sstr1:string = ""
    sstr2:string = ""
    sstr3:string = ""
    w_length:int = 40
    progname:string = ""
    temp_amt:Decimal = to_decimal("0.0")
    wi_gastnr:int = 0
    ind_gastnr:int = 0
    ma_gst_amount:Decimal = to_decimal("0.0")
    ma_gst_tot_sales_artikel:Decimal = to_decimal("0.0")
    ma_gst_tot_non_taxable:Decimal = to_decimal("0.0")
    ma_gst_tot_taxable:Decimal = to_decimal("0.0")
    ma_gst_gtot_tax:Decimal = to_decimal("0.0")
    curr_guest:string = ""
    tot_inclvat:Decimal = to_decimal("0.0")
    net_amount:Decimal = to_decimal("0.0")
    serv_code:Decimal = to_decimal("0.0")
    acc_tax:Decimal = to_decimal("0.0")
    vat_cam:Decimal = to_decimal("0.0")
    do_it:bool = False
    membernumber:string = ""
    mgst:Decimal = to_decimal("0.0")
    artnr_1001:Decimal = to_decimal("0.0")
    guest_taxcode:string = ""
    nopd:string = ""
    tot_service_code:Decimal = to_decimal("0.0")
    serv1:Decimal = to_decimal("0.0")
    vat1:Decimal = to_decimal("0.0")
    vat3:Decimal = to_decimal("0.0")
    fact1:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    selected_room:string = ""
    service_ns:Decimal = to_decimal("0.0")
    vat_ns:Decimal = to_decimal("0.0")
    amount_bef_tax_ns:Decimal = to_decimal("0.0")
    vat2_ns:Decimal = to_decimal("0.0")
    fact_ns:Decimal = 1
    paidout:int = 0
    frate:Decimal = 1
    rm_serv:bool = False
    rm_vat:bool = False
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    amount_bef_tax:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = 1
    guest = htparam = paramtext = bill = mc_guest = res_line = artikel = bill_line = arrangement = waehrung = zimmer = queasy = exrate = None

    bline_list = sum_tbl = t_str3 = t_spbill_list = bl_guest = bline_vatlist = guest1 = None

    bline_list_data, Bline_list = create_model("Bline_list", {"bl_recid":int, "artnr":int, "dept":int, "anzahl":int, "massnr":int, "billin_nr":int, "zeit":int, "mwst_code":int, "vatproz":Decimal, "epreis":Decimal, "netto":Decimal, "fsaldo":Decimal, "saldo":Decimal, "orts_tax":Decimal, "voucher":string, "bezeich":string, "zinr":string, "gname":string, "origin_id":string, "userinit":string, "ankunft":date, "abreise":date, "datum":date}, {"origin_id": ""})
    sum_tbl_data, Sum_tbl = create_model("Sum_tbl", {"mwst_code":int, "sum_date":string, "sum_roomnr":string, "sum_desc":string, "sum_amount":Decimal, "sum_id":string, "sum_amount_bef_tax":Decimal}, {"sum_date": "", "sum_roomnr": "", "sum_desc": "", "sum_id": ""})
    t_str3_data, T_str3 = create_model("T_str3", {"str3":string})
    bl_guest_data, bl_guest = create_model("bl_guest", {"zinr":string, "curr_guest":string})
    bline_vatlist_data, Bline_vatlist = create_model("Bline_vatlist", {"seqnr":int, "vatnr":int, "bezeich":string, "betrag":Decimal})

    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str1, str2, str3, t_str3_data, lvcarea, briefnr2, briefnr21, htl_name, htl_adr1, htl_adr2, htl_adr3, htl_tel, htl_fax, htl_email, bill_recv, bill_no, bl_descript, bl_descript0, bl_voucher, bl0_balance, bl0_balance1, bl_balance, bl_balance1, sum_anz, address1, address2, address3, email, hp_no, acc, adult, child1, child2, complgst, room_no, room_price, arrival, departure, bl_guest, l_guest, bl_instruct, resno, in_word, room_cat, city, country, zip, hp_guest, phone, sstr1, sstr2, sstr3, w_length, progname, temp_amt, wi_gastnr, ind_gastnr, ma_gst_amount, ma_gst_tot_sales_artikel, ma_gst_tot_non_taxable, ma_gst_tot_taxable, ma_gst_gtot_tax, curr_guest, tot_inclvat, net_amount, serv_code, acc_tax, vat_cam, do_it, membernumber, mgst, artnr_1001, guest_taxcode, nopd, tot_service_code, serv1, vat1, vat3, fact1, netto, selected_room, service_ns, vat_ns, amount_bef_tax_ns, vat2_ns, fact_ns, paidout, frate, rm_serv, rm_vat, service, vat, amount_bef_tax, vat2, fact, guest, htparam, paramtext, bill, mc_guest, res_line, artikel, bill_line, arrangement, waehrung, zimmer, queasy, exrate
        nonlocal pvilanguage, curr_status, briefnr, resnr, reslinnr, inv_type, rechnr, curr_program, gastnr, spbill_flag, user_init, lnldelimeter
        nonlocal guest1


        nonlocal bline_list, sum_tbl, t_str3, t_spbill_list, bl_guest, bline_vatlist, guest1
        nonlocal bline_list_data, sum_tbl_data, t_str3_data, bl_guest_data, bline_vatlist_data

        return {"str1": str1, "str2": str2, "str3": str3, "t-str3": t_str3_data}

    def calc_bl_balance1(datum:date, betrag:Decimal, fremdwbetrag:Decimal, fbetrag:Decimal):

        nonlocal str1, str2, str3, t_str3_data, lvcarea, briefnr2, briefnr21, htl_name, htl_adr1, htl_adr2, htl_adr3, htl_tel, htl_fax, htl_email, bill_recv, bill_no, bl_descript, bl_descript0, bl_voucher, bl0_balance, bl0_balance1, bl_balance, bl_balance1, sum_anz, address1, address2, address3, email, hp_no, acc, adult, child1, child2, complgst, room_no, room_price, arrival, departure, bl_guest, l_guest, bl_instruct, resno, in_word, room_cat, city, country, zip, hp_guest, phone, sstr1, sstr2, sstr3, w_length, progname, temp_amt, wi_gastnr, ind_gastnr, ma_gst_amount, ma_gst_tot_sales_artikel, ma_gst_tot_non_taxable, ma_gst_tot_taxable, ma_gst_gtot_tax, curr_guest, tot_inclvat, net_amount, serv_code, acc_tax, vat_cam, do_it, membernumber, mgst, artnr_1001, guest_taxcode, nopd, tot_service_code, serv1, vat1, vat3, fact1, netto, selected_room, service_ns, vat_ns, amount_bef_tax_ns, vat2_ns, fact_ns, paidout, frate, rm_serv, rm_vat, service, vat, amount_bef_tax, vat2, fact, guest, htparam, paramtext, bill, mc_guest, res_line, artikel, bill_line, arrangement, waehrung, zimmer, queasy, exrate
        nonlocal pvilanguage, curr_status, briefnr, resnr, reslinnr, inv_type, rechnr, curr_program, gastnr, spbill_flag, user_init, lnldelimeter
        nonlocal guest1


        nonlocal bline_list, sum_tbl, t_str3, t_spbill_list, bl_guest, bline_vatlist, guest1
        nonlocal bline_list_data, sum_tbl_data, t_str3_data, bl_guest_data, bline_vatlist_data

        billdate:date = None
        resline_exrate:Decimal = to_decimal("0.0")
        rline = None

        def generate_inner_output():
            return (fbetrag)

        Rline =  create_buffer("Rline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
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

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, rline.betriebsnr)]})

                    if waehrung:
                        resline_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                    else:
                        resline_exrate =  to_decimal(rline.reserve_dec)
                else:

                    exrate = get_cache (Exrate, {"datum": [(eq, rline.ankunft)],"artnr": [(eq, rline.betriebsnr)]})

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 415)]})
    briefnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 495)]})
    briefnr21 = htparam.finteger

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr1 = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 202)]})
    htl_adr2 = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
    htl_adr3 = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 205)]})
    htl_fax = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 206)]})
    htl_email = paramtext.ptexte

    bill = get_cache (Bill, {"rechnr": [(eq, rechnr)]})

    if curr_program.lower()  == ("ns-invoice").lower() :

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:

            mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastnr)]})

            if mc_guest:
                membernumber = mc_guest.cardnum
            bill_recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name + " " + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            city = trim(guest.wohnort)
            country = trim(guest.land)
            zip = trim(guest.plz)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
            phone = to_string(guest.telefon, "x(16)")
            guest_taxcode = to_string(guest.firmen_nr)

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr),(eq, bill.reslinnr)]})

        if res_line:

            guest1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

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

        if not spbill_flag:

            bill_line_obj_list = {}
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                    bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:
                            ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                        if artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:
                                    ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                                if artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

                    if artikel.service_code != 0:
                        serv1, vat1, vat3, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        netto =  to_decimal(bill_line.betrag) / to_decimal(fact1)
                        tot_service_code =  to_decimal(tot_service_code) + to_decimal((netto) * to_decimal(serv1) )

        else:

            bill_line_obj_list = {}
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True

                t_spbill_list = query(t_spbill_list_data, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:
                            ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                        if artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:
                                    ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                                if artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)


        if ma_gst_amount != 0:
            ma_gst_amount = ( to_decimal(ma_gst_amount) * to_decimal("6") / to_decimal(100)) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)
        else:

            if artnr_1001 != 0:
                ma_gst_amount =  to_decimal(artnr_1001)
                ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(artnr_1001) - to_decimal(ma_gst_tot_non_taxable) )


            ma_gst_gtot_tax =  to_decimal(artnr_1001) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 416)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 410)]})
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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

        if htparam.flogical:
            bline_vatlist_data = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_data, first=True)

            if bline_vatlist:
                do_it = True

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

        if bill_line:

            if bill_line.departement == 0:
                nopd = "01.00171.400"

            elif bill_line.departement == 11:
                nopd = "01.00171.403"
            else:
                nopd = "01.00171.401"
        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bill_recv == None:
                bill_recv = ""

            if bill_no == None:
                bill_no = ""

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if hp_no == None:
                hp_no = ""

            if room_no == None:
                room_no = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if user_init == None:
                user_init = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if htl_name == None:
                htl_name = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM")
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$city" + city + lnldelimeter + "$country" + country + lnldelimeter + "$zip" + zip + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$guest-taxcode" + guest_taxcode + lnldelimeter + "$nopd" + nopd + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99")
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("RoomNo", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if inv_type == 2:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

                if bill_line:
                    bl_voucher = ""
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:

                        if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                            if num_entries(bl_descript, "/") > 2:
                                bl_voucher = entry(2, bl_descript, "/")
                        else:
                            bl_voucher = entry(1, bl_descript, "/")

                    res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if guest:
                            curr_guest = guest.name


                    else:
                        curr_guest = " "


                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                if do_it:

                    bline_vatlist = query(bline_vatlist_data, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_data, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
            else:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

                if bill_line:
                    bl_voucher = ""
                    bl_descript = bill_line.bezeich
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:

                        if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                            if num_entries(bl_descript, "/") > 2:
                                bl_voucher = entry(2, bl_descript, "/")
                        else:
                            bl_voucher = entry(1, bl_descript, "/")

                    res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if guest:
                            curr_guest = guest.name


                    else:
                        curr_guest = " "


                    fact_ns =  to_decimal("1")

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                    if artikel.mwst_code != 0 or artikel.service_code != 0 or artikel.prov_code != 0:
                        service_ns, vat_ns, vat2_ns, fact_ns = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                    vat_ns =  to_decimal(vat_ns) + to_decimal(vat2_ns)


                    amount_bef_tax_ns =  to_decimal(bill_line.betrag)
                    amount_bef_tax_ns =  to_decimal(amount_bef_tax_ns) / to_decimal(fact_ns)
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(amount_bef_tax_ns, "->>>,>>>,>>>,>>>,>>9.99")

                if do_it:

                    bline_vatlist = query(bline_vatlist_data, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_data, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bill_recv == None:
                bill_recv = ""

            if bill_no == None:
                bill_no = ""

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if hp_no == None:
                hp_no = ""

            if room_no == None:
                room_no = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if user_init == None:
                user_init = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if htl_name == None:
                htl_name = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM")
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$city" + city + lnldelimeter + "$country" + country + lnldelimeter + "$zip" + zip + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$guest-taxcode" + guest_taxcode + lnldelimeter + "$nopd" + nopd + lnldelimeter + "$service-code" + to_string(tot_service_code, "->>>,>>>,>>>,>>>,>>9.99")
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("RoomNo", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if not spbill_flag:

                if inv_type == 2:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        sum_tbl = query(sum_tbl_data, filters=(lambda sum_tbl: sum_tbl.mwst_code == artikel.mwst_code), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_data.append(sum_tbl)

                            sum_tbl.mwst_code = artikel.mwst_code
                            sum_tbl.sum_desc = bl_descript
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_data):
                        sum_anz =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == rechnr) & (Bill_line.artnr == sum_tbl.mwst_code)).order_by(Bill_line._recid).all():
                            sum_anz =  to_decimal(sum_anz) + to_decimal(bill_line.anzahl)
                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + bl_descript + lnldelimeter + to_string(sum_anz, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest

                elif inv_type == 3:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        sum_tbl = query(sum_tbl_data, filters=(lambda sum_tbl: sum_tbl.sum_desc == bill_line.bezeich), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_data.append(sum_tbl)

                            sum_tbl.sum_date = to_string(bill_line.bill_datum)
                            sum_tbl.sum_desc = bill_line.bezeich
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        sum_tbl = query(sum_tbl_data, filters=(lambda sum_tbl: sum_tbl.sum_desc == bill_line.bezeich), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_data.append(sum_tbl)

                            sum_tbl.sum_desc = bill_line.bezeich
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_data):
                        sum_anz =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == rechnr) & (Bill_line.bezeich == sum_tbl.sum_desc)).order_by(Bill_line._recid).all():
                            sum_anz =  to_decimal(sum_anz) + to_decimal(bill_line.anzahl)
                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = sum_tbl.sum_date + lnldelimeter + bl_descript + lnldelimeter + to_string(sum_anz, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3


                else:

                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        fact_ns =  to_decimal("1")

                        artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                        if artikel.mwst_code != 0 or artikel.service_code != 0 or artikel.prov_code != 0:
                            service_ns, vat_ns, vat2_ns, fact_ns = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                        vat_ns =  to_decimal(vat_ns) + to_decimal(vat2_ns)


                        amount_bef_tax_ns =  to_decimal(bill_line.betrag)
                        amount_bef_tax_ns =  to_decimal(amount_bef_tax_ns) / to_decimal(fact_ns)
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(amount_bef_tax_ns, "->>>,>>>,>>>,>>>,>>9.99")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3


            else:

                if inv_type == 2:

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True


                        bl_descript0 = entry(0, bl_descript, "/")
                        bl_voucher = ""

                        if num_entries(bl_descript, "/") > 1:

                            if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3

                elif inv_type == 3:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit, Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                        str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.bezeich + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3


                else:

                    bill_line_obj_list = {}
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        t_spbill_list = query(t_spbill_list_data, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:

                            if matches(bl_descript,r"*c/i*") or matches(bl_descript,r"*c/o*"):

                                if num_entries(bl_descript, "/") > 2:
                                    bl_voucher = entry(2, bl_descript, "/")
                            else:
                                bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)],"zinr": [(eq, bill_line.zinr)]})

                        if res_line:

                            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                            if guest:
                                curr_guest = guest.name


                        else:
                            curr_guest = " "


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + bill_line.zinr + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + curr_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bill_line.epreis, "->>>,>>>,>>>,>>>,>>9.99")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = str3

    elif curr_program.lower()  == ("fo-invoice").lower() :

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if not res_line:

            return generate_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 242)]})
        paidout = htparam.finteger
        bline_list_data.clear()

        if not spbill_flag:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})
                bline_list = Bline_list()
                bline_list_data.append(bline_list)

                buffer_copy(bill_line, bline_list)
                bline_list.bl_recid = bill_line._recid
                bline_list.dept = bill_line.departement
                bline_list.datum = bill_line.bill_datum
                bline_list.fsaldo =  to_decimal("0")
                bline_list.saldo =  to_decimal(bill_line.betrag)
                bline_list.epreis =  to_decimal(bill_line.epreis)


                bline_list.fsaldo = calc_bl_balance1(bill_line.bill_datum, bill_line.betrag, bill_line.fremdwbetrag, bline_list.fsaldo)

        else:

            bill_line_obj_list = {}
            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True

                t_spbill_list = query(t_spbill_list_data, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})
                bline_list = Bline_list()
                bline_list_data.append(bline_list)

                buffer_copy(bill_line, bline_list)
                bline_list.bl_recid = bill_line._recid
                bline_list.dept = bill_line.departement
                bline_list.datum = bill_line.bill_datum
                bline_list.fsaldo =  to_decimal("0")
                bline_list.saldo =  to_decimal(bill_line.betrag)
                bline_list.epreis =  to_decimal(bill_line.epreis)


                bline_list.fsaldo = calc_bl_balance1(bill_line.bill_datum, bill_line.betrag, bill_line.fremdwbetrag, bline_list.fsaldo)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
        rm_serv = htparam.flogical

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.artnr_logis)],"departement": [(eq, 0)]})

        if res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        service =  to_decimal("0")
        vat =  to_decimal("0")

        if rm_serv:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal) / to_decimal("100")

        if rm_vat:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

            htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

            if htparam.flogical:
                vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        if guest:
            bill_recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name + " " + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            email = trim(guest.email_adr)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
            phone = to_string(guest.telefon, "x(16)")


            htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
            wi_gastnr = htparam.finteger

            htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
            ind_gastnr = htparam.finteger

            if guest.karteityp == 0 or guest.gastnr == wi_gastnr or guest.gastnr == ind_gastnr:
                room_price = to_string(res_line.zipreis, ">>>,>>>,>>9.99")

            elif res_line.gastnrmember == res_line.gastnrpay:
                room_price = to_string(res_line.zipreis, ">>>,>>>,>>9.99")

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr),(eq, bill.reslinnr)]})

        if res_line:

            guest1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest1:
                hp_guest = to_string(guest1.mobil_telefon, "x(16)")


        ma_gst_amount =  to_decimal("0")
        ma_gst_tot_sales_artikel =  to_decimal("0")
        ma_gst_tot_non_taxable =  to_decimal("0")
        ma_gst_tot_taxable =  to_decimal("0")
        mgst =  to_decimal("0")

        bill_line_obj_list = {}
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                 (Bill_line._recid.in_(list(set([bline_list.bl_recid for bline_list in bline_list_data]))))).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True


            bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
            bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
            bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

            if (artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9):
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

            elif artikel.artart == 6 and artikel.zwkum == paidout:
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                if bill_line.bill_datum <= 08/31/18:

                    if artikel.mwst_code != 0:
                        ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                    if artikel.mwst_code == 0:
                        ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                else:

                    if artikel.artnr == 1001 or artikel.artnr == 1002:

                        if bill_line.betrag > 0:
                            artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                        mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr != 1001:

                            if artikel.mwst_code != 0:
                                ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                            if artikel.mwst_code == 0:
                                ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

        if ma_gst_amount != 0:
            ma_gst_amount = ( to_decimal(ma_gst_amount) * to_decimal("6") / to_decimal(100)) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)
        else:

            if artnr_1001 != 0:
                ma_gst_amount =  to_decimal(artnr_1001)
                ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(artnr_1001) - to_decimal(ma_gst_tot_non_taxable) )


            ma_gst_gtot_tax =  to_decimal(artnr_1001) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 416)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 410)]})
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

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

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

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:
                bl_guest = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

                if mc_guest:
                    membernumber = mc_guest.cardnum

            if res_line.code != "":

                queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

                if queasy:
                    bl_instruct = trim(queasy.char1)
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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

        if htparam.flogical:
            bline_vatlist_data = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_data, first=True)

            if bline_vatlist:
                do_it = True

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

        if bill_line.departement == 0:
            nopd = "01.00171.400"

        elif bill_line.departement == 11:
            nopd = "01.00171.403"
        else:
            nopd = "01.00171.401"
        str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$email" + email + lnldelimeter + "$hp-no" + hp_no + lnldelimeter + "$acc" + acc + lnldelimeter + "$adult" + adult + lnldelimeter + "$child1" + child1 + lnldelimeter + "$child2" + child2 + lnldelimeter + "$complgst" + complgst + lnldelimeter + "$room-no" + room_no + lnldelimeter + "$room-price" + room_price + lnldelimeter + "$arrival" + arrival + lnldelimeter + "$arrival0" + arrival + lnldelimeter + "$departure" + departure + lnldelimeter + "$departure0" + departure + lnldelimeter + "$bl-guest" + trim(bl_guest) + lnldelimeter + "$bl-instruct" + bl_instruct + lnldelimeter + "$resno" + resno + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter + "$room-cat" + room_cat + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$nopd" + nopd
        str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("Description/Voucher", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("RmNo", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("ID", lvcarea, "") + lnldelimeter + translateExtended ("Guest Name", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("Amount Before Tax", lvcarea, "") + lnldelimeter + translateExtended ("Foreign Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("In Word", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")
        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            bline_list = query(bline_list_data, first=True)

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
            str3 = to_string(bline_list.datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bline_list.anzahl, "->>>") + lnldelimeter + bline_list.zinr + lnldelimeter + to_string(bline_list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bline_list.userinit + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(amount_bef_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bline_list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99")
            t_str3 = T_str3()
            t_str3_data.append(t_str3)

            t_str3.str3 = str3

            if do_it:

                bline_vatlist = query(bline_vatlist_data, first=True)

                if bline_vatlist:
                    str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                    t_str3 = query(t_str3_data, first=True)

                    if t_str3:
                        t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            for bline_list in query(bline_list_data):
                bl_voucher = ""
                bl_descript = bline_list.bezeich
                bl_descript0 = entry(0, bl_descript, "/")

                if num_entries(bl_descript, "/") > 1:
                    bl_voucher = entry(1, bl_descript, "/")
                fact =  to_decimal("1")

                bill_line = get_cache (Bill_line, {"_recid": [(eq, bline_list.bl_recid)]})

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if artikel.mwst_code != 0 or artikel.service_code != 0 or artikel.prov_code != 0:
                    service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_line.bill_datum))
                vat =  to_decimal(vat) + to_decimal(vat2)


                amount_bef_tax =  to_decimal(bline_list.saldo)
                amount_bef_tax =  to_decimal(amount_bef_tax) / to_decimal(fact)
                bl_balance =  to_decimal(bl_balance) + to_decimal(bline_list.saldo)
                str3 = to_string(bline_list.datum) + lnldelimeter + bl_descript + lnldelimeter + to_string(bline_list.anzahl, "->>>") + lnldelimeter + bline_list.zinr + lnldelimeter + to_string(bline_list.saldo, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bline_list.userinit + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(amount_bef_tax, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bline_list.epreis, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + in_word + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")
                t_str3 = T_str3()
                t_str3_data.append(t_str3)

                t_str3.str3 = str3

            if do_it:

                for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                    str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                    t_str3 = T_str3()
                    t_str3_data.append(t_str3)

                    t_str3.str3 = str3

    elif curr_program.lower()  == ("master-inv").lower() :

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:

            mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if mc_guest:
                membernumber = mc_guest.cardnum
            bill_recv = guest.anrede1 + " . " + guest.vorname1 + " , " + guest.name + " " + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
            phone = to_string(guest.telefon, "x(16)")
            guest_taxcode = to_string(guest.firmen_nr)

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)]})

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

            guest1 = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest1:
                hp_guest = to_string(guest.mobil_telefon, "x(16)")

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 13)).order_by(Res_line.name, Res_line.zinr).all():

                if res_line.name != " ":
                    bl_guest = bl_guest + res_line.name + " # " + res_line.zinr + chr_unicode(10)

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")
        ma_gst_amount =  to_decimal("0")
        ma_gst_tot_sales_artikel =  to_decimal("0")
        ma_gst_tot_non_taxable =  to_decimal("0")
        ma_gst_tot_taxable =  to_decimal("0")

        if not spbill_flag:

            bill_line_obj_list = {}
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                    bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                elif artikel.artart == 6 and artikel.zwkum == paidout:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:
                            ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                        if artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:
                                    ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                                if artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)

        else:

            bill_line_obj_list = {}
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                     (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.bill_datum, Bill_line.zeit).all():
                if bill_line_obj_list.get(bill_line._recid):
                    continue
                else:
                    bill_line_obj_list[bill_line._recid] = True

                t_spbill_list = query(t_spbill_list_data, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)
                bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
                bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

                if (artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9):
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

                elif artikel.artart == 6 and artikel.zwkum == paidout:
                    bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

                if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                    ma_gst_tot_sales_artikel =  to_decimal(ma_gst_tot_sales_artikel) + to_decimal(bill_line.betrag)

                    if bill_line.bill_datum <= 08/31/18:

                        if artikel.mwst_code != 0:
                            ma_gst_tot_taxable =  to_decimal(ma_gst_tot_taxable) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                        if artikel.mwst_code == 0:
                            ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)
                    else:

                        if artikel.artnr == 1001 or artikel.artnr == 1002:

                            if bill_line.betrag > 0:
                                artnr_1001 =  to_decimal(artnr_1001) + to_decimal(bill_line.betrag)


                            mgst =  to_decimal(mgst) + to_decimal(bill_line.betrag)
                        else:

                            if artikel.artnr != 1001:

                                if artikel.mwst_code != 0:
                                    ma_gst_amount =  to_decimal(ma_gst_amount) + to_decimal((bill_line.betrag) / to_decimal(1.06))

                                if artikel.mwst_code == 0:
                                    ma_gst_tot_non_taxable =  to_decimal(ma_gst_tot_non_taxable) + to_decimal(bill_line.betrag)


        if ma_gst_amount != 0:
            ma_gst_amount = ( to_decimal(ma_gst_amount) * to_decimal("6") / to_decimal(100)) + to_decimal(mgst)


            ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(ma_gst_amount) - to_decimal(ma_gst_tot_non_taxable))
            ma_gst_gtot_tax =  to_decimal(ma_gst_amount) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)
        else:

            if artnr_1001 != 0:
                ma_gst_amount =  to_decimal(artnr_1001)
                ma_gst_tot_taxable = ( to_decimal(ma_gst_tot_sales_artikel) - to_decimal(artnr_1001) - to_decimal(ma_gst_tot_non_taxable) )


            ma_gst_gtot_tax =  to_decimal(artnr_1001) + to_decimal(ma_gst_tot_taxable) + to_decimal(ma_gst_tot_non_taxable)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 416)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 410)]})
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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

        if htparam.flogical:
            bline_vatlist_data = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_data, first=True)

            if bline_vatlist:
                do_it = True

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

        if bill_line:

            if bill_line.departement == 0:
                nopd = "01.00171.400"

            elif bill_line.departement == 11:
                nopd = "01.00171.403"
            else:
                nopd = "01.00171.401"
        bl_balance =  to_decimal("0")

        if curr_status.lower()  == ("design").lower() :

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bill_recv == None:
                bill_recv = ""

            if bill_no == None:
                bill_no = ""

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if hp_no == None:
                hp_no = ""

            if room_no == None:
                room_no = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if user_init == None:
                user_init = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if htl_name == None:
                htl_name = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$hp-no" + hp_no + lnldelimeter + "$room-no" + room_no + lnldelimeter + "$arrival" + arrival + lnldelimeter + "$arrival0" + arrival + lnldelimeter + "$departure" + departure + lnldelimeter + "$departure0" + departure + lnldelimeter + "$bl-guest" + bl_guest + lnldelimeter + "$resno" + resno + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$memberno" + membernumber + lnldelimeter + "$guest-taxcode" + guest_taxcode + lnldelimeter + "$nopd" + nopd
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99")
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("RmNo", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("ID", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if inv_type == 2:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

                if bill_line:

                    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, bill_line.zinr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

                    if res_line:
                        l_guest = res_line.name


                    bl_voucher = ""
                    bl_descript0 = entry(0, bl_descript, "/")

                    if num_entries(bl_descript, "/") > 1:
                        bl_voucher = entry(1, bl_descript, "/")
                    bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                    str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bill_line.bezeich + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest

                if do_it:

                    bline_vatlist = query(bline_vatlist_data, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_data, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
            else:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

                if bill_line:

                    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, bill_line.zinr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

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

                    bline_vatlist = query(bline_vatlist_data, first=True)

                    if bline_vatlist:
                        str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                        t_str3 = query(t_str3_data, first=True)

                        if t_str3:
                            t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if bill_recv == None:
                bill_recv = ""

            if bill_no == None:
                bill_no = ""

            if address1 == None:
                address1 = ""

            if address2 == None:
                address2 = ""

            if address3 == None:
                address3 = ""

            if hp_no == None:
                hp_no = ""

            if room_no == None:
                room_no = ""

            if arrival == None:
                arrival = ""

            if departure == None:
                departure = ""

            if bl_guest == None:
                bl_guest = ""

            if resno == None:
                resno = ""

            if user_init == None:
                user_init = ""

            if hp_guest == None:
                hp_guest = ""

            if phone == None:
                phone = ""

            if membernumber == None:
                membernumber = ""

            if htl_name == None:
                htl_name = ""

            if htl_adr1 == None:
                htl_adr1 = ""

            if htl_adr2 == None:
                htl_adr2 = ""

            if htl_adr3 == None:
                htl_adr3 = ""

            if htl_tel == None:
                htl_tel = ""

            if htl_fax == None:
                htl_fax = ""

            if htl_email == None:
                htl_email = ""
            str1 = "$bill-recv" + bill_recv + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$address3" + address3 + lnldelimeter + "$hp-no" + hp_no + lnldelimeter + "$room-no" + room_no + lnldelimeter + "$arrival" + arrival + lnldelimeter + "$arrival0" + arrival + lnldelimeter + "$departure" + departure + lnldelimeter + "$departure0" + departure + lnldelimeter + "$bl-guest" + bl_guest + lnldelimeter + "$resno" + resno + lnldelimeter + "$bl-id" + user_init + lnldelimeter + "$Date" + to_string(get_current_date(), "99/99/9999") + lnldelimeter + "$bl-time" + to_string(get_current_time_in_seconds(), "HH:MM") + lnldelimeter + "$hp-guest" + hp_guest + lnldelimeter + "$phone" + phone + lnldelimeter + "$guest-taxcode" + guest_taxcode + lnldelimeter + "$nopd" + nopd
            str1 = str1 + lnldelimeter + "$htl-name" + htl_name + lnldelimeter + "$htl-adr1" + htl_adr1 + lnldelimeter + "$htl-adr2" + htl_adr2 + lnldelimeter + "$htl-adr3" + htl_adr3 + lnldelimeter + "$htl-tel" + htl_tel + lnldelimeter + "$htl-fax" + htl_fax + lnldelimeter + "$htl-email" + htl_email + lnldelimeter + "$gst-amount" + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$tot-taxable" + to_string(ma_gst_tot_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$non-taxable" + to_string(ma_gst_tot_non_taxable, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "$grand-total" + to_string(ma_gst_gtot_tax, "->>>,>>>,>>>,>>>,>>9.99")
            str2 = translateExtended ("Date", lvcarea, "") + lnldelimeter + translateExtended ("RmNo", lvcarea, "") + lnldelimeter + translateExtended ("Description", lvcarea, "") + lnldelimeter + translateExtended ("Qty", lvcarea, "") + lnldelimeter + translateExtended ("Amount", lvcarea, "") + lnldelimeter + translateExtended ("Balance", lvcarea, "") + lnldelimeter + translateExtended ("ID", lvcarea, "") + lnldelimeter + translateExtended ("Voucher", lvcarea, "") + lnldelimeter + translateExtended ("GST 6%", lvcarea, "")

            if not spbill_flag:

                if inv_type == 2:

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & ((Artikel.artart == 0) | (Artikel.artart == 1) | (Artikel.artart == 8) | (Artikel.artart == 9))).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        sum_tbl = query(sum_tbl_data, filters=(lambda sum_tbl: sum_tbl.mwst_code == artikel.mwst_code), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_data.append(sum_tbl)

                            sum_tbl.mwst_code = artikel.mwst_code
                            sum_tbl.sum_desc = bl_descript
                            sum_tbl.sum_amount =  to_decimal(bill_line.betrag)


                            pass
                        else:
                            temp_amt =  to_decimal(sum_tbl.sum_amount)
                            temp_amt =  to_decimal(temp_amt) + to_decimal(bill_line.betrag)
                            sum_tbl.sum_amount =  to_decimal(temp_amt)


                            pass

                    for sum_tbl in query(sum_tbl_data):
                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + "" + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "" + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3

                elif inv_type == 4:
                    temp_amt =  to_decimal("0")

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        sum_tbl = query(sum_tbl_data, filters=(lambda sum_tbl: sum_tbl.sum_desc == bill_line.bezeich and sum_tbl.sum_roomnr == bill_line.zinr), first=True)

                        if not sum_tbl:
                            sum_tbl = Sum_tbl()
                            sum_tbl_data.append(sum_tbl)

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

                    for sum_tbl in query(sum_tbl_data):
                        sum_anz =  to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                 (Bill_line.rechnr == rechnr) & (Bill_line.bezeich == sum_tbl.sum_desc)).order_by(Bill_line._recid).all():
                            sum_anz =  to_decimal(sum_anz) + to_decimal(bill_line.anzahl)

                        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, sum_tbl.sum_roomnr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

                        if res_line:
                            l_guest = res_line.name


                        bl_voucher = ""
                        bl_descript = sum_tbl.sum_desc
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(sum_tbl.sum_amount)
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = to_string(sum_tbl.sum_date) + lnldelimeter + sum_tbl.sum_roomnr + lnldelimeter + bl_descript + lnldelimeter + to_string(sum_anz, "->>>") + lnldelimeter + to_string(sum_tbl.sum_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + sum_tbl.sum_id + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3


                else:

                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, bill_line.zinr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

                        if res_line:
                            l_guest = res_line.name

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = str3


            else:

                if inv_type == 2:

                    bill_line_obj_list = {}
                    for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True


                        bl_voucher = ""
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, bill_line.zinr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

                        if res_line:
                            l_guest = res_line.name


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = "" + lnldelimeter + "" + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + "" + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")

                    if do_it:

                        for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                            str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                            t_str3 = T_str3()
                            t_str3_data.append(t_str3)

                            t_str3.str3 = str3

                elif inv_type == 4:

                    bill_line_obj_list = {}
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit, Bill_line.zinr, Bill_line.bezeich, Bill_line.bill_datum.desc()).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        t_spbill_list = query(t_spbill_list_data, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, bill_line.zinr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

                        if res_line:
                            l_guest = res_line.name


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = str3


                else:

                    bill_line_obj_list = {}
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line._recid.in_(list(set([t_spbill_list.bl_recid for t_spbill_list in t_spbill_list_data if t_spbill_list.selected ])))) & (Bill_line.rechnr == rechnr)).order_by(Bill_line.sysdate, Bill_line.zeit).all():
                        if bill_line_obj_list.get(bill_line._recid):
                            continue
                        else:
                            bill_line_obj_list[bill_line._recid] = True

                        t_spbill_list = query(t_spbill_list_data, (lambda t_spbill_list: (bill_line._recid == t_spbill_list.bl_recid)), first=True)
                        bl_voucher = ""
                        bl_descript = bill_line.bezeich
                        bl_descript0 = entry(0, bl_descript, "/")

                        if num_entries(bl_descript, "/") > 1:
                            bl_voucher = entry(1, bl_descript, "/")
                        bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)

                        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, bill_line.zinr)],"resstatus": [(ne, 12),(ne, 9),(ne, 10),(ne, 13)]})

                        if res_line:
                            l_guest = res_line.name


                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = to_string(bill_line.bill_datum) + lnldelimeter + bill_line.zinr + lnldelimeter + bl_descript + lnldelimeter + to_string(bill_line.anzahl, "->>>") + lnldelimeter + to_string(bill_line.betrag, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(bl_balance, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + bill_line.userinit + lnldelimeter + in_word + lnldelimeter + bl_guest + lnldelimeter + bl_descript0 + lnldelimeter + bl_voucher + lnldelimeter + to_string(ma_gst_amount, "->>>,>>>,>>>,>>>,>>9.99") + lnldelimeter + l_guest + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ")


                if do_it:

                    for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                        str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                        t_str3 = T_str3()
                        t_str3_data.append(t_str3)

                        t_str3.str3 = str3

    if curr_program.lower()  == ("master-inv-room").lower() :

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:
            bill_recv = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name + " " + guest.anredefirma
            address1 = trim(guest.adresse1)
            address2 = trim(guest.adresse2)
            address3 = trim(guest.adresse3)
            city = trim(guest.wohnort)
            country = trim(guest.land)
            zip = trim(guest.plz)
            hp_no = to_string(guest.mobil_telefon, "x(16)")
        bline_list_data.clear()

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == rechnr) & (Bill_line.zinr == (selected_room).lower())).order_by(Bill_line._recid).all():
            bline_list = Bline_list()
            bline_list_data.append(bline_list)

            buffer_copy(bill_line, bline_list)
            bline_list.bl_recid = bill_line._recid
            bline_list.dept = bill_line.departement
            bline_list.datum = bill_line.bill_datum
            bline_list.fsaldo =  to_decimal("0")
            bline_list.saldo =  to_decimal(bill_line.betrag)
            bline_list.epreis =  to_decimal(bill_line.epreis)


            bline_list.fsaldo = calc_bl_balance1(bill_line.bill_datum, bill_line.betrag, bill_line.fremdwbetrag, bline_list.fsaldo)

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"resstatus": [(ne, 12)],"zinr": [(eq, selected_room)]})

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

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:
                bl_guest = guest.anrede1 + ". " + guest.vorname1 + ", " + guest.name
            acc = to_string(res_line.erwachs + res_line.kind1 + res_line.kind2 + res_line.gratis)
            adult = to_string(res_line.erwachs)
            child1 = to_string(res_line.kind1)
            child2 = to_string(res_line.kind2)
            complgst = to_string(res_line.gratis)
            resno = to_string(resnr)

        zimmer = get_cache (Zimmer, {"zinr": [(eq, selected_room)]})

        if zimmer:
            room_cat = zimmer.bezeich

        if bill.flag == 0:
            bill_no = to_string(bill.rechnr) + " / " + to_string(bill.printnr)

        elif bill.flag == 1:
            bill_no = to_string(bill.rechnr) + translateExtended ("(DUPLICATE)", lvcarea, "")

        bill_line_obj_list = {}
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                 (Bill_line._recid.in_(list(set([bline_list.bl_recid for bline_list in bline_list_data]))))).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True


            bl_balance =  to_decimal(bl_balance) + to_decimal(bill_line.betrag)
            bl0_balance1 =  to_decimal(bl0_balance1) + to_decimal(bill_line.fremdwbetrag)
            bl_balance1 =  to_decimal(bl_balance1) + to_decimal(bill_line.fremdwbetrag)

            if (artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9):
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

            elif artikel.artart == 6 and artikel.zwkum == paidout:
                bl0_balance =  to_decimal(bl0_balance) + to_decimal(bill_line.betrag)

        if briefnr == briefnr2 or briefnr == briefnr21:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 416)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 410)]})
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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

        if htparam.flogical:
            bline_vatlist_data = get_output(fobill_vatlistbl(pvilanguage, rechnr))

            bline_vatlist = query(bline_vatlist_data, first=True)

            if bline_vatlist:
                do_it = True

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechnr)]})

        if bill_line:

            if bill_line.departement == 0:
                nopd = "01.00171.400"

            elif bill_line.departement == 11:
                nopd = "01.00171.403"
            else:
                nopd = "01.00171.401"
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

            bline_list = query(bline_list_data, first=True)

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
            t_str3_data.append(t_str3)

            t_str3.str3 = str3

            if do_it:

                bline_vatlist = query(bline_vatlist_data, first=True)

                if bline_vatlist:
                    str3 = str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

                    t_str3 = query(t_str3_data, first=True)

                    if t_str3:
                        t_str3.str3 = t_str3.str3 + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")

        elif curr_status.lower()  == ("print").lower() :

            for bline_list in query(bline_list_data):

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
                t_str3_data.append(t_str3)

                t_str3.str3 = str3

            if do_it:

                for bline_vatlist in query(bline_vatlist_data, filters=(lambda bline_vatlist: bline_vatlist.vatnr != 0), sort_by=[("seqnr",False),("vatnr",False)]):
                    str3 = to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + " " + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + to_string(" ") + lnldelimeter + " " + lnldelimeter + to_string(bline_vatlist.bezeich, "x(25)") + lnldelimeter + to_string(bline_vatlist.betrag, "->>>,>>>,>>9.99")
                    t_str3 = T_str3()
                    t_str3_data.append(t_str3)

                    t_str3.str3 = str3

    return generate_output()