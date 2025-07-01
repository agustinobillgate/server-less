DEFINE TEMP-TABLE request1 LIKE eg-request.
DEFINE TEMP-TABLE t-eg-location LIKE eg-location.
DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEFINE TEMP-TABLE t-zimmer LIKE zimmer
    FIELD gname-str AS CHAR  FORMAT "x(60)". /*For web*/.
DEFINE BUFFER resline1 FOR res-line.              
DEFINE BUFFER guest1 FOR guest.
DEF INPUT PARAMETER pvILanguage AS INTEGER          NO-UNDO.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER status-str AS CHAR.
DEF OUTPUT PARAMETER open-str AS CHAR.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER dept-str AS CHAR.
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR request1.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.
{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "eg-mkreq". 
DEFINE VARIABLE guestname AS CHAR.
CREATE request1.
RUN define-group.
RUN define-engineering.
RUN initiate-it.
FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ci-date = htparam.fdate.
/*
FOR EACH eg-location WHERE eg-location.guestflag NO-LOCK:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.
*/
FOR EACH eg-location NO-LOCK:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.
FOR EACH queasy WHERE queasy.KEY = 132 OR queasy.KEY = 133 OR queasy.KEY = 130
    OR queasy.KEY = 19 OR queasy.KEY = 135 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.
FOR EACH zimmer NO-LOCK:
    RUN get-guestname(zimmer.zinr).
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
    ASSIGN t-zimmer.gname-str = guestname.
END.
PROCEDURE Define-engineering:
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION.*/
    END.
END.
PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.
PROCEDURE initiate-it:
    DEF BUFFER queasy1 FOR queasy.
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
            FIND CURRENT counters NO-LOCK.
        END.
    ASSIGN /*request1.reqnr    = counters.counter + 1 */
        request1.reqstatus   = 1
        request1.opened-by      = user-init 
        request1.opened-date    = TODAY
        request1.opened-time    = TIME
        request1.urgency        = 1.
    status-str = translateExtended("New", lvCAREA, "").
    open-str = STRING(request1.opened-time, "HH:MM:SS").
    ASSIGN request1.deptnum = int(EngID).
    
    FIND FIRST queasy1 WHERE queasy1.KEY = 19 AND queasy1.number1 = 
            request1.deptnum NO-LOCK NO-ERROR.
    IF NOT AVAILABLE queasy1 THEN
    DO:
        flag = 1.
        ASSIGN request1.deptnum = 0.
        /*MT
        dept-str = "".
        DISPLAY request1.deptnum dept-str WITH FRAME frame1.
        */
    END.
    ELSE
    DO:
        flag = 2.
        ASSIGN dept-str = queasy1.char3.
        /*MTDISPLAY request1.deptnum dept-str WITH FRAME frame1.*/
    END.
    /*MTAPPLY "entry" TO request1.SOURCE.*/
END.
PROCEDURE get-guestname:
    DEF INPUT PARAM h-zinr AS CHAR.
    FIND FIRST resline1 WHERE resline1.active-flag = 1 AND resline1.zinr = h-zinr /*"415" h-zinr*/ 
        AND resline1.resstatus NE 13 USE-INDEX zinr_index NO-LOCK NO-ERROR.
    IF AVAILABLE resline1 THEN
    DO:
        FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
            guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
                guest1.anrede1 + guest1.anredefirma.
        END.
    END.
    ELSE
    DO:
        FIND FIRST resline1 WHERE resline1.active-flag = 0 AND resline1.zinr = h-zinr /*"415" h-zinr*/ 
            AND resline1.resstatus NE 13 USE-INDEX zinr_index NO-LOCK NO-ERROR.
        IF AVAILABLE resline1 THEN
        DO:
            FIND FIRST guest1 WHERE guest1.gastnr = resline1.gastnrmember
                USE-INDEX gastnr_index NO-LOCK NO-ERROR.
            IF AVAILABLE guest1 THEN
            DO:
                guestname = guest1.NAME + " " + guest1.vorname1 + ", " + 
                    guest1.anrede1 + guest1.anredefirma.
            END.
        END.
        ELSE
        DO:
            guestname = "".
        END.
    END.
END.
