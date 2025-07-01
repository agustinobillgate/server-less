  
DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line  
    FIELD rec-id AS INT.  
  
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.  
DEF INPUT  PARAMETER rec-id-h-bill AS INT.  
DEF INPUT PARAMETER dept AS INT.  
DEF INPUT PARAMETER guestnr AS INT.  
DEF INPUT PARAMETER paid AS DECIMAL.  
DEF INPUT PARAMETER price-decimal AS INT.  
  
DEF INPUT PARAMETER transdate AS DATE.  
DEF INPUT PARAMETER change-str AS CHAR.  
DEF INPUT PARAMETER tischnr AS INT.  
DEF INPUT PARAMETER add-zeit AS INT.  
DEF INPUT PARAMETER curr-select AS INT.  
DEF INPUT PARAMETER hoga-card AS CHAR.  
DEF INPUT PARAMETER cancel-str AS CHAR.  
DEF INPUT PARAMETER curr-waiter AS INTEGER.  
DEF INPUT PARAMETER amount-foreign AS DECIMAL.  
DEF INPUT PARAMETER curr-room AS CHAR.  
DEF INPUT PARAMETER user-init AS CHAR.  
DEF INPUT PARAMETER cc-comment AS CHAR.  
  
DEF OUTPUT PARAMETER billart AS INT.  
DEF OUTPUT PARAMETER qty AS INT.  
DEF OUTPUT PARAMETER description AS CHAR.  
DEF OUTPUT PARAMETER amount AS DECIMAL.  
  
DEF OUTPUT PARAMETER price AS DECIMAL.  
DEF OUTPUT PARAMETER bill-date AS DATE.  
  
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.  
DEF OUTPUT PARAMETER msg-str AS CHAR.  
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.  
  
  
DEFINE buffer bill-guest FOR vhp.guest.   
  
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill.  
  RUN check-rpaymentbl.p(pvILanguage, guestnr, h-bill.departement,  
                     OUTPUT billart, OUTPUT msg-str).   
  IF billart GT 0 THEN   
  DO:   
    FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement =  
      vhp.h-bill.departement AND vhp.h-artikel.artnrfront = billart   
      AND vhp.h-artikel.artart = 2 NO-LOCK NO-ERROR.   
    IF AVAILABLE vhp.h-artikel THEN   
    DO:   
      FIND FIRST bill-guest WHERE bill-guest.gastnr = guestnr NO-LOCK.   
      billart = vhp.h-artikel.artnr.   
      qty = 1.   
      description = vhp.h-artikel.bezeich.   
      amount = paid.   
      RUN ts-splitbill-update-billbl.p  
          (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
           price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
           curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
        
      IF ROUND(vhp.h-bill.saldo, price-decimal) = 0 THEN   
      DO:   
        RUN del-queasy.   
        FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
        vhp.h-bill.flag = 1.   
        FIND CURRENT vhp.h-bill NO-LOCK.  
        fl-code = 1.  
      END.   
      ELSE DO:   
        fl-code = 2.  
      END.   
    END.   
    ELSE DO:  
      fl-code = 3.  
    END.   
  END.  
  
FOR EACH h-bill-line WHERE h-bill-line.departement = dept
    AND h-bill-line.rechnr = h-bill.rechnr NO-LOCK:  
  CREATE t-h-bill-line.  
  BUFFER-COPY h-bill-line TO t-h-bill-line.  
  ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
END.  
  
PROCEDURE del-queasy:   
  FOR EACH vhp.queasy WHERE vhp.queasy.key = 4   
    AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
    AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK:   
    DELETE vhp.queasy.   
  END.   
  RELEASE vhp.queasy.
END.   
