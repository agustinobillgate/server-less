
/*This BL for VHP Web Based*/
DEF TEMP-TABLE t-parameters LIKE parameters.
DEF TEMP-TABLE t-gl-accthis LIKE gl-accthis.
DEF TEMP-TABLE glacct-list  LIKE gl-acct.
DEF TEMP-TABLE t-gl-acct    LIKE gl-acct.
DEF TEMP-TABLE t-artikel    LIKE artikel.
DEF TEMP-TABLE t-umsz
    FIELD curr-date     AS DATE
    FIELD artnr         AS INT
    FIELD dept          AS INT
    FIELD fact          AS DECIMAL
    FIELD betrag        AS DECIMAL.

DEFINE TEMP-TABLE g-list
    FIELD datum         AS DATE    INITIAL ?
    FIELD grecid        AS INTEGER INITIAL 0
    FIELD fibu          AS CHAR
    INDEX fibu_ix fibu.

DEFINE TEMP-TABLE temp-list
    FIELD vstring       AS CHARACTER
    FIELD debit         AS DECIMAL
    FIELD credit        AS DECIMAL.

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
    /*geral D5D0FB debit - credit MTD & YTD*/
    FIELD debit-today           AS DECIMAL
    FIELD credit-today          AS DECIMAL
    FIELD debit-MTD             AS DECIMAL
    FIELD credit-MTD            AS DECIMAL
    FIELD debit-YTD             AS DECIMAL
    FIELD credit-YTD            AS DECIMAL
    FIELD today-balance         AS DECIMAL
    FIELD MTD-balance           AS DECIMAL
    FIELD YTD-balance           AS DECIMAL
.

/*ragung*/


DEFINE TEMP-TABLE stat-list
    FIELD ct            AS INTEGER
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD flag          AS CHAR.

DEFINE TEMP-TABLE rev-list 
    FIELD ct            AS INTEGER
    FIELD descr         AS CHAR FORMAT "x(35)"
    FIELD departement   AS INTEGER
    FIELD t-day         AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD dper          AS DECIMAL FORMAT ">>9.99"
    FIELD mtd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD mtd-per       AS DECIMAL FORMAT "->>9.99"
    FIELD mtd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD variance      AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd           AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-budget    AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
    FIELD ytd-per       AS DECIMAL FORMAT ">>9.99"
    FIELD flag          AS CHAR
    FIELD flag-grup     AS LOGICAL.

DEFINE BUFFER   b-stat-list     FOR stat-list.
DEFINE BUFFER   b-stat          FOR stat-list.

DEF INPUT PARAMETER briefnr         AS INTEGER.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER user-init       AS CHARACTER.
DEF INPUT PARAMETER gl-month        AS INTEGER. 
DEF INPUT PARAMETER link            AS CHARACTER.
DEF OUTPUT PARAMETER mess-result    AS CHARACTER INITIAL "Failed to generate data".
 
/*
DEF VAR briefnr         AS INTEGER INIT 154.
DEF VAR from-date       AS DATE INIT 01/01/24.
DEF VAR to-date         AS DATE INIT 01/10/24.
DEF VAR user-init       AS CHARACTER INIT "01".
DEF VAR gl-month        AS INT.
DEF VAR stime AS INT.
DEF VAR link AS CHAR.

stime = TIME.
gl-month = month(to-date). 
IF day(to-date) LT 15 THEN gl-month = gl-month - 1. 
IF gl-month = 0 THEN gl-month = 12.
DEF VAR mess-result    AS CHARACTER.
*/

DEFINE STREAM s1.

DEFINE VARIABLE month-str AS CHAR EXTENT 12 
    INITIAL ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE", 
    "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]. 

DEFINE VARIABLE ChCol AS CHAR EXTENT 52 INITIAL
    ["A","B","C","D","E","F","G","H","I","J","K","L","M",
     "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
     "AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM",
     "AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ"].

DEFINE VARIABLE curr-date       AS DATE.
DEFINE VARIABLE curr-i          AS INTEGER.
DEFINE VARIABLE curr-row        AS INTEGER.
DEFINE VARIABLE curr-col        AS INTEGER.
DEFINE VARIABLE serv            AS DECIMAL. 
DEFINE VARIABLE vat             AS DECIMAL. 
DEFINE VARIABLE fact            AS DECIMAL. 
DEFINE VARIABLE n-betrag        AS DECIMAL.
DEFINE VARIABLE credit          AS DECIMAL.
DEFINE VARIABLE debit           AS DECIMAL.
DEFINE VARIABLE frate           AS DECIMAL INITIAL 1.
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE gl-year         AS INTEGER.
DEFINE VARIABLE from-year       AS DECIMAL.
DEFINE VARIABLE to-year         AS DECIMAL.
DEFINE VARIABLE foreign-flag    AS LOGICAL INIT NO.
DEFINE VARIABLE prev-str        AS CHAR.
DEFINE VARIABLE cell-val        AS CHAR.
DEFINE VARIABLE exrate-betrag   AS DECIMAL INITIAL 0.
DEFINE VARIABLE hist-flag       AS LOGICAL INIT NO.

DEFINE VARIABLE curr-close-year AS INT.
DEFINE VARIABLE found-flag      AS LOGICAL INIT NO.
DEFINE VARIABLE ytd-bal         AS DECIMAL NO-UNDO.
DEFINE VARIABLE val-sign        AS INT.
DEFINE VARIABLE j               AS INT.
DEFINE VARIABLE i               AS INT.
DEFINE VARIABLE diff            AS DECIMAL.
DEFINE VARIABLE lmdiff          AS DECIMAL.

DEFINE VARIABLE mtd-betrag      AS DECIMAL.
DEFINE VARIABLE ytd-betrag      AS DECIMAL.

DEFINE VARIABLE start-row       AS INT INIT 0.
DEFINE VARIABLE start-col       AS INT INIT 0.
DEFINE VARIABLE end-row         AS INT.
DEFINE VARIABLE end-col         AS INT.
DEFINE VARIABLE htl-no          AS CHAR.

DEFINE VARIABLE datum1          AS DATE.
DEFINE VARIABLE jan1            AS DATE.
DEFINE VARIABLE Ljan1           AS DATE.
DEFINE VARIABLE Lfrom-date      AS DATE.
DEFINE VARIABLE Lto-date        AS DATE.
DEFINE VARIABLE cash-flow       AS LOGICAL INIT NO.

IF (month(to-date) NE 2) OR (day(to-date) NE 29) THEN 
    Lto-date = DATE(month(to-date), day(to-date), year(to-date) - 1). 
ELSE Lto-date = DATE(month(to-date), 28, year(to-date) - 1). 
    
ASSIGN
    jan1        = DATE(1,1,YEAR(to-date))
    Ljan1       = DATE(1,1,YEAR(to-date) - 1)
    Lfrom-date  = DATE(MONTH(to-date),1,YEAR(to-date) - 1).

DEFINE BUFFER buff-exrate FOR exrate.

/*ragung add define param*/
DEFINE BUFFER b-param FOR parameters.

DEFINE VARIABLE foreign-curr AS DECIMAL.
FIND FIRST waehrung WHERE waehrung.waehrungsnr EQ 2 NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN foreign-curr = waehrung.ankauf.

DEFINE VARIABLE ct1           AS INTEGER.
DEFINE VARIABLE mon-saldo       AS DECIMAL EXTENT 31 INITIAL 
      [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0].

DEFINE VARIABLE vat2            AS DECIMAL. 
DEFINE VARIABLE ytd-flag  AS LOGICAL INITIAL YES.
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE n-serv          AS DECIMAL. 
DEFINE VARIABLE n-tax           AS DECIMAL. 

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
price-decimal = htparam.finteger.

FIND FIRST paramtext WHERE paramtext.txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN
    RUN decode-string(paramtext.ptexte, OUTPUT htl-no). 

FOR EACH g-list:
    DELETE g-list.
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

IF ytd-flag THEN datum1 = jan1. 
ELSE datum1 = from-date.


OS-DELETE VALUE ("/usr1/vhp/tmp/output_" + htl-no + ".txt").
OUTPUT STREAM s1 TO VALUE("/usr1/vhp/tmp/output_" + htl-no + ".txt") APPEND UNBUFFERED.

/*
OS-DELETE VALUE ("C:\Users\sinda\OneDrive\Desktop\tes PNL jane" + htl-no + ".txt").
OUTPUT STREAM s1 TO VALUE("C:\Users\sinda\OneDrive\Desktop\tes PNL jane" + htl-no + ".txt") APPEND UNBUFFERED.
*/

FIND FIRST parameters WHERE parameters.progname = "GL-macro"
    AND parameters.SECTION = STRING(briefnr) AND parameters.vstring = "$IN-FOREIGN" 
    NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN 
DO:
    foreign-flag = YES.
    RUN fill-exrate.
    PUT STREAM s1 UNFORMATTED 
        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
END.

/*adjusting from 1UI*/
FIND FIRST parameters WHERE parameters.progname = "GL-Macro"
    AND parameters.SECTION = STRING(briefnr) AND NUM-ENTRIES(parameters.varname,"-") = 3
    AND ENTRY(3,parameters.varname,"-") = "CF" NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN
DO:
    cash-flow = YES.
END.

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

RUN create-rev-list.

RUN fill-tot-room. /*Agu*/
RUN fill-tot-avail.
RUN fill-inactive.
RUN fill-rmstat("ooo").
/*RUN fill-rmstat("oos").*/
RUN fill-rmocc. 
RUN fill-stat("vacant").
RUN fill-segm("HSE").
RUN fill-segm("COM").
RUN fill-segm("COM-GS").
RUN fill-comproomnew.
RUN fill-roomsold.
RUN fill-occ-pay.
RUN fill-occ-comp-hu.
RUN fill-tot-rev.
RUN fill-avg-rmrate-rp.
RUN fill-avg-rmrate-frg.
RUN fill-revpar.
RUN fill-rmstat("dayuse").
RUN fill-rmstat("No-Show").
RUN fill-rmstat("arrival-WIG").
RUN fill-rmstat("NewRes").
RUN fill-rmstat("CancRes").
RUN fill-rmstat("Early-CO").
RUN fill-rmstat("arrival").
RUN fill-rmstat("pers-arrival").
RUN fill-rmstat("departure").
RUN fill-rmstat("pers-depature").
RUN fill-rmstat("ArrTmrw").
RUN fill-rmstat("pers-ArrTmrw").
RUN fill-rmstat("DepTmrw").
RUN fill-rmstat("pers-DepTmrw").
RUN fill-rmstat("arrival-RSV").
RUN fill-gs-inhouse.
RUN fill-statistic. 


/*
FIND FIRST parameters WHERE parameters.progname = "GL-Macro"
    AND parameters.SECTION = STRING(briefnr)
    AND (parameters.vstring MATCHES "*stat-tot-rm*" 
         OR parameters.vstring MATCHES "*stat-act-rm*" 
         OR parameters.vstring MATCHES "*stat-ooo*"
         OR parameters.vstring MATCHES "*stat-rrom-90*" 
         OR parameters.vstring MATCHES "*stat-rrom-91*"         
         OR parameters.vstring MATCHES "*stat-rrom-92*" 
         OR parameters.vstring MATCHES "*stat-occ-rm*"
         OR parameters.vstring MATCHES "*stat-rm-wig*" 
         OR parameters.vstring MATCHES "*stat-nguest*"
         OR parameters.vstring MATCHES "*stat-day-use*" 
         OR parameters.vstring MATCHES "*stat-numcompl*"
         OR parameters.vstring MATCHES "*stat-rm-rsv*" 
         OR parameters.vstring MATCHES "*stat-rm-arr*"
         OR parameters.vstring MATCHES "*stat-prs-arr*" 
         OR parameters.vstring MATCHES "*stat-rm-dep*"
         OR parameters.vstring MATCHES "*stat-prs-dep*" 
         OR parameters.vstring MATCHES "*stat-rm-wig*"
         OR parameters.vstring MATCHES "*stat-noshow*" 
         OR parameters.vstring MATCHES "*stat-newres*"
         OR parameters.vstring MATCHES "*stat-cancel*" 
         OR parameters.vstring MATCHES "*stat-earco*"
         OR parameters.vstring MATCHES "*stat-rm-arrtmr*" 
         OR parameters.vstring MATCHES "*stat-prs-arrtmr*"
         OR parameters.vstring MATCHES "*stat-rm-deptmr*" 
         ) NO-LOCK NO-ERROR.
IF AVAILABLE parameters THEN RUN fill-statistic(parameters.vstring).
/*end*/*/


ASSIGN gl-year = YEAR(to-date).
FOR EACH parameters WHERE parameters.progname = "GL-macro"
    AND parameters.SECTION = STRING(briefnr) NO-LOCK BY parameters.varname:
    
    IF prev-str NE parameters.varname THEN
    DO:
        ASSIGN
            debit    = 0
            credit   = 0
            prev-str = parameters.varname
        .
        
        CREATE t-parameters.
        BUFFER-COPY parameters TO t-parameters.

        IF SUBSTR(parameters.vstring,1,1) NE "$" THEN
        DO:
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
    
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = parameters.vstring NO-LOCK NO-ERROR.
            IF AVAILABLE gl-acct THEN
            DO:
                FIND FIRST t-gl-acct WHERE t-gl-acct.fibukonto = gl-acct.fibukonto NO-LOCK NO-ERROR.
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
    
            IF parameters.vtype = 23 AND NUM-ENTRIES(parameters.varname,"-") = 2 THEN
            DO:
                FIND FIRST artikel WHERE artikel.artnr = INT(SUBSTR(parameters.vstring,3)) 
                    AND artikel.departement = INT(SUBSTR(parameters.vstring,1,2))
                    NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    FIND FIRST t-artikel WHERE t-artikel.artnr = artikel.artnr
                        AND t-artikel.departement = artikel.departement
                        NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE t-artikel THEN
                    DO:
                        CREATE t-artikel.
                        BUFFER-COPY artikel TO t-artikel.
                    END.
                END.
        
                DO curr-date = DATE(01,01,YEAR(to-date)) TO to-date:
                    ASSIGN 
                        serv = 0
                        vat  = 0.
                    FIND FIRST umsatz WHERE umsatz.datum = curr-date 
                        AND umsatz.artnr = INT(SUBSTR(parameters.vstring,3))
                        AND umsatz.departement = INT(SUBSTR(parameters.vstring,1,2)) 
                        NO-LOCK NO-ERROR. 
                    IF AVAILABLE umsatz THEN
                    DO:
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
                        IF price-decimal = 0 THEN n-betrag = ROUND(n-betrag, 0).
                    END.
                    IF AVAILABLE umsatz THEN 
                    DO: 
                        CREATE t-umsz.
                        ASSIGN t-umsz.curr-date   = curr-date
                             t-umsz.fact        = fact
                             t-umsz.betrag      = n-betrag
                             t-umsz.artnr       = umsatz.artnr
                             t-umsz.dept        = umsatz.departement.
                    END.
                END.
            END.     
        END.
    END.
END.  

CREATE glacct-list.

FIND FIRST htparam WHERE htparam.paramnr = 795 NO-LOCK. /* last close year */
ASSIGN curr-close-year = YEAR(htparam.fdate) + 1.
IF gl-year LT curr-close-year THEN ASSIGN hist-flag = YES.

FIND FIRST t-parameters WHERE t-parameters.progname = "GL-Macro"
    AND NUM-ENTRIES(t-parameters.varname,"-") = 3
    AND ENTRY(3,t-parameters.varname,"-") = "CF" NO-LOCK NO-ERROR.
IF AVAILABLE t-parameters THEN
DO:
    FOR EACH t-parameters WHERE NUM-ENTRIES(t-parameters.varname,"-") = 3
        AND ENTRY(3,t-parameters.varname,"-") = "CF" 
        AND NUM-ENTRIES(t-parameters.vstring,":") GT 1 NO-LOCK:
        ASSIGN
            curr-row   = INTEGER(ENTRY(1, t-parameters.varname, "-"))
            curr-col   = INTEGER(ENTRY(2, t-parameters.varname, "-"))
            end-row    = curr-row  
            end-col    = curr-col.
        
        IF NUM-ENTRIES(t-parameters.vstring, ":") GT 1 THEN
        DO:
            FIND FIRST t-list WHERE t-list.fibukonto = ENTRY(1, t-parameters.vstring, ":")
                AND t-list.cf = INT(ENTRY(2, t-parameters.vstring, ":")) 
                NO-ERROR.
            IF AVAILABLE t-list THEN
            DO:
                cell-val = "".
                IF t-parameters.vtype = 25 THEN
                    ASSIGN cell-val = STRING(t-list.debit,"->,>>>,>>>,>>>,>>>,>>9.99"). 
                ELSE IF t-parameters.vtype = 26 THEN
                    ASSIGN cell-val = STRING(t-list.credit,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 79 THEN
                    ASSIGN cell-val = STRING(t-list.debit-lsyear,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 80 THEN
                    ASSIGN cell-val = STRING(t-list.credit-lsyear,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 81 THEN
                    ASSIGN cell-val = STRING(t-list.debit-lsmonth,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 82 THEN
                    ASSIGN cell-val = STRING(t-list.credit-lsmonth,"->,>>>,>>>,>>>,>>>,>>9.99").    
                ELSE IF t-parameters.vtype = 1 THEN
                    ASSIGN cell-val = STRING(t-list.balance,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 3 THEN
                    ASSIGN cell-val = STRING(t-list.pm-balance,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 4 THEN
                    ASSIGN cell-val = STRING(t-list.ly-balance,"->,>>>,>>>,>>>,>>>,>>9.99").
                /*geral D5D0FB debit - credit - balance MTD & YTD*/
                ELSE IF t-parameters.vtype = 90 THEN
                    ASSIGN cell-val = STRING(t-list.debit-today,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 91 THEN
                    ASSIGN cell-val = STRING(t-list.credit-today,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 92 THEN
                    ASSIGN cell-val = STRING(t-list.debit-MTD,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 93 THEN
                    ASSIGN cell-val = STRING(t-list.credit-MTD,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 94 THEN
                    ASSIGN cell-val = STRING(t-list.debit-YTD,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 95 THEN
                    ASSIGN cell-val = STRING(t-list.credit-YTD,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 96 THEN
                    ASSIGN cell-val = STRING(t-list.today-balance,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 97 THEN
                    ASSIGN cell-val = STRING(t-list.MTD-balance,"->,>>>,>>>,>>>,>>>,>>9.99").
                ELSE IF t-parameters.vtype = 98 THEN
                    ASSIGN cell-val = STRING(t-list.YTD-balance,"->,>>>,>>>,>>>,>>>,>>9.99").
            END.
            ELSE
                ASSIGN cell-val = "".
        END.               
        IF cell-val NE "" THEN
            PUT STREAM s1 UNFORMATTED 
                STRING(curr-row) ";" STRING(curr-col) ";" cell-val SKIP.
        ELSE
            PUT STREAM s1 UNFORMATTED 
                STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    END.
END.

FOR EACH t-parameters WHERE NUM-ENTRIES(t-parameters.varname,"-") LE 2 BY t-parameters.varname:
    ASSIGN
        curr-row = INTEGER(ENTRY(1, t-parameters.varname, "-"))
        curr-col = INTEGER(ENTRY(2, t-parameters.varname, "-"))
        end-row  = curr-row
        end-col  = curr-col
    .
    IF start-row = 0 THEN
        start-row = curr-row.
    IF start-col = 0 THEN
        start-col = curr-col.
    
    IF t-parameters.vtype = 0 THEN
    DO:
        cell-val = "".
        CASE t-parameters.vstring:
            WHEN "$DATUM" THEN
                ASSIGN  cell-val = "Created: " + STRING(TODAY) + " - " + user-init.
            WHEN "$CLOSE-DATE" THEN
                ASSIGN cell-val = "Closing Date: " + STRING(to-date, "99/99/9999").
            WHEN "$CLOSE-MONTH" THEN
                ASSIGN cell-val = "Accounting Period: " + month-str[MONTH(to-date)] 
                       + " " + STRING(YEAR(to-date),"9999").
            WHEN "$CLOSE-MONTH1" THEN
                ASSIGN cell-val = STRING(MONTH(to-date),"99") + "/" + STRING(YEAR(to-date),"9999").
            WHEN "$EXRATE" THEN
            DO:
                RUN gl-parxls1-find-exratebl.p (to-date, foreign-flag, OUTPUT exrate-betrag, OUTPUT frate).
                ASSIGN cell-val = "ExchgRate: " + TRIM(STRING(exrate-betrag,"->>>>>>>>>>>>>9.99")).
            END.
        END CASE.
        IF cell-val NE "" THEN
            PUT STREAM s1 UNFORMATTED 
                STRING(curr-row) ";" STRING(curr-col) ";" cell-val SKIP.
        ELSE
            PUT STREAM s1 UNFORMATTED 
                STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    END.         
    ELSE IF t-parameters.vtype GT 0 THEN      /*here*/
    DO:
        IF hist-flag THEN 
        DO:    
            FIND FIRST t-gl-accthis WHERE t-gl-accthis.fibukonto = t-parameters.vstring AND t-gl-accthis.YEAR = gl-year
                NO-LOCK NO-ERROR.
            found-flag = AVAILABLE t-gl-accthis. 
            IF found-flag THEN BUFFER-COPY t-gl-accthis TO glacct-list.
        END.
        ELSE
        DO:    
            FIND FIRST t-gl-acct WHERE t-gl-acct.fibukonto = t-parameters.vstring
                NO-LOCK NO-ERROR.
            found-flag = AVAILABLE t-gl-acct. 
            IF found-flag THEN BUFFER-COPY t-gl-acct TO glacct-list.
        END.
    END.
    
    IF t-parameters.vtype GT 0 THEN 
    DO:
        cell-val = "".
        IF found-flag AND (glacct-list.acc-type = 1 OR glacct-list.acc-type = 4) THEN
        CASE t-parameters.vtype:
            WHEN 1  THEN 
            DO:
                IF glacct-list.actual[gl-month] = ? THEN ASSIGN glacct-list.actual[gl-month] = 0.
                cell-val = TRIM(STRING(- glacct-list.actual[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 2  THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.actual[curr-i] = ? THEN ASSIGN glacct-list.actual[curr-i] = 0.
                    ytd-bal = ytd-bal - glacct-list.actual[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 3  THEN 
            DO:  
                IF gl-month = 1 THEN
                DO:
                    IF glacct-list.last-yr[12] = ? THEN ASSIGN glacct-list.last-yr[12] = 0.
                    cell-val = TRIM(STRING(- glacct-list.last-yr[12],"->>>>>>>>>>>>>>>>9.99")). 
                END.
                ELSE
                DO:
                    IF glacct-list.actual[gl-month - 1] = ? THEN ASSIGN glacct-list.actual[gl-month - 1] = 0.
                    cell-val = TRIM(STRING(- glacct-list.actual[gl-month - 1],"->>>>>>>>>>>>>>>>9.99")). 
                END.

            END.
            WHEN 4  THEN
            DO:
                IF glacct-list.last-yr[gl-month] = ? THEN ASSIGN glacct-list.last-yr[gl-month] = 0.
                cell-val = TRIM(STRING(- glacct-list.last-yr[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 5  THEN   
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.last-yr[curr-i] = ? THEN ASSIGN glacct-list.last-yr[curr-i] = 0.
                    ytd-bal = ytd-bal - glacct-list.last-yr[curr-i].    /*FT diubah +*/
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 6  THEN 
            DO:
                IF glacct-list.budget[gl-month] = ? THEN ASSIGN glacct-list.budget[gl-month] = 0.
                cell-val = TRIM(STRING(- glacct-list.budget[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 7  THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.budget[curr-i] = ? THEN ASSIGN glacct-list.budget[curr-i] = 0.
                    ytd-bal = ytd-bal - glacct-list.budget[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 8  THEN 
            DO:  
                IF gl-month = 1 THEN
                DO:
                    IF glacct-list.ly-budget[12] = ? THEN ASSIGN glacct-list.ly-budget[12] = 0.
                    cell-val = TRIM(STRING(- glacct-list.ly-budget[12],"->>>>>>>>>>>>>>>>9.99")). 
                END.
                ELSE
                DO:
                    IF glacct-list.budget[gl-month - 1] = ? THEN ASSIGN glacct-list.budget[gl-month - 1] = 0.
                    cell-val = TRIM(STRING(- glacct-list.budget[gl-month - 1],"->>>>>>>>>>>>>>>>9.99")). 
                END.
            END.
            WHEN 9  THEN
            DO:
                IF glacct-list.ly-budget[gl-month] = ? THEN ASSIGN glacct-list.ly-budget[gl-month] = 0.
                cell-val = TRIM(STRING(- glacct-list.ly-budget[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 10 THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.ly-budget[curr-i] = ? THEN ASSIGN glacct-list.ly-budget[curr-i] = 0.
                    ytd-bal = ytd-bal - glacct-list.ly-budget[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 11 THEN cell-val = TRIM(STRING(- glacct-list.actual[1],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 12 THEN cell-val = TRIM(STRING(- glacct-list.actual[2],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 13 THEN cell-val = TRIM(STRING(- glacct-list.actual[3],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 14 THEN cell-val = TRIM(STRING(- glacct-list.actual[4],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 15 THEN cell-val = TRIM(STRING(- glacct-list.actual[5],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 16 THEN cell-val = TRIM(STRING(- glacct-list.actual[6],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 17 THEN cell-val = TRIM(STRING(- glacct-list.actual[7],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 18 THEN cell-val = TRIM(STRING(- glacct-list.actual[8],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 19 THEN cell-val = TRIM(STRING(- glacct-list.actual[9],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 20 THEN cell-val = TRIM(STRING(- glacct-list.actual[10],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 21 THEN cell-val = TRIM(STRING(- glacct-list.actual[11],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 22 THEN cell-val = TRIM(STRING(- glacct-list.actual[12],"->>>>>>>>>>>>>>>>9.99")). 
        END CASE.
        ELSE IF found-flag THEN
        CASE t-parameters.vtype:
            WHEN 1  THEN
            DO: 
                IF glacct-list.actual[gl-month] = ? THEN ASSIGN glacct-list.actual[gl-month] = 0.
                cell-val = TRIM(STRING(glacct-list.actual[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 2  THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.actual[curr-i] = ? THEN ASSIGN glacct-list.actual[curr-i] = 0.
                    ytd-bal = ytd-bal + glacct-list.actual[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 3  THEN 
            DO:  
                IF gl-month = 1 THEN
                DO:
                    IF glacct-list.last-yr[12] = ? THEN ASSIGN glacct-list.last-yr[12] = 0.
                    cell-val = TRIM(STRING(glacct-list.last-yr[12],"->>>>>>>>>>>>>>>>9.99")). 
                END.
                ELSE
                DO: 
                    IF glacct-list.actual[gl-month - 1] = ? THEN ASSIGN glacct-list.actual[gl-month - 1] = 0.
                    cell-val = TRIM(STRING(glacct-list.actual[gl-month - 1],"->>>>>>>>>>>>>>>>9.99")). 
                END.
            END.
            WHEN 4  THEN 
            DO:    
                IF glacct-list.last-yr[gl-month] = ? THEN ASSIGN glacct-list.last-yr[gl-month] = 0.
                cell-val = TRIM(STRING(glacct-list.last-yr[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 5  THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.last-yr[curr-i] = ? THEN ASSIGN glacct-list.last-yr[curr-i] = 0.
                    ytd-bal = ytd-bal + glacct-list.last-yr[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 6  THEN 
            DO:    
                IF glacct-list.budget[gl-month] = ? THEN ASSIGN glacct-list.budget[gl-month] = 0.
                cell-val = TRIM(STRING(glacct-list.budget[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 7  THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.budget[curr-i] = ? THEN ASSIGN glacct-list.budget[curr-i] = 0.
                    ytd-bal = ytd-bal + glacct-list.budget[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 8  THEN 
            DO:  
                IF gl-month = 1 THEN
                DO: 
                    IF glacct-list.ly-budget[12] = ? THEN ASSIGN glacct-list.ly-budget[12] = 0.
                    cell-val = TRIM(STRING(glacct-list.ly-budget[12],"->>>>>>>>>>>>>>>>9.99")). 
                END.
                ELSE
                DO: 
                    IF glacct-list.budget[gl-month - 1] = ? THEN ASSIGN glacct-list.budget[gl-month - 1] = 0.
                    cell-val = TRIM(STRING(glacct-list.budget[gl-month - 1],"->>>>>>>>>>>>>>>>9.99")). 
                END.
            END.
            WHEN 9  THEN 
            DO:    
                IF glacct-list.ly-budget[gl-month] = ? THEN ASSIGN glacct-list.ly-budget[gl-month] = 0.
                cell-val = TRIM(STRING(glacct-list.ly-budget[gl-month],"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 10 THEN 
            DO: 
                ytd-bal = 0.
                DO curr-i = 1 TO gl-month:
                    IF glacct-list.ly-budget[curr-i] = ? THEN ASSIGN glacct-list.ly-budget[curr-i] = 0.
                    ytd-bal = ytd-bal + glacct-list.ly-budget[curr-i].
                END.
                cell-val = TRIM(STRING(ytd-bal,"->>>>>>>>>>>>>>>>9.99")). 
            END.
            WHEN 11 THEN cell-val = TRIM(STRING(glacct-list.actual[1],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 12 THEN cell-val = TRIM(STRING(glacct-list.actual[2],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 13 THEN cell-val = TRIM(STRING(glacct-list.actual[3],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 14 THEN cell-val = TRIM(STRING(glacct-list.actual[4],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 15 THEN cell-val = TRIM(STRING(glacct-list.actual[5],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 16 THEN cell-val = TRIM(STRING(glacct-list.actual[6],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 17 THEN cell-val = TRIM(STRING(glacct-list.actual[7],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 18 THEN cell-val = TRIM(STRING(glacct-list.actual[8],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 19 THEN cell-val = TRIM(STRING(glacct-list.actual[9],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 20 THEN cell-val = TRIM(STRING(glacct-list.actual[10],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 21 THEN cell-val = TRIM(STRING(glacct-list.actual[11],"->>>>>>>>>>>>>>>>9.99")). 
            WHEN 22 THEN cell-val = TRIM(STRING(glacct-list.actual[12],"->>>>>>>>>>>>>>>>9.99")). 
        END CASE.

        IF found-flag AND (t-parameters.vtype = 25 OR t-parameters.vtype = 26) THEN
        DO:
            FIND FIRST temp-list WHERE temp-list.vstring = t-parameters.vstring NO-LOCK NO-ERROR.
            IF AVAILABLE temp-list THEN
            DO:
                IF t-parameters.vtype = 25 THEN cell-val = TRIM(STRING(temp-list.debit,"->>>>>>>>>>>>>>>>9.99")).
                IF t-parameters.vtype = 26 THEN cell-val = TRIM(STRING(temp-list.credit,"->>>>>>>>>>>>>>>>9.99")).
            END.
        END.

        IF found-flag THEN 
        DO: 
            IF glacct-list.acc-type = 1 OR glacct-list.acc-type = 4 THEN val-sign = - 1. 
            ELSE val-sign = 1.
            IF t-parameters.vtype GE 31 AND t-parameters.vtype LE 42 THEN
            DO:
                j = 0.
                DO i = 31 TO 42:
                    j = j + 1.
                    IF t-parameters.vtype = i THEN
                    cell-val = TRIM(STRING(val-sign * glacct-list.budget[j] ,"->>>>>>>>>>>>>>>>9.99")). 
                END.
            END.

            IF t-parameters.vtype GE 43 AND t-parameters.vtype LE 54 THEN
            DO:
                j = 0.
                DO i = 43 TO 54:
                    j = j + 1.
                    IF t-parameters.vtype = i THEN
                    cell-val = TRIM(STRING(val-sign * glacct-list.last-yr[j] ,"->>>>>>>>>>>>9.99")). 
                END.
            END.

            IF t-parameters.vtype GE 55 AND t-parameters.vtype LE 66 THEN
            DO:
                j = 0.
                DO i = 55 TO 66:
                    j = j + 1.
                    IF t-parameters.vtype = i THEN
                        cell-val = TRIM(STRING(val-sign * glacct-list.debit[j] ,"->>>>>>>>>>>>>>>>9.99")). 
                END.
            END.
        
            /*dody 201016 add keyword Last Year Budget*/
            IF t-parameters.vtype GE 67 AND t-parameters.vtype LE 78 THEN
            DO:
                j = 0.
                DO i = 67 TO 78:
                    j = j + 1.
                    IF t-parameters.vtype = i THEN
                        cell-val = TRIM(STRING(val-sign * glacct-list.ly-budget[j] ,"->>>>>>>>>>>>>>>>9.99")). 
                END.
            END.
            /*dody end*/

            IF t-parameters.vtype = 27 THEN
                ASSIGN
                    diff = glacct-list.actual[gl-month] - glacct-list.budget[gl-month]
                    cell-val = TRIM(STRING(diff,"->>>>>>>>>>>>>>>>9.99")). 
        
            IF t-parameters.vtype = 28 THEN
            DO:
                IF gl-month = 1 THEN
                    lmdiff = glacct-list.last-yr[12] - glacct-list.ly-budget[12].
                ELSE
                    lmdiff = glacct-list.actual[gl-month - 1] - glacct-list.budget[gl-month - 1].
                cell-val = TRIM(STRING(lmdiff,"->>>>>>>>>>>>>>>>9.99")). 
            END.
        END.

        IF t-parameters.vtype = 23 THEN
        DO:
            ASSIGN mtd-betrag = 0
                ytd-betrag = 0.
            FIND FIRST t-artikel WHERE t-artikel.artnr = INT(SUBSTR(t-parameters.vstring,3)) 
                AND t-artikel.departement = INT(SUBSTR(t-parameters.vstring,1,2)) NO-LOCK NO-ERROR.
            IF AVAILABLE t-artikel THEN
            DO curr-date = DATE(01,01,YEAR(to-date)) TO to-date:
                ASSIGN 
                    serv = 0
                    vat  = 0
                    n-betrag = 0.
                FIND FIRST t-umsz WHERE t-umsz.curr-date = curr-date AND t-umsz.artnr = INT(SUBSTR(t-parameters.vstring,3)) 
                    AND t-umsz.dept = INT(SUBSTR(t-parameters.vstring,1,2)) NO-LOCK NO-ERROR.
                IF AVAILABLE t-umsz THEN 
                DO:
                    n-betrag = t-umsz.betrag.
                END.
                IF curr-date GE DATE(MONTH(to-date),01,YEAR(to-date)) AND curr-date LE to-date THEN
                    mtd-betrag = mtd-betrag + n-betrag.
                ytd-betrag = ytd-betrag + n-betrag.
            END.
            cell-val = STRING(mtd-betrag).
        END.
        IF t-parameters.vtype = 24 THEN cell-val = STRING(ytd-betrag).
        
        IF cell-val NE "" THEN DO:
            IF cell-val = "0" THEN
                PUT STREAM s1 UNFORMATTED 
                    STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
            ELSE
                PUT STREAM s1 UNFORMATTED 
                    STRING(curr-row) ";" STRING(curr-col) ";" cell-val SKIP.
        END.            
        ELSE 
            PUT STREAM s1 UNFORMATTED 
                STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    END.
END.

OUTPUT STREAM s1 CLOSE.

mess-result = "Successfully generate data".


OS-COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/output_" + htl-no + ".txt " + link).
OS-DELETE VALUE ("/usr1/vhp/tmp/output_" + htl-no + ".txt").

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

  DO ind = 1 TO to-month:
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

PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 

PROCEDURE fill-segment:
    DEFINE BUFFER s-param FOR parameters.
    DEFINE VARIABLE prev-param      AS CHAR.
    DEFINE VARIABLE ytd-flag        AS LOGICAL INIT NO.
    DEFINE VARIABLE lytd-flag       AS LOGICAL INIT NO.
    DEFINE VARIABLE lmtd-flag       AS LOGICAL INIT NO.
    DEFINE VARIABLE ytd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mtd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE nr AS INT INIT 0.
    DEFINE VARIABLE segm AS INT INIT 0.
    DEFINE VARIABLE mm AS INT.
    DEFINE VARIABLE prev-segm AS INT.

    DEFINE VARIABLE tday-rev  AS DECIMAL.
    DEFINE VARIABLE tday-pers AS DECIMAL.
    DEFINE VARIABLE tday-room AS DECIMAL.
    DEFINE VARIABLE mtd-rev  AS DECIMAL.
    DEFINE VARIABLE mtd-pers AS DECIMAL.
    DEFINE VARIABLE mtd-room AS DECIMAL.
    DEFINE VARIABLE ytd-rev  AS DECIMAL.
    DEFINE VARIABLE ytd-pers AS DECIMAL.
    DEFINE VARIABLE ytd-room AS DECIMAL.

    DEFINE VARIABLE ltday-rev  AS DECIMAL.
    DEFINE VARIABLE ltday-pers AS DECIMAL.
    DEFINE VARIABLE ltday-room AS DECIMAL.
    DEFINE VARIABLE lmtd-rev  AS DECIMAL.
    DEFINE VARIABLE lmtd-pers AS DECIMAL.
    DEFINE VARIABLE lmtd-room AS DECIMAL.
    DEFINE VARIABLE lytd-rev  AS DECIMAL.
    DEFINE VARIABLE lytd-pers AS DECIMAL.
    DEFINE VARIABLE lytd-room AS DECIMAL.

    DEFINE VARIABLE btday-rev  AS DECIMAL.
    DEFINE VARIABLE btday-pers AS DECIMAL.
    DEFINE VARIABLE btday-room AS DECIMAL.
    DEFINE VARIABLE bmtd-rev  AS DECIMAL.
    DEFINE VARIABLE bmtd-pers AS DECIMAL.
    DEFINE VARIABLE bmtd-room AS DECIMAL.
    DEFINE VARIABLE bytd-rev  AS DECIMAL.
    DEFINE VARIABLE bytd-pers AS DECIMAL.
    DEFINE VARIABLE bytd-room AS DECIMAL.


    DEFINE VARIABLE do-it    AS LOGICAL  INIT NO.

    
    FOR EACH s-param WHERE s-param.progname = "GL-macro"
        AND s-param.SECTION = STRING(briefnr)
        AND NUM-ENTRIES(s-param.vstring,":") = 1 
        AND NUM-ENTRIES(s-param.varname,"-") = 3
        AND ENTRY(3,s-param.varname,"-") = "FO"
        AND SUBSTR(s-param.vstring,1,4) = "segm" NO-LOCK BY s-param.varname:

         ASSIGN
            curr-row = INTEGER(ENTRY(1, s-param.varname, "-"))
            curr-col = INTEGER(ENTRY(2, s-param.varname, "-"))
            end-row  = curr-row
            end-col  = curr-col
            do-it    = NO
         .

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

        IF ytd-flag THEN datum1 = jan1.
        ELSE datum1 = from-date.
        mm = MONTH(to-date). 

        ASSIGN 
            tday-rev    = 0  
            tday-pers   = 0
            tday-room   = 0
            mtd-rev     = 0
            mtd-pers    = 0
            mtd-room    = 0
            ltday-rev   = 0
            ltday-pers  = 0
            ltday-room  = 0
            lmtd-rev    = 0
            lmtd-pers   = 0
            lmtd-room   = 0
            lytd-rev    = 0
            lytd-pers   = 0
            lytd-room   = 0
            btday-rev   = 0
            btday-pers  = 0
            btday-room  = 0
            bmtd-rev    = 0
            bmtd-pers   = 0
            bmtd-room   = 0
            bytd-rev    = 0
            bytd-pers   = 0
            bytd-room   = 0
            ytd-rev     = 0
            ytd-pers    = 0
            ytd-room    = 0
        .

        FOR EACH genstat WHERE genstat.datum GE datum1 
            AND genstat.datum LE to-date 
            AND genstat.resstatus NE 13 
            AND genstat.segmentcode = segm
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] EQ YES NO-LOCK BY genstat.segmentcode:
    
            IF genstat.datum = to-date THEN
            DO:
                IF nr = 1 THEN tday-rev  = tday-rev  + genstat.logis.
                IF nr = 2 THEN tday-pers = tday-pers + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                IF nr = 3 THEN tday-room = tday-room + 1.
            END.
    
            IF MONTH(genstat.datum) = mm THEN
            DO:
                IF nr = 1 THEN mtd-rev  = mtd-rev  + genstat.logis.
                IF nr = 2 THEN mtd-pers = mtd-pers + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                IF nr = 3 THEN mtd-room = mtd-room + 1.
            END.

            IF nr = 1 THEN ytd-rev  = ytd-rev  + genstat.logis.
            IF nr = 2 THEN ytd-pers = ytd-pers + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
            IF nr = 3 THEN ytd-room = ytd-room + 1.

        END.

        IF s-param.vtype = 83 THEN DO:
            IF tday-rev NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(tday-rev) SKIP.
            ELSE IF tday-pers NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(tday-pers) SKIP.
            ELSE IF tday-room NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(tday-room) SKIP.
            ELSE PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.

        END.
        ELSE IF s-param.vtype = 23 THEN DO:
            IF mtd-rev NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(mtd-rev) SKIP.
            ELSE IF mtd-pers NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(mtd-pers) SKIP.
            ELSE IF mtd-room NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(mtd-room) SKIP.
            ELSE PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.

        END.
        ELSE IF s-param.vtype = 24 THEN DO:
            IF ytd-rev NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(ytd-rev) SKIP.
            ELSE IF ytd-pers NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(ytd-pers) SKIP.
            ELSE IF ytd-room NE 0 THEN
                PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(ytd-room) SKIP.
            ELSE PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.

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
                AND genstat.segmentcode = segm 
                AND genstat.nationnr NE 0
                AND genstat.zinr NE ""
                AND genstat.res-logic[2] EQ YES NO-LOCK BY genstat.segmentcode:
                

                IF genstat.datum = Lto-date THEN
                DO:
                    IF nr = 1 THEN ltday-rev  = ltday-rev  + genstat.logis.
                    IF nr = 2 THEN ltday-pers = ltday-pers + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    IF nr = 3 THEN ltday-room = ltday-room + 1.
                END.
        
                IF MONTH(genstat.datum) = mm THEN
                DO:
                    IF nr = 1 THEN lmtd-rev  = lmtd-rev  + genstat.logis.
                    IF nr = 2 THEN lmtd-pers = lmtd-pers + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                    IF nr = 3 THEN lmtd-room = lmtd-room + 1.
                END.
    
                IF nr = 1 THEN lytd-rev  = ytd-rev  + genstat.logis.
                IF nr = 2 THEN lytd-pers = ytd-pers + genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis.
                IF nr = 3 THEN lytd-room = ytd-room + 1.
            END.
    
            IF s-param.vtype = 86 THEN DO:
                IF lmtd-rev NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lmtd-rev) SKIP.
                ELSE IF lmtd-pers NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lmtd-pers) SKIP.
                ELSE IF lmtd-room NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lmtd-room) SKIP.
                ELSE PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    
            END.
            ELSE IF s-param.vtype = 87 THEN DO:
                IF lytd-rev NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lytd-rev) SKIP.
                ELSE IF lytd-pers NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lytd-pers) SKIP.
                ELSE IF lytd-room NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lytd-room) SKIP.
                ELSE PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    
            END.
        END.

        IF mtd-budget-flag OR ytd-budget-flag THEN
        DO:
            IF ytd-budget-flag THEN datum1 = jan1.
            ELSE datum1 = from-date.
    
            mm = MONTH(to-date).
            prev-segm = 0.
    
            FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
                AND segmentstat.datum LE to-date
                AND segmentstat.segmentcode = segm NO-LOCK  BY segmentstat.segmentcode:
           
    
                IF segmentstat.datum = to-date THEN
                DO:
                    IF nr = 1 THEN btday-rev  = btday-rev  + segmentstat.budlogis.
                    IF nr = 2 THEN btday-pers = btday-pers + segmentstat.budpersanz.
                    IF nr = 3 THEN btday-room = btday-room + segmentstat.budzimmeranz.
                END.
        
                IF MONTH(segmentstat.datum) = mm THEN
                DO:
                    IF nr = 1 THEN bmtd-rev  = bmtd-rev  + segmentstat.budlogis.
                    IF nr = 2 THEN bmtd-pers = bmtd-pers + segmentstat.budpersanz.
                    IF nr = 3 THEN bmtd-room = bmtd-room + segmentstat.budzimmeranz.
                END.
        
                IF nr = 1 THEN bytd-rev  = bytd-rev  + segmentstat.budlogis.
                IF nr = 2 THEN bytd-pers = bytd-pers + segmentstat.budpersanz.
                IF nr = 3 THEN bytd-room = bytd-room + segmentstat.budzimmeranz.
            END.   

            IF s-param.vtype = 84 THEN DO:
                IF bmtd-rev NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(bmtd-rev) SKIP.
                ELSE IF bmtd-pers NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(bmtd-pers) SKIP.
                ELSE IF bmtd-room NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(bmtd-room) SKIP.
                ELSE PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    
            END.
            ELSE IF s-param.vtype = 85 THEN DO:
                IF bytd-rev NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(bytd-rev) SKIP.
                ELSE IF bytd-pers NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(bytd-pers) SKIP.
                ELSE IF bytd-room NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(bytd-room) SKIP.
                ELSE PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
    
            END.
        END.             
    END.                                    
END.


PROCEDURE fill-revenue:                 
    DEFINE BUFFER s-param FOR parameters.
    DEFINE VARIABLE prev-param      AS CHAR INIT "".
    DEFINE VARIABLE ytd-flag        AS LOGICAL INIT NO.
    DEFINE VARIABLE lytd-flag       AS LOGICAL INIT NO.
    DEFINE VARIABLE lmtd-flag       AS LOGICAL INIT NO.
    DEFINE VARIABLE ytd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mtd-budget-flag AS LOGICAL INIT NO.
    DEFINE VARIABLE mm              AS INTEGER.
    DEFINE VARIABLE cell-datum      AS CHAR     INIT "".
    DEFINE VARIABLE saldo-betrag    AS DECIMAL  INIT 0.
    DEFINE VARIABLE ytd-betrag      AS DECIMAL  INIT 0.
    DEFINE VARIABLE t-betrag        AS DECIMAL  INIT 0.
    DEFINE VARIABLE lastyr-betrag   AS DECIMAL  INIT 0.
    DEFINE VARIABLE lytd-saldo      AS DECIMAL  INIT 0.
    DEFINE VARIABLE tbudget         AS DECIMAL  INIT 0.
    DEFINE VARIABLE mtd-budget      AS DECIMAL  INIT 0.
    DEFINE VARIABLE ytd-budget      AS DECIMAL  INIT 0.
    DEFINE VARIABLE do-it           AS LOGICAL  INIT NO.
    


    FOR EACH s-param WHERE s-param.progname = "GL-macro"
        AND s-param.SECTION = STRING(briefnr)
        AND NUM-ENTRIES(s-param.vstring,":") = 1 
        AND NUM-ENTRIES(s-param.varname,"-") = 3
        AND ENTRY(3,s-param.varname,"-") = "REV" NO-LOCK BY s-param.varname:

        ASSIGN
            curr-row = INTEGER(ENTRY(1, s-param.varname, "-"))
            curr-col = INTEGER(ENTRY(2, s-param.varname, "-"))
            end-row  = curr-row
            end-col  = curr-col
            do-it    = NO.
            

        IF prev-param NE s-param.varname THEN
        DO:
            ASSIGN
                prev-param = s-param.varname    
                saldo-betrag  = 0
                ytd-betrag    = 0
                t-betrag      = 0
                lastyr-betrag = 0
                lytd-saldo    = 0
                tbudget       = 0
                mtd-budget    = 0
                ytd-budget    = 0.

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

        FIND FIRST artikel WHERE artikel.artnr = INT(SUBSTR(s-param.vstring,3)) 
            AND artikel.departement = INT(SUBSTR(s-param.vstring,1,2)) NO-LOCK NO-ERROR.
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
                
                IF umsatz.datum = to-date THEN t-betrag = t-betrag + n-betrag.
                IF MONTH(umsatz.datum) = mm THEN
                    saldo-betrag = saldo-betrag + n-betrag.

                ytd-betrag = ytd-betrag + n-betrag.
            END.

            IF s-param.vtype = 23 AND do-it = NO THEN DO:
               IF saldo-betrag NE 0 THEN
                   PUT STREAM s1 UNFORMATTED 
                       STRING(curr-row) ";" STRING(curr-col) ";" STRING(saldo-betrag) SKIP.
               ELSE 
                   PUT STREAM s1 UNFORMATTED 
                       STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
               ASSIGN do-it = YES.
           END.
           ELSE IF s-param.vtype = 24 AND do-it = NO THEN DO:
               IF ytd-betrag NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(ytd-betrag) SKIP.
               ELSE 
                    PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
               ASSIGN do-it = YES.
           END.
           /*ELSE IF do-it = NO THEN DO:
               IF t-betrag NE 0 THEN
                    PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" STRING(t-betrag) SKIP.
               ELSE 
                    PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
               ASSIGN do-it = YES.
           END.*/
                     
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
                        lastyr-betrag = lastyr-betrag + n-betrag.
    
                    lytd-saldo = lytd-saldo + n-betrag.
                END.

                IF s-param.vtype = 86 AND do-it = NO THEN DO:                        
                        IF lastyr-betrag NE 0 THEN
                            PUT STREAM s1 UNFORMATTED 
                                STRING(curr-row) ";" STRING(curr-col) ";" STRING(lastyr-betrag) SKIP.
                        ELSE 
                            PUT STREAM s1 UNFORMATTED 
                                STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
                        ASSIGN do-it = YES.
                END.
                ELSE IF s-param.vtype = 87 AND do-it = NO THEN DO:
                    IF lytd-saldo NE 0 THEN
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(lytd-saldo) SKIP.
                    ELSE 
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
                    ASSIGN do-it = YES.
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
                    AND budget.datum LE to-date NO-LOCK BY budget.artnr:
                    IF budget.datum = to-date THEN
                        tbudget = tbudget + budget.betrag.
                    IF MONTH(budget.datum) = mm THEN
                        mtd-budget = mtd-budget + budget.betrag.
                    ytd-budget = ytd-budget + budget.betrag.                    
                END.

                IF s-param.vtype = 84 AND do-it = NO THEN DO:
                    IF mtd-budget NE 0 THEN
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(mtd-budget) SKIP.
                    ELSE 
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
                    ASSIGN do-it = YES.
                END.
                ELSE IF s-param.vtype = 85 AND do-it = NO THEN DO:
                    IF ytd-budget NE 0 THEN
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(ytd-budget) SKIP.
                    ELSE 
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
                    ASSIGN do-it = YES.
                END.
                /*ELSE IF do-it = NO THEN DO:     
                    MESSAGE "3" curr-row curr-col tbudget s-param.vstring VIEW-AS ALERT-BOX INFO.
                    IF tbudget NE 0 THEN
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" STRING(tbudget) SKIP.
                    ELSE 
                        PUT STREAM s1 UNFORMATTED 
                            STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.
                    ASSIGN do-it = YES.
                END.      */          
            END.    
        END.
    END.         
END.

/*sini*/
PROCEDURE fill-statistic:
DEFINE VAR key-word AS CHAR.

DEFINE VARIABLE do-it    AS LOGICAL  INIT NO.

  FOR EACH b-param WHERE b-param.progname = "GL-macro"
     AND b-param.SECTION = STRING(briefnr)
     AND NUM-ENTRIES(b-param.vstring,":") = 1 
     AND NUM-ENTRIES(b-param.varname,"-") = 3
     AND ENTRY(3,b-param.varname,"-") = "FO"
     AND SUBSTR(b-param.vstring,1,4) = "stat" NO-LOCK BY b-param.varname:

    key-word = b-param.vstring.

    ASSIGN
        curr-row = INTEGER(ENTRY(1, b-param.varname, "-"))
        curr-col = INTEGER(ENTRY(2, b-param.varname, "-"))
        end-row  = curr-row
        end-col  = curr-col
        do-it    = NO
         .
        
    
    FIND FIRST stat-list WHERE stat-list.flag = key-word NO-LOCK NO-ERROR.
    IF AVAILABLE stat-list THEN DO:
        IF stat-list.flag = "stat-nguest" THEN DO:
            MESSAGE 
                stat-list.mtd SKIP
                stat-list.ytd
                VIEW-AS ALERT-BOX INFO BUTTONS OK.
        END.
        IF b-param.vtype = 83 AND stat-list.t-day NE 0 THEN
            PUT STREAM s1 UNFORMATTED 
                    STRING(curr-row) ";" STRING(curr-col) ";" STRING(stat-list.t-day) SKIP.
        ELSE IF b-param.vtype = 23 AND stat-list.mtd NE 0 THEN
            PUT STREAM s1 UNFORMATTED 
                    STRING(curr-row) ";" STRING(curr-col) ";" STRING(stat-list.mtd) SKIP.
        ELSE IF b-param.vtype = 24 AND stat-list.ytd NE 0 THEN
            PUT STREAM s1 UNFORMATTED 
                    STRING(curr-row) ";" STRING(curr-col) ";" STRING(stat-list.ytd) SKIP.
        ELSE PUT STREAM s1 UNFORMATTED 
                        STRING(curr-row) ";" STRING(curr-col) ";" "''" SKIP.

    END.

  END.
END.


/*ragung */

PROCEDURE create-rev-list:
DEFINE VARIABLE t-day            AS DECIMAL.
DEFINE VARIABLE mtd              AS DECIMAL.
DEFINE VARIABLE mtd-budget       AS DECIMAL.
DEFINE VARIABLE ytd              AS DECIMAL.
DEFINE VARIABLE ytd-budget       AS DECIMAL.
DEFINE VARIABLE variance         AS DECIMAL.
DEFINE VARIABLE ct1              AS INTEGER.

    FOR EACH artikel WHERE (artikel.artart EQ 0 OR artikel.artart EQ 8) AND umsatzart EQ 1 AND artikel.departement EQ 0 NO-LOCK:
        DO curr-date = from-date TO to-date: 
        ASSIGN 
            serv = 0
            vat  = 0.
        
            FIND FIRST umsatz WHERE umsatz.datum = curr-date 
              AND umsatz.artnr = artikel.artnr AND umsatz.departement = artikel.departement NO-LOCK NO-ERROR. 
            IF AVAILABLE umsatz THEN 
        
              RUN calc-servtaxesbl.p(1, umsatz.artnr, umsatz.departement,
                                     umsatz.datum, OUTPUT serv, OUTPUT vat, OUTPUT vat2, OUTPUT fact).
        
            fact = 1.00 + serv + vat + vat2.
        
            d-flag = AVAILABLE umsatz AND (MONTH(umsatz.datum) = MONTH(to-date))
              AND (YEAR(umsatz.datum) = YEAR(to-date)).
        
            n-betrag = 0. 
            IF AVAILABLE umsatz THEN 
            DO: 
              IF foreign-flag THEN 
              DO:  
                RUN find-exrate(curr-date). 
                IF AVAILABLE exrate THEN frate = exrate.betrag. 
              END. 
        
              ASSIGN
                n-betrag = umsatz.betrag / (fact * frate) 
                n-serv   = n-betrag * serv
                n-tax    = n-betrag * vat.
        
              IF umsat.datum = to-date THEN
              ASSIGN t-day      = t-day + n-betrag.
        
              IF price-decimal = 0 THEN 
              DO:
                ASSIGN 
                  n-betrag = ROUND(n-betrag, 0)
                  n-serv = ROUND(n-serv, 0)
                  n-tax = ROUND(n-tax, 0).
              END.
            END. 
        
            FIND FIRST budget WHERE budget.artnr = artikel.artnr 
            AND budget.departement = artikel.departement 
            AND budget.datum = curr-date NO-LOCK NO-ERROR.
        
            IF curr-date LT from-date THEN 
            DO: 
              IF AVAILABLE umsatz THEN 
                  ASSIGN ytd       = ytd + n-betrag.
              IF AVAILABLE budget THEN 
                  ASSIGN ytd-budget = ytd-budget + budget.betrag. 
            END.    
            ELSE DO:
                  IF AVAILABLE umsatz THEN 
                  DO: 
                    IF ytd-flag THEN 
                        ASSIGN ytd = ytd + n-betrag. 
                    IF MONTH(curr-date) = MONTH(to-date) THEN 
                        ASSIGN mtd      = mtd + mon-saldo[DAY(umsatz.datum)] + n-betrag.
                  END. 
        
                  IF AVAILABLE budget THEN 
                  DO: 
                    mtd-budget = mtd-budget + budget.betrag.   
                  END. 
            END.
            ASSIGN variance = mtd - mtd-budget.
        END.  
        ct1 = ct1 + 1.
        CREATE rev-list.
        ASSIGN rev-list.ct           = ct
               rev-list.flag         = "Room"
               rev-list.departement  = 0
               rev-list.t-day        = t-day
               rev-list.mtd          = mtd
               rev-list.mtd-budget   = mtd-budget
               rev-list.ytd          = ytd
               rev-list.ytd-budget   = ytd-budget
               rev-list.descr        = artikel.bezeich.
 

    END.
END.

PROCEDURE fill-tot-room:

DEFINE VARIABLE datum          AS DATE.
DEFINE VARIABLE anz             AS INTEGER. 
DEFINE VARIABLE anz0            AS INTEGER.
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
  ct1 = ct1 + 1.   
  FIND FIRST stat-list WHERE stat-list.flag EQ "stat-tot-rm" NO-LOCK NO-ERROR.
  IF NOT AVAILABLE stat-list THEN DO:
          CREATE stat-list.
          ASSIGN stat-list.ct       = ct1
                 stat-list.descr    = "Total Room"
                 stat-list.flag     = "stat-tot-rm".
          DO datum = datum1 TO to-date: 
              FIND FIRST zinrstat WHERE zinrstat.datum = datum
                AND zinrstat.zinr = "tot-rm" NO-LOCK NO-ERROR.
              IF AVAILABLE zinrstat THEN anz = zinrstat.zimmeranz.
              ELSE anz = anz0.
            
              d-flag = AVAILABLE zinrstat AND (MONTH(zinrstat.datum) = MONTH(to-date))
                AND (YEAR(zinrstat.datum) = YEAR(to-date)).
              IF AVAILABLE zinrstat  THEN
              IF d-flag THEN stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zinrstat.datum)] + anz.
              
              IF datum = to-date THEN stat-list.t-day = stat-list.t-day + anz. 
              IF from-date NE ? THEN
              DO:
                IF (datum LT from-date) AND (datum GE from-date) 
                  THEN stat-list.ytd = stat-list.ytd + anz. 
                ELSE 
                DO: 
                  IF ytd-flag AND (datum GE from-date) THEN 
                    stat-list.ytd = stat-list.ytd + anz. 
                END.
              END.
              ELSE
              DO:
                IF (datum LT from-date) THEN stat-list.ytd = stat-list.ytd + anz. 
                ELSE 
                DO: 
                  IF ytd-flag THEN stat-list.ytd = stat-list.ytd + anz. 
                END.
              END.
                
              /*IF MONTH(datum) = MONTH(to-date) THEN DO:
                  FIND FIRST setup-stat WHERE setup-stat.descr EQ "Total Room" NO-LOCK NO-ERROR.
                  IF AVAILABLE setup-stat THEN DO:
                     FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
                        AND budget.departement = 0 AND budget.datum = datum NO-LOCK NO-ERROR.
                     IF AVAILABLE budget THEN DO:                     
                         stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
                     END.                         
                  END.
              END.*/
          END.
  END.
END.
                  
PROCEDURE fill-tot-avail:
    ct1 = ct1 + 1.   
    FIND FIRST stat-list WHERE stat-list.flag EQ "stat-act-rm" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE stat-list THEN DO:
    CREATE stat-list.
    ASSIGN stat-list.ct       = ct1  
           stat-list.descr    = "Room Available"
           stat-list.flag     = "stat-act-rm".

                FOR EACH zkstat WHERE zkstat.datum GE datum1 AND zkstat.datum LE to-date NO-LOCK: 
          IF zkstat.datum = to-date THEN stat-list.t-day = stat-list.t-day + zkstat.anz100. 
          IF zkstat.datum LT from-date THEN 
            stat-list.ytd = stat-list.ytd + zkstat.anz100. 
          ELSE 
          DO: 
            IF ytd-flag THEN stat-list.ytd = stat-list.ytd + zkstat.anz100. 
          END. 
          IF MONTH(zkstat.datum) = MONTH(to-date) AND YEAR(zkstat.datum) = YEAR(to-date) THEN
            stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zkstat.datum)] + zkstat.anz100.
        END.

        /*FIND FIRST setup-stat WHERE setup-stat.descr EQ "Rooms Available" NO-LOCK NO-ERROR.
        IF AVAILABLE setup-stat THEN DO:
            FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
            AND budget.departement = 0
            AND budget.datum = datum1 NO-LOCK NO-ERROR.
            IF datum1 LT from-date THEN .
            ELSE DO:
            IF AVAILABLE budget THEN 
                 DO: 
                   stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag. 
                 END.
            END.
        END.*/
    END.  
END.

PROCEDURE fill-inactive:
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
    ct1 = ct1 + 1.   
    FIND FIRST stat-list WHERE stat-list.flag EQ "tot-inactive" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE stat-list THEN DO:
        CREATE stat-list.
        ASSIGN stat-list.ct       = ct1  
               stat-list.descr    = "InactiveRoom"
               stat-list.flag     = "tot-inactive".  
        
        FOR EACH b-stat-list NO-LOCK:
            IF b-stat-list.flag EQ "tot-rm"  THEN 
                ASSIGN tday1 = b-stat-list.t-day 
                       mtd1  = b-stat-list.mtd
                       ytd1  = b-stat-list.ytd.
            
            IF b-stat-list.flag EQ "tot-rmavail"  THEN 
                ASSIGN tday2 = b-stat-list.t-day
                       mtd2  = b-stat-list.mtd
                       ytd2  = b-stat-list.ytd.
        

       END.
       ASSIGN stat-list.t-day =  tday1 - tday2
              stat-list.mtd   =  mtd1 - mtd2 
              stat-list.ytd   =  ytd1 - ytd2.
    END.
END.

PROCEDURE fill-rmstat:
DEFINE INPUT PARAMETER key-word AS CHAR.
DEFINE VARIABLE datum         AS DATE.
DEFINE VARIABLE anz             AS INTEGER. 
DEFINE VARIABLE anz0            AS INTEGER.
DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE cur-key         AS CHAR.
/* DEFINE VARIABLE cur-key1        AS CHAR.  */
  ct1 = ct1 + 1.
  FIND FIRST stat-list WHERE stat-list.flag EQ key-word NO-LOCK NO-ERROR.
  IF NOT AVAILABLE stat-list THEN DO:
  CREATE stat-list.
  ASSIGN stat-list.ct       = ct1.

  IF key-word = "ooo" THEN 
      ASSIGN stat-list.descr = "Out of Order Rooms"
             stat-list.flag  = "stat-ooo".
  ELSE IF key-word = "oos" THEN 
      ASSIGN stat-list.descr = "Rooms Occupied"
             stat-list.flag  = "stat-ooc".
  ELSE IF key-word = "dayuse" THEN 
      ASSIGN stat-list.descr = "Day Use"
             stat-list.flag  = "stat-day-use".
  ELSE IF key-word = "No-Show" THEN 
      ASSIGN stat-list.descr = "No Show"
             stat-list.flag  = "stat-noshow".
  ELSE IF key-word = "arrival-WIG" THEN 
      ASSIGN stat-list.descr = "Walk in Guest"
             stat-list.flag  = "stat-rm-wig".
  ELSE IF key-word = "NewRes" THEN 
      ASSIGN stat-list.descr = "Reservation Made Today"
             stat-list.flag  = "stat-newres".
  ELSE IF key-word = "CancRes" THEN 
      ASSIGN stat-list.descr = "Cancellation For Today"
             stat-list.flag  = "stat-cancel".
  ELSE IF key-word = "Early-CO" THEN 
      ASSIGN stat-list.descr = "Early Check Out"
             stat-list.flag  = "stat-earco".
  ELSE IF key-word = "arrival" THEN 
      ASSIGN stat-list.descr = "Room Arrivals"
             stat-list.flag  = "stat-rm-arr".
  ELSE IF key-word = "pers-arrival" THEN DO:
      ASSIGN cur-key         = "pers-arrival"
             key-word        = "arrival"
             stat-list.descr = "Person Arrivals"
             stat-list.flag  = "stat-prs-arr".
  END.
  ELSE IF key-word = "departure" THEN 
      ASSIGN stat-list.descr = "Room Departures"
             stat-list.flag  = "stat-rm-dep".
  ELSE IF key-word = "pers-depature" THEN DO:
      ASSIGN cur-key         = "pers-depature"
             key-word        = "departure"
             stat-list.descr = "Person Depatures"
             stat-list.flag  = "stat-prs-dep".
  END.  
  ELSE IF key-word = "ArrTmrw" THEN 
      ASSIGN stat-list.descr = "Room Arrivals Tomorrow"
             stat-list.flag  = "stat-rm-arrtmr".
  ELSE IF key-word = "pers-ArrTmrw" THEN DO:
      ASSIGN cur-key         = "pers-ArrTmrw"
             key-word        = "ArrTmrw"
             stat-list.descr = "Person Arrivals Tomorrow"
             stat-list.flag  = "stat-prs-arrtmr".
  END. 
  ELSE IF key-word = "DepTmrw" THEN 
      ASSIGN stat-list.descr = "Room Departures Tomorrow"
             stat-list.flag  = "stat-rm-deptmr".
  ELSE IF key-word = "pers-DepTmrw" THEN DO:
      ASSIGN cur-key         = "pers-DepTmrw"
             key-word        = "DepTmrw"
             stat-list.descr = "Person Departures Tomorrow".
  END. 
  ELSE IF key-word = "arrival-RSV" THEN DO:
    ASSIGN stat-list.descr = "Room Arrivals (Resv)"
           stat-list.flag  = "stat-rm-rsv".
  END.

      FOR EACH zinrstat WHERE zinrstat.datum GE datum1 
      AND zinrstat.datum LE to-date 
      AND zinrstat.zinr = key-word NO-LOCK: 
      
      d-flag = (MONTH(zinrstat.datum) = MONTH(to-date))
               AND (YEAR(zinrstat.datum) = YEAR(to-date)).

          IF d-flag THEN DO: 
             IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zinrstat.datum)] + zinrstat.personen. 
             ELSE stat-list.mtd = stat-list.mtd + mon-saldo[DAY(zinrstat.datum)] + zinrstat.zimmeranz.
    
          END.
          /*IF (MONTH(zinrstat.datum) = MONTH(to-date))
               AND (YEAR(zinrstat.datum) = YEAR(to-date)) THEN DO: 
          IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.mtd = stat-list.mtd + zinrstat.personen. 
          ELSE stat-list.mtd = stat-list.mtd  + zinrstat.zimmeranz.
          END.*/

          IF zinrstat.datum = to-date THEN DO: 
             IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.t-day = stat-list.t-day + zinrstat.personen.
             ELSE stat-list.t-day = stat-list.t-day + zinrstat.zimmeranz. 
          END.
          IF zinrstat.datum LT from-date THEN DO:
             IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.ytd = stat-list.ytd + zinrstat.personen.
             ELSE stat-list.ytd = stat-list.ytd + zinrstat.zimmeranz.    
          END.
          ELSE 
          DO: 
            IF ytd-flag THEN DO:
              IF SUBSTR(cur-key,1,4) EQ "pers" THEN stat-list.ytd = stat-list.ytd + zinrstat.personen.
              ELSE stat-list.ytd = stat-list.ytd + zinrstat.zimmeranz.  
            END.
          END. 
      END.

      /*FOR EACH setup-stat NO-LOCK:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.

        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               IF setup-stat.descr = "OOO Room" AND key-word = "ooo" THEN stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
               ELSE IF setup-stat.descr = "Rooms Occupied" AND key-word = "occ" THEN stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.
      END.*/
  END.    
END.

PROCEDURE fill-rmocc: 
    DEFINE VARIABLE curr-date       AS DATE. 
    DEFINE VARIABLE datum1          AS DATE. 
    DEFINE VARIABLE datum2          AS DATE. 
    DEFINE VARIABLE d-flag          AS LOGICAL NO-UNDO.
    DEFINE VARIABLE dbudget-flag    AS LOGICAL NO-UNDO.
    DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
    DEFINE VARIABLE frate1          AS DECIMAL NO-UNDO.

    IF ytd-flag THEN datum1 = jan1. 
    ELSE datum1 = from-date. 
    
    ct1 = ct1 + 1.
    CREATE stat-list.
    ASSIGN stat-list.ct    = ct1
           stat-list.descr = "Rooms Occupied"
           stat-list.flag  = "stat-occ-rm".
        
    FOR EACH genstat WHERE
      genstat.datum GE datum1 AND genstat.datum LE to-date
      AND genstat.resstatus NE 13 /*AND genstat.segmentcode NE 0*/
      /*AND genstat.res-int[1] NE 13*/
      AND genstat.nationnr NE 0
      AND genstat.segmentcode NE 0
      AND genstat.nationnr NE 0
      AND genstat.zinr NE ""
      AND genstat.res-logic[2] EQ YES /*MU 27032012 sleeping = yes */
      USE-INDEX nat_ix NO-LOCK
      BY genstat.segmentcode:
  
      d-flag = (MONTH(genstat.datum) = MONTH(to-date))
          AND (YEAR(genstat.datum) = YEAR(to-date)).

      IF genstat.datum = to-date THEN 
      DO:         
          stat-list.t-day = stat-list.t-day + 1.
      END. 
      IF MONTH(genstat.datum) EQ MONTH(to-date) AND YEAR(genstat.datum) EQ YEAR(to-date) THEN
      DO:
         stat-list.mtd = stat-list.mtd + 1.
      END.
      IF ytd-flag THEN 
      DO: 
         stat-list.ytd = stat-list.ytd + 1. 
      END.
    END. 

     /*FIND FIRST setup-stat WHERE setup-stat.descr EQ "Rooms Occupied" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
         FOR EACH budget WHERE budget.artnr = setup-stat.artnr
         AND budget.departement = 0 
         AND budget.datum GE from-date
         AND budget.datum LE to-date NO-LOCK:
             stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
         END.
     END.*/
END.

PROCEDURE fill-stat:
DEFINE INPUT PARAMETER key-word AS CHAR.
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
 ct1 = ct1 + 1.
 FIND FIRST stat-list WHERE stat-list.flag EQ key-word NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = key-word.

     IF key-word = "vacant" THEN ASSIGN stat-list.descr = "Vacant Rooms".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "tot-rmavail"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "ooo"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.

        IF b-stat-list.flag EQ "occ"  THEN 
            ASSIGN tday3 = b-stat-list.t-day
                   mtd3  = b-stat-list.mtd
                   ytd3  = b-stat-list.ytd.


     END.

     ASSIGN stat-list.t-day =  tday1 - tday2 - tday3
            stat-list.mtd   =  mtd1 - mtd2 - mtd3
            stat-list.ytd   =  ytd1 - ytd2 - ytd3.

     /*FIND FIRST setup-stat WHERE setup-stat.descr = "Vacant Rooms" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FOR EACH budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum GE from-date
        AND budget.datum GE to-date NO-LOCK:
            stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
        END.   
     END.*/
 END.
END.

PROCEDURE fill-segm :
DEFINE INPUT PARAMETER key-word AS CHAR.

DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE mm AS INTEGER.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.
DEFINE VARIABLE comp-tday     AS INTEGER.

    mm = MONTH(to-date).
    /*saldo*/
    ct1 = ct1 + 1.

    IF key-word = "HSE" THEN
        FIND FIRST segment WHERE segment.betriebsnr = 2 NO-LOCK NO-ERROR.
    ELSE IF key-word = "COM" THEN
        FIND FIRST segment WHERE segment.betriebsnr = 1 NO-LOCK NO-ERROR.
    ELSE IF key-word = "COM-GS" THEN
        FIND FIRST segment WHERE segment.betriebsnr = 1 NO-LOCK NO-ERROR.

    IF AVAILABLE segment THEN DO:
        CREATE stat-list.
        ASSIGN stat-list.ct      = ct1.

        IF key-word EQ "HSE" THEN
            ASSIGN  stat-list.descr   = "House Uses"
                    stat-list.flag    = "stat-rrom-91".
        ELSE IF key-word EQ "COM" THEN 
            ASSIGN  stat-list.descr   = "Complimentary"
                    stat-list.flag    = "stat-rrom-90".
        ELSE IF key-word EQ "COM-GS" THEN 
            ASSIGN  stat-list.descr   = "Complimentary Guest"
                    stat-list.flag    = "stat-numcompl".

        FOR EACH genstat WHERE genstat.segmentcode = segment.segmentcode
          AND genstat.datum GE datum1 
          AND genstat.datum LE to-date 
          AND genstat.resstatus NE 13 
          /*AND genstat.gratis EQ 0 */
          AND genstat.segmentcode NE 0 
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] EQ YES NO-LOCK:
            
            IF foreign-flag THEN 
            DO: 
              RUN find-exrate(genstat.datum). 
              IF AVAILABLE exrate THEN frate = exrate.betrag. 
            END. 

            d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                 AND (YEAR(genstat.datum) = YEAR(to-date)).
                
            IF genstat.datum = to-date THEN DO:
                IF key-word EQ "COM-GS" THEN
                    stat-list.t-day = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
                ELSE stat-list.t-day = stat-list.t-day + 1. 
            END.
            
            IF MONTH(genstat.datum) = mm THEN DO:
                IF key-word EQ "COM-GS" THEN
                stat-list.mtd = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
                ELSE stat-list.mtd = stat-list.mtd + mon-saldo[DAY(genstat.datum)] + 1.    
            END.
            IF key-word EQ "COM-GS" THEN
                stat-list.mtd = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.kind3.
            ELSE stat-list.ytd = stat-list.ytd + 1.
        END.

        /*FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
        AND segmentstat.datum LE to-date 
        AND segmentstat.segmentcode = segment-list.segmentcode NO-LOCK:
        
            IF MONTH(segmentstat.datum) = mm THEN DO:
                stat-list.mtd-budget = stat-list.mtd-budget + mon-budget[DAY(segmentstat.datum)] + segmentstat.budzimmeranz.
            END.
            
            stat-list.ytd-budget = stat-list.ytd-budget + segmentstat.budzimmeranz.

        END.*/

    END.
END.


PROCEDURE fill-comproomnew :

DEFINE VARIABLE d-flag         AS LOGICAL NO-UNDO.
DEFINE VARIABLE mm AS INTEGER.
DEFINE VARIABLE frate1         AS DECIMAL NO-UNDO.

    mm = MONTH(to-date).
    /*saldo*/
    ct1 = ct1 + 1.

        CREATE stat-list.
        ASSIGN stat-list.ct      = ct1
               stat-list.flag    = "Compl" 
               stat-list.descr   = "Complimentary Paying Guest".

        FOR EACH genstat WHERE genstat.datum GE datum1
            AND genstat.datum LE to-date
            AND genstat.zipreis = 0
            AND genstat.gratis = 0
            AND genstat.resstatus = 6 
            AND genstat.res-logic[3] NO-LOCK, 
            FIRST segment WHERE segment.segmentcode = genstat.segmentcode NO-LOCK:
                
            IF segment.betriebsnr = 0 THEN
            DO:
                IF foreign-flag THEN 
                DO: 
                  RUN find-exrate(genstat.datum). 
                  IF AVAILABLE exrate THEN frate = exrate.betrag. 
                END. 
    
                d-flag = (MONTH(genstat.datum) = MONTH(to-date))
                     AND (YEAR(genstat.datum) = YEAR(to-date)).
                    
                IF genstat.datum = to-date THEN DO:
                    stat-list.t-day = stat-list.t-day + 1.   
                END.
                
                IF MONTH(genstat.datum) = mm THEN DO:
                    stat-list.mtd = stat-list.mtd + mon-saldo[DAY(genstat.datum)] + 1.    
            END.

            stat-list.ytd = stat-list.ytd + 1.
            END.
        END.
END.

PROCEDURE fill-roomsold :
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "rmsold" NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "rmsold"
            stat-list.descr    = "Rooms Sold".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "stat-rrom-91"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "stat-rrom-90"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.

        IF b-stat-list.flag EQ "stat-occ-rm"  THEN 
            ASSIGN tday3 = b-stat-list.t-day
                   mtd3  = b-stat-list.mtd
                   ytd3  = b-stat-list.ytd.


     END.
    
        
     ASSIGN stat-list.t-day =  tday1 + tday2 + tday3
            stat-list.mtd   =  mtd1 + mtd2 + mtd3
            stat-list.ytd   =  ytd1 + ytd2 + ytd3.
    
     /*FIND FIRST setup-stat WHERE setup-stat.descr = "Room Sold" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.*/
 END.
END.

PROCEDURE fill-occ-pay :
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "occpay" NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "occ-pay"
            stat-list.descr    = "% Occupancy (Paying)".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "tot-rm"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "rmsold"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday2 / tday1) * 100
            stat-list.mtd   =  (mtd2 / mtd1) * 100 
            stat-list.ytd   =  (ytd2 / ytd1) * 100.
    
     /*FIND FIRST setup-stat WHERE setup-stat.descr = "% Occupancy" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.*/
 END.
END.

PROCEDURE fill-occ-comp-hu :
DEFINE VARIABLE tday1 AS INT.
DEFINE VARIABLE tday2 AS INT.
DEFINE VARIABLE tday3 AS INT.
DEFINE VARIABLE mtd1  AS INT.
DEFINE VARIABLE mtd2  AS INT.
DEFINE VARIABLE mtd3  AS INT.
DEFINE VARIABLE ytd1  AS INT.
DEFINE VARIABLE ytd2  AS INT.
DEFINE VARIABLE ytd3  AS INT.
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "occ-comp-hu" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "occ-comp-hu"
            stat-list.descr    = "% Occupancy (Comp + HU)".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "occ"  THEN 
            ASSIGN tday1 = b-stat-list.t-day 
                   mtd1  = b-stat-list.mtd
                   ytd1  = b-stat-list.ytd.
        
        IF b-stat-list.flag EQ "tot-rm"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday1 / tday2) * 100
            stat-list.mtd   =  (mtd1 / mtd2) * 100 
            stat-list.ytd   =  (ytd1 / ytd2) * 100.

     /*FIND FIRST setup-stat WHERE setup-stat.descr = "% Occupancy with Comp and HU" NO-LOCK NO-ERROR.
     IF AVAILABLE setup-stat THEN DO:
        FIND FIRST budget WHERE budget.artnr = setup-stat.artnr
        AND budget.departement = 0 
        AND budget.datum = curr-date NO-LOCK NO-ERROR.
    
        IF curr-date LT from-date THEN .
        ELSE DO:
        IF AVAILABLE budget THEN 
            DO: 
               stat-list.mtd-budget = stat-list.mtd-budget + budget.betrag.
            END.
        END.   
     END.*/
 END.
END.

PROCEDURE fill-tot-rev:
DEFINE VARIABLE tday1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday3 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.
    FIND FIRST stat-list WHERE stat-list.flag EQ "tot-rev" NO-LOCK NO-ERROR.
    IF NOT AVAILABLE stat-list THEN DO:
         CREATE stat-list.
         ASSIGN stat-list.ct       = ct1
                stat-list.flag     = "stat-tot-rev"
                stat-list.descr    = "Total Room Revenue".

         FIND FIRST rev-list WHERE rev-list.flag = "Room" AND rev-list.descr MATCHES "*Room Revenue*" NO-LOCK NO-ERROR.
         IF AVAILABLE rev-list THEN DO:

            ASSIGN
                stat-list.t-day        = rev-list.t-day            
                stat-list.mtd          = rev-list.mtd        
                stat-list.ytd          = rev-list.ytd        
                stat-list.mtd-budget   = rev-list.mtd-budget.    
         END.
    END.
END.



PROCEDURE fill-avg-rmrate-rp :

DEFINE VARIABLE tday1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday3 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "avg-rmrate-rp" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "avg-rmrate-rp"
            stat-list.descr    = "Average Room Rate Rp.".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "rmsold"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     FIND FIRST b-stat WHERE b-stat.flag EQ "stat-tot-rev" NO-LOCK NO-ERROR.
     IF AVAILABLE b-stat THEN DO:
        ASSIGN
            tday1 = b-stat.t-day            
            mtd1  = b-stat.mtd        
            ytd1  = b-stat.ytd.        
     END.


     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday1 / tday2)
            stat-list.mtd   =  (mtd1 / mtd2) 
            stat-list.ytd   =  (ytd1 / ytd2).
 END.
END.


PROCEDURE fill-avg-rmrate-frg :
DEFINE VARIABLE tday1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday3 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd3  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.
FIND FIRST stat-list WHERE stat-list.flag EQ "avg-rmrate-frg" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "avg-rmrate-frg" 
            stat-list.descr    = "Average Room Rate US$".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "rmsold"  THEN 
            ASSIGN tday2 = b-stat-list.t-day
                   mtd2  = b-stat-list.mtd
                   ytd2  = b-stat-list.ytd.
     END.
     
     FIND FIRST rev-list NO-LOCK NO-ERROR.
     IF AVAILABLE rev-list THEN DO:

         RUN find-exrate(to-date). 
         IF AVAILABLE exrate THEN frate = exrate.betrag. 
        
        
         ASSIGN tday1 = rev-list.t-day / (fact * frate)
                mtd1  = rev-list.mtd / (fact * frate)
                ytd1  = rev-list.ytd / (fact * frate).
     END.
    
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day =  (tday1 / tday2) / foreign-curr
            stat-list.mtd   =  (mtd1 / mtd2) / foreign-curr
            stat-list.ytd   =  (ytd1 / ytd2) / foreign-curr.

     
 END.
END.

PROCEDURE fill-revpar:
DEFINE VARIABLE tday1       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE tday2       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd-budget1 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE mtd-budget2 AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd1        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
DEFINE VARIABLE ytd2        AS DECIMAL FORMAT "->,>>>,>>>,>>9.99".
ct1 = ct1 + 1.           
FIND FIRST stat-list WHERE stat-list.flag EQ "revpar" NO-LOCK NO-ERROR.
IF NOT AVAILABLE stat-list THEN DO:
     CREATE stat-list.
     ASSIGN stat-list.ct       = ct1
            stat-list.flag     = "revpar" 
            stat-list.descr    = "Revenue Per Available Room / Revpar".      
     
     FOR EACH b-stat-list NO-LOCK:
        IF b-stat-list.flag EQ "tot-rmav"  THEN 
            ASSIGN tday2       = b-stat-list.t-day
                   mtd2        = b-stat-list.mtd
                   mtd-budget2 = b-stat-list.mtd-budget 
                   ytd2        = b-stat-list.ytd.
     END.
     
     FIND FIRST rev-list WHERE rev-list.descr EQ "TOTAL ROOM REVENUE" NO-LOCK NO-ERROR.
     IF AVAILABLE rev-list THEN DO:
         ASSIGN tday1       = rev-list.t-day
                mtd1        = rev-list.mtd
                mtd-budget1 = rev-list.mtd-budget
                ytd1        = rev-list.ytd.
     END.
        
     IF mtd-budget1 NE 0 AND mtd-budget2 NE 0 THEN
     stat-list.mtd-budget    =  (mtd-budget1 / mtd-budget2).
        
     IF tday2 NE 0 OR mtd2 NE 0 OR ytd2 NE 0 THEN
     ASSIGN stat-list.t-day         =  (tday1 / tday2)
            stat-list.mtd           =  (mtd1 / mtd2) 
            stat-list.ytd           =  (ytd1 / ytd2).
 END.
END.

PROCEDURE fill-gs-inhouse:
DEFINE VARIABLE datum1          AS DATE. 
DEFINE VARIABLE datum2          AS DATE. 
DEFINE VARIABLE curr-date       AS DATE. 
DEFINE VARIABLE ly-currdate     AS DATE.
DEFINE VARIABLE d-flag          AS LOGICAL.
DEFINE VARIABLE dbudget-flag    AS LOGICAL.
DEFINE VARIABLE dlmtd-flag      AS LOGICAL NO-UNDO.
DEFINE VARIABLE frate1          AS DECIMAL NO-UNDO.
  IF ytd-flag THEN datum1 = jan1. 
  ELSE datum1 = from-date. 

 ct1 = ct1 + 1.  

 FIND FIRST stat-list WHERE stat-list.flag = "stat-nguest" NO-LOCK NO-ERROR.
 IF NOT AVAILABLE stat-list THEN DO:
    CREATE stat-list.
    ASSIGN  stat-list.ct       = ct1
            stat-list.flag     = "stat-nguest" 
            stat-list.descr    = "Guest In House".
    FOR EACH segmentstat WHERE segmentstat.datum GE datum1 
     AND segmentstat.datum LE to-date 
     AND segmentstat.segmentcode = segment.segmentcode NO-LOCK: 
         frate = 1.
         IF foreign-flag THEN 
         DO: 
          RUN find-exrate(segmentstat.datum). 
          IF AVAILABLE exrate THEN frate = exrate.betrag. 
         END. 
        
         d-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
            AND (YEAR(segmentstat.datum) = YEAR(to-date)).
         dbudget-flag = (MONTH(segmentstat.datum) = MONTH(to-date))
            AND (YEAR(segmentstat.datum) = YEAR(to-date)).   
    
         IF segmentstat.datum = to-date THEN 
         DO: 
            stat-list.t-day = segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
         END.
         
         IF MONTH(segmentstat.datum) = MONTH(to-date) THEN DO:
             stat-list.mtd = stat-list.mtd + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
         END.

         IF segmentstat.datum LT from-date THEN 
         stat-list.ytd = stat-list.ytd + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis.
         ELSE 
         DO: 
         IF ytd-flag THEN stat-list.ytd = stat-list.ytd + segmentstat.persanz 
                + segmentstat.kind1 + segmentstat.kind2 + segmentstat.gratis. 
         END.
     END.
 END.
END.


PROCEDURE calc-CF:
DEFINE VARIABLE from-lsyr   AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE to-lsyr     AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE Pfrom-date  AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE Pto-date    AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE from-month  AS DATE NO-UNDO INIT ?.
DEFINE VARIABLE from-year   AS DATE NO-UNDO INIT ?.
    
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

    /*geral D5D0FB debit - credit MTD & YTD*/
    IF from-month = ? THEN from-month = DATE(MONTH(to-date), 1, YEAR(to-date)).
    IF from-year  = ? THEN from-year  = DATE(1, 1, YEAR(to-date)).
    
    RUN glacct-cashflow_1bl.p(from-date, to-date, from-lsyr, to-lsyr, 
        Pfrom-date, Pto-date, from-month, from-year, TABLE coa-list, OUTPUT TABLE t-list).
END.


