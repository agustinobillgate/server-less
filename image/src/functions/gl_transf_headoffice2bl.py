from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_jouhdr, Gl_journal, Gl_htljournal, Counters

def gl_transf_headoffice2bl(lic_nr:str, t_gl_jouhdr:[T_gl_jouhdr], t_gl_journal:[T_gl_journal]):
    gl_jouhdr = gl_journal = gl_htljournal = counters = None

    t_gl_jouhdr = t_gl_journal = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)
    t_gl_journal_list, T_gl_journal = create_model_like(Gl_journal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr, gl_journal, gl_htljournal, counters


        nonlocal t_gl_jouhdr, t_gl_journal
        nonlocal t_gl_jouhdr_list, t_gl_journal_list
        return {}


    for t_gl_jouhdr in query(t_gl_jouhdr_list):

        gl_htljournal = db_session.query(Gl_htljournal).filter(
                    (Gl_htljournal.htl_jnr == t_gl_jouhdr.jnr) &  (func.lower(Gl_htljournal.htl_license) == (lic_nr).lower())).first()

        if gl_htljournal:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.jnr == gl_htljournal.jnr)).all():
                db_session.delete(gl_jouhdr)

            for gl_journal in db_session.query(Gl_journal).filter(
                        (Gl_journal.jnr == gl_htljournal.jnr)).all():
                db_session.delete(gl_journal)
        else:

            counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 25)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 25
                counters.counter_bez = "G/L Transaction Journal"


            counters = counters + 1

            counters = db_session.query(Counters).first()
            gl_htljournal = Gl_htljournal()
            db_session.add(gl_htljournal)

            gl_htljournal.htl_jnr = t_gl_jouhdr.jnr
            gl_htljournal.jnr = counters
            gl_htljournal.htl_license = lic_nr
            gl_htljournal.datum = t_gl_jouhdr.datum


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        buffer_copy(t_gl_jouhdr, gl_jouhdr,except_fields=["t_gl_jouhdr.jnr"])
        gl_jouhdr.jnr = gl_htljournal.jnr
        gl_jouhdr.jtype = gl_jouhdr.jtype + 10
        gl_jouhdr.activeflag = 0

        for t_gl_journal in query(t_gl_journal_list, filters=(lambda t_gl_journal :t_gl_journal.jnr == t_gl_jouhdr.jnr)):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            buffer_copy(t_gl_journal, gl_journal,except_fields=["t_gl_journal.jnr"])
            gl_journal.jnr = gl_htljournal.jnr
            gl_journal.activeflag = 0


            t_gl_journal_list.remove(t_gl_journal)

            gl_journal = db_session.query(Gl_journal).first()


        gl_htljournal = db_session.query(Gl_htljournal).first()


        gl_jouhdr = db_session.query(Gl_jouhdr).first()

    return generate_output()