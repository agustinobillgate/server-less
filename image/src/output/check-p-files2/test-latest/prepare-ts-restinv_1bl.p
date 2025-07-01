

DEF TEMP-TABLE hbill
    FIELD kellner-nr LIKE h-bill.kellner-nr.

DEF TEMP-TABLE t-kellner
    FIELD kellner-nr LIKE kellner.kellner-nr.

DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER curr-dept      AS INT.
DEF INPUT  PARAMETER curr-printer   AS INT.
DEF INPUT  PARAMETER user-init-str  AS CHAR.
DEF INPUT  PARAMETER transdate      AS DATE.

DEF OUTPUT PARAMETER mealcoupon-cntrl   AS LOGICAL.
DEF OUTPUT PARAMETER must-print         AS LOGICAL.
DEF OUTPUT PARAMETER zero-flag          AS LOGICAL.
DEF OUTPUT PARAMETER multi-cash         AS LOGICAL.
DEF OUTPUT PARAMETER cancel-exist       AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER msg-str            AS CHAR.

DEF OUTPUT PARAMETER disc-art1          AS INT.
DEF OUTPUT PARAMETER disc-art2          AS INT.
DEF OUTPUT PARAMETER disc-art3          AS INT.
DEF OUTPUT PARAMETER mi-ordertaker      AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER price-decimal      AS INT.
DEF OUTPUT PARAMETER curr-local         AS CHAR.
DEF OUTPUT PARAMETER curr-foreign       AS CHAR.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL.
DEF OUTPUT PARAMETER foreign-rate       AS LOGICAL.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL INIT 1.
DEF OUTPUT PARAMETER b-title            AS CHAR.
DEF OUTPUT PARAMETER deptname           AS CHAR.
DEF OUTPUT PARAMETER p-223              AS LOGICAL.
DEF OUTPUT PARAMETER curr-waiter        AS INT INIT 0.
DEF OUTPUT PARAMETER fl-code            AS INT INIT 0.
DEF OUTPUT PARAMETER pos1               AS INT.
DEF OUTPUT PARAMETER pos2               AS INT.
DEF OUTPUT PARAMETER cashless-flag      AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER c-param870         AS CHAR.
DEF OUTPUT PARAMETER activate-deposit   AS LOGICAL.
/*DEF OUTPUT PARAMETER p-451              AS CHARACTER.*/
DEF OUTPUT PARAMETER TABLE FOR hbill.
DEF OUTPUT PARAMETER TABLE FOR t-kellner.


DEFINE BUFFER bill-guest FOR vhp.guest. 

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

DEFINE VARIABLE user-init AS CHAR NO-UNDO.
DEFINE VARIABLE from-acct AS LOGICAL INIT NO.

/*
FIND FIRST htparam WHERE htparam.paramnr = 451 NO-LOCK. 
p-451 = vhp.htparam.fchar.
*/
/*FT 23/12/2014*/
IF NUM-ENTRIES(user-init-str,";") GT 1 THEN
    ASSIGN
        user-init = ENTRY(1,user-init-str,";")
        from-acct = LOGICAL(ENTRY(2,user-init-str,";")).
ELSE user-init = user-init-str. 

FIND FIRST PRINTER WHERE PRINTER.nr = curr-printer NO-LOCK NO-ERROR.
IF NOT AVAILABLE PRINTER THEN
DO:
  msg-str = msg-str + CHR(2)
          + translateExtended ("Number Printer ",lvCAREA,"")
          + STRING(curr-printer)
          + translateExtended (" was not defined in Printer Administration.",lvCAREA,"").
  RETURN. 
END.

/* SY 27/02/2014 */
FIND FIRST htparam WHERE htparam.paramnr = 834 NO-LOCK.
ASSIGN cashless-flag = htparam.flogical.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 274 NO-LOCK. 
mealcoupon-cntrl = flogical. 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 877 NO-LOCK. 
must-print = flogical. 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 869 NO-LOCK. 
zero-flag = flogical. 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 833 NO-LOCK. 
multi-cash = flogical. 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 870 NO-LOCK. 
c-param870 = fchar. 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 588 NO-LOCK. 
activate-deposit = flogical. 

FIND FIRST vhp.queasy WHERE vhp.queasy.key = 11 NO-LOCK NO-ERROR. 
cancel-exist = AVAILABLE vhp.queasy. 

FIND FIRST vhp.htparam WHERE htpara.paramnr = 867 NO-LOCK. 
FIND FIRST bill-guest WHERE bill-guest.gastnr = vhp.htparam.finteger 
  NO-LOCK NO-ERROR. 
IF NOT AVAILABLE bill-guest THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("GuestNo (Param 867) for credit restaurant undefined",lvCAREA,"")
          + CHR(10)
          + translateExtended ("Posting not possible.",lvCAREA,"").
  RETURN. 
END. 


FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
  disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
  disc-art2 = vhp.htparam.finteger.
FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK.
  disc-art3 = vhp.htparam.finteger.

FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 NO-LOCK NO-ERROR.
IF NOT AVAILABLE vhp.queasy THEN mi-ordertaker = NO.

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

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = curr-dept NO-LOCK. 
b-title = vhp.hoteldpt.depart + " Bills". 
IF AVAILABLE vhp.waehrung THEN 
  b-title = b-title + " / Today's Exchange Rate = " + STRING(exchg-rate). 
deptname = vhp.hoteldpt.depart. 

/* SY 16 NOV 2015 */
FIND FIRST htparam WHERE htparam.paramnr = 300 NO-LOCK. /* micros flag */
b-title = b-title + ";" + STRING(htparam.flogical).

FIND FIRST htparam WHERE htparam.paramnr = 223 NO-LOCK. 
p-223 = htparam.flogical.

ASSIGN
    /*MTcurr-user = user-init + " " + user-name*/
    curr-waiter = INTEGER(user-init)
.

FIND FIRST vhp.kellner WHERE vhp.kellner.kellner-nr = curr-waiter 
  AND vhp.kellner.departement = curr-dept NO-LOCK NO-ERROR. 
IF NOT AVAILABLE vhp.kellner THEN curr-waiter = 0.
IF AVAILABLE vhp.kellner THEN
DO:
    CREATE t-kellner.
    ASSIGN t-kellner.kellner-nr = kellner.kellner-nr.
END.

IF from-acct THEN RUN chg-billdate(NO).
/*dody 230124 stuck trace*/
FOR EACH h-bill WHERE h-bill.departement = curr-dept AND h-bill.flag = 0 NO-LOCK:
    CREATE hbill.
    ASSIGN
      hbill.kellner-nr = h-bill.kellner-nr.
END.

FIND FIRST vhp.htparam WHERE paramnr = 337 NO-LOCK. 
pos1 =  vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 338 NO-LOCK. 
pos2 =  vhp.htparam.finteger. 

PROCEDURE chg-billdate: 
DEFINE INPUT PARAMETER message-flag AS LOGICAL. 
DEFINE VARIABLE zugriff             AS LOGICAL. 
DEFINE VARIABLE datum               AS DATE. 
DEFINE BUFFER vhpusr FOR vhp.bediener. 
  FIND FIRST vhpusr WHERE vhpusr.userinit = user-init NO-LOCK. 
  IF SUBSTR(vhpusr.permission,15,1) GE "1" OR 
     SUBSTR(vhpusr.permission,38,1) GE "1" THEN 
  DO: 
    datum = transdate.
    fl-code = 1.
    /*MTRUN clbill-postdate.p(INPUT-OUTPUT datum). 
    IF datum NE ? THEN 
    DO: 
      transdate = datum. 
      FIND FIRST vhp.htparam WHERE paramnr = 110 NO-LOCK. 
      IF vhp.htparam.fdate NE transdate AND double-currency THEN 
      DO: 
        FIND FIRST vhp.exrate WHERE vhp.exrate.datum = transdate 
          NO-LOCK NO-ERROR. 
        IF AVAILABLE vhp.exrate THEN exchg-rate = vhp.exrate.betrag. 
      END. 
    END.*/
  END.
  ELSE IF message-flag THEN 
  DO:
    msg-str = msg-str + CHR(2)
            + translateExtended ("Sorry, no access right.",lvCAREA,"").
  END.
END.
