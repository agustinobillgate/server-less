#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_tada_post_menubl import prepare_tada_post_menubl
from functions.ts_hbline_get_pricebl import ts_hbline_get_pricebl
from functions.tada_update_billbl import tada_update_billbl
from functions.add_kitchprbl import add_kitchprbl
from models import H_artikel, H_bill, Kellner, Queasy, Bediener, Guest

menu_list_data, Menu_list = create_model("Menu_list", {"artnr":int, "description":string, "qty":int, "price":Decimal, "special_request":string})

def tada_dashboard_post_menubl(user_init:string, tablenumber:int, outletnumber:int, guestname:string, pax:int, orderid:int, menu_list_data:[Menu_list]):

    prepare_cache ([H_artikel, H_bill, Queasy, Guest])

    billnumber = 0
    returnmessage = ""
    guestnr:int = 0
    tischnr:int = 0
    record_id:int = 0
    language_code:int = 0
    curr_room:string = ""
    resnr:int = 0
    reslinnr:int = 0
    curr_dept:int = 0
    gname:string = ""
    amount:Decimal = to_decimal("0.0")
    mealcoupon_cntrl:bool = False
    must_print:bool = False
    zero_flag:bool = False
    multi_cash:bool = False
    cancel_exist:bool = False
    msg_str:string = ""
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    mi_ordertaker:bool = True
    price_decimal:int = 0
    curr_local:string = ""
    curr_foreign:string = ""
    double_currency:bool = False
    foreign_rate:bool = False
    exchg_rate:Decimal = 1
    b_title:string = ""
    deptname:string = ""
    p_223:bool = False
    curr_waiter:int = 0
    fl_code:int = 0
    pos1:int = 0
    pos2:int = 0
    cashless_flag:bool = False
    price:Decimal = to_decimal("0.0")
    add_zeit:int = 0
    bill_date:date = None
    cancel_flag:bool = False
    mwst:Decimal = to_decimal("0.0")
    mwst_foreign:Decimal = to_decimal("0.0")
    balance:Decimal = to_decimal("0.0")
    bcol:int = 0
    balance_foreign:Decimal = to_decimal("0.0")
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    p_88:bool = False
    closed:bool = False
    doit:bool = False
    error_str:string = ""
    active_flag:int = 1
    deptno:int = 0
    err:bool = False
    err1:bool = False
    fract:Decimal = 1
    vhp_itemnumber:int = 0
    strchar:string = ""
    tmp_menu_name:string = ""
    order_phone:string = ""
    order_name:string = ""
    order_email:string = ""
    curr_gastnr:int = 0
    h_artikel = h_bill = kellner = queasy = bediener = guest = None

    hbill = t_kellner = t_h_artikel = menu_list = t_h_bill = t_submenu_list = kellner1 = crd_list = mn_list = orderhdr = orderline = bguest = None

    hbill_data, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_data, T_kellner = create_model("T_kellner", {"kellner_nr":int})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_submenu_list_data, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    kellner1_data, Kellner1 = create_model_like(Kellner)
    crd_list_data, Crd_list = create_model("Crd_list", {"deptno":int, "uname":string, "pass":string, "tada_outlet_id":int})

    Mn_list = Menu_list
    mn_list_data = menu_list_data

    Orderhdr = create_buffer("Orderhdr",Queasy)
    Orderline = create_buffer("Orderline",Queasy)
    Bguest = create_buffer("Bguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billnumber, returnmessage, guestnr, tischnr, record_id, language_code, curr_room, resnr, reslinnr, curr_dept, gname, amount, mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, price, add_zeit, bill_date, cancel_flag, mwst, mwst_foreign, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, doit, error_str, active_flag, deptno, err, err1, fract, vhp_itemnumber, strchar, tmp_menu_name, order_phone, order_name, order_email, curr_gastnr, h_artikel, h_bill, kellner, queasy, bediener, guest
        nonlocal user_init, tablenumber, outletnumber, guestname, pax, orderid
        nonlocal mn_list, orderhdr, orderline, bguest


        nonlocal hbill, t_kellner, t_h_artikel, menu_list, t_h_bill, t_submenu_list, kellner1, crd_list, mn_list, orderhdr, orderline, bguest
        nonlocal hbill_data, t_kellner_data, t_h_artikel_data, t_h_bill_data, t_submenu_list_data, kellner1_data, crd_list_data

        return {"billnumber": billnumber, "returnmessage": returnmessage}

    returnmessage = ""
    tischnr = tablenumber
    curr_dept = outletnumber
    gname = guestname

    if (tischnr == 0 or tischnr == None):
        returnmessage = "You must enter a table number before proceeding"

        return generate_output()

    if (curr_dept == 0 or curr_dept == None):
        returnmessage = "Please enter an outlet number"

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1)).order_by(Queasy.betriebsnr, Queasy.number2).all():

        if (queasy.number2 == 27 or queasy.number2 == 28 or queasy.number2 == 29 or queasy.number2 == 30):

            if num_entries(queasy.char2, ";") >= 2:
                crd_list = Crd_list()
                crd_list_data.append(crd_list)

                crd_list.deptno = to_int(entry(0, queasy.char2, ";"))
                crd_list.uname = entry(1, queasy.char2, ";")
                crd_list.pass = entry(2, queasy.char2, ";")
                crd_list.tada_outlet_id = to_int(entry(3, queasy.char2, ";"))

    crd_list = query(crd_list_data, filters=(lambda crd_list: crd_list.deptno == curr_dept), first=True)

    if crd_list:
        deptno = crd_list.tada_outlet_id
    mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_data, t_kellner_data = get_output(prepare_tada_post_menubl(language_code, curr_dept, 0, user_init, None))

    t_kellner = query(t_kellner_data, first=True)

    h_bill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"flag": [(eq, 0)],"tischnr": [(eq, tischnr)]})

    if h_bill:
        record_id = h_bill._recid
    else:
        record_id = 0

    for orderline in db_session.query(Orderline).filter(
             (Orderline.key == 271) & (Orderline.betriebsnr == 2) & (Orderline.number2 == orderid) & (Orderline.logi1 == False)).order_by(Orderline._recid).all():

        mn_list = query(mn_list_data, filters=(lambda mn_list: mn_list.artnr == orderline.number1), first=True)

        if not mn_list:
            tmp_menu_name = entry(1, orderline.char1, "|")

            if matches(tmp_menu_name,r"*DISC*"):
                menu_list = Menu_list()
                menu_list_data.append(menu_list)

                menu_list.artnr = orderline.number1
                menu_list.description = tmp_menu_name
                menu_list.qty = to_int(entry(0, orderline.char1, "|"))
                menu_list.price =  to_decimal(to_decimal(entry(3 , orderline.char1 , "|")) )
                menu_list.special_request = ""

    for menu_list in query(menu_list_data):

        if not matches(menu_list.DESCRIPTION,r"*DISC*"):

            queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 2)],"betriebsnr": [(eq, curr_dept)],"number2": [(eq, menu_list.artnr)]})

            if not queasy:
                returnmessage = "Posting is not possible because the article has not been mapped yet."

                return generate_output()

    for menu_list in query(menu_list_data):
        vhp_itemnumber = 0

        if not matches(menu_list.DESCRIPTION,r"*DISC*"):

            queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 2)],"betriebsnr": [(eq, curr_dept)],"number2": [(eq, menu_list.artnr)]})

            if queasy:
                vhp_itemnumber = queasy.number3
            else:
                returnmessage = "Posting is not possible because the article has not been mapped yet."

                return generate_output()
        else:
            vhp_itemnumber = menu_list.artnr
            menu_list.price =  - to_decimal(menu_list.price)
        add_zeit = add_zeit + 1

        h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, vhp_itemnumber)]})

        if not h_artikel:
            returnmessage = "Posting is not possible because the article has not been mapped yet."

            return generate_output()

        if record_id == 0:

            t_h_bill = query(t_h_bill_data, first=True)

            if t_h_bill:
                record_id = t_h_bill.rec_id

        if h_artikel.epreis1 != 0:
            err, err1, price, fract = get_output(ts_hbline_get_pricebl(h_artikel.artnr, curr_dept))
        else:
            price =  to_decimal(menu_list.price)
        amount =  to_decimal(price) * to_decimal(menu_list.qty)
        bill_date, cancel_flag, fl_code, mwst, mwst_foreign, billnumber, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, kellner1_data = get_output(tada_update_billbl(language_code, record_id, h_artikel._recid, "", None, h_artikel.artart, False, h_artikel.service_code, amount, 0, price, double_currency, menu_list.qty, exchg_rate, price_decimal, user_init, tischnr, curr_dept, user_init, gname, pax, 0, add_zeit, h_artikel.artnr, menu_list.DESCRIPTION, "", "", "", menu_list.special_request, "", "", True, False, h_artikel.artnrfront, 0, guestnr, "", False, foreign_rate, curr_room, user_init, resnr, reslinnr, t_submenu_list_data))

        t_h_bill = query(t_h_bill_data, first=True)

        if t_h_bill:
            billnumber = t_h_bill.rechnr
        doit = True

    if doit :

        bediener = get_cache (Bediener, {"userinit": [(eq, trim(user_init))]})
        returnmessage = "Post Menu Success"

        orderhdr = get_cache (Queasy, {"key": [(eq, 271)],"betriebsnr": [(eq, 1)],"number1": [(eq, deptno)],"number2": [(eq, orderid)]})

        if orderhdr:
            strchar = orderhdr.char2
            pass
            orderhdr.logi1 = True
            orderhdr.number3 = billnumber
            orderhdr.char2 = entry(0, strchar, "|") + "|" + to_string(tablenumber) + "|" + entry(2, strchar, "|") + "|" + entry(3, strchar, "|") + "|" + entry(4, strchar, "|") + "|" + entry(5, strchar, "|")


            order_phone = entry(5, strchar, "|")
            order_name = entry(2, strchar, "|")
            order_email = entry(4, strchar, "|")
            pass
            pass

        for menu_list in query(menu_list_data):

            orderline = get_cache (Queasy, {"key": [(eq, 271)],"betriebsnr": [(eq, 2)],"number2": [(eq, orderid)],"number1": [(eq, menu_list.artnr)]})

            if orderline:
                pass
                orderline.logi1 = True
                orderline.number3 = billnumber


                pass
                pass

        guest = get_cache (Guest, {"mobil_telefon": [(eq, order_phone)],"karteityp": [(eq, 0)]})

        if not guest:

            guest = get_cache (Guest, {"telefon": [(eq, order_phone)],"karteityp": [(eq, 0)]})

            if not guest:

                for bguest in db_session.query(Bguest).order_by(Bguest.gastnr.desc()).yield_per(100):
                    curr_gastnr = bguest.gastnr
                    break

                if curr_gastnr == 0:
                    curr_gastnr = 1
                else:
                    curr_gastnr = curr_gastnr + 1
                guest = Guest()
                db_session.add(guest)

                guest.karteityp = 0
                guest.name = order_name
                guest.email_adr = order_email
                guest.telefon = order_phone
                guest.mobil_telefon = order_phone
                guest.gastnr = curr_gastnr
                gastnr = curr_gastnr
            else:
                guest.name = order_name
                guest.email_adr = order_email
                guest.telefon = order_phone
                guest.mobil_telefon = order_phone
        else:
            guest.name = order_name
            guest.email_adr = order_email
            guest.telefon = order_phone
            guest.mobil_telefon = order_phone
        pass
    error_str = get_output(add_kitchprbl(language_code, "", curr_dept, billnumber, bill_date, user_init))

    return generate_output()