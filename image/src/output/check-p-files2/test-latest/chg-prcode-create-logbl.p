DEFINE TEMP-TABLE t-res-history LIKE res-history.
DEFINE INPUT PARAMETER TABLE FOR t-res-history.

FOR EACH t-res-history:
    CREATE res-history.
    BUFFER-COPY t-res-history TO res-history.
END.

