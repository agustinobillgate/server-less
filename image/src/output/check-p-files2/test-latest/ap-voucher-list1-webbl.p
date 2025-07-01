DEFINE TEMP-TABLE age-list
    FIELD supplier          AS CHAR    FORMAT "x(24)"
    FIELD invoice           AS INTEGER
    FIELD datum             AS DATE
    FIELD counter           AS INTEGER
    FIELD debit             AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
    FIELD credit            AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
    FIELD balance           AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" INITIAL 0
    FIELD user-init         AS CHAR FORMAT "x(2)"
    .

DEFINE TEMP-TABLE input-paylist
    FIELD fdate             AS CHARACTER
    FIELD tdate             AS CHARACTER 
    FIELD excl-pay          AS LOGICAL.
    
DEFINE VARIABLE pay-flag    AS LOGICAL INITIAL NO.
DEFINE VARIABLE tot-debit   AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-credit  AS DECIMAL INITIAL 0.
DEFINE VARIABLE tot-balance AS DECIMAL INITIAL 0.

DEFINE VARIABLE from-date   AS DATE.
DEFINE VARIABLE to-date     AS DATE.

DEFINE BUFFER b-kredit FOR l-kredit.

DEFINE INPUT  PARAMETER TABLE FOR input-paylist.
DEFINE OUTPUT PARAMETER TABLE FOR age-list.
            
FIND FIRST input-paylist NO-LOCK.

from-date = DATE(input-paylist.fdate).
to-date   = DATE(input-paylist.tdate).

FOR EACH l-kredit WHERE l-kredit.rechnr NE 0 
    AND l-kredit.rgdatum GE from-date 
    AND l-kredit.rgdatum LE to-date NO-LOCK,
    FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-kredit.lief-nr NO-LOCK
    BY l-kredit.rechnr BY l-lieferant.firma  
    BY l-kredit.rgdatum BY l-kredit.zahlkonto:

    FIND FIRST age-list WHERE age-list.invoice EQ l-kredit.rechnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE age-list THEN
    DO:
        CREATE age-list.
        ASSIGN
            age-list.supplier = l-lieferant.firma + ", " + l-lieferant.anredefirma
            age-list.invoice  = l-kredit.rechnr
            age-list.counter  = l-kredit.counter
            age-list.datum    = l-kredit.rgdatum
            pay-flag          = NO.
            
    END.

    IF l-kredit.zahlkonto EQ 0 AND l-kredit.saldo GT 0 THEN
    DO:
        FIND FIRST bediener WHERE bediener.nr EQ l-kredit.bediener-nr NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
        ASSIGN
            age-list.credit   = age-list.credit + l-kredit.saldo
            age-list.balance  = age-list.balance + l-kredit.saldo
            tot-credit        = tot-credit + l-kredit.saldo
            tot-balance       = tot-balance + l-kredit.saldo.
    END.
    ELSE IF l-kredit.zahlkonto NE 0 AND l-kredit.saldo LT 0 THEN
    DO:
        ASSIGN
            age-list.debit   = age-list.debit + l-kredit.saldo
            age-list.balance = age-list.balance + l-kredit.saldo
            tot-debit        = tot-debit + l-kredit.saldo
            tot-balance      = tot-balance + l-kredit.saldo.
    END.
    

    /* Naufal Afthar - 043772 -> req exclude payment*/
    IF input-paylist.excl-pay THEN
    DO:
        FIND FIRST b-kredit WHERE b-kredit.rechnr EQ age-list.invoice
            AND b-kredit.counter EQ age-list.counter 
            /* Naufal Afthar - 598CFB -> handle next bug year, ex: 12/06/24 < 01/01/25*/
            AND (YEAR(b-kredit.rgdatum) LT YEAR(from-date) 
                 OR (YEAR(b-kredit.rgdatum) EQ YEAR(from-date) 
                     AND MONTH(b-kredit.rgdatum) LT MONTH(from-date))
                 ) NO-LOCK NO-ERROR.
        IF AVAILABLE b-kredit AND b-kredit.zahlkonto NE l-kredit.zahlkonto THEN /* Naufal Afthar - 598CFB -> make sure curr l-kredit is also not a debt*/
        DO:
            IF NOT pay-flag THEN
            DO:
                IF l-kredit.saldo LT 0 THEN
                DO:
                    tot-debit   = tot-debit - l-kredit.saldo.
                    tot-balance = tot-balance - l-kredit.saldo.
                END.
                ELSE IF l-kredit.saldo GT 0 THEN
                DO:
                    
                    tot-credit  = tot-credit - l-kredit.saldo.
                    tot-balance = tot-balance - l-kredit.saldo.
                END.
                pay-flag = YES.
                DELETE age-list.
            END.
            ELSE
            DO:
                pay-flag = NO.
                DELETE age-list.
            END.
        END.
    END.
END.

/* Naufal Afthar - 043772 -> req add total*/
CREATE age-list.
ASSIGN
    age-list.supplier = "T O T A L   "
    age-list.debit    = tot-debit
    age-list.credit   = tot-credit
    age-list.balance  = tot-balance.
/* end Naufal Afthar*/

FOR EACH age-list NO-LOCK:
    DISP age-list WITH WIDTH 300.
END.

