#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_mdetail, Eg_maintain, Counters, Eg_property

property_data, Property = create_model("Property", {"prop_nr":int, "prop_nm":string, "prop_loc":int, "prop_loc_nm":string, "prop_zinr":string, "prop_selected":bool, "str":string})

def sel_copymaintenance_btn_okbl(property_data:[Property], maintain_nr:int, all_main:bool, all_only:bool, fdate:date, tdate:date, stnumber:int, lsnumber:int, user_init:string, blcpy:int, lsno:int, stno:int):

    prepare_cache ([Eg_mdetail, Eg_maintain, Counters, Eg_property])

    blcopy:string = ""
    year:int = 0
    month:int = 0
    week:int = 0
    maintask:int = 0
    type:int = 0
    propertynr:int = 0
    workdate:date = None
    comments:string = ""
    created_by:string = ""
    created_date:date = None
    estworkdate:date = None
    typework:int = 0
    nr:int = 0
    stlocation:int = 0
    stzinr:string = ""
    a:date = None
    b:date = None
    eg_mdetail = eg_maintain = counters = eg_property = None

    property = qbuff = None

    Qbuff = create_buffer("Qbuff",Eg_mdetail)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal blcopy, year, month, week, maintask, type, propertynr, workdate, comments, created_by, created_date, estworkdate, typework, nr, stlocation, stzinr, a, b, eg_mdetail, eg_maintain, counters, eg_property
        nonlocal maintain_nr, all_main, all_only, fdate, tdate, stnumber, lsnumber, user_init, blcpy, lsno, stno
        nonlocal qbuff


        nonlocal property, qbuff

        return {"blcpy": blcpy, "lsno": lsno, "stno": stno}

    eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, maintain_nr)]})

    if eg_maintain:
        blcopy = "1"
        type = eg_maintain.type
        propertynr = eg_maintain.propertynr
        comments = eg_maintain.comments
        created_by = eg_maintain.created_by
        created_date = get_current_date()
        estworkdate = eg_maintain.estworkdate
        typework = eg_maintain.typework


    else:
        blcopy = "0"

    if all_main:

        for property in query(property_data):
            property.prop_selected = True

    if blcopy.lower()  == ("1").lower() :
        a = fdate

        if all_only:
            while a <= tdate:

                eg_maintain = get_cache (Eg_maintain, {"propertynr": [(eq, propertynr)],"estworkdate": [(eq, a)]})

                if eg_maintain:
                    pass
                else:

                    # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
                    # counters = get_cache (Counters, {"counter_no": [(eq, 38)]})
                    counters = db_session.query(Counters).with_for_update().filter(
                             (Counters.counter_no == 38)).first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 38
                        counters.counter_bez = "Counter for maintenance in engineering"
                        counters.counter = 0


                    counters.counter = counters.counter + 1
                    pass
                    nr = counters.counter

                    if stnumber == 0:
                        stnumber = nr

                    if lsnumber == 0:
                        lsnumber = nr
                    else:

                        if lsnumber < nr:
                            lsnumber = nr

                    eg_property = get_cache (Eg_property, {"nr": [(eq, propertynr)]})

                    if eg_property:
                        stlocation = eg_property.location
                        stzinr = eg_property.zinr
                    else:
                        stlocation = 0
                        stzinr = ""
                    eg_maintain = Eg_maintain()
                    db_session.add(eg_maintain)

                    eg_maintain.maintainnr = nr
                    eg_maintain.type = 1
                    eg_maintain.propertynr = propertynr
                    eg_maintain.location = stlocation
                    eg_maintain.zinr = stzinr
                    eg_maintain.comments = comments
                    eg_maintain.created_by = user_init
                    eg_maintain.created_date = get_current_date()
                    eg_maintain.estworkdate = a
                    eg_maintain.typework = typework

                    eg_mdetail = get_cache (Eg_mdetail, {"maintainnr": [(eq, maintain_nr)]})

                    if eg_mdetail:

                        for qbuff in db_session.query(Qbuff).filter(
                                 (Qbuff.maintainnr == maintain_nr)).order_by(Qbuff._recid).all():
                            eg_mdetail = Eg_mdetail()
                            db_session.add(eg_mdetail)

                            eg_mdetail.key = qbuff.key
                            eg_mdetail.maintainnr = nr
                            eg_mdetail.nr = qbuff.nr
                            eg_mdetail.bezeich = qbuff.bezeich
                            eg_mdetail.type = qbuff.type
                            eg_mdetail.create_date = get_current_date()
                            eg_mdetail.create_time = get_current_time_in_seconds()
                            eg_mdetail.create_by = user_init

                if typework == 1:
                    a = a + timedelta(days=1)

                elif typework == 2:
                    a = a + timedelta(days=7)

                elif typework == 3:
                    a = a + timedelta(days=30)

                elif typework == 4:
                    a = a + timedelta(days=90)

                elif typework == 5:
                    a = a + timedelta(days=180)

                elif typework == 6:
                    a = a + timedelta(days=365)
            a = fdate


        while a <= tdate :

            for property in query(property_data, filters=(lambda property: property.prop_selected)):

                eg_maintain = get_cache (Eg_maintain, {"propertynr": [(eq, property.prop_nr)],"estworkdate": [(eq, a)]})

                if eg_maintain:
                    pass
                else:

                    # counters = get_cache (Counters, {"counter_no": [(eq, 38)]})
                    # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
                    counters = db_session.query(Counters).with_for_update().filter(
                             (Counters.counter_no == 38)).first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 38
                        counters.counter_bez = "Counter for maintenance in engineering"
                        counters.counter = 0


                    counters.counter = counters.counter + 1
                    pass
                    nr = counters.counter

                    if stnumber == 0:
                        stnumber = nr

                    if lsnumber == 0:
                        lsnumber = nr
                    else:

                        if lsnumber < nr:
                            lsnumber = nr
                    eg_maintain = Eg_maintain()
                    db_session.add(eg_maintain)


                    eg_property = get_cache (Eg_property, {"nr": [(eq, property.prop_nr)]})

                    if eg_property:
                        stlocation = eg_property.location
                        stzinr = eg_property.zinr
                    else:
                        stlocation = 0
                        stzinr = ""
                    eg_maintain.maintainnr = nr
                    eg_maintain.type = 1
                    eg_maintain.propertynr = property.prop_nr
                    eg_maintain.location = stlocation
                    eg_maintain.zinr = stzinr
                    eg_maintain.comments = comments
                    eg_maintain.created_by = user_init
                    eg_maintain.created_date = get_current_date()
                    eg_maintain.estworkdate = a
                    eg_maintain.typework = typework

                    eg_mdetail = get_cache (Eg_mdetail, {"maintainnr": [(eq, maintain_nr)]})

                    if eg_mdetail:

                        for qbuff in db_session.query(Qbuff).filter(
                                 (Qbuff.maintainnr == maintain_nr)).order_by(Qbuff._recid).all():
                            eg_mdetail = Eg_mdetail()
                            db_session.add(eg_mdetail)

                            eg_mdetail.key = qbuff.key
                            eg_mdetail.maintainnr = nr
                            eg_mdetail.nr = qbuff.nr
                            eg_mdetail.bezeich = qbuff.bezeich
                            eg_mdetail.type = qbuff.type
                            eg_mdetail.create_date = get_current_date()
                            eg_mdetail.create_time = get_current_time_in_seconds()
                            eg_mdetail.create_by = user_init

            if typework == 1:
                a = a + timedelta(days=1)

            elif typework == 2:
                a = a + timedelta(days=7)

            elif typework == 3:
                a = a + timedelta(days=30)

            elif typework == 4:
                a = a + timedelta(days=90)

            elif typework == 5:
                a = a + timedelta(days=180)

            elif typework == 6:
                a = a + timedelta(days=365)

    if lsnumber == 0 and stnumber == 0:
        blcpy = 0
        lsno = lsnumber
        stno = stnumber


    else:
        blcpy = 1
        lsno = lsnumber
        stno = stnumber

    return generate_output()