DEF TEMP-TABLE s-list LIKE l-order
    FIELD curr          AS CHAR
    FIELD exrate        AS DEC
    FIELD s-recid       AS INTEGER
    FIELD amount        AS DEC  /*IT 270612 -> add local amount and total*/
    FIELD supp1         AS INT
    FIELD supp2         AS INT /*FT 210912*/
    FIELD supp3         AS INT  
    FIELD suppn1        AS CHAR FORMAT "x(30)"
    FIELD suppn2        AS CHAR FORMAT "x(30)"
    FIELD suppn3        AS CHAR FORMAT "x(30)"
    FIELD supps         AS CHAR FORMAT "x(30)"
    FIELD du-price1     AS DEC
    FIELD du-price2     AS DEC  
    FIELD du-price3     AS DEC
    FIELD curr1         AS CHAR
    FIELD curr2         AS CHAR
    FIELD curr3         AS CHAR
    FIELD fdate1        AS DATE
    FIELD fdate2        AS DATE
    FIELD fdate3        AS DATE
    FIELD tdate1        AS DATE
    FIELD tdate2        AS DATE
    FIELD tdate3        AS DATE
    FIELD desc-coa      AS CHARACTER FORMAT "x(20)"
    FIELD last-pprice   AS DECIMAL
    FIELD avg-pprice    AS DECIMAL        
    FIELD lprice        AS DECIMAL
    FIELD lief-fax2     AS CHARACTER
    FIELD ek-letzter    AS DECIMAL
    FIELD lief-einheit  AS INTEGER
    FIELD supplier      AS CHARACTER
    FIELD lief-fax-2    AS CHARACTER
    FIELD vk-preis      AS DECIMAL
    FIELD soh           AS DECIMAL
    FIELD last-pdate    AS DATE 
    FIELD a-firma       AS CHARACTER
    FIELD last-pbook    AS DECIMAL
    FIELD avg-cons      AS DECIMAL
    .

DEFINE TEMP-TABLE approved
    FIELD nr AS INTEGER
    FIELD flag AS LOGICAL
    FIELD usrid AS CHAR
    FIELD app-date AS DATE
    FIELD app-time AS CHAR.

/* DEFINE TEMP-TABLE t-l-order LIKE l-order. */
DEFINE TEMP-TABLE t-l-lieferant LIKE l-lieferant.
DEFINE TEMP-TABLE old-l-orderhdr LIKE l-orderhdr.
DEFINE TEMP-TABLE old-l-order LIKE l-order.

DEFINE BUFFER t-lieferant FOR l-lieferant.

DEF INPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER TABLE FOR approved.
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER deptnr AS INT.
DEF INPUT PARAMETER comments-screen-value AS CHAR.
DEF INPUT PARAMETER rej-id AS CHAR.
DEF INPUT PARAMETER lieferdatum AS DATE.
DEF INPUT PARAMETER rej-flag AS LOGICAL.
DEF INPUT PARAMETER user-init    AS CHAR.

DEFINE VARIABLE sfdate1 AS CHAR INITIAL "".
DEFINE VARIABLE sfdate2 AS CHAR INITIAL "".
DEFINE VARIABLE sfdate3 AS CHAR INITIAL "".
DEFINE VARIABLE stdate1 AS CHAR INITIAL "".
DEFINE VARIABLE stdate2 AS CHAR INITIAL "".
DEFINE VARIABLE stdate3 AS CHAR INITIAL "".
DEFINE VARIABLE app-id  AS CHAR EXTENT 4 FORMAT "x(11)" FGCOLOR 12. 
DEFINE VARIABLE i       AS INT  INITIAL "".
DEFINE VARIABLE app-str AS CHAR INITIAL "".
DEFINE VARIABLE str     AS CHAR INITIAL "".

DEFINE VARIABLE count-app AS INTEGER NO-UNDO.

DEFINE VARIABLE j AS INTEGER INITIAL 0.
/* DEFINE VARIABLE old-bestellart AS CHAR NO-UNDO.
DEFINE VARIABLE new-bestellart AS CHAR NO-UNDO.*/
DEFINE VARIABLE logstring AS CHAR FORMAT "x(125)" NO-UNDO.
DEF BUFFER sbuff FOR s-list.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id EXCLUSIVE-LOCK.

BUFFER-COPY l-orderhdr TO old-l-orderhdr NO-ERROR.

l-orderhdr.lief-fax[3]      = comments-screen-value.
l-orderhdr.lieferdatum      = lieferdatum.
l-orderhdr.angebot-lief[1]  = deptnr.

IF l-orderhdr.lief-fax[3] NE old-l-orderhdr.lief-fax[3] THEN 
DO:
    IF l-orderhdr.lief-fax[3] EQ ? THEN l-orderhdr.lief-fax[3] = " ".
    IF old-l-orderhdr.lief-fax[3] EQ ? THEN old-l-orderhdr.lief-fax[3] = " ".
    logstring = "[CHG ORDERHDR]DOC NO: " + l-orderhdr.docu-nr 
              + " Order Instruction changed From: " + STRING(old-l-orderhdr.lief-fax[3]) 
              + " To: " + STRING(l-orderhdr.lief-fax[3]).
    RUN create-log (logstring).
END.
IF l-orderhdr.lieferdatum NE old-l-orderhdr.lieferdatum THEN 
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + l-orderhdr.docu-nr 
              + " Needed Date changed From: " + STRING(old-l-orderhdr.lieferdatum) 
              + " To: " + STRING(l-orderhdr.lieferdatum).
    RUN create-log (logstring).
END.
IF l-orderhdr.angebot-lief[1] NE old-l-orderhdr.angebot-lief[1] THEN 
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + l-orderhdr.docu-nr 
              + " Dept No changed From: " + STRING(old-l-orderhdr.angebot-lief[1]) 
              + " To: " + STRING(l-orderhdr.angebot-lief[1]).
    RUN create-log (logstring).
END.

l-orderhdr.lief-fax[2] = "".
DO i = 1 TO 4:
    app-str = "".
    FIND FIRST approved WHERE approved.nr = i NO-LOCK NO-ERROR.
    IF AVAILABLE approved THEN
    DO:
        app-str = approved.usrid + " " + STRING(approved.app-date) + " " + approved.app-time.

        /*ITA export to DP*/
        IF approved.nr = 1 THEN DO:
            FIND FIRST queasy WHERE queasy.KEY = 278
                AND queasy.char1 = l-orderhdr.docu-nr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN DO:
                CREATE queasy.
                ASSIGN queasy.KEY       = 278
                       queasy.char1     = l-orderhdr.docu-nr
                       queasy.logi1     = YES
                       queasy.logi2     = NO
                       queasy.date1     = TODAY
                       queasy.number2   = TIME
                 .
            END.
        END.
    END.
    str = str + app-str + ";".
END.

IF rej-id = ? THEN ASSIGN rej-id = " ".
l-orderhdr.lief-fax[2] = SUBSTR(str,1,LENGTH(str)- 1) + rej-id.


FIND CURRENT l-orderhdr NO-LOCK. 

FOR EACH sbuff:
    FIND FIRST l-order WHERE RECID(l-order) = sbuff.s-recid EXCLUSIVE-LOCK.
    FIND FIRST s-list WHERE s-list.s-recid = INTEGER(RECID(l-order)).
    
    /*DS 03052019 - Add log history*/
    BUFFER-COPY l-order TO old-l-order.
    /* old-bestellart = l-order.bestellart. */    /*Naufal - error tidak bisa reject pr*/
        
    ASSIGN
        l-order.einzelpreis = s-list.einzelpreis
        l-order.anzahl      = s-list.anzahl
        l-order.stornogrund = s-list.stornogrund
        l-order.besteller   = s-list.besteller
        /*M 010612 -> add supplier and currency */
        l-order.angebot-lief[3] = s-list.angebot-lief[3]
        l-order.angebot-lief[2] = s-list.angebot-lief[2]
        l-order.warenwert   = s-list.amount
        l-order.lief-fax[2] = s-list.lief-fax-2.

    IF l-order.einzelpreis NE old-l-order.einzelpreis THEN 
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                    + " - ITEM NO: " + STRING(l-order.artnr)
                    + " DUnit Price changed From: " + STRING(old-l-order.einzelpreis) 
                    + " To: " + STRING(l-order.einzelpreis).
        RUN create-log (logstring).
    END.
    IF l-order.anzahl NE old-l-order.anzahl THEN 
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                    + " - ITEM NO: " + STRING(l-order.artnr)
                    + " Ammount changed From: " + STRING(old-l-order.anzahl) 
                    + " To: " + STRING(l-order.anzahl).
        RUN create-log (logstring).
    END.
    IF l-order.stornogrund NE old-l-order.stornogrund THEN 
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                    + " - ITEM NO: " + STRING(l-order.artnr)
                    + " AcctNo changed From: " + STRING(old-l-order.stornogrund) 
                    + " To: " + STRING(l-order.stornogrund).
        RUN create-log (logstring).
    END.
    IF l-order.besteller NE old-l-order.besteller THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                    + " - ITEM NO: " + STRING(l-order.artnr)
                    + " Remark changed From: " + STRING(old-l-order.besteller) 
                    + " To: " + STRING(l-order.besteller).
        RUN create-log (logstring).
    END.
    IF l-order.angebot-lief[3] NE old-l-order.angebot-lief[3] THEN 
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                    + " - ITEM NO: " + STRING(l-order.artnr)
                    + " Delivery Ammount changed From: " + STRING(old-l-order.angebot-lief[3]) 
                    + " To: " + STRING(l-order.angebot-lief[3]).
        RUN create-log (logstring).
    END.
    
    /*FT 210912*/
    IF s-list.fdate1 = ? THEN 
        ASSIGN sfdate1 = ""
            stdate1 = "".
    ELSE
        ASSIGN sfdate1 = STRING(s-list.fdate1)
            stdate1 = STRING(s-list.tdate1).

    IF s-list.fdate2 = ? THEN
        ASSIGN sfdate2 = ""
            stdate2 = "".
    ELSE
        ASSIGN sfdate2 = STRING(s-list.fdate2)
            stdate2 = STRING(s-list.tdate2).

    IF s-list.fdate3 = ? THEN
        ASSIGN sfdate3 = ""
            stdate3 = "".
    ELSE
        ASSIGN sfdate3 = STRING(s-list.fdate3)
            stdate3 = STRING(s-list.tdate3).

    l-order.bestellart = 
            STRING(s-list.supp1) + ";" + STRING(s-list.du-price1 * 100) + ";" + s-list.curr1 + ";" + sfdate1 + ";" + stdate1 + "-" + 
            STRING(s-list.supp2) + ";" + STRING(s-list.du-price2 * 100) + ";" + s-list.curr2 + ";" + sfdate2 + ";" + stdate2 + "-" +
            STRING(s-list.supp3) + ";" + STRING(s-list.du-price3 * 100) + ";" + s-list.curr3 + ";" + sfdate3 + ";" + stdate3.
    
    IF NUM-ENTRIES(old-l-order.bestellart, "-") > 0 THEN 
    DO:
        DO j = 1 TO NUM-ENTRIES(l-order.bestellart, "-"):
            IF TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NE TRIM(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";"))
            AND TRIM(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";")) EQ "0" THEN
            DO:
                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ INTEGER(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
                IF AVAILABLE l-lieferant THEN 
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is added"
                                + " Value: " + l-lieferant.firma.
                END.
                ELSE 
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is added"
                                + " Value: " + TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")).
                END.
                RUN create-log (logstring).
            END.
            ELSE IF TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NE TRIM(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";"))
            AND TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) EQ "0" THEN
            DO:
                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ INTEGER(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
                IF AVAILABLE l-lieferant THEN 
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is removed"
                                + " Value: " + l-lieferant.firma.
                END.
                ELSE
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is removed"
                                + " Value: " + TRIM(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";")).
                END.
                RUN create-log (logstring).
            END.
            ELSE IF TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NE TRIM(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";")) THEN
            DO:
                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ INTEGER(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
                IF AVAILABLE l-lieferant THEN 
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is changed"
                                + " From: " + l-lieferant.firma.
                END.
                ELSE
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is changed"
                                + " From: " + TRIM(ENTRY(1,ENTRY(j, old-l-order.bestellart, "-"), ";")).
                END.

                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr EQ INTEGER(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
                IF AVAILABLE l-lieferant THEN 
                DO:
                    logstring = logstring
                                + " To: " + l-lieferant.firma.
                END.
                ELSE
                DO:
                    logstring = logstring
                                + " To: " + TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")).
                END.

                RUN create-log (logstring).
            END.
        END.
    END.
    ELSE
    DO:
        DO j = 1 TO NUM-ENTRIES(l-order.bestellart, "-"):
            IF TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NE "0" THEN
            DO:
                FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = INTEGER(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
                IF AVAILABLE l-lieferant THEN 
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is added"
                                + " Value: " + l-lieferant.firma.
                END.
                ELSE 
                DO:
                    logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr 
                                + " - ITEM NO: " + STRING(l-order.artnr)
                                + " Supplier " + STRING(j) + " is added"
                                + " Value: " + TRIM(ENTRY(1,ENTRY(j, l-order.bestellart, "-"), ";")).
                END.

                RUN create-log (logstring).
            END.
        END.
    END.

    /* new-bestellart = l-order.bestellart. */    /*Naufal - error tidak bisa reject pr*/
    
    FIND CURRENT l-order NO-LOCK.
END.

IF rej-flag = YES THEN
FOR EACH l-order WHERE l-order.lief-nr = 0 AND 
    l-order.docu-nr = l-orderhdr.docu-nr:
    ASSIGN 
        l-order.loeschflag = 1.
        /* new-bestellart     = l-order.bestellart. */    /*Naufal - error tidak bisa reject pr*/
END.

/* FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
CREATE res-history.
ASSIGN 
    res-history.nr = bediener.nr
    res-history.datum = TODAY
    res-history.zeit = TIME
    res-history.action = "Supplier"
    res-history.aenderung = "Change Supplier name from: " + CHR(10) + CHR(10) +
        STRING(old-bestellart) + "*** Changed to:" + CHR(10) + CHR(10) +        /*t-l-order.bestellart*/    /*Naufal - error tidak bisa reject pr*/
        STRING(new-bestellart).                                                 /*l-order.bestellart*/      /*Naufal - error tidak bisa reject pr*/

FIND CURRENT res-history NO-LOCK.
RELEASE res-history. */

PROCEDURE create-log:
    DEFINE INPUT PARAMETER aend-str AS CHAR.
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
    CREATE res-history.
    ASSIGN 
        res-history.nr        = bediener.nr
        res-history.datum     = TODAY
        res-history.zeit      = TIME
        res-history.action    = "Purchase Request"
        res-history.aenderung = aend-str.
    
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.
