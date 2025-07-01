
DEF INPUT PARAMETER hbrecid AS INT.

DEF OUTPUT PARAMETER order-id        AS CHAR.
DEF OUTPUT PARAMETER prdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEF OUTPUT PARAMETER disc-art1       AS INTEGER INITIAL -1   NO-UNDO. 
DEF OUTPUT PARAMETER disc-art2       AS INTEGER INITIAL -1   NO-UNDO. 
DEF OUTPUT PARAMETER disc-art3       AS INTEGER INITIAL -1   NO-UNDO. 
DEF OUTPUT PARAMETER disc-zwkum      AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER print-balance   AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER incl-service    AS LOGICAL. 
DEF OUTPUT PARAMETER incl-mwst       AS LOGICAL.
DEF OUTPUT PARAMETER service-taxable AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER print-fbTotal   AS LOGICAL INITIAL NO NO-UNDO. 

DEFINE VARIABLE curr-dept       AS INTEGER NO-UNDO.

FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = hbrecid NO-LOCK NO-ERROR. /* Malik Serverless 520 NO-LOCK -> NO-LOCK NO-ERROR */ 
IF AVAILABLE vhp.h-bill THEN
DO:
  ASSIGN curr-dept = vhp.h-bill.departement.
  IF vhp.h-bill.betriebsnr NE 0 THEN 
  DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 
        AND vhp.queasy.number1 = vhp.h-bill.betriebsnr NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN order-id = "/" + vhp.queasy.char1. 
  END. 
END.

FIND FIRST vhp.htparam WHERE paramnr = 857 NO-LOCK. 
prdisc-flag = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = disc-art1
  AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-artikel THEN disc-zwkum = vhp.h-artikel.zwkum.

FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN disc-art2 = vhp.htparam.finteger. 
IF disc-zwkum = 0 AND disc-art2 NE 0 THEN
DO:
  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = disc-art2
    AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.h-artikel THEN disc-zwkum = vhp.h-artikel.zwkum.
END.

FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN disc-art3 = vhp.htparam.finteger. 
IF disc-zwkum = 0 AND disc-art3 NE 0 THEN
DO:
  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = disc-art3
    AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
  IF AVAILABLE vhp.h-artikel THEN disc-zwkum = vhp.h-artikel.zwkum.
END.
 
FIND FIRST vhp.htparam WHERE paramnr = 899 NO-LOCK. 
print-balance = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK. 
incl-service = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK. 
incl-mwst = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK. 
service-taxable = vhp.htparam.flogical. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 948 NO-LOCK.
IF vhp.htparam.paramgr = 19 AND vhp.htparam.flogical THEN
  print-fbTotal = htparam.flogical.
