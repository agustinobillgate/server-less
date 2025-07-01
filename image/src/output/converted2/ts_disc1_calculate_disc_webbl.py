#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_disc1_get_articlebl import ts_disc1_get_articlebl
from functions.ts_disc1_cal_amountbl import ts_disc1_cal_amountbl
from functions.read_h_artikelbl import read_h_artikelbl
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.htpdec import htpdec
from models import H_bill_line, H_artikel, Htparam, Hoteldpt

menu_disc_list, Menu_disc = create_model_like(H_bill_line)

def ts_disc1_calculate_disc_webbl(pvilanguage:int, dept:int, procent:Decimal, disc_value:Decimal, menu_disc_list:[Menu_disc]):

    prepare_cache ([Htparam, Hoteldpt])

    msg_str = ""
    t_calc_disc_list = []
    disc_list_list = []
    lvcarea:string = "TS-disc1"
    incl_service:bool = False
    incl_mwst:bool = False
    service_tax:bool = False
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = 1
    fb_netto:Decimal = to_decimal("0.0")
    f_dec:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    balance:Decimal = to_decimal("0.0")
    orig_amt:Decimal = to_decimal("0.0")
    disc_alert:bool = True
    disc_service:bool = False
    disc_tax:bool = False
    h_service:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    mwst:Decimal = to_decimal("0.0")
    netto_betrag:Decimal = to_decimal("0.0")
    nett_amount:Decimal = to_decimal("0.0")
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
    description:string = ""
    tmp_count:Decimal = to_decimal("0.0")
    servtax_use_foart:bool = False
    tot_disc:Decimal = to_decimal("0.0")
    h_bill_line = h_artikel = htparam = hoteldpt = None

    menu_disc = disc_list = t_calc_disc = t_hart = t_h_artikel = t_artikel = None

    disc_list_list, Disc_list = create_model("Disc_list", {"h_artnr":int, "bezeich":string, "artnr":int, "mwst":int, "service":int, "umsatzart":int, "defaultflag":bool, "amount":Decimal, "netto_amt":Decimal, "service_amt":Decimal, "mwst_amt":Decimal})
    t_calc_disc_list, T_calc_disc = create_model("T_calc_disc", {"select_amt_taxserv":Decimal, "disc_taxserv":Decimal, "balance_taxserv":Decimal, "selected_amount":Decimal, "discount":Decimal, "balance":Decimal})
    t_hart_list, T_hart = create_model_like(H_artikel)
    t_h_artikel_list, T_h_artikel = create_model("T_h_artikel", {"mwst":int, "service":int, "artnr":int, "bezeich":string, "service_code":int, "mwst_code":int})
    t_artikel_list, T_artikel = create_model("T_artikel", {"umsatzart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, t_calc_disc_list, disc_list_list, lvcarea, incl_service, incl_mwst, service_tax, vat2, fact, fb_netto, f_dec, amount, balance, orig_amt, disc_alert, disc_service, disc_tax, h_service, service, h_mwst, mwst, netto_betrag, nett_amount, voucher_art, disc_art1, disc_art2, disc_art3, price_decimal, b_billart, b2_billart, billart, o_artnrfront, b_artnrfront, description, tmp_count, servtax_use_foart, tot_disc, h_bill_line, h_artikel, htparam, hoteldpt
        nonlocal pvilanguage, dept, procent, disc_value


        nonlocal menu_disc, disc_list, t_calc_disc, t_hart, t_h_artikel, t_artikel
        nonlocal disc_list_list, t_calc_disc_list, t_hart_list, t_h_artikel_list, t_artikel_list

        return {"msg_str": msg_str, "t-calc-disc": t_calc_disc_list, "disc-list": disc_list_list}

    billart, description, b_artnrfront, o_artnrfront, disc_list_list = get_output(ts_disc1_get_articlebl(dept, disc_value, procent, b_billart, b2_billart))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1203)]})

    if htparam:

        if htparam.paramgruppe == 19 and htparam.feldtyp == 4:
            disc_alert = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})

    if htparam:
        disc_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})

    if htparam:
        disc_tax = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

    if htparam:
        incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

    if htparam:
        incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

    if htparam:
        service_tax = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})

    if htparam:
        voucher_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam:
        disc_art3 = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult
    netto_betrag =  to_decimal("0")
    service =  to_decimal("0")
    mwst =  to_decimal("0")

    for disc_list in query(disc_list_list):
        disc_list.netto_amt =  to_decimal("0")
        disc_list.amount =  to_decimal("0")
        disc_list.service_amt =  to_decimal("0")
        disc_list.mwst_amt =  to_decimal("0")


    t_calc_disc_list.clear()
    t_calc_disc = T_calc_disc()
    t_calc_disc_list.append(t_calc_disc)


    for menu_disc in query(menu_disc_list, filters=(lambda menu_disc: menu_disc.artnr != disc_art1 and menu_disc.artnr != disc_art2 and menu_disc.artnr != disc_art3)):
        balance =  to_decimal(balance) + to_decimal(menu_disc.betrag)
        t_h_artikel_list, t_artikel_list = get_output(ts_disc1_cal_amountbl(menu_disc.artnr, menu_disc.departement))

        t_h_artikel = query(t_h_artikel_list, first=True)

        t_artikel = query(t_artikel_list, first=True)
        netto_betrag =  to_decimal(netto_betrag) + to_decimal(menu_disc.anzahl) * to_decimal(menu_disc.epreis)
        nett_amount =  to_decimal(nett_amount) + to_decimal(menu_disc.anzahl) * to_decimal(menu_disc.epreis)

        disc_list = query(disc_list_list, filters=(lambda disc_list: disc_list.umsatzart == t_artikel.umsatzart and disc_list.mwst == t_h_artikel.mwst_code and disc_list.service == t_h_artikel.service_code), first=True)

        if not disc_list:

            if disc_alert:
                msg_str = translateExtended ("Discount Article [1] not found for menu item:", lvcarea, "") + " " + to_string(t_h_artikel.artnr) + " - " + t_h_artikel.bezeich

            disc_list = query(disc_list_list, filters=(lambda disc_list: disc_list.umsatzart == t_artikel.umsatzart and disc_list.mwst == t_h_artikel.mwst_code), first=True)

            if not disc_list:

                if disc_alert:
                    msg_str = translateExtended ("Discount Article [2] not found for menu item:", lvcarea, "") + " " + to_string(t_h_artikel.artnr) + " - " + t_h_artikel.bezeich

                disc_list = query(disc_list_list, filters=(lambda disc_list: disc_list.umsatzart == t_artikel.umsatzart), first=True)
        disc_list.netto_amt =  to_decimal(disc_list.netto_amt) + to_decimal(menu_disc.anzahl) * to_decimal(menu_disc.epreis)

        if servtax_use_foart:
            t_hart_list = get_output(read_h_artikelbl(1, disc_list.h_artnr, dept, "", 0, 0, True))

            t_hart = query(t_hart_list, first=True)
            h_service, h_mwst, vat2, fact = get_output(calc_servtaxesbl(1, t_hart.artnrfront, dept, None))
            h_mwst =  to_decimal(h_mwst) + to_decimal(vat2)

            if incl_service or not disc_service:
                h_service =  to_decimal("0")

            if incl_mwst or not disc_tax:
                h_mwst =  to_decimal("0")
            h_service =  to_decimal(menu_disc.epreis) * to_decimal(h_service)
            disc_list.service_amt =  to_decimal(disc_list.service_amt) + to_decimal(h_service) * to_decimal(menu_disc.anzahl)
            service =  to_decimal(service) + to_decimal(h_service) * to_decimal(menu_disc.anzahl)
            h_mwst =  to_decimal(menu_disc.epreis) * to_decimal(h_mwst)
            disc_list.mwst_amt =  to_decimal(disc_list.mwst_amt) + to_decimal(h_mwst) * to_decimal(menu_disc.anzahl)
            mwst =  to_decimal(mwst) + to_decimal(h_mwst) * to_decimal(menu_disc.anzahl)


        else:
            h_service =  to_decimal("0")

            if not incl_service and t_h_artikel.service_code != 0 and disc_service:
                f_dec = get_output(htpdec(disc_list.service))

                if f_dec != 0:
                    h_service =  to_decimal(menu_disc.epreis) * to_decimal(f_dec) / to_decimal("100")
                    disc_list.service_amt =  to_decimal(disc_list.service_amt) + to_decimal(h_service) * to_decimal(menu_disc.anzahl)
                    service =  to_decimal(service) + to_decimal(h_service) * to_decimal(menu_disc.anzahl)


            h_mwst =  to_decimal("0")

            if not incl_mwst and t_h_artikel.mwst_code != 0 and disc_tax:
                f_dec = get_output(htpdec(disc_list.mwst))

                if f_dec != 0:
                    h_mwst =  to_decimal(f_dec)
                    tmp_count =  to_decimal(menu_disc.epreis) + to_decimal(h_service)

                    if service_tax:
                        h_mwst =  to_decimal(h_mwst) * to_decimal(tmp_count) / to_decimal("100")
                    else:
                        h_mwst =  to_decimal(h_mwst) * to_decimal(menu_disc.epreis) / to_decimal("100")
                    disc_list.mwst_amt =  to_decimal(disc_list.mwst_amt) + to_decimal(h_mwst) * to_decimal(menu_disc.anzahl)
                    mwst =  to_decimal(mwst) + to_decimal(h_mwst) * to_decimal(menu_disc.anzahl)


    fb_netto =  to_decimal(netto_betrag)
    netto_betrag =  - to_decimal(procent) * to_decimal(netto_betrag) / to_decimal("100")
    service =  - to_decimal(procent) * to_decimal(service) / to_decimal("100")
    mwst =  - to_decimal(procent) * to_decimal(mwst) / to_decimal("100")
    amount =  to_decimal(netto_betrag) + to_decimal(service) + to_decimal(mwst)

    if disc_value == 0:
        amount = to_decimal(round(netto_betrag + service + mwst , price_decimal))
    else:
        amount =  - to_decimal(disc_value)

    for disc_list in query(disc_list_list, filters=(lambda disc_list: disc_list.netto_amt != 0)):
        disc_list.amount =  to_decimal(amount) * to_decimal((disc_list.netto_amt) / to_decimal(fb_netto) )

        if disc_list.netto_amt != 0 and disc_value == 0:
            disc_list.netto_amt =  - to_decimal(procent) * to_decimal(disc_list.netto_amt) / to_decimal("100")
            disc_list.service_amt =  - to_decimal(procent) * to_decimal(disc_list.service_amt) / to_decimal("100")
            disc_list.mwst_amt =  - to_decimal(procent) * to_decimal(disc_list.mwst_amt) / to_decimal("100")
            disc_list.amount =  to_decimal(disc_list.netto_amt) +\
                    disc_list.service_amt + to_decimal(disc_list.mwst_amt)
            disc_list.amount = to_decimal(round(disc_list.amount , price_decimal))
            tot_disc =  to_decimal(tot_disc) + to_decimal(disc_list.amount)


    for disc_list in query(disc_list_list, filters=(lambda disc_list: disc_list.netto_amt == 0), sort_by=[("h_artnr",True)]):
        disc_list.amount =  to_decimal(amount) - to_decimal(tot_disc)
        break

    for disc_list in query(disc_list_list, filters=(lambda disc_list: disc_list.netto_amt == 0), sort_by=[("h_artnr",True)]):
        amount =  to_decimal(amount) - to_decimal(disc_list.amount)
        break
    t_calc_disc.select_amt_taxserv = to_decimal(round(balance , price_decimal))
    t_calc_disc.disc_taxserv = to_decimal(round(t_calc_disc.disc_taxserv + amount , price_decimal))
    t_calc_disc.balance_taxserv = to_decimal(round(balance + t_calc_disc.disc_taxserv , price_decimal))
    t_calc_disc.selected_amount = to_decimal(round(nett_amount , price_decimal))
    t_calc_disc.discount = to_decimal(round(t_calc_disc.discount + netto_betrag , price_decimal))
    t_calc_disc.balance = to_decimal(round(nett_amount + t_calc_disc.discount , price_decimal))

    return generate_output()