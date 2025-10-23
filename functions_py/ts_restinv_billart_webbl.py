#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 17-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import H_artikel, Bediener, Queasy, Htparam, H_menu, H_journal, Wgrpdep, Paramtext

t_request_list_data, T_request_list = create_model("T_request_list", {"billart":int, "curr_dept":int, "user_init":string})

def ts_restinv_billart_webbl(t_request_list_data:[T_request_list]):

    prepare_cache ([H_artikel, Queasy, Htparam, H_menu, H_journal, Paramtext])

    price = to_decimal("0.0")
    error_message = ""
    t_h_artikel_data = []
    perm:List[int] = create_empty_list(120,0)
    loopn:int = 0
    curr_qty_posted:int = 0
    bill_date:date = None
    h_artikel = bediener = queasy = htparam = h_menu = h_journal = wgrpdep = paramtext = None

    t_request_list = t_h_artikel = tp_bediener = h_artikel_buff = queasy_buff = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"happy_hours":bool, "t_h_menu_flag":int, "sub_menu_bezeich":string, "rec_id":int, "isincluded":bool, "max_soldout_qty":int, "soldout_flag":bool, "posted_qty":int, "sub_menu_qty":int})
    tp_bediener_data, Tp_bediener = create_model_like(Bediener)

    H_artikel_buff = create_buffer("H_artikel_buff",H_artikel)
    Queasy_buff = create_buffer("Queasy_buff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price, error_message, t_h_artikel_data, perm, loopn, curr_qty_posted, bill_date, h_artikel, bediener, queasy, htparam, h_menu, h_journal, wgrpdep, paramtext
        nonlocal h_artikel_buff, queasy_buff


        nonlocal t_request_list, t_h_artikel, tp_bediener, h_artikel_buff, queasy_buff
        nonlocal t_h_artikel_data, tp_bediener_data

        return {"price": price, "error_message": error_message, "t-h-artikel": t_h_artikel_data}

    def get_price():

        nonlocal price, error_message, t_h_artikel_data, perm, loopn, curr_qty_posted, bill_date, h_artikel, bediener, queasy, htparam, h_menu, h_journal, wgrpdep, paramtext
        nonlocal h_artikel_buff, queasy_buff


        nonlocal t_request_list, t_h_artikel, tp_bediener, h_artikel_buff, queasy_buff
        nonlocal t_h_artikel_data, tp_bediener_data

        i:int = 0
        n:int = 0
        j:int = 0
        tolerance:int = 0
        curr_min:int = 0
        price =  to_decimal(h_artikel.epreis1)

        if h_artikel.epreis2 == 0:

            return

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + t_request_list.curr_dept))]})

        if paramtext:
            tolerance = paramtext.sprachcode
            curr_min = to_int(substring(to_string(get_current_time_in_seconds(), "HH:MM:SS") , 3, 2))
            i = round((get_current_time_in_seconds() / 3600 - 0.5) , 0)

            if i <= 0:
                i = 24
            n = to_int(substring(paramtext.ptexte, i - 1, 1))

            if n == 2:
                price =  to_decimal(h_artikel.epreis2)

            elif tolerance > 0:

                if i == 1:
                    j = 24
                else:
                    j = i - 1

                if to_int(substring(paramtext.ptexte, j - 1, 1)) == 2 and curr_min <= tolerance:
                    price =  to_decimal(h_artikel.epreis2)


    t_request_list = query(t_request_list_data, first=True)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    bediener = get_cache (Bediener, {"userinit": [(eq, t_request_list.user_init)]})

    if bediener:
        tp_bediener = Tp_bediener()
        tp_bediener_data.append(tp_bediener)

        buffer_copy(bediener, tp_bediener)

    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == t_request_list.billart) & (H_artikel.departement == t_request_list.curr_dept) & (H_artikel.activeflag) & (H_artikel.artart == 0)).first()

    if h_artikel:
        t_h_artikel = T_h_artikel()
        t_h_artikel_data.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid
        t_h_artikel.t_h_menu_flag = 1

        get_price()

        if price == h_artikel.epreis2 and h_artikel.epreis1 != 0:
            t_h_artikel.happy_hours = True
        else:
            t_h_artikel.happy_hours = False

        queasy = get_cache (Queasy, {"key": [(eq, 361)],"number2": [(eq, h_artikel.departement)],"number1": [(eq, h_artikel.artnr)],"char1": [(eq, "fixed-sub-menu")],"number3": [(eq, h_artikel.betriebsnr)]})

        if queasy:
            t_h_artikel.isincluded = queasy.logi1


        else:
            t_h_artikel.isincluded = False

        h_menu_obj_list = {}
        h_menu = H_menu()
        h_artikel_buff = H_artikel()
        queasy = Queasy()
        for h_menu.artnr, h_menu.departement, h_menu._recid, h_artikel_buff.bezeich, h_artikel_buff.artnr, h_artikel_buff.departement, h_artikel_buff._recid, queasy.logi1, queasy.deci1, queasy._recid, queasy.logi2 in db_session.query(H_menu.artnr, H_menu.departement, H_menu._recid, H_artikel_buff.bezeich, H_artikel_buff.artnr, H_artikel_buff.departement, H_artikel_buff._recid, Queasy.logi1, Queasy.deci1, Queasy._recid, Queasy.logi2).join(H_artikel_buff,(H_artikel_buff.artnr == H_menu.artnr) & (H_artikel_buff.departement == H_menu.departement)).join(Queasy,(Queasy.key == 361) & (Queasy.number2 == H_menu.departement) & (Queasy.number3 == H_menu.nr) & (Queasy.number1 == H_menu.artnr) & (Queasy.char1 == ("Qty-Sub-Menu").lower())).filter(
                 (H_menu.nr == h_artikel.betriebsnr) & (H_menu.departement == h_artikel.departement)).order_by(H_menu._recid).all():
            if h_menu_obj_list.get(h_menu._recid):
                continue
            else:
                h_menu_obj_list[h_menu._recid] = True


            t_h_artikel = T_h_artikel()
            t_h_artikel_data.append(t_h_artikel)

            t_h_artikel.sub_menu_bezeich = h_artikel_buff.bezeich
            t_h_artikel.t_h_menu_flag = 2
            t_h_artikel.sub_menu_qty = to_int(queasy.deci1)
            t_h_artikel.artnr = h_menu.artnr
            t_h_artikel.departement = h_menu.departement

            queasy_buff = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artikel_buff.artnr)],"number3": [(eq, h_menu.departement)]})

            if queasy_buff:
                t_h_artikel.max_soldout_qty = to_int(queasy_buff.deci1)
                t_h_artikel.soldout_flag = queasy_buff.logi2

            if t_h_artikel.max_soldout_qty > 0:
                curr_qty_posted = 0

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.artnr == h_artikel_buff.artnr) & (H_journal.departement == h_artikel_buff.departement) & (H_journal.bill_datum == bill_date)).order_by(H_journal._recid).all():
                    curr_qty_posted = curr_qty_posted + h_journal.anzahl
                t_h_artikel.posted_qty = curr_qty_posted
            t_h_artikel.bezeich = None
            t_h_artikel.zwkum = None
            t_h_artikel.endkum = None
            t_h_artikel.epreis1 =  to_decimal(None)
            t_h_artikel.artart = None
            t_h_artikel.autosaldo = None
            t_h_artikel.bezaendern = None
            t_h_artikel.mwst_code = None
            t_h_artikel.prozent =  to_decimal(None)
            t_h_artikel.epreis2 =  to_decimal(None)
            t_h_artikel.lagernr = None
            t_h_artikel.abbuchung = None
            t_h_artikel.bondruckernr = None
            t_h_artikel.aenderwunsch = None
            t_h_artikel.artnrfront = None
            t_h_artikel.artnrlager = None
            t_h_artikel.artnrrezept = None
            t_h_artikel.gang = None
            t_h_artikel.service_code = None
            t_h_artikel.activeflag = None
            t_h_artikel.s_gueltig = None
            t_h_artikel.e_gueltig = None
            t_h_artikel.betriebsnr = None

        tp_bediener = query(tp_bediener_data, first=True)
        for loopn in range(1,length(tp_bediener.permissions)  + 1) :
            perm[loopn - 1] = to_int(substring(tp_bediener.permissions, loopn - 1, 1))

        wgrpdep = db_session.query(Wgrpdep).filter(
                 (Wgrpdep.zknr == t_h_artikel.zwkum) & (Wgrpdep.departement == t_h_artikel.departement) & (matches(Wgrpdep.bezeich,"*DISCOUNT*"))).first()

        if wgrpdep:

            if perm[78] < 2:
                error_message = "Sorry, No Access Right. Access Code = 79,2"

                return generate_output()

    return generate_output()