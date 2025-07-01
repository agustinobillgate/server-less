#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Kellner, Htparam, Waehrung, Artikel, H_artikel

def prepare_rest_daysalesp1bl():

    prepare_cache ([Htparam, Waehrung, Artikel, H_artikel])

    disc_art1 = -1
    disc_art2 = -1
    disc_art3 = -1
    exchg_rate = to_decimal("0.0")
    curr_local = ""
    curr_foreign = ""
    serv_taxable = False
    dpt_str = ""
    art_str = ""
    oth_str = ""
    anzahl = 0
    curr_dept = 0
    dept_name = ""
    voucher_art = 0
    use_voucher = True
    from_date = None
    to_date = None
    htl_dept_dptnr = 0
    err_flag = 0
    p_110 = None
    p_240 = False
    buf_art_list = []
    htl_dept_list = []
    usr1_list = []
    f_cash:bool = False
    i:int = 0
    str_tmp:string = ""
    artnr_list:List[int] = create_empty_list(21,0)
    show_option:bool = False
    hoteldpt = kellner = htparam = waehrung = artikel = h_artikel = None

    htl_dept = t_hoteldpt = buf_art = usr1 = None

    htl_dept_list, Htl_dept = create_model("Htl_dept", {"dptnr":int, "bezeich":string})
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    buf_art_list, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":string, "departement":int})
    usr1_list, Usr1 = create_model_like(Kellner, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal disc_art1, disc_art2, disc_art3, exchg_rate, curr_local, curr_foreign, serv_taxable, dpt_str, art_str, oth_str, anzahl, curr_dept, dept_name, voucher_art, use_voucher, from_date, to_date, htl_dept_dptnr, err_flag, p_110, p_240, buf_art_list, htl_dept_list, usr1_list, f_cash, i, str_tmp, artnr_list, show_option, hoteldpt, kellner, htparam, waehrung, artikel, h_artikel


        nonlocal htl_dept, t_hoteldpt, buf_art, usr1
        nonlocal htl_dept_list, t_hoteldpt_list, buf_art_list, usr1_list

        return {"disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "serv_taxable": serv_taxable, "dpt_str": dpt_str, "art_str": art_str, "oth_str": oth_str, "anzahl": anzahl, "curr_dept": curr_dept, "dept_name": dept_name, "voucher_art": voucher_art, "use_voucher": use_voucher, "from_date": from_date, "to_date": to_date, "htl_dept_dptnr": htl_dept_dptnr, "err_flag": err_flag, "p_110": p_110, "p_240": p_240, "buf-art": buf_art_list, "htl-dept": htl_dept_list, "usr1": usr1_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam.finteger > 0:
        disc_art3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam.finteger > 0:
        disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam.finteger > 0:
        disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

    if htparam.flogical:
        serv_taxable = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 716)]})

    if htparam.fchar != "":
        for i in range(1,num_entries(htparam.fchar, ";")  + 1) :
            str_tmp = entry(i - 1, htparam.fchar, ";")

            if substring(str_tmp, 0, 1) == "D":
                dpt_str = substring(str_tmp, 1, (length(str_tmp) - 1))
            elif substring(str_tmp, 0, 1) == "A":
                art_str = substring(str_tmp, 1, (length(str_tmp) - 1))
            elif substring(str_tmp, 0, 1) == "G":
                oth_str = substring(str_tmp, 1, (length(str_tmp) - 1))
    else:
        err_flag = 1

        return generate_output()

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)
    for i in range(1,num_entries(art_str, ",")  + 1) :

        if i > 21:
            pass
        else:
            artnr_list[i - 1] = to_int(entry(i - 1, art_str, ","))

            if artnr_list[i - 1] == disc_art2 or artnr_list[i - 1] == disc_art3:
                show_option = True
            anzahl = anzahl + 1
    for i in range(1,num_entries(dpt_str, ",")  + 1) :

        if to_int(entry(i - 1, dpt_str, ",")) != 0:

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_int(entry(i - 1, dpt_str, ",")))]})

            if hoteldpt:
                htl_dept = Htl_dept()
                htl_dept_list.append(htl_dept)

                htl_dept.dptnr = hoteldpt.num
                htl_dept.bezeich = hoteldpt.depart

    htl_dept = query(htl_dept_list, first=True)

    if not htl_dept:
        err_flag = 2

        return generate_output()
    curr_dept = htl_dept.dptnr
    dept_name = htl_dept.bezeich


    htl_dept_dptnr = htl_dept.dptnr
    for i in range(1,anzahl + 1) :

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr == artnr_list[i - 1])).order_by(Artikel._recid).all():
            buf_art = Buf_art()
            buf_art_list.append(buf_art)

            buf_art.artnr = artikel.artnr
            buf_art.bezeich = artikel.bezeich
            buf_art.departement = artikel.departement

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})

    if htparam.finteger > 0:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"artart": [(eq, 6)]})

        if h_artikel:
            voucher_art = h_artikel.artnr

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            artikel = Artikel()
            for h_artikel.artnr, h_artikel._recid, artikel.artnr, artikel.bezeich, artikel.departement, artikel._recid in db_session.query(H_artikel.artnr, H_artikel._recid, Artikel.artnr, Artikel.bezeich, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == 0) & (Artikel.pricetab)).filter(
                     (H_artikel.artart == 6)).order_by(H_artikel._recid).all():
                if h_artikel_obj_list.get(h_artikel._recid):
                    continue
                else:
                    h_artikel_obj_list[h_artikel._recid] = True


                f_cash = True
                use_voucher = False


                break

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    to_date = from_date

    for kellner in db_session.query(Kellner).order_by(Kellner._recid).all():
        usr1 = Usr1()
        usr1_list.append(usr1)

        buffer_copy(kellner, usr1)
        usr1.rec_id = kellner._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    p_110 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    p_240 = htparam.flogical

    return generate_output()