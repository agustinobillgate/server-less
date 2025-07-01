
DEF TEMP-TABLE t-parameters LIKE parameters.

DEF INPUT PARAMETER TABLE FOR t-parameters.

FOR EACH t-parameters NO-LOCK:
    CREATE parameters.
    BUFFER-COPY t-parameters TO parameters.
END.
