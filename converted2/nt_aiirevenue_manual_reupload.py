from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
import re
from functions.get_room_breakdown import get_room_breakdown
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Zimkateg, Arrangement, Queasy, Prmarket, Ratecode, Waehrung, Genstat, Artikel, Nightaudit, Nitehist, Htparam, Paramtext, Res_line, Reslin_queasy, Reservation, Segment, Zkstat, Zinrstat, Segmentstat, Umsatz, Budget, Guest, Guestseg, Sourccod, Guest_pr, Nation, exrate, Gl_acct

def nt_aiirevenue_manual_reupload(ci_date:date):
    fr_date:date = None
    fr_date1:date = None
    to_date:date = None
    htl_no:str = ""
    datum:date = None
    loop_datum:date = None
    co_date:date = None
    rsv_date:date = None
    birthdate:str = ""
    canceldate:str = ""
    expdate:str = ""
    address:str = ""
    flight1:str = ""
    flight2:str = ""
    eta:str = ""
    etd:str = ""
    str_rsv:str = ""
    purpose:str = ""
    ankunft:str = ""
    abreise:str = ""
    hharr:str = ""
    mmarr:str = ""
    hhdep:str = ""
    mmdep:str = ""
    ci_time:str = ""
    co_time:str = ""
    pickup:str = ""
    voucherno:str = ""
    contcode:str = ""
    bookdate:str = ""
    dropoff:str = ""
    memozinr:str = ""
    rsv_time:str = ""
    outstr:str = ""
    segm__purcode:int = 0
    loop_i:int = 0
    curr_i:int = 0
    price_decimal:int = 0
    i_counter:int = 0
    droom:int = 0
    mroom:int = 0
    mbroom:int = 0
    flodging:decimal = to_decimal("0.0")
    lodging:decimal = to_decimal("0.0")
    breakfast:decimal = to_decimal("0.0")
    lunch:decimal = to_decimal("0.0")
    dinner:decimal = to_decimal("0.0")
    others:decimal = to_decimal("0.0")
    rmrev:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    tot_lodging:decimal = to_decimal("0.0")
    tot_breakfast:decimal = to_decimal("0.0")
    tot_lunch:decimal = to_decimal("0.0")
    tot_dinner:decimal = to_decimal("0.0")
    tot_others:decimal = to_decimal("0.0")
    tot_rmrev:decimal = to_decimal("0.0")
    tot_vat:decimal = to_decimal("0.0")
    tot_service:decimal = to_decimal("0.0")
    payable_sum:decimal = to_decimal("0.0")
    taxed_payable_sum:decimal = to_decimal("0.0")
    drev:decimal = to_decimal("0.0")
    mrev:decimal = to_decimal("0.0")
    dtrev:decimal = to_decimal("0.0")
    mtrev:decimal = to_decimal("0.0")
    otherrev:decimal = to_decimal("0.0")
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    reihenfolge:int = 0
    progname:str = "nt-aiirevenue.p"
    exrate:decimal = to_decimal("0.0")
    frate:decimal = to_decimal("0.0")
    anz:int = 0
    anz0:int = 0
    gastnr_wi:int = 0
    gastnr_ind:int = 0
    cat_flag:bool = False
    fact:decimal = to_decimal("0.0")
    n_betrag:decimal = to_decimal("0.0")
    n1_betrag:decimal = to_decimal("0.0")
    foreign_flag:bool = False
    tot_taxed_payables:decimal = to_decimal("0.0")
    tot_payables1:decimal = to_decimal("0.0")
    tot_payables2:decimal = to_decimal("0.0")
    tot_payables3:decimal = to_decimal("0.0")
    tot_payables4:decimal = to_decimal("0.0")
    rev_gross_day:decimal = to_decimal("0.0")
    rev_gross_bud:decimal = to_decimal("0.0")
    rev_gross_mtd:decimal = to_decimal("0.0")
    rev_gross_ytd:decimal = to_decimal("0.0")
    zimkateg = arrangement = queasy = prmarket = ratecode = waehrung = genstat = artikel = nightaudit = nitehist = htparam = paramtext = res_line = reslin_queasy = reservation = segment = zkstat = zinrstat = segmentstat = umsatz = budget = guest = guestseg = sourccod = guest_pr = nation = exrate = gl_acct = None

    rsv_list = guest_list = ta_list = arrangement_list = zimkateg_list = temp_gastnr = temp_reslin_queasy = segmentrevenue = totalsegmentsrevenue = totalroomrevenue = totalfbrevenue = totalotherrevenue = hotelnetrevenue = hotelgrossrevenue = totalroom = roomsavailable = roomsoccupied = houseuses = complimentaryrooms = roomspaying = vacantrooms = outoforderrooms = noshows = reservationmadetoday = cancellationfortoday = earlycheckout = roomarrivalstoday = personarrivalstoday = roomdeparturestoday = persondeparturestoday = roomarrivalstomorrow = personarrivalstomorrow = roomdeparturestomorrow = persondeparturestomorrow = roomtype = rate_list = w1 = rsvdetails = rc = rmtyp = rooms = t_zimkateg = t_arrangement = t_qsy2 = t_qsy18 = t_qsy152 = t_prmarket = temp_rc = wrung = gstat = buffart = qsy18 = None

    rsv_list_list, Rsv_list = create_model("Rsv_list", {"resnr":str, "reslinnr":str, "arr_date":str, "dep_date":str, "flight1":str, "flight2":str, "eta":str, "etd":str, "pickup":str, "dropoff":str, "nights":str, "adults":str, "childs":str, "infants":str, "infantage":str, "comp":str, "comp_ch":str, "voucher":str, "ta_code":str, "ratecode":str, "qty":str, "roomcat":str, "argt":str, "curr":str, "roomrate":str, "roomcharge":str, "roomtax":str, "roomserv":str, "room_bf":str, "room_lunch":str, "room_dinner":str, "room_others":str, "discount":str, "commission":str, "fixrate":str, "billinstruction":str, "purpose":str, "memo":str, "gastnrmember":str, "guest_status":str, "rsv_type":str, "rsv_status":str, "rsv_time":str, "cancel_nr":str, "cancel_date":str, "cancel":str, "ci_time":str, "co_time":str, "resstatus":int, "active_flag":int, "zinr":str, "isdayuseincluded":str, "modifydate":str})
    guest_list_list, Guest_list = create_model("Guest_list", {"gastnr":str, "lastname":str, "firstname":str, "address":str, "city":str, "prov":str, "zip":str, "country":str, "birthplace":str, "birthdate":str, "sex":str, "phone":str, "mobile":str, "fax":str, "email":str, "occupation":str, "idcard_nr":str, "idcard_type":str, "idcard_exp":str, "companyguestnr":str, "mainsegment":str, "codes":str, "vip":str, "comments":str, "nation":str, "modifydate":str})
    ta_list_list, Ta_list = create_model("Ta_list", {"gastnr":str, "refno":str, "name":str, "ta_title":str, "address":str, "city":str, "prov":str, "zip":str, "country":str, "phone":str, "telefax":str, "email":str, "ratecode":str, "mainsegment":str, "booksource":str, "comments":str, "iscompany":str})
    arrangement_list_list, Arrangement_list = create_model("Arrangement_list", {"arrangement":str, "argt_bez":str})
    zimkateg_list_list, Zimkateg_list = create_model("Zimkateg_list", {"kurzbez":str, "bezeichnung":str})
    temp_gastnr_list, Temp_gastnr = create_model("Temp_gastnr", {"gastnr":int})
    temp_reslin_queasy_list, Temp_reslin_queasy = create_model("Temp_reslin_queasy", {"resnr":int, "reslinnr":int, "number2":int, "modify_date":date})
    segmentrevenue_list, Segmentrevenue = create_model("Segmentrevenue", {"segmentcode":int, "segmentdescription":str, "segmentcomment":str, "todayroomnight":int, "todayrevenue":decimal, "todayrevenuepercentage":decimal, "mtdroomnight":int, "mtdrevenue":decimal, "mtdrevenuepercentage":decimal, "ytdroomnight":int, "ytdrevenue":decimal, "ytdrevenuepercentage":decimal, "budget":decimal, "variance":decimal})
    totalsegmentsrevenue_list, Totalsegmentsrevenue = create_model("Totalsegmentsrevenue", {"day":decimal, "todaypercentage":decimal, "mtd":decimal, "mtdpercentage":decimal, "ytd":decimal, "ytdpercentage":decimal, "budget":decimal, "variance":decimal})
    totalroomrevenue_list, Totalroomrevenue = create_model("Totalroomrevenue", {"day":decimal, "todaypercentage":decimal, "mtd":decimal, "mtdpercentage":decimal, "ytd":decimal, "ytdpercentage":decimal, "budget":decimal, "variance":decimal})
    totalfbrevenue_list, Totalfbrevenue = create_model("Totalfbrevenue", {"day":decimal, "todaypercentage":decimal, "mtd":decimal, "mtdpercentage":decimal, "ytd":decimal, "ytdpercentage":decimal, "budget":decimal, "variance":decimal})
    totalotherrevenue_list, Totalotherrevenue = create_model("Totalotherrevenue", {"day":decimal, "todaypercentage":decimal, "mtd":decimal, "mtdpercentage":decimal, "ytd":decimal, "ytdpercentage":decimal, "budget":decimal, "variance":decimal})
    hotelnetrevenue_list, Hotelnetrevenue = create_model("Hotelnetrevenue", {"day":decimal, "todaypercentage":decimal, "mtd":decimal, "mtdpercentage":decimal, "ytd":decimal, "ytdpercentage":decimal, "budget":decimal, "variance":decimal})
    hotelgrossrevenue_list, Hotelgrossrevenue = create_model("Hotelgrossrevenue", {"day":decimal, "todaypercentage":decimal, "mtd":decimal, "mtdpercentage":decimal, "ytd":decimal, "ytdpercentage":decimal, "budget":decimal, "variance":decimal})
    totalroom_list, Totalroom = create_model("Totalroom", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomsavailable_list, Roomsavailable = create_model("Roomsavailable", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomsoccupied_list, Roomsoccupied = create_model("Roomsoccupied", {"day":int, "mtd":int, "budget":int, "ytd":int})
    houseuses_list, Houseuses = create_model("Houseuses", {"day":int, "mtd":int, "budget":int, "ytd":int})
    complimentaryrooms_list, Complimentaryrooms = create_model("Complimentaryrooms", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomspaying_list, Roomspaying = create_model("Roomspaying", {"day":int, "mtd":int, "budget":int, "ytd":int})
    vacantrooms_list, Vacantrooms = create_model("Vacantrooms", {"day":int, "mtd":int, "budget":int, "ytd":int})
    outoforderrooms_list, Outoforderrooms = create_model("Outoforderrooms", {"day":int, "mtd":int, "budget":int, "ytd":int})
    noshows_list, Noshows = create_model("Noshows", {"day":int, "mtd":int, "budget":int, "ytd":int})
    reservationmadetoday_list, Reservationmadetoday = create_model("Reservationmadetoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    cancellationfortoday_list, Cancellationfortoday = create_model("Cancellationfortoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    earlycheckout_list, Earlycheckout = create_model("Earlycheckout", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomarrivalstoday_list, Roomarrivalstoday = create_model("Roomarrivalstoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    personarrivalstoday_list, Personarrivalstoday = create_model("Personarrivalstoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomdeparturestoday_list, Roomdeparturestoday = create_model("Roomdeparturestoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    persondeparturestoday_list, Persondeparturestoday = create_model("Persondeparturestoday", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomarrivalstomorrow_list, Roomarrivalstomorrow = create_model("Roomarrivalstomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    personarrivalstomorrow_list, Personarrivalstomorrow = create_model("Personarrivalstomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomdeparturestomorrow_list, Roomdeparturestomorrow = create_model("Roomdeparturestomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    persondeparturestomorrow_list, Persondeparturestomorrow = create_model("Persondeparturestomorrow", {"day":int, "mtd":int, "budget":int, "ytd":int})
    roomtype_list, Roomtype = create_model("Roomtype", {"roomtypecode":str, "roomtypedescription":str, "todayroomnight":int, "todayrevenue":decimal, "mtdroomnight":int, "mtdrevenue":decimal, "ytdroomnight":int, "ytdrevenue":decimal})
    rate_list_list, Rate_list = create_model("Rate_list", {"code":str, "bezeich":str})
    w1_list, W1 = create_model("W1", {"tday_saldo":decimal, "mtd_saldo":decimal, "mtd_budget":decimal, "ytd_saldo":decimal})
    rsvdetails_list, Rsvdetails = create_model("Rsvdetails", {"resnum":str, "reslinnum":str, "inhousedate":str, "date_str":str, "modifydate":str, "ratecode":str, "roomrate":str, "roomrateroomcharge":str, "roomratetax":str, "roomrateserv":str, "roomratebf":str, "roomratelunch":str, "roomratedinner":str, "roomrateother":str, "earlybookingdisc":str, "bonafidecommission":str, "roomcatcode":str, "roomargtcode":str})
    rc_list, Rc = create_model("Rc", {"rcode":str, "parentrcode":str, "zikatnr":int, "percent_flag":bool, "ratecalcpercentage":decimal, "ratecalcamount":decimal, "rcode_bez":str, "rcode_seg":str, "rcode_argt":str, "curr":str, "dyna_flag":str})
    rmtyp_list, Rmtyp = create_model("Rmtyp", {"rcode":str, "zikatnr":int, "rmtype":str})
    rooms_list, Rooms = create_model("Rooms", {"rcode":str, "zikatnr":int, "rmtype":str, "daysofweek":int, "adultcount":int, "childcount":int, "infantcount":int, "adultrate":decimal, "childrate":decimal, "infantrate":decimal, "startdate":date, "enddate":date, "str_fdate":str, "str_tdate":str, "bookroom":int, "compliment":int, "maxcomplirooms":int})
    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    t_arrangement_list, T_arrangement = create_model_like(Arrangement)
    t_qsy2_list, T_qsy2 = create_model_like(Queasy)
    t_qsy18_list, T_qsy18 = create_model_like(Queasy)
    t_qsy152_list, T_qsy152 = create_model_like(Queasy)
    t_prmarket_list, T_prmarket = create_model_like(Prmarket)
    temp_rc_list, Temp_rc = create_model_like(Ratecode)

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
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        return {}

    def datetime2char(datum:date, zeit:int):

        nonlocal fr_date, fr_date1, to_date, htl_no, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        str:str = ""
        str = to_string(get_year(datum) , "9999") +\
                to_string(get_month(datum) , "99") +\
                to_string(get_day(datum) , "99") + "T" +\
                to_string(zeit, "HH:MM:SS")


        return str


    def dec2char(d:decimal):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        str:str = ""
        d = to_decimal(round(d , 2))
        str = trim(to_string(d, "->>>>>>>>>>>>>>>>>9.99"))


        str = replace_str(str, ",", ".")
        return str


    def decode_string(in_str:str):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def create_rsv_list(i_resnr:int, i_reslinnr:int, i_date:date, i_time:int):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        gbuff = None
        s_time:str = ""
        rmcat:int = 0
        rm_service:decimal = to_decimal("0.0")
        rm_vat:decimal = to_decimal("0.0")
        rm_vat2:decimal = to_decimal("0.0")
        rm_fact:decimal = to_decimal("0.0")
        rm_tot_tax:decimal = to_decimal("0.0")
        rm_tot_serv:decimal = to_decimal("0.0")
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
        rsv_list_list.append(rsv_list)


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

        if re.match(r".*,contcode, re.IGNORECASE)|*":
            contcode = replace_str(contcode, "|", "")

        rate_list = query(rate_list_list, filters=(lambda rate_list: rate_list.code.lower()  == (contcode).lower()), first=True)

        if not rate_list and contcode != "":
            rate_list = Rate_list()
            rate_list_list.append(rate_list)

            rate_list.code = contcode

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (func.lower(Queasy.char1) == (contcode).lower())).first()

            if queasy:
                rate_list.bezeich = queasy.char2
        ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
        kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

        if ebdisc_flag:
            rsv_list.discount = "1"
        else:
            rsv_list.discount = "0"

        if kbdisc_flag:
            rsv_list.commission = "1"
        else:
            rsv_list.commission = "0"

        if res_line.resstatus != 9 and res_line.resstatus != 99 and res_line.resstatus != 10:

            wrung = db_session.query(Wrung).filter(
                     (Wrung.waehrungsnr == res_line.betriebsnr)).first()

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
                rsvdetails_list.append(rsvdetails)

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

                genstat = db_session.query(Genstat).filter(
                         (Genstat.datum == datum) & (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr) & (Genstat.zinr == res_line.zinr)).first()

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

                zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.zikatnr == rmcat)).first()

                if zimkateg:
                    rsvdetails.roomcatcode = zimkateg.kurzbez
                else:
                    rsvdetails.roomcatcode = ""

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 == datum) & (Reslin_queasy.date2 == datum)).first()

                if reslin_queasy:
                    rsvdetails.ratecode = reslin_queasy.char2

                elif not reslin_queasy:

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 == res_line.ankunft) & (Reslin_queasy.date2 == res_line.abreise)).first()

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

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

        if reslin_queasy:
            rsv_list.fixrate = "1"
        else:
            rsv_list.fixrate = "0"

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 143) & (Queasy.number1 == segm__purcode)).first()

        if queasy:
            rsv_list.purpose = queasy.char1 + " " + queasy.char3

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            rsv_list.roomcat = zimkateg.kurzbez
        else:
            rsv_list.roomcat = ""
        rsv_list.curr = "IDR"

        if re.match(r".*pickup.*",res_line.zimmer_wunsch, re.IGNORECASE):
            rsv_list.pickup = "1"
        else:
            rsv_list.pickup = "0"

        if re.match(r".*drop-passanger.*",res_line.zimmer_wunsch, re.IGNORECASE):
            rsv_list.dropoff = "1"
        else:
            rsv_list.dropoff = "0"

        if session_date_format() == ("dmy").lower() :
            rsv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

        elif session_date_format() == ("mdy").lower() :
            rsv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
        else:
            rsv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff.gastnr == res_line.gastnr)).first()

        if gbuff:
            rsv_list.ta_code = to_string(gbuff.gastnr)

            ta_list = query(ta_list_list, filters=(lambda ta_list: ta_list.gastnr == rsv_list.TA_code), first=True)

            if not ta_list and rsv_list.TA_code != "":
                ta_list = Ta_list()
                ta_list_list.append(ta_list)

                ta_list.gastnr = rsv_list.TA_code
                ta_list.name = gbuff.name
                ta_list.ta_title = gbuff.anredefirma
                ta_list.address = gbuff.adresse1 + ", " + gbuff.adresse2 + ", " + gbuff.adresse3
                ta_list.city = gbuff.wohnort
                ta_list.zip = gbuff.plz
                ta_list.country = gbuff.land
                ta_list.email = gbuff.email_adr
                ta_list.comments = gbuff.bemerkung

                if re.match(r".*,gbuff.telefon, re.IGNORECASE)|*":
                    ta_list.phone = replace_str(gbuff.telefon, "|", "-")

                if re.match(r".*,gbuff.fax, re.IGNORECASE)|*":
                    ta_list.telefax = replace_str(gbuff.fax, "|", "-")

                if gbuff.karteityp == 1:
                    ta_list.iscompany = "1"
                else:
                    ta_list.iscompany = "0"

                if re.match(r".*,ta_list.comments, re.IGNORECASE)|*":
                    ta_list.comments = replace_str(ta_list.comments, "|", "-")

                if re.match(r".*" + chr(124) + r".*",gbuff.steuernr, re.IGNORECASE):
                    ta_list.refno = entry(0, gbuff.steuernr, chr(124))

                elif not re.match(r".*" + chr(124) + r".*",gbuff.steuernr, re.IGNORECASE) and gbuff.steuernr != "":
                    ta_list.refno = gbuff.steuernr
                else:
                    ta_list.refno = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gbuff.gastnr) & (Guestseg.reihenfolge == 1)).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == guestseg.segmentcode)).first()

                    if segment:
                        ta_list.mainsegment = entry(0, segment.bezeich, "$$0")

                sourccod = db_session.query(Sourccod).filter(
                         (Sourccod.source_code == gbuff.segment3)).first()

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

            gstat = db_session.query(Gstat).filter(
                     (Gstat.resnr == res_line.resnr) & (Gstat.res_int[inc_value(0)] == res_line.reslinnr) & (Gstat.zinr == res_line.zinr) & (Gstat.gastnrmember == res_line.gastnrmember) & (Gstat.datum == ci_date)).first()

            if gstat:
                rsv_list.isdayuseincluded = "1"
        else:

            if ci_date == res_line.abreise:

                gstat = db_session.query(Gstat).filter(
                         (Gstat.resnr == res_line.resnr) & (Gstat.res_int[inc_value(0)] == res_line.reslinnr) & (Gstat.zinr == res_line.zinr) & (Gstat.gastnrmember == res_line.gastnrmember) & (Gstat.datum == ci_date)).first()

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

        if re.match(r".*;.*",res_line.memozinr, re.IGNORECASE):
            rsv_list.memo = entry(1, res_line.memozinr, ";")

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()

        if guest:

            guest_list = query(guest_list_list, filters=(lambda guest_list: guest_list.to_int(guest_list.gastnr) == guest.gastnr), first=True)

            if not guest_list:
                guest_list = Guest_list()
                guest_list_list.append(guest_list)


                nation = db_session.query(Nation).filter(
                         (Nation.kurzbez == guest.nation1)).first()

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

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == guestseg.segmentcode)).first()

                    if segment and not re.match(r".*VIP.*",entry(0, segment.bezeich, "$$0"), re.IGNORECASE):
                        guest_list.codes = guest_list.codes + entry(0, segment.bezeich, "$$0") + ";"

                    if re.match(r".*VIP.*",entry(0, segment.bezeich, "$$0"), re.IGNORECASE):
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

                if re.match(r".*,guest_list.comments, re.IGNORECASE)|*":
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


    def add_line(s:str, line_nr:int):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        nitehist = db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (Nitehist.reihenfolge == reihenfolge) & (Nitehist.line_nr == line_nr)).first()

        if not nitehist:
            create_nitehis(line_nr, s)


    def create_nitehis(linenr:int, line_str:str):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list


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
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        foreign_nr:int = 0

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        if htparam.fchar != "":

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                foreign_nr = waehrung.waehrungsnr

        if foreign_nr != 0:

            exrate = db_session.query(exrate).filter(
                     (exrate.artnr == foreign_nr) & (exrate.datum == curr_date)).first()
        else:

            exrate = db_session.query(exrate).filter(
                     (exrate.datum == curr_date)).first()


    def find_payable(fib:str, curr_val:decimal, curr_taxed_val:decimal, prev_val:decimal):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        final_val = to_decimal("0.0")
        payable_sum = to_decimal("0.0")
        taxed_payable_sum = to_decimal("0.0")

        def generate_inner_output():
            return (final_val, payable_sum, taxed_payable_sum)

        payable_sum =  to_decimal("0")
        taxed_payable_sum =  to_decimal("0")

        gl_acct = db_session.query(Gl_acct).filter(
                 (func.lower(Gl_acct.fibukonto) == (fib).lower()) & (Gl_acct.acc_type != 4)).first()

        if gl_acct:
            final_val =  to_decimal(prev_val) + to_decimal(curr_val)
        else:
            payable_sum =  to_decimal(payable_sum) + to_decimal(curr_val)
            final_val =  to_decimal(prev_val)

        return generate_inner_output()


    def find_gross(fib:str, n1_betrag:decimal, prev_betrag:decimal):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        rev_gross = to_decimal("0.0")

        def generate_inner_output():
            return (rev_gross)


        gl_acct = db_session.query(Gl_acct).filter(
                 (func.lower(Gl_acct.fibukonto) == (fib).lower()) & (Gl_acct.acc_type != 4)).first()

        if gl_acct:
            rev_gross =  to_decimal(prev_betrag) + to_decimal(n1_betrag)
        else:
            rev_gross =  to_decimal(prev_betrag)

        return generate_inner_output()


    def validate_field(str:str):

        nonlocal fr_date, fr_date1, to_date, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

        outval = ""
        tempvar1:str = ""
        tempvar2:str = ""

        def generate_inner_output():
            return (outval)


        if str == None:
            str = ""
        outval = ""
        tempvar1 = str
        tempvar2 = replace_str(tempvar1, chr(10) , " ")
        tempvar2 = replace_str(tempvar1, chr(13) , " ")
        outval = tempvar2

        return generate_inner_output()


    def fill_persocc():

        nonlocal fr_date, fr_date1, htl_no, datum, loop_datum, co_date, rsv_date, birthdate, canceldate, expdate, address, flight1, flight2, eta, etd, str_rsv, purpose, ankunft, abreise, hharr, mmarr, hhdep, mmdep, ci_time, co_time, pickup, voucherno, contcode, bookdate, dropoff, memozinr, rsv_time, outstr, segm__purcode, loop_i, curr_i, price_decimal, i_counter, droom, mroom, mbroom, flodging, lodging, breakfast, lunch, dinner, others, rmrev, vat, service, tot_lodging, tot_breakfast, tot_lunch, tot_dinner, tot_others, tot_rmrev, tot_vat, tot_service, payable_sum, taxed_payable_sum, drev, mrev, dtrev, mtrev, otherrev, ebdisc_flag, kbdisc_flag, reihenfolge, progname, exrate, frate, anz, anz0, gastnr_wi, gastnr_ind, cat_flag, fact, n_betrag, n1_betrag, foreign_flag, tot_taxed_payables, tot_payables1, tot_payables2, tot_payables3, tot_payables4, rev_gross_day, rev_gross_bud, rev_gross_mtd, rev_gross_ytd, zimkateg, arrangement, queasy, prmarket, ratecode, waehrung, genstat, artikel, nightaudit, nitehist, htparam, paramtext, res_line, reslin_queasy, reservation, segment, zkstat, zinrstat, segmentstat, umsatz, budget, guest, guestseg, sourccod, guest_pr, nation, exrate, gl_acct
        nonlocal ci_date
        nonlocal wrung, gstat, buffart, qsy18


        nonlocal rsv_list, guest_list, ta_list, arrangement_list, zimkateg_list, temp_gastnr, temp_reslin_queasy, segmentrevenue, totalsegmentsrevenue, totalroomrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroom, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roomspaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtype, rate_list, w1, rsvdetails, rc, rmtyp, rooms, t_zimkateg, t_arrangement, t_qsy2, t_qsy18, t_qsy152, t_prmarket, temp_rc, wrung, gstat, buffart, qsy18
        nonlocal rsv_list_list, guest_list_list, ta_list_list, arrangement_list_list, zimkateg_list_list, temp_gastnr_list, temp_reslin_queasy_list, segmentrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roomspaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtype_list, rate_list_list, w1_list, rsvdetails_list, rc_list, rmtyp_list, rooms_list, t_zimkateg_list, t_arrangement_list, t_qsy2_list, t_qsy18_list, t_qsy152_list, t_prmarket_list, temp_rc_list

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

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    for nitehist in db_session.query(Nitehist).filter(
             (Nitehist.datum == ci_date) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
        db_session.delete(nitehist)

    nitehist = db_session.query(Nitehist).filter(
             (Nitehist.datum == ci_date) & (Nitehist.reihenfolge == reihenfolge)).first()

    if nitehist:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 109)).first()
    gastnr_wi = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 123)).first()
    gastnr_ind = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    price_decimal = 2

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2)).order_by(Queasy._recid).all():
        t_qsy2 = T_qsy2()
        t_qsy2_list.append(t_qsy2)

        buffer_copy(queasy, t_qsy2)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 18)).order_by(Queasy._recid).all():
        t_qsy18 = T_qsy18()
        t_qsy18_list.append(t_qsy18)

        buffer_copy(queasy, t_qsy18)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 152)).order_by(Queasy._recid).all():
        t_qsy152 = T_qsy152()
        t_qsy152_list.append(t_qsy152)

        buffer_copy(queasy, t_qsy152)

    for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

    for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

    for prmarket in db_session.query(Prmarket).order_by(Prmarket._recid).all():
        t_prmarket = T_prmarket()
        t_prmarket_list.append(t_prmarket)

        buffer_copy(prmarket, t_prmarket)

    reslin_queasy_obj_list = []
    for reslin_queasy, res_line in db_session.query(Reslin_queasy, Res_line).join(Res_line,(Res_line.resnr == Reslin_queasy.resnr) & (Res_line.reslinnr == Reslin_queasy.reslinnr) & (Res_line.ankunft != None) & (Res_line.abreise != None) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12)).filter(
             (Reslin_queasy.date2 == ci_date) & (func.lower(Reslin_queasy.key) == ("ResChanges").lower())).order_by(Reslin_queasy._recid).all():
        if reslin_queasy._recid in reslin_queasy_obj_list:
            continue
        else:
            reslin_queasy_obj_list.append(reslin_queasy._recid)

        temp_reslin_queasy = query(temp_reslin_queasy_list, filters=(lambda temp_reslin_queasy: temp_reslin_queasy.resnr == reslin_queasy.resnr and temp_reslin_queasy.reslinnr == reslin_queasy.reslinnr), first=True)

        if not temp_reslin_queasy:
            temp_reslin_queasy = Temp_reslin_queasy()
            temp_reslin_queasy_list.append(temp_reslin_queasy)

            temp_reslin_queasy.resnr = reslin_queasy.resnr
            temp_reslin_queasy.reslinnr = reslin_queasy.reslinnr
            temp_reslin_queasy.number2 = reslin_queasy.number2
            temp_reslin_queasy.modify_date = date_mdy(entry(23, reslin_queasy.char3, ";"))

    for res_line in db_session.query(Res_line).filter(
             (((Res_line.ankunft == ci_date) & (Res_line.active_flag == 1)) | ((Res_line.ankunft == ci_date) & (Res_line.active_flag == 2)) | ((Res_line.abreise == ci_date) & (Res_line.active_flag == 2)) | ((Res_line.cancelled == ci_date) & (Res_line.active_flag == 2)) | ((Res_line.ankunft == ci_date) & (Res_line.resstatus == 10)) | ((Res_line.cancelled == None) & (Res_line.active_flag == 2) & (Res_line.resstatus == 9))) & (Res_line.ankunft != None) & (Res_line.abreise != None) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():

        temp_reslin_queasy = query(temp_reslin_queasy_list, filters=(lambda temp_reslin_queasy: temp_reslin_queasy.resnr == res_line.resnr and temp_reslin_queasy.reslinnr == res_line.reslinnr), first=True)

        if not temp_reslin_queasy:
            temp_reslin_queasy = Temp_reslin_queasy()
            temp_reslin_queasy_list.append(temp_reslin_queasy)

            temp_reslin_queasy.resnr = res_line.resnr
            temp_reslin_queasy.reslinnr = res_line.reslinnr
            temp_reslin_queasy.modify_date = None

    res_line_obj_list = []
    for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == temp_reslin_queasy.resnr)).filter(
             ((Res_line.resnr.in_(list(set([temp_reslin_queasy.resnr for temp_reslin_queasy in temp_reslin_queasy_list])))) & (Res_line.reslinnr == temp_reslin_queasy.reslinnr))).order_by(Res_line._recid).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)

        temp_reslin_queasy = query(temp_reslin_queasy_list, (lambda temp_reslin_queasy: (res_line.resnr == temp_reslin_queasy.resnr)), first=True)

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

    for t_arrangement in query(t_arrangement_list, filters=(lambda t_arrangement: t_arrangement.weeksplit != YES)):
        arrangement_list = Arrangement_list()
        arrangement_list_list.append(arrangement_list)

        arrangement_list.arrangement = t_arrangement.arrangement
        arrangement_list.argt_bez = t_arrangement.argt_bez

    for t_zimkateg in query(t_zimkateg_list):
        zimkateg_list = Zimkateg_list()
        zimkateg_list_list.append(zimkateg_list)

        zimkateg_list.kurzbez = t_zimkateg.kurzbez
        zimkateg_list.bezeichnung = t_zimkateg.bezeichnung


    create_nitehis(0, "SEND|0")
    i_counter = 0

    for rsv_list in query(rsv_list_list, filters=(lambda rsv_list: rsv_list.resnr != "")):
        i_counter = i_counter + 1
        outstr = "RSV" + "|" + rsv_list.resnr + "|" + rsv_list.reslinnr + "|" + rsv_list.arr_date + "|" + rsv_list.dep_date + "|" + rsv_list.flight1 + "|" + rsv_list.flight2 + "|" + rsv_list.eta + "|" + rsv_list.etd + "|" + rsv_list.pickup + "|" + rsv_list.dropoff + "|" + rsv_list.nights + "|" + rsv_list.adults + "|" + rsv_list.childs + "|" + rsv_list.infants + "|" + rsv_list.infantage + "|" + rsv_list.comp + "|" + rsv_list.comp_ch + "|" + rsv_list.voucher + "|" + rsv_list.TA_code + "|" + rsv_list.ratecode + "|" + rsv_list.qty + "|" + rsv_list.roomcat + "|" + rsv_list.argt + "|" + rsv_list.curr + "|" + rsv_list.roomrate + "|" + rsv_list.roomcharge + "|" + rsv_list.roomtax + "|" + rsv_list.roomserv + "|" + rsv_list.room_bf + "|" + rsv_list.room_lunch + "|" + rsv_list.room_dinner + "|" + rsv_list.room_others + "|" + rsv_list.discount + "|" + rsv_list.commission + "|" + rsv_list.fixrate + "|" + rsv_list.billinstruction + "|" + rsv_list.purpose + "|" + rsv_list.memo + "|" + rsv_list.gastnrmember + "|" + rsv_list.guest_status + "|" + rsv_list.rsv_type + "|" + rsv_list.rsv_status + "|" + rsv_list.rsv_time + "|" + rsv_list.cancel_nr + "|" + rsv_list.cancel_date + "|" + rsv_list.cancel + "|" + rsv_list.co_time + "|" + rsv_list.ci_time + "|" + to_string(rsv_list.resstatus) + "|" + to_string(rsv_list.active_flag) + "|" + rsv_list.zinr + "|" + rsv_list.isdayuseincluded + "|" + rsv_list.modifydate
        add_line(outstr, i_counter)

    for guest_list in query(guest_list_list, filters=(lambda guest_list: guest_list.gastnr != "")):
        i_counter = i_counter + 1
        outstr = "GST" + "|" + guest_list.gastnr + "|" + guest_list.lastname + "|" + guest_list.firstname + "|" + guest_list.address + "|" + guest_list.city + "|" + guest_list.prov + "|" + guest_list.zip + "|" + guest_list.country + "|" + guest_list.birthplace + "|" + guest_list.birthdate + "|" + guest_list.sex + "|" + guest_list.phone + "|" + guest_list.mobile + "|" + guest_list.fax + "|" + guest_list.email + "|" + guest_list.occupation + "|" + guest_list.idcard_nr + "|" + guest_list.idcard_type + "|" + guest_list.idcard_exp + "|" + guest_list.companyguestnr + "|" + guest_list.mainsegment + "|" + guest_list.codes + "|" + guest_list.comments + "|" + guest_list.nation + "|" + guest_list.modifydate + "|" + guest_list.vip
        add_line(outstr, i_counter)

    for arrangement_list in query(arrangement_list_list):
        i_counter = i_counter + 1
        outstr = "ARG" + "|" + arrangement_list.arrangement + "|" + arrangement_list.argt_bez
        add_line(outstr, i_counter)

    for zimkateg_list in query(zimkateg_list_list):
        i_counter = i_counter + 1
        outstr = "ROM" + "|" + zimkateg_list.kurzbez + "|" + zimkateg_list.bezeichnung
        add_line(outstr, i_counter)
    fr_date = date_mdy(1, 1, get_year(ci_date))
    fr_date1 = date_mdy(get_month(ci_date) , 1, get_year(ci_date))
    anz0 = 0

    for segment in db_session.query(Segment).order_by(Segment._recid).all():
        segmentrevenue = Segmentrevenue()
        segmentrevenue_list.append(segmentrevenue)

        segmentrevenue.segmentcode = segment.segmentcode
        segmentrevenue.segmentdescription = segment.bezeich
        segmentrevenue.segmentcomment = segment.bemerkung


    roomsavailable = Roomsavailable()
    roomsavailable_list.append(roomsavailable)


    for zkstat in db_session.query(Zkstat).filter(
             (Zkstat.datum >= fr_date) & (Zkstat.datum <= ci_date)).order_by(Zkstat._recid).all():

        if zkstat.datum == ci_date:
            roomsavailable.day = roomsavailable.day + zkstat.anz100

        if get_month(zkstat.datum) == get_month(ci_date):
            roomsavailable.mtd = roomsavailable.mtd + zkstat.anz100
        roomsavailable.ytd = roomsavailable.ytd + zkstat.anz100

    for t_zimkateg in query(t_zimkateg_list):
        roomtype = Roomtype()
        roomtype_list.append(roomtype)

        roomtype.roomtypecode = t_zimkateg.kurzbez
        roomtype.roomtypedescription = t_zimkateg.bezeichnung


    totalsegmentsrevenue = Totalsegmentsrevenue()
    totalsegmentsrevenue_list.append(totalsegmentsrevenue)

    totalroomrevenue = Totalroomrevenue()
    totalroomrevenue_list.append(totalroomrevenue)

    totalfbrevenue = Totalfbrevenue()
    totalfbrevenue_list.append(totalfbrevenue)

    totalotherrevenue = Totalotherrevenue()
    totalotherrevenue_list.append(totalotherrevenue)

    hotelnetrevenue = Hotelnetrevenue()
    hotelnetrevenue_list.append(hotelnetrevenue)

    hotelgrossrevenue = Hotelgrossrevenue()
    hotelgrossrevenue_list.append(hotelgrossrevenue)

    roomsoccupied = Roomsoccupied()
    roomsoccupied_list.append(roomsoccupied)

    complimentaryrooms = Complimentaryrooms()
    complimentaryrooms_list.append(complimentaryrooms)

    roomspaying = Roomspaying()
    roomspaying_list.append(roomspaying)

    houseuses = Houseuses()
    houseuses_list.append(houseuses)

    noshows = Noshows()
    noshows_list.append(noshows)

    cancellationfortoday = Cancellationfortoday()
    cancellationfortoday_list.append(cancellationfortoday)

    outoforderrooms = Outoforderrooms()
    outoforderrooms_list.append(outoforderrooms)

    vacantrooms = Vacantrooms()
    vacantrooms_list.append(vacantrooms)

    reservationmadetoday = Reservationmadetoday()
    reservationmadetoday_list.append(reservationmadetoday)

    earlycheckout = Earlycheckout()
    earlycheckout_list.append(earlycheckout)

    roomarrivalstoday = Roomarrivalstoday()
    roomarrivalstoday_list.append(roomarrivalstoday)

    personarrivalstoday = Personarrivalstoday()
    personarrivalstoday_list.append(personarrivalstoday)

    roomdeparturestoday = Roomdeparturestoday()
    roomdeparturestoday_list.append(roomdeparturestoday)

    persondeparturestoday = Persondeparturestoday()
    persondeparturestoday_list.append(persondeparturestoday)

    roomarrivalstomorrow = Roomarrivalstomorrow()
    roomarrivalstomorrow_list.append(roomarrivalstomorrow)

    personarrivalstomorrow = Personarrivalstomorrow()
    personarrivalstomorrow_list.append(personarrivalstomorrow)

    roomdeparturestomorrow = Roomdeparturestomorrow()
    roomdeparturestomorrow_list.append(roomdeparturestomorrow)

    persondeparturestomorrow = Persondeparturestomorrow()
    persondeparturestomorrow_list.append(persondeparturestomorrow)

    totalroom = Totalroom()
    totalroom_list.append(totalroom)

    w1 = W1()
    w1_list.append(w1)

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

    genstat_obj_list = []
    for genstat, segment, zimkateg in db_session.query(Genstat, Segment, Zimkateg).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).filter(
             (Genstat.datum >= fr_date) & (Genstat.datum <= ci_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
        if genstat._recid in genstat_obj_list:
            continue
        else:
            genstat_obj_list.append(genstat._recid)

        segmentrevenue = query(segmentrevenue_list, filters=(lambda segmentrevenue: segmentrevenue.segmentRevenue.segmentcode == genstat.segmentcode), first=True)

        roomtype = query(roomtype_list, filters=(lambda roomtype: roomtype.roomType.RoomTypeCode == zimkateg.kurzbez), first=True)

        if genstat.datum == ci_date:

            if roomtype:
                roomtype.todayroomnight = roomtype.todayroomnight + 1
                roomtype.todayrevenue =  to_decimal(roomtype.todayrevenue) + to_decimal(genstat.logis)

            if segmentRevenue:
                segmentrevenue.todayroomnight = segmentrevenue.todayroomnight + 1
                segmentrevenue.todayrevenue =  to_decimal(segmentrevenue.todayrevenue) + to_decimal(genstat.logis)

            if segment.betriebsnr == 0:
                roomspaying.day = roomspaying.day + 1

            elif segment.betriebsnr == 1:
                complimentaryrooms.day = complimentaryrooms.day + 1

            elif segment.betriebsnr == 2:
                houseuses.day = houseuses.day + 1
            totalsegmentsrevenue.day =  to_decimal(totalsegmentsrevenue.day) + to_decimal(SegmentRevenue.TodayRevenue)
            roomsoccupied.day = roomsoccupied.day + 1

        if get_month(genstat.datum) == get_month(ci_date):

            if roomtype:
                roomtype.mtdroomnight = roomtype.mtdroomnight + 1
                roomtype.mtdrevenue =  to_decimal(roomtype.mtdrevenue) + to_decimal(genstat.logis)

            if segmentRevenue:
                segmentrevenue.mtdroomnight = segmentrevenue.mtdroomnight + 1
                segmentrevenue.mtdrevenue =  to_decimal(segmentrevenue.mtdrevenue) + to_decimal(genstat.logis)

            if segment.betriebsnr == 0:
                roomspaying.mtd = roomspaying.mtd + 1

            elif segment.betriebsnr == 1:
                complimentaryrooms.mtd = complimentaryrooms.mtd + 1

            elif segment.betriebsnr == 2:
                houseuses.mtd = houseuses.mtd + 1
            totalsegmentsrevenue.mtd =  to_decimal(totalsegmentsrevenue.mtd) + to_decimal(SegmentRevenue.MTDRevenue)
            roomsoccupied.mtd = roomsoccupied.mtd + 1

        if roomType:
            roomtype.ytdroomnight = roomtype.ytdroomnight + 1
            roomtype.ytdrevenue =  to_decimal(roomtype.ytdrevenue) + to_decimal(genstat.logis)

        if segmentRevenue:
            segmentrevenue.ytdroomnight = segmentrevenue.ytdroomnight + 1
            segmentrevenue.ytdrevenue =  to_decimal(segmentrevenue.ytdrevenue) + to_decimal(genstat.logis)

        if segment.betriebsnr == 0:
            roomspaying.ytd = roomspaying.ytd + 1

        elif segment.betriebsnr == 1:
            complimentaryrooms.ytd = complimentaryrooms.ytd + 1

        elif segment.betriebsnr == 2:
            houseuses.ytd = houseuses.ytd + 1
        totalsegmentsrevenue.ytd =  to_decimal(totalsegmentsrevenue.ytd) + to_decimal(SegmentRevenue.YTDRevenue)
        roomsoccupied.ytd = roomsoccupied.ytd + 1

    for segmentstat in db_session.query(Segmentstat).filter(
             (Segmentstat.datum >= fr_date1) & (Segmentstat.datum <= ci_date)).order_by(Segmentstat._recid).all():

        segmentrevenue = query(segmentrevenue_list, filters=(lambda segmentrevenue: segmentrevenue.SegmentRevenue.segmentcode == segmentstat.segmentcode), first=True)

        if segmentRevenue:
            segmentrevenue.budget =  to_decimal(segmentrevenue.budget) + to_decimal(segmentstat.budlogis)


        totalsegmentsrevenue.budget =  to_decimal(totalsegmentsrevenue.budget) + to_decimal(segmentstat.budlogis)

    for segmentrevenue in query(segmentrevenue_list):

        if totalSegmentsRevenue.DAY != 0:
            segmentrevenue.todayrevenuepercentage =  to_decimal(SegmentRevenue.TodayRevenue) / to_decimal(totalSegmentsRevenue.DAY) * to_decimal("100")
        else:
            segmentrevenue.todayrevenuepercentage =  to_decimal("0")

        if totalSegmentsRevenue.MTD != 0:
            segmentrevenue.mtdrevenuepercentage =  to_decimal(SegmentRevenue.MTDRevenue) / to_decimal(totalSegmentsRevenue.MTD) * to_decimal("100")
        else:
            segmentrevenue.mtdrevenuepercentage =  to_decimal("0")

        if totalSegmentsRevenue.YTD != 0:
            segmentrevenue.ytdrevenuepercentage =  to_decimal(SegmentRevenue.YTDRevenue) / to_decimal(totalSegmentsRevenue.YTD) * to_decimal("100")
        else:
            segmentrevenue.ytdrevenuepercentage =  to_decimal("0")
        segmentrevenue.variance =  to_decimal(SegmentRevenue.MTDRevenue) - to_decimal(SegmentRevenue.Budget)

    umsatz_obj_list = []
    for umsatz, artikel in db_session.query(Umsatz, Artikel).join(Artikel,(Artikel.artnr == Umsatz.artnr) & (Artikel.departement == Umsatz.departement)).filter(
             (Umsatz.datum >= fr_date) & (Umsatz.datum <= ci_date)).order_by(Umsatz._recid).all():
        if umsatz._recid in umsatz_obj_list:
            continue
        else:
            umsatz_obj_list.append(umsatz._recid)

        budget = db_session.query(Budget).filter(
                 (Budget.artnr == umsatz.artnr) & (Budget.departement == umsatz.departement) & (Budget.datum == umsatz.datum)).first()
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
                TotalRoomRevenue.DAY, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalRoomRevenue.DAY)
                rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)

            elif artikel.umsatzart == 4:

                if artikel.departement >= 1:

                    buffart = db_session.query(Buffart).filter(
                             (Buffart.departement == umsatz.departement) & ((Buffart.umsatzart == 5) | (Buffart.umsatzart == 6))).first()

                    if buffart:
                        TotalFBRevenue.DAY, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.DAY)
                        rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)
                    else:
                        TotalOtherRevenue.DAY, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalOtherRevenue.DAY)
                        rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)

                elif artikel.departement == 0:
                    TotalOtherRevenue.DAY, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalOtherRevenue.DAY)
                    rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)

            elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
                TotalFBRevenue.DAY, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.DAY)
                rev_gross_day = find_gross(artikel.fibukonto, n1_betrag, rev_gross_day)
            tot_payables1 =  to_decimal(tot_payables1) + to_decimal(payable_sum)

        if get_month(umsatz.datum) == get_month(ci_date):

            if budget and artikel.umsatzart == 1:
                TotalRoomRevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, TotalRoomRevenue.Budget)
                rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)

            elif budget and artikel.umsatzart == 4:

                if artikel.departement >= 1:

                    buffart = db_session.query(Buffart).filter(
                             ((Buffart.umsatzart == 5) & (Buffart.departement == umsatz.departement)) | ((Buffart.umsatzart == 6) & (Buffart.departement == umsatz.departement))).first()

                    if buffart:
                        TotalFBRevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.Budget)
                        rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)
                    else:
                        TotalOtherRevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, TotalOtherRevenue.Budget)
                        rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)

                elif artikel.departement == 0:
                    TotalOtherRevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, TotalOtherRevenue.Budget)
                    rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)

            elif budget and (artikel.umsatzart == 5 or artikel.umsatzart == 6):
                TotalFBRevenue.Budget, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, budget.betrag, budget.betrag, TotalFBRevenue.Budget)
                rev_gross_bud = find_gross(artikel.fibukonto, n1_betrag, rev_gross_bud)
            tot_payables2 =  to_decimal(tot_payables2) + to_decimal(payable_sum)

            if artikel.umsatzart == 1:
                TotalRoomRevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalRoomRevenue.mtd)
                rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)

            elif artikel.umsatzart == 4:

                if artikel.departement >= 1:

                    buffart = db_session.query(Buffart).filter(
                             ((Buffart.umsatzart == 5) & (Buffart.departement == umsatz.departement)) | ((Buffart.umsatzart == 6) & (Buffart.departement == umsatz.departement))).first()

                    if buffart:
                        TotalFBRevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.mtd)
                        rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)
                    else:
                        TotalOtherRevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalOtherRevenue.mtd)
                        rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)

                elif artikel.departement == 0:
                    TotalOtherRevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalOtherRevenue.mtd)
                    rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)

            elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
                TotalFBRevenue.mtd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.mtd)
                rev_gross_mtd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_mtd)
            tot_payables3 =  to_decimal(tot_payables3) + to_decimal(payable_sum)

        if artikel.umsatzart == 1:
            TotalRoomRevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalRoomRevenue.ytd)
            rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)

        elif artikel.umsatzart == 4:

            if artikel.departement >= 1:

                buffart = db_session.query(Buffart).filter(
                         ((Buffart.umsatzart == 5) & (Buffart.departement == umsatz.departement)) | ((Buffart.umsatzart == 6) & (Buffart.departement == umsatz.departement))).first()

                if buffart:
                    TotalFBRevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.ytd)
                    rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)
                else:
                    TotalOtherRevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalOtherRevenue.ytd)
                    rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)

            elif artikel.departement == 0:
                TotalOtherRevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalOtherRevenue.ytd)
                rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)

        elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
            TotalFBRevenue.ytd, payable_sum, taxed_payable_sum = find_payable(artikel.fibukonto, n_betrag, n1_betrag, TotalFBRevenue.ytd)
            rev_gross_ytd = find_gross(artikel.fibukonto, n1_betrag, rev_gross_ytd)
        tot_payables4 =  to_decimal(tot_payables4) + to_decimal(payable_sum)


    hotelnetrevenue.day =  to_decimal(TotalRoomRevenue.DAY) + to_decimal(TotalFBRevenue.DAY) + to_decimal(TotalOtherRevenue.DAY)
    hotelgrossrevenue.day =  to_decimal(rev_gross_day)
    hotelnetrevenue.budget =  to_decimal(TotalRoomRevenue.Budget) + to_decimal(TotalFBRevenue.Budget) + to_decimal(TotalOtherRevenue.Budget)
    hotelgrossrevenue.budget =  to_decimal(rev_gross_bud)
    hotelnetrevenue.mtd =  to_decimal(TotalRoomRevenue.mtd) + to_decimal(TotalFBRevenue.mtd) + to_decimal(TotalOtherRevenue.mtd)
    hotelgrossrevenue.mtd =  to_decimal(rev_gross_mtd)
    hotelnetrevenue.ytd =  to_decimal(TotalRoomRevenue.ytd) + to_decimal(TotalFBRevenue.ytd) + to_decimal(TotalOtherRevenue.ytd)
    hotelgrossrevenue.ytd =  to_decimal(rev_gross_ytd)

    if HotelNetRevenue.DAY != 0:
        totalsegmentsrevenue.todaypercentage =  to_decimal(totalSegmentsRevenue.DAY) / to_decimal(HotelNetRevenue.DAY) * to_decimal("100")
    else:
        totalsegmentsrevenue.todaypercentage =  to_decimal("0")

    if HotelNetRevenue.mtd != 0:
        totalsegmentsrevenue.mtdpercentage =  to_decimal(totalSegmentsRevenue.mtd) / to_decimal(HotelNetRevenue.mtd) * to_decimal("100")
    else:
        totalsegmentsrevenue.mtdpercentage =  to_decimal("0")

    if HotelNetRevenue.ytd != 0:
        totalsegmentsrevenue.ytdpercentage =  to_decimal(totalSegmentsRevenue.ytd) / to_decimal(HotelNetRevenue.ytd) * to_decimal("100")
    else:
        totalsegmentsrevenue.ytdpercentage =  to_decimal("0")

    if HotelNetRevenue.DAY != 0:
        totalroomrevenue.todaypercentage =  to_decimal(totalRoomRevenue.DAY) / to_decimal(HotelNetRevenue.DAY) * to_decimal("100")
    else:
        totalroomrevenue.todaypercentage =  to_decimal("0")

    if HotelNetRevenue.mtd != 0:
        totalroomrevenue.mtdpercentage =  to_decimal(totalRoomRevenue.mtd) / to_decimal(HotelNetRevenue.mtd) * to_decimal("100")
    else:
        totalroomrevenue.mtdpercentage =  to_decimal("0")

    if HotelNetRevenue.Ytd != 0:
        totalroomrevenue.ytdpercentage =  to_decimal(totalRoomRevenue.Ytd) / to_decimal(HotelNetRevenue.ytd) * to_decimal("100")
    else:
        totalroomrevenue.ytdpercentage =  to_decimal("0")

    if HotelNetRevenue.DAY != 0:
        totalfbrevenue.todaypercentage =  to_decimal(TotalFBRevenue.DAY) / to_decimal(HotelNetRevenue.DAY) * to_decimal("100")
    else:
        totalfbrevenue.todaypercentage =  to_decimal("0")

    if HotelNetRevenue.mtd != 0:
        totalfbrevenue.mtdpercentage =  to_decimal(TotalFBRevenue.mtd) / to_decimal(HotelNetRevenue.mtd) * to_decimal("100")
    else:
        totalfbrevenue.mtdpercentage =  to_decimal("0")

    if HotelNetRevenue.Ytd != 0:
        totalfbrevenue.ytdpercentage =  to_decimal(TotalFBRevenue.Ytd) / to_decimal(HotelNetRevenue.ytd) * to_decimal("100")
    else:
        totalfbrevenue.ytdpercentage =  to_decimal("0")

    if HotelNetRevenue.DAY != 0:
        totalotherrevenue.todaypercentage =  to_decimal(TotalOtherRevenue.DAY) / to_decimal(HotelNetRevenue.DAY) * to_decimal("100")
    else:
        totalotherrevenue.todaypercentage =  to_decimal("0")

    if HotelNetRevenue.mtd != 0:
        totalotherrevenue.mtdpercentage =  to_decimal(TotalOtherRevenue.mtd) / to_decimal(HotelNetRevenue.mtd) * to_decimal("100")
    else:
        totalotherrevenue.mtdpercentage =  to_decimal("0")

    if HotelNetRevenue.Ytd != 0:
        totalotherrevenue.ytdpercentage =  to_decimal(TotalOtherRevenue.Ytd) / to_decimal(HotelNetRevenue.ytd) * to_decimal("100")
    else:
        totalotherrevenue.ytdpercentage =  to_decimal("0")

    if HotelNetRevenue.DAY != 0:
        hotelnetrevenue.todaypercentage =  to_decimal(HotelNetRevenue.DAY) / to_decimal(HotelNetRevenue.DAY) * to_decimal("100")
    else:
        hotelnetrevenue.todaypercentage =  to_decimal("0")

    if HotelNetRevenue.mtd != 0:
        hotelnetrevenue.mtdpercentage =  to_decimal(HotelNetRevenue.mtd) / to_decimal(HotelNetRevenue.mtd) * to_decimal("100")
    else:
        hotelnetrevenue.mtdpercentage =  to_decimal("0")

    if HotelNetRevenue.ytd != 0:
        hotelnetrevenue.ytdpercentage =  to_decimal(HotelNetRevenue.ytd) / to_decimal(HotelNetRevenue.ytd) * to_decimal("100")
    else:
        hotelnetrevenue.ytdpercentage =  to_decimal("0")

    if HotelNetRevenue.DAY != 0:
        hotelgrossrevenue.todaypercentage =  to_decimal(HotelGrossRevenue.DAY) / to_decimal(HotelNetRevenue.DAY) * to_decimal("100")
    else:
        hotelgrossrevenue.todaypercentage =  to_decimal("0")

    if HotelNetRevenue.mtd != 0:
        hotelgrossrevenue.mtdpercentage =  to_decimal(HotelGrossRevenue.mtd) / to_decimal(HotelNetRevenue.mtd) * to_decimal("100")
    else:
        hotelgrossrevenue.mtdpercentage =  to_decimal("0")

    if HotelNetRevenue.ytd != 0:
        hotelgrossrevenue.ytdpercentage =  to_decimal(HotelGrossRevenue.ytd) / to_decimal(HotelNetRevenue.ytd) * to_decimal("100")
    else:
        hotelgrossrevenue.ytdpercentage =  to_decimal("0")
    totalsegmentsrevenue.variance =  to_decimal(totalSegmentsRevenue.mtd) - to_decimal(totalSegmentsRevenue.Budget)
    totalroomrevenue.variance =  to_decimal(totalRoomRevenue.mtd) - to_decimal(totalRoomRevenue.Budget)
    totalfbrevenue.variance =  to_decimal(TotalFBRevenue.mtd) - to_decimal(TotalFBRevenue.Budget)
    totalotherrevenue.variance =  to_decimal(TotalOtherRevenue.mtd) - to_decimal(TotalOtherRevenue.Budget)
    hotelnetrevenue.variance =  to_decimal(HotelNetRevenue.mtd) - to_decimal(HotelNetRevenue.Budget)
    hotelgrossrevenue.variance =  to_decimal(HotelGrossRevenue.mtd) - to_decimal(HotelGrossRevenue.Budget)

    for rate_list in query(rate_list_list):
        i_counter = i_counter + 1
        outstr = "RATE" + "|" + rate_list.code + "|" + rate_list.bezeich
        add_line(outstr, i_counter)

    for ta_list in query(ta_list_list):
        i_counter = i_counter + 1
        outstr = "TravelAgent" + "|" + ta_list.gastnr + "|" + ta_list.name + "|" + ta_list.ta_title + "|" + ta_list.address + "|" + ta_list.city + "|" + ta_list.zip + "|" + ta_list.country + "|" + ta_list.phone + "|" + ta_list.telefax + "|" + ta_list.email + "|" + ta_list.ratecode + "|" + ta_list.mainsegment + "|" + ta_list.booksource + "|" + ta_list.comment + "|" + ta_list.refno + "|" + ta_list.iscompany
        add_line(outstr, i_counter)

    for segmentrevenue in query(segmentrevenue_list):
        i_counter = i_counter + 1
        outstr = "SEGREV" + "|" + to_string(SegmentRevenue.segmentCode) + "|" + SegmentRevenue.SegmentDescription + "|" + to_string(SegmentRevenue.TodayRoomNight) + "|" + dec2char (SegmentRevenue.TodayRevenue) + "|" + dec2char (SegmentRevenue.TodayRevenuePercentage) + "|" + to_string(SegmentRevenue.MTDRoomNight) + "|" + dec2char (SegmentRevenue.MTDRevenue) + "|" + dec2char (SegmentRevenue.MTDRevenuePercentage) + "|" + to_string(SegmentRevenue.YTDRoomNight) + "|" + dec2char (SegmentRevenue.YTDRevenue) + "|" + dec2char (SegmentRevenue.YTDRevenuePercentage) + "|" + dec2char (SegmentRevenue.Budget) + "|" + dec2char (SegmentRevenue.Variance) + "|" + SegmentRevenue.SegmentComment
        add_line(outstr, i_counter)

    totalsegmentsrevenue = query(totalsegmentsrevenue_list, first=True)

    if TotalSegmentsRevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-SEGMENT" + "|" + dec2char (TotalSegmentsRevenue.DAY) + "|" +\
                dec2char (TotalSegmentsRevenue.TodayPercentage) + "|" + dec2char (TotalSegmentsRevenue.MTD) + "|" +\
                dec2char (TotalSegmentsRevenue.MTDPercentage) + "|" + dec2char (TotalSegmentsRevenue.YTD) + "|" +\
                dec2char (TotalSegmentsRevenue.YTDPercentage) + "|" + dec2char (TotalSegmentsRevenue.Budget) + "|" +\
                dec2char (TotalSegmentsRevenue.Variance)


        add_line(outstr, i_counter)

    totalroomrevenue = query(totalroomrevenue_list, first=True)

    if TotalRoomRevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-ROOMREV" + "|" + dec2char (TotalRoomRevenue.DAY) + "|" +\
                dec2char (TotalRoomRevenue.TodayPercentage) + "|" + dec2char (TotalRoomRevenue.MTD) + "|" +\
                dec2char (TotalRoomRevenue.MTDPercentage) + "|" + dec2char (TotalRoomRevenue.YTD) + "|" +\
                dec2char (TotalRoomRevenue.YTDPercentage) + "|" + dec2char (TotalRoomRevenue.Budget) + "|" +\
                dec2char (TotalRoomRevenue.Variance)


        add_line(outstr, i_counter)

    totalfbrevenue = query(totalfbrevenue_list, first=True)

    if TotalFBRevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-FBREV" + "|" + dec2char (TotalFBRevenue.DAY) + "|" +\
                dec2char (TotalFBRevenue.TodayPercentage) + "|" + dec2char (TotalFBRevenue.MTD) + "|" +\
                dec2char (TotalFBRevenue.MTDPercentage) + "|" + dec2char (TotalFBRevenue.YTD) + "|" +\
                dec2char (TotalFBRevenue.YTDPercentage) + "|" + dec2char (TotalFBRevenue.Budget) + "|" +\
                dec2char (TotalFBRevenue.Variance)


        add_line(outstr, i_counter)

    totalotherrevenue = query(totalotherrevenue_list, first=True)

    if TotalOtherRevenue:
        i_counter = i_counter + 1
        outstr = "TOTAL-otherrev" + "|" + dec2char (TotalOtherRevenue.DAY) + "|" +\
                dec2char (TotalOtherRevenue.TodayPercentage) + "|" + dec2char (TotalOtherRevenue.MTD) + "|" +\
                dec2char (TotalOtherRevenue.MTDPercentage) + "|" + dec2char (TotalOtherRevenue.YTD) + "|" +\
                dec2char (TotalOtherRevenue.YTDPercentage) + "|" + dec2char (TotalOtherRevenue.Budget) + "|" +\
                dec2char (TotalOtherRevenue.Variance)


        add_line(outstr, i_counter)

    hotelnetrevenue = query(hotelnetrevenue_list, first=True)

    if HotelNetRevenue:
        i_counter = i_counter + 1
        outstr = "NETREV" + "|" + dec2char (HotelNetRevenue.DAY) + "|" +\
                dec2char (HotelNetRevenue.TodayPercentage) + "|" + dec2char (HotelNetRevenue.MTD) + "|" +\
                dec2char (HotelNetRevenue.MTDPercentage) + "|" + dec2char (HotelNetRevenue.YTD) + "|" +\
                dec2char (HotelNetRevenue.YTDPercentage) + "|" + dec2char (HotelNetRevenue.Budget) + "|" +\
                dec2char (HotelNetRevenue.Variance)


        add_line(outstr, i_counter)

    hotelgrossrevenue = query(hotelgrossrevenue_list, first=True)

    if HotelGrossRevenue:
        i_counter = i_counter + 1
        outstr = "GROSSREV" + "|" + dec2char (HotelGrossRevenue.DAY) + "|" +\
                dec2char (HotelGrossRevenue.TodayPercentage) + "|" + dec2char (HotelGrossRevenue.MTD) + "|" +\
                dec2char (HotelGrossRevenue.MTDPercentage) + "|" + dec2char (HotelGrossRevenue.YTD) + "|" +\
                dec2char (HotelGrossRevenue.YTDPercentage) + "|" + dec2char (HotelGrossRevenue.Budget) + "|" +\
                dec2char (HotelGrossRevenue.Variance)


        add_line(outstr, i_counter)

    totalroom = query(totalroom_list, first=True)

    if TotalRoom:
        i_counter = i_counter + 1
        outstr = "TOTAL-ROOM" + "|" + to_string(TotalRoom.DAY) + "|" +\
                to_string(TotalRoom.MTD) + "|" + to_string(TotalRoom.YTD)


        add_line(outstr, i_counter)

    roomsavailable = query(roomsavailable_list, first=True)

    if RoomsAvailable:
        i_counter = i_counter + 1
        outstr = "ROOM-AVAIL" + "|" + to_string(RoomsAvailable.DAY) + "|" +\
                to_string(RoomsAvailable.MTD) + "|" + to_string(RoomsAvailable.YTD)


        add_line(outstr, i_counter)

    roomsoccupied = query(roomsoccupied_list, first=True)

    if RoomsOccupied:
        i_counter = i_counter + 1
        outstr = "ROOM-OCC" + "|" + to_string(RoomsOccupied.DAY) + "|" +\
                to_string(RoomsOccupied.MTD) + "|" + to_string(RoomsOccupied.YTD)


        add_line(outstr, i_counter)

    houseuses = query(houseuses_list, first=True)

    if HouseUses:
        i_counter = i_counter + 1
        outstr = "HOUSE-USE" + "|" + to_string(HouseUses.DAY) + "|" +\
                to_string(HouseUses.MTD) + "|" + to_string(HouseUses.YTD)


        add_line(outstr, i_counter)

    complimentaryrooms = query(complimentaryrooms_list, first=True)

    if ComplimentaryRooms:
        i_counter = i_counter + 1
        outstr = "COMP-ROOM" + "|" + to_string(ComplimentaryRooms.DAY) + "|" +\
                to_string(ComplimentaryRooms.MTD) + "|" + to_string(ComplimentaryRooms.YTD)


        add_line(outstr, i_counter)

    roomspaying = query(roomspaying_list, first=True)

    if RoomsPaying:
        i_counter = i_counter + 1
        outstr = "PAY-ROOM" + "|" + to_string(RoomsPaying.DAY) + "|" +\
                to_string(RoomsPaying.MTD) + "|" + to_string(RoomsPaying.YTD)


        add_line(outstr, i_counter)

    vacantrooms = query(vacantrooms_list, first=True)

    if VacantRooms:
        i_counter = i_counter + 1
        outstr = "VACANT-ROOM" + "|" + to_string(VacantRooms.DAY) + "|" +\
                to_string(VacantRooms.MTD) + "|" + to_string(VacantRooms.YTD)


        add_line(outstr, i_counter)

    outoforderrooms = query(outoforderrooms_list, first=True)

    if OutOfOrderRooms:
        i_counter = i_counter + 1
        outstr = "OOO-ROOM" + "|" + to_string(OutOfOrderRooms.DAY) + "|" +\
                to_string(OutOfOrderRooms.MTD) + "|" + to_string(OutOfOrderRooms.YTD)


        add_line(outstr, i_counter)

    noshows = query(noshows_list, first=True)

    if NoShows:
        i_counter = i_counter + 1
        outstr = "NO-SHOW" + "|" + to_string(NoShows.DAY) + "|" +\
                to_string(NoShows.MTD) + "|" + to_string(NoShows.YTD)


        add_line(outstr, i_counter)

    reservationmadetoday = query(reservationmadetoday_list, first=True)

    if ReservationMadeToday:
        i_counter = i_counter + 1
        outstr = "RSV-TODAY" + "|" + to_string(ReservationMadeToday.DAY) + "|" +\
                to_string(ReservationMadeToday.MTD) + "|" + to_string(ReservationMadeToday.YTD)


        add_line(outstr, i_counter)

    cancellationfortoday = query(cancellationfortoday_list, first=True)

    if CancellationForToday:
        i_counter = i_counter + 1
        outstr = "CANCEL-TODAY" + "|" + to_string(CancellationForToday.DAY) + "|" +\
                to_string(CancellationForToday.MTD) + "|" + to_string(CancellationForToday.YTD)


        add_line(outstr, i_counter)

    earlycheckout = query(earlycheckout_list, first=True)

    if EarlyCheckout:
        i_counter = i_counter + 1
        outstr = "EARLY-CO" + "|" + to_string(EarlyCheckout.DAY) + "|" +\
                to_string(EarlyCheckout.MTD) + "|" + to_string(EarlyCheckout.YTD)


        add_line(outstr, i_counter)

    roomarrivalstoday = query(roomarrivalstoday_list, first=True)

    if RoomArrivalsToday:
        i_counter = i_counter + 1
        outstr = "ARR-ROOM" + "|" + to_string(RoomArrivalsToday.DAY) + "|" +\
                to_string(RoomArrivalsToday.MTD) + "|" + to_string(RoomArrivalsToday.YTD)


        add_line(outstr, i_counter)

    personarrivalstoday = query(personarrivalstoday_list, first=True)

    if PersonArrivalsToday:
        i_counter = i_counter + 1
        outstr = "ARR-PERSON" + "|" + to_string(PersonArrivalsToday.DAY) + "|" +\
                to_string(PersonArrivalsToday.MTD) + "|" + to_string(PersonArrivalsToday.YTD)


        add_line(outstr, i_counter)

    roomdeparturestoday = query(roomdeparturestoday_list, first=True)

    if RoomDeparturesToday:
        i_counter = i_counter + 1
        outstr = "DEPT-ROOM" + "|" + to_string(RoomDeparturesToday.DAY) + "|" +\
                to_string(RoomDeparturesToday.MTD) + "|" + to_string(RoomDeparturesToday.YTD)


        add_line(outstr, i_counter)

    persondeparturestoday = query(persondeparturestoday_list, first=True)

    if PersonDeparturesToday:
        i_counter = i_counter + 1
        outstr = "DEPT-PERSON" + "|" + to_string(PersonDeparturesToday.DAY) + "|" +\
                to_string(PersonDeparturesToday.MTD) + "|" + to_string(PersonDeparturesToday.YTD)


        add_line(outstr, i_counter)

    roomarrivalstomorrow = query(roomarrivalstomorrow_list, first=True)

    if RoomArrivalsTomorrow:
        i_counter = i_counter + 1
        outstr = "ROOM-ARR-TOMORROW" + "|" + to_string(RoomArrivalsTomorrow.DAY) + "|" +\
                to_string(RoomArrivalsTomorrow.MTD) + "|" + to_string(RoomArrivalsTomorrow.YTD)


        add_line(outstr, i_counter)

    personarrivalstomorrow = query(personarrivalstomorrow_list, first=True)

    if PersonArrivalsTomorrow:
        i_counter = i_counter + 1
        outstr = "PERSON-ARR-TOMORROW" + "|" + to_string(PersonArrivalsTomorrow.DAY) + "|" +\
                to_string(PersonArrivalsTomorrow.MTD) + "|" + to_string(PersonArrivalsTomorrow.YTD)


        add_line(outstr, i_counter)

    roomdeparturestomorrow = query(roomdeparturestomorrow_list, first=True)

    if RoomDeparturesTomorrow:
        i_counter = i_counter + 1
        outstr = "ROOM-DEPT-TOMORROW" + "|" + to_string(RoomDeparturesTomorrow.DAY) + "|" +\
                to_string(RoomDeparturesTomorrow.MTD) + "|" + to_string(RoomDeparturesTomorrow.YTD)


        add_line(outstr, i_counter)

    persondeparturestomorrow = query(persondeparturestomorrow_list, first=True)

    if PersonDeparturesTomorrow:
        i_counter = i_counter + 1
        outstr = "PERSON-DEPT-TOMORROW" + "|" + to_string(PersonDeparturesTomorrow.DAY) + "|" +\
                to_string(PersonDeparturesTomorrow.MTD) + "|" + to_string(PersonDeparturesTomorrow.YTD)


        add_line(outstr, i_counter)

    for roomtype in query(roomtype_list):
        i_counter = i_counter + 1
        outstr = "ROOMTYPE" + "|" + to_string(RoomType.RoomTypeCode) + "|" + RoomType.RoomTypeDescription + "|" + to_string(RoomType.TodayRoomNight) + "|" + dec2char (RoomType.TodayRevenue) + "|" + to_string(RoomType.MTDRoomNight) + "|" + dec2char (RoomType.MTDRevenue) + "|" + to_string(RoomType.YTDRoomNight) + "|" + dec2char (RoomType.YTDRevenue)
        add_line(outstr, i_counter)

    for w1 in query(w1_list):
        i_counter = i_counter + 1
        outstr = "GUEST-INHOUSE-DRR" + "|" + to_string(w1.tday_saldo) + "|" + to_string(w1.mtd_saldo) + "|" + to_string(w1.mtd_budget) + "|" + to_string(w1.ytd_saldo)
        add_line(outstr, i_counter)

    for rsvdetails in query(rsvdetails_list):
        i_counter = i_counter + 1
        outstr = "RESERVATION-DETAILS" + "|" + to_string(rsvdetails.resnum) + "|" + to_string(rsvdetails.reslinnum) + "|" + to_string(rsvdetails.inhousedate) + "|" + to_string(rsvdetails.date_str) + "|" + to_string(rsvdetails.modifydate) + "|" + to_string(rsvdetails.ratecode) + "|" + to_string(rsvdetails.roomrate) + "|" + to_string(rsvdetails.roomrateroomcharge) + "|" + to_string(rsvdetails.roomratetax) + "|" + to_string(rsvdetails.roomrateserv) + "|" + to_string(rsvdetails.roomratebf) + "|" + to_string(rsvdetails.roomratelunch) + "|" + to_string(rsvdetails.roomratedinner) + "|" + to_string(rsvdetails.roomrateother) + "|" + to_string(rsvdetails.earlybookingdisc) + "|" + to_string(rsvdetails.bonafidecommission) + "|" + to_string(rsvdetails.roomcatcode) + "|" + to_string(rsvdetails.roomargtcode)
        add_line(outstr, i_counter)

    for rc in query(rc_list):
        i_counter = i_counter + 1
        outstr = "MASTER-RC" + "|" + to_string(rc.rcode) + "|" + to_string(rc.parentrcode) + "|" + to_string(rc.zikatnr) + "|" + to_string(rc.percent_flag) + "|" + to_string(rc.ratecalcpercentage) + "|" + to_string(rc.ratecalcamount) + "|" + to_string(rc.rcode_bez) + "|" + to_string(rc.rcode_seg) + "|" + to_string(rc.rcode_argt) + "|" + to_string(rc.curr) + "|" + to_string(rc.dyna_flag)
        add_line(outstr, i_counter)

    for rmtyp in query(rmtyp_list):
        i_counter = i_counter + 1
        outstr = "RC-RMTYP" + "|" + to_string(rmtyp.rcode) + "|" + to_string(rmtyp.zikatnr) + "|" + to_string(rmtyp.rmtype)
        add_line(outstr, i_counter)

    for rooms in query(rooms_list):
        i_counter = i_counter + 1
        outstr = "RC-ROOMS" + "|" + to_string(rooms.rcode) + "|" + to_string(rooms.zikatnr) + "|" + to_string(rooms.rmtype) + "|" + to_string(rooms.daysofweek) + "|" + to_string(rooms.adultcount) + "|" + to_string(rooms.childcount) + "|" + to_string(rooms.infantcount) + "|" + to_string(rooms.adultrate) + "|" + to_string(rooms.childrate) + "|" + to_string(rooms.infantrate) + "|" + to_string(rooms.startdate) + "|" + to_string(rooms.enddate) + "|" + to_string(rooms.str_fdate) + "|" + to_string(rooms.str_tdate) + "|" + to_string(rooms.bookroom) + "|" + to_string(rooms.compliment) + "|" + to_string(rooms.maxcomplirooms)
        add_line(outstr, i_counter)

    return generate_output()