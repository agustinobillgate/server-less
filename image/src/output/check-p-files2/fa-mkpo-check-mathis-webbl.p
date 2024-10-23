
DEF TEMP-TABLE t-mathis LIKE mathis
    FIELD remain-budget  AS DECIMAL
    FIELD init-budget    AS DECIMAL
    .
DEFINE TEMP-TABLE remain-budget-list
    FIELD fa-number     AS INTEGER
    FIELD fa-account    AS CHARACTER
    FIELD remain-budget AS DECIMAL
    FIELD amount        AS DECIMAL
    FIELD init-budget    AS DECIMAL
    .

DEF INPUT  PARAMETER art-nr       AS INT.
DEF INPUT  PARAMETER order-date   AS DATE.
DEF OUTPUT PARAMETER avail-mathis AS LOGICAL INIT YES.
DEF INPUT-OUTPUT PARAMETER TABLE FOR t-mathis.

DEFINE VARIABLE mtd-budget    AS DECIMAL.
DEFINE VARIABLE mtd-balance   AS DECIMAL.
DEFINE VARIABLE t-warenwert   AS DECIMAL.
DEFINE VARIABLE remain-budget AS DECIMAL.
DEFINE VARIABLE grup-nr       AS DECIMAL.

FIND FIRST mathis WHERE mathis.nr = art-nr NO-LOCK NO-ERROR. 
IF NOT AVAILABLE mathis THEN avail-mathis = NO.

/*FDL July 17, 2024 => Ticket D710C2*/
FIND FIRST fa-artikel WHERE fa-artikel.nr EQ art-nr NO-LOCK NO-ERROR.
IF AVAILABLE fa-artikel THEN
DO:
    FIND FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK NO-ERROR.
    IF AVAILABLE fa-grup THEN
    DO:
        CREATE remain-budget-list.
        ASSIGN
            grup-nr                         = fa-grup.gnr
            remain-budget-list.fa-number    = fa-artikel.nr
            remain-budget-list.fa-account   = fa-artikel.fibukonto
            .
    END.
END.

FIND FIRST remain-budget-list NO-LOCK NO-ERROR.
IF AVAILABLE remain-budget-list THEN
DO:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ remain-budget-list.fa-account NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN 
    ASSIGN
        remain-budget-list.remain-budget = gl-acct.budget[MONTH(order-date)]
        remain-budget-list.init-budget = gl-acct.budget[MONTH(order-date)] /* Dzikri 01B1DB */
    .
END.

t-warenwert = 0.
FOR EACH fa-op WHERE fa-op.loeschflag LE 1
    AND MONTH(fa-op.datum) EQ MONTH(order-date)
    AND YEAR(fa-op.datum) EQ YEAR(order-date) NO-LOCK,
    FIRST fa-artikel WHERE fa-artikel.nr EQ fa-op.nr NO-LOCK,
 /* FIRST fa-grup WHERE fa-grup.gnr EQ fa-artikel.subgrp AND fa-grup.flag GT 0 NO-LOCK, */ /* Dzikri 01B1DB */
    FIRST gl-acct WHERE gl-acct.fibukonto EQ fa-artikel.fibukonto NO-LOCK
    BY fa-artikel.fibukonto:
    
    IF fa-artikel.subgrp EQ grup-nr THEN t-warenwert = t-warenwert + fa-op.warenwert. /* Dzikri 01B1DB */
    
    FIND FIRST remain-budget-list WHERE remain-budget-list.fa-account EQ fa-artikel.fibukonto NO-LOCK NO-ERROR.
    IF AVAILABLE remain-budget-list THEN
    DO:
        ASSIGN
           mtd-budget  = gl-acct.budget[MONTH(order-date)]
           mtd-balance = (mtd-budget - t-warenwert).

        remain-budget-list.amount = t-warenwert.
        remain-budget-list.remain-budget = mtd-balance.
    END.       
END.  

FOR EACH mathis WHERE mathis.nr = art-nr NO-LOCK:
    CREATE t-mathis.
    BUFFER-COPY mathis TO t-mathis.

    /*FDL July 17, 2024 => Ticket D710C2*/
    FIND FIRST remain-budget-list WHERE remain-budget-list.fa-number EQ mathis.nr NO-LOCK NO-ERROR.
    IF AVAILABLE remain-budget-list THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ remain-budget-list.fa-account NO-LOCK NO-ERROR.
        IF AVAILABLE gl-acct THEN
        ASSIGN
            t-mathis.remain-budget = remain-budget-list.remain-budget
            t-mathis.init-budget = remain-budget-list.init-budget /* Dzikri 01B1DB */
        . 
    END.
END.
