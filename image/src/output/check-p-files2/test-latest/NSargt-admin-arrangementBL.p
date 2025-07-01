
DEF INPUT PARAMETER p-arrangement   AS CHAR.
DEF INPUT PARAMETER p-argtnr        AS INT.
DEF OUTPUT PARAMETER avail-arr      AS LOGICAL INIT NO.

DEFINE buffer arr1 FOR arrangement. 

FIND FIRST arr1 WHERE arr1.arrangement = p-arrangement
    AND arr1.argtnr NE p-argtnr NO-LOCK NO-ERROR.
IF AVAILABLE arr1 THEN avail-arr = YES.
