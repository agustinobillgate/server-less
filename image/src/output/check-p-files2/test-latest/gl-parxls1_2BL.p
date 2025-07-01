DEF TEMP-TABLE coa-list
    FIELD fibu LIKE gl-acct.fibukonto
.
DEFINE TEMP-TABLE t-list
    FIELD cf                    AS INTEGER
    FIELD fibukonto             AS CHARACTER
    FIELD debit                 AS DECIMAL
    FIELD credit                AS DECIMAL
    FIELD debit-lsyear          AS DECIMAL
    FIELD credit-lsyear         AS DECIMAL
    FIELD debit-lsmonth         AS DECIMAL
    FIELD credit-lsmonth        AS DECIMAL
    FIELD balance		        AS DECIMAL   
    FIELD ly-balance            AS DECIMAL
    FIELD pm-balance            AS DECIMAL
.

DEF TEMP-TABLE t-parameters LIKE parameters.
DEF TEMP-TABLE t-gl-accthis LIKE gl-accthis.
DEF TEMP-TABLE t-gl-acct    LIKE gl-acct.
DEF TEMP-TABLE t-artikel    LIKE artikel.
DEF TEMP-TABLE t-umsz
    FIELD curr-date   AS DATE
    FIELD artnr       AS INT
    FIELD dept        AS INT
    FIELD fact        AS DECIMAL
    FIELD betrag      AS DECIMAL.

DEFINE TEMP-TABLE g-list
    FIELD datum  AS DATE    INITIAL ?
    FIELD grecid AS INTEGER INITIAL 0
    FIELD fibu   AS CHAR
    INDEX fibu_ix fibu.

DEFINE TEMP-TABLE temp-list
    FIELD vstring       AS CHARACTER
    FIELD debit         AS DECIMAL
    FIELD credit        AS DECIMAL.

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

DEF INPUT PARAMETER briefnr         AS INTEGER.
DEF INPUT PARAMETER gl-year         AS INTEGER.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER foreign-flag    AS LOGICAL.
DEF OUTPUT PARAMETER combo-pf-file1 AS CHARACTER.
DEF OUTPUT PARAMETER combo-pf-file2 AS CHARACTER.
DEF OUTPUT PARAMETER TABLE FOR t-parameters.
DEF OUTPUT PARAMETER TABLE FOR t-gl-accthis.
DEF OUTPUT PARAMETER TABLE FOR t-gl-acct.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-umsz.
DEF OUTPUT PARAMETER TABLE FOR temp-list.
DEF OUTPUT PARAMETER TABLE FOR t-list.
DEF OUTPUT PARAMETER TABLE FOR w1.
/*
DEF VAR briefnr         AS INTEGER INIT 130.
DEF VAR gl-year         AS INTEGER INIT 2017.
DEF VAR from-date       AS DATE INIT 03/01/17.
DEF VAR to-date         AS DATE INIT 03/31/17.
DEF VAR foreign-flag    AS LOGICAL INIT NO.
DEF VAR combo-pf-file1 AS CHARACTER.
DEF VAR combo-pf-file2 AS CHARACTER.*/

DEFINE VARIABLE curr-date     AS DATE.
DEFINE VARIABLE curr-i        AS INTEGER.
DEFINE VARIABLE serv          AS DECIMAL. 
DEFINE VARIABLE vat           AS DECIMAL. 
DEFINE VARIABLE fact          AS DECIMAL. 
DEFINE VARIABLE n-betrag      AS DECIMAL.
DEFINE VARIABLE credit        AS DECIMAL.
DEFINE VARIABLE debit         AS DECIMAL.
DEFINE VARIABLE frate         AS DECIMAL INITIAL 1.
DEFINE VARIABLE price-decimal AS INTEGER. 
DEFINE VARIABLE from-year     AS DECIMAL.
DEFINE VARIABLE to-year       AS DECIMAL.
DEFINE VARIABLE cash-flow     AS LOGICAL INIT NO.
DEFINE VARIABLE prev-str      AS CHARACTER.
DEFINE VARIABLE done-segment  AS LOGICAL INIT NO.
DEFINE VARIABLE datum1        AS DATE.
DEFINE VARIABLE jan1          AS DATE.
DEFINE VARIABLE Ljan1         AS DATE.
DEFINE VARIABLE Lfrom-date    AS DATE.
DEFINE VARIABLE Lto-date      AS DATE.
DEFINE VARIABLE do-it         AS LOGICAL INIT YES.

IF (month(to-date) NE 2) OR (day(to-date) NE 29) THEN 
    Lto-date = DATE(month(to-date), day(to-date), year(to-date) - 1). 
ELSE Lto-date = DATE(month(to-date), 28, year(to-date) - 1). 
    
ASSIGN
    jan1        = DATE(1,1,YEAR(to-date))
    Ljan1       = DATE(1,1,YEAR(to-date) - 1)
    Lfrom-date  = DATE(MONTH(to-date),1,YEAR(to-date) - 1).

DEFINE BUFFER buff-exrate FOR exrate.

DEFINE VARIABLE actual-exrate AS DECIMAL EXTENT 12 
    INITIAL [1,1,1,1,1,1,1,1,1,1,1,1]   NO-UNDO.
DEFINE VARIABLE budget-exrate AS DECIMAL EXTENT 12 
    INITIAL [1,1,1,1,1,1,1,1,1,1,1,1]   NO-UNDO.
DEFINE VARIABLE lyear-exrate  AS DECIMAL EXTENT 12 
    INITIAL [1,1,1,1,1,1,1,1,1,1,1,1]   NO-UNDO.
DEFINE VARIABLE blyear-exrate AS DECIMAL EXTENT 12 
    INITIAL [1,1,1,1,1,1,1,1,1,1,1,1]   NO-UNDO.
DEFINE VARIABLE bnyear-exrate AS DECIMAL EXTENT 12 
    INITIAL [1,1,1,1,1,1,1,1,1,1,1,1]   NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = 2.

FIND FIRST htparam WHERE htparam.paramnr = 339 NO-LOCK.
combo-pf-file1 = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 340 NO-LOCK.
combo-pf-file2 = htparam.fchar.

FOR EACH g-list:
    DELETE g-list.
END.

FIND FIRST parameters WHERE parameters.progname = "GL-Macro"
    AND parameters.SECTION = STRING(briefnr) AND NUM-ENTRIES(parameters.varname,"-") = 3
    AND ENTRY(3,parameters.varname,"-") = "CF" NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN
DO:
    cash-flow = YES.
END.

FIND FIRST parameters WHERE parameters.progname = "GL-Macro"
    AND parameters.SECTION = STRING(briefnr) AND NUM-ENTRIES(parameters.varname,"-") = 3
    AND ENTRY(3,parameters.varname,"-") = "REV" NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN
DO:
    RUN fill-revenue.
END.

FIND FIRST parameters WHERE parameters.progname = "GL-Macro"
    AND parameters.SECTION = STRING(briefnr)
    AND (parameters.vstring MATCHES "*segmrev*" OR parameters.vstring MATCHES "*segmpers*" 
         OR parameters.vstring MATCHES "*segmroom*") NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN RUN fill-segment.
    
IF cash-flow THEN
DO:
    FOR EACH parameters WHERE parameters.progname = "GL-Macro"
        AND parameters.SECTION = STRING(briefnr) AND NUM-ENTRIES(parameters.varname,"-") = 3
        AND ENTRY(3,parameters.varname,"-") = "CF" NO-LOCK BY parameters.varname:
        CREATE t-parameters.
        BUFFER-COPY parameters TO t-parameters.
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = 
            ENTRY(1, t-parameters.vstring, ":") NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        DO:
            FIND FIRST coa-list WHERE coa-list.fibu = gl-acct.fibukonto
                NO-ERROR.
            IF NOT AVAILABLE coa-list THEN
            DO:
                CREATE coa-list.
                ASSIGN coa-list.fibu = gl-acct.fibukonto.
            END.
        END.
    END.
    RUN calc-CF.
END.

FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date
    AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:
    FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr 
        NO-LOCK BY gl-journal.fibukonto:
        CREATE g-list.
        ASSIGN
            g-list.datum  = gl-jouhdr.datum
            g-list.grecid = RECID(gl-journal)
            g-list.fibu   = gl-journal.fibukonto.
    END.
END.

FOR EACH parameters WHERE parameters.progname = "GL-macro"
    AND parameters.SECTION = STRING(briefnr)
    AND parameters.varname MATCHES "*combo*" NO-LOCK BY parameters.varname:
    IF prev-str NE parameters.varname THEN
    DO:
        prev-str = parameters.varname.
        CREATE t-parameters.
        BUFFER-COPY parameters TO t-parameters.
    END.                                       
END.

prev-str = "".

FOR EACH parameters WHERE parameters.progname = "GL-macro"
    AND parameters.SECTION = STRING(briefnr)
    AND NUM-ENTRIES(PARAMETERS.vstring,":") = 1 
    AND NUM-ENTRIES(parameters.varname,"-") = 2 NO-LOCK BY parameters.varname:

    /*IF NUM-ENTRIES(parameters.varname,"-") = 3 THEN
    DO:
        IF ENTRY(3,parameters.varname,"-") = "FO" OR ENTRY(3,parameters.varname,"-") = "CF" 
            AND ENTRY(3,parameters.varname,"-") = "REV" THEN
            do-it = NO.
    END.*/

    IF prev-str NE parameters.varname /*AND do-it*/ THEN
    DO:
        prev-str = parameters.varname.
        
        IF parameters.vstring = "$IN-FOREIGN" THEN 
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
            RUN fill-exrate.
        END.    

        IF SUBSTR(parameters.vstring,1,1) = "$" THEN 
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
        END. 
        
        IF SUBSTR(parameters.vstring,1,1) NE "$" THEN
        DO:
            CREATE t-parameters.
            BUFFER-COPY parameters TO t-parameters.
            ASSIGN
                debit    = 0
                credit   = 0.
            FIND FIRST gl-accthis WHERE gl-accthis.fibukonto
                = parameters.vstring AND gl-accthis.YEAR = gl-year NO-LOCK NO-ERROR.
            IF AVAILABLE gl-accthis THEN
            DO:
                FIND FIRST t-gl-accthis WHERE t-gl-accthis.fibukonto = gl-accthis.fibukonto
                    AND t-gl-accthis.YEAR = gl-accthis.YEAR NO-LOCK NO-ERROR.
                IF NOT AVAILABLE t-gl-accthis THEN
                DO:
                    CREATE t-gl-accthis.
                    BUFFER-COPY gl-accthis TO t-gl-accthis.
                    IF SUBSTR(t-gl-accthis.fibukonto,1,1) = "9" THEN .  /* grand mirage, statistic acct */
                    ELSE
                    DO curr-i = 1 TO 12:
                      ASSIGN
                        t-gl-accthis.actual[curr-i]    = t-gl-accthis.actual[curr-i] / actual-exrate[curr-i]
                        t-gl-accthis.budget[curr-i]    = t-gl-accthis.budget[curr-i] / budget-exrate[curr-i]
                        t-gl-accthis.last-yr[curr-i]   = t-gl-accthis.last-yr[curr-i] / lyear-exrate[curr-i]
                        t-gl-accthis.ly-budget[curr-i] = t-gl-accthis.ly-budget[curr-i] / blyear-exrate[curr-i]
                      .
                    END.
                END.
            END.
        
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = parameters.vstring 
                NO-LOCK NO-ERROR.
            IF AVAILABLE gl-acct THEN
            DO:
                FIND FIRST t-gl-acct WHERE t-gl-acct.fibukonto = gl-acct.fibukonto
                    NO-LOCK NO-ERROR.
                IF NOT AVAILABLE t-gl-acct THEN
                DO:
                    CREATE t-gl-acct.
                    BUFFER-COPY gl-acct TO t-gl-acct.
                    IF SUBSTR(t-gl-acct.fibukonto,1,1) = "9" THEN .  /* grand mirage, statistic acct */
                    ELSE
                    DO curr-i = 1 TO 12:                        
                      ASSIGN
                        t-gl-acct.actual[curr-i]    = t-gl-acct.actual[curr-i] / actual-exrate[curr-i]
                        t-gl-acct.budget[curr-i]    = t-gl-acct.budget[curr-i] / budget-exrate[curr-i]
                        t-gl-acct.last-yr[curr-i]   = t-gl-acct.last-yr[curr-i] / lyear-exrate[curr-i]
                        t-gl-acct.ly-budget[curr-i] = t-gl-acct.ly-budget[curr-i] / blyear-exrate[curr-i]
                      .
                    END.
                END.
            END.
            
            IF parameters.vtype = 25 OR parameters.vtype = 26 THEN     
            DO:
                FOR EACH g-list WHERE g-list.fibu EQ parameters.vstring
                  USE-INDEX fibu_ix BY g-list.fibu BY g-list.datum:
                  RELEASE gl-journal.
                  IF g-list.grecid NE 0 THEN
                  DO:
                    FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
                    IF AVAILABLE gl-journal THEN
                      ASSIGN
                        debit  = debit + gl-journal.debit. 
                        credit = credit + gl-journal.credit. 
                  END.
                END.
                CREATE temp-list.
                ASSIGN
                    temp-list.vstring = parameters.vstring
                    temp-list.debit = debit
                    temp-list.credit = credit.
            END.
        END.
    END.    
END.

PROCEDURE fill-exrate:
DEF VAR to-month    AS INTEGER NO-UNDO.
DEF VAR ind         AS INTEGER NO-UNDO.
DEF VAR curr-yr     AS INTEGER NO-UNDO.
DEF VAR last-yr     AS INTEGER NO-UNDO.
DEF VAR next-yr     AS INTEGER NO-UNDO.
DEF VAR curr-date   AS DATE    NO-UNDO.
DEF VAR lyear-date  AS DATE    NO-UNDO.
DEF VAR nyear-date  AS DATE    NO-UNDO.
  ASSIGN
    to-month = MONTH(to-date)
    curr-yr  = YEAR(to-date)
    last-yr  = YEAR(to-date) - 1
    next-yr  = YEAR(to-date) + 1
  .

  /*DO ind = 1 TO to-month:*/
  DO ind = 1 TO 12:
    IF ind = 12 THEN
    ASSIGN
        curr-date  = DATE(12, 31, curr-yr)
        lyear-date = DATE(12, 31, last-yr)
        nyear-date = DATE(12, 31, next-yr)
    .
    ELSE
    ASSIGN
       curr-date  = DATE(ind, 1, curr-yr) + 35
       curr-date  = DATE(MONTH(curr-date), 1, curr-yr) - 1
       lyear-date = DATE(ind, 1, last-yr) + 35
       lyear-date = DATE(MONTH(lyear-date), 1, last-yr) - 1
       nyear-date = DATE(ind, 1, next-yr) + 35
       nyear-date = DATE(MONTH(nyear-date), 1, next-yr) - 1
    .

    FIND FIRST exrate WHERE exrate.artnr = 99999 
        AND exrate.datum = curr-date NO-LOCK NO-ERROR.
    IF AVAILABLE exrate THEN ASSIGN actual-exrate[ind] = exrate.betrag.
    FIND FIRST exrate WHERE exrate.artnr = 99999 
        AND exrate.datum = lyear-date NO-LOCK NO-ERROR.
    IF AVAILABLE exrate THEN ASSIGN lyear-exrate[ind] = exrate.betrag.
    FIND FIRST exrate WHERE exrate.artnr = 99998 
        AND exrate.datum = curr-date NO-LOCK NO-ERROR.
    IF AVAILABLE exrate THEN ASSIGN budget-exrate[ind] = exrate.betrag.
    FIND FIRST exrate WHERE exrate.artnr = 99998 
        AND exrate.datum = lyear-date NO-LOCK NO-ERROR.
    IF AVAILABLE exrate THEN ASSIGN blyear-exrate[ind] = exrate.betrag.
    FIND FIRST exrate WHERE exrate.artnr = 99998 
        AND exrate.datum = nyear-date NO-LOCK NO-ERROR.
    IF AVAILABLE exrate THEN ASSIGN bnyear-exrate[ind] = exrate.betrag.
  END.
END.

PROCEDURE calc-CF:
DEFINE VARIABLE from-lsyr   AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE to-lsyr     AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE Pfrom-date  AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE Pto-date    AS DATE NO-UNDO INIT ?.
    
    IF MONTH(from-date) = 1 THEN 
        Pfrom-date = DATE(12, DAY(from-date), YEAR(from-date) - 1).
    ELSE Pfrom-date = DATE(MONTH(from-date) - 1, DAY(from-date), YEAR(from-date)) NO-ERROR.

    IF MONTH(to-date) = 1 THEN 
        Pto-date = DATE(12, DAY(to-date), YEAR(to-date) - 1).
    ELSE Pto-date = DATE(MONTH(to-date) - 1, DAY(to-date), YEAR(to-date)) NO-ERROR.

    from-lsyr = DATE(MONTH(from-date), DAY(from-date), YEAR(from-date)- 1) NO-ERROR.

    IF MONTH(to-date) = 2 AND (YEAR(to-date) MOD 4 = 0) THEN 
        to-lsyr   = DATE(MONTH(to-date), DAY(to-date) - 1, YEAR(to-date)- 1) NO-ERROR.
    ELSE to-lsyr   = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date)- 1) NO-ERROR.

    IF Pfrom-date = ? THEN pfrom-date = DATE(MONTH(from-date), 1, YEAR(from-date)) - 1.
    IF Pto-date   = ? THEN Pto-date   = DATE(MONTH(to-date), 1, YEAR(to-date)) - 1.
    IF from-lsyr  = ? THEN from-lsyr  = DATE(MONTH(from-date), 1, YEAR(from-date) - 1) - 1.
    IF to-lsyr    = ? THEN to-lsyr    = DATE(MONTH(to-date), 1, YEAR(to-date) - 1) - 1.
    
    RUN glacct-cashflowbl.p(from-date, to-date, from-lsyr, to-lsyr, 
        Pfrom-date, Pto-date, TABLE coa-list, OUTPUT TABLE t-list).
END.

PROCEDURE find-exrate: 
DEFINE INPUT PARAMETER curr-date AS DATE NO-UNDO. 
DEFINE VARIABLE foreign-nr       AS INTEGER INITIAL 0 NO-UNDO. 

  IF foreign-flag THEN
  DO:
      FIND FIRST buff-exrate WHERE buff-exrate.artnr = 99999 
          AND buff-exrate.datum = curr-date NO-LOCK NO-ERROR.
      IF AVAILABLE buff-exrate THEN RETURN.
  END.

  FIND FIRST htparam WHERE htparam.paramnr = 144 NO-LOCK. 
  IF htparam.fchar NE "" THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN foreign-nr = waehrung.waehrungsnr. 
  END. 

  IF foreign-nr NE 0 THEN FIND FIRST buff-exrate WHERE buff-exrate.artnr = foreign-nr 
    AND buff-exrate.datum = curr-date NO-LOCK NO-ERROR. 
  ELSE FIND FIRST buff-exrate WHERE buff-exrate.datum = curr-date NO-LOCK NO-ERROR. 
END. 

PROCEDURE fill-segment:
    DEFINE BUFFER s-param FOR parameters.
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
    
    FOR EACH s-param WHERE s-param.progname = "GL-macro"
        AND s-param.SECTION = STRING(briefnr)
        AND NUM-ENTRIES(s-param.vstring,":") = 1 
        AND NUM-ENTRIES(s-param.varname,"-") = 3
        AND ENTRY(3,s-param.varname,"-") = "FO"
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

            CREATE t-parameters.
            BUFFER-COPY s-param TO t-parameters.
            
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
        AND genstat.res-logic[2] EQ YES NO-LOCK BY genstat.segmentcode:

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
            AND genstat.res-logic[2] EQ YES NO-LOCK BY genstat.segmentcode:
            
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

PROCEDURE fill-revenue:
    DEFINE BUFFER s-param FOR parameters.
    DEFINE VARIABLE prev-param AS CHAR INIT "".
    DEFINE VARIABLE ytd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE lytd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE lmtd-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE ytd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mtd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mm AS INT.
    
    DEFINE BUFFER w4  FOR w1.
    
    FOR EACH s-param WHERE s-param.progname = "GL-macro"
        AND s-param.SECTION = STRING(briefnr)
        AND NUM-ENTRIES(s-param.vstring,":") = 1 
        AND NUM-ENTRIES(s-param.varname,"-") = 3
        AND ENTRY(3,s-param.varname,"-") = "REV" NO-LOCK BY s-param.varname:
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

            CREATE t-parameters.
            BUFFER-COPY s-param TO t-parameters.
            
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
