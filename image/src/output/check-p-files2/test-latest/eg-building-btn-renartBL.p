
DEF INPUT PARAMETER build-number1 AS INT.
DEF OUTPUT PARAMETER fl-code AS INT INIT 0.

FIND FIRST eg-location WHERE eg-location.building = build-number1 
    NO-LOCK NO-ERROR.
IF AVAILABLE eg-location THEN fl-code = 1.
