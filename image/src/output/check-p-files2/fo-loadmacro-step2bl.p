DEFINE TEMP-TABLE t-parameters LIKE parameters.

DEFINE INPUT PARAMETER TABLE FOR t-parameters.

FOR EACH t-parameters:
    CREATE parameters.
    BUFFER-COPY t-parameters TO parameters.
END.
