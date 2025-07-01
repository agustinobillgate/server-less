
/*********Temp Table*****************/
DEFINE TEMP-TABLE b-detail
    FIELD resno         AS DECIMAL FORMAT ">>>,>>9"
    FIELD erwachs       AS INTEGER FORMAT "999"
    FIELD kind1         AS INTEGER FORMAT "99"
    FIELD kind2         AS INTEGER FORMAT "99"
    FIELD gratis        AS INTEGER FORMAT "99"
    FIELD nama          AS CHAR FORMAT "x(24)"
    FIELD rt            AS CHAR FORMAT "x(10)"
    FIELD arg           AS CHAR FORMAT "x(3)"
    FIELD room          AS CHAR FORMAT "x(24)"
    FIELD arr           AS DATE FORMAT "99/99/99" 
    FIELD dep           AS DATE FORMAT "99/99/99".


DEFINE INPUT PARAMETER resNo        AS INTEGER.
DEFINE INPUT PARAMETER reslinNo     AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR   b-detail.

DEFINE VARIABLE nama     AS CHARACTER   INITIAL "" NO-UNDO.
DEFINE VARIABLE room     AS CHARACTER   INITIAL "" NO-UNDO.
DEFINE VARIABLE arr      AS DATE        INITIAL "" NO-UNDO.
DEFINE VARIABLE dep      AS DATE        INITIAL "" NO-UNDO.

/*****************************************************************************/


FOR EACH b-detail:
    DELETE b-detail.
END.

FIND FIRST res-line WHERE res-line.resnr = resNo 
    AND res-line.reslinnr = reslinNo 
    AND res-line.resstatus NE 9 AND res-line.resstatus NE 12 
    NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    /*arr = res-line.ankunf.*/
    arr = res-line.ankunft. /*Alder - Serverless - Issue 523*/
    dep = res-line.abreise.
    
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR .
    IF AVAILABLE guest THEN nama = guest.name + ", " + guest.vorname1 + " " + guest.anrede1.
        
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE zimkateg THEN room = zimkateg.kurzbez.
    
    CREATE b-detail.
    ASSIGN  b-detail.resno = res-line.resnr
            b-detail.nama  = nama
            b-detail.room  = res-line.zinr
            b-detail.rt = room
            b-detail.arr   = arr
            b-detail.dep   = dep
            b-detail.kind1 = res-line.kind1
            b-detail.kind2 = res-line.kind2
            b-detail.erwachs = res-line.erwachs
            b-detail.arg = res-line.arrangement.
END.
