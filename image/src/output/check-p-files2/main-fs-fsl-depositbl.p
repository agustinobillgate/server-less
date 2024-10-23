
DEFINE TEMP-TABLE buf-bkveran LIKE bk-veran.

DEFINE INPUT PARAMETER fsl-veran-nr AS INT.
DEFINE INPUT PARAMETER fsl-deposit LIKE bk-veran.deposit.
DEFINE OUTPUT PARAMETER TABLE FOR buf-bkveran.

FOR EACH buf-bkveran:
    DELETE buf-bkveran.
END.

FIND FIRST bk-veran WHERE bk-veran.veran-nr = fsl-veran-nr 
  EXCLUSIVE-LOCK. 
bk-veran.deposit = fsl-deposit. 
FIND CURRENT bk-veran NO-LOCK. 

FIND FIRST bk-veran WHERE bk-veran.veran-nr = fsl-veran-nr  NO-LOCK NO-ERROR.
IF AVAILABLE bk-veran THEN DO:
    CREATE buf-bkveran.
    BUFFER-COPY bk-veran TO buf-bkveran.
END.
