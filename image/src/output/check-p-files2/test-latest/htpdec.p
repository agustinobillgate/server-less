DEFINE INPUT PARAMETER htparamNum AS INTEGER           NO-UNDO.
DEFINE OUTPUT PARAMETER htpdecimal LIKE htparam.fdecimal NO-UNDO.

htpdecimal = 0.
FIND FIRST htparam WHERE htparam.paramnr = htparamNum NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
  htpdecimal = htparam.fdecimal.
RETURN.
