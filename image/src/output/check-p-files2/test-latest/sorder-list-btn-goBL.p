DEFINE TEMP-TABLE str-list 
    FIELD docu-nr AS CHAR FORMAT "x(12)" 
    FIELD s AS CHAR FORMAT "x(135)" 
    FIELD dunit AS CHAR FORMAT "x(8)" 
    FIELD content AS INTEGER 
    FIELD lief-nr AS INTEGER 
    FIELD warenwert AS DECIMAL.
/*Naufal - add cost-list to store department*/
DEFINE WORKFILE cost-list 
    FIELD nr AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(24)".
/*end*/
DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER sorttype     AS INT  NO-UNDO.
DEFINE INPUT PARAMETER s-artnr      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER from-date    AS DATE NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE NO-UNDO.
DEFINE INPUT PARAMETER from-sup     AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER to-sup       AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER closepo      AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.
    
DEFINE VARIABLE amount1 AS DECIMAL. 
DEFINE VARIABLE amount2 AS DECIMAL. 
DEFINE VARIABLE long-digit AS LOGICAL. 
DEFINE VARIABLE show-price AS LOGICAL. 
DEFINE VARIABLE price-decimal AS INTEGER. 
  
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

/*MESSAGE "IN sorder-list-btn-gobl"
    VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
RUN create-costlist.    /*naufal 170320 - get department data*/
IF sorttype = 1 THEN 
DO: 
    IF s-artnr = 0 THEN RUN create-list1. 
    ELSE RUN create-list11. 
END. 
ELSE IF sorttype = 2 THEN 
DO: 
    IF s-artnr = 0 THEN RUN create-list2. 
    ELSE RUN create-list22. 
END.
/*naufal 180320 - add sort by department*/
ELSE IF sorttype = 3 THEN
DO:
    IF s-artnr = 0 THEN RUN create-list3.
    ELSE RUN create-list33.
END.
/*end*/  
/******************************** PROCEDURE ***********************************/ 
PROCEDURE create-list1: 
    DEFINE VARIABLE i AS INTEGER. 
    IF closepo = NO THEN /*OPEN PO ORIGINAL*/
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 
        amount1 = 0. 
        amount2 = 0. 

        FOR EACH l-order WHERE l-order.pos GT 0 AND l-order.loeschflag = 0 
            AND l-order.bestelldatum GE from-date 
            AND l-order.bestelldatum LE to-date AND l-order.betriebsnr = 0 
            NO-LOCK USE-INDEX artnr_index, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-order.lief-nr 
            AND l-lieferant.firma GE from-sup AND l-lieferant.firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
        /* BY l-order.bestelldatum */ BY l-order.docu-nr BY l-order.pos: 

            CREATE str-list. 
            ASSIGN 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.s = STRING(l-order.bestelldatum) 
                 + STRING(l-order.docu-nr, "x(12)") 
                 + STRING(l-order.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(30)") 
                 + STRING(l-order.anzahl, ">>>,>>9.99"). 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        create str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
    ELSE IF closepo = YES THEN /*CLOSE PO DODY 14/06/2017 REQUEST BY ASTON PONTI TS ARTHA*/
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 
        amount1 = 0. 
        amount2 = 0. 

        FOR EACH l-order WHERE l-order.pos GT 0 AND l-order.loeschflag = 1 
            AND l-order.bestelldatum GE from-date 
            AND l-order.bestelldatum LE to-date AND l-order.betriebsnr = 0 
            NO-LOCK USE-INDEX artnr_index, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-order.lief-nr 
            AND l-lieferant.firma GE from-sup AND l-lieferant.firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
        /* BY l-order.bestelldatum */ BY l-order.docu-nr BY l-order.pos: 

            CREATE str-list. 
            ASSIGN 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.s = STRING(l-order.bestelldatum) 
                 + STRING(l-order.docu-nr, "x(12)") 
                 + STRING(l-order.artnr, "9999999") 
                 + STRING(l-artikel.bezeich, "x(30)") 
                 + STRING(l-order.anzahl, ">>>,>>9.99"). 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        create str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
END. 
 
PROCEDURE create-list11: 
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE VARIABLE tot-anz AS DECIMAL INITIAL 0. 
    IF closepo = NO THEN /*OPEN PO ORIGINAL*/
    DO:
        amount1 = 0. 
        amount2 = 0. 
        FOR EACH l-order WHERE l-order.artnr = s-artnr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 0 
            AND l-order.bestelldatum GE from-date AND l-order.bestelldatum LE to-date 
            AND l-order.betriebsnr = 0 NO-LOCK, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup 
            NO-LOCK BY l-order.bestelldatum BY l-order.docu-nr: 
            CREATE str-list. 
            ASSIGN 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.s = STRING(l-order.bestelldatum) 
                   + STRING(l-order.docu-nr, "x(12)") 
                   + STRING(l-order.artnr, "9999999") 
                   + STRING(l-artikel.bezeich, "x(30)") 
                   + STRING(l-order.anzahl, ">>>,>>9.99") 
            . 
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 
            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
            str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9").     
    END.
    ELSE IF closepo = YES THEN /*CLOSE PO DODY 14/06/2017 REQUEST BY ASTON PONTI TS ARTHA*/
    DO:
        amount1 = 0. 
        amount2 = 0. 
        FOR EACH l-order WHERE l-order.artnr = s-artnr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 1
            AND l-order.bestelldatum GE from-date AND l-order.bestelldatum LE to-date 
            AND l-order.betriebsnr = 0 NO-LOCK, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup 
            NO-LOCK BY l-order.bestelldatum BY l-order.docu-nr: 
            CREATE str-list. 
            ASSIGN 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.s = STRING(l-order.bestelldatum) 
                   + STRING(l-order.docu-nr, "x(12)") 
                   + STRING(l-order.artnr, "9999999") 
                   + STRING(l-artikel.bezeich, "x(30)") 
                   + STRING(l-order.anzahl, ">>>,>>9.99") 
            . 
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 
            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
            str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9").         
    END. 
END. 
 
PROCEDURE create-list2: 
    DEFINE VARIABLE i AS INTEGER.
    
    IF closepo = NO THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        amount1 = 0. 
        amount2 = 0. 

        FOR EACH l-orderhdr WHERE l-orderhdr.lieferdatum GE from-date 
            AND l-orderhdr.lieferdatum LE to-date  NO-LOCK, 
            EACH l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 0 
            AND l-order.betriebsnr = 0 NO-LOCK USE-INDEX order_ix,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
            BY l-orderhdr.lieferdatum BY l-lieferant.firma BY l-order.artnr: 

            CREATE str-list. 
            ASSIGN 
              str-list.lief-nr = l-order.lief-nr 
              str-list.docu-nr = l-order.docu-nr 
              str-list.dunit = l-order.lief-fax[3] 
              str-list.content = l-order.txtnr 
              str-list.warenwert = l-order.warenwert 
              str-list.s = STRING(l-order.bestelldatum) 
                + STRING(l-order.docu-nr, "x(12)") 
                + STRING(l-order.artnr, "9999999") 
                + STRING(l-artikel.bezeich, "x(30)") 
                + STRING(l-order.anzahl, ">>>,>>9.99") 
            . 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
    ELSE IF closepo = YES THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        amount1 = 0. 
        amount2 = 0. 

        FOR EACH l-orderhdr WHERE l-orderhdr.lieferdatum GE from-date 
            AND l-orderhdr.lieferdatum LE to-date  NO-LOCK, 
            EACH l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 1 
            AND l-order.betriebsnr = 0 NO-LOCK USE-INDEX order_ix,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
            BY l-lieferant.firma  BY l-orderhdr.lieferdatum BY l-order.artnr: 

            CREATE str-list. 
            ASSIGN 
              str-list.lief-nr = l-order.lief-nr 
              str-list.docu-nr = l-order.docu-nr 
              str-list.dunit = l-order.lief-fax[3] 
              str-list.content = l-order.txtnr 
              str-list.warenwert = l-order.warenwert 
              str-list.s = STRING(l-order.bestelldatum) 
                + STRING(l-order.docu-nr, "x(12)") 
                + STRING(l-order.artnr, "9999999") 
                + STRING(l-artikel.bezeich, "x(30)") 
                + STRING(l-order.anzahl, ">>>,>>9.99") 
            . 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END. 
END. 
 
PROCEDURE create-list22: 
DEFINE VARIABLE i AS INTEGER.
    
    IF closepo = NO THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        amount1 = 0. 
        amount2 = 0. 
        FOR EACH l-orderhdr WHERE l-orderhdr.lieferdatum GE from-date 
            AND l-orderhdr.lieferdatum LE to-date  NO-LOCK, 
            EACH l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 0 
            AND l-order.betriebsnr = 0 AND l-order.artnr = s-artnr 
            NO-LOCK USE-INDEX order_ix,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
            BY l-lieferant.firma BY l-orderhdr.lieferdatum: 

            CREATE str-list. 
            ASSIGN 
            str-list.lief-nr = l-order.lief-nr 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.warenwert = l-order.warenwert 
            str-list.s = STRING(l-order.bestelldatum) 
                + STRING(l-order.docu-nr, "x(12)") 
                + STRING(l-order.artnr, "9999999") 
                + STRING(l-artikel.bezeich, "x(30)") 
                + STRING(l-order.anzahl, ">>>,>>9.99") 
                . 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
            str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
    ELSE IF closepo = YES THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        amount1 = 0. 
        amount2 = 0. 
        FOR EACH l-orderhdr WHERE l-orderhdr.lieferdatum GE from-date 
            AND l-orderhdr.lieferdatum LE to-date  NO-LOCK, 
            EACH l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 1 
            AND l-order.betriebsnr = 0 AND l-order.artnr = s-artnr 
            NO-LOCK USE-INDEX order_ix,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
            BY l-lieferant.firma BY l-orderhdr.lieferdatum: 

            CREATE str-list. 
            ASSIGN 
            str-list.lief-nr = l-order.lief-nr 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.warenwert = l-order.warenwert 
            str-list.s = STRING(l-order.bestelldatum) 
                + STRING(l-order.docu-nr, "x(12)") 
                + STRING(l-order.artnr, "9999999") 
                + STRING(l-artikel.bezeich, "x(30)") 
                + STRING(l-order.anzahl, ">>>,>>9.99") 
                . 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
            str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
END.

PROCEDURE create-list3:
    DEFINE VARIABLE i AS INTEGER. 
    IF closepo = NO THEN /*OPEN PO ORIGINAL*/
    DO:
        FOR EACH str-list:
            DELETE str-list.
        END.

        amount1 = 0. 
        amount2 = 0. 

        FOR EACH l-order WHERE l-order.pos GT 0 AND l-order.loeschflag = 0 
            AND l-order.bestelldatum GE from-date 
            AND l-order.bestelldatum LE to-date AND l-order.betriebsnr = 0 
            NO-LOCK USE-INDEX artnr_index, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-order.lief-nr 
            AND l-lieferant.firma GE from-sup AND l-lieferant.firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK
            BY cost-list.nr BY l-orderhdr.bestelldatum BY l-order.docu-nr BY l-lieferant.firma BY l-order.artnr:

            CREATE str-list. 
            ASSIGN 
                str-list.docu-nr = l-order.docu-nr 
                str-list.dunit = l-order.lief-fax[3] 
                str-list.content = l-order.txtnr 
                str-list.s = STRING(l-order.bestelldatum)
                    + STRING(l-order.docu-nr, "x(12)") 
                    + STRING(l-order.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(30)") 
                    + STRING(l-order.anzahl, ">>>,>>9.99").

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END.

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END.
        END.
        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
    ELSE IF closepo = YES THEN /*CLOSE PO DODY 14/06/2017 REQUEST BY ASTON PONTI TS ARTHA*/
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 
        amount1 = 0. 
        amount2 = 0. 

        FOR EACH l-order WHERE l-order.pos GT 0 AND l-order.loeschflag = 1 
            AND l-order.bestelldatum GE from-date 
            AND l-order.bestelldatum LE to-date AND l-order.betriebsnr = 0 
            NO-LOCK USE-INDEX artnr_index, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-order.lief-nr 
            AND l-lieferant.firma GE from-sup AND l-lieferant.firma LE to-sup NO-LOCK, 
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK 
            BY cost-list.nr BY l-orderhdr.bestelldatum BY l-order.docu-nr BY l-lieferant.firma BY l-order.artnr: 

            CREATE str-list. 
            ASSIGN 
                str-list.docu-nr = l-order.docu-nr 
                str-list.dunit = l-order.lief-fax[3] 
                str-list.content = l-order.txtnr 
                str-list.s = STRING(l-order.bestelldatum) 
                    + STRING(l-order.docu-nr, "x(12)") 
                    + STRING(l-order.artnr, "9999999") 
                    + STRING(l-artikel.bezeich, "x(30)") 
                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        create str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
        str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 
    END.
END.

PROCEDURE create-list33:
    DEFINE VARIABLE i AS INTEGER. 
    DEFINE VARIABLE tot-anz AS DECIMAL INITIAL 0. 
    IF closepo = NO THEN /*OPEN PO ORIGINAL*/
    DO:
        amount1 = 0. 
        amount2 = 0. 
        FOR EACH l-order WHERE l-order.artnr = s-artnr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 0 
            AND l-order.bestelldatum GE from-date AND l-order.bestelldatum LE to-date 
            AND l-order.betriebsnr = 0 NO-LOCK, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup NO-LOCK 
            BY cost-list.nr BY l-orderhdr.bestelldatum BY l-order.docu-nr BY l-lieferant.firma BY l-order.artnr: 
            CREATE str-list. 
            ASSIGN 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.s = STRING(l-order.bestelldatum) 
                   + STRING(l-order.docu-nr, "x(12)") 
                   + STRING(l-order.artnr, "9999999") 
                   + STRING(l-artikel.bezeich, "x(30)") 
                   + STRING(l-order.anzahl, ">>>,>>9.99") 
            . 
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 
            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
            str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9").     
    END.
    ELSE IF closepo = YES THEN /*CLOSE PO DODY 14/06/2017 REQUEST BY ASTON PONTI TS ARTHA*/
    DO:
        amount1 = 0. 
        amount2 = 0. 
        FOR EACH l-order WHERE l-order.artnr = s-artnr 
            AND l-order.pos GT 0 AND l-order.loeschflag = 1
            AND l-order.bestelldatum GE from-date AND l-order.bestelldatum LE to-date 
            AND l-order.betriebsnr = 0 NO-LOCK, 
            FIRST l-orderhdr WHERE l-orderhdr.lief-nr = l-order.lief-nr 
            AND l-orderhdr.docu-nr = l-order.docu-nr NO-LOCK,
            FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,  /*Naufal - validation to get department*/
            FIRST l-artikel WHERE l-artikel.artnr = l-order.artnr NO-LOCK, 
            FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr 
            AND l-lieferant.firma GE from-sup AND firma LE to-sup NO-LOCK 
            BY cost-list.nr BY l-orderhdr.bestelldatum BY l-order.docu-nr BY l-lieferant.firma BY l-order.artnr: 
            CREATE str-list. 
            ASSIGN 
            str-list.docu-nr = l-order.docu-nr 
            str-list.dunit = l-order.lief-fax[3] 
            str-list.content = l-order.txtnr 
            str-list.s = STRING(l-order.bestelldatum) 
                   + STRING(l-order.docu-nr, "x(12)") 
                   + STRING(l-order.artnr, "9999999") 
                   + STRING(l-artikel.bezeich, "x(30)") 
                   + STRING(l-order.anzahl, ">>>,>>9.99") 
            . 
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                        str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 
                    ELSE 
                        str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 
                END. 
            END. 
            IF l-orderhdr.lieferdatum NE ? THEN 
                str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 
            ELSE str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

            str-list.s = str-list.s + STRING(cost-list.bezeich).

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            str-list.s = str-list.s + " ". 
        END. 
            str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 
        IF NOT long-digit THEN 
             str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 
        ELSE str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9").         
    END.
END.

PROCEDURE create-costlist: 
/*DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0.*/
    FOR EACH parameters WHERE progname = "CostCenter" 
        AND section = "Name" AND varname GT "" NO-LOCK: 
        create cost-list. 
        cost-list.nr = INTEGER(parameters.varname). 
        cost-list.bezeich = parameters.vstring. 
    END. 
END.
