DEFINE TEMP-TABLE output-list 
    FIELD betriebsnr      AS INTEGER INITIAL 0 
    FIELD ap-recid        AS INTEGER INITIAL 0 
    FIELD curr-pay        AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD lscheinnr       AS CHAR
    FIELD STR             AS CHAR
    FIELD firma           AS CHARACTER
    FIELD billdate        AS DATE
    FIELD docunr          AS CHARACTER
    FIELD delivnote       AS CHARACTER
    FIELD amount          AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD paid-amount     AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD paiddate        AS CHARACTER
    FIELD balance         AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99"
    FIELD duedate         AS DATE
    FIELD desc1           AS CHARACTER
    FIELD steuercode      AS INTEGER /*FD*/ 
    FIELD recv-date       AS DATE /*gerald*/
    FIELD rechnr          AS INTEGER /* Naufal Afthar - 9FF12E*/
  . 

DEF INPUT  PARAMETER from-date      AS DATE.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF INPUT  PARAMETER lastname       AS CHAR.
DEF INPUT  PARAMETER sorttype       AS INT.
DEF INPUT  PARAMETER price-decimal  AS INT.
DEF INPUT  PARAMETER check-disp     AS INTEGER. /* Gerald 130220 */
DEF INPUT  PARAMETER voucher-only   AS LOGICAL. /* Naufal Afthar - 9FF12E -> apply summary by voucher number*/
DEF OUTPUT PARAMETER TABLE FOR output-list.

/*DEFINE INPUT  PARAMETER from-date      AS DATE.
DEFINE INPUT  PARAMETER to-date        AS DATE.
DEFINE INPUT  PARAMETER lastname       AS CHAR.
DEFINE INPUT  PARAMETER sorttype       AS INTEGER .
DEFINE INPUT  PARAMETER price-decimal  AS INTEGER .
DEFINE INPUT  PARAMETER type1          AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VAR from-date      AS DATE INITIAL 1/1/19.
DEFINE VAR to-date        AS DATE INITIAL 1/3/19.
DEFINE VAR lastname       AS CHAR INITIAL "Dima Mandiri, Cv".
DEFINE VAR sorttype       AS INTEGER INITIAL 0.
DEFINE VAR price-decimal  AS INTEGER INITIAL 0.
DEFINE VAR type1          AS CHARACTER INITIAL "2".*/

DEFINE VARIABLE t-ap    AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-pay   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE t-bal   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-ap  AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-pay AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE tot-bal AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE i       AS INTEGER.

DEFINE VARIABLE stauer-code1       AS INTEGER INITIAL ? NO-UNDO.
DEFINE VARIABLE stauer-code2       AS INTEGER INITIAL 0 NO-UNDO.

DEFINE VARIABLE sorttype1       AS INTEGER INITIAL ? NO-UNDO.
DEFINE VARIABLE sorttype2       AS INTEGER INITIAL 0 NO-UNDO.

IF sorttype EQ 1 THEN
DO:
    sorttype1 = 0.
    sorttype2 = 2.
END.
ELSE IF sorttype EQ 0 THEN
DO:
    sorttype1 = 0.
    sorttype2 = 0.
END.
ELSE IF sorttype EQ 2 THEN
DO:
    sorttype1 = 2.
    sorttype2 = 2.
END.

/* Disable this filter because from UI date is mandatory. If date happened to be null just let it blank by Oscar (18 Oktober 2024) - 05C934 */
/* IF from-date = ? AND to-date = ? THEN RUN disp-it.
ELSE IF from-date = ? AND to-date NE ? THEN RUN disp-it0.
ELSE RUN disp-it1. */
/* Naufal Afthar - 9FF12E*/
IF NOT voucher-only THEN RUN disp-it1.
ELSE RUN disp-it2.

/* PROCEDURE disp-it:
    DEFINE VARIABLE curr-firma  AS CHAR INITIAL "". 
    DEFINE VARIABLE s2          AS CHAR. 
    DEFINE VARIABLE d2          AS CHAR. 
    DEFINE VARIABLE curr-pay    AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99". 
    DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
    DEFINE VARIABLE doit        AS LOGICAL NO-UNDO.

    DEFINE BUFFER l-ap     FOR l-kredit.

    FOR EACH output-list:
        DELETE output-list.
    END.

    t-ap    = 0. 
    t-pay   = 0. 
    t-bal   = 0. 
    tot-ap  = 0. 
    tot-pay = 0. 
    tot-bal = 0. 

    IF lastname = " " THEN
    DO:
        IF check-disp = 0 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                        CREATE output-list.
                        output-list.firma       =  "T O T A L    ".
                        output-list.amount      = t-ap.
                        output-list.paid-amount = t-pay.  
                        output-list.balance     = t-bal.
                        t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0. 
                        curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay. 

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE IF check-disp = 1 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                /*AND l-kredit.rechnr NE 0000000*/
                AND l-kredit.steuercode  = 1
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                        CREATE output-list.
                        output-list.firma       =  "T O T A L    ".
                        output-list.amount      = t-ap.
                        output-list.paid-amount = t-pay.  
                        output-list.balance     = t-bal.
                        t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0. 
                        curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay. 

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE IF check-disp = 2 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                /*AND l-kredit.rechnr NE 0000000*/
                AND l-kredit.steuercode  = 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                        CREATE output-list.
                        output-list.firma       =  "T O T A L    ".
                        output-list.amount      = t-ap.
                        output-list.paid-amount = t-pay.  
                        output-list.balance     = t-bal.
                        t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0. 
                        curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay. 

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
                

                FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                    AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    do-it = YES.
                    IF l-kredit.opart = 1 THEN do-it = NO.
                    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                        IF curr-firma NE l-lieferant.firma THEN
                        DO:
                            CREATE output-list.
                            output-list.firma       =  "T O T A L    ".
                            output-list.amount      = t-ap.
                            output-list.paid-amount = t-pay.  
                            output-list.balance     = t-bal.
                            t-ap   = 0. 
                            t-pay  = 0. 
                            t-bal  = 0. 
                            curr-firma = l-lieferant.firma. 
                        END.
                        /*t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0.*/
                        curr-pay = 0.
                        IF l-kredit.counter GT 0 THEN
                        DO:
                            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                                BY l-ap.rgdatum:
                                curr-pay = curr-pay - l-ap.saldo.
                                d2 = STRING(l-ap.rgdatum).
                            END.
                        END.
                        IF curr-pay = 0 THEN d2 = " ".
                        CREATE output-list. 
                        output-list.betriebsnr  = l-kredit.betriebsnr. 
                        output-list.ap-recid    = RECID(l-kredit). 
                        output-list.curr-pay    = curr-pay. 
                        output-list.firma       = l-lieferant.firma.
                        output-list.billdate    = l-kredit.rgdatum.
                        output-list.docunr      = l-kredit.name.
                        output-list.lscheinnr   = l-kredit.lscheinnr.
                        output-list.amount      = l-kredit.netto.
                        output-list.paid-amount = curr-pay.
                        output-list.paiddate    = d2.
                        output-list.balance     = l-kredit.netto - curr-pay.
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                        output-list.desc1       = l-kredit.bemerk.
                        output-list.steuercode  = l-kredit.steuercode.
                        output-list.recv-date   = queasy.date1.
                    
                        t-ap    = t-ap + l-kredit.netto. 
                        t-pay   = t-pay + curr-pay. 
                        t-bal   = t-bal + l-kredit.netto - curr-pay. 
                        tot-ap  = tot-ap + l-kredit.netto. 
                        tot-pay = tot-pay + curr-pay. 
                        tot-bal = tot-bal + l-kredit.netto - curr-pay. 
                    END.
                END.                       
            END.
        END.
        CREATE output-list.
        output-list.firma       = "T O T A L    ".            
        output-list.amount      = t-ap.
        output-list.paid-amount = t-pay.  
        output-list.balance     = t-bal.
        t-ap   = 0. 
        t-pay  = 0. 
        t-bal  = 0. 
        
        CREATE output-list. 
        output-list.firma       = "GRAND TOTAL    ".
        output-list.amount      = tot-ap.
        output-list.paid-amount = tot-pay.  
        output-list.balance     = tot-bal.
    END.
    ELSE
    DO:
        doit = NO.
        FIND FIRST l-lieferant WHERE l-lieferant.firma = lastname NO-LOCK NO-ERROR. 
        IF AVAILABLE l-lieferant THEN
        DO:
            IF segm = 0 THEN doit = YES.
            ELSE doit = l-lieferant.segment1 = segm.
        END.
        IF doit THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr = l-lieferant.lief-nr 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix BY l-kredit.rgdatum: 

                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.

                IF do-it THEN
                DO:
                  curr-pay = 0.
                  IF l-kredit.counter GT 0 THEN 
                  DO: 
                      FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
                          AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
                          BY l-ap.rgdatum: 
                          curr-pay = curr-pay - l-ap.saldo. 
                          d2 = STRING(l-ap.rgdatum). 
                      END. 
                  END. 
                  /*IF curr-pay = 0 THEN d2 = "".
                  d2 = STRING(l-ap.rgdatum).*/
                  
                  IF curr-pay = 0 THEN d2 = "".
                  CREATE output-list.
                  output-list.betriebsnr  = l-kredit.betriebsnr. 
                  output-list.ap-recid    = RECID(l-kredit). 
                  output-list.curr-pay    = curr-pay.
                  output-list.firma       = l-lieferant.firma.
                  output-list.billdate    = l-kredit.rgdatum.
                  output-list.docunr      = l-kredit.name.
                  output-list.lscheinnr   = l-kredit.lscheinnr.
                  output-list.desc1       = l-kredit.bemerk.
                  output-list.steuercode  = l-kredit.steuercode.
                  output-list.amount      = l-kredit.netto.
                  output-list.paid-amount = curr-pay .
                  output-list.paiddate    = d2.
                  output-list.balance     = l-kredit.netto - curr-pay.
                  output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                  
                  /* fix miscalculation total by Oscar (18 Oktober 2024) - 05C934 */
                  /* output-list.amount      = t-ap  + l-kredit.netto. 
                  output-list.paid-amount = t-pay + curr-pay.
                  output-list.balance     = t-bal + l-kredit.netto - curr-pay. */
                  t-ap  = t-ap + l-kredit.netto. 
                  t-pay = t-pay + curr-pay. 
                  t-bal = t-bal + l-kredit.netto - curr-pay.
                  
                  FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                      AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                  IF AVAILABLE queasy THEN
                  DO:
                      ASSIGN
                          output-list.recv-date = queasy.date1.
                  END.
                END.
            END.
        END.
        CREATE output-list.
        output-list.firma = output-list.firma + "GRAND TOTAL    ". 
        output-list.amount      = t-ap  . 
        output-list.paid-amount = t-pay .
        output-list.balance     = t-bal .
    END.

    /* fix total output for per supplier by Oscar (18 Oktober 2024) - 05C934 */
    /* CREATE output-list.
    output-list.firma = output-list.firma + "T O T A L     ". 
    output-list.amount      = t-ap  . 
    output-list.paid-amount = t-pay .
    output-list.balance     = t-bal . */
END. */

/* PROCEDURE disp-it0:
    DEFINE VARIABLE curr-firma  AS CHAR INITIAL "". 
    DEFINE VARIABLE s2          AS CHAR. 
    DEFINE VARIABLE d2          AS CHAR. 
    DEFINE VARIABLE curr-pay    AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99". 
    DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
    DEFINE VARIABLE doit        AS LOGICAL NO-UNDO.

    DEFINE BUFFER l-ap FOR l-kredit.

    FOR EACH output-list:
        DELETE output-list.
    END.

    t-ap    = 0. 
    t-pay   = 0. 
    t-bal   = 0. 
    tot-ap  = 0. 
    tot-pay = 0. 
    tot-bal = 0. 

    IF lastname = " " THEN
    DO:
        IF check-disp = 0 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                            CREATE output-list.
                            output-list.firma       =  "T O T A L    ".
                            output-list.amount      = t-ap.
                            output-list.paid-amount = t-pay.  
                            output-list.balance     = t-bal.
                            t-ap   = 0. 
                            t-pay  = 0. 
                            t-bal  = 0. 
                            curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay.
            
                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE IF check-disp = 1 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                /*AND l-kredit.rechnr NE 0000000*/
                AND l-kredit.steuercode  = 1
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                            CREATE output-list.
                            output-list.firma       =  "T O T A L    ".
                            output-list.amount      = t-ap.
                            output-list.paid-amount = t-pay.  
                            output-list.balance     = t-bal.
                            t-ap   = 0. 
                            t-pay  = 0. 
                            t-bal  = 0. 
                            curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay.
            
                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE IF check-disp = 2 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                /*AND l-kredit.rechnr NE 0000000*/
                AND l-kredit.steuercode  = 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                        CREATE output-list.
                        output-list.firma       =  "T O T A L    ".
                        output-list.amount      = t-ap.
                        output-list.paid-amount = t-pay.  
                        output-list.balance     = t-bal.
                        t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0. 
                        curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay. 

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                    AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    do-it = YES.
                    IF l-kredit.opart = 1 THEN do-it = NO.
                    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                        IF curr-firma NE l-lieferant.firma THEN
                        DO:
                                CREATE output-list.
                                output-list.firma       =  "T O T A L    ".
                                output-list.amount      = t-ap.
                                output-list.paid-amount = t-pay.  
                                output-list.balance     = t-bal.
                                t-ap   = 0. 
                                t-pay  = 0. 
                                t-bal  = 0. 
                                curr-firma = l-lieferant.firma. 
                        END.
                        /*t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0.*/
                        curr-pay = 0.
                        IF l-kredit.counter GT 0 THEN
                        DO:
                            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                                BY l-ap.rgdatum:
                                curr-pay = curr-pay - l-ap.saldo.
                                d2 = STRING(l-ap.rgdatum).
                            END.
                        END.
                        IF curr-pay = 0 THEN d2 = " ".
                        CREATE output-list. 
                        output-list.betriebsnr  = l-kredit.betriebsnr. 
                        output-list.ap-recid    = RECID(l-kredit). 
                        output-list.curr-pay    = curr-pay. 
                        output-list.firma       = l-lieferant.firma.
                        output-list.billdate    = l-kredit.rgdatum.
                        output-list.docunr      = l-kredit.name.
                        output-list.lscheinnr   = l-kredit.lscheinnr.
                        output-list.amount      = l-kredit.netto.
                        output-list.paid-amount = curr-pay.
                        output-list.paiddate    = d2.
                        output-list.balance     = l-kredit.netto - curr-pay.
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                        output-list.desc1       = l-kredit.bemerk.
                        output-list.steuercode  = l-kredit.steuercode.
                        output-list.recv-date   = queasy.date1.
                    
                        t-ap    = t-ap + l-kredit.netto. 
                        t-pay   = t-pay + curr-pay. 
                        t-bal   = t-bal + l-kredit.netto - curr-pay. 
                        tot-ap  = tot-ap + l-kredit.netto. 
                        tot-pay = tot-pay + curr-pay. 
                        tot-bal = tot-bal + l-kredit.netto - curr-pay.
                    END. 
                END.                      
            END.
        END.
        CREATE output-list.
        output-list.firma = "T O T A L    ".

        output-list.amount      = t-ap.
        output-list.paid-amount = t-pay.  
        output-list.balance     = t-bal.
        t-ap   = 0. 
        t-pay  = 0. 
        t-bal  = 0. 
        
        CREATE output-list. 
        output-list.firma = "GRAND TOTAL    ".
        output-list.amount      = tot-ap.
        output-list.paid-amount = tot-pay.  
        output-list.balance     = tot-bal.
    END.
    ELSE
    DO:
        doit = NO.
        FIND FIRST l-lieferant WHERE l-lieferant.firma = lastname NO-LOCK NO-ERROR. 
        IF AVAILABLE l-lieferant THEN
        DO:
            IF segm = 0 THEN doit = YES.
            ELSE do-it = l-lieferant.segment1 = segm.
        END.
        IF doit THEN
        DO:

            FOR EACH l-kredit WHERE l-kredit.lief-nr = l-lieferant.lief-nr 
                AND l-kredit.zahlkonto = 0 
                /*AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 */
                AND l-kredit.opart = sorttype 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix BY l-kredit.rgdatum: 

                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.

                IF do-it THEN
                DO:
                  curr-pay = 0.
                  IF l-kredit.counter GT 0 THEN
                  DO:
                      FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
                          AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
                          BY l-ap.rgdatum: 
                          curr-pay = curr-pay - l-ap.saldo.
                          d2 = STRING(l-ap.rgdatum).
                      END.
                  END.
                  /*    IF curr-pay = 0 THEN d2 = "".
                          d2 = STRING(l-ap.rgdatum).
                      END.
                  END.*/
                  IF curr-pay = 0 THEN d2 = "".
                  CREATE output-list.
                  output-list.betriebsnr  = l-kredit.betriebsnr. 
                  output-list.ap-recid    = RECID(l-kredit). 
                  output-list.curr-pay    = curr-pay.
                  output-list.firma       = l-lieferant.firma.
                  output-list.billdate    = l-kredit.rgdatum.
                  output-list.docunr      = l-kredit.name.
                  output-list.lscheinnr   = l-kredit.lscheinnr.
                  output-list.desc1       = l-kredit.bemerk.
                  output-list.steuercode  = l-kredit.steuercode.
                  output-list.amount      = l-kredit.netto.
                  output-list.paid-amount = curr-pay .
                  output-list.paiddate    = d2.
                  output-list.balance     = l-kredit.netto - curr-pay.
                  output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
              
                  /* fix miscalculation total by Oscar (18 Oktober 2024) - 05C934 */
                  /* output-list.amount      = t-ap  + l-kredit.netto. 
                  output-list.paid-amount = t-pay + curr-pay.
                  output-list.balance     = t-bal + l-kredit.netto - curr-pay. */
                  t-ap  = t-ap + l-kredit.netto. 
                  t-pay = t-pay + curr-pay. 
                  t-bal = t-bal + l-kredit.netto - curr-pay.

                  FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                      AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                  IF AVAILABLE queasy THEN
                  DO:
                      ASSIGN
                          output-list.recv-date = queasy.date1.
                  END.
                END.
            END.
        END.
        CREATE output-list.
        output-list.firma = output-list.firma + "GRAND TOTAL    ". 
        output-list.amount      = t-ap  . 
        output-list.paid-amount = t-pay .
        output-list.balance     = t-bal .
    END.
    /* fix total output for per supplier by Oscar (18 Oktober 2024) - 05C934 */
    /* CREATE output-list.
    output-list.firma = output-list.firma + "T O T A L     ". 
    output-list.amount      = t-ap  . 
    output-list.paid-amount = t-pay .
    output-list.balance     = t-bal . */
END. */

PROCEDURE disp-it1:
    DEFINE VARIABLE curr-firma  AS CHAR INITIAL "". 
    DEFINE VARIABLE s2          AS CHAR. 
    DEFINE VARIABLE d2          AS CHAR. 
    DEFINE VARIABLE curr-pay    AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99". 
    DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
    DEFINE VARIABLE doit        AS LOGICAL NO-UNDO.

    DEFINE BUFFER l-ap FOR l-kredit.

    FOR EACH output-list:
        DELETE output-list.
    END.

    t-ap    = 0. 
    t-pay   = 0. 
    t-bal   = 0. 
    tot-ap  = 0. 
    tot-pay = 0. 
    tot-bal = 0. 

        /*
               AND l-kredit.opart GE sorttype1 
            AND l-kredit.opart LE sorttype2 
            AND l-kredit.counter GE 0 
            AND l-kredit.netto NE 0
            AND l-kredit.steuercode GE stauer-code1 
            AND l-kredit.steuercode LE stauer-code2 
    */

    IF lastname = " " THEN
    DO:
        IF check-disp = 0 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum GE from-date 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                            CREATE output-list.
                            output-list.firma       =  "T O T A L    ".
                            output-list.amount      = t-ap.
                            output-list.paid-amount = t-pay.  
                            output-list.balance     = t-bal.
                            t-ap   = 0. 
                            t-pay  = 0. 
                            t-bal  = 0. 
                            curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.rechnr      = l-kredit.rechnr. /* Naufal Afthar - 9FF12E*/
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay.

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE IF check-disp = 1 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum GE from-date 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                /*AND l-kredit.rechnr NE 0000000*/
                AND l-kredit.steuercode  = 1
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                            CREATE output-list.
                            output-list.firma       =  "T O T A L    ".
                            output-list.amount      = t-ap.
                            output-list.paid-amount = t-pay.  
                            output-list.balance     = t-bal.
                            t-ap   = 0. 
                            t-pay  = 0. 
                            t-bal  = 0. 
                            curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.rechnr      = l-kredit.rechnr. /* Naufal Afthar - 9FF12E*/
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay.

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE IF check-disp = 2 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum GE from-date 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                /*AND l-kredit.rechnr NE 0000000*/
                AND l-kredit.steuercode  = 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                    IF curr-firma NE l-lieferant.firma THEN
                    DO:
                        CREATE output-list.
                        output-list.firma       =  "T O T A L    ".
                        output-list.amount      = t-ap.
                        output-list.paid-amount = t-pay.  
                        output-list.balance     = t-bal.
                        t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0. 
                        curr-firma = l-lieferant.firma. 
                    END.
                    /*t-ap   = 0. 
                    t-pay  = 0. 
                    t-bal  = 0.*/
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
                            curr-pay = curr-pay - l-ap.saldo.
                            d2 = STRING(l-ap.rgdatum).
                        END.
                    END.
                    IF curr-pay = 0 THEN d2 = " ".
                    CREATE output-list. 
                    output-list.rechnr      = l-kredit.rechnr. /* Naufal Afthar - 9FF12E*/
                    output-list.betriebsnr  = l-kredit.betriebsnr. 
                    output-list.ap-recid    = RECID(l-kredit). 
                    output-list.curr-pay    = curr-pay. 
                    output-list.firma       = l-lieferant.firma.
                    output-list.billdate    = l-kredit.rgdatum.
                    output-list.docunr      = l-kredit.name.
                    output-list.lscheinnr   = l-kredit.lscheinnr.
                    output-list.amount      = l-kredit.netto.
                    output-list.paid-amount = curr-pay.
                    output-list.paiddate    = d2.
                    output-list.balance     = l-kredit.netto - curr-pay.
                    output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    output-list.desc1       = l-kredit.bemerk.
                    output-list.steuercode  = l-kredit.steuercode.
            
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay. 

                    FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                        AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN
                            output-list.recv-date = queasy.date1.
                    END.
                END.                       
            END.
        END.
        ELSE
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr GT 0 
                AND l-kredit.zahlkonto = 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum GE from-date 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr = l-kredit.lief-nr NO-LOCK BY l-lieferant.firma BY l-kredit.rgdatum: 
            
                FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                    AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:    
                    do-it = YES.
                    IF l-kredit.opart = 1 THEN do-it = NO.
                    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        IF curr-firma = "" THEN curr-firma = l-lieferant.firma.
                        IF curr-firma NE l-lieferant.firma THEN
                        DO:
                                CREATE output-list.
                                output-list.firma       =  "T O T A L    ".
                                output-list.amount      = t-ap.
                                output-list.paid-amount = t-pay.  
                                output-list.balance     = t-bal.
                                t-ap   = 0. 
                                t-pay  = 0. 
                                t-bal  = 0. 
                                curr-firma = l-lieferant.firma. 
                        END.
                        /*t-ap   = 0. 
                        t-pay  = 0. 
                        t-bal  = 0.*/
                        curr-pay = 0.
                        IF l-kredit.counter GT 0 THEN
                        DO:
                            FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter
                                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                                BY l-ap.rgdatum:
                                
                                curr-pay = curr-pay - l-ap.saldo.
                                d2 = STRING(l-ap.rgdatum).
                            END.
                        END.
                        IF curr-pay = 0 THEN d2 = " ".
                        CREATE output-list. 
                        output-list.rechnr      = l-kredit.rechnr. /* Naufal Afthar - 9FF12E*/
                        output-list.betriebsnr  = l-kredit.betriebsnr. 
                        output-list.ap-recid    = RECID(l-kredit). 
                        output-list.curr-pay    = curr-pay. 
                        output-list.firma       = l-lieferant.firma.
                        output-list.billdate    = l-kredit.rgdatum.
                        output-list.docunr      = l-kredit.name.
                        output-list.lscheinnr   = l-kredit.lscheinnr.
                        output-list.amount      = l-kredit.netto.
                        output-list.paid-amount = curr-pay.
                        output-list.paiddate    = d2.
                        output-list.balance     = l-kredit.netto - curr-pay.
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                        output-list.desc1       = l-kredit.bemerk.
                        output-list.steuercode  = l-kredit.steuercode.
                        output-list.recv-date   = queasy.date1.
                    
                        t-ap    = t-ap + l-kredit.netto. 
                        t-pay   = t-pay + curr-pay. 
                        t-bal   = t-bal + l-kredit.netto - curr-pay. 
                        tot-ap  = tot-ap + l-kredit.netto. 
                        tot-pay = tot-pay + curr-pay. 
                        tot-bal = tot-bal + l-kredit.netto - curr-pay.
                    END.
                END.                       
            END.
        END.
        CREATE output-list.
        output-list.firma = "T O T A L    ".

            output-list.amount      = t-ap.
            output-list.paid-amount = t-pay.  
            output-list.balance     = t-bal.
            t-ap   = 0. 
            t-pay  = 0. 
            t-bal  = 0. 
            
            CREATE output-list. 
            output-list.firma = "GRAND TOTAL    ".
            output-list.amount      = tot-ap.
            output-list.paid-amount = tot-pay.  
            output-list.balance     = tot-bal.
    END.
    ELSE
    DO:
        doit = NO.
        FIND FIRST l-lieferant WHERE l-lieferant.firma = lastname NO-LOCK NO-ERROR. 
        IF AVAILABLE l-lieferant THEN
        DO:
            IF segm = 0 THEN doit = YES.
            ELSE doit = l-lieferant.segment1 EQ segm.
        END.
        IF doit THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.lief-nr = l-lieferant.lief-nr 
            AND l-kredit.zahlkonto = 0 
            AND l-kredit.opart GE sorttype1 
            AND l-kredit.opart LE sorttype2 
            AND l-kredit.rgdatum GE from-date 
            AND l-kredit.rgdatum LE to-date 
            AND l-kredit.counter GE 0 
            AND l-kredit.netto NE 0
            NO-LOCK USE-INDEX counter_ix BY l-kredit.rgdatum: 

                do-it = YES.
                IF l-kredit.opart = 1 THEN do-it = NO.

                IF do-it THEN
                DO:
                  curr-pay = 0.
                  IF l-kredit.counter GT 0 THEN
                  DO:
                      FOR EACH l-ap WHERE l-ap.counter = l-kredit.counter 
                          AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK 
                          BY l-ap.rgdatum: 
                          curr-pay = curr-pay - l-ap.saldo.
                          d2 = STRING(l-ap.rgdatum).
                      END.
                  END.
                  /*    IF curr-pay = 0 THEN d2 = "".
                      d2 = STRING(l-ap.rgdatum).
                  END.
                  END.*/
                  IF curr-pay = 0 THEN d2 = "".
                  CREATE output-list.
                  output-list.rechnr      = l-kredit.rechnr. /* Naufal Afthar - 9FF12E*/
                  output-list.betriebsnr  = l-kredit.betriebsnr. 
                  output-list.ap-recid    = RECID(l-kredit). 
                  output-list.curr-pay    = curr-pay.
                  output-list.firma       = l-lieferant.firma.
                  output-list.billdate    = l-kredit.rgdatum.
                  output-list.docunr      = l-kredit.name.
                  output-list.lscheinnr   = l-kredit.lscheinnr.
                  output-list.desc1       = l-kredit.bemerk.
                  output-list.steuercode  = l-kredit.steuercode.
                  output-list.amount      = l-kredit.netto.
                  output-list.paid-amount = curr-pay .
                  output-list.paiddate    = d2.
                  output-list.balance     = l-kredit.netto - curr-pay.
                  output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel.
                    
                  /* fix miscalculation total by Oscar (18 Oktober 2024) - 05C934 */
                  /* output-list.amount      = t-ap  + l-kredit.netto. 
                  output-list.paid-amount = t-pay + curr-pay.
                  output-list.balance     = t-bal + l-kredit.netto - curr-pay. */
                  t-ap  = t-ap + l-kredit.netto. 
                  t-pay = t-pay + curr-pay. 
                  t-bal = t-bal + l-kredit.netto - curr-pay.
                  
                  FIND FIRST queasy WHERE queasy.KEY = 221 AND queasy.number1 = l-kredit.lief-nr
                      AND queasy.char1 = l-kredit.lscheinnr /*l-kredit.NAME*/ NO-LOCK NO-ERROR.
                  IF AVAILABLE queasy THEN
                  DO:
                      ASSIGN
                          output-list.recv-date = queasy.date1.
                  END.
                END.
            END.
        END.
        CREATE output-list.
        output-list.firma = output-list.firma + "GRAND TOTAL    ". 
        output-list.amount      = t-ap  . 
        output-list.paid-amount = t-pay .
        output-list.balance     = t-bal .
    END.

    /* fix total output for per supplier by Oscar (18 Oktober 2024) - 05C934 */
    /* CREATE output-list.
    output-list.firma = output-list.firma + "T O T A L     ". 
    output-list.amount      = t-ap  . 
    output-list.paid-amount = t-pay .
    output-list.balance     = t-bal . */
END.

/* Naufal Afthar - 9FF12E*/
PROCEDURE disp-it2:
    DEFINE VARIABLE curr-rechnr AS INTEGER INITIAL 0. 
    DEFINE VARIABLE s2          AS CHAR. 
    DEFINE VARIABLE d2          AS CHAR. 
    DEFINE VARIABLE curr-pay    AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>>,>>9.99". 
    DEFINE VARIABLE do-it       AS LOGICAL NO-UNDO.
    DEFINE VARIABLE doit        AS LOGICAL NO-UNDO.

    DEFINE BUFFER l-ap FOR l-kredit.

    FOR EACH output-list:
        DELETE output-list.
    END.

    t-ap    = 0. 
    t-pay   = 0. 
    t-bal   = 0. 
    tot-ap  = 0. 
    tot-pay = 0. 
    tot-bal = 0. 

    IF lastname EQ " " THEN
    DO:
        IF check-disp EQ 0 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.rechnr NE 0
                AND l-kredit.zahlkonto EQ 0
                AND l-kredit.opart GE sorttype1
                AND l-kredit.opart LE sorttype2
                AND l-kredit.rgdatum GE from-date
                AND l-kredit.rgdatum LE to-date
                AND l-kredit.counter GE 0
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix,
                FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-kredit.lief-nr 
                NO-LOCK BY l-kredit.rechnr BY l-lieferant.firma BY l-kredit.rgdatum:

                do-it = YES.
                IF l-kredit.opart EQ 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-rechnr EQ 0 THEN curr-rechnr = l-kredit.rechnr.
                    IF curr-rechnr NE l-kredit.rechnr THEN
                    DO:
                        CREATE output-list.
                        ASSIGN
                            output-list.firma = "T O T A L    "
                            output-list.amount = t-ap
                            output-list.paid-amount = t-pay
                            output-list.balance = t-bal
                            t-ap = 0
                            t-pay = 0
                            t-bal = 0
                            curr-rechnr = l-kredit.rechnr.
                    END.
                    curr-pay = 0.
                    IF l-kredit.counter GE 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter EQ l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:

                            ASSIGN
                                curr-pay = curr-pay - l-ap.saldo
                                d2 = STRING(l-ap.rgdatum)
                                .
                        END.
                    END.
                    IF curr-pay EQ 0 THEN d2 = " ".
                    CREATE output-list.
                    ASSIGN
                        output-list.rechnr      = l-kredit.rechnr
                        output-list.betriebsnr  = l-kredit.betriebsnr
                        output-list.ap-recid    = RECID(l-kredit)
                        output-list.curr-pay    = curr-pay
                        output-list.firma       = l-lieferant.firma
                        output-list.billdate    = l-kredit.rgdatum
                        output-list.docunr      = l-kredit.NAME
                        output-list.lscheinnr   = l-kredit.lscheinnr
                        output-list.amount      = l-kredit.netto
                        output-list.paid-amount = curr-pay
                        output-list.paiddate    = d2
                        output-list.balance     = l-kredit.netto - curr-pay
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel
                        output-list.desc1       = l-kredit.bemerk.
                        output-list.steuercode  = l-kredit.steuercode
                        .
                    ASSIGN
                        t-ap    = t-ap + l-kredit.netto 
                        t-pay   = t-pay + curr-pay 
                        t-bal   = t-bal + l-kredit.netto - curr-pay 
                        tot-ap  = tot-ap + l-kredit.netto 
                        tot-pay = tot-pay + curr-pay 
                        tot-bal = tot-bal + l-kredit.netto - curr-pay
                        .

                    FIND FIRST queasy WHERE queasy.KEY EQ 221 AND queasy.number1 EQ l-kredit.lief-nr 
                        AND queasy.char1 EQ l-kredit.lscheinnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN ASSIGN output-list.recv-date = queasy.date1.
                END.
            END.
        END.
        ELSE IF check-disp EQ 1 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.rechnr NE 0
                AND l-kredit.lief-nr GT 0
                AND l-kredit.zahlkonto EQ 0 
                AND l-kredit.opart GE sorttype1 
                AND l-kredit.opart LE sorttype2 
                AND l-kredit.rgdatum GE from-date 
                AND l-kredit.rgdatum LE to-date 
                AND l-kredit.counter GE 0 
                AND l-kredit.netto NE 0
                AND l-kredit.steuercode EQ 1
                NO-LOCK USE-INDEX counter_ix, 
                FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-kredit.lief-nr 
                NO-LOCK BY l-kredit.rechnr BY l-lieferant.firma BY l-kredit.rgdatum:
    
                do-it = YES.
                IF l-kredit.opart EQ 1 THEN do-it = YES.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-rechnr EQ 0 THEN curr-rechnr = l-kredit.rechnr.
                    IF curr-rechnr NE l-kredit.rechnr THEN
                    DO:
                        CREATE output-list.
                        ASSIGN
                            output-list.firma       = "T O T A L    "
                            output-list.amount      = t-ap
                            output-list.paid-amount = t-pay
                            output-list.balance     = t-bal
                            t-ap = 0
                            t-pay = 0
                            t-bal = 0
                            curr-rechnr = l-kredit.rechnr
                            .
                    END.
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter EQ l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:

                            ASSIGN
                                curr-pay = curr-pay - l-ap.saldo
                                d2 = STRING(l-ap.rgdatum)
                                .
                        END.
                    END.
                    IF curr-pay EQ 0 THEN d2 = " ".
                    CREATE output-list.
                    ASSIGN
                        output-list.rechnr      = l-kredit.rechnr
                        output-list.betriebsnr  = l-kredit.betriebsnr
                        output-list.ap-recid    = RECID(l-kredit)
                        output-list.curr-pay    = curr-pay
                        output-list.firma       = l-lieferant.firma
                        output-list.billdate    = l-kredit.rgdatum
                        output-list.docunr      = l-kredit.NAME
                        output-list.lscheinnr   = l-kredit.lscheinnr
                        output-list.amount      = l-kredit.netto
                        output-list.paid-amount = curr-pay
                        output-list.paiddate    = d2
                        output-list.balance     = l-kredit.netto - curr-pay
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel
                        output-list.desc1       = l-kredit.bemerk
                        output-list.steuercode  = l-kredit.steuercode
                        .
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay.
    
                    FIND FIRST queasy WHERE queasy.KEY EQ 221 AND queasy.number1 EQ l-kredit.lief-nr
                        AND queasy.char1 EQ l-kredit.lscheinnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN ASSIGN output-list.recv-date = queasy.date1.
                END.
            END.
        END.
        ELSE IF check-disp EQ 2 THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.rechnr NE 0
                AND l-kredit.lief-nr GT 0
                AND l-kredit.zahlkonto EQ 0
                AND l-kredit.opart GE sorttype1
                AND l-kredit.opart LE sorttype2
                AND l-kredit.rgdatum GE from-date
                AND l-kredit.rgdatum LE to-date
                AND l-kredit.counter GE 0
                AND l-kredit.netto NE 0
                AND l-kredit.steuercode EQ 0
                NO-LOCK USE-INDEX counter_ix,
                FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-kredit.lief-nr 
                NO-LOCK BY l-kredit.rechnr BY l-lieferant.firma BY l-kredit.rgdatum:
    
                do-it = YES.
                IF l-kredit.opart EQ 1 THEN do-it = NO.
                IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                IF do-it THEN
                DO:
                    IF curr-rechnr EQ 0 THEN curr-rechnr = l-kredit.rechnr.
                    IF curr-rechnr NE l-kredit.rechnr THEN
                    DO:
                        CREATE output-list.
                        ASSIGN
                            output-list.firma = "T O T A L    "
                            output-list.amount = t-ap
                            output-list.paid-amount = t-pay
                            output-list.balance = t-bal
                            t-ap = 0
                            t-pay = 0
                            t-bal = 0
                            curr-rechnr = l-kredit.rechnr
                            .
                    END.
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter EQ l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:
    
                            ASSIGN
                                curr-pay = curr-pay - l-ap.saldo
                                d2 = STRING(l-ap.rgdatum)
                                .
                        END.
                    END.
                    IF curr-pay EQ 0 THEN d2 = " ".
                    CREATE output-list.
                    ASSIGN
                        output-list.rechnr      = l-kredit.rechnr
                        output-list.betriebsnr  = l-kredit.betriebsnr
                        output-list.ap-recid    = RECID(l-kredit)
                        output-list.curr-pay    = curr-pay 
                        output-list.firma       = l-lieferant.firma
                        output-list.billdate    = l-kredit.rgdatum
                        output-list.docunr      = l-kredit.NAME
                        output-list.lscheinnr   = l-kredit.lscheinnr
                        output-list.amount      = l-kredit.netto
                        output-list.paid-amount = curr-pay
                        output-list.paiddate    = d2
                        output-list.balance     = l-kredit.netto - curr-pay
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel
                        output-list.desc1       = l-kredit.bemerk
                        output-list.steuercode  = l-kredit.steuercode
                        .
                    t-ap    = t-ap + l-kredit.netto. 
                    t-pay   = t-pay + curr-pay. 
                    t-bal   = t-bal + l-kredit.netto - curr-pay. 
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay. 

                    FIND FIRST queasy WHERE queasy.KEY EQ 221 AND queasy.number1 EQ l-kredit.lief-nr
                        AND queasy.char1 EQ l-kredit.lscheinnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN ASSIGN output-list.recv-date = queasy.date1.
                END.
            END.
        END.
        ELSE
        DO:
            FOR EACH l-kredit WHERE l-kredit.rechnr NE 0
                AND l-kredit.zahlkonto EQ 0
                AND l-kredit.opart GE sorttype1
                AND l-kredit.opart LE sorttype2
                AND l-kredit.rgdatum GE from-date
                AND l-kredit.rgdatum LE to-date
                AND l-kredit.counter GE 0
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix,
                FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-kredit.lief-nr
                NO-LOCK BY l-kredit.rechnr BY l-lieferant.firma BY l-kredit.rgdatum:

                FIND FIRST queasy WHERE queasy.KEY EQ 221 AND queasy.number1 EQ l-kredit.lief-nr
                    AND queasy.char1 EQ l-kredit.lscheinnr NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    do-it = YES.
                    IF l-kredit.opart EQ 1 THEN do-it = NO.
                    IF segm NE 0 AND l-lieferant.segment1 NE segm THEN do-it = NO.
                    IF do-it THEN
                    DO:
                        IF curr-rechnr EQ 0 THEN curr-rechnr = l-kredit.rechnr.
                        IF curr-rechnr NE l-kredit.rechnr THEN
                        DO:
                            CREATE output-list.
                            ASSIGN
                                output-list.firma       = "T O T A L    "
                                output-list.amount      = t-ap
                                output-list.paid-amount = t-pay
                                output-list.balance     = t-bal
                                t-ap  = 0
                                t-pay = 0
                                t-bal = 0
                                curr-rechnr = l-kredit.rechnr
                                .
                        END.
                        curr-pay = 0.
                        IF l-kredit.counter GT 0 THEN
                        DO:
                            FOR EACH l-ap WHERE l-ap.counter EQ l-kredit.counter
                                AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                                BY l-ap.rgdatum:

                                ASSIGN
                                    curr-pay = curr-pay - l-ap.saldo
                                    d2 = STRING(l-ap.rgdatum)
                                    .
                            END.
                        END.
                        IF curr-pay EQ 0 THEN d2 = " ".
                        CREATE output-list.
                        ASSIGN
                            output-list.rechnr      = l-kredit.rechnr
                            output-list.betriebsnr  = l-kredit.betriebsnr 
                            output-list.ap-recid    = RECID(l-kredit) 
                            output-list.curr-pay    = curr-pay 
                            output-list.firma       = l-lieferant.firma
                            output-list.billdate    = l-kredit.rgdatum
                            output-list.docunr      = l-kredit.NAME
                            output-list.lscheinnr   = l-kredit.lscheinnr
                            output-list.amount      = l-kredit.netto
                            output-list.paid-amount = curr-pay
                            output-list.paiddate    = d2
                            output-list.balance     = l-kredit.netto - curr-pay
                            output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel
                            output-list.desc1       = l-kredit.bemerk
                            output-list.steuercode  = l-kredit.steuercode
                            output-list.recv-date   = queasy.date1
                            .
                         t-ap    = t-ap + l-kredit.netto. 
                        t-pay   = t-pay + curr-pay. 
                        t-bal   = t-bal + l-kredit.netto - curr-pay. 
                        tot-ap  = tot-ap + l-kredit.netto. 
                        tot-pay = tot-pay + curr-pay. 
                        tot-bal = tot-bal + l-kredit.netto - curr-pay.
                    END.
                END.
            END.
        END.
        CREATE output-list.
        ASSIGN
            output-list.firma = "T O T A L    "
            output-list.amount = t-ap
            output-list.paid-amount = t-pay
            output-list.balance = t-bal
            t-ap = 0
            t-pay = 0
            t-bal = 0
            .
        CREATE output-list.
        ASSIGN
            output-list.firma = "GRAND TOTAL    "
            output-list.amount = tot-ap
            output-list.paid-amount = tot-pay
            output-list.balance = tot-bal
            .
    END.
    ELSE 
    DO:
        doit = NO.
        FIND FIRST l-lieferant WHERE l-lieferant.firma EQ lastname NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
            IF segm EQ 0 THEN doit = YES.
            ELSE doit = l-lieferant.segment1 EQ segm.
        END.
        IF doit THEN
        DO:
            FOR EACH l-kredit WHERE l-kredit.rechnr NE 0
                AND l-kredit.lief-nr EQ l-lieferant.lief-nr
                AND l-kredit.zahlkonto EQ 0
                AND l-kredit.opart GE sorttype1
                AND l-kredit.opart LE sorttype2
                AND l-kredit.rgdatum GE from-date
                AND l-kredit.rgdatum LE to-date
                AND l-kredit.counter GE 0
                AND l-kredit.netto NE 0
                NO-LOCK USE-INDEX counter_ix 
                BY l-kredit.rechnr BY l-lieferant.firma BY l-kredit.rgdatum:

                do-it = YES.
                IF l-kredit.opart EQ 1 THEN do-it = NO.

                IF do-it THEN
                DO:
                    IF curr-rechnr EQ 0 THEN curr-rechnr = l-kredit.rechnr.
                    IF curr-rechnr NE l-kredit.rechnr THEN
                    DO:
                        CREATE output-list.
                        ASSIGN
                            output-list.firma       = "T O T A L    "
                            output-list.amount      = t-ap
                            output-list.paid-amount = t-pay
                            output-list.balance     = t-bal
                            t-ap  = 0
                            t-pay = 0
                            t-bal = 0
                            curr-rechnr = l-kredit.rechnr
                            .
                    END.
                    curr-pay = 0.
                    IF l-kredit.counter GT 0 THEN
                    DO:
                        FOR EACH l-ap WHERE l-ap.counter EQ l-kredit.counter
                            AND l-ap.zahlkonto GT 0 AND l-ap.opart GT 0 NO-LOCK
                            BY l-ap.rgdatum:

                            ASSIGN
                                curr-pay = curr-pay - l-ap.saldo
                                d2 = STRING(l-ap.rgdatum)
                                .
                        END.
                    END.
                    IF curr-pay EQ 0 THEN d2 = " ".
                    CREATE output-list.
                    ASSIGN
                        output-list.rechnr = l-kredit.rechnr
                        output-list.betriebsnr  = l-kredit.betriebsnr 
                        output-list.ap-recid    = RECID(l-kredit)
                        output-list.curr-pay    = curr-pay
                        output-list.firma       = l-lieferant.firma
                        output-list.billdate    = l-kredit.rgdatum
                        output-list.docunr      = l-kredit.NAME
                        output-list.lscheinnr   = l-kredit.lscheinnr
                        output-list.desc1       = l-kredit.bemerk
                        output-list.steuercode  = l-kredit.steuercode
                        output-list.amount      = l-kredit.netto
                        output-list.paid-amount = curr-pay 
                        output-list.paiddate    = d2
                        output-list.balance     = l-kredit.netto - curr-pay
                        output-list.duedate     = l-kredit.rgdatum + l-kredit.ziel
                        .
                    t-ap  = t-ap + l-kredit.netto. 
                    t-pay = t-pay + curr-pay. 
                    t-bal = t-bal + l-kredit.netto - curr-pay.
                    tot-ap  = tot-ap + l-kredit.netto. 
                    tot-pay = tot-pay + curr-pay. 
                    tot-bal = tot-bal + l-kredit.netto - curr-pay.

                    FIND FIRST queasy WHERE queasy.KEY EQ 221 AND queasy.number1 EQ l-kredit.lief-nr
                        AND queasy.char1 EQ l-kredit.lscheinnr NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN ASSIGN output-list.recv-date = queasy.date1.
                END.
            END.
        END.
        CREATE output-list.
        ASSIGN
            output-list.firma = "T O T A L    "
            output-list.amount = t-ap
            output-list.paid-amount = t-pay
            output-list.balance = t-bal
            .
        CREATE output-list.
        ASSIGN
            output-list.firma = "GRAND TOTAL    "
            output-list.amount = tot-ap
            output-list.paid-amount = tot-pay
            output-list.balance = tot-bal
            .
    END.
END.

