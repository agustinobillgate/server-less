DEFINE buffer bk-rsv FOR bk-reser. 
DEF TEMP-TABLE q3-list
    FIELD bk-func-recid AS INT
    FIELD bk-rsv-recid  AS INT
    FIELD veran-seite   LIKE bk-rsv.veran-seite
    FIELD veran-resnr   LIKE bk-rsv.veran-resnr
    FIELD raum          LIKE bk-rsv.raum
    FIELD datum         LIKE bk-func.datum
    FIELD bis-datum     LIKE bk-func.bis-datum
    FIELD resstatus     LIKE bk-func.resstatus
    FIELD kartentext    LIKE bk-func.kartentext
    FIELD sonstiges     LIKE bk-func.sonstiges
    FIELD veran-nr      LIKE bk-func.veran-nr
    FIELD von-zeit      LIKE bk-rsv.von-zeit
    FIELD bis-zeit      LIKE bk-rsv.bis-zeit.

DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER b1-resline     AS INT.
DEF INPUT  PARAMETER show-all       AS LOGICAL.
DEF INPUT  PARAMETER rsvsort        AS INT.
DEF INPUT  PARAMETER recid-bk-veran AS INT.
DEF OUTPUT PARAMETER TABLE FOR q3-list.

FIND FIRST bk-veran WHERE RECID(bk-veran) = recid-bk-veran.
IF b1-resnr NE 0 AND NOT show-all THEN DO:
FOR EACH bk-func WHERE bk-func.veran-nr = b1-resnr 
    AND bk-func.veran-seite = b1-resline USE-INDEX vernr-pg-ix NO-LOCK, 
    FIRST bk-rsv WHERE bk-rsv.veran-nr = bk-func.veran-nr 
    AND bk-rsv.veran-resnr = bk-func.veran-seite NO-LOCK 
    BY bk-rsv.veran-resnr:
    RUN create-q3-list.
END.
END.
ELSE IF b1-resnr NE 0 AND show-all THEN DO:
FOR EACH bk-func WHERE bk-func.veran-nr = b1-resnr 
    AND bk-func.resstatus EQ rsvsort /*LE 3*/ USE-INDEX vernr-pg-ix NO-LOCK, 
    FIRST bk-rsv WHERE bk-rsv.veran-nr = bk-func.veran-nr 
    AND bk-rsv.veran-resnr = bk-func.veran-seite NO-LOCK 
    BY bk-rsv.veran-resnr:
    RUN create-q3-list.
END.
END.
ELSE DO:
 FOR EACH bk-func WHERE bk-func.veran-nr = bk-veran.veran-nr 
    AND bk-func.resstatus = rsvsort USE-INDEX vernr-pg-ix NO-LOCK, 
    FIRST bk-rsv WHERE bk-rsv.veran-nr = bk-func.veran-nr 
    AND bk-rsv.veran-resnr = bk-func.veran-seite NO-LOCK 
    BY bk-rsv.veran-resnr:
    RUN create-q3-list.
 END.
END.


PROCEDURE create-q3-list:
DEF VAR i AS INT.
    CREATE q3-list.
    ASSIGN
        q3-list.bk-func-recid = RECID(bk-func)
        q3-list.bk-rsv-recid  = RECID(bk-rsv)
        q3-list.veran-seite   = bk-rsv.veran-seite
        q3-list.veran-resnr   = bk-rsv.veran-resnr
        q3-list.raum          = bk-rsv.raum
        q3-list.datum         = bk-func.datum
        q3-list.bis-datum     = bk-func.bis-datum
        q3-list.resstatus     = bk-func.resstatus
        q3-list.veran-nr      = bk-func.veran-nr
        q3-list.von-zeit      = bk-rsv.von-zeit
        q3-list.bis-zeit      = bk-rsv.bis-zeit.

    DO i = 1 TO 8:
        ASSIGN
            q3-list.kartentext[i]    = bk-func.kartentext[i]
            q3-list.sonstiges[i]     = bk-func.sonstiges[i].
        /*i = i + 1.*/
    END.
END.
