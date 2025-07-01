#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Htparam

def prepare_gl_batchjoubl(sorttype:int, from_refno:string, depttype:int):

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    b1_list_list = []
    gl_jouhdr = htparam = None

    b1_list = None

    b1_list_list, B1_list = create_model_like(Gl_jouhdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, b1_list_list, gl_jouhdr, htparam
        nonlocal sorttype, from_refno, depttype


        nonlocal b1_list
        nonlocal b1_list_list

        return {"from_date": from_date, "to_date": to_date, "b1-list": b1_list_list}

    def get_bemerk(bemerk:string):

        nonlocal from_date, to_date, b1_list_list, gl_jouhdr, htparam
        nonlocal sorttype, from_refno, depttype


        nonlocal b1_list
        nonlocal b1_list_list

        n:int = 0
        s1:string = ""
        n = get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk


    def display_it():

        nonlocal from_date, to_date, b1_list_list, gl_jouhdr, htparam
        nonlocal sorttype, from_refno, depttype


        nonlocal b1_list
        nonlocal b1_list_list

        b_flag:bool = False

        if sorttype == 0:
            b_flag = True

        if from_refno == "":

            if depttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.jtype > 0) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.batch == b_flag)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_b1()

            else:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.jtype == depttype) & (Gl_jouhdr.batch == b_flag)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_b1()


            if gl_jouhdr:
                pass
        else:

            if depttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.jtype > 0) & (Gl_jouhdr.refno == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.batch == b_flag)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_b1()

            else:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.batch == b_flag) & (Gl_jouhdr.refno == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.jtype == depttype) & (Gl_jouhdr.batch == b_flag)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_b1()


            if gl_jouhdr:
                pass


    def assign_b1():

        nonlocal from_date, to_date, b1_list_list, gl_jouhdr, htparam
        nonlocal sorttype, from_refno, depttype


        nonlocal b1_list
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        buffer_copy(gl_jouhdr, b1_list)
        b1_list.rec_id = gl_jouhdr._recid


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    from_date = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    to_date = get_current_date()
    display_it()

    return generate_output()