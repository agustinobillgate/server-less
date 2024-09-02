from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_propmeter

def eg_propertymeter_btn_createbl(blframe:int, intres:int, frd:date, tod:date, strname:str):
    temp_rec_list = []
    sday:date = None
    eday:date = None
    eg_propmeter = None

    temp_rec = None

    temp_rec_list, Temp_rec = create_model("Temp_rec", {"prop_nr":int, "prop_nm":str, "rec_date":date, "rec_time":int, "rec_by":str, "rec_hour":int, "rec_meter":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_rec_list, sday, eday, eg_propmeter


        nonlocal temp_rec
        nonlocal temp_rec_list
        return {"temp-rec": temp_rec_list}


    temp_rec_list.clear()

    if blframe == 0:
        sday = frd
        eday = tod
        while sday <= eday :

            eg_propmeter = db_session.query(Eg_propmeter).filter(
                    (Eg_propmeter.rec_date == sday) &  (Eg_propmeter.propertynr == intres)).first()

            if eg_propmeter:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = eg_propmeter.rec_date
                temp_rec.rec_hour = eg_propMeter.val_hour
                temp_rec.rec_meter = eg_propmeter.val_meter


            else:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = sday
                temp_rec.rec_hour = 0
                temp_rec.rec_meter = 0


            sday = sday + 1
    else:
        sday = frd
        eday = tod
        while sday <= eday :

            eg_propmeter = db_session.query(Eg_propmeter).filter(
                    (Eg_propmeter.rec_date == sday) &  (Eg_propmeter.propertynr == intres)).first()

            if eg_propmeter:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = eg_propmeter.rec_date
                temp_rec.rec_hour = eg_propMeter.val_hour
                temp_rec.rec_meter = eg_propmeter.val_meter


            else:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = sday
                temp_rec.rec_hour = 0
                temp_rec.rec_meter = 0


            sday = sday + 1

    return generate_output()