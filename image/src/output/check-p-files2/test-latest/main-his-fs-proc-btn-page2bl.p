DEFINE OUTPUT PARAMETER lAvail AS LOGICAL.

lAvail = NO.
FIND FIRST htparam WHERE htparam.paramnr = 900 USE-INDEX paramnr_ix NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN 
DO: 
  FIND FIRST zwkum WHERE zwkum.departement = htparam.finteger AND zwkum.zknr LT 100 USE-INDEX zknr_ix NO-LOCK NO-ERROR. 
  IF AVAILABLE zwkum THEN 
  DO:
      lAvail = YES.
  END.
END.

