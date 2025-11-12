#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# - Fix lowercase variable and temp-table
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
import re
from functions.get_room_breakdown import get_room_breakdown
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Zimkateg, Arrangement, Queasy, Prmarket, Ratecode, Waehrung, Genstat, Artikel, Nightaudit, Nitehist, Htparam, Paramtext, Res_line, Reslin_queasy, Reservation, Segment, Zkstat, Zinrstat, Segmentstat, Umsatz, Budget, Guest, Guestseg, Sourccod, Guest_pr, Nation, exrate, Gl_acct

def nt_aiirevenue_manual_reupload(ci_date:date):

    prepare_cache ([Waehrung, Genstat, Artikel, Nightaudit, Htparam, Paramtext, Res_line, Reslin_queasy, Reservation, Segment, Zkstat, Zinrstat, Segmentstat, Umsatz, Budget, Guest, Guestseg, Guest_pr, Nation, exrate])

    fr_date:date = None
    fr_date1:date = None
    to_date:date = None
    htl_no:string = ""
    datum:date = None
    loop_datum:date = None
    co_date:date = None
    rsv_date:date = None
    birthdate:string = ""
    canceldate:string = ""
    expdate:string = ""
    address:string = ""
    flight1:string = ""
    flight2:string = ""
    eta:string = ""
    etd:string = ""
    str_rsv:string = ""
    purpose:string = ""
    ankunft:string = ""
    abreise:string = ""
    hharr:string = ""
    mmarr:string = ""
    hhdep:string = ""
    mmdep:string = ""
    ci_time:string = ""
    co_time:string = ""
    pickup:string = ""
    voucherno:string = ""
    contcode:string = ""
    bookdate:string = ""
    dropoff:string = ""
    memozinr:string = ""
    rsv_time:string = ""
    outstr:string = ""
    segm__purcode:int = 0
    loop_i:int = 0
    curr_i:int = 0
    price_decimal:int = 0
    i_counter:int = 0
    droom:int = 0
    mroom:int = 0
    mbroom:int = 0
    flodging:Decimal = to_decimal("0.0")
    lodging:Decimal = to_decimal("0.0")
    breakfast:Decimal = to_decimal("0.0")
    lunch:Decimal = to_decimal("0.0")
    dinner:Decimal = to_decimal("0.0")
    others:Decimal = to_decimal("0.0")
    rmrev:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    tot_lodging:Decimal = to_decimal("0.0")
    tot_breakfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_others:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_vat:Decimal = to_decimal("0.0")
    tot_service:Decimal = to_decimal("0.0")
    payable_sum:Decimal = to_decimal("0.0")
    taxed_payable_sum:Decimal = to_decimal("0.0")
    drev:Decimal = to_decimal("0.0")
    mrev:Decimal = to_decimal("0.0")
    dtrev:Decimal = to_decimal("0.0")
    mtrev:Decimal = to_decimal("0.0")
    otherrev:Decimal = to_decimal("0.0")
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    reihenfolge:int = 0
    progname:string = "nt-aiirevenue.p"
    exrate:Decimal = to_decimal("0.0")
    frate:Decimal = to_decimal("0.0")
    anz:int = 0
    anz0:int = 0
    gastnr_wi:int = 0
    gastnr_ind:int = 0
    cat_flag:bool = False
    fact:Decimal = to_decimal("0.0")
    n_betrag:Decimal = to_decimal("0.0")
    n1_betrag:Decimal = to_decimal("0.0")
    foreign_flag:bool = False
    tot_taxed_payables:Decimal = to_decimal("0.0")
    tot_payables1:Decimal = to_decimal("0.0")
    tot_payables2:Decimal = to_decimal("0.0")
    tot_payables3:Decimal = to_decimal("0.0")
    tot_payables4:Decimal = to_decimal("0.0")
    rev_gross_day:Decimal = to_decimal("0.0")
    rev_gross_bud:Decimal = to_decimal("0.0")
    rev_gross_mtd:Decimal = to_decimal("0.0")
    rev_gross_ytd:Decimal = to_decimal("0.0")
    zimkateg = arrangement = queasy = prmarket = ratecode = waehrung = genstat = artikel = nightaudit = nitehist = htparam = paramtext = res_line = reslin_queasy = reservation = segment = zkstat = zinrstat = segmentstat = umsatz = budget = guest = guestseg = sourccod = guest_pr = nation = exrate = gl_acct = None

    rsv_list = guest_list = ta_list = arrangement_list = zimkateg_list = temp_gastnr = temp_reslin_queasy = segmentrevenue = totalsegmentsrevenue = totalroomrevenue = totalfbrevenue = totalotherrevenue = hotelnetrevenue = hotelgrossrevenue = totalroom = roomsavailable = roomsoccupied = houseuses = complimentaryrooms = roomspaying = vacantrooms = outoforderrooms = noshows = reservationmadetoday = cancellationfortoday = earlycheckout = roomarrivalstoday = personarrivalstoday = roomdeparturestoday = persondeparturestoday = roomarrivalstomorrow = personarrivalstomorrow = roomdeparturestomorrow = persondeparturestomorrow = roomtype = rate_list = w1 = rsvdetails = rc = rmtyp = rooms = t_zimkateg = t_arrangement = t_qsy2 = t_qsy18 = t_qsy152 = t_prmarket = temp_rc = wrung = gstat = buffart = qsy18 = None

    rsv_list_data, Rsv_list = create_model("Rsv_list", {"resnr":string, "reslinnr":string, "arr_date":string, "dep_date":string, "flight1":string, "flight2":string, "eta":string, "etd":string, "pickup":string, "dropoff":string, "nights":string, "adults":string, "childs":string, "infants":string, "infantage":string, "comp":string, "comp_ch":string, "voucher":string, "ta_code":string, "ratecode":string, "qty":string, "roomcat":string, "argt":string, "curr":string, "roomrate":string, "roomcharge":string, "roomtax":string, "roomserv":string, "room_bf":string, "room_lunch":string, "room_dinner":string, "room_others":string, "discount":string, "commission":string, "fixrate":string, "billinstruction":string, "purpose":string, "memo":string, "gastnrmember":string, "guest_status":string, "rsv_type":string, "rsv_status":string, "rsv_time":string, "cancel_nr":string, "cancel_date":string, "cancel":string, "ci_time":string, "co_time":string, "resstatus":int, "active_flag":int, "zinr":string, "isdayuseincluded":string, "modifydate":string})
    guest_list_data, Guest_list = create_model("Guest_list", {"gastnr":string, "lastname":string, "firstname":string, "address":string, "city":string, "prov":string, "zip":string, "country":string, "birthplace":string, "birthdate":string, "sex":string, "phone":string, "mobile":string, "fax":string, "email":string, "occupation":string, "idcard_nr":string, "idcard_type":string, "idcard_exp":string, "companyguestnr":string, "mainsegment":string, "codes":string, "vip":string, "comments":string, "nation":string, "modifydate":string})
    ta_list_data, Ta_list = create_model("Ta_list", {"gastnr":string, "refno":string, "name":string, "ta_title":string, "address":string, "city":string, "prov":string, "zip":string, "country":string, "phone":string, "telefax":string, "email":string, "ratecode":string, "mainsegment":string, "booksource":string, "comments":string, "iscompany":string})
    arrangement_list_data, Arrangement_list = create_model("Arrangement_list", {"arrangement":string, "argt_bez":string})
    zimkateg_list_data, Zimkateg_list = create_model("Zimkateg_list", {"kurzbez":string, "bezeichnung":string})
    temp_gastnr_data, Temp_gastnr = create_model("Temp_gastnr", {"gastnr":int})
    temp_reslin_queasy_data, Temp_reslin_queasy = create_model("Temp_reslin_queasy", {"resnr":int, "reslinnr":int, "number2":int, "modify_date":date})
    segmentrevenue_data, Segmentrevenue = create_model("Segmentrevenue", {"segmentcode":int, "segmentdescription":string, "segmentcomment":string, "todayroomnight":int, "todayrevenue":Decimal, "todayrevenuepercentage":Decimal, "mtdroomnight":int, "mtdrevenue":Decimal, "mtdrevenuepercentage":Decimal, "ytdroomnight":int, "ytdrevenue":Decimal, "ytdrevenuepercentage":Decimal, "budget":Decimal, "variance":Decimal})
    totalsegmentsrevenue_data, Totalsegmentsrevenue = create_model("Totalsegmentsrevenue", {"day":Decimal, "todaypercentage":Decimal, "mtd":Decimal, "mtdpercentage":Decimal, "ytd":Decimal, "ytdpercentage":Decimal, "budget":Decimal, "variance":Decimal})
    totalroomrevenue_data, Totalroomrevenue = create_model("Totalroomrevenue", {"day":Decimal, "todaypercentage":Decimal, "mtd":Decimal, "mtdpercentage":Decimal, "ytd":Decimal, "ytdpercentage":Decimal, "budget":Decimal, "variance":Decimal})
    totalfbrevenue_data, Totalfbrevenue = create_model("Totalfbrevenue", {"day":Decimal, "todaypercentage":Decimal, "mtd":Decimal, "mtdpercentage":Decimal, "ytd":Decimal, "ytdpercentage":Decimal, "budget":Decimal, "variance":Decimal})
    totalotherrevenue_data, Totalotherrevenue = create_model("Totalotherrevenue", {"day":Decimal, "todaypercentage":Decimal, "mtd":Decimal, "mtdpercentage":Decimal, "ytd":Decimal, "ytdpercentage":Decimal, "budget":Decimal, "variance":Decimal})
    hotelnetrevenue_data, Hotelnetrevenue = create_model("Hotelnetrevenue", {"day":Decimal, "todaypercentage":Decimal, "mtd":Decimal, "mtdpercentage":Decimal, "ytd":Decimal, "ytdpercentage":Decimal, "budget":Decimal, "variance":Decimal})
    hotelgrossrevenue_data, Hotelgrossrevenue = create_model("Hotelgrossrevenue", {"day":Decimal, "todaypercentage":Decimal, "mtd":Decimal, "mtdpercentage":Decimal, "ytd":Decimal, "ytdpercentage":Decimal, "budget":Decimal, "variance":Decimal})
    totalroom_data, Totalroom = create_model("Totalroom", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomsavailable_data, Roomsavailable = create_model("Roomsavailable", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomsoccupied_data, Roomsoccupied = create_model("Roomsoccupied", {"day":int, "mtd":int, "budget":int, "ytd":int})
    houseuses_data, Houseuses = create_model("Houseuses", {"day":int, "mtd":int, "budget":int, "ytd":int})
    complimentaryrooms_data, Complimentaryrooms = create_model("Complimentaryrooms", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomspaying_data, Roomspaying = create_model("Roomspaying", {"day":int, "mtd":int, "budget":int, "ytd":int})
    vacantrooms_data, Vacantrooms = create_model("Vacantrooms", {"day":int, "mtd":int, "budget":int, "ytd":int})
    outoforderrooms_data, Outoforderrooms = create_model("Outoforderrooms", {"day":int, "mtd":int, "budget":int, "ytd":int})
    noshows_data, Noshows = create_model("Noshows", {"day":int, "mtd":int, "budget":int, "ytd":int})
    reservationmadetoday_data, Reservationmadetoday = create_model("Reservationmadetoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    cancellationfortoday_data, Cancellationfortoday = create_model("Cancellationfortoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    earlycheckout_data, Earlycheckout = create_model("Earlycheckout", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomarrivalstoday_data, Roomarrivalstoday = create_model("Roomarrivalstoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    personarrivalstoday_data, Personarrivalstoday = create_model("Personarrivalstoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomdeparturestoday_data, Roomdeparturestoday = create_model("Roomdeparturestoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    persondeparturestoday_data, Persondeparturestoday = create_model("Persondeparturestoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomarrivalstomorrow_data, Roomarrivalstomorrow = create_model("Roomarrivalstomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    personarrivalstomorrow_data, Personarrivalstomorrow = create_model("Personarrivalstomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomdeparturestomorrow_data, Roomdeparturestomorrow = create_model("Roomdeparturestomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    persondeparturestomorrow_data, Persondeparturestomorrow = create_model("Persondeparturestomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomtype_data, Roomtype = create_model("Roomtype", {"roomtypecode":string, "roomtypedescription":string, "todayroomnight":int, "todayrevenue":Decimal, "mtdroomnight":int, "mtdrevenue":Decimal, "ytdroomnight":int, "ytdrevenue":Decimal})
    rate_list_data, Rate_list = create_model("Rate_list", {"code":string, "bezeich":string})
    w1_data, W1 = create_model("W1", {"tday_saldo":Decimal, "mtd_saldo":Decimal, "mtd_budget":Decimal, "ytd_saldo":Decimal})
    rsvdetails_data, Rsvdetails = create_model("Rsvdetails", {"resnum":string, "reslinnum":string, "inhousedate":string, "date_str":string, "modifydate":string, "ratecode":string, "roomrate":string, "roomrateroomcharge":string, "roomratetax":string, "roomrateserv":string, "roomratebf":string, "roomratelunch":string, "roomratedinner":string, "roomrateother":string, "earlybookingdisc":string, "bonafidecommission":string, "roomcatcode":string, "roomargtcode":string})
    rc_data, Rc = create_model("Rc", {"rcode":string, "parentrcode":string, "zikatnr":int, "percent_flag":bool, "ratecalcpercentage":Decimal, "ratecalcamount":Decimal, "rcode_bez":string, "rcode_seg":string, "rcode_argt":string, "curr":string, "dyna_flag":string})
    rmtyp_data, Rmtyp = create_model("Rmtyp", {"rcode":string, "zikatnr":int, "rmtype":string})
    rooms_data, Rooms = create_model("Rooms", {"rcode":string, "zikatnr":int, "rmtype":string, "daysofweek":int, "adultcount":int, "childcount":int, "infantcount":int, "adultrate":Decimal, "childrate":Decimal, "infantrate":Decimal, "startdate":date, "enddate":date, "str_fdate":string, "str_tdate":string, "bookroom":int, "compliment":int, "maxcomplirooms":int})
    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)
    t_arrangement_data, T_arrangement = create_model_like(Arrangement)
    t_qsy2_data, T_qsy2 = create_model_like(Queasy)
    t_qsy18_data, T_qsy18 = create_model_like(Queasy)
    t_qsy152_data, T_qsy152 = create_model_like(Queasy)
    t_prmarket_data, T_prmarket = create_model_like(Prmarket)
    temp_rc_data, Temp_rc = create_model_like(Ratecode)

    Wrung = create_buffer("Wrung",Waehrung)
    Gstat = create_buffer("Gstat",Genstat)
    Buffart = create_buffer("Buffart",Artikel)
    Qsy18 = create_buffer("Qsy18",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        return {}

    def datetime2char(datum:date, zeit:int):

        nonlocal fr_date, fr_date1, to_date, htl_no, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        str:string = ""
        str = to_string(get_year(datum) , "9999") +\
                to_string(get_month(datum) , "99") +\
                to_string(get_day(datum) , "99") + "T" +\
                to_string(zeit, "HH:MM:SS")


        return str


    def dec2char(d:Decimal):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        str:string = ""
        d = to_decimal(round(d , 2))
        str = trim(to_string(d, "->>>>>>>>>>>>>>>>>9.99"))


        str = replace_str(str, ",", ".")
        return str


    def decode_string(in_str:string):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def create_rsv_list(i_resnr:int, i_reslinnr:int, i_date:date, i_time:int):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        gbuff = None
        s_time:string = ""
        rmcat:int = 0
        rm_service:Decimal = to_decimal("0.0")
        rm_vat:Decimal = to_decimal("0.0")
        rm_vat2:Decimal = to_decimal("0.0")
        rm_fact:Decimal = to_decimal("0.0")
        rm_tot_tax:Decimal = to_decimal("0.0")
        rm_tot_serv:Decimal = to_decimal("0.0")
        Gbuff =  create_buffer("Gbuff",Guest)

        if i_time == 0:
            s_time = "00:00:00"
        else:
            s_time = to_string(i_time, "hh:mm:ss")

        if res_line.resstatus == 9 or res_line.resstatus == 99:
            s_time = entry(1, entry(1, res_line.cancelled_id, ";") , "-")

        if i_date > ci_date:
            i_date = ci_date
        rsv_list = Rsv_list()
        rsv_list_data.append(rsv_list)


        if res_line.abreise == res_line.ankunft:
            co_date = res_line.abreise
        else:
            co_date = res_line.abreise - timedelta(days=1)
        tot_lodging =  to_decimal("0")
        tot_breakfast =  to_decimal("0")
        tot_lunch =  to_decimal("0")
        tot_dinner =  to_decimal("0")
        tot_others =  to_decimal("0")
        tot_rmrev =  to_decimal("0")
        tot_vat =  to_decimal("0")
        tot_service =  to_decimal("0")
        curr_i = 0
        rmrev =  to_decimal("0")
        vat =  to_decimal("0")
        service =  to_decimal("0")
        rmcat = 0
        contcode = ""


        for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

            if substring(str_rsv, 0, 6) == ("$CODE$").lower() :
                contcode = substring(str_rsv, 6)

            elif substring(str_rsv, 0, 5) == ("DATE,").lower() :
                bookdate = substring(str_rsv, 5)

            elif substring(str_rsv, 0, 8) == ("SEGM_PUR").lower() :
                segm__purcode = to_int(substring(str_rsv, 8))

        if matches(contcode,r"*|*"):
            contcode = replace_str(contcode, "|", "")

        rate_list = query(rate_list_data, filters=(lambda rate_list: rate_list.code.lower()  == (contcode).lower()), first=True)

        if not rate_list and contcode != "":
            rate_list = Rate_list()
            rate_list_data.append(rate_list)

            rate_list.code = contcode

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

            if queasy:
                rate_list.bezeich = queasy.char2
        ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
        kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

        if ebdisc_flag:
            rsv_list.discount = "1"
        else:
            rsv_list.discount = "0"

        if kbdisc_flag:
            rsv_list.commission = "1"
        else:
            rsv_list.commission = "0"

        if res_line.resstatus != 9 and res_line.resstatus != 99 and res_line.resstatus != 10:

            wrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if wrung:
                exrate =  to_decimal(wrung.ankauf) / to_decimal(wrung.einheit)
            else:
                exrate =  to_decimal("1")

            if res_line.resstatus == 6 and res_line.reserve_dec > 0:
                frate =  to_decimal(res_line.reserve_dec)
            else:
                frate =  to_decimal(exrate)
            for datum in date_range(res_line.ankunft,co_date) :
                curr_i = curr_i + 1
                flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, datum))
                rm_service, rm_vat, rm_vat2, rm_fact = get_output(calc_servtaxesbl(2, 99, 0, datum))

                if rmrev == 0:
                    vat =  to_decimal("0")
                    service =  to_decimal("0")
                    lodging =  to_decimal("0")
                    breakfast =  to_decimal("0")
                    lunch =  to_decimal("0")
                    dinner =  to_decimal("0")
                    others =  to_decimal("0")


                rm_tot_tax =  to_decimal(rm_vat) + to_decimal(rm_vat2)
                rm_tot_serv =  to_decimal(rm_service)
                rmrev =  to_decimal(rmrev) * to_decimal(frate)
                vat =  to_decimal(vat) * to_decimal(frate)
                service =  to_decimal(service) * to_decimal(frate)
                tot_lodging =  to_decimal(tot_lodging) + to_decimal(lodging)
                tot_breakfast =  to_decimal(tot_breakfast) + to_decimal(breakfast)
                tot_lunch =  to_decimal(tot_lunch) + to_decimal(lunch)
                tot_dinner =  to_decimal(tot_dinner) + to_decimal(dinner)
                tot_others =  to_decimal(tot_others) + to_decimal(others)
                tot_rmrev =  to_decimal(tot_rmrev) + to_decimal(rmrev)
                tot_vat =  to_decimal(tot_vat) + to_decimal(vat)
                tot_service =  to_decimal(tot_service) + to_decimal(service)


                rsvdetails = Rsvdetails()
                rsvdetails_data.append(rsvdetails)

                rsvdetails.resnum = to_string(res_line.resnr)
                rsvdetails.reslinnum = to_string(res_line.reslinnr)
                rsvdetails.inhousedate = to_string(get_year(datum) , "9999") + "-" +\
                        to_string(get_month(datum) , "99") + "-" +\
                        to_string(get_day(datum) , "99")
                rsvdetails.date_str = to_string(get_year(i_date) , "9999") + "-" +\
                        to_string(get_month(i_date) , "99") + "-" +\
                        to_string(get_day(i_date) , "99")
                rsvdetails.modifydate = to_string(get_year(i_date) , "9999") + "-" +\
                        to_string(get_month(i_date) , "99") + "-" +\
                        to_string(get_day(i_date) , "99") + "T" + s_time
                rsvdetails.earlybookingdisc = rsv_list.discount
                rsvdetails.bonafidecommission = rsv_list.commission

                genstat = get_cache (Genstat, {"datum": [(eq, datum)],"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)],"zinr": [(eq, res_line.zinr)]})

                if genstat:
                    rmcat = genstat.zikatnr
                    rsvdetails.roomargtcode = genstat.argt
                    rsvdetails.roomrate = to_string(round(genstat.zipreis, price_decimal))
                    rsvdetails.roomrateroomcharge = to_string(round(genstat.logis, price_decimal))
                    rsvdetails.roomratebf = to_string(round(genstat.res_deci[1], price_decimal))
                    rsvdetails.roomratelunch = to_string(round(genstat.res_deci[2], price_decimal))
                    rsvdetails.roomratedinner = to_string(round(genstat.res_deci[3], price_decimal))
                    rsvdetails.roomrateother = to_string(round(genstat.res_deci[4], price_decimal))
                    rsvdetails.roomratetax = to_string(round(genstat.logis * rm_tot_tax, price_decimal))
                    rsvdetails.roomrateserv = to_string(round(genstat.logis * rm_tot_serv, price_decimal))

                elif not genstat:
                    rmcat = res_line.zikatnr
                    rsvdetails.roomargtcode = res_line.arrangement
                    rsvdetails.roomrate = to_string(round(rmrev, price_decimal))
                    rsvdetails.roomrateroomcharge = to_string(round(lodging / res_line.zimmeranz, price_decimal))
                    rsvdetails.roomratebf = to_string(round(breakfast / res_line.zimmeranz, price_decimal))
                    rsvdetails.roomratelunch = to_string(round(lunch / res_line.zimmeranz, price_decimal))
                    rsvdetails.roomratedinner = to_string(round(dinner / res_line.zimmeranz, price_decimal))
                    rsvdetails.roomrateother = to_string(round(others / res_line.zimmeranz, price_decimal))
                    rsvdetails.roomratetax = to_string(round(vat / res_line.zimmeranz, price_decimal))
                    rsvdetails.roomrateserv = to_string(round(service / res_line.zimmeranz, price_decimal))

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rmcat)]})

                if zimkateg:
                    rsvdetails.roomcatcode = zimkateg.kurzbez
                else:
                    rsvdetails.roomcatcode = ""

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(eq, datum)],"date2": [(eq, datum)]})

                if reslin_queasy:
                    rsvdetails.ratecode = reslin_queasy.char2

                elif not reslin_queasy:

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(eq, res_line.ankunft)],"date2": [(eq, res_line.abreise)]})

                    if reslin_queasy:
                        rsvdetails.ratecode = reslin_queasy.char2

                    elif not reslin_queasy:
                        rsvdetails.ratecode = contcode
            rsv_list.roomcharge = to_string(round(tot_lodging / curr_i, price_decimal))
            rsv_list.room_bf = to_string(round(tot_breakfast / curr_i, price_decimal))
            rsv_list.room_lunch = to_string(round(tot_lunch / curr_i, price_decimal))
            rsv_list.room_dinner = to_string(round(tot_dinner / curr_i, price_decimal))
            rsv_list.room_others = to_string(round(tot_others / curr_i, price_decimal))
            rsv_list.roomtax = to_string(round(tot_vat / curr_i, price_decimal))
            rsv_list.roomserv = to_string(round(tot_service / curr_i, price_decimal))
            rsv_list.roomrate = to_string(round(tot_rmrev / curr_i, price_decimal))

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if reslin_queasy:
            rsv_list.fixrate = "1"
        else:
            rsv_list.fixrate = "0"

        queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, segm__purcode)]})

        if queasy:
            rsv_list.purpose = queasy.char1 + " " + queasy.char3

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            rsv_list.roomcat = zimkateg.kurzbez
        else:
            rsv_list.roomcat = ""
        rsv_list.curr = "IDR"

        if matches(res_line.zimmer_wunsch,r"*pickup*"):
            rsv_list.pickup = "1"
        else:
            rsv_list.pickup = "0"

        if matches(res_line.zimmer_wunsch,r"*drop-passanger*"):
            rsv_list.dropoff = "1"
        else:
            rsv_list.dropoff = "0"

        if session_date_format() == ("dmy").lower() :
            rsv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

        elif session_date_format() == ("mdy").lower() :
            rsv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
        else:
            rsv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

        gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if gbuff:
            rsv_list.ta_code = to_string(gbuff.gastnr)

            ta_list = query(ta_list_data, filters=(lambda ta_list: ta_list.gastnr == rsv_list.TA_code), first=True)

            if not ta_list and rsv_list.TA_code != "":
                ta_list = Ta_list()
                ta_list_data.append(ta_list)

                ta_list.gastnr = rsv_list.TA_code
                ta_list.name = gbuff.name
                ta_list.ta_title = gbuff.anredefirma
                ta_list.address = gbuff.adresse1 + ", " + gbuff.adresse2 + ", " + gbuff.adresse3
                ta_list.city = gbuff.wohnort
                ta_list.zip = gbuff.plz
                ta_list.country = gbuff.land
                ta_list.email = gbuff.email_adr
                ta_list.comments = gbuff.bemerkung

                if matches(gbuff.telefon,r"*|*"):
                    ta_list.phone = replace_str(gbuff.telefon, "|", "-")

                if matches(gbuff.fax,r"*|*"):
                    ta_list.telefax = replace_str(gbuff.fax, "|", "-")

                if gbuff.karteityp == 1:
                    ta_list.iscompany = "1"
                else:
                    ta_list.iscompany = "0"

                if matches(ta_list.comments,r"*|*"):
                    ta_list.comments = replace_str(ta_list.comments, "|", "-")

                if matches(gbuff.steuernr,r"*" + chr_unicode(124) + r"*"):
                    ta_list.refno = entry(0, gbuff.steuernr, chr_unicode(124))

                elif not matches(gbuff.steuernr,r"*" + chr_unicode(124) + r"*") and gbuff.steuernr != "":
                    ta_list.refno = gbuff.steuernr
                else:
                    ta_list.refno = ""

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, gbuff.gastnr)],"reihenfolge": [(eq, 1)]})

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                    if segment:
                        ta_list.mainsegment = entry(0, segment.bezeich, "$$0")

                sourccod = get_cache (Sourccod, {"source_code": [(eq, gbuff.segment3)]})

                if Sourccod:
                    ta_list.booksource = Sourccod.bezeich

                for guest_pr in db_session.query(Guest_pr).filter(
                         (Guest_pr.gastnr == gbuff.gastnr)).order_by(Guest_pr._recid).all():
                    ta_list.ratecode = ta_list.ratecode + guest_pr.code + ";"
        eta = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2) + ":00"
        etd = substring(res_line.flight_nr, 17, 2) + ":" + substring(res_line.flight_nr, 19, 2) + ":00"
        rsv_list.resnr = to_string(res_line.resnr)
        rsv_list.reslinnr = to_string(res_line.reslinnr)
        rsv_list.arr_date = to_string(get_year(res_line.ankunft) , "9999") + "-" + to_string(get_month(res_line.ankunft) , "99") + "-" +\
                to_string(get_day(res_line.ankunft) , "99")
        rsv_list.dep_date = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" +\
                to_string(get_day(res_line.abreise) , "99")
        rsv_list.flight1 = substring(res_line.flight_nr, 0, 6)
        rsv_list.flight2 = substring(res_line.flight_nr, 11, 6)
        rsv_list.nights = to_string(res_line.anztage)
        rsv_list.adults = to_string(res_line.erwachs)
        rsv_list.childs = to_string(res_line.kind1)
        rsv_list.infants = to_string(res_line.kind2)
        rsv_list.infantage = ""
        rsv_list.comp = to_string(res_line.gratis)
        rsv_list.comp_ch = to_string(res_line.l_zuordnung[3])
        rsv_list.ratecode = contcode
        rsv_list.qty = to_string(res_line.zimmeranz)
        rsv_list.argt = res_line.arrangement
        rsv_list.billinstruction = res_line.code
        rsv_list.gastnrmember = to_string(res_line.gastnrmember)
        rsv_list.cancel_nr = to_string(res_line.storno_nr)
        rsv_list.cancel = res_line.stornogrund
        rsv_list.resstatus = res_line.resstatus
        rsv_list.active_flag = res_line.active_flag
        rsv_list.zinr = res_line.zinr
        rsv_list.isdayuseincluded = "0"
        rsv_list.modifydate = to_string(get_year(i_date) , "9999") + "-" + to_string(get_month(i_date) , "99") + "-" +\
                to_string(get_day(i_date) , "99") + "T" + s_time

        if res_line.ankunft == res_line.abreise:

            gstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)],"zinr": [(eq, res_line.zinr)],"gastnrmember": [(eq, res_line.gastnrmember)],"datum": [(eq, ci_date)]})

            if gstat:
                rsv_list.isdayuseincluded = "1"
        else:

            if ci_date == res_line.abreise:

                gstat = get_cache (Genstat, {"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)],"zinr": [(eq, res_line.zinr)],"gastnrmember": [(eq, res_line.gastnrmember)],"datum": [(eq, ci_date)]})

                if gstat:
                    rsv_list.isdayuseincluded = "1"

        if reservation:
            rsv_list.rsv_time = to_string(get_year(reservation.resdat) , "9999") + "-" + to_string(get_month(reservation.resdat) , "99") + "-" +\
                    to_string(get_day(reservation.resdat) , "99") + "T" + substring(res_line.reserve_char, 8, 5) + ":00"
            rsv_list.voucher = reservation.vesrdepot

        if res_line.resstatus == 1:
            rsv_list.rsv_type = "Guaranted"

        elif res_line.resstatus == 2:
            rsv_list.rsv_type = "6PM"

        elif res_line.resstatus == 3:
            rsv_list.rsv_type = "Tentative"

        elif res_line.resstatus == 5:
            rsv_list.rsv_type = "VerbalConfirm"
        else:
            rsv_list.rsv_type = ""

        if res_line.resstatus == 11 or res_line.resstatus == 13:
            rsv_list.guest_status = "roomsharer"
        else:
            rsv_list.guest_status = "mainguest"

        if res_line.resstatus == 9 or res_line.resstatus == 99:
            rsv_list.rsv_status = "cancel"

        elif res_line.resstatus == 6 or res_line.resstatus == 13:
            rsv_list.rsv_status = "Check-In"

        elif res_line.resstatus == 8:
            rsv_list.rsv_status = "Check-Out"

        elif res_line.resstatus == 10:
            rsv_list.rsv_status = "NoShow"
        else:
            rsv_list.rsv_status = ""

        if eta == "":
            rsv_list.eta = rsv_list.arr_date + "T" + "00:00:00"
        else:
            rsv_list.eta = rsv_list.arr_date + "T" + eta

        if etd == "":
            rsv_list.etd = rsv_list.dep_date + "T" + "00:00:00"
        else:
            rsv_list.etd = rsv_list.dep_date + "T" + etd
        rsv_list.ci_time = rsv_list.arr_date + "T" + to_string(res_line.ankzeit , "hh:mm:ss")
        rsv_list.co_time = rsv_list.dep_date + "T" + to_string(res_line.abreisezeit, "hh:mm:ss")

        if res_line.cancelled != None:
            canceldate = to_string(get_year(res_line.cancelled) , "9999") + to_string(get_month(res_line.cancelled) , "99") +\
                    to_string(get_day(res_line.cancelled) , "99")
            rsv_list.cancel_date = canceldate


        else:
            rsv_list.cancel_date = ""

        if matches(res_line.memozinr,r"*;*"):
            rsv_list.memo = entry(1, res_line.memozinr, ";")

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:

            guest_list = query(guest_list_data, filters=(lambda guest_list: guest_list.to_int(guest_list.gastnr) == guest.gastnr), first=True)

            if not guest_list:
                guest_list = Guest_list()
                guest_list_data.append(guest_list)


                nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

                if nation:
                    guest_list.nation = validate_field(nation.bezeich)

                if guest.modif_datum == None:
                    guest_list.modifydate = to_string(get_year(guest.anlage_datum) , "9999") + "-" + to_string(get_month(guest.anlage_datum) , "99") + "-" + to_string(get_day(guest.anlage_datum) , "99") + "T00:00:00"
                else:
                    guest_list.modifydate = to_string(get_year(guest.modif_datum) , "9999") + "-" + to_string(get_month(guest.modif_datum) , "99") + "-" + to_string(get_day(guest.modif_datum) , "99") + "T00:00:00"

                if reservation:
                    guest_list.mainsegment = validate_field(reservation.segmentcode)
                guest_list.vip = "0"

                for guestseg in db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == guest.gastnr)).order_by(Guestseg._recid).all():

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                    if segment and not matches(entry(0, segment.bezeich, "$$0"),r"*VIP*"):
                        guest_list.codes = guest_list.codes + entry(0, segment.bezeich, "$$0") + ";"

                    if matches(entry(0, segment.bezeich, "$$0"),r"*VIP*"):
                        guest_list.vip = "1"

                if guest.geburtdatum1 == None:
                    birthdate = ""
                else:
                    birthdate = to_string(get_year(guest.geburtdatum1) , "9999") + to_string(get_month(guest.geburtdatum1) , "99") + to_string(get_day(guest.geburtdatum1) , "99")

                if guest.geburtdatum2 == None:
                    expdate = ""
                else:
                    expdate = to_string(get_year(guest.geburtdatum2) , "9999") + to_string(get_month(guest.geburtdatum2) , "99") + to_string(get_day(guest.geburtdatum2) , "99")

                if guest.adresse1 != "" and guest.adresse2 != "":
                    address = guest.adresse1 + ',' + guest.adresse2

                elif guest.adresse1 != "" and guest.adresse2 == "":
                    address = guest.adresse1
                else:
                    address = ""
                guest_list.address = address
                guest_list.companyguestnr = ""
                guest_list.comments = guest.bemerkung

                if matches(guest_list.comments,r"*|*"):
                    guest_list.comments = replace_str(guest_list.comments, "|", "-")
                guest_list.gastnr = validate_field(to_string(guest.gastnr))
                guest_list.lastname = validate_field(guest.NAME)
                guest_list.firstname = validate_field(guest.vorname1)
                guest_list.city = validate_field(guest.wohnort)
                guest_list.prov = validate_field(guest.geburt_ort2)
                guest_list.zip = validate_field(guest.plz)
                guest_list.country = validate_field(guest.land)
                guest_list.birthplace = validate_field(guest.telex)
                guest_list.birthdate = validate_field(birthdate)
                guest_list.sex = validate_field(guest.geschlecht)
                guest_list.fax = validate_field(guest.fax)
                guest_list.email = validate_field(guest.email_adr)
                guest_list.occupation = validate_field(guest.beruf)
                guest_list.idcard_type = validate_field(guest.geburt_ort1)
                guest_list.idcard_exp = validate_field(expdate)
                guest_list.phone = validate_field(guest.telefon)
                guest_list.mobile = validate_field(guest.mobil_telefon)
                guest_list.idcard_nr = validate_field(guest.ausweis_nr1)
                guest_list.codes = validate_field(guest_list.codes)
                guest_list.address = validate_field(guest_list.address)
                guest_list.comments = validate_field(guest_list.comments)


    def add_line(s:string, line_nr:int):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        nitehist = get_cache (Nitehist, {"datum": [(eq, ci_date)],"reihenfolge": [(eq, reihenfolge)],"line_nr": [(eq, line_nr)]})

        if not nitehist:
            create_nitehis(line_nr, s)


    def create_nitehis(linenr:int, line_str:string):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data


        nitehist = Nitehist()
        db_session.add(nitehist)

        nitehist.datum = ci_date
        nitehist.reihenfolge = reihenfolge
        nitehist.line_nr = linenr
        nitehist.line = line_str


    def find_exrate(curr_date:date):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        foreign_nr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        if htparam.fchar != "":

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                foreign_nr = waehrung.waehrungsnr

        if foreign_nr != 0:

            exrate = get_cache (exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            exrate = get_cache (exrate, {"datum": [(eq, curr_date)]})


    def find_payable(fib:string, curr_val:Decimal, curr_taxed_val:Decimal, prev_val:Decimal):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        final_val = to_decimal("0.0")
        payable_sum = to_decimal("0.0")
        taxed_payable_sum = to_decimal("0.0")

        def generate_inner_output():
            return (final_val, payable_sum, taxed_payable_sum)

        payable_sum =  to_decimal("0")
        taxed_payable_sum =  to_decimal("0")

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fib)],"acc_type": [(ne, 4)]})

        if gl_acct:
            final_val =  to_decimal(prev_val) + to_decimal(curr_val)
        else:
            payable_sum =  to_decimal(payable_sum) + to_decimal(curr_val)
            final_val =  to_decimal(prev_val)

        return generate_inner_output()


    def find_gross(fib:string, n1_betrag:Decimal, prev_betrag:Decimal):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        rev_gross = to_decimal("0.0")

        def generate_inner_output():
            return (rev_gross)


        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fib)],"acc_type": [(ne, 4)]})

        if gl_acct:
            rev_gross =  to_decimal(prev_betrag) + to_decimal(n1_betrag)
        else:
            rev_gross =  to_decimal(prev_betrag)

        return generate_inner_output()


    def validate_field(str:string):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        outval = ""
        tempvar1:string = ""
        tempvar2:string = ""

        def generate_inner_output():
            return (outval)


        if str == None:
            str = ""
        outval = ""
        tempvar1 = str
        tempvar2 = replace_str(tempvar1, chr_unicode(10) , " ")
        tempvar2 = replace_str(tempvar1, chr_unicode(13) , " ")
        outval = tempvar2

        return generate_inner_output()


    def fill_persocc():

        nonlocal fr_date, fr_date1, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_data, guest_list_data, ta_list_data, arrangement_list_data, zimkateg_list_data, temp_gastnr_data, temp_reslin_queasy_data, segmentrevenue_data, totalsegmentsrevenue_data, totalroomrevenue_data, totalfbrevenue_data, totalotherrevenue_data, hotelnetrevenue_data, hotelgrossrevenue_data, totalroom_data, roomsavailable_data, roomsoccupied_data, houseuses_data, complimentaryrooms_data, roomspaying_data, vacantrooms_data, outoforderrooms_data, noshows_data, reservationmadetoday_data, cancellationfortoday_data, earlycheckout_data, roomarrivalstoday_data, personarrivalstoday_data, roomdeparturestoday_data, persondeparturestoday_data, roomarrivalstomorrow_data, personarrivalstomorrow_data, roomdeparturestomorrow_data, persondeparturestomorrow_data, roomtype_data, rate_list_data, w1_data, rsvdetails_data, rc_data, rmtyp_data, rooms_data, t_zimkateg_data, t_arrangement_data, t_qsy2_data, t_qsy18_data, t_qsy152_data, t_prmarket_data, temp_rc_data

        d_flag:bool = False
        foreign_nr:int = 0
        to_date:date = None
        jan1:date = None
        from_date:date = None
        datum1:date = None
        segmbuff = None
        statbuff = None
        Segmbuff =  create_buffer("Segmbuff",Segment)
        Statbuff =  create_buffer("Statbuff",Segmentstat)
        to_date = ci_date
        jan1 = date_mdy(1, 1, get_year(to_date))
        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= from_date) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():

                if segmentstat.datum == to_date:
                    w1.tday_saldo =  to_decimal(w1.tday_saldo) + to_decimal(segmentstat.persanz) +\
                            segmentstat.kind1 + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)


                w1.mtd_saldo =  to_decimal(w1.mtd_saldo) + to_decimal(segmentstat.persanz) +\
                        segmentstat.kind1 + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

            for statbuff in db_session.query(Statbuff).filter(
                     (Statbuff.datum >= jan1) & (Statbuff.datum <= to_date) & (Statbuff.segmentcode == segment.segmentcode)).order_by(Statbuff._recid).all():
                w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(statbuff.persanz) +\
                        statbuff.kind1 + to_decimal(statbuff.kind2) + to_decimal(statbuff.gratis)

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    for nitehist in db_session.query(Nitehist).filter(
             (Nitehist.datum == ci_date) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
        db_session.delete(nitehist)

    nitehist = get_cache (Nitehist, {"datum": [(eq, ci_date)],"reihenfolge": [(eq, reihenfolge)]})

    if nitehist:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
    gastnr_wi = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
    gastnr_ind = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    price_decimal = 2

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(Queasy._recid).all():
        t_qsy2 = T_qsy2()
        t_qsy2_data.append(t_qsy2)

        buffer_copy(queasy, t_qsy2)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 18)).order_by(Queasy._recid).all():
        t_qsy18 = T_qsy18()
        t_qsy18_data.append(t_qsy18)

        buffer_copy(queasy, t_qsy18)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy._recid).all():
        t_qsy152 = T_qsy152()
        t_qsy152_data.append(t_qsy152)

        buffer_copy(queasy, t_qsy152)

    for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
        t_arrangement = T_arrangement()
        t_arrangement_data.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_data.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

    for prmarket in db_session.query(Prmarket).order_by(Prmarket._recid).all():
        t_prmarket = T_prmarket()
        t_prmarket_data.append(t_prmarket)

        buffer_copy(prmarket, t_prmarket)

    reslin_queasy_obj_list = {}
    reslin_queasy = Reslin_queasy()
    res_line = Res_line()
    for reslin_queasy.char2, reslin_queasy.resnr, reslin_queasy.reslinnr, reslin_queasy.number2, reslin_queasy.char3, reslin_queasy._recid, res_line.resstatus, res_line.cancelled_id, res_line.ankunft, res_line.abreise, res_line.zimmer_wunsch, res_line.betriebsnr, res_line.reserve_dec, res_line._recid, res_line.resnr, res_line.reslinnr, res_line.zinr, res_line.zikatnr, res_line.arrangement, res_line.zimmeranz, res_line.reserve_char, res_line.gastnr, res_line.flight_nr, res_line.anztage, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.l_zuordnung, res_line.code, res_line.gastnrmember, res_line.storno_nr, res_line.stornogrund, res_line.active_flag, res_line.ankzeit, res_line.abreisezeit, res_line.cancelled, res_line.memozinr in db_session.query(Reslin_queasy.char2, Reslin_queasy.resnr, Reslin_queasy.reslinnr, Reslin_queasy.number2, Reslin_queasy.char3, Reslin_queasy._recid, Res_line.resstatus, Res_line.cancelled_id, Res_line.ankunft, Res_line.abreise, Res_line.zimmer_wunsch, Res_line.betriebsnr, Res_line.reserve_dec, Res_line._recid, Res_line.resnr, Res_line.reslinnr, Res_line.zinr, Res_line.zikatnr, Res_line.arrangement, Res_line.zimmeranz, Res_line.reserve_char, Res_line.gastnr, Res_line.flight_nr, Res_line.anztage, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.l_zuordnung, Res_line.code, Res_line.gastnrmember, Res_line.storno_nr, Res_line.stornogrund, Res_line.active_flag, Res_line.ankzeit, Res_line.abreisezeit, Res_line.cancelled, Res_line.memozinr).join(Res_line,(Res_line.resnr == Reslin_queasy.resnr) & (Res_line.reslinnr == Reslin_queasy.reslinnr) & (Res_line.ankunft != None) & (Res_line.abreise != None) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12)).filter(
             (Reslin_queasy.date2 == ci_date) & (Reslin_queasy.key == ("ResChanges").lower())).order_by(Reslin_queasy._recid).all():
        if reslin_queasy_obj_list.get(reslin_queasy._recid):
            continue
        else:
            reslin_queasy_obj_list[reslin_queasy._recid] = True

        temp_reslin_queasy = query(temp_reslin_queasy_data, filters=(lambda temp_reslin_queasy: temp_reslin_queasy.resnr == reslin_queasy.resnr and temp_reslin_queasy.reslinnr == reslin_queasy.reslinnr), first=True)

        if not temp_reslin_queasy:
            temp_reslin_queasy = Temp_reslin_queasy()
            temp_reslin_queasy_data.append(temp_reslin_queasy)

            temp_reslin_queasy.resnr = reslin_queasy.resnr
            temp_reslin_queasy.reslinnr = reslin_queasy.reslinnr
            temp_reslin_queasy.number2 = reslin_queasy.number2
            temp_reslin_queasy.modify_date = date_mdy(entry(23, reslin_queasy.char3, ";"))

    for res_line in db_session.query(Res_line).filter(
             (((Res_line.ankunft == ci_date) & (Res_line.active_flag == 1)) | ((Res_line.ankunft == ci_date) & (Res_line.active_flag == 2)) | ((Res_line.abreise == ci_date) & (Res_line.active_flag == 2)) | ((Res_line.cancelled == ci_date) & (Res_line.active_flag == 2)) | ((Res_line.ankunft == ci_date) & (Res_line.resstatus == 10)) | ((Res_line.cancelled == None) & (Res_line.active_flag == 2) & (Res_line.resstatus == 9))) & (Res_line.ankunft != None) & (Res_line.abreise != None) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():

        temp_reslin_queasy = query(temp_reslin_queasy_data, filters=(lambda temp_reslin_queasy: temp_reslin_queasy.resnr == res_line.resnr and temp_reslin_queasy.reslinnr == res_line.reslinnr), first=True)

        if not temp_reslin_queasy:
            temp_reslin_queasy = Temp_reslin_queasy()
            temp_reslin_queasy_data.append(temp_reslin_queasy)

            temp_reslin_queasy.resnr = res_line.resnr
            temp_reslin_queasy.reslinnr = res_line.reslinnr
            temp_reslin_queasy.modify_date = None

    res_line_obj_list = {}
    for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == temp_reslin_queasy.resnr)).filter(
             ((Res_line.resnr.in_(list(set([temp_reslin_queasy.resnr for temp_reslin_queasy in temp_reslin_queasy_data])))) & (Res_line.reslinnr == temp_reslin_queasy.reslinnr))).order_by(Res_line._recid).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True

        temp_reslin_queasy = query(temp_reslin_queasy_data, (lambda temp_reslin_queasy: (res_line.resnr == temp_reslin_queasy.resnr)), first=True)

        if temp_reslin_queasy.modify_date == None:

            if res_line.resstatus == 8:
                temp_reslin_queasy.modify_date = res_line.abreise
                temp_reslin_queasy.number2 = res_line.abreisezeit

            elif res_line.resstatus == 6 or res_line.resstatus == 13 or res_line.resstatus == 10:
                temp_reslin_queasy.modify_date = res_line.ankunft
                temp_reslin_queasy.number2 = res_line.ankzeit

            elif res_line.resstatus == 9 or res_line.resstatus == 99:
                temp_reslin_queasy.modify_date = res_line.cancelled
                temp_reslin_queasy.number2 = temp_reslin_queasy.number2


            else:
                temp_reslin_queasy.modify_date = reservation.resdat
                temp_reslin_queasy.number2 = temp_reslin_queasy.number2


        create_rsv_list(temp_reslin_queasy.resnr, temp_reslin_queasy.reslinnr, temp_reslin_queasy.modify_date, temp_reslin_queasy.number2)

    for t_arrangement in query(t_arrangement_data, filters=(lambda t_arrangement: t_arrangement.weeksplit != True)):
        arrangement_list = Arrangement_list()
        arrangement_list_data.append(arrangement_list)

        arrangement_list.arrangement = t_arrangement.arrangement
        arrangement_list.argt_bez = t_arrangement.argt_bez

    for t_zimkateg in query(t_zimkateg_data):
        zimkateg_list = Zimkateg_list()
        zimkateg_list_data.append(zimkateg_list)

        zimkateg_list.kurzbez = t_zimkateg.kurzbez
        zimkateg_list.bezeichnung = t_zimkateg.bezeichnung


    create_nitehis(0, "SEND|0")
    i_counter = 0

    for rsv_list in query(rsv_list_data, filters=(lambda rsv_list: rsv_list.resnr != "")):
        i_counter = i_counter + 1
        outstr = "RSV" + "|" + rsv_list.resnr + "|" + rsv_list.reslinnr + "|" + rsv_list.arr_date + "|" + rsv_list.dep_date + "|" + rsv_list.flight1 + "|" + rsv_list.flight2 + "|" + rsv_list.eta + "|" + rsv_list.etd + "|" + rsv_list.pickup + "|" + rsv_list.dropoff + "|" + rsv_list.nights + "|" + rsv_list.adults + "|" + rsv_list.childs + "|" + rsv_list.infants + "|" + rsv_list.infantage + "|" + rsv_list.comp + "|" + rsv_list.comp_ch + "|" + rsv_list.voucher + "|" + rsv_list.TA_code + "|" + rsv_list.ratecode + "|" + rsv_list.qty + "|" + rsv_list.roomcat + "|" + rsv_list.argt + "|" + rsv_list.curr + "|" + rsv_list.roomrate + "|" + rsv_list.roomcharge + "|" + rsv_list.roomtax + "|" + rsv_list.roomserv + "|" + rsv_list.room_bf + "|" + rsv_list.room_lunch + "|" + rsv_list.room_dinner + "|" + rsv_list.room_others + "|" + rsv_list.discount + "|" + rsv_list.commission + "|" + rsv_list.fixrate + "|" + rsv_list.billinstruction + "|" + rsv_list.purpose + "|" + rsv_list.memo + "|" + rsv_list.gastnrmember + "|" + rsv_list.guest_status + "|" + rsv_list.rsv_type + "|" + rsv_list.rsv_status + "|" + rsv_list.rsv_time + "|" + rsv_list.cancel_nr + "|" + rsv_list.cancel_date + "|" + rsv_list.cancel + "|" + rsv_list.co_time + "|" + rsv_list.ci_time + "|" + to_string(rsv_list.resstatus) + "|" + to_string(rsv_list.active_flag) + "|" + rsv_list.zinr + "|" + rsv_list.isdayuseincluded + "|" + rsv_list.modifydate
        add_line(outstr, i_counter)

    for guest_list in query(guest_list_data, filters=(lambda guest_list: guest_list.gastnr != "")):
        i_counter = i_counter + 1
        outstr = "GST" + "|" + guest_list.gastnr + "|" + guest_list.lastname + "|" + guest_list.firstname + "|" + guest_list.address + "|" + guest_list.city + "|" + guest_list.prov + "|" + guest_list.zip + "|" + guest_list.country + "|" + guest_list.birthplace + "|" + guest_list.birthdate + "|" + guest_list.sex + "|" + guest_list.phone + "|" + guest_list.mobile + "|" + guest_list.fax + "|" + guest_list.email + "|" + guest_list.occupation + "|" + guest_list.idcard_nr + "|" + guest_list.idcard_type + "|" + guest_list.idcard_exp + "|" + guest_list.companyguestnr + "|" + guest_list.mainsegment + "|" + guest_list.codes + "|" + guest_list.comments + "|" + guest_list.nation + "|" + guest_list.modifydate + "|" + guest_list.vip
        add_line(outstr, i_counter)

    for arrangement_list in query(arrangement_list_data):
        i_counter = i_counter + 1
        outstr = "ARG" + "|" + arrangement_list.arrangement + "|" + arrangement_list.argt_bez
        add_line(outstr, i_counter)

    for zimkateg_list in query(zimkateg_list_data):
        i_counter = i_counter + 1
        outstr = "ROM" + "|" + zimkateg_list.kurzbez + "|" + zimkateg_list.bezeichnung
        add_line(outstr, i_counter)
    fr_date = date_mdy(1, 1, get_year(ci_date))
    fr_date1 = date_mdy(get_month(ci_date) , 1, get_year(ci_date))
    anz0 = 0

    for segment in db_session.query(Segment).order_by(Segment._recid).all():
        segmentrevenue = Segmentrevenue()
        segmentrevenue_data.append(segmentrevenue)

        segmentrevenue.segmentcode = segment.segmentcode
        segmentrevenue.segmentdescription = segment.bezeich
        segmentrevenue.segmentcomment = segment.bemerkung


    roomsavailable = Roomsavailable()
    roomsavailable_data.append(roomsavailable)


    for zkstat in db_session.query(Zkstat).filter(
             (Zkstat.datum >= fr_date) & (Zkstat.datum <= ci_date)).order_by(Zkstat._recid).all():

        if zkstat.datum == ci_date:
            roomsavailable.day = roomsavailable.day + zkstat.anz100

        if get_month(zkstat.datum) == get_month(ci_date):
            roomsavailable.mtd = roomsavailable.mtd + zkstat.anz100
        roomsavailable.ytd = roomsavailable.ytd + zkstat.anz100

    for t_zimkateg in query(t_zimkateg_data):
        roomtype = Roomtype()
        roomtype_data.append(roomtype)

        roomtype.roomtypecode = t_zimkateg.kurzbez
        roomtype.roomtypedescription = t_zimkateg.bezeichnung


    totalsegmentsrevenue = Totalsegmentsrevenue()
    totalsegmentsrevenue_data.append(totalsegmentsrevenue)

    totalroomrevenue = Totalroomrevenue()
    totalroomrevenue_data.append(totalroomrevenue)

    totalfbrevenue = Totalfbrevenue()
    totalfbrevenue_data.append(totalfbrevenue)

    totalotherrevenue = Totalotherrevenue()
    totalotherrevenue_data.append(totalotherrevenue)

    hotelnetrevenue = Hotelnetrevenue()
    hotelnetrevenue_data.append(hotelnetrevenue)

    hotelgrossrevenue = Hotelgrossrevenue()
    hotelgrossrevenue_data.append(hotelgrossrevenue)

    roomsoccupied = Roomsoccupied()
    roomsoccupied_data.append(roomsoccupied)

    complimentaryrooms = Complimentaryrooms()
    complimentaryrooms_data.append(complimentaryrooms)

    roomspaying = Roomspaying()
    roomspaying_data.append(roomspaying)

    houseuses = Houseuses()
    houseuses_data.append(houseuses)

    noshows = Noshows()
    noshows_data.append(noshows)

    cancellationfortoday = Cancellationfortoday()
    cancellationfortoday_data.append(cancellationfortoday)

    outoforderrooms = Outoforderrooms()
    outoforderrooms_data.append(outoforderrooms)

    vacantrooms = Vacantrooms()
    vacantrooms_data.append(vacantrooms)

    reservationmadetoday = Reservationmadetoday()
    reservationmadetoday_data.append(reservationmadetoday)

    earlycheckout = Earlycheckout()
    earlycheckout_data.append(earlycheckout)

    roomarrivalstoday = Roomarrivalstoday()
    roomarrivalstoday_data.append(roomarrivalstoday)

    personarrivalstoday = Personarrivalstoday()
    personarrivalstoday_data.append(personarrivalstoday)

    roomdeparturestoday = Roomdeparturestoday()
    roomdeparturestoday_data.append(roomdeparturestoday)

    persondeparturestoday = Persondeparturestoday()
    persondeparturestoday_data.append(persondeparturestoday)

    roomarrivalstomorrow = Roomarrivalstomorrow()
    roomarrivalstomorrow_data.append(roomarrivalstomorrow)

    personarrivalstomorrow = Personarrivalstomorrow()
    personarrivalstomorrow_data.append(personarrivalstomorrow)

    roomdeparturestomorrow = Roomdeparturestomorrow()
    roomdeparturestomorrow_data.append(roomdeparturestomorrow)

    persondeparturestomorrow = Persondeparturestomorrow()
    persondeparturestomorrow_data.append(persondeparturestomorrow)

    totalroom = Totalroom()
    totalroom_data.append(totalroom)

    w1 = W1()
    w1_data.append(w1)

    fill_persocc()

    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.datum >= fr_date) & (Zinrstat.datum <= ci_date)).order_by(Zinrstat._recid).all():

        if zinrstat.zinr.lower()  == ("tot-rm").lower() :

            if zinrstat.datum == ci_date:
                totalroom.day = totalroom.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                totalroom.mtd = totalroom.mtd + zinrstat.zimmeranz
            totalroom.ytd = totalroom.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("No-Show").lower() :

            if zinrstat.datum == ci_date:
                noshows.day = noshows.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                noshows.mtd = noshows.mtd + zinrstat.zimmeranz
            noshows.ytd = noshows.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("cancRes").lower() :

            if zinrstat.datum == ci_date:
                cancellationfortoday.day = cancellationfortoday.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                cancellationfortoday.mtd = cancellationfortoday.mtd + zinrstat.zimmeranz
            cancellationfortoday.ytd = cancellationfortoday.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("ooo").lower() :

            if zinrstat.datum == ci_date:
                outoforderrooms.day = outoforderrooms.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                outoforderrooms.mtd = outoforderrooms.mtd + zinrstat.zimmeranz
            outoforderrooms.ytd = outoforderrooms.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("vacant").lower() :

            if zinrstat.datum == ci_date:
                vacantrooms.day = vacantrooms.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                vacantrooms.mtd = vacantrooms.mtd + zinrstat.zimmeranz
            vacantrooms.ytd = vacantrooms.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("NewRes").lower() :

            if zinrstat.datum == ci_date:
                reservationmadetoday.day = reservationmadetoday.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                reservationmadetoday.mtd = reservationmadetoday.mtd + zinrstat.zimmeranz
            reservationmadetoday.ytd = reservationmadetoday.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("Early-CO").lower() :

            if zinrstat.datum == ci_date:
                earlycheckout.day = earlycheckout.day + zinrstat.zimmeranz

            if get_month(zinrstat.datum) == get_month(ci_date):
                earlycheckout.mtd = earlycheckout.mtd + zinrstat.zimmeranz
            earlycheckout.ytd = earlycheckout.ytd + zinrstat.zimmeranz

        elif zinrstat.zinr.lower()  == ("Arrival").lower() :

            if zinrstat.datum == ci_date:
                roomarrivalstoday.day = roomarrivalstoday.day + zinrstat.zimmeranz
                personarrivalstoday.day = personarrivalstoday.day + zinrstat.personen

            if get_month(zinrstat.datum) == get_month(ci_date):
                roomarrivalstoday.mtd = roomarrivalstoday.mtd + zinrstat.zimmeranz
                personarrivalstoday.mtd = personarrivalstoday.mtd + zinrstat.personen


            roomarrivalstoday.ytd = roomarrivalstoday.ytd + zinrstat.zimmeranz


            personarrivalstoday.ytd = personarrivalstoday.ytd + zinrstat.personen

        elif zinrstat.zinr.lower()  == ("ArrTmrw").lower() :

            if zinrstat.datum == ci_date:
                roomarrivalstomorrow.day = roomarrivalstomorrow.day + zinrstat.zimmeranz
                personarrivalstomorrow.day = personarrivalstomorrow.day + zinrstat.personen

            if get_month(zinrstat.datum) == get_month(ci_date):
                roomarrivalstomorrow.mtd = roomarrivalstomorrow.mtd + zinrstat.zimmeranz
                personarrivalstomorrow.mtd = personarrivalstomorrow.mtd + zinrstat.personen


            roomarrivalstomorrow.ytd = roomarrivalstomorrow.ytd + zinrstat.zimmeranz


            personarrivalstomorrow.ytd = personarrivalstomorrow.ytd + zinrstat.personen

        elif zinrstat.zinr.lower()  == ("Departure").lower() :

            if zinrstat.datum == ci_date:
                roomdeparturestoday.day = roomdeparturestoday.day + zinrstat.zimmeranz
                persondeparturestoday.day = persondeparturestoday.day + zinrstat.personen

            if get_month(zinrstat.datum) == get_month(ci_date):
                roomdeparturestoday.mtd = roomdeparturestoday.mtd + zinrstat.zimmeranz
                persondeparturestoday.mtd = persondeparturestoday.mtd + zinrstat.personen


            roomdeparturestoday.ytd = roomdeparturestoday.ytd + zinrstat.zimmeranz
            persondeparturestoday.ytd = persondeparturestoday.ytd + zinrstat.personen

        elif zinrstat.zinr.lower()  == ("DepTmrw").lower() :

            if zinrstat.datum == ci_date:
                roomdeparturestomorrow.day = roomdeparturestomorrow.day + zinrstat.zimmeranz
                persondeparturestomorrow.day = persondeparturestomorrow.day + zinrstat.personen

            if get_month(zinrstat.datum) == get_month(ci_date):
                roomdeparturestomorrow.mtd = roomdeparturestomorrow.mtd + zinrstat.zimmeranz
                persondeparturestomorrow.mtd = persondeparturestomorrow.mtd + zinrstat.personen


            roomdeparturestomorrow.ytd = roomdeparturestomorrow.ytd + zinrstat.zimmeranz
            persondeparturestomorrow.ytd = persondeparturestomorrow.ytd + zinrstat.personen

    genstat_obj_list = {}
    for genstat, segment, zimkateg in db_session.query(Genstat, Segment, Zimkateg).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
             (Genstat.datum >= fr_date) & (Genstat.datum <= ci_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
        if genstat_obj_list.get(genstat._recid):
            continue
        else:
            genstat_obj_list[genstat._recid] = True

        segmentrevenue = query(segmentrevenue_data, filters=(lambda segmentrevenue: segmentrevenue.segmentRevenue.segmentcode == genstat.segmentcode), first=True)

        roomtype = query(roomtype_data, filters=(lambda roomtype: roomtype.roomType.RoomTypeCode == zimkateg.kurzbez), first=True)

        if genstat.datum == ci_date:

            if roomtype:
                roomtype.todayroomnight = roomtype.todayroomnight + 1
                roomtype.todayrevenue =  to_decimal(roomtype.todayrevenue) + to_decimal(genstat.logis)

            if segmentrevenue:
                segmentrevenue.todayroomnight = segmentrevenue.todayroomnight + 1
                segmentrevenue.todayrevenue =  to_decimal(segmentrevenue.todayrevenue) + to_decimal(genstat.logis)

            if segment.betriebsnr == 0:
                roomspaying.day = roomspaying.day + 1

            elif segment.betriebsnr == 1:
                complimentaryrooms.day = complimentaryrooms.day + 1

            elif segment.betriebsnr == 2:
                houseuses.day = houseuses.day + 1
            totalsegmentsrevenue.day =  to_decimal(totalsegmentsrevenue.day) + to_decimal(segmentrevenue.TodayRevenue)
            roomsoccupied.day = roomsoccupied.day + 1

        if get_month(genstat.datum) == get_month(ci_date):

            if roomtype:
                roomtype.mtdroomnight = roomtype.mtdroomnight + 1
                roomtype.mtdrevenue =  to_decimal(roomtype.mtdrevenue) + to_decimal(genstat.logis)

            if segmentrevenue:
                segmentrevenue.mtdroomnight = segmentrevenue.mtdroomnight + 1
                segmentrevenue.mtdrevenue =  to_decimal(segmentrevenue.mtdrevenue) + to_decimal(genstat.logis)

            if segment.betriebsnr == 0:
                roomspaying.mtd = roomspaying.mtd + 1

            elif segment.betriebsnr == 1:
                complimentaryrooms.mtd = complimentaryrooms.mtd + 1

            elif segment.betriebsnr == 2:
                houseuses.mtd = houseuses.mtd + 1
            totalsegmentsrevenue.mtd =  to_decimal(totalsegmentsrevenue.mtd) + to_decimal(segmentrevenue.MTDRevenue)
            roomsoccupied.mtd = roomsoccupied.mtd + 1

        if roomtype:
            roomtype.ytdroomnight = roomtype.ytdroomnight + 1
            roomtype.ytdrevenue =  to_decimal(roomtype.ytdrevenue) + to_decimal(genstat.logis)

        if segmentrevenue:
            segmentrevenue.ytdroomnight = segmentrevenue.ytdroomnight + 1
            segmentrevenue.ytdrevenue =  to_decimal(segmentrevenue.ytdrevenue) + to_decimal(genstat.logis)

        if segment.betriebsnr == 0:
            roomspaying.ytd = roomspaying.ytd + 1

        elif segment.betriebsnr == 1:
            complimentaryrooms.ytd = complimentaryrooms.ytd + 1

        elif segment.betriebsnr == 2:
            houseuses.ytd = houseuses.ytd + 1
        totalsegmentsrevenue.ytd =  to_decimal(totalsegmentsrevenue.ytd) + to_decimal(segmentrevenue.YTDRevenue)
        roomsoccupied.ytd = roomsoccupied.ytd + 1

    for segmentstat in db_session.query(Segmentstat).filter(
             (Segmentstat.datum >= fr_date1) & (Segmentstat.datum <= ci_date)).order_by(Segmentstat._recid).all():

        segmentrevenue = query(segmentrevenue_data, filters=(lambda segmentrevenue: segmentrevenue.SegmentRevenue.segmentcode == segmentstat.segmentcode), first=True)

        if segmentrevenue:
            segmentrevenue.budget =  to_decimal(segmentrevenue.budget) + to_decimal(segmentstat.budlogis)


        totalsegmentsrevenue.budget =  to_decimal(totalsegmentsrevenue.budget) + to_decimal(segmentstat.budlogis)

    for segmentrevenue in query(segmentrevenue_data):

        if totalsegmentsrevenue.DAY != 0:
            segmentrevenue.todayrevenuepercentage =  to_decimal(segmentrevenue.TodayRevenue) / to_decimal(totalsegmentsrevenue.DAY) * to_decimal("100")
        else:
            segmentrevenue.todayrevenuepercentage =  to_decimal("0")

        if totalsegmentsrevenue.MTD != 0:
            segmentrevenue.mtdrevenuepercentage =  to_decimal(segmentrevenue.MTDRevenue) / to_decimal(totalsegmentsrevenue.MTD) * to_decimal("100")
        else:
            segmentrevenue.mtdrevenuepercentage =  to_decimal("0")

        if totalsegmentsrevenue.YTD != 0:
            segmentrevenue.ytdrevenuepercentage =  to_decimal(segmentrevenue.YTDRevenue) / to_decimal(totalsegmentsrevenue.YTD) * to_decimal("100")
        else:
            segmentrevenue.ytdrevenuepercentage =  to_decimal("0")
        segmentrevenue.variance =  to_decimal(segmentrevenue.MTDRevenue) - to_decimal(segmentrevenue.Budget)

    umsatz_obj_list = {}
    umsatz = Umsatz()
    artikel = Artikel()
    for umsatz.artnr, umsatz.departement, umsatz.datum, umsatz.betrag, umsatz._recid, artikel.service_code, artikel.mwst_code, artikel.artart, artikel.fibukonto, artikel.umsatzart, artikel.departement, artikel._recid in db_session.query(Umsatz.artnr, Umsatz.departement, Umsatz.datum, Umsatz.betrag, Umsatz._recid, Artikel.service_code, Artikel.mwst_code, Artikel.artart, Artikel.fibukonto, Artikel.umsatzart, Artikel.departement, Artikel._recid).join(Artikel,(Artikel.artnr == Umsatz.artnr) & (Artikel.departement == Umsatz.departement)).filter(
             (Umsatz.datum >= fr_date) & (Umsatz.datum <= ci_date)).order_by(Umsatz._recid).all():
        if umsatz_obj_list.get(umsatz._recid):
            continue
        else:
            umsatz_obj_list[umsatz._recid] = True

        budget = get_cache (Budget, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)],"datum": [(eq, umsatz.datum)]})
        service, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
        fact =  to_decimal(1.00) + to_decimal(service) + to_decimal(vat)
        n_betrag =  to_decimal("0")
        n1_betrag =  to_decimal("0")
        frate =  to_decimal("1")

        if foreign_flag:
            find_exrate(umsatz.datum)

            if exrate:
                frate =  to_decimal(exrate.betrag)
        n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
        n_betrag = to_decimal(round(n_betrag , price_decimal))
        n1_betrag =  to_decimal(umsatz.betrag) / to_decimal((frate) )
        n1_betrag = to_decimal(round(n1_betrag , price_decimal))

        if umsatz.datum == ci_date and artikel.artart != 9:

            if artikel.umsatzart == 1:
                totalroomrevenue.day, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalroomrevenue.day)
                rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)

            elif artikel.umsatzart == 4:

                if artikel.departement >= 1:

                    buffart = db_session.query(Buffart).filter(
                             (Buffart.departement == umsatz.departement) & ((Buffart.umsatzart == 5) | (Buffart.umsatzart == 6))).first()

                    if buffart:
                        totalfbrevenue.day, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.day)
                        rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)
                    else:
                        totalotherrevenue.day, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalotherrevenue.day)
                        rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)

                elif artikel.departement == 0:
                    totalotherrevenue.day, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalotherrevenue.day)
                    rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)

            elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
                totalfbrevenue.day, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.day)
                rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)
            tot_payables1 =  to_decimal(tot_payables1) + to_decimal(payable_sum)

        if get_month(umsatz.datum) == get_month(ci_date):

            if budget and artikel.umsatzart == 1:
                totalroomrevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, totalroomrevenue.Budget)
                rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)

            elif budget and artikel.umsatzart == 4:

                if artikel.departement >= 1:

                    buffart = db_session.query(Buffart).filter(
                             ((Buffart.umsatzart == 5) & (Buffart.departement == umsatz.departement)) | ((Buffart.umsatzart == 6) & (Buffart.departement == umsatz.departement))).first()

                    if buffart:
                        totalfbrevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.Budget)
                        rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)
                    else:
                        totalotherrevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, totalotherrevenue.Budget)
                        rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)

                elif artikel.departement == 0:
                    totalotherrevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, totalotherrevenue.Budget)
                    rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)

            elif budget and (artikel.umsatzart == 5 or artikel.umsatzart == 6):
                totalfbrevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, totalfbrevenue.Budget)
                rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)
            tot_payables2 =  to_decimal(tot_payables2) + to_decimal(payable_sum)

            if artikel.umsatzart == 1:
                totalroomrevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalroomrevenue.mtd)
                rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)

            elif artikel.umsatzart == 4:

                if artikel.departement >= 1:

                    buffart = db_session.query(Buffart).filter(
                             ((Buffart.umsatzart == 5) & (Buffart.departement == umsatz.departement)) | ((Buffart.umsatzart == 6) & (Buffart.departement == umsatz.departement))).first()

                    if buffart:
                        totalfbrevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.mtd)
                        rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)
                    else:
                        totalotherrevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalotherrevenue.mtd)
                        rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)

                elif artikel.departement == 0:
                    totalotherrevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalotherrevenue.mtd)
                    rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)

            elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
                totalfbrevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.mtd)
                rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)
            tot_payables3 =  to_decimal(tot_payables3) + to_decimal(payable_sum)

        if artikel.umsatzart == 1:
            totalroomrevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalroomrevenue.ytd)
            rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)

        elif artikel.umsatzart == 4:

            if artikel.departement >= 1:

                buffart = db_session.query(Buffart).filter(
                         ((Buffart.umsatzart == 5) & (Buffart.departement == umsatz.departement)) | ((Buffart.umsatzart == 6) & (Buffart.departement == umsatz.departement))).first()

                if buffart:
                    totalfbrevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.ytd)
                    rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)
                else:
                    totalotherrevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalotherrevenue.ytd)
                    rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)

            elif artikel.departement == 0:
                totalotherrevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalotherrevenue.ytd)
                rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)

        elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
            totalfbrevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, totalfbrevenue.ytd)
            rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)
        tot_payables4 =  to_decimal(tot_payables4) + to_decimal(payable_sum)


    hotelnetrevenue.day =  to_decimal(totalroomrevenue.DAY) + to_decimal(totalfbrevenue.DAY) + to_decimal(totalotherrevenue.DAY)
    hotelgrossrevenue.day =  to_decimal(rev_gross_day)
    hotelnetrevenue.budget =  to_decimal(totalroomrevenue.Budget) + to_decimal(totalfbrevenue.Budget) + to_decimal(totalotherrevenue.Budget)
    hotelgrossrevenue.budget =  to_decimal(rev_gross_bud)
    hotelnetrevenue.mtd =  to_decimal(totalroomrevenue.mtd) + to_decimal(totalfbrevenue.mtd) + to_decimal(totalotherrevenue.mtd)
    hotelgrossrevenue.mtd =  to_decimal(rev_gross_mtd)
    hotelnetrevenue.ytd =  to_decimal(totalroomrevenue.ytd) + to_decimal(totalfbrevenue.ytd) + to_decimal(totalotherrevenue.ytd)
    hotelgrossrevenue.ytd =  to_decimal(rev_gross_ytd)

    if hotelnetrevenue.DAY != 0:
        totalsegmentsrevenue.todaypercentage =  to_decimal(totalsegmentsrevenue.DAY) / to_decimal(hotelnetrevenue.DAY) * to_decimal("100")
    else:
        totalsegmentsrevenue.todaypercentage =  to_decimal("0")

    if hotelnetrevenue.mtd != 0:
        totalsegmentsrevenue.mtdpercentage =  to_decimal(totalsegmentsrevenue.mtd) / to_decimal(hotelnetrevenue.mtd) * to_decimal("100")
    else:
        totalsegmentsrevenue.mtdpercentage =  to_decimal("0")

    if hotelnetrevenue.ytd != 0:
        totalsegmentsrevenue.ytdpercentage =  to_decimal(totalsegmentsrevenue.ytd) / to_decimal(hotelnetrevenue.ytd) * to_decimal("100")
    else:
        totalsegmentsrevenue.ytdpercentage =  to_decimal("0")

    if hotelnetrevenue.DAY != 0:
        totalroomrevenue.todaypercentage =  to_decimal(totalroomrevenue.DAY) / to_decimal(hotelnetrevenue.DAY) * to_decimal("100")
    else:
        totalroomrevenue.todaypercentage =  to_decimal("0")

    if hotelnetrevenue.mtd != 0:
        totalroomrevenue.mtdpercentage =  to_decimal(totalroomrevenue.mtd) / to_decimal(hotelnetrevenue.mtd) * to_decimal("100")
    else:
        totalroomrevenue.mtdpercentage =  to_decimal("0")

    if hotelnetrevenue.Ytd != 0:
        totalroomrevenue.ytdpercentage =  to_decimal(totalroomrevenue.Ytd) / to_decimal(hotelnetrevenue.ytd) * to_decimal("100")
    else:
        totalroomrevenue.ytdpercentage =  to_decimal("0")

    if hotelnetrevenue.DAY != 0:
        totalfbrevenue.todaypercentage =  to_decimal(totalfbrevenue.DAY) / to_decimal(hotelnetrevenue.DAY) * to_decimal("100")
    else:
        totalfbrevenue.todaypercentage =  to_decimal("0")

    if hotelnetrevenue.mtd != 0:
        totalfbrevenue.mtdpercentage =  to_decimal(totalfbrevenue.mtd) / to_decimal(hotelnetrevenue.mtd) * to_decimal("100")
    else:
        totalfbrevenue.mtdpercentage =  to_decimal("0")

    if hotelnetrevenue.Ytd != 0:
        totalfbrevenue.ytdpercentage =  to_decimal(totalfbrevenue.Ytd) / to_decimal(hotelnetrevenue.ytd) * to_decimal("100")
    else:
        totalfbrevenue.ytdpercentage =  to_decimal("0")

    if hotelnetrevenue.DAY != 0:
        totalotherrevenue.todaypercentage =  to_decimal(totalotherrevenue.DAY) / to_decimal(hotelnetrevenue.DAY) * to_decimal("100")
    else:
        totalotherrevenue.todaypercentage =  to_decimal("0")

    if hotelnetrevenue.mtd != 0:
        totalotherrevenue.mtdpercentage =  to_decimal(totalotherrevenue.mtd) / to_decimal(hotelnetrevenue.mtd) * to_decimal("100")
    else:
        totalotherrevenue.mtdpercentage =  to_decimal("0")

    if hotelnetrevenue.Ytd != 0:
        totalotherrevenue.ytdpercentage =  to_decimal(totalotherrevenue.Ytd) / to_decimal(hotelnetrevenue.ytd) * to_decimal("100")
    else:
        totalotherrevenue.ytdpercentage =  to_decimal("0")

    if hotelnetrevenue.DAY != 0:
        hotelnetrevenue.todaypercentage =  to_decimal(hotelnetrevenue.DAY) / to_decimal(hotelnetrevenue.DAY) * to_decimal("100")
    else:
        hotelnetrevenue.todaypercentage =  to_decimal("0")

    if hotelnetrevenue.mtd != 0:
        hotelnetrevenue.mtdpercentage =  to_decimal(hotelnetrevenue.mtd) / to_decimal(hotelnetrevenue.mtd) * to_decimal("100")
    else:
        hotelnetrevenue.mtdpercentage =  to_decimal("0")

    if hotelnetrevenue.ytd != 0:
        hotelnetrevenue.ytdpercentage =  to_decimal(hotelnetrevenue.ytd) / to_decimal(hotelnetrevenue.ytd) * to_decimal("100")
    else:
        hotelnetrevenue.ytdpercentage =  to_decimal("0")

    if hotelnetrevenue.DAY != 0:
        hotelgrossrevenue.todaypercentage =  to_decimal(hotelgrossrevenue.DAY) / to_decimal(hotelnetrevenue.DAY) * to_decimal("100")
    else:
        hotelgrossrevenue.todaypercentage =  to_decimal("0")

    if hotelnetrevenue.mtd != 0:
        hotelgrossrevenue.mtdpercentage =  to_decimal(hotelgrossrevenue.mtd) / to_decimal(hotelnetrevenue.mtd) * to_decimal("100")
    else:
        hotelgrossrevenue.mtdpercentage =  to_decimal("0")

    if hotelnetrevenue.ytd != 0:
        hotelgrossrevenue.ytdpercentage =  to_decimal(hotelgrossrevenue.ytd) / to_decimal(hotelnetrevenue.ytd) * to_decimal("100")
    else:
        hotelgrossrevenue.ytdpercentage =  to_decimal("0")
    totalsegmentsrevenue.variance =  to_decimal(totalsegmentsrevenue.mtd) - to_decimal(totalsegmentsrevenue.Budget)
    totalroomrevenue.variance =  to_decimal(totalroomrevenue.mtd) - to_decimal(totalroomrevenue.Budget)
    totalfbrevenue.variance =  to_decimal(totalfbrevenue.mtd) - to_decimal(totalfbrevenue.Budget)
    totalotherrevenue.variance =  to_decimal(totalotherrevenue.mtd) - to_decimal(totalotherrevenue.Budget)
    hotelnetrevenue.variance =  to_decimal(hotelnetrevenue.mtd) - to_decimal(hotelnetrevenue.Budget)
    hotelgrossrevenue.variance =  to_decimal(hotelgrossrevenue.mtd) - to_decimal(hotelgrossrevenue.Budget)

    for rate_list in query(rate_list_data):
        i_counter = i_counter + 1
        outstr = "RATE" + "|" + rate_list.code + "|" + rate_list.bezeich
        add_line(outstr, i_counter)

    for ta_list in query(ta_list_data):
        i_counter = i_counter + 1
        outstr = "TravelAgent" + "|" + ta_list.gastnr + "|" + ta_list.name + "|" + ta_list.ta_title + "|" + ta_list.address + "|" + ta_list.city + "|" + ta_list.zip + "|" + ta_list.country + "|" + ta_list.phone + "|" + ta_list.telefax + "|" + ta_list.email + "|" + ta_list.ratecode + "|" + ta_list.mainsegment + "|" + ta_list.booksource + "|" + ta_list.comment + "|" + ta_list.refno + "|" + ta_list.iscompany
        add_line(outstr, i_counter)

    for segmentrevenue in query(segmentrevenue_data):
        i_counter = i_counter + 1
        outstr = "SEGREV" + "|" + to_string(segmentrevenue.segmentCode) + "|" + segmentrevenue.SegmentDescription + "|" + to_string(segmentrevenue.TodayRoomNight) + "|" + dec2char (segmentrevenue.TodayRevenue) + "|" + dec2char (segmentrevenue.TodayRevenuePercentage) + "|" + to_string(segmentrevenue.MTDRoomNight) + "|" + dec2char (segmentrevenue.MTDRevenue) + "|" + dec2char (segmentrevenue.MTDRevenuePercentage) + "|" + to_string(segmentrevenue.YTDRoomNight) + "|" + dec2char (segmentrevenue.YTDRevenue) + "|" + dec2char (segmentrevenue.YTDRevenuePercentage) + "|" + dec2char (segmentrevenue.Budget) + "|" + dec2char (segmentrevenue.Variance) + "|" + segmentrevenue.SegmentComment
        add_line(outstr, i_counter)

    totalsegmentsrevenue = query(totalsegmentsrevenue_data, first=True)

    if totalsegmentsrevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-SEGMENT" + "|" + dec2char (totalsegmentsrevenue.DAY) + "|" +\
                dec2char (totalsegmentsrevenue.TodayPercentage) + "|" + dec2char (totalsegmentsrevenue.MTD) + "|" +\
                dec2char (totalsegmentsrevenue.MTDPercentage) + "|" + dec2char (totalsegmentsrevenue.YTD) + "|" +\
                dec2char (totalsegmentsrevenue.YTDPercentage) + "|" + dec2char (totalsegmentsrevenue.Budget) + "|" +\
                dec2char (totalsegmentsrevenue.Variance)


        add_line(outstr, i_counter)

    totalroomrevenue = query(totalroomrevenue_data, first=True)

    if totalroomrevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-ROOMREV" + "|" + dec2char (totalroomrevenue.DAY) + "|" +\
                dec2char (totalroomrevenue.TodayPercentage) + "|" + dec2char (totalroomrevenue.MTD) + "|" +\
                dec2char (totalroomrevenue.MTDPercentage) + "|" + dec2char (totalroomrevenue.YTD) + "|" +\
                dec2char (totalroomrevenue.YTDPercentage) + "|" + dec2char (totalroomrevenue.Budget) + "|" +\
                dec2char (totalroomrevenue.Variance)


        add_line(outstr, i_counter)

    totalfbrevenue = query(totalfbrevenue_data, first=True)

    if totalfbrevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-FBREV" + "|" + dec2char (totalfbrevenue.DAY) + "|" +\
                dec2char (totalfbrevenue.TodayPercentage) + "|" + dec2char (totalfbrevenue.MTD) + "|" +\
                dec2char (totalfbrevenue.MTDPercentage) + "|" + dec2char (totalfbrevenue.YTD) + "|" +\
                dec2char (totalfbrevenue.YTDPercentage) + "|" + dec2char (totalfbrevenue.Budget) + "|" +\
                dec2char (totalfbrevenue.Variance)


        add_line(outstr, i_counter)

    totalotherrevenue = query(totalotherrevenue_data, first=True)

    if totalotherrevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-otherrev" + "|" + dec2char (totalotherrevenue.DAY) + "|" +\
                dec2char (totalotherrevenue.TodayPercentage) + "|" + dec2char (totalotherrevenue.MTD) + "|" +\
                dec2char (totalotherrevenue.MTDPercentage) + "|" + dec2char (totalotherrevenue.YTD) + "|" +\
                dec2char (totalotherrevenue.YTDPercentage) + "|" + dec2char (totalotherrevenue.Budget) + "|" +\
                dec2char (totalotherrevenue.Variance)


        add_line(outstr, i_counter)

    hotelnetrevenue = query(hotelnetrevenue_data, first=True)

    if hotelnetrevenue:
        i_counter = i_counter + 1
        outstr = "NETREV" + "|" + dec2char (hotelnetrevenue.DAY) + "|" +\
                dec2char (hotelnetrevenue.TodayPercentage) + "|" + dec2char (hotelnetrevenue.MTD) + "|" +\
                dec2char (hotelnetrevenue.MTDPercentage) + "|" + dec2char (hotelnetrevenue.YTD) + "|" +\
                dec2char (hotelnetrevenue.YTDPercentage) + "|" + dec2char (hotelnetrevenue.Budget) + "|" +\
                dec2char (hotelnetrevenue.Variance)


        add_line(outstr, i_counter)

    hotelgrossrevenue = query(hotelgrossrevenue_data, first=True)

    if hotelgrossrevenue:
        i_counter = i_counter + 1
        outstr = "GROSSREV" + "|" + dec2char (hotelgrossrevenue.DAY) + "|" +\
                dec2char (hotelgrossrevenue.TodayPercentage) + "|" + dec2char (hotelgrossrevenue.MTD) + "|" +\
                dec2char (hotelgrossrevenue.MTDPercentage) + "|" + dec2char (hotelgrossrevenue.YTD) + "|" +\
                dec2char (hotelgrossrevenue.YTDPercentage) + "|" + dec2char (hotelgrossrevenue.Budget) + "|" +\
                dec2char (hotelgrossrevenue.Variance)


        add_line(outstr, i_counter)

    totalroom = query(totalroom_data, first=True)

    if totalroom:
        i_counter = i_counter + 1
        outstr = "TOTAL-ROOM" + "|" + to_string(totalroom.DAY) + "|" +\
                to_string(totalroom.MTD) + "|" + to_string(totalroom.YTD)


        add_line(outstr, i_counter)

    roomsavailable = query(roomsavailable_data, first=True)

    if roomsavailable:
        i_counter = i_counter + 1
        outstr = "ROOM-AVAIL" + "|" + to_string(roomsavailable.DAY) + "|" +\
                to_string(roomsavailable.MTD) + "|" + to_string(roomsavailable.YTD)


        add_line(outstr, i_counter)

    roomsoccupied = query(roomsoccupied_data, first=True)

    if roomsoccupied:
        i_counter = i_counter + 1
        outstr = "ROOM-OCC" + "|" + to_string(roomsoccupied.DAY) + "|" +\
                to_string(roomsoccupied.MTD) + "|" + to_string(roomsoccupied.YTD)


        add_line(outstr, i_counter)

    houseuses = query(houseuses_data, first=True)

    if houseuses:
        i_counter = i_counter + 1
        outstr = "HOUSE-USE" + "|" + to_string(houseuses.DAY) + "|" +\
                to_string(houseuses.MTD) + "|" + to_string(houseuses.YTD)


        add_line(outstr, i_counter)

    complimentaryrooms = query(complimentaryrooms_data, first=True)

    if complimentaryrooms:
        i_counter = i_counter + 1
        outstr = "COMP-ROOM" + "|" + to_string(complimentaryrooms.DAY) + "|" +\
                to_string(complimentaryrooms.MTD) + "|" + to_string(complimentaryrooms.YTD)


        add_line(outstr, i_counter)

    roomspaying = query(roomspaying_data, first=True)

    if roomspaying:
        i_counter = i_counter + 1
        outstr = "PAY-ROOM" + "|" + to_string(roomspaying.DAY) + "|" +\
                to_string(roomspaying.MTD) + "|" + to_string(roomspaying.YTD)


        add_line(outstr, i_counter)

    vacantrooms = query(vacantrooms_data, first=True)

    if vacantrooms:
        i_counter = i_counter + 1
        outstr = "VACANT-ROOM" + "|" + to_string(vacantrooms.DAY) + "|" +\
                to_string(vacantrooms.MTD) + "|" + to_string(vacantrooms.YTD)


        add_line(outstr, i_counter)

    outoforderrooms = query(outoforderrooms_data, first=True)

    if outoforderrooms:
        i_counter = i_counter + 1
        outstr = "OOO-ROOM" + "|" + to_string(outoforderrooms.DAY) + "|" +\
                to_string(outoforderrooms.MTD) + "|" + to_string(outoforderrooms.YTD)


        add_line(outstr, i_counter)

    noshows = query(noshows_data, first=True)

    if noshows:
        i_counter = i_counter + 1
        outstr = "NO-SHOW" + "|" + to_string(noshows.DAY) + "|" +\
                to_string(noshows.MTD) + "|" + to_string(noshows.YTD)


        add_line(outstr, i_counter)

    reservationmadetoday = query(reservationmadetoday_data, first=True)

    if reservationmadetoday:
        i_counter = i_counter + 1
        outstr = "RSV-TODAY" + "|" + to_string(reservationmadetoday.DAY) + "|" +\
                to_string(reservationmadetoday.MTD) + "|" + to_string(reservationmadetoday.YTD)


        add_line(outstr, i_counter)

    cancellationfortoday = query(cancellationfortoday_data, first=True)

    if cancellationfortoday:
        i_counter = i_counter + 1
        outstr = "CANCEL-TODAY" + "|" + to_string(cancellationfortoday.DAY) + "|" +\
                to_string(cancellationfortoday.MTD) + "|" + to_string(cancellationfortoday.YTD)


        add_line(outstr, i_counter)

    earlycheckout = query(earlycheckout_data, first=True)

    if earlycheckout:
        i_counter = i_counter + 1
        outstr = "EARLY-CO" + "|" + to_string(earlycheckout.DAY) + "|" +\
                to_string(earlycheckout.MTD) + "|" + to_string(earlycheckout.YTD)


        add_line(outstr, i_counter)

    roomarrivalstoday = query(roomarrivalstoday_data, first=True)

    if roomarrivalstoday:
        i_counter = i_counter + 1
        outstr = "ARR-ROOM" + "|" + to_string(roomarrivalstoday.DAY) + "|" +\
                to_string(roomarrivalstoday.MTD) + "|" + to_string(roomarrivalstoday.YTD)


        add_line(outstr, i_counter)

    personarrivalstoday = query(personarrivalstoday_data, first=True)

    if personarrivalstoday:
        i_counter = i_counter + 1
        outstr = "ARR-PERSON" + "|" + to_string(personarrivalstoday.DAY) + "|" +\
                to_string(personarrivalstoday.MTD) + "|" + to_string(personarrivalstoday.YTD)


        add_line(outstr, i_counter)

    roomdeparturestoday = query(roomdeparturestoday_data, first=True)

    if roomdeparturestoday:
        i_counter = i_counter + 1
        outstr = "DEPT-ROOM" + "|" + to_string(roomdeparturestoday.DAY) + "|" +\
                to_string(roomdeparturestoday.MTD) + "|" + to_string(roomdeparturestoday.YTD)


        add_line(outstr, i_counter)

    persondeparturestoday = query(persondeparturestoday_data, first=True)

    if persondeparturestoday:
        i_counter = i_counter + 1
        outstr = "DEPT-PERSON" + "|" + to_string(persondeparturestoday.DAY) + "|" +\
                to_string(persondeparturestoday.MTD) + "|" + to_string(persondeparturestoday.YTD)


        add_line(outstr, i_counter)

    roomarrivalstomorrow = query(roomarrivalstomorrow_data, first=True)

    if roomarrivalstomorrow:
        i_counter = i_counter + 1
        outstr = "ROOM-ARR-TOMORROW" + "|" + to_string(roomarrivalstomorrow.DAY) + "|" +\
                to_string(roomarrivalstomorrow.MTD) + "|" + to_string(roomarrivalstomorrow.YTD)


        add_line(outstr, i_counter)

    personarrivalstomorrow = query(personarrivalstomorrow_data, first=True)

    if personarrivalstomorrow:
        i_counter = i_counter + 1
        outstr = "PERSON-ARR-TOMORROW" + "|" + to_string(personarrivalstomorrow.DAY) + "|" +\
                to_string(personarrivalstomorrow.MTD) + "|" + to_string(personarrivalstomorrow.YTD)


        add_line(outstr, i_counter)

    roomdeparturestomorrow = query(roomdeparturestomorrow_data, first=True)

    if roomdeparturestomorrow:
        i_counter = i_counter + 1
        outstr = "ROOM-DEPT-TOMORROW" + "|" + to_string(roomdeparturestomorrow.DAY) + "|" +\
                to_string(roomdeparturestomorrow.MTD) + "|" + to_string(roomdeparturestomorrow.YTD)


        add_line(outstr, i_counter)

    persondeparturestomorrow = query(persondeparturestomorrow_data, first=True)

    if persondeparturestomorrow:
        i_counter = i_counter + 1
        outstr = "PERSON-DEPT-TOMORROW" + "|" + to_string(persondeparturestomorrow.DAY) + "|" +\
                to_string(persondeparturestomorrow.MTD) + "|" + to_string(persondeparturestomorrow.YTD)


        add_line(outstr, i_counter)

    for roomtype in query(roomtype_data):
        i_counter = i_counter + 1
        outstr = "ROOMTYPE" + "|" + to_string(roomtype.RoomTypeCode) + "|" + roomtype.roomtypeDescription + "|" + to_string(roomtype.TodayRoomNight) + "|" + dec2char (roomtype.TodayRevenue) + "|" + to_string(roomtype.MTDRoomNight) + "|" + dec2char (roomtype.MTDRevenue) + "|" + to_string(roomtype.YTDRoomNight) + "|" + dec2char (roomtype.YTDRevenue)
        add_line(outstr, i_counter)

    for w1 in query(w1_data):
        i_counter = i_counter + 1
        outstr = "GUEST-INHOUSE-DRR" + "|" + to_string(w1.tday_saldo) + "|" + to_string(w1.mtd_saldo) + "|" + to_string(w1.mtd_budget) + "|" + to_string(w1.ytd_saldo)
        add_line(outstr, i_counter)

    for rsvdetails in query(rsvdetails_data):
        i_counter = i_counter + 1
        outstr = "RESERVATION-DETAILS" + "|" + to_string(rsvdetails.resnum) + "|" + to_string(rsvdetails.date_str) + "|" + to_string(rsvdetails.modifydate) + "|" + to_string(rsvdetails.ratecode) + "|" + to_string(rsvdetails.roomrate) + "|" + to_string(rsvdetails.roomrateroomcharge) + "|" + to_string(rsvdetails.roomratetax) + "|" + to_string(rsvdetails.roomrateserv) + "|" + to_string(rsvdetails.roomratebf) + "|" + to_string(rsvdetails.roomratelunch) + "|" + to_string(rsvdetails.roomratedinner) + "|" + to_string(rsvdetails.roomrateother) + "|" + to_string(rsvdetails.earlybookingdisc) + "|" + to_string(rsvdetails.bonafidecommission) + "|" + to_string(rsvdetails.roomcatcode) + "|" + to_string(rsvdetails.roomargtcode)
        add_line(outstr, i_counter)

    for rc in query(rc_data):
        i_counter = i_counter + 1
        outstr = "MASTER-RC" + "|" + to_string(rc.rcode) + "|" + to_string(rc.parentrcode) + "|" + to_string(rc.zikatnr) + "|" + to_string(rc.percent_flag) + "|" + to_string(rc.ratecalcpercentage) + "|" + to_string(rc.ratecalcamount) + "|" + to_string(rc.rcode_bez) + "|" + to_string(rc.rcode_seg) + "|" + to_string(rc.rcode_argt) + "|" + to_string(rc.curr) + "|" + to_string(rc.dyna_flag)
        add_line(outstr, i_counter)

    for rmtyp in query(rmtyp_data):
        i_counter = i_counter + 1
        outstr = "RC-RMTYP" + "|" + to_string(rmtyp.rcode) + "|" + to_string(rmtyp.zikatnr) + "|" + to_string(rmtyp.rmtype)
        add_line(outstr, i_counter)

    for rooms in query(rooms_data):
        i_counter = i_counter + 1
        outstr = "RC-ROOMS" + "|" + to_string(rooms.rcode) + "|" + to_string(rooms.zikatnr) + "|" + to_string(rooms.rmtype) + "|" + to_string(rooms.daysofweek) + "|" + to_string(rooms.adultcount) + "|" + to_string(rooms.childcount) + "|" + to_string(rooms.infantcount) + "|" + to_string(rooms.adultrate) + "|" + to_string(rooms.startdate) + "|" + to_string(rooms.enddate) + "|" + to_string(rooms.str_fdate) + "|" + to_string(rooms.str_tdate) + "|" + to_string(rooms.bookroom) + "|" + to_string(rooms.compliment) + "|" + to_string(rooms.maxcomplirooms)
        add_line(outstr, i_counter)

    return generate_output()