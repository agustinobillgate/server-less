from functions.additional_functions import *
import decimal
from models import L_quote

def quote_list_btn_gobl(pvilanguage:int, curr_type:str, user_init:str, t_quote:[T_quote], t_quote1:[T_quote1]):
    msg_str = ""
    lvcarea:str = "quote_list"
    l_quote = None

    t_quote = t_quote1 = b_lquote = None

    t_quote_list, T_quote = create_model("T_quote", {"artnr":int, "lief_nr":int, "supname":str, "artname":str, "devunit":str, "content":decimal, "unitprice":decimal, "curr":str, "from_date":date, "to_date":date, "remark":str, "filname":str, "activeflag":bool, "docu_nr":str, "minqty":decimal, "delivday":int, "disc":decimal, "avl":bool}, {"activeflag": True, "avl": True})
    t_quote1_list, T_quote1 = create_model_like(T_quote)

    B_lquote = L_quote

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, l_quote
        nonlocal b_lquote


        nonlocal t_quote, t_quote1, b_lquote
        nonlocal t_quote_list, t_quote1_list
        return {"msg_str": msg_str}


    t_quote = query(t_quote_list, first=True)

    if curr_type.lower()  == "new":

        l_quote = db_session.query(L_quote).filter(
                (L_quote.artnr == t_quote.artnr) &  (L_quote.lief_nr == t_quote.lief_nr) &  (L_quote.docu_nr == t_quote.docu_nr) &  (L_quote.from_date == t_quote.from_date) &  (L_quote.to_date == t_quote.to_date)).first()

        if l_quote and l_quote.reserve_int[4] <= 1:
            msg_str = translateExtended ("Article already exist for the same Supplier, same DocuNo and same periode.", lvcarea, "")
        l_quote = L_quote()
        db_session.add(l_quote)

        buffer_copy(t_quote, l_quote)
        l_quote.createID = user_init
        l_quote.createDate = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()))
        l_quote.createTime = get_current_time_in_seconds()
        l_quote.reserve_char[0] = t_quote.curr
        l_quote.reserve_deci[0] = t_quote.minqty
        l_quote.reserve_deci[1] = t_quote.disc
        l_quote.reserve_logic[0] = not t_quote.avl
        l_quote.reserve_int[0] = t_quote.delivDay

        if t_quote.activeFlag :
            l_quote.reserve_int[4] = 1
        else:
            l_quote.reserve_int[4] = 0


    elif curr_type.lower()  == "chg":

        t_quote1 = query(t_quote1_list, first=True)

        l_quote = db_session.query(L_quote).filter(
                (L_quote.artnr == t_quote1.artnr) &  (L_quote.lief_nr == t_quote1.lief_nr) &  (L_quote.docu_nr == t_quote1.docu_nr) &  (L_quote.from_date == t_quote1.from_date) &  (L_quote.to_date == t_quote1.to_date) &  (L_quote.unitprice == t_quote1.unitprice) &  (L_quote.reserve_char[0] == t_quote1.curr) &  (L_quote.remark == t_quote1.remark) &  (L_quote.filname == t_quote1.filname) &  (L_quote.activeflag == t_quote1.activeflag)).first()

        if l_quote:

            if (l_quote.from_date != t_quote.from_date and l_quote.to_date != t_quote.to_date) or l_quote.docu_nr != t_quote.docu_nr:

                b_lquote = db_session.query(B_lquote).filter(
                        (B_lquote.artnr == t_quote.artnr) &  (B_lquote.lief_nr == t_quote.lief_nr) &  (B_lquote.docu_nr == t_quote.docu_nr) &  (B_lquote.from_date == t_quote.from_date) &  (B_lquote.to_date == t_quote.to_date) &  (B_lquote.activeflag)).first()

                if b_lquote and b_lquote.reserve_int[4] <= 1:
                    msg_str = translateExtended ("Article already exist for the same Supplier, same DocuNo and same periode.", lvcarea, "")

            l_quote = db_session.query(L_quote).first()
            buffer_copy(t_quote, l_quote)
            l_quote.chgID = user_init
            l_quote.chgDate = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()))
            l_quote.chgTime = get_current_time_in_seconds()
            l_quote.reserve_char[0] = t_quote.curr
            l_quote.reserve_deci[0] = t_quote.minqty
            l_quote.reserve_deci[1] = t_quote.disc
            l_quote.reserve_logic[0] = not t_quote.avl
            l_quote.reserve_int[0] = t_quote.delivDay

            if t_quote.activeFlag :
                l_quote.reserve_int[4] = 1
            else:
                l_quote.reserve_int[4] = 0

            l_quote = db_session.query(L_quote).first()

    elif curr_type.lower()  == "del":

        l_quote = db_session.query(L_quote).filter(
                (L_quote.artnr == t_quote.artnr) &  (L_quote.lief_nr == t_quote.lief_nr) &  (L_quote.from_date == t_quote.from_date) &  (L_quote.to_date == t_quote.to_date)).first()

        if l_quote:

            l_quote = db_session.query(L_quote).first()
            l_quote.chgID = user_init
            l_quote.chgDate = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()))
            l_quote.chgTime = get_current_time_in_seconds()
            l_quote.reserve_int[4] = 2

            l_quote = db_session.query(L_quote).first()

    return generate_output()