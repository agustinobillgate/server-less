DEFINE INPUT PARAMETER htparamNum AS INTEGER                     NO-UNDO.
DEFINE OUTPUT PARAMETER htplogic LIKE htparam.flogical INITIAL ? NO-UNDO.

htplogic = ?.
FIND FIRST htparam WHERE htparam.paramnr = htparamNum NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
  htplogic = htparam.flogical.
RETURN.
