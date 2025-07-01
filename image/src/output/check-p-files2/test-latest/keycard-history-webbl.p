
DEFINE BUFFER ubuff FOR bediener.

DEFINE TEMP-TABLE input-list
    FIELD from-date     AS DATE
    FIELD to-date       AS DATE
    FIELD usrID         AS CHARACTER
.

DEFINE TEMP-TABLE output-list
    FIELD datum     LIKE res-history.datum
    /* FIELD action    LIKE res-history.action */
    FIELD aenderung LIKE res-history.aenderung
    FIELD username  LIKE ubuff.username
    FIELD zeit      AS CHARACTER
.

/* */
DEF INPUT PARAMETER TABLE FOR input-list.
DEF OUTPUT PARAMETER TABLE FOR output-list.
DEF OUTPUT PARAMETER err-msg AS CHARACTER INITIAL "".

FIND FIRST input-list WHERE input-list.from-date NE ? AND input-list.to-date NE ? NO-LOCK NO-ERROR.
IF NOT AVAILABLE input-list THEN 
DO:
    err-msg = "ERROR : Date input can't be null".
    RETURN.
END.

RUN create-list.

PROCEDURE create-list:
    IF input-list.usrID NE "" AND input-list.usrID NE ? THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = TRIM(ENTRY(1, input-list.usrID, "-"))
            NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN
        DO:
            FOR EACH res-history WHERE res-history.datum GE input-list.from-date
                AND res-history.datum LE input-list.to-date 
                AND res-history.action EQ "Keycard"
                AND res-history.nr EQ bediener.nr NO-LOCK 
                BY res-history.datum BY res-history.zeit:
                    CREATE output-list.
                    ASSIGN
                        output-list.datum     = res-history.datum
                        /* output-list.action    = res-history.action */
                        output-list.aenderung = res-history.aenderung
                        output-list.zeit      = STRING(res-history.zeit,"HH:MM:SS")
                    .
                    FIND FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK NO-ERROR.
                    IF AVAILABLE ubuff THEN output-list.username  = ubuff.username.
            END.
        END.
        ELSE 
        DO:
            err-msg = "ERROR : User not found".
            RETURN.
        END.
    END.
    ELSE
    DO:
        FOR EACH res-history WHERE res-history.datum GE from-date
            AND res-history.datum LE to-date 
            AND res-history.action EQ "Keycard" NO-LOCK
            BY res-history.datum BY res-history.zeit:
                CREATE output-list.
                ASSIGN
                    output-list.datum     = res-history.datum
                    /* output-list.action    = res-history.action */
                    output-list.aenderung = res-history.aenderung
                    output-list.zeit      = STRING(res-history.zeit,"HH:MM:SS")
                .
                FIND FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK NO-ERROR.
                IF AVAILABLE ubuff THEN output-list.username  = ubuff.username.
        END.
    END.
END.

