from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Waehrung, Nightaudit, Nitehist, Queasy, Zimkateg, Arrangement, Nation

def dataexchange_dailybl(ci_date:date):
    avail_data = False
    currname = ""
    currcode = ""
    reservations_list = []
    reservationrooms_list = []
    guests_list = []
    travelagents_list = []
    segmentsrevenue_list = []
    totalsegmentsrevenue_list = []
    totalroomrevenue_list = []
    totalfbrevenue_list = []
    totalotherrevenue_list = []
    hotelnetrevenue_list = []
    hotelgrossrevenue_list = []
    totalroom_list = []
    roomsavailable_list = []
    roomsoccupied_list = []
    houseuses_list = []
    complimentaryrooms_list = []
    roompaying_list = []
    vacantrooms_list = []
    outoforderrooms_list = []
    noshows_list = []
    reservationmadetoday_list = []
    cancellationfortoday_list = []
    earlycheckout_list = []
    roomarrivalstoday_list = []
    personarrivalstoday_list = []
    roomdeparturestoday_list = []
    persondeparturestoday_list = []
    roomarrivalstomorrow_list = []
    personarrivalstomorrow_list = []
    roomdeparturestomorrow_list = []
    persondeparturestomorrow_list = []
    roomtypes_list = []
    hotelid:str = "pop"
    filepath:str = "d:\\dataExchange\\"
    str:str = ""
    str1:str = ""
    str_drr:str = ""
    filenm:str = ""
    i:int = 0
    reihenfolge:int = 0
    progname:str = "nt-aiirevenue.p"
    htparam = waehrung = nightaudit = nitehist = queasy = zimkateg = arrangement = nation = None

    reservations = guests = reservationrooms = travelagents = header1 = segmentsrevenue = totalsegmentsrevenue = totalfbrevenue = totalotherrevenue = hotelnetrevenue = hotelgrossrevenue = totalroomrevenue = totalroom = roomavailable = occupancypercentage = arr = roomrevenue = totalrevenue = fbrevenue = roomsavailable = roomsoccupied = houseuses = complimentaryrooms = roompaying = vacantrooms = outoforderrooms = noshows = reservationmadetoday = cancellationfortoday = earlycheckout = roomarrivalstoday = personarrivalstoday = roomdeparturestoday = persondeparturestoday = roomarrivalstomorrow = personarrivalstomorrow = roomdeparturestomorrow = persondeparturestomorrow = roomtypes = None

    reservations_list, Reservations = create_model("Reservations", {"reservationnumber":str, "reservationlinenumber":str, "arrivaldate":str, "departdate":str, "arrivalflightno":str, "departflightno":str, "arrivalflighttime":str, "departflighttime":str, "pickup":str, "dropoff":str, "nights":str, "adults":str, "childs":str, "infants":str, "infantage":str, "complimentary":str, "complimentarychild":str, "voucher":str, "travelagentcode":str, "ratecode":str, "ratename":str, "quantity":str, "roomcategorycode":str, "roomcategoryname":str, "roomarrangementcode":str, "roomarrangementname":str, "currencycode":str, "currencyname":str, "roomrate":str, "roomrate__roomcharge":str, "roomrate__tax":str, "roomrate__service":str, "roomrate__breakfast":str, "roomrate__lunch":str, "roomrate__dinner":str, "roomrate__other":str, "earlybookingdiscount":str, "bonafidecommission":str, "fixrate":str, "billinstruction":str, "purpose":str, "memoroomnumber":str, "guestnumber":str, "guestreservationstatus":str, "reservationtype":str, "reservationrecordstatus":str, "reservationtime":str, "cancelnumber":str, "canceldate":str, "cancelreason":str})
    guests_list, Guests = create_model("Guests", {"guestnumber":str, "lastname":str, "firstname":str, "address":str, "city":str, "province":str, "postalcode":str, "countrycode":str, "countryname":str, "birthplace":str, "birthdate":str, "sex":str, "phone":str, "mobile":str, "fax":str, "email":str, "occupation":str, "idcardnumber":str, "idcardtype":str, "idcardexpire":str, "companyguestnumber":str, "selectedsegment":str, "guestsegment":str, "comments":str})
    reservationrooms_list, Reservationrooms = create_model("Reservationrooms", {"reservationnumber":str, "reservationlinenumber":str, "roomnumber":str, "checkintime":str, "checkouttime":str})
    travelagents_list, Travelagents = create_model("Travelagents", {"code":str, "name":str, "salutation":str, "address":str, "city":str, "zip":str, "countrycode":str, "countryname":str, "phone":str, "telefax":str, "email":str, "ratecode":str, "mainsegment":str, "booksource":str, "comments":str})
    header1_list, Header1 = create_model("Header1", {"datatype":str, "vhphotelid":str, "timestampofinsertion":str, "currencysymbol":str, "currencycode":str, "currencyname":str})
    segmentsrevenue_list, Segmentsrevenue = create_model("Segmentsrevenue", {"segmentcode":str, "segmentdescription":str, "segmentcomment":str, "todayroomnight":str, "todayrevenue":str, "todayrevenuepercentage":str, "mtdroomnight":str, "mtdrevenue":str, "mtdrevenuepercentage":str, "ytdroomnight":str, "ytdrevenue":str, "ytdrevenuepercentage":str, "budget":str, "variance":str})
    totalsegmentsrevenue_list, Totalsegmentsrevenue = create_model("Totalsegmentsrevenue", {"today1":str, "todaypercentage":str, "mtd":str, "mtdpercentage":str, "budget":str, "variance":str, "ytd":str, "ytdpercentage":str})
    totalfbrevenue_list, Totalfbrevenue = create_model("Totalfbrevenue", {"today1":str, "todaypercentage":str, "mtd":str, "mtdpercentage":str, "ytd":str, "ytdpercentage":str, "budget":str, "variance":str})
    totalotherrevenue_list, Totalotherrevenue = create_model("Totalotherrevenue", {"today1":str, "todaypercentage":str, "mtd":str, "mtdpercentage":str, "ytd":str, "ytdpercentage":str, "budget":str, "variance":str})
    hotelnetrevenue_list, Hotelnetrevenue = create_model("Hotelnetrevenue", {"today1":str, "todaypercentage":str, "mtd":str, "mtdpercentage":str, "ytd":str, "ytdpercentage":str, "budget":str, "variance":str})
    hotelgrossrevenue_list, Hotelgrossrevenue = create_model("Hotelgrossrevenue", {"today1":str, "todaypercentage":str, "mtd":str, "mtdpercentage":str, "ytd":str, "ytdpercentage":str, "budget":str, "variance":str})
    totalroomrevenue_list, Totalroomrevenue = create_model("Totalroomrevenue", {"today1":str, "todaypercentage":str, "mtd":str, "mtdpercentage":str, "ytd":str, "ytdpercentage":str, "budget":str, "variance":str})
    totalroom_list, Totalroom = create_model("Totalroom", {"today1":str, "mtd":str, "ytd":str})
    roomavailable_list, Roomavailable = create_model("Roomavailable", {"todayactual":str, "mtdactual":str, "mtdbudget":str, "ytdactual":str})
    occupancypercentage_list, Occupancypercentage = create_model("Occupancypercentage", {"todayactual":str, "mtdactual":str, "mtdbudget":str, "ytdactual":str})
    arr_list, Arr = create_model("Arr", {"todayactual":str, "mtdactual":str, "mtdbudget":str, "ytdactual":str})
    roomrevenue_list, Roomrevenue = create_model("Roomrevenue", {"todayactual":str, "mtdactual":str, "mtdbudget":str, "ytdactual":str})
    totalrevenue_list, Totalrevenue = create_model("Totalrevenue", {"todayactual":str, "mtdactual":str, "mtdbudget":str, "ytdactual":str})
    fbrevenue_list, Fbrevenue = create_model("Fbrevenue", {"todayactual":str, "mtdactual":str, "mtdbudget":str, "ytdactual":str})
    roomsavailable_list, Roomsavailable = create_model("Roomsavailable", {"today1":str, "mtd":str, "ytd":str})
    roomsoccupied_list, Roomsoccupied = create_model("Roomsoccupied", {"today1":str, "mtd":str, "ytd":str})
    houseuses_list, Houseuses = create_model("Houseuses", {"today1":str, "mtd":str, "ytd":str})
    complimentaryrooms_list, Complimentaryrooms = create_model("Complimentaryrooms", {"today1":str, "mtd":str, "ytd":str})
    roompaying_list, Roompaying = create_model("Roompaying", {"today1":str, "mtd":str, "ytd":str})
    vacantrooms_list, Vacantrooms = create_model("Vacantrooms", {"today1":str, "mtd":str, "ytd":str})
    outoforderrooms_list, Outoforderrooms = create_model("Outoforderrooms", {"today1":str, "mtd":str, "ytd":str})
    noshows_list, Noshows = create_model("Noshows", {"today1":str, "mtd":str, "ytd":str})
    reservationmadetoday_list, Reservationmadetoday = create_model("Reservationmadetoday", {"today1":str, "mtd":str, "ytd":str})
    cancellationfortoday_list, Cancellationfortoday = create_model("Cancellationfortoday", {"today1":str, "mtd":str, "ytd":str})
    earlycheckout_list, Earlycheckout = create_model("Earlycheckout", {"today1":str, "mtd":str, "ytd":str})
    roomarrivalstoday_list, Roomarrivalstoday = create_model("Roomarrivalstoday", {"today1":str, "mtd":str, "ytd":str})
    personarrivalstoday_list, Personarrivalstoday = create_model("Personarrivalstoday", {"today1":str, "mtd":str, "ytd":str})
    roomdeparturestoday_list, Roomdeparturestoday = create_model("Roomdeparturestoday", {"today1":str, "mtd":str, "ytd":str})
    persondeparturestoday_list, Persondeparturestoday = create_model("Persondeparturestoday", {"today1":str, "mtd":str, "ytd":str})
    roomarrivalstomorrow_list, Roomarrivalstomorrow = create_model("Roomarrivalstomorrow", {"today1":str, "mtd":str, "ytd":str})
    personarrivalstomorrow_list, Personarrivalstomorrow = create_model("Personarrivalstomorrow", {"today1":str, "mtd":str, "ytd":str})
    roomdeparturestomorrow_list, Roomdeparturestomorrow = create_model("Roomdeparturestomorrow", {"today1":str, "mtd":str, "ytd":str})
    persondeparturestomorrow_list, Persondeparturestomorrow = create_model("Persondeparturestomorrow", {"today1":str, "mtd":str, "ytd":str})
    roomtypes_list, Roomtypes = create_model("Roomtypes", {"roomtypecode":str, "roomtypedescription":str, "todayroomnight":str, "todayrevenue":str, "mtdroomnight":str, "mtdrevenue":str, "ytdroomnight":str, "ytdrevenue":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_data, currname, currcode, reservations_list, reservationrooms_list, guests_list, travelagents_list, segmentsrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roompaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtypes_list, hotelid, filepath, str, str1, str_drr, filenm, i, reihenfolge, progname, htparam, waehrung, nightaudit, nitehist, queasy, zimkateg, arrangement, nation
        nonlocal ci_date


        nonlocal reservations, guests, reservationrooms, travelagents, header1, segmentsrevenue, totalsegmentsrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroomrevenue, totalroom, roomavailable, occupancypercentage, arr, roomrevenue, totalrevenue, fbrevenue, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roompaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtypes
        nonlocal reservations_list, guests_list, reservationrooms_list, travelagents_list, header1_list, segmentsrevenue_list, totalsegmentsrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroomrevenue_list, totalroom_list, roomavailable_list, occupancypercentage_list, arr_list, roomrevenue_list, totalrevenue_list, fbrevenue_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roompaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtypes_list

        return {"avail_data": avail_data, "currname": currname, "currcode": currcode, "reservations": reservations_list, "reservationrooms": reservationrooms_list, "guests": guests_list, "travelAgents": travelagents_list, "SegmentsRevenue": segmentsrevenue_list, "TotalSegmentsRevenue": totalsegmentsrevenue_list, "TotalRoomRevenue": totalroomrevenue_list, "TotalFBRevenue": totalfbrevenue_list, "TotalOtherRevenue": totalotherrevenue_list, "HotelNetRevenue": hotelnetrevenue_list, "HotelGrossRevenue": hotelgrossrevenue_list, "TotalRoom": totalroom_list, "RoomsAvailable": roomsavailable_list, "RoomsOccupied": roomsoccupied_list, "HouseUses": houseuses_list, "ComplimentaryRooms": complimentaryrooms_list, "RoomPaying": roompaying_list, "VacantRooms": vacantrooms_list, "OutOfOrderRooms": outoforderrooms_list, "NoShows": noshows_list, "ReservationMadeToday": reservationmadetoday_list, "CancellationForToday": cancellationfortoday_list, "EarlyCheckout": earlycheckout_list, "RoomArrivalsToday": roomarrivalstoday_list, "PersonArrivalsToday": personarrivalstoday_list, "RoomDeparturesToday": roomdeparturestoday_list, "PersonDeparturesToday": persondeparturestoday_list, "RoomArrivalsTomorrow": roomarrivalstomorrow_list, "PersonArrivalsTomorrow": personarrivalstomorrow_list, "RoomDeparturesTomorrow": roomdeparturestomorrow_list, "PersonDeparturesTomorrow": persondeparturestomorrow_list, "RoomTypes": roomtypes_list}

    def dec2char(d:decimal):

        nonlocal avail_data, currname, currcode, reservations_list, reservationrooms_list, guests_list, travelagents_list, segmentsrevenue_list, totalsegmentsrevenue_list, totalroomrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroom_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roompaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtypes_list, hotelid, filepath, str1, str_drr, filenm, i, reihenfolge, progname, htparam, waehrung, nightaudit, nitehist, queasy, zimkateg, arrangement, nation
        nonlocal ci_date


        nonlocal reservations, guests, reservationrooms, travelagents, header1, segmentsrevenue, totalsegmentsrevenue, totalfbrevenue, totalotherrevenue, hotelnetrevenue, hotelgrossrevenue, totalroomrevenue, totalroom, roomavailable, occupancypercentage, arr, roomrevenue, totalrevenue, fbrevenue, roomsavailable, roomsoccupied, houseuses, complimentaryrooms, roompaying, vacantrooms, outoforderrooms, noshows, reservationmadetoday, cancellationfortoday, earlycheckout, roomarrivalstoday, personarrivalstoday, roomdeparturestoday, persondeparturestoday, roomarrivalstomorrow, personarrivalstomorrow, roomdeparturestomorrow, persondeparturestomorrow, roomtypes
        nonlocal reservations_list, guests_list, reservationrooms_list, travelagents_list, header1_list, segmentsrevenue_list, totalsegmentsrevenue_list, totalfbrevenue_list, totalotherrevenue_list, hotelnetrevenue_list, hotelgrossrevenue_list, totalroomrevenue_list, totalroom_list, roomavailable_list, occupancypercentage_list, arr_list, roomrevenue_list, totalrevenue_list, fbrevenue_list, roomsavailable_list, roomsoccupied_list, houseuses_list, complimentaryrooms_list, roompaying_list, vacantrooms_list, outoforderrooms_list, noshows_list, reservationmadetoday_list, cancellationfortoday_list, earlycheckout_list, roomarrivalstoday_list, personarrivalstoday_list, roomdeparturestoday_list, persondeparturestoday_list, roomarrivalstomorrow_list, personarrivalstomorrow_list, roomdeparturestomorrow_list, persondeparturestomorrow_list, roomtypes_list

        str:str = ""
        d = to_decimal(round(d , 2))
        str = trim(to_string(d, "->>>>>>>>>>>9.99"))


        str = replace_str(str, ",", ".")
        return str


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 152)).first()

    if htparam:

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            currname = waehrung.bezeich
            currcode = waehrung.wabkurz

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if not nightaudit:

        return generate_output()
    reihenfolge = nightaudit.reihenfolge

    nitehist = db_session.query(Nitehist).filter(
             (Nitehist.datum == ci_date) & (Nitehist.reihenfolge == reihenfolge)).first()

    if not nitehist:

        return generate_output()

    nitehist = db_session.query(Nitehist).filter(
             (Nitehist.datum == ci_date) & (Nitehist.line == "SEND|Nitehist.0") & (Nitehist.reihenfolge == reihenfolge)).first()

    if not nitehist:
        avail_data = False

    elif nitehist:
        avail_data = True

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("RSV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            reservations = Reservations()
            reservations_list.append(reservations)

            reservations.reservationnumber = entry(1, nitehist.line, "|")
            reservations.reservationlinenumber = entry(2, nitehist.line, "|")
            reservations.arrivaldate = entry(3, nitehist.line, "|")
            reservations.departdate = entry(4, nitehist.line, "|")
            reservations.arrivalflightno = entry(5, nitehist.line, "|")
            reservations.departflightno = entry(6, nitehist.line, "|")
            reservations.arrivalflighttime = entry(7, nitehist.line, "|")
            reservations.departflighttime = entry(8, nitehist.line, "|")
            reservations.pickup = entry(9, nitehist.line, "|")
            reservations.dropoff = entry(10, nitehist.line, "|")
            reservations.nights = entry(11, nitehist.line, "|")
            reservations.adults = entry(12, nitehist.line, "|")
            reservations.childs = entry(13, nitehist.line, "|")
            reservations.infants = entry(14, nitehist.line, "|")
            reservations.infantage = entry(15, nitehist.line, "|")
            reservations.complimentary = entry(16, nitehist.line, "|")
            reservations.complimentarychild = entry(17, nitehist.line, "|")
            reservations.voucher = entry(18, nitehist.line, "|")
            reservations.travelagentcode = entry(19, nitehist.line, "|")
            reservations.ratecode = entry(20, nitehist.line, "|")
            reservations.quantity = entry(21, nitehist.line, "|")
            reservations.roomcategorycode = entry(22, nitehist.line, "|")
            reservations.roomarrangementcode = entry(23, nitehist.line, "|")
            reservations.currencycode = entry(24, nitehist.line, "|")
            reservations.roomrate = entry(25, nitehist.line, "|")
            reservations.roomrate__roomcharge = entry(26, nitehist.line, "|")
            reservations.roomrate__tax = entry(27, nitehist.line, "|")
            reservations.roomrate__service = entry(28, nitehist.line, "|")
            reservations.roomrate__breakfast = entry(29, nitehist.line, "|")
            reservations.roomrate__lunch = entry(30, nitehist.line, "|")
            reservations.roomrate__dinner = entry(31, nitehist.line, "|")
            reservations.roomrate__other = entry(32, nitehist.line, "|")
            reservations.earlybookingdiscount = entry(33, nitehist.line, "|")
            reservations.bonafidecommission = entry(34, nitehist.line, "|")
            reservations.fixrate = entry(35, nitehist.line, "|")
            reservations.billinstruction = entry(36, nitehist.line, "|")
            reservations.purpose = entry(37, nitehist.line, "|")
            reservations.memoroomnumber = entry(38, nitehist.line, "|")
            reservations.guestnumber = entry(39, nitehist.line, "|")
            reservations.guestreservationstatus = entry(40, nitehist.line, "|")
            reservations.reservationtype = entry(41, nitehist.line, "|")
            reservations.reservationrecordstatus = entry(42, nitehist.line, "|")
            reservations.reservationtime = entry(43, nitehist.line, "|")
            reservations.cancelnumber = entry(44, nitehist.line, "|")
            reservations.canceldate = entry(45, nitehist.line, "|")
            reservations.cancelreason = entry(46, nitehist.line, "|")

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (Queasy.char1 == reservations.ratecode)).first()

            if queasy:
                reservations.ratename = queasy.char2

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.kurzbez == reservations.roomcategorycode)).first()

            if zimkateg:
                reservations.roomcategoryname = zimkateg.bezeichnung

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.arrangement == reservations.roomarrangementcode)).first()

            if arrangement:
                reservations.roomarrangementname = arrangement.argt_bez

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == reservations.currencycode)).first()

            if waehrung:
                reservations.currencyname = waehrung.bezeich

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("RSV").lower()) & (entry(51, Nitehist.line, "|Nitehist.") != "") & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            reservationrooms = Reservationrooms()
            reservationrooms_list.append(reservationrooms)

            reservationrooms.reservationnumber = entry(1, nitehist.line, "|")
            reservationrooms.reservationlinenumber = entry(2, nitehist.line, "|")
            reservationrooms.roomnumber = entry(51, nitehist.line, "|")
            reservationrooms.checkintime = entry(48, nitehist.line, "|")
            reservationrooms.checkouttime = entry(47, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("GST").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            guests = Guests()
            guests_list.append(guests)

            guests.guestnumber = entry(1, nitehist.line, "|")
            guests.lastname = entry(2, nitehist.line, "|")
            guests.firstname = entry(3, nitehist.line, "|")
            guests.address = entry(4, nitehist.line, "|")
            guests.city = entry(5, nitehist.line, "|")
            guests.province = entry(6, nitehist.line, "|")
            guests.postalcode = entry(7, nitehist.line, "|")
            guests.countrycode = entry(8, nitehist.line, "|")
            guests.birthplace = entry(9, nitehist.line, "|")
            guests.birthdate = entry(10, nitehist.line, "|")
            guests.sex = entry(11, nitehist.line, "|")
            guests.phone = entry(12, nitehist.line, "|")
            guests.mobil = entry(13, nitehist.line, "|")
            guests.fax = entry(14, nitehist.line, "|")
            guests.email = entry(15, nitehist.line, "|")
            guests.occupation = entry(16, nitehist.line, "|")
            guests.idcardnumber = entry(17, nitehist.line, "|")
            guests.idcardtype = entry(18, nitehist.line, "|")
            guests.idcardexpire = entry(19, nitehist.line, "|")
            guests.companyguestnumber = entry(20, nitehist.line, "|")
            guests.selectedsegment = entry(21, nitehist.line, "|")
            guests.guestsegment = entry(22, nitehist.line, "|")
            guests.comments = entry(23, nitehist.line, "|")

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == guests.countrycode)).first()

            if nation:
                guests.countryname = nation.bezeich

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("travelAgents").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            travelagents = Travelagents()
            travelagents_list.append(travelagents)

            travelagents.code = entry(1, nitehist.line, "|")
            travelagents.name = entry(2, nitehist.line, "|")
            travelagents.salutation = entry(3, nitehist.line, "|")
            travelagents.address = entry(4, nitehist.line, "|")
            travelagents.city = entry(5, nitehist.line, "|")
            travelagents.zip = entry(6, nitehist.line, "|")
            travelagents.countrycode = entry(7, nitehist.line, "|")
            travelagents.phone = entry(8, nitehist.line, "|")
            travelagents.telefax = entry(9, nitehist.line, "|")
            travelagents.email = entry(10, nitehist.line, "|")
            travelagents.ratecode = entry(11, nitehist.line, "|")
            travelagents.mainsegment = entry(12, nitehist.line, "|")
            travelagents.booksource = entry(13, nitehist.line, "|")
            travelagents.comments = entry(14, nitehist.line, "|")

            nation = db_session.query(Nation).filter(
                     (Nation.kurzbez == travelAgents.countrycode)).first()

            if nation:
                travelagents.countryname = nation.bezeich

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("SEGREV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            segmentsrevenue = Segmentsrevenue()
            segmentsrevenue_list.append(segmentsrevenue)

            segmentsrevenue.segmentcode = entry(1, nitehist.line, "|")
            segmentsrevenue.segmentdescription = entry(2, nitehist.line, "|")
            segmentsrevenue.segmentcomment = entry(14, nitehist.line, "|")
            segmentsrevenue.todayroomnight = entry(3, nitehist.line, "|")
            segmentsrevenue.todayrevenue = entry(4, nitehist.line, "|")
            segmentsrevenue.todayrevenuepercentage = entry(5, nitehist.line, "|")
            segmentsrevenue.mtdroomnight = entry(6, nitehist.line, "|")
            segmentsrevenue.mtdrevenue = entry(7, nitehist.line, "|")
            segmentsrevenue.mtdrevenuepercentage = entry(8, nitehist.line, "|")
            segmentsrevenue.ytdroomnight = entry(9, nitehist.line, "|")
            segmentsrevenue.ytdrevenue = entry(10, nitehist.line, "|")
            segmentsrevenue.ytdrevenuepercentage = entry(11, nitehist.line, "|")
            segmentsrevenue.budget = entry(12, nitehist.line, "|")
            segmentsrevenue.variance = entry(13, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("TOTAL-SEGMENT").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            totalsegmentsrevenue = Totalsegmentsrevenue()
            totalsegmentsrevenue_list.append(totalsegmentsrevenue)

            totalsegmentsrevenue.today1 = entry(1, nitehist.line, "|")
            totalsegmentsrevenue.todaypercentage = entry(2, nitehist.line, "|")
            totalsegmentsrevenue.mtd = entry(3, nitehist.line, "|")
            totalsegmentsrevenue.mtdpercentage = entry(4, nitehist.line, "|")
            totalsegmentsrevenue.budget = entry(7, nitehist.line, "|")
            totalsegmentsrevenue.variance = entry(8, nitehist.line, "|")
            totalsegmentsrevenue.ytd = entry(5, nitehist.line, "|")
            totalsegmentsrevenue.ytdpercentage = entry(6, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("TOTAL-ROOMREV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            totalroomrevenue = Totalroomrevenue()
            totalroomrevenue_list.append(totalroomrevenue)

            totalroomrevenue.today1 = entry(1, nitehist.line, "|")
            totalroomrevenue.todaypercentage = entry(2, nitehist.line, "|")
            totalroomrevenue.mtd = entry(3, nitehist.line, "|")
            totalroomrevenue.mtdpercentage = entry(4, nitehist.line, "|")
            totalroomrevenue.budget = entry(7, nitehist.line, "|")
            totalroomrevenue.variance = entry(8, nitehist.line, "|")
            totalroomrevenue.ytd = entry(5, nitehist.line, "|")
            totalroomrevenue.ytdpercentage = entry(6, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("TOTAL-FBREV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            totalfbrevenue = Totalfbrevenue()
            totalfbrevenue_list.append(totalfbrevenue)

            totalfbrevenue.today1 = entry(1, nitehist.line, "|")
            totalfbrevenue.todaypercentage = entry(2, nitehist.line, "|")
            totalfbrevenue.mtd = entry(3, nitehist.line, "|")
            totalfbrevenue.mtdpercentage = entry(4, nitehist.line, "|")
            totalfbrevenue.budget = entry(7, nitehist.line, "|")
            totalfbrevenue.variance = entry(8, nitehist.line, "|")
            totalfbrevenue.ytd = entry(5, nitehist.line, "|")
            totalfbrevenue.ytdpercentage = entry(6, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("TOTAL-OTHERREV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            totalotherrevenue = Totalotherrevenue()
            totalotherrevenue_list.append(totalotherrevenue)

            totalotherrevenue.today1 = entry(1, nitehist.line, "|")
            totalotherrevenue.todaypercentage = entry(2, nitehist.line, "|")
            totalotherrevenue.mtd = entry(3, nitehist.line, "|")
            totalotherrevenue.mtdpercentage = entry(4, nitehist.line, "|")
            totalotherrevenue.budget = entry(7, nitehist.line, "|")
            totalotherrevenue.variance = entry(8, nitehist.line, "|")
            totalotherrevenue.ytd = entry(5, nitehist.line, "|")
            totalotherrevenue.ytdpercentage = entry(6, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("NETREV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            hotelnetrevenue = Hotelnetrevenue()
            hotelnetrevenue_list.append(hotelnetrevenue)

            hotelnetrevenue.today1 = entry(1, nitehist.line, "|")
            hotelnetrevenue.todaypercentage = entry(2, nitehist.line, "|")
            hotelnetrevenue.mtd = entry(3, nitehist.line, "|")
            hotelnetrevenue.mtdpercentage = entry(4, nitehist.line, "|")
            hotelnetrevenue.budget = entry(7, nitehist.line, "|")
            hotelnetrevenue.variance = entry(8, nitehist.line, "|")
            hotelnetrevenue.ytd = entry(5, nitehist.line, "|")
            hotelnetrevenue.ytdpercentage = entry(6, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("GROSSREV").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            hotelgrossrevenue = Hotelgrossrevenue()
            hotelgrossrevenue_list.append(hotelgrossrevenue)

            hotelgrossrevenue.today1 = entry(1, nitehist.line, "|")
            hotelgrossrevenue.todaypercentage = entry(2, nitehist.line, "|")
            hotelgrossrevenue.mtd = entry(3, nitehist.line, "|")
            hotelgrossrevenue.mtdpercentage = entry(4, nitehist.line, "|")
            hotelgrossrevenue.budget = entry(7, nitehist.line, "|")
            hotelgrossrevenue.variance = entry(8, nitehist.line, "|")
            hotelgrossrevenue.ytd = entry(5, nitehist.line, "|")
            hotelgrossrevenue.ytdpercentage = entry(6, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("TOTAL-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            totalroom = Totalroom()
            totalroom_list.append(totalroom)

            totalroom.today1 = entry(1, nitehist.line, "|")
            totalroom.mtd = entry(2, nitehist.line, "|")
            totalroom.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("ROOM-AVAIL").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomsavailable = Roomsavailable()
            roomsavailable_list.append(roomsavailable)

            roomsavailable.today1 = entry(1, nitehist.line, "|")
            roomsavailable.mtd = entry(2, nitehist.line, "|")
            roomsavailable.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("ROOM-OCC").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomsoccupied = Roomsoccupied()
            roomsoccupied_list.append(roomsoccupied)

            roomsoccupied.today1 = entry(1, nitehist.line, "|")
            roomsoccupied.mtd = entry(2, nitehist.line, "|")
            roomsoccupied.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("HOUSE-USE").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            houseuses = Houseuses()
            houseuses_list.append(houseuses)

            houseuses.today1 = entry(1, nitehist.line, "|")
            houseuses.mtd = entry(2, nitehist.line, "|")
            houseuses.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("COMP-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            complimentaryrooms = Complimentaryrooms()
            complimentaryrooms_list.append(complimentaryrooms)

            complimentaryrooms.today1 = entry(1, nitehist.line, "|")
            complimentaryrooms.mtd = entry(2, nitehist.line, "|")
            complimentaryrooms.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("PAY-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roompaying = Roompaying()
            roompaying_list.append(roompaying)

            roompaying.today1 = entry(1, nitehist.line, "|")
            roompaying.mtd = entry(2, nitehist.line, "|")
            roompaying.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("VACANT-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            vacantrooms = Vacantrooms()
            vacantrooms_list.append(vacantrooms)

            vacantrooms.today1 = entry(1, nitehist.line, "|")
            vacantrooms.mtd = entry(2, nitehist.line, "|")
            vacantrooms.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("OOO-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            outoforderrooms = Outoforderrooms()
            outoforderrooms_list.append(outoforderrooms)

            outoforderrooms.today1 = entry(1, nitehist.line, "|")
            outoforderrooms.mtd = entry(2, nitehist.line, "|")
            outoforderrooms.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("NO-SHOW").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            noshows = Noshows()
            noshows_list.append(noshows)

            noshows.today1 = entry(1, nitehist.line, "|")
            noshows.mtd = entry(2, nitehist.line, "|")
            noshows.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("RSV-TODAY").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            reservationmadetoday = Reservationmadetoday()
            reservationmadetoday_list.append(reservationmadetoday)

            reservationmadetoday.today1 = entry(1, nitehist.line, "|")
            reservationmadetoday.mtd = entry(2, nitehist.line, "|")
            reservationmadetoday.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("CANCEL-TODAY").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            cancellationfortoday = Cancellationfortoday()
            cancellationfortoday_list.append(cancellationfortoday)

            cancellationfortoday.today1 = entry(1, nitehist.line, "|")
            cancellationfortoday.mtd = entry(2, nitehist.line, "|")
            cancellationfortoday.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("EARLY-CO").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            earlycheckout = Earlycheckout()
            earlycheckout_list.append(earlycheckout)

            earlycheckout.today1 = entry(1, nitehist.line, "|")
            earlycheckout.mtd = entry(2, nitehist.line, "|")
            earlycheckout.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("ARR-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomarrivalstoday = Roomarrivalstoday()
            roomarrivalstoday_list.append(roomarrivalstoday)

            roomarrivalstoday.today1 = entry(1, nitehist.line, "|")
            roomarrivalstoday.mtd = entry(2, nitehist.line, "|")
            roomarrivalstoday.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("ARR-PERSON").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            personarrivalstoday = Personarrivalstoday()
            personarrivalstoday_list.append(personarrivalstoday)

            personarrivalstoday.today1 = entry(1, nitehist.line, "|")
            personarrivalstoday.mtd = entry(2, nitehist.line, "|")
            personarrivalstoday.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("DEPT-ROOM").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomdeparturestoday = Roomdeparturestoday()
            roomdeparturestoday_list.append(roomdeparturestoday)

            roomdeparturestoday.today1 = entry(1, nitehist.line, "|")
            roomdeparturestoday.mtd = entry(2, nitehist.line, "|")
            roomdeparturestoday.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("DEPT-PERSON").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            persondeparturestoday = Persondeparturestoday()
            persondeparturestoday_list.append(persondeparturestoday)

            persondeparturestoday.today1 = entry(1, nitehist.line, "|")
            persondeparturestoday.mtd = entry(2, nitehist.line, "|")
            persondeparturestoday.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == "ROOM-ARR-TOMORNitehist.ROW") & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomarrivalstomorrow = Roomarrivalstomorrow()
            roomarrivalstomorrow_list.append(roomarrivalstomorrow)

            roomarrivalstomorrow.today1 = entry(1, nitehist.line, "|")
            roomarrivalstomorrow.mtd = entry(2, nitehist.line, "|")
            roomarrivalstomorrow.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == "PERSON-ARR-TOMORNitehist.ROW") & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            personarrivalstomorrow = Personarrivalstomorrow()
            personarrivalstomorrow_list.append(personarrivalstomorrow)

            personarrivalstomorrow.today1 = entry(1, nitehist.line, "|")
            personarrivalstomorrow.mtd = entry(2, nitehist.line, "|")
            personarrivalstomorrow.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == "ROOM-DEPT-TOMORNitehist.ROW") & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomdeparturestomorrow = Roomdeparturestomorrow()
            roomdeparturestomorrow_list.append(roomdeparturestomorrow)

            roomdeparturestomorrow.today1 = entry(1, nitehist.line, "|")
            roomdeparturestomorrow.mtd = entry(2, nitehist.line, "|")
            roomdeparturestomorrow.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == "PERSON-DEPT-TOMORNitehist.ROW") & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            persondeparturestomorrow = Persondeparturestomorrow()
            persondeparturestomorrow_list.append(persondeparturestomorrow)

            persondeparturestomorrow.today1 = entry(1, nitehist.line, "|")
            persondeparturestomorrow.mtd = entry(2, nitehist.line, "|")
            persondeparturestomorrow.ytd = entry(3, nitehist.line, "|")

        for nitehist in db_session.query(Nitehist).filter(
                 (Nitehist.datum == ci_date) & (entry(0, Nitehist.line, "|Nitehist.") == ("RoomTypes").lower()) & (Nitehist.reihenfolge == reihenfolge)).order_by(Nitehist._recid).all():
            roomtypes = Roomtypes()
            roomtypes_list.append(roomtypes)

            roomtypes.roomtypecode = entry(1, nitehist.line, "|")
            roomtypes.roomtypedescription = entry(2, nitehist.line, "|")
            roomtypes.todayroomnight = entry(3, nitehist.line, "|")
            roomtypes.todayrevenue = entry(4, nitehist.line, "|")
            roomtypes.mtdroomnight = entry(5, nitehist.line, "|")
            roomtypes.mtdrevenue = entry(6, nitehist.line, "|")
            roomtypes.ytdroomnight = entry(7, nitehist.line, "|")
            roomtypes.ytdrevenue = entry(8, nitehist.line, "|")

    return generate_output()