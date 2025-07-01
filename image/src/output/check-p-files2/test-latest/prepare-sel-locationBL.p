

DEF TEMP-TABLE t-eg-location LIKE eg-location.
DEF TEMP-TABLE t-queasy      LIKE queasy.

DEF OUTPUT PARAMETER TABLE FOR t-eg-location.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

FOR EACH queasy WHERE queasy.KEY = 135:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

FOR EACH eg-location:
    CREATE t-eg-location.
    BUFFER-COPY eg-location TO t-eg-location.
END.
