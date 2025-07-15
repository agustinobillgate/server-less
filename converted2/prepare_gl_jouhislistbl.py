#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_main, Htparam

def prepare_gl_jouhislistbl():

    prepare_cache ([Gl_main, Htparam])

    from_date = None
    close_date = None
    close_year = None
    from_main = 0
    main_bez = ""
    chr977 = ""
    gl_main_list_data = []
    gl_depart_list_data = []
    gl_main = htparam = None

    gl_main_list = gl_depart_list = gl_main1 = None

    gl_main_list_data, Gl_main_list = create_model("Gl_main_list", {"code":int, "nr":int, "bezeich":string})
    gl_depart_list_data, Gl_depart_list = create_model("Gl_depart_list", {"nr":int, "bezeich":string})

    Gl_main1 = create_buffer("Gl_main1",Gl_main)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, close_date, close_year, from_main, main_bez, chr977, gl_main_list_data, gl_depart_list_data, gl_main, htparam
        nonlocal gl_main1


        nonlocal gl_main_list, gl_depart_list, gl_main1
        nonlocal gl_main_list_data, gl_depart_list_data

        return {"from_date": from_date, "close_date": close_date, "close_year": close_year, "from_main": from_main, "main_bez": main_bez, "chr977": chr977, "gl-main-list": gl_main_list_data, "gl-depart-list": gl_depart_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    from_date = date_mdy(1, 1, get_year(htparam.fdate) - timedelta(days=3))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    close_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate
    close_year = date_mdy(get_month(close_year) , get_day(close_year) , get_year(close_year) + timedelta(days=1))

    gl_main = db_session.query(Gl_main).first()

    if gl_main:
        from_main = gl_main.code
        main_bez = gl_main.bezeich

    for gl_main in db_session.query(Gl_main).order_by(Gl_main._recid).all():
        gl_main_list = Gl_main_list()
        gl_main_list_data.append(gl_main_list)

        gl_main_list.code = gl_main.code
        gl_main_list.nr = gl_main.nr
        gl_main_list.bezeich = gl_main.bezeich

    for gl_depart_list in query(gl_depart_list_data):
        gl_depart_list = Gl_depart_list()
        gl_depart_list_data.append(gl_depart_list)

        gl_depart_list.nr = gl_depart_list.nr
        gl_depart_list.bezeich = gl_depart_list.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    chr977 = htparam.fchar

    return generate_output()