from datetime import date
from sqlalchemy import func, and_, case, Integer, Date, or_
from decimal import Decimal
from functions.additional_functions import *
from models.res_line import Res_line
from models.reservation import Reservation
from models.segment import Segment
from models.zimkateg import Zimkateg
from models.arrangement import Arrangement
from models.guest import Guest
from models.nation import Nation
from models.htparam import Htparam


def ai_generated_content():
    def ai_arrival_guest_report(*args, **kwargs):
        param1 = kwargs['param1']
        param2 = kwargs['param2']
        param3 = kwargs['param3']

        db_session = local_storage.db_session

        # Step 1: Get system date
        param87 = db_session.query(Htparam).filter(Htparam.paramnr == 87).first()
        system_date = param87.fdate if param87 else None
        if not system_date:
            def generate_output():
                return {'error': 'System date not configured'}
            return generate_output()

        # Step 2: Get segment codes for OTA and FIT
        ota_segment = db_session.query(Segment).filter(Segment.bezeich == 'OTA').first()
        fit_segment = db_session.query(Segment).filter(Segment.bezeich == 'FIT').first()
        ota_code = ota_segment.segmentcode if ota_segment else None
        fit_code = fit_segment.segmentcode if fit_segment else None

        if ota_code is None or fit_code is None:
            def generate_output():
                return {'error': 'OTA or FIT segment not found'}
            return generate_output()

        # Step 3: Define date range
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 3)

        # Step 4: Query res-line for arrival guests
        # query = db_session.query(
        #         Res_line.zinr.label("room_number"),
        #         Res_line.resnr.label("reservation_number"),
        #         Res_line.name.label("guest_name"),
        #         Res_line.ankunft.label("arrival_date"),
        #         Res_line.abreise.label("departure_date"),
        #         Res_line.zipreis.label("room_rate")
        #     ).join(
        #         Reservation, Reservation.resnr == Res_line.resnr
        #     ).filter(
        #         Res_line.ankunft >= start_date,
        #         Res_line.ankunft <= end_date,
        #         Res_line.resstatus.in_([1, 2, 5, 6]),
        #         Res_line.gratis == 0,
        #         Reservation.resart > 0,
        #     ).order_by(
        #         Res_line.ankunft,
        #         Res_line.zinr
        #     )
        
        query = db_session.query(
            Res_line.zinr.label("room_number"),
            Res_line.resnr.label("reservation_number"),
            Res_line.name.label("guest_name"),
            Zimkateg.kurzbez.label("room_type"),
            Nation.kurzbez.label("nationality"),
            Res_line.ankunft.label("arrival_date"),
            Res_line.abreise.label("departure_date"),
            Segment.bezeich.label("segment_code"),
            Arrangement.argt_bez.label("arrangement"),
            Res_line.zipreis.label("room_rate")
        ).join(
            Reservation, Reservation.resnr == Res_line.resnr
        ).join(
            Segment, Segment.segmentcode == Reservation.segmentcode
        ).join(
            Guest, Guest.gastnr == Reservation.gastnr
        ).join(
            Nation, Nation.kurzbez == Guest.nation1
        ).join(
            Zimkateg, Zimkateg.zikatnr == Res_line.zikatnr
        ).join(  # Changed from outerjoin to join
            Arrangement, Arrangement.arrangement == Res_line.arrangement
        ).filter(
            Res_line.ankunft >= start_date,
            Res_line.ankunft <= end_date,
            Res_line.resstatus.in_([1, 2, 5, 6]),
            Res_line.gratis == 0,
            Reservation.resart > 0,
            Segment.segmentcode.in_([ota_code, fit_code])
        ).order_by(
            Res_line.ankunft,
            Res_line.zinr
        )
        nrec = query.count()

    

        def generate_output():
            return {'nrec': nrec}

        return generate_output()

    return ai_arrival_guest_report(param1="xx", param2=123, param3=True)




"""
from datetime import date
from sqlalchemy import func, and_, case, Integer, Date, or_
from decimal import Decimal
from functions.additional_functions import *
from models.res_line import Res_line
from models.reservation import Reservation
from models.segment import Segment
from models.zimkateg import Zimkateg
from models.arrangement import Arrangement
from models.guest import Guest
from models.nation import Nation
from models.htparam import Htparam


def ai_generated_content():
    def ai_arrival_guest_report(*args, **kwargs):
        param1 = kwargs['param1']
        param2 = kwargs['param2']
        param3 = kwargs['param3']

        db_session = local_storage.db_session

        # Step 1: Get system date
        param87 = db_session.query(Htparam).filter(Htparam.paramnr == 87).first()
        system_date = param87.fdate if param87 else None
        if not system_date:
            def generate_output():
                return {'error': 'System date not configured'}
            return generate_output()

        # Step 2: Get segment codes for OTA and FIT
        ota_segment = db_session.query(Segment).filter(Segment.bezeich == 'OTA').first()
        fit_segment = db_session.query(Segment).filter(Segment.bezeich == 'FIT').first()
        ota_code = ota_segment.segmentcode if ota_segment else None
        fit_code = fit_segment.segmentcode if fit_segment else None

        if ota_code is None or fit_code is None:
            def generate_output():
                return {'error': 'OTA or FIT segment not found'}
            return generate_output()

        # Step 3: Define date range
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 3)

        # Step 4: Query res-line for arrival guests
        query = db_session.query(
            Res_line.zinr.label("room_number"),
            Res_line.resnr.label("reservation_number"),
            Res_line.name.label("guest_name"),
            Zimkateg.kurzbez.label("room_type"),
            Nation.kurzbez.label("nationality"),
            Res_line.ankunft.label("arrival_date"),
            Res_line.abreise.label("departure_date"),
            Segment.bezeich.label("segment_code"),
            Arrangement.argt_bez.label("arrangement"),
            Res_line.zipreis.label("room_rate")
        ).join(
            Reservation, Reservation.resnr == Res_line.resnr
        ).join(
            Segment, Segment.segmentcode == Reservation.segmentcode
        ).join(
            Guest, Guest.gastnr == Reservation.gastnr
        ).join(
            Nation, Nation.kurzbez == Guest.nation1
        ).join(
            Zimkateg, Zimkateg.zikatnr == Res_line.zikatnr
        ).outerjoin(
            Arrangement, Arrangement.arrangement == Res_line.arrangement
        ).filter(
            Res_line.ankunft >= start_date,
            Res_line.ankunft <= end_date,
            Res_line.resstatus.in_([1, 2, 5, 6]),
            Res_line.gratis == 0,
            Reservation.resart > 0,
            Segment.segmentcode.in_([ota_code, fit_code])
        ).order_by(
            Res_line.ankunft,
            Res_line.zinr
        )

        results = []
        for row in query.all():
            results.append({
                "Room Number": row.room_number,
                "Reservation Number": row.reservation_number,
                "Guest Name": row.guest_name,
                "Room Type": row.room_type,
                "Nationality": row.nationality,
                "Arrival Date": row.arrival_date.isoformat(),
                "Departure Date": row.departure_date.isoformat(),
                "Segment Code": row.segment_code,
                "Arrangement": row.arrangement if row.arrangement else "",
                "Room Rate": float(row.room_rate) if row.room_rate else 0.0
            })

        def generate_output():
            return {'result': results}

        return generate_output()

    return ai_arrival_guest_report(param1="xx", param2=123, param3=True)
    """