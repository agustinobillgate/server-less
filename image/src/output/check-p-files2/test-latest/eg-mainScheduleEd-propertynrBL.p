
DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER m-propertynr AS INT.
DEF INPUT PARAMETER h-location AS INT.
DEF INPUT PARAMETER h-zinr AS CHAR.

DEF OUTPUT PARAMETER avail-eg-property AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER t-maintask AS INT.
DEF OUTPUT PARAMETER t-bezeich AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

IF case-type = 1 THEN
    FIND FIRST eg-property WHERE 
        eg-property.nr = m-propertynr AND 
        eg-property.location = h-location AND 
        eg-property.zinr = h-zinr NO-LOCK NO-ERROR.
ELSE IF case-type = 2 THEN
    FIND FIRST eg-property WHERE 
        eg-property.nr = m-propertynr AND 
        eg-property.location = h-location NO-LOCK NO-ERROR.

IF AVAILABLE eg-property THEN
DO:
    avail-eg-property = YES.
    t-maintask = eg-property.maintask.
    t-bezeich = eg-property.bezeich.
    FOR EACH queasy WHERE KEY = 132 OR KEY = 133 NO-LOCK:
        CREATE t-queasy.
        BUFFER-COPY queasy TO t-queasy.
    END.
END.
     
