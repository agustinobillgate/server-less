DEF TEMP-TABLE t-parameters LIKE parameters.
DEFINE TEMP-TABLE w1 
    FIELD nr          AS INTEGER 
    FIELD varname     AS CHAR 
    FIELD main-code   AS INTEGER   /* eg. 805 FOR AVAILABLE room */ 
    FIELD s-artnr     AS CHAR
    FIELD artnr       AS INTEGER 
    FIELD dept        AS INTEGER 
    FIELD grpflag     AS INTEGER INITIAL 0 
    FIELD done        AS LOGICAL INITIAL NO 
    FIELD bezeich     AS CHAR 
    FIELD int-flag    AS LOGICAL INITIAL NO 
    
    FIELD tday        AS DECIMAL INITIAL 0 
    FIELD tday-serv   AS DECIMAL INITIAL 0 
    FIELD tday-tax    AS DECIMAL INITIAL 0 
    FIELD mtd-serv    AS DECIMAL INITIAL 0 
    FIELD mtd-tax     AS DECIMAL INITIAL 0 
    FIELD ytd-serv    AS DECIMAL INITIAL 0 
    FIELD ytd-tax     AS DECIMAL INITIAL 0 
    FIELD yesterday   AS DECIMAL INITIAL 0 
    FIELD saldo       AS DECIMAL INITIAL 0 
    FIELD lastmon     AS DECIMAL INITIAL 0
    FIELD pmtd-serv   AS DECIMAL INITIAL 0 
    FIELD pmtd-tax    AS DECIMAL INITIAL 0 
    FIELD lmtd-serv   AS DECIMAL INITIAL 0 
    FIELD lmtd-tax    AS DECIMAL INITIAL 0 
    FIELD lastyr      AS DECIMAL INITIAL 0 
    FIELD lytoday     AS DECIMAL INITIAL 0 
    FIELD ytd-saldo   AS DECIMAL INITIAL 0 
    FIELD lytd-saldo  AS DECIMAL INITIAL 0 
    
    FIELD year-saldo  AS DECIMAL EXTENT 12 INITIAL 
    [0,0,0,0,0,0,0,0,0,0,0,0] 
    
    FIELD mon-saldo   AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]
    
    FIELD mon-budget   AS DECIMAL EXTENT 31 INITIAL 
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]
    
    FIELD mon-lmtd     AS DECIMAL EXTENT 31 INITIAL 
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0]
    
    FIELD tbudget     AS DECIMAL INITIAL 0 
    FIELD budget      AS DECIMAL INITIAL 0 
    FIELD lm-budget   AS DECIMAL INITIAL 0 
    FIELD lm-today    AS DECIMAL INITIAL 0 
    FIELD lm-today-serv  AS DECIMAL INITIAL 0 
    FIELD lm-today-tax   AS DECIMAL INITIAL 0 
    FIELD lm-mtd      AS DECIMAL INITIAL 0 
    FIELD lm-ytd      AS DECIMAL INITIAL 0 
    FIELD ly-budget   AS DECIMAL INITIAL 0 
    FIELD ny-budget   AS DECIMAL INITIAL 0   /*FT*/
    FIELD ytd-budget  AS DECIMAL INITIAL 0 
    FIELD nytd-budget AS DECIMAL INITIAL 0  /*FT*/
    FIELD nmtd-budget AS DECIMAL INITIAL 0  /*FT*/
    FIELD lytd-budget AS DECIMAL INITIAL 0
.


DEFINE INPUT  PARAMETER foreign-flag AS LOGICAL.
DEFINE INPUT  PARAMETER from-date AS DATE.
DEFINE INPUT  PARAMETER to-date   AS DATE.
DEFINE INPUT  PARAMETER TABLE FOR t-parameters.
DEFINE OUTPUT PARAMETER TABLE FOR w1.  

DEFINE VARIABLE prev-str      AS CHARACTER.
DEFINE VARIABLE done-segment  AS LOGICAL INIT NO.
DEFINE VARIABLE datum1        AS DATE.
DEFINE VARIABLE jan1          AS DATE.
DEFINE VARIABLE Ljan1         AS DATE.
DEFINE VARIABLE Lfrom-date    AS DATE.
DEFINE VARIABLE Lto-date      AS DATE.
DEFINE VARIABLE do-it         AS LOGICAL INIT YES.

DEFINE BUFFER buff-exrate FOR exrate.

DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE serv            AS DECIMAL. 
DEFINE VARIABLE vat             AS DECIMAL. 
DEFINE VARIABLE fact            AS DECIMAL. 
DEFINE VARIABLE n-betrag        AS DECIMAL.
DEFINE VARIABLE frate           AS DECIMAL INIT 1.
DEFINE VARIABLE price-decimal   AS INTEGER.

IF (month(to-date) NE 2) OR (day(to-date) NE 29) THEN 
    Lto-date = DATE(month(to-date), day(to-date), year(to-date) - 1). 
ELSE Lto-date = DATE(month(to-date), 28, year(to-date) - 1). 
    
ASSIGN
    jan1        = DATE(1,1,YEAR(to-date))
    Ljan1       = DATE(1,1,YEAR(to-date) - 1)
    Lfrom-date  = DATE(MONTH(to-date),1,YEAR(to-date) - 1).

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

FIND FIRST t-parameters WHERE NUM-ENTRIES(t-parameters.varname,"-") = 3
    AND ENTRY(3,t-parameters.varname,"-") = "comboREV" NO-LOCK NO-ERROR.
IF AVAILABLE t-parameters THEN RUN fill-revenue.

FIND FIRST t-parameters WHERE (t-parameters.vstring MATCHES "*segmrev*" 
                               OR t-parameters.vstring MATCHES "*segmpers*" 
                               OR t-parameters.vstring MATCHES "*segmroom*")
    AND NUM-ENTRIES(t-parameters.varname,"-") = 3
    AND ENTRY(3,t-parameters.varname,"-") = "comboFO" NO-LOCK NO-ERROR.
IF AVAILABLE t-parameters THEN RUN fill-segment.

PROCEDURE fill-revenue:
    DEFINE BUFFER s-param FOR t-parameters.
    DEFINE VARIABLE prev-param AS CHAR INIT "".
    DEFINE VARIABLE ytd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE lytd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE lmtd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE ytd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mtd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mm AS INT.
    
    FOR EACH s-param WHERE NUM-ENTRIES(s-param.vstring,":") = 1 
        AND NUM-ENTRIES(s-param.varname,"-") = 3
        AND ENTRY(3,s-param.varname,"-") = "comboREV" NO-LOCK BY s-param.varname:
        IF prev-param NE s-param.varname THEN
        DO:
            prev-param = s-param.varname.
            FIND FIRST w1 WHERE w1.nr = 4 AND w1.s-artnr = s-param.vstring NO-LOCK NO-ERROR.
            IF NOT AVAILABLE w1 THEN
            DO:
                CREATE w1.
                ASSIGN
                    w1.nr = 4
                    w1.s-artnr = s-param.vstring.
            END.

            IF s-param.vtype = 24 THEN
                ytd-flag = YES.
            IF s-param.vtype = 84 THEN
                mtd-budget-flag = YES.
            IF s-param.vtype = 85 THEN
                ytd-budget-flag = YES.
            IF s-param.vtype = 86 THEN
                lmtd-flag = YES.
            IF s-param.vtype = 87 THEN
                lytd-flag = YES.
        END.                    
    END.

    FOR EACH w1 WHERE w1.nr = 4 NO-LOCK BY w1.s-artnr:
        FIND FIRST artikel WHERE artikel.artnr = INT(SUBSTR(w1.s-artnr,3)) 
            AND artikel.departement = INT(SUBSTR(w1.s-artnr,1,2)) NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
        DO:
            IF ytd-flag THEN datum1 = jan1.
            ELSE datum1 = from-date.
            mm = MONTH(to-date). 

            FOR EACH umsatz WHERE umsatz.datum GE datum1
                AND umsatz.datum LE to-date 
                AND umsatz.artnr = artikel.artnr
                AND umsatz.departement = artikel.departement NO-LOCK:

                ASSIGN 
                    serv = 0
                    vat  = 0.

                RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                    artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                fact = 1.00 + serv + vat.
                n-betrag = 0.
                IF foreign-flag THEN 
                DO: 
                    RUN find-exrate(curr-date). 
                    IF AVAILABLE buff-exrate THEN frate = buff-exrate.betrag. 
                END. 
                n-betrag = umsatz.betrag / (fact * frate).
                n-betrag = ROUND(n-betrag, 2).

                IF umsatz.datum = to-date THEN
                    w1.tday = w1.tday + n-betrag.
                IF MONTH(umsatz.datum) = mm THEN
                    w1.saldo = w1.saldo + n-betrag.

                w1.ytd-saldo = w1.ytd-saldo + n-betrag.
            END.

            IF lmtd-flag OR lytd-flag THEN
            DO:
                IF lytd-flag THEN datum1 = Ljan1. 
                ELSE datum1 = Lfrom-date.
                mm = MONTH(Lto-date).
                
                FOR EACH umsatz WHERE umsatz.datum GE datum1
                    AND umsatz.datum LE Lto-date
                    AND umsatz.artnr = artikel.artnr
                    AND umsatz.departement = artikel.departement NO-LOCK:
    
                    ASSIGN 
                        serv = 0
                        vat  = 0.
    
                    RUN calc-servvat.p(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service-code, 
                        artikel.mwst-code, OUTPUT serv, OUTPUT vat).
                    fact = 1.00 + serv + vat.
                    n-betrag = 0.
                    IF foreign-flag THEN 
                    DO: 
                        RUN find-exrate(curr-date). 
                        IF AVAILABLE buff-exrate THEN frate = buff-exrate.betrag. 
                    END. 
                    n-betrag = umsatz.betrag / (fact * frate).
                    n-betrag = ROUND(n-betrag, 2).
                    
                    IF MONTH(umsatz.datum) = mm THEN
                        w1.lastyr = w1.lastyr + n-betrag.
    
                    w1.lytd-saldo = w1.lytd-saldo + n-betrag.
                END.
            END.  

            IF mtd-budget-flag OR ytd-budget-flag THEN
            DO:
                IF ytd-budget-flag THEN datum1 = jan1.
                ELSE datum1 = from-date.
                mm = MONTH(to-date).

                FOR EACH budget WHERE budget.artnr = artikel.artnr 
                    AND budget.departement = artikel.departement
                    AND budget.datum GE datum1
                    AND budget.datum LE to-date NO-LOCK:

                    IF budget.datum = to-date THEN
                        w1.tbudget = w1.tbudget + budget.betrag.
                    IF MONTH(budget.datum) = mm THEN
                        w1.budget = w1.budget + budget.betrag.
                    w1.ytd-budget = w1.ytd-budget + budget.betrag.
                END.
            END.    
        END.    
    END.        
END.

PROCEDURE fill-segment:
    DEFINE BUFFER s-param FOR t-parameters.
    DEFINE VARIABLE prev-param AS CHAR.
    DEFINE VARIABLE ytd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE lytd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE lmtd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE ytd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mtd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE nr AS INT INIT 0.
    DEFINE VARIABLE segm AS INT INIT 0.
    DEFINE VARIABLE mm AS INT.
    DEFINE VARIABLE prev-segm AS INT.

    DEFINE BUFFER w-rev  FOR w1.
    DEFINE BUFFER w-pers FOR w1.
    DEFINE BUFFER w-room FOR w1.
    
    FOR EACH s-param WHERE NUM-ENTRIES(s-param.vstring,":") = 1 
        AND NUM-ENTRIES(s-param.varname,"-") = 3
        AND ENTRY(3,s-param.varname,"-") = "comboFO"
        AND SUBSTR(s-param.vstring,1,4) = "segm" NO-LOCK BY s-param.varname:
        IF prev-param NE s-param.varname THEN
        DO:
            prev-param = s-param.varname.

            IF ENTRY(1,s-param.vstring,"-") = "segmrev" THEN
                nr = 1.
            ELSE IF ENTRY(1,s-param.vstring,"-") = "segmpers" THEN
                nr = 2.
            ELSE IF ENTRY(1,s-param.vstring,"-") = "segmroom" THEN
                nr = 3.

            IF NUM-ENTRIES(s-param.vstring,"-") GT 1 THEN
                segm = INT(ENTRY(2,s-param.vstring,"-")).

            FIND FIRST w1 WHERE w1.nr = nr AND w1.artnr = segm NO-LOCK NO-ERROR.
            IF NOT AVAILABLE w1 THEN
            DO:
                CREATE w1.
                ASSIGN
                    w1.nr = nr
                    w1.artnr = segm.
            END.

            IF s-param.vtype = 24 THEN
                ytd-flag = YES.
            IF s-param.vtype = 84 THEN
                mtd-budget-flag = YES.
            IF s-param.vtype = 85 THEN
                ytd-budget-flag = YES.
            IF s-param.vtype = 86 THEN
                lmtd-flag = YES.
            IF s-param.vtype = 87 THEN
                lytd-flag = YES.
        END.                    
    END.

    IF ytd-flag THEN datum1 = jan1.
    ELSE datum1 = from-date.
    mm = MONTH(to-date).    
    FOR EACH genstat WHERE genstat.datum GE datum1 
        AND genstat.datum LE to-date 
        AND genstat.resstatus NE 13 
        /*AND genstat.gratis EQ 0 */
        AND genstat.segmentcode NE 0 
        AND genstat.nationnr NE 0
        AND genstat.zinr NE ""
        AND genstat.res-logic[2] NO-LOCK BY genstat.segmentcode:

        IF prev-segm NE genstat.segmentcode THEN
        DO:
            prev-segm = genstat.segmentcode.
            FIND FIRST w-rev WHERE w-rev.nr = 1 AND w-rev.artnr = genstat.segmentcode NO-LOCK NO-ERROR.
            FIND FIRST w-pers WHERE w-pers.nr = 2 AND w-pers.artnr = genstat.segmentcode NO-LOCK NO-ERROR.
            FIND FIRST w-room WHERE w-room.nr = 3 AND w-room.artnr = genstat.segmentcode NO-LOCK NO-ERROR.
        END.

        IF genstat.datum = to-date THEN
        DO:
            IF AVAILABLE w-rev THEN
                w-rev.tday = w-rev.tday + genstat.logis.
            IF AVAILABLE w-pers THEN
                w-pers.tday = w-pers.tday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
            IF AVAILABLE w-room THEN
                w-room.tday = w-room.tday + 1.
        END.

        IF MONTH(genstat.datum) = mm THEN
        DO:
            IF AVAILABLE w-rev THEN
                w-rev.saldo = w-rev.saldo + genstat.logis.
            IF AVAILABLE w-pers THEN
                w-pers.saldo = w-pers.saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
            IF AVAILABLE w-room THEN
                w-room.saldo = w-room.saldo + 1.
        END.

        IF AVAILABLE w-rev THEN
            w-rev.ytd-saldo = w-rev.ytd-saldo + genstat.logis.
        IF AVAILABLE w-pers THEN
            w-pers.ytd-saldo = w-pers.ytd-saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
        IF AVAILABLE w-room THEN
            w-room.ytd-saldo = w-room.ytd-saldo + 1.
    END.

    IF lmtd-flag OR lytd-flag THEN
    DO:
        IF lytd-flag THEN datum1 = Ljan1. 
        ELSE datum1 = Lfrom-date.
        mm = MONTH(Lto-date).
        prev-segm = 0.

        FOR EACH genstat WHERE genstat.datum GE datum1 
            AND genstat.datum LE Lto-date 
            AND genstat.resstatus NE 13 
            /*AND genstat.gratis EQ 0 */
            AND genstat.segmentcode NE 0 
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] NO-LOCK BY genstat.segmentcode:
            
            IF prev-segm NE genstat.segmentcode THEN
            DO:
                prev-segm = genstat.segmentcode.
                FIND FIRST w-rev WHERE w-rev.nr = 1 AND w-rev.artnr = genstat.segmentcode NO-LOCK NO-ERROR.
                FIND FIRST w-pers WHERE w-pers.nr = 2 AND w-pers.artnr = genstat.segmentcode NO-LOCK NO-ERROR.
                FIND FIRST w-room WHERE w-room.nr = 3 AND w-room.artnr = genstat.segmentcode NO-LOCK NO-ERROR.
            END.

            IF genstat.datum = to-date THEN
            DO:
                IF AVAILABLE w-rev THEN
                    w-rev.lytoday = w-rev.lytoday + genstat.logis.
                IF AVAILABLE w-pers THEN
                    w-pers.lytoday = w-pers.lytoday + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                IF AVAILABLE w-room THEN
                    w-room.lytoday = w-room.lytoday + 1.
            END.
    
            IF MONTH(genstat.datum) = mm THEN
            DO:
                IF AVAILABLE w-rev THEN
                    w-rev.lastyr = w-rev.lastyr + genstat.logis.
                IF AVAILABLE w-pers THEN
                    w-pers.lastyr = w-pers.lastyr + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                IF AVAILABLE w-room THEN
                    w-room.lastyr = w-room.lastyr + 1.
            END.
    
            IF AVAILABLE w-rev THEN
                w-rev.lytd-saldo = w-rev.lytd-saldo + genstat.logis.
            IF AVAILABLE w-pers THEN
                w-pers.lytd-saldo = w-pers.lytd-saldo + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
            IF AVAILABLE w-room THEN
                w-room.lytd-saldo = w-room.lytd-saldo + 1.
        END.
    END.

    IF mtd-budget-flag OR ytd-budget-flag THEN
    DO:
        IF ytd-budget-flag THEN datum1 = jan1.
        ELSE datum1 = from-date.

        mm = MONTH(to-date).
        prev-segm = 0.

        FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
            AND segmentstat.datum LE to-date NO-LOCK BY segmentstat.segmentcode:
            
            IF prev-segm NE segmentstat.segmentcode THEN
            DO:
                prev-segm = segmentstat.segmentcode.
                FIND FIRST w-rev WHERE w-rev.nr = 1 AND w-rev.artnr = segmentstat.segmentcode NO-LOCK NO-ERROR.
                FIND FIRST w-pers WHERE w-pers.nr = 2 AND w-pers.artnr = segmentstat.segmentcode NO-LOCK NO-ERROR.
                FIND FIRST w-room WHERE w-room.nr = 3 AND w-room.artnr = segmentstat.segmentcode NO-LOCK NO-ERROR.
            END.

            IF segmentstat.datum = to-date THEN
            DO:
                IF AVAILABLE w-rev THEN
                    w-rev.tbudget = w-rev.tbudget + segmentstat.budlogis.
                IF AVAILABLE w-pers THEN
                    w-pers.tbudget = w-pers.tbudget + segmentstat.budpersanz. 
                IF AVAILABLE w-room THEN
                    w-room.tbudget = w-room.tbudget + 1.
            END.
    
            IF MONTH(segmentstat.datum) = mm THEN
            DO:
                IF AVAILABLE w-rev THEN
                    w-rev.budget = w-rev.budget + segmentstat.budlogis.
                IF AVAILABLE w-pers THEN
                    w-pers.budget = w-pers.budget + segmentstat.budpersanz. 
                IF AVAILABLE w-room THEN
                    w-room.budget = w-room.budget + 1.
            END.
    
            IF AVAILABLE w-rev THEN
                w-rev.ytd-budget = w-rev.ytd-budget + segmentstat.budlogis.
            IF AVAILABLE w-pers THEN
                w-pers.ytd-budget = w-pers.ytd-budget + segmentstat.budpersanz. 
            IF AVAILABLE w-room THEN
                w-room.ytd-budget = w-room.ytd-budget + 1.
        END.                                              
    END.                                                  
END.

