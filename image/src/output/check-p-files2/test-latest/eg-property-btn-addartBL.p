
DEF OUTPUT PARAMETER nr AS INT.

DEFINE VARIABLE temp-nr AS INTEGER INITIAL 0.

FOR EACH eg-property NO-LOCK BY eg-property.nr:
    IF temp-nr = 0 THEN
    DO:
        temp-nr = eg-property.nr.
    END.
    ELSE
    DO:
        IF temp-nr < eg-property.nr THEN
            temp-nr = eg-property.nr.
        ELSE temp-nr = temp-nr.
    END.
END.
nr = temp-nr + 1. 
