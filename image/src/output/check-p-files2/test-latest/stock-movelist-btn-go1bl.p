DEFINE TEMP-TABLE str-list 
  FIELD s AS CHAR FORMAT "x(150)"
  FIELD ID  AS CHAR FORMAT "x(4)"
  FIELD m-unit AS CHAR FORMAT "x(7)"
  . 

DEFINE TEMP-TABLE str-list2
    FIELD datum     AS CHARACTER
    FIELD lscheinnr AS CHARACTER
    FIELD init-qty  AS CHARACTER
    FIELD init-val  AS CHARACTER
    FIELD in-qty    AS CHARACTER
    FIELD in-val    AS CHARACTER
    FIELD out-qty   AS CHARACTER
    FIELD out-val   AS CHARACTER
    FIELD note      AS CHARACTER
    FIELD id        AS CHARACTER
    FIELD m-unit    AS CHARACTER.

DEFINE TEMP-TABLE stock-movelist
    FIELD datum     AS DATE
    FIELD lscheinnr AS CHARACTER
    FIELD init-qty  AS DECIMAL FORMAT "->>>,>>9.999"
    FIELD init-val  AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD in-qty    AS DECIMAL FORMAT "->>>,>>9.999"
    FIELD in-val    AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD out-qty   AS DECIMAL FORMAT "->>>,>>9.999"
    FIELD out-val   AS DECIMAL  FORMAT ">,>>>,>>>,>>9.99"
    FIELD note      AS CHARACTER
    FIELD id        AS CHARACTER
    .  

DEF INPUT PARAMETER pvILanguage AS INT.
DEF INPUT PARAMETER s-artnr AS INT.
DEF INPUT PARAMETER show-price AS LOGICAL.
DEF INPUT PARAMETER from-lager AS INT.
DEF INPUT PARAMETER to-lager AS INT.
DEF OUTPUT PARAMETER TABLE FOR stock-movelist.

{ supertransbl.i }
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "stock-movelist".

/*    DEF VAR pvILanguage AS INT INIT 1.
    DEF VAR s-artnr AS INT INIT 3312036.
    DEF VAR show-price AS LOGICAL INIT YES.
    DEF VAR from-lager AS INT INIT 1.
    DEF VAR to-lager AS INT INIT 99.*/

DEFINE VARIABLE tot-anz     AS DECIMAL. 
DEFINE VARIABLE tot-val     AS DECIMAL. 
DEFINE VARIABLE t-anz       AS DECIMAL. 
DEFINE VARIABLE t-val       AS DECIMAL. 
DEFINE VARIABLE long-digit  AS LOGICAL. 
DEFINE VARIABLE t-incoming  AS DECIMAL. /*add by bernatd A5AE8E 2025*/
DEFINE VARIABLE t-inval     AS DECIMAL. /*add by bernatd A5AE8E 2025*/
DEFINE VARIABLE t-outgoing  AS DECIMAL. /*add by bernatd A5AE8E 2025*/
DEFINE VARIABLE t-outval    AS DECIMAL. /*add by bernatd A5AE8E 2025*/

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    ASSIGN long-digit = htparam.flogical.
END.

FIND FIRST l-artikel WHERE l-artikel.artnr EQ s-artnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-artikel THEN RETURN.

/*RUN stock-movelist-btn-gobl.p
    (pvILanguage, s-artnr, show-price, from-lager, to-lager, OUTPUT TABLE str-list).*/

RUN create-list(
    INPUT pvILanguage,
    INPUT s-artnr,
    INPUT show-price,
    INPUT from-lager,
    INPUT to-lager,
    OUTPUT TABLE str-list2).

FOR EACH stock-movelist:
    DELETE stock-movelist.
END.

FOR EACH str-list:
    CREATE stock-movelist.
    ASSIGN             
       stock-movelist.datum        = DATE(SUBSTRING(str-list.s,1,8))        /*Alder - Serverless - Issue 656*/
       stock-movelist.lscheinnr    = SUBSTRING(str-list.s,9,16)             /*Alder - Serverless - Issue 656*/
       stock-movelist.init-qty     = DECIMAL(SUBSTRING(str-list.s,25,12))   /*Alder - Serverless - Issue 656*/
       stock-movelist.init-val     = DECIMAL(SUBSTRING(str-list.s,37,15))   /*Alder - Serverless - Issue 656*/
       stock-movelist.in-qty       = DECIMAL(SUBSTRING(str-list.s,52,14))   /*Alder - Serverless - Issue 656*/
       stock-movelist.in-val       = DECIMAL(SUBSTRING(str-list.s,66,14))   /*Alder - Serverless - Issue 656*/ 
       stock-movelist.out-qty      = DECIMAL(SUBSTRING(str-list.s,80,14))   /*Alder - Serverless - Issue 656*/ 
       stock-movelist.out-val      = DECIMAL(SUBSTRING(str-list.s,94,14))   /*Alder - Serverless - Issue 656*/
       stock-movelist.note         = SUBSTRING(str-list.s,118,13)           /*Alder - Serverless - Issue 656*/
       stock-movelist.id           = str-list.id.
END.

/*FOR EACH stock-movelist:
    DISP stock-movelist.
END.*/

PROCEDURE create-list:
    DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
    DEFINE INPUT PARAMETER s-artnr      AS INTEGER.
    DEFINE INPUT PARAMETER show-price   AS LOGICAL.
    DEFINE INPUT PARAMETER from-lager   AS INTEGER.
    DEFINE INPUT PARAMETER to-lager     AS INTEGER.
    DEFINE OUTPUT PARAMETER TABLE FOR str-list2.

    DEFINE VARIABLE t-qty AS DECIMAL INITIAL 0.
    DEFINE VARIABLE t-wert AS DECIMAL INITIAL 0.
    DEFINE VARIABLE bemerk AS CHARACTER NO-UNDO.
    DEFINE VARIABLE close-date AS DATE NO-UNDO.
    DEFINE VARIABLE preis AS DECIMAL INITIAL 0.
    DEFINE VARIABLE wert AS DECIMAL INITIAL 0.
    DEFINE VARIABLE it-exist AS LOGICAL INITIAL NO NO-UNDO.
    DEFINE VARIABLE last-date AS DATE NO-UNDO.
    DEFINE VARIABLE first-rec AS LOGICAL NO-UNDO.

    DEFINE BUFFER usr FOR bediener.
    DEFINE BUFFER l-oh FOR l-bestand.
    DEFINE BUFFER l-op1 FOR l-op.
    DEFINE BUFFER buf-ophdr FOR l-ophdr.

    IF l-artikel.endkum LE 2 THEN
    DO:
        FIND FIRST htparam WHERE paramnr EQ 221 NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO:
            ASSIGN close-date = htparam.fdate.
        END.
    END.

    FIND FIRST l-oh WHERE l-oh.artnr EQ s-artnr AND l-oh.lager-nr EQ 0 NO-LOCK NO-ERROR.
    IF AVAILABLE l-oh THEN
    DO:
        ASSIGN t-qty = l-oh.anz-anf-best + l-oh.anz-eingang - l-oh.anz-ausgang.
        IF show-price THEN
        DO:
            ASSIGN t-wert = l-oh.val-anf-best + l-oh.wert-eingang - l-oh.wert-ausgang.
        END.
    END.

    FOR EACH str-list2:
        DELETE str-list2.
    END.

    ASSIGN
        tot-anz = 0
        tot-val = 0.

    FOR EACH l-lager WHERE l-lager.lager-nr GE from-lager AND l-lager.lager-nr LE to-lager NO-LOCK:
        FIND FIRST l-bestand WHERE l-bestand.lager-nr EQ l-lager.lager-nr AND l-bestand.artnr EQ s-artnr NO-LOCK NO-ERROR.
        IF AVAILABLE l-bestand THEN
        DO:
            ASSIGN t-anz = l-bestand.anz-anf-best.
            IF show-price THEN
            DO:
                ASSIGN t-val = l-bestand.val-anf-best.
            END.
            CREATE str-list2.
            ASSIGN
                str-list2.datum = ""
                str-list2.lscheinnr = STRING(l-lager.lager-nr) + " " + STRING(l-lager.bezeich).

            CREATE str-list2.
            ASSIGN str-list2.m-unit = l-artikel.masseinheit.
            IF show-price THEN
            DO:
                IF NOT long-digit THEN
                DO:
                    ASSIGN 
                        str-list2.datum = ""
                        str-list2.lscheinnr = ""
                        str-list2.init-qty = STRING("DEBUG").
                END.
                ELSE
                DO:
                END.
            END.
            ELSE
            DO:
                IF NOT long-digit THEN
                DO:
                END.
                ELSE
                DO:
                END.
            END.
        END.
        FOR EACH l-op WHERE l-op.lager-nr EQ l-lager.lager-nr 
            AND l-op.artnr EQ s-artnr 
            AND loeschflag LE 1 
            AND l-op.datum LE close-date 
            NO-LOCK 
            BY l-op.datum 
            BY l-op.op-art:
            ASSIGN it-exist = YES.
            IF show-price THEN
            DO:
                ASSIGN
                    preis = l-op.einzelpreis
                    wert = l-op.warenwert.
            END.
            IF l-op.op-art EQ 1 THEN /*1*/
            DO:
                ASSIGN bemerk = "".
                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ l-op.lief-nr NO-LOCK NO-ERROR.
                IF AVAILABLE l-lieferant THEN
                DO:
                    ASSIGN bemerk = l-lieferant.firma.
                END.
                ASSIGN
                    t-anz = t-anz + l-op.anzahl
                    t-val = t-val + wert.
                CREATE str-list2.
                RUN add-id.
                ASSIGN
                    str-list2.m-unit    = l-artikel.masseinheit
                    str-list2.datum     = STRING(l-op.datum)
                    str-list2.lscheinnr = STRING(l-op.lscheinnr)
                    str-list2.init-qty  = STRING(0)
                    str-list2.init-val  = STRING(0)
                    str-list2.in-qty    = STRING(l-op.anzahl)
                    str-list2.in-val    = STRING(wert)
                    str-list2.out-qty   = STRING(0)
                    str-list2.out-val   = STRING(0)
                    str-list2.note      = STRING(bemerk)
                    t-incoming          = t-incoming + l-op.anzahl
                    t-inval             = t-inval + wert.
            END.
            ELSE IF l-op.op-art EQ 2 THEN /*2*/
            DO:
                IF l-op.herkunftflag EQ 1 THEN
                DO:
                    FIND FIRST l-op1 WHERE l-op1.op-art EQ 4
                        AND l-op1.datum EQ l-op.datum
                        AND l-op1.artnr EQ l-op.artnr
                        AND l-op1.anzahl EQ l-op.anzahl
                        AND l-op1.pos EQ l-op.lager-nr
                        AND l-op1.zeit EQ l-op.zeit
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE l-op1 THEN
                    DO:
                        ASSIGN bemerk = translateExtended("From",lvCAREA,"") + " " + STRING(l-op1.lager-nr).
                    END.
                    ELSE
                    DO:
                        ASSIGN bemerk = translateExtended("Transferred",lvCAREA,"").
                    END.
                END.
                ELSE IF l-op.herkunftflag EQ 3 THEN
                DO:
                    ASSIGN bemerk = translateExtended("Transform In",lvCAREA,"").
                END.
                ASSIGN
                    t-anz = t-anz + l-op.anzahl
                    t-val = t-val + wert.
                CREATE str-list2.
                RUN add-id.
                ASSIGN
                    str-list2.m-unit    = l-artikel.masseinheit
                    str-list2.datum     = STRING(l-op.datum)
                    str-list2.lscheinnr = STRING(l-op.lscheinnr)
                    str-list2.init-qty  = STRING(0)
                    str-list2.init-val  = STRING(0)
                    str-list2.in-qty    = STRING(l-op.anzahl)
                    str-list2.in-val    = STRING(wert)
                    str-list2.out-qty   = STRING(0)
                    str-list2.out-val   = STRING(0)
                    str-list2.note      = STRING(bemerk)
                    t-incoming          = t-incoming + l-op.anzahl
                    t-inval             = t-inval + wert.
            END.
            ELSE IF l-op.op-art EQ 3 THEN /*3*/
            DO:
                ASSIGN bemerk = "".
                IF l-op.stornogrund NE "" THEN
                DO:
                    FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ l-op.stornogrund NO-LOCK NO-ERROR.
                    IF AVAILABLE gl-acct THEN
                    DO:
                        ASSIGN bemerk = gl-acct.fibukonto.
                    END.
                END.
                ELSE
                DO:
                    FIND FIRST l-ophdr WHERE l-ophdr.op-typ EQ "STT"
                        AND l-ophdr.datum EQ l-op.datum
                        AND l-ophdr.lscheinnr EQ l-op.lscheinnr
                        AND l-ophdr.fibukonto NE ""
                        NO-LOCK NO-ERROR.
                    IF AVAILABLE l-ophdr THEN
                    DO:
                        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ l-ophdr.fibukonto NO-LOCK NO-ERROR.
                        IF AVAILABLE gl-acct THEN
                        DO:
                            ASSIGN bemerk = gl-acct.fibukonto.
                        END.
                    END.
                END.
                ASSIGN
                    t-anz = t-anz - l-op.anzahl
                    t-val = t-val - wert.
                CREATE str-list2.
                RUN add-id.
                ASSIGN
                    str-list2.m-unit    = l-artikel.masseinheit
                    str-list2.datum     = STRING(l-op.datum)
                    str-list2.lscheinnr = STRING(l-op.lscheinnr)
                    str-list2.init-qty  = STRING(0)
                    str-list2.init-val  = STRING(0)
                    str-list2.in-qty    = STRING(0)
                    str-list2.in-val    = STRING(0)
                    str-list2.out-qty   = STRING(l-op.anzahl)
                    str-list2.out-val   = STRING(wert)
                    str-list2.note      = STRING(bemerk)
                    t-outgoing          = t-outgoing + l-op.anzahl
                    t-outval            = t-outval + wert.
            END.
            ELSE IF l-op.op-art EQ 4 THEN /*4*/
            DO:
                IF l-op.herkunftflag EQ 1 THEN
                DO:
                    ASSIGN bemerk = translateExtended("To Store",lvCAREA,"") + " " + STRING(l-op.pos).
                END.
                ELSE
                DO:
                    ASSIGN bemerk = translateExtended("Transform Out",lvCAREA,"").
                END.
                ASSIGN
                    t-anz = t-anz - l-op.anzahl
                    t-val = t-val - wert.
                CREATE str-list2.
                ASSIGN
                    str-list2.m-unit    = l-artikel.masseinheit
                    str-list2.datum     = STRING(l-op.datum)
                    str-list2.lscheinnr = STRING(l-op.lscheinnr)
                    str-list2.init-qty  = STRING(0)
                    str-list2.init-val  = STRING(0)
                    str-list2.in-qty    = STRING(0)
                    str-list2.in-val    = STRING(0)
                    str-list2.out-qty   = STRING(l-op.anzahl)
                    str-list2.out-val   = STRING(wert)
                    str-list2.note      = STRING(bemerk)
                    t-outgoing          = t-outgoing + l-op.anzahl
                    t-outval            = t-outval + wert.
            END.
        END.
        IF AVAILABLE l-bestand THEN
        DO:
            ASSIGN
                tot-anz = tot-anz + t-anz
                tot-val = tot-val + t-val.
            IF l-artikel.vk-preis NE 0 THEN
            DO:
                ASSIGN t-val = t-anz * l-artikel.vk-preis.
            END.
            CREATE str-list2.
            ASSIGN
                str-list2.m-unit = l-artikel.masseinheit
                str-list2.datum = ""
                str-list2.lscheinnr = STRING(translateExtended("Stock Onhand:",lvCAREA,""))
                str-list2.init-qty = STRING(t-anz)
                str-list2.init-val = STRING(t-val).
        END.
    END.
    CREATE str-list2.
    CREATE str-list2.
    IF l-artikel.vk-preis NE 0 THEN
    DO:
        ASSIGN t-wert = t-qty * l-artikel.vk-preis.
    END.
    ASSIGN
        str-list2.datum = ""
        str-list2.lscheinnr = "T O T A L :     "
        str-list2.init-qty  = STRING(t-qty)
        str-list2.init-val  = STRING(t-wert)
        str-list2.in-qty    = STRING(t-incoming)
        str-list2.in-val    = STRING(t-inval)
        str-list2.out-qty   = STRING(t-outgoing)
        str-list2.out-val   = STRING(t-outval).
    IF NOT it-exist THEN
    DO:
        FOR EACH l-ophis WHERE l-ophis.artnr EQ s-artnr
            AND l-ophis.op-art EQ 1
            NO-LOCK
            BY l-ophis.datum
            DESCENDING:
            ASSIGN last-date = l-ophis.datum.
            LEAVE.
        END.
        ASSIGN first-rec = YES.
        FOR EACH l-ophis WHERE l-ophis.artnr EQ s-artnr
            AND l-ophis.op-art EQ 1
            AND l-ophis.datum EQ last-date
            NO-LOCK:
            CREATE str-list2.
            IF first-rec THEN
            DO:
                ASSIGN
                    str-list2.m-unit = l-artikel.masseinheit
                    str-list2.datum = STRING(l-ophis.datum)
                    str-list2.lscheinnr = STRING(translateExtended("Last Receiving:",lvCAREA,""))
                    /*str-list2.init-qty*/
                    /*str-list2.init-val*/
                    str-list2.in-qty    = STRING(l-ophis.anzahl)
                    str-list2.in-val    = STRING(l-ophis.warenwert)
                    /*str-list2.out-qty*/
                    /*str-list2.out-val*/.
            END.
            ELSE
            DO:
                ASSIGN
                    str-list2.m-unit    = l-artikel.masseinheit
                    str-list2.datum     = STRING(l-ophis.datum)
                    /*str-list2.lscheinnr*/
                    /*str-list2.init-qty*/
                    /*str-list2.init-val*/
                    str-list2.in-qty    = STRING(l-ophis.anzahl)
                    str-list2.in-val    = STRING(l-ophis.warenwert)
                    /*str-list2.out-qty*/
                    /*str-list2.out-val*/.
            END.
            ASSIGN first-rec = NO.
        END.
        FOR EACH l-ophis WHERE l-ophis.artnr EQ s-artnr
            AND l-ophis.op-art EQ 3
            NO-LOCK
            BY l-ophis.datum
            DESCENDING:
            ASSIGN last-date = l-ophis.datum.
            LEAVE.
        END.
        ASSIGN first-rec = YES.
        FOR EACH l-ophis WHERE l-ophis.artnr EQ s-artnr
            AND l-ophis.op-art EQ 3
            AND l-ophis.datum EQ last-date
            NO-LOCK:
            CREATE str-list2.
            IF first-rec THEN
            DO:
                ASSIGN
                    str-list2.m-unit = l-artikel.masseinheit
                    str-list2.datum = STRING(l-ophis.datum)
                    str-list2.lscheinnr = STRING(translateExtended("Last Outgoing:",lvCAREA,""))
                    /*str-list2.init-qty*/
                    /*str-list2.init-val*/
                    /*str-list2.in-qty*/
                    /*str-list2.in-val*/
                    str-list2.out-qty   = STRING(l-ophis.anzahl)
                    str-list2.out-val   = STRING(l-ophis.warenwert).
            END.
            ELSE
            DO:
                ASSIGN
                    str-list2.m-unit = l-artikel.masseinheit
                    str-list2.datum = STRING(l-ophis.datum)
                    /*str-list2.lscheinnr*/
                    /*str-list2.init-qty*/
                    /*str-list2.init-val*/
                    /*str-list2.in-qty*/
                    /*str-list2.in-val*/
                    str-list2.out-qty   = STRING(l-ophis.anzahl)
                    str-list2.out-val   = STRING(l-ophis.warenwert).
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE add-id:
    DEFINE BUFFER usr FOR bediener.
    FIND FIRST usr WHERE usr.nr EQ l-op.fuellflag NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN
    DO:
        ASSIGN str-list2.id = usr.userinit.
    END.
    ELSE
    DO:
        ASSIGN str-list2.id = "??".
    END.
END PROCEDURE.
