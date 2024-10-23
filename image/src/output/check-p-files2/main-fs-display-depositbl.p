DEFINE TEMP-TABLE buf-bkveran LIKE bk-veran.

DEFINE INPUT PARAMETER veran-nr AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR buf-bkveran.

FOR EACH buf-bkveran:
    DELETE buf-bkveran.
END.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = veran-nr NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN DO:
    CREATE buf-bkveran.
    BUFFER-COPY bk-veran TO buf-bkveran.
END.
