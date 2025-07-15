from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Htparam, Waehrung, Artikel, Nightaudit, Nitestor, Hoteldpt, H_bill, H_bill_line, H_artikel

def nt_posrev():
    tot_food:decimal = to_decimal("0.0")
    tot_beverage:decimal = to_decimal("0.0")
    tot_misc:decimal = to_decimal("0.0")
    tot_cigar:decimal = to_decimal("0.0")
    tot_disc:decimal = to_decimal("0.0")
    tot_serv:decimal = to_decimal("0.0")
    tot_tax:decimal = to_decimal("0.0")
    tot_credit:decimal = to_decimal("0.0")
    tot_cash:decimal = to_decimal("0.0")
    tot_cash1:decimal = to_decimal("0.0")
    tot_trans:decimal = to_decimal("0.0")
    tot_ledger:decimal = to_decimal("0.0")
    tot_cover:int = 0
    i:int = 0
    anzahl:int = 0
    paramnr_list:List[int] = [489, 490, 492, 553, 554]
    artnr_list:List[int] = create_empty_list(5,0)
    bezeich:List[str] = create_empty_list(5,"")
    title_str:str = ""
    sep_line:str = ""
    n:int = 0
    progname:str = "nt-posrev.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 132
    p_length:int = 56
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    curr_date:date = None
    price_decimal:int = 0
    exchg_rate:decimal = 1
    foreign_rate:bool = False
    paramtext = htparam = waehrung = artikel = nightaudit = nitestor = hoteldpt = h_bill = h_bill_line = h_artikel = None

    output_list = turnover = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    turnover_list, Turnover = create_model("Turnover", {"departement":int, "deptname":str, "artnr":int, "food":decimal, "beverage":decimal, "misc":decimal, "cigarette":decimal, "discount":decimal, "t_service":decimal, "t_tax":decimal, "t_credit":decimal, "t_debit":decimal, "p_cash":decimal, "p_cash1":decimal, "r_transfer":decimal, "c_ledger":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_credit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, i, anzahl, paramnr_list, artnr_list, bezeich, title_str, sep_line, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, price_decimal, exchg_rate, foreign_rate, paramtext, htparam, waehrung, artikel, nightaudit, nitestor, hoteldpt, h_bill, h_bill_line, h_artikel


        nonlocal output_list, turnover
        nonlocal output_list_list, turnover_list

        return {}

    def balance_list():

        nonlocal tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_credit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, anzahl, paramnr_list, artnr_list, bezeich, title_str, sep_line, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, price_decimal, exchg_rate, foreign_rate, paramtext, htparam, waehrung, artikel, nightaudit, nitestor, hoteldpt, h_bill, h_bill_line, h_artikel


        nonlocal output_list, turnover
        nonlocal output_list_list, turnover_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Bill.Date :" + " " + to_string(curr_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "POS Daily Summary Sales Report"
        add_line(line)
        line = ""
        for i in range(1,130 + 1) :
            line = line + "_"
        add_line(line)
        add_line(" ")
        line = "Department FoodSales Beverage Misc Cigarett Discount service Tax Cash Cash(USD) Room-Transf CityLedger"
        add_line(line)
        line = ""
        for i in range(1,130 + 1) :
            line = line + "-"
        add_line(line)
        add_line("##end-header")

        for turnover in query(turnover_list):
            it_exist = True

            if turnover.departement == 0:
                line = ""
                for i in range(1,130 + 1) :
                    line = line + "-"
                add_line(line)
            line = to_string(turnover.deptname, "x(10)") + " " + to_string(turnover.food, "->>,>>>,>>9 ") + to_string(turnover.beverage, "->,>>>,>>9 ") + to_string(turnover.misc, "->>>,>>9 ") + to_string(turnover.cigarette, "->>>,>>9 ") + to_string(turnover.discount, "->,>>>,>>9 ") + to_string(turnover.t_service, "->,>>>,>>9 ") + to_string(turnover.t_tax, "->,>>>,>>9 ") + to_string(turnover.p_cash, "->>,>>>,>>9 ") + to_string(turnover.p_cash1, "->,>>9.99 ") + to_string(turnover.r_transfer, "->>,>>>,>>9 ") + to_string(turnover.c_ledger, "->>,>>>,>>9 ")
            add_line(line)

        if not it_exist:
            add_line("***** " + "No Bookings found" + " *****")
        add_line("##end-of-file")


    def add_line(s:str):

        nonlocal tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_credit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, i, anzahl, paramnr_list, artnr_list, bezeich, title_str, sep_line, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, price_decimal, exchg_rate, foreign_rate, paramtext, htparam, waehrung, artikel, nightaudit, nitestor, hoteldpt, h_bill, h_bill_line, h_artikel


        nonlocal output_list, turnover
        nonlocal output_list_list, turnover_list

        nitestor = db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge) & (Nitestor.line_nr == line_nr)).first()

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1


    def daysale_list():

        nonlocal tot_food, tot_beverage, tot_misc, tot_cigar, tot_disc, tot_serv, tot_tax, tot_credit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, anzahl, paramnr_list, artnr_list, bezeich, title_str, sep_line, n, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, curr_date, price_decimal, exchg_rate, foreign_rate, paramtext, htparam, waehrung, artikel, nightaudit, nitestor, hoteldpt, h_bill, h_bill_line, h_artikel


        nonlocal output_list, turnover
        nonlocal output_list_list, turnover_list

        curr_s:int = 0
        billnr:int = 0
        d_name:str = ""
        usr_nr:int = 0
        d_found:bool = "no"
        c_found:bool = "no"
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        netto:decimal = to_decimal("0.0")
        i:int = 0
        found:bool = False
        turnover_list.clear()
        tot_cover = 0
        tot_food =  to_decimal("0")
        tot_beverage =  to_decimal("0")
        tot_misc =  to_decimal("0")
        tot_disc =  to_decimal("0")
        tot_serv =  to_decimal("0")
        tot_tax =  to_decimal("0")
        tot_credit =  to_decimal("0")
        tot_cash1 =  to_decimal("0")
        tot_cash =  to_decimal("0")
        tot_trans =  to_decimal("0")
        tot_ledger =  to_decimal("0")

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1)).order_by(Hoteldpt.num).all():

            for h_bill in db_session.query(H_bill).filter(
                     (H_bill.departement == hoteldpt.num)).order_by(rechnr).all():

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == curr_date)).order_by(H_bill_line._recid).all():

                    turnover = query(turnover_list, filters=(lambda turnover: turnover.departement == hoteldpt.num), first=True)

                    if not turnover:
                        turnover = Turnover()
                        turnover_list.append(turnover)

                        turnover.departement = hoteldpt.num
                        turnover.deptname = hoteldpt.depart

                    if h_bill_line.artnr == 0:
                        turnover.r_transfer =  to_decimal(turnover.r_transfer) - to_decimal(h_bill_line.betrag)
                        turnover.t_debit =  to_decimal(turnover.t_debit) - to_decimal(h_bill_line.betrag)
                        tot_trans =  to_decimal(tot_trans) - to_decimal(h_bill_line.betrag)
                    else:

                        h_artikel = db_session.query(H_artikel).filter(
                                 (H_artikel.artnr == h_bill_line.artnr) & (H_artikel.departement == hoteldpt.num)).first()

                        if h_artikel.artart == 0:

                            artikel = db_session.query(Artikel).filter(
                                     (Artikel.departement == hoteldpt.num) & (Artikel.artnr == h_artikel.artnrfront)).first()
                        else:

                            artikel = db_session.query(Artikel).filter(
                                     (Artikel.departement == 0) & (Artikel.artnr == h_artikel.artnrfront)).first()

                        if h_artikel.artart == 0:
                            service =  to_decimal("0")
                            vat =  to_decimal("0")

                            if h_artikel.service_code > 0:

                                htparam = db_session.query(Htparam).filter(
                                         (Htparam.paramnr == h_artikel.service_code)).first()

                                if htparam:
                                    service =  to_decimal(0.01) * to_decimal(htparam.fdecimal)

                            htparam = db_session.query(Htparam).filter(
                                     (Htparam.paramnr == h_artikel.mwst_code)).first()

                            if htparam:
                                vat =  to_decimal(0.01) * to_decimal(htparam.fdecimal) * to_decimal((1) + to_decimal(service))
                            netto =  to_decimal(h_bill_line.betrag) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                            turnover.t_service =  to_decimal(turnover.t_service) + to_decimal(netto) * to_decimal(service)
                            turnover.t_tax =  to_decimal(turnover.t_tax) + to_decimal(netto) * to_decimal(vat)
                            turnover.t_credit =  to_decimal(turnover.t_credit) + to_decimal(h_bill_line.betrag)
                            tot_serv =  to_decimal(tot_serv) + to_decimal(netto) * to_decimal(service)
                            tot_tax =  to_decimal(tot_tax) + to_decimal(netto) * to_decimal(vat)
                            tot_credit =  to_decimal(tot_credit) + to_decimal(h_bill_line.betrag)

                            if artikel.artnr == artnr_list[0]:
                                turnover.food =  to_decimal(turnover.food) + to_decimal(netto)
                                tot_food =  to_decimal(tot_food) + to_decimal(netto)

                            elif artikel.artnr == artnr_list[1]:
                                turnover.beverage =  to_decimal(turnover.beverage) + to_decimal(netto)
                                tot_beverage =  to_decimal(tot_beverage) + to_decimal(netto)

                            elif artikel.artnr == artnr_list[2]:
                                turnover.misc =  to_decimal(turnover.misc) + to_decimal(netto)
                                tot_misc =  to_decimal(tot_misc) + to_decimal(netto)

                            elif artikel.artnr == artnr_list[3]:
                                turnover.cigarette =  to_decimal(turnover.cigarette) + to_decimal(netto)
                                tot_cigar =  to_decimal(tot_cigar) + to_decimal(netto)

                            elif artikel.artnr == artnr_list[4]:
                                turnover.discount =  to_decimal(turnover.discount) + to_decimal(netto)
                                tot_disc =  to_decimal(tot_disc) + to_decimal(netto)

                        elif h_artikel.artart == 6:

                            artikel = db_session.query(Artikel).filter(
                                     (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == 0)).first()

                            if artikel.pricetab:
                                turnover.p_cash1 =  to_decimal(turnover.p_cash1) - to_decimal(h_bill_line.fremdwbetrag)
                                tot_cash1 =  to_decimal(tot_cash1) - to_decimal(h_bill_line.fremdwbetrag)
                            else:
                                turnover.p_cash =  to_decimal(turnover.p_cash) - to_decimal(h_bill_line.betrag)
                                tot_cash =  to_decimal(tot_cash) - to_decimal(h_bill_line.betrag)
                            turnover.t_debit =  to_decimal(turnover.t_debit) - to_decimal(h_bill_line.betrag)

                        elif h_artikel.artart == 7 or h_artikel.artart == 2:
                            turnover.artnr = artikel.artnr
                            turnover.c_ledger =  to_decimal(turnover.c_ledger) - to_decimal(h_bill_line.betrag)
                            turnover.t_debit =  to_decimal(turnover.t_debit) - to_decimal(h_bill_line.betrag)
                            tot_ledger =  to_decimal(tot_ledger) - to_decimal(h_bill_line.betrag)
        turnover = Turnover()
        turnover_list.append(turnover)

        turnover.deptname = "TOTAL"
        turnover.food =  to_decimal(tot_food)
        turnover.beverage =  to_decimal(tot_beverage)
        turnover.misc =  to_decimal(tot_misc)
        turnover.discount =  to_decimal(tot_disc)
        turnover.t_service =  to_decimal(tot_serv)
        turnover.t_tax =  to_decimal(tot_tax)
        turnover.t_credit =  to_decimal(tot_credit)
        turnover.p_cash =  to_decimal(tot_cash)
        turnover.p_cash1 =  to_decimal(tot_cash1)
        turnover.r_transfer =  to_decimal(tot_trans)
        turnover.c_ledger =  to_decimal(tot_ledger)

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()
    htl_adr = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()
    htl_tel = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()

    if htparam.flogical:
        foreign_rate = True

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 240)).first()

    if htparam.flogical:
        foreign_rate = True

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    for i in range(1,5 + 1) :

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == paramnr_list[i - 1])).first()
        artnr_list[i - 1] = htparam.finteger

        if htparam.finteger != 0:
            anzahl = anzahl + 1

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == htparam.finteger) & (Artikel.departement == 1)).first()

            if artikel:
                bezeich[i - 1] = artikel.bezeich

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:
        pass
    else:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        daysale_list()
        balance_list()

    return generate_output()