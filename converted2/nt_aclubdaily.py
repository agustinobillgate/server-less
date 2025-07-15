from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Res_line, Mc_guest, Mc_types, Guest, Arrangement, Bill_line, Genstat, Waehrung, Artikel, Bill, H_artikel, H_bill_line, Mc_aclub, H_journal, H_bill

def nt_aclubdaily():
    bill_date:date = None
    curr_date:date = None
    from_date:date = None
    to_date:date = None
    price_decimal:int = 0
    foreign_rate:bool = False
    rm_vat:bool = False
    rm_serv:bool = False
    serv_taxable:bool = False
    dec_netroom_rate:decimal = to_decimal("0.0")
    dec_room_rate:decimal = to_decimal("0.0")
    netroom_rev:decimal = to_decimal("0.0")
    dec_room_rev:decimal = to_decimal("0.0")
    dec_netroom_rev:decimal = to_decimal("0.0")
    dec_netfb_rev:decimal = to_decimal("0.0")
    dec_fb_rev:decimal = to_decimal("0.0")
    dec_netother_rev:decimal = to_decimal("0.0")
    dec_other_rev:decimal = to_decimal("0.0")
    dec_nettotal_rev:decimal = to_decimal("0.0")
    dec_total_rev:decimal = to_decimal("0.0")
    do_it:bool = False
    post_dayuse:bool = False
    frate:decimal = to_decimal("0.0")
    rate:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    service_vat:decimal = to_decimal("0.0")
    lodg_betrag:decimal = to_decimal("0.0")
    str_type:str = ""
    str_guest:str = ""
    bill_no:int = 0
    qty_night:int = 0
    ct:str = ""
    contcode:str = ""
    str_rate:str = ""
    htparam = res_line = mc_guest = mc_types = guest = arrangement = bill_line = genstat = waehrung = artikel = bill = h_artikel = h_bill_line = mc_aclub = h_journal = h_bill = None

    room_trans = s_list = vat_serv = None

    room_trans_list, Room_trans = create_model("Room_trans", {"art_desc":str, "bill_no":int, "dept_nr":int, "amt":decimal})
    s_list_list, S_list = create_model("S_list", {"rechnr":int, "departement":int, "resnr":int, "reslinnr":int})
    vat_serv_list, Vat_serv = create_model("Vat_serv", {"artnr":int, "departement":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, curr_date, from_date, to_date, price_decimal, foreign_rate, rm_vat, rm_serv, serv_taxable, dec_netroom_rate, dec_room_rate, netroom_rev, dec_room_rev, dec_netroom_rev, dec_netfb_rev, dec_fb_rev, dec_netother_rev, dec_other_rev, dec_nettotal_rev, dec_total_rev, do_it, post_dayuse, frate, rate, service, vat, vat2, service_vat, lodg_betrag, str_type, str_guest, bill_no, qty_night, ct, contcode, str_rate, htparam, res_line, mc_guest, mc_types, guest, arrangement, bill_line, genstat, waehrung, artikel, bill, h_artikel, h_bill_line, mc_aclub, h_journal, h_bill


        nonlocal room_trans, s_list, vat_serv
        nonlocal room_trans_list, s_list_list, vat_serv_list

        return {}

    def create_temp_hbill(from_date:date, to_date:date):

        nonlocal bill_date, curr_date, price_decimal, foreign_rate, rm_vat, rm_serv, serv_taxable, dec_netroom_rate, dec_room_rate, netroom_rev, dec_room_rev, dec_netroom_rev, dec_netfb_rev, dec_fb_rev, dec_netother_rev, dec_other_rev, dec_nettotal_rev, dec_total_rev, do_it, post_dayuse, frate, rate, service, vat, vat2, service_vat, lodg_betrag, str_type, str_guest, bill_no, qty_night, ct, contcode, str_rate, htparam, res_line, mc_guest, mc_types, guest, arrangement, bill_line, genstat, waehrung, artikel, bill, h_artikel, h_bill_line, mc_aclub, h_journal, h_bill


        nonlocal room_trans, s_list, vat_serv
        nonlocal room_trans_list, s_list_list, vat_serv_list


        s_list_list.clear()

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.artnr != 0)).order_by(H_journal._recid).all():

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.rechnr == h_journal.rechnr) & (H_bill.departement == h_journal.departement)).first()

            if h_bill and h_bill.resnr == res_line.resnr and h_bill.reslinnr == res_line.reslinnr:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.resnr == h_bill.resnr and s_list.reslinnr == h_bill.reslinnr and s_list.rechnr == h_bill.rechnr and s_list.departement == h_bill.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    buffer_copy(h_bill, s_list)


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 127)).first()
    rm_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    rm_serv = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    for res_line in db_session.query(Res_line).filter(
             ((Res_line.active_flag == 2) & (Res_line.abreise == bill_date) & (Res_line.resstatus == 8)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.zinr).all():
        dec_netroom_rate =  to_decimal("0")
        do_it = True
        post_dayuse = False

        if do_it:

            mc_guest = db_session.query(Mc_guest).filter(
                     (Mc_guest.gastnr == res_line.gastnrmember) & (Mc_guest.activeflag)).first()

            if not mc_guest:
                do_it = False
            else:

                for mc_guest in db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == res_line.gastnrmember) & (Mc_guest.activeflag)).order_by(Mc_guest._recid).all():
                    do_it = False

                    mc_types = db_session.query(Mc_types).filter(
                             (Mc_types.nr == mc_guest.nr)).first()

                    if mc_types:
                        do_it = True

                    if do_it:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == res_line.gastnrmember)).first()
                        str_type = mc_type.bezeich
                        str_guest = guest.name + ", " + guest.vorname1 + " " + guest.anrede1


                        break

        if do_it:

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == res_line.arrangement)).first()

            bill_line = db_session.query(Bill_line).filter(
                     (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == bill_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
            post_dayuse = None != bill_line

        if not post_dayuse:
            qty_night = res_line.abreise - res_line.ankunft
            from_date = res_line.ankunft
            to_date = res_line.abreise - timedelta(days=1)


        else:
            qty_night = res_line.abreise - res_line.ankunft + 1
            from_date = res_line.ankunft
            to_date = res_line.abreise


        create_temp_hbill(res_line.ankunft, res_line.abreise)
        for curr_date in date_range(from_date,to_date) :
            rate =  to_decimal("0")

            if curr_date < bill_date:

                genstat = db_session.query(Genstat).filter(
                         (Genstat.datum == curr_date) & (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr)).first()

                if genstat:
                    rate =  to_decimal(genstat.rateLocal)

                elif res_line.zipreis != 0:

                    if res_line.reserve_dec != 0:
                        frate =  to_decimal(res_line.reserve_dec)
                    else:

                        waehrung = db_session.query(Waehrung).filter(
                                 (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                        if waehrung:
                            frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                    rate =  to_decimal(res_line.zipreis) * to_decimal(frate)
            else:

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                    if waehrung:
                        frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                rate =  to_decimal(res_line.zipreis) * to_decimal(frate)

            if rm_serv:

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()
                service, vat, vat2, service_vat = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
                rate =  to_decimal(rate) / to_decimal(service_vat)

            if dec_netroom_rate < rate:
                dec_netroom_rate =  to_decimal(rate)
            dec_netroom_rev =  to_decimal(dec_netroom_rev) + to_decimal(rate)

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr)).order_by(Bill._recid).all():

            if bill.reslinnr == res_line.reslinnr:
                bill_no = bill.rechnr

            bill_line_obj_list = []
            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (((Artikel.artart == 0)) | ((Artikel.artart == 8)) | ((Artikel.artart == 9) & (Artikel.artgrp > 0)))).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                if bill_line._recid in bill_line_obj_list:
                    continue
                else:
                    bill_line_obj_list.append(bill_line._recid)


                service, vat, vat2, service_vat = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))

                if artikel.umsatzart == 1:
                    dec_netroom_rev =  to_decimal(dec_netroom_rev) + to_decimal(bill_line.betrag) / to_decimal(service_vat)

                elif artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                    dec_netfb_rev =  to_decimal(dec_netfb_rev) + to_decimal(bill_line.betrag) / to_decimal(service_vat)

                elif artikel.umsatzart == 4:
                    dec_netother_rev =  to_decimal(dec_netother_rev) + to_decimal(bill_line.betrag) / to_decimal(service_vat)

        for s_list in query(s_list_list):

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.rechnr == s_list.rechnr) & (H_bill_line.departement == s_list.departement) & (H_bill_line.artnr > 0)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()
                service, vat, vat2, service_vat = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))

                if artikel.umsatzart == 1:
                    dec_netroom_rev =  to_decimal(dec_netroom_rev) + to_decimal(h_bill_line.betrag) / to_decimal(service_vat)

                elif artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                    dec_netfb_rev =  to_decimal(dec_netfb_rev) + to_decimal(h_bill_line.betrag) / to_decimal(service_vat)

                elif artikel.umsatzart == 4:
                    dec_netother_rev =  to_decimal(dec_netother_rev) + to_decimal(h_bill_line.betrag) / to_decimal(service_vat)
            s_list_list.remove(s_list)
        str_rate = ""
        ct = res_line.zimmer_wunsch

        if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
            ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
            contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)

        if trim (contcode) != "":
            str_rate = contcode

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()

        if mc_type:
            str_guest = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
        else:
            str_guest = ""
        mc_aclub = Mc_aclub()
        db_session.add(mc_aclub)

        mc_aclub.key = 2
        mc_aclub.cardnum = mc_guest.cardnum
        mc_aclub.date1 = res_line.ankunft
        mc_aclub.date2 = res_line.abreise
        mc_aclub.rechnr = bill_no
        mc_aclub.resnr = res_line.resnr
        mc_aclub.reslinnr = res_line.reslinnr
        mc_aclub.char1 = str_type
        mc_aclub.char2 = str_guest
        mc_aclub.char3 = str_rate
        mc_aclub.deci1 =  to_decimal(dec_netfb_rev)
        mc_aclub.deci2 =  to_decimal(dec_netroom_rate)
        mc_aclub.deci3 =  to_decimal(dec_netroom_rev)
        mc_aclub.deci4 =  to_decimal(dec_netother_rev)
        mc_aclub.deci5 =  to_decimal(dec_netfb_rev) + to_decimal(dec_netroom_rev) + to_decimal(dec_netother_rev)
        mc_aclub.billdatum = bill_date
        mc_aclub.sysdate = get_current_date()
        mc_aclub.zeit = get_current_time_in_seconds()


        str_type = ""
        str_guest = ""
        bill_no = 0
        qty_night = 0
        dec_other_rev =  to_decimal("0")
        dec_netother_rev =  to_decimal("0")
        dec_fb_rev =  to_decimal("0")
        dec_netfb_rev =  to_decimal("0")
        dec_room_rate =  to_decimal("0")
        dec_netroom_rate =  to_decimal("0")
        dec_room_rev =  to_decimal("0")
        dec_netroom_rev =  to_decimal("0")
        netroom_rev =  to_decimal("0")

    return generate_output()