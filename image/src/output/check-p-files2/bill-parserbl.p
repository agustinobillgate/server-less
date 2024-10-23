
/*FT -> 22/10/13 perbaikan create t-list*/
DEFINE WORKFILE brief-list 
  FIELD b-text AS CHAR. 
 
DEFINE WORKFILE htp-list 
  FIELD paramnr AS INTEGER 
  FIELD fchar   AS CHAR.

DEFINE WORKFILE loop-list 
  FIELD texte AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE loop1-list 
  FIELD texte AS CHAR FORMAT "x(132)". 

DEFINE WORKFILE header-list 
  FIELD texte AS CHAR FORMAT "x(132)". 
 
DEFINE TEMP-TABLE bill-list
    FIELD rechnr LIKE bill.rechnr
    FIELD NAME LIKE bill.NAME
    FIELD rechnr2 LIKE bill.rechnr2.

DEFINE TEMP-TABLE output-list
    FIELD str AS CHAR
    FIELD pos AS INTEGER.

DEFINE WORKFILE s-list 
  FIELD nr      AS INTEGER 
  FIELD ankunft AS DATE 
  FIELD abreise AS DATE 
  FIELD bezeich AS CHAR 
  FIELD rmcat   AS CHAR 
  FIELD preis   AS DECIMAL
  FIELD lRate   AS DECIMAL INITIAL 0
  FIELD datum   AS DATE 
  FIELD qty     AS INTEGER 
  FIELD erwachs AS INTEGER 
  FIELD kind1   AS INTEGER 
  FIELD kind2   AS INTEGER. 
 
DEFINE WORKFILE t-list 
  FIELD nr      AS INTEGER 
  FIELD ankunft AS DATE 
  FIELD abreise AS DATE 
  FIELD bezeich AS CHAR 
  FIELD rmcat   AS CHAR 
  FIELD preis   AS DECIMAL 
  FIELD lRate   AS DECIMAL
  FIELD tage    AS INTEGER 
  FIELD date1   AS DATE 
  FIELD date2   AS DATE 
  FIELD qty     AS INTEGER 
  FIELD betrag  AS DECIMAL 
  FIELD erwachs AS INTEGER 
  FIELD kind1   AS INTEGER 
  FIELD kind2   AS INTEGER. 
 
DEFINE WORKFILE bline-list 
  FIELD bl-recid    AS INTEGER 
  FIELD artnr       AS INTEGER 
  FIELD dept        AS INTEGER 
  FIELD anzahl      AS INTEGER 
  FIELD massnr      AS INTEGER    
  FIELD billin-nr   AS INTEGER 
  FIELD zeit        AS INTEGER
  FIELD mwst-code   AS INTEGER INITIAL 0
  FIELD vatProz     AS DECIMAL INITIAL 0
  FIELD epreis      AS DECIMAL 
  FIELD netto       AS DECIMAL INITIAL 0 
  FIELD fsaldo      AS DECIMAL 
  FIELD saldo       AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99" 
  FIELD orts-tax    AS DECIMAL INITIAL 0 
  FIELD voucher     AS CHAR 
  FIELD bezeich     AS CHAR 
  FIELD zinr        AS CHAR 
  FIELD gname       AS CHAR 
  FIELD origin-id   AS CHAR INITIAL ""
  FIELD userinit    AS CHAR FORMAT "x(2)" INITIAL "" 
  FIELD ankunft     AS DATE 
  FIELD abreise     AS DATE 
  FIELD datum       AS DATE 
. 

DEFINE TEMP-TABLE t-spbill-list
  FIELD selected AS LOGICAL INITIAL YES 
  FIELD bl-recid AS INTEGER. 

DEFINE INPUT PARAMETER pvILanguage  AS INT      NO-UNDO.
DEFINE INPUT PARAMETER case-type    AS INTEGER. 
DEFINE INPUT PARAMETER briefnr      AS INTEGER. 
DEFINE INPUT PARAMETER reslinnr     AS INTEGER. 
DEFINE INPUT PARAMETER resnr        AS INTEGER. 
DEFINE INPUT PARAMETER rechnr       AS INTEGER. 
DEFINE INPUT PARAMETER gastnr       AS INTEGER. 
DEFINE INPUT PARAMETER f-page       AS LOGICAL. 
DEFINE INPUT PARAMETER spbill-flag  AS LOGICAL. 
DEFINE INPUT PARAMETER inv-type     AS INTEGER.
DEFINE INPUT PARAMETER user-init    AS CHAR.
DEFINE INPUT PARAMETER printnr      AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR t-spbill-list.
DEFINE OUTPUT PARAMETER succes-flag     AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER outfile     AS CHAR.
DEFINE OUTPUT PARAMETER run-ask     AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR bill-list.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

{ supertransbl.i }.
DEF VAR lvCAREA AS CHAR INITIAL "bill-parser". 

/*
DEF VAR case-type  AS INTEGER INIT 1.
DEF VAR briefnr  AS INTEGER INIT 42.
DEF VAR reslinnr AS INTEGER INIT 14.
DEF VAR resnr    AS INTEGER INIT 16378.
DEF VAR rechnr   AS INTEGER INIT 1251.
DEF VAR printnr   AS INTEGER INIT 99.
DEF VAR gastnr   AS INTEGER INIT 10343.
DEF VAR f-page   AS LOGICAL INIT YES.
DEF VAR spbill-flag   AS LOGICAL INIT NO.
DEF VAR inv-type AS INTEGER INIT 1.
DEF VAR user-init AS CHAR INIT 01.
DEF VAR run-ask AS LOGICAL INIT NO.
DEF VAR outfile AS CHAR. 
 */
DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE billdate        AS DATE. 
DEFINE VARIABLE price-decimal   AS INTEGER. 
DEFINE VARIABLE vat-artnr       AS INTEGER EXTENT 5 INITIAL [0,0,0,0,0]. 
DEFINE VARIABLE n               AS INTEGER. 
DEFINE VARIABLE serv-vat        AS LOGICAL. 
DEFINE VARIABLE briefnr2            AS INTEGER. /* Master bill foreign amt */ 
DEFINE VARIABLE briefnr21           AS INTEGER. /* single line foreign amt */
DEF VAR print-rc                    AS LOGICAL INITIAL NO NO-UNDO.  
DEFINE VARIABLE f-gastnr        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE f-resnr         AS LOGICAL INITIAL NO. 
DEFINE VARIABLE f-resline       AS LOGICAL INITIAL NO. 
DEFINE VARIABLE f-bill          AS LOGICAL INITIAL NO. 
DEFINE VARIABLE longer-billamt  AS LOGICAL INITIAL NO.
DEFINE VARIABLE long-billamt    AS LOGICAL INITIAL NO.
DEFINE VARIABLE master-ankunft  AS DATE. 
DEFINE VARIABLE master-abreise  AS DATE. 
DEFINE VARIABLE fixrate-flag        AS LOGICAL INITIAL NO.
DEFINE VARIABLE long-digit      AS LOGICAL. 
DEFINE VARIABLE exchg-rate          AS DECIMAL INITIAL 1. 
DEFINE VARIABLE curr-line       AS INTEGER. 
DEFINE VARIABLE curr-page       AS INTEGER. 
DEFINE VARIABLE curr-pos        AS INTEGER. 
DEFINE VARIABLE blloop          AS INTEGER INITIAL 0. 
DEFINE VARIABLE headloop        AS INTEGER INITIAL 0. 
DEFINE VARIABLE f-lmargin       AS LOGICAL INITIAL NO. 
DEFINE VARIABLE lmargin         AS INTEGER INITIAL 1. 
DEFINE VARIABLE proforma-inv    AS LOGICAL INITIAL NO. 
DEFINE VARIABLE bline-flag      AS INTEGER INITIAL -1. 
DEFINE VARIABLE keychar         AS CHAR. 
DEFINE VARIABLE bl-balance      LIKE vhp.bill.saldo INITIAL 0. 
DEFINE VARIABLE bl-balance1     LIKE vhp.bill.saldo INITIAL 0. 
DEFINE VARIABLE bl0-balance     LIKE vhp.bill.saldo INITIAL 0. 
DEFINE VARIABLE bl0-balance1    LIKE vhp.bill.saldo INITIAL 0. 
DEFINE VARIABLE bl1-balance     LIKE vhp.bill.saldo INITIAL 0. 
DEFINE VARIABLE bl1-balance1    LIKE vhp.bill.saldo INITIAL 0. 
DEFINE VARIABLE bline-nr            AS INTEGER INITIAL 0. 
DEFINE VARIABLE print-all-member AS LOGICAL INITIAL NO NO-UNDO. 
DEFINE VARIABLE g-length        AS INTEGER INITIAL 16. 
DEFINE VARIABLE d-length        AS INTEGER INITIAL 24. 
DEFINE VARIABLE c-length        AS INTEGER INITIAL 48. /* resline comment length */ 
DEFINE VARIABLE w-length        AS INTEGER INITIAL 40.  /* vhp.bill.saldo WordLen */ 
DEFINE VARIABLE v-length        AS INTEGER INITIAL 16.  /* voucher NO */ 
DEFINE VARIABLE print-member    AS LOGICAL INITIAL YES. 
DEFINE VARIABLE short-arrival   AS LOGICAL INITIAL NO.
DEFINE VARIABLE short-depart    AS LOGICAL INITIAL NO.
DEFINE VARIABLE ntab            AS INTEGER INITIAL 1. 
DEFINE VARIABLE nskip           AS INTEGER INITIAL 1. 
DEFINE VARIABLE wd-array AS INTEGER EXTENT 8 
  INITIAL [7, 1, 2, 3, 4, 5, 6, 7]. 
DEFINE VARIABLE bonus-array     AS LOGICAL EXTENT 999 INITIAL NO. 
DEFINE VARIABLE curr-bl-vat     AS DECIMAL INITIAL 0. 
DEFINE VARIABLE bl-netto        AS DECIMAL INITIAL 0. 


DEFINE BUFFER rmember FOR vhp.res-line. 
DEFINE BUFFER mainres FOR vhp.reservation. 


FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK.
IF case-type = 2 THEN
DO:
    RUN update-bill.
    RETURN.
END.

CREATE output-list.


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 550 NO-LOCK.
IF vhp.htparam.feldtyp = 4 THEN new-contrate = vhp.htparam.flogical.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
 billdate = vhp.htparam.fdate. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 132 NO-LOCK. 
IF vhp.htparam.feldtyp = 1 THEN vat-artnr[1] = vhp.htparam.finteger. 
ELSE IF vhp.htparam.feldtyp = 5 THEN
DO n = 1 TO NUM-ENTRIES(htparam.fchar, ";"):
 IF TRIM(ENTRY(n, vhp.htparam.fchar, ";")) NE "" AND n LE 5 THEN
    ASSIGN vat-artnr[n] = INTEGER(TRIM(ENTRY(n, vhp.htparam.fchar, ";"))) NO-ERROR.
END.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
serv-vat = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 415 NO-LOCK. 
briefnr2 = vhp.htparam.finteger. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 495 NO-LOCK. 
briefnr21 = vhp.htparam.finteger. 

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 435 NO-LOCK. 
print-rc = (htparam.finteger = briefnr). 
 
FIND FIRST vhp.guest WHERE vhp.guest.gastnr = gastnr NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.guest THEN f-gastnr = YES. 
FIND FIRST vhp.reservation WHERE vhp.reservation.resnr = resnr NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.reservation THEN f-resnr = YES. 
f-resline = NO.
IF resnr GT 0 AND reslinnr GT 0 THEN 
DO: 
  FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = resnr 
    AND vhp.res-line.reslinnr = reslinnr NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.res-line THEN f-resline = YES. 
END. 
FIND FIRST vhp.bill WHERE vhp.bill.rechnr = rechnr NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.bill THEN 
DO:    
  f-bill = YES. 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = vhp.bill.rechnr NO-LOCK
    BY vhp.bill-line.betrag:
    IF (vhp.bill-line.betrag LE -1000000000) 
     OR (vhp.bill-line.betrag GE 1000000000) THEN
    DO:
      longer-billamt = YES.
      LEAVE.
    END.
    ELSE IF vhp.bill-line.betrag LE -100000000 
        OR (vhp.bill-line.betrag GE 1000000000) THEN
    DO:
      long-billamt = YES.
    END.
  END.
END.
 
IF f-bill AND vhp.bill.resnr GT 0 AND vhp.bill.reslinnr = 0 THEN 
DO: 
  FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.bill.resnr 
    AND vhp.res-line.resstatus = 6 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.res-line THEN 
  FIND FIRST vhp.res-line WHERE vhp.res-line.resnr = vhp.bill.resnr 
    AND vhp.res-line.resstatus = 8 NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.res-line THEN 
  DO: 
    f-resline = YES. 
    master-ankunft = vhp.res-line.ankunft. 
    master-abreise = vhp.res-line.abreise. 
    FOR EACH rmember WHERE rmember.resnr = vhp.bill.resnr 
      AND rmember.resstatus GE 6 AND rmember.resstatus LE 8 NO-LOCK:
      IF rmember.ankunft LT master-ankunft THEN master-ankunft = rmember.ankunft. 
      IF rmember.abreise GT master-abreise THEN master-abreise = rmember.abreise. 
    END. 
  END. 
END. 
 
/* group 7: fixed exchange rate during whole stay --> YES */ 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 264 NO-LOCK. 
fixrate-flag = vhp.htparam.flogical. 

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 246 NO-LOCK. 
long-digit = vhp.htparam.flogical. 
 
IF f-resline THEN 
DO: 
  IF vhp.res-line.reserve-dec NE 0 THEN exchg-rate = vhp.res-line.reserve-dec. 
  ELSE 
  DO: 
    FIND FIRST vhp.waehrung WHERE vhp.waehrung.waehrungsnr = vhp.res-line.betriebsnr 
       NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.waehrung THEN exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
    ELSE 
    DO: 
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
      FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = vhp.htparam.fchar 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.waehrung THEN exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
    END. 
  END. 
END. 
ELSE 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz = vhp.htparam.fchar 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.waehrung THEN exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
END. 

IF printnr = 0 THEN outfile = ".\vhp-letter.rtf". 
ELSE DO: 
  FIND FIRST vhp.PRINTER WHERE vhp.printer.nr = printnr NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE vhp.PRINTER THEN
  DO: 
    hide MESSAGE NO-PAUSE. 
    MESSAGE "Printer not yet selected" VIEW-AS ALERT-BOX INFORMATION. 
    RETURN. 
  END. 
  ELSE outfile = vhp.printer.path. 
END. 

RUN fill-list. 
 
curr-line = 1. 
curr-page = 1. 
FOR EACH brief-list: 
  IF curr-line GE vhp.printer.pglen THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + "".
    CREATE output-list.
    
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
    ASSIGN output-list.str = output-list.str + "".
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
  ELSE IF blloop = 3 THEN 
  DO: 
    IF proforma-inv THEN RUN do-pbill-line. 
    ELSE 
    DO: 
      IF bline-flag = -1 THEN /* ALL Bill Lines */
      DO: 
        IF NOT spbill-flag THEN 
        DO: 
          IF inv-type = 1 THEN RUN do-billlineA. 
          ELSE IF inv-type = 2 THEN RUN do-billlineB. 
          ELSE IF inv-type GE 3 THEN RUN do-billlineC. 
        END. 
        ELSE RUN do-SPbillline. 
      END. 
      ELSE IF bline-flag = 0 THEN /* ALL revenue Bill Lines */
      DO: 
        IF NOT spbill-flag THEN 
        DO: 
          IF inv-type EQ 1 THEN RUN do-billline0. 
          ELSE IF inv-type EQ 2 THEN RUN do-billlineB. 
          ELSE IF inv-type GE 3 THEN RUN do-billline0C.
        END.
        ELSE
        DO:
            IF inv-type EQ 1 THEN RUN do-SPbillline0. 
            ELSE IF inv-type EQ 2 THEN RUN do-SPbillline0B. 
            ELSE IF inv-type GE 3 THEN RUN do-SPbillline0C.
        END.
      END. 
/* $$$ */ 
      ELSE IF bline-flag = 1 /* AND inv-type NE 2 */ THEN 
      DO: 
        IF NOT spbill-flag THEN RUN do-billline1. 
        ELSE RUN do-SPbillline1. 
      END. 
      ELSE IF bline-flag = 2 /* AND inv-type NE 2 */ THEN 
      DO: 
        IF NOT spbill-flag THEN RUN do-billline2. 
        ELSE RUN do-SPbillline2. 
      END. 
    END. 
  END. 
  ELSE IF headloop = 3 THEN RUN do-billhead. 
 
  IF blloop = 1 THEN blloop = 2. 
  IF headloop = 1 THEN headloop = 2. 
END. 


/**OUTPUT STREAM s1 CLOSE.*/


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 465 NO-LOCK. 
IF (NOT proforma-inv) AND AVAILABLE bill AND vhp.bill.rechnr NE 0 
  /*AND vhp.bill.rechnr2 = 0*/
  AND vhp.htparam.flogical THEN ASSIGN run-ask = YES.


FOR EACH bill WHERE bill.rechnr = rechnr:
    BUFFER-COPY bill TO bill-list.
END.

/*************** PROCEDURE ***************/
FUNCTION get-rackrate RETURNS DECIMAL 
    (INPUT erwachs AS INTEGER, 
     INPUT kind1 AS INTEGER, 
     INPUT kind2 AS INTEGER). 
  DEF VAR rate AS DECIMAL INITIAL 0. 
  IF erwachs GE 1 AND erwachs LE 4 THEN 
      rate = rate + vhp.katpreis.perspreis[erwachs]. 
  rate = rate + kind1 * vhp.katpreis.kindpreis[1] 
              + kind2 * vhp.katpreis.kindpreis[2]. 
  RETURN rate. 
END FUNCTION. 

PROCEDURE fill-list: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE l AS INTEGER. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE keycont AS CHAR. 
DEFINE VARIABLE continued AS LOGICAL INITIAL NO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 600 NO-LOCK. 
  keychar = vhp.htparam.fchar. 
  FIND FIRST vhp.htparam WHERE paramnr = 1122 NO-LOCK. 
  keycont = keychar + vhp.htparam.fchar. 
 
  FOR EACH vhp.htparam WHERE htparam.paramgr = 17 AND htparam.bezeich NE "Not Used" 
      NO-LOCK BY LENGTH(htparam.fchar) DESCENDING: 
    CREATE htp-list. 
    ASSIGN
      htp-list.paramnr = vhp.htparam.paramnr
      htp-list.fchar   = keychar + vhp.htparam.fchar
    . 
  END. 

  DO: 
    FOR EACH vhp.briefzei WHERE vhp.briefzei.briefnr = briefnr NO-LOCK 
      BY vhp.briefzei.briefzeilnr: 
      j = 1. 
      DO i = 1 TO length(briefzei.texte): 
         IF asc(SUBSTR(briefzei.texte, i , 1)) EQ 10 THEN 
         DO: 
           n = i - j. 
           c = SUBSTR(briefzei.texte, j,  n). 
           l = length(c). 
           IF NOT continued THEN create brief-list. 
           brief-list.b-text = brief-list.b-text + c. 
           j = i + 1. 
           IF l GT length(keycont) AND 
             SUBSTR(c, l - length(keycont) + 1, length(keycont)) = keycont THEN 
           DO: 
             continued = YES. 
             b-text = SUBSTR(b-text, 1, length(b-text) - length(keycont)). 
           END. 
           ELSE continued = NO. 
         END. 
      END. 
      n = length(briefzei.texte) - j + 1. 
      c = SUBSTR(briefzei.texte, j,  n). 
      IF NOT continued THEN create brief-list. 
      brief-list.b-text = brief-list.b-text + c. 
    END. 
  END. 
END. 
 
PROCEDURE analyse-text: 
DEFINE VARIABLE len AS INTEGER. 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2300. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN headloop = 1. 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2301. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN headloop = headloop + 1. 
 
  FIND FIRST htp-list WHERE htp-list.paramnr = 2302. 
  IF TRIM(brief-list.b-text) = htp-list.fchar THEN 
  DO: 
    blloop = 1. 
    bline-flag = -1.  /* all vhp.bill-lines */ 
  END. 
  ELSE 
  DO: 
    len = length(TRIM(brief-list.b-text)). 
    IF SUBSTR(TRIM(brief-list.b-text), 1, len - 1)  = htp-list.fchar THEN 
    DO: 
      IF SUBSTR(TRIM(brief-list.b-text), len, 1) = "0" THEN 
      DO: 
        blloop = 1. 
        bline-flag = 0.  /* revenue vhp.bill-lines */ 
      END. 
      ELSE IF SUBSTR(TRIM(brief-list.b-text), len, 1) = "1" THEN 
      DO: 
        blloop = 1. 
        bline-flag = 1. /* payment vhp.bill-lines */ 
      END. 
      ELSE IF SUBSTR(TRIM(brief-list.b-text), len, 1) = "2" THEN 
      DO: 
        blloop = 1. 
        bline-flag = 2. /* payment vhp.bill-lines excluding C/L articles */ 
      END. 
    END. 
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
  DO i = 1 TO length(curr-texte): 
    IF SUBSTR( curr-texte,i,1) = keychar THEN 
    DO: 
      IF i = length(curr-texte) THEN found = NO. 
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
    RUN put-string (SUBSTR(curr-texte, j, length(curr-texte) - j + 1)). 
END.
 
PROCEDURE build-loop-line: 
DEFINE INPUT PARAMETER curr-texte AS CHAR FORMAT "x(132)". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE found AS LOGICAL INITIAL NO. 
  DO i = 1 TO length(curr-texte): 
    IF SUBSTR( curr-texte,i,1) = keychar THEN 
    DO: 
      IF i = length(curr-texte) THEN found = NO. 
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
    RUN put-string(SUBSTR(curr-texte, j, length(curr-texte) - j + 1)). 
END. 
 
PROCEDURE cal-vat: 
DEFINE OUTPUT PARAMETER t-vat AS DECIMAL INITIAL 0. 
DEFINE VARIABLE vat  AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE fact AS DECIMAL. 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND artart NE 2 AND artart NE 4 AND artart NE 6 
    AND artart NE 7 NO-LOCK: 
    serv = 0. 
    vat = 0. 
    IF vhp.bill-line.orts-tax NE 0 THEN t-vat = t-vat + vhp.bill-line.orts-tax. 
    ELSE 
    DO: 
      IF vhp.artikel.service-code NE 0 AND serv-vat THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = vhp.artikel.service-code 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.htparam THEN serv = vhp.htparam.fdecimal / 100. 
      END. 
      IF vhp.artikel.mwst-code NE 0 THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = vhp.artikel.mwst-code 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.htparam THEN vat = vhp.htparam.fdecimal / 100. 
        IF serv-vat THEN vat = vat + vat * serv. 
      END. 
 
      IF (vhp.artikel.artnr = vat-artnr[1] OR vhp.artikel.artnr = vat-artnr[2] 
          OR vhp.artikel.artnr = vat-artnr[3] OR vhp.artikel.artnr = vat-artnr[4] 
          OR vhp.artikel.artnr = vat-artnr[5])
          AND vhp.artikel.departement = 0 THEN 
      DO: 
        fact = 1. 
        vat  = 1. 
        serv = 0. 
      END. 
      ELSE 
 
      fact = 1.00 + serv + vat. 
      t-vat = t-vat + vhp.bill-line.betrag / fact * vat. 
    END. 
  END. 
END. 
 
PROCEDURE cal-SPvat: 
DEFINE OUTPUT PARAMETER t-vat AS DECIMAL INITIAL 0. 
DEFINE VARIABLE vat AS DECIMAL. 
DEFINE VARIABLE serv AS DECIMAL. 
DEFINE VARIABLE fact AS DECIMAL. 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
    AND vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND artart NE 2 AND artart NE 4 AND artart NE 6 
    AND artart NE 7 NO-LOCK: 
    serv = 0. 
    vat = 0. 
    IF vhp.bill-line.orts-tax NE 0 THEN t-vat = t-vat + vhp.bill-line.orts-tax. 
    ELSE 
    DO: 
      IF vhp.artikel.service-code NE 0 AND serv-vat THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = vhp.artikel.service-code 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.htparam THEN serv = vhp.htparam.fdecimal / 100. 
      END. 
      IF vhp.artikel.mwst-code NE 0 THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = vhp.artikel.mwst-code 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.htparam THEN vat = vhp.htparam.fdecimal / 100. 
        IF serv-vat THEN vat = vat + vat * serv. 
      END. 
 
      IF (vhp.artikel.artnr = vat-artnr[1] OR vhp.artikel.artnr = vat-artnr[2] 
          OR vhp.artikel.artnr = vat-artnr[3] OR vhp.artikel.artnr = vat-artnr[4] 
          OR vhp.artikel.artnr = vat-artnr[5])
          AND vhp.artikel.departement = 0 THEN 
      DO: 
        fact = 1. 
        vat  = 1. 
        serv = 0. 
      END. 
      ELSE fact = 1.00 + serv + vat. 
      t-vat = t-vat + vhp.bill-line.betrag / fact * vat. 
    END. 
  END. 
END.
 
PROCEDURE do-billlineA: 
DEFINE VARIABLE n AS INTEGER NO-UNDO. 
DEFINE VARIABLE saldo AS DECIMAL INITIAL 0 NO-UNDO. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl-balance = 0. 
  bl-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE vhp.artikel THEN 
        FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 NO-LOCK. 
 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
        CREATE bline-list. 
        BUFFER-COPY vhp.bill-line TO bline-list.
        ASSIGN 
          bline-list.bl-recid = RECID(bill-line)
          bline-list.dept     = vhp.bill-line.departement
          bline-list.datum    = vhp.bill-line.bill-datum
          bline-list.fsaldo   = vhp.bill-line.fremdwbetrag 
          bline-list.saldo    = vhp.bill-line.betrag
        . 
    END. 
    IF (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9) THEN 
      bl0-balance = bl0-balance + vhp.bill-line.betrag. 
    ELSE IF vhp.artikel.artart = 6 AND vhp.artikel.zwkum = paidout THEN 
        bl0-balance = bl0-balance + vhp.bill-line.betrag. 
  END. 
 
  bline-nr = 0. 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
    saldo = saldo + vhp.bill-line.betrag. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
 
  IF f-bill THEN 
  DO: 
    FIND FIRST vhp.bill WHERE vhp.bill.rechnr = rechnr NO-LOCK. 
    bl-balance = vhp.bill.saldo. 
/* 
    bl-balance1 = vhp.bill.mwst[99]. 
*/ 
  END. 
 
  IF (bl-balance - saldo) GE 0.5 OR (saldo - bl-balance) GE 0.5 THEN 
  DO: 
    /*hide MESSAGE NO-PAUSE. 
    MESSAGE "New vhp.bill-line exists during printing the bill;" 
    SKIP 
    "Please re-check the bill balance on the print-out." 
    VIEW-AS ALERT-BOX WARNING. */
  END. 
 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-billlineB: 
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE s-bezeich   AS CHAR. 
DEFINE VARIABLE netto       AS DECIMAL. 
DEFINE VARIABLE curr-bl-vat AS DECIMAL. 
DEFINE VARIABLE paidout     AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE vat%        AS DECIMAL INITIAL 0 NO-UNDO.
DEFINE VARIABLE vatcode     AS INTEGER INITIAL 0 NO-UNDO.
DEFINE BUFFER foart         FOR vhp.artikel. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl0-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (vhp.artikel.artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK: 

    IF vhp.bill-line.origin-id NE "" THEN
    DO:
      RUN get-vat(vhp.bill-line.origin-id, OUTPUT vat%).
      vatcode = 0.
      IF vat% EQ 1000 THEN 
      ASSIGN 
          vat%        = 0
          curr-bl-vat = 0
      .  
      ELSE
      DO:
        curr-bl-vat = vat%.
        FIND FIRST vhp.htparam WHERE vhp.htparam.fdecimal = vat% NO-LOCK 
          NO-ERROR. 
        IF AVAILABLE vhp.htparam THEN vatcode = vhp.htparam.paramnr.
      END.
      FIND FIRST bline-list WHERE bline-list.vatProz = vat% NO-ERROR. 
      IF NOT AVAILABLE bline-list THEN 
      DO:
        CREATE bline-list. 
        BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
            TO bline-list.
        ASSIGN 
            bline-list.bl-recid  = RECID(bill-line)
            bline-list.dept      = vhp.bill-line.departement
            bline-list.zinr      = vhp.bill.zinr
            bline-list.mwst-code = vatcode
            bline-list.vatproz   = vat%
        . 
      END. 
      ASSIGN
        bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
        bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag
        bl0-balance         = bl0-balance  + vhp.bill-line.betrag
        bl0-balance1        = bl0-balance1 + vhp.bill-line.fremdwbetrag
      .  
      DO: 
        IF vhp.bill-line.orts-tax NE 0 
          THEN netto = vhp.bill-line.betrag - vhp.bill-line.orts-tax. 
        ELSE 
        ASSIGN 
          netto = vhp.bill-line.betrag / (1 + curr-bl-vat / 100)
          netto = ROUND(netto, price-decimal)
        . 
        bline-list.netto = bline-list.netto + netto. 
      END.
    END.
    ELSE
    DO:
      FIND FIRST bline-list WHERE bline-list.mwst-code = vhp.artikel.mwst-code
        NO-ERROR. 
      IF NOT AVAILABLE bline-list THEN 
      DO:
        CREATE bline-list. 
        BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
            TO bline-list.
        ASSIGN 
            bline-list.bl-recid  = RECID(bill-line)
            bline-list.dept      = vhp.bill-line.departement
            bline-list.zinr      = vhp.bill.zinr
            bline-list.mwst-code = vhp.artikel.mwst-code
        . 
      END. 
      ASSIGN
        bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
        bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag
        bl0-balance         = bl0-balance  + vhp.bill-line.betrag
        bl0-balance1        = bl0-balance1 + vhp.bill-line.fremdwbetrag
      . 
 
      IF (vhp.artikel.artnr = vat-artnr[1] OR vhp.artikel.artnr = vat-artnr[2] 
        OR vhp.artikel.artnr = vat-artnr[3] OR vhp.artikel.artnr = vat-artnr[4] 
        OR vhp.artikel.artnr = vat-artnr[5])
        AND vhp.artikel.departement = 0 THEN .
      ELSE 
      DO: 
        FIND FIRST foart WHERE foart.artnr = vhp.bill-line.artnr 
          AND foart.departement = vhp.bill-line.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE foart THEN 
        DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN 
          ASSIGN    
              curr-bl-vat        = vhp.htparam.fdecimal
              bline-list.vatproz = curr-bl-vat
          .
          ELSE curr-bl-vat = 0. 
        END. 
        IF vhp.bill-line.orts-tax NE 0 
          THEN netto = vhp.bill-line.betrag - vhp.bill-line.orts-tax. 
        ELSE 
        ASSIGN 
          netto = vhp.bill-line.betrag / (1 + curr-bl-vat / 100)
          netto = round(netto, price-decimal)
        . 
        bline-list.netto = bline-list.netto + netto. 
      END.
    END. 
  END. 
 
/* the previous one 
  bline-nr = 0. 
  IF AVAILABLE bline-list THEN 
  DO: 
    bline-nr = 1. 
    bl-balance = bline-list.saldo. 
    bl-balance1 = bline-list.fsaldo. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      PUT STREAM s1 "" SKIP. 
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 

    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      PUT STREAM s1 "" SKIP. 
      curr-line = curr-line + 1. 
    END. 
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
*/
  bline-nr = 0. 
  FOR EACH bline-list: 
    ASSIGN
      bline-nr    = bline-nr    + 1 
      bl-balance  = bl-balance  + bline-list.saldo 
      bl-balance1 = bl-balance1 + bline-list.fsaldo
    . 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 

END. 
 
PROCEDURE do-billlineC: 
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE saldo       AS DECIMAL INITIAL 0. 
DEFINE VARIABLE descript    AS CHAR. 
DEFINE BUFFER resline       FOR vhp.res-line. 
DEFINE BUFFER rline         FOR vhp.res-line.
DEFINE VARIABLE paidout     AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl-balance = 0. 
  bl-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9) NO-LOCK 
    BY vhp.bill-line.zinr BY vhp.bill-line.bezeich BY vhp.bill-line.bill-datum descending: 

    IF inv-type = 3 THEN
    DO:
      IF vhp.artikel.bezaendern OR vhp.artikel.artart = 1 THEN
      FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.bezeich = vhp.bill-line.bezeich 
     /* AND bline-list.zinr = vhp.bill-line.zinr */ NO-ERROR. 
      ELSE FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
     /* AND bline-list.zinr = vhp.bill-line.zinr */ NO-ERROR. 
    END.
    ELSE IF inv-type = 4 THEN
    DO:
      IF vhp.artikel.bezaendern OR vhp.artikel.artart = 1 THEN
      FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.bezeich = vhp.bill-line.bezeich 
        AND bline-list.zinr = vhp.bill-line.zinr NO-ERROR. 
      ELSE FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.zinr = vhp.bill-line.zinr NO-ERROR. 
    END.

    IF NOT AVAILABLE bline-list THEN 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF AVAILABLE resline AND resline.zimmerfix THEN
      DO:
          FIND FIRST rline WHERE rline.resnr = resline.resnr 
              AND rline.zinr = resline.zinr
              AND NOT rline.zimmerfix NO-LOCK NO-ERROR.
          IF AVAILABLE rline THEN FIND FIRST resline WHERE
              RECID(resline) = RECID(rline) NO-LOCK.
      END.
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10 NO-LOCK NO-ERROR. 
 
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
          TO bline-list.
      ASSIGN bline-list.bl-recid = RECID(bill-line)
             bline-list.dept     = vhp.bill-line.departement
             bline-list.datum    = vhp.bill-line.bill-datum.
 
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
    ASSIGN
      bline-list.orts-tax = bline-list.orts-tax + vhp.bill-line.orts-tax
      bline-list.anzahl   = bline-list.anzahl + vhp.bill-line.anzahl
      bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag 
      bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag 
      bl0-balance         = bl0-balance + vhp.bill-line.betrag
    . 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 2 OR artart = 5 OR artart = 6 OR artart = 7) NO-LOCK 
    BY vhp.bill-line.bezeich BY vhp.bill-line.bill-datum descending: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich NO-ERROR. 
    IF NOT AVAILABLE bline-list THEN 
    DO: 
        CREATE bline-list. 
        BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
            TO bline-list.
        ASSIGN bline-list.bl-recid = RECID(bill-line).
    END. 
    ASSIGN
      bline-list.saldo = bline-list.saldo + vhp.bill-line.betrag
      bline-list.dept   = vhp.bill-line.departement
      bline-list.fsaldo = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
    . 
    IF vhp.artikel.zwkum = paidout THEN 
        bl0-balance = bl0-balance + vhp.bill-line.betrag. 
 
  END. 
 
  FOR EACH bline-list WHERE bline-list.saldo = 0: 
    DELETE bline-list. 
  END. 
 
  bline-nr = 0. 
  FOR EACH bline-list: 
    bline-nr = bline-nr + 1. 
    bl-balance = bl-balance + bline-list.saldo. 
    bl-balance1 = bl-balance1 + bline-list.fsaldo. 
    saldo = saldo + bline-list.saldo. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
 
  IF f-bill THEN 
  DO: 
    FIND FIRST vhp.bill WHERE vhp.bill.rechnr = rechnr NO-LOCK. 
    bl-balance = vhp.bill.saldo. 
/* 
    bl-balance1 = vhp.bill.mwst[99]. 
*/ 
  END. 
 
  IF (bl-balance - saldo) GE 0.5 OR (saldo - bl-balance) GE 0.5 THEN 
  DO: 
    /*hide MESSAGE NO-PAUSE. 
    MESSAGE "New vhp.bill-line exists during printing the bill;" 
    SKIP 
    "Please re-check the bill balance on the print-out." 
    VIEW-AS ALERT-BOX WARNING. */
  END. 
 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-SPbillline: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE VARIABLE saldo AS DECIMAL INITIAL 0. 
 
  bl-balance = 0. 
  bl-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
    AND vhp.bill-line.rechnr = rechnr NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
        CREATE bline-list. 
        BUFFER-COPY vhp.bill-line TO bline-list.
        ASSIGN 
          bline-list.bl-recid = RECID(bill-line)
          bline-list.datum    = vhp.bill-line.bill-datum
          bline-list.dept     = vhp.bill-line.departement
          bline-list.fsaldo   = vhp.bill-line.fremdwbetrag 
          bline-list.saldo    = vhp.bill-line.betrag
        . 
    END. 
  END. 
 
  bline-nr = 0. 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
    saldo = saldo + vhp.bill-line.betrag. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
 
  IF f-bill THEN 
  DO: 
    FIND FIRST vhp.bill WHERE vhp.bill.rechnr = rechnr NO-LOCK. 
    IF NOT spbill-flag THEN bl-balance = vhp.bill.saldo. 
/* 
    bl-balance1 = vhp.bill.mwst[99]. 
*/ 
  END. 
 
  IF ((bl-balance - saldo) GE 0.5 OR (saldo - bl-balance) GE 0.5) 
    AND NOT spbill-flag THEN 
  DO: 
    /*hide MESSAGE NO-PAUSE. 
    MESSAGE "New vhp.bill-line exists during printing the bill;" 
    SKIP 
    "Please re-check the bill balance on the print-out." 
    VIEW-AS ALERT-BOX WARNING. */
  END. 
 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END.
 
PROCEDURE do-billline0: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER resline FOR vhp.res-line. 
 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl0-balance1 = 0. 
  bl-balance = 0. 
  bl-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
         OR (vhp.artikel.artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line TO bline-list.
      ASSIGN 
        bline-list.bl-recid = RECID(bill-line)
        bline-list.datum    = vhp.bill-line.bill-datum
        bline-list.dept     = vhp.bill-line.departement
        bline-list.fsaldo   = vhp.bill-line.fremdwbetrag 
        bline-list.saldo    = vhp.bill-line.betrag
      . 
      
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
  END. 
 
  bline-nr = 0. 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl0-balance = bl0-balance + vhp.bill-line.betrag. 
    bl0-balance1 = bl0-balance1 + vhp.bill-line.fremdwbetrag. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-billline0C: 
DEFINE VARIABLE n       AS INTEGER. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE BUFFER resline   FOR vhp.res-line.
DEFINE BUFFER rline     FOR vhp.res-line.
 

  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl0-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK 
    BY vhp.bill-line.zinr BY vhp.bill-line.bezeich BY vhp.bill-line.bill-datum: 

    IF inv-type = 3 THEN
    DO:
      IF vhp.artikel.bezaendern OR vhp.artikel.artart = 1 THEN
      FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.bezeich = vhp.bill-line.bezeich 
    /* AND bline-list.zinr = vhp.bill-line.zinr */ NO-ERROR. 
      ELSE FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
    /* AND bline-list.zinr = vhp.bill-line.zinr */ NO-ERROR. 
    END.
    ELSE IF inv-type = 4 THEN /* 28/08/08 */
    DO:
      IF vhp.artikel.bezaendern OR vhp.artikel.artart = 1 THEN
      FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.bezeich = vhp.bill-line.bezeich 
        AND bline-list.zinr = vhp.bill-line.zinr NO-ERROR. 
      ELSE FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.zinr = vhp.bill-line.zinr NO-ERROR. 
    END.

    IF NOT AVAILABLE bline-list THEN 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF AVAILABLE resline AND resline.zimmerfix THEN
      DO:
          FIND FIRST rline WHERE rline.resnr = resline.resnr 
              AND rline.zinr = resline.zinr
              AND NOT rline.zimmerfix NO-LOCK NO-ERROR.
          IF AVAILABLE rline THEN FIND FIRST resline WHERE
              RECID(resline) = RECID(rline) NO-LOCK.
      END.
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10 AND resline.resstatus NE 99
        AND resline.l-zuordnung[3] = 0 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
          TO bline-list.
      ASSIGN bline-list.bl-recid = RECID(bill-line)
             bline-list.dept     = vhp.bill-line.departement
             bline-list.datum    = vhp.bill-line.bill-datum.
      
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
    ASSIGN
      bline-list.orts-tax = bline-list.orts-tax + vhp.bill-line.orts-tax
      bline-list.anzahl   = bline-list.anzahl + vhp.bill-line.anzahl
      bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag 
      bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
    . 
  END. 
 
  FOR EACH bline-list WHERE bline-list.saldo = 0: 
    DELETE bline-list. 
  END. 
 
  bline-nr = 0. 
  FOR EACH bline-list: 
    bline-nr = bline-nr + 1. 
    bl0-balance = bl0-balance + bline-list.saldo. 
    bl0-balance1 = bl0-balance1 + bline-list.fsaldo. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-SPbillline0: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl0-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
    AND vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line TO bline-list.
      ASSIGN 
        bline-list.bl-recid = RECID(bill-line)
        bline-list.datum    = vhp.bill-line.bill-datum
        bline-list.dept     = vhp.bill-line.departement
        bline-list.fsaldo   = vhp.bill-line.fremdwbetrag 
        bline-list.saldo    = vhp.bill-line.betrag
      . 
      
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
  END. 
 
  bline-nr = 0.
  IF inv-type = 4 THEN
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.zinr BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl0-balance = bl0-balance + vhp.bill-line.betrag. 
    bl0-balance1 = bl0-balance1 + vhp.bill-line.fremdwbetrag. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
  ELSE
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl0-balance = bl0-balance + vhp.bill-line.betrag. 
    bl0-balance1 = bl0-balance1 + vhp.bill-line.fremdwbetrag. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
/* 
  bl-balance = bl-balance + bl0-balance. 
  bl-balance1 = bl-balance1 + bl0-balance1. 
*/ 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END.
 
PROCEDURE do-SPbillline0B: 
DEFINE VARIABLE n           AS INTEGER. 
DEFINE VARIABLE s-bezeich   AS CHAR. 
DEFINE VARIABLE netto       AS DECIMAL. 
DEFINE VARIABLE curr-bl-vat AS DECIMAL. 
DEFINE VARIABLE paidout     AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE BUFFER foart FOR vhp.artikel. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl0-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (vhp.artikel.artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK: 
    FIND FIRST bline-list WHERE bline-list.mwst-code = vhp.artikel.mwst-code
        NO-ERROR. 
    IF NOT AVAILABLE bline-list THEN 
    DO: 
        CREATE bline-list. 
        BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
            TO bline-list.
        ASSIGN 
            bline-list.bl-recid  = RECID(bill-line)
            bline-list.dept      = vhp.bill-line.departement
            bline-list.zinr      = vhp.bill.zinr
            bline-list.mwst-code = vhp.artikel.mwst-code
        . 
    END. 
    ASSIGN
      bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
      bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag
      bl0-balance         = bl0-balance  + vhp.bill-line.betrag
      bl0-balance1        = bl0-balance1 + vhp.bill-line.fremdwbetrag
    . 
 
    IF (vhp.artikel.artnr = vat-artnr[1] OR vhp.artikel.artnr = vat-artnr[2] 
        OR vhp.artikel.artnr = vat-artnr[3] OR vhp.artikel.artnr = vat-artnr[4] 
        OR vhp.artikel.artnr = vat-artnr[5])
        AND vhp.artikel.departement = 0 THEN .
    ELSE 
    DO: 
      FIND FIRST foart WHERE foart.artnr = vhp.bill-line.artnr 
        AND foart.departement = vhp.bill-line.departement NO-LOCK NO-ERROR. 
      IF AVAILABLE foart THEN 
      DO: 
        FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
          NO-ERROR. 
        IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
        ELSE curr-bl-vat = 0. 
      END. 
      IF vhp.bill-line.orts-tax NE 0 
        THEN netto = vhp.bill-line.betrag - vhp.bill-line.orts-tax. 
      ELSE 
      DO: 
        netto = vhp.bill-line.betrag / (1 + curr-bl-vat / 100). 
        netto = round(netto, price-decimal). 
      END. 
      bline-list.netto = bline-list.netto + netto. 
    END. 
  END. 
 
  bline-nr = 0. 
  IF AVAILABLE bline-list THEN 
  DO: 
    bline-nr = 1. 
    bl-balance = bline-list.saldo. 
    bl-balance1 = bline-list.fsaldo. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 

    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 

END.
 
PROCEDURE do-SPbillline0C: 
DEFINE VARIABLE n       AS INTEGER. 
DEFINE BUFFER resline   FOR vhp.res-line. 
DEFINE BUFFER rline     FOR vhp.res-line.
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl0-balance = 0. 
  bl0-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = vhp.bill-line.departement 
    AND (artart = 0 OR artart = 1 OR artart = 8 OR artart = 9 
     OR (artart = 6 AND vhp.artikel.zwkum = paidout)) NO-LOCK 
    BY vhp.bill-line.zinr BY vhp.bill-line.bezeich BY vhp.bill-line.bill-datum: 

    IF inv-type = 3 THEN
    DO:
      IF vhp.artikel.bezaendern OR vhp.artikel.artart = 1 THEN
      FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.bezeich = vhp.bill-line.bezeich 
     /* AND bline-list.zinr = vhp.bill-line.zinr */ NO-ERROR. 
      ELSE FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
    /* AND bline-list.zinr = vhp.bill-line.zinr */ NO-ERROR. 
    END.
    ELSE IF inv-type = 4 THEN
    DO:
      IF vhp.artikel.bezaendern OR vhp.artikel.artart = 1 THEN
      FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.bezeich = vhp.bill-line.bezeich 
        AND bline-list.zinr = vhp.bill-line.zinr NO-ERROR. 
      ELSE FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
        AND bline-list.dept = vhp.bill-line.departement 
        AND bline-list.zinr = vhp.bill-line.zinr NO-ERROR. 
    END.

    IF NOT AVAILABLE bline-list THEN 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF AVAILABLE resline AND resline.zimmerfix THEN
      DO:
          FIND FIRST rline WHERE rline.resnr = resline.resnr 
              AND rline.zinr = resline.zinr
              AND NOT rline.zimmerfix NO-LOCK NO-ERROR.
          IF AVAILABLE rline THEN FIND FIRST resline WHERE
              RECID(resline) = RECID(rline) NO-LOCK.
      END.
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
          TO bline-list.
      ASSIGN bline-list.bl-recid = RECID(bill-line)
             bline-list.dept     = vhp.bill-line.departement
             bline-list.datum    = vhp.bill-line.bill-datum.
      
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
    ASSIGN
      bline-list.orts-tax = bline-list.orts-tax + vhp.bill-line.orts-tax
      bline-list.anzahl   = bline-list.anzahl + vhp.bill-line.anzahl
      bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag 
      bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
    . 
  END. 
 
  FOR EACH bline-list WHERE bline-list.saldo = 0: 
    DELETE bline-list. 
  END. 
 
  bline-nr = 0. 
  FOR EACH bline-list: 
    bline-nr = bline-nr + 1. 
    bl0-balance = bl0-balance + bline-list.saldo. 
    bl0-balance1 = bl0-balance1 + bline-list.fsaldo. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END.
 
PROCEDURE do-billline1: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl1-balance = 0. 
  bl1-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 2 OR artart = 5 OR artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
 
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
          TO bline-list.
      ASSIGN 
          bline-list.bl-recid = RECID(bill-line)
          bline-list.datum    = vhp.bill-line.bill-datum
          bline-list.dept     = vhp.bill-line.departement
          bline-list.saldo    = bline-list.saldo + vhp.bill-line.betrag
          bline-list.fsaldo   = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
      . 

      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr 
    AND vhp.bill-line.departement = 0 NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 2 OR artart = 5 OR artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    
    ASSIGN
      bline-nr = bline-nr + 1
      bl1-balance = bl1-balance + vhp.bill-line.betrag 
      bl1-balance1 = bl1-balance1 + vhp.bill-line.fremdwbetrag 
      bl-balance = bl-balance + vhp.bill-line.betrag
      bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag
    . 
 
    IF vhp.artikel.zwkum = paidout THEN 
        bl0-balance = bl0-balance + vhp.bill-line.betrag. 
 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
/* 
  bl-balance = bl-balance + bl1-balance. 
  bl-balance1 = bl-balance1 + bl1-balance1. 
*/ 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-SPbillline1: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl1-balance = 0. 
  bl1-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
    AND vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 2 OR artart = 5 OR artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line EXCEPT vhp.bill-line.orts-tax vhp.bill-line.anzahl
          TO bline-list.
      ASSIGN 
          bline-list.bl-recid = RECID(bill-line)
          bline-list.datum    = vhp.bill-line.bill-datum
          bline-list.dept     = vhp.bill-line.departement
          bline-list.saldo = bline-list.saldo + vhp.bill-line.betrag
          bline-list.fsaldo = bline-list.fsaldo + vhp.bill-line.fremdwbetrag
      . 
      
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr 
    AND vhp.bill-line.departement = 0 NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 2 OR artart = 5 OR artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    
    ASSIGN
      bline-nr = bline-nr + 1
      bl1-balance = bl1-balance + vhp.bill-line.betrag
      bl1-balance1 = bl1-balance1 + vhp.bill-line.fremdwbetrag 
      bl-balance = bl-balance + vhp.bill-line.betrag
      bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag
    . 
 
    IF vhp.artikel.zwkum = paidout THEN 
        bl0-balance = bl0-balance + vhp.bill-line.betrag. 
 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
/* 
  bl-balance = bl-balance + bl1-balance. 
  bl-balance1 = bl-balance1 + bl1-balance1. 
*/ 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END.
 
PROCEDURE do-billline2: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl1-balance = 0. 
  bl1-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 

  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 6 OR artart = 7) AND vhp.artikel.zwkum NE paidout NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line TO bline-list.
      ASSIGN 
        bline-list.bl-recid = RECID(bill-line)
        bline-list.datum    = vhp.bill-line.bill-datum
        bline-list.dept     = vhp.bill-line.departement
        bline-list.fsaldo   = vhp.bill-line.fremdwbetrag 
        bline-list.saldo    = vhp.bill-line.betrag
      . 

      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr 
    AND vhp.bill-line.departement = 0 NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl1-balance = bl1-balance + vhp.bill-line.betrag. 
    bl1-balance1 = bl1-balance1 + vhp.bill-line.fremdwbetrag. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
 
    IF vhp.artikel.zwkum = paidout THEN bl0-balance = bl0-balance + 
        vhp.bill-line.betrag. 
 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END. 
  END. 
/* 
  bl-balance = bl-balance + bl1-balance. 
  bl-balance1 = bl-balance1 + bl1-balance1. 
*/ 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-SPbillline2: 
DEFINE VARIABLE n AS INTEGER. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE VARIABLE paidout AS INTEGER INITIAL 0 NO-UNDO. 
 
  FIND FIRST vhp.htparam WHERE paramnr = 242 NO-LOCK. 
  paidout = vhp.htparam.finteger. 
 
  bl1-balance = 0. 
  bl1-balance1 = 0. 
 
  FOR EACH bline-list: 
    DELETE bline-list. 
  END. 
 
  FOR EACH t-spbill-list WHERE t-spbill-list.selected = YES, 
    FIRST vhp.bill-line WHERE RECID(bill-line) = t-spbill-list.bl-recid 
    AND vhp.bill-line.rechnr = rechnr NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK 
    BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    FIND FIRST bline-list WHERE bline-list.artnr = vhp.bill-line.artnr 
      AND bline-list.dept = vhp.bill-line.departement 
      AND bline-list.bezeich = vhp.bill-line.bezeich 
      AND bline-list.datum = vhp.bill-line.bill-datum 
      AND bline-list.saldo = - vhp.bill-line.betrag NO-ERROR. 
    IF AVAILABLE bline-list THEN DELETE bline-list. 
    ELSE 
    DO: 
      FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr 
        NO-LOCK NO-ERROR. 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
      
      CREATE bline-list. 
      BUFFER-COPY vhp.bill-line TO bline-list.
      ASSIGN 
        bline-list.bl-recid = RECID(bill-line)
        bline-list.datum    = vhp.bill-line.bill-datum
        bline-list.dept     = vhp.bill-line.departement
        bline-list.fsaldo   = vhp.bill-line.fremdwbetrag 
        bline-list.saldo    = vhp.bill-line.betrag
      . 
      
      IF AVAILABLE resline THEN bline-list.gname = resline.name. 
      IF AVAILABLE mainres THEN bline-list.voucher = mainres.vesrdepot. 
    END. 
  END. 
 
  FOR EACH vhp.bill-line WHERE vhp.bill-line.rechnr = rechnr 
    AND vhp.bill-line.departement = 0 NO-LOCK, 
    FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.bill-line.artnr 
    AND vhp.artikel.departement = 0 
    AND (artart = 6 OR artart = 7) 
    AND vhp.artikel.zwkum NE paidout NO-LOCK, 
    FIRST bline-list WHERE bline-list.bl-recid = INTEGER(RECID(bill-line)) 
    NO-LOCK BY vhp.bill-line.sysdate BY vhp.bill-line.zeit: 
    bline-nr = bline-nr + 1. 
    bl1-balance = bl1-balance + vhp.bill-line.betrag. 
    bl1-balance1 = bl1-balance1 + vhp.bill-line.fremdwbetrag. 
    bl-balance = bl-balance + vhp.bill-line.betrag. 
    bl-balance1 = bl-balance1 + vhp.bill-line.fremdwbetrag. 
 
    IF vhp.artikel.zwkum = paidout THEN bl0-balance = bl0-balance 
        + vhp.bill-line.betrag. 
 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
    END. 
  END. 
/* 
  bl-balance = bl-balance + bl1-balance. 
  bl-balance1 = bl-balance1 + bl1-balance1. 
*/ 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END.
 
PROCEDURE do-pbill-line: 
DEFINE VARIABLE n AS INTEGER. 
  bl-balance = 0. 
  bl-balance1 = 0. 
  FOR EACH t-list BY t-list.nr BY t-list.date1: 
    bl-balance = bl-balance + t-list.betrag. 
    bl-balance1 = bl-balance. 
    IF curr-line GE vhp.printer.pglen THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-page = curr-page + 1. 
      curr-line = 1. 
      RUN do-billhead. 
    END. 
    FOR EACH loop-list: 
      curr-pos = 1. 
      IF f-lmargin THEN DO n = 1 TO lmargin: 
        RUN put-string(" "). 
      END. 
      RUN build-loop-line (loop-list.texte). 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
      curr-line = curr-line + 1. 
    END.
  END. 
  FOR EACH loop-list: 
    DELETE loop-list. 
  END. 
  blloop = 0. 
END. 
 
PROCEDURE do-billhead: 
DEFINE VARIABLE n AS INTEGER. 
  headloop = 3. 
  FOR EACH header-list: 
    DELETE header-list. 
  END. 
  FOR EACH loop1-list: 
    CREATE header-list.    
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
    DO i = 1 TO length(header-list.texte): 
      ASSIGN output-list.str = output-list.str + STRING(SUBSTR(header-list.texte, i, 1), "x(1)").
      
    END. 
    ASSIGN output-list.str = output-list.str + "".
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
    IF htp-list.fchar = SUBSTR(curr-texte, j, length(htp-list.fchar)) THEN 
    DO: 
      found = YES. 
      i = j + length(htp-list.fchar) - 1. 
 
      print-all-member = NO. 
      IF htp-list.paramnr = 1094  /* vhp.bill-line GuestName */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) = "*" THEN 
        DO: 
          i = i + 1. 
          print-all-member = YES. 
        END. 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          g-length = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
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
          IF rowno GT vhp.printer.pglen THEN rowno = vhp.printer.pglen.          
          i = i + 2. 
          IF curr-line < rowno THEN 
          DO: 
            DO j = 1 TO (rowno - curr-line): 
              ASSIGN output-list.str = output-list.str + "".
              CREATE output-list.
              
            END. 
            curr-line = rowno. 
            curr-pos = 1. 
          END. 
          ELSE IF curr-line > rowno THEN /* 30/03/2008 */
          DO: 
            /*PAGE STREAM s1.*/
            curr-page = curr-page + 1.
            curr-line = 1. 
            RUN do-billhead. 
            DO j = 1 TO (rowno - curr-line): 
              ASSIGN output-list.str = output-list.str + "".
              CREATE output-list.
              
            END. 
            curr-line = rowno. 
            curr-pos = 1. 
          END. 
        END. 
        ELSE IF curr-line > rowno THEN 
        DO: 
          DO j = 1 TO (rowno - curr-line): 
            ASSIGN output-list.str = output-list.str + "".
            CREATE output-list.
            
          END. 
          curr-line = rowno. 
          curr-pos = 1. 
        END. 
        IF curr-line GE vhp.printer.pglen THEN 
        DO: 
          curr-page = curr-page + 1. 
          curr-line = 1. 
          RUN do-billhead. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 1091  /* resLine comment word length */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          c-length = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          i = i + 2. 
        END. 
      END. 

      ELSE IF htp-list.paramnr = 1096  /* vhp.bill.saldo word length */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          w-length = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          i = i + 2. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 1589  /* Voucher word length */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 1, 1) LE "9" 
          AND SUBSTR(curr-texte, i + 2, 1) GE "0" 
          AND SUBSTR(curr-texte, i + 2, 1) LE "9" THEN 
        DO: 
          v-length = INTEGER(SUBSTR(curr-texte, i + 1, 2)). 
          i = i + 2. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 664  /* Bill Receiver */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) EQ "0" THEN 
        DO: 
          print-member = NO. 
          i = i + 1. 
        END. 
      END. 
 
      ELSE IF htp-list.paramnr = 655  /* Arrival Date */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) EQ "0" THEN 
        DO: 
          short-arrival = YES.
          i = i + 1. 
        END. 
      END. 

      ELSE IF htp-list.paramnr = 656  /* Departure Date */  THEN 
      DO: 
        IF SUBSTR(curr-texte, i + 1, 1) EQ "0" THEN 
        DO: 
          short-depart = YES.
          i = i + 1. 
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
 
              6       vhp.reservation start 
              7       vhp.reservation END 
 
              8       debt start 
              9       debt END 
 
             10       length OF vhp.bill-line description 
*/ 
  IF (paramnr LE 500) THEN 
      RUN decode-key1 (paramnr, OUTPUT out-str, OUTPUT status-code). 
  ELSE IF ((paramnr GE 501) AND (paramnr LE 649)) OR (paramnr = 1110) THEN 
      RUN decode-key2 (paramnr, OUTPUT out-str, OUTPUT status-code). 
  ELSE IF (paramnr GE 650) AND (paramnr LE 699) THEN 
      RUN decode-key3 (paramnr, OUTPUT out-str, OUTPUT status-code). 
  ELSE IF (paramnr EQ 1105) OR (paramnr EQ 1107) THEN 
      RUN decode-key4 (paramnr, OUTPUT out-str, OUTPUT status-code). 
  ELSE IF (paramnr GE 700) AND (paramnr LE 1092) THEN 
      RUN decode-key4 (paramnr, OUTPUT out-str, OUTPUT status-code). 
  ELSE IF (paramnr EQ 1095) OR (paramnr EQ 1096) THEN 
      RUN decode-key4 (paramnr, OUTPUT out-str, OUTPUT status-code). 
  ELSE IF (paramnr GE 1094) AND (paramnr LE 2401) THEN 
  DO: 
    IF proforma-inv THEN 
    RUN decode-key5p (paramnr, OUTPUT out-str, OUTPUT status-code). 
    ELSE 
    DO: 
      IF inv-type = 1 THEN 
        RUN decode-key5A (paramnr, OUTPUT out-str, OUTPUT status-code). 
      ELSE IF inv-type = 2 THEN 
        RUN decode-key5B (paramnr, OUTPUT out-str, OUTPUT status-code). 
      ELSE IF inv-type = 3 OR inv-type = 4 THEN 
        RUN decode-key5C (paramnr, OUTPUT out-str, OUTPUT status-code). 
    END. 
  END. 
  IF (status-code GE 1 AND status-code LE 3) OR status-code = 10 THEN 
  DO: 
    RUN find-parameter(paramnr, curr-texte, status-code, INPUT-OUTPUT i). 
  END. 
  IF status-code = 1 THEN 
  DO: 
    m = curr-pos + 1. 
    IF curr-pos GT ntab THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      
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
      DO:
          ASSIGN output-list.str = output-list.str + "".
          CREATE output-list.
    
      END.
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
DEFINE VARIABLE d-length        AS INTEGER INITIAL 24.  
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
    ELSE IF status-code = 10 THEN d-length = n. 
    i = j. 
  END. 
END. 
 
PROCEDURE decode-key1: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE summe LIKE vhp.reservation.depositbez. 
DEFINE VARIABLE t-vat AS DECIMAL INITIAL 0. 
DEFINE BUFFER gmember FOR guest.

  IF paramnr = 100      /* total VAT ON the bill */ THEN 
  DO: 
    IF f-bill THEN 
    DO: 
      IF NOT spbill-flag THEN RUN cal-vat(OUTPUT t-vat). 
      ELSE RUN cal-SPvat(OUTPUT t-vat). 
    END. 
    IF NOT long-digit THEN RUN put-string(STRING(t-vat, "->>>,>>>,>>9.99")). 
    ELSE RUN put-string(STRING(t-vat, "->>,>>>,>>>,>>9")). 
  END. 

  ELSE IF paramnr = 361 AND f-resnr /* 2nd deposit */ THEN 
  DO: 
    IF NOT long-digit THEN 
         RUN put-string(STRING(vhp.reservation.depositgef2, "->>,>>>,>>9.99")). 
    ELSE RUN put-string(STRING(vhp.reservation.depositgef2, "->,>>>,>>>,>>9")). 
  END. 
  
  ELSE IF paramnr = 362 AND f-resnr /* limitdate */ 
    THEN RUN put-string(STRING(vhp.reservation.limitdate2)). 
  
  ELSE IF paramnr = 365 /* today's exchange rate */ THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
         IF price-decimal = 0 THEN 
           RUN put-string(STRING(exchg-rate, ">>,>>9.99")). 
         ELSE RUN put-string(STRING(exchg-rate, ">>,>>9.999999")). 
    END. 
    ELSE RUN put-string(STRING(exchg-rate, ">,>>>,>>9")). 
  END. 
  ELSE IF (paramnr = 366 OR paramnr = 367) AND f-resnr  /* deposit refund / paid */ THEN 
  DO: 
    summe = (vhp.reservation.depositbez + vhp.reservation.depositbez2). 
    IF NOT long-digit THEN RUN put-string(STRING(summe, "->>,>>>,>>9.99")). 
    ELSE RUN put-string(STRING(summe, "->,>>>,>>>,>>9")). 
  END. 
  
  ELSE IF paramnr = 380 AND f-resline /* total price per vhp.res-line */ THEN 
  DO: 
    summe = (vhp.res-line.zipreis * vhp.res-line.zimmeranz * vhp.res-line.anztage). 
    RUN put-string(STRING(summe), "->,>>>,>>>,>>9.99"). 
  END. 
  ELSE IF paramnr = 381 /* total price OF a vhp.reservation) */ THEN 
  DO: 
    summe = 0. 
    FOR EACH vhp.res-line WHERE vhp.res-line.resnr = vhp.bill.resnr 
        AND vhp.res-line.active-flag LE 1 NO-LOCK: 
      summe = summe + (vhp.res-line.zipreis * vhp.res-line.zimmeranz * vhp.res-line.anztage). 
    END. 
    RUN put-string(STRING(summe, "->>,>>>,>>9.99")). 
  END. 
 
  ELSE IF paramnr = 382      /* Telephone number */   THEN 
  DO: 
      IF AVAILABLE vhp.guest THEN 
        RUN put-string(STRING(vhp.guest.telefon,"x(24)")). 
  END. 
 
  ELSE IF paramnr = 383 AND f-resnr     /* vhp.reservation user-ID*/ 
    THEN RUN put-string(TRIM(vhp.reservation.useridanlage)). 
  ELSE IF paramnr = 386      /* resnr */ 
    THEN RUN put-string(STRING(vhp.bill.resnr, ">>,>>>,>>9")). 

  ELSE IF paramnr = 397 AND f-resnr     /* ETA flight*/ 
    THEN RUN put-string(SUBSTR(vhp.res-line.flight-nr,1,6)). 

  ELSE IF paramnr = 413 AND f-resline THEN /* guest mobile number */
  DO:
    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
    RUN put-string(STRING(gmember.mobil-telefon,"x(16)")).
  END.

  ELSE IF paramnr = 414 AND f-resline      /* night of stay */ 
    THEN RUN put-string(STRING(vhp.res-line.abreise - vhp.res-line.ankunft, ">>9")). 

END. 
 
PROCEDURE decode-key2: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE n AS INTEGER. 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = paramnr NO-LOCK. 
  IF paramnr = 601           /* page      */  THEN /*page STREAM s1*/ . 
  ELSE IF paramnr = 602      /* page NO   */ 
    /*THEN RUN put-string(STRING(page-number(s1))). */
    THEN RUN put-string(STRING(curr-page)). 
  ELSE IF paramnr = 603 THEN /* Tabulator */ status-code = 1. 
  
  ELSE IF paramnr = 604      /* today's DATE */ 
    THEN RUN put-string(STRING(TODAY)). 
  ELSE IF paramnr = 1110     /* today's Billing Date */ 
    THEN RUN put-string(STRING(billdate)). 
  
  ELSE IF paramnr = 605     /* time token   */ 
    THEN RUN put-string(STRING(TIME,"HH:MM:SS")). 
  ELSE IF paramnr = 606      /* letter's DATE */ 
    THEN RUN put-string(STRING(TODAY)). 
  ELSE IF paramnr = 607      /* billing instruction */ THEN 
  DO: 
    IF AVAILABLE vhp.res-line AND vhp.res-line.code NE "" THEN 
    DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 AND vhp.queasy.number1 = 
        INTEGER(vhp.res-line.code) NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN RUN put-string(vhp.queasy.char1). 
    END. 
  END. 
  ELSE IF paramnr = 608 THEN /* letter start   */ status-code = -1. 
  ELSE IF paramnr = 609 THEN /* letter END     */ status-code = -2. 
  ELSE IF paramnr = 616      /* left margin ON */ THEN 
  DO: 
    f-lmargin = YES. 
    status-code = 3. 
  END. 
  ELSE IF paramnr = 617 THEN /* left margin off */ f-lmargin = NO. 
  ELSE IF (paramnr GE 618) AND (paramnr LE 629) /* vhp.printcod */ THEN 
  DO: 
    FIND FIRST vhp.printcod WHERE vhp.printcod.emu = vhp.printer.emu 
      AND vhp.printcod.code = vhp.htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.printcod THEN RUN put-string(TRIM(printcod.contcod)). 
  END. 
  ELSE IF paramnr = 630      /* complete addr */ THEN 
  DO: 
    RUN put-string(TRIM(vhp.guest.adresse1)). 
    IF headloop = 0 THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
      curr-pos = 1. 
    END. 
    IF f-lmargin THEN DO n = 1 TO lmargin: 
      RUN put-string(" "). 
    END. 
    RUN put-string(TRIM(vhp.guest.adresse2)). 
    IF headloop = 0 THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + "".
      CREATE output-list.
      curr-line = curr-line + 1. 
      curr-pos = 1. 
    END. 
    curr-line = curr-line + 1. 
    curr-pos = 1. 
    IF f-lmargin THEN DO n = 1 TO lmargin: 
      RUN put-string(" "). 
    END. 
    RUN put-string(TRIM(vhp.guest.adresse3)). 
  END. 
  ELSE IF paramnr = 635      /* birth DATE */ THEN
  DO:
    IF guest.geburtdatum1 NE ? THEN RUN put-string(STRING(vhp.guest.geburtdatum1)). 
    ELSE RUN put-string("          ").
  END.
  ELSE IF paramnr = 637      /* name contact */ THEN 
  DO: 
   FIND FIRST vhp.akt-kont WHERE vhp.akt-kont.gastnr = guest.gastnr 
     AND vhp.akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
   IF AVAILABLE vhp.akt-kont THEN 
     RUN put-string(akt-kont.name + ", " + vhp.akt-kont.vorname 
            + " " + vhp.akt-kont.anrede). 
  END. 
  ELSE IF paramnr = 638      /* guest name */  THEN 
  DO: 
  DEFINE BUFFER rline FOR vhp.res-line. 
    IF proforma-inv THEN 
    DO: 
      FIND FIRST rline WHERE rline.resnr = resnr AND rline.reslinnr = reslinnr 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE rline THEN 
      FIND FIRST rline WHERE rline.resnr = resnr AND rline.resstatus NE 9 
        AND rline.resstatus NE 10 AND rline.resstatus NE 12
        AND rline.resstatus NE 99 NO-LOCK NO-ERROR. 
      RUN put-string(TRIM(rline.name)). 
    END. 
    ELSE RUN put-string(TRIM(vhp.guest.name)). 
  END. 
  ELSE IF paramnr = 639      /* guest firstname */ 
    THEN RUN put-string(TRIM(vhp.guest.vorname1)). 
  ELSE IF paramnr = 641      /* guest TITLE */ 
    THEN RUN put-string(TRIM(vhp.guest.anrede1)). 
  ELSE IF paramnr = 643      /* address1 */ 
    THEN RUN put-string(TRIM(vhp.guest.adresse1)). 
  ELSE IF paramnr = 644      /* address2 */ 
    THEN RUN put-string(TRIM(vhp.guest.adresse2)). 
  ELSE IF paramnr = 645      /* address3 */ 
    THEN RUN put-string(TRIM(vhp.guest.adresse3)). 
  ELSE IF paramnr = 646      /* land */ 
    THEN RUN put-string(TRIM(vhp.guest.land)). 
  ELSE IF paramnr = 647      /* PLZ */ 
    THEN RUN put-string(STRING(vhp.guest.plz)). 
  ELSE IF paramnr = 648      /* city */ 
    THEN RUN put-string(TRIM(vhp.guest.wohnort)). 
END.
 
PROCEDURE decode-key3: 
DEFINE INPUT  PARAMETER paramnr     AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str     AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE saldo               LIKE vhp.bill.saldo. 
DEFINE VARIABLE i                   AS INTEGER. 
DEFINE VARIABLE bemerk              AS CHAR.
DEFINE BUFFER guest1  FOR vhp.guest. 
DEFINE BUFFER gmember FOR vhp.guest.

  RELEASE gmember.
  IF f-resline THEN 
    FIND FIRST gmember WHERE gmember.gastnr = vhp.res-line.gastnrmember NO-LOCK. 

  IF paramnr = 650 THEN /* vhp.reservation start */ status-code = 6. 
  ELSE IF paramnr = 651 THEN /* vhp.reservation END   */ status-code = 7. 
  ELSE IF paramnr = 652 AND f-resnr /* Res Type */ THEN 
  DO: 
    RUN put-string(STRING(vhp.reservation.resart)).  /*   ergaenzen !!!! */ 
  END. 
  ELSE IF paramnr = 653 AND f-resnr      /* Ref DATE */ 
    THEN RUN put-string(STRING(vhp.reservation.refdatum)). 
  ELSE IF paramnr = 654      /* vhp.arrangement */ AND f-resline 
    THEN RUN put-string(TRIM(vhp.res-line.arrangement)). 
 
  ELSE IF paramnr = 655      /* Arrival DATE */ AND f-resline THEN 
  DO: 
    IF AVAILABLE bill AND vhp.bill.resnr GT 0 AND vhp.bill.reslinnr = 0 THEN 
      RUN put-string(STRING(master-ankunft)). 
    ELSE 
    DO: 
    DEF VAR ank-str AS CHAR. 
      ank-str = STRING(vhp.res-line.ankunft). 
      IF vhp.res-line.ankzeit NE 0 AND NOT short-arrival 
        THEN ank-str = ank-str + " " + STRING(vhp.res-line.ankzeit,"HH:MM"). 
      RUN put-string(ank-str). 
    END. 
  END. 
 
  ELSE IF paramnr = 656      /* Departure DATE */ AND f-resline THEN 
  DO: 
    IF AVAILABLE bill AND vhp.bill.resnr GT 0 AND vhp.bill.reslinnr = 0 THEN 
      RUN put-string(STRING(master-abreise)). 
    ELSE 
    DO: 
    DEF VAR abr-str AS CHAR. 
      abr-str = STRING(vhp.res-line.abreise). 
      IF vhp.res-line.abreisezeit NE 0 AND NOT short-depart
        THEN abr-str = abr-str + " " + STRING(vhp.res-line.abreisezeit,"HH:MM"). 
      RUN put-string(abr-str). 
    END. 
  END. 
 
  ELSE IF paramnr = 657      /* Cat & Anzahl */ AND f-resline THEN 
  DO: 
    FIND FIRST vhp.zimkateg WHERE vhp.zimkateg.zikatnr = vhp.res-line.zikatnr NO-LOCK. 
    RUN put-string(vhp.zimkateg.kurzbez + " / " + STRING(vhp.res-line.zimmeranz)). 
  END. 
 
  ELSE IF paramnr = 658      /* Room RAte */ AND f-resline THEN 
  DO: 
    DEF VAR WI-gastnr  AS INTEGER NO-UNDO INITIAL 0.
    DEF VAR IND-gastnr AS INTEGER NO-UNDO INITIAL 0.
    DEF BUFFER gast    FOR vhp.guest. 
    FIND FIRST htparam WHERE htparam.paramnr = 109 NO-LOCK.
    WI-gastnr = htparam.finteger.
    FIND FIRST htparam WHERE htparam.paramnr = 123 NO-LOCK.
    IND-gastnr = htparam.finteger.
    FIND FIRST gast WHERE gast.gastnr = vhp.res-line.gastnr NO-LOCK. 
    IF gast.karteityp = 0 OR gast.gastnr = WI-gastnr
        OR gast.gastnr = IND-gastnr THEN 
      RUN put-string(TRIM(STRING(vhp.res-line.zipreis, ">>>,>>>,>>9.99"))). 
    ELSE IF vhp.res-line.gastnrmember = vhp.res-line.gastnrpay THEN
      RUN put-string(TRIM(STRING(vhp.res-line.zipreis, ">>>,>>>,>>9.99"))). 
    ELSE RUN put-string(STRING("", "x(14)")). 
  END. 
 
  ELSE IF paramnr = 660 AND f-resnr      /* deposit */ 
    THEN RUN put-string(STRING(vhp.reservation.depositgef, "->,>>>,>>>,>>9")). 
  ELSE IF paramnr = 661 AND f-resnr      /*  Due DATE */ 
    THEN RUN put-string(STRING(vhp.reservation.limitdate)). 
  ELSE IF paramnr = 662      /* RoomNo */ AND f-resline 
    THEN RUN put-string(TRIM(vhp.res-line.zinr)). 
  ELSE IF paramnr = 663      /* Persons */ AND f-resline 
    THEN RUN put-string(STRING(vhp.res-line.erwachs + vhp.res-line.gratis)). 
  ELSE IF paramnr = 664      /* Bill Receiver */ THEN 
  DO: 
  DEFINE BUFFER mbill FOR vhp.bill. 
    IF proforma-inv THEN 
    DO: 
      FIND FIRST mbill WHERE mbill.resnr = resnr AND mbill.reslinnr = 0 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE mbill THEN 
        FIND FIRST guest1 WHERE guest1.gastnr = mbill.gastnr NO-LOCK. 
      ELSE FIND FIRST guest1 WHERE guest1.gastnr = vhp.reservation.gastnr NO-LOCK. 
      RUN put-string(guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1 
                 + guest1.anredefirma). 
    END. 
    ELSE IF f-resline AND reslinnr GT 0 THEN 
    DO:
      FIND FIRST guest1 WHERE guest1.gastnr = vhp.res-line.gastnrpay NO-LOCK. 
      RUN put-string(guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1 
                 + guest1.anredefirma). 
    END. 
    ELSE IF /* paramnr = 664 */ f-bill THEN 
    DO: 
    DEFINE VARIABLE billname AS CHAR. 
      FIND FIRST guest1 WHERE guest1.gastnr = vhp.bill.gastnr NO-LOCK. 
      billname = guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1 
        + guest1.anredefirma. 
      IF guest1.karteityp GT 0 AND f-resline AND print-member THEN 
      DO: 
        IF AVAILABLE gmember AND gmember.gastnr NE guest1.gastnr 
          AND gmember.karteityp = 0 THEN 
          billname = billname + " / " + vhp.res-line.name. 
      END.
    END. 
    RUN put-string(billname). 
  END. 
  ELSE IF paramnr = 665      /*  ResNo */ 
/*    THEN RUN put-string(STRING(vhp.bill.resnr)). */
      THEN RUN put-string(STRING(resnr)).

  ELSE IF paramnr = 666 AND f-resnr /*  Reserved Guest */ THEN 
  DO: 
    FIND FIRST guest1 WHERE guest1.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-gname(guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1 
                 + guest1.anredefirma). 
 
  END. 
  ELSE IF paramnr = 667 AND f-resnr /*  vhp.reservation groupname */ THEN 
  DO: 
    RUN put-string(TRIM(vhp.reservation.groupname)). 
  END. 
  ELSE IF paramnr = 668 THEN /* length OF bill description */ status-code = 10. 
  ELSE IF paramnr = 670 THEN /* debt start */ status-code = 8. 
  ELSE IF paramnr = 671 THEN /* debt END   */ status-code = 9. 
  ELSE IF paramnr = 672      /* bill DATE */ AND f-bill 
    THEN RUN put-string(STRING(vhp.bill.datum)). 
  ELSE IF paramnr = 673      /* bill NO */ AND f-bill THEN 
  DO: 
    IF vhp.bill.flag = 0 THEN 
    DO: 
      RUN put-string(STRING(vhp.bill.rechnr)). 
      RUN put-string(" / "). 
      RUN put-string(STRING(vhp.bill.printnr)). 
    END. 
    ELSE IF vhp.bill.flag = 1 THEN 
    DO: 
    DEFINE VARIABLE rechnr-str AS CHAR FORMAT "x(24)". 
      rechnr-str = STRING(vhp.bill.rechnr)
         + translateExtended ("(DUPLICATE)",lvCAREA,"").
      RUN put-string(rechnr-str).
    END. 
  END. 
  ELSE IF paramnr = 674      /* bill balance */ THEN 
  DO: 
    saldo = 0. 
    IF f-bill THEN 
    DO: 
      FIND FIRST vhp.bill WHERE vhp.bill.rechnr = rechnr NO-LOCK. 
      saldo = vhp.bill.saldo. 
    END. 
    IF NOT long-digit THEN 
      RUN put-string(STRING(saldo, "->>>,>>>,>>9.99")). 
    ELSE RUN put-string(STRING(saldo, "->>>,>>>,>>>,>>9")). 
  END. 
  ELSE IF paramnr = 680      /* name contact */ THEN 
  DO: 
   FIND FIRST vhp.akt-kont WHERE vhp.akt-kont.gastnr = vhp.guest.gastnr 
     AND vhp.akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
   IF AVAILABLE vhp.akt-kont THEN RUN put-string(TRIM(akt-kont.name)). 
  END. 
  ELSE IF paramnr = 681      /* name contact */ THEN 
  DO: 
   FIND FIRST vhp.akt-kont WHERE vhp.akt-kont.gastnr = guest.gastnr 
     AND vhp.akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
   IF AVAILABLE vhp.akt-kont THEN RUN put-string(TRIM(akt-kont.vorname)). 
  END. 
  ELSE IF paramnr = 682      /* name contact */ THEN 
  DO: 
   FIND FIRST vhp.akt-kont WHERE vhp.akt-kont.gastnr = guest.gastnr 
     AND vhp.akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
   IF AVAILABLE vhp.akt-kont THEN RUN put-string(TRIM(akt-kont.funktion)). 
  END. 
  ELSE IF paramnr = 683      /* name contact */ THEN 
  DO: 
   FIND FIRST vhp.akt-kont WHERE vhp.akt-kont.gastnr = guest.gastnr 
     AND vhp.akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
   IF AVAILABLE vhp.akt-kont THEN RUN put-string(TRIM(akt-kont.abteilung)). 
  END. 
  ELSE IF paramnr = 684      /* name contact */ THEN 
  DO: 
   FIND FIRST vhp.akt-kont WHERE vhp.akt-kont.gastnr = guest.gastnr 
     AND vhp.akt-kont.hauptkontakt = YES NO-LOCK NO-ERROR. 
   IF AVAILABLE vhp.akt-kont THEN RUN put-string(TRIM(akt-kont.anrede)). 
  END. 
  ELSE IF paramnr = 686      /* room detailed description */ AND f-resline THEN 
  DO: 
    FIND FIRST vhp.zimmer WHERE vhp.zimmer.zinr = vhp.res-line.zinr NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.zimmer THEN RUN put-string(TRIM(vhp.zimmer.bezeich)). 
  END. 
  ELSE IF paramnr = 689      /* company name */ THEN 
  DO: 
    IF guest.karteityp GT 0 THEN RUN put-string(TRIM(vhp.guest.name)). 
  END. 
  ELSE IF paramnr = 690      /* company TITLE */ THEN
    RUN put-string(TRIM(vhp.guest.anredefirma)). 
  ELSE IF paramnr = 691      /* Fax */           THEN
    RUN put-string(TRIM(vhp.guest.fax)). 
  ELSE IF paramnr = 692      /* guest comments */ THEN 
  DO: 
    bemerk = "". 
    DO i = 1 TO length(vhp.guest.bemerk): 
      IF SUBSTR(vhp.guest.bemerk,i,1) = chr(10) THEN bemerk = bemerk + " ". 
      ELSE bemerk = bemerk + SUBSTR(vhp.guest.bemerk,i,1). 
    END. 
    RUN put-string(SUBSTR(TRIM(bemerk), 1, 48)). 
  END. 

  ELSE IF paramnr = 693      /* GCF NO */ THEN
    RUN put-string(STRING(vhp.guest.gastnr)). 
  
  ELSE IF paramnr = 694      /* nation*/ THEN
  DO:
    IF AVAILABLE gmember THEN RUN put-string(TRIM(gmember.nation1)).
    ELSE RUN put-string(TRIM(vhp.guest.nation1)).
  END.

  ELSE IF paramnr = 695      /* Type of Document */ THEN
  DO:
    IF AVAILABLE gmember THEN RUN put-string(TRIM(gmember.geburt-ort1)). 
    ELSE RUN put-string(TRIM(vhp.guest.geburt-ort1)). 
  END.

  ELSE IF paramnr = 696      /* occupation */ THEN
  DO:
    IF AVAILABLE gmember THEN RUN put-string(TRIM(gmember.beruf)). 
    ELSE RUN put-string(TRIM(vhp.guest.beruf)). 
  END.

  ELSE IF paramnr = 697      /* Type OF ID */ THEN
  DO:
    IF AVAILABLE gmember THEN RUN put-string(TRIM(gmember.ausweis-art)). 
    ELSE RUN put-string(TRIM(vhp.guest.ausweis-art)). 
  END.
  ELSE IF paramnr = 698      /* ID Number */  THEN
  DO:
    IF AVAILABLE gmember THEN RUN put-string(TRIM(gmember.ausweis-nr1)). 
    ELSE RUN put-string(TRIM(vhp.guest.ausweis-nr1)). 
  END.
  ELSE IF paramnr = 699      /* car licence */ THEN
  DO:
    IF AVAILABLE gmember THEN RUN put-string(TRIM(gmember.autonr)). 
    ELSE RUN put-string(TRIM(vhp.guest.autonr)). 
  END.
END. 
 
PROCEDURE decode-key4: 
DEFINE INPUT PARAMETER paramnr      AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str     AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 

DEFINE VARIABLE i                   AS INTEGER           NO-UNDO. 
DEFINE VARIABLE pos1                AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE bemerk              AS CHAR              NO-UNDO. 
DEFINE VARIABLE gname               AS CHAR INITIAL ""   NO-UNDO. 
DEFINE VARIABLE voucher             AS CHAR INITIAL ""   NO-UNDO. 
DEFINE VARIABLE vat-str             AS CHAR INITIAL ""   NO-UNDO.

DEFINE BUFFER resline  FOR vhp.res-line. 
DEFINE BUFFER gmember  FOR vhp.guest.
DEFINE BUFFER rsvguest FOR vhp.guest.

  IF paramnr = 711 THEN
  DO:
    IF f-bill THEN
    DO:
        FIND FIRST gmember WHERE gmember.gastnr = bill.gastnr NO-LOCK.
        RUN put-string(STRING(gmember.sternzeichen, "x(20)")).
    END.
    ELSE RUN put-string(STRING("", "x(20)")).
  END.

  ELSE IF paramnr = 713 AND f-resline     /* ETA time*/ 
    THEN RUN put-string(SUBSTR(vhp.res-line.flight-nr,7,5)). 
  ELSE IF paramnr = 714 AND f-resline     /* ETD flight*/ 
    THEN RUN put-string(SUBSTR(vhp.res-line.flight-nr,12,6)). 
  ELSE IF paramnr = 715 AND f-resline     /* ETD time*/ 
    THEN RUN put-string(SUBSTR(vhp.res-line.flight-nr,18,5)). 

  ELSE IF paramnr = 717            /* RmSharer Indicator */ 
    THEN RUN put-string("(R)"). 

  ELSE IF paramnr = 725 AND f-resline THEN /* birth place */
  DO:
    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
    RUN put-string(STRING(gmember.telex,"x(24)")).
  END.

  ELSE IF paramnr = 726 AND f-resline THEN /* passport expired date */
  DO:
    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
    IF gmember.geburtdatum2 NE ? THEN 
        RUN put-string(STRING(gmember.geburtdatum2,"99/99/9999")).
    ELSE RUN put-string(STRING("","x(10)")).
  END.

  ELSE IF paramnr = 730 AND f-resline THEN /* purpose of stay */
  DO:
  DEF VAR ct  AS CHAR   INITIAL "" NO-UNDO.
  DEF VAR anz AS INTEGER           NO-UNDO.
    DO anz = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
      ct = ENTRY(anz, res-line.zimmer-wunsch, ";").
      IF SUBSTR(ct,1,8) = "segm_pur" THEN 
      DO:
        ct = SUBSTR(ct,9).
        FIND FIRST queasy WHERE queasy.KEY = 143 
          AND queasy.number1 = INTEGER(ct) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN ct = queasy.char3.
        LEAVE.
      END.
    END.
    RUN put-string(STRING(ct, "x(12)")).
  END.

  ELSE IF paramnr = 731 AND f-resline THEN /* guest mobile number */
  DO:
    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
    RUN put-string(STRING(gmember.mobil-telefon,"x(16)")).
  END.

  ELSE IF paramnr = 733 AND f-resline THEN /* guest's company name  */
  DO:
    FIND FIRST gmember WHERE gmember.gastnr = res-line.gastnrmember NO-LOCK.
    IF gmember.master-gastnr NE 0 THEN
    DO:
    DEF BUFFER gbuff FOR guest.
      FIND FIRST gbuff WHERE gbuff.gastnr = gmember.master-gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE gbuff THEN
      RUN put-string(STRING((gbuff.NAME + ", " + gbuff.anredefirma),"x(24)")).
    END.
  END.

  ELSE IF paramnr = 743       /* Adult */ AND f-resline 
    THEN RUN put-string(STRING(vhp.res-line.erwachs)). 
  ELSE IF paramnr = 746       /* Complimentary */ AND f-resline 
    THEN RUN put-string(STRING(vhp.res-line.gratis)). 
 
  ELSE IF paramnr = 759 AND f-resnr /*  Reserved Guest address 1 */ THEN 
  DO: 
    FIND FIRST rsvguest WHERE rsvguest.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-string(rsvguest.adresse1).  
  END. 
  ELSE IF paramnr = 760 AND f-resnr /*  Reserved Guest Address 2 */ THEN 
  DO: 
    FIND FIRST rsvguest WHERE rsvguest.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-string(rsvguest.adresse2).  
  END. 
  ELSE IF paramnr = 761 AND f-resnr /*  Reserved Guest Address 3 */ THEN 
  DO: 
    FIND FIRST rsvguest WHERE rsvguest.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-string(rsvguest.adresse3).  
  END. 
  ELSE IF paramnr = 762 AND f-resnr /*  Reserved Guest City */ THEN 
  DO: 
    FIND FIRST rsvguest WHERE rsvguest.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-string(rsvguest.wohnort).  
  END. 
  ELSE IF paramnr = 763 AND f-resnr /*  Reserved Guest Zip Code */ THEN 
  DO: 
    FIND FIRST rsvguest WHERE rsvguest.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-string(rsvguest.plz).  
  END. 
  ELSE IF paramnr = 765 AND f-resnr /*  Reserved Guest Country */ THEN 
  DO: 
    FIND FIRST rsvguest WHERE rsvguest.gastnr = vhp.reservation.gastnr NO-LOCK. 
    RUN put-string(rsvguest.land).  
  END. 
  ELSE IF paramnr = 766 AND f-resnr /*  CreditCard Number and Expiry */ THEN 
  DO: 
    FIND FIRST gmember WHERE gmember.gastnr = vhp.res-line.gastnrmember NO-LOCK. 
    IF gmember.ausweis-nr2 NE "" THEN
    DO:
      DEF VAR cc-str    AS CHAR                NO-UNDO.
      DEF VAR cc-nr     AS CHAR    INITIAL ""  NO-UNDO.
      DEF VAR mm        AS INTEGER INITIAL 0   NO-UNDO.
      DEF VAR yy        AS INTEGER INITIAL 0   NO-UNDO.
      DEF VAR cc-valid  AS LOGICAL INITIAL YES NO-UNDO.
      ASSIGN
        cc-str = ENTRY(1, gmember.ausweis-nr2, "|")
        cc-nr  = ENTRY(2, cc-str, "\")
        mm     = INTEGER(SUBSTR(ENTRY(3, cc-str, "\"),1,2)) 
        yy     = INTEGER(SUBSTR(ENTRY(3, cc-str, "\"),3)) NO-ERROR
      .
      IF cc-nr = "" THEN cc-valid = NO.
      IF cc-valid THEN IF yy LT YEAR(TODAY) THEN cc-valid = NO.
      IF cc-valid THEN IF (yy = YEAR(TODAY) AND mm LT MONTH(TODAY)) THEN cc-valid = NO.
      IF cc-valid THEN 
      DO:    
        ASSIGN
          cc-nr = SUBSTR(cc-nr,1,1) 
                + FILL("X", LENGTH(cc-nr) - 5) 
                + SUBSTR(cc-nr, LENGTH(cc-nr) - 3)
          cc-nr = cc-nr + ", " + SUBSTR(ENTRY(3, cc-str, "\"),1,2) + "/"
                + SUBSTR(ENTRY(3, cc-str, "\"),3) NO-ERROR
        .
        RUN PUT-STRING(cc-nr).
      END.
    END.
  END. 

  ELSE IF paramnr = 764 THEN
  DO:
    RUN bill-vatsum.p(rechnr, curr-pos, OUTPUT vat-str).
    RUN put-string(vat-str).
  END.

  ELSE IF paramnr = 847 AND f-resnr THEN /* vhp.reservation Voucher NO */ 
    RUN put-string(vhp.reservation.vesrdepot). 
  ELSE IF paramnr = 849 THEN            /* indicates OF Advance Bill */ 
  DO: 
    FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR.
    IF AVAILABLE master THEN RUN read-proforma-inv. 
    ELSE RUN read-proforma-inv1.
    proforma-inv = YES. 
  END. 
 
  ELSE IF paramnr = 1087      /* email */ 
    THEN RUN put-string(TRIM(vhp.guest.email-adr)). 
  ELSE IF paramnr = 1088 AND f-resnr      /* source */ 
    THEN RUN put-string(STRING(vhp.reservation.source-code)). 
  ELSE IF paramnr = 1091      /* vhp.res-line comment */ AND f-resline THEN 
  DO: 
    bemerk = "". 
    DO i = 1 TO length(vhp.res-line.bemerk): 
      IF SUBSTR(vhp.res-line.bemerk,i,1) = chr(10) THEN bemerk = bemerk + " ". 
      ELSE bemerk = bemerk + SUBSTR(vhp.res-line.bemerk,i,1). 
    END.
    DO i = 1 TO c-length:
        IF LENGTH(bemerk) LT i THEN RUN put-string(" ").
        ELSE RUN put-string(SUBSTR(bemerk,i,1)).
    END.
/*  OLD: RUN put-string(SUBSTR(TRIM(bemerk), 1, 48)). */
  END. 
  ELSE IF paramnr = 1092 AND f-resnr /* vhp.reservation comment */ THEN 
  DO: 
    bemerk = "". 
    DO i = 1 TO length(vhp.reservation.bemerk): 
      IF SUBSTR(vhp.reservation.bemerk,i,1) = chr(10) THEN bemerk = bemerk + " ". 
      ELSE bemerk = bemerk + SUBSTR(vhp.reservation.bemerk,i,1). 
    END. 
    RUN put-string(SUBSTR(TRIM(bemerk), 1, 48)). 
  END. 
 
  ELSE IF paramnr = 1077      /* Registration NO */ AND f-bill THEN 
  DO: 
    RUN put-string(STRING(vhp.bill.rechnr2)). 
  END. 
 
  ELSE IF paramnr = 1078      /* Disc IN % TO Publish Rate */ AND f-bill THEN 
  DO: 
  DEF VAR discval AS DECIMAL INITIAL 0. 
  DEF VAR do-it AS LOGICAL INITIAL YES. 
  DEF VAR publish-rate AS DECIMAL INITIAL 0. 
  DEF BUFFER mresline FOR vhp.res-line. 
     IF vhp.bill.flag = 0 AND vhp.bill.zinr NE ""  THEN 
     DO: 
       FIND FIRST mresline WHERE mresline.resnr = vhp.bill.resnr 
           AND mresline.reslinnr = vhp.bill.parent-nr NO-LOCK. 
       FIND FIRST vhp.guest-pr WHERE vhp.guest-pr.gastnr = vhp.reservation.gastnr 
         NO-LOCK NO-ERROR. 
       IF AVAILABLE vhp.guest-pr AND mresline.zipreis > 0 THEN 
       DO: 
         FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "arrangement" 
           AND vhp.reslin-queasy.resnr = vhp.bill.resnr 
           AND vhp.reslin-queasy.reslinnr = vhp.bill.parent-nr NO-LOCK NO-ERROR. 
         do-it = AVAILABLE vhp.reslin-queasy. 
       END. 
       IF do-it AND mresline.zipreis > 0 THEN 
       DO: 
         FIND FIRST vhp.arrangement WHERE vhp.arrangement.arrangement = mresline.arrangement 
           NO-LOCK. 
         FIND FIRST vhp.katpreis WHERE vhp.katpreis.zikatnr = mresline.zikatnr 
           AND vhp.katpreis.argtnr = vhp.arrangement.argtnr 
           AND vhp.katpreis.startperiode LE billdate 
           AND vhp.katpreis.endperiode GE billdate 
           AND vhp.katpreis.betriebsnr = wd-array[WEEKDAY(billdate)] NO-LOCK NO-ERROR. 
         IF NOT AVAILABLE vhp.katpreis THEN 
         FIND FIRST vhp.katpreis WHERE vhp.katpreis.zikatnr = mresline.zikatnr 
           AND vhp.katpreis.argtnr = vhp.arrangement.argtnr 
           AND vhp.katpreis.startperiode LE billdate 
           AND vhp.katpreis.endperiode GE billdate 
           AND vhp.katpreis.betriebsnr = 0 NO-LOCK NO-ERROR. 
         IF AVAILABLE vhp.katpreis THEN publish-rate = 
            get-rackrate(mresline.erwachs, mresline.kind1, mresline.kind2). 
       END. 
       IF publish-rate > 0 THEN 
         discval = (1 - (mresline.zipreis / publish-rate)) * 100. 
       discval = ROUND(discval, 0). 
       IF discval = 0 THEN RUN put-string(" "). 
       ELSE RUN put-string(STRING(discval)). 
     END. 
  END. 
 
  ELSE IF paramnr = 1094 /* vhp.bill-line GuestName */ 
    AND f-bill AND NOT print-all-member THEN 
  DO: 
    IF vhp.bill.resnr GT 0 THEN 
    DO: 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      FIND FIRST resline WHERE resline.resnr = vhp.bill.resnr 
        AND resline.zinr = vhp.bill-line.zinr 
        AND resline.resstatus NE 12 AND resline.resstatus NE 9 
        AND resline.resstatus NE 10
        AND resline.resstatus NE 99 NO-LOCK NO-ERROR. 
    END. 
    ELSE IF vhp.bill-line.zinr NE "" THEN 
    DO: 
      FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
        AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE resline THEN 
      DO: 
        IF vhp.bill.datum GT vhp.bill-line.bill-datum THEN 
        FIND FIRST resline WHERE resline.zinr = vhp.bill-line.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.ankunft LE vhp.bill-line.bill-datum 
          AND resline.abreise GT vhp.bill-line.bill-datum NO-LOCK NO-ERROR. 
        ELSE 
        FIND FIRST resline WHERE resline.zinr = vhp.bill-line.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.ankunft LE vhp.bill-line.bill-datum 
          AND resline.abreise GE vhp.bill-line.bill-datum NO-LOCK NO-ERROR. 
      END. 
    END. 
    IF AVAILABLE resline THEN gname = resline.name. 
    ELSE IF AVAILABLE bline-list THEN gname = bline-list.gname. 
    IF AVAILABLE mainres THEN voucher = mainres.vesrdepot. 
 
    DO i = 1 TO g-length: 

      IF length(gname) LT i THEN ASSIGN output-list.str = output-list.str + " ".
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(gname,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + g-length. 
  END. 
 
  ELSE IF paramnr = 1094  /* vhp.bill-line GuestName */  AND f-bill 
    AND print-all-member THEN 
  DO: 
    FOR EACH resline WHERE resline.resnr = vhp.bill.resnr 
      AND resline.resstatus NE 12 AND resline.resstatus NE 9 
      AND resline.resstatus NE 10 AND resline.resstatus NE 13 
      AND resline.resstatus NE 99
      NO-LOCK BY resline.name BY resline.zinr: 
      gname = resline.name. 
      IF pos1 NE 0 THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + "".
        CREATE output-list.
        
        curr-line = curr-line + 1.
        DO i = 1 TO pos1: 
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
          
        END. 
      END. 
      DO i = 1 TO g-length: 
        IF length(gname) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
        ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(gname,i,1), "x(1)").
      END. 
      ASSIGN output-list.str = output-list.str + STRING(" #", "x(2)").
      ASSIGN output-list.str = output-list.str + STRING(resline.zinr, "x(6)").
      IF pos1 = 0 THEN 
      DO: 
        pos1 = curr-pos - 1. 
        curr-pos = curr-pos + g-length + 7. 
      END. 
    END. 
  END. 
 
  ELSE IF paramnr = 1095 THEN RUN put-string(STRING(bline-nr,">>9")). 
  ELSE IF paramnr = 1096 THEN 
  DO: 
  DEFINE VARIABLE progname AS CHAR. 
  DEFINE VARIABLE str1 AS CHAR. 
  DEFINE VARIABLE str2 AS CHAR. 
  DEF VAR str3 AS CHAR INITIAL "". 
 
    IF briefnr = briefnr2 OR briefnr = briefnr21 THEN
      FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 416 NO-LOCK. 
    ELSE FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 410 NO-LOCK. 
    progname = vhp.htparam.fchar. 
    IF (progname NE "") AND AVAILABLE bill THEN 
    DO: 
      IF progname = "word_chinese.p" THEN 
      DO: 
        IF briefnr = briefnr2 THEN /* Revenue Amount IN Foreign Currency */ 
          RUN VALUE(progname) (bl0-balance1, w-length, OUTPUT str1, OUTPUT str2, 
            OUTPUT str3). 
        ELSE 
        DO: 
          IF bl0-balance NE 0 THEN RUN VALUE(progname) (bl0-balance, w-length, 
            OUTPUT str1, OUTPUT str2, OUTPUT str3). 
          ELSE IF inv-type = 2  /** single line option **/ OR spbill-flag THEN 
          RUN VALUE(progname) (bl-balance, w-length, OUTPUT str1, 
            OUTPUT str2, OUTPUT str3). 
          ELSE RUN VALUE(progname) (vhp.bill.saldo, w-length, OUTPUT str1, 
            OUTPUT str2, OUTPUT str3). 
        END. 
      END. 
      ELSE DO: 
        IF briefnr = briefnr2 OR briefnr = briefnr21 
        THEN /* Revenue Amount IN Foreign Currency */ 
          RUN value(progname) (bl0-balance1, w-length, OUTPUT str1, OUTPUT str2). 
        ELSE 
        DO: 
          IF bl0-balance NE 0 THEN 
            RUN value(progname) (bl0-balance, w-length, OUTPUT str1, OUTPUT str2). 
          ELSE IF inv-type = 2  /** single line option **/ OR spbill-flag THEN 
            RUN value(progname) (bl-balance, w-length, OUTPUT str1, OUTPUT str2). 
          ELSE RUN value(progname) (vhp.bill.saldo, w-length, OUTPUT str1, OUTPUT str2). 
        END. 
      END. 
 
      IF str3 NE "" THEN 
      DO: 
        DO i = 1 TO LENGTH(str3): 
          ASSIGN output-list.str = output-list.str + STRING(SUBSTR(str3,i,1), "x(1)").
        END. 
        ASSIGN output-list.str = output-list.str + " ".
        CREATE output-list.
        curr-line = curr-line + 1.
        DO i = 1 TO (curr-pos - 1): 
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)"). 
        END. 
      END. 
      DO i = 1 TO length(str1): 
        ASSIGN output-list.str = output-list.str + STRING(SUBSTR(str1,i,1), "x(1)").
      END. 
      IF str2 = "" THEN curr-pos = curr-pos + length(str1). 
      ELSE 
      DO: 
        ASSIGN output-list.str = output-list.str + "".
        CREATE output-list.
        
        curr-line = curr-line + 1.
        DO i = 1 TO (curr-pos - 1): 
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
        DO i = 1 TO length(str2): 
          ASSIGN output-list.str = output-list.str + STRING(SUBSTR(str2,i,1), "x(1)").
        END. 
        curr-pos = curr-pos + length(str2). 
      END. 
    END. 
  END. 
 
  ELSE IF paramnr = 1107 THEN  /* vhp.res-line currency code */ 
  DO: 
    DEFINE VARIABLE exrate AS DECIMAL INITIAL 1. 
    DEFINE BUFFER exchg-buff FOR vhp.exrate. 
    IF f-resline THEN 
    DO: 
      IF vhp.res-line.reserve-dec NE 0 THEN 
      DO: 
        IF vhp.res-line.ankunft = billdate THEN 
        DO: 
          FIND FIRST vhp.waehrung WHERE vhp.waehrung.waehrungsnr = vhp.res-line.betriebsnr 
            NO-LOCK NO-ERROR. 
          IF AVAILABLE vhp.waehrung THEN exrate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
          ELSE exrate = vhp.res-line.reserve-dec. 
        END. 
        ELSE 
        DO: 
          FIND FIRST exchg-buff WHERE exchg-buff.datum = vhp.res-line.ankunft 
            AND exchg-buff.artnr = vhp.res-line.betriebsnr NO-LOCK NO-ERROR. 
          IF AVAILABLE exchg-buff THEN exrate = exchg-buff.betrag. 
          ELSE exrate = vhp.res-line.reserve-dec. 
        END. 
      END. 
      ELSE 
      DO: 
        FIND FIRST vhp.waehrung WHERE vhp.waehrung.waehrungsnr = vhp.res-line.betriebsnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.waehrung THEN exrate = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
      END. 
    END. 
 
    IF NOT long-digit THEN 
    DO: 
         IF price-decimal = 0 THEN 
           RUN put-string(STRING(exrate, ">>,>>9.99")). 
         ELSE RUN put-string(STRING(exrate, ">>,>>9.999999")). 
    END. 
    ELSE RUN put-string(STRING(exrate, ">,>>>,>>9")). 
 
  END. 
 
  ELSE IF paramnr = 1105 THEN  /* vhp.res-line currency exchange rate */ 
  DO: 
    IF f-resline THEN 
    DO: 
      FIND FIRST vhp.waehrung WHERE vhp.waehrung.waehrungsnr = vhp.res-line.betriebsnr 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.waehrung THEN 
        RUN put-string(STRING(waehrung.wabkurz,"x(4)")). 
      ELSE RUN put-string(STRING("    ","x(4)")). 
    END. 
    ELSE RUN put-string(STRING("    ","x(4)")). 
  END. 
 
  ELSE IF paramnr = 1589 THEN 
  DO: 
    IF vhp.bill-line.zinr NE "" THEN FIND FIRST mainres 
      WHERE mainres.resnr = vhp.bill-line.massnr NO-LOCK NO-ERROR. 
    IF AVAILABLE mainres THEN voucher = mainres.vesrdepot. 
    DO i = 1 TO v-length: 
      IF length(voucher) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(voucher,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + v-length. 
  END. 
END. 
 
PROCEDURE decode-key5A: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE stime AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE netto AS DECIMAL. 
DEFINE VARIABLE gname AS CHAR INITIAL "". 
DEFINE VARIABLE voucher AS CHAR INITIAL "". 
DEFINE VARIABLE pos1 AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE BUFFER foart FOR vhp.artikel. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE BUFFER guest1 FOR vhp.guest. 
 
  IF paramnr = 1094 AND NOT print-all-member /* vhp.bill-line guest name  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN gname = vhp.res-line.name. 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO:
      IF NOT AVAILABLE vhp.bill-line THEN FIND FIRST vhp.bill-line WHERE 
          vhp.bill-line.rechnr = vhp.bill.rechnr AND vhp.bill-line.zinr NE "" NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE vhp.bill-line THEN FIND FIRST vhp.bill-line WHERE 
          vhp.bill-line.rechnr = vhp.bill.rechnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.bill-line AND vhp.bill-line.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
          AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = vhp.bill-line.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE vhp.bill-line.bill-datum 
          AND resline.abreise GT vhp.bill-line.bill-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN gname = resline.name. 
      END. 
    END. 
    DO i = 1 TO g-length: 
      IF length(gname) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(gname,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + g-length. 
  END. 
 
  ELSE IF paramnr = 1094  /* vhp.bill-line GuestName */ AND print-all-member THEN 
  DO: 
    FOR EACH resline WHERE resline.resnr = vhp.bill.resnr 
      AND resline.resstatus NE 12 AND resline.resstatus NE 9 
      AND resline.resstatus NE 10 AND resline.resstatus NE 13 
      AND resline.resstatus NE 99
      NO-LOCK BY resline.name BY resline.zinr: 
      gname = resline.name. 
      IF pos1 NE 0 THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + "".
        CREATE output-list.
        
        curr-line = curr-line + 1.
        DO i = 1 TO pos1: 
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
      END. 
      DO i = 1 TO g-length: 
        IF LENGTH(gname) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
        ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(gname,i,1), "x(1)").
      END. 
      ASSIGN output-list.str = output-list.str + STRING(" #", "x(2)").
      ASSIGN output-list.str = output-list.str + STRING(resline.zinr, "x(6)").
      IF pos1 = 0 THEN 
      DO: 
        pos1 = curr-pos - 1. 
        curr-pos = curr-pos + g-length + 7. 
      END. 
    END. 
  END. 
 
  ELSE IF paramnr = 1103            /* Arrival DATE  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.res-line.ankunft). 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO: 
      IF vhp.bill-line.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
          AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = vhp.bill-line.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE vhp.bill-line.bill-datum 
          AND resline.abreise GT vhp.bill-line.bill-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN ASSIGN output-list.str = output-list.str + STRING(resline.ankunft). 
        ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)"). 
      END. 
      ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
    END. 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1104            /* Departure DATE  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.res-line.abreise). 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO: 
      IF vhp.bill-line.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = vhp.bill-line.massnr 
          AND resline.reslinnr = vhp.bill-line.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = vhp.bill-line.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE vhp.bill-line.bill-datum 
          AND resline.abreise GT vhp.bill-line.bill-datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN ASSIGN output-list.str = output-list.str + STRING(resline.abreise). 
        ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
      END. 
      ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
    END. 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1117            /* vhp.bill-line Userinit */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.userinit, "x(4)").
    curr-pos = curr-pos + 4. 
  END. 
 
  ELSE IF paramnr = 1380            /* vhp.bill-line VAT */  THEN 
  DO: 
    IF vhp.bill-line.orts-tax NE 0 THEN 
       RUN get-vat(bill-line.origin-id, OUTPUT curr-bl-vat).
    ELSE 
    DO: 
        FIND FIRST foart WHERE foart.artnr = vhp.bill-line.artnr 
          AND foart.departement = vhp.bill-line.departement NO-LOCK NO-ERROR. 
        IF AVAILABLE foart THEN 
        DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
          ELSE curr-bl-vat = 0. 
        END. 
    END. 
    IF curr-bl-vat = 1000 THEN 
      ASSIGN output-list.str = output-list.str + STRING("     ", "x(5)"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING(curr-bl-vat, ">9.99").
    curr-pos = curr-pos + 5. 
  END. 
  ELSE IF paramnr = 1400            /* vhp.bill-line NET Amount */  THEN 
  DO: 
    IF (vhp.artikel.artnr = vat-artnr[1] OR vhp.artikel.artnr = vat-artnr[2] 
        OR vhp.artikel.artnr = vat-artnr[3] OR vhp.artikel.artnr = vat-artnr[4] 
        OR vhp.artikel.artnr = vat-artnr[5])
        AND vhp.artikel.departement = 0 THEN netto = 0. 
    ELSE IF vhp.bill-line.orts-tax NE 0 
      THEN netto = vhp.bill-line.betrag - vhp.bill-line.orts-tax. 
    ELSE 
    DO: 
      FIND FIRST foart WHERE foart.artnr = vhp.bill-line.artnr 
        AND foart.departement = vhp.bill-line.departement NO-LOCK NO-ERROR. 
      IF AVAILABLE foart THEN 
      DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
          ELSE curr-bl-vat = 0. 
      END. 
      netto = vhp.bill-line.betrag / (1 + curr-bl-vat / 100). 
      netto = round(netto, price-decimal). 
    END. 
    bl-netto = bl-netto + netto. 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(netto, "->>,>>>,>>9.99").
      curr-pos = curr-pos + 14. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(netto, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 1401            /* Total Net Sales Amount */ THEN 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-netto, "->>,>>>,>>9.99").
      curr-pos = curr-pos + 14. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-netto, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
 
  ELSE IF paramnr = 1589 THEN 
  DO: 
    FIND FIRST mainres WHERE mainres.resnr = vhp.bill-line.massnr NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE mainres THEN voucher = mainres.vesrdepot. 
    DO i = 1 TO v-length: 
      IF length(voucher) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(voucher,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + v-length. 
  END. 
 
  ELSE IF paramnr = 2304            /* Bill Artnr */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.artnr, ">>>9").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2305            /* qty */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.anzahl, "->>9").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2306            /* Description */  THEN 
  DO: 
    DO i = 1 TO d-length: 
      IF length(bill-line.bezeich) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(bill-line.bezeich,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + d-length. 
  END. 
  ELSE IF paramnr = 2307            /* Price */  THEN 
  DO: 
    IF NOT long-digit THEN ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.epreis, "->,>>>,>>9.99"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.epreis, "->>>>,>>>,>>9").
    curr-pos = curr-pos + 13. 
  END. 
  ELSE IF paramnr = 2308            /* Amount */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO:
      IF longer-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.betrag, "->>>>,>>>,>>9.99").
        curr-pos = curr-pos + 16. 
      END.
      ELSE IF long-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.betrag, "->>>,>>>,>>9.99").
        curr-pos = curr-pos + 15. 
      END.
      ELSE
      DO:
        ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.betrag, "->>,>>>,>>9.99").
        curr-pos = curr-pos + 14. 
      END.
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.betrag, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 2318            /* Foreign Amount */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.fremdwbetrag, "->>,>>9.99").
    curr-pos = curr-pos + 10. 
  END. 
  ELSE IF paramnr = 2309            /* room */  THEN 
  DO: 
    IF /* vhp.bill.zinr NE vhp.bill-line.zinr AND */ vhp.bill-line.zinr NE "" THEN 
      ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.zinr, "x(6)"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING("    ").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2310            /* vhp.bill-line DATE */  THEN 
  DO: 
    IF inv-type EQ 1 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.bill-line.bill-datum). 
    ELSE ASSIGN output-list.str = output-list.str + STRING("        ").
    curr-pos = curr-pos + 8. 
  END. 
  ELSE IF paramnr = 2316  THEN     /* Balance ON the CURRENT vhp.bill-line */ 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>9.99").
      curr-pos = curr-pos + 15. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 2319  THEN  /* Foreign Balance ON CURRENT vhp.bill-line */ 
  DO: 
    IF bline-flag = 0 THEN 
    DO: 
      IF fixrate-flag AND AVAILABLE vhp.res-line AND vhp.res-line.reserve-dec NE 0 
        AND bl0-balance NE 0 THEN 
        bl0-balance1 = bl0-balance / vhp.res-line.reserve-dec.
      IF bl0-balance1 NE 0 THEN 
      DO: 
        IF bl0-balance1 GE 100000 OR bl0-balance1 LE -100000 THEN 
        DO: 
          ASSIGN output-list.str = output-list.str + STRING(bl0-balance1, "->>>,>>>,>>>,>>9.99").
          curr-pos = curr-pos + 16. 
        END. 
        ELSE 
        DO: 
          ASSIGN output-list.str = output-list.str + STRING(bl0-balance1, "->>,>>9.99").
          curr-pos = curr-pos + 10. 
        END. 
      END. 
      ELSE 
      DO: 
        DEFINE VARIABLE fbal AS DECIMAL. 
        fbal = (bl0-balance / exchg-rate). 
        IF fbal GE 100000 OR fbal LE -100000 THEN 
        DO: 
          ASSIGN output-list.str = output-list.str + STRING(fbal, "->>>,>>>,>>>,>>9").
          curr-pos = curr-pos + 16. 
        END. 
        ELSE 
        DO: 
          ASSIGN output-list.str = output-list.str + STRING(fbal, "->>,>>9.99").
          curr-pos = curr-pos + 10. 
        END. 
      END. 
    END. 
    ELSE 
    DO: 
      IF bl-balance1 GE 100000 OR bl-balance1 LE -100000 THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>>,>>>,>>>,>>9").
        curr-pos = curr-pos + 16. 
      END. 
      ELSE 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>,>>9.99").
        curr-pos = curr-pos + 10. 
      END. 
    END. 
  END. 
  ELSE IF paramnr = 2317  THEN       /* Complete Name OF Hotel Guestname */ 
  DO: 
    DEFINE VARIABLE gname1 AS CHAR FORMAT "x(32)". 
    FIND FIRST guest1 WHERE guest1.gastnr = vhp.res-line.gastnrmember NO-LOCK
        NO-ERROR.
    IF AVAILABLE guest1 THEN
    DO:
      gname1 = guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1. 
      RUN put-string(gname1). 
      curr-pos = curr-pos + 32. 
    END.
  END. 
 
  ELSE IF paramnr = 2311            /* CURRENT Time */  THEN 
  DO: 
    stime = STRING(time, "HH:MM"). 
    RUN put-string(stime). 
  END. 

  ELSE IF paramnr = 2312            /* CURRENT User Id */  THEN
    RUN put-string(user-init). 
 
  ELSE IF paramnr = 2401            /* CURRENT User Name */  THEN 
    RUN put-string(STRING(vhp.bediener.username,"x(16)")). 

END. 
 
PROCEDURE decode-key5B: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE VARIABLE stime AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE bezeich AS CHAR. 
DEFINE VARIABLE netto AS DECIMAL. 
DEFINE VARIABLE voucher AS CHAR INITIAL "". 
DEFINE BUFFER foart FOR vhp.artikel. 
DEFINE BUFFER resline FOR vhp.res-line. 
DEFINE BUFFER htp FOR vhp.htparam. 
DEFINE BUFFER guest1 FOR vhp.guest. 
 
  IF paramnr = 1103            /* Arrival DATE  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.res-line.ankunft). 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO: 
      IF bline-list.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = bline-list.massnr 
          AND resline.reslinnr = bline-list.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = bline-list.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE bline-list.datum 
          AND resline.abreise GT bline-list.datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN ASSIGN output-list.str = output-list.str + STRING(resline.ankunft). 
        ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
      END. 
      ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
    END. 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1104            /* Departure DATE  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.res-line.abreise). 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO: 
      IF bline-list.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = bline-list.massnr 
          AND resline.reslinnr = bline-list.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = bline-list.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE bline-list.datum 
          AND resline.abreise GT bline-list.datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN ASSIGN output-list.str = output-list.str + STRING(resline.abreise). 
        ELSE ASSIGN output-list.str = output-list.str + STRING(STRING("", "x(8)")).
      END. 
      ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
    END. 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1380            /* vhp.bill-line VAT */  THEN 
  DO: 
    IF AVAILABLE vhp.bill-line AND vhp.bill-line.orts-tax NE 0 THEN 
      RUN get-vat(bill-line.origin-id, OUTPUT curr-bl-vat).
    ELSE 
    DO: 
        FIND FIRST foart WHERE foart.artnr = bline-list.artnr 
          AND foart.departement = bline-list.dept NO-LOCK NO-ERROR. 
        IF AVAILABLE foart THEN 
        DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
          ELSE curr-bl-vat = 0. 
        END. 
    END. 
    IF curr-bl-vat = 1000 THEN 
      ASSIGN output-list.str = output-list.str + STRING("     ", "x(5)").
    ELSE ASSIGN output-list.str = output-list.str + STRING(curr-bl-vat, ">9.99"). 
    curr-pos = curr-pos + 5. 
  END. 
 
  ELSE IF paramnr = 1400            /* vhp.bill-line NET Amount */  THEN 
  DO: 
    IF bline-list.netto NE 0 THEN netto = bline-list.netto. 
    ELSE IF (bline-list.artnr = vat-artnr[1] OR bline-list.artnr = vat-artnr[2] 
        OR bline-list.artnr = vat-artnr[3] OR bline-list.artnr = vat-artnr[4] 
        OR bline-list.artnr = vat-artnr[5])
        AND bline-list.dept = 0 THEN netto = 0.     
    ELSE IF bline-list.orts-tax NE 0 
      THEN netto = bline-list.saldo - bline-list.orts-tax. 
    ELSE 
    DO: 
      FIND FIRST foart WHERE foart.artnr = bline-list.artnr 
        AND foart.departement = bline-list.dept NO-LOCK NO-ERROR. 
      IF AVAILABLE foart THEN 
      DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
          ELSE curr-bl-vat = 0. 
      END. 
      netto = bline-list.saldo / (1 + curr-bl-vat / 100). 
    END. 
    netto = round(netto, price-decimal). 
    bl-netto = bl-netto + netto. 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(netto, "->>,>>>,>>9.99"). 
      curr-pos = curr-pos + 14. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(netto, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
 
  ELSE IF paramnr = 1401 THEN      /* Total Net Sales Amount */ 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-netto, "->>,>>>,>>9.99").
      curr-pos = curr-pos + 14. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-netto, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
 
  ELSE IF paramnr = 1589 THEN 
  DO: 
    IF bline-list.zinr NE "" THEN FIND FIRST mainres 
      WHERE mainres.resnr = bline-list.massnr NO-LOCK NO-ERROR. 
    IF AVAILABLE mainres THEN voucher = mainres.vesrdepot. 
    DO i = 1 TO v-length: 
      IF length(voucher) LT i THEN ASSIGN output-list.str = output-list.str + STRING(" "). 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(voucher,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + v-length. 
  END. 
 
  ELSE IF paramnr = 2304            /* Bill Artnr */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(0, ">>>>").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2305            /* qty */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(1, "->>9").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2306            /* Description */  THEN 
  DO: 
    /*MT
    IF bline-flag LE 0 THEN RUN enter-single-line.p(OUTPUT bezeich). 
    ELSE bezeich = bline-list.bezeich.
    */
    bezeich = bline-list.bezeich.
    DO i = 1 TO d-length: 
      IF length(bezeich) LT i THEN ASSIGN output-list.str = output-list.str + STRING(" ").
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(bezeich, i, 1), "x(1)").
    END. 
    curr-pos = curr-pos + d-length. 
  END. 
  ELSE IF paramnr = 2307            /* Price */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(0, "->>>>,>>>,>>>").
    curr-pos = curr-pos + 13. 
  END. 
  ELSE IF paramnr = 2308            /* Amount */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO:
      IF longer-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>>>,>>>,>>9.99").
        curr-pos = curr-pos + 16. 
      END.
      ELSE IF long-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>>,>>>,>>9.99").
        curr-pos = curr-pos + 15. 
      END.
      ELSE
      DO:
        ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>,>>>,>>9.99").
        curr-pos = curr-pos + 14. 
      END.
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 2318            /* Foreign Amount */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(bline-list.fsaldo, "->>,>>9.99").
    curr-pos = curr-pos + 10. 
  END. 
  ELSE IF paramnr = 2309            /* room */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING("    ").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2310            /* vhp.bill-line DATE */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING("        ", "x(8)").
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1117            /* vhp.bill-line Userinit */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING("  ", "x(4)").
    curr-pos = curr-pos + 4. 
  END. 
 
  ELSE IF paramnr = 2316 THEN      /* Balance ON the CURRENT vhp.bill-line */ 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>9.99").
      curr-pos = curr-pos + 15. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 2319 THEN  /* Foreign Balance ON CURRENT vhp.bill-line */ 
  DO: 
    IF bl-balance1 GE 100000 OR bl-balance1 LE -100000 THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>>,>>>,>>>,>>9.99").
      curr-pos = curr-pos + 16. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>,>>9.99").
      curr-pos = curr-pos + 10. 
    END. 
  END. 
  ELSE IF paramnr = 2317  THEN       /* Complete Name OF Hotel Guestname */ 
  DO: 
    DEFINE VARIABLE gname AS CHAR FORMAT "x(32)". 
    FIND FIRST guest1 WHERE guest1.gastnr = vhp.res-line.gastnrmember NO-LOCK. 
    gname = guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1. 
    RUN put-string(gname). 
    curr-pos = curr-pos + 32. 
  END. 
 
  ELSE IF paramnr = 2311            /* CURRENT Time */  THEN 
  DO: 
    stime = STRING(time, "HH:MM"). 
    RUN put-string(stime). 
  END. 
 
  ELSE IF paramnr = 2312            /* CURRENT User Id */  THEN 
    RUN put-string(user-init).

  ELSE IF paramnr = 2401            /* CURRENT User Name */  THEN 
    RUN put-string(STRING(vhp.bediener.username,"x(16)")). 

END. 
 
PROCEDURE decode-key5C: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE BUFFER guest1 FOR vhp.guest. 
DEFINE VARIABLE stime AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE netto AS DECIMAL. 
DEFINE VARIABLE pos1 AS INTEGER INITIAL 0 NO-UNDO. 
DEFINE VARIABLE gname AS CHAR INITIAL "". 
DEFINE BUFFER foart FOR vhp.artikel. 
DEFINE BUFFER resline FOR vhp.res-line. 
 
  IF paramnr = 1380            /* vhp.bill-line VAT */  THEN 
  DO: 
    IF bline-list.orts-tax NE 0 THEN 
      RUN get-vat(bline-list.origin-id, OUTPUT curr-bl-vat).
    ELSE 
    DO: 
      FIND FIRST foart WHERE foart.artnr = bline-list.artnr 
        AND foart.departement = bline-list.dept NO-LOCK NO-ERROR. 
      IF AVAILABLE foart THEN 
      DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
          ELSE curr-bl-vat = 0. 
      END. 
    END. 
    IF curr-bl-vat = 1000 THEN 
      ASSIGN output-list.str = output-list.str + STRING("     ", "x(5)"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING(curr-bl-vat, ">9.99").
    curr-pos = curr-pos + 5. 
  END. 
  ELSE IF paramnr = 1400            /* vhp.bill-line NET Amount */  THEN 
  DO: 
    IF (bline-list.artnr = vat-artnr[1] OR bline-list.artnr = vat-artnr[2] 
        OR bline-list.artnr = vat-artnr[3] OR bline-list.artnr = vat-artnr[4] 
        OR bline-list.artnr = vat-artnr[5])
        AND bline-list.dept = 0 THEN netto = 0.     
    ELSE IF bline-list.orts-tax NE 0 
      THEN netto = bline-list.saldo - bline-list.orts-tax. 
    ELSE 
    DO: 
      FIND FIRST foart WHERE foart.artnr = bline-list.artnr 
        AND foart.departement = bline-list.dept NO-LOCK NO-ERROR. 
      IF AVAILABLE foart THEN 
      DO: 
          FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = foart.mwst-code NO-LOCK 
            NO-ERROR. 
          IF AVAILABLE vhp.htparam THEN curr-bl-vat = vhp.htparam.fdecimal. 
          ELSE curr-bl-vat = 0. 
      END. 
      netto = bline-list.saldo / (1 + curr-bl-vat / 100). 
      netto = round(netto, price-decimal). 
    END. 
    bl-netto = bl-netto + netto. 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(netto, "->>,>>>,>>9.99").
      curr-pos = curr-pos + 14. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(netto, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 1401 THEN       /* Total Net Sales Amount */ 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-netto, "->>,>>>,>>9.99").
      curr-pos = curr-pos + 14. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-netto, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
 
  ELSE IF paramnr = 1094 AND NOT print-all-member  /* guest name */  THEN 
  DO: 
    DO i = 1 TO g-length: 
      IF length(bline-list.gname) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(bline-list.gname,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + g-length. 
  END. 
 
  ELSE IF paramnr = 1094  /* vhp.bill-line GuestName */ AND print-all-member THEN 
  DO: 
    FOR EACH resline WHERE resline.resnr = vhp.bill.resnr 
      AND resline.resstatus NE 12 AND resline.resstatus NE 9 
      AND resline.resstatus NE 10 AND resline.resstatus NE 13 
      AND resline.resstatus NE 99
      NO-LOCK BY resline.name BY resline.zinr: 
      gname = resline.name. 
      IF pos1 NE 0 THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + "".
        CREATE output-list.
        curr-line = curr-line + 1.
        DO i = 1 TO pos1: 
          ASSIGN output-list.str = output-list.str + STRING(" ", "x(1)").
        END. 
      END. 
      DO i = 1 TO g-length: 
        IF LENGTH(gname) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
        ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(gname,i,1), "x(1)").
      END. 
      ASSIGN output-list.str = output-list.str + STRING(" #", "x(2)").
      ASSIGN output-list.str = output-list.str + STRING(resline.zinr, "x(6)").
      IF pos1 = 0 THEN 
      DO: 
        pos1 = curr-pos - 1. 
        curr-pos = curr-pos + g-length + 7. 
      END. 
    END. 
  END. 
 
  ELSE IF paramnr = 1103            /* Arrival DATE  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.res-line.ankunft). 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO: 
      IF bline-list.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = bline-list.massnr 
          AND resline.reslinnr = bline-list.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = bline-list.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE bline-list.datum 
          AND resline.abreise GT bline-list.datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN ASSIGN output-list.str = output-list.str + STRING(resline.ankunft). 
        ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
      END. 
      ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
    END. 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1104            /* Departure DATE  */  THEN 
  DO: 
    IF f-resline AND reslinnr GT 0 THEN ASSIGN output-list.str = output-list.str + STRING(vhp.res-line.abreise). 
    ELSE IF f-resline AND reslinnr = 0 THEN 
    DO: 
      IF bline-list.zinr NE "" THEN 
      DO: 
        FIND FIRST resline WHERE resline.resnr = bline-list.massnr 
          AND resline.reslinnr = bline-list.billin-nr NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE resline THEN 
        FIND FIRST resline WHERE resline.zinr = bline-list.zinr 
          AND resline.resstatus NE 12 AND resline.resstatus NE 9 
          AND resline.resstatus NE 10 AND resline.resstatus NE 99
          AND resline.active-flag GE 1 AND resline.active-flag LE 2 
          AND resline.ankunft LE bline-list.datum 
          AND resline.abreise GT bline-list.datum NO-LOCK NO-ERROR. 
        IF AVAILABLE resline THEN ASSIGN output-list.str = output-list.str + STRING(resline.abreise). 
        ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
      END. 
      ELSE ASSIGN output-list.str = output-list.str + STRING("", "x(8)").
    END. 
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1589 THEN 
  DO: 
    DO i = 1 TO v-length: 
      IF length(bline-list.voucher) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(bline-list.voucher,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + v-length. 
  END. 
 
  ELSE IF paramnr = 2304            /* Bill Artnr */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(bline-list.artnr, ">>>9").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2305            /* qty */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(bline-list.anzahl, "->>9").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2306            /* Description */  THEN 
  DO: 
    DO i = 1 TO d-length: 
      IF length(bline-list.bezeich) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(bline-list.bezeich,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + d-length. 
  END. 
  ELSE IF paramnr = 2307            /* Price */  THEN 
  DO: 
    IF NOT long-digit THEN ASSIGN output-list.str = output-list.str + STRING(bline-list.epreis, "->,>>>,>>9.99"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING(bline-list.epreis, "->>>>,>>>,>>9").
    curr-pos = curr-pos + 13. 
  END. 
  ELSE IF paramnr = 2308            /* Amount */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO:
      IF longer-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>>>,>>>,>>9.99").
        curr-pos = curr-pos + 16. 
      END.
      ELSE IF long-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>>,>>>,>>9.99").
        curr-pos = curr-pos + 15. 
      END.
      ELSE
      DO:
        ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>,>>>,>>9.99").
        curr-pos = curr-pos + 14. 
      END.
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bline-list.saldo, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 2318            /* Foreign Amount */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(bline-list.fsaldo, "->>,>>9.99").
    curr-pos = curr-pos + 10. 
  END. 
  ELSE IF paramnr = 2309            /* room */  THEN 
  DO: 
    IF bline-list.zinr NE "" THEN 
      ASSIGN output-list.str = output-list.str + STRING(bline-list.zinr, "x(6)"). 
    ELSE ASSIGN output-list.str = output-list.str + "    ".
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2310            /* vhp.bill-line DATE */  THEN 
  DO: 
    IF bline-list.datum = ? THEN 
      ASSIGN output-list.str = output-list.str + STRING("        ", "x(8)"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING(bline-list.datum).
    curr-pos = curr-pos + 8. 
  END. 
  ELSE IF paramnr = 1117            /* vhp.bill-line Userinit */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(bline-list.userinit, "x(4)").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2316            /* Balance ON the CURRENT vhp.bill-line */ 
  THEN 
  DO: 
    IF bline-flag = -1 THEN 
    DO: 
      IF NOT long-digit THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>9.99").
        curr-pos = curr-pos + 15. 
      END. 
      ELSE 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>>,>>9").
        curr-pos = curr-pos + 16. 
      END. 
    END. 
    ELSE IF bline-flag = 0 THEN 
    DO: 
      IF NOT long-digit THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl0-balance, "->>,>>>,>>9.99").
        curr-pos = curr-pos + 14. 
      END. 
      ELSE 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl0-balance, "->>>,>>>,>>>,>>9").
        curr-pos = curr-pos + 16. 
      END. 
    END. 
  END. 
  ELSE IF paramnr = 2319 THEN     /* Foreign Balance ON CURRENT vhp.bill-line */ 
  DO: 
    IF bline-flag = -1 THEN 
    DO: 
      IF bl-balance1 GE 100000 OR bl-balance1 LE -100000 THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>>,>>>,>>>,>>9").
        curr-pos = curr-pos + 16. 
      END. 
      ELSE 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>,>>9.99").
        curr-pos = curr-pos + 10. 
      END. 
    END. 
    ELSE IF bline-flag = 0 THEN 
    DO: 
    DEFINE VARIABLE fbal AS DECIMAL. 
      IF bl0-balance1 NE 0 THEN fbal = bl0-balance1. 
      ELSE fbal = bl0-balance / exchg-rate. 
      IF fbal GE 100000 OR fbal LE -100000 THEN 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(fbal, "->>>,>>>,>>>,>>9").
        curr-pos = curr-pos + 16. 
      END. 
      ELSE 
      DO: 
        ASSIGN output-list.str = output-list.str + STRING(fbal, "->>,>>9.99").
        curr-pos = curr-pos + 10. 
      END. 
    END. 
  END. 
  ELSE IF paramnr = 2317  THEN       /* Complete Name OF Hotel Guestname */ 
  DO: 
    FIND FIRST guest1 WHERE guest1.gastnr = vhp.res-line.gastnrmember NO-LOCK. 
    gname = guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1. 
    RUN put-string(gname). 
    curr-pos = curr-pos + 32. 
  END. 
 
  ELSE IF paramnr = 2311            /* CURRENT Time */  THEN 
  DO: 
    stime = STRING(time, "HH:MM"). 
    RUN put-string(stime). 
  END. 
 
  ELSE IF paramnr = 2312            /* CURRENT User Id */  THEN 
    RUN put-string(user-init).

  ELSE IF paramnr = 2401            /* CURRENT User Name */  THEN 
    RUN put-string(STRING(vhp.bediener.username,"x(16)")). 

END. 
 
PROCEDURE decode-key5p: 
DEFINE INPUT PARAMETER paramnr AS INTEGER. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE OUTPUT PARAMETER status-code AS INTEGER INITIAL 0. 
DEFINE BUFFER guest1 FOR vhp.guest. 
DEFINE VARIABLE stime AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE ch AS CHAR. 
 
  IF paramnr = 2304            /* Bill Artnr */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(t-list.nr, ">>>>").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2305            /* qty */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(t-list.qty, "->>9").
    curr-pos = curr-pos + 4. 
  END. 
  ELSE IF paramnr = 2306            /* Description */  THEN 
  DO: 
    IF t-list.rmcat NE "" THEN ch = (t-list.rmcat + " " + t-list.bezeich). 
    ELSE ch = t-list.bezeich. 
    DO i = 1 TO d-length: 
      IF length(ch) LT i THEN ASSIGN output-list.str = output-list.str + " ". 
      ELSE ASSIGN output-list.str = output-list.str + STRING(SUBSTR(ch,i,1), "x(1)").
    END. 
    curr-pos = curr-pos + d-length. 
  END. 
  ELSE IF paramnr = 2307            /* Price */  THEN 
  DO: 
    IF NOT long-digit THEN ASSIGN output-list.str = output-list.str + STRING(t-list.preis, "->,>>>,>>9.99"). 
    ELSE ASSIGN output-list.str = output-list.str + STRING(t-list.preis, "->>>>,>>>,>>9").
    curr-pos = curr-pos + 13. 
  END. 
  ELSE IF paramnr = 2308            /* Amount */  THEN 
  DO: 
    IF NOT long-digit THEN 
    DO:
      IF longer-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(t-list.betrag, "->>>>,>>>,>>9.99").
        curr-pos = curr-pos + 16. 
      END.
      ELSE IF long-billamt THEN
      DO:
        ASSIGN output-list.str = output-list.str + STRING(t-list.betrag, "->>>,>>>,>>9.99").
        curr-pos = curr-pos + 15. 
      END.
      ELSE
      DO:
        ASSIGN output-list.str = output-list.str + STRING(t-list.betrag, "->>,>>>,>>9.99").
        curr-pos = curr-pos + 14. 
      END.
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(t-list.betrag, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END. 
  ELSE IF paramnr = 2318            /* Foreign Amount */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(t-list.betrag, "->>,>>9.99").
    curr-pos = curr-pos + 10. 
  END. 
  ELSE IF paramnr = 2309            /* number OF days */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(t-list.tage, ">>9").
    curr-pos = curr-pos + 3. 
  END. 
  ELSE IF paramnr = 2310            /* vhp.bill-line DATE */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(t-list.date1).
    curr-pos = curr-pos + 8. 
  END. 
 
  ELSE IF paramnr = 1117            /* vhp.bill-line Userinit */  THEN 
  DO: 
    ASSIGN output-list.str = output-list.str + STRING(" ", "x(4)").
    curr-pos = curr-pos + 4. 
  END. 
 
  ELSE IF paramnr = 2316 THEN       /* Balance ON the CURRENT vhp.bill-line */ 
  DO: 
    IF NOT long-digit THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>9.99").
      curr-pos = curr-pos + 15. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance, "->>>,>>>,>>>,>>9").
      curr-pos = curr-pos + 16. 
    END. 
  END.
  ELSE IF paramnr = 2319 THEN     /* Foreign Balance ON CURRENT vhp.bill-line */ 
  DO: 
    IF bl-balance1 GE 100000 OR bl-balance1 LE -100000 THEN 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance1, " ->>>,>>>,>>9.99").
      curr-pos = curr-pos + 16. 
    END. 
    ELSE 
    DO: 
      ASSIGN output-list.str = output-list.str + STRING(bl-balance1, "->>,>>9.99").
      curr-pos = curr-pos + 10. 
    END. 
  END. 
  ELSE IF paramnr = 2317            /* Complete Name OF Hotel Guestname */ 
  THEN DO: 
    FIND FIRST guest1 WHERE guest1.gastnr = vhp.res-line.gastnrmember NO-LOCK. 
    RUN put-string(guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1). 
    curr-pos = curr-pos + 
      length(guest1.name + ", " + guest1.vorname1 + " " + guest1.anrede1). 
  END. 
 
  ELSE IF paramnr = 2311            /* CURRENT Time */  THEN 
  DO: 
    stime = STRING(time, "HH:MM"). 
    RUN put-string(stime). 
  END. 
 
  ELSE IF paramnr = 2312            /* CURRENT User Id */  THEN 
    RUN put-string(user-init).

  ELSE IF paramnr = 2401            /* CURRENT User Name */  THEN 
    RUN put-string(STRING(vhp.bediener.username,"x(16)")). 

END. 
 
PROCEDURE put-string: 
DEFINE INPUT PARAMETER STR AS CHAR. 
DEFINE VARIABLE len AS INTEGER. 
DEFINE VARIABLE i AS INTEGER. 
  len = length(str). 
  DO i = 1 TO len: 
    IF headloop = 0 THEN ASSIGN output-list.str = output-list.str + STRING(SUBSTR(str, i, 1), "x(1)"). 
    ELSE IF headloop = 3 THEN 
      header-list.texte = header-list.texte + SUBSTR(str, i, 1). 
    IF SUBSTR(str, i, 1) = CHR(10) THEN curr-pos = 1.
  END. 
  curr-pos = curr-pos + len. 
END. 
 
PROCEDURE put-gname: 
DEFINE INPUT PARAMETER STR AS CHAR. 
DEF VAR len AS INTEGER. 
DEF VAR i AS INTEGER. 
  len = ROUND(LENGTH(STR) / 2 + 0.4, 0). 
  DO i = 1 TO len: 
    ASSIGN output-list.str = output-list.str + STRING(SUBSTR(STR, (i * 2 - 1), 2), "x(2)").
  END. 
  curr-pos = curr-pos + len * 2. 
END. 
 
PROCEDURE create-bonus: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER INITIAL 1. 
DEFINE VARIABLE k AS INTEGER. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
DEFINE VARIABLE stay AS INTEGER. 
DEFINE VARIABLE pay AS INTEGER. 
DEFINE VARIABLE num-bonus AS INTEGER INITIAL 0. 
 
  DO i = 1 TO 999: 
      bonus-array[i] = NO. 
  END. 
  j = 1. 
  DO i = 1 TO 4: 
    stay = INTEGER(SUBSTR(vhp.arrangement.options, j, 2)). 
    pay  = INTEGER(SUBSTR(vhp.arrangement.options, j + 2, 2)). 
    IF (stay - pay) GT 0 THEN 
    DO: 
      n = num-bonus + pay  + 1. 
      DO k = n TO stay: 
        bonus-array[k] = YES. 
      END. 
      num-bonus = stay - pay. 
    END. 
     j = j + 4. 
  END. 
END. 
 

PROCEDURE read-proforma-inv: 
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE co-date         AS DATE. 
DEFINE VARIABLE add-it          AS LOGICAL. 
DEFINE VARIABLE ankunft         AS DATE. 
DEFINE VARIABLE abreise         AS DATE. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE argt-rate       AS DECIMAL. 
DEFINE VARIABLE argt-defined    AS LOGICAL. 
DEFINE VARIABLE delta           AS INTEGER. 
DEFINE VARIABLE start-date      AS DATE. 
DEFINE VARIABLE fixed-rate      AS LOGICAL. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE child1          AS INTEGER NO-UNDO. 
DEFINE VARIABLE bill-date       AS DATE NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER NO-UNDO. 
 
DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.

DEFINE BUFFER w1                FOR vhp.waehrung. 
DEFINE BUFFER resline           FOR vhp.res-line. 


DEFINE VARIABLE i       AS INT.
DEFINE VARIABLE j       AS INT.
DEFINE VARIABLE qty1    AS INT.
 
  FOR EACH resline WHERE resline.resnr = resnr 
    AND resline.active-flag LE 2 AND resline.resstatus NE 12 
    AND resline.resstatus NE 9 AND resline.resstatus NE 10
    AND resline.resstatus NE 99 NO-LOCK: 
 
    ebdisc-flag = resline.zimmer-wunsch MATCHES ("*ebdisc*").
    kbdisc-flag = resline.zimmer-wunsch MATCHES ("*kbdisc*").
    IF resline.l-zuordnung[1] NE 0 THEN curr-zikatnr = resline.l-zuordnung[1]. 
    ELSE curr-zikatnr = resline.zikatnr. 
 
    FIND FIRST vhp.zimkateg WHERE vhp.zimkateg.zikatnr = resline.zikatnr NO-LOCK. 
    FIND FIRST vhp.arrangement WHERE vhp.arrangement.arrangement 
      = resline.arrangement NO-LOCK. 
    ankunft = resline.ankunft. 
    abreise = resline.abreise. 
    fixed-rate = NO. 
    IF resline.was-status = 1 THEN fixed-rate = YES. 
    co-date = resline.abreise. 
    IF co-date GT resline.ankunft THEN co-date = co-date - 1. 
 
    RUN create-bonus. 
 
    DO datum = resline.ankunft TO co-date: 
      bill-date = datum. 
      argt-rate = 0. 
      rm-rate = resline.zipreis. 
      pax = resline.erwachs. 
/*    IF resline.erwachs GT 0 THEN */ 
  
      IF fixed-rate THEN 
      DO: 
        FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "arrangement" 
          AND vhp.reslin-queasy.resnr = resline.resnr 
          AND vhp.reslin-queasy.reslinnr = resline.reslinnr 
          AND datum GE vhp.reslin-queasy.date1 
          AND datum LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.reslin-queasy THEN 
        DO: 
          rm-rate = vhp.reslin-queasy.deci1. 
          IF vhp.reslin-queasy.number3 NE 0 THEN pax = vhp.reslin-queasy.number3. 
        END. 
        RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). 
      END. 
      ELSE 
      DO: 
        FIND FIRST vhp.guest WHERE vhp.guest.gastnr = resline.gastnr NO-LOCK. 
        FIND FIRST vhp.guest-pr WHERE vhp.guest-pr.gastnr = vhp.guest.gastnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.guest-pr THEN 
        DO: 
          FIND FIRST vhp.queasy WHERE vhp.queasy.key = 18 AND vhp.queasy.number1 
            = resline.reserve-int NO-LOCK NO-ERROR. 
          IF AVAILABLE vhp.queasy AND vhp.queasy.logi3 THEN 
          bill-date = resline.ankunft. 
            
          IF new-contrate THEN 
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resline.resnr, 
              resline.reslinnr, vhp.guest-pr.CODE, ?, bill-date, resline.ankunft,
              resline.abreise, resline.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
          ELSE
          DO:
            RUN pricecod-rate.p(resline.resnr, resline.reslinnr,
              vhp.guest-pr.CODE, bill-date, resline.ankunft, resline.abreise, 
              resline.reserve-int, vhp.arrangement.argtnr, curr-zikatnr, 
              resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, 
              OUTPUT rm-rate, OUTPUT rate-found).
            /*RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist).*/
            IF it-exist THEN rate-found = YES.
            IF NOT it-exist AND bonus-array[datum - resline.ankunft + 1] = YES 
              THEN rm-rate = 0.  
          END. /* old contract rate */
        END.   /* availab;e vhp.guest-pr */  
      END.     /* IF contract rate */ 
 
      FIND FIRST s-list WHERE s-list.bezeich = vhp.arrangement.argt-rgbez 
        AND s-list.rmcat = vhp.zimkateg.kurzbez 
        AND s-list.preis = rm-rate 
        AND s-list.datum = datum 
        AND s-list.ankunft = resline.ankunft 
        AND s-list.abreise = resline.abreise 
        AND s-list.erwachs = pax 
        AND s-list.kind1 = resline.kind1 
        AND s-list.kind2 = resline.kind2 NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list. 
        s-list.bezeich = vhp.arrangement.argt-rgbez. 
        s-list.rmcat = vhp.zimkateg.kurzbez. 
        s-list.preis = rm-rate. 
        s-list.datum = datum. 
        s-list.ankunft = resline.ankunft. 
        s-list.abreise = resline.abreise. 
        s-list.erwachs = pax. 
        s-list.kind1 = resline.kind1. 
        s-list.kind2 = resline.kind2. 
      END. 
      s-list.qty = s-list.qty + resline.zimmeranz. 
 
/**** additional fix cost ******/ 
      FOR EACH vhp.fixleist WHERE vhp.fixleist.resnr = resline.resnr 
        AND vhp.fixleist.reslinnr = resline.reslinnr NO-LOCK: 
        add-it = NO. 
        argt-rate = 0. 
        IF vhp.fixleist.sequenz = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 2 OR vhp.fixleist.sequenz = 3 THEN 
        DO: 
          IF resline.ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF vhp.fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 6 THEN 
        DO: 
          IF lfakt = ? THEN delta = 0. 
          ELSE 
          DO: 
            delta = lfakt - resline.ankunft. 
            IF delta LT 0 THEN delta = 0. 
          END. 
          start-date = resline.ankunft + delta. 
          IF (resline.abreise - start-date) LT vhp.fixleist.dekade 
            THEN start-date = resline.ankunft. 
          IF datum LE (start-date + (vhp.fixleist.dekade - 1)) THEN add-it = YES. 
          IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
        END. 
        IF add-it THEN 
        DO: 
          FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.fixleist.artnr 
            AND vhp.artikel.departement = vhp.fixleist.departement NO-LOCK. 
          argt-rate = vhp.fixleist.betrag * vhp.fixleist.number. 
          IF NOT fixed-rate AND AVAILABLE vhp.guest-pr THEN 
          DO: 
          DEF VAR ct       AS CHAR.
          DEF VAR contcode AS CHAR.
            contcode = vhp.guest-pr.CODE.
            ct = resline.zimmer-wunsch.
            IF ct MATCHES("*$CODE$*") THEN
            DO:
              ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
              contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
            END.
            FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "argt-line" 
              AND vhp.reslin-queasy.char1 = contcode 
              AND vhp.reslin-queasy.number1 = resline.reserve-int 
              AND vhp.reslin-queasy.number2 = vhp.arrangement.argtnr 
              AND vhp.reslin-queasy.reslinnr = resline.zikatnr 
              AND vhp.reslin-queasy.number3 = vhp.fixleist.artnr 
              AND vhp.reslin-queasy.resnr = vhp.fixleist.departement 
              AND bill-date GE vhp.reslin-queasy.date1 
              AND bill-date LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
            IF AVAILABLE vhp.reslin-queasy THEN 
              argt-rate = vhp.reslin-queasy.deci1 * vhp.fixleist.number. 
          END. 
        END. 
        IF argt-rate NE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.bezeich = vhp.artikel.bezeich 
            AND s-list.preis = (argt-rate / vhp.fixleist.number) 
            AND s-list.datum = datum 
            AND s-list.ankunft = resline.ankunft 
            AND s-list.abreise = resline.abreise 
            AND s-list.erwachs = pax 
            AND s-list.kind1 = resline.kind1 
            AND s-list.kind2 = resline.kind2 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.nr = vhp.artikel.artnr. 
            s-list.bezeich = vhp.artikel.bezeich. 
            s-list.preis = argt-rate / vhp.fixleist.number. 
            s-list.datum = datum. 
            s-list.ankunft = resline.ankunft. 
            s-list.abreise = resline.abreise. 
            s-list.erwachs = pax. 
            s-list.kind1 = resline.kind1. 
            s-list.kind2 = resline.kind2. 
          END. 
          s-list.qty = s-list.qty + (vhp.fixleist.number * resline.zimmeranz). 
        END. /* argt-rate NE 0 */  
      END.   /* each vhp.fixleist */ 
    END.     /* datum */
  END.       /* for each resline */
 
  FOR EACH s-list BY s-list.ankunft BY s-list.datum BY s-list.bezeich 
    BY s-list.erwachs: 
    IF s-list.nr = 0 THEN 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.rmcat = s-list.rmcat 
        AND t-list.preis = s-list.preis 
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.nr = s-list.nr. 
        t-list.bezeich = s-list.bezeich. 
        t-list.rmcat = s-list.rmcat. 
        t-list.preis = s-list.preis. 
        t-list.date1 = s-list.datum. 
        t-list.ankunft = s-list.ankunft. 
        t-list.abreise = s-list.abreise. 
        t-list.erwachs = s-list.erwachs. 
        t-list.kind1 = s-list.kind1. 
        t-list.kind2 = s-list.kind2. 
      END. 
      IF s-list.qty GE t-list.qty THEN   /*FT 22/10/13*/
        t-list.tage = t-list.tage + 1. 
      t-list.date2 = s-list.datum. 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
      /*FT 22/10/13*/
      IF s-list.qty NE t-list.qty AND s-list.preis = t-list.preis THEN
      DO:
          qty1 = t-list.qty.
          CREATE t-list.
          ASSIGN
            t-list.nr = s-list.nr
            t-list.bezeich = s-list.bezeich 
            t-list.rmcat = s-list.rmcat 
            t-list.preis = s-list.preis 
            t-list.date1 = s-list.datum 
            t-list.ankunft = s-list.ankunft 
            t-list.abreise = s-list.abreise 
            t-list.erwachs = s-list.erwachs
            t-list.kind1 = s-list.kind1
            t-list.kind2 = s-list.kind2
            t-list.date1 = s-list.datum
            t-list.tage  = 1.
          IF s-list.qty GT qty1 THEN
            ASSIGN  
              j = s-list.qty - qty1
              t-list.qty = j.
          ELSE
            ASSIGN
              j = qty1 - s-list.qty
              t-list.qty = s-list.qty.
      END. /*endFT 22/10/13*/
    END. 
    ELSE 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.preis = s-list.preis 
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        t-list.nr = s-list.nr. 
        t-list.bezeich = s-list.bezeich. 
        t-list.preis = s-list.preis. 
        t-list.date1 = s-list.datum. 
        t-list.ankunft = s-list.ankunft. 
        t-list.abreise = s-list.abreise. 
        t-list.erwachs = s-list.erwachs. 
        t-list.kind1 = s-list.kind1. 
        t-list.kind2 = s-list.kind2. 
      END. 
      t-list.tage = t-list.tage + 1. 
      t-list.date2 = s-list.datum. 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
    END. 
    DELETE s-list. 
  END. 
 
  FOR EACH t-list: 
    t-list.betrag = t-list.qty * t-list.tage * t-list.preis. 
  END. 
 
END. 
 

PROCEDURE read-proforma-inv1: 
DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE co-date         AS DATE. 
DEFINE VARIABLE add-it          AS LOGICAL. 
DEFINE VARIABLE ankunft         AS DATE. 
DEFINE VARIABLE abreise         AS DATE. 
DEFINE VARIABLE rm-rate         AS DECIMAL. 
DEFINE VARIABLE argt-rate       AS DECIMAL. 
DEFINE VARIABLE argt-defined    AS LOGICAL. 
DEFINE VARIABLE delta           AS INTEGER. 
DEFINE VARIABLE start-date      AS DATE. 
DEFINE VARIABLE fixed-rate      AS LOGICAL. 
DEFINE VARIABLE qty             AS INTEGER. 
DEFINE VARIABLE it-exist        AS LOGICAL INITIAL NO. 
DEFINE VARIABLE exrate1         AS DECIMAL INITIAL 1. 
DEFINE VARIABLE ex2             AS DECIMAL INITIAL 1. 
DEFINE VARIABLE pax             AS INTEGER NO-UNDO. 
DEFINE VARIABLE child1          AS INTEGER NO-UNDO. 
DEFINE VARIABLE bill-date       AS DATE NO-UNDO. 
DEFINE VARIABLE curr-zikatnr    AS INTEGER NO-UNDO. 

DEFINE VARIABLE curr-no         AS INTEGER INITIAL 1000 NO-UNDO.
DEFINE VARIABLE do-it           AS LOGICAL              NO-UNDO.
DEFINE VARIABLE curr-date       AS DATE                 NO-UNDO.
DEFINE VARIABLE lRate           AS DECIMAL              NO-UNDO.

DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.

DEFINE BUFFER w1                FOR vhp.waehrung. 
DEFINE BUFFER resline           FOR vhp.res-line. 
 
  FOR EACH resline WHERE resline.resnr = resnr 
    AND resline.reslinnr = reslinnr NO-LOCK: 
 
    ebdisc-flag = resline.zimmer-wunsch MATCHES ("*ebdisc*").
    kbdisc-flag = resline.zimmer-wunsch MATCHES ("*kbdisc*").
    IF resline.l-zuordnung[1] NE 0 THEN curr-zikatnr = resline.l-zuordnung[1]. 
    ELSE curr-zikatnr = resline.zikatnr. 
 
    FIND FIRST vhp.zimkateg WHERE vhp.zimkateg.zikatnr = resline.zikatnr NO-LOCK. 
    FIND FIRST vhp.arrangement WHERE vhp.arrangement.arrangement 
      = resline.arrangement NO-LOCK. 
    ankunft = resline.ankunft. 
    abreise = resline.abreise. 
    fixed-rate = NO. 
    IF resline.was-status = 1 THEN fixed-rate = YES. 
    co-date = resline.abreise. 
    IF co-date GT resline.ankunft THEN co-date = co-date - 1. 
 
    RUN create-bonus. 
 
    DO datum = resline.ankunft TO co-date: 
      bill-date = datum. 
      argt-rate = 0. 
      rm-rate = resline.zipreis. 
      pax = resline.erwachs. 
/*    IF resline.erwachs GT 0 THEN */ 
  
      IF fixed-rate THEN 
      DO: 
        FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "arrangement" 
          AND vhp.reslin-queasy.resnr = resline.resnr 
          AND vhp.reslin-queasy.reslinnr = resline.reslinnr 
          AND datum GE vhp.reslin-queasy.date1 
          AND datum LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.reslin-queasy THEN 
        DO: 
          rm-rate = vhp.reslin-queasy.deci1. 
          IF vhp.reslin-queasy.number3 NE 0 THEN pax = vhp.reslin-queasy.number3. 
        END. 
        /*RUN usr-prog1(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist). masdod due serverless*/
      END. 
      ELSE 
      DO: 
        FIND FIRST vhp.guest WHERE vhp.guest.gastnr = resline.gastnr NO-LOCK. 
        FIND FIRST vhp.guest-pr WHERE vhp.guest-pr.gastnr = vhp.guest.gastnr 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.guest-pr THEN 
        DO: 
          FIND FIRST vhp.queasy WHERE vhp.queasy.key = 18 AND vhp.queasy.number1 
            = resline.reserve-int NO-LOCK NO-ERROR. 
          IF AVAILABLE vhp.queasy AND vhp.queasy.logi3 THEN 
          bill-date = resline.ankunft. 
            
          IF new-contrate THEN 
            RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, resline.resnr, 
              resline.reslinnr, vhp.guest-pr.CODE, ?, bill-date, resline.ankunft,
              resline.abreise, resline.reserve-int, vhp.arrangement.argtnr,
              curr-zikatnr, resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, OUTPUT rate-found,
              OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
          ELSE
          DO:
            RUN pricecod-rate.p(resline.resnr, resline.reslinnr,
              vhp.guest-pr.CODE, bill-date, resline.ankunft, resline.abreise, 
              resline.reserve-int, vhp.arrangement.argtnr, curr-zikatnr, 
              resline.erwachs, resline.kind1, resline.kind2,
              resline.reserve-dec, resline.betriebsnr, 
              OUTPUT rm-rate, OUTPUT rate-found).
            RUN usr-prog2(datum, INPUT-OUTPUT rm-rate, OUTPUT it-exist).
            IF it-exist THEN rate-found = YES.
            IF NOT it-exist AND bonus-array[datum - resline.ankunft + 1] = YES 
              THEN rm-rate = 0.  
          END. /* old contract rate */
        END.   /* availab;e vhp.guest-pr */  
      END.     /* IF contract rate */ 
 
      lRate = rm-rate.
      IF datum LT billdate THEN
      DO:
          FIND FIRST genstat WHERE genstat.resnr = resnr
              AND genstat.res-int[1] = reslinnr
              AND genstat.datum = datum NO-LOCK NO-ERROR.
          IF AVAILABLE genstat THEN rm-rate = genstat.rateLocal.
          ELSE
          DO:
              FIND FIRST exrate WHERE exrate.artnr = resline.betriebsnr
                  AND exrate.datum = datum NO-LOCK NO-ERROR.
              IF AVAILABLE exrate THEN lRate = rm-rate * exrate.betrag.
          END.
      END.
      ELSE
      DO:
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = resline.betriebsnr
              NO-LOCK NO-ERROR.
          IF AVAILABLE waehrung THEN 
            lRate = rm-rate * waehrung.ankauf / waehrung.einheit.
      END.

      FIND FIRST s-list WHERE s-list.bezeich = vhp.arrangement.argt-rgbez 
        AND s-list.rmcat = vhp.zimkateg.kurzbez 
        AND s-list.preis = rm-rate 
        AND s-list.lRate = lRate
        AND s-list.datum = datum 
        AND s-list.ankunft = resline.ankunft 
        AND s-list.abreise = resline.abreise 
        AND s-list.erwachs = pax 
        AND s-list.kind1 = resline.kind1 
        AND s-list.kind2 = resline.kind2 NO-ERROR. 
      IF NOT AVAILABLE s-list THEN 
      DO: 
        CREATE s-list. 
        ASSIGN
          s-list.bezeich = vhp.arrangement.argt-rgbez
          s-list.rmcat = vhp.zimkateg.kurzbez
          s-list.preis = rm-rate
          s-list.lRate = lRate
          s-list.datum = datum 
          s-list.ankunft = resline.ankunft
          s-list.abreise = resline.abreise 
          s-list.erwachs = pax
          s-list.kind1 = resline.kind1 
          s-list.kind2 = resline.kind2
        . 
      END. 
      s-list.qty = s-list.qty + resline.zimmeranz. 


/**** additional fix cost ******/ 
      FOR EACH vhp.fixleist WHERE vhp.fixleist.resnr = resline.resnr 
        AND vhp.fixleist.reslinnr = resline.reslinnr NO-LOCK: 
        add-it = NO. 
        argt-rate = 0. 
        IF vhp.fixleist.sequenz = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 2 OR vhp.fixleist.sequenz = 3 THEN 
        DO: 
          IF resline.ankunft EQ datum THEN add-it = YES. 
        END. 
        ELSE IF vhp.fixleist.sequenz = 4 AND day(datum) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 5 
          AND day(datum + 1) = 1 THEN add-it = YES. 
        ELSE IF vhp.fixleist.sequenz = 6 THEN 
        DO: 
          IF lfakt = ? THEN delta = 0. 
          ELSE 
          DO: 
            delta = lfakt - resline.ankunft. 
            IF delta LT 0 THEN delta = 0. 
          END. 
          start-date = resline.ankunft + delta. 
          IF (resline.abreise - start-date) LT vhp.fixleist.dekade 
            THEN start-date = resline.ankunft. 
          IF datum LE (start-date + (vhp.fixleist.dekade - 1)) THEN add-it = YES. 
          IF datum LT start-date THEN add-it = no. /* may NOT post !! */ 
        END. 
        IF add-it THEN 
        DO: 
          FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.fixleist.artnr 
            AND vhp.artikel.departement = vhp.fixleist.departement NO-LOCK. 
          argt-rate = vhp.fixleist.betrag * vhp.fixleist.number. 
          IF NOT fixed-rate AND AVAILABLE vhp.guest-pr THEN 
          DO: 
          DEF VAR ct       AS CHAR.
          DEF VAR contcode AS CHAR.
            contcode = vhp.guest-pr.CODE.
            ct = resline.zimmer-wunsch.
            IF ct MATCHES("*$CODE$*") THEN
            DO:
              ct = SUBSTR(ct,INDEX(ct,"$CODE$") + 6).
              contcode = SUBSTR(ct, 1, INDEX(ct,";") - 1).
            END.
            FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "argt-line" 
              AND vhp.reslin-queasy.char1 = contcode 
              AND vhp.reslin-queasy.number1 = resline.reserve-int 
              AND vhp.reslin-queasy.number2 = vhp.arrangement.argtnr 
              AND vhp.reslin-queasy.reslinnr = resline.zikatnr 
              AND vhp.reslin-queasy.number3 = vhp.fixleist.artnr 
              AND vhp.reslin-queasy.resnr = vhp.fixleist.departement 
              AND bill-date GE vhp.reslin-queasy.date1 
              AND bill-date LE vhp.reslin-queasy.date2 NO-LOCK NO-ERROR. 
            IF AVAILABLE vhp.reslin-queasy THEN 
              argt-rate = vhp.reslin-queasy.deci1 * vhp.fixleist.number. 
          END. 
        END. 
        IF argt-rate NE 0 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.bezeich = vhp.artikel.bezeich 
            AND s-list.preis = (argt-rate / vhp.fixleist.number) 
            AND s-list.datum = datum 
            AND s-list.ankunft = resline.ankunft 
            AND s-list.abreise = resline.abreise 
            AND s-list.erwachs = pax 
            AND s-list.kind1 = resline.kind1 
            AND s-list.kind2 = resline.kind2 NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            CREATE s-list. 
            s-list.nr = vhp.artikel.artnr. 
            s-list.bezeich = vhp.artikel.bezeich. 
            s-list.preis = argt-rate / vhp.fixleist.number. 
            s-list.datum = datum. 
            s-list.ankunft = resline.ankunft. 
            s-list.abreise = resline.abreise. 
            s-list.erwachs = pax. 
            s-list.kind1 = resline.kind1. 
            s-list.kind2 = resline.kind2. 
          END. 
          s-list.qty = s-list.qty + (vhp.fixleist.number * resline.zimmeranz). 
        END. /* argt-rate NE 0 */  
      END.   /* each vhp.fixleist */ 
    END.     /* datum */
  END.       /* for each resline */
 
  FOR EACH s-list BY s-list.ankunft BY s-list.datum BY s-list.bezeich 
    BY s-list.erwachs: 
    IF s-list.nr = 0 THEN 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.rmcat = s-list.rmcat 
        AND t-list.preis = s-list.preis 
        AND t-list.lRate = s-list.lRate
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        create t-list. 
        ASSIGN
          t-list.nr = s-list.nr
          t-list.bezeich = s-list.bezeich
          t-list.rmcat = s-list.rmcat
          t-list.preis = s-list.preis
          t-list.lRate = s-list.lRate
          t-list.date1 = s-list.datum 
          t-list.ankunft = s-list.ankunft 
          t-list.abreise = s-list.abreise 
          t-list.erwachs = s-list.erwachs 
          t-list.kind1 = s-list.kind1 
          t-list.kind2 = s-list.kind2
        . 
      END. 
      ASSIGN
        t-list.tage = t-list.tage + 1
        t-list.date2 = s-list.datum
      . 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
    END. 
    ELSE 
    DO: 
      FIND FIRST t-list WHERE t-list.bezeich = s-list.bezeich 
        AND t-list.preis = s-list.preis
        AND t-list.lRate = s-list.lRate
        AND t-list.ankunft = s-list.ankunft 
        AND t-list.abreise = s-list.abreise 
        AND t-list.erwachs = s-list.erwachs 
        AND t-list.kind1 = s-list.kind1 
        AND t-list.kind2 = s-list.kind2 NO-ERROR. 
      IF NOT AVAILABLE t-list THEN 
      DO: 
        CREATE t-list.
        ASSIGN
          t-list.nr = s-list.nr
          t-list.bezeich = s-list.bezeich
          t-list.preis = s-list.preis
          t-list.lRate = s-list.lRate
          t-list.date1 = s-list.datum 
          t-list.ankunft = s-list.ankunft
          t-list.abreise = s-list.abreise 
          t-list.erwachs = s-list.erwachs 
          t-list.kind1 = s-list.kind1
          t-list.kind2 = s-list.kind2
        . 
      END.
      ASSIGN
        t-list.tage = t-list.tage + 1
        t-list.date2 = s-list.datum
      . 
      IF s-list.datum = t-list.date1 THEN t-list.qty = t-list.qty + s-list.qty. 
    END. 
    DELETE s-list. 
  END. 
 
  FOR EACH t-list: 
    /*t-list.betrag = t-list.qty * t-list.tage * t-list.lRate.*/
    /*fixcost show in proforma MG ED4E67*/
    IF t-list.lRate NE 0 THEN t-list.betrag = t-list.qty * t-list.tage * t-list.lRate. 
    ELSE t-list.betrag = t-list.qty * t-list.tage * t-list.preis.
  END.

  IF rechnr GT 0 THEN
  DO:
      FOR EACH bill-line WHERE bill-line.rechnr = bill.rechnr NO-LOCK,
          FIRST artikel WHERE artikel.artnr = bill-line.artnr
          AND artikel.departement = bill-line.departement NO-LOCK
          BY bill-line.bill-datum BY bill-line.zeit:
          do-it = YES.
          IF artikel.artart EQ 9 THEN
          DO:
              FIND FIRST arrangement WHERE arrangement.argt-artikelnr
                  = artikel.artnr NO-LOCK NO-ERROR.
              IF NOT AVAILABLE arrangement OR arrangement.segmentcode = 0 THEN
                  do-it = NO.
          END.
          IF do-it THEN DO:
            CREATE t-list.
            ASSIGN
              curr-no = curr-no + 1
              t-list.nr = curr-no 
              t-list.bezeich = bill-line.bezeich
              t-list.preis   = 0
              t-list.date1   = bill-line.bill-datum 
              t-list.betrag  = bill-line.betrag
            . 
          END.
      END.
  END.
 
END. 
/* 
PROCEDURE usr-prog1: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST vhp.reslin-queasy WHERE vhp.reslin-queasy.key = "rate-prog" 
    AND vhp.reslin-queasy.number1 = resnr 
    AND vhp.reslin-queasy.number2 = 0 AND vhp.reslin-queasy.char1 = "" 
    AND vhp.reslin-queasy.reslinnr = 1 USE-INDEX argt_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.reslin-queasy THEN prog-str = vhp.reslin-queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    /*OUTPUT STREAM s1 TO ".\_rate.p". */
    DO i = 1 TO length(prog-str): 
      /*PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". */
    END. 
    /*OUTPUT STREAM s1 CLOSE. */
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". 
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, resnr, reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 

PROCEDURE usr-prog2: 
DEFINE INPUT PARAMETER bill-date AS DATE. 
DEFINE INPUT-OUTPUT PARAMETER roomrate AS DECIMAL. 
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO. 
DEFINE VARIABLE prog-str AS CHAR INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
  FIND FIRST vhp.queasy WHERE vhp.queasy.key = 2 
    AND vhp.queasy.char1 = vhp.guest-pr.code NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.queasy THEN prog-str = vhp.queasy.char3. 
  IF prog-str NE "" THEN 
  DO: 
    /*OUTPUT STREAM s1 TO ".\_rate.p". */
    DO i = 1 TO length(prog-str): 
      /*PUT STREAM s1 SUBSTR(prog-str, i, 1) FORMAT "x(1)". */
    END. 
    /*OUTPUT STREAM s1 CLOSE. 
    compile value(".\_rate.p"). 
    dos silent "del .\_rate.p". */
    IF NOT compiler:ERROR THEN 
    DO: 
      RUN value(".\_rate.p") (0, resnr, reslinnr, 
      bill-date, roomrate, NO, OUTPUT roomrate). 
      it-exist = YES. 
    END. 
  END. 
END. 
*/

PROCEDURE get-vat:
DEF INPUT  PARAMETER inp-str AS CHAR.
DEF OUTPUT PARAMETER mwst    AS DECIMAL INITIAL 1000.
.
DEF VAR tokcounter                 AS INTEGER NO-UNDO.
DEF VAR mesStr                     AS CHAR    NO-UNDO.
DEF VAR mesToken                   AS CHAR    NO-UNDO.
DEF VAR mesValue                   AS CHAR    NO-UNDO.
  IF INDEX(inp-str, "VAT%") = 0 THEN RETURN.
  DO tokcounter = 1 TO NUM-ENTRIES(inp-str, ";") - 1:
    ASSIGN
      mesStr   = ENTRY(tokcounter, inp-str, ";")
      mesToken = ENTRY(1, mesStr, ",")
      mesValue = ENTRY(2, mesStr, ",")
    .
    CASE mesToken:
        WHEN "VAT%"  THEN 
        DO:    
          mwst = DECIMAL(mesValue) / 100.
          RETURN.
        END.
    END CASE.
  END.
END.



PROCEDURE update-bill:
    FIND FIRST bill WHERE bill.rechnr = rechnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE bill THEN
    DO:
        ASSIGN bill.rechnr2 = briefnr.
        succes-flag = YES.
    END.
    FIND FIRST bill NO-LOCK.

END.
