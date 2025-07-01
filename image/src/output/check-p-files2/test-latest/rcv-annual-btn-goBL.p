/*Only Used Foe vhpCloud Now*/
DEFINE TEMP-TABLE str-list
    FIELD num       AS INTEGER
    FIELD artnr     AS INTEGER
    FIELD bezeich   AS CHAR FORMAT "x(32)"
    /*FIELD qty       AS INTEGER FORMAT "->>,>>9" EXTENT 12 */
    FIELD qty       AS DECIMAL FORMAT "->>,>>9.99" EXTENT 12
    FIELD avrg      AS DECIMAL FORMAT "->,>>>,>>9.99" EXTENT 12
    FIELD amt       AS DECIMAL FORMAT "->,>>>,>>>,>>9" EXTENT 12
    /*FIELD tot-qty   AS INTEGER FORMAT ">>>,>>9"*/
    FIELD tot-qty   AS DECIMAL FORMAT ">>>,>>9.99"
    FIELD tot-amt   AS DECIMAL FORMAT "->,>>>,>>>,>>9"
    FIELD del-flag  AS LOGICAL.

DEF INPUT PARAMETER pvILanguage AS INT  NO-UNDO.
DEF INPUT PARAMETER from-grp    AS INT.
DEF INPUT PARAMETER mm          AS INT.
DEF INPUT PARAMETER yy          AS INT.
DEF INPUT PARAMETER sorttype    AS INT.
DEF OUTPUT PARAMETER TABLE FOR str-list.

{ supertransbl.i } 
DEF VAR lvCAREA AS CHAR INITIAL "rcv-annual".

IF from-grp = 0 THEN RUN create-list(mm, yy). 
ELSE RUN create-list1(mm, yy). 

PROCEDURE create-list:
    DEFINE INPUT PARAMETER mm   AS INTEGER.
    DEFINE INPUT PARAMETER yy   AS INTEGER.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEFINE VARIABLE to-date     AS DATE NO-UNDO.
    DEFINE VARIABLE from-date   AS DATE NO-UNDO.
    DEFINE VARIABLE datum       AS DATE NO-UNDO.
    DEF VAR closed-date         AS DATE NO-UNDO.
    DEF VAR date-mat            AS DATE NO-UNDO.
    DEF VAR date-fb             AS DATE NO-UNDO.
    DEF VAR tot-qty             AS INTEGER EXTENT 12.
    DEF VAR tot-amt             AS DECIMAL EXTENT 12.
    DEF VAR del-flag            AS LOGICAL INITIAL YES.
    DEFINE VARIABLE zeit        AS INTEGER.
    /*
    FIND FIRST htparam WHERE paramnr = 474 NO-LOCK.
    date1 = fdate.
    date2 = DATE(MONTH(date1), 1, YEAR(date1)).
    beg-date = date2 - 1.
    */
    FIND FIRST htparam WHERE paramnr = 221 NO-LOCK.
    date-mat = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */
    FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.
    date-fb = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

    IF date-mat GT date-fb THEN closed-date = date-mat.
    ELSE closed-date = date-fb.

    FOR EACH str-list:
        DELETE str-list.
    END.

    DO i = /*1*/ mm TO mm:
        from-date   = DATE(i, 1, yy).
        /*to-date     = from-date + 32.
        to-date     = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1.*/
        to-date     = DATE(i + 1, 1, yy).
        to-date     = to-date - 1.        
        
        DO datum = from-date TO to-date:
            IF datum LE closed-date THEN
            DO:                
                FOR EACH l-ophis WHERE l-ophis.datum = datum 
                    AND l-ophis.op-art = 1 NO-LOCK,
                    FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr NO-LOCK BY l-ophis.artnr:
                     
                    FIND FIRST str-list WHERE str-list.artnr = l-ophis.artnr NO-ERROR.
                    IF NOT AVAILABLE str-list THEN
                    DO:
                        CREATE str-list.
                        ASSIGN 
                            str-list.artnr      = l-artikel.artnr
                            str-list.bezeich    = l-artikel.bezeich.
                    END.

                    ASSIGN
                        str-list.qty[i]    = str-list.qty[i] + l-ophis.anzahl
                        str-list.amt[i]    = str-list.amt[i] + l-ophis.warenwert.
                    IF str-list.qty[i] GT 0 THEN
                        str-list.avrg[i]   = str-list.amt[i] / str-list.qty[i]
                        .
                END.
            END.       
            ELSE 
            DO:
                FOR EACH l-op WHERE l-op.datum = datum 
                    AND l-op.op-art = 1 AND l-op.loeschflag LE 1 NO-LOCK,
                    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
                    NO-LOCK BY l-op.artnr : 
                
                   FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR.
                   IF NOT AVAILABLE str-list THEN
                   DO:
                       CREATE str-list.
                       ASSIGN 
                           str-list.artnr      = l-artikel.artnr
                           str-list.bezeich    = l-artikel.bezeich.
                   END.
                   ASSIGN
                       str-list.qty[i]    = str-list.qty[i] + l-op.anzahl
                       str-list.amt[i]    = str-list.amt[i] + l-op.warenwert.
                   IF str-list.qty[i] GT 0 THEN
                       str-list.avrg[i]   = str-list.amt[i] / str-list.qty[i].
                END.
            END.
        END.
    END.           

    FOR EACH str-list NO-LOCK:
        DO i = /*1 TO 12*/ mm TO mm:
            ASSIGN
                str-list.tot-qty = str-list.tot-qty + str-list.qty[i]
                str-list.tot-amt = str-list.tot-amt + str-list.amt[i]
                tot-qty[i]       = tot-qty[i] + str-list.qty[i]
                tot-amt[i]       = tot-amt[i] + str-list.amt[i].
        END.
    END.

    IF sorttype = 0 THEN
    DO:
        FOR EACH str-list WHERE str-list.tot-qty = 0:
            DELETE str-list.
        END.
    END.
    ELSE IF sorttype = 1 THEN
    DO:
        FOR EACH str-list:
            del-flag = YES.
            DO i = /*1 TO 12*/ mm TO mm:
                IF str-list.avrg[i] NE 0 THEN
                    del-flag = NO.
            END.
            IF del-flag THEN DELETE str-list.
        END.
    END.
    ELSE 
    DO:
        FOR EACH str-list WHERE str-list.tot-amt = 0:
            DELETE str-list.
        END.
    END.
           
    IF sorttype NE 1 THEN
    DO:
        CREATE str-list.
        ASSIGN
            str-list.bezeich = translateExtended("T O T A L", lvCAREA, "").
        DO i = /*1 TO 12*/ mm TO mm:
            ASSIGN
                str-list.qty[i]     = tot-qty[i]
                str-list.amt[i]     = tot-amt[i].
                
        END.
    END.    
END.


PROCEDURE create-list1:
    DEFINE INPUT PARAMETER mm   AS INTEGER.
    DEFINE INPUT PARAMETER yy   AS INTEGER.
    DEFINE VARIABLE i           AS INTEGER NO-UNDO.
    DEFINE VARIABLE to-date     AS DATE NO-UNDO.
    DEFINE VARIABLE from-date   AS DATE NO-UNDO.
    DEFINE VARIABLE datum       AS DATE NO-UNDO.
    DEF VAR closed-date         AS DATE NO-UNDO.
    DEF VAR date-mat            AS DATE NO-UNDO.
    DEF VAR date-fb             AS DATE NO-UNDO.
    DEF VAR tot-qty             AS INTEGER EXTENT 12.
    DEF VAR tot-amt             AS DECIMAL EXTENT 12.
    DEF VAR del-flag            AS LOGICAL INITIAL YES.
    DEFINE VARIABLE zeit        AS INTEGER.

    /*
    FIND FIRST htparam WHERE paramnr = 474 NO-LOCK.
    date1 = fdate.
    date2 = DATE(MONTH(date1), 1, YEAR(date1)).
    beg-date = date2 - 1.
    */
    FIND FIRST htparam WHERE paramnr = 221 NO-LOCK.
    date-mat = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */
    FIND FIRST htparam WHERE paramnr = 224 NO-LOCK.
    date-fb = htparam.fdate.        /* Rulita 211024 | Fixing for serverless */

    IF date-mat GT date-fb THEN closed-date = date-mat.
    ELSE closed-date = date-fb.
    
    FOR EACH str-list:
        DELETE str-list.
    END.
/*
    FOR EACH l-artikel WHERE l-artikel.endkum = from-grp
        NO-LOCK BY l-artikel.bezeich : 
        CREATE str-list.
        ASSIGN
            str-list.artnr      = l-artikel.artnr
            str-list.bezeich    = l-artikel.bezeich.
  */
        DO i = /*1*/ mm TO mm:           
            from-date   = DATE(i, 1, yy).
            /*to-date     = from-date + 32.
            to-date     = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1.*/
            to-date     = DATE(i + 1, 1, yy).
            to-date     = to-date - 1.
            
            DO datum = from-date TO to-date:
                IF datum LE closed-date THEN
                DO:
                    FOR EACH l-ophis WHERE l-ophis.datum = datum 
                        AND l-ophis.op-art = 1 NO-LOCK, 
                        FIRST l-artikel WHERE l-artikel.artnr = l-ophis.artnr 
                        AND l-artikel.endkum = from-grp NO-LOCK BY l-ophis.artnr:

                        FIND FIRST str-list WHERE str-list.artnr = l-ophis.artnr NO-ERROR.
                        IF NOT AVAILABLE str-list THEN
                        DO:
                            CREATE str-list.
                            ASSIGN 
                                str-list.artnr      = l-artikel.artnr
                                str-list.bezeich    = l-artikel.bezeich.
                        END.
                        ASSIGN
                            str-list.qty[i]    = str-list.qty[i] + l-ophis.anzahl
                            str-list.amt[i]    = str-list.amt[i] + l-ophis.warenwert.
                        IF str-list.qty[i] GT 0 THEN
                            str-list.avrg[i]   = str-list.amt[i] / str-list.qty[i].
                    END.
                END.                    
                ELSE
                DO:
                    FOR EACH l-op WHERE l-op.datum = datum 
                        AND l-op.op-art = 1 AND l-op.loeschflag LT 2 NO-LOCK,
                        FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
                        AND l-artikel.endkum = from-grp NO-LOCK BY l-op.artnr : 

                        FIND FIRST str-list WHERE str-list.artnr = l-op.artnr NO-ERROR.
                        IF NOT AVAILABLE str-list THEN
                        DO:
                            CREATE str-list.
                            ASSIGN 
                                str-list.artnr      = l-artikel.artnr
                                str-list.bezeich    = l-artikel.bezeich.
                        END.

                        ASSIGN
                            str-list.qty[i]    = str-list.qty[i] + l-op.anzahl
                            str-list.amt[i]    = str-list.amt[i] + l-op.warenwert.
                        IF str-list.qty[i] GT 0 THEN
                            str-list.avrg[i]   = str-list.amt[i] / str-list.qty[i].
                    END.
                END.                                    
            END.
        END.
        
  /*  END. /*for each l-artikel*/*/

    FOR EACH str-list NO-LOCK:
        DO i = /*1 TO 12*/ mm TO mm:
            ASSIGN
                str-list.tot-qty = str-list.tot-qty + str-list.qty[i]
                str-list.tot-amt = str-list.tot-amt + str-list.amt[i]
                tot-qty[i]       = tot-qty[i] + str-list.qty[i]
                tot-amt[i]       = tot-amt[i] + str-list.amt[i].
        END.
    END.
    
    IF sorttype = 0 THEN
    DO:
        FOR EACH str-list WHERE str-list.tot-qty = 0:
            DELETE str-list.
        END.
    END.
        
    ELSE IF sorttype = 1 THEN
    DO:
        FOR EACH str-list:
           del-flag = YES.
           DO i = /*1 TO 12*/ mm TO mm:
               IF str-list.avrg[i] NE 0 THEN
                   del-flag = NO.
           END.
           IF del-flag THEN DELETE str-list.
       END.
    END.
    ELSE 
    DO:
       FOR EACH str-list WHERE str-list.tot-amt = 0:
           DELETE str-list.
       END.
    END.       
    
    IF sorttype NE 1 THEN
    DO: 
        CREATE str-list.
        ASSIGN
            str-list.bezeich = translateExtended("T O T A L", lvCAREA, "").
        DO i = /*1 TO 12*/ mm TO mm:
            ASSIGN
                str-list.qty[i]     = tot-qty[i]
                str-list.amt[i]     = tot-amt[i].
                
        END.
    END.    
END.
