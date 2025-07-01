
DEF INPUT PARAMETER s-artnr     AS INT.
DEF INPUT PARAMETER curr-lager  AS INT.
DEF INPUT PARAMETER qty         AS DECIMAL.

DEF OUTPUT PARAMETER rest AS DECIMAL.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER htparam-paramgruppe AS INT.
DEF OUTPUT PARAMETER htparam-flogical AS LOGICAL.

DEFINE buffer l-oh FOR l-bestand. 

IF qty LT 0 THEN 
DO:
    FIND FIRST l-oh WHERE l-oh.artnr = s-artnr AND l-oh.lager-nr = curr-lager NO-LOCK NO-ERROR.
    IF AVAILABLE l-oh AND (anz-anf-best + anz-eingang - anz-ausgang + qty) LT 0 THEN 
    DO: 
        rest = (anz-anf-best + anz-eingang - anz-ausgang + qty).
        fl-code = 1.
    END.
END.

FIND FIRST htparam WHERE paramnr = 402 NO-LOCK.
htparam-paramgruppe = htparam.paramgruppe.
htparam-flogical = htparam.flogical.
