#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.nt_tauziarpt_gen_occfcast_gsheetbl import nt_tauziarpt_gen_occfcast_gsheetbl
from functions.nt_tauziarpt_gen_occfcastbl import nt_tauziarpt_gen_occfcastbl
from functions.nt_tauziarpt_gen_clientdatabl import nt_tauziarpt_gen_clientdatabl
from functions.nt_tauziarpt_gen_revdatabl import nt_tauziarpt_gen_revdatabl
from functions.nt_tauziarpt_gen_otbmseg_gsheetbl import nt_tauziarpt_gen_otbmseg_gsheetbl
from models import Guest, Segment

def tauziarpt_webbl(curr_date:date, occrpt:bool, occ_month:int, occ_year:int, linkgsheet:string, filenm:string, guestrpt:bool, fdate:date, tdate:date, revrpt:bool, fdate1:date, tdate1:date, otbmseg:bool, otbmonth:int, otbyear:int):
    occupancy_forecast_data = []
    t_list_data = []
    s_list_data = []
    u_list_data = []
    week_list:List[string] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    month_list:List[string] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
    guest = segment = None

    s_list = t_list = u_list = segtmp = occupancy_forecast = None

    s_list_data, S_list = create_model("S_list", {"gastnr":int, "datum":string, "name":string, "address":string, "city":string, "zimmeranz":int, "lodging":Decimal})
    t_list_data, T_list = create_model_like(Guest, {"cp1":string, "cp2":string, "cp3":string, "guest_name":string, "guest_adr":string})
    u_list_data, U_list = create_model("U_list", {"rmsegmt":int, "rmrev":Decimal})
    occupancy_forecast_data, Occupancy_forecast = create_model("Occupancy_forecast", {"datum":string, "days":string, "group_onhand_definite":int, "group_onhand_tentative":int, "booking_onhand_fit":int, "total_otb_group_fit":int, "total_room_avail":int, "arr_otb":int, "total_otb_percent":string, "leadtime_booking":int, "samedate_lastyear":int, "samedate_lastyear_percent":string, "arr_last_year":int})

    Segtmp = create_buffer("Segtmp",Segment)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, week_list, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data

        return {"occupancy-forecast": occupancy_forecast_data, "t-list": t_list_data, "s-list": s_list_data, "u-list": u_list_data}

    def generate_occupancyforecast():

        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, week_list, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data

        currdate:date = None
        lydate:date = None
        i:int = 0
        j:int = 1
        lastday:int = 0
        lylastday:int = 0
        qtyfit:int = 0
        qtygroupd:int = 0
        qtygroupt:int = 0
        lyqtyfit:int = 0
        lyqtygroupd:int = 0
        lyqtygroupt:int = 0
        avrgrate:Decimal = to_decimal("0.0")
        lyavrgrate:Decimal = to_decimal("0.0")
        qtytotal:int = 0
        lyqtytotal:int = 0
        lytotal:int = 0
        totroom:int = 0
        lytotroom:int = 0
        grandtot_fit:int = 0
        grandtot_groupd:int = 0
        grandtotqty:int = 0
        grandlytotqty:int = 0
        grandtotroom:int = 0
        grandtotlyroom:int = 0
        str_avfit:string = ""
        str_avgroupd:string = ""
        str_qtytotal:string = ""
        str_qtytotally:string = ""
        str_gtqty:string = ""
        str_gtroom:string = ""
        str_gtroomly:string = ""
        lead_time:Decimal = to_decimal("0.0")
        pay:int = 0
        lypay:int = 0
        casetype:int = 0

        if linkgsheet == None:
            linkgsheet = ""

        if linkgsheet != "":
            get_output(nt_tauziarpt_gen_occfcast_gsheetbl(curr_date, occ_month, occ_year, filenm, linkgsheet))
        else:
            for i in range(0,2  + 1) :
                grandtot_fit = 0
                grandtot_groupd = 0
                grandtotqty = 0
                grandlytotqty = 0
                grandtotroom = 0
                grandtotlyroom = 0


                lastday = lastdayinmonth(occ_month + i, occ_year)
                lylastday = lastdayinmonth(occ_month + i, occ_year - 1)

                if occ_month > 10:

                    if occ_month + i == 13:
                        lastday = lastdayinmonth(1, occ_year + 1)
                        lylastday = lastdayinmonth(1, occ_year)

                    elif occ_month + i == 14:
                        lastday = lastdayinmonth(2, occ_year + 1)
                        lylastday = lastdayinmonth(2, occ_year)
                for j in range(1,lastday  + 1) :

                    if occ_month + i == 13:
                        currdate = date_mdy(1, j, occ_year + 1)
                        lydate = date_mdy(1, j , occ_year)

                    elif occ_month + i == 14:
                        currdate = date_mdy(2, j, occ_year + 1)

                        if get_month(currdate) == 2 and get_day(currdate) == 29 and get_year(currdate) % 4 == 0:
                            lydate = date_mdy(2, 28 , occ_year)
                        else:
                            lydate = date_mdy(2, j , occ_year)
                    else:
                        currdate = date_mdy(occ_month + i, j, occ_year)

                        if get_month(currdate) == 2 and get_day(currdate) == 29 and get_year(currdate) % 4 == 0:
                            lydate = date_mdy(occ_month + i, 28 , occ_year - 1)
                        else:
                            lydate = date_mdy(occ_month + i, j , occ_year - 1)

                    if currdate < curr_date:
                        casetype = 1
                    else:
                        casetype = 2
                    avrgrate, lyavrgrate, qtygroupd, lyqtygroupd, qtygroupt, qtyfit, lyqtyfit, totroom, lytotroom, lead_time, pay, lypay = get_output(nt_tauziarpt_gen_occfcastbl(lydate, casetype, currdate, curr_date))
                    qtytotal = qtyfit + qtygroupd
                    lyqtytotal = lyqtyfit + lyqtygroupd
                    grandtot_fit = grandtot_fit + qtyfit
                    grandtot_groupd = grandtot_groupd + qtygroupd
                    grandtotqty = grandtotqty + qtytotal
                    grandlytotqty = grandlytotqty + lyqtytotal
                    grandtotroom = grandtotroom + totroom
                    grandtotlyroom = grandtotlyroom + lytotroom


                    str_qtytotal = create_decimal(to_string((pay / totroom) * 100), 8)
                    str_qtytotally = create_decimal(to_string((lypay / lytotroom) * 100), 8)
                    occupancy_forecast = Occupancy_forecast()
                    occupancy_forecast_data.append(occupancy_forecast)

                    datum = to_string(currdate)
                    days = week_list[get_weekday(currdate) - 1]
                    group_onhand_definite = qtygroupd
                    group_onhand_tentative = qtygroupt
                    booking_onhand_fit = qtyfit
                    total_otb_group_fit = qtytotal
                    total_room_avail = totroom
                    arr_otb = avrgrate
                    total_otb_percent = str_qtytotal
                    leadtime_booking = lead_time
                    samedate_lastyear = lyqtytotal
                    samedate_lastyear_percent = str_qtytotally
                    arr_last_year = lyavrgrate


                occupancy_forecast = Occupancy_forecast()
                occupancy_forecast_data.append(occupancy_forecast)

                datum = "Total"
                days = ""
                group_onhand_definite = grandtot_groupd
                group_onhand_tentative = 0
                booking_onhand_fit = grandtot_fit
                total_otb_group_fit = grandtotqty
                total_room_avail = grandtotroom
                arr_otb = 0
                total_otb_percent = ""
                leadtime_booking = 0
                samedate_lastyear = grandlytotqty
                samedate_lastyear_percent = ""
                arr_last_year = 0


                str_avfit = create_decimal(to_string(grandtot_fit / (lastday - 1)), 6)
                str_avgroupd = create_decimal(to_string(grandtot_groupd / (lastday - 1)), 6)
                str_gtqty = create_decimal(to_string(grandtotqty / (lastday - 1)), 6)
                str_gtroom = create_decimal(to_string(grandtotroom / (lastday - 1)), 6)
                str_gtroomly = create_decimal(to_string(grandlytotqty / (lylastday - 1)), 6)
                occupancy_forecast = Occupancy_forecast()
                occupancy_forecast_data.append(occupancy_forecast)

                datum = "Average"
                days = ""
                group_onhand_definite = to_int(str_avgroupd)
                group_onhand_tentative = 0
                booking_onhand_fit = to_int(str_avfit)
                total_otb_group_fit = to_int(str_gtqty)
                total_room_avail = to_int(str_gtroom)
                arr_otb = 0
                total_otb_percent = ""
                leadtime_booking = 0
                samedate_lastyear = to_int(str_gtroomly)
                samedate_lastyear_percent = ""
                arr_last_year = 0


    def generate_clientdata():

        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, week_list, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data


        t_list_data = get_output(nt_tauziarpt_gen_clientdatabl(2, curr_date, fdate, tdate))


    def generate_revenuedata():

        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, week_list, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data


        s_list_data = get_output(nt_tauziarpt_gen_revdatabl(fdate1, tdate1))


    def lastdayinmonth(intmont:int, intyear:int):

        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, week_list, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data

        lastday = 0

        def generate_inner_output():
            return (lastday)


        if intmont == 1 or intmont == 3 or intmont == 5 or intmont == 7 or intmont == 8 or intmont == 10 or intmont == 12:
            lastday = 31
        elif intmont == 4 or intmont == 6 or intmont == 9 or intmont == 11:
            lastday = 30
        elif intmont == 2:

            if (intyear % 4) == 0:
                lastday = 29
            else:
                lastday = 28

        return generate_inner_output()


    def create_decimal(strprice:string, digit:int):

        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, week_list, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data

        stramount = ""
        sint:string = ""
        sdec:string = ""
        i:int = 0
        ndec:string = ""

        def generate_inner_output():
            return (stramount)


        if strprice == "":

            return generate_inner_output()

        if num_entries(strprice, ".") > 1:
            sint = entry(0, strprice, ".")
            sdec = entry(1, strprice, ".")

            if length(sdec) > 2:
                ndec = substring(sdec, 0, 2)
            else:
                ndec = sdec

            if digit > (length(sint) + length(ndec) + 1):
                for i in range(1,(digit - (length(sint) + length(ndec) + 1))  + 1) :
                    stramount = stramount + " "

            if to_int(sint) == 0:
                stramount = stramount + "0." + ndec
            else:
                stramount = stramount + sint + "." + ndec
        else:

            if length(strprice) < digit:
                for i in range(1,(digit - length(strprice))  + 1) :
                    stramount = stramount + " "
                stramount = stramount + strprice
            else:
                stramount = strprice

        return generate_inner_output()


    def generate_otbmseg():

        nonlocal occupancy_forecast_data, t_list_data, s_list_data, u_list_data, month_list, guest, segment
        nonlocal curr_date, occrpt, occ_month, occ_year, linkgsheet, filenm, guestrpt, fdate, tdate, revrpt, fdate1, tdate1, otbmseg, otbmonth, otbyear
        nonlocal segtmp


        nonlocal s_list, t_list, u_list, segtmp, occupancy_forecast
        nonlocal s_list_data, t_list_data, u_list_data, occupancy_forecast_data

        currdate:date = None
        lydate:date = None
        lastday:int = 0
        j:int = 1
        h:int = 0
        icolseg:int = 0
        irowseg:int = 0
        icolumn:int = 0
        ccolumn:string = ""
        crange:string = ""
        curr_row:int = 7
        week_row:List[int] = create_empty_list(2,0)
        curr_col:int = 1
        totroom:int = 0
        rsold:int = 0
        rrev:Decimal = to_decimal("0.0")
        rseg:string = ""
        colseg:string = ""
        tmpseg:string = ""
        week_list:List[string] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        totroom, u_list_data = get_output(nt_tauziarpt_gen_otbmseg_gsheetbl(None))

    if occrpt:
        generate_occupancyforecast()

    if guestrpt:
        generate_clientdata()

    if revrpt:
        generate_revenuedata()

    if otbmseg:
        generate_otbmseg()

    return generate_output()