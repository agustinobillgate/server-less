from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Mc_guest, Bill, Res_line, Artikel, Bill_line, Mc_aclub, H_bill_line, H_artikel, H_bill

def nt_aclub():
    curr_date:date = None
    vat:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    do_it:bool = False
    serv_taxable:bool = False
    htparam = mc_guest = bill = res_line = artikel = bill_line = mc_aclub = h_bill_line = h_artikel = h_bill = None

    hbbuff = artbuff = None

    Hbbuff = create_buffer("Hbbuff",H_bill_line)
    Artbuff = create_buffer("Artbuff",H_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, vat, service, do_it, serv_taxable, htparam, mc_guest, bill, res_line, artikel, bill_line, mc_aclub, h_bill_line, h_artikel, h_bill
        nonlocal hbbuff, artbuff


        nonlocal hbbuff, artbuff

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()

    if htparam.flogical:
        serv_taxable = True

    res_line_obj_list = []
    for res_line, mc_guest, bill in db_session.query(Res_line, Mc_guest, Bill).join(Mc_guest,(Mc_guest.gastnr == Res_line.gastnrmember) & (Mc_guest.activeflag)).join(Bill,(Bill.resnr == Res_line.resnr) & (Bill.reslinnr == Res_line.reslinnr)).filter(
             (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == curr_date)).order_by(Res_line._recid).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)

        bill_line_obj_list = []
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & ((Artikel.artart == 0) | ((Artikel.artart == 9) & (Artikel.artgrp == 0)) | (Artikel.artart == 1))).filter(
                 (Bill_line.rechnr == bill.rechnr) | ((Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr))).order_by(Bill_line._recid).all():
            if bill_line._recid in bill_line_obj_list:
                continue
            else:
                bill_line_obj_list.append(bill_line._recid)


            mc_aclub = Mc_aclub()
            db_session.add(mc_aclub)

            mc_aclub.sysdate = get_current_date()
            mc_aclub.zeit = get_current_time_in_seconds()
            mc_aclub.key = 1
            mc_aclub.incl_flag = 1
            mc_aclub.cardnum = mc_guest.cardnum
            mc_aclub.billdatum = bill_line.bill_datum
            mc_aclub.billtype = 0
            mc_aclub.rechnr = bill.rechnr
            mc_aclub.artnr = bill_line.artnr
            mc_aclub.departement = bill_line.departement
            mc_aclub.betrag =  to_decimal(bill_line.betrag)
            mc_aclub.resnr = res_line.resnr
            mc_aclub.reslinnr = res_line.reslinnr
            mc_aclub.bemerk = bill_line.bezeich


            service =  to_decimal("0")
            vat =  to_decimal("0")

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.service_code)).first()

            if htparam:
                service =  to_decimal(0.01) * to_decimal(htparam.fdecimal)

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam:

                if serv_taxable:
                    vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal) * to_decimal((1) + to_decimal(service))
                else:
                    vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal)
            mc_aclub.service =  to_decimal(bill_line.betrag) / to_decimal(service)
            mc_aclub.vat =  to_decimal(bill_line.betrag) / to_decimal(vat)
            mc_aclub.nettobetrag =  to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )

    h_bill_obj_list = []
    for h_bill, hbbuff, mc_guest in db_session.query(H_bill, Hbbuff, Mc_guest).join(Hbbuff,(Hbbuff.rechnr == H_bill.rechnr) & (Hbbuff.bill_datum == curr_date) & (Hbbuff.departement == H_bill.departement)).join(Mc_guest,(Mc_guest.gastnr == H_bill.resnr) & (Mc_guest.activeflag)).filter(
             (H_bill.resnr > 0) & (H_bill.reslinnr == 0) & (H_bill.flag == 1)).order_by(H_bill._recid).all():
        if h_bill._recid in h_bill_obj_list:
            continue
        else:
            h_bill_obj_list.append(h_bill._recid)


        do_it = False

        h_bill_line_obj_list = []
        for h_bill_line, artbuff in db_session.query(H_bill_line, Artbuff).join(Artbuff,(Artbuff.artnr == H_bill_line.artnr) & (Artbuff.departement == H_bill_line.departement) & ((Artbuff.artart == 2) | (Artbuff.artart == 6) | (Artbuff.artart == 7))).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == curr_date) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            do_it = True

        if do_it:

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.bill_datum == curr_date)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()
                mc_aclub = Mc_aclub()
                db_session.add(mc_aclub)

                mc_aclub.sysdate = get_current_date()
                mc_aclub.zeit = get_current_time_in_seconds()
                mc_aclub.key = 1
                mc_aclub.incl_flag = 1
                mc_aclub.cardnum = mc_guest.cardnum
                mc_aclub.billdatum = h_bill_line.bill_datum
                mc_aclub.billtype = 1
                mc_aclub.rechnr = h_bill.rechnr
                mc_aclub.artnr = artikel.artnr
                mc_aclub.departement = h_bill_line.departement
                mc_aclub.betrag =  to_decimal(h_bill_line.betrag)
                mc_aclub.nettobetrag =  to_decimal(h_bill_line.nettobetrag)
                mc_aclub.bemerk = to_string(h_artikel.artnr, ">>>9") + "-" +\
                        h_bill_line.bezeich


                service =  to_decimal("0")
                vat =  to_decimal("0")

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == artikel.service_code)).first()

                if htparam:
                    service =  to_decimal(0.01) * to_decimal(htparam.fdecimal)

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == artikel.mwst_code)).first()

                if htparam:

                    if serv_taxable:
                        vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal) * to_decimal((1) + to_decimal(service))
                    else:
                        vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal)
                mc_aclub.vat =  to_decimal(vat)
                mc_aclub.service =  to_decimal(service)


    h_bill_obj_list = []
    for h_bill, hbbuff, res_line, mc_guest in db_session.query(H_bill, Hbbuff, Res_line, Mc_guest).join(Hbbuff,(Hbbuff.rechnr == H_bill.rechnr) & (Hbbuff.bill_datum == curr_date) & (Hbbuff.departement == H_bill.departement)).join(Res_line,(Res_line.resnr == H_bill.resnr) & (Res_line.reslinnr == H_bill.reslinnr)).join(Mc_guest,(Mc_guest.gastnr == Res_line.gastnrmember) & (Mc_guest.activeflag)).filter(
             (H_bill.resnr > 0) & (H_bill.reslinnr > 0) & (H_bill.flag == 1)).order_by(H_bill._recid).all():
        if h_bill._recid in h_bill_obj_list:
            continue
        else:
            h_bill_obj_list.append(h_bill._recid)


        do_it = False

        h_bill_line_obj_list = []
        for h_bill_line, artbuff in db_session.query(H_bill_line, Artbuff).join(Artbuff,(Artbuff.artnr == H_bill_line.artnr) & (Artbuff.departement == H_bill_line.departement) & ((Artbuff.artart == 2) | (Artbuff.artart == 6) | (Artbuff.artart == 7))).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == curr_date) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            do_it = True

        if do_it:

            h_bill_line_obj_list = []
            for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.bill_datum == curr_date)).order_by(H_bill_line._recid).all():
                if h_bill_line._recid in h_bill_line_obj_list:
                    continue
                else:
                    h_bill_line_obj_list.append(h_bill_line._recid)

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()
                mc_aclub = Mc_aclub()
                db_session.add(mc_aclub)

                mc_aclub.sysdate = get_current_date()
                mc_aclub.zeit = get_current_time_in_seconds()
                mc_aclub.key = 1
                mc_aclub.incl_flag = 1
                mc_aclub.cardnum = mc_guest.cardnum
                mc_aclub.billdatum = h_bill_line.bill_datum
                mc_aclub.billtype = 1
                mc_aclub.rechnr = h_bill.rechnr
                mc_aclub.artnr = artikel.artnr
                mc_aclub.departement = h_bill_line.departement
                mc_aclub.betrag =  to_decimal(h_bill_line.betrag)
                mc_aclub.nettobetrag =  to_decimal(h_bill_line.nettobetrag)
                mc_aclub.bemerk = to_string(h_artikel.artnr, ">>>9") + "-" +\
                        h_bill_line.bezeich


                service =  to_decimal("0")
                vat =  to_decimal("0")

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == artikel.service_code)).first()

                if htparam:
                    service =  to_decimal(0.01) * to_decimal(htparam.fdecimal)

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == artikel.mwst_code)).first()

                if htparam:

                    if serv_taxable:
                        vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal) * to_decimal((1) + to_decimal(service))
                    else:
                        vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal)
                mc_aclub.vat =  to_decimal(vat)
                mc_aclub.service =  to_decimal(service)


    return generate_output()