
DEFINE TEMP-TABLE output-list  
    FIELD str        AS CHARACTER  
    FIELD pos        AS INT  
    .

DEFINE TEMP-TABLE op-list 
  FIELD artnr       AS INTEGER 
  FIELD anzahl      AS DECIMAL 
  FIELD bezeich     AS CHAR 
  FIELD bez-aend    AS LOGICAL INITIAL NO 
  FIELD disc        AS DECIMAL 
  FIELD disc2       AS DECIMAL 
  FIELD vat         AS DECIMAL 
  FIELD epreis      AS DECIMAL 
  FIELD epreis0     AS DECIMAL 
  FIELD warenwert   AS DECIMAL 
  FIELD konto       AS CHAR 
  FIELD warenwert0  AS DECIMAL
  FIELD remark      AS CHAR
. 
DEFINE WORKFILE header-list 
  FIELD texte AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE loop1-list 
  FIELD texte AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE loop-list 
  FIELD texte AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE brief-list 
  FIELD b-text AS CHAR. 

DEFINE WORKFILE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar AS CHAR. 

DEF INPUT  PARAMETER briefnr  AS INTEGER. 
DEF INPUT  PARAMETER docu-nr        AS CHAR. 
DEF INPUT  PARAMETER printnr        AS INT.
DEF OUTPUT PARAMETER err            AS INT INIT 0.
DEF OUTPUT PARAMETER outfile        AS CHAR. 
DEF OUTPUT PARAMETER printer-pglen  AS INT.
DEF OUTPUT PARAMETER supplier-name  AS CHAR.
DEF OUTPUT PARAMETER bill-recv      AS CHAR.
DEF OUTPUT PARAMETER address1       AS CHAR.
DEF OUTPUT PARAMETER address2       AS CHAR.
DEF OUTPUT PARAMETER order-date     AS DATE.
DEF OUTPUT PARAMETER deliv-date     AS DATE.
DEF OUTPUT PARAMETER telefon        AS CHAR.
DEF OUTPUT PARAMETER fax            AS CHAR.
DEF OUTPUT PARAMETER pr-nr          AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR output-list.  
DEF OUTPUT PARAMETER TABLE FOR op-list.

DEFINE VARIABLE long-digit          AS LOGICAL. 
DEFINE VARIABLE price-decimal       AS INTEGER.
DEFINE VARIABLE foreign-currency    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE saldo               AS DECIMAL FORMAT "->>,>>>,>>9.99". 
DEFINE VARIABLE bl-balance          AS DECIMAL FORMAT "->>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot-qty             AS DECIMAL FORMAT "->>,>>9.99" INITIAL 0. 
DEFINE VARIABLE currloop            AS INTEGER. 

DEFINE VARIABLE pos-bez             AS INTEGER INITIAL 0. 
DEFINE VARIABLE keychar             AS CHAR. 
DEFINE VARIABLE remain-bez          AS CHAR. 

DEFINE VARIABLE pr                  AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE curr-line           AS INTEGER. 
DEFINE VARIABLE curr-page           AS INTEGER. 
DEFINE VARIABLE curr-pos            AS INTEGER. 
DEFINE VARIABLE blloop              AS INTEGER INITIAL 0. 
DEFINE VARIABLE headloop            AS INTEGER INITIAL 0. 
DEFINE VARIABLE f-lmargin           AS LOGICAL INITIAL NO. 
DEFINE VARIABLE lmargin             AS INTEGER INITIAL 1. 
DEFINE VARIABLE n                   AS INTEGER. 
DEFINE VARIABLE disc2-flag          AS LOGICAL INITIAL NO.
DEFINE VARIABLE remark-len          AS INTEGER INITIAL 24.

DEFINE VARIABLE bez-len         AS INTEGER INITIAL 35. 
DEFINE VARIABLE pos-ord         AS INTEGER INITIAL 0. 
DEFINE VARIABLE ord-len         AS INTEGER INITIAL 35. 
DEFINE VARIABLE ntab            AS INTEGER INITIAL 1. 
DEFINE VARIABLE nskip           AS INTEGER INITIAL 1. 

IF printnr = 0 THEN outfile = "\vhp-letter.rtf". 
ELSE DO: 
  FIND FIRST PRINTER WHERE printer.nr = printnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE PRINTER THEN 
  DO: 
    err = 1.
    /*hide MESSAGE NO-PAUSE. 
    MESSAGE "Printer not yet selected" VIEW-AS ALERT-BOX INFORMATION. */
    RETURN. 
  END. 
  ELSE outfile = printer.path. 
END. 
printer-pglen = printer.pglen.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 

FIND FIRST fa-ordheader WHERE fa-ordheader.order-nr = docu-nr NO-LOCK NO-ERROR.
IF NOT AVAILABLE fa-ordheader THEN
DO:
  err = 2.
  /*MT
  HIDE MESSAGE NO-PAUSE.
  MESSAGE "fa-order record not found. Printing process stopped."
    VIEW-AS ALERT-BOX INFORMATION.
  */
  RETURN.
END.
 
pr = fa-ordheader.pr-nr. 
 
FIND FIRST waehrung WHERE waehrung.waehrungsnr = fa-ordheader.currency 
  NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  IF htparam.fchar NE "" AND (htparam.fchar NE waehrung.wabkurz) THEN 
    foreign-currency = YES. 
END. 
 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr 
  = fa-ordheader.supplier-nr NO-LOCK NO-ERROR. 
FIND FIRST gl-department WHERE gl-department.nr = fa-ordheader.dept-nr 
  NO-LOCK NO-ERROR. 

IF AVAILABLE l-lieferant THEN
DO:
  ASSIGN 
      supplier-name = l-lieferant.namekontakt + ", " + l-lieferant.vorname1 
                      + " " + l-lieferant.anrede1
      bill-recv     = l-lieferant.firma
      address1      = l-lieferant.adresse1
      address2      = l-lieferant.adresse2
      order-date    = DATE(fa-ordheader.order-date)
      deliv-date    = DATE(fa-ordheader.expected-delivery)
      telefon       = l-lieferant.telefon
      fax           = l-lieferant.fax
      pr-nr         = fa-ordheader.pr-nr
      .

END.

CREATE output-list.
RUN fill-list.


curr-line = 1. 
curr-page = 1.
DEF VAR a AS INT.
FOR EACH brief-list:
    a = a + 1.
END.

FOR EACH brief-list:

    IF curr-line GT printer.pglen THEN 
    DO: 
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    curr-pos = 1. 
    RUN analyse-text. 

    
    IF blloop = 0  AND headloop = 0 THEN 
    DO: 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" ").
      END. 
      RUN build-text-line (brief-list.b-text). 
      output-list.str = output-list.str + STRING("").
      CREATE output-list.
      /*MT
      PUT STREAM s1 "" SKIP. 
      */
      curr-line = curr-line + 1. 
      curr-pos = 1. 
    END. 
    
    ELSE IF blloop = 2 THEN 
    DO: 
      create loop-list. 
      loop-list.texte = brief-list.b-text. 
      curr-pos = 1. 
    END. 
    
    ELSE IF headloop = 2 THEN 
    DO: 
      create loop1-list. 
      loop1-list.texte = brief-list.b-text. 
      curr-pos = 1. 
    END. 
    ELSE IF blloop = 3 THEN RUN do-billline. 
    ELSE IF headloop = 3 THEN RUN do-billhead.
    
    IF blloop = 1 THEN blloop = 2. 
    IF headloop = 1 THEN headloop = 2.
END. 

FIND FIRST fa-ordheader WHERE fa-ordheader.supplier-nr = fa-ordheader.supplier-nr 
  AND fa-ordheader.order-nr = docu-nr /*AND l-order.pos = 0*/ EXCLUSIVE-LOCK. 
fa-ordheader.printed = TODAY. 
fa-ordheader.PrintedTime = TIME. 
FIND CURRENT fa-ordheader NO-LOCK. 

/*************** PROCEDURES ***************/
PROCEDURE analyse-text: 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2300. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN headloop = 1. 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2301. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN headloop = headloop + 1. 
 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2302. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN 
  DO: 
    blloop = 1. 
  END. 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2303. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN blloop = blloop + 1. 
END. 

PROCEDURE build-text-line: 
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
  DO i = 1 TO LENGTH(curr-texte): 
    IF SUBSTR( curr-texte,i,1) = keychar THEN 
    DO: 
      IF i = LENGTH(curr-texte) THEN found = NO. 
      ELSE IF SUBSTR(curr-texte, i + 1, 1) = " " THEN found = NO. 
      ELSE 
      DO: 
        RUN put-string(SUBSTR(curr-texte, j, i - j)). 
        RUN interprete-text(curr-texte, INPUT-OUTPUT i, OUTPUT found). 
        j = i + 1. 
      END. 
    END. 
    ELSE found = NO. 
  END. 
  IF NOT found THEN 
    RUN put-string (SUBSTR(curr-texte, j, LENGTH(curr-texte) - j + 1)). 
END. 

PROCEDURE fill-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE l AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE keycont AS CHAR. 
DEFINE VARIABLE continued AS LOGICAL INITIAL NO. 
 
  FIND FIRST htparam WHERE paramnr = 600 NO-LOCK. 
  keychar = htparam.fchar. 
  FIND FIRST htparam WHERE paramnr = 1122 NO-LOCK. 
  keycont = keychar + htparam.fchar. 
 
  FOR EACH htparam WHERE paramgruppe = 17 AND htparam.bezeich NE "Not used" 
      NO-LOCK BY LENGTH(htparam.fchar) descending: 
    create htp-list. 
    htp-list.paramnr = htparam.paramnr. 
    htp-list.fchar = keychar + htparam.fchar. 
  END. 
  DO: 
    FOR EACH briefzei WHERE briefzei.briefnr = briefnr NO-LOCK 
      BY briefzei.briefzeilnr: 
      j = 1. 
      DO i = 1 TO LENGTH(briefzei.texte): 
         IF asc(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
         DO: 
           n = i - j. 
           c = SUBSTR(briefzei.texte, j,  n). 
           l = LENGTH(c). 
           IF NOT continued THEN create brief-list. 
           brief-list.b-text = brief-list.b-text + c. 
           j = i + 1. 
           IF l GT LENGTH(keycont) AND 
             SUBSTR(c, l - LENGTH(keycont) + 1, LENGTH(keycont)) = keycont THEN 
           DO: 
             continued = YES. 
             b-text = SUBSTR(b-text, 1, LENGTH(b-text) - LENGTH(keycont)). 
           END. 
           ELSE continued = NO. 
         END. 
      END. 
      n = LENGTH(briefzei.texte) - j + 1. 
      c = SUBSTR(briefzei.texte, j,  n). 
      IF NOT continued THEN create brief-list. 
      brief-list.b-text = brief-list.b-text + c. 
    END. 
  END. 
END. 

PROCEDURE do-billhead: 
    
DEFINE VARIABLE n AS INTEGER. 
  headloop = 3. 
  FOR EACH header-list: 
    delete header-list. 
  END. 
  FOR EACH loop1-list: 
    create header-list. 
    curr-pos = 1. 
    IF f-lmargin THEN DO n = 1 TO lmargin: 
      RUN put-string(" "). 
    END. 
    RUN build-loop-line (loop1-list.texte). 
  END. 
  headloop = 0. 
  RUN print-billhead.
END. 


 
PROCEDURE build-loop-line: 
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
  DO i = 1 TO LENGTH(curr-texte): 
    IF SUBSTR( curr-texte,i,1) = keychar THEN 
    DO: 
      IF i = LENGTH(curr-texte) THEN found = NO. 
      ELSE IF SUBSTR(curr-texte, i + 1, 1) = " " THEN found = NO. 
      ELSE DO: 
        RUN put-string(SUBSTR(curr-texte, j, i - j)). 
        RUN interprete-text(curr-texte, INPUT-OUTPUT i, OUTPUT found). 
        j = i + 1. 
      END. 
    END. 
    ELSE found = NO. 
  END. 
  IF NOT found THEN 
    RUN put-string(SUBSTR(curr-texte, j, LENGTH(curr-texte) - j + 1)). 
END. 
 
PROCEDURE do-billline: 
    
DEFINE buffer l-art FOR l-artikel. 
DEFINE VARIABLE create-it AS LOGICAL. 
DEFINE VARIABLE curr-bez AS CHAR. 
DEFINE VARIABLE bez-aend AS LOGICAL. 
DEFINE VARIABLE disc AS DECIMAL. 
DEFINE VARIABLE disc2 AS DECIMAL. 
DEFINE VARIABLE vat AS DECIMAL. 
  saldo = 0. 
  bl-balance = 0. 
  FOR EACH op-list: 
    delete op-list. 
  END. 

  FOR EACH fa-order WHERE fa-order.order-nr = docu-nr AND 
    fa-order.activeflag = 0 NO-LOCK BY fa-order.fa-pos :

    create-it = NO. 
    bez-aend = NO. 
    
    FIND FIRST mathis WHERE mathis.nr = fa-order.fa-nr NO-LOCK.
    curr-bez = mathis.NAME.

    disc = 0. 
    disc2 = 0. 

    FIND FIRST op-list WHERE op-list.artnr = fa-order.fa-nr 
    AND op-list.epreis = fa-order.order-price 
    AND op-list.bezeich = mathis.NAME
    AND op-list.disc = fa-order.discount1 AND op-list.disc2 = discount2 
    NO-ERROR. 

    IF NOT AVAILABLE op-list OR create-it THEN 
    DO: 
      vat = 0. 
      CREATE op-list.
      ASSIGN
        op-list.artnr = fa-order.fa-nr
        op-list.bezeich = curr-bez
        op-list.bez-aend = bez-aend 
        op-list.epreis = fa-order.order-price 
        op-list.epreis0 = fa-order.order-price 
        /*op-list.konto = l-order.stornogrund*/
        op-list.remark = fa-order.fa-remarks
        op-list.disc = fa-order.discount1
        op-list.disc2 = fa-order.discount2
        op-list.vat = fa-order.vat
        disc = fa-order.discount1 / 100
        disc2 = fa-order.discount2 / 100
        vat = fa-order.vat / 100.
    END. 
    op-list.epreis0 = fa-order.order-price / (1 - disc) / (1 - disc2) / (1 + vat). 
    op-list.anzahl = op-list.anzahl + fa-order.order-qty. 
    op-list.warenwert = op-list.warenwert + fa-order.order-amount. 
    op-list.warenwert0 = op-list.warenwert0 
        + fa-order.order-amount / (1 - disc) / (1 - disc2) / (1 + vat). 
    tot-qty = tot-qty + fa-order.order-qty. 
  END. 
 
  currloop = 0. 
  FOR EACH op-list: 
    IF op-list.anzahl = 0 THEN delete op-list. 
  END. 
  
  FOR EACH op-list, 
      FIRST mathis WHERE mathis.nr = op-list.artnr NO-LOCK: 

      IF curr-line GT printer.pglen THEN 
      DO: 
          curr-page = curr-page + 1. 
          curr-line = 1. 
          RUN do-billhead. 
      END. 
      currloop = currloop + 1. 
      bl-balance = bl-balance + op-list.warenwert. 
      saldo = saldo + op-list.warenwert. 
      FOR EACH loop-list: 
          curr-pos = 1. 
          remain-bez = "". 
          IF f-lmargin THEN DO n = 1 TO lmargin:
              RUN put-string(" "). 
          END. 
          RUN build-loop-line (loop-list.texte). 

          CREATE output-list.
          output-list.str = output-list.str + STRING("").
          /*MT
          PUT STREAM s1 "" SKIP. 
          */
          curr-line = curr-line + 1. 
          DO WHILE remain-bez NE "": 
              RUN print-bezeich1. 
              CREATE output-list.
              output-list.str = output-list.str + STRING("").
              /*MT
              PUT STREAM s1 "" SKIP. 
              */
              curr-line = curr-line + 1. 
          END. 
      END. 
  END. 
  FOR EACH loop-list:
      delete loop-list. 
  END. 
  blloop = 0. 
END. 
 
 
PROCEDURE print-billhead: 
DEFINE VARIABLE i AS INTEGER. 
  FOR EACH header-list: 
      curr-pos = 1. 
      DO i = 1 TO LENGTH(header-list.texte):
          output-list.str = output-list.str + STRING(SUBSTR(header-list.texte, i, 1), "x(1)").
          /*MTPUT STREAM s1 SUBSTR(header-list.texte, i, 1) FORMAT "x(1)". */
      END.
      output-list.str = output-list.str + STRING("").
      CREATE output-list.
      /*MT PUT STREAM s1 "" SKIP. */
      curr-line = curr-line + 1. 
  END. 
END. 
 
PROCEDURE interprete-text: 
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)". 
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER. 
DEFINE OUTPUT PARAMETER found AS LOGICAL INITIAL NO. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE rowno AS INTEGER INITIAL 0. 
 
  j = i. 
  FIND FIRST htp-list. 
  DO WHILE AVAILABLE htp-list AND NOT found: 
    IF htp-list.fchar = SUBSTR(curr-texte, j, LENGTH(htp-list.fchar)) THEN 
    DO: 
      found = YES. 
      i = j + LENGTH(htp-list.fchar) - 1. 
 
      IF htp-list.paramnr = 777 /* disc AND disc2 */ THEN 
      DO: 
        disc2-flag = NO. 
        IF SUBSTR(curr-texte, i + 1, 1) EQ "2" THEN 
        DO: 
          disc2-flag = YES. 
          i = i + 1. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 1005  /* item's remark */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          remark-len = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          i = i + 2. 
        END. 
      END. 

      ELSE IF htp-list.paramnr = 1063 THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          rowno = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          IF rowno GT printer.pglen THEN rowno = PRINTER.pglen.          
          i = i + 2. 
          IF curr-line < rowno THEN 
          DO: 
            DO j = 1 TO (rowno - curr-line):
                output-list.str = output-list.str + STRING(" ").
                CREATE output-list.
                /*MT PUT STREAM s1 "" SKIP. */
            END. 
            curr-line = rowno. 
            curr-pos = 1. 
          END. 
        END. 
        IF curr-line GE printer.pglen THEN 
        DO: 
          curr-page = curr-page + 1. 
          curr-line = 1. 
          RUN do-billhead. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 2306  /* Description */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          bez-len = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          i = i + 2. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 692  /* Order Instruction */  THEN 
      DO: 
        pos-ord = curr-pos. 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          ord-len = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          IF bez-len GT ord-len THEN ord-len = bez-len. 
          i = i + 2. 
        END. 
      END. 
      RUN decode-key(curr-texte, INPUT htp-list.paramnr, INPUT-OUTPUT i). 
    END. 
    FIND NEXT htp-list NO-ERROR. 
  END. 
  IF NOT found THEN RUN put-string(SUBSTR(curr-texte, j, 1)). 
END. 
 
PROCEDURE decode-key: 
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)". 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER. 
DEFINE VARIABLE out-str AS CHAR. 
DEFINE VARIABLE status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE m AS INTEGER. 
 
/* 
status-code = 0   ==> NO-ERROR 
             -1       letter start 
             -2       letter END 
 
              1       TAB 
              2       SKIP 
              3       left margin ON 
 
              6       reservation start 
              7       reservation END 
 
              8       debt start 
              9       debt END 
*/ 
  RUN decode-key1 (paramnr, OUTPUT out-str, OUTPUT status-code). 

 
  IF status-code GE 1 AND status-code LE 5 THEN 
  DO: 
    RUN find-parameter(paramnr, curr-texte, status-code, INPUT-OUTPUT i). 
  END. 
  IF status-code = 1 THEN 
  DO: 
    m = curr-pos + 1. 
    IF curr-pos GT ntab THEN 
    DO:
      output-list.str = output-list.str + STRING("").
      CREATE output-list.
      /*MT PUT STREAM s1 "" SKIP. */
      curr-line = curr-line + 1. 
      curr-pos = 1. 
      DO n = 2 TO ntab: 
        RUN put-string(" "). 
      END. 
    END. 
    ELSE DO n = m TO ntab: 
      RUN put-string(" "). 
    END. 
    curr-pos = ntab. 
  END. 
  ELSE IF status-code = 2 AND headloop = 0 AND blloop = 0 THEN DO n = 1 TO nskip: 
    output-list.str = output-list.str + STRING("").
    CREATE output-list.
    /*MT PUT STREAM s1 "" SKIP. */
    curr-pos = 1. 
    curr-line = curr-line + 1. 
  END. 
  ELSE IF status-code = 3 THEN DO n = 1 TO lmargin: 
    RUN put-string (" "). 
  END. 
END. 
 
PROCEDURE find-parameter: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)". 
DEFINE INPUT PARAMETER status-code AS INTEGER. 
DEFINE INPUT-OUTPUT PARAMETER i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE stopped AS LOGICAL INITIAL NO. 
  FIND FIRST htp-list WHERE htp-list.paramnr = paramnr. 
  j = i + 1. 
  DO WHILE NOT stopped: 
    IF SUBSTR(curr-texte, j, 1) LT "0" 
      OR SUBSTR(curr-texte, j, 1) GT "9" THEN stopped = YES. 
    ELSE j = j + 1. 
  END. 
  IF j GT (i + 1) THEN 
  DO: 
    j = j - 1. 
    n = INTEGER(SUBSTR(curr-texte, i + 1, j - i)). 
    IF status-code = 1 THEN ntab = n. 
    ELSE IF status-code = 2 THEN nskip = n. 
    ELSE IF status-code = 3 THEN lmargin = n. 
    i = j. 
  END. 
END. 
 
PROCEDURE decode-key1: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE curr-bez AS CHAR. 
  FIND FIRST htparam WHERE paramnr = paramnr NO-LOCK. 
  IF paramnr = 601           /* page      */  THEN /*MT page STREAM s1. */.
  ELSE IF paramnr = 602      /* page NO   */ THEN 
      RUN put-string(STRING(curr-page)).
  ELSE IF paramnr = 603 THEN /* Tabulator */ status-code = 1. 
  ELSE IF paramnr = 604      /* today's DATE */ THEN 
      RUN put-string(STRING(today)).
  ELSE IF paramnr = 605 THEN /* SKIP      */ status-code = 2. 
  ELSE IF paramnr = 637      /* name contact */ AND AVAILABLE l-lieferant THEN 
  DO: 
     RUN put-string(l-lieferant.namekontakt + ", " + l-lieferant.vorname1 
            + " " + l-lieferant.anrede1).
  END. 
  ELSE IF paramnr = 664      /* PO Receiver */ AND AVAILABLE l-lieferant THEN 
    RUN put-string(l-lieferant.firma).
  ELSE IF paramnr = 643      /* address1 */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.adresse1)).
  ELSE IF paramnr = 644      /* address2 */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.adresse2)).
  ELSE IF paramnr = 645      /* address3 */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.adresse3)).
  ELSE IF paramnr = 646      /* land */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.land)).
  ELSE IF paramnr = 647      /* PLZ */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(STRING(l-lieferant.plz)).
  ELSE IF paramnr = 648      /* city */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.wohnort)).
  ELSE IF paramnr = 691      /* Fax */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.fax)).
  ELSE IF paramnr = 382      /* Phone */ AND AVAILABLE l-lieferant 
    THEN RUN put-string(TRIM(l-lieferant.telefon)).
 
  ELSE IF paramnr = 616      /* left margin ON */ THEN 
  DO: 
    f-lmargin = YES. 
    status-code = 3. 
  END. 
  ELSE IF paramnr = 617 THEN /* left margin off */ f-lmargin = NO. 
  ELSE IF (paramnr GE 618) AND (paramnr LE 629) /* printcod */ THEN 
  DO: 
    FIND FIRST htparam WHERE htparam.paramnr = paramnr NO-LOCK. 
    FIND FIRST printcod WHERE printcod.emu = printer.emu 
      AND printcod.code = htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE printcod THEN RUN put-string(TRIM(printcod.contcod)).
  END. 
 
  ELSE IF paramnr = 652            /* Purchase Request Number */  THEN 
  DO: 
    DEFINE buffer l-od0 FOR fa-ordheader. 
    FIND FIRST l-od0 WHERE l-od0.order-nr = docu-nr 
      AND l-od0.supplier-nr = fa-ordheader.supplier-nr /*AND l-od0.pos = 0*/ NO-LOCK. 
    RUN put-string(STRING(l-od0.pr-nr)).
  END. 
 
  ELSE IF paramnr = 661            /* Credit Term */  THEN 
    RUN put-string(STRING(fa-ordheader.credit-term)).
 
  ELSE IF paramnr = 672           /* Order DATE */  THEN 
    RUN put-string(STRING(fa-ordheader.order-date)).
 
  ELSE IF paramnr = 655           /* Delivery DATE */  THEN 
    RUN put-string(STRING(fa-ordheader.expected-delivery)).
 
  ELSE IF paramnr = 673      /* PO NO */ THEN 
  DO: 
  DEF VAR docu-str AS CHAR NO-UNDO. 
    docu-str = docu-nr.
    IF fa-ordheader.created-time > 0  THEN docu-str = docu-str + "*" .
    RUN put-string(STRING(docu-str)).
  END. 
 
  ELSE IF paramnr = 727           /* Payment DATE */  THEN 
      RUN put-string(STRING(fa-ordheader.paymentdate)).
 
  ELSE IF paramnr = 1088            /* Department */  THEN 
  DO: 
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
      AND parameters.section = "Name" 
      AND INTEGER(parameters.varname) = fa-ordheader.dept-nr 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE parameters THEN RUN put-string(TRIM(parameters.vstring)).
  END. 
 
  ELSE IF paramnr = 1107           /* Currency */  THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = fa-ordheader.currency 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
      RUN put-string(STRING(waehrung.wabkurz)).
  END. 
 
  ELSE IF paramnr = 2302 THEN /* po-line start */ status-code = 6. 
  ELSE IF paramnr = 2303 THEN /* po-line END   */ status-code = 7. 
 
  ELSE IF paramnr = 633            /* CURRENT loop NO */  THEN 
  DO: 
    output-list.str = output-list.str + STRING(currloop, ">>9").
    /*MT PUT STREAM s1 currloop FORMAT ">>9". */
    curr-pos = curr-pos + 3. 
  END. 
 
  ELSE IF paramnr = 2320            /* delivery unit */  THEN 
  DO: 
    /*PUT STREAM s1 l-artikel.traubensort FORMAT "x(5)". 
    curr-pos = curr-pos + 5. */
  END. 
 
  ELSE IF paramnr = 675            /* total quantity */  THEN 
  DO: 
    output-list.str = output-list.str + STRING(tot-qty, "->,>>9.9").
    /*MT PUT STREAM s1 tot-qty FORMAT "->,>>9.9". */
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 692            /* Order Instruction */  THEN 
  DO: 
    RUN print-instruction. 
  END. 

  ELSE IF paramnr = 1004      /* order name */ AND AVAILABLE fa-ordheader
    THEN RUN put-string(TRIM(fa-ordheader.order-name)).

  ELSE IF paramnr = 1005      /* order item's remark */ THEN 
  DO i = 1 TO remark-len: 
    IF AVAILABLE op-list THEN
    DO:
        IF LENGTH(op-list.remark) GE i THEN 
            output-list.str = output-list.str + STRING(SUBSTR(op-list.remark, i, 1), "x(1)").
          /*MT PUT STREAM s1 SUBSTR(op-list.remark, i, 1) FORMAT "x(1)". */
        ELSE output-list.str = output-list.str + STRING(" ", "x(1)") 
            /*MT PUT STREAM s1 " " FORMAT "x(1)". */ .
        curr-pos = curr-pos + 1. 
    END.
  END.

  ELSE IF paramnr = 2304            /*  Artnr */  THEN 
  DO: 
    output-list.str = output-list.str + STRING(mathis.nr, "9999999").
    /*MT PUT STREAM s1 mathis.nr FORMAT "9999999". */
    curr-pos = curr-pos + 7. 
  END. 
  ELSE IF paramnr = 2305            /* qty */  THEN 
  DO: 
    IF AVAILABLE op-list THEN
    DO:
        IF op-list.anzahl GE 10000 OR (- op-list.anzahl GE 10000) THEN 
            output-list.str = output-list.str + STRING(op-list.anzahl, "->>>,>>9").
          /*MT PUT STREAM s1 op-list.anzahl FORMAT "->>>,>>9". */
        ELSE IF op-list.anzahl GE 1000 OR (- op-list.anzahl GE 1000) THEN 
        DO: 
          IF op-list.anzahl GE 0 THEN 
              output-list.str = output-list.str + STRING(op-list.anzahl, ">,>>9.99").
              /*MT PUT STREAM s1 op-list.anzahl FORMAT ">,>>9.99". */
          ELSE output-list.str = output-list.str + STRING(op-list.anzahl, "->,>>9.9"). 
              /*MT PUT STREAM s1 op-list.anzahl FORMAT "->,>>9.9". */ .
        END. 
        ELSE 
        DO: 
          IF LENGTH(STRING(op-list.anzahl - ROUND(op-list.anzahl - 0.5, 0))) GT 3 
            THEN output-list.str = output-list.str + STRING(op-list.anzahl, "->>9.999").
              /*MT PUT STREAM s1 op-list.anzahl FORMAT "->>9.999". */
          ELSE output-list.str = output-list.str + STRING(op-list.anzahl, "->>9.99 ").
              /*MT PUT STREAM s1 op-list.anzahl FORMAT "->>9.99 ". */
        END. 
        curr-pos = curr-pos + 8. 
    END.
  END. 
  ELSE IF paramnr = 2306            /* Description */  THEN 
  DO: 
    pos-bez = curr-pos.
    IF AVAILABLE op-list THEN
    DO: 
        curr-bez = op-list.bezeich. 
        IF NOT op-list.bez-aend THEN 
        DO: 
          DO i = 1 TO bez-len: 
            IF LENGTH(curr-bez) GE i THEN 
                output-list.str = output-list.str + STRING(SUBSTR(curr-bez, i, 1), "x(1)").
              /*MT PUT STREAM s1 SUBSTR(curr-bez, i, 1) FORMAT "x(1)". */
            ELSE output-list.str = output-list.str + STRING(" ", "x(1)").
                /*MT PUT STREAM s1 " " FORMAT "x(1)". */
          END. 
          curr-pos = curr-pos + bez-len. 
        END. 
        ELSE RUN print-bezeich(curr-bez). 
    END.
  END. 
 
  ELSE IF paramnr = 710            /* AcctNo */  THEN 
  DO: 
  DEFINE VARIABLE c AS CHAR. 
  DEFINE VARIABLE len AS INTEGER. 
    IF AVAILABLE op-list THEN
    DO:
        RUN convert-fibu(op-list.konto, OUTPUT c). 
    END.
    len = LENGTH(c). 
    DO i = 1 TO len: 
        output-list.str = output-list.str + STRING(SUBSTR(c, i, 1), "x(1)").
        /*MT PUT STREAM s1 SUBSTR(c, i, 1) FORMAT "x(1)". */
    END. 
    curr-pos = curr-pos + len. 
  END. 
 
  ELSE IF paramnr = 777            /* Disc */  THEN 
  DO: 
    IF AVAILABLE op-list THEN
    DO:
        IF disc2-flag = NO THEN 
            output-list.str = output-list.str + STRING(op-list.disc, ">9.99").
          /*MT PUT STREAM s1 op-list.disc FORMAT ">9.99". */
        ELSE output-list.str = output-list.str + STRING(op-list.disc2, ">9.99").
            /*MT PUT STREAM s1 op-list.disc2 FORMAT ">9.99". */
        curr-pos = curr-pos + 5. 
    END.
  END. 
 
  ELSE IF paramnr = 779            /* Unit Price before discount */  THEN 
  DO: 
    IF AVAILABLE op-list THEN
    DO:
        IF NOT long-digit THEN 
        DO: 
          IF op-list.epreis GE 10000000 THEN 
              output-list.str = output-list.str + STRING(op-list.epreis0, "->>,>>>,>>>,>>>,>>9").  /*" >>>,>>>,>>9"*/ /*gerald tambah digit 1D9FD1*/
              /*MT PUT STREAM s1 op-list.epreis0 FORMAT " >>>,>>>,>>9". */
          ELSE 
          DO: 
              output-list.str = output-list.str + STRING(op-list.epreis0, "->>>,>>>,>>>,>>9.99").  /*">,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
              /*MT PUT STREAM s1 op-list.epreis0 FORMAT ">,>>>,>>9.99". */ .
          END. 
          curr-pos = curr-pos + 12. 
        END. 
        ELSE 
        DO: 
            output-list.str = output-list.str + STRING(op-list.epreis0, "->>,>>>,>>>,>>>,>>9").  /*">,>>>,>>>,>>9"*/ /*gerald tambah digit 1D9FD1*/
            /*MT PUT STREAM s1 op-list.epreis0 FORMAT ">,>>>,>>>,>>9". */
            curr-pos = curr-pos + 13. 
        END. 
    END.
  END. 
 
  ELSE IF paramnr = 780            /* VAT */  THEN 
  DO: 
      IF AVAILABLE op-list THEN
      output-list.str = output-list.str + STRING(op-list.vat, ">9.99").
      /*MT PUT STREAM s1 op-list.vat FORMAT ">9.99". */
      curr-pos = curr-pos + 5. 
  END. 
 
  ELSE IF paramnr = 2307            /* Unit Price */  THEN 
  DO: 
    IF AVAILABLE op-list THEN
    DO:
        IF NOT long-digit THEN 
        DO: 
          IF op-list.epreis GE 10000000 THEN
              output-list.str = output-list.str + STRING(op-list.epreis, "->>,>>>,>>>,>>>,>>9"). /*"   >>>,>>>,>>9"*/ /*gerald tambah digit 1D9FD1*/
              /*MT PUT STREAM s1 op-list.epreis FORMAT "   >>>,>>>,>>9". */
          ELSE 
          DO: 
              output-list.str = output-list.str + STRING(op-list.epreis, "->>>,>>>,>>>,>>9.99"). /*">>>,>>>,>>9.99"*/ /*gerald tambah digit 1D9FD1*/
              /*MT PUT STREAM s1 op-list.epreis FORMAT ">>>,>>>,>>9.99". */
          END. 
          curr-pos = curr-pos + 12. 
        END. 
        ELSE 
        DO: 
            output-list.str = output-list.str + STRING(op-list.epreis, "->>,>>>,>>>,>>>,>>9"). /*">>>,>>>,>>9.99*/ /*gerald tambah digit 1D9FD1*/
            /*MT PUT STREAM s1 op-list.epreis FORMAT ">,>>>,>>>,>>9". */
            curr-pos = curr-pos + 13. 
        END. 
    END.
  END. 
 
  ELSE IF paramnr = 2308            /* Amount */  THEN 
  DO: 
    IF AVAILABLE op-list THEN
    DO:
        IF NOT long-digit THEN 
        DO: 
          IF price-decimal = 0 AND NOT foreign-currency THEN 
              output-list.str = output-list.str + STRING(op-list.warenwert, "->,>>>,>>>,>>>,>>9").
              /*MT PUT STREAM s1 op-list.warenwert FORMAT "->,>>>,>>>,>>>,>>9". */
          ELSE IF price-decimal = 2 OR foreign-currency THEN 
              output-list.str = output-list.str + STRING(op-list.warenwert, "->,>>>,>>>,>>>,>>9.99").
              /*MT PUT STREAM s1 op-list.warenwert FORMAT "->,>>>,>>>,>>>,>>9.99". */ .
            curr-pos = curr-pos + 11. 
        END. 
        ELSE 
        DO: 
            output-list.str = output-list.str + STRING(op-list.warenwert, "->,>>>,>>>,>>>,>>9").
            /*MT PUT STREAM s1 op-list.warenwert FORMAT "->,>>>,>>>,>>>,>>9". */
            curr-pos = curr-pos + 14. 
        END. 
    END.
  END. 
 
  ELSE IF paramnr = 2316            /* Balance ON the CURRENT bill-line */ 
  THEN DO: 
     
    IF NOT long-digit THEN 
    DO: 
      IF price-decimal = 0 AND NOT foreign-currency THEN 
          output-list.str = output-list.str + STRING(bl-balance, "->,>>>,>>>,>>>,>>9").
          /*MT PUT STREAM s1 bl-balance FORMAT "->,>>>,>>>,>>>,>>9"*/
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
          output-list.str = output-list.str + STRING(bl-balance, "->,>>>,>>>,>>>,>>9.99").
          /*MT PUT STREAM s1 bl-balance FORMAT "->,>>>,>>>,>>>,>>9.99"*/ .
      curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
      output-list.str = output-list.str + STRING(bl-balance, "->,>>>,>>>,>>>,>>9").
      /*MT PUT STREAM s1 bl-balance FORMAT "->,>>>,>>>,>>>,>>9"*/
      curr-pos = curr-pos + 14. 
    END. 
  END. 
 
  ELSE IF paramnr = 674      /* Total balance */ THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
     IF price-decimal = 0 AND NOT foreign-currency THEN 
         output-list.str = output-list.str + STRING(saldo, "->>,>>>,>>9").
         /*MT PUT STREAM s1 saldo FORMAT "->>,>>>,>>9". */
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
          output-list.str = output-list.str + STRING(saldo, "->>>,>>9.99").
          /*MT PUT STREAM s1 saldo FORMAT "->>>,>>9.99". */
      curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
        output-list.str = output-list.str + STRING(saldo, "->,>>>,>>>,>>9").
        /*MT PUT STREAM s1 saldo FORMAT "->,>>>,>>>,>>9". */
        curr-pos = curr-pos + 14. 
    END. 
  END. 
END. 
 
PROCEDURE put-string: 
DEFINE INPUT PARAMETER STR AS CHAR. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
  len = LENGTH(STR). 
  DO i = 1 TO len: 
    IF headloop = 0 THEN 
        output-list.str = output-list.str + STRING(SUBSTR(STR, i, 1), "x(1)").
        /*MT PUT STREAM s1 SUBSTR(STR, i, 1) FORMAT "x(1)". */
    ELSE IF headloop = 3 THEN 
    DO:
        IF AVAILABLE header-list THEN
        header-list.texte = header-list.texte + SUBSTR(STR, i, 1). 
    END.
  END. 
  curr-pos = curr-pos + len. 
END. 
 
PROCEDURE print-bezeich: 
DEFINE INPUT PARAMETER curr-bez AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  curr-pos = curr-pos + bez-len. 
  DO i = 1 TO bez-len: 
    IF SUBSTR(curr-bez,i,2) = "\" + chr(10) THEN 
    DO: 
      i = i + 1. 
      remain-bez = SUBSTR(curr-bez, (i + 1), LENGTH(curr-bez) - i). 
      DO j = 1 TO (bez-len - i + 2):
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      END. 
      RETURN. 
    END. 
    ELSE IF i = LENGTH(curr-bez) THEN 
    DO: 
        output-list.str = output-list.str + STRING(SUBSTR(curr-bez, i, 1), "x(1)").
        /*MT PUT STREAM s1 SUBSTR(curr-bez, i, 1) FORMAT "x(1)". */
        DO j = 1 TO (bez-len - i): 
            output-list.str = output-list.str + STRING(" ", "x(1)").
            /*MT PUT STREAM s1 " " FORMAT "x(1)". */
        END. 
        RETURN. 
    END. 
    ELSE output-list.str = output-list.str + STRING(SUBSTR(curr-bez, i, 1), "x(1)").
         /*MT PUT STREAM s1 SUBSTR(curr-bez, i, 1) FORMAT "x(1)". */ .
  END. 
  remain-bez = SUBSTR(curr-bez, i, LENGTH(curr-bez)). 
END. 
 
PROCEDURE print-bezeich1: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  DO i = 1 TO pos-bez - 1: 
      output-list.str = output-list.str + STRING(" ", "x(1)").
      /*MT PUT STREAM s1 " " FORMAT "x(1)". */
  END. 
  DO i = 1 TO bez-len: 
    IF SUBSTR(remain-bez,i,2) = "\" + chr(10) THEN 
    DO: 
      i = i + 1. 
      remain-bez = SUBSTR(remain-bez, (i + 1), LENGTH(remain-bez) - i). 
      DO j = (bez-len - i) TO bez-len: 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      END. 
      RETURN. 
    END. 
    ELSE IF i = LENGTH(remain-bez) THEN 
    DO: 
      output-list.str = output-list.str + STRING(SUBSTR(remain-bez, i, 1), "x(1)").
      /*MT PUT STREAM s1 SUBSTR(remain-bez, i, 1) FORMAT "x(1)". */
      DO j = (bez-len - i) TO bez-len: 
        output-list.str = output-list.str + STRING(" ", "x(1)").
        /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      END. 
      remain-bez = "". 
      RETURN. 
    END. 
    ELSE output-list.str = output-list.str + STRING(SUBSTR(remain-bez, i, 1), "x(1)").
         /*MT PUT STREAM s1 SUBSTR(remain-bez, i, 1) FORMAT "x(1)". */ .
  END. 
  remain-bez = SUBSTR(remain-bez, i, LENGTH(remain-bez)). 
END. 
 
PROCEDURE print-instruction: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE ind AS INTEGER. 
  IF ord-len GT 0 THEN 
  DO: 
    RUN print-instruct1. 
    RETURN. 
  END. 
 
  IF pos-bez = 0 THEN 
  DO: 
    output-list.str = output-list.str + STRING("").
    output-list.pos = 20.
    /*MT PUT STREAM s1 "" AT 20. */
    ind = 0. 
    DO i = 1 TO LENGTH(fa-ordheader.order-desc): 
      ind = ind + 1. 
      IF ind = 57 THEN 
      DO: 
        output-list.str = output-list.str + STRING("").
        output-list.pos = 20.
        /*MT PUT STREAM s1 SKIP "" AT 20. */
        ind = 1. 
        curr-line = curr-line + 1.
      END. 
      IF SUBSTR(fa-ordheader.order-desc,i,2) = "\" + chr(10) THEN 
      DO: 
        output-list.str = output-list.str + STRING("").
        output-list.pos = 20.
        /*MT PUT STREAM s1 SKIP "" AT 20. */
        curr-line = curr-line + 1.
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(fa-ordheader.order-desc,i,1) = chr(10) THEN 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      ELSE output-list.str = output-list.str + STRING(SUBSTR(fa-ordheader.order-desc, i, 1), "x(1)").
           /*MT PUT STREAM s1 SUBSTR(fa-ordheader.order-desc, i, 1) FORMAT "x(1)". */ .
    END. 
  END. 
  ELSE 
  DO: 
    output-list.str = output-list.str + STRING("").
    CREATE output-list.
    /*MT PUT STREAM s1 "" SKIP. */
    curr-line = curr-line + 1.
    DO j = 1 TO (pos-bez - 1): 
      output-list.str = output-list.str + STRING(" ", "x(1)").
      /*MT PUT STREAM s1 " " FORMAT "x(1)". */
    END. 
    ind = 0. 
    DO i = 1 TO LENGTH(fa-ordheader.order-desc): 
      ind = ind + 1. 
      IF ind = (bez-len + 1) THEN 
      DO: 
        output-list.str = output-list.str + STRING("").
        CREATE output-list.
        /*MT PUT STREAM s1 "" SKIP. */
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-bez - 1): 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
        END. 
        ind = 1. 
      END. 
      IF SUBSTR(fa-ordheader.order-desc,i,2) = "\" + chr(10) THEN 
      DO: 
        output-list.str = output-list.str + STRING("").
        CREATE output-list.
        /*MT PUT STREAM s1 "" SKIP. */
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-bez - 1): 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
        END. 
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(fa-ordheader.order-desc,i,1) = chr(10) THEN 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      ELSE output-list.str = output-list.str + STRING(SUBSTR(fa-ordheader.order-desc, i, 1), "x(1)"). 
           /*MT PUT STREAM s1 SUBSTR(fa-ordheader.order-desc, i, 1) FORMAT "x(1)". */ .
    END. 
  END. 
  output-list.str = output-list.str + STRING("").
  CREATE output-list.
  /*MT PUT STREAM s1 ""SKIP. */
  curr-line = curr-line + 1.
  curr-pos = 1. 
END. 
 
PROCEDURE print-instruct1: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE ind AS INTEGER. 
DEFINE VARIABLE s AS CHAR FORMAT "x(40)". 
  IF pos-ord = 0 THEN 
  DO: 
    IF ord-len GE 75 THEN 
    DO:
        output-list.str = output-list.str + STRING("").
        output-list.pos = 5.
        /*MT PUT STREAM s1 SKIP "" AT 5. */ .
    END.
    ELSE IF ord-len GE 60 THEN 
    DO:
        output-list.str = output-list.str + STRING("").
        output-list.pos = 10.
        /*MT PUT STREAM s1 SKIP "" AT 10. */ .
    END.
    ELSE IF ord-len GE 55 THEN 
    DO:
        output-list.str = output-list.str + STRING("").
        output-list.pos = 15.
        /*MT PUT STREAM s1 SKIP "" AT 15. */ .
    END.
    ELSE
    DO:
        output-list.str = output-list.str + STRING("").
        output-list.pos = 20.
        /*MT PUT STREAM s1 SKIP "" AT 20. */ .
    END.
    ind = 0. 
    DO i = 1 TO LENGTH(fa-ordheader.order-desc): 
      ind = ind + 1. 
      IF ind GT ord-len AND SUBSTR(fa-ordheader.order-desc,i,1) = " " THEN 
      DO: 
        IF ord-len GE 80 THEN 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 5.
            /*MT PUT STREAM s1 SKIP "" AT 5. */ .
        END.
        ELSE IF ord-len GE 60 THEN 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 10.
            /*MT PUT STREAM s1 SKIP "" AT 10. */ .
        END.
        ELSE IF ord-len GE 55 THEN 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 15.
            /*MT PUT STREAM s1 SKIP "" AT 15. */ .
        END.
        ELSE 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 20.
            /*MT PUT STREAM s1 SKIP "" AT 20. */ .
        END.
        ind = 1. 
      END. 
      ELSE IF SUBSTR(fa-ordheader.order-desc,i,2) = "\" + chr(10) THEN 
      DO: 
        IF ord-len GE 80 THEN 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 5.
            /*MT PUT STREAM s1 SKIP "" AT 5. */ .
        END.
        ELSE IF ord-len GE 60 THEN 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 10.
            /*MT PUT STREAM s1 SKIP "" AT 10. */ .
        END.
        ELSE IF ord-len GE 55 THEN 
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 15.
            /*MT PUT STREAM s1 SKIP "" AT 15. */ .
        END.
        ELSE
        DO:
            output-list.str = output-list.str + STRING("").
            output-list.pos = 20.
            /*MT PUT STREAM s1 SKIP "" AT 20. */ .
        END.
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(fa-ordheader.order-desc,i,1) = chr(10) THEN 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      ELSE output-list.str = output-list.str + STRING(SUBSTR(fa-ordheader.order-desc, i, 1), "x(1)").
           /*MT PUT STREAM s1 SUBSTR(fa-ordheader.order-desc, i, 1) FORMAT "x(1)". */ .
    END. 
  END. 
  ELSE 
  DO: 
    output-list.str = output-list.str + STRING("").
    CREATE output-list.
    /*MT PUT STREAM s1 "" SKIP. */
    curr-line = curr-line + 1.
    DO j = 1 TO (pos-ord - 1): 
      output-list.str = output-list.str + STRING(" ", "x(1)").
      /*MT PUT STREAM s1 " " FORMAT "x(1)". */
    END. 
    ind = 0. 
    DO i = 1 TO LENGTH(fa-ordheader.order-desc): 
      ind = ind + 1. 
      IF ind GT ord-len AND SUBSTR(fa-ordheader.order-desc,i,1) = " " THEN 
      DO: 
        output-list.str = output-list.str + STRING("").
        CREATE output-list.
        /*MT PUT STREAM s1 "" SKIP. */
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-ord - 1): 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
        END. 
        ind = 1. 
      END. 
      ELSE IF SUBSTR(fa-ordheader.order-desc,i,2) = "\" + chr(10) THEN 
      DO: 
        output-list.str = output-list.str + STRING("").
        CREATE output-list.
        /*MT PUT STREAM s1 "" SKIP. */
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-ord - 1): 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
        END. 
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(fa-ordheader.order-desc,i,1) = chr(10) THEN 
          output-list.str = output-list.str + STRING(" ", "x(1)").
          /*MT PUT STREAM s1 " " FORMAT "x(1)". */
      ELSE output-list.str = output-list.str + STRING(SUBSTR(fa-ordheader.order-desc, i, 1), "x(1)").
           /*MT PUT STREAM s1 SUBSTR(fa-ordheader.order-desc, i, 1) FORMAT "x(1)". */ .
    END. 
  END. 
  output-list.str = output-list.str + STRING("").
  CREATE output-list.
  /*MT PUT STREAM s1 ""SKIP. */
  curr-line = curr-line + 1.
  curr-pos = 1. 
END. 
 
PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO LENGTH(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 
 
