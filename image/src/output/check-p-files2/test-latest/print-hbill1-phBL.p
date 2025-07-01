/*FT 080616 menambahkan validasi jika reprint sudah beda tanggal,
jika taxnserv pada h-artikel 0, maka mengambil taxnserv h-artikel*/

DEFINE TEMP-TABLE art-list   
  FIELD printed     AS LOGICAL INITIAL NO  
  FIELD disc-flag   AS LOGICAL INITIAL NO   
  FIELD dept        AS INTEGER   
  FIELD artnr       AS INTEGER   
  FIELD bezeich     AS CHAR FORMAT "x(32)"   
  FIELD artart      AS INTEGER   
  FIELD zwkum       AS INTEGER INITIAL 0  
  FIELD qty         AS INTEGER FORMAT "->>>"   
  FIELD price       AS DECIMAL   
  FIELD amount      AS DECIMAL  
  FIELD betrag      AS DECIMAL INITIAL 0  
  FIELD happyhr     AS CHAR FORMAT "x(1)" INITIAL ""  
  FIELD datum       AS DATE  
  FIELD sysdate     AS DATE  
  FIELD zeit        AS INTEGER  
  FIELD condiment   AS INTEGER 
  FIELD i-group     AS INTEGER INIT 0
  INDEX DATE_ix sysdate zeit
.  
DEF TEMP-TABLE t-printer LIKE printer.  
DEF TEMP-TABLE vat-list   
    FIELD vat-amt AS DECIMAL   
    FIELD betrag-amt AS DECIMAL INITIAL 0.   
  
DEFINE TEMP-TABLE output-list  
    FIELD str        AS CHARACTER  
    FIELD pos        AS INT  
    FIELD flag-popup AS LOGICAL INIT NO  
    FIELD npause     AS INT
    FIELD sort-i     AS INT.
  
DEFINE TEMP-TABLE FB-vatlist
    FIELD i-type    AS INTEGER
    FIELD artNo     AS INTEGER
    FIELD vatNo     AS INTEGER
    FIELD bezeich   AS CHAR
    FIELD vatValue  AS DECIMAL INIT 0
    FIELD vatAmt    AS DECIMAL INIT 0
.
DEF TEMP-TABLE t-htp LIKE htparam.

DEF INPUT  PARAMETER pvILanguage        AS INTEGER NO-UNDO.  
DEF INPUT  PARAMETER session-parameter  AS CHAR.  
DEF INPUT  PARAMETER user-init          AS CHAR.  
DEF INPUT  PARAMETER hbrecid            AS INT.  
DEF INPUT  PARAMETER printnr            AS INT.  
DEF INPUT  PARAMETER use-h-queasy       AS LOGICAL.  

DEF INPUT-OUTPUT PARAMETER print-all    AS LOGICAL.  
ASSIGN print-all = YES. /* necessary when printing bill with SCD */

DEF OUTPUT PARAMETER filename           AS CHAR.   
DEF OUTPUT PARAMETER msg-str            AS CHAR.   
DEF OUTPUT PARAMETER winprinterFLag     AS LOGICAL INITIAL NO.  
DEF OUTPUT PARAMETER TABLE FOR output-list.  
DEF OUTPUT PARAMETER TABLE FOR t-printer.  
  
{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "print-hbill1".  
  
DEFINE BUFFER   artBuff      FOR vhp.artikel.  
DEFINE BUFFER   abuff        FOR art-list.  
DEFINE VARIABLE disc-bezeich AS CHAR NO-UNDO.  
DEFINE VARIABLE amount          AS DECIMAL.   
  
DEFINE VARIABLE sort-i          AS INT INIT 0 NO-UNDO.
DEFINE VARIABLE order-id        AS CHAR.  
DEFINE VARIABLE disc-zwkum      AS INTEGER NO-UNDO.  
DEFINE VARIABLE print-balance   AS LOGICAL INITIAL YES.  
DEFINE VARIABLE disc-art1       AS INTEGER INITIAL -1   NO-UNDO.  
DEFINE VARIABLE disc-art2       AS INTEGER INITIAL -1   NO-UNDO.  
DEFINE VARIABLE disc-art3       AS INTEGER INITIAL -1   NO-UNDO.  
DEFINE VARIABLE incl-service    AS LOGICAL.  
DEFINE VARIABLE incl-mwst       AS LOGICAL.  
DEFINE VARIABLE service-taxable AS LOGICAL NO-UNDO.  
DEFINE VARIABLE print-fbTotal   AS LOGICAL INITIAL NO NO-UNDO.  
  
DEFINE VARIABLE prdisc-flag     AS LOGICAL INITIAL NO NO-UNDO.  
  
DEFINE VARIABLE mwst-str        AS CHAR FORMAT "x(16)".  
DEFINE VARIABLE service-str     AS CHAR FORMAT "x(16)".  
DEFINE VARIABLE loctax-str      AS CHAR FORMAT "x(16)".  
  
DEFINE VARIABLE hmargin         AS INTEGER.  
DEFINE VARIABLE bmargin         AS INTEGER INITIAL 1.  
DEFINE VARIABLE lpage           AS INTEGER.  
DEFINE VARIABLE nbezeich        AS INTEGER.   
DEFINE VARIABLE nwidth          AS INTEGER.   
DEFINE VARIABLE npause          AS INTEGER.   
  
DEFINE VARIABLE bill-date110    AS DATE.  
DEFINE VARIABLE bill-date       AS DATE.   
DEFINE VARIABLE price-decimal   AS INTEGER.   
DEFINE VARIABLE n11             AS INTEGER INITIAL 11.   
DEFINE VARIABLE long-digit      AS LOGICAL.   
DEFINE VARIABLE prTwoLine       AS LOGICAL INITIAL NO.  
  
DEFINE VARIABLE printed-line    AS INTEGER INITIAL 0.   
DEFINE VARIABLE last-amount     AS DECIMAL INITIAL 0.   
DEFINE VARIABLE zeit            AS INTEGER.   
DEFINE VARIABLE comp-flag       AS LOGICAL INITIAL NO NO-UNDO.   
  
DEFINE VARIABLE service         AS DECIMAL.   
DEFINE VARIABLE mwst            AS DECIMAL.   
DEFINE VARIABLE vat2            AS DECIMAL.   
DEFINE VARIABLE tot-amount      AS DECIMAL              NO-UNDO.   
  
DEFINE VARIABLE comp-taxserv    AS LOGICAL INITIAL NO NO-UNDO.   
DEFINE VARIABLE tot-sales       AS DECIMAL INITIAL 0    NO-UNDO.   
DEFINE VARIABLE new-item        AS LOGICAL.   
DEFINE VARIABLE printed         AS LOGICAL.   
  
DEFINE VARIABLE qty             AS INTEGER.   
DEFINE VARIABLE do-it           AS LOGICAL INITIAL YES.  
DEFINE VARIABLE rm-transfer     AS LOGICAL INITIAL NO.   
DEFINE VARIABLE new-fbart       AS LOGICAL INITIAL NO.   
DEFINE VARIABLE tot-line        AS INTEGER INITIAL 0.   
DEFINE VARIABLE h-service       AS DECIMAL.  
DEFINE VARIABLE h-mwst          AS DECIMAL.  
DEFINE VARIABLE h-vat2          AS DECIMAL.  
  
DEFINE VARIABLE serv%           AS DECIMAL INITIAL 0.  
DEFINE VARIABLE mwst%           AS DECIMAL INITIAL 0.  
DEFINE VARIABLE vat2%           AS DECIMAL INITIAL 0.  
DEFINE VARIABLE fact            AS DECIMAL INITIAL 1.   
DEFINE VARIABLE mwst1           AS DECIMAL INITIAL 0.   
  
DEFINE VARIABLE subtotal        AS DECIMAL              NO-UNDO.   
DEFINE VARIABLE subtotal2       AS DECIMAL              NO-UNDO.   
DEFINE VARIABLE bline-exist     AS LOGICAL INITIAL NO.  
DEFINE VARIABLE qty1000         AS LOGICAL INITIAL NO. /* if big QTY exists */  
  
DEFINE VARIABLE i               AS INTEGER.  
DEFINE VARIABLE n               AS INTEGER.  
DEFINE VARIABLE curr-j          AS INTEGER.   
DEFINE VARIABLE npage           AS INTEGER.   
  
DEFINE VARIABLE tot-ndisc-line  AS INTEGER INITIAL 0    NO-UNDO.   
DEFINE VARIABLE tot-disc-line   AS INTEGER INITIAL 0    NO-UNDO.   
DEFINE VARIABLE buttom-lines    AS INTEGER INITIAL 0.  
  
DEFINE VARIABLE prTableDesc     AS LOGICAL INITIAL NO.  
DEFINE VARIABLE header1         AS CHAR INITIAL "".  
DEFINE VARIABLE header2         AS CHAR INITIAL "".  
DEFINE VARIABLE foot1           AS CHAR FORMAT "x(32)".   
DEFINE VARIABLE foot2           AS CHAR FORMAT "x(32)".   
DEFINE VARIABLE anz-foot        AS INTEGER INITIAL 0.   
  
DEFINE VARIABLE overhead1       AS INTEGER.   
DEFINE VARIABLE overhead2       AS INTEGER.   
DEFINE VARIABLE overhead3       AS INTEGER.   
DEFINE VARIABLE overhead4       AS INTEGER.   
  
DEFINE VARIABLE total-food      AS DECIMAL INITIAL 0 NO-UNDO.  
DEFINE VARIABLE total-bev       AS DECIMAL INITIAL 0 NO-UNDO.  
DEFINE VARIABLE total-other     AS DECIMAL INITIAL 0 NO-UNDO.  
DEFINE VARIABLE total-Fdisc     AS DECIMAL INITIAL 0 NO-UNDO.  
DEFINE VARIABLE total-Bdisc     AS DECIMAL INITIAL 0 NO-UNDO.  
DEFINE VARIABLE total-Odisc     AS DECIMAL INITIAL 0 NO-UNDO.  

DEFINE VARIABLE gst-logic       AS LOGICAL INITIAL NO.
DEFINE VARIABLE serv-disc       AS LOGICAL INITIAL YES.
DEFINE VARIABLE vat-disc        AS LOGICAL INITIAL YES.
DEFINE VARIABLE f-discArt       AS INTEGER INITIAL -1 NO-UNDO.
DEFINE VARIABLE is-scd          AS LOGICAL INITIAL NO.
DEFINE VARIABLE scd-val         AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE sub-scd-val     AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE serv-scd-val    AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE serv-art        AS INTEGER NO-UNDO.
DEFINE VARIABLE vat-art         AS INTEGER NO-UNDO.

DEFINE VARIABLE sc-art          AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE sc-art1         AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE sc-art2         AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE vat-str         AS CHARACTER         NO-UNDO.

DEFINE VARIABLE oth-art         AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE disc-art        AS INTEGER NO-UNDO.
DEFINE VARIABLE f-discArt1      AS INTEGER NO-UNDO.
DEFINE VARIABLE f-discArt2      AS INTEGER NO-UNDO.
DEFINE VARIABLE scd%            AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE disc            AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE disc-sc         AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE str451          AS CHARACTER FORMAT "x(50)" NO-UNDO.
DEFINE VARIABLE str452          AS CHARACTER FORMAT "x(50)" NO-UNDO.
DEFINE VARIABLE t-str           AS CHARACTER FORMAT "x(50)" NO-UNDO.
DEFINE VARIABLE art-str         AS CHARACTER FORMAT "x(100)" NO-UNDO.

DEFINE VARIABLE loopi           AS INTEGER NO-UNDO.
DEFINE VARIABLE bartnr          AS INTEGER NO-UNDO.
DEFINE VARIABLE is-bev          AS LOGICAL NO-UNDO.
DEFINE VARIABLE is-food         AS LOGICAL NO-UNDO.

/*
DEFINE VARIABLE str451          AS INTEGER EXTENT 10    NO-UNDO.
DEFINE VARIABLE str452          AS INTEGER EXTENT 10    NO-UNDO.
DEFINE VARIABLE cnt             AS INTEGER INITIAL 1    NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 451 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN t-str = htparam.fchar.
t-str = REPLACE(t-str, "," , ";").
t-str = REPLACE(t-str, "-" , ";").
DO WHILE cnt < (LENGTH(t-str) / 4):
    ASSIGN str451[cnt] = INTEGER(ENTRY(cnt, t-str, ";")).
    cnt = cnt + 1.
END.
ASSIGN cnt = 1.
ASSIGN t-str = "".

FIND FIRST htparam WHERE htparam.paramnr = 452 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN t-str = htparam.fchar.
t-str = REPLACE(t-str, "," , ";").
t-str = REPLACE(t-str, "-" , ";").
DO WHILE cnt < (LENGTH(t-str) / 4):
    ASSIGN str452[cnt] = INTEGER(ENTRY(cnt, t-str, ";")).
    cnt = cnt + 1.
END.
*/

FIND FIRST htparam WHERE htparam.paramnr = 468 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN serv-disc = htparam.flogic.

FIND FIRST htparam WHERE htparam.paramnr = 469 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN vat-disc = htparam.flogic.

/* 
SC disc rest articles for food, bev and other will be defined here 
DEFINE VARIABLE sc-art AS INTEGER NO-UNDO.
*/
RUN htpchar.p(451, OUTPUT str451).
str451 = REPLACE(str451, "," , ";").
str451 = REPLACE(str451, "-" , ";").
ASSIGN
    sc-art  = INTEGER(ENTRY(1, str451, ";")) /* SCD rest article for food */
    sc-art1 = INTEGER(ENTRY(2, str451, ";"))
    sc-art2 = INTEGER(ENTRY(3, str451, ";")) NO-ERROR
.

/* VAT, SC and other Taxes will be defined here */
RUN htpchar.p(452, OUTPUT str452).
str452 = REPLACE(str452, "," , ";").
str452 = REPLACE(str452, "-" , ";").
vat-str = TRIM(str452).

FIND FIRST h-bill WHERE RECID(h-bill) = hbrecid NO-LOCK.  
DO loopi = 1 TO NUM-ENTRIES(str452, ";"):
    ASSIGN 
        bartnr  = 0
        bartnr  = INTEGER(ENTRY(loopi, str452, ";")) NO-ERROR
    .
    IF bartnr NE 0 THEN
    DO:
        FIND FIRST h-artikel WHERE h-artikel.artnr = bartnr
            AND h-artikel.departement = h-bill.departement NO-LOCK.
        FIND FIRST htparam WHERE htparam.paramgr = 4 AND htparam.bezeich = h-artikel.bezeich
            NO-LOCK NO-ERROR.
        CREATE FB-vatlist.
        ASSIGN
            FB-vatlist.i-type     = loopi + 1
            FB-vatlist.artNo      = bartnr
            FB-vatlist.vatNo      = htparam.paramnr
            FB-vatlist.bezeich    = h-artikel.bezeich
            FB-vatlist.vatValue   = htparam.fdecimal * 0.01
        .
        IF NUM-ENTRIES(htparam.fchar, " ") GE 2 THEN
            FB-vatlist.vatValue = DECIMAL(ENTRY(2, htparam.fchar, " ")) * 0.0001.
    END.
END.

/* Senior Citizen Discount in % */
RUN htpdec.p(462, OUTPUT scd%).

FIND FIRST htparam WHERE htparam.paramnr = 556 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN f-discArt2 = htparam.finteger.
art-str = TRIM(art-str) + ";" + TRIM(STRING(f-discArt2)).

FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK NO-ERROR.   
IF AVAILABLE htparam THEN f-discArt = htparam.finteger.
art-str = TRIM(art-str) + ";" + TRIM(STRING(f-discArt)).

FIND FIRST htparam WHERE htparam.paramnr = 596 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN f-discArt1 = htparam.finteger.
art-str = TRIM(art-str) + ";" + TRIM(STRING(f-discArt1)).

IF printnr GT 0 THEN   
DO:  
  FIND FIRST vhp.printer WHERE vhp.printer.nr = printnr 
      NO-LOCK NO-ERROR.
  IF NOT AVAILABLE PRINTER THEN
  DO:
      msg-str = translateExtended ("No such Printer Number:",lvCAREA,"")
           + " " + STRING(printnr).
      RETURN.
  END.
  CREATE t-printer.  
  BUFFER-COPY printer TO t-printer.  
END.  

RUN prepare-print-hbill1bl.p  
    (hbrecid, OUTPUT order-id, OUTPUT prdisc-flag, OUTPUT disc-art1,  
     OUTPUT disc-art2, OUTPUT disc-art3, OUTPUT disc-zwkum, OUTPUT print-balance,  
     OUTPUT incl-service, OUTPUT incl-mwst, OUTPUT service-taxable,  
     OUTPUT print-fbTotal).  
  
IF printnr NE 0 THEN   
DO:  
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 132 NO-LOCK.   
  FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.htparam.finteger   
        AND vhp.artikel.departement = 0 NO-LOCK NO-ERROR.   
  IF AVAILABLE vhp.artikel THEN   
  DO:   
      FIND FIRST artBuff WHERE artBuff.artnr = vhp.artikel.artnr  
          AND artBuff.departement = vhp.h-bill.departement NO-LOCK  
          NO-ERROR.  
      IF AVAILABLE artBuff AND artBuff.endkum = artikel.endkum THEN  
          mwst-str = artBuff.bezeich.   
      ELSE mwst-str = vhp.artikel.bezeich.   
  END.  
  
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 133 NO-LOCK.   
  FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.htparam.finteger   
        AND vhp.artikel.departement = 0 NO-LOCK NO-ERROR.   
  IF AVAILABLE vhp.artikel THEN service-str = vhp.artikel.bezeich.   
   
  FIND FIRST vhp.htparam WHERE paramnr = 850 NO-LOCK.   
  hmargin = vhp.htparam.finteger.   
  FIND FIRST vhp.htparam WHERE paramnr = 858 NO-LOCK.   
  IF vhp.htparam.finteger NE 0 THEN bmargin = vhp.htparam.finteger.   
  FIND FIRST vhp.htparam WHERE paramnr = 851 NO-LOCK.   
  lpage = vhp.htparam.finteger.   
  
  FIND FIRST vhp.htparam WHERE paramnr = 871 NO-LOCK.   
  nbezeich = vhp.htparam.finteger.   
  
  FIND FIRST vhp.htparam WHERE paramnr = 831 NO-LOCK.   
  nwidth = vhp.htparam.finteger.   
  FIND FIRST vhp.htparam WHERE paramnr = 890 NO-LOCK.   
  npause = vhp.htparam.finteger.   
   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK.   
  /* bill DATE */   
  ASSIGN  
    bill-date110 = vhp.htparam.fdate  
    bill-date    = vhp.htparam.fdate  
  .   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */   
  IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1.   
   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK.   
  price-decimal = vhp.htparam.finteger.   
  IF price-decimal = 0 THEN n11 = 25.  
    
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 246 NO-LOCK.   
  long-digit = vhp.htparam.flogical.   
  IF long-digit THEN n11 = 25.   
  
  FIND FIRST vhp.htparam WHERE paramnr = 874 NO-LOCK.   
  IF vhp.htparam.feldtyp = 4 AND vhp.htparam.flogical THEN print-all = YES.   
    
  RUN optional-params.  
  IF prTwoLine THEN n11 = 1.  
  
/****** number OF printed lines ON bill ***/   
  IF NOT use-h-queasy THEN   
  DO:   
    FIND FIRST vhp.queasy WHERE vhp.queasy.key = 4   
      AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
      AND vhp.queasy.number2 = 0   
      AND vhp.queasy.deci2   = billnr USE-INDEX rbill_ix NO-LOCK NO-ERROR.   
    IF AVAILABLE vhp.queasy AND NOT print-all THEN   
    DO:   
      ASSIGN  
        printed-line = vhp.queasy.number3   
        last-amount  = vhp.queasy.deci1  
      .   
      IF printed-line = lpage THEN printed-line = 0.   
    END.   
    IF NOT AVAILABLE vhp.queasy THEN   
    DO:   
      CREATE vhp.queasy.  
      ASSIGN  
        vhp.queasy.key     = 4   
        vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
        vhp.queasy.number2 = 0   
        vhp.queasy.deci2   = billnr  
      .  
    END.   
  END.   
  ELSE   
  DO:   
    FIND FIRST vhp.h-queasy WHERE   
      vhp.h-queasy.number1     = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
      AND vhp.h-queasy.number2 = 0   
      AND vhp.h-queasy.billno  = billnr NO-LOCK NO-ERROR.   
    IF AVAILABLE vhp.h-queasy AND NOT print-all THEN   
    DO:  
      ASSIGN   
        printed-line    = vhp.h-queasy.number3   
        last-amount     = vhp.h-queasy.deci1  
      .  
      IF printed-line = lpage THEN printed-line = 0.   
    END.   
    IF NOT AVAILABLE vhp.h-queasy THEN   
    DO:   
      CREATE vhp.h-queasy.   
      ASSIGN  
        vhp.h-queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)  
        vhp.h-queasy.number2 = 0  
        vhp.h-queasy.billno = billnr  
      .  
    END.   
  END.   
   
  FIND FIRST vhp.kellner WHERE vhp.kellner.departement = vhp.h-bill.departement   
    AND vhp.kellner.kellner-nr = vhp.h-bill.kellner-nr NO-LOCK NO-ERROR.   
  FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num   
    = vhp.h-bill.departement NO-LOCK.   
  zeit = time.   
   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 824 NO-LOCK.   
  comp-flag = vhp.htparam.flogical.   
   
  ASSIGN  
    service    = 0   
    mwst       = 0   
    tot-amount = last-amount  
  .   
  
  IF vhp.h-bill.flag = 1 THEN  
  DO:  
    FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr   
      AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.  
    IF AVAILABLE vhp.h-bill-line THEN bill-date = vhp.h-bill-line.bill-datum.  
  END.  
  
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr   
    AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK:   
   
    IF vhp.h-bill-line.artnr NE 0 THEN   
    DO:   
      FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr   
        = vhp.h-bill-line.artnr AND vhp.h-artikel.departement   
        = vhp.h-bill-line.departement NO-LOCK.   
      IF (vhp.h-artikel.artart = 11 OR vhp.h-artikel.artart = 12) 
          THEN comp-taxserv = NOT comp-taxserv.   /*FT*/
      ELSE IF vhp.h-artikel.artart = 0 THEN   
          tot-sales = tot-sales + vhp.h-bill-line.betrag.  
    END.   
   
    ASSIGN  
      new-item = NO  
      printed  = YES  
    .  
  
    IF NOT use-h-queasy THEN   
    DO:   
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 4   
        AND vhp.queasy.number1 = (vhp.h-bill.departement   
                               + vhp.h-bill.rechnr * 100)   
        AND vhp.queasy.number2 = INTEGER(RECID(vhp.h-bill-line))   
        AND vhp.queasy.deci2 = billnr USE-INDEX rbill_ix NO-LOCK NO-ERROR.   
      IF NOT AVAILABLE vhp.queasy THEN   
      DO:   
        new-item = YES.  
        IF printnr GE 0 THEN   
        DO:   
          CREATE vhp.queasy.   
          ASSIGN  
            vhp.queasy.key     = 4   
            vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)  
            vhp.queasy.number2 = INTEGER(RECID(vhp.h-bill-line))  
            vhp.queasy.deci2   = billnr  
          .  
        END.   
      END.   
    END.   
    ELSE   
    DO:   
      FIND FIRST vhp.h-queasy WHERE   
        vhp.h-queasy.number1     = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
        AND vhp.h-queasy.number2 = INTEGER(RECID(vhp.h-bill-line))   
        AND vhp.h-queasy.billno  = billnr NO-LOCK NO-ERROR.   
      IF NOT AVAILABLE vhp.h-queasy THEN   
      DO:   
        new-item = YES.   
        IF printnr GE 0 THEN   
        DO:   
          CREATE vhp.h-queasy.   
          ASSIGN  
            vhp.h-queasy.number1   = (vhp.h-bill.departement   
                                   + vhp.h-bill.rechnr * 100)  
            vhp.h-queasy.number2   = INTEGER(RECID(vhp.h-bill-line))  
            vhp.h-queasy.billno    = billnr  
          .  
        END.   
      END.   
    END.  
  
    IF new-item OR print-all THEN printed = NO.  
    IF (vhp.h-bill-line.artnr = 0 OR vhp.h-artikel.artart NE 0)   
        AND NOT new-item THEN  
    ASSIGN  
        new-item = YES  
        printed  = YES  .  
      
    DO:   
      qty = vhp.h-bill-line.anzahl.   
      IF qty = 0 THEN qty = 1.   
  
      RELEASE art-list.  
      do-it = AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0  
        AND vhp.h-artikel.zwkum NE disc-zwkum.  
      IF do-it THEN  
      FIND FIRST art-list WHERE art-list.artnr = vhp.h-bill-line.artnr   
        AND art-list.dept = vhp.h-bill-line.departement   
        AND art-list.bezeich = vhp.h-bill-line.bezeich   
        AND art-list.price = vhp.h-bill-line.epreis   
        AND art-list.condiment = 0   
        AND NOT art-list.printed NO-LOCK NO-ERROR.   
        
      IF vhp.h-bill-line.artnr = 0 THEN rm-transfer = NOT rm-transfer.   
      IF vhp.h-bill-line.artnr NE 0 THEN   
      DO:   
        IF vhp.h-artikel.artart = 0 AND (new-item OR print-all)   
          THEN new-fbart = YES.   
      END.   
      IF NOT AVAILABLE art-list OR vhp.h-bill-line.betriebsnr = 1 THEN   
      DO:   
        CREATE art-list.   
        ASSIGN   
          art-list.printed  = printed  
          art-list.artnr    = vhp.h-bill-line.artnr   
          art-list.dept     = vhp.h-bill-line.departemen   
          art-list.bezeich  = vhp.h-bill-line.bezeich   
          art-list.price    = vhp.h-bill-line.epreis   
          art-list.datum    = vhp.h-bill-line.bill-datum  
          art-list.sysdate  = vhp.h-bill-line.sysdate  
          art-list.zeit     = vhp.h-bill-line.zeit  
        .   
        IF vhp.h-bill-line.artnr NE 0 THEN   
        ASSIGN  
          art-list.artart = vhp.h-artikel.artart  
          art-list.zwkum  = vhp.h-artikel.zwkum  
        .   
        ELSE art-list.artart = 2.   
   
        IF AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0   
            AND vhp.h-artikel.epreis2 NE 0  
            AND art-list.price = vhp.h-artikel.epreis2 THEN  
            art-list.happyhr = "*".  
  
        IF AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0 THEN   
            art-list.condiment = vhp.h-bill-line.betriebsnr.   
        
        IF prdisc-flag THEN art-list.disc-flag = prdisc-flag AND (art-list.zwkum = disc-zwkum).   
        ELSE art-list.disc-flag = (art-list.zwkum = disc-zwkum).

/* related to SC Discount */
        IF AVAILABLE vhp.h-artikel AND vhp.h-artikel.artart = 0 THEN 
        DO:
            IF h-artikel.artnr = sc-art THEN 
                ASSIGN art-list.i-group = 1.
            ELSE
            DO:
                FIND FIRST FB-vatlist WHERE FB-vatlist.artNo =
                    art-list.artnr NO-ERROR.
                IF AVAILABLE FB-vatlist THEN
                ASSIGN
                    art-list.i-group = FB-vatlist.i-type
                    FB-vatlist.vatAmt = FB-vatlist.vatAmt + h-bill-line.betrag
                .
            END.
        END.

        tot-line = tot-line + 1.   
      END.  
  
      ASSIGN  
        art-list.betrag = art-list.betrag + vhp.h-bill-line.betrag  
        h-service = 0  
        h-mwst    = 0
        h-vat2    = 0.  
  
      ASSIGN amount = vhp.h-bill-line.betrag.
      
      IF art-list.artart = 0 THEN   
      DO:  
        RUN cal-servat (vhp.h-artikel.departement, vhp.h-artikel.artnr,  
          vhp.h-artikel.service-code, vhp.h-artikel.mwst-code, vhp.h-bill-line.bill-datum,  
          OUTPUT serv%, OUTPUT mwst%, OUTPUT vat2%, OUTPUT fact). 

        /* for SC Discount */
        IF art-list.i-group = 0 THEN
        DO:
            RUN inv-cat(h-bill-line.artnr, OUTPUT is-bev, OUTPUT is-food).
            FIND FIRST FB-vatlist WHERE FB-vatlist.i-type = 2.
            IF is-food THEN
            ASSIGN 
                FB-vatlist.vatAmt = FB-vatlist.vatAmt +
                ROUND(h-bill-line.betrag / fact * mwst%, price-decimal)
            .
            FIND FIRST FB-vatlist WHERE FB-vatlist.i-type = 3.
            ASSIGN 
                FB-vatlist.vatAmt = FB-vatlist.vatAmt +
                ROUND(h-bill-line.betrag / fact * serv%, price-decimal)
            .
            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                AND artikel.departement = h-artikel.departement NO-LOCK.
            IF artikel.prov-code NE 0 THEN
            DO:
                FIND FIRST htparam WHERE htparam.paramgr = 4 
                    AND htparam.paramnr = artikel.prov-code NO-LOCK.
                FIND FIRST FB-vatlist WHERE FB-vatlist.bezeich =
                    htparam.bezeich.
                /*IF is-bev THEN
                DO:*/
                FB-vatlist.vatAmt = FB-vatlist.vatAmt +
                ROUND(h-bill-line.betrag / fact * vat2%, price-decimal).
                /*END.*/
            END.
        END.

        IF NOT serv-disc AND h-bill-line.artnr = f-discArt THEN.
        ELSE 
            ASSIGN
                h-service = vhp.h-bill-line.betrag / fact * serv%
                h-service = ROUND(h-service,2).

        IF NOT vat-disc AND h-bill-line.artnr = f-discArt THEN.
        ELSE 
            ASSIGN
                h-mwst = vhp.h-bill-line.betrag / fact * mwst%
                h-mwst = ROUND(h-mwst,2).

        IF NOT vat-disc AND h-bill-line.artnr = f-discArt THEN.
        ELSE
            ASSIGN
                h-vat2 = vhp.h-bill-line.betrag / fact * vat2%
                h-vat2 = ROUND(h-vat2,2).
                        
        IF NOT incl-service THEN   
            ASSIGN  
                amount  = amount - h-service  
                service = service + h-service. 

        IF NOT incl-mwst THEN   
            ASSIGN  
                amount = amount - h-mwst - h-vat2
                /*amount = amount - h-mwst*/
                mwst   = mwst   + h-mwst  
                mwst1  = mwst1  + h-mwst
                vat2   = vat2   + h-vat2.   
        /*IF (art-list.artnr NE vat-art AND art-list.artnr NE serv-art) THEN subtotal = subtotal + amount.*/
        /*IF art-list.artnr NE vat-art OR art-list.artnr NE serv-art OR art-list.artnr NE sc-art OR art-list.artnr NE sc-art1 OR art-list.artnr NE sc-art2 THEN*/
        /*IF amount GE 0 THEN subtotal = subtotal + amount.*/

      END.  
      
      ASSIGN art-list.amount = art-list.amount + amount.  
      IF vhp.h-bill-line.artnr NE 0 THEN art-list.qty = art-list.qty + qty.   
    END.  
  END.  
    
  FOR EACH art-list:   
    IF (art-list.qty = 0 AND ROUND(art-list.amount, 0) = 0) THEN   
    DO:   
      DELETE art-list.   
      tot-line = tot-line - 1.   
      bline-exist = YES.  
    END.   
    ELSE IF art-list.qty GT 999 OR art-list.qty LT -999 THEN qty1000 = YES.  
    IF art-list.artnr EQ vat-art THEN is-scd = YES.
  END.   
    
 
  FOR EACH abuff WHERE (abuff.zwkum = disc-zwkum) AND abuff.bezeich MATCHES ("*-*"):  
    ASSIGN disc-bezeich = REPLACE(abuff.bezeich, "-", "").  
    FIND FIRST art-list WHERE art-list.artnr = abuff.artnr  
        AND art-list.bezeich = disc-bezeich  
        AND art-list.amount = - abuff.amount NO-ERROR.  
    IF AVAILABLE art-list THEN  
    DO:  
      DELETE art-list.  
      DELETE abuff.  
      tot-line = tot-line - 2.  
    END.  
  END.  
  
  FOR EACH abuff WHERE abuff.disc-flag :  
    ASSIGN disc-bezeich = abuff.bezeich.  
    FIND FIRST art-list WHERE art-list.artnr = abuff.artnr  
        AND art-list.bezeich = disc-bezeich  
        AND art-list.amount = - abuff.amount NO-ERROR.  
    IF AVAILABLE art-list THEN  
    DO:  
      DELETE art-list.  
      DELETE abuff.  
      tot-line = tot-line - 2.  
    END.  
  END.  
  
  RUN add-unitprice-text.   
  
  FIND FIRST art-list WHERE art-list.printed = NO NO-ERROR.   
  IF NOT AVAILABLE art-list AND printnr GE 0 AND NOT bline-exist THEN   
  DO:   
    msg-str = msg-str + CHR(2)  
            + translateExtended ("No new bill-lines was found.",lvCAREA,"").  
    RETURN.   
  END.   

   
  RUN check-pages.   
    
  IF printnr GT 0 THEN   
  DO:      
  END.  
  ELSE IF printnr LT 0 THEN   
  DO:   
    filename = "billdir\" + STRING(vhp.h-bill.tischnr) + "_"   
      + STRING(vhp.h-bill.departement,"99").   
  END.   
    
  DO i = 1 TO printed-line:  
      CREATE output-list.  
      output-list.str = output-list.str + STRING("").
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  END.  
  CREATE output-list.
  output-list.sort-i = sort-i.
  sort-i = sort-i + 1.
   
  IF prdisc-flag AND tot-ndisc-line GE 1 AND tot-disc-line GE 1 THEN   
  DO:   
    
    FIND FIRST art-list WHERE art-list.artart = 0 AND NOT art-list.disc-flag   
        AND art-list.i-group = 0
        AND NOT art-list.printed NO-ERROR.   
    n = 0.   
    curr-j = printed-line.   
    DO i = 1 TO npage:   
      IF NOT AVAILABLE art-list THEN i = npage.  
      RUN print-overhead1.   
      DO WHILE AVAILABLE art-list AND (curr-j LE lpage):   
        
        /*DO i = 1 TO NUM-ENTRIES(art-str, ";"):
            IF art-list.artnr EQ INTEGER(ENTRY(i, art-str, ";")) THEN .
            ELSE RUN print-billine.
        END.*/
        RUN print-billine.
        FIND NEXT art-list WHERE art-list.artart = 0 AND NOT art-list.disc-flag   
            AND art-list.i-group = 0          
            AND NOT art-list.printed NO-ERROR.   
        IF NOT AVAILABLE art-list THEN i = npage.  
      END.  


      IF i = npage THEN  /* all bill-lines are printed  */   
      DO:
        RUN print-overhead2(0).   
        /* Modifying @ 28/01/2019 */
        FOR EACH art-list WHERE art-list.artart = 0 AND NOT art-list.disc-flag   
        AND art-list.i-group = 0
        AND NOT art-list.printed:
        /* FOR EACH art-list WHERE art-list.artart = 0 AND art-list.disc-flag: */
        /* End of modifying */
            subtotal = subtotal + art-list.amount.
            RUN print-billine. 
        END.     
        IF new-fbart THEN RUN print-overhead2(1).  
        IF overhead3 GT 0 THEN RUN print-overhead3.   
        IF overhead4 GT 0 OR buttom-lines GE 1 THEN RUN print-overhead4.  
        RUN cut-it.  
/*    page STREAM s1. */   
      END.   
      ELSE IF curr-j GT lpage THEN DO:  
          CREATE output-list.  
          ASSIGN  
              output-list.flag-popup = YES  
              output-list.npause = npause
              output-list.sort-i = sort-i
              sort-i = sort-i + 1.
        curr-j = 0.   
        printed-line = 0.   
      END.     
    END.   
  END.   
  ELSE   
  DO:   
    /*FIND FIRST art-list WHERE art-list.artart = 0 
        AND art-list.i-group = 0
        AND NOT art-list.printed  USE-INDEX DATE_ix NO-ERROR.*/   
      FIND FIRST art-list WHERE art-list.artart = 0 AND NOT art-list.disc-flag 
          AND art-list.i-group = 0
          AND NOT art-list.printed  USE-INDEX DATE_ix NO-ERROR.   
    n = 0.   
    curr-j = printed-line.   
    DO i = 1 TO npage:   
      IF NOT AVAILABLE art-list THEN i = npage.   
      RUN print-overhead1.   
      DO WHILE AVAILABLE art-list AND (curr-j LE lpage): 
        
        /*DO i = 1 TO NUM-ENTRIES(art-str, ";"):
            IF art-list.artnr EQ INTEGER(ENTRY(i, art-str, ";")) THEN .
            ELSE RUN print-billine.
        END.*/
    
        RUN print-billine.
        /*FIND NEXT art-list WHERE art-list.artart = 0 
            AND art-list.i-group = 0
            AND NOT art-list.printed NO-ERROR.*/   
        FIND NEXT art-list WHERE art-list.artart = 0 AND NOT art-list.disc-flag 
            AND art-list.i-group = 0
            AND NOT art-list.printed NO-ERROR.   
        IF NOT AVAILABLE art-list THEN i = npage.   
      END.   
      IF i = npage THEN  /* all bill-lines are printed  */   
      DO:   
        IF new-fbart THEN RUN print-overhead2(2).   
        IF overhead3 GT 0 THEN RUN print-overhead3.   
        IF overhead4 GT 0 OR buttom-lines GE 1 THEN RUN print-overhead4.  
        RUN cut-it.  
/*    page STREAM s1. */   
      END.   
      ELSE IF curr-j GT lpage THEN DO:   
        CREATE output-list.  
        ASSIGN  
            output-list.flag-popup = YES  
            output-list.npause = npause
            output-list.sort-i = sort-i
            sort-i = sort-i + 1.
        curr-j = 0.   
        printed-line = 0.   
      END.   
    END.   
  END.   
   
  /*MTOUTPUT STREAM s1 CLOSE.*/  
   
  tot-amount = 0.  
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr  
      AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK:  
    tot-amount = tot-amount + vhp.h-bill-line.betrag.  
    /*tot-amount = ROUND(tot-amount,0).*/
  END.  
  
  IF /*new-fbart AND */ printnr GE 0 THEN   
  DO:   
    IF NOT use-h-queasy THEN   
    DO:   
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 4   
        AND vhp.queasy.number1 = (vhp.h-bill.departement   
                               + vhp.h-bill.rechnr * 100)   
        AND vhp.queasy.number2 = 0   
        AND vhp.queasy.deci2   = billnr USE-INDEX rbill_ix EXCLUSIVE-LOCK.   
      ASSIGN  
        vhp.queasy.number3 = printed-line   
        vhp.queasy.deci1   = tot-amount  
      .   
      FIND CURRENT vhp.queasy NO-LOCK.   
    END.   
    ELSE   
    DO:   
      FIND FIRST vhp.h-queasy WHERE   
        vhp.h-queasy.number1     = (vhp.h-bill.departement   
                                 + vhp.h-bill.rechnr * 100)   
        AND vhp.h-queasy.number2 = 0   
        AND vhp.h-queasy.billno  = billnr EXCLUSIVE-LOCK NO-ERROR.  
      IF AVAILABLE vhp.h-queasy THEN  
      DO:  
        ASSIGN  
          vhp.h-queasy.number3 = printed-line  
          vhp.h-queasy.deci1   = tot-amount  
        .   
        FIND CURRENT vhp.h-queasy NO-LOCK.   
      END.  
    END.  
  END.   
END.   
  
/*********************** PROCEDURE ***********************/  
PROCEDURE optional-params:  
    DEFINE VARIABLE  lvCTmp AS CHARACTER            NO-UNDO.   
    DEFINE VARIABLE lvCLeft AS CHARACTER            NO-UNDO.   
    DEFINE VARIABLE lvCVal AS CHARACTER             NO-UNDO.   
    DEFINE VARIABLE lvICnt AS INTEGER               NO-UNDO.   
    DEFINE VARIABLE lvI AS INTEGER                  NO-UNDO.   
    DEFINE VARIABLE lvITmp AS INTEGER               NO-UNDO.   
   
    lvICnt = NUM-ENTRIES(session-parameter, ";").   
    DO lvI = 1 TO lvICnt:   
        ASSIGN   
            lvCTmp  = ""   
            lvCLeft = ""   
        .    
        lvCtmp = TRIM(ENTRY(lvI, session-parameter, ";")).   
        lvCLeft = TRIM(ENTRY(1, lvCTmp, "=")) NO-ERROR.   
   
        CASE lvCLeft:   
            WHEN "WINPRINTER" THEN winprinterFlag = YES.  
            WHEN "TableDesc" THEN DO:   
                lvCVal = ENTRY(2, lvCTmp, "=") NO-ERROR.   
                IF lvCVal = "YES" THEN prTableDesc = TRUE.   
            END.   
            WHEN "Pr2Line" THEN DO:   
                lvCVal = ENTRY(2, lvCTmp, "=") NO-ERROR.   
                IF lvCVal = "YES" THEN prTwoLine = TRUE.   
            END.   
            WHEN "print-all" THEN DO:   
                lvITmp = INTEGER(ENTRY(2, lvCTmp, "=")) NO-ERROR.   
                IF lvITmp = 1 THEN print-all = TRUE.   
            END.   
            WHEN "top-margin" THEN DO:  
                lvITmp = -1.  
                lvITmp = INTEGER(ENTRY(2, lvCTmp, "=")) NO-ERROR.   
                IF lvITmp GE 1 THEN hmargin = lvITmp.   
            END.   
            WHEN "num-lines" THEN DO:  
                lvITmp = -1.  
                lvITmp = INTEGER(ENTRY(2, lvCTmp, "=")) NO-ERROR.   
                IF lvITmp GE 1 THEN lpage = lvITmp.   
            END.   
            WHEN "DesLen" THEN DO:  
                lvITmp = INTEGER(ENTRY(2, lvCTmp, "=")) NO-ERROR.   
                IF lvITmp GE 1 THEN nbezeich = lvITmp.   
            END.   
            WHEN "buttom-lines" THEN DO:  
                lvITmp = INTEGER(ENTRY(2, lvCTmp, "=")) NO-ERROR.   
                IF lvITmp GE 1 THEN buttom-lines = lvITmp.   
            END.   
            WHEN "header1" THEN  
                ASSIGN header1 = ENTRY(2, lvCTmp, "=").  
            WHEN "header2" THEN  
                ASSIGN header2 = ENTRY(2, lvCTmp, "=").  
            WHEN "foot1" THEN  
            ASSIGN  
                foot1 = ENTRY(2, lvCTmp, "=")  
                foot2 = ""  
                anz-foot = 1  
            .  
            WHEN "foot2" THEN  
            ASSIGN  
                foot2 = ENTRY(2, lvCTmp, "=")  
                anz-foot = 2  
            .  
        END CASE.   
    END.   
END PROCEDURE.   
  
PROCEDURE cal-servat:  
DEF INPUT PARAMETER depart          AS INT.  
DEF INPUT PARAMETER h-artnr         AS INT.  
DEF INPUT PARAMETER service-code    AS INT.  
DEF INPUT PARAMETER mwst-code       AS INT.
DEF INPUT PARAMETER inpDate         AS DATE.
DEF OUTPUT PARAMETER serv%          AS DECIMAL INITIAL 0.  
DEF OUTPUT PARAMETER mwst%          AS DECIMAL INITIAL 0.  
DEF OUTPUT PARAMETER vat2%           AS DECIMAL INITIAL 0. 
DEF OUTPUT PARAMETER servat         AS DECIMAL INITIAL 0. 
  
DEF VAR serv-htp AS DECIMAL            NO-UNDO.  
DEF VAR vat-htp  AS DECIMAL            NO-UNDO.  
/*DEF VAR vat2     AS DECIMAL INITIAL 0.*/  
  
DEF BUFFER hbuff FOR vhp.h-artikel.  
DEF BUFFER aBuff FOR vhp.artikel.  
  
    FIND FIRST hbuff WHERE hbuff.artnr = h-artnr  
        AND hbuff.departement = depart NO-LOCK.    
    FIND FIRST abuff WHERE abuff.artnr = hbuff.artnrfront  
        AND abuff.departement = depart NO-LOCK.  

    /* SY AUG 13 2017 */
    RUN calc-servtaxesbl.p(1, abuff.artnr, abuff.departement, 
        inpDate, OUTPUT serv%, OUTPUT mwst%, OUTPUT vat2%, OUTPUT servat).
    ASSIGN mwst% = mwst%
           vat2% = vat2%
           serv% = serv%.
END.
    
PROCEDURE add-unitprice-text:   
DEFINE VARIABLE n AS INTEGER.   
DEFINE VARIABLE s AS CHAR.   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 412 NO-LOCK.   
  IF NOT vhp.htparam.flogical THEN RETURN.   
  IF vhp.htparam.paramgr NE 19 THEN RETURN.   
  IF prTwoLine THEN RETURN.  
  
  FOR EACH art-list WHERE (art-list.qty NE 1) AND (art-list.qty NE -1)   
    AND art-list.qty NE 0 AND art-list.artnr NE 0:   
    s = " @" + STRING(art-list.price).   
    IF LENGTH(art-list.bezeich + s) LE nbezeich THEN   
      art-list.bezeich = art-list.bezeich + s.   
    ELSE   
    art-list.bezeich = SUBSTR(art-list.bezeich, 1, nbezeich - LENGTH(s)) + s.   
  END.   
END.   
  
PROCEDURE check-pages:   
DEFINE VARIABLE total-line     AS INTEGER NO-UNDO.   
DEFINE VARIABLE new-sold-item  AS LOGICAL NO-UNDO.  
  
  IF prdisc-flag THEN   
  DO:   
    FOR EACH art-list WHERE art-list.artart = 0:   
      IF art-list.disc-flag THEN tot-disc-line = tot-disc-line + 1.   
      ELSE tot-ndisc-line = tot-ndisc-line + 1.   
    END.   
  END.   
   
  FIND FIRST art-list WHERE art-list.artart = 0 NO-ERROR.  
  new-sold-item = AVAILABLE art-list.  
  
  overhead1 = hmargin + bmargin + 3.  /* 3 header-lines */   
  overhead2 = 6. /* space-line, subtotal, service, tax, -----, total  */   
   
  overhead3 = 0.   
  FOR EACH art-list WHERE art-list.artart NE 0:   
    IF new-sold-item OR (NOT art-list.printed) THEN overhead3 = overhead3 + 1.   
  END.   
  IF overhead3 NE 0 THEN overhead3 = overhead3 + 2.  /* ---- AND balance */   
   
  IF vhp.h-bill.saldo = 0 OR print-all THEN  
  DO:  
    FIND FIRST vhp.paramtext WHERE txtnr = 712 NO-LOCK.   
    IF foot2 = "" AND ptexte NE "" THEN   
    DO:   
      foot2 = ptexte.   
      anz-foot = 2.   
    END.   
    FIND FIRST vhp.paramtext WHERE txtnr = 711 NO-LOCK.   
    IF foot1 = "" AND ptexte NE "" THEN   
    DO:   
      foot1 = ptexte.   
      IF anz-foot = 0 THEN anz-foot = 1.   
    END.  
  END.  
  IF anz-foot = 0 THEN overhead4 = 0.   
  ELSE overhead4 = anz-foot + 2. /* 2 space lines */   
   
  npage = 1.   
  total-line = overhead1 + tot-line + overhead2 + overhead3 + overhead4.   
  IF tot-ndisc-line GE 1 AND tot-ndisc-line GE 1 THEN   
    total-line = total-line + 3.   
   
  DO WHILE total-line GT lpage:   
    npage = npage + 1.   
    total-line = total-line - (lpage - overhead1).   
  END.   
  npage = 9999.   
END.   
  
PROCEDURE print-overhead1:   
DEFINE VARIABLE i AS INTEGER.   
DEFINE VARIABLE rechnr-str AS CHAR FORMAT "x(8)".   
DEFINE VARIABLE kname AS CHAR.  
  /*MT22CREATE output-list.*/  
  
  FIND FIRST vhp.bediener WHERE vhp.bediener.userinit = user-init  
      NO-LOCK NO-ERROR.  
  IF AVAILABLE vhp.bediener THEN kname = vhp.bediener.username + order-id.    
  ELSE IF AVAILABLE vhp.kellner THEN kname = vhp.kellner.kellnername + order-id.   
  IF printed-line = 0 OR print-all THEN   
  DO:   
    DO i = 1 TO hmargin:  
      output-list.str = output-list.str + STRING(" ").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 " " SKIP.*/  
      curr-j = curr-j + 1.   
      printed-line = printed-line + 1.   
    END.   
      
    IF header1 NE "" THEN  
    DO:  
      DO i = 1 TO LENGTH(header1):  
        output-list.str = output-list.str + STRING(SUBSTR(header1,i,1), "x(1)").  
        /*MTPUT STREAM s1 SUBSTR(header1,i,1) FORMAT "x(1)".*/  
      END.  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 "" SKIP.*/  
      printed-line = printed-line + 1.  
    END.  
  
    IF header2 NE "" THEN  
    DO:  
      DO i = 1 TO LENGTH(header2):  
        /*MTPUT STREAM s1 SUBSTR(header2,i,1) FORMAT "x(1)".*/  
        output-list.str = output-list.str + STRING(SUBSTR(header2,i,1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 "" SKIP.*/  
      printed-line = printed-line + 1.  
    END.  
  
    IF header1 NE "" OR header2 NE "" THEN  
    DO:  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 "" SKIP.*/  
      printed-line = printed-line + 1.  
    END.  
  
    rechnr-str = STRING(vhp.h-bill.rechnr).   
    IF vhp.h-bill.mwst[90] NE 0 THEN rechnr-str = STRING(vhp.h-bill.mwst[90]).   
    IF print-all THEN rechnr-str = rechnr-str + "**".
    IF vhp.h-bill.bilname NE "" THEN   
    DO:  
      IF gst-logic THEN
        output-list.str = output-list.str   
                + STRING("     " + STRING(bill-date) + " "   
                         + STRING(time, "HH:MM") + " "   
                         + translateExtended ("Tax Invoice No",lvCAREA,"") + " "   
                         + STRING(rechnr-str, "x(43)")). 
      ELSE 
         output-list.str = output-list.str   
                + STRING("     " + STRING(bill-date) + " "   
                         + STRING(time, "HH:MM") + " "   
                         + translateExtended ("Bill No",lvCAREA,"") + " "   
                         + STRING(rechnr-str, "x(33)")).  

      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str  
                + STRING("     " + vhp.hoteldpt.depart, "x(32)").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str  
                + STRING("     " + translateExtended ("Table",lvCAREA,"") + " "   
                         + STRING(vhp.h-bill.tischnr, ">>>9") + "/"   
                         + STRING(vhp.h-bill.belegung,"->>>9 ") + kname, "x(32)"  
                        ).  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1   
        STRING("     " + STRING(bill-date) + " "   
        + STRING(time, "HH:MM")   
        + " " + translateExtended ("BillNo",lvCAREA,"") + " "   
        + rechnr-str) FORMAT "x(33)" SKIP   
  
        STRING("     " + vhp.hoteldpt.depart) FORMAT "x(32)" SKIP   
          
        STRING("     " + translateExtended ("Table",lvCAREA,"") + " "   
        + STRING(vhp.h-bill.tischnr, ">>>9")   
        + "/" + STRING(vhp.h-bill.belegung,"->>>9 ")   
        + kname) FORMAT "x(32)" SKIP.  
      */  
  
      IF prTableDesc THEN   
      DO:  
        FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = vhp.h-bill.tischnr   
            AND vhp.tisch.departement = vhp.h-bill.departement   
            NO-LOCK NO-ERROR.  
        IF AVAILABLE vhp.tisch AND vhp.tisch.bezeich NE "" THEN  
        DO:  
          output-list.str = output-list.str + STRING("     " + vhp.tisch.bezeich, "x(32)").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 STRING("     " + vhp.tisch.bezeich) FORMAT "x(32)" SKIP.*/  
          curr-j = curr-j + 1.  
        END.  
      END.  
  
      output-list.str = output-list.str   
            + STRING("     " + translateExtended ("Guest",lvCAREA,"") + " "   
                     + vhp.h-bill.bilname, "x(32)").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.

      IF gst-logic THEN /*FT 020415*/
      DO:
          CREATE output-list.
          ASSIGN
            output-list.sort-i = sort-i
            sort-i = sort-i + 1
            output-list.str = output-list.str  
                              + STRING("            " + translateExtended ("Tax Invoice",lvCAREA,"")).
          CREATE output-list.
          ASSIGN
            output-list.sort-i = sort-i
            sort-i = sort-i + 1
            output-list.str = output-list.str  
                              + STRING("       " + translateExtended ("GST ID : 001865060352",lvCAREA,"")).
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.    
      END.

      /*MTPUT STREAM s1   
        STRING("     " + translateExtended ("Guest",lvCAREA,"") + " "   
        + vhp.h-bill.bilname) FORMAT "x(32)" SKIP.*/  
  
      curr-j = curr-j + 4.   
      printed-line = printed-line + 4.   
  
      IF vhp.h-bill.resnr GT 0 AND vhp.h-bill.reslinnr GT 0 THEN  
      DO:  
        FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill.resnr  
            AND vhp.res-line.reslinnr = vhp.h-bill.reslinnr  
            NO-LOCK NO-ERROR.  
        IF AVAILABLE vhp.res-line THEN  
        FIND FIRST vhp.mc-guest WHERE vhp.mc-guest.gastnr = vhp.res-line.gastnrmember   
          AND vhp.mc-guest.activeflag NO-LOCK NO-ERROR.  
      END.  
      ELSE IF vhp.h-bill.resnr GT 0 AND vhp.h-bill.reslinnr = 0 THEN  
      DO:  
        FIND FIRST vhp.mc-guest WHERE vhp.mc-guest.gastnr = vhp.h-bill.resnr  
          AND vhp.mc-guest.activeflag NO-LOCK NO-ERROR.  
      END.  
      IF AVAILABLE vhp.mc-guest THEN   
      DO:  
         output-list.str = output-list.str   
                + STRING("     " + translateExtended ("MemberCard",lvCAREA,"")   
                         + " " + vhp.mc-guest.cardnum, "x(32)").  
         CREATE output-list.
         output-list.sort-i = sort-i.
         sort-i = sort-i + 1.
         /*MTPUT STREAM s1  
         STRING("     " + translateExtended ("MemberCard",lvCAREA,"") + " "   
           + vhp.mc-guest.cardnum) FORMAT "x(32)" SKIP.*/  
         curr-j = curr-j + 1.   
         printed-line = printed-line + 1.   
      END.  
    END.  
    ELSE   
    DO:  
      IF gst-logic THEN
        output-list.str = output-list.str   
                + STRING("     " + STRING(bill-date) + " "   
                         + STRING(time, "HH:MM") + " "   
                         + translateExtended ("Tax Invoice No",lvCAREA,"") + " "   
                         + STRING(rechnr-str, "x(43)")). 
      ELSE
        output-list.str = output-list.str  
            + STRING("     " + STRING(bill-date) + " " + STRING(TIME, "HH:MM")   
                + " " + translateExtended ("Bill No",lvCAREA,"") + " "   
                + STRING(rechnr-str, "x(33)")).  
      
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str  
            + STRING("     " + vhp.hoteldpt.depart, "x(32)").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str  
            + STRING("     " + translateExtended ("Table",lvCAREA,"") + " "   
                     + STRING(vhp.h-bill.tischnr, ">>>9") + "/"   
                     + STRING(vhp.h-bill.belegung,"->>>9 ")   
                     + kname, "x(32)").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.

      IF gst-logic THEN   /*FT 020415*/
      DO:
          CREATE output-list.
          ASSIGN
            output-list.sort-i = sort-i
            sort-i = sort-i + 1
            output-list.str = output-list.str  
                              + STRING("            " + translateExtended ("Tax Invoice",lvCAREA,"")).
          CREATE output-list.
          ASSIGN
            output-list.sort-i = sort-i
            sort-i = sort-i + 1
            output-list.str = output-list.str  
                              + STRING("       " + translateExtended ("GST ID : 001865060352",lvCAREA,"")).
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
      END.
  
      /*MTPUT STREAM s1   
        STRING("     " + STRING(bill-date) + " "   
        + STRING(TIME, "HH:MM")   
        + " " + translateExtended ("BillNo",lvCAREA,"") + " "   
        + rechnr-str) FORMAT "x(33)" SKIP   
          
        STRING("     " + vhp.hoteldpt.depart) FORMAT "x(32)" SKIP   
  
        STRING("     " + translateExtended ("Table",lvCAREA,"")   
        + " " + STRING(vhp.h-bill.tischnr, ">>>9")   
        + "/" + STRING(vhp.h-bill.belegung,"->>>9 ")   
        + kname) FORMAT "x(32)" SKIP.*/  
        
      IF prTableDesc THEN   
      DO:  
        FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = vhp.h-bill.tischnr   
            AND vhp.tisch.departement = vhp.h-bill.departement   
            NO-LOCK NO-ERROR.  
        IF AVAILABLE vhp.tisch AND vhp.tisch.bezeich NE "" THEN  
        DO:  
          output-list.str = output-list.str  
                + STRING("     " + vhp.tisch.bezeich, "x(32)").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 STRING("     " + vhp.tisch.bezeich) FORMAT "x(32)" SKIP.*/  
          curr-j = curr-j + 1.  
        END.  
      END.  
  
      curr-j = curr-j + 3.   
      printed-line = printed-line + 3.   
    END.   
      
    DO i = 1 TO bmargin:   
      curr-j = curr-j + 1.   
      printed-line = printed-line + 1.   
      output-list.str = output-list.str + STRING(" ").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 " " SKIP.*/  
    END.   
  END.   
END.   
  
PROCEDURE print-billine:   
DEFINE VAR i            AS INTEGER.   
DEFINE VAR anz          AS INTEGER INITIAL 0.  
DEFINE VAR leerCH       AS CHAR INITIAL "".  
DEFINE VAR ct           AS CHAR.  
DEFINE VAR bezeich      AS CHAR.  
DEFINE VAR is-str451    AS LOGICAL.
DEFINE VAR is-str452    AS LOGICAL.
DEFINE BUFFER h-art FOR vhp.h-artikel.  

    RUN read-htparambl.p(5, ?,?, OUTPUT TABLE t-htp).
    FIND FIRST t-htp WHERE t-htp.paramnr EQ 10.
    ASSIGN serv% = t-htp.fdeci.
    
 /*IF art-list.artnr EQ vat-art OR art-list.artnr EQ serv-art OR art-list.artnr EQ oth-art OR art-list.artnr EQ sc-art OR art-list.artnr EQ sc-art1 
     OR art-list.artnr EQ sc-art2 OR art-list.artnr EQ f-discArt OR art-list.artnr EQ f-discArt1 OR art-list.artnr EQ f-discArt2 THEN.
 ELSE DO:*/
      bezeich = art-list.happyhr + art-list.bezeich.     
      IF qty1000 THEN  
        output-list.str = output-list.str + STRING(" ") + STRING(art-list.qty, "->>>> ") + STRING (" ").
      ELSE DO: 
          IF art-list.qty GT 99 OR art-list.qty LT -99 THEN
            output-list.str = output-list.str + STRING(" ") + STRING(art-list.qty) + STRING (" "). 
          ELSE IF art-list.qty GT 9 OR art-list.qty LT -9 THEN
              output-list.str = output-list.str + STRING("  ") + STRING(art-list.qty) + STRING (" "). 
          ELSE output-list.str = output-list.str + STRING("   ") + STRING(art-list.qty) + STRING (" ").
      END.
      
      DO i = 1 TO nbezeich:
        IF i GT LENGTH(bezeich) THEN /*MTPUT STREAM s1 " "*/  
            output-list.str = output-list.str + STRING(" ").  
        ELSE /*MTPUT STREAM s1 SUBSTR(bezeich, i, 1) FORMAT "x(1)".*/  
            output-list.str = output-list.str + STRING(SUBSTR(bezeich, i, 1), "x(1)").  
      END.   
      
      IF prTwoLine THEN   
      DO:  
          output-list.str = output-list.str + STRING("").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 "" SKIP.*/  
          ASSIGN  
            curr-j        = curr-j + 1  
            printed-line  = printed-line + 1  
          .  
      END.  
      ELSE   
      DO:  
            IF art-list.artnr EQ serv-art THEN
            DO:
                serv-scd-val = ((serv% / 100) * subtotal).
    
                IF price-decimal = 0 THEN   
                DO:   
                   IF NOT long-digit THEN   
                   DO:  
                       output-list.str = output-list.str + STRING(serv-scd-val, "->>>,>>>,>>9").  
                       /*MTCREATE output-list.*/  
                       /*MTPUT STREAM s1 art-list.amount FORMAT "->>>,>>>,>>9" SKIP.*/  
                   END.  
                   ELSE  
                   DO:  
                       output-list.str = output-list.str + STRING(serv-scd-val, "->>>,>>>,>>9").  
                       /*MTCREATE output-list.*/  
                       /*MTPUT STREAM s1 art-list.amount FORMAT "->,>>>,>>>,>>9" SKIP.*/  
                   END.  
                END.   
                ELSE  
                DO:  
                    output-list.str = output-list.str + STRING(serv-scd-val, "->>>,>>>,>>9.99").  
                    /*MTCREATE output-list.*/  
                    /*MTPUT STREAM s1 art-list.amount FORMAT "->>>,>>9.99" SKIP.*/  
                END.  
            END.  
            ELSE
            DO:
                IF price-decimal = 0 THEN   
                DO:   
                   IF NOT long-digit THEN   
                   DO:  
                       output-list.str = output-list.str + STRING(art-list.amount, "->>>,>>>,>>9").  
                       /*MTCREATE output-list.*/  
                       /*MTPUT STREAM s1 art-list.amount FORMAT "->>>,>>>,>>9" SKIP.*/  
                   END.  
                   ELSE  
                   DO:  
                       output-list.str = output-list.str + STRING(art-list.amount, "->>>,>>>,>>9").  
                       /*MTCREATE output-list.*/  
                       /*MTPUT STREAM s1 art-list.amount FORMAT "->,>>>,>>>,>>9" SKIP.*/  
                   END.  
                END.   
                ELSE  
                DO:  
                    output-list.str = output-list.str + STRING(art-list.amount, "->>>,>>>,>>9.99").  
                    /*MTCREATE output-list.*/  
                    /*MTPUT STREAM s1 art-list.amount FORMAT "->>>,>>9.99" SKIP.*/  
                END.
            END.
        ASSIGN  
          curr-j        = curr-j + 1  
          printed-line = printed-line + 1 .  
      END.
      ASSIGN subtotal = subtotal + art-list.amount.
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
        
      IF prTwoLine THEN  
      DO:  
        IF qty1000 THEN /*MTPUT STREAM s1 "      "*/  
            output-list.str = output-list.str + STRING("      ").  
        ELSE /*MTPUT STREAM s1 "     "*/  
            output-list.str = output-list.str + STRING("     ").  
          
        anz = nbezeich - 22.  
        IF anz GT 0 THEN leerCH = FILL(" ", anz).  
        IF price-decimal = 0 THEN  
        ct = "@" + STRING(art-list.price, "->,>>>,>>9") + leerCH  
           + STRING(art-list.amount, "->>>,>>>,>>9") + CHR(10).  
        ELSE  
        ct = "@" + STRING(art-list.price, "->>,>>9.99") + leerCH  
           + STRING(art-list.amount, "->>>,>>9.99") + CHR(10).  
      
        DO i = 1 TO LENGTH(ct):  
            output-list.str = output-list.str + STRING(SUBSTR(ct, i, 1), "x(1)").  
            /*MTPUT STREAM s1 SUBSTR(ct, i, 1) FORMAT "x(1)".*/  
        END.  
        ASSIGN  
          curr-j       = curr-j + 1  
          printed-line = printed-line + 1  
        .  
      END.  
      
      IF art-list.condiment = 0 OR art-list.disc-flag THEN RETURN.  
      FOR EACH vhp.h-mjourn WHERE vhp.h-mjourn.departement = art-list.dept   
        AND vhp.h-mjourn.h-artnr = art-list.artnr   
        AND vhp.h-mjourn.rechnr = vhp.h-bill.rechnr   
        AND vhp.h-mjourn.bill-datum = art-list.datum   
        AND vhp.h-mjourn.sysdate = art-list.sysdate   
        AND vhp.h-mjourn.zeit = art-list.zeit NO-LOCK:   
        FIND FIRST h-art WHERE h-art.artnr = vhp.h-mjourn.artnr   
          AND h-art.departement = dept NO-LOCK NO-ERROR.   
        IF AVAILABLE h-art THEN   
        DO:  
          bezeich = h-art.bezeich.  
          output-list.str = output-list.str + STRING(art-list.qty) + STRING(" ").  
          /*MTPUT STREAM s1 art-list.qty " ".*/  
          DO i = 1 TO nbezeich:   
            IF i GT LENGTH(bezeich) THEN /*MTPUT STREAM s1 " "*/  
                output-list.str = output-list.str + STRING(" ").  
            ELSE /*MTPUT STREAM s1 SUBSTR(bezeich, i, 1) FORMAT "x(1)"*/  
                output-list.str = output-list.str + STRING(SUBSTR(bezeich, i, 1), "x(1)").  
          END.  
          output-list.str = output-list.str + STRING(translateExtended("(Condiment)",lvCAREA,""), "x(11)").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 translateExtended("(Condiment)",lvCAREA,"")  
             FORMAT "x(11)" SKIP.     */  
        END.  
        curr-j = curr-j + 1.   
        printed-line = printed-line + 1.  
      END.
 /*END.*/  
END.   
  
PROCEDURE print-overhead2:   
DEFINE INPUT PARAMETER prall-flag AS INTEGER.   
DEFINE VARIABLE i       AS INTEGER.   
DEFINE VARIABLE pos     AS INTEGER.   
DEFINE VARIABLE nbez1   AS INTEGER.   
DEFINE VARIABLE s       AS CHAR.   
DEFINE VARIABLE tot-str AS CHAR.   

   IF curr-j GT (lpage - 6) THEN DO:   
    CREATE output-list.
    ASSIGN  
        output-list.flag-popup = YES  
        output-list.npause = npause
        output-list.sort-i = sort-i
        sort-i = sort-i + 1.
    curr-j = 0.   
    printed-line = 0.   
    RUN print-overhead1. /* print billheader IF curr-j = 0 OR print-all */   
  END.   
    
  pos = 5.  
  IF qty1000 THEN pos = 6.  
    
  nbez1 = nbezeich.  
  IF prTwoLine THEN nbez1 = nbez1 - 11.  

  IF prall-flag LE 1 THEN   
  DO:   
    IF qty1000 THEN 
        output-list.str = output-list.str + STRING("", "x(6)").  
    ELSE 
        output-list.str = output-list.str + STRING("", "x(5)").  
    DO i = 1 TO (nbezeich + n11):  
      output-list.str = output-list.str + STRING("-", "x(1)").  
    END.  
    output-list.str = output-list.str + STRING("").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1 "" SKIP.*/  
    printed-line = printed-line + 1.   
  END.   
  
  /**/
  FOR EACH art-list:
      IF art-list.artnr EQ f-discArt OR art-list.artnr EQ f-discArt1 OR art-list.artnr EQ f-discArt2 THEN
      DO:
          DO i = 1 TO pos:  
              output-list.str = output-list.str + STRING(" ").  
          END.   

          FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr AND h-bill-line.artnr EQ f-discArt.

          DO i = 1 TO nbez1:   
            IF i GT LENGTH(h-bill-line.bezeich) THEN  
                output-list.str = output-list.str + STRING(" ").  
            ELSE output-list.str = output-list.str + STRING(SUBSTR(h-bill-line.bezeich, i, 1), "x(1)").  
          END.   

          ASSIGN disc = art-list.price.
          IF price-decimal = 0 THEN   
          DO:   
             IF NOT long-digit THEN   
             DO:  
                 output-list.str = output-list.str + STRING(art-list.price, "->>>,>>>,>>9").  
                 CREATE output-list.
                 output-list.sort-i = sort-i.
                 sort-i = sort-i + 1.
             END.  
             ELSE  
             DO:  
                 output-list.str = output-list.str + STRING(art-list.price, "->,>>>,>>>,>>9").  
                 CREATE output-list.
                 output-list.sort-i = sort-i.
                 sort-i = sort-i + 1.
             END.  
          END.   
          ELSE  
          DO:  
              output-list.str = output-list.str + STRING(art-list.price, "->>>,>>>,>>9.99").  
              CREATE output-list.
              output-list.sort-i = sort-i.
              sort-i = sort-i + 1.
          END.  
          printed-line = printed-line + 1.   
      END.
  END.
  /**/

  IF disc NE 0 THEN ASSIGN subtotal = subtotal + disc.
  /*IF scd-val NE 0 THEN ASSIGN subtotal = subtotal + scd-val.*/
  IF sc-art NE 0 THEN
  DO:
      FIND FIRST h-bill WHERE RECID(h-bill) = hbrecid NO-LOCK.  
      FIND FIRST h-bill-line WHERE 
          h-bill-line.rechnr = h-bill.rechnr
          AND h-bill-line.departement = h-bill.departement
          AND h-bill-line.artnr = sc-art
          NO-LOCK NO-ERROR.
      IF AVAILABLE h-bill-line THEN
      DO:
          scd-val = subtotal * (scd% / 100) * -1.
      END.
  END.

  /*IF is-scd THEN
      ASSIGN service = subtotal * (serv% / 100)/*service = ((subtotal - (scd% / 100 * subtotal)) * (serv% / 100))*/
             mwst    = 0.
  ELSE ASSIGN service = subtotal * (serv% / 100).*/

  /* */
    DO i = 1 TO pos:  
        output-list.str = output-list.str + STRING(" ").  
    END.   

  DO i = 1 TO (nbezeich + n11 + 4):   
    IF i LT (nbezeich + n11 + 4) THEN /*MTPUT STREAM s1 "-" FORMAT "x(1)"*/  
        output-list.str = output-list.str + STRING("-", "x(1)").  
    ELSE  
    DO:
        output-list.str = output-list.str + STRING("-", "x(1)").  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
        /*MTPUT STREAM s1 "-" FORMAT "x(1)" SKIP.*/  
    END.  
  END.   
  /* */

  /* Sales subtotal */
  IF service NE 0 OR mwst NE 0 THEN   
  DO:   
    IF comp-taxserv AND comp-flag THEN   
    DO:   
        s = translateExtended ("Total",lvCAREA,"") + "   ".   
          
        IF qty1000 THEN 
            output-list.str = output-list.str + STRING("", "x(6)").  
        ELSE output-list.str = output-list.str + STRING("", "x(5)").  
        DO i = 1 TO (nbezeich + n11):   
          IF i LT (nbezeich + n11) THEN 
              output-list.str = output-list.str + STRING("-", "x(1)").  
          ELSE  
          DO:  
              output-list.str = output-list.str + STRING("-", "x(1)").  
              CREATE output-list.
              output-list.sort-i = sort-i.
              sort-i = sort-i + 1.
          END.  
        END.   
        printed-line = printed-line + 1.   
    END.   
    ELSE s = translateExtended ("Subtotal",lvCAREA,"").   
   
    DO i = 1 TO pos:  
        output-list.str = output-list.str + STRING(" ").  
    END.   
   
    DO i = 1 TO nbez1:   
      IF i GT LENGTH(s) THEN  
          output-list.str = output-list.str + STRING(" ").  
      ELSE output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
    END.   
      
    IF price-decimal = 0 THEN   
    DO:   
       IF NOT long-digit THEN   
       DO:  
           output-list.str = output-list.str + STRING(subtotal, "->>>,>>>,>>9").  
           CREATE output-list.
           output-list.sort-i = sort-i.
           sort-i = sort-i + 1.
       END.  
       ELSE  
       DO:  
           output-list.str = output-list.str + STRING(subtotal, "->,>>>,>>>,>>9").  
           CREATE output-list.
           output-list.sort-i = sort-i.
           sort-i = sort-i + 1.
       END.  
    END.   
    ELSE  
    DO:  
        output-list.str = output-list.str + STRING(subtotal, "->>>,>>>,>>9.99").  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
    END.  
    printed-line = printed-line + 1.   
    /* Sales subtotal */
      
    /* Change line */
    CREATE output-list.
    ASSIGN
        output-list.sort-i = sort-i
        sort-i             = sort-i + 1
        printed-line       = printed-line + 1
    . 

    DO i = 1 TO pos:  
        output-list.str = output-list.str + STRING(" ").  
        /*MTPUT STREAM s1 " ".*/  
    END.   
    /* Change line */

    IF sc-art NE 0 THEN
    DO:
        FIND FIRST h-bill WHERE RECID(h-bill) = hbrecid NO-LOCK.  
        FIND FIRST h-bill-line WHERE 
            h-bill-line.rechnr = h-bill.rechnr
            AND h-bill-line.departement = h-bill.departement
            AND h-bill-line.artnr = sc-art
            NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill-line THEN
        DO:
            FIND FIRST art-list WHERE art-list.i-group EQ 2 NO-ERROR.
            mwst = art-list.amount.
        END.
    END.

    /* VAT exempt */
    ASSIGN
        s = translateExtended ("VAT exempt sale",lvCAREA,"")
        output-list.str = FILL(" ", pos)
        output-list.str = output-list.str
                        + SUBSTR(s, 1, nbez1)
                        + FILL(" ", nbez1 - LENGTH(s))
    .

    IF price-decimal = 0 THEN  
        output-list.str = output-list.str + "        " + STRING(mwst, "->>9").
    ELSE
        output-list.str = output-list.str + "        " + STRING(mwst, "->>9.99").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /* VAT exempt */

  /* Service charge & Taxes */
  FOR EACH FB-vatlist WHERE FB-vatlist.i-type GE 3
    BY FB-vatlist.i-type:
    IF FB-vatlist.vatAmt NE 0 THEN
    DO:
      ASSIGN
          s = FB-vatlist.bezeich   
          output-list.str = FILL(" ", pos)
          output-list.str = output-list.str
                          + SUBSTR(s, 1, nbez1)
                          + FILL(" ", nbez1 - LENGTH(s))
          tot-amount = tot-amount + FB-vatlist.vatAmt
      .
      IF price-decimal = 0 THEN   
      DO:   
        IF NOT long-digit THEN   
        DO:  
          output-list.str = output-list.str + STRING(FB-vatlist.vatAmt, "->>>,>>>,>>9").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
        END.  
        ELSE  
        DO:  
          output-list.str = output-list.str + STRING(FB-vatlist.vatAmt, "->,>>>,>>>,>>9").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
        END.  
      END.   
      ELSE  
      DO:  
        output-list.str = output-list.str + STRING(FB-vatlist.vatAmt, "->>>,>>>,>>9.99").  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
      END.  
      printed-line = printed-line + 1. 
    END.
  END.
  /* Service charge & Taxes */ 
  
  /* Change line */
  CREATE output-list.
  ASSIGN
      output-list.sort-i = sort-i
      sort-i             = sort-i + 1
      printed-line       = printed-line + 1
  . 

  DO i = 1 TO pos:  
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 " ".*/  
  END.   
  /* Change line */
   
    /* Senior Citizen Discount */
    FIND FIRST art-list WHERE art-list.i-group = 1 NO-ERROR.
    IF AVAILABLE art-list THEN
    DO:
        ASSIGN
            /*scd-val         = art-list.amount*/
            output-list.str = FILL(" ", pos)
            output-list.str = output-list.str
                            + SUBSTR(art-list.bezeich, 1, nbez1) 
                            + FILL(" ", nbez1 - LENGTH(art-list.bezeich))
        .
        IF price-decimal = 0 THEN   
        DO:   
           IF NOT long-digit THEN   
           DO:  
               output-list.str = output-list.str + STRING(scd-val, "->>>,>>>,>>9").  
               CREATE output-list.
               output-list.sort-i = sort-i.
               sort-i = sort-i + 1.
           END.  
           ELSE  
           DO:  
               output-list.str = output-list.str + STRING(scd-val, "->,>>>,>>>,>>9").  
               CREATE output-list.
               output-list.sort-i = sort-i.
               sort-i = sort-i + 1.
           END.  
        END.   
        ELSE  
        DO:  
            output-list.str = output-list.str + STRING(scd-val, "->>>,>>>,>>9.99").  
            CREATE output-list.
            output-list.sort-i = sort-i.
            sort-i = sort-i + 1.
        END.  
        printed-line = printed-line + 1.   
    END.
    /* Senior Citizen Discount */

  /* */
    DO i = 1 TO pos:  
        output-list.str = output-list.str + STRING(" ").  
    END.   
 
    DO i = 1 TO (nbezeich + n11 + 4):   
      IF i LT (nbezeich + n11 + 4) THEN /*MTPUT STREAM s1 "-" FORMAT "x(1)"*/  
        output-list.str = output-list.str + STRING("-", "x(1)").  
      ELSE  
      DO:
        output-list.str = output-list.str + STRING("-", "x(1)").  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
        /*MTPUT STREAM s1 "-" FORMAT "x(1)" SKIP.*/  
      END.  
    END.   
  /* */
    ASSIGN
        s = translateExtended ("After SC Disc.",lvCAREA,"")
        output-list.str = FILL(" ", pos)
        output-list.str = output-list.str
                        + SUBSTR(s, 1, nbez1)
                        + FILL(" ", nbez1 - LENGTH(s))
        subtotal2 = subtotal + tot-amount + scd-val
    .
    IF price-decimal = 0 THEN   
    DO:   
      IF NOT long-digit THEN   
      DO:  
         output-list.str = output-list.str + STRING(subtotal2, "->>>,>>>,>>9").  
         CREATE output-list.
         output-list.sort-i = sort-i.
         sort-i = sort-i + 1.
      END.  
      ELSE  
      DO:  
         output-list.str = output-list.str + STRING(subtotal2, "->,>>>,>>>,>>9").  
         CREATE output-list.
         output-list.sort-i = sort-i.
         sort-i = sort-i + 1.
      END.  
    END.   
    ELSE  
    DO:  
       output-list.str = output-list.str + STRING(subtotal2, "->>>,>>>,>>9.99").  
       CREATE output-list.
       output-list.sort-i = sort-i.
       sort-i = sort-i + 1.
    END.  
    printed-line = printed-line + 1.   

    IF prall-flag = 0 THEN RETURN.   
   
    tot-amount = subtotal2.
  END.

  /* Change line */
  CREATE output-list.
  ASSIGN
      output-list.sort-i = sort-i
      sort-i             = sort-i + 1
      printed-line       = printed-line + 1
  . 

  DO i = 1 TO pos:  
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 " ".*/  
  END.   
  /* Change line */
   
  FIND FIRST vhp.htparam WHERE htparam.paramnr = 846 NO-LOCK.   
  IF htparam.fchar = "" THEN tot-str = translateExtended ("Total",lvCAREA,"").   
  ELSE tot-str = vhp.htparam.fchar.   
  DO i = 1 TO nbez1:   
      IF i GT LENGTH(tot-str) THEN /*MTPUT STREAM s1 " "*/  
          output-list.str = output-list.str + STRING(" ").  
      ELSE /*MTPUT STREAM s1 SUBSTR(tot-str, i, 1) FORMAT "x(1)"*/  
          output-list.str = output-list.str + STRING(SUBSTR(tot-str, i, 1), "x(1)").  
  END.   
       
  IF price-decimal = 0 THEN   
  DO:   
     IF NOT long-digit THEN  
     DO:  
         output-list.str = output-list.str + STRING(ROUND(tot-amount, 2), "->>>,>>>,>>9").  
         CREATE output-list.
         output-list.sort-i = sort-i.
         sort-i = sort-i + 1.
         /*MTPUT STREAM s1 tot-amount FORMAT "->>>,>>>,>>9" SKIP.*/  
     END.  
     ELSE  
     DO:  
         output-list.str = output-list.str + STRING(ROUND(tot-amount, 2), "->,>>>,>>>,>>9").  
         CREATE output-list.
         output-list.sort-i = sort-i.
         sort-i = sort-i + 1.
         /*MTPUT STREAM s1 tot-amount FORMAT "->,>>>,>>>,>>9" SKIP.*/  
     END.  
  END.   
  ELSE  
  DO:  
      output-list.str = output-list.str + STRING(ROUND(tot-amount, 2), "->>>,>>>,>>9.99").  /*FT 051216*/
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 tot-amount FORMAT "->>>,>>9.99" SKIP.*/  
  END.  
  printed-line = printed-line + 1.   
  curr-j = curr-j + 6.   
  RUN multi-currency.   
END.   
  
PROCEDURE print-overhead3:   
DEFINE VARIABLE nbez1           AS INTEGER.   
DEFINE VARIABLE i               AS INTEGER.   
DEFINE VARIABLE pos             AS INTEGER.   
DEFINE VARIABLE lpage1          AS INTEGER.   
  
DEFINE VARIABLE balance         AS DECIMAL.   
DEFINE VARIABLE amt             AS DECIMAL.   
  
DEFINE VARIABLE bal-str         AS CHAR.   
DEFINE VARIABLE chg-str         AS CHAR.   
  
DEFINE VARIABLE new-sold-item   AS LOGICAL.  
DEFINE VARIABLE compli-notax    AS LOGICAL INITIAL NO.  
  
  FIND FIRST art-list WHERE art-list.artart = 0 NO-ERROR.  
  new-sold-item = AVAILABLE art-list.  
  
  nbez1 = nbezeich.  
  IF prTwoLine THEN nbez1 = nbez1 - 11.  
     
  IF anz-foot = 0 THEN lpage1 = lpage - 4.   
  ELSE lpage1 = lpage - 8.   
  IF curr-j GT lpage1 THEN   
  DO:   
    CREATE output-list.
    ASSIGN  
        output-list.flag-popup = YES  
        output-list.npause = npause
        output-list.sort-i = sort-i
        sort-i = sort-i + 1.
    curr-j = 0.   
    printed-line = 0.   
    RUN print-overhead1. /* print billheader IF curr-j = 0 OR print-all */   
  END.   
   
  balance = tot-amount /* + last-amount */.   
  FOR EACH art-list WHERE art-list.artart NE 0:     /* payments */   
  
    IF new-sold-item OR NOT art-list.printed THEN  
    DO:  
      IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
          output-list.str = output-list.str + STRING("", "x(6)").  
      ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
          output-list.str = output-list.str + STRING("", "x(5)").  
      DO i = 1 TO nbez1:   
        IF i GT LENGTH(art-list.bezeich) THEN /*MTPUT STREAM s1 " "*/  
            output-list.str = output-list.str + STRING(" ").  
        ELSE /*MTPUT STREAM s1 SUBSTR(art-list.bezeich, i, 1) FORMAT "x(1)"*/  
            output-list.str = output-list.str + STRING(SUBSTR(art-list.bezeich, i, 1), "x(1)").  
      END.   
    END.  
  
    IF (art-list.artart = 11 OR art-list.artart = 12) AND comp-taxserv AND comp-flag THEN   
    DO:   
      IF art-list.amount * subtotal > 0 THEN amt = subtotal.   
      ELSE amt = - subtotal.   
      ASSIGN  
        balance      = balance + amt  
        last-amount  = last-amount + amt  
        compli-notax = YES    
      .   
   
      IF new-sold-item OR NOT art-list.printed THEN  
      DO:  
        IF price-decimal = 0 THEN   
        DO:   
         IF NOT long-digit THEN  
         DO:  
             output-list.str = output-list.str + STRING(amt, "->>>,>>>,>>9").  
             CREATE output-list.
             output-list.sort-i = sort-i.
             sort-i = sort-i + 1.
             /*MTPUT STREAM s1 amt FORMAT "->>>,>>>,>>9" SKIP.*/  
         END.  
         ELSE  
         DO:  
             output-list.str = output-list.str + STRING(amt, "->,>>>,>>>,>>9").  
             CREATE output-list.
             output-list.sort-i = sort-i.
             sort-i = sort-i + 1.
             /*MTPUT STREAM s1 amt FORMAT "->,>>>,>>>,>>9" SKIP.*/  
         END.  
        END.   
        ELSE  
        DO:  
            output-list.str = output-list.str + STRING(amt, "->>>,>>>,>>9.99").  /*FT 051216*/
            CREATE output-list.
            output-list.sort-i = sort-i.
            sort-i = sort-i + 1.
            /*MTPUT STREAM s1 amt FORMAT "->>>,>>9.99" SKIP.*/  
        END.  
        printed-line = printed-line + 1.   
      END.   
    END.  
    ELSE   
    DO:   
      IF NOT art-list.printed OR print-all   
          THEN balance = balance + art-list.amount.   
      last-amount = last-amount + art-list.amount.   
  
      IF new-sold-item OR NOT art-list.printed THEN  
      DO:  
        IF price-decimal = 0 THEN   
        DO:   
           IF NOT long-digit THEN  
           DO:  
               output-list.str = output-list.str + STRING(art-list.amount, "->>>,>>>,>>9").  
               CREATE output-list.
               output-list.sort-i = sort-i.
               sort-i = sort-i + 1.
               /*MTPUT STREAM s1 art-list.amount FORMAT "->>>,>>>,>>9" SKIP.*/  
           END.  
           ELSE  
           DO:  
               output-list.str = output-list.str + STRING(art-list.amount, "->,>>>,>>>,>>9").  
               CREATE output-list.
               output-list.sort-i = sort-i.
               sort-i = sort-i + 1.
               /*MTPUT STREAM s1 art-list.amount FORMAT "->,>>>,>>>,>>9" SKIP.*/  
           END.  
        END.   
        ELSE  
        DO:  
            output-list.str = output-list.str + STRING(art-list.amount, "->>>,>>>,>>9.99").  /*FT 051216*/
            CREATE output-list.
            output-list.sort-i = sort-i.
            sort-i = sort-i + 1.
            /*MTPUT STREAM s1 art-list.amount FORMAT "->>>,>>9.99" SKIP.*/  
        END.  
        printed-line = printed-line + 1.   
      END.   
    END.  
  END.  
  
  IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
      output-list.str = output-list.str + STRING("", "x(6)").  
  ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
      output-list.str = output-list.str + STRING("", "x(5)").  
  DO i = 1 TO (nbezeich + n11 + 4):   
    IF i LT (nbezeich + n11 + 4) THEN /*MTPUT STREAM s1 "-" FORMAT "x(1)"*/  
        output-list.str = output-list.str + STRING("-", "x(1)").  
    ELSE  
    DO:  
        output-list.str = output-list.str + STRING("-", "x(1)").  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
        /*MTPUT STREAM s1 "-" FORMAT "x(1)" SKIP.*/  
    END.  
  END.   
  printed-line = printed-line + 1.   
   
  pos = 5.   
  IF qty1000 THEN pos = 6.  
    
  DO i = 1 TO pos:   
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 " ".*/  
  END.   
   
  IF NOT compli-notax THEN  
  DO:  
      balance = 0.  
      FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr  
          AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK:  
        balance = balance + vhp.h-bill-line.betrag.  
      END.  
  END.  
  
  IF (balance GE 0) THEN   
  DO:   
    IF NOT rm-transfer OR print-balance OR balance NE 0 THEN   
    DO:   
      bal-str = translateExtended ("Balance",lvCAREA,"").   
      DO i = 1 TO nbez1:   
        IF i GT LENGTH(bal-str) THEN /*MTPUT STREAM s1 " "*/  
            output-list.str = output-list.str + STRING(" ").  
        ELSE /*MTPUT STREAM s1 SUBSTR(bal-str, i, 1) FORMAT "x(1)"*/  
            output-list.str = output-list.str + STRING(SUBSTR(bal-str, i, 1), "x(1)").  
      END.   
      IF price-decimal = 0 THEN   
      DO:   
        IF NOT long-digit THEN   
        DO:  
            output-list.str = output-list.str + STRING(balance, "->>>,>>>,>>9").  
            CREATE output-list.
            output-list.sort-i = sort-i.
            sort-i = sort-i + 1.
            /*MTPUT STREAM s1 balance FORMAT "->>>,>>>,>>9" SKIP.*/  
        END.  
        ELSE  
        DO:  
            output-list.str = output-list.str + STRING(balance, "->,>>>,>>>,>>9").  
            CREATE output-list.
            output-list.sort-i = sort-i.
            sort-i = sort-i + 1.
            /*MTPUT STREAM s1 balance FORMAT "->,>>>,>>>,>>9" SKIP.*/  
        END.  
      END.   
      ELSE  
      DO:  
          output-list.str = output-list.str + STRING(balance, "->>>,>>>,>>9.99").  /*ft 051216*/
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 balance FORMAT "->>>,>>9.99" SKIP.*/  
      END.  
      printed-line = printed-line + 1.   
    END.   
  END.   
  ELSE   
  DO:   
    chg-str = translateExtended ("CHANGE",lvCAREA,"").   
    DO i = 1 TO nbez1:   
      IF i GT LENGTH(chg-str) THEN /*MTPUT STREAM s1 " "*/  
          output-list.str = output-list.str + STRING(" ").  
      ELSE /*MTPUT STREAM s1 SUBSTR(chg-str, i, 1) FORMAT "x(1)"*/  
          output-list.str = output-list.str + STRING(SUBSTR(chg-str, i, 1), "x(1)").  
    END.   
    IF price-decimal = 0 THEN   
    DO:   
       IF NOT long-digit THEN  
       DO:  
           output-list.str = output-list.str + STRING(- balance, "->>>,>>>,>>9").  
           CREATE output-list.
           output-list.sort-i = sort-i.
           sort-i = sort-i + 1.
           /*MTPUT STREAM s1 - balance FORMAT "->>>,>>>,>>9" SKIP.*/  
       END.  
       ELSE  
       DO:  
           output-list.str = output-list.str + STRING(- balance, "->,>>>,>>>,>>9").  
           CREATE output-list.
           output-list.sort-i = sort-i.
           sort-i = sort-i + 1.
           /*MTPUT STREAM s1 - balance FORMAT "->,>>>,>>>,>>9" SKIP.*/  
       END.  
    END.   
    ELSE  
    DO:  
        output-list.str = output-list.str + STRING(- balance, "->>>,>>>,>>9.99").  /*ft 051216*/
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
        /*MTPUT STREAM s1 - balance FORMAT "->>>,>>9.99" SKIP.*/  
    END.  
    printed-line = printed-line + 1.   
  END.   
   
  RUN print-net-vat.   
  RUN print-in-word.   
   
  IF vhp.h-bill.bilname NE "" THEN   
  DO:  
    IF vhp.h-bill.resnr GT 0 AND vhp.h-bill.reslinnr GT 0 THEN  
    DO:  
      FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.h-bill.resnr  
        AND vhp.res-line.reslinnr = vhp.h-bill.reslinnr NO-LOCK NO-ERROR.  
      IF AVAILABLE vhp.res-line THEN  
      DO:  
        output-list.str = output-list.str + STRING("").  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
        /*MTPUT STREAM s1 "" SKIP.*/  
  
        IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
            output-list.str = output-list.str + STRING("", "x(5)").  
        ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
            output-list.str = output-list.str + STRING("", "x(5)").  
  
        output-list.str = output-list.str +   
                STRING(translateExtended ("Room  :",lvCAREA,"")  
                       + " "  
                       + vhp.res-line.zinr).  
        CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
        /*MTPUT STREAM s1  
          translateExtended ("Room  :",lvCAREA,"")  
          " "  
          vhp.res-line.zinr SKIP.*/  
      END.  
      ELSE  
      DO:  
          output-list.str = output-list.str + STRING("").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 "" SKIP.*/  
      END.  
    END.
    ELSE DO:
          output-list.str = output-list.str + STRING("").  
          CREATE output-list.
          output-list.sort-i = sort-i.
          sort-i = sort-i + 1.
          /*MTPUT STREAM s1 "" SKIP.*/  
    END.

    IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
        output-list.str = output-list.str + STRING("", "x(6)").  
    ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
        output-list.str = output-list.str + STRING("", "x(5)").  
  
    output-list.str = output-list.str +   
            STRING(translateExtended ("Guest :",lvCAREA,"")) +  
            STRING(" ") + STRING(vhp.h-bill.bilname, "x(20)").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.

    /*MTPUT STREAM s1  
      translateExtended ("Guest :",lvCAREA,"")   
      " "   
      vhp.h-bill.bilname FORMAT "x(20)" SKIP.*/  
    IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
        output-list.str = output-list.str + STRING("", "x(6)").  
    ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
        output-list.str = output-list.str + STRING("", "x(5)").  
  
    output-list.str = output-list.str +   
        STRING(translateExtended ("Time  :",lvCAREA,"") + " "   
               + STRING(time,"HH:MM:SS") , "x(20)").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1  
      translateExtended ("Time  :",lvCAREA,"")   
      " "   
      STRING(time,"HH:MM:SS") FORMAT "x(20)" SKIP.*/  
  END.  
  ELSE   
  DO:  
    output-list.str = output-list.str + STRING("").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1 "" SKIP.*/  
    IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
        output-list.str = output-list.str + STRING("", "x(6)").  
    ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
        output-list.str = output-list.str + STRING("", "x(5)").  
  
    output-list.str = output-list.str +   
        STRING(translateExtended ("Time  :",lvCAREA,"")   
               + " " + STRING(time,"HH:MM:SS"), "x(20)").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1    
      translateExtended ("Time  :",lvCAREA,"")   
      " "   
      STRING(time,"HH:MM:SS") FORMAT "x(20)" SKIP. */  
  END.  
  RUN multi-currency.  

  IF gst-logic THEN
  DO:
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
    
      CREATE output-list.
      ASSIGN
        output-list.sort-i = sort-i
        sort-i = sort-i + 1
        output-list.str = output-list.str + STRING(translateExtended ("     Tax Code      Amount     GST",lvCAREA,"")).
    
      IF comp-taxserv THEN
      DO:
        CREATE output-list.
        ASSIGN
          output-list.sort-i = sort-i
          sort-i = sort-i + 1
          output-list.str = output-list.str + STRING(translateExtended ("     " + STRING(mwst-str,"x(13)") 
                                                                      + STRING(subtotal,"->>9.99 ") 
                                                                      + STRING(0,"->>9.99"),lvCAREA,"")).
      END.
      ELSE
      DO:
        CREATE output-list.
        ASSIGN
          output-list.sort-i = sort-i
          sort-i = sort-i + 1
          output-list.str = output-list.str + STRING(translateExtended ("     " + STRING(mwst-str,"x(13)") 
                                                                      + STRING(subtotal,"->>9.99 ") 
                                                                      + STRING(mwst,"->>9.99"),lvCAREA,"")).
      END.
        
      CREATE output-list.
        output-list.sort-i = sort-i.
        sort-i = sort-i + 1.
  END.                      
END.   
  
PROCEDURE print-overhead4:   
DEF VAR i AS INTEGER NO-UNDO.  
  IF anz-foot GT 0 THEN   
  DO:   
    output-list.str = output-list.str + STRING("").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
  
    output-list.str = output-list.str + STRING(foot1).  
    output-list.pos = 6.  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MT  
    PUT STREAM s1 "" SKIP(1)   
               foot1 AT 6 SKIP.*/  
    printed-line = printed-line + 3.   
  END.   
  IF foot2 NE "" THEN   
  DO:  
    output-list.str = output-list.str + STRING(foot2).  
    output-list.pos = 6.  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1 foot2 AT 6 SKIP.*/  
    printed-line = printed-line + 1.   
  END.   
  IF buttom-lines GE 1 THEN  
  DO i = 1 TO buttom-lines:  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 "" SKIP.*/  
      printed-line = printed-line + 1.  
  END.  
END.   
  
PROCEDURE cut-it:  
  FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu   
    AND vhp.printcod.code = "cut" NO-LOCK NO-ERROR.   
  IF AVAILABLE vhp.printcod THEN   
  DO:  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str + STRING(vhp.printcod.contcod).  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
        
      /*MTPUT STREAM s1 "" SKIP   
      vhp.printcod.contcod SKIP.*/  
  END.  
END.  
  
PROCEDURE cal-totalFB:  
DEF VAR billdate AS DATE    NO-UNDO.  
DEF VAR fact     AS INTEGER NO-UNDO.  
    
  IF NOT print-fbTotal THEN RETURN.  
  
  FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr  
    AND vhp.h-bill-line.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.  
  
  IF NOT AVAILABLE vhp.h-bill-line THEN RETURN.  
  ASSIGN billdate = vhp.h-bill-line.bill-datum.  
  
  
  FOR EACH vhp.h-journal WHERE vhp.h-journal.bill-datum = billdate  
    AND vhp.h-journal.departement = vhp.h-bill.departement  
    AND vhp.h-journal.rechnr = vhp.h-bill.rechnr NO-LOCK,  
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-journal.artnr  
      AND vhp.h-artikel.departement = vhp.h-journal.departement   
      AND vhp.h-artikel.artart = 0 NO-LOCK:    
  
    fact = 1.  
/*  
    IF (vhp.h-artikel.artnr = disc-art1) OR  
       (vhp.h-artikel.artnr = disc-art2) OR  
       (vhp.h-artikel.artnr = disc-art2) THEN  
    DO:  
      IF vhp.h-journal.bezeich MATCHES("*")   
        AND vhp.h-journal.anzahl * vhp.h-journal.betrag GT 0 THEN fact = -1.  
    END.  
*/  
    IF vhp.h-artikel.artnr = disc-art1 THEN  
        total-Fdisc = total-Fdisc + fact * vhp.h-journal.epreis.  
    ELSE IF vhp.h-artikel.artnr = disc-art2 THEN  
        total-Bdisc = total-Bdisc + fact * vhp.h-journal.epreis.  
    ELSE IF vhp.h-artikel.artnr = disc-art3 THEN    
        total-Odisc = total-Odisc + fact * vhp.h-journal.epreis.  
    ELSE  
    DO:  
      FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront  
        AND vhp.artikel.departement = vhp.h-artikel.departement NO-LOCK.  
      IF artikel.umsatzart = 3 OR artikel.umsatzart = 5 THEN  
        total-food = total-food   
          + fact * vhp.h-journal.anzahl * vhp.h-journal.epreis.   
      ELSE IF artikel.umsatzart = 6 THEN  
        total-bev = total-bev   
          + fact * vhp.h-journal.anzahl * vhp.h-journal.epreis.   
      ELSE IF artikel.umsatzart = 4 THEN  
        total-other = total-other   
          + fact * vhp.h-journal.anzahl * vhp.h-journal.epreis.   
    END.  
  END.  
END.      
  
PROCEDURE print-totalFB:  
DEF VAR pos         AS INTEGER            NO-UNDO.  
DEF VAR s           AS CHAR               NO-UNDO.  
DEF VAR i           AS INTEGER            NO-UNDO.  
DEF VAR nbez1       AS INTEGER.   
/*  
  IF NOT print-fbTotal THEN RETURN.  
  IF total-food EQ 0 AND total-bev EQ 0 AND total-other EQ 0 THEN RETURN.  
*/  
  
/* not allowed if discount item has been splitted, can cause mistake */  
  FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr  
    AND vhp.h-bill-line.departement = vhp.h-bill.departement  
    AND vhp.h-bill-line.artnr = f-discArt  
    AND SUBSTR(vhp.h-bill-line.bezeich, LENGTH(vhp.h-bill-line.bezeich)) = "*"  
    NO-LOCK NO-ERROR.  
  IF AVAILABLE vhp.h-bill-line THEN RETURN.  
  
  pos = 5.   
  IF qty1000 THEN pos = 6.  
  
  nbez1 = nbezeich.  
  IF prTwoLine THEN nbez1 = nbez1 - 11.  
  
  IF total-food NE 0 OR total-bev NE 0 OR total-other NE 0 THEN  
  DO:  
    output-list.str = output-list.str + STRING("").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1 "" SKIP.*/  
    printed-line = printed-line + 1.   
  END.
    
  IF total-food NE 0 THEN  
  DO:  
      DO i = 1 TO pos:  
          output-list.str = output-list.str + STRING(" ").  
          /*MTPUT STREAM s1 " ".*/  
      END.   
      s = translateExtended("FOOD", lvCAREA,"").  
      DO i = 1 TO nbez1:   
          IF i GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
              output-list.str = output-list.str + STRING(" ").  
          ELSE /*MTPUT STREAM s1 SUBSTR(s, i, 1) FORMAT "x(1)"*/  
              output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING(total-food, "->>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 total-food FORMAT "->>>,>>>,>>9" SKIP.*/  
      printed-line = printed-line + 1.   
  END.  
          
  IF total-bev NE 0 THEN  
  DO:  
      DO i = 1 TO pos:   
          /*MTPUT STREAM s1 " ".*/  
          output-list.str = output-list.str + STRING(" ").  
      END.   
      s = translateExtended("BEVERAGE", lvCAREA,"").  
      DO i = 1 TO nbez1:   
          IF i GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
              output-list.str = output-list.str + STRING(" ").  
          ELSE /*MTPUT STREAM s1 SUBSTR(s, i, 1) FORMAT "x(1)"*/  
              output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING(total-bev, "->>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 total-bev FORMAT "->>>,>>>,>>9" SKIP.*/  
      printed-line = printed-line + 1.   
  END.  
  
  IF total-other NE 0 THEN  
  DO:  
      DO i = 1 TO pos:  
          output-list.str = output-list.str + STRING(" ").  
          /*MTPUT STREAM s1 " ".*/  
      END.   
      s = translateExtended("OTHER", lvCAREA,"").  
      DO i = 1 TO nbez1:   
          IF i GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
              output-list.str = output-list.str + STRING(" ").  
          ELSE /*MTPUT STREAM s1 SUBSTR(s, i, 1) FORMAT "x(1)"*/  
              output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING(total-other, "->>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 total-other FORMAT "->>>,>>>,>>9" SKIP.*/  
      printed-line = printed-line + 1.   
  END.  
  
  IF total-fdisc NE 0 THEN  
  DO:  
      DO i = 1 TO pos:  
          output-list.str = output-list.str + STRING(" ").  
          /*MTPUT STREAM s1 " ".*/  
      END.   
      s = translateExtended("DISC FOOD", lvCAREA,"").  
      DO i = 1 TO nbez1:   
          IF i GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
              output-list.str = output-list.str + STRING(" ").  
          ELSE /*MTPUT STREAM s1 SUBSTR(s, i, 1) FORMAT "x(1)"*/  
              output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING(total-fdisc, "->>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 total-fdisc FORMAT "->>>,>>>,>>9" SKIP.*/  
      printed-line = printed-line + 1.   
  END.  
          
  IF total-bdisc NE 0 THEN  
  DO:  
      DO i = 1 TO pos:  
          output-list.str = output-list.str + STRING(" ").  
          /*MTPUT STREAM s1 " ".*/  
      END.   
      s = translateExtended("DISC BEVERAGE", lvCAREA,"").  
      DO i = 1 TO nbez1:   
          IF i GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
              output-list.str = output-list.str + STRING(" ").  
          ELSE /*MTPUT STREAM s1 SUBSTR(s, i, 1) FORMAT "x(1)"*/  
              output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING(total-bdisc, "->>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 total-bdisc FORMAT "->>>,>>>,>>9" SKIP.*/  
      printed-line = printed-line + 1.   
  END.  
          
  IF total-odisc NE 0 THEN  
  DO:  
      DO i = 1 TO pos:  
          output-list.str = output-list.str + STRING(" ").  
          /*MTPUT STREAM s1 " ".*/  
      END.   
      s = translateExtended("DISC OTHER", lvCAREA,"").  
      DO i = 1 TO nbez1:   
          IF i GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
              output-list.str = output-list.str + STRING(" ").  
          ELSE /*MTPUT STREAM s1 SUBSTR(s, i, 1) FORMAT "x(1)"*/  
              output-list.str = output-list.str + STRING(SUBSTR(s, i, 1), "x(1)").  
      END.  
      output-list.str = output-list.str + STRING(total-odisc, "->>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 total-odisc FORMAT "->>>,>>>,>>9" SKIP.*/  
      printed-line = printed-line + 1.   
  END.  
    
  output-list.str = output-list.str + STRING("").  
  CREATE output-list.
  output-list.sort-i = sort-i.
  sort-i = sort-i + 1.
  /*MTPUT STREAM s1 "" SKIP.*/  
  printed-line = printed-line + 1.   
  
END.  
  
PROCEDURE multi-currency:   
DEF VAR i            AS INTEGER  NO-UNDO.   
DEF VAR n            AS INTEGER  NO-UNDO.   
DEF VAR mesval       AS CHAR     NO-UNDO.   
DEF VAR s            AS CHAR     NO-UNDO.   
DEF VAR exchg-rate   AS DECIMAL  NO-UNDO.   
DEF VAR foreign-amt  AS DECIMAL  NO-UNDO.   
   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 830 NO-LOCK.   
  IF vhp.htparam.feldtyp NE 5 OR vhp.htparam.fchar = "" THEN RETURN.   
  DO i = 1 TO NUM-ENTRIES(vhp.htparam.fchar, ";"):   
    mesval = TRIM(ENTRY(i, vhp.htparam.fchar, ";")).   
    FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = mesval NO-LOCK NO-ERROR.   
    IF AVAILABLE vhp.waehrung THEN   
    DO:   
      exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit.   
      foreign-amt = ROUND(tot-amount / exchg-rate, 2).   
      s = vhp.waehrung.wabkurz + " " + translateExtended ("Total",lvCAREA,"").   
      IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
          output-list.str = output-list.str + STRING("", "x(6)").  
      ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
          output-list.str = output-list.str + STRING("", "x(5)").  
      DO n = 1 TO (nbezeich - 2):   
        IF n GT LENGTH(s) THEN /*MTPUT STREAM s1 " "*/  
            output-list.str = output-list.str + STRING(" ").  
        ELSE /*MTPUT STREAM s1 SUBSTR(s, n, 1) FORMAT "x(1)"*/  
            output-list.str = output-list.str + STRING(SUBSTR(s, n, 1), "x(1)").  
      END.   
      output-list.str = output-list.str + STRING(foreign-amt, "->>>,>>>,>>9.99").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 foreign-amt FORMAT "->,>>>,>>9.99" SKIP.*/  
      ASSIGN  
          curr-j = curr-j + 1  
          printed-line = printed-line + 1.   
    END.   
  END.   
   
END.   
  
PROCEDURE print-net-vat:   
DEFINE VARIABLE lpage1 AS INTEGER.   
DEFINE VARIABLE net-amt AS DECIMAL.   
DEFINE VARIABLE vat-str AS CHAR.   
DEFINE VARIABLE vat-proz AS DECIMAL.   
DEFINE VARIABLE vat-num AS INTEGER INITIAL 0.   
  
  IF comp-taxserv OR rm-transfer THEN RETURN.   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 376 NO-LOCK.   
  IF NOT vhp.htparam.flogical THEN RETURN.   
   
  FOR EACH vat-list:  
      DELETE vat-list.  
  END.  
  FOR EACH vhp.h-bill-line NO-LOCK WHERE   
      vhp.h-bill-line.rechnr = vhp.h-bill.rechnr AND  
      vhp.h-bill-line.departement = vhp.h-bill.departement,  
      FIRST vhp.h-artikel NO-LOCK WHERE   
      vhp.h-artikel.artnr = vhp.h-bill-line.artnr AND  
      vhp.h-artikel.departement = vhp.h-bill-line.departement AND  
      vhp.h-artikel.artart = 0 AND  
      vhp.h-artikel.mwst-code NE 0:  
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr   
      = vhp.h-artikel.mwst-code NO-LOCK.   
    IF vhp.htparam.fdecimal NE 0 THEN   
    DO:   
/*      IF NOT service-taxable THEN */  
      DO:   
        FIND FIRST vat-list WHERE vat-list.vat-amt = vhp.htparam.fdecimal   
          NO-ERROR.   
        IF NOT AVAILABLE vat-list THEN   
        DO:   
          CREATE vat-list.   
          ASSIGN vat-list.vat-amt = vhp.htparam.fdecimal.   
        END.   
        vat-list.betrag-amt = vat-list.betrag-amt + vhp.h-bill-line.betrag.   
      END.   
    END.   
  END.   
  
  FIND FIRST vat-list NO-ERROR.   
  
  IF AVAILABLE vat-list THEN   
  DO:   
    net-amt = 0.   
    FOR EACH vat-list:   
      vat-num = vat-num + 1.   
      vat-proz = vat-list.vat-amt.   
      net-amt = net-amt + vat-list.betrag-amt / (1 + vat-list.vat-amt / 100).   
      DELETE vat-list.   
    END.   
    ASSIGN  
      net-amt = ROUND(net-amt, price-decimal)   
      mwst1   = tot-sales - net-amt  
    .   
  END.   
  ELSE net-amt = tot-amount - mwst1.   
   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 872 NO-LOCK.   
  IF vhp.htparam.fchar NE "" THEN vat-str = vhp.htparam.fchar.   
  ELSE vat-str = translateExtended ("VAT",lvCAREA,"").   
  IF vat-num = 1 THEN vat-str = vat-str + " " + STRING(vat-proz) + "%".   
   
  IF anz-foot = 0 THEN lpage1 = lpage - 3.   
  ELSE lpage1 = lpage - 7.   
  IF curr-j GT lpage1 THEN   
  DO:   
    CREATE output-list.  
    ASSIGN  
        output-list.flag-popup = YES  
        output-list.npause = npause
        output-list.sort-i = sort-i
        sort-i = sort-i + 1.
    curr-j = 0.   
    printed-line = 0.   
    RUN print-overhead1. /* print billheader IF curr-j = 0 OR print-all */   
  END.   
   
  IF qty1000 THEN  
  DO:  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str + STRING(translateExtended ("NET",lvCAREA,"")).  
      output-list.pos = 7.  
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 "" SKIP translateExtended ("NET",lvCAREA,"") AT 7  " ".*/  
  END.  
  ELSE  
  DO:  
      output-list.str = output-list.str + STRING("").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
  
      output-list.str = output-list.str + STRING(translateExtended ("NET",lvCAREA,"")).  
      output-list.pos = 6.  
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 "" SKIP translateExtended ("NET",lvCAREA,"") AT 6  " ".*/  
  END.  
  
  IF NOT long-digit THEN   
  DO:  
      output-list.str = output-list.str + STRING(net-amt, "->>,>>>,>>9.99").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
     /*MTPUT STREAM s1 net-amt FORMAT "->>,>>>,>>9.99" SKIP.*/  
  END.  
  ELSE  
  DO:  
      output-list.str = output-list.str + STRING(net-amt, "->,>>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 net-amt FORMAT "->,>>>,>>>,>>9" SKIP.*/  
  END.  
  printed-line = printed-line + 2.   
   
  IF qty1000 THEN   
  DO:  
      output-list.str = output-list.str + STRING(vat-str).  
      output-list.pos = 7.  
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 vat-str AT 7  " ".*/  
  END.  
  ELSE  
  DO:  
      output-list.str = output-list.str + STRING(vat-str).  
      output-list.pos = 6.  
      output-list.str = output-list.str + STRING(" ").  
      /*MTPUT STREAM s1 vat-str AT 6  " ".*/  
  END.  
  
  IF NOT long-digit THEN   
  DO:  
      output-list.str = output-list.str + STRING(mwst1, "->>,>>>,>>9.99").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 mwst1 FORMAT "->>,>>>,>>9.99" SKIP.*/  
  END.  
  ELSE  
  DO:  
      output-list.str = output-list.str + STRING(mwst1, "->,>>>,>>>,>>9").  
      CREATE output-list.
      output-list.sort-i = sort-i.
      sort-i = sort-i + 1.
      /*MTPUT STREAM s1 mwst1 FORMAT "->,>>>,>>>,>>9" SKIP.*/  
  END.  
  printed-line = printed-line + 2.   
END.   
   
PROCEDURE print-in-word:   
DEFINE VARIABLE lpage1 AS INTEGER.   
DEFINE VARIABLE progname AS CHAR NO-UNDO.   
DEFINE VARIABLE str1 AS CHAR NO-UNDO.   
DEFINE VARIABLE str2 AS CHAR NO-UNDO.   
DEFINE VARIABLE w-length AS INTEGER NO-UNDO.   
DEFINE VARIABLE i AS INTEGER NO-UNDO.   
  
  IF comp-taxserv THEN RETURN.   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 825 NO-LOCK.   
  IF vhp.htparam.flogical = NO THEN RETURN.   
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 829 NO-LOCK.   
  IF vhp.htparam.fchar = "" THEN RETURN.   
   
   IF anz-foot = 0 THEN lpage1 = lpage - 3.   
   ELSE lpage1 = lpage - 7.   
   IF curr-j GT lpage1 THEN DO:   
    CREATE output-list.
    ASSIGN  
        output-list.flag-popup = YES  
        output-list.npause = npause
        output-list.sort-i = sort-i
        sort-i = sort-i + 1.
    curr-j = 0.   
    printed-line = 0.   
    RUN print-overhead1. /* print billheader IF curr-j = 0 OR print-all */   
  END.   
   
  progname = vhp.htparam.fchar.   
  w-length = nbezeich.  
  IF NOT prTwoLine THEN w-length = w-length + 15.   
    
  RUN value(progname) (tot-amount, w-length, OUTPUT str1, OUTPUT str2).   
  output-list.str = output-list.str + STRING("").  
  CREATE output-list.
  output-list.sort-i = sort-i.
  sort-i = sort-i + 1.
  /*MTPUT STREAM s1 "" SKIP.*/  
  IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
      output-list.str = output-list.str + STRING("", "x(6)").  
  ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
      output-list.str = output-list.str + STRING("", "x(5)").  
  
  DO i = 1 TO LENGTH(str1):   
      output-list.str = output-list.str + STRING(SUBSTR(str1,i,1), "x(1)").  
      /*MTPUT STREAM s1 SUBSTR(str1,i,1) FORMAT "x(1)".*/  
  END.   
  output-list.str = output-list.str + STRING("").  
  CREATE output-list.
  output-list.sort-i = sort-i.
  sort-i = sort-i + 1.
  /*MTPUT STREAM s1 "" SKIP.*/  
  printed-line = printed-line + 2.   
  IF TRIM(str2) NE "" THEN   
  DO:   
    IF qty1000 THEN /*MTPUT STREAM s1 "" FORMAT "x(6)"*/  
        output-list.str = output-list.str + STRING("", "x(6)").  
    ELSE /*MTPUT STREAM s1 "" FORMAT "x(5)"*/  
        output-list.str = output-list.str + STRING("", "x(5)").  
    DO i = 1 TO LENGTH(str2):   
        output-list.str = output-list.str + STRING(SUBSTR(str2,i,1), "x(1)").  
        /*MTPUT STREAM s1 SUBSTR(str2,i,1) FORMAT "x(1)".*/  
    END.  
    output-list.str = output-list.str + STRING("").  
    CREATE output-list.
    output-list.sort-i = sort-i.
    sort-i = sort-i + 1.
    /*MTPUT STREAM s1 "" SKIP.*/  
    printed-line = printed-line + 1.   
  END.   
END.   

/* */
PROCEDURE inv-cat:
DEFINE INPUT PARAMETER artnr AS INTEGER.
DEFINE OUTPUT PARAMETER is-bev AS LOGICAL.
DEFINE OUTPUT PARAMETER is-food AS LOGICAL.

FIND FIRST h-artikel WHERE h-artikel.artnr EQ artnr NO-LOCK NO-ERROR.
IF AVAILABLE h-artikel THEN
    IF h-artikel.endkum EQ 1 THEN
        ASSIGN is-food = YES
            is-bev = NO.
    IF h-artikel.endkum EQ 2 THEN
        ASSIGN is-bev = YES
            is-food = NO.
END.
