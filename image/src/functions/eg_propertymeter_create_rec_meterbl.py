from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_propmeter

def eg_propertymeter_create_rec_meterbl():
    rec_meter_list = []
    eg_propmeter = None

    rec_meter = None

    rec_meter_list, Rec_meter = create_model("Rec_meter", {"prop_nr":int, "rec_date":date, "rec_time":int, "rec_by":str, "rec_hour":int, "rec_meter":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_meter_list, eg_propmeter


        nonlocal rec_meter
        nonlocal rec_meter_list
        return {"rec-meter": rec_meter_list}

    def create_rec_meter():

        nonlocal rec_meter_list, eg_propmeter


        nonlocal rec_meter
        nonlocal rec_meter_list


        rec_meter_list.clear()

        for eg_propmeter in db_session.query(Eg_propmeter).all():
            rec_meter = Rec_meter()
            rec_meter_list.append(rec_meter)

            rec_meter.prop_nr = eg_propMeter.propertynr
            rec_meter.rec_date = eg_propMeter.rec_date
            rec_meter.rec_time = eg_propMeter.rec_time
            rec_meter.rec_by = eg_propMeter.rec_by
            rec_meter.rec_hour = eg_propMeter.val_hour
            rec_meter.rec_meter = eg_propMeter.val_meter


    create_rec_meter()

    return generate_output()