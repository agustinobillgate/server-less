
DEFINE TEMP-TABLE t-eg-property LIKE eg-property.

DEF OUTPUT PARAMETER TABLE FOR t-eg-property.
    
FOR EACH eg-property NO-LOCK:
    CREATE t-eg-property.
    BUFFER-COPY eg-property TO t-eg-property.
END.
