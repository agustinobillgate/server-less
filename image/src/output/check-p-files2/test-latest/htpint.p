DEFINE INPUT PARAMETER htparamNum AS INTEGER                   NO-UNDO.
DEFINE OUTPUT PARAMETER htpint LIKE htparam.finteger INITIAL 0 NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = htparamNum NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
  htpint = htparam.finteger.
RETURN.
