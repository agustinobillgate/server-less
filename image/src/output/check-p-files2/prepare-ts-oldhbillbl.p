
DEFINE INPUT-OUTPUT PARAMETER rechnr AS INTEGER.

DEF INPUT PARAMETER knr          AS INT.
DEF INPUT PARAMETER curr-dept    AS INT.
DEF INPUT PARAMETER income-audit AS LOGICAL.

DEF OUTPUT PARAMETER supervise   AS LOGICAL.
DEF OUTPUT PARAMETER bill-date   AS DATE.

DEFINE buffer waiter FOR vhp.kellner.

FIND FIRST waiter WHERE waiter.kellner-nr = knr 
  AND waiter.departement = curr-dept NO-LOCK NO-ERROR. 
supervise = (AVAILABLE waiter AND waiter.masterkey) OR income-audit. 
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 NO-LOCK. 
bill-date = vhp.htparam.fdate. 
FIND FIRST vhp.hoteldpt WHERE vhp.hoteldpt.num = curr-dept NO-LOCK. 
 
IF rechnr = 0 AND AVAILABLE waiter THEN 
DO: 
  RUN find-billno. 
  /*MTDISP rechnr WITH FRAME frame1. */
END.


PROCEDURE find-billno: 
  FOR EACH vhp.h-journal WHERE vhp.h-journal.bill-datum = bill-date 
      AND vhp.h-journal.departement = curr-dept 
      AND vhp.h-journal.kellner-nr = knr AND vhp.h-journal.zeit GT 0 
      NO-LOCK USE-INDEX kellner_ix BY vhp.h-journal.sysdate descending 
      BY vhp.h-journal.zeit descending: 
      rechnr = vhp.h-journal.rechnr. 
      RETURN.
  END. 
END. 
