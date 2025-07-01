
DEFINE TEMP-TABLE MENU 
    FIELD pos AS int 
    FIELD bezeich AS CHAR 
    FIELD artnr AS int. 

DEFINE TEMP-TABLE Lhbline 
  FIELD nr AS INTEGER 
  FIELD rid AS INTEGER. 

DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line
    FIELD rec-id AS INT.

DEF INPUT  PARAMETER dept               AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER tischnr            AS INTEGER NO-UNDO.

DEF OUTPUT PARAMETER multi-vat          AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER zero-flag          AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER multi-cash         AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER price-decimal      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER foreign-rate       AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER double-currency    AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER exchg-rate         AS DECIMAL NO-UNDO INIT 1.
DEF OUTPUT PARAMETER deptname           AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER must-print         AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER fl-warn            AS LOGICAL NO-UNDO INIT NO.
DEF OUTPUT PARAMETER max-Lapos          AS INTEGER NO-UNDO INIT 0.
DEF OUTPUT PARAMETER cashless-flag      AS LOGICAL NO-UNDO.

DEF OUTPUT PARAMETER TABLE FOR t-h-bill.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.
DEF OUTPUT PARAMETER TABLE FOR MENU.
DEF OUTPUT PARAMETER TABLE FOR Lhbline.

/* SY 27/02/2014 */
FIND FIRST htparam WHERE htparam.paramnr = 834 NO-LOCK.
ASSIGN cashless-flag = htparam.flogical.

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 271 NO-LOCK. 
IF vhp.htparam.feldtyp = 4 THEN multi-vat = vhp.htparam.flogical.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 869 NO-LOCK. 
zero-flag = flogical. 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 833 NO-LOCK. 
multi-cash = flogical.


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491. 
price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 143 NO-LOCK. 
foreign-rate = vhp.htparam.flogical. 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 240 NO-LOCK. 
double-currency = vhp.htparam.flogical. 

IF FOREIGN-RATE THEN 
DO: 
  FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 144 NO-LOCK. 
  FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz 
    = vhp.htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.waehrung THEN exchg-rate 
    = vhp.waehrung.ankauf / vhp.waehrung.einheit. 
END. 

FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = dept NO-LOCK. 
deptname = vhp.hoteldpt.depart. 
 
FIND FIRST vhp.htparam WHERE htpara.paramnr = 877 NO-LOCK. 
must-print = flogical. 


FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement = dept 
  AND vhp.h-bill.tischnr = tischnr AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE h-bill THEN RETURN. /*FT serverless*/
        
CREATE t-h-bill.
BUFFER-COPY h-bill TO t-h-bill.
ASSIGN t-h-bill.rec-id = RECID(h-bill).


FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 948 NO-LOCK.
IF vhp.htparam.paramgr = 19 AND vhp.htparam.flogical THEN 
/* print TOTAL Food/Bev amount */
DO:
  FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. /*rest food disc artNo */ 
  FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = vhp.h-bill.rechnr
      AND vhp.h-bill-line.departement = dept
      AND vhp.h-bill-line.artnr = vhp.htparam.finteger
      AND vhp.h-bill-line.betrag NE 0 NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.h-bill-line THEN
  DO:
    fl-warn = YES.
  END.
END.

FOR EACH h-bill-line WHERE h-bill-line.departement = dept 
    AND h-bill-line.tischnr = tischnr 
    AND h-bill-line.rechnr = h-bill.rechnr NO-LOCK:
    CREATE t-h-bill-line.
    BUFFER-COPY h-bill-line TO t-h-bill-line.
    ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).
END.

RUN ts-splitbill-build-lmenubl.p
    (RECID(h-bill), dept, OUTPUT max-Lapos, OUTPUT TABLE menu, 
     OUTPUT TABLE Lhbline).
