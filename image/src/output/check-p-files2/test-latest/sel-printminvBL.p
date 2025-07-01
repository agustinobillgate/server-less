
DEF INPUT  PARAMETER ind     AS INTEGER.
DEF INPUT-OUTPUT PARAMETER briefnr AS INTEGER.

FIND FIRST htparam WHERE paramnr = 688 no-lock. /* layout FOR single line */ 
IF htparam.finteger GT 0 THEN 
DO: 
  FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
  IF AVAILABLE brief THEN briefnr = htparam.finteger. 
END. 
IF ind = 2 THEN
DO:
  FIND FIRST htparam WHERE paramnr = 495 no-lock. /* layout FOR single line */ 
  IF htparam.finteger GT 0 THEN
  DO: 
    FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
    IF AVAILABLE brief THEN briefnr = htparam.finteger. 
  END. 
END.
