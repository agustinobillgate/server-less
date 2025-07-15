from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Bill, Billjournal, Artikel

def create_online_tax_vanguard():
    fr_date:date = 03/29/17
    to_date:date = 03/29/17
    datum:date = None
    res_line = bill = billjournal = artikel = None

    tlist = tlist_line = None

    tlist_list, Tlist = create_model("Tlist", {"checknumber":int, "departement":int, "openchecktime":str, "closedchecktime":str, "ordertype":str, "outletname":str, "tablenumber":str, "cashierid":str, "cashiername":str, "cover":str, "companyname1":str, "companyname2":str, "address1":str, "address2":str, "taxcode":str, "emailaddress":str, "subtotal":decimal, "servicecharge":decimal, "tax1":decimal, "tax2":decimal, "tot_amt":decimal, "paymenttype":str, "tip":decimal})
    tlist_line_list, Tlist_line = create_model("Tlist_line", {"checknumber":int, "departement":int, "itemname":str, "itemqty":str, "itemprice":decimal, "itemtotal":decimal, "discountname":str, "discountqty":int, "discountprice":decimal, "discounttotal":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fr_date, to_date, datum, res_line, bill, billjournal, artikel


        nonlocal tlist, tlist_line
        nonlocal tlist_list, tlist_line_list

        return {}

    def step1(bill_date:date):

        nonlocal fr_date, to_date, datum, res_line, bill, billjournal, artikel


        nonlocal tlist, tlist_line
        nonlocal tlist_list, tlist_line_list

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resstatus == 8) & (Res_line.abreise == bill_date)).first()
        while None != res_line :

            for bill in db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr)).order_by(Bill._recid).all():

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.rechnr == bill.rechnr) & (Billjournal.anzahl != 0) & (Billjournal.betrag != 0)).order_by(Billjournal.rechnr, Billjournal.departement, Billjournal.artnr).all():

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == billjournal.artnr) & (Artikel.departement == billjournal.departement)).first()

                    if artikel:

                        if artikel.artart == 0 or artikel.artart == 8:
                            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == bill_date) & (Res_line._recid > curr_recid)).first()


    for datum in date_range(fr_date,to_date) :
        step1(datum)

    return generate_output()