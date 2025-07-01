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
    FIELD lprice        LIKE l-artikel.ek-letzter       /*last-purchase based artikel*/
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
    FIELD avg-cons      AS DECIMAL FORMAT ">>>9.99"        /* 4A959F Rulita 28/09/22| add Average Consumetion */.

DEFINE TEMP-TABLE supp-list
    FIELD sno       AS INT
    FIELD sname     AS CHAR
    FIELD sprice    AS DEC
    FIELD scurr     AS CHAR
    FIELD fdate     AS DATE
    FIELD tdate     AS DATE
    FIELD flag      AS INT
    FIELD sr        AS INT.

DEFINE TEMP-TABLE qsupp-list LIKE supp-list.
DEFINE TEMP-TABLE rsupp-list LIKE supp-list.

DEFINE TEMP-TABLE t-buff-order LIKE l-order.

DEF INPUT  PARAMETER TABLE FOR s-list.
DEF INPUT  PARAMETER docu-nr        AS CHAR FORMAT "x(10)". 
DEF INPUT  PARAMETER flag-oe        AS INT.
DEF INPUT  PARAMETER artno          AS INT.
DEF INPUT  PARAMETER lieferdatum    AS DATE.
DEF OUTPUT PARAMETER pr-no          AS CHAR.
DEF OUTPUT PARAMETER mainno         AS INT.
DEF OUTPUT PARAMETER mainsupp       AS CHAR.
DEF OUTPUT PARAMETER mainprice      AS DEC.
DEF OUTPUT PARAMETER maincurr       AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR qsupp-list.
DEF OUTPUT PARAMETER TABLE FOR rsupp-list.
DEF OUTPUT PARAMETER TABLE FOR supp-list.
DEF OUTPUT PARAMETER TABLE FOR t-buff-order.

DEFINE BUFFER b-order FOR l-order.

FOR EACH supp-list: 
    DELETE supp-list. 
END. 
FOR EACH qsupp-list: 
    DELETE qsupp-list. 
END. 
FOR EACH rsupp-list: 
    DELETE rsupp-list. 
END.

IF flag-oe = 1 THEN
DO:
    FOR EACH l-quote WHERE l-quote.artnr = artno 
        AND l-quote.from-date LE lieferdatum 
        AND l-quote.to-date GE lieferdatum NO-LOCK:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
          CREATE qsupp-list.
          ASSIGN
            qsupp-list.scurr  = l-quote.reserve-char[1]
            qsupp-list.sno    = l-quote.lief-nr 
            qsupp-list.sname  = l-lieferant.firma 
            qsupp-list.sprice = l-quote.unitprice
            qsupp-list.fdate  = l-quote.from-date
            qsupp-list.tdate  = l-quote.to-date
            qsupp-list.flag   = 0.
        END.
    END. 
    FOR EACH l-quote WHERE l-quote.artnr = artno 
        AND lieferdatum GT l-quote.to-date
        AND (lieferdatum - l-quote.to-date) LE 30 NO-LOCK:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-quote.lief-nr NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
          CREATE qsupp-list.
          ASSIGN
            qsupp-list.scurr  = l-quote.reserve-char[1]
            qsupp-list.sno    = l-quote.lief-nr 
            qsupp-list.sname  = l-lieferant.firma 
            qsupp-list.sprice = l-quote.unitprice
            qsupp-list.fdate  = l-quote.from-date
            qsupp-list.tdate  = l-quote.to-date
            qsupp-list.flag   = 1. 
        END.
    END.
END.



FIND FIRST b-order WHERE b-order.artnr = artno AND b-order.lief-nr EQ 0
  AND b-order.docu-nr = docu-nr NO-LOCK NO-ERROR.
IF AVAILABLE b-order THEN
DO:
  FIND PREV b-order WHERE b-order.artnr = artno AND b-order.lief-nr EQ 0 
    AND b-order.bestellart NE "" AND b-order.bestellart NE ? NO-LOCK NO-ERROR.
  IF AVAILABLE b-order THEN
  DO:
      ASSIGN pr-no = b-order.docu-nr.
      /*MT DISP pr-no WITH FRAME frame4. */
      IF INT(ENTRY(2, ENTRY(1, b-order.bestellart, "-"), ";")) NE 0 THEN
      DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = INT(ENTRY(1, ENTRY(1, b-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
          CREATE rsupp-list.
          ASSIGN 
            rsupp-list.scurr  = ENTRY(3, ENTRY(1, b-order.bestellart, "-"), ";")
            rsupp-list.sno    = INT(ENTRY(1, ENTRY(1, b-order.bestellart, "-"), ";"))
            rsupp-list.sname  = l-lieferant.firma
            rsupp-list.sprice = INT(ENTRY(2, ENTRY(1, b-order.bestellart, "-"), ";")) / 100
            rsupp-list.fdate  = DATE(ENTRY(4, ENTRY(1, b-order.bestellart, "-"), ";"))
            rsupp-list.tdate  = DATE(ENTRY(5, ENTRY(1, b-order.bestellart, "-"), ";")).
          IF rsupp-list.tdate LT lieferdatum THEN
            rsupp-list.flag   = 1.
          ELSE
            rsupp-list.flag   = 0.
        END.

      END.
      IF INT(ENTRY(2, ENTRY(2, b-order.bestellart, "-"), ";")) NE 0 THEN
      DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = INT(ENTRY(1, ENTRY(2, b-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
          CREATE rsupp-list.
          ASSIGN 
            rsupp-list.scurr  = ENTRY(3, ENTRY(2, b-order.bestellart, "-"), ";")
            rsupp-list.sno    = INT(ENTRY(1, ENTRY(2, b-order.bestellart, "-"), ";"))
            rsupp-list.sname  = l-lieferant.firma
            rsupp-list.sprice = INT(ENTRY(2, ENTRY(2, b-order.bestellart, "-"), ";")) / 100
            rsupp-list.fdate  = DATE(ENTRY(4, ENTRY(2, b-order.bestellart, "-"), ";"))
            rsupp-list.tdate  = DATE(ENTRY(5, ENTRY(2, b-order.bestellart, "-"), ";")).
          IF rsupp-list.tdate LT lieferdatum THEN
            rsupp-list.flag   = 1.
          ELSE
            rsupp-list.flag   = 0.
        END.
      END.
      IF INT(ENTRY(2, ENTRY(3, b-order.bestellart, "-"), ";")) NE 0 THEN
      DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = INT(ENTRY(1, ENTRY(3, b-order.bestellart, "-"), ";")) NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
          CREATE rsupp-list.
          ASSIGN 
            rsupp-list.scurr  = ENTRY(3, ENTRY(3, b-order.bestellart, "-"), ";")
            rsupp-list.sno    = INT(ENTRY(1, ENTRY(3, b-order.bestellart, "-"), ";"))
            rsupp-list.sname  = l-lieferant.firma
            rsupp-list.sprice = INT(ENTRY(2, ENTRY(3, b-order.bestellart, "-"), ";")) / 100
            rsupp-list.fdate  = DATE(ENTRY(4, ENTRY(3, b-order.bestellart, "-"), ";"))
            rsupp-list.tdate  = DATE(ENTRY(5, ENTRY(3, b-order.bestellart, "-"), ";")).
          IF rsupp-list.tdate LT lieferdatum THEN
            rsupp-list.flag   = 1.
          ELSE
            rsupp-list.flag   = 0.
        END.
      END.
  END.
END.

FIND FIRST s-list WHERE s-list.artnr = artno NO-LOCK NO-ERROR.
IF AVAILABLE s-list THEN
DO:
    IF s-list.du-price1 NE 0 THEN
    DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp1 NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
            CREATE supp-list.
            ASSIGN 
              supp-list.scurr  = s-list.curr1 
              supp-list.sno    = s-list.supp1  
              supp-list.sname  = l-lieferant.firma
              supp-list.sprice = s-list.du-price1
              supp-list.fdate  = s-list.fdate1
              supp-list.tdate  = s-list.tdate1.
            IF supp-list.tdate LT lieferdatum THEN
              supp-list.flag   = 1.
            ELSE
              supp-list.flag   = 0.
        END.

    END.

    IF s-list.du-price2 NE 0 THEN
    DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp2 NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
            CREATE supp-list.
            ASSIGN 
              supp-list.sno    = s-list.supp2
              supp-list.sname  = l-lieferant.firma
              supp-list.sprice = s-list.du-price2
              supp-list.scurr  = s-list.curr2
              supp-list.fdate  = s-list.fdate2
              supp-list.tdate  = s-list.tdate2.
            IF supp-list.tdate LT lieferdatum THEN
              supp-list.flag   = 1.
            ELSE
              supp-list.flag   = 0.
        END.
    END.

    IF s-list.du-price3 NE 0 THEN
    DO:
        FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.supp3 NO-LOCK NO-ERROR.
        IF AVAILABLE l-lieferant THEN
        DO:
            CREATE supp-list.
            ASSIGN 
              supp-list.sno    = s-list.supp3
              supp-list.sname  = l-lieferant.firma
              supp-list.sprice = s-list.du-price3
              supp-list.scurr  = s-list.curr3
              supp-list.fdate  = s-list.fdate3
              supp-list.tdate  = s-list.tdate3.
            IF supp-list.tdate LT lieferdatum THEN
              supp-list.flag   = 1.
            ELSE
              supp-list.flag   = 0.
        END.
    END.
END.

FOR EACH rsupp-list:
    FIND FIRST qsupp-list WHERE qsupp-list.sno = rsupp-list.sno AND qsupp-list.sprice = rsupp-list.sprice 
      AND qsupp-list.flag = rsupp-list.flag NO-LOCK NO-ERROR.
    IF AVAILABLE qsupp-list THEN
      DELETE qsupp-list.
END.

FOR EACH supp-list:
    FIND FIRST qsupp-list WHERE qsupp-list.sno = supp-list.sno AND qsupp-list.sprice = supp-list.sprice 
      AND qsupp-list.flag = supp-list.flag NO-LOCK NO-ERROR.
    IF AVAILABLE qsupp-list THEN
      DELETE qsupp-list.
END.

FOR EACH supp-list:
    FIND FIRST rsupp-list WHERE rsupp-list.sno = supp-list.sno AND rsupp-list.sprice = supp-list.sprice 
      AND rsupp-list.flag = supp-list.flag NO-LOCK NO-ERROR.
    IF AVAILABLE rsupp-list THEN
      DELETE rsupp-list.
END.

FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = s-list.angebot-lief[2] NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN
DO:
    ASSIGN
      mainno    = s-list.angebot-lief[2]
      mainsupp  = l-lieferant.firma
      mainprice = s-list.einzelpreis
      maincurr  = s-list.curr.
END.

DEFINE BUFFER buff-order FOR l-order.
FIND FIRST buff-order WHERE buff-order.docu-nr = pr-no 
    AND buff-order.artnr = artno NO-LOCK NO-ERROR.
IF AVAILABLE buff-order THEN
DO:
    CREATE t-buff-order.
    BUFFER-COPY buff-order TO t-buff-order.
END.
