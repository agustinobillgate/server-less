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
    
/* DEFINE VARIABLE fdate     AS DATE INITIAL 01/01/19. */
/* DEFINE VARIABLE tdate     AS DATE INITIAL 11/30/19. */

DEFINE INPUT PARAMETER fdate AS DATE.
DEFINE INPUT PARAMETER tdate AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR age-list.
            
FOR EACH l-kredit WHERE l-kredit.rechnr NE 0 
    /*AND l-kredit.counter GE 0*/ 
    AND l-kredit.rgdatum GE fdate 
    AND l-kredit.rgdatum LE tdate NO-LOCK,
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
            age-list.datum    = l-kredit.rgdatum.
    END.

    IF l-kredit.zahlkonto EQ 0 THEN
    DO:
        FIND FIRST bediener WHERE bediener.nr EQ l-kredit.bediener-nr NO-LOCK NO-ERROR.
        IF AVAILABLE bediener THEN age-list.user-init = bediener.userinit.
        ASSIGN
            age-list.credit   = age-list.credit + l-kredit.saldo
            age-list.balance = age-list.balance + l-kredit.saldo.
    END.
    ELSE
    DO:
        ASSIGN
            age-list.debit  = age-list.debit + l-kredit.saldo
            age-list.balance = age-list.balance + l-kredit.saldo.
    END.

END.
