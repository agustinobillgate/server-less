
DEFINE BUFFER mat-buff FOR mathis.
DEFINE TEMP-TABLE q1-list
    FIELD mathis-name   LIKE mathis.NAME
    FIELD mathis-asset  LIKE mathis.asset
    FIELD location      LIKE mathis.location
    FIELD warenwert     LIKE fa-artikel.warenwert
    FIELD nr            LIKE mat-buff.nr
    FIELD matbuff-name  LIKE mat-buff.NAME
    FIELD matbuff-asset LIKE mat-buff.asset
    FIELD deleted       LIKE fa-artikel.deleted
    FIELD did           LIKE fa-artikel.did
    FIELD recid-fa-artikel AS INT.

DEF INPUT  PARAMETER fdate AS DATE.
DEF INPUT  PARAMETER tdate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FOR EACH fa-artikel WHERE fa-artikel.deleted GE fdate
    AND fa-artikel.deleted LE tdate NO-LOCK, FIRST mathis WHERE mathis.nr = fa-artikel.nr
    AND mathis.flag = 2 NO-LOCK, FIRST mat-buff WHERE mat-buff.nr = fa-artikel.p-nr
    NO-LOCK BY fa-artikel.deleted:
    CREATE q1-list.
    ASSIGN
        q1-list.mathis-name   = mathis.NAME
        q1-list.mathis-asset  = mathis.asset
        q1-list.location      = mathis.location
        q1-list.warenwert     = fa-artikel.warenwert
        q1-list.nr            = mat-buff.nr
        q1-list.matbuff-name  = mat-buff.NAME
        q1-list.matbuff-asset = mat-buff.asset
        q1-list.deleted       = fa-artikel.deleted
        q1-list.did           = fa-artikel.did
        q1-list.recid-fa-artikel = RECID(fa-artikel).
END.
