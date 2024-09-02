from functions.additional_functions import *
import decimal
from models import Queasy, Eg_subtask

def prepare_sel_egmainall_webbl(dept_nr:int):
    main_task_list = []
    queasy = eg_subtask = None

    main_task = queasy1 = subtask = None

    main_task_list, Main_task = create_model("Main_task", {"nr":int, "bezeich":str, "categ_nr":int, "categ_nm":str})

    Queasy1 = Queasy
    Subtask = Eg_subtask

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_task_list, queasy, eg_subtask
        nonlocal queasy1, subtask


        nonlocal main_task, queasy1, subtask
        nonlocal main_task_list
        return {"main-task": main_task_list}

    def create_main():

        nonlocal main_task_list, queasy, eg_subtask
        nonlocal queasy1, subtask


        nonlocal main_task, queasy1, subtask
        nonlocal main_task_list


        Queasy1 = Queasy
        Subtask = Eg_subtask

        if dept_nr == 0:

            for queasy1 in db_session.query(Queasy1).filter(
                    (Queasy1.key == 133)).all():
                main_task = Main_task()
                main_task_list.append(main_task)

                main_task.nr = queasy1.number1
                main_task.bezeich = queasy1.CHAR1

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 132) &  (Queasy.number1 == queasy1.number2)).first()

                if queasy:
                    main_task.categ_nr = queasy.number1
                    main_task.categ_nm = queasy.char1

        else:

            for queasy1 in db_session.query(Queasy1).filter(
                    (Queasy1.key == 133)).all():

                subtask = db_session.query(Subtask).filter(
                        (Subtask.main_nr == queasy1.number1) &  (Subtask.dept_nr == dept_nr)).first()

                if subtask:
                    main_task = Main_task()
                    main_task_list.append(main_task)

                    main_task.nr = queasy1.number1
                    main_task.bezeich = queasy1.char1

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 132) &  (Queasy.number1 == queasy1.number2)).first()

                    if queasy:
                        main_task.categ_nr = queasy.number1
                        main_task.categ_nm = queasy.char1

    create_main()

    return generate_output()