
DEFINE TEMP-TABLE ubuff
    /*FIELD nr        AS INTEGER
    FIELD usercode  AS CHARACTER*/
    FIELD userinit  AS CHARACTER
    FIELD username  AS CHARACTER.

DEFINE TEMP-TABLE t-bediener
    /*FIELD nr        AS INTEGER
    FIELD usercode  AS CHARACTER*/
    FIELD userinit  AS CHARACTER
    FIELD username  AS CHARACTER.

DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR ubuff.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.
DEF INPUT-OUTPUT PARAMETER reshist-action AS CHAR NO-UNDO.


FOR EACH bediener WHERE bediener.nr NE 0 NO-LOCK:
    CREATE ubuff.
    /*BUFFER-COPY bediener TO ubuff.*/
    ASSIGN
        /*ubuff.nr        = bediener.nr      
        ubuff.usercode  = bediener.usercode*/
        ubuff.userinit  = bediener.userinit
        ubuff.username  = bediener.username.
END.

RUN check-reshistory.
RUN fill-users.
RUN fill-key.
RUN htpdate.p(87, OUTPUT from-date).

PROCEDURE check-reshistory:
DEF BUFFER rbuff FOR res-history.
    FIND FIRST res-history WHERE res-history.nr = 0 
        AND res-history.betriebsnr NE 0 USE-INDEX bediener-time-date_ix
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE res-history THEN RETURN.
    
    DO WHILE AVAILABLE res-history:
        DO TRANSACTION:
            FIND FIRST rbuff WHERE RECID(rbuff) = RECID(res-history)
                EXCLUSIVE-LOCK.
            ASSIGN rbuff.nr = rbuff.betriebsnr.
            FIND CURRENT rbuff NO-LOCK.
            RELEASE rbuff.
        END.
        FIND NEXT res-history WHERE res-history.nr = 0 
            AND res-history.betriebsnr NE 0 USE-INDEX bediener-time-date_ix
            NO-LOCK NO-ERROR.
    END.
END.

PROCEDURE fill-users:
    FOR EACH bediener WHERE bediener.flag = 0 NO-LOCK BY bediener.username:
        CREATE t-bediener.
        ASSIGN
            /*t-bediener.nr        = bediener.nr      
            t-bediener.usercode  = bediener.usercode*/
            t-bediener.userinit  = bediener.userinit
            t-bediener.username  = bediener.username.
    END.
END.


PROCEDURE fill-key:
    DEFINE VARIABLE curr-action AS CHAR NO-UNDO INITIAL " ".
    DEFINE VARIABLE loopi       AS INTEGER.

    IF reshist-action = ""  THEN DO:
        FIND FIRST res-history USE-INDEX action_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE res-history :
            IF res-history.action NE curr-action THEN DO:
                ASSIGN reshist-action = res-history.action + ";" + reshist-action.
            END.
            
            ASSIGN curr-action = res-history.action.
            FIND NEXT res-history USE-INDEX action_ix NO-LOCK NO-ERROR.
        END.
    END.
    ELSE RETURN.

    
END.
