#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from functions.del_reslinebl import del_reslinebl
from functions.if_vhp_bookeng_store_resbl import if_vhp_bookeng_store_resbl
from functions.if_vhp_modify_reslinebl import if_vhp_modify_reslinebl
from models import Res_line, Queasy, Guest, Reservation, Zimkateg

res_info_data, Res_info = create_model("Res_info", {"res_time":string, "res_id":string, "ota_code":string, "commission":string, "curr":string, "adult":string, "child1":string, "child2":string, "remark":string, "eta":string, "given_name":string, "sure_name":string, "phone":string, "email":string, "address1":string, "address2":string, "city":string, "zip":string, "state":string, "country":string, "uniq_id":string, "res_status":string, "deposit":Decimal, "membership":string, "card_info":string, "gastnrmember":int})
room_list_data, Room_list = create_model("Room_list", {"reslinnr":int, "res_id":string, "ci_date":string, "co_date":string, "amount":string, "room_type":string, "rate_code":string, "number":int, "adult":int, "child1":int, "child2":int, "service":string, "gastnr":string, "comment":string, "argtnr":string, "ankunft":date, "abreise":date, "zikatnr":int})
service_list_data, Service_list = create_model("Service_list", {"ci_date":string, "co_date":string, "res_id":string, "amountaftertax":Decimal, "amountbeforetax":Decimal, "tamountaftertax":Decimal, "tamountbeforetax":Decimal, "bezeich":string, "rph":string, "id":string, "curr":string, "qty":int})
guest_list_data, Guest_list = create_model("Guest_list", {"res_id":string, "given_name":string, "sure_name":string, "phone":string, "email":string, "address1":string, "address2":string, "city":string, "zip":string, "state":string, "country":string, "gastnr":string, "gastnrmember":int})

def if_vhp_bookeng_modifybl(res_info_data:[Res_info], room_list_data:[Room_list], service_list_data:[Service_list], guest_list_data:[Guest_list], becode:int, t_guest_nat:string, t_curr_name:string, dyna_code:string, chdelimeter:string, chdelimeter1:string, chdelimeter2:string, chdelimeter3:string):

    prepare_cache ([Queasy, Guest, Reservation, Zimkateg])

    error_str = ""
    done = False
    cm_gastno:int = 0
    ota_gastnr:int = 0
    check_integer:int = 0
    asc_str:string = ""
    j:int = 0
    i:int = 0
    k:int = 0
    cat_flag:bool = False
    counter:int = 0
    gastnrmember:int = 1
    rsegm:int = 0
    avalue:string = ""
    del_mainres:bool = False
    cancel_msg:string = ""
    curr_resnr:int = 0
    curr_reslinnr:int = 0
    m:int = 0
    yy:int = 0
    dd:int = 0
    date_str:string = ""
    bill_date:date = None
    upto_date:date = None
    zikatnr:int = 0
    iftask:string = ""
    rline_origcode:string = ""
    commission_str:string = ""
    commission_dec:Decimal = to_decimal("0.0")
    dcommission:bool = False
    markup_str:string = ""
    markup_dec:Decimal = to_decimal("0.0")
    artnr_comm:int = 0
    loop_i:int = 0
    firstname:string = ""
    lastname:string = ""
    res_line = queasy = guest = reservation = zimkateg = None

    res_info = guest_list = service_list = room_list = detres = tb_detres = room_list1 = t_resline = qsy = rqueasy = bqueasy = rgast = bres = None

    detres_data, Detres = create_model("Detres", {"reslinnr":int, "res_id":string, "ci_date":string, "co_date":string, "amount":string, "room_type":string, "rate_code":string, "number":int, "adult":int, "child1":int, "child2":int, "service":string, "gastnr":string, "comment":string, "argtnr":string, "ankunft":date, "abreise":date, "zikatnr":int, "firstname":string, "lastname":string, "selected":bool})
    tb_detres_data, Tb_detres = create_model_like(Detres)
    room_list1_data, Room_list1 = create_model_like(Room_list)
    t_resline_data, T_resline = create_model_like(Res_line, {"firstname":string, "lastname":string, "uniq_id":string, "typ":int, "flag":bool, "selected":bool})

    Qsy = create_buffer("Qsy",Queasy)
    Rqueasy = create_buffer("Rqueasy",Queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Rgast = create_buffer("Rgast",Guest)
    Bres = create_buffer("Bres",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, done, cm_gastno, ota_gastnr, check_integer, asc_str, j, i, k, cat_flag, counter, gastnrmember, rsegm, avalue, del_mainres, cancel_msg, curr_resnr, curr_reslinnr, m, yy, dd, date_str, bill_date, upto_date, zikatnr, iftask, rline_origcode, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, loop_i, firstname, lastname, res_line, queasy, guest, reservation, zimkateg
        nonlocal becode, t_guest_nat, t_curr_name, dyna_code, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3
        nonlocal qsy, rqueasy, bqueasy, rgast, bres


        nonlocal res_info, guest_list, service_list, room_list, detres, tb_detres, room_list1, t_resline, qsy, rqueasy, bqueasy, rgast, bres
        nonlocal detres_data, tb_detres_data, room_list1_data, t_resline_data

        return {"error_str": error_str, "done": done}

    def modify_res(curr_resnr:int, curr_reslinnr:int):

        nonlocal error_str, done, cm_gastno, ota_gastnr, check_integer, asc_str, j, i, k, cat_flag, counter, gastnrmember, rsegm, avalue, del_mainres, cancel_msg, m, yy, dd, date_str, bill_date, upto_date, zikatnr, iftask, rline_origcode, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, loop_i, firstname, lastname, res_line, queasy, guest, reservation, zimkateg
        nonlocal becode, t_guest_nat, t_curr_name, dyna_code, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3
        nonlocal qsy, rqueasy, bqueasy, rgast, bres


        nonlocal res_info, guest_list, service_list, room_list, detres, tb_detres, room_list1, t_resline, qsy, rqueasy, bqueasy, rgast, bres
        nonlocal detres_data, tb_detres_data, room_list1_data, t_resline_data

        curr_i:int = 0
        accompany1:string = ""
        accompany2:string = ""
        accompany3:string = ""
        get_output(if_vhp_modify_reslinebl(curr_resnr, curr_reslinnr, t_curr_name, dyna_code, accompany1, accompany2, accompany3, tb_detRes_data, res_info_data, service_list_data, dcommission, commission_dec, artnr_comm))


    def chk_ascii(str1:string):

        nonlocal error_str, done, cm_gastno, ota_gastnr, check_integer, asc_str, j, i, k, cat_flag, counter, gastnrmember, rsegm, avalue, del_mainres, cancel_msg, curr_resnr, curr_reslinnr, m, yy, dd, date_str, bill_date, upto_date, zikatnr, iftask, rline_origcode, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, loop_i, firstname, lastname, res_line, queasy, guest, reservation, zimkateg
        nonlocal becode, t_guest_nat, t_curr_name, dyna_code, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3
        nonlocal qsy, rqueasy, bqueasy, rgast, bres


        nonlocal res_info, guest_list, service_list, room_list, detres, tb_detres, room_list1, t_resline, qsy, rqueasy, bqueasy, rgast, bres
        nonlocal detres_data, tb_detres_data, room_list1_data, t_resline_data

        str2 = ""
        curr_i:int = 0

        def generate_inner_output():
            return (str2)

        str2 = ""
        for curr_i in range(1,length(str1)  + 1) :

            if asc(substring(str1, curr_i - 1, 1)) == 10:
                str2 = str2 + "-"

            elif asc(substring(str1, curr_i - 1, 1)) < 32:
                str2 = str2 + "-"

            elif asc(substring(str1, curr_i - 1, 1)) == 192 or asc(substring(str1, curr_i, 1)) == 193 or asc(substring(str1, curr_i, 1)) == 194 or asc(substring(str1, curr_i, 1)) == 195 or asc(substring(str1, curr_i, 1)) == 196 or asc(substring(str1, curr_i, 1)) == 197:
                str2 = str2 + "A"

            elif asc(substring(str1, curr_i - 1, 1)) == 224 or asc(substring(str1, curr_i, 1)) == 225 or asc(substring(str1, curr_i, 1)) == 226 or asc(substring(str1, curr_i, 1)) == 227 or asc(substring(str1, curr_i, 1)) == 228 or asc(substring(str1, curr_i, 1)) == 229:
                str2 = str2 + "a"

            elif asc(substring(str1, curr_i - 1, 1)) == 200 or asc(substring(str1, curr_i, 1)) == 201 or asc(substring(str1, curr_i, 1)) == 202 or asc(substring(str1, curr_i, 1)) == 203:
                str2 = str2 + "E"

            elif asc(substring(str1, curr_i - 1, 1)) == 232 or asc(substring(str1, curr_i, 1)) == 233 or asc(substring(str1, curr_i, 1)) == 234 or asc(substring(str1, curr_i, 1)) == 235:
                str2 = str2 + "e"

            elif asc(substring(str1, curr_i - 1, 1)) == 204 or asc(substring(str1, curr_i, 1)) == 205 or asc(substring(str1, curr_i, 1)) == 206 or asc(substring(str1, curr_i, 1)) == 207:
                str2 = str2 + "i"

            elif asc(substring(str1, curr_i - 1, 1)) == 236 or asc(substring(str1, curr_i, 1)) == 237 or asc(substring(str1, curr_i, 1)) == 238 or asc(substring(str1, curr_i, 1)) == 239:
                str2 = str2 + "i"

            elif asc(substring(str1, curr_i - 1, 1)) == 210 or asc(substring(str1, curr_i, 1)) == 211 or asc(substring(str1, curr_i, 1)) == 212 or asc(substring(str1, curr_i, 1)) == 213 or asc(substring(str1, curr_i, 1)) == 214:
                str2 = str2 + "O"

            elif asc(substring(str1, curr_i - 1, 1)) == 242 or asc(substring(str1, curr_i, 1)) == 243 or asc(substring(str1, curr_i, 1)) == 244 or asc(substring(str1, curr_i, 1)) == 245 or asc(substring(str1, curr_i, 1)) == 246:
                str2 = str2 + "o"

            elif asc(substring(str1, curr_i - 1, 1)) == 217 or asc(substring(str1, curr_i, 1)) == 218 or asc(substring(str1, curr_i, 1)) == 219 or asc(substring(str1, curr_i, 1)) == 220:
                str2 = str2 + "U"

            elif asc(substring(str1, curr_i - 1, 1)) == 249 or asc(substring(str1, curr_i, 1)) == 250 or asc(substring(str1, curr_i, 1)) == 251 or asc(substring(str1, curr_i, 1)) == 252:
                str2 = str2 + "u"

            elif asc(substring(str1, curr_i - 1, 1)) == 209:
                str2 = str2 + "N"

            elif asc(substring(str1, curr_i - 1, 1)) == 241:
                str2 = str2 + "n"

            elif asc(substring(str1, curr_i - 1, 1)) == 160:
                str2 = str2 + " "

            elif asc(substring(str1, curr_i - 1, 1)) > 127 or asc(substring(str1, curr_i, 1)) < 32:
                str2 = str2 + "-"
            else:
                str2 = str2 + substring(str1, curr_i - 1, 1)

        return generate_inner_output()


    t_resline_data.clear()
    detRes_data.clear()
    tb_detRes_data.clear()

    res_info = query(res_info_data, first=True)

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

    if queasy:
        cm_gastno = queasy.number2

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if res_info.ota_code != "":

        rgast = db_session.query(Rgast).filter(
                 (Rgast.karteityp > 0) & (matches(trim(entry(0, Rgast.steuernr, "|")),trim(res_info.ota_code)))).first()

        if not rgast:

            rgast = get_cache (Guest, {"gastnr": [(eq, cm_gastno)]})

            if rgast:
                ota_gastnr = rgast.gastnr
            else:
                error_str = "GuestNo " + to_string(cm_gastno) + " not found"

                return generate_output()
        else:
            ota_gastnr = rgast.gastnr
    else:
        ota_gastnr = cm_gastno

    guest = get_cache (Guest, {"gastnr": [(eq, ota_gastnr)]})

    if guest:

        if num_entries(guest.steuernr, "|") > 5:

            if entry(1, guest.steuernr, "|") != "" or entry(1, guest.steuernr, "|") != None:
                commission_str = entry(1, guest.steuernr, "|")
                commission_str = replace_str(commission_str, "-", "")
                commission_str = replace_str(commission_str, "%", "")
                commission_str = replace_str(commission_str, ",", ".")
                commission_dec =  to_decimal(to_decimal(commission_str) )

            if entry(6, guest.steuernr, "|") != "" or entry(6, guest.steuernr, "|") != None:
                markup_str = entry(6, guest.steuernr, "|")
                markup_str = replace_str(commission_str, "-", "")
                markup_str = replace_str(commission_str, "%", "")
                markup_str = replace_str(commission_str, ",", ".")
                markup_dec =  to_decimal(to_decimal(commission_str) )

            if entry(7, guest.steuernr, "|") != "" or entry(7, guest.steuernr, "|") != None:
                dcommission = logical(entry(7, guest.steuernr, "|"))

            if entry(8, guest.steuernr, "|") != "" or entry(8, guest.steuernr, "|") != None:
                artnr_comm = to_int(entry(8, guest.steuernr, "|"))

        elif num_entries(guest.steuernr, "|") == 5:

            if entry(1, guest.steuernr, "|") != "" or entry(1, guest.steuernr, "|") != None:
                commission_str = entry(1, guest.steuernr, "|")
                commission_str = replace_str(commission_str, "-", "")
                commission_str = replace_str(commission_str, "%", "")
                commission_str = replace_str(commission_str, ",", ".")
                commission_dec =  to_decimal(to_decimal(commission_str) )

            if entry(2, guest.steuernr, "|") != "" or entry(2, guest.steuernr, "|") != None:
                markup_str = entry(2, guest.steuernr, "|")
                markup_str = replace_str(commission_str, "-", "")
                markup_str = replace_str(commission_str, "%", "")
                markup_str = replace_str(commission_str, ",", ".")
                markup_dec =  to_decimal(to_decimal(commission_str) )

            if entry(3, guest.steuernr, "|") != "" or entry(3, guest.steuernr, "|") != None:
                dcommission = logical(entry(3, guest.steuernr, "|"))

            if entry(4, guest.steuernr, "|") != "" or entry(4, guest.steuernr, "|") != None:
                artnr_comm = to_int(entry(4, guest.steuernr, "|"))

    reservation = get_cache (Reservation, {"gastnr": [(eq, ota_gastnr)],"vesrdepot": [(eq, res_info.res_id)],"activeflag": [(eq, 0)]})

    if not reservation:

        reservation = get_cache (Reservation, {"vesrdepot": [(eq, res_info.res_id)],"activeflag": [(eq, 0)]})

    if not reservation:
        error_str = "Reservation " + res_info.res_id + " not found"

        reservation = get_cache (Reservation, {"vesrdepot": [(eq, res_info.res_id)]})

        if reservation:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr)).order_by(Res_line._recid).all():

                if res_line.ankunft == res_line.abreise:
                    upto_date = res_line.abreise
                else:
                    upto_date = res_line.abreise - timedelta(days=1)
                for bill_date in date_range(res_line.ankunft,upto_date) :

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                    if zimkateg:

                        if cat_flag:
                            zikatnr = zimkateg.typ
                        else:
                            zikatnr = zimkateg.zikatnr
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                            rline_origcode = substring(iftask, 10)
                            break

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, rline_origcode)]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            bqueasy.logi2 = True
                            pass
                            pass

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, "")]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            bqueasy.logi2 = True
                            pass
                            pass

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"l_zuordnung[2]": [(eq, 0)],"active_flag": [(eq, 0)]})

    if not res_line:
        error_str = "Reservation " + res_info.res_id + " not found. Expired Modify Date"

        return generate_output()

    bres = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

    if bres:
        bres.bemerk = res_info.remark
        pass
        pass
    curr_resnr = reservation.resnr

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == reservation.resnr) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.active_flag == 0)).order_by(Res_line._recid).all():
        t_resline = T_resline()
        t_resline_data.append(t_resline)

        buffer_copy(res_line, t_resline)
        t_resline.firstname = trim(entry(1, t_resline.NAME, ","))
        t_resline.lastname = trim(entry(0, t_resline.NAME, ","))
        t_resline.uniq_id = res_info.res_id

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            t_resline.typ = zimkateg.typ
    asc_str = chk_ascii(res_info.sure_name)
    res_info.sure_name = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.city)
    res_info.city = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.given_name)
    res_info.given_name = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.address1)
    res_info.address1 = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.address2)
    res_info.address2 = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.city)
    res_info.city = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.remark)
    res_info.remark = asc_str
    asc_str = ""
    asc_str = chk_ascii(res_info.email)
    res_info.email = asc_str
    asc_str = ""
    loop_i = 0

    for room_list in query(room_list_data):

        if room_list.ankunft < get_current_date() or room_list.abreise < get_current_date():
            error_str = "Expired Modify Checkin / Checkout Date "

            return generate_output()
        loop_i = loop_i + 1
        room_list.reslinnr = loop_i
        detres = Detres()
        detres_data.append(detres)

        buffer_copy(room_list, detres)
        detres.reslinnr = loop_i

        guest_list = query(guest_list_data, filters=(lambda guest_list: guest_list.gastnr == room_list.gastnr), first=True)

        if guest_list:
            detres.firstname = guest_list.given_name
            detres.lastname = guest_list.sure_name
            firstname = guest_list.given_name
            lastname = guest_list.sure_name


        else:
            detres.firstname = res_info.given_name
            detres.lastname = res_info.sure_name
            firstname = res_info.given_name
            lastname = res_info.sure_name

        if cat_flag:

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, room_list.room_type)]})

            if queasy:

                t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.typ == queasy.number1 and not t_resline.flag and t_resline.firstname.lower()  == (firstname).lower()  and t_resline.lastname.lower()  == (lastname).lower()), first=True)

                if not t_resline:

                    t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.typ == queasy.number1 and not t_resline.flag), first=True)

                if t_resline:
                    detres.zikatnr = t_resline.zikatnr
                    t_resline.flag = True

                if detRes.zikatnr == 0:

                    zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})

                    if zimkateg:
                        detres.zikatnr = zimkateg.zikatnr
            else:
                error_str = error_str + chr_unicode(10) + room_list.room_type + "No such Room Category"

                return generate_output()
        else:

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, room_list.room_type)]})

            if zimkateg:

                t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.zikatnr == zimkateg.zikatnr and not t_resline.flag and t_resline.firstname.lower()  == (firstname).lower()  and t_resline.lastname.lower()  == (lastname).lower()), first=True)

                if not t_resline:

                    t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.zikatnr == zimkateg.zikatnr and not t_resline.flag), first=True)

                if t_resline:
                    t_resline.flag = True
                    detres.zikatnr = t_resline.zikatnr

                if detRes.zikatnr == 0:
                    detres.zikatnr = zimkateg.zikatnr
            else:
                error_str = error_str + chr_unicode(10) + room_list.room_type + "No such Room Category"

                return generate_output()

    for t_resline in query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False), sort_by=[("reslinnr",False)]):

        detres = query(detres_data, filters=(lambda detres: detres.detRes.firstname == t_resline.firstname and detRes.lastname == t_resline.lastname and detRes.zikatnr == t_resline.zikatnr and detRes.reslinnr == t_resline.reslinnr and detRes.selected == False), first=True)

        if detRes:

            tb_detres = query(tb_detres_data, first=True)

            if not tb_detRes:
                tb_detres = Tb_detres()
                tb_detres_data.append(tb_detres)

            buffer_copy(detRes, tb_detres)
            t_resline.selected = True
            detres.selected = True


            modify_res(t_resline.resnr, t_resline.reslinnr)
            get_output(intevent_1(9, t_resline.zinr, "Priscilla", t_resline.resnr, t_resline.reslinnr))
    tb_detRes_data.clear()

    t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False), first=True)

    if t_resline:

        for t_resline in query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False)):

            detres = query(detres_data, filters=(lambda detres: detres.detRes.zikatnr == t_resline.zikatnr and detRes.reslinnr == t_resline.reslinnr and detRes.selected == False), first=True)

            if detRes:

                tb_detres = query(tb_detres_data, first=True)

                if not tb_detRes:
                    tb_detres = Tb_detres()
                    tb_detres_data.append(tb_detres)

                buffer_copy(detRes, tb_detres)
                t_resline.selected = True
                detres.selected = True


                modify_res(t_resline.resnr, t_resline.reslinnr)
                get_output(intevent_1(9, t_resline.zinr, "Priscilla", t_resline.resnr, t_resline.reslinnr))

    tb_detRes_data.clear()

    t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False), first=True)

    if t_resline:

        for t_resline in query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False)):

            detres = query(detres_data, filters=(lambda detres: detres.detRes.firstname == t_resline.firstname and detRes.lastname == t_resline.lastname and detRes.zikatnr == t_resline.zikatnr and detRes.selected == False), first=True)

            if detRes:

                tb_detres = query(tb_detres_data, first=True)

                if not tb_detRes:
                    tb_detres = Tb_detres()
                    tb_detres_data.append(tb_detres)

                buffer_copy(detRes, tb_detres)
                t_resline.selected = True
                detres.selected = True


                modify_res(t_resline.resnr, t_resline.reslinnr)
                get_output(intevent_1(9, t_resline.zinr, "Priscilla", t_resline.resnr, t_resline.reslinnr))

    tb_detRes_data.clear()

    t_resline = query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False), first=True)

    if t_resline:

        for t_resline in query(t_resline_data, filters=(lambda t_resline: t_resline.selected == False)):

            detres = query(detres_data, filters=(lambda detres: detres.detRes.selected == False and (detRes.zikatnr == t_resline.zikatnr or detRes.reslinnr == t_resline.reslinnr)), first=True)

            if detRes:

                tb_detres = query(tb_detres_data, first=True)

                if not tb_detRes:
                    tb_detres = Tb_detres()
                    tb_detres_data.append(tb_detres)

                buffer_copy(detRes, tb_detres)
                t_resline.selected = True
                detres.selected = True


                modify_res(t_resline.resnr, t_resline.reslinnr)
                get_output(intevent_1(9, t_resline.zinr, "Priscilla", t_resline.resnr, t_resline.reslinnr))
            else:
                del_mainres, cancel_msg = get_output(del_reslinebl(1, "cancel", t_resline.resnr, t_resline.reslinnr, "**", "BookEngine " + t_resline.uniq_id + " Modified - Cancelled RoomType"))


    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == reservation.resnr)).order_by(Res_line.reslinnr.desc()).all():
        curr_reslinnr = res_line.reslinnr
        break

    for detres in query(detres_data):

        if detRes.selected == False:
            curr_reslinnr = curr_reslinnr + 1
            detres.reslinnr = curr_reslinnr


            room_list1 = Room_list1()
            room_list1_data.append(room_list1)

            buffer_copy(detRes, room_list1)
        else:
            detres_data.remove(detres)

    res_info = query(res_info_data, first=True)
    error_str, done = get_output(if_vhp_bookeng_store_resbl(res_info_data, room_list1_data, service_list_data, guest_list_data, "insert", dyna_code, becode, curr_resnr, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name))
    done = True

    return generate_output()