
DEF INPUT PARAMETER rechnr AS INT.
DEF INPUT PARAMETER departement AS INT.
DEF OUTPUT PARAMETER flag AS LOGICAL INIT NO.

DEFINE BUFFER sp-bline   FOR vhp.h-bill-line.
FIND FIRST sp-bline WHERE sp-bline.rechnr = rechnr 
    AND sp-bline.departement = departement 
    AND sp-bline.waehrungsnr GT 0 NO-LOCK NO-ERROR.
IF AVAILABLE sp-bline THEN
DO:
    flag = YES.
    RETURN NO-APPLY. 
END.
