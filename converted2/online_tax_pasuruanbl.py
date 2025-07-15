from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from models import H_bill_line, Htparam, Interface, Billjournal, Artikel, Hoteldpt, H_bill, H_artikel

def online_tax_pasuruanbl():
    tlist_list = []
    bill_date:date = None
    do_it:bool = False
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    serv_betrag:decimal = to_decimal("0.0")
    vat_betrag:decimal = to_decimal("0.0")
    serv_taxable:bool = False
    service_code:int = 0
    vat_proz:decimal = 10
    service_proz:decimal = 10
    count_int:int = 0
    h_bill_line = htparam = interface = billjournal = artikel = hoteldpt = h_bill = h_artikel = None

    tlist = bline = None

    tlist_list, Tlist = create_model("Tlist", {"datum":date, "id_no":int, "rmno":str, "amount":decimal, "amount_pjk":decimal, "date_time":str, "depart":int})

    Bline = create_buffer("Bline",H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tlist_list, bill_date, do_it, serv, vat, netto, serv_betrag, vat_betrag, serv_taxable, service_code, vat_proz, service_proz, count_int, h_bill_line, htparam, interface, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal bline


        nonlocal tlist, bline
        nonlocal tlist_list

        return {"tlist": tlist_list}

    def datetime2char(datum:date, zeit:int):

        nonlocal tlist_list, bill_date, do_it, serv, vat, netto, serv_betrag, vat_betrag, serv_taxable, service_code, vat_proz, service_proz, count_int, h_bill_line, htparam, interface, billjournal, artikel, hoteldpt, h_bill, h_artikel
        nonlocal bline


        nonlocal tlist, bline
        nonlocal tlist_list

        str:str = ""
        str = to_string(get_year(datum) , "9999") + "-" +\
                to_string(get_month(datum) , "99") + "-" +\
                to_string(get_day(datum) , "99") + " " +\
                substring(to_string(zeit, "HH:MM:SS") , 0, 2) + ":" +\
                substring(to_string(zeit, "HH:MM:SS") , 3, 2) + ":" +\
                substring(to_string(zeit, "HH:MM:SS") , 6, 2)


        return str


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 479)).first()
    serv_taxable = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1)).first()

    if htparam.fdecimal != 0:
        vat_proz =  to_decimal(htparam.fdecimal)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 136)).first()
    service_code = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == service_code)).first()

    if htparam and htparam.fdecimal != 0:
        service_proz =  to_decimal(htparam.fdecimal)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    if htparam:
        bill_date = htparam.fdate

    for interface in db_session.query(Interface).filter(
             (Interface.key == 38) & (Interface.action) & (func.lower(Interface.parameters) == ("close-bill").lower()) & (Interface.betriebsnr == 0)).order_by(Interface._recid).all():
        count_int = count_int + 1

        if count_int > 10:
            break

        if interface.decfield == 0:

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.rechnr == interface.intfield) & (to_decimal(Billjournal.departement) == interface.decfield) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).first()
            while None != billjournal:
                do_it = True

                if do_it:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()
                    do_it = None != artikel and (artikel.mwst_code != 0 or artikel.service_code != 0)

                    if do_it:
                        do_it = (artikel.artart == 0 or artikel.artart == 8)

                if do_it and re.match(r".*Remain.*",artikel.bezeich, re.IGNORECASE) and re.match(r".*Balance.*",artikel.bezeich, re.IGNORECASE):
                    do_it = False

                if do_it:

                    hoteldpt = db_session.query(Hoteldpt).filter(
                             (Hoteldpt.num == artikel.departement)).first()
                    serv =  to_decimal("0")
                    vat =  to_decimal("0")
                    netto =  to_decimal("0")
                    serv_betrag =  to_decimal("0")
                    vat_betrag =  to_decimal("0")


                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, billjournal.bill_datum, artikel.service_code, artikel.mwst_code))

                    if vat == 1:
                        netto =  to_decimal(billjournal.betrag) * to_decimal("100") / to_decimal(vat_proz)


                    else:

                        if serv == 1:
                            serv_betrag =  to_decimal(netto)

                        elif vat > 0:
                            netto =  to_decimal(billjournal.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                            serv_betrag =  to_decimal(netto) * to_decimal(serv)
                            vat_betrag =  to_decimal(netto) * to_decimal(vat)

                    if netto != 0:

                        tlist = query(tlist_list, filters=(lambda tlist: tlist.id_no == billjournal.rechnr and tlist.depart == billjournal.departement), first=True)

                        if not tlist:
                            tlist = Tlist()
                            tlist_list.append(tlist)

                            tlist.id_no = billjournal.rechnr
                            tlist.rmno = billjournal.zinr
                            tlist.depart = billjournal.departement


                        tlist.amount =  to_decimal(tlist.amount) + to_decimal(billjournal.betrag)
                        tlist.amount_pjk =  to_decimal(tlist.amount_pjk) + to_decimal(vat_betrag)
                        tlist.datum = billjournal.bill_datum
                        tlist.date_time = datetime2char (billjournal.bill_datum, billjournal.zeit)

                curr_recid = billjournal._recid
                billjournal = db_session.query(Billjournal).filter(
                         (Billjournal.rechnr == interface.intfield) & (to_decimal(Billjournal.departement) == interface.decfield) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0) & (Billjournal._recid > curr_recid)).first()
        else:

            h_bill_obj_list = []
            for h_bill, h_bill_line in db_session.query(H_bill, H_bill_line).join(H_bill_line,(H_bill_line.rechnr == H_bill.rechnr) & (H_bill_line.departement == H_bill.departement) & (H_bill_line.zeit >= 0) & (H_bill_line.artnr > 0) & (H_bill_line.betrag != 0)).filter(
                     (H_bill.flag == 1) & (H_bill.departement == to_int(interface.decfield)) & (H_bill.rechnr == interface.intfield)).order_by(H_bill._recid).all():
                if h_bill._recid in h_bill_obj_list:
                    continue
                else:
                    h_bill_obj_list.append(h_bill._recid)

                bline_obj_list = []
                for bline, h_artikel in db_session.query(Bline, H_artikel).join(H_artikel,(H_artikel.artnr == Bline.artnr) & (H_artikel.departement == Bline.departement)).filter(
                         (Bline.departement == h_bill.departement) & (Bline.rechnr == h_bill.rechnr) & (Bline.artnr > 0)).order_by(Bline._recid).all():
                    if bline._recid in bline_obj_list:
                        continue
                    else:
                        bline_obj_list.append(bline._recid)

                    if h_artikel.artart == 0 or h_artikel.artart == 8:
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")
                        netto =  to_decimal("0")
                        serv_betrag =  to_decimal("0")
                        vat_betrag =  to_decimal("0")

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == h_artikel.departement)).first()

                        if artikel:
                            serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bline.bill_datum, artikel.service_code, artikel.mwst_code))

                            if bline.betrag > 0:

                                if vat == 1:
                                    netto =  to_decimal(bline.betrag) * to_decimal("100") / to_decimal(vat_proz)


                                else:

                                    if serv == 1:
                                        serv_betrag =  to_decimal(netto)

                                    elif vat > 0:
                                        netto =  to_decimal(bline.betrag) / to_decimal((1) + to_decimal(serv) + to_decimal(vat) )
                                        serv_betrag =  to_decimal(netto) * to_decimal(serv)
                                        vat_betrag =  to_decimal(netto) * to_decimal(vat)

                                if netto != 0:

                                    tlist = query(tlist_list, filters=(lambda tlist: tlist.id_no == bline.rechnr and tlist.depart == bline.departement), first=True)

                                    if not tlist:
                                        tlist = Tlist()
                                        tlist_list.append(tlist)

                                        tlist.id_no = bline.rechnr
                                        tlist.depart = bline.departement
                                        tlist.rmno = to_string(h_bill.tischnr)


                                    tlist.datum = bline.bill_datum
                                    tlist.amount =  to_decimal(tlist.amount) + to_decimal(bline.betrag)
                                    tlist.amount_pjk =  to_decimal(tlist.amount_pjk) + to_decimal(vat_betrag)
                                    tlist.date_time = datetime2char (bline.bill_datum, bline.zeit)

    return generate_output()