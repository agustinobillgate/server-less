DEFINE TEMP-TABLE str-list
    FIELD num       AS INTEGER
    FIELD artnr     AS INTEGER
    FIELD bezeich   AS CHAR FORMAT "x(32)"
    FIELD qty       AS INTEGER FORMAT "->,>>>,>>9" EXTENT 12 
    FIELD avrg      AS DECIMAL FORMAT "->>,>>>,>>9.99" EXTENT 12
    FIELD amt       AS DECIMAL FORMAT "->,>>>,>>>,>>9" EXTENT 12
    FIELD tot-qty   AS INTEGER FORMAT ">,>>>,>>9"
    FIELD tot-amt   AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD del-flag  AS LOGICAL 
    .

DEF INPUT  PARAMETER pvILanguage AS INT  NO-UNDO.
DEF INPUT  PARAMETER sorttype    AS INT.
DEF INPUT  PARAMETER from-grp    AS INT.
DEF INPUT  PARAMETER mm          AS INT.
DEF INPUT  PARAMETER yy          AS INT.
DEF OUTPUT PARAMETER TABLE FOR str-list.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "stock-outannual". 

DEFINE VARIABLE end-date AS INTEGER EXTENT 12  NO-UNDO
    INITIAL [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31].

DEFINE VARIABLE end-date1 AS INTEGER EXTENT 12 NO-UNDO
    INITIAL [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31].


DEFINE VARIABLE to-date     AS DATE NO-UNDO.
DEFINE VARIABLE from-date   AS DATE NO-UNDO.
DEFINE VARIABLE datum       AS DATE NO-UNDO.
DEFINE VARIABLE closed-date AS DATE NO-UNDO.
DEFINE VARIABLE date-mat    AS DATE NO-UNDO.
DEFINE VARIABLE date-fb     AS DATE NO-UNDO.
DEFINE VARIABLE num-date    AS INTEGER. /* Malik Serverless 658 */


FIND FIRST htparam WHERE paramnr = 221 NO-LOCK.
date-mat = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.
date-fb = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

IF date-mat GT date-fb THEN
    closed-date = date-mat.
ELSE closed-date = date-fb.

ASSIGN from-date = DATE(1,1,yy).

/* Malik Serverless 658 update date conversion */
IF yy MODULO 4 NE 0 THEN
DO:
    num-date = end-date1[mm].
    /* to-date   = DATE(mm, end-date1[mm], yy). */
    to-date   = DATE(mm, num-date, yy).
END.
ELSE
DO:
    num-date = end-date1[mm].
    /* to-date   = DATE(mm, end-date[mm], yy). */
    to-date   = DATE(mm, num-date, yy).
END.
/* END Malik */

IF from-date LE closed-date THEN DO:
    IF from-grp = 0 THEN RUN create-list(mm, yy).
    ELSE RUN create-list1(mm, yy).

END.
ELSE DO:
    IF from-grp = 0 THEN RUN create-list2(mm, yy).
    ELSE RUN create-list3(mm, yy).
END.


PROCEDURE create-list:
    DEFINE INPUT PARAMETER mm   AS INTEGER.
    DEFINE INPUT PARAMETER yy   AS INTEGER.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEF VAR tot-qty             AS INTEGER EXTENT 12.
    DEF VAR tot-amt             AS DECIMAL EXTENT 12.
    DEF VAR del-flag AS LOGICAL INITIAL YES.

    DEF VARIABLE sdate AS DATE NO-UNDO.
    DEF VARIABLE edate AS DATE NO-UNDO.
    
    FOR EACH str-list:
        DELETE str-list.
    END.

    ASSIGN 
        sdate = from-date
        /*edate = closed-date.*/
        edate = to-date.

    
    FOR EACH l-ophis WHERE l-ophis.datum GE sdate
        AND l-ophis.datum LE edate 
        AND l-ophis.op-art = 3,
        FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr
           NO-LOCK BY l-ophis.artnr:
        
         FIND FIRST str-list WHERE str-list.artnr = l-ophis.artnr
            NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            CREATE str-list.
            ASSIGN 
                str-list.artnr      = l-artikel.artnr
                str-list.bezeich    = l-artikel.bezeich.
        END.
        ASSIGN 
            str-list.qty[MONTH(l-ophis.datum)] = str-list.qty[MONTH(l-ophis.datum)] + l-ophis.anzahl
            str-list.amt[MONTH(l-ophis.datum)] = str-list.amt[MONTH(l-ophis.datum)] + l-ophis.warenwert.
        IF str-list.qty[MONTH(l-ophis.datum)] GT 0 THEN
            str-list.avrg[MONTH(l-ophis.datum)] = str-list.amt[MONTH(l-ophis.datum)] / str-list.qty[MONTH(l-ophis.datum)].
    END.

    ASSIGN sdate = closed-date + 1
           edate = to-date.

    FOR EACH l-op WHERE l-op.datum GE sdate
          AND l-op.datum LE edate
          AND l-op.op-art = 3
          AND l-op.loeschflag LE 1 NO-LOCK,
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.artnr:

        FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            CREATE str-list.
            ASSIGN 
                str-list.artnr      = l-artikel.artnr
                str-list.bezeich    = l-artikel.bezeich.
        END.
        ASSIGN 
            str-list.qty[MONTH(l-op.datum)]    = str-list.qty[MONTH(l-op.datum)] + l-op.anzahl
            str-list.amt[MONTH(l-op.datum)]    = str-list.amt[MONTH(l-op.datum)] + l-op.warenwert.
        IF str-list.qty[MONTH(l-op.datum)] GT 0 THEN
            str-list.avrg[MONTH(l-op.datum)]   = str-list.amt[MONTH(l-op.datum)] / str-list.qty[MONTH(l-op.datum)].
    END.

    FOR EACH str-list NO-LOCK:
        DO i = 1 TO 12:
            ASSIGN
                str-list.tot-qty = str-list.tot-qty + str-list.qty[i]
                str-list.tot-amt = str-list.tot-amt + str-list.amt[i]
                tot-qty[i]       = tot-qty[i] + str-list.qty[i]
                tot-amt[i]       = tot-amt[i] + str-list.amt[i].
        END.
    END.

    IF sorttype = 0 THEN
        FOR EACH str-list WHERE str-list.tot-qty = 0:
            DELETE str-list.
        END.
     ELSE IF sorttype = 1 THEN
     DO:
         FOR EACH str-list:
            del-flag = YES.
            DO i = 1 TO 12:
                IF str-list.avrg[i] NE 0 THEN
                    del-flag = NO.
            END.
            IF del-flag THEN
                DELETE str-list.
        END.
     END.
     ELSE 
        FOR EACH str-list WHERE str-list.tot-amt = 0:
            DELETE str-list.
        END.
   
    IF sorttype NE 1 THEN
    DO:
        CREATE str-list.
        ASSIGN
            str-list.bezeich = translateExtended("T O T A L", lvCAREA, "").
        DO i = 1 TO 12:
            ASSIGN
                str-list.qty[i]     = tot-qty[i]
                str-list.amt[i]     = tot-amt[i].
                
        END.
    END.
    /*MTHIDE FRAME frame2 NO-PAUSE.*/
END.


PROCEDURE create-list1:
    DEFINE INPUT PARAMETER mm   AS INTEGER.
    DEFINE INPUT PARAMETER yy   AS INTEGER.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEFINE VARIABLE tot-qty     AS INTEGER EXTENT 12.
    DEFINE VARIABLE tot-amt     AS DECIMAL EXTENT 12.
    DEFINE VARIABLE del-flag    AS LOGICAL INITIAL YES.

    DEF VARIABLE sdate AS DATE NO-UNDO.
    DEF VARIABLE edate AS DATE NO-UNDO.
    

    FOR EACH str-list:
        DELETE str-list.
    END.

    ASSIGN 
        sdate = from-date
        /*edate = closed-date.*/
        edate = to-date.

    FOR EACH l-ophis WHERE l-ophis.datum GE sdate
        AND l-ophis.datum LE edate 
        AND l-ophis.op-art = 3,
        FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr
            AND l-artikel.endkum = from-grp NO-LOCK BY l-ophis.artnr:
        
         FIND FIRST str-list WHERE str-list.artnr = l-ophis.artnr
            NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            CREATE str-list.
            ASSIGN 
                str-list.artnr      = l-artikel.artnr
                str-list.bezeich    = l-artikel.bezeich.
        END.
        ASSIGN 
            str-list.qty[MONTH(l-ophis.datum)] = str-list.qty[MONTH(l-ophis.datum)] + l-ophis.anzahl
            str-list.amt[MONTH(l-ophis.datum)] = str-list.amt[MONTH(l-ophis.datum)] + l-ophis.warenwert.
        IF str-list.qty[MONTH(l-ophis.datum)] GT 0 THEN
            str-list.avrg[MONTH(l-ophis.datum)] = str-list.amt[MONTH(l-ophis.datum)] / str-list.qty[MONTH(l-ophis.datum)].
    END.

    ASSIGN sdate = closed-date + 1
           edate = to-date.

    FOR EACH l-op WHERE l-op.datum GE sdate
        AND l-op.datum LE edate
        AND l-op.op-art = 3
        AND l-op.loeschflag LE 1 NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            AND l-artikel.endkum = from-grp NO-LOCK BY l-op.artnr:

        FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            CREATE str-list.
            ASSIGN 
                str-list.artnr      = l-artikel.artnr
                str-list.bezeich    = l-artikel.bezeich.
        END.
        ASSIGN 
            str-list.qty[MONTH(l-op.datum)]    = str-list.qty[MONTH(l-op.datum)] + l-op.anzahl
            str-list.amt[MONTH(l-op.datum)]    = str-list.amt[MONTH(l-op.datum)] + l-op.warenwert.
        IF str-list.qty[MONTH(l-op.datum)] GT 0 THEN
            str-list.avrg[MONTH(l-op.datum)]   = str-list.amt[MONTH(l-op.datum)] / str-list.qty[MONTH(l-op.datum)].
    END.

    
    FOR EACH str-list NO-LOCK:
        DO i = 1 TO 12:
            ASSIGN
                str-list.tot-qty = str-list.tot-qty + str-list.qty[i]
                str-list.tot-amt = str-list.tot-amt + str-list.amt[i]
                tot-qty[i]       = tot-qty[i] + str-list.qty[i]
                tot-amt[i]       = tot-amt[i] + str-list.amt[i].
        END.
    END.

    IF sorttype = 0 THEN
        FOR EACH str-list WHERE str-list.tot-qty = 0:
            DELETE str-list.
        END.
     ELSE IF sorttype = 1 THEN
     DO:
         FOR EACH str-list:
            del-flag = YES.
            DO i = 1 TO 12:
                IF str-list.avrg[i] NE 0 THEN
                    del-flag = NO.
            END.
            IF del-flag THEN
                DELETE str-list.
        END.
     END.
     ELSE 
        FOR EACH str-list WHERE str-list.tot-amt = 0:
            DELETE str-list.
        END.
   
    IF sorttype NE 1 THEN
    DO:
        CREATE str-list.
        ASSIGN
            str-list.bezeich = translateExtended("T O T A L", lvCAREA, "").
        DO i = 1 TO 12:
            ASSIGN
                str-list.qty[i]     = tot-qty[i]
                str-list.amt[i]     = tot-amt[i].
                
        END.
    END.
    /*MTHIDE FRAME frame2 NO-PAUSE.*/
END.

PROCEDURE create-list2:
    DEFINE INPUT PARAMETER mm   AS INTEGER.
    DEFINE INPUT PARAMETER yy   AS INTEGER.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEF VAR tot-qty             AS INTEGER EXTENT 12.
    DEF VAR tot-amt             AS DECIMAL EXTENT 12.
    DEF VAR del-flag AS LOGICAL INITIAL YES.

    DEF VARIABLE sdate AS DATE NO-UNDO.
    DEF VARIABLE edate AS DATE NO-UNDO.
    
    FOR EACH str-list:
        DELETE str-list.
    END.

    FOR EACH l-op WHERE l-op.datum GE from-date
          AND l-op.datum LE to-date
          AND l-op.op-art = 3
          AND l-op.loeschflag LE 1 NO-LOCK,
          FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
          NO-LOCK BY l-op.artnr:

        FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            CREATE str-list.
            ASSIGN 
                str-list.artnr      = l-artikel.artnr
                str-list.bezeich    = l-artikel.bezeich.
        END.
        ASSIGN 
            str-list.qty[MONTH(l-op.datum)]    = str-list.qty[MONTH(l-op.datum)] + l-op.anzahl
            str-list.amt[MONTH(l-op.datum)]    = str-list.amt[MONTH(l-op.datum)] + l-op.warenwert.
        IF str-list.qty[MONTH(l-op.datum)] GT 0 THEN
            str-list.avrg[MONTH(l-op.datum)]   = str-list.amt[MONTH(l-op.datum)] / str-list.qty[MONTH(l-op.datum)].
    END.

    FOR EACH str-list NO-LOCK:
        DO i = 1 TO 12:
            ASSIGN
                str-list.tot-qty = str-list.tot-qty + str-list.qty[i]
                str-list.tot-amt = str-list.tot-amt + str-list.amt[i]
                tot-qty[i]       = tot-qty[i] + str-list.qty[i]
                tot-amt[i]       = tot-amt[i] + str-list.amt[i].
        END.
    END.

    IF sorttype = 0 THEN
        FOR EACH str-list WHERE str-list.tot-qty = 0:
            DELETE str-list.
        END.
     ELSE IF sorttype = 1 THEN
     DO:
         FOR EACH str-list:
            del-flag = YES.
            DO i = 1 TO 12:
                IF str-list.avrg[i] NE 0 THEN
                    del-flag = NO.
            END.
            IF del-flag THEN
                DELETE str-list.
        END.
     END.
     ELSE 
        FOR EACH str-list WHERE str-list.tot-amt = 0:
            DELETE str-list.
        END.
   
    IF sorttype NE 1 THEN
    DO:
        CREATE str-list.
        ASSIGN
            str-list.bezeich = translateExtended("T O T A L", lvCAREA, "").
        DO i = 1 TO 12:
            ASSIGN
                str-list.qty[i]     = tot-qty[i]
                str-list.amt[i]     = tot-amt[i].
                
        END.
    END.
    /*MTHIDE FRAME frame2 NO-PAUSE.*/
END.


PROCEDURE create-list3:
    DEFINE INPUT PARAMETER mm   AS INTEGER.
    DEFINE INPUT PARAMETER yy   AS INTEGER.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEF VAR tot-qty             AS INTEGER EXTENT 12.
    DEF VAR tot-amt             AS DECIMAL EXTENT 12.
    DEF VAR del-flag AS LOGICAL INITIAL YES.

    DEF VARIABLE sdate AS DATE NO-UNDO.
    DEF VARIABLE edate AS DATE NO-UNDO.
    

    FOR EACH str-list:
        DELETE str-list.
    END.

    FOR EACH l-op WHERE l-op.datum GE from-date
        AND l-op.datum LE to-date
        AND l-op.op-art = 3
        AND l-op.loeschflag LE 1 NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
            AND l-artikel.endkum = from-grp NO-LOCK BY l-op.artnr:

        FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            CREATE str-list.
            ASSIGN 
                str-list.artnr      = l-artikel.artnr
                str-list.bezeich    = l-artikel.bezeich.
        END.
        ASSIGN 
            str-list.qty[MONTH(l-op.datum)]    = str-list.qty[MONTH(l-op.datum)] + l-op.anzahl
            str-list.amt[MONTH(l-op.datum)]    = str-list.amt[MONTH(l-op.datum)] + l-op.warenwert.
        IF str-list.qty[MONTH(l-op.datum)] GT 0 THEN
            str-list.avrg[MONTH(l-op.datum)]   = str-list.amt[MONTH(l-op.datum)] / str-list.qty[MONTH(l-op.datum)].
    END.

    
    FOR EACH str-list NO-LOCK:
        DO i = 1 TO 12:
            ASSIGN
                str-list.tot-qty = str-list.tot-qty + str-list.qty[i]
                str-list.tot-amt = str-list.tot-amt + str-list.amt[i]
                tot-qty[i]       = tot-qty[i] + str-list.qty[i]
                tot-amt[i]       = tot-amt[i] + str-list.amt[i].
        END.
    END.

    IF sorttype = 0 THEN
        FOR EACH str-list WHERE str-list.tot-qty = 0:
            DELETE str-list.
        END.
     ELSE IF sorttype = 1 THEN
     DO:
         FOR EACH str-list:
            del-flag = YES.
            DO i = 1 TO 12:
                IF str-list.avrg[i] NE 0 THEN
                    del-flag = NO.
            END.
            IF del-flag THEN
                DELETE str-list.
        END.
     END.
     ELSE 
        FOR EACH str-list WHERE str-list.tot-amt = 0:
            DELETE str-list.
        END.
   
    IF sorttype NE 1 THEN
    DO:
        CREATE str-list.
        ASSIGN
            str-list.bezeich = translateExtended("T O T A L", lvCAREA, "").
        DO i = 1 TO 12:
            ASSIGN
                str-list.qty[i]     = tot-qty[i]
                str-list.amt[i]     = tot-amt[i].
                
        END.
    END.
    /*MTHIDE FRAME frame2 NO-PAUSE.*/
END.

