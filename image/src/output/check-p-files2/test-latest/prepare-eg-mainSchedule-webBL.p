
DEFINE TEMP-TABLE t-eg-location LIKE eg-location.
DEFINE TEMP-TABLE t-eg-property LIKE eg-property.
DEFINE TEMP-TABLE t-eg-staff LIKE eg-staff.
DEFINE TEMP-TABLE t-zimmer LIKE zimmer
    FIELD gname-str AS CHAR FORMAT "x(60)".
DEFINE TEMP-TABLE t-queasy LIKE queasy.

DEFINE TEMP-TABLE action LIKE eg-action
    FIELD SELECTED AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE staff LIKE eg-staff
    FIELD staff-SELECTED AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE maintain LIKE eg-maintain.

DEF BUFFER resline1 FOR res-line.              
DEF BUFFER guest1 FOR guest.              

DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT PARAMETER dayplan  AS DATE.
DEF INPUT PARAMETER firstday AS DATE.
DEF INPUT PARAMETER endday   AS DATE.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER TABLE FOR maintain.
DEF OUTPUT PARAMETER TABLE FOR action.
DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR t-zimmer.
DEF OUTPUT PARAMETER TABLE FOR t-eg-property.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-eg-staff.

/*DEF VAR user-init AS CHAR INIT "01".
DEF VAR dayplan  AS DATE INIT "".
DEF VAR firstday AS DATE INIT "".
DEF VAR endday   AS DATE INIT "".
DEF VAR GroupID AS INT.
DEF VAR EngID AS INT.*/

DEF VAR guestname AS CHAR.

CREATE maintain. 

RUN define-group.
RUN define-engineering.
RUN create-action.
RUN create-Staff.
RUN init-maintain.

FOR EACH eg-location:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.

FOR EACH zimmer:
    RUN get-guestname(zimmer.zinr).
    CREATE t-zimmer.
    BUFFER-COPY zimmer TO t-zimmer.
    ASSIGN t-zimmer.gname-str = guestname.
END.

FOR EACH eg-property:
    CREATE t-eg-property.
    BUFFER-COPY eg-property TO t-eg-property.
END.

FOR EACH queasy WHERE KEY = 132 OR KEY = 133 OR KEY = 135:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

FOR EACH eg-staff:
    CREATE t-eg-staff.
    BUFFER-COPY eg-staff TO t-eg-staff.
END.

/*FOR EACH t-queasy:
    MESSAGE t-queasy.KEY t-queasy.char1 VIEW-AS ALERT-BOX INFO.
END.*/

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
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
            VIEW-AS ALERT-BOX INFORMATION. */
    END.
END.

PROCEDURE create-action:
    DEF BUFFER qbuff FOR eg-action.

    FOR EACH action:
        DELETE action.
    END.

    FOR EACH qbuff WHERE qbuff.usefor NE 2 NO-LOCK:
        CREATE action.
        ASSIGN action.actionnr = qbuff.actionnr
           action.bezeich = qbuff.bezeich
           action.maintask = qbuff.maintask
           action.SELECTED = NO.
    END.                                    
END.

PROCEDURE create-Staff:
    DEF BUFFER qbuff FOR eg-staff.

    FOR EACH staff :
        DELETE staff.
    END.

    FOR EACH qbuff WHERE qbuff.usergroup = engid  AND qbuff.activeflag = YES NO-LOCK:
        CREATE staff.
        ASSIGN staff.nr = qbuff.nr
           staff.NAME = qbuff.NAME
           staff.staff-SELECTED = NO.
    END.                                    
END.

PROCEDURE init-maintain:

    FIND FIRST counters WHERE counters.counter-no = 38 EXCLUSIVE-LOCK NO-ERROR.
    IF NOT AVAILABLE counters THEN
        DO:
            CREATE counters.
            ASSIGN counters.counter-no = 38
                counters.counter-bez = "Counter for maintenance in engineering"
                counters.counter = 0.
        END.
    ELSE
        DO:
            FIND CURRENT counters NO-LOCK.
        END.

    ASSIGN
        maintain.maintainnr = counters.counter + 1
        maintain.workdate = ? 
        maintain.TYPE = 1
        maintain.category = 0
        maintain.maintask = 0  
        maintain.propertynr = 0
        maintain.comments = ""
        maintain.typework = 1
        maintain.pic = 0
        .

    IF dayplan NE ? THEN
    DO:
       ASSIGN
            maintain.estworkdate = dayplan.
    END.
    ELSE
    DO:

        IF Firstday > TODAY THEN
        DO:
            ASSIGN
                maintain.estworkdate = firstday.
        END.
        ELSE
        DO:
            IF endday > TODAY THEN
            DO:
                ASSIGN
                    maintain.estworkdate = TODAY.
            END.
            ELSE
            DO:
                ASSIGN                                
                    maintain.estworkdate = TODAY.
            END.
        END.
    END.
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
