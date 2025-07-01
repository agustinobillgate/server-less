
DEFINE TEMP-TABLE b-list    LIKE vhp.h-bill-line. 
DEFINE TEMP-TABLE t-b-list  LIKE b-list.
DEFINE TEMP-TABLE t-h-bill  LIKE h-bill
    FIELD rec-id AS INT.
DEFINE TEMP-TABLE t-h-artikel  LIKE h-artikel
    FIELD rec-id AS INT.


DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER inp-rechnr     AS INT.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER user-name      AS CHAR.
DEF INPUT  PARAMETER curr-printer   AS INT.

DEF OUTPUT PARAMETER must-print     AS LOGICAL.
DEF OUTPUT PARAMETER rev-sign       AS INT INIT 1.
DEF OUTPUT PARAMETER cancel-exist   AS LOGICAL.
DEF OUTPUT PARAMETER price-decimal  AS INT.
DEF OUTPUT PARAMETER curr-local     AS CHAR.
DEF OUTPUT PARAMETER curr-foreign   AS CHAR.
DEF OUTPUT PARAMETER double-currency AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate   AS LOGICAL.
DEF OUTPUT PARAMETER exchg-rate     AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER f-disc         AS INT INIT 0.
DEF OUTPUT PARAMETER b-artnr        AS INT INIT 0.
DEF OUTPUT PARAMETER b-title        AS CHAR.
DEF OUTPUT PARAMETER deptname       AS CHAR.
DEF OUTPUT PARAMETER curr-user      AS CHAR.
DEF OUTPUT PARAMETER curr-waiter    AS INT INIT 1.
DEF OUTPUT PARAMETER tischnr        AS INT.
DEF OUTPUT PARAMETER rechnr         AS INT.
DEF OUTPUT PARAMETER pax            AS INT.
DEF OUTPUT PARAMETER balance        AS DECIMAL.
DEF OUTPUT PARAMETER balance-foreign AS DECIMAL.
DEF OUTPUT PARAMETER bcol           AS INT INIT 2.
DEF OUTPUT PARAMETER printed        AS CHAR INIT "".

DEF OUTPUT PARAMETER bill-date      AS DATE.
DEF OUTPUT PARAMETER kreditlimit    AS DECIMAL.
DEF OUTPUT PARAMETER total-saldo    AS DECIMAL.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER msg-str1       AS CHAR.
DEF OUTPUT PARAMETER rec-kellner    AS INT.
DEF OUTPUT PARAMETER rec-bill-guest AS INT.
DEF OUTPUT PARAMETER cashless-flag  AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER cashless-artnr AS INTEGER NO-UNDO INIT ?.
DEF OUTPUT PARAMETER multi-cash     AS LOGICAL.

DEF OUTPUT PARAMETER TABLE FOR t-b-list.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-closeinv".

DEFINE VARIABLE fogl-date   AS DATE NO-UNDO.
DEFINE BUFFER   bill-guest  FOR vhp.guest. 

/* SY 27/02/2014 */
FIND FIRST htparam WHERE htparam.paramnr = 834 NO-LOCK.
ASSIGN cashless-flag = htparam.flogical.
IF cashless-flag THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 569 NO-LOCK.
  IF htparam.paramnr NE 0 THEN 
    ASSIGN cashless-artnr = htparam.finteger.
END.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 833 NO-LOCK. 
multi-cash = flogical. 

FIND FIRST vhp.htparam WHERE htpara.paramnr = 1003 NO-LOCK. 
fogl-date = vhp.htparam.fdate. 
FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.departement = curr-dept 
  AND vhp.h-bill-line.rechnr = inp-rechnr NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-bill-line AND vhp.h-bill-line.bill-datum LE fogl-date THEN
DO:
  msg-str = msg-str + CHR(2) + "&W"
          + translateExtended ("Bill older than last transfer date to G/L (Param 1003).",lvCAREA,"").
END.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 877 NO-LOCK. 
must-print = flogical. 
RUN determine-revsign.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK. 
FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bill-guest THEN 
DO:
  msg-str1 = msg-str1 + CHR(2)
           + translateExtended ("GuestNo (Param 867) for credit restaurant undefined",lvCAREA,"")
           + CHR(10)
           + translateExtended ("Posting not possible.",lvCAREA,"").
  RETURN. 
END. 

FIND FIRST vhp.queasy WHERE vhp.queasy.key = 11 NO-LOCK NO-ERROR. 
cancel-exist = AVAILABLE vhp.queasy. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK. 
price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST vhp.htparam WHERE paramnr = 152 NO-LOCK. 
curr-local = fchar. 
FIND FIRST vhp.htparam WHERE paramnr = 144 NO-LOCK. 
curr-foreign = fchar. 
 
FIND FIRST vhp.htparam WHERE paramnr = 240 NO-LOCK. 
double-currency = vhp.htparam.flogical.


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 143 NO-LOCK. 
foreign-rate = vhp.htparam.flogical. 
 
IF FOREIGN-RATE OR DOUBLE-CURRENCY THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz 
    = vhp.htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.waehrung THEN exchg-rate 
    = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
END. 
 
FIND FIRST vhp.htparam WHERE paramnr = 557 no-lock. /*rest artnr food disc*/ 
f-disc = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 no-lock. /*rest artnr bev disc*/ 
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.htparam.finteger 
  AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR. 
IF AVAILABLE h-artikel THEN 
  FIND FIRST vhp.artikel WHERE vhp.artikel.artnr = vhp.h-artikel.artnrfront 
  AND vhp.artikel.departement = curr-dept NO-LOCK. 
IF AVAILABLE vhp.artikel THEN b-artnr = vhp.artikel.artnr. 


FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = curr-dept NO-LOCK. 
b-title = vhp.hoteldpt.depart. 
IF AVAILABLE vhp.waehrung THEN 
  b-title = b-title + " ! " 
    + translateExtended ("Today's Exchange Rate",lvCAREA,"") 
    + " = " + STRING(exchg-rate). 
deptname = vhp.hoteldpt.depart. 

/* Eko 22 jan 2016 */
FIND FIRST htparam WHERE htparam.paramnr = 300 NO-LOCK. /* micros flag */
deptname = deptname + CHR(3) + STRING(htparam.flogical).

FIND FIRST vhp.h-bill WHERE vhp.h-bill.rechnr = inp-rechnr
  AND vhp.h-bill.departement = curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-bill THEN 
DO:
    FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = vhp.h-bill.kellner-nr
      AND vhp.kellner.departement = vhp.h-bill.departement NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.kellner THEN curr-user = vhp.kellner.kellnername.
    ELSE curr-user = user-init + " " + user-name. 
         
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END. 
ELSE curr-user = user-init + " " + user-name. 
IF AVAILABLE kellner THEN rec-kellner = RECID(kellner).
IF curr-printer NE 0 THEN curr-waiter = INTEGER(user-init). 
FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = curr-waiter 
  AND vhp.kellner.departement = curr-dept NO-LOCK NO-ERROR. 

RUN open-table.

RUN cal-total-saldo.

FOR EACH h-artikel WHERE h-artikel.departement = curr-dept
    AND (h-artikel.artart = 2 OR h-artikel.artart = 6
    OR h-artikel.artart = 7 OR h-artikel.artart = 11
    OR h-artikel.artart = 12) NO-LOCK:
    CREATE t-h-artikel.
    BUFFER-COPY h-artikel TO t-h-artikel.
    ASSIGN t-h-artikel.rec-id = INTEGER(RECID(h-artikel)).
    IF t-h-artikel.artnr = cashless-artnr THEN
    ASSIGN t-h-artikel.bezeich = REPLACE(t-h-artikel.bezeich, " ", "").
END.
IF AVAILABLE bill-guest THEN rec-bill-guest = RECID(bill-guest).

PROCEDURE determine-revsign: 
DEFINE VARIABLE s AS DECIMAL INITIAL 0. 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = inp-rechnr 
    AND vhp.h-bill-line.departement = curr-dept NO-LOCK, 
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
    AND vhp.h-artikel.departement = vhp.h-bill-line.departement 
    AND vhp.h-artikel.artart = 0 NO-LOCK: 
    s = s + vhp.h-bill-line.betrag. 
  END. 
  IF s LT 0 THEN rev-sign = - 1. 
END. 



PROCEDURE open-table:
  RUN create-blist.
 
  FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK.
  FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger NO-LOCK 
    NO-ERROR.
  kreditlimit = bill-guest.kreditlimit. 
  
  FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = curr-dept 
    AND vhp.h-bill.rechnr = inp-rechnr AND vhp.h-bill.flag = 1 NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.h-bill THEN 
  DO: 
    FIND FIRST vhp.tisch WHERE vhp.tisch.tischnr = vhp.h-bill.tischnr. 
    tischnr = vhp.tisch.tischnr. 
    rechnr = vhp.h-bill.rechnr. 
    RUN disp-bill-line.
 
    pax = vhp.h-bill.belegung. 
    balance = vhp.h-bill.saldo. 
    balance-foreign = vhp.h-bill.mwst[99]. 
    IF balance LE kreditlimit THEN bcol = 2. 
/*    ELSE bcol = 12. */ 
    IF vhp.h-bill.rgdruck = 0 THEN printed = "". 
    ELSE printed = "*". 
    /*MTDISP tischnr pax balance /*printed*/ WITH FRAME frame1.*/
    IF double-currency THEN 
    DO: 
      /*MTDISP balance-foreign WITH FRAME frame1. 
      b11:TITLE IN FRAME frame1 = b-title   + "  " 
          + translateExtended ("BillNo",lvCAREA,"") + " " + STRING(rechnr).*/
    END. 
    ELSE /*MTb1:TITLE IN FRAME frame1 = b-title + "  " 
        + translateExtended ("BillNo",lvCAREA,"") + " " + STRING(rechnr)*/.
    /*MTENABLE btn-cash btn-ccard btn-transfer WITH FRAME frame1.*/
    IF vhp.h-bill.betriebsnr NE 0 THEN 
    DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 
        AND vhp.queasy.number1 = vhp.h-bill.betriebsnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN 
      DO: 
        curr-user = TRIM(curr-user + " - " + vhp.queasy.char1). 
        /*MTDISP curr-user WITH FRAME frame1.*/
      END. 
    END. 
    /*MTIF double-currency THEN APPLY "entry" TO b11. 
    ELSE APPLY "entry" TO b1. */
    RETURN NO-APPLY. 
  END. 
END. 


PROCEDURE create-blist: 
DEFINE buffer h-art FOR vhp.h-artikel. 
DEFINE VARIABLE create-it AS LOGICAL. 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
  bill-date = vhp.htparam.fdate. 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = inp-rechnr 
    AND vhp.h-bill-line.departement = curr-dept NO-LOCK 
    BY vhp.h-bill-line.waehrungsnr: 

    create-it = YES. 
    FIND FIRST h-art WHERE h-art.artnr = vhp.h-bill-line.artnr 
      AND h-art.departement = vhp.h-bill-line.departement NO-LOCK NO-ERROR. 
    IF (AVAILABLE h-art AND h-art.artart NE 0) OR h-bill-line.artnr = 0 THEN 
    DO: 
      FIND FIRST b-list WHERE b-list.artnr = vhp.h-bill-line.artnr 
        AND b-list.betrag = - vhp.h-bill-line.betrag 
        AND b-list.bill-datum = vhp.h-bill-line.bill-datum NO-ERROR. 
      IF AVAILABLE b-list THEN 
      DO: 
        delete b-list. 
        create-it = NO. 
      END. 
      ELSE bill-date = vhp.h-bill-line.bill-datum. 
    END. 
    IF create-it THEN 
    DO: 
      CREATE b-list. 
      ASSIGN 
        b-list.rechnr = inp-rechnr 
        b-list.artnr = vhp.h-bill-line.artnr 
        b-list.bezeich = vhp.h-bill-line.bezeich 
        b-list.anzahl = vhp.h-bill-line.anzahl 
        b-list.nettobetrag = vhp.h-bill-line.nettobetrag 
        b-list.fremdwbetrag = vhp.h-bill-line.fremdwbetrag 
        b-list.betrag = vhp.h-bill-line.betrag 
        b-list.tischnr = vhp.h-bill-line.tischnr 
        b-list.departement = vhp.h-bill-line.departement 
        b-list.epreis = vhp.h-bill-line.epreis 
        b-list.zeit = vhp.h-bill-line.zeit 
        b-list.bill-datum = vhp.h-bill-line.bill-datum 
        b-list.sysdate = vhp.h-bill-line.sysdate 
        b-list.segmentcode = vhp.h-bill-line.segmentcode 
        b-list.waehrungsnr = vhp.h-bill-line.waehrungsnr 
        b-list.transferred = YES. 
    END. 
  END. 
  IF vhp.htparam.fdate NE bill-date AND double-currency THEN 
  DO: 
    FIND FIRST vhp.exrate WHERE vhp.exrate.datum = bill-date NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.exrate THEN exchg-rate = vhp.exrate.betrag. 
  END. 
END. 



PROCEDURE disp-bill-line: 
  IF double-currency THEN 
  FOR EACH b-list WHERE b-list.rechnr = vhp.h-bill.rechnr 
      AND b-list.departement = curr-dept NO-LOCK 
      BY b-list.sysdate descending BY b-list.zeit descending:
      CREATE t-b-list.
      BUFFER-COPY b-list TO t-b-list.
  END.
  ELSE 
  FOR EACH b-list WHERE b-list.rechnr = vhp.h-bill.rechnr 
      AND b-list.departement = curr-dept NO-LOCK 
      BY b-list.sysdate descending BY b-list.zeit descending:
      CREATE t-b-list.
      BUFFER-COPY b-list TO t-b-list.
  END.
END. 

PROCEDURE cal-total-saldo: 
  total-saldo = 0. 
  FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr= vhp.h-bill.rechnr 
    AND vhp.h-bill-line.departement = vhp.h-bill.departement 
    AND vhp.h-bill-line.artnr NE 0 NO-LOCK, 
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr 
    AND vhp.h-artikel.departement = vhp.h-bill-line.departement 
    AND vhp.h-artikel.artart = 0 NO-LOCK: 
    total-saldo = total-saldo + vhp.h-bill-line.betrag. 
  END.
END. 
