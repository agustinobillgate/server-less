DEFINE TEMP-TABLE payload-list
    FIELD user-init AS CHARACTER
    FIELD reason    AS CHARACTER
    FIELD lscheinnr AS CHARACTER
.

DEFINE TEMP-TABLE response-list
    FIELD success-status AS LOGICAL
    FIELD msg-str        AS CHARACTER
.

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR response-list.

DEFINE VARIABLE user-init      AS CHARACTER.
DEFINE VARIABLE reason         AS CHARACTER.
DEFINE VARIABLE lscheinnr      AS CHARACTER.
DEFINE VARIABLE success-status AS LOGICAL INITIAL YES.
DEFINE VARIABLE msg-str        AS CHARACTER.
DEFINE VARIABLE log-msg        AS CHARACTER.

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        user-init = payload-list.user-init
        reason    = payload-list.reason
        lscheinnr = payload-list.lscheinnr
    .

    RUN unapprove-sr.

    CREATE response-list.
    ASSIGN
        response-list.success-status = success-status
        response-list.msg-str        = msg-str
    .
END.

PROCEDURE unapprove-sr:
    DEFINE VARIABLE close-date  AS DATE.
    DEFINE VARIABLE close-date2 AS DATE.

    DEFINE BUFFER b-l-op FOR l-op.

    FIND FIRST htparam WHERE paramnr = 224 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN close-date = htparam.fdate.          

    FIND FIRST htparam WHERE paramnr = 221 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN close-date2 = htparam.fdate.

    IF close-date LT close-date2 THEN close-date = close-date2.

    close-date = DATE(MONTH(close-date), 1, YEAR(close-date)) - 1.

    FIND FIRST l-op WHERE l-op.lscheinnr EQ lscheinnr 
        AND l-op.op-art GE 13 AND l-op.op-art LE 14 NO-LOCK NO-ERROR.
    IF AVAILABLE l-op THEN
    DO:
        FIND FIRST b-l-op WHERE b-l-op.lscheinnr EQ lscheinnr 
            AND b-l-op.op-art GE 3 AND b-l-op.op-art LE 4 
            AND b-l-op.herkunftflag LE 2 NO-LOCK NO-ERROR.

        IF l-op.datum LE close-date THEN
        DO:
            success-status = NO.
            msg-str = "Failed to unapprove SR because SR created before close inventory date. Last close inventory: " 
                    + STRING(close-date).
        END.
        ELSE IF l-op.loeschflag EQ 2 THEN
        DO:
            success-status = NO.
            msg-str = "Failed to unapprove SR because SR was deleted".
        END.
        ELSE IF AVAILABLE b-l-op OR l-op.herkunftflag EQ 2 THEN
        DO:
            success-status = NO.
            msg-str = "Failed to unapprove SR because SR already marked as outgoing".
        END.
        ELSE
        DO:
            FIND FIRST l-ophdr WHERE l-ophdr.op-typ EQ "REQ"
                AND l-ophdr.lscheinnr EQ l-op.lscheinnr
                AND l-ophdr.docu-nr EQ l-op.lscheinnr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE l-ophdr THEN
            DO:
                l-ophdr.betriebsnr = 0.
                FIND CURRENT l-ophdr NO-LOCK.
                RELEASE l-ophdr.
            END.

            log-msg = "SR with Request Code: " + STRING(lscheinnr) + " is unapproved. Reason: " + reason.

            FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
            IF AVAILABLE bediener THEN
            DO:
                CREATE res-history. 
                ASSIGN 
                    res-history.nr        = bediener.nr 
                    res-history.datum     = TODAY 
                    res-history.zeit      = TIME 
                    res-history.action    = "Unapprove SR"
                    res-history.aenderung = log-msg
                . 
            END.
        END.
    END.
END.
