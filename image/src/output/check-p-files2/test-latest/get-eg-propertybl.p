DEFINE TEMP-TABLE t-eg-property LIKE eg-property.

DEFINE BUFFER qbuff FOR queasy.

DEFINE INPUT PARAMETER loc-nr AS INTEGER.
DEFINE INPUT PARAMETER zinr AS CHARACTER.
DEFINE INPUT PARAMETER maintask AS INTEGER.
DEFINE INPUT PARAMETER category AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-eg-property.

FOR EACH eg-property WHERE eg-property.location = loc-nr 
    AND eg-property.zinr = zinr NO-LOCK,
    FIRST queasy WHERE queasy.KEY = 133 AND queasy.number1 = eg-property.maintask NO-LOCK,
    FIRST qbuff WHERE qbuff.KEY = 132 AND qbuff.number1 = queasy.number2 
        AND qbuff.number1 = category NO-LOCK:

    CREATE t-eg-property.
    BUFFER-COPY eg-property TO t-eg-property.
END.


