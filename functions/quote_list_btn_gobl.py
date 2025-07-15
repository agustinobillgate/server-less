#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_quote

t_quote_data, T_quote = create_model("T_quote", {"artnr":int, "lief_nr":int, "supname":string, "artname":string, "devunit":string, "content":Decimal, "unitprice":Decimal, "curr":string, "from_date":date, "to_date":date, "remark":string, "filname":string, "activeflag":bool, "docu_nr":string, "minqty":Decimal, "delivday":int, "disc":Decimal, "avl":bool}, {"activeflag": True, "avl": True})
t_quote1_data, T_quote1 = create_model_like(T_quote)

def quote_list_btn_gobl(pvilanguage:int, curr_type:string, user_init:string, t_quote_data:[T_quote], t_quote1_data:[T_quote1]):

    prepare_cache ([L_quote])

    msg_str = ""
    lvcarea:string = "quote-list"
    l_quote = None

    t_quote = t_quote1 = b_lquote = None

    B_lquote = create_buffer("B_lquote",L_quote)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, l_quote
        nonlocal pvilanguage, curr_type, user_init, t_quote1_data
        nonlocal b_lquote


        nonlocal t_quote, t_quote1, b_lquote

        return {"msg_str": msg_str}


    t_quote = query(t_quote_data, first=True)

    if curr_type.lower()  == ("new").lower() :

        l_quote = get_cache (L_quote, {"artnr": [(eq, t_quote.artnr)],"lief_nr": [(eq, t_quote.lief_nr)],"docu_nr": [(eq, t_quote.docu_nr)],"from_date": [(eq, t_quote.from_date)],"to_date": [(eq, t_quote.to_date)]})

        if l_quote and l_quote.reserve_int[4] <= 1:
            msg_str = translateExtended ("Article already exist for the same Supplier, same DocuNo and same periode.", lvcarea, "")
        l_quote = L_quote()
        db_session.add(l_quote)

        buffer_copy(t_quote, l_quote)
        l_quote.createid = user_init
        l_quote.createdate = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()))
        l_quote.createtime = get_current_time_in_seconds()
        l_quote.reserve_char[0] = t_quote.curr
        l_quote.reserve_deci[0] = t_quote.minqty
        l_quote.reserve_deci[1] = t_quote.disc
        l_quote.reserve_logic[0] = not t_quote.avl
        l_quote.reserve_int[0] = t_quote.delivDay

        if t_quote.activeflag :
            l_quote.reserve_int[4] = 1
        else:
            l_quote.reserve_int[4] = 0
        pass

    elif curr_type.lower()  == ("chg").lower() :

        t_quote1 = query(t_quote1_data, first=True)

        l_quote = get_cache (L_quote, {"artnr": [(eq, t_quote1.artnr)],"lief_nr": [(eq, t_quote1.lief_nr)],"docu_nr": [(eq, t_quote1.docu_nr)],"from_date": [(eq, t_quote1.from_date)],"to_date": [(eq, t_quote1.to_date)],"unitprice": [(eq, t_quote1.unitprice)],"reserve_char[0]": [(eq, t_quote1.curr)],"remark": [(eq, t_quote1.remark)],"filname": [(eq, t_quote1.filname)],"activeflag": [(eq, t_quote1.activeflag)]})

        if l_quote:

            if (l_quote.from_date != t_quote.from_date and l_quote.to_date != t_quote.to_date) or l_quote.docu_nr != t_quote.docu_nr:

                b_lquote = db_session.query(B_lquote).filter(
                         (B_lquote.artnr == t_quote.artnr) & (B_lquote.lief_nr == t_quote.lief_nr) & (B_lquote.docu_nr == t_quote.docu_nr) & (B_lquote.from_date == t_quote.from_date) & (B_lquote.to_date == t_quote.to_date) & (B_lquote.activeflag)).first()

                if b_lquote and b_lquote.reserve_int[4] <= 1:
                    msg_str = translateExtended ("Article already exist for the same Supplier, same DocuNo and same periode.", lvcarea, "")
            pass
            buffer_copy(t_quote, l_quote)
            l_quote.chgid = user_init
            l_quote.chgdate = date_mdy(get_month(get_current_date()) , get_day(get_current_date()) , get_year(get_current_date()))
            l_quote.chgtime = get_current_time_in_seconds()
            l_quote.reserve_char[0] = t_quote.curr
            l_quote.reserve_deci[0] = t_quote.minqty
            l_quote.reserve_deci[1] = t_quote.disc
            l_quote.reserve_logic[0] = not t_quote.avl
            l_quote.reserve_int[0] = t_quote.delivDay

            if t_quote.activeflag :
                l_quote.reserve_int[4] = 1
            else:
                l_quote.reserve_int[4] = 0
            pass

    elif curr_type.lower()  == ("del").lower() :

        l_quote = get_cache (L_quote, {"artnr": [(eq, t_quote.artnr)],"lief_nr": [(eq, t_quote.lief_nr)],"from_date": [(eq, t_quote.from_date)],"to_date": [(eq, t_quote.to_date)]})

        if l_quote:
            pass
            db_session.delete(l_quote)
            pass

    return generate_output()