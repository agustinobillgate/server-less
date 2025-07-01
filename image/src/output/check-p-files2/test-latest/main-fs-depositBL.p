
DEFINE TEMP-TABLE buf-bkveran LIKE bk-veran.



DEFINE INPUT PARAMETER bk-veran-recid AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR buf-bkveran.

FIND FIRST bk-veran WHERE RECID(bk-veran) = bk-veran-recid NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN DO:
    CREATE buf-bkveran.
    BUFFER-COPY bk-veran TO buf-bkveran.
END.
