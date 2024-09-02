from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_propmeter

def eg_propertymeter_btn_okbl(temp_rec:[Temp_rec], user_init:str, blframe:int, frd:date, tod:date, intres:int):
    eg_propmeter = None

    temp_rec = None

    temp_rec_list, Temp_rec = create_model("Temp_rec", {"prop_nr":int, "prop_nm":str, "rec_date":date, "rec_time":int, "rec_by":str, "rec_hour":int, "rec_meter":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_propmeter


        nonlocal temp_rec
        nonlocal temp_rec_list
        return {}

    if blframe == 0:

        for eg_propmeter in db_session.query(Eg_propmeter).filter(
                (Eg_propmeter.rec_date >= frd) &  (Eg_propmeter.rec_date <= tod) &  (Eg_propmeter.propertynr == intres)).all():
            db_session.delete(eg_propmeter)

        for temp_rec in query(temp_rec_list):
            eg_propmeter = Eg_propmeter()
            db_session.add(eg_propmeter)

            eg_propmeter.propertynr = temp_rec.prop_nr
            eg_propmeter.rec_date = temp_rec.rec_date
            eg_propmeter.rec_by = user_init
            eg_propmeter.val_meter = temp_rec.rec_meter
            eg_propmeter.val_hour = temp_rec.rec_hour
            eg_propmeter.create_date = get_current_date()
            eg_propmeter.create_time = get_current_time_in_seconds()


    else:

        for eg_propmeter in db_session.query(Eg_propmeter).filter(
                (Eg_propmeter.rec_date >= frd) &  (Eg_propmeter.rec_date <= tod) &  (Eg_propmeter.propertynr == intres)).all():
            db_session.delete(eg_propmeter)

        for temp_rec in query(temp_rec_list):
            eg_propmeter = Eg_propmeter()
            db_session.add(eg_propmeter)

            eg_propmeter.propertynr = temp_rec.prop_nr
            eg_propmeter.rec_date = temp_rec.rec_date
            eg_propmeter.rec_by = user_init
            eg_propmeter.val_meter = temp_rec.rec_meter
            eg_propmeter.val_hour = temp_rec.rec_hour
            eg_propmeter.create_date = get_current_date()
            eg_propmeter.create_time = get_current_time_in_seconds()

    return generate_output()