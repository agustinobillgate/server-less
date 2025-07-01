DEF TEMP-TABLE t-l-lager
  FIELD lager-nr LIKE l-lager.lager-nr
  FIELD bezeich  LIKE l-lager.bezeich.
DEF TEMP-TABLE temp-bediener LIKE bediener.
/*MT
DEF TEMP-TABLE t-l-ophdr     LIKE l-ophdr
    FIELD rec-id AS INT.
*/

DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER t-lschein      AS CHAR.
DEF INPUT  PARAMETER out-type       AS INTEGER.
DEF INPUT  PARAMETER t-datum        AS DATE.
DEF OUTPUT PARAMETER show-price     AS LOGICAL.
DEF OUTPUT PARAMETER req-flag       AS LOGICAL.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER closedate      AS DATE.
DEF OUTPUT PARAMETER mat-closedate  AS DATE.
DEF OUTPUT PARAMETER p-221          AS DATE.
/*MTDEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.*/
DEF OUTPUT PARAMETER TABLE FOR temp-bediener.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.

FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK. 
FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK. 
show-price = htparam.flogical. 
IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 

FIND FIRST htparam WHERE paramnr = 475 NO-LOCK. 
req-flag = NOT htparam.flogical. 

FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
p-221 = htparam.fdate. 
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
mat-closedate = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
IF t-lschein NE "" THEN
DO:
DEF VAR op-num AS INTEGER INITIAL 14 NO-UNDO.
  IF out-type = 2 THEN op-num = 13.
  FIND FIRST l-op WHERE l-op.artnr GE 3000000
    AND l-op.datum = t-datum
    AND l-op.op-art = op-num
    AND l-op.lscheinnr = t-lschein NO-LOCK NO-ERROR.
  IF AVAILABLE l-op THEN FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
END.
closedate = htparam.fdate. 
IF billdate GT closedate THEN billdate = closedate. 
/*MT
DO TRANSACTION: 
   CREATE l-ophdr.
   FIND CURRENT l-ophdr NO-LOCK.
   CREATE t-l-ophdr.
   BUFFER-COPY l-ophdr TO t-l-ophdr.
   ASSIGN t-l-ophdr.rec-id = RECID(l-ophdr).
END.
*/
FOR EACH bediener:
    CREATE temp-bediener.
    BUFFER-COPY bediener TO temp-bediener.
END.

FOR EACH l-lager:
    CREATE t-l-lager.
    ASSIGN
        t-l-lager.lager-nr = l-lager.lager-nr
        t-l-lager.bezeich  = l-lager.bezeich.
END.
