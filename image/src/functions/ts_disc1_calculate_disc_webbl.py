from functions.additional_functions import *
import decimal
from functions.ts_disc1_get_articlebl import ts_disc1_get_articlebl
from functions.ts_disc1_cal_amountbl import ts_disc1_cal_amountbl
from functions.read_h_artikelbl import read_h_artikelbl
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.htpdec import htpdec
from models import H_bill_line, H_artikel, Htparam, Hoteldpt

def ts_disc1_calculate_disc_webbl(pvilanguage:int, dept:int, procent:decimal, disc_value:decimal, menu_disc:[Menu_disc]):
    msg_str = ""
    t_calc_disc_list = []
    disc_list_list = []
    lvcarea:str = "TS_disc1"
    incl_service:bool = False
    incl_mwst:bool = False
    service_tax:bool = False
    vat2:decimal = 0
    fact:decimal = 1
    fb_netto:decimal = 0
    f_dec:decimal = 0
    amount:decimal = 0
    balance:decimal = 0
    orig_amt:decimal = 0
    disc_alert:bool = True
    disc_service:bool = False
    disc_tax:bool = False
    h_service:decimal = 0
    service:decimal = 0
    h_mwst:decimal = 0
    mwst:decimal = 0
    netto_betrag:decimal = 0
    nett_amount:decimal = 0
    voucher_art:int = 0
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    price_decimal:int = 0
    b_billart:int = 0
    b2_billart:int = 0
    billart:int = 0
    o_artnrfront:int = 0
    b_artnrfront:int = 0
    description:str = ""
    servtax_use_foart:bool = False
    h_bill_line = h_artikel = htparam = hoteldpt = None

    menu_disc = disc_list = t_calc_disc = t_hart = t_h_artikel = t_artikel = None

    menu_disc_list, Menu_disc = create_model_like(H_bill_line)
    disc_list_list, Disc_list = create_model("Disc_list", {"h_artnr":int, "bezeich":str, "artnr":int, "mwst":int, "service":int, "umsatzart":int, "defaultflag":bool, "amount":decimal, "netto_amt":decimal, "service_amt":decimal, "mwst_amt":decimal})
    t_calc_disc_list, T_calc_disc = create_model("T_calc_disc", {"select_amt_taxserv":decimal, "disc_taxserv":decimal, "balance_taxserv":decimal, "selected_amount":decimal, "discount":decimal, "balance":decimal})
    t_hart_list, T_hart = create_model_like(H_artikel)
    t_h_artikel_list, T_h_artikel = create_model("T_h_artikel", {"mwst":int, "service":int, "artnr":int, "bezeich":str, "service_code":int, "mwst_code":int})
    t_artikel_list, T_artikel = create_model("T_artikel", {"umsatzart":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_calc_disc_list, disc_list_list, lvcarea, incl_service, incl_mwst, service_tax, vat2, fact, fb_netto, f_dec, amount, balance, orig_amt, disc_alert, disc_service, disc_tax, h_service, service, h_mwst, mwst, netto_betrag, nett_amount, voucher_art, disc_art1, disc_art2, disc_art3, price_decimal, b_billart, b2_billart, billart, o_artnrfront, b_artnrfront, description, servtax_use_foart, h_bill_line, h_artikel, htparam, hoteldpt


        nonlocal menu_disc, disc_list, t_calc_disc, t_hart, t_h_artikel, t_artikel
        nonlocal menu_disc_list, disc_list_list, t_calc_disc_list, t_hart_list, t_h_artikel_list, t_artikel_list
        return {"msg_str": msg_str, "t-calc-disc": t_calc_disc_list, "disc-list": disc_list_list}

    billart, description, b_artnrfront, o_artnrfront, disc_list_list = get_output(ts_disc1_get_articlebl(dept, disc_value, procent, b_billart, b2_billart))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1203)).first()

    if htparam.paramgruppe == 19 and htparam.feldtyp == 4:
        disc_alert = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 468)).first()
    disc_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 469)).first()
    disc_tax = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()
    incl_mwst = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()
    incl_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 479)).first()
    service_tax = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()
    voucher_art = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()
    disc_art1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()
    disc_art2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()
    disc_art3 = htparam.finteger

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult
    netto_betrag = 0
    service = 0
    mwst = 0

    for disc_list in query(disc_list_list):
        disc_list.netto_amt = 0
        disc_list.amount = 0
        disc_list.service_amt = 0
        disc_list.mwst_amt = 0


    t_calc_disc_list.clear()
    t_calc_disc = T_calc_disc()
    t_calc_disc_list.append(t_calc_disc)


    for menu_disc in query(menu_disc_list, filters=(lambda menu_disc :menu_disc.artnr != disc_art1 and menu_disc.artnr != disc_art2 and menu_disc.artnr != disc_art3)):
        balance = balance + menu_disc.betrag
        t_h_artikel_list, t_artikel_list = get_output(ts_disc1_cal_amountbl(menu_disc.artnr, menu_disc.departement))

        t_h_artikel = query(t_h_artikel_list, first=True)

        t_artikel = query(t_artikel_list, first=True)
        netto_betrag = netto_betrag + menu_disc.anzahl * menu_disc.epreis
        nett_amount = nett_amount + menu_disc.anzahl * menu_disc.epreis

        disc_list = query(disc_list_list, filters=(lambda disc_list :disc_list.umsatzart == t_artikel.umsatzart and disc_list.mwst == t_h_artikel.mwst and disc_list.service == t_h_artikel.service), first=True)

        if not disc_list:

            if disc_alert:
                msg_str = translateExtended ("Discount Article [1] not found for menu item:", lvcarea, "") + " " + to_string(t_h_artikel.artnr) + " - " + t_h_artikel.bezeich

            disc_list = query(disc_list_list, filters=(lambda disc_list :disc_list.umsatzart == t_artikel.umsatzart and disc_list.mwst == t_h_artikel.mwst), first=True)

            if not disc_list:

                if disc_alert:
                    msg_str = translateExtended ("Discount Article [2] not found for menu item:", lvcarea, "") + " " + to_string(t_h_artikel.artnr) + " - " + t_h_artikel.bezeich

                disc_list = query(disc_list_list, filters=(lambda disc_list :disc_list.umsatzart == t_artikel.umsatzart), first=True)
        disc_list.netto_amt = disc_list.netto_amt + menu_disc.anzahl * menu_disc.epreis

        if servtax_use_foart:
            t_hart_list = get_output(read_h_artikelbl(1, disc_list.h_artnr, dept, "", 0, 0, True))

            t_hart = query(t_hart_list, first=True)
            h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, t_hart.artnrfront, dept, None))
            h_mwst = h_mwst + vat2

            if incl_service or not disc_service:
                h_service = 0

            if incl_mwst or not disc_tax:
                h_mwst = 0
            h_service = menu_disc.epreis * h_service
            disc_list.service_amt = disc_list.service_amt + h_service * menu_disc.anzahl
            service = service + h_service * menu_disc.anzahl
            h_mwst = menu_disc.epreis * h_mwst
            disc_list.mwst_amt = disc_list.mwst_amt + h_mwst * menu_disc.anzahl
            mwst = mwst + h_mwst * menu_disc.anzahl


        else:
            h_service = 0

            if not incl_service and t_h_artikel.service_code != 0 and disc_service:
                f_dec = get_output(htpdec(disc_list.service))

                if f_dec != 0:
                    h_service = menu_disc.epreis * f_dec / 100
                    disc_list.service_amt = disc_list.service_amt + h_service * menu_disc.anzahl
                    service = service + h_service * menu_disc.anzahl


            h_mwst = 0

            if not incl_mwst and t_h_artikel.mwst_code != 0 and disc_tax:
                f_dec = get_output(htpdec(disc_list.mwst))

                if f_dec != 0:
                    h_mwst = f_dec

                    if service_tax:
                        h_mwst = h_mwst * (menu_disc.epreis + h_service) / 100
                    else:
                        h_mwst = h_mwst * menu_disc.epreis / 100
                    disc_list.mwst_amt = disc_list.mwst_amt + h_mwst * menu_disc.anzahl
                    mwst = mwst + h_mwst * menu_disc.anzahl


    fb_netto = netto_betrag
    netto_betrag = - procent * netto_betrag / 100
    service = - procent * service / 100
    mwst = - procent * mwst / 100
    amount = netto_betrag + service + mwst

    if disc_value == 0:
        amount = round(netto_betrag + service + mwst, price_decimal)
    else:
        amount = - disc_value

    for disc_list in query(disc_list_list, filters=(lambda disc_list :disc_list.netto_amt != 0)):
        disc_list.amount = amount * (disc_list.netto_amt / fb_netto)

        if disc_list.netto_amt != 0 and disc_value == 0:
            disc_list.netto_amt = - procent * disc_list.netto_amt / 100
            disc_list.service_amt = - procent * disc_list.service_amt / 100
            disc_list.mwst_amt = - procent * disc_list.mwst_amt / 100
            disc_list.amount = disc_list.netto_amt +\
                    disc_list.service_amt + disc_list.mwst_amt
            disc_list.amount = round(disc_list.amount, price_decimal)


    t_calc_disc.select_amt_taxserv = round(balance, price_decimal)
    t_calc_disc.disc_taxserv = round(t_calc_disc.disc_taxserv + amount, price_decimal)
    t_calc_disc.balance_taxserv = round(balance + t_calc_disc.disc_taxserv, price_decimal)
    t_calc_disc.selected_amount = round(nett_amount, price_decimal)
    t_calc_disc.discount = round(t_calc_disc.discount + netto_betrag, price_decimal)
    t_calc_disc.balance = round(nett_amount + t_calc_disc.discount, price_decimal)

    return generate_output()