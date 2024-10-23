DEFINE TEMP-TABLE output-list
    FIELD str        AS CHARACTER
    FIELD pos        AS INT.

DEFINE WORKFILE op-list 
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
 
DEFINE WORKFILE brief-list 
  FIELD b-text      AS CHAR. 
 
DEFINE WORKFILE htp-list 
  FIELD paramnr     AS INTEGER 
  FIELD fchar       AS CHAR. 

DEFINE WORKFILE loop-list 
  FIELD texte       AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE loop1-list 
  FIELD texte       AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE header-list 
  FIELD texte       AS CHAR FORMAT "x(132)". 

DEFINE INPUT  PARAMETER briefnr         AS INTEGER. 
DEFINE INPUT  PARAMETER printnr         AS INTEGER. 
DEFINE INPUT  PARAMETER docu-nr         AS CHAR. 
DEFINE OUTPUT PARAMETER outfile         AS CHAR FORMAT "x(60)". 
DEFINE OUTPUT PARAMETER printer-pglen   AS INT.
DEFINE OUTPUT PARAMETER err-code        AS INT INIT 0.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE f-page           AS LOGICAL INITIAL YES. 
DEFINE VARIABLE foot-text1       AS CHAR. 
DEFINE VARIABLE foot-char2       AS CHAR. 
DEFINE VARIABLE foreign-currency AS LOGICAL INITIAL NO. 

DEFINE VARIABLE currloop        AS INTEGER. 
DEFINE VARIABLE betrag          AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE saldo           AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99". 
DEFINE VARIABLE bl-balance      AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99" INITIAL 0. 
DEFINE VARIABLE tot-qty         AS DECIMAL FORMAT "->>>,>>9.99" INITIAL 0. /* malik A6E20A */ 
 
DEFINE VARIABLE pos-bez    AS INTEGER INITIAL 0. 
DEFINE VARIABLE bez-len    AS INTEGER INITIAL 35. 
DEFINE VARIABLE remark-len AS INTEGER INITIAL 24.
DEFINE VARIABLE pos-ord    AS INTEGER INITIAL 0. 
DEFINE VARIABLE ord-len    AS INTEGER INITIAL 35. 
DEFINE VARIABLE remain-bez AS CHAR. 
 
DEFINE VARIABLE disc2-flag AS LOGICAL INITIAL NO. 
 
DEFINE VARIABLE pr        AS CHAR FORMAT "x(16)". 
DEFINE VARIABLE f-lmargin AS LOGICAL INITIAL NO. 
DEFINE VARIABLE headloop  AS INTEGER INITIAL 0. 
DEFINE VARIABLE blloop    AS INTEGER INITIAL 0. 
DEFINE VARIABLE lmargin   AS INTEGER INITIAL 1. 
DEFINE VARIABLE nskip     AS INTEGER INITIAL 1. 
DEFINE VARIABLE ntab      AS INTEGER INITIAL 1. 
DEFINE VARIABLE n         AS INTEGER. 
DEFINE VARIABLE curr-pos  AS INTEGER. 
DEFINE VARIABLE curr-line AS INTEGER. 
DEFINE VARIABLE curr-page AS INTEGER. 

DEFINE VARIABLE buttom-line   AS INTEGER. 
DEFINE VARIABLE keychar       AS CHAR. 
DEFINE VARIABLE price-decimal AS INTEGER. 
 
DEFINE VARIABLE globaldisc    AS DECIMAL NO-UNDO.

DEFINE VARIABLE long-digit AS LOGICAL. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 


/*************** MAIN ***************/
FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
 
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr AND l-orderhdr.lief-nr > 0 
  NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-orderhdr THEN
FIND FIRST l-orderhdr WHERE l-orderhdr.docu-nr = docu-nr AND l-orderhdr.lief-nr = 0 
  NO-LOCK NO-ERROR.
FIND FIRST l-order WHERE l-order.lief-nr = l-orderhdr.lief-nr 
  AND l-order.docu-nr = docu-nr AND l-order.pos = 0 NO-LOCK NO-ERROR.

IF NOT AVAILABLE l-order THEN
DO:
  err-code = 1.
  /*MTHIDE MESSAGE NO-PAUSE.
  MESSAGE "l-order record not found. Printing process stopped."
    VIEW-AS ALERT-BOX INFORMATION.*/
  RETURN.
END.
 
ASSIGN
    pr         = l-order.lief-fax[1]
    globaldisc = l-order.warenwert
. 
 
FIND FIRST waehrung WHERE waehrung.waehrungsnr = l-orderhdr.angebot-lief[3] 
  NO-LOCK NO-ERROR. 
IF AVAILABLE waehrung THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  IF htparam.fchar NE "" AND (htparam.fchar NE waehrung.wabkurz) THEN 
    foreign-currency = YES. 
END. 
 
FIND FIRST l-lieferant WHERE l-lieferant.lief-nr 
  = l-orderhdr.lief-nr NO-LOCK NO-ERROR. 
FIND FIRST gl-department WHERE gl-department.nr = l-orderhdr.angebot-lief[1] 
  NO-LOCK NO-ERROR. 
 
IF printnr = 0 THEN outfile = "\vhp-letter.rtf". 
ELSE DO: 
  FIND FIRST PRINTER WHERE printer.nr = printnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE PRINTER THEN 
  DO: 
    err-code = 2.
    /*MThide MESSAGE NO-PAUSE. 
    MESSAGE "Printer not yet selected" VIEW-AS ALERT-BOX INFORMATION.*/
    RETURN. 
  END. 
  ELSE outfile = printer.path. 

END. 
/*MTIF f-page THEN OUTPUT STREAM s1 TO value(outfile) paged 
   page-size value(printer.pglen) UNBUFFERED. 
ELSE OUTPUT STREAM s1 TO value(outfile) UNBUFFERED.*/
printer-pglen = printer.pglen.
RUN fill-list. 
 
curr-line = 1. 
curr-page = 1. 

CREATE output-list.
FOR EACH brief-list:
  IF curr-line GT printer.pglen THEN 
  DO: 
    curr-page = curr-page + 1. 
    curr-line = 1. 
    RUN do-billhead. 
  END. 
  curr-pos = 1. 
  RUN analyse-text. 
 
  /* DISP headloop briefzei.texte FORMAT "x(60)". */ 
 
  IF blloop = 0  AND headloop = 0 THEN 
  DO: 
    IF f-lmargin THEN DO n = 1 TO lmargin: 
      RUN put-string(" "). 
    END. 
    RUN build-text-line (brief-list.b-text).
    /*MTPUT STREAM s1 "" SKIP.*/
    ASSIGN output-list.str = output-list.str + STRING(" ").
    CREATE output-list.
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
 
/*MTOUTPUT STREAM s1 CLOSE.*/
 
FIND FIRST l-order WHERE l-order.lief-nr = l-orderhdr.lief-nr 
  AND l-order.docu-nr = docu-nr AND l-order.pos = 0 EXCLUSIVE-LOCK. 
l-order.gedruckt = TODAY. 
l-order.zeit = TIME. 
FIND CURRENT l-order NO-LOCK. 


/*************** PROCEDURES ***************/
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
  CREATE htp-list. 
  ASSIGN
    htp-list.paramnr = 9990
    htp-list.fchar = keychar + "Globdisc".
  CREATE htp-list. 
  ASSIGN
    htp-list.paramnr = 9989
    htp-list.fchar = keychar + "AfterDisc".

  CREATE htp-list. /*ITA 07Sept 2016 Keyword Created BY*/
  ASSIGN
    htp-list.paramnr = 9991
    htp-list.fchar = keychar + "createdby".

  CREATE htp-list. /*Alder 23/04/2024 9C78B3 Order Type*/
  ASSIGN
    htp-list.paramnr = 9992
    htp-list.fchar = keychar + "orderType".

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
 
  FOR EACH l-order WHERE l-order.docu-nr = docu-nr 
    AND l-order.loeschflag LE 1 AND l-order.pos GT 0 NO-LOCK 
    /*MT 19/03/13
    BY l-order.betriebsnr DESCENDING BY l-order.pos DESCENDING
    BY SUBSTR(l-order.stornogrund,13,LENGTH(l-order.stornogrund))*/,
    FIRST l-art WHERE l-art.artnr = l-order.artnr NO-LOCK BY l-art.bezeich: /*SIS 22-03-13*/
    create-it = NO. 
    bez-aend = NO.
    curr-bez = l-art.bezeich. 

    disc = 0. 
    disc2 = 0. 
    IF l-order.quality NE "" THEN 
    DO: 
      disc = INTEGER(SUBSTR(l-order.quality,1,2)) 
        + INTEGER(SUBSTR(l-order.quality,4,2)) * 0.01. 
      /*IF LENGTH(l-order.quality) GT 12 THEN 
      disc2 = INTEGER(SUBSTR(l-order.quality,13,2)) 
        + INTEGER(SUBSTR(l-order.quality,16,2)) * 0.01. */
    END. 
 
    IF l-art.jahrgang = 0 OR LENGTH(l-order.stornogrund) LE 12 THEN 
      FIND FIRST op-list WHERE op-list.artnr = l-order.artnr 
      AND op-list.epreis = l-order.einzelpreis 
      AND op-list.bezeich = l-art.bezeich 
      AND op-list.disc = disc AND op-list.disc2 = disc2 
      AND op-list.konto = l-order.stornogrund NO-ERROR. 
    ELSE 
    DO: 
      curr-bez = SUBSTR(l-order.stornogrund,13,LENGTH(l-order.stornogrund)). 
      create-it = YES. 
      bez-aend = YES.                                                     
    END.
    
    IF LENGTH(l-order.stornogrund) GT 12 THEN 
        curr-bez = SUBSTR(l-order.stornogrund, 13).
    
    IF NOT AVAILABLE op-list OR create-it THEN 
    DO: 
      vat = 0. 
      CREATE op-list.
      ASSIGN
        op-list.artnr = l-order.artnr
        op-list.bezeich = curr-bez
        op-list.bez-aend = bez-aend 
        op-list.epreis = l-order.einzelpreis 
        op-list.epreis0 = l-order.einzelpreis 
        op-list.konto = l-order.stornogrund
        op-list.remark = l-order.besteller
      . 
      IF l-order.quality NE "" THEN 
      DO: 
        
        vat = INTEGER(SUBSTR(l-order.quality,7,2)) + 
          INTEGER(SUBSTR(l-order.quality,10,2)) * 0.01. 
        
        op-list.disc = disc. 
        op-list.disc2 = disc2. 
        op-list.vat = vat. 
        disc = disc / 100. 
        disc2 = disc2 / 100. 
        vat = vat / 100. 
      END. 
    END. 
    op-list.epreis0 = l-order.einzelpreis / (1 - disc) / (1 - disc2) / (1 + vat). 
    op-list.anzahl = op-list.anzahl + l-order.anzahl. 
    op-list.warenwert = op-list.warenwert + l-order.warenwert. 
    op-list.warenwert0 = op-list.warenwert0 
        + l-order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat). 
    tot-qty = tot-qty + l-order.anzahl. 
  END. 
 
  currloop = 0. 
 
  FOR EACH op-list: 
    IF op-list.anzahl = 0 THEN delete op-list. 
  END. 
 
  FOR EACH op-list, 
    FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK: 
 
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
      /*MTPUT STREAM s1 "" SKIP.*/
      ASSIGN output-list.str = output-list.str + STRING("").
      CREATE output-list.
      curr-line = curr-line + 1. 
      DO WHILE remain-bez NE "": 
        RUN print-bezeich1. 
        /*MTPUT STREAM s1 "" SKIP.*/
        ASSIGN output-list.str = output-list.str + STRING("").
        CREATE output-list.
        curr-line = curr-line + 1. 
      END. 
    END. 
  END. 
  FOR EACH loop-list: 
    delete loop-list. 
  END. 
  blloop = 0. 
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
 
PROCEDURE print-billhead: 
  DEFINE VARIABLE i AS INTEGER. 
  FOR EACH header-list: 
    curr-pos = 1. 
    DO i = 1 TO LENGTH(header-list.texte): 
      /*MTPUT STREAM s1 SUBSTR(header-list.texte, i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(header-list.texte, i, 1), "x(1)").
    END. 
    /*MTPUT STREAM s1 "" SKIP.*/
    ASSIGN output-list.str = output-list.str + STRING("").
    CREATE output-list.
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
      
      /* item's remark */    
      ELSE IF htp-list.paramnr = 1005    
      THEN 
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
              /*MTPUT STREAM s1 "" SKIP.*/
              ASSIGN output-list.str = output-list.str + STRING("").
              CREATE output-list.
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
    /* DISP curr-pos ntab TRIM(curr-texte) FORMAT "x(30)". */ 
    IF curr-pos GT ntab THEN 
    DO: 
      /*MTPUT STREAM s1 "" SKIP.*/
      ASSIGN output-list.str = output-list.str + STRING("").
      CREATE output-list.
      curr-line = curr-line + 1. 
      curr-pos = 1. 
      DO n = 2 TO ntab: 
        /*MTRUN put-string(" ").*/
        ASSIGN output-list.str = output-list.str + STRING(" ").
        CREATE output-list.
      END. 
    END. 
    ELSE DO n = m TO ntab: 
      RUN put-string(" "). 
    END. 
    curr-pos = ntab. 
  END. 
  ELSE IF status-code = 2 AND headloop = 0 AND blloop = 0 THEN DO n = 1 TO nskip: 
    /*MTPUT STREAM s1 "" SKIP.*/
    ASSIGN output-list.str = output-list.str + STRING("").
    CREATE output-list.
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

/* Debugging (mulai dari sini untuk formatting) */
PROCEDURE decode-key1: 
  DEFINE INPUT PARAMETER paramnr AS INTEGER. 
  DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
  DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE n AS INTEGER. 
  DEFINE VARIABLE curr-bez AS CHAR. 
  FIND FIRST htparam WHERE paramnr = paramnr NO-LOCK. 
  /*MTIF paramnr = 601           /* page      */  THEN page STREAM s1. 
  ELSE*/
  /* page NO   */
  /*    THEN RUN put-string(STRING(page-number(s1))).  */ 
  IF paramnr = 602 THEN
  DO:
      RUN put-string(STRING(curr-page)).
  END.
      
  ELSE IF paramnr = 603 THEN /* Tabulator */ status-code = 1. 
  /* today's DATE */
  ELSE IF paramnr = 604 THEN
  DO:
        RUN put-string(STRING(today)).
  END.
      
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
    DEFINE buffer l-od0 FOR l-order. 
    FIND FIRST l-od0 WHERE l-od0.docu-nr = l-orderhdr.docu-nr 
      AND l-od0.lief-nr = l-orderhdr.lief-nr AND l-od0.pos = 0 NO-LOCK. 
    RUN put-string(STRING(l-od0.lief-fax[1])). 
  END. 
 
  ELSE IF paramnr = 661            /* Credit Term */  THEN 
    RUN put-string(STRING(l-orderhdr.angebot-lief[2])). 

  /*Alder 9C78B3 Start*/
  ELSE IF paramnr = 9992            /* Order Type */  THEN 
    RUN put-string(STRING(l-orderhdr.bestellart)). 
  /*Alder 9C78B3 End*/
 
  ELSE IF paramnr = 672           /* Order DATE */  THEN 
    RUN put-string(STRING(l-orderhdr.bestelldatum)). 
 
  ELSE IF paramnr = 655           /* Delivery DATE */  THEN 
    RUN put-string(STRING(l-orderhdr.lieferdatum)). 
 
  ELSE IF paramnr = 673      /* PO NO */ THEN 
  DO: 
  DEF VAR docu-str AS CHAR NO-UNDO. 
    docu-str = docu-nr. 
    /*IF AVAILABLE l-order AND l-order.zeit > 0 THEN docu-str = docu-str + "*". */
    
    IF AVAILABLE l-order THEN 
    DO:
      /*geral add queasy for reprint with parameter curr-status 8B3325*/
      IF l-order.zeit = 0 THEN 
      DO:
        FIND FIRST queasy WHERE queasy.KEY = 240 AND queasy.char1 = l-order.docu-nr NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
          docu-str = docu-str.
          
          CREATE queasy.
          ASSIGN 
             queasy.KEY     = 240
             queasy.char1   = docu-nr
             queasy.number1 = 1.
        END.
      END.
      ELSE
      DO:
        FIND FIRST queasy WHERE queasy.KEY = 240 AND queasy.char1 = l-order.docu-nr NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
          docu-str = docu-str.
          
          CREATE queasy.
          ASSIGN 
             queasy.KEY     = 240
             queasy.char1   = docu-nr
             queasy.number1 = 1.
        END.
        ELSE
        DO:
          queasy.number1 = queasy.number1 + 1.
          docu-str       = docu-str + "-REPRINT" + STRING(queasy.number1).
        END.
      END.
      /*end*/
    END.

    RUN put-string(STRING(docu-str)). 
  END. 
 
  ELSE IF paramnr = 727           /* Payment DATE */  THEN 
      RUN put-string(STRING(l-orderhdr.gefaxt)). 
 
  ELSE IF paramnr = 1088            /* Department */  THEN 
  DO: 
    FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
      AND parameters.section = "Name" 
      AND INTEGER(parameters.varname) = l-orderhdr.angebot-lief[1] 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE parameters THEN RUN put-string(TRIM(parameters.vstring)). 
  END. 
 
  ELSE IF paramnr = 1107           /* Currency */  THEN 
  DO: 
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = l-orderhdr.angebot-lief[3] 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE waehrung THEN 
      RUN put-string(STRING(waehrung.wabkurz)). 
  END. 
 
  ELSE IF paramnr = 2302 THEN /* po-line start */ status-code = 6. 
  ELSE IF paramnr = 2303 THEN /* po-line END   */ status-code = 7. 
 
  ELSE IF paramnr = 633            /* CURRENT loop NO */  THEN 
  DO: 
    /*MTPUT STREAM s1 currloop FORMAT ">>9".*/
    ASSIGN output-list.str = output-list.str + STRING(currloop, ">>9").
    curr-pos = curr-pos + 3. 
  END. 
 
  ELSE IF paramnr = 2320            /* delivery unit */  THEN 
  DO: 
    /*MTPUT STREAM s1 l-artikel.traubensort FORMAT "x(5)".*/
    ASSIGN output-list.str = output-list.str + STRING(l-artikel.traubensort, "x(5)").
    curr-pos = curr-pos + 5. 
  END. 
 
  ELSE IF paramnr = 675            /* total quantity */  THEN 
  DO: 
    /*MTPUT STREAM s1 tot-qty FORMAT "->,>>9.9".*/
    ASSIGN output-list.str = output-list.str + STRING(tot-qty, "->,>>9.99"). /* malik A6E20A  "->,>>9.9" to "->,>>9.99" */ 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 692            /* Order Instruction */  THEN 
  DO: 
    RUN print-instruction. 
  /*    PUT STREAM s1 l-orderhdr.lief-fax[3] FORMAT "x(24)" 
        curr-pos = curr-pos + 24. 
  */ 
  END. 

  ELSE IF paramnr = 1004      /* order name */ AND AVAILABLE l-orderhdr
    THEN RUN put-string(TRIM(l-orderhdr.lief-fax[2])). 

  /* order item's remark */ 
  ELSE IF paramnr = 1005      
  THEN 
  DO i = 1 TO remark-len: 
    IF LENGTH(op-list.remark) GE i THEN 
      /*MTPUT STREAM s1 SUBSTR(op-list.remark, i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(op-list.remark, i, 1), "x(1)").
    ELSE /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)")
    curr-pos = curr-pos + 1. 
  END.

  ELSE IF paramnr = 2304            /*  Artnr */  THEN 
  DO: 
    /*MTPUT STREAM s1 l-artikel.artnr FORMAT "9999999".*/
    ASSIGN output-list.str = output-list.str + STRING(l-artikel.artnr, "9999999")
    curr-pos = curr-pos + 7. 
  END. 
  ELSE IF paramnr = 2305            /* qty */  THEN 
  DO: 
    IF op-list.anzahl GE 10000 OR (- op-list.anzahl GE 10000) THEN 
      /*MTPUT STREAM s1 op-list.anzahl FORMAT "->>>,>>9".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.anzahl, "->>>,>>>,>>9.99")+ "      ". /* malik A6E20A "->>>,>>>,>>9" to "->>>,>>>,>>9.99" */ 
    ELSE IF op-list.anzahl GE 1000 OR (- op-list.anzahl GE 1000) THEN 
    DO: 
      IF op-list.anzahl GE 0 THEN /*MTPUT STREAM s1 op-list.anzahl FORMAT ">,>>9.99".*/
          ASSIGN output-list.str = output-list.str + "     "  + STRING(op-list.anzahl, ">>>,>>9.99")+ "      ". /* malik A6E20A ">>>,>>9.99" to  ">>>,>>9.99" */
      ELSE /*MTPUT STREAM s1 op-list.anzahl FORMAT "->,>>9.9".*/
          ASSIGN output-list.str = output-list.str + "     " + STRING(op-list.anzahl, "->>>,>>9.99")+ "      ". /* malik A6E20A "->>>,>>9.9" to "->>>,>>9.99" */
    END. 
    ELSE 
    DO: 
      IF LENGTH(STRING(op-list.anzahl - ROUND(op-list.anzahl - 0.5, 0))) GT 3 THEN 
          /*MTPUT STREAM s1 op-list.anzahl FORMAT "->>9.999".*/
          ASSIGN output-list.str = output-list.str + STRING(op-list.anzahl, "->>9.99")+ "  ". /* malik A6E20A "->>9.999" to "->>9.99" */ 
      ELSE /*MTPUT STREAM s1 op-list.anzahl FORMAT "->>9.99 ".*/
          ASSIGN output-list.str = output-list.str + STRING(op-list.anzahl, "->>>9.99 ")+ "  ". /* malik A6E20A "->>>9.99 " to  "->>>9.99 "*/
    END. 
    curr-pos = curr-pos + 8. 
  END. 
  ELSE IF paramnr = 2306            /* Description */  THEN 
  DO: 
    pos-bez = curr-pos. 
    curr-bez = op-list.bezeich. 
    IF NOT op-list.bez-aend THEN 
    DO: 
      DO i = 1 TO bez-len: 
        IF LENGTH(curr-bez) GE i THEN 
          /*MTPUT STREAM s1 SUBSTR(curr-bez, i, 1) FORMAT "x(1)".*/
            ASSIGN output-list.str = output-list.str + STRING(SUBSTR(curr-bez, i, 1), "x(1)").
        ELSE /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
            ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      END. 
      curr-pos = curr-pos + bez-len. 
    END. 
    ELSE RUN print-bezeich(curr-bez). 
  END. 
  ELSE IF paramnr = 9990 THEN
  DO:
    IF NOT long-digit THEN 
    DO: 
      IF price-decimal = 0 AND NOT foreign-currency THEN 
        ASSIGN output-list.str = output-list.str + STRING(globaldisc, "->>>,>>>,>>9.99"). /* malik A6E20A "->>>,>>>,>>9" to "->>>,>>>,>>9.99" */
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
        ASSIGN output-list.str = output-list.str + STRING(globaldisc, "->>>,>>9.99"). /* malik A6E20A "->>>,>>9.99" to "->>>,>>9.99" */
      curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(globaldisc, "->,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>9" to "->,>>>,>>>,>>9.99" */
      curr-pos = curr-pos + 14. 
    END.
  END.
  ELSE IF paramnr = 9991 THEN DO: /*ITA 07Sept 2016 created by*/
    RUN put-string(STRING(l-orderhdr.besteller)). 
  END.
  ELSE IF paramnr = 710            /* AcctNo */  THEN 
  DO: 
  DEFINE VARIABLE c AS CHAR. 
  DEFINE VARIABLE len AS INTEGER. 
    RUN convert-fibu(op-list.konto, OUTPUT c). 
    len = LENGTH(c). 
    DO i = 1 TO len: 
      /*MTPUT STREAM s1 SUBSTR(c, i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(c, i, 1), "x(1)").
    END. 
    curr-pos = curr-pos + len. 
  END. 
 
  ELSE IF paramnr = 777            /* Disc */  THEN 
  DO: 
    IF disc2-flag = NO THEN 
      /*MTPUT STREAM s1 op-list.disc FORMAT ">9.99".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.disc, ">9.99"). /* malik A6E20A ">9.99" to ">9.99" */
    ELSE /*MTPUT STREAM s1 op-list.disc2 FORMAT ">9.99".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.disc2, ">9.99"). /* malik A6E20A ">9.99" to ">9.99" */ 
    curr-pos = curr-pos + 5. 
  END. 
 
  ELSE IF paramnr = 779            /* Unit Price before discount */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      IF op-list.epreis GE 10000000 THEN 
        /*MTPUT STREAM s1 op-list.epreis0 FORMAT " >>>,>>>,>>9".*/
          ASSIGN output-list.str = output-list.str + STRING(op-list.epreis0, " >>,>>>,>>>,>>9.99"). /* malik A6E20A " >>,>>>,>>>,>>9" to " >>,>>>,>>>,>>9.99" */
      ELSE 
      DO: 
  /*
          IF LENGTH(STRING(op-list.epreis0 - ROUND(op-list.epreis0 - 0.5, 0))) 
            GT 3 THEN PUT STREAM s1 op-list.epreis0 FORMAT " >>>,>>9.999". 
          ELSE PUT STREAM s1 op-list.epreis0 FORMAT ">,>>>,>>9.99". 
  */
        /*MTPUT STREAM s1 op-list.epreis0 FORMAT ">,>>>,>>9.99".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.epreis0, ">>,>>>,>>>,>>9.99"). /* malik A6E20A ">>,>>>,>>>,>>9.99" to ">>,>>>,>>>,>>9.99" */
      END. 
      curr-pos = curr-pos + 12. 
    END. 
    ELSE 
    DO: 
      /*MTPUT STREAM s1 op-list.epreis0 FORMAT ">,>>>,>>>,>>9".*/
      ASSIGN output-list.str = output-list.str + STRING(op-list.epreis0, ">,>>>,>>9.99"). /* malik A6E20A ">,>>>,>>9.99" to ">,>>>,>>9.99" */
      curr-pos = curr-pos + 13. 
    END. 
  END. 
 
  ELSE IF paramnr = 780            /* VAT */  THEN 
  DO: 
    /*MTPUT STREAM s1 op-list.vat FORMAT ">9.99".*/
    ASSIGN output-list.str = output-list.str + STRING(op-list.vat, ">9.99"). /* malik A6E20A ">9.99" to ">9.99" */
    curr-pos = curr-pos + 5. 
  END. 
 
  ELSE IF paramnr = 2307            /* Unit Price */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      IF op-list.epreis GE 10000000000 THEN 
        /*MTPUT STREAM s1 op-list.epreis FORMAT " >>>,>>>,>>9".*/
          ASSIGN output-list.str = output-list.str + STRING(op-list.epreis, " >>>,>>>,>>>,>>9.99"). /* malik A6E20A " >>>,>>>,>>>,>>9" to " >>>,>>>,>>>,>>9.99" */
      ELSE 
      DO: 
  /*
          IF LENGTH(STRING(op-list.epreis - ROUND(op-list.epreis - 0.5, 0))) 
            GT 3 THEN PUT STREAM s1 op-list.epreis FORMAT " >>>,>>9.999". 
          ELSE PUT STREAM s1 op-list.epreis FORMAT ">,>>>,>>9.99". 
  */        
        /*MTPUT STREAM s1 op-list.epreis FORMAT ">,>>>,>>9.99".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.epreis, ">,>>>,>>>,>>9.99"). /* malik A6E20A ">,>>>,>>>,>>9.99" to ">,>>>,>>>,>>9.99" */  /*>,>>>,>>9.99 Modified By Gerald >,>>>,>>>,>>9*/
      END. 
      curr-pos = curr-pos + 12. 
    END. 
    ELSE 
    DO: 
      /*MTPUT STREAM s1 op-list.epreis FORMAT ">,>>>,>>>,>>9".*/
      ASSIGN output-list.str = output-list.str + STRING(op-list.epreis, ">,>>>,>>>,>>9.99"). /* malik A6E20A ">,>>>,>>>,>>9" to  ">,>>>,>>>,>>9.99" */ 
      curr-pos = curr-pos + 13. 
    END. 
  END. 
 
  ELSE IF paramnr = 2308            /* Amount */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      IF price-decimal = 0 AND NOT foreign-currency THEN 
        /*MTPUT STREAM s1 op-list.warenwert FORMAT "->>,>>>,>>9".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.warenwert, "->,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>9" to "->,>>>,>>>,>>9.99" */  /*"->>,>>>,>>9"*/
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
        /*MTPUT STREAM s1 op-list.warenwert FORMAT "->>>,>>9.99".*/
        ASSIGN output-list.str = output-list.str + STRING(op-list.warenwert, "->,>>>,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>>,>>9.99" to "->,>>>,>>>,>>>,>>9.99" */      /*"->>>,>>9.99""*/
        curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
      /*MTPUT STREAM s1 op-list.warenwert FORMAT "->,>>>,>>>,>>9".*/
      ASSIGN output-list.str = output-list.str + STRING(op-list.warenwert, "->,>>>,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>>,>>9" to "->,>>>,>>>,>>>,>>9.99" */   /*"->,>>>,>>>,>>9"*/
      curr-pos = curr-pos + 14. 
    END. 
  END. 
 
  ELSE IF paramnr = 2316            /* Balance ON the CURRENT bill-line */ 
  THEN DO: 
    IF NOT long-digit THEN 
    DO: 
      IF price-decimal = 0 AND NOT foreign-currency THEN 
      /*MTPUT STREAM s1 bl-balance FORMAT "->>,>>>,>>9".*/
          ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>,>>>,>>>,>>9.99"). /* malik A6E20A "->>,>>>,>>>,>>9" to "->>,>>>,>>>,>>9.99" */
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
      /*MTPUT STREAM s1 bl-balance FORMAT "->>>,>>9.99".*/
          ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>,>>>,>>9.99"). /* malik A6E20A "->>,>>>,>>9.99" to "->>,>>>,>>9.99" */
      curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
      /*MTPUT STREAM s1 bl-balance FORMAT "->,>>>,>>>,>>9".*/
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>9" to "->,>>>,>>>,>>9.99"*/
      curr-pos = curr-pos + 14. 
    END. 
  END. 
 
  ELSE IF paramnr = 674      /* Total balance */ THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
     IF price-decimal = 0 AND NOT foreign-currency THEN 
      /*MTPUT STREAM s1 saldo FORMAT "->>,>>>,>>9".*/
         ASSIGN output-list.str = output-list.str + STRING(saldo, "->,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>9" to "->,>>>,>>>,>>9.99" */ 
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
      /*MTPUT STREAM s1 saldo FORMAT "->>>,>>9.99".*/
          ASSIGN output-list.str = output-list.str + STRING(saldo, "->>>,>>9.99"). /* malik A6E20A "->>>,>>9.99" to "->>>,>>9.99" */ 
      curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
      /*MTPUT STREAM s1 saldo FORMAT "->,>>>,>>>,>>9".*/
      ASSIGN output-list.str = output-list.str + STRING(saldo, "->,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>9" to "->,>>>,>>>,>>9.99"*/ 
      curr-pos = curr-pos + 14. 
    END. 
  END. 

  ELSE IF paramnr = 9989      /* Total after disc */ THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
     IF price-decimal = 0 AND NOT foreign-currency THEN 
      /*MTPUT STREAM s1 saldo FORMAT "->>,>>>,>>9".*/
         ASSIGN output-list.str = output-list.str + STRING(saldo - globaldisc, "->>>,>>>,>>9.99"). /* malik A6E20A "->>>,>>>,>>9" to "->>>,>>>,>>9.99"*/
      ELSE IF price-decimal = 2 OR foreign-currency THEN 
      /*MTPUT STREAM s1 saldo FORMAT "->>>,>>9.99".*/
          ASSIGN output-list.str = output-list.str + STRING(saldo - globaldisc, "->>>,>>9.99"). /* malik A6E20A "->>>,>>9.99" to "->>>,>>9.99" */
      curr-pos = curr-pos + 11. 
    END. 
    ELSE 
    DO: 
      /*MTPUT STREAM s1 saldo FORMAT "->,>>>,>>>,>>9".*/
      ASSIGN output-list.str = output-list.str + STRING(saldo - globaldisc, "->,>>>,>>>,>>9.99"). /* malik A6E20A "->,>>>,>>>,>>9" to "->,>>>,>>>,>>9.99" */
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
    IF headloop = 0 THEN /*MTPUT STREAM s1 SUBSTR(STR, i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(STR, i, 1), "x(1)").
    ELSE IF headloop = 3 THEN 
      header-list.texte = header-list.texte + SUBSTR(STR, i, 1). 
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
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      END. 
      RETURN. 
    END. 
    ELSE IF i = LENGTH(curr-bez) THEN 
    DO: 
      /*MTPUT STREAM s1 SUBSTR(curr-bez, i, 1) FORMAT "x(1)".*/
      ASSIGN output-list.str = output-list.str + STRING(SUBSTR(curr-bez, i, 1), "x(1)").
      DO j = 1 TO (bez-len - i): 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      END. 
      RETURN. 
    END. 
    ELSE /*MTPUT STREAM s1 SUBSTR(curr-bez, i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(curr-bez, i, 1), "x(1)").
  END. 
  remain-bez = SUBSTR(curr-bez, i, LENGTH(curr-bez)). 
END. 
 
PROCEDURE print-bezeich1: 
  DEFINE VARIABLE i AS INTEGER. 
  DEFINE VARIABLE j AS INTEGER. 
  DO i = 1 TO pos-bez - 1: 
    /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
    ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
  END. 
  DO i = 1 TO bez-len: 
    IF SUBSTR(remain-bez,i,2) = "\" + chr(10) THEN 
    DO: 
      i = i + 1. 
      remain-bez = SUBSTR(remain-bez, (i + 1), LENGTH(remain-bez) - i). 
      DO j = (bez-len - i) TO bez-len: 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      END. 
      RETURN. 
    END. 
    ELSE IF i = LENGTH(remain-bez) THEN 
    DO: 
      /*MTPUT STREAM s1 SUBSTR(remain-bez, i, 1) FORMAT "x(1)".*/
      ASSIGN output-list.str = output-list.str + STRING(SUBSTR(remain-bez, i, 1), "x(1)").
      DO j = (bez-len - i) TO bez-len: 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      END. 
      remain-bez = "". 
      RETURN. 
    END. 
    ELSE /*MTPUT STREAM s1 SUBSTR(remain-bez, i, 1) FORMAT "x(1)". */
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(remain-bez, i, 1), "x(1)").
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
    /*MTPUT STREAM s1 "" AT 20.*/
    ASSIGN output-list.str = output-list.str + STRING("")
           output-list.pos = 20.
    ind = 0. 
    DO i = 1 TO LENGTH(l-orderhdr.lief-fax[3]): 
      ind = ind + 1. 
      IF ind = 57 THEN 
      DO: 
        /*MTPUT STREAM s1 SKIP "" AT 20.*/
        ASSIGN output-list.str = output-list.str + STRING("")
               output-list.pos = 20.
        ind = 1. 
        curr-line = curr-line + 1.
      END. 
      IF SUBSTR(l-orderhdr.lief-fax[3],i,2) = "\" + chr(10) THEN 
      DO: 
        /*MTPUT STREAM s1 SKIP "" AT 20.*/
        ASSIGN output-list.str = output-list.str + STRING("")
               output-list.pos = 20.
        curr-line = curr-line + 1.
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(l-orderhdr.lief-fax[3],i,1) = chr(10) THEN 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      ELSE /*MTPUT STREAM s1 SUBSTR(l-orderhdr.lief-fax[3], i, 1) FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-orderhdr.lief-fax[3], i, 1), "x(1)").
    END. 
  END. 
  ELSE 
  DO: 
    /*MTPUT STREAM s1 "" SKIP.*/
    ASSIGN output-list.str = output-list.str + STRING("").
    CREATE output-list.
    curr-line = curr-line + 1.
    DO j = 1 TO (pos-bez - 1): 
      /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
      ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
    END. 
    ind = 0. 
    DO i = 1 TO LENGTH(l-orderhdr.lief-fax[3]): 
      ind = ind + 1. 
      IF ind = (bez-len + 1) THEN 
      DO: 
        /*MTPUT STREAM s1 "" SKIP.*/
        ASSIGN output-list.str = output-list.str + STRING("").
        CREATE output-list.
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-bez - 1): 
          /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
        ind = 1. 
      END. 
      IF SUBSTR(l-orderhdr.lief-fax[3],i,2) = "\" + chr(10) THEN 
      DO: 
        /*MTPUT STREAM s1 "" SKIP.*/
        ASSIGN output-list.str = output-list.str + STRING("").
        CREATE output-list.
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-bez - 1): 
          /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(l-orderhdr.lief-fax[3],i,1) = chr(10) THEN 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      ELSE /*MTPUT STREAM s1 SUBSTR(l-orderhdr.lief-fax[3], i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-orderhdr.lief-fax[3], i, 1), "x(1)").
    END. 
  END.
  /*MTPUT STREAM s1 ""SKIP.*/
  ASSIGN output-list.str = output-list.str + STRING("").
  CREATE output-list.
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
        /*MTPUT STREAM s1 SKIP "" AT 5.*/
        CREATE output-list.
        ASSIGN output-list.str = output-list.str + STRING("")
               output-list.pos = 5.
    END.
    ELSE IF ord-len GE 60 THEN 
    DO:
        /*MTPUT STREAM s1 SKIP "" AT 10.*/
        CREATE output-list.
        ASSIGN output-list.str = output-list.str + STRING("")
               output-list.pos = 10.
    END.
    ELSE IF ord-len GE 55 THEN 
    DO:
        /*MTPUT STREAM s1 SKIP "" AT 15.*/
        CREATE output-list.
        ASSIGN output-list.str = output-list.str + STRING("")
               output-list.pos = 15.
    END.
    ELSE
    DO:
        /*MTPUT STREAM s1 SKIP "" AT 20.*/
        CREATE output-list.
        ASSIGN output-list.str = output-list.str + STRING("")
               output-list.pos = 20.
    END.
    ind = 0. 
    DO i = 1 TO LENGTH(l-orderhdr.lief-fax[3]): 
      ind = ind + 1. 
      IF ind GT ord-len AND SUBSTR(l-orderhdr.lief-fax[3],i,1) = " " THEN 
      DO: 
        IF ord-len GE 80 THEN 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 5.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 5.
        END.
        ELSE IF ord-len GE 60 THEN 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 10.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 10.
        END.
        ELSE IF ord-len GE 55 THEN 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 15.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 15.
        END.
        ELSE 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 20.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 20.
        END.
        ind = 1. 
      END. 
      ELSE IF SUBSTR(l-orderhdr.lief-fax[3],i,2) = "\" + chr(10) THEN 
      DO: 
        IF ord-len GE 80 THEN
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 5.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 5.
        END.
        ELSE IF ord-len GE 60 THEN 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 10.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 10.
        END.
        ELSE IF ord-len GE 55 THEN 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 15.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 15.
        END.
        ELSE 
        DO:
            /*MTPUT STREAM s1 SKIP "" AT 20.*/
            CREATE output-list.
            ASSIGN output-list.str = output-list.str + STRING("")
                   output-list.pos = 20.
        END.
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(l-orderhdr.lief-fax[3],i,1) = chr(10) THEN 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      ELSE /*MTPUT STREAM s1 SUBSTR(l-orderhdr.lief-fax[3], i, 1) FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-orderhdr.lief-fax[3], i, 1), "x(1)").
    END. 
  END. 
  ELSE 
  DO: 
    /*MTPUT STREAM s1 "" SKIP.*/
    ASSIGN output-list.str = output-list.str + STRING("").
    CREATE output-list.
    curr-line = curr-line + 1.
    DO j = 1 TO (pos-ord - 1): 
      /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
      ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
    END. 
    ind = 0. 
    DO i = 1 TO LENGTH(l-orderhdr.lief-fax[3]): 
      ind = ind + 1. 
      IF ind GT ord-len AND SUBSTR(l-orderhdr.lief-fax[3],i,1) = " " THEN 
      DO: 
        /*MTPUT STREAM s1 "" SKIP.*/
        ASSIGN output-list.str = output-list.str + STRING("").
        CREATE output-list.
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-ord - 1): 
          /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
        ind = 1. 
      END. 
      ELSE IF SUBSTR(l-orderhdr.lief-fax[3],i,2) = "\" + chr(10) THEN 
      DO: 
        /*MTPUT STREAM s1 "" SKIP.*/
        ASSIGN output-list.str = output-list.str + STRING("").
        CREATE output-list.
        curr-line = curr-line + 1.
        DO j = 1 TO (pos-ord - 1): 
          /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
        ind = 1. 
        i = i + 1. 
      END. 
      ELSE IF SUBSTR(l-orderhdr.lief-fax[3],i,1) = chr(10) THEN 
        /*MTPUT STREAM s1 " " FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
      ELSE /*MTPUT STREAM s1 SUBSTR(l-orderhdr.lief-fax[3], i, 1) FORMAT "x(1)".*/
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(l-orderhdr.lief-fax[3], i, 1), "x(1)").
    END. 
  END. 
  /*MTPUT STREAM s1 ""SKIP.*/
  ASSIGN output-list.str = output-list.str + STRING("").
  CREATE output-list.
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
 


