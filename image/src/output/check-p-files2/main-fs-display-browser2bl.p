DEF TEMP-TABLE q2-list
    FIELD rechnr            AS INT
    FIELD bk-veran-recid    AS INT
    FIELD resstatus         LIKE bk-veran.resstatus
    FIELD veran-nr          LIKE bk-veran.veran-nr
    FIELD anlass            LIKE bk-veran.anlass.

DEF INPUT  PARAMETER b1-resnr       AS INT.
DEF INPUT  PARAMETER glist-gastnr   AS INT.
DEF INPUT  PARAMETER rsvsort        AS INT.
DEF INPUT  PARAMETER guestsort      AS INT.
DEF INPUT  PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER bq-rechnr      AS INT.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

DEF BUFFER bkres-buff FOR bk-reser. 
DEF BUFFER bkgast FOR guest. 

IF b1-resnr NE 0 THEN 
FOR EACH bk-veran WHERE bk-veran.gastnr = glist-gastnr 
    AND bk-veran.activeflag = 0 AND bk-veran.veran-nr = b1-resnr 
    USE-INDEX gastnr_ix NO-LOCK, 
    FIRST bkres-buff WHERE bkres-buff.veran-nr = bk-veran.veran-nr 
    AND bkres-buff.resstatus = rsvsort NO-LOCK, 
    FIRST bkgast WHERE bkgast.gastnr = bk-veran.gastnr 
    AND bkgast.karteityp = guestsort NO-LOCK BY bk-veran.veran-nr:
    RUN create-q2-list.
END.
ELSE 
FOR EACH bk-veran WHERE bk-veran.gastnr = glist-gastnr 
    AND bk-veran.activeflag = 0 
    AND bk-veran.limit-date LE to-date USE-INDEX gastnr_ix NO-LOCK, 
    FIRST bkres-buff WHERE bkres-buff.veran-nr = bk-veran.veran-nr 
    AND bkres-buff.resstatus = rsvsort NO-LOCK, 
    FIRST bkgast WHERE bkgast.gastnr = bk-veran.gastnr 
    AND bkgast.karteityp = guestsort NO-LOCK BY bk-veran.veran-nr:
    RUN create-q2-list.
END.
 
IF AVAILABLE bk-veran THEN bq-rechnr = bk-veran.rechnr. 

PROCEDURE create-q2-list:
    CREATE q2-list.
    ASSIGN
        q2-list.rechnr            = bk-veran.rechnr
        q2-list.bk-veran-recid    = RECID(bk-veran)
        q2-list.resstatus         = bk-veran.resstatus
        q2-list.veran-nr          = bk-veran.veran-nr
        q2-list.anlass            = bk-veran.anlass.
END.
