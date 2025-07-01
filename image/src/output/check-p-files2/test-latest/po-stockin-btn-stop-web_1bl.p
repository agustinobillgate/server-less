DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD rec-id AS INTEGER
    FIELD vat-no    AS INTEGER
    FIELD vat-value AS DECIMAL.

DEFINE TEMP-TABLE t-l-order LIKE l-order
    FIELD rec-id        AS INT
    FIELD art-bezeich   AS CHAR
    FIELD jahrgang      AS INTEGER
    FIELD alkoholgrad   AS DECIMAL
    FIELD lief-einheit  AS DECIMAL
    FIELD curr-disc     AS INTEGER
    FIELD curr-disc2    AS INTEGER
    FIELD curr-vat      AS INTEGER.

DEFINE INPUT PARAMETER user-init        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER l-orderhdr-recid AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER f-endkum         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER b-endkum         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER m-endkum         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fb-closedate     AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER m-closedate      AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER lief-nr          AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER billdate         AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER docu-nr          AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER lscheinnr        AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER crterm           AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-lager       AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER t-amount         AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR op-list.
DEFINE INPUT PARAMETER TABLE FOR t-l-order.
DEFINE OUTPUT PARAMETER fl-code         AS INTEGER NO-UNDO INIT 0.

DEFINE BUFFER l-art FOR l-artikel.
DEFINE BUFFER l-order1 FOR l-order. 
DEFINE VARIABLE tot-wert AS DECIMAL. 
DEFINE VARIABLE tot-anz  AS DECIMAL. 
DEFINE VARIABLE curr-pos AS INTEGER. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.

FOR EACH op-list:
    FIND FIRST t-l-order WHERE t-l-order.rec-id = op-list.rec-id NO-LOCK NO-ERROR.
    IF AVAILABLE t-l-order THEN DO:
        FIND FIRST l-order WHERE RECID(l-order) = t-l-order.rec-id NO-LOCK NO-ERROR.
        FIND FIRST l-art WHERE l-art.artnr = t-l-order.artnr NO-LOCK NO-ERROR.
        
        RUN create-l-op.
    END.
END.
IF lief-nr NE 0 THEN RUN create-ap.

RUN close-po.

/*ragung add validasi for close*/
FOR EACH queasy WHERE queasy.KEY = 331 
    AND (queasy.char2 EQ "Inv-Cek Reciving" 
    OR queasy.char2 EQ "Inv-Cek Reorg"
    OR queasy.char2 EQ "Inv-Cek Journal"):
    DELETE queasy.
END.

/*Alder - Serverless - Issue 651 - Start*/
PROCEDURE create-l-op:
    DO TRANSACTION:
        IF AVAILABLE l-order THEN
        DO:
            FIND CURRENT l-order EXCLUSIVE-LOCK.
            ASSIGN
                l-order.geliefert = l-order.geliefert + op-list.anzahl /*t-l-order.geliefert*/
                /*l-order.angebot-lief[1] = t-l-order.angebot-lief[1]*/
                l-order.rechnungspreis  = t-l-order.rechnungspreis
                l-order.rechnungswert   = l-order.rechnungswert + t-l-order.rechnungswert 
                l-order.lieferdatum-eff = t-l-order.lieferdatum-eff
                l-order.lief-fax[2]     = bediener.username. 
            FIND CURRENT l-order NO-LOCK.
            RELEASE l-order.
        END.
        
        FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = l-orderhdr-recid NO-LOCK NO-ERROR.
        IF AVAILABLE l-orderhdr THEN
        DO:
            FIND FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr AND l-order1.pos = 0 NO-LOCK NO-ERROR. 
            IF AVAILABLE l-order1 THEN
            DO:
                FIND CURRENT l-order1 EXCLUSIVE-LOCK.
                ASSIGN
                    l-order1.rechnungspreis = l-order1.rechnungspreis + op-list.einzelpreis
                    l-order1.rechnungswert = l-order1.rechnungswert + op-list.einzelpreis. 
                FIND CURRENT l-order1 NO-LOCK.
                RELEASE l-order1.
            END.
        END.

        IF AVAILABLE l-art THEN
        DO:
            IF l-art.ek-aktuell NE op-list.einzelpreis THEN 
            DO: 
                FIND CURRENT l-art EXCLUSIVE-LOCK. 
                ASSIGN
                    l-art.ek-letzter = l-art.ek-aktuell
                    l-art.ek-aktuell = op-list.einzelpreis. 
                FIND CURRENT l-art NO-LOCK. 
            END.

            IF ((l-art.endkum = f-endkum OR l-art.endkum = b-endkum) AND billdate LE fb-closedate) OR (l-art.endkum GE m-endkum AND billdate LE m-closedate) THEN 
            DO: 
                /* UPDATE stock onhand  */ 
                FIND FIRST l-bestand WHERE l-bestand.lager-nr = 0 AND l-bestand.artnr = l-art.artnr NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE l-bestand THEN 
                DO: 
                    CREATE l-bestand. 
                    ASSIGN
                        l-bestand.anf-best-dat = billdate
                        l-bestand.artnr = l-art.artnr. 
                END. 
                ELSE
                DO:
                    FIND CURRENT l-bestand EXCLUSIVE-LOCK.
                    ASSIGN
                        l-bestand.anz-eingang  = l-bestand.anz-eingang + op-list.anzahl
                        l-bestand.wert-eingang = l-bestand.wert-eingang + op-list.warenwert 
                        tot-anz  = l-bestand.anz-anf-best + l-bestand.anz-eingang - l-bestand.anz-ausgang 
                        tot-wert = l-bestand.val-anf-best + l-bestand.wert-eingang - l-bestand.wert-ausgang. 
                    FIND CURRENT l-bestand NO-LOCK. 
                    RELEASE l-bestand.
                END.
         
                FIND FIRST l-bestand WHERE l-bestand.lager-nr = op-list.lager-nr AND l-bestand.artnr = l-art.artnr NO-LOCK NO-ERROR. 
                IF NOT AVAILABLE l-bestand THEN 
                DO: 
                    CREATE l-bestand. 
                    ASSIGN
                        l-bestand.anf-best-dat = billdate
                        l-bestand.artnr        = l-art.artnr
                        l-bestand.lager-nr     = op-list.lager-nr. 
                END.
                ELSE
                DO:
                    FIND CURRENT l-bestand EXCLUSIVE-LOCK.
                    ASSIGN
                        l-bestand.anz-eingang = l-bestand.anz-eingang + op-list.anzahl
                        l-bestand.wert-eingang = l-bestand.wert-eingang + op-list.warenwert. 
                    FIND CURRENT l-bestand NO-LOCK. 
                    RELEASE l-bestand.
                END.
         
                /* UPDATE average price */ 
                FIND CURRENT l-art EXCLUSIVE-LOCK.
                IF tot-anz NE 0 THEN l-art.vk-preis = tot-wert / tot-anz. 
                FIND CURRENT l-art NO-LOCK. 
                RELEASE l-art.
            END. 
        END.
     
        /* UPDATE supplier turnover */ 
        FIND FIRST  l-liefumsatz WHERE l-liefumsatz.lief-nr = op-list.lief-nr AND l-liefumsatz.datum = billdate NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-liefumsatz THEN 
        DO: 
            CREATE l-liefumsatz. 
            ASSIGN
                l-liefumsatz.datum = billdate
                l-liefumsatz.lief-nr = op-list.lief-nr. 
        END. 
        ELSE
        DO:
            FIND CURRENT l-liefumsatz EXCLUSIVE-LOCK.
            ASSIGN l-liefumsatz.gesamtumsatz = l-liefumsatz.gesamtumsatz + op-list.warenwert.          
            FIND CURRENT l-liefumsatz NO-LOCK.
            RELEASE l-liefumsatz.   
        END.

        CREATE l-op.
        BUFFER-COPY op-list TO l-op.
        RUN l-op-pos(OUTPUT curr-pos). 
        ASSIGN
            l-op.pos = curr-pos
            l-op.fuellflag = bediener.nr. 

        /*ITA VAT for Vietname*/
        FIND FIRST queasy WHERE queasy.KEY = 304 
            AND queasy.char1 = l-op.lscheinnr 
            AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN 
        DO:
            CREATE queasy.
            ASSIGN queasy.KEY     = 304 
                queasy.char1   = l-op.lscheinnr 
                queasy.number1 = l-op.artnr
                queasy.number2 = op-list.vat-no
                queasy.deci1   = op-list.vat-value.   
            RELEASE queasy.
        END.
        FIND CURRENT l-op NO-LOCK. 
        RUN create-purchase-book. 

        /* create l-ophdr  */ 
        FIND FIRST l-ophdr WHERE l-ophdr.lscheinnr = lscheinnr 
            AND l-ophdr.op-typ = "STI" 
            AND l-ophdr.lager-nr = curr-lager 
            AND l-ophdr.datum = billdate NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE l-ophdr THEN 
        DO: 
            CREATE l-ophdr. 
            ASSIGN
                l-ophdr.datum = billdate
                l-ophdr.lager-nr = curr-lager 
                l-ophdr.docu-nr = docu-nr
                l-ophdr.lscheinnr = lscheinnr 
                l-ophdr.op-typ = "STI". 
            FIND CURRENT l-ophdr NO-LOCK. 
        END.
    END.
END PROCEDURE.



PROCEDURE l-op-pos: 
    DEFINE OUTPUT PARAMETER pos AS INTEGER INITIAL 0. 
    DEFINE buffer l-op1 FOR l-op. 
    pos = 1. 
END PROCEDURE. 

PROCEDURE create-ap: 
    DEFINE VARIABLE ap-license AS LOGICAL INITIAL NO. 
    DEFINE VARIABLE ap-acct AS CHAR. 
    DEFINE VARIABLE do-it AS LOGICAL INITIAL YES. 
 
    FIND FIRST htparam WHERE paramnr = 1016 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN ap-license = htparam.flogical.
    END.
    IF NOT ap-license THEN RETURN. 
 
    FIND FIRST htparam WHERE paramnr = 986 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN ap-acct = htparam.fchar.
    END.

    /*FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN 
    DO: 
        IF l-lieferant.z-code NE "" THEN 
        DO: 
            FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-lieferant.z-code NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acct AND (l-lieferant.z-code NE ap-acct) THEN do-it = NO. 
        END. 
    END.*/

    FIND FIRST gl-acct WHERE gl-acct.fibukonto = ap-acct NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN ASSIGN do-it = NO.
   
    IF do-it THEN 
    DO:
        CREATE l-kredit. 
        ASSIGN 
            l-kredit.name           = docu-nr 
            l-kredit.lief-nr        = lief-nr 
            l-kredit.lscheinnr      = lscheinnr 
            l-kredit.rgdatum        = billdate 
            l-kredit.datum          = ? 
            l-kredit.saldo          = t-amount 
            l-kredit.ziel           = crterm 
            l-kredit.netto          = t-amount 
            l-kredit.bediener-nr    = bediener.nr. 
        CREATE ap-journal. 
        ASSIGN 
            ap-journal.lief-nr        = lief-nr 
            ap-journal.docu-nr        = docu-nr 
            ap-journal.lscheinnr      = lscheinnr 
            ap-journal.rgdatum        = billdate 
            ap-journal.saldo          = t-amount 
            ap-journal.netto          = t-amount 
            ap-journal.userinit       = bediener.userinit 
            ap-journal.zeit           = TIME.
    END. 
END PROCEDURE. 

PROCEDURE close-po:  /* A/P is still OPEN / NOT yet paid   */ 
    DEFINE buffer l-od FOR l-order. 
    DEFINE VARIABLE closed AS LOGICAL INIT YES.
 
    /*FIND FIRST l-od WHERE l-od.docu-nr = docu-nr AND l-od.artnr GT 0 AND 
    l-od.pos GT 0 /*AND (l-od.anzahl GT l-od.geliefert)*/ AND 
    l-od.loeschflag = 0 NO-LOCK NO-ERROR. 
    FIND FIRST l-artikel WHERE l-artikel.artnr = l-od.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE l-od AND ((l-od.anzahl * l-artikel.lief-einheit) GT l-od.geliefert) THEN RETURN. */

    FOR EACH l-od WHERE l-od.docu-nr = docu-nr 
        AND l-od.artnr GT 0 AND l-od.pos GT 0 AND l-od.loeschflag = 0 NO-LOCK,
        FIRST l-artikel WHERE l-artikel.artnr = l-od.artnr NO-LOCK:
        IF (l-od.anzahl * l-artikel.lief-einheit) GT l-od.geliefert THEN
        DO:
            closed = NO.
            LEAVE.
        END.
    END.

    IF NOT closed THEN RETURN.

    FIND FIRST l-od WHERE l-od.docu-nr = docu-nr AND l-od.pos EQ 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-od THEN
    DO:
        FIND CURRENT l-od EXCLUSIVE-LOCK.
        ASSIGN
            l-od.loeschflag      = 1
            l-od.lieferdatum-eff = billdate 
            l-od.lief-fax[3]     = bediener.username. 
        FIND CURRENT l-od NO-LOCK.
    END.
 
    FOR EACH l-od WHERE l-od.docu-nr = docu-nr AND l-od.pos GT 0 AND l-od.loeschflag = 0 EXCLUSIVE-LOCK: 
        ASSIGN
            l-od.loeschflag  = 1
            l-od.lieferdatum = billdate. 
        RELEASE l-od. 
    END. 
 
    fl-code = 1.
END PROCEDURE. 

PROCEDURE create-purchase-book: 
    DEFINE VARIABLE max-anz     AS INTEGER. 
    DEFINE VARIABLE curr-anz    AS INTEGER. 
    DEFINE VARIABLE created     AS LOGICAL INITIAL NO. 
    DEFINE VARIABLE curr-disc   AS INTEGER.
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE buffer l-price1 FOR l-pprice. 
    FIND FIRST htparam WHERE paramnr = 225 NO-LOCK NO-ERROR.    /* max stored p-price */ 
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN max-anz = htparam.finteger.  /* Rulita 211024 | Fixing for serverless */  
    END.
  
    IF max-anz = 0 THEN max-anz = 1. 
    curr-anz = l-art.lieferfrist. 
    
    /*IF curr-anz GT 0 THEN 
    DO: 
        FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr 
            AND l-pprice.bestelldatum = l-op.datum 
            AND l-pprice.einzelpreis = l-op.einzelpreis 
            AND l-pprice.lief-nr = l-op.lief-nr NO-LOCK NO-ERROR. 
        IF AVAILABLE l-pprice THEN RETURN. 
    END.*/

    IF curr-anz GE max-anz THEN 
    DO: 
        FIND FIRST l-price1 WHERE l-price1.artnr = l-op.artnr AND l-price1.counter = 1 USE-INDEX counter_ix EXCLUSIVE-LOCK NO-ERROR. 
        IF AVAILABLE l-price1 THEN 
        DO: 
            l-price1.docu-nr = docu-nr. 
            l-price1.artnr = l-op.artnr. 
            l-price1.anzahl = l-op.anzahl. 
            l-price1.einzelpreis = l-op.einzelpreis. 
            l-price1.warenwert = l-op.warenwert. 
            l-price1.bestelldatum = l-op.datum. 
            l-price1.lief-nr = l-op.lief-nr. 
            l-price1.counter = 0. 
            created = YES. 
        END. 
        DO i = 2 TO curr-anz: 
            FIND FIRST l-pprice WHERE l-pprice.artnr = l-op.artnr AND l-pprice.counter = i USE-INDEX counter_ix NO-LOCK NO-ERROR. 
            IF AVAILABLE l-pprice THEN 
            DO: 
                FIND CURRENT l-pprice EXCLUSIVE-LOCK. 
                l-pprice.counter = l-pprice.counter - 1. 
                FIND CURRENT l-pprice NO-LOCK.
                RELEASE l-pprice.
            END. 
        END. 
        IF created THEN 
        DO: 
            l-price1.counter = curr-anz. 
            FIND CURRENT l-price1 NO-LOCK. 
        END. 
    END. 
    IF NOT created THEN 
    DO: 
        CREATE l-pprice. 
        l-pprice.docu-nr = docu-nr. 
        l-pprice.artnr = l-op.artnr. 
        l-pprice.anzahl = l-op.anzahl. 
        l-pprice.einzelpreis = l-op.einzelpreis. 
        l-pprice.warenwert = l-op.warenwert. 
        l-pprice.bestelldatum = l-op.datum. 
        l-pprice.lief-nr = l-op.lief-nr. 
        l-pprice.counter = curr-anz + 1. 
        l-pprice.betriebsnr = curr-disc. 
        FIND CURRENT l-pprice NO-LOCK. 
        FIND CURRENT l-art EXCLUSIVE-LOCK. 
        l-art.lieferfrist = curr-anz + 1. 
        FIND CURRENT l-art NO-LOCK. 
        RELEASE l-art.
    END. 
END PROCEDURE. 
/*Alder - Serverless - Issue 651 - End*/
