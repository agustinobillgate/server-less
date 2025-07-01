DEF TEMP-TABLE t-l-kredit LIKE l-kredit.
DEFINE BUFFER supplier FOR l-lieferant.
/*DEFINE BUFFER suBuff FOR l-lieferant.*/    /*Alder - Serverless - Issue 559*/
DEFINE BUFFER subuff FOR l-lieferant.        /*Alder - Serverless - Issue 559*/

DEF INPUT  PARAMETER TABLE FOR t-l-kredit.
DEF INPUT  PARAMETER recid-ap       AS INT.
DEF INPUT  PARAMETER orig-liefnr    AS INT.
DEF INPUT  PARAMETER lief-nr        AS INT.
DEF INPUT  PARAMETER firma          AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.

/*
FIND FIRST l-kredit WHERE RECID(l-kredit) = recid-ap NO-LOCK. 
FIND FIRST suBuff   WHERE suBuff.lief-nr   = l-kredit.lief-nr NO-LOCK.
FIND FIRST supplier WHERE supplier.lief-nr = lief-nr NO-LOCK. 
  
FIND FIRST t-l-kredit NO-LOCK.
FIND FIRST l-kredit WHERE RECID(l-kredit) = recid-ap EXCLUSIVE-LOCK.
ASSIGN
    l-kredit.lief-nr = t-l-kredit.lief-nr
    l-kredit.rabatt = t-l-kredit.rabatt 
    l-kredit.rabattbetrag = t-l-kredit.rabattbetrag 
    l-kredit.ziel = t-l-kredit.ziel 
    l-kredit.netto = t-l-kredit.netto 
    l-kredit.bediener-nr = t-l-kredit.bediener-nr
    l-kredit.bemerk = t-l-kredit.bemerk
  . 
IF orig-liefnr NE lief-nr THEN 
DO: 
    FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = l-kredit.NAME 
        EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE gl-jouhdr THEN DO: 
        gl-jouhdr.bezeich = firma. 
        FIND CURRENT gl-jouhdr NO-LOCK. 
    END. 
END. 
FIND FIRST bediener WHERE bediener.userinit = user-init NO-ERROR.
CREATE res-history. 
  ASSIGN 
    res-history.nr = bediener.nr 
    res-history.datum = TODAY 
    res-history.zeit = TIME 
    res-history.aenderung = "P/O " + l-kredit.NAME 
      + "; DeliveryNote " + l-kredit.lscheinnr
      + "; Change Supplier " + suBuff.firma 
      + " -> " + supplier.firma.
    res-history.action = "A/P". 
  FIND CURRENT res-history NO-LOCK. 
  RELEASE res-history.
*/

/*Alder - Serverless - Issue 559 - Start*/
FIND FIRST l-kredit WHERE RECID(l-kredit) EQ recid-ap NO-LOCK NO-ERROR.
IF AVAILABLE l-kredit THEN
DO:
    FIND FIRST subuff WHERE subuff.lief-nr EQ l-kredit.lief-nr NO-LOCK NO-ERROR.
    IF AVAILABLE subuff THEN
    DO:
        FIND FIRST supplier WHERE supplier.lief-nr EQ lief-nr NO-LOCK NO-ERROR.
        IF AVAILABLE supplier THEN
        DO:
            FIND FIRST t-l-kredit NO-LOCK NO-ERROR.
            IF AVAILABLE t-l-kredit THEN
            DO:
                FIND CURRENT l-kredit EXCLUSIVE-LOCK.
                ASSIGN
                    l-kredit.lief-nr = t-l-kredit.lief-nr
                    l-kredit.rabatt = t-l-kredit.rabatt 
                    l-kredit.rabattbetrag = t-l-kredit.rabattbetrag 
                    l-kredit.ziel = t-l-kredit.ziel 
                    l-kredit.netto = t-l-kredit.netto 
                    l-kredit.bediener-nr = t-l-kredit.bediener-nr
                    l-kredit.bemerk = t-l-kredit.bemerk.
                IF orig-liefnr NE lief-nr THEN 
                DO: 
                    FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno EQ l-kredit.NAME NO-LOCK NO-ERROR.
                    IF AVAILABLE gl-jouhdr THEN
                    DO:
                        FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK.
                        ASSIGN gl-jouhdr.bezeich = firma.
                        FIND CURRENT gl-jouhdr NO-LOCK.
                        RELEASE gl-jouhdr.
                    END.
                END. 
                FIND FIRST bediener WHERE bediener.userinit EQ user-init NO-LOCK NO-ERROR.
                IF AVAILABLE bediener THEN
                DO:
                    CREATE res-history. 
                    ASSIGN 
                        res-history.nr          = bediener.nr 
                        res-history.datum       = TODAY 
                        res-history.zeit        = TIME 
                        res-history.aenderung   = "P/O " + l-kredit.NAME 
                                                + "; DeliveryNote " + l-kredit.lscheinnr
                                                + "; Change Supplier " + subuff.firma 
                                                + " -> " + supplier.firma.
                        res-history.action      = "A/P". 
                    FIND CURRENT res-history NO-LOCK. 
                    RELEASE res-history.
                END.
            END.
        END.
    END.
END.
/*Alder - Serverless - Issue 559 - End*/

 
