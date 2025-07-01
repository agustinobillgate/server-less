
DEFINE TEMP-TABLE main-task
    FIELD nr        AS INTEGER COLUMN-LABEL "No" FORMAT ">>9"
    FIELD bezeich   AS CHAR    COLUMN-LABEL "Object" FORMAT "x(32)"
    .
DEFINE INPUT  PARAMETER categ-nr AS INTEGER.
DEFINE INPUT  PARAMETER dept-nr AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR main-task.

RUN create-main.


PROCEDURE create-main:
    DEF BUFFER queasy1 FOR queasy.
    DEF BUFFER subtask FOR eg-subtask.

   /* IF dept-nr = 0 THEN
   */
        FOR EACH queasy1 WHERE queasy1.KEY = 133 AND queasy1.number2 = categ-nr NO-LOCK BY queasy1.number1:
            CREATE main-task.
            ASSIGN 
                main-task.nr = queasy1.number1
                main-task.bezeich = queasy1.CHAR1.
        END.
/*
    ELSE
        FOR EACH queasy1 WHERE queasy1.KEY = 133 AND queasy1.number2 = categ-nr NO-LOCK BY queasy1.number1:
            FIND FIRST subtask WHERE subtask.main-nr = queasy1.number1 AND
                subtask.dept-nr = dept-nr /*AND subtask.reserve-int = ""*/ NO-LOCK NO-ERROR.
            IF AVAILABLE subtask THEN
            DO:
                CREATE main-task.
                ASSIGN
                    main-task.nr = queasy1.number1
                    main-task.bezeich = queasy1.char1
                    .
            END.
            /*
            ELSE
            DO:
                    CREATE main-task.
                    ASSIGN 
                        main-task.nr = queasy1.number1
                        main-task.bezeich = queasy1.CHAR1.

            END.
            */
        END.
     */   
END.
