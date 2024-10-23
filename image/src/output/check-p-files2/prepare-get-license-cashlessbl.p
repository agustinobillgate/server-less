DEFINE OUTPUT PARAMETER cashless-license    AS LOGICAL. /*FDL - Cashless Payment Feature*/
DEFINE OUTPUT PARAMETER cashless-minsaldo   AS DECIMAL. /*FDL - Cashless Payment Feature*/

FIND FIRST htparam WHERE htparam.paramnr EQ 1022 
    AND htparam.bezeich NE "not used"
    AND htparam.flogical NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN cashless-license = YES.

FIND FIRST htparam WHERE htparam.paramnr EQ 586 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN cashless-minsaldo = htparam.fdecimal.
