#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_propmeter

def eg_propertymeter_create_rec_meterbl():

    prepare_cache ([Eg_propmeter])

    rec_meter_data = []
    eg_propmeter = None

    rec_meter = None

    rec_meter_data, Rec_meter = create_model("Rec_meter", {"prop_nr":int, "rec_date":date, "rec_time":int, "rec_by":string, "rec_hour":int, "rec_meter":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_meter_data, eg_propmeter


        nonlocal rec_meter
        nonlocal rec_meter_data

        return {"rec-meter": rec_meter_data}

    def create_rec_meter():

        nonlocal rec_meter_data, eg_propmeter


        nonlocal rec_meter
        nonlocal rec_meter_data


        rec_meter_data.clear()

        for eg_propmeter in db_session.query(Eg_propmeter).order_by(Eg_propmeter._recid).all():
            rec_meter = Rec_meter()
            rec_meter_data.append(rec_meter)

            rec_meter.prop_nr = eg_propmeter.propertynr
            rec_meter.rec_date = eg_propmeter.rec_date
            rec_meter.rec_time = eg_propmeter.rec_time
            rec_meter.rec_by = eg_propmeter.rec_by
            rec_meter.rec_hour = eg_propmeter.val_hour
            rec_meter.rec_meter = eg_propmeter.val_meter

    create_rec_meter()

    return generate_output()