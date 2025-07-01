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
    FIELD last-pprice   AS DECIMAL FORMAT "->>,>>>,>>9.99"  /* Add by Michael @ 09/05/2019 for Luxton Cirebon request - ticket no C071EE */
    FIELD avg-pprice    LIKE l-artikel.vk-preis        
    FIELD lprice        LIKE l-artikel.ek-letzter    /*last-purchase based artikel*/
    FIELD lief-fax2     LIKE l-orderhdr.lief-fax[2]
    FIELD ek-letzter    AS DECIMAL
    FIELD lief-einheit  AS INTEGER
    FIELD supplier      AS CHARACTER
    FIELD lief-fax-2    LIKE l-order.lief-fax[2]
    FIELD vk-preis      LIKE l-artikel.vk-preis 
    FIELD soh           AS DECIMAL
    FIELD last-pdate    AS DATE /*gerald add last purchase date*/
    FIELD a-firma       LIKE l-lieferant.firma   /*gerald last-supplier*/
    FIELD last-pbook    AS DECIMAL FORMAT "->>,>>>,>>9.99" /*gerald last-purchase based pbook*/
    .

DEFINE TEMP-TABLE tt-app-id
    FIELD i-counter AS INTEGER
    FIELD app-id    AS CHAR.

DEFINE TEMP-TABLE t-l-order LIKE l-order.
DEFINE TEMP-TABLE t-l-lieferant LIKE l-lieferant.

DEFINE BUFFER t-lieferant FOR l-lieferant.

DEF INPUT PARAMETER TABLE FOR s-list.
DEF INPUT PARAMETER TABLE FOR tt-app-id.
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
DEFINE VARIABLE app-id AS CHAR EXTENT 4 FORMAT "x(11)" FGCOLOR 12. 
FOR EACH tt-app-id:
    app-id[tt-app-id.i-counter] = tt-app-id.app-id.
END.

DEFINE VARIABLE old-bestellart AS CHAR NO-UNDO.
DEFINE VARIABLE new-bestellart AS CHAR NO-UNDO.
DEF BUFFER sbuff FOR s-list.

FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = rec-id EXCLUSIVE-LOCK.

l-orderhdr.lief-fax[3]      = comments-screen-value.
l-orderhdr.lieferdatum      = lieferdatum.
l-orderhdr.angebot-lief[1]  = deptnr.
l-orderhdr.lief-fax[2]      = app-id[1] + ";" + app-id[2] + ";" + app-id[3] + ";" + app-id[4] + rej-id. 
FIND CURRENT l-orderhdr NO-LOCK. 

FOR EACH sbuff:
    FIND FIRST l-order WHERE RECID(l-order) = sbuff.s-recid 
        EXCLUSIVE-LOCK.
    FIND FIRST s-list WHERE s-list.s-recid = INTEGER(RECID(l-order)).
    
    /*DS 03052019 - Add log history*/
    BUFFER-COPY l-order TO t-l-order.
    old-bestellart = l-order.bestellart.    /*Naufal - error tidak bisa reject pr*/
        
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
    
    new-bestellart = l-order.bestellart.    /*Naufal - error tidak bisa reject pr*/
    
    FIND CURRENT l-order NO-LOCK.
END.

IF rej-flag = YES THEN
FOR EACH l-order WHERE l-order.lief-nr = 0 AND 
    l-order.docu-nr = l-orderhdr.docu-nr:
    ASSIGN 
        l-order.loeschflag = 1
        new-bestellart     = l-order.bestellart.    /*Naufal - error tidak bisa reject pr*/
END.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
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
RELEASE res-history.
