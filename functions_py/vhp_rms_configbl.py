#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

report_list_data, Report_list = create_model("Report_list", {"nr":int, "report_name":string, "activate_flag":bool, "activate_date":date})

def vhp_rms_configbl(case_type:int, report_list_data:[Report_list]):

    prepare_cache ([Queasy])

    loop_i:int = 0
    rpt_list:List[string] = create_empty_list(14,"")
    queasy = None

    report_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal loop_i, rpt_list, queasy
        nonlocal case_type


        nonlocal report_list

        return {"report-list": report_list_data}


    rpt_list[0] = "Master Data"
    rpt_list[1] = "Room Overview"
    rpt_list[2] = "Room Availability"
    rpt_list[3] = "Monthly Forecast Of Room Occupancy"
    rpt_list[4] = "Forecast Room Production"
    rpt_list[5] = "Future Booking"
    rpt_list[6] = "Reservation By Creation Date"
    rpt_list[7] = "Inhouse Guest List"
    rpt_list[8] = "Cancelled Reservation"
    rpt_list[9] = "Room Revenue Breakdown"
    rpt_list[10] = "Front Office Turnover Report"
    rpt_list[11] = "Company Room Production"
    rpt_list[12] = "Travel Agent Room Production"
    rpt_list[13] = "Room Recapitulation With Guest Segment"

    if case_type == 1:
        for loop_i in range(1,14 + 1) :

            # queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 1)],"number1": [(eq, loop_i)]})
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 347) &
                (Queasy.betriebsnr == 1) &
                (Queasy.number1 == loop_i)).with_for_update().first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 347
                queasy.betriebsnr = 1
                queasy.number1 = loop_i
                queasy.char1 = rpt_list[loop_i - 1]
                queasy.logi1 = False
                queasy.date1 = None

    elif case_type == 2:

        for report_list in query(report_list_data):

            # queasy = get_cache (Queasy, {"key": [(eq, 347)],"betriebsnr": [(eq, 1)],"number1": [(eq, report_list.nr)]})
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 347) & (Queasy.betriebsnr == 1) & (Queasy.number1 == report_list.nr)).with_for_update().first()

            if queasy:

                if report_list.activate_flag != queasy.logi1:
                    pass
                    queasy.logi1 = report_list.activate_flag
                    queasy.date1 = get_current_date()

                    pass
                pass
    report_list_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 347) & (Queasy.betriebsnr == 1)).order_by(Queasy._recid).all():
        report_list = Report_list()
        report_list_data.append(report_list)

        report_list.nr = queasy.number1
        report_list.report_name = queasy.char1
        report_list.activate_flag = queasy.logi1
        report_list.activate_date = queasy.date1

    return generate_output()