DEFINE TEMP-TABLE f-list
    FIELD bname AS CHAR FORMAT "x(24)"
    FIELD room  AS CHAR FORMAT "x(24)"
    FIELD id    AS CHAR FORMAT "x(2)"
    FIELD event AS CHAR FORMAT "x(16)"
    FIELD cdate AS DATE FORMAT "99/99/99"
    FIELD cancel AS DATE FORMAT "99/99/99"
    FIELD pax   AS INTEGER FORMAT ">>>,>>9"
    FIELD rmrev AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD fbrev AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD otrev AS DECIMAL FORMAT "->>>,>>>,>>9.99"
    FIELD totrev AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    .

DEFINE TEMP-TABLE output-list
    FIELD flag AS CHAR
    FIELD bezeich  AS CHAR
    FIELD room  AS CHAR
    FIELD id    AS CHAR
    FIELD ba-event AS CHAR
    FIELD datum AS DATE
    FIELD cancel AS DATE
    FIELD pax   AS INTEGER
    FIELD rmrev AS DECIMAL
    FIELD fbrev AS DECIMAL
    FIELD othrev AS DECIMAL
    FIELD totrev AS DECIMAL.

DEF INPUT  PARAMETER sorttype  AS INTEGER.
DEF INPUT  PARAMETER fdate     AS DATE.
DEF INPUT  PARAMETER tdate     AS DATE.
DEF OUTPUT PARAMETER TABLE FOR output-list.

DEFINE BUFFER gast        FOR guest.
DEFINE BUFFER usr         FOR bediener.
DEFINE BUFFER room        FOR bk-raum.
DEFINE BUFFER event       FOR ba-typ.


DEFINE VARIABLE str1        AS CHAR    INITIAL "".
DEFINE VARIABLE totrmrev    AS DECIMAL INITIAL 0.
DEFINE VARIABLE totfbrev    AS DECIMAL INITIAL 0.
DEFINE VARIABLE totother    AS DECIMAL INITIAL 0.
DEFINE VARIABLE totrev      AS DECIMAL INITIAL 0.
DEFINE VARIABLE totpax      AS INTEGER.
DEFINE VARIABLE subrmrev    AS DECIMAL INITIAL 0.
DEFINE VARIABLE subfbrev    AS DECIMAL INITIAL 0.
DEFINE VARIABLE subother    AS DECIMAL INITIAL 0.
DEFINE VARIABLE subrev      AS DECIMAL INITIAL 0.
DEFINE VARIABLE subpax      AS INTEGER.


RUN create-browse.

PROCEDURE create-browse:
    DEFINE VARIABLE groupby AS CHAR  INITIAL "" NO-UNDO.
    DEFINE VARIABLE line1   AS INTEGER INITIAL 0 NO-UNDO.

    FOR EACH output-list:
        DELETE output-list.
    END.

    RUN create-list.
    
    ASSIGN
        totrmrev    = 0
        totfbrev    = 0
        totother    = 0
        totpax      = 0
        totrev      = 0.

    IF sorttype = 0 THEN
    DO:
        FOR EACH f-list NO-LOCK BY f-list.ID:
            line1 = line1 + 1.
            
            IF line1 = 1 THEN
            DO:
                groupby = f-list.ID.
                RUN create-group ("SALES ID", groupby).
            END.

            IF f-list.ID NE groupby THEN
            DO:
                RUN create-subtotal.
                RUN create-group("SALES ID", f-list.id).
            END.

            RUN create-data.
            groupby = f-list.ID.
        END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
        FOR EACH f-list NO-LOCK BY f-list.room:
            line1 = line1 + 1.

            IF line1 = 1 THEN
            DO:
                groupby = f-list.room.
                RUN create-group ("ROOM", groupby).
            END.

            IF f-list.room NE groupby THEN
            DO:
                RUN create-subtotal.
                RUN create-group ("ROOM", f-list.room).
            END.

            RUN create-data.
            groupby = f-list.room.
        END.
    END.    
    ELSE
    DO:
        FOR EACH f-list NO-LOCK BY f-list.event:
            line1 = line1 + 1.

            IF line1 = 1 THEN
            DO:
                groupby = f-list.event.
                RUN create-group ("EVENT", groupby).
            END.

            IF f-list.event NE groupby THEN
            DO:
                RUN create-subtotal.
                RUN create-group ("EVENT", f-list.event).
            END.

            RUN create-data.
            groupby = f-list.event.
        END.
    END.

    FIND FIRST f-list NO-LOCK NO-ERROR.
    IF AVAILABLE f-list THEN
    DO:
        RUN create-subtotal.
    
       CREATE output-list.
       ASSIGN 
           output-list.flag = "TOTAL"
           output-list.bezeich = "T O T A L"
           output-list.pax = totpax
           output-list.rmrev = totrmrev
           output-list.fbrev = totfbrev
           output-list.othrev = totother
           output-list.totrev = totrev.
    END.
END.   

PROCEDURE create-data:
    CREATE output-list.
    ASSIGN 
        output-list.bezeich = f-list.bname
        output-list.room = f-list.room
        output-list.id = f-list.ID
        output-list.ba-event = f-list.EVENT
        output-list.datum = f-list.cDATE
        output-list.cancel = f-list.cancel
        output-list.pax = f-list.pax
        output-list.rmrev = f-list.rmrev
        output-list.fbrev = f-list.fbrev
        output-list.othrev = f-list.otrev
        output-list.totrev = f-list.totrev.
        
    ASSIGN
        subpax   = subpax + f-list.pax
        subrmrev = subrmrev + f-list.rmrev
        subfbrev = subfbrev + f-list.fbrev
        subother = subother + f-list.otrev
        subrev   = subrev + f-list.totrev
        totpax   = totpax + f-list.pax
        totrmrev = totrmrev + f-list.rmrev
        totfbrev = totfbrev + f-list.fbrev
        totother = totother + f-list.otrev
        totrev   = totrev + f-list.totrev
    .
END.


PROCEDURE create-list:
    DEF VAR salesid     AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR roomDesc    AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR bname       AS CHAR    INITIAL "" NO-UNDO.
    DEF VAR other-rev   AS DECIMAL INITIAL 0  NO-UNDO.
    DEF VAR eventDesc   AS CHAR    INITIAL "" NO-UNDO.
    
    FOR EACH f-list:
        DELETE f-list.
    END.

    FOR EACH bk-stat WHERE bk-stat.datum GE fdate AND bk-stat.datum LE tdate
        AND bk-stat.isstatus = 9 USE-INDEX datestat_ix NO-LOCK:
               
        FIND FIRST room WHERE room.raum = bk-stat.room USE-INDEX raum-ix NO-LOCK NO-ERROR.
        IF AVAILABLE room THEN roomDesc = room.bezeich.
        ELSE roomDesc = "Not defined".

        FIND FIRST gast WHERE gast.gastnr = bk-stat.gastnr USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE gast THEN bname = gast.name + ", " + gast.vorname1 + " " 
            + gast.anrede1 + gast.anredefirma.
        ELSE bname = "Not defined".

        FIND FIRST event WHERE event.typ-id = bk-stat.event-nr USE-INDEX bankettyp_ix NO-LOCK NO-ERROR.
        IF AVAILABLE event THEN eventDesc = event.bezeichnung.

        CREATE f-list.
        ASSIGN
            f-list.bname = bname
            f-list.room  = roomDesc
            f-list.ID    = bk-stat.salesID
            f-list.event = eventDesc
            f-list.cdate = bk-stat.datum
            f-list.cancel = bk-stat.cancel-date
            f-list.pax   = bk-stat.pax
            f-list.rmrev = bk-stat.rm-rev
            f-list.fbrev = bk-stat.fb-rev
            f-list.otrev = bk-stat.other-rev
            f-list.totrev = bk-stat.rm-rev + bk-stat.fb-rev + 
                bk-stat.other-rev
            .
    END.
END. 


PROCEDURE create-group:
    DEFINE INPUT PARAMETER bezeich AS CHAR.
    DEFINE INPUT PARAMETER bezeich1 AS CHAR.

    CREATE output-list.
    ASSIGN 
        output-list.flag = "GROUP"
        output-list.bezeich = bezeich + " : " + bezeich1.
END.

PROCEDURE create-subtotal:
    CREATE output-list.
    ASSIGN
        output-list.flag = "LINE".
    
    CREATE output-list.
    ASSIGN 
        output-list.flag = "SUB"
        output-list.bezeich = "Subtotal"
        output-list.pax = subpax
        output-list.rmrev = subrmrev
        output-list.fbrev = subfbrev
        output-list.othrev = subother
        output-list.totrev = subrev.

    CREATE output-list.
    output-list.flag = "SPACE".
         

    ASSIGN
        subrmrev    = 0
        subfbrev    = 0
        subother    = 0 
        subrev      = 0
        subpax      = 0
        .
END.

