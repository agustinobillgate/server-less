
DEF TEMP-TABLE t-mapping-nation
    FIELD nationVHP AS CHAR
    FIELD nationBE  AS CHAR
    FIELD descr     AS CHAR
    FIELD nr        AS INT
    .

DEF OUTPUT PARAMETER TABLE FOR t-mapping-nation.
DEF INPUT  PARAMETER bookengID AS INT.

FOR EACH nation WHERE nation.natcode = 0 NO-LOCK BY nation.kurzbez:
    CREATE t-mapping-nation.
    ASSIGN
        t-mapping-nation.nationVHP  = nation.kurzbez
        t-mapping-nation.descr      = ENTRY(1, nation.bezeich, ";")
        t-mapping-nation.nr         = nation.nationnr.

    FIND FIRST queasy WHERE queasy.KEY = 165
        AND queasy.number1 = bookengID
        AND queasy.number2 = nation.nationnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN t-mapping-nation.nationBE = queasy.char2.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 165
            queasy.number1 = bookengID
            queasy.number2 = nation.nationnr
            queasy.char1   = nation.kurzbez.
    END.

END.
