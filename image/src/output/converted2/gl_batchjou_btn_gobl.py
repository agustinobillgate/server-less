from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr

def gl_batchjou_btn_gobl(sorttype:int, from_refno:str, depttype:int, from_date:date, to_date:date):
    b1_list_list = []
    gl_jouhdr = None

    b1_list = None

    b1_list_list, B1_list = create_model_like(Gl_jouhdr, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, gl_jouhdr
        nonlocal sorttype, from_refno, depttype, from_date, to_date


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def get_bemerk(bemerk:str):

        nonlocal b1_list_list, gl_jouhdr
        nonlocal sorttype, from_refno, depttype, from_date, to_date


        nonlocal b1_list
        nonlocal b1_list_list

        n:int = 0
        s1:str = ""
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk


    def display_it():

        nonlocal b1_list_list, gl_jouhdr
        nonlocal sorttype, from_refno, depttype, from_date, to_date


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
                         (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.jtype > 0) & (func.lower(Gl_jouhdr.refno) == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.batch == b_flag)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_b1()

            else:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.batch == b_flag) & (func.lower(Gl_jouhdr.refno) == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_jouhdr.jtype == depttype) & (Gl_jouhdr.batch == b_flag)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_b1()


            if gl_jouhdr:
                pass


    def assign_b1():

        nonlocal b1_list_list, gl_jouhdr
        nonlocal sorttype, from_refno, depttype, from_date, to_date


        nonlocal b1_list
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        buffer_copy(gl_jouhdr, b1_list)
        b1_list.rec_id = gl_jouhdr._recid

    display_it()

    return generate_output()