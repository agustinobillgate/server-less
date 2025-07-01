#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_propmeter

def eg_propertymeter_btn_createbl(blframe:int, intres:int, frd:date, tod:date, strname:string):

    prepare_cache ([Eg_propmeter])

    temp_rec_list = []
    sday:date = None
    eday:date = None
    eg_propmeter = None

    temp_rec = None

    temp_rec_list, Temp_rec = create_model("Temp_rec", {"prop_nr":int, "prop_nm":string, "rec_date":date, "rec_time":int, "rec_by":string, "rec_hour":int, "rec_meter":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_rec_list, sday, eday, eg_propmeter
        nonlocal blframe, intres, frd, tod, strname


        nonlocal temp_rec
        nonlocal temp_rec_list

        return {"temp-rec": temp_rec_list}


    temp_rec_list.clear()

    if blframe == 0:
        sday = frd
        eday = tod
        while sday <= eday :

            eg_propmeter = get_cache (Eg_propmeter, {"rec_date": [(eq, sday)],"propertynr": [(eq, intres)]})

            if eg_propmeter:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = eg_propmeter.rec_date
                temp_rec.rec_hour = eg_propmeter.val_hour
                temp_rec.rec_meter = eg_propmeter.val_meter


            else:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = sday
                temp_rec.rec_hour = 0
                temp_rec.rec_meter = 0


            sday = sday + timedelta(days=1)
    else:
        sday = frd
        eday = tod
        while sday <= eday :

            eg_propmeter = get_cache (Eg_propmeter, {"rec_date": [(eq, sday)],"propertynr": [(eq, intres)]})

            if eg_propmeter:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = eg_propmeter.rec_date
                temp_rec.rec_hour = eg_propmeter.val_hour
                temp_rec.rec_meter = eg_propmeter.val_meter


            else:
                temp_rec = Temp_rec()
                temp_rec_list.append(temp_rec)

                temp_rec.prop_nr = intres
                temp_rec.prop_nm = strname
                temp_rec.rec_date = sday
                temp_rec.rec_hour = 0
                temp_rec.rec_meter = 0


            sday = sday + timedelta(days=1)

    return generate_output()