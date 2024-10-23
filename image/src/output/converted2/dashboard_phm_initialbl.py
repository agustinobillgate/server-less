from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown_phm import get_room_breakdown_phm
from models import Guest, Res_line, Htparam, Reservation, Zimkateg, Bediener, Segment

def dashboard_phm_initialbl(banquet_dept:str, commision:str, payable:str):
    his_res_list = []
    datum:date = None
    datum2:date = None
    ci_date:date = None
    i:int = 0
    j:int = 0
    iftask:str = ""
    last_rechnr:int = 0
    curr_i:int = 0
    curr_date:date = None
    end_date:date = None
    fnet_lodg:decimal = to_decimal("0.0")
    net_lodg:decimal = to_decimal("0.0")
    tot_breakfast:decimal = to_decimal("0.0")
    tot_lunch:decimal = to_decimal("0.0")
    tot_dinner:decimal = to_decimal("0.0")
    tot_other:decimal = to_decimal("0.0")
    tot_rmrev:decimal = to_decimal("0.0")
    tot_vat:decimal = to_decimal("0.0")
    tot_service:decimal = to_decimal("0.0")
    tot_fb:decimal = to_decimal("0.0")
    tot_banquet:decimal = to_decimal("0.0")
    tot_commision:decimal = to_decimal("0.0")
    tot_payable:decimal = to_decimal("0.0")
    do_it1:bool = False
    vat_proz:decimal = 10
    do_it:bool = False
    serv_taxable:bool = False
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    netto:decimal = to_decimal("0.0")
    serv_betrag:decimal = to_decimal("0.0")
    outstr:str = ""
    outstr1:str = ""
    revcode:str = ""
    rechnr_nottax:int = 0
    bill_date:date = None
    bill_resnr:int = 0
    bill_reslinnr:int = 0
    bill_parentnr:int = 0
    bill_gastnr:int = 0
    ex_article:str = ""
    t_reslinnr:int = 0
    guest = res_line = htparam = reservation = zimkateg = bediener = segment = None

    his_res = his_inv = temp_res = future_res = future_inv = non_room = t_list = gbuff = bufhis_inv = buffuture_inv = bufres_line = None

    his_res_list, His_res = create_model("His_res", {"number":int, "resnr":int, "reslinnr":int, "staydate":date, "ci_date":date, "co_date":date, "nbrofroom":int, "room_type":str, "rm_rev":decimal, "fb_rev":decimal, "other_rev":decimal, "resstatus":str, "reserveid":int, "reservename":str, "bookdate":date, "rate_code":str, "nationality":str, "segmentcode":str, "cancel_date":str, "zinr":str, "nights":int, "adult":int, "child":int, "complimentary":int, "arrangement":str, "guest_name":str, "banquet_rev":decimal, "commision":decimal, "payable":decimal, "nation2":str, "booktime":str, "salesid":str})
    his_inv_list, His_inv = create_model("His_inv", {"datum":date, "room_type":str, "room_status":str, "qty":int, "zikatnr":int})
    temp_res_list, Temp_res = create_model_like(His_res)
    future_res_list, Future_res = create_model_like(His_res)
    future_inv_list, Future_inv = create_model_like(His_inv)
    non_room_list, Non_room = create_model("Non_room", {"postingdate":date, "departmentid":int, "departmentname":str, "rm_rev":decimal, "fb_rev":decimal, "other_rev":decimal})
    t_list_list, T_list = create_model("T_list", {"departement":int, "rechnr":int, "bill_datum":date, "sysdate":date, "zeit":int, "fb":decimal, "other":decimal, "fb_service":decimal, "other_service":decimal, "pay":decimal, "compli":decimal})

    Gbuff = create_buffer("Gbuff",Guest)
    Bufhis_inv = His_inv
    bufhis_inv_list = his_inv_list

    Buffuture_inv = Future_inv
    buffuture_inv_list = future_inv_list

    Bufres_line = create_buffer("Bufres_line",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal his_res_list, datum, datum2, ci_date, i, j, iftask, last_rechnr, curr_i, curr_date, end_date, fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_fb, tot_banquet, tot_commision, tot_payable, do_it1, vat_proz, do_it, serv_taxable, serv, vat, netto, serv_betrag, outstr, outstr1, revcode, rechnr_nottax, bill_date, bill_resnr, bill_reslinnr, bill_parentnr, bill_gastnr, ex_article, t_reslinnr, guest, res_line, htparam, reservation, zimkateg, bediener, segment
        nonlocal banquet_dept, commision, payable
        nonlocal gbuff, bufhis_inv, buffuture_inv, bufres_line


        nonlocal his_res, his_inv, temp_res, future_res, future_inv, non_room, t_list, gbuff, bufhis_inv, buffuture_inv, bufres_line
        nonlocal his_res_list, his_inv_list, temp_res_list, future_res_list, future_inv_list, non_room_list, t_list_list
        return {"his-res": his_res_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for reservation in db_session.query(Reservation).filter(
             (Reservation.resdat >= 01/01/16) & (Reservation.resdat < ci_date)).order_by(Reservation.resdat).all():

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).first()
        while None != res_line:

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnr)).first()

            gbuff = db_session.query(Gbuff).filter(
                     (Gbuff.gastnr == res_line.gastnrmember)).first()
            his_res = His_res()
            his_res_list.append(his_res)

            his_res.resnr = res_line.resnr
            his_res.reslinnr = res_line.reslinnr
            his_res.ci_date = res_line.ankunft
            his_res.co_date = res_line.abreise
            his_res.adult = res_line.erwachs
            his_res.child = res_line.kind1
            his_res.complimentary = res_line.gratis
            his_res.arrangement = res_line.arrangement
            his_res.booktime = substring(res_line.reserve_char, 8, 5)
            his_res.guest_name = res_line.name

            if res_line.resstatus == 11 or res_line.resstatus == 13:
                his_res.nbrofroom = 0
            else:
                his_res.nbrofroom = res_line.zimmeranz

            if res_line.ankunft != res_line.abreise:
                his_res.nights = res_line.abreise - res_line.ankunft
            else:
                his_res.nights = 1

            if zimkateg:
                his_res.room_type = zimkateg.kurzbez

            if guest:

                if guest.phonetik3 != "":

                    bediener = db_session.query(Bediener).filter(
                             (Bediener.nr == to_int(guest.phonetik3))).first()

                    if bediener:
                        his_res.salesid = bediener.username
                his_res.reserveid = guest.gastnr

                if guest.vorname1 != "":
                    his_res.reservename = guest.name + " " + guest.vorname1
                else:
                    his_res.reservename = guest.name

            if gbuff:
                his_res.nationality = gbuff.nation1
                his_res.nation2 = gbuff.nation2

            if reservation:
                his_res.bookdate = reservation.resdat

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()

                if segment:
                    his_res.segmentcode = segment.bezeich

            if res_line.resstatus == 1:
                his_res.resstatus = "Guaranteed"

            elif res_line.resstatus == 2:
                his_res.resstatus = "6PM"

            elif res_line.resstatus == 3:
                his_res.resstatus = "Tentative"

            elif res_line.resstatus == 4:
                his_res.resstatus = "WaitList"

            elif res_line.resstatus == 5:
                his_res.resstatus = "VerbalConfirm"

            elif res_line.resstatus == 6:
                his_res.resstatus = "Inhouse"

            elif res_line.resstatus == 8:
                his_res.resstatus = "Departed"

            elif res_line.resstatus == 9:
                his_res.resstatus = "Cancelled"

            elif res_line.resstatus == 10:
                his_res.resstatus = "NoShow"

            elif res_line.resstatus == 11:
                his_res.resstatus = "ShareRes"

            elif res_line.resstatus == 13:
                his_res.resstatus = "RmSharer"

            if re.match(r".*\$OrigCode\$.*",res_line.zimmer_wunsch, re.IGNORECASE):
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                        his_res.rate_code = substring(iftask, 10)

            if res_line.ankunft != res_line.abreise:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = res_line.abreise
            for datum in date_range(res_line.ankunft,datum2) :
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_banquet, tot_commision, tot_payable = get_output(get_room_breakdown_phm(res_line._recid, datum, curr_i, curr_date, banquet_dept, commision, payable))
                his_res.fb_rev =  to_decimal(his_res.fb_rev) + to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                his_res.rm_rev =  to_decimal(his_res.rm_rev) + to_decimal(net_lodg)
                his_res.other_rev =  to_decimal(his_res.other_rev) + to_decimal(tot_other)
                his_res.banquet_rev =  to_decimal(his_res.banquet_rev) + to_decimal(tot_banquet)
                his_res.commision =  to_decimal(his_res.commision) + to_decimal(tot_commision)
                his_res.payable =  to_decimal(his_res.payable) + to_decimal(tot_payable)

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).filter(Res_line._recid > curr_recid).first()

    return generate_output()