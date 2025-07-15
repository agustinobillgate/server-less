#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown_phm import get_room_breakdown_phm
from models import Guest, Res_line, Htparam, Reservation, Zimkateg, Bediener, Segment

def dashboard_phm_initialbl(banquet_dept:string, commision:string, payable:string):

    prepare_cache ([Guest, Htparam, Reservation, Zimkateg, Bediener, Segment])

    his_res_data = []
    datum:date = None
    datum2:date = None
    ci_date:date = None
    i:int = 0
    j:int = 0
    iftask:string = ""
    last_rechnr:int = 0
    curr_i:int = 0
    curr_date:date = None
    end_date:date = None
    fnet_lodg:Decimal = to_decimal("0.0")
    net_lodg:Decimal = to_decimal("0.0")
    tot_breakfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_other:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_vat:Decimal = to_decimal("0.0")
    tot_service:Decimal = to_decimal("0.0")
    tot_fb:Decimal = to_decimal("0.0")
    tot_banquet:Decimal = to_decimal("0.0")
    tot_commision:Decimal = to_decimal("0.0")
    tot_payable:Decimal = to_decimal("0.0")
    do_it1:bool = False
    vat_proz:Decimal = 10
    do_it:bool = False
    serv_taxable:bool = False
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    netto:Decimal = to_decimal("0.0")
    serv_betrag:Decimal = to_decimal("0.0")
    outstr:string = ""
    outstr1:string = ""
    revcode:string = ""
    rechnr_nottax:int = 0
    bill_date:date = None
    bill_resnr:int = 0
    bill_reslinnr:int = 0
    bill_parentnr:int = 0
    bill_gastnr:int = 0
    ex_article:string = ""
    t_reslinnr:int = 0
    guest = res_line = htparam = reservation = zimkateg = bediener = segment = None

    his_res = his_inv = temp_res = future_res = future_inv = non_room = t_list = gbuff = bufhis_inv = buffuture_inv = bufres_line = None

    his_res_data, His_res = create_model("His_res", {"number":int, "resnr":int, "reslinnr":int, "staydate":date, "ci_date":date, "co_date":date, "nbrofroom":int, "room_type":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal, "resstatus":string, "reserveid":int, "reservename":string, "bookdate":date, "rate_code":string, "nationality":string, "segmentcode":string, "cancel_date":string, "zinr":string, "nights":int, "adult":int, "child":int, "complimentary":int, "arrangement":string, "guest_name":string, "banquet_rev":Decimal, "commision":Decimal, "payable":Decimal, "nation2":string, "booktime":string, "salesid":string})
    his_inv_data, His_inv = create_model("His_inv", {"datum":date, "room_type":string, "room_status":string, "qty":int, "zikatnr":int})
    temp_res_data, Temp_res = create_model_like(His_res)
    future_res_data, Future_res = create_model_like(His_res)
    future_inv_data, Future_inv = create_model_like(His_inv)
    non_room_data, Non_room = create_model("Non_room", {"postingdate":date, "departmentid":int, "departmentname":string, "rm_rev":Decimal, "fb_rev":Decimal, "other_rev":Decimal})
    t_list_data, T_list = create_model("T_list", {"departement":int, "rechnr":int, "bill_datum":date, "sysdate":date, "zeit":int, "fb":Decimal, "other":Decimal, "fb_service":Decimal, "other_service":Decimal, "pay":Decimal, "compli":Decimal})

    Gbuff = create_buffer("Gbuff",Guest)
    Bufhis_inv = His_inv
    bufhis_inv_data = his_inv_data

    Buffuture_inv = Future_inv
    buffuture_inv_data = future_inv_data

    Bufres_line = create_buffer("Bufres_line",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal his_res_data, datum, datum2, ci_date, i, j, iftask, last_rechnr, curr_i, curr_date, end_date, fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, tot_fb, tot_banquet, tot_commision, tot_payable, do_it1, vat_proz, do_it, serv_taxable, serv, vat, netto, serv_betrag, outstr, outstr1, revcode, rechnr_nottax, bill_date, bill_resnr, bill_reslinnr, bill_parentnr, bill_gastnr, ex_article, t_reslinnr, guest, res_line, htparam, reservation, zimkateg, bediener, segment
        nonlocal banquet_dept, commision, payable
        nonlocal gbuff, bufhis_inv, buffuture_inv, bufres_line


        nonlocal his_res, his_inv, temp_res, future_res, future_inv, non_room, t_list, gbuff, bufhis_inv, buffuture_inv, bufres_line
        nonlocal his_res_data, his_inv_data, temp_res_data, future_res_data, future_inv_data, non_room_data, t_list_data

        return {"his-res": his_res_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for reservation in db_session.query(Reservation).filter(
             (Reservation.resdat >= 01/01/16) & (Reservation.resdat < ci_date)).order_by(Reservation.resdat).all():

        res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"resstatus": [(ne, 12),(ne, 99)],"l_zuordnung[2]": [(eq, 0)]})
        while None != res_line:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            his_res = His_res()
            his_res_data.append(his_res)

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
                his_res.nights = (res_line.abreise - res_line.ankunft).days
            else:
                his_res.nights = 1

            if zimkateg:
                his_res.room_type = zimkateg.kurzbez

            if guest:

                if guest.phonetik3 != "":

                    bediener = get_cache (Bediener, {"nr": [(eq, to_int(guest.phonetik3))]})

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

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

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

            if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
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
                     (Res_line.resnr == reservation.resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line._recid > curr_recid)).first()

    return generate_output()