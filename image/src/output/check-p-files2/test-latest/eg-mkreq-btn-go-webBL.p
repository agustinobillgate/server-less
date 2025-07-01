DEFINE TEMP-TABLE request1 LIKE eg-request.

DEF INPUT-OUTPUT PARAMETER TABLE FOR request1.
DEF INPUT PARAMETER sguestflag AS LOGICAL.
DEF INPUT PARAMETER sub-str AS CHAR.
DEF INPUT PARAMETER main-str AS CHAR.
DEF INPUT PARAMETER prop-bezeich AS CHAR.

DEFINE VARIABLE ci-date AS DATE.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.

FIND FIRST request1.
RUN create-request.
RUN create-history.

PROCEDURE create-request:
    DEF VAR strMemo AS CHAR.
    DEF VAR nr AS INTEGER INITIAL 0.
    DEF VAR prop-nr AS INTEGER.
    DEF BUFFER buff FOR eg-queasy.
    DEF BUFFER usr FOR bediener.
    DEF BUFFER buff-property FOR eg-property.

    DO TRANSACTION:
        
        FIND FIRST counters WHERE counters.counter-no = 34 NO-LOCK NO-ERROR.
        IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN 
                counters.counter-no  = 34
                counters.counter-bez = "Counter for Engineering RequestNo"
                counters.counter     = 1.
            FIND CURRENT counters NO-LOCK.
        END.
        ELSE
        DO:
            FIND CURRENT counters EXCLUSIVE-LOCK.
            ASSIGN counters.counter = counters.counter + 1.
            FIND CURRENT counters NO-LOCK.
        END.
    
        ASSIGN request1.reqnr = counters.counter.
        
        request1.opened-time = TIME.
        
        IF request1.propertynr = 0 THEN /*Create Artikel*/
        DO:
            /*
            FIND LAST buff-property NO-LOCK NO-ERROR.
            IF AVAILABLE buff-property THEN prop-nr = buff-property.nr + 1.
            */
            FOR EACH buff-property NO-LOCK BY buff-property.nr DESC:
                prop-nr = buff-property.nr.
                LEAVE.
            END.
            prop-nr = prop-nr + 1.
            
            CREATE eg-property.
            ASSIGN
                eg-property.nr          = prop-nr
                eg-property.bezeich     = prop-bezeich
                eg-property.maintask    = request1.maintask                    
                eg-property.zinr        = request1.zinr   
                eg-property.datum       = TODAY
            .
            IF sguestflag EQ YES THEN
            DO:
                FIND FIRST eg-location WHERE eg-location.guestflag = YES NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN eg-property.location = eg-location.nr. 
            END.                                  
            ELSE eg-property.location = request1.reserve-int.   
            FIND FIRST queasy WHERE queasy.KEY = 133 AND queasy.number1 = request1.maintask NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN MESSAGE "ada queasy" queasy.char1 VIEW-AS ALERT-BOX.
            IF NOT AVAILABLE queasy THEN MESSAGE "ga ada queasy" VIEW-AS ALERT-BOX.
            request1.propertynr = prop-nr.
        END.
        
        IF sguestflag = YES THEN
        DO:
            FIND FIRST eg-location WHERE eg-location.guestflag = YES NO-LOCK NO-ERROR.
            IF AVAILABLE eg-location THEN
            DO:
                ASSIGN request1.reserve-int = eg-location.nr.
            END.

            IF request1.zinr NE "" OR request1.zinr NE ? THEN RUN get-guestname.
        END.                               

        ASSIGN request1.subtask-bezeich = sub-str.

        CREATE eg-request.
        BUFFER-COPY request1 TO eg-request.
        FIND CURRENT eg-request NO-LOCK.                

        FOR EACH buff WHERE buff.KEY = 3 AND buff.reqnr = request1.reqnr NO-LOCK:
            IF buff.hist-nr GT nr THEN nr = buff.hist-nr.
        END.
        
        CREATE eg-queasy.
        ASSIGN
            eg-queasy.KEY       = 3 
            eg-queasy.reqnr     = request1.reqnr
            eg-queasy.hist-nr   = nr + 1
            eg-queasy.hist-time  = TIME
            eg-queasy.hist-fdate = TODAY.

        IF request1.assign-to NE 0 THEN
        DO:
            eg-queasy.usr-nr = request1.assign-to.
            FIND CURRENT eg-queasy NO-LOCK.
        END.
    END.
END.

PROCEDURE create-history:
    DEF BUFFER resline1 FOR res-line.

    FIND FIRST resline1 WHERE resline1.resnr = request1.resnr AND 
        resline1.reslinnr = request1.reslinnr NO-LOCK NO-ERROR.
    CREATE history.
    ASSIGN
        history.gastnr      = request1.gastnr
        history.resnr       = request1.resnr
        history.reslinnr    = request1.reslinnr
        history.zi-wechsel  = YES
        history.bemerk      = main-str + ", " + sub-str + ", " + request1.task-def.
    IF AVAILABLE resline1 THEN
        ASSIGN
            history.ankunft = resline1.ankunft
            history.abreise = resline1.abreise
            history.zinr    = resline1.zinr
        .
    FIND CURRENT history NO-LOCK.
END.

PROCEDURE get-guestname:
    DEF BUFFER resline1 FOR res-line.              
    DEF BUFFER guest1 FOR guest.              

    FIND FIRST resline1 WHERE resline1.active-flag = 1 AND resline1.zinr = 
        request1.zinr AND resline1.resstatus NE 12 AND resline1.ankunft LE ci-date
        AND resline1.abreise GE ci-date NO-LOCK NO-ERROR.
    IF AVAILABLE resline1 THEN
    DO:
        FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
            request1.gastnr = resline1.gastnrmember.            
            request1.resnr = resline1.resnr.
            request1.reslinnr = resline1.reslinnr.
        END.
    END.
END.
