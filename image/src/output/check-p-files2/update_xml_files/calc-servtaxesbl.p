
DEF INPUT PARAMETER i-case       AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-artNo    AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-deptNo   AS INTEGER NO-UNDO.
DEF INPUT PARAMETER inp-date     AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER service     AS DECIMAL NO-UNDO INIT 0.
DEF OUTPUT PARAMETER vat         AS DECIMAL NO-UNDO INIT 0.
DEF OUTPUT PARAMETER vat2        AS DECIMAL NO-UNDO INIT 0.
DEF OUTPUT PARAMETER fact-scvat  AS DECIMAL NO-UNDO INIT 1.

/*
DEF VARIABLE i-case       AS INTEGER NO-UNDO INIT 1.
DEF VARIABLE inp-artNo    AS INTEGER NO-UNDO INIT 102.
DEF VARIABLE inp-deptNo   AS INTEGER NO-UNDO INIT 0.
DEF VARIABLE inp-date     AS DATE    NO-UNDO INIT 06/21/2015.
DEF VARIABLE service      AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE vat          AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE vat2         AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE fact-scvat   AS DECIMAL NO-UNDO INIT 1.
*/
DEF VARIABLE service-code        AS INTEGER NO-UNDO.
DEF VARIABLE tax-code            AS INTEGER NO-UNDO.
DEF VARIABLE vat-code            AS INTEGER NO-UNDO.
DEF VARIABLE bill-date           AS DATE    NO-UNDO.
DEF VARIABLE serv-vat            AS LOGICAL NO-UNDO. 
DEF VARIABLE tax-vat             AS LOGICAL NO-UNDO. 
DEF VARIABLE ct                  AS CHAR    NO-UNDO.
DEF VARIABLE l-deci              AS INTEGER NO-UNDO INIT 2.
DEF VARIABLE rm-serv             AS LOGICAL NO-UNDO.
DEF VARIABLE rm-vat              AS LOGICAL NO-UNDO.
DEF VARIABLE incl-service        AS LOGICAL NO-UNDO. 
DEF VARIABLE incl-mwst           AS LOGICAL NO-UNDO. 
DEF VARIABLE returnFlag          AS LOGICAL NO-UNDO INIT NO.


FIND FIRST artikel WHERE artikel.artnr = inp-artNo
    AND artikel.departement = inp-deptNo NO-LOCK NO-ERROR.
IF NOT AVAILABLE artikel THEN RETURN.
ASSIGN
    service-code = artikel.service-code
    tax-code     = artikel.prov-code
    vat-code     = artikel.mwst-code
.

RUN htpdate.p(110,  OUTPUT bill-date).
RUN htplogic.p(479, OUTPUT serv-vat).
RUN htplogic.p(483, OUTPUT tax-vat).
RUN htplogic.p(127, OUTPUT rm-vat).
RUN htplogic.p(128, OUTPUT rm-serv).
RUN htplogic.p(135, OUTPUT incl-service).
RUN htplogic.p(134, OUTPUT incl-mwst).

IF inp-date NE ? AND inp-date LT bill-date THEN 
DO:    
    RUN calculate-it2.
    IF returnFlag THEN RETURN.
END.

IF service-code NE 0 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = service-code NO-LOCK
        NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO:
        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
          ASSIGN service = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
        ELSE service = htparam.fdecimal.
    END.
END.

IF tax-code NE 0 THEN
DO:
    FIND FIRST htparam WHERE htparam.paramnr = tax-code NO-LOCK
        NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO:
        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
          ASSIGN vat2 = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
        ELSE vat2 = htparam.fdecimal.
        IF serv-vat THEN vat2 = vat2 + (vat2 * service) / 100.
        ASSIGN 
            ct     = REPLACE(STRING(vat), ".", ",")
            l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
        .
        IF l-deci LE 2     THEN vat2 = ROUND(vat2, 2).
        ELSE IF l-deci = 3 THEN vat2 = ROUND(vat2, 3).
        ELSE vat2 = ROUND(vat2, 4).
    END.
END.


IF vat-code NE 0 THEN 
DO: 
    FIND FIRST htparam WHERE htparam.paramnr = vat-code NO-LOCK
        NO-ERROR. 
    IF AVAILABLE htparam AND htparam.fdecimal NE 0 THEN 
    DO: 
        IF NUM-ENTRIES(htparam.fchar, CHR(2)) GE 2 THEN
          ASSIGN vat = DECIMAL(ENTRY(2, htparam.fchar, CHR(2))) / 10000.
        ELSE vat = htparam.fdecimal.
        IF serv-vat AND NOT tax-vat THEN vat = vat + vat * service / 100.
        ELSE IF serv-vat AND tax-vat THEN vat = vat + vat * (service + vat2) / 100.
        ELSE IF NOT serv-vat AND tax-vat THEN vat = vat + vat * vat2 / 100.
        ASSIGN 
            ct     = REPLACE(STRING(vat), ".", ",")
            l-deci = LENGTH(ENTRY(2, ct, ",")) NO-ERROR
        .
        IF l-deci LE 2     THEN vat = ROUND(vat, 2).
        ELSE IF l-deci = 3 THEN vat = ROUND(vat, 3).
        ELSE vat = ROUND(vat, 4).
    END. 
END. 

ASSIGN
    service = service / 100
    vat     = vat / 100
    vat2    = vat2 / 100
.


IF i-case = 2 THEN
DO:     
    IF NOT rm-vat THEN 
    ASSIGN
        vat  = 0
        vat2 = 0
    .
    IF NOT rm-serv THEN ASSIGN service = 0.
END.
IF i-case = 3 THEN
DO:     
    IF NOT incl-mwst THEN 
    ASSIGN
        vat  = 0
        vat2 = 0
    .
    IF NOT incl-service THEN ASSIGN service = 0.
END.

ASSIGN fact-scvat = 1 + service + vat + vat2.

IF vat = 1 THEN 
ASSIGN
    fact-scvat  = 1
    service     = 0
    vat2        = 0
.
ELSE IF vat2 = 1 THEN 
ASSIGN
    fact-scvat = 1
    service    = 0
    vat        = 0
.
ELSE IF service = 1 THEN 
ASSIGN
    fact-scvat = 1
    vat        = 0
    vat2       = 0
.

RETURN.

PROCEDURE calculate-it2:
    
    FIND FIRST kontplan NO-LOCK WHERE 
        kontplan.betriebsnr = inp-deptNo AND
        kontplan.kontignr   = inp-artNo  AND 
        kontplan.datum      = inp-date   NO-ERROR.
    IF NOT AVAILABLE kontplan THEN RETURN.
    IF kontplan.anzkont GE 100000 THEN
    ASSIGN  
        service = kontplan.anzkont  / 10000000
        vat     = kontplan.anzconf / 10000000
    .    
    ELSE
    ASSIGN 
        service = kontplan.anzkont  / 10000
        vat     = kontplan.anzconf / 10000
    .    
    FIND FIRST kontplan NO-LOCK WHERE 
        kontplan.betriebsnr = inp-deptNo + 100 AND
        kontplan.kontignr   = inp-artNo        AND 
        kontplan.datum      = inp-date NO-ERROR.
    IF AVAILABLE kontplan THEN
    ASSIGN vat2 = kontplan.anzconf / 10000000.    

    IF i-case = 2 THEN
    DO:     
        IF NOT rm-vat THEN 
        ASSIGN
            vat  = 0
            vat2 = 0
        .
        IF NOT rm-serv THEN ASSIGN service = 0.
    END.
    IF i-case = 3 THEN
    DO:     
        IF NOT incl-mwst THEN 
        ASSIGN
            vat  = 0
            vat2 = 0
        .
        IF NOT incl-service THEN ASSIGN service = 0.
    END.

    ASSIGN fact-scvat = 1 + service + vat + vat2.
    
    IF vat = 1 THEN 
    ASSIGN
        fact-scvat  = 1
        service     = 0
        vat2        = 0
    .
    ELSE IF vat2 = 1 THEN 
    ASSIGN
        fact-scvat  = 1
        service     = 0
        vat         = 0
    .
    ELSE IF service = 1 THEN 
    ASSIGN
        fact-scvat  = 1
        vat         = 0
        vat2        = 0
    .
    returnFlag = YES.
END.
