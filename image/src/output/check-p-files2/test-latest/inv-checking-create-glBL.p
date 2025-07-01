DEF TEMP-TABLE artikel3
    FIELD kum LIKE l-untergrup.zwkum
    FIELD zeich2 LIKE l-untergrup.bezeich FORMAT "x(24)" COLUMN-LABEL "Description"
    FIELD numb LIKE queasy.number1 FORMAT ">>9" COLUMN-LABEL "Main"
    FIELD fibu LIKE gl-acct.fibukonto
    FIELD zeich3 LIKE gl-acct.bezeich FORMAT "x(32)".

DEF OUTPUT PARAMETER TABLE FOR artikel3.

RUN create-gl.

PROCEDURE create-gl:
    FOR EACH artikel3:
        DELETE artikel3.
    END.
  
    FOR EACH l-untergrup NO-LOCK:
        FIND FIRST queasy WHERE KEY = 29 AND queasy.number2 = l-untergrup.zwkum
            NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto NO-LOCK.
            CREATE artikel3.
            ASSIGN
                    artikel3.kum = l-untergrup.zwkum
                    artikel3.zeich2 = l-untergrup.bezeich
                    artikel3.numb = queasy.number1
                    artikel3.fibu = gl-acct.fibukonto
                    artikel3.zeich3 = gl-acct.bezeich.
        END.
    END.
END.


