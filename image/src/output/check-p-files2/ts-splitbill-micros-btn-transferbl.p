DEFINE TEMP-TABLE vat-list  
  FIELD vatProz AS DECIMAL INITIAL 0  
  FIELD vatAmt  AS DECIMAL INITIAL 0  
  FIELD netto   AS DECIMAL INITIAL 0  
  FIELD betrag  AS DECIMAL INITIAL 0  
  FIELD fBetrag AS DECIMAL INITIAL 0.  
  
DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line  
    FIELD rec-id AS INT.  
  
DEF INPUT PARAMETER rec-id-h-bill   AS INT.  
DEF INPUT PARAMETER curr-select     AS INT.  
DEF INPUT PARAMETER multi-vat       AS LOGICAL.  
DEF INPUT PARAMETER balance         AS DECIMAL.  
DEF INPUT PARAMETER transf-str      AS CHAR.
DEF INPUT PARAMETER pay-type        AS INT.  
DEF INPUT PARAMETER transdate       AS DATE.  
DEF INPUT PARAMETER price-decimal   AS INT.  
DEF INPUT PARAMETER exchg-rate      AS DECIMAL.  
DEF INPUT PARAMETER foreign-rate    AS LOGICAL.  
  
DEF INPUT PARAMETER dept            AS INT.  
DEF INPUT PARAMETER change-str      AS CHAR.  
DEF INPUT PARAMETER add-zeit        AS INT.  
DEF INPUT PARAMETER hoga-card       AS CHAR.  
DEF INPUT PARAMETER cancel-str      AS CHAR.  
DEF INPUT PARAMETER curr-waiter     AS INTEGER.  
DEF INPUT PARAMETER curr-room       AS CHAR.  
DEF INPUT PARAMETER user-init       AS CHAR.  
DEF INPUT PARAMETER cc-comment      AS CHAR.  
DEF INPUT PARAMETER guestnr         AS INT.  
DEF INPUT PARAMETER tischnr         AS INT.  
  
DEF INPUT PARAMETER double-currency AS LOGICAL.  
  
DEF INPUT-OUTPUT PARAMETER amount-foreign AS DECIMAL.  
DEF OUTPUT PARAMETER err-flag       AS INT INIT 0.  
DEF OUTPUT PARAMETER billart        AS INT.  
DEF OUTPUT PARAMETER qty            AS INT.  
DEF OUTPUT PARAMETER price          AS DECIMAL.  
DEF OUTPUT PARAMETER amount         AS DECIMAL.  
DEF OUTPUT PARAMETER transfer-zinr  AS CHAR.  
DEF OUTPUT PARAMETER bill-date      AS DATE.  
DEF OUTPUT PARAMETER fl-code        AS INT.  
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.  
  
DEF VAR payment-found AS LOGICAL INITIAL NO NO-UNDO.  
DEFINE BUFFER kellner1 FOR vhp.kellner.   
  
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill.  
      
FOR EACH vhp.h-bill-line NO-LOCK WHERE   
    vhp.h-bill-line.rechnr = vhp.h-bill.rechnr  
    AND vhp.h-bill-line.departement = vhp.h-bill.departement  
    AND vhp.h-bill-line.waehrungsnr = curr-select,  
    FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.h-bill-line.artnr  
      AND vhp.h-artikel.departement = vhp.h-bill-line.departement  
      AND vhp.h-artikel.artart NE 0 NO-LOCK:  
    payment-found = YES.  
    LEAVE.  
END.  
IF payment-found AND multi-vat THEN  
DO:  
    err-flag = 1.  
    RETURN NO-APPLY.  
END.  
  
ASSIGN  
    billart         = 0  
    qty             = 1  
    price           = 0   
    amount          = - balance  
    transfer-zinr   = ENTRY(2, ENTRY(1, transf-str, "*"), " ")
. 

RUN ts-splitbill-update-billbl.p  
  (rec-id-h-bill, 0, 1, 0, dept, amount, transdate, billart, transfer-zinr, change-str, qty, tischnr,  
   price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
   curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
  
IF ROUND(vhp.h-bill.saldo, price-decimal) = 0 THEN   
DO:   
    RUN del-queasy.   
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
    vhp.h-bill.flag = 1.   
    FIND CURRENT vhp.h-bill NO-LOCK.   
    fl-code = 1.  
    /*MTAPPLY "choose" TO btn-b IN FRAME frame1.*/  
END.   
ELSE fl-code = 2.  
  
FOR EACH h-bill-line WHERE h-bill-line.departement = dept
    AND h-bill-line.rechnr = h-bill.rechnr NO-LOCK:  
  CREATE t-h-bill-line.  
  BUFFER-COPY h-bill-line TO t-h-bill-line.  
  ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
END.  
      
PROCEDURE del-queasy:   
  FOR EACH vhp.queasy WHERE vhp.queasy.key = 4   
    AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
    AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0:   
    DELETE vhp.queasy.   
  END.   
END.   
  
