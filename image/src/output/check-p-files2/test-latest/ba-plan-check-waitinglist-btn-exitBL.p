 
DEF INPUT PARAMETER rec-id AS INT.

DEF BUFFER resline FOR bk-reser. 
DEF BUFFER bf      FOR bk-func. 

FIND FIRST resline WHERE RECID(resline) = rec-id NO-LOCK.
DO TRANSACTION: 
    FIND CURRENT resline EXCLUSIVE-LOCK. 
    resline.resstatus = 2. 
    FIND CURRENT resline NO-LOCK. 
    FIND FIRST bf WHERE bf.veran-nr = resline.veran-nr 
        AND bf.veran-seite = resline.veran-seite EXCLUSIVE-LOCK. 
    IF bf.veran-seite GT 8 THEN
        ASSIGN
            bf.c-resstatus[1] = "T" 
            bf.r-resstatus[1] = 2 
            bf.resstatus = 2.
    ELSE 
        ASSIGN 
            bf.c-resstatus[bf.veran-seite] = "T" 
            bf.r-resstatus[bf.veran-seite] = 2 
            bf.resstatus = 2 . 
    FIND CURRENT bf NO-LOCK. 
END.

