DEFINE TEMP-TABLE str-list 
  FIELD docu-nr AS CHAR FORMAT "x(12)" 
  FIELD s AS CHAR FORMAT "x(135)" 
  FIELD dunit AS CHAR FORMAT "x(8)" 
  FIELD content AS INTEGER 
  FIELD lief-nr AS INTEGER 
  FIELD warenwert AS DECIMAL.

/*Alder - Serverless - Issue 640*/ /*DEFINE TEMP-TABLE*/
DEFINE TEMP-TABLE str-list2
    FIELD docu-nr                   AS CHARACTER
    FIELD l-order-bestelldatum      AS CHARACTER
    FIELD l-order-docu-nr           AS CHARACTER
    FIELD l-order-artnr             AS CHARACTER
    FIELD l-artikel-bezeich         AS CHARACTER
    FIELD l-order-anzahl            AS CHARACTER
    FIELD l-order-preis             AS CHARACTER
    FIELD l-order-warenwert         AS CHARACTER
    FIELD l-order-geliefert         AS CHARACTER
    FIELD l-order-angebot-lief1     AS CHARACTER
    FIELD l-order-rechnungswert     AS CHARACTER
    FIELD l-orderhdr-lieferdatum    AS CHARACTER
    FIELD l-lieferant-firma         AS CHARACTER
    FIELD cost-list-bezeich         AS CHARACTER
    FIELD dunit                     AS CHARACTER
    FIELD content                   AS INTEGER
    FIELD lief-nr                   AS INTEGER
    FIELD warenwert                 AS DECIMAL.

DEFINE TEMP-TABLE po-list
    FIELD datum         AS DATE
    FIELD document-no   AS CHAR      FORMAT "x(12)"
    FIELD artno         AS INTEGER
    FIELD artdesc       AS CHARACTER FORMAT "x(30)"
    FIELD orderqty      AS INTEGER
    FIELD unit-price    AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD amount1       AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD delivered     AS INTEGER
    FIELD s-unit        AS INTEGER
    FIELD amount2       AS DECIMAL   FORMAT "->,>>>,>>>,>>9.99"
    FIELD delivdate     AS DATE
    FIELD supplier      AS CHARACTER FORMAT "x(30)".

DEFINE WORKFILE cost-list 
    FIELD nr AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(24)".

DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER sorttype  AS INTEGER.
DEFINE INPUT PARAMETER s-artnr   AS INTEGER.
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date   AS DATE.
DEFINE INPUT PARAMETER from-sup  AS CHAR.
DEFINE INPUT PARAMETER to-sup    AS CHAR.
DEFINE INPUT PARAMETER closepo   AS LOGICAL NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR po-list.

DEFINE VARIABLE delidate AS DATE FORMAT "99/99/99".
DEFINE VARIABLE amount1 AS DECIMAL. 
DEFINE VARIABLE amount2 AS DECIMAL. 
DEFINE VARIABLE long-digit AS LOGICAL. 
DEFINE VARIABLE show-price AS LOGICAL. 
DEFINE VARIABLE price-decimal AS INTEGER. 

/*RUN sorder-list-btn-gobl.p(user-init, sorttype, s-artnr, 
                            from-date, to-date, from-sup, to-sup, closepo,
                            OUTPUT TABLE str-list).*/

RUN sorder-list-btn-gobl(
    INPUT user-init,
    INPUT sorttype,
    INPUT s-artnr,
    INPUT from-date,
    INPUT to-date,
    INPUT from-sup,
    INPUT to-sup,
    INPUT closepo,
    OUTPUT TABLE str-list2).

FOR EACH po-list:
    DELETE po-list.
END.

/*FOR EACH str-list:
    IF str-list.s MATCHES "*T O T A L*" THEN 
    DO:
        CREATE po-list.
        ASSIGN 
            artdesc     = "T O T A L"
            amount1     = DECIMAL(TRIM(SUBSTR(str-list.s, 81, 15))).
    END.
    ELSE
    DO:
        delidate = DATE(TRIM(SUBSTR(str-list.s, 123, 8))).

        CREATE po-list.
        ASSIGN
            datum       = DATE(TRIM(SUBSTR(str-list.s, 1, 8)))
            document-no = TRIM(SUBSTR(str-list.s, 9, 12))   
            artno       = INT(TRIM(SUBSTR(str-list.s, 21, 7)))
            artdesc     = TRIM(SUBSTR(str-list.s, 28, 30))  
            orderqty    = INT(TRIM(SUBSTR(str-list.s, 58, 10)))
            unit-price  = DECIMAL(TRIM(SUBSTR(str-list.s, 68, 13)))
            amount1     = DECIMAL(TRIM(SUBSTR(str-list.s, 81, 15)))
            delivered   = INT(TRIM(SUBSTR(str-list.s, 96, 11)))
            s-unit      = INT(TRIM(SUBSTR(str-list.s, 106, 4)))
            amount2     = DECIMAL(TRIM(SUBSTR(str-list.s, 109, 15)))
            delivdate   = delidate
            supplier    = TRIM(SUBSTR(str-list.s, 131, 16))
            .
    END.
END.*/

FOR EACH str-list2:
    IF str-list2.l-order-preis MATCHES "*T O T A L*" THEN
    DO:
        CREATE po-list.
        ASSIGN
            artdesc = "T O T A L"
            amount1 = DECIMAL(str-list2.l-order-warenwert).
    END.
    ELSE
    DO:
        CREATE po-list.
        ASSIGN
            datum       = DATE(str-list2.l-order-bestelldatum)
            document-no = str-list2.l-order-docu-nr
            artno       = INTEGER(str-list2.l-order-artnr)
            artdesc     = str-list2.l-artikel-bezeich
            orderqty    = INTEGER(str-list2.l-order-anzahl)
            unit-price  = DECIMAL(str-list2.l-order-preis)
            amount1     = DECIMAL(str-list2.l-order-warenwert)
            delivered   = INTEGER(str-list2.l-order-geliefert)
            s-unit      = INTEGER(str-list2.l-order-angebot-lief1)
            amount2     = DECIMAL(str-list2.l-order-rechnungswert)
            delivdate   = DATE(str-list2.l-orderhdr-lieferdatum)
            supplier    = str-list2.l-lieferant-firma.
    END.
END.

PROCEDURE sorder-list-btn-gobl:
    DEFINE INPUT PARAMETER user-init    AS CHAR NO-UNDO.
    DEFINE INPUT PARAMETER sorttype     AS INT  NO-UNDO.
    DEFINE INPUT PARAMETER s-artnr      AS INT  NO-UNDO.
    DEFINE INPUT PARAMETER from-date    AS DATE NO-UNDO.
    DEFINE INPUT PARAMETER to-date      AS DATE NO-UNDO.
    DEFINE INPUT PARAMETER from-sup     AS CHAR NO-UNDO.
    DEFINE INPUT PARAMETER to-sup       AS CHAR NO-UNDO.
    DEFINE INPUT PARAMETER closepo      AS LOGICAL NO-UNDO.
    DEFINE OUTPUT PARAMETER TABLE FOR str-list2.
      
    FIND FIRST htparam WHERE htparam.paramnr = 491. 
    price-decimal = htparam.finteger. 
    FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
    long-digit = htparam.flogical. 
    
    /*Alder - Serverless - Issue 640*/ /*IF AVAILABLE*/
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 
    IF AVAILABLE bediener THEN
    DO:
        IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
    END.
    
    /*Alder - Serverless - Issue 640*/ /*IF AVAILABLE*/
    FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        show-price = htparam.flogical. 
    END.
    
    RUN create-costlist.
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
    ELSE IF sorttype = 3 THEN
    DO:
        IF s-artnr = 0 THEN RUN create-list3.
        ELSE RUN create-list33.
    END. 
END PROCEDURE.

PROCEDURE create-list1: 
    DEFINE VARIABLE i AS INTEGER. 
    IF closepo = NO THEN /*OPEN PO ORIGINAL*/
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                    
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99").

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).   /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9").

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99").

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/

                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                     ASSIGN                                                                 /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

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

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/
            
        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99").

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99").

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                         
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/
            
        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END. 
END. 
 
PROCEDURE create-list2: 
    DEFINE VARIABLE i AS INTEGER.
    
    IF closepo = NO THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.lief-nr    = l-order.lief-nr 
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.warenwert  = l-order.warenwert 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.lief-nr               = l-order.lief-nr               /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.warenwer              = l-order.warenwert             /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END.
    ELSE IF closepo = YES THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.lief-nr    = l-order.lief-nr 
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.warenwert  = l-order.warenwert 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.lief-nr               = l-order.lief-nr               /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.warenwert             = l-order.warenwert             /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99").

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                         
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END. 
END. 
 
PROCEDURE create-list22: 
DEFINE VARIABLE i AS INTEGER.
    
    IF closepo = NO THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.lief-nr    = l-order.lief-nr 
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.warenwert  = l-order.warenwert 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.lief-nr               = l-order.lief-nr               /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.warenwert             = l-order.warenwert             /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/
            
        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END.
    ELSE IF closepo = YES THEN
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.lief-nr    = l-order.lief-nr 
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.warenwert  = l-order.warenwert 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.lief-nr               = l-order.lief-nr               /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.warenwert             = l-order.warenwert             /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END.
END.

PROCEDURE create-list3:
    DEFINE VARIABLE i AS INTEGER. 
    IF closepo = NO THEN /*OPEN PO ORIGINAL*/
    DO:
        FOR EACH str-list:
            DELETE str-list.
        END.

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum)
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99").

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END.

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

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

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END.
    ELSE IF closepo = YES THEN /*CLOSE PO DODY 14/06/2017 REQUEST BY ASTON PONTI TS ARTHA*/
    DO:
        FOR EACH str-list: 
            DELETE str-list. 
        END. 

        FOR EACH str-list2:     /*Alder - Serverless - Issue 640*/
            DELETE str-list2.   /*Alder - Serverless - Issue 640*/
        END.                    /*Alder - Serverless - Issue 640*/

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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/

            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99"). 
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9"). 
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 

            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
        END. 

        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/
        
        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
             
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/

                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/

        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9").    

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
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
                str-list.docu-nr    = l-order.docu-nr 
                str-list.dunit      = l-order.lief-fax[3] 
                str-list.content    = l-order.txtnr 
                str-list.s          = STRING(l-order.bestelldatum) 
                                    + STRING(l-order.docu-nr, "x(12)") 
                                    + STRING(l-order.artnr, "9999999") 
                                    + STRING(l-artikel.bezeich, "x(30)") 
                                    + STRING(l-order.anzahl, ">>>,>>9.99"). 

            CREATE str-list2.                                                   /*Alder - Serverless - Issue 640*/
            ASSIGN                                                              /*Alder - Serverless - Issue 640*/
                str-list2.docu-nr               = l-order.docu-nr               /*Alder - Serverless - Issue 640*/
                str-list2.dunit                 = l-order.lief-fax[3]           /*Alder - Serverless - Issue 640*/
                str-list2.content               = l-order.txtnr                 /*Alder - Serverless - Issue 640*/
                str-list2.l-order-bestelldatum  = STRING(l-order.bestelldatum)  /*Alder - Serverless - Issue 640*/
                str-list2.l-order-docu-nr       = STRING(l-order.docu-nr)       /*Alder - Serverless - Issue 640*/
                str-list2.l-order-artnr         = STRING(l-order.artnr)         /*Alder - Serverless - Issue 640*/
                str-list2.l-artikel-bezeich     = STRING(l-artikel.bezeich)     /*Alder - Serverless - Issue 640*/
                str-list2.l-order-anzahl        = STRING(l-order.anzahl).       /*Alder - Serverless - Issue 640*/
            
            IF NOT long-digit THEN 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">>,>>>,>>9.99"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99") + STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>>,>>>,>>9.99"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            ELSE 
            DO: 
                IF show-price THEN 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.einzelpreis, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.einzelpreis).   /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(l-order.rechnungspreis,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(l-order.rechnungspreis).    /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(l-order.warenwert, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(l-order.rechnungswert, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(l-order.warenwert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(l-order.rechnungswert).    /*Alder - Serverless - Issue 640*/
                END. 
                ELSE 
                DO: 
                    IF l-order.geliefert = 0 THEN 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0, ">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                    ELSE 
                    DO:
                        ASSIGN str-list.s = str-list.s + STRING(0,">,>>>,>>>,>>9"). 

                        ASSIGN str-list2.l-order-preis = STRING(0). /*Alder - Serverless - Issue 640*/
                    END.
                        
                    ASSIGN
                        str-list.s = str-list.s + STRING(0, ">,>>>>,>>>,>>9")
                        str-list.s = str-list.s + STRING(l-order.geliefert, "->>>,>>9.99")+ STRING(l-order.angebot-lief[1], ">>9")
                        str-list.s = str-list.s + STRING(0, ">>,>>>,>>>,>>9"). 

                    ASSIGN                                                                  /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-warenwert     = STRING(0)                         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-geliefert     = STRING(l-order.geliefert)         /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-angebot-lief1 = STRING(l-order.angebot-lief[1])   /*Alder - Serverless - Issue 640*/
                        str-list2.l-order-rechnungswert = STRING(0).                        /*Alder - Serverless - Issue 640*/
                END. 
            END. 
            
            IF l-orderhdr.lieferdatum NE ? THEN 
            DO:
                ASSIGN str-list.s = str-list.s + STRING(l-orderhdr.lieferdatum) + STRING(l-lieferant.firma, "x(16)"). 

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING(l-orderhdr.lieferdatum)    /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.
            ELSE 
            DO:
                ASSIGN str-list.s = str-list.s + "        " + STRING(l-lieferant.firma, "x(16)").

                ASSIGN 
                    str-list2.l-orderhdr-lieferdatum    = STRING("")                        /*Alder - Serverless - Issue 640*/
                    str-list2.l-lieferant-firma         = STRING(l-lieferant.firma).        /*Alder - Serverless - Issue 640*/
            END.

            ASSIGN str-list.s = str-list.s + STRING(cost-list.bezeich).

            ASSIGN str-list2.cost-list-bezeich = STRING(cost-list.bezeich). /*Alder - Serverless - Issue 640*/

            IF show-price THEN 
            DO: 
                amount1 = amount1 + l-order.warenwert. 
                amount2 = amount2 + l-order.rechnungswert. 
            END. 
            tot-anz = tot-anz + l-order.anzahl. 
        END. 
        
        CREATE str-list. 
        DO i = 1 TO 67: 
            ASSIGN str-list.s = str-list.s + " ". 
        END. 

        CREATE str-list2.                                   /*Alder - Serverless - Issue 640*/
        ASSIGN                                              /*Alder - Serverless - Issue 640*/
            str-list2.l-order-bestelldatum  = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-docu-nr       = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-artnr         = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-artikel-bezeich     = STRING("")    /*Alder - Serverless - Issue 640*/
            str-list2.l-order-anzahl        = STRING("").   /*Alder - Serverless - Issue 640*/
            
        ASSIGN str-list.s = str-list.s + STRING("T O T A L", "x(10)"). 

        ASSIGN str-list2.l-order-preis = STRING("T O T A L", "x(10)").  /*Alder - Serverless - Issue 640*/

        IF NOT long-digit THEN 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">>,>>>,>>>,>>9.99"). 

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
        ELSE 
        DO:
            ASSIGN str-list.s = str-list.s + STRING(amount1, ">,>>>,>>>,>>>,>>9").   

            ASSIGN str-list2.l-order-warenwert = STRING(amount1).   /*Alder - Serverless - Issue 640*/
        END.
    END.
END PROCEDURE.

PROCEDURE create-costlist: 
    FOR EACH parameters WHERE progname = "CostCenter" 
        AND section = "Name" AND varname GT "" NO-LOCK: 
        CREATE cost-list. 
        ASSIGN
            cost-list.nr = INTEGER(parameters.varname)
            cost-list.bezeich = parameters.vstring. 
    END. 
END PROCEDURE.
