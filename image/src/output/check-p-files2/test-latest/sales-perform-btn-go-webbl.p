/* Oscar - used only for VHP Cloud Version */

DEFINE TEMP-TABLE slist
    FIELD bezeich       AS CHARACTER
    FIELD Yr            AS INTEGER
    FIELD mnth          AS INTEGER
    FIELD userinit      AS CHARACTER
    FIELD lodg          LIKE salestat.argtumsatz
    FIELD lbudget       LIKE salesbud.argtumsatz
    FIELD lproz         AS DECIMAL FORMAT ">>9.99"
    FIELD fbrev         LIKE salestat.f-b-umsatz
    FIELD fbbudget      LIKE salesbud.f-b-umsatz
    FIELD fbproz        AS DECIMAL FORMAT ">>9.99"
    FIELD otrev         LIKE salestat.sonst-umsatz
    FIELD otbudget      LIKE salesbud.sonst-umsatz
    FIELD otproz        AS DECIMAL FORMAT ">>9.99"
    FIELD rmnight       LIKE salestat.room-nights
    FIELD rbudget       LIKE salesbud.room-nights 
    FIELD rmproz        AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-lodg      LIKE salestat.argtumsatz
    FIELD ytd-lbudget   LIKE salesbud.argtumsatz
    FIELD ytd-lproz     AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-fbrev     LIKE salestat.sonst-umsatz
    FIELD ytd-fbbudget  LIKE salesbud.sonst-umsatz
    FIELD ytd-fbproz    AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-rmnight   LIKE salestat.room-nights
    FIELD ytd-rbudget   LIKE salesbud.room-nights 
    FIELD ytd-rmproz    AS DECIMAL FORMAT ">>9.99"
    FIELD ytd-otrev     LIKE salestat.sonst-umsatz
    FIELD ytd-otbudget  LIKE salesbud.sonst-umsatz
    FIELD ytd-otproz    AS DECIMAL FORMAT ">>9.99"
    FIELD is-data       AS LOGICAL
.

DEF INPUT  PARAMETER from-date      AS CHAR.
DEF INPUT  PARAMETER to-date        AS CHAR.
DEF INPUT  PARAMETER usr-init       AS CHAR.
DEF INPUT  PARAMETER show-breakdown AS LOGICAL INITIAL YES.
DEF OUTPUT PARAMETER its-ok    AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER TABLE FOR slist.

DEFINE VARIABLE m1 AS INTEGER. 
DEFINE VARIABLE m2 AS INTEGER. 
DEFINE VARIABLE y1 AS INTEGER. 
DEFINE VARIABLE y2 AS INTEGER. 
DEFINE VARIABLE yy AS INTEGER. 
DEFINE VARIABLE monat AS INTEGER. 
DEFINE VARIABLE jahr AS INTEGER.
DEFINE VARIABLE usr-grp AS INT.

DEFINE VARIABLE user-total-lodg     AS DECIMAL.
DEFINE VARIABLE user-total-lbudget  AS DECIMAL.
DEFINE VARIABLE user-total-lproz    AS DECIMAL.
DEFINE VARIABLE user-total-fbrev    AS DECIMAL.
DEFINE VARIABLE user-total-fbbudget AS DECIMAL.
DEFINE VARIABLE user-total-fbproz   AS DECIMAL.
DEFINE VARIABLE user-total-otrev    AS DECIMAL.
DEFINE VARIABLE user-total-otbudget AS DECIMAL.
DEFINE VARIABLE user-total-otproz   AS DECIMAL.
DEFINE VARIABLE user-total-rmnight  AS DECIMAL.
DEFINE VARIABLE user-total-rbudget  AS DECIMAL.
DEFINE VARIABLE user-total-rmproz   AS DECIMAL.

FUNCTION add-start-zero RETURNS CHARACTER
    (input-int AS INTEGER, number-of-char AS INTEGER):

    DEFINE VARIABLE char-tmp AS CHARACTER NO-UNDO.
    DEFINE VARIABLE needed   AS INTEGER NO-UNDO.

    char-tmp = STRING(input-int).
    needed   = number-of-char - LENGTH(char-tmp).

    IF needed < 0 THEN needed = 0.

    char-tmp = FILL("0", needed) + char-tmp.

    RETURN char-tmp.
END FUNCTION.

m1 = INTEGER(SUBSTR(from-date,1,2)). 
y1 = INTEGER(SUBSTR(from-date,3,4)). 
y2 = INTEGER(SUBSTR(to-date,3,4)). 
m2 = INTEGER(SUBSTR(to-date,1,2)). 

IF usr-init EQ "ALL" OR usr-init EQ ? THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr EQ 547 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
        usr-grp = htparam.finteger.

    FOR EACH bediener WHERE bediener.user-group EQ usr-grp NO-LOCK:
        RUN check-budget.
        IF its-ok THEN
        DO: 
            ASSIGN
                user-total-lodg     = 0
                user-total-lbudget  = 0
                user-total-fbrev    = 0
                user-total-fbbudget = 0
                user-total-otrev    = 0
                user-total-otbudget = 0
                user-total-rmnight  = 0
                user-total-rbudget  = 0
            .

            IF show-breakdown THEN
            DO:
                CREATE slist.
                ASSIGN
                    slist.userinit = bediener.userinit
                    slist.bezeich  = bediener.userinit + " - " + bediener.username
                    slist.Yr       = -2
                    slist.mnth     = -2
                    slist.is-data  = NO
                .
            END.

            RUN create-list.
            RUN include-outlet-fnb.

            IF show-breakdown THEN
            DO:
                CREATE slist.
                ASSIGN
                    slist.userinit = bediener.userinit
                    slist.bezeich  = "T O T A L"
                    slist.Yr       = -2
                    slist.mnth     = -2
                    slist.lodg     = user-total-lodg    
                    slist.lbudget  = user-total-lbudget 
                    slist.fbrev    = user-total-fbrev   
                    slist.fbbudget = user-total-fbbudget
                    slist.otrev    = user-total-otrev   
                    slist.otbudget = user-total-otbudget
                    slist.rmnight  = user-total-rmnight 
                    slist.rbudget  = user-total-rbudget 
                    slist.is-data  = YES
                .

                CREATE slist.
                ASSIGN
                    slist.Yr       = -2
                    slist.mnth     = -2
                    slist.is-data  = NO
                .
            END.
        END.
    END.
    
    RUN count-ytd. /* Oscar (18/02/2025) - B89C44 - Seperate ytd calculation */
    RUN count-total. /* Oscar (18/02/2025) - B89C44 - Total calculation */
END.
ELSE
DO:
    FIND FIRST bediener WHERE bediener.userinit = usr-init NO-LOCK NO-ERROR. 
    RUN check-budget.
    IF its-ok THEN
    DO:
        RUN create-list.
        RUN include-outlet-fnb.
        RUN count-ytd. /* Oscar (18/02/2025) - B89C44 - Seperate ytd calculation */
    END.
    RUN count-total. /* Oscar (18/02/2025) - B89C44 - Total calculation */
END.


PROCEDURE check-budget: 
    DEFINE VARIABLE m1 AS INTEGER. 
    DEFINE VARIABLE m2 AS INTEGER. 
    DEFINE VARIABLE y1 AS INTEGER. 
    DEFINE VARIABLE y2 AS INTEGER. 
    DEFINE VARIABLE yy AS INTEGER. 
    DEFINE VARIABLE monat AS INTEGER. 
    DEFINE VARIABLE jahr AS INTEGER. 
    y1 = INTEGER(SUBSTR(from-date,3,4)). 
    y2 = INTEGER(SUBSTR(to-date,3,4)). 
    m1 = INTEGER(SUBSTR(from-date,1,2)). 
    /* m2 = INTEGER(SUBSTR(to-date,1,2)) + y2 - y1. */
    m2 = INTEGER(SUBSTR(to-date,1,2)) + (12 * (y2 - y1)).  /* modify logic to count month2 by Oscar (27 September 2024) - EAF061 */
    
    jahr = y1. 
    DO monat = m1 TO m2: 
        IF monat GT 12 THEN 
        DO: 
            monat = 1. 
            jahr = jahr + 1. 
    END. 
    FIND FIRST salesbud WHERE salesbud.bediener-nr = bediener.nr 
        AND salesbud.monat = monat AND salesbud.jahr = jahr 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE salesbud THEN 
    DO:
        CREATE salesbud.
        ASSIGN
            salesbud.bediener-nr = bediener.nr
            salesbud.monat       = monat
            salesbud.jahr        = jahr
        .
        FIND CURRENT salesbud NO-LOCK.
        /*
        hide MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("No Sales budget for period ",lvCAREA,"") + STRING(monat,"99") 
            "/" + STRING(jahr,"9999") 
            SKIP 
            translateExtended ("Calculation not possible",lvCAREA,"") 
        VIEW-AS ALERT-BOX INFORMATION. 
        its-ok = NO. 
        */      
        RETURN. 
    END. 

    /*gerald 300720*/
    FIND FIRST salestat WHERE salestat.bediener-nr = bediener.nr 
        AND salestat.monat = monat AND salestat.jahr = jahr 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE salestat THEN 
    DO:
        CREATE salestat.
        ASSIGN
            salestat.bediener-nr = bediener.nr
            salestat.monat       = monat
            salestat.jahr        = jahr
        .
        FIND CURRENT salesbud NO-LOCK.
        RETURN. 
    END. 
  END. 
END. 

PROCEDURE create-list:
    DEF VARIABLE do-it          AS LOGICAL NO-UNDO.
    DEF VARIABLE fdate          AS DATE    NO-UNDO.
    DEF VARIABLE fdate-1styear  AS DATE    NO-UNDO.
    DEF VARIABLE tdate          AS DATE    NO-UNDO.
    DEF VARIABLE loopi          AS DATE    NO-UNDO.

    /* DEF VARIABLE mtd-lodging AS DECIMAL NO-UNDO.
    DEF VARIABLE mtd-rmnight AS DECIMAL NO-UNDO. */
    
    DEF BUFFER stat-buff FOR salestat.
    DEF BUFFER bud-buff  FOR salesbud.
    DEF BUFFER bgenstat  FOR genstat.

    ASSIGN 
        fdate = DATE(INT(SUBSTR(from-date, 1,2)), 1, INT(SUBSTR(from-date, 3,4))).
    
    IF INT(SUBSTR(to-date, 1,2)) EQ 12 THEN
        tdate = DATE(1, 1, INT(SUBSTR(to-date, 3,4)) + 1) - 1.
    ELSE
        tdate = DATE(INT(SUBSTR(to-date, 1,2)) + 1, 1, INT(SUBSTR(to-date, 3,4))) - 1.
    

    DO loopi = fdate TO tdate:
        IF show-breakdown THEN
        DO:
            FIND FIRST slist WHERE slist.mnth EQ MONTH(loopi) 
                AND slist.yr EQ YEAR(loopi)
                AND slist.userinit EQ bediener.userinit NO-LOCK NO-ERROR.  
            IF NOT AVAILABLE slist THEN 
            DO:
                CREATE slist.
                ASSIGN
                    slist.userinit  = bediener.userinit
                    slist.yr        = YEAR(loopi)
                    slist.mnth      = MONTH(loopi)
                    slist.bezeich   = add-start-zero(MONTH(loopi), 2) + "/" + add-start-zero(YEAR(loopi), 4)
                    slist.is-data   = YES
                .
            END.
        END.
        ELSE
        DO:
            FIND FIRST slist WHERE slist.mnth EQ MONTH(loopi) 
                AND slist.yr EQ YEAR(loopi) NO-LOCK NO-ERROR.  
            IF NOT AVAILABLE slist THEN 
            DO:
                CREATE slist.
                ASSIGN
                    slist.userinit  = bediener.userinit
                    slist.yr        = YEAR(loopi)
                    slist.mnth      = MONTH(loopi)
                    slist.bezeich   = add-start-zero(MONTH(loopi), 2) + "/" + add-start-zero(YEAR(loopi), 4)
                    slist.is-data   = YES
                .
            END.
        END.
    END.
        
    ASSIGN fdate-1styear = DATE(1,1, INT(SUBSTR(from-date, 3,4))).
        
    FOR EACH genstat WHERE genstat.datum GE fdate-1styear
        AND genstat.datum LE tdate
        AND genstat.zinr NE "" 
        AND genstat.res-logic[2] EQ YES
        USE-INDEX date_ix NO-LOCK,
        FIRST guest WHERE guest.gastnr = genstat.gastnr 
        NO-LOCK BY genstat.datum BY guest.name BY guest.gastnr:

            ASSIGN do-it = YES.
            IF genstat.zipreis = 0 THEN DO:
                IF (genstat.gratis GT 0) THEN do-it = NO.
                IF (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis = 0)
                    AND genstat.resstatus NE 13 THEN do-it = NO.
            END.
        
            IF do-it THEN 
            DO:
                IF guest.phonetik3 EQ TRIM(bediener.userinit) THEN 
                DO: 
                    IF show-breakdown THEN
                    DO:
                        FIND FIRST slist WHERE slist.mnth EQ MONTH(genstat.datum) 
                            AND slist.yr EQ YEAR(genstat.datum) 
                            AND slist.userinit EQ bediener.userinit
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE slist THEN 
                        DO:
                            IF genstat.resstatus NE 13 THEN
                            DO:
                                ASSIGN
                                    slist.lodg        = slist.lodg + genstat.logis
                                    slist.rmnight     = slist.rmnight + 1

                                    user-total-lodg    = user-total-lodg    + genstat.logis
                                    user-total-rmnight = user-total-rmnight + 1
                                .
                            END.
                        END.   
                    END.
                    ELSE
                    DO:
                        FIND FIRST slist WHERE slist.mnth EQ MONTH(genstat.datum) 
                            AND slist.yr EQ YEAR(genstat.datum) 
                            NO-LOCK NO-ERROR.
                        IF AVAILABLE slist THEN 
                        DO:
                            IF genstat.resstatus NE 13 THEN
                            DO:
                                ASSIGN
                                    slist.lodg        = slist.lodg + genstat.logis
                                    slist.rmnight     = slist.rmnight + 1

                                    user-total-lodg    = user-total-lodg    + genstat.logis
                                    user-total-rmnight = user-total-rmnight + 1
                                .
                            END.
                        END.   
                    END.
                END.
            END.
    END.

    FOR EACH salestat WHERE salestat.bediener-nr = bediener.nr 
        AND ((salestat.jahr GT YEAR(fdate-1styear) AND salestat.monat GE 1) 
        OR (salestat.jahr EQ YEAR(fdate-1styear) AND salestat.monat GE MONTH(fdate-1styear))) 
        AND ((salestat.jahr LT INTEGER(SUBSTR(to-date,3,4)) AND salestat.monat GE 1) 
        OR (salestat.jahr EQ INTEGER(SUBSTR(to-date,3,4)) AND salestat.monat LE INTEGER(SUBSTR(to-date,1,2)))) 
        NO-LOCK,
        FIRST salesbud WHERE salesbud.bediener-nr = salestat.bediener-nr 
        AND salesbud.monat = salestat.monat AND salesbud.jahr = salestat.jahr 
        NO-LOCK BY salestat.jahr BY salestat.monat:

        IF show-breakdown THEN
        DO:
            FIND FIRST slist WHERE (slist.mnth EQ salestat.monat) 
                AND (slist.Yr EQ salestat.jahr)
                AND slist.userinit EQ bediener.userinit NO-ERROR.
            IF AVAILABLE slist THEN
            DO:
                /* Dzikri 1A9361 - repair program */
                ASSIGN      
                    slist.otrev        = slist.otrev    + salestat.sonst-umsatz
                    slist.otbudget     = slist.otbudget + salesbud.sonst-umsatz
                    slist.fbrev        = slist.fbrev    + salestat.f-b-umsatz
                    slist.fbbudget     = slist.fbbudget + salesbud.f-b-umsatz  
                    slist.rbudget      = slist.rbudget  + salesbud.room-nights
                    slist.lbudget      = slist.lbudget  + salesbud.argtumsatz


                    user-total-otrev    = user-total-otrev    + salestat.sonst-umsatz
                    user-total-otbudget = user-total-otbudget + salesbud.sonst-umsatz
                    user-total-fbrev    = user-total-fbrev    + salestat.f-b-umsatz
                    user-total-fbbudget = user-total-fbbudget + salesbud.f-b-umsatz  
                    user-total-lbudget  = user-total-lbudget  + salesbud.room-nights
                    user-total-rbudget  = user-total-rbudget  + salesbud.argtumsatz
                .
            END.
        END.
        ELSE
        DO:
            FIND FIRST slist WHERE (slist.mnth EQ salestat.monat) 
                AND (slist.Yr EQ salestat.jahr) NO-ERROR.
            IF AVAILABLE slist THEN
            DO:
                /* Dzikri 1A9361 - repair program */
                ASSIGN      
                    slist.otrev        = slist.otrev    + salestat.sonst-umsatz
                    slist.otbudget     = slist.otbudget + salesbud.sonst-umsatz
                    slist.fbrev        = slist.fbrev    + salestat.f-b-umsatz
                    slist.fbbudget     = slist.fbbudget + salesbud.f-b-umsatz  
                    slist.rbudget      = slist.rbudget  + salesbud.room-nights
                    slist.lbudget      = slist.lbudget  + salesbud.argtumsatz


                    user-total-otrev    = user-total-otrev    + salestat.sonst-umsatz
                    user-total-otbudget = user-total-otbudget + salesbud.sonst-umsatz
                    user-total-fbrev    = user-total-fbrev    + salestat.f-b-umsatz
                    user-total-fbbudget = user-total-fbbudget + salesbud.f-b-umsatz  
                    user-total-lbudget  = user-total-lbudget  + salesbud.room-nights
                    user-total-rbudget  = user-total-rbudget  + salesbud.argtumsatz
                .
                /* Dzikri 1A9361 - END */
                
                /* Oscar - A7E967 - change calculation method to reduce loop inside loop*/
                /* FOR EACH stat-buff WHERE stat-buff.bediener-nr = bediener.nr 
                    AND stat-buff.jahr = salestat.jahr AND stat-buff.monat LE salestat.monat NO-LOCK, 
                    FIRST bud-buff WHERE bud-buff.bediener-nr = stat-buff.bediener-nr
                    AND bud-buff.monat = stat-buff.monat AND bud-buff.jahr = stat-buff.jahr NO-LOCK 
                    BY stat-buff.jahr BY stat-buff.monat:
                    
                    ASSIGN 
                        slist.ytd-lbudget  = slist.ytd-lbudget    + bud-buff.argtumsatz
                        slist.ytd-otrev    = slist.ytd-otrev      + stat-buff.sonst-umsatz
                        slist.ytd-otbudget = slist.ytd-otbudget   + bud-buff.sonst-umsatz
                        slist.ytd-fbrev    = slist.ytd-fbrev      + stat-buff.f-b-umsatz
                        slist.ytd-fbbudget = slist.ytd-fbbudget   + bud-buff.f-b-umsatz
                        slist.ytd-rbudget  = slist.ytd-rbudget    + bud-buff.room-nights.
                    
                END. */
                    
                /* ASSIGN
                    slist.ytd-fbproz       = slist.ytd-fbrev / slist.ytd-fbbudget * 100
                    slist.ytd-otproz       = slist.ytd-otrev / slist.ytd-otbudget * 100.
                    
                    
                IF slist.otproz = ? THEN slist.otproz = 0.00.
                IF slist.fbproz = ? THEN slist.fbproz = 0.00.
                IF slist.ytd-fbproz = ? THEN slist.ytd-fbproz = 0.00.
                IF slist.ytd-otproz = ? THEN slist.ytd-otproz = 0.00. */
            END.
        END.
    END.
END.

/* Oscar (18/02/2025) - B89C44 - Seperate ytd calculation */
PROCEDURE count-ytd:
    DEFINE VARIABLE year-tmp        AS INTEGER NO-UNDO.
    DEFINE VARIABLE user-tmp        AS CHARACTER NO-UNDO.
    
    DEFINE VARIABLE ytd-lodging     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-rmnight     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-fnb         AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-other       AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-bud-lodg    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-bud-rmnight AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-bud-fnb     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE ytd-bud-ot      AS DECIMAL NO-UNDO.

    DEFINE VARIABLE usr-tot-ytd-lodging     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-rmnight     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-fnb         AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-other       AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-bud-lodg    AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-bud-rmnight AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-bud-fnb     AS DECIMAL NO-UNDO.
    DEFINE VARIABLE usr-tot-ytd-bud-ot      AS DECIMAL NO-UNDO.

    DEFINE BUFFER sbuff FOR slist.

    FOR EACH slist WHERE slist.Yr GE 0
        BY slist.userinit BY slist.Yr BY slist.mnth:

        IF user-tmp NE slist.userinit THEN
        DO:
            FIND FIRST sbuff WHERE sbuff.userinit EQ user-tmp
                AND sbuff.bezeich EQ "T O T A L" NO-ERROR.
            IF AVAILABLE sbuff THEN
            DO:
                ASSIGN
                    sbuff.ytd-lodg     = usr-tot-ytd-lodging
                    sbuff.ytd-rmnight  = usr-tot-ytd-rmnight
                    sbuff.ytd-otrev    = usr-tot-ytd-other
                    sbuff.ytd-fbrev    = usr-tot-ytd-fnb
                    sbuff.ytd-lbudget  = usr-tot-ytd-bud-lodg   
                    sbuff.ytd-rbudget  = usr-tot-ytd-bud-rmnight
                    sbuff.ytd-otbudget = usr-tot-ytd-bud-ot   
                    sbuff.ytd-fbbudget = usr-tot-ytd-bud-fnb  
                .

                sbuff.ytd-lproz  = sbuff.ytd-lodg / sbuff.ytd-lbudget * 100.
                sbuff.ytd-rmproz = sbuff.ytd-rmnight / sbuff.ytd-rbudget * 100.
                sbuff.ytd-otproz = sbuff.ytd-otrev / sbuff.ytd-otbudget * 100.
                sbuff.ytd-fbproz = sbuff.ytd-fbrev / sbuff.ytd-fbbudget * 100.

                IF sbuff.ytd-lproz  = ? THEN sbuff.ytd-lproz  = 0.00.
                IF sbuff.ytd-rmproz = ? THEN sbuff.ytd-rmproz = 0.00.
                IF sbuff.ytd-otproz = ? THEN sbuff.ytd-otproz = 0.00.
                IF sbuff.ytd-fbproz = ? THEN sbuff.ytd-fbproz = 0.00.
            END.

            ASSIGN
                usr-tot-ytd-lodging     = 0
                usr-tot-ytd-rmnight     = 0
                usr-tot-ytd-fnb         = 0
                usr-tot-ytd-other       = 0
                usr-tot-ytd-bud-lodg    = 0
                usr-tot-ytd-bud-rmnight = 0
                usr-tot-ytd-bud-fnb     = 0
                usr-tot-ytd-bud-ot      = 0
            .
        END.

        IF user-tmp NE slist.userinit
            OR year-tmp NE slist.Yr THEN
        DO:
            ASSIGN
                ytd-lodging     = 0
                ytd-rmnight     = 0
                ytd-fnb         = 0
                ytd-other       = 0
                ytd-bud-lodg    = 0
                ytd-bud-rmnight = 0
                ytd-bud-fnb     = 0
                ytd-bud-ot      = 0
            .

            user-tmp = slist.userinit.
            year-tmp = slist.Yr.
        END.

        ASSIGN 
            slist.lproz      = slist.lodg / slist.lbudget * 100
            slist.rmproz     = slist.rmnight / slist.rbudget * 100
            slist.otproz     = slist.otrev / slist.otbudget * 100
            slist.fbproz     = slist.fbrev / slist.fbbudget * 100
        .

        IF slist.lproz = ? THEN slist.lproz = 0.00.
        IF slist.rmproz = ? THEN slist.rmproz = 0.00.
        IF slist.otproz = ? THEN slist.otproz = 0.00.
        IF slist.fbproz = ? THEN slist.fbproz = 0.00.
        
        ASSIGN
            ytd-lodging     = ytd-lodging     + slist.lodg
            ytd-rmnight     = ytd-rmnight     + slist.rmnight
            ytd-fnb         = ytd-fnb         + slist.fbrev
            ytd-other       = ytd-other       + slist.otrev
            ytd-bud-lodg    = ytd-bud-lodg    + slist.lbudget
            ytd-bud-rmnight = ytd-bud-rmnight + slist.rbudget
            ytd-bud-fnb     = ytd-bud-fnb     + slist.fbbudget
            ytd-bud-ot      = ytd-bud-ot      + slist.otbudget           
        
            slist.ytd-lodg     = ytd-lodging
            slist.ytd-rmnight  = ytd-rmnight
            slist.ytd-otrev    = ytd-other
            slist.ytd-fbrev    = ytd-fnb
            slist.ytd-lbudget  = ytd-bud-lodg   
            slist.ytd-rbudget  = ytd-bud-rmnight
            slist.ytd-otbudget = ytd-bud-ot    
            slist.ytd-fbbudget = ytd-bud-fnb     

            slist.ytd-lproz  = slist.ytd-lodg / slist.ytd-lbudget * 100
            slist.ytd-rmproz = slist.ytd-rmnight / slist.ytd-rbudget * 100
            slist.ytd-otproz = slist.ytd-otrev / slist.ytd-otbudget * 100
            slist.ytd-fbproz = slist.ytd-fbrev / slist.ytd-fbbudget * 100
        .

        IF slist.lodg    EQ 0 THEN slist.ytd-lodg    = 0.
        IF slist.rmnight EQ 0 THEN slist.ytd-rmnight = 0.
        IF slist.fbrev   EQ 0 THEN slist.ytd-fbrev   = 0.
        IF slist.otrev   EQ 0 THEN slist.ytd-otrev   = 0.

        ASSIGN
            usr-tot-ytd-lodging     = usr-tot-ytd-lodging     + slist.ytd-lodg     
            usr-tot-ytd-rmnight     = usr-tot-ytd-rmnight     + slist.ytd-rmnight  
            usr-tot-ytd-other       = usr-tot-ytd-other       + slist.ytd-otrev    
            usr-tot-ytd-fnb         = usr-tot-ytd-fnb         + slist.ytd-fbrev    
            usr-tot-ytd-bud-lodg    = usr-tot-ytd-bud-lodg    + slist.ytd-lbudget  
            usr-tot-ytd-bud-rmnight = usr-tot-ytd-bud-rmnight + slist.ytd-rbudget  
            usr-tot-ytd-bud-ot      = usr-tot-ytd-bud-ot      + slist.ytd-otbudget 
            usr-tot-ytd-bud-fnb     = usr-tot-ytd-bud-fnb     + slist.ytd-fbbudget 
        .
    
        IF slist.ytd-lproz  = ? THEN slist.ytd-lproz  = 0.00.
        IF slist.ytd-rmproz = ? THEN slist.ytd-rmproz = 0.00.
        IF slist.ytd-otproz = ? THEN slist.ytd-otproz = 0.00.
        IF slist.ytd-fbproz = ? THEN slist.ytd-fbproz = 0.00.
    END.
END.

/* Oscar (18/02/2025) - B89C44 - Total calculation */
PROCEDURE count-total:
    DEFINE BUFFER buff-slist FOR slist.

    CREATE slist.
    ASSIGN
        slist.mnth    = -1
        slist.Yr      = -1
        slist.is-data = YES
    .
    IF show-breakdown THEN
    DO:
        slist.bezeich = "GRAND TOTAL".
    END.
    ELSE
    DO:
        slist.bezeich = "T O T A L".
    END.

    FOR EACH buff-slist WHERE buff-slist.Yr GE 0
        AND buff-slist.mnth GE 0 NO-LOCK:
            ASSIGN
                slist.lodg         = slist.lodg         + buff-slist.lodg        
                slist.lbudget      = slist.lbudget      + buff-slist.lbudget     
                slist.fbrev        = slist.fbrev        + buff-slist.fbrev       
                slist.fbbudget     = slist.fbbudget     + buff-slist.fbbudget    
                slist.otrev        = slist.otrev        + buff-slist.otrev       
                slist.otbudget     = slist.otbudget     + buff-slist.otbudget    
                slist.rmnight      = slist.rmnight      + buff-slist.rmnight     
                slist.rbudget      = slist.rbudget      + buff-slist.rbudget     
                slist.ytd-lodg     = slist.ytd-lodg     + buff-slist.ytd-lodg    
                slist.ytd-lbudget  = slist.ytd-lbudget  + buff-slist.ytd-lbudget 
                slist.ytd-fbrev    = slist.ytd-fbrev    + buff-slist.ytd-fbrev   
                slist.ytd-fbbudget = slist.ytd-fbbudget + buff-slist.ytd-fbbudget
                slist.ytd-rmnight  = slist.ytd-rmnight  + buff-slist.ytd-rmnight 
                slist.ytd-rbudget  = slist.ytd-rbudget  + buff-slist.ytd-rbudget 
                slist.ytd-otrev    = slist.ytd-otrev    + buff-slist.ytd-otrev   
                slist.ytd-otbudget = slist.ytd-otbudget + buff-slist.ytd-otbudget
            .
    END.
    
    ASSIGN
        slist.lproz        = slist.lodg / slist.lbudget * 100
        slist.rmproz       = slist.rmnight / slist.rbudget * 100
        slist.fbproz       = slist.fbrev / slist.fbbudget * 100
        slist.otproz       = slist.otrev / slist.otbudget * 100 

        slist.ytd-lproz    = slist.ytd-lodg / slist.ytd-lbudget * 100
        slist.ytd-rmproz   = slist.ytd-rmnight / slist.ytd-rbudget * 100
        slist.ytd-fbproz   = slist.ytd-fbrev / slist.ytd-fbbudget * 100
        slist.ytd-otproz   = slist.ytd-otrev / slist.ytd-otbudget * 100 
    .

    IF slist.lproz = ? THEN slist.lproz = 0.00.
    IF slist.rmproz = ? THEN slist.rmproz = 0.00.
    IF slist.otproz = ? THEN slist.otproz = 0.00.
    IF slist.fbproz = ? THEN slist.fbproz = 0.00.
    IF slist.ytd-lproz = ? THEN slist.ytd-lproz = 0.00.
    IF slist.ytd-rmproz = ? THEN slist.ytd-rmproz = 0.00.
    IF slist.ytd-otproz = ? THEN slist.ytd-otproz = 0.00.
    IF slist.ytd-fbproz = ? THEN slist.ytd-fbproz = 0.00.
END.

/* Oscar (24/01/25) - A7E967 - Add function to include Outlet transaction with Guest that have Sales ID */
PROCEDURE include-outlet-fnb:
    DEFINE VARIABLE from-date  AS DATE NO-UNDO.
    DEFINE VARIABLE to-date    AS DATE NO-UNDO.
    DEFINE VARIABLE temp-date  AS DATE NO-UNDO.
    DEFINE VARIABLE count-loop AS INTEGER INITIAL 0.

    IF show-breakdown THEN
    DO:
        FOR EACH slist WHERE slist.userinit EQ bediener.userinit
            AND slist.Yr GE 0
            BY slist.Yr BY slist.mnth:

            from-date = DATE(slist.mnth, 1, slist.Yr).
            IF slist.mnth EQ 12 THEN
                to-date = DATE(1, 1, slist.Yr + 1) - 1.
            ELSE
                to-date = DATE(slist.mnth + 1, 1, slist.Yr) - 1.

            FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE from-date
                AND h-bill-line.bill-datum LE to-date
                AND h-bill-line.artnr NE 0 NO-LOCK,
                FIRST h-bill WHERE h-bill.rechnr EQ h-bill-line.rechnr
                AND h-bill.departement EQ h-bill-line.departement
                AND h-bill.flag EQ 1 NO-LOCK,
                FIRST guest WHERE guest.gastnr EQ h-bill.resnr
                AND guest.phonetik3 EQ TRIM(bediener.userinit) NO-LOCK,
                FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr 
                AND h-artikel.departement EQ h-bill-line.departement NO-LOCK,
                FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                AND artikel.departement EQ h-artikel.departement AND artikel.artart EQ 0 NO-LOCK
                BY h-bill-line.bill-datum:
                    
                IF artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 6 THEN
                DO:
                    slist.fbrev      = slist.fbrev + h-bill-line.betrag.
                    user-total-fbrev = user-total-fbrev + h-bill-line.betrag.
                END.
                ELSE IF artikel.umsatzart EQ 4 THEN
                DO:
                    slist.otrev      = slist.otrev + h-bill-line.betrag.
                    user-total-otrev = user-total-otrev + h-bill-line.betrag.
                END.
            END.
        END.
    END.
    ELSE
    DO:
        FOR EACH slist WHERE slist.Yr GE 0
            BY slist.Yr BY slist.mnth:

            from-date = DATE(slist.mnth, 1, slist.Yr).
            IF slist.mnth EQ 12 THEN
                to-date = DATE(1, 1, slist.Yr + 1) - 1.
            ELSE
                to-date = DATE(slist.mnth + 1, 1, slist.Yr) - 1.

            FOR EACH h-bill-line WHERE h-bill-line.bill-datum GE from-date
                AND h-bill-line.bill-datum LE to-date
                AND h-bill-line.artnr NE 0 NO-LOCK,
                FIRST h-bill WHERE h-bill.rechnr EQ h-bill-line.rechnr
                AND h-bill.departement EQ h-bill-line.departement
                AND h-bill.flag EQ 1 NO-LOCK,
                FIRST guest WHERE guest.gastnr EQ h-bill.resnr
                AND guest.phonetik3 EQ TRIM(bediener.userinit) NO-LOCK,
                FIRST h-artikel WHERE h-artikel.artnr EQ h-bill-line.artnr 
                AND h-artikel.departement EQ h-bill-line.departement NO-LOCK,
                FIRST artikel WHERE artikel.artnr EQ h-artikel.artnrfront
                AND artikel.departement EQ h-artikel.departement AND artikel.artart EQ 0 NO-LOCK
                BY h-bill-line.bill-datum:
                    
                IF artikel.umsatzart EQ 3 OR artikel.umsatzart EQ 5 OR artikel.umsatzart EQ 6 THEN
                DO:
                    slist.fbrev      = slist.fbrev + h-bill-line.betrag.
                    user-total-fbrev = user-total-fbrev + h-bill-line.betrag.
                END.
                ELSE IF artikel.umsatzart EQ 4 THEN
                DO:
                    slist.otrev      = slist.otrev + h-bill-line.betrag.
                    user-total-otrev = user-total-otrev + h-bill-line.betrag.
                END.
            END.
        END.
    END.
    
END.
