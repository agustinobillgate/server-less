
DEFINE buffer gl-jouhdr1 FOR gl-jouhdr.

DEF INPUT PARAMETER refno AS CHAR.
DEF OUTPUT PARAMETER err-no AS INT INIT 0.

FIND FIRST gl-jouhdr1 WHERE gl-jouhdr1.refno = refno 
    AND gl-jouhdr1.jtype = 7 NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr1 THEN err-no = 1.
