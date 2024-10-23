
DEF INPUT PARAMETER q-order-nr AS CHAR.
DEF OUTPUT PARAMETER found AS LOGICAL INITIAL NO. 

FIND FIRST fa-order WHERE fa-order.order-nr = q-order-nr 
  AND fa-order.fa-pos GT 0 AND fa-order.activeflag = 0 
  AND (fa-order.order-qty NE fa-order.delivered-qty) NO-LOCK NO-ERROR. 
IF AVAILABLE fa-order THEN found = YES. 
ELSE 
DO WHILE (NOT found) AND  AVAILABLE fa-order: 
  FIND NEXT fa-order WHERE fa-order.order-nr = q-order-nr
    AND fa-order.fa-pos GT 0 AND fa-order.activeflag = 0 
    AND (fa-order.order-qty NE fa-order.delivered-qty) NO-LOCK NO-ERROR. 
  IF AVAILABLE fa-order THEN found = YES. 
END. 
