DEFINE TEMP-TABLE b3-list
    FIELD resnr     LIKE res-line.resnr
    FIELD ankunft   LIKE res-line.ankunft
    FIELD abreise   LIKE res-line.abreise
    FIELD name      LIKE guest.name
    FIELD vorname1  LIKE guest.vorname1
    FIELD zimmeranz LIKE res-line.zimmeranz
    FIELD kurzbez   LIKE zimkateg.kurzbez
    FIELD zinr      LIKE res-line.zinr
    FIELD resstatus LIKE res-line.resstatus
    FIELD erwachs   LIKE res-line.erwachs
    FIELD kind1     LIKE res-line.kind1
    FIELD kind2     LIKE res-line.kind2 .

DEF INPUT PARAMETER resnr    AS INT.
DEF INPUT PARAMETER reslinnr AS INT.
DEF INPUT PARAMETER gastnr   AS INT.
DEF OUTPUT PARAMETER TABLE FOR b3-list.

IF resnr NE 0 THEN
DO:
    IF reslinnr = 0 THEN
    DO:
        FOR EACH res-line WHERE res-line.resnr = resnr 
            AND (res-line.active-flag = 1 OR res-line.active-flag = 0) AND 
            res-line.resstatus NE 12 NO-LOCK, 
            FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            USE-INDEX gastnr_index NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY 
            res-line.ankunft:
            RUN assign-it.
        END.
    END.
    ELSE
    DO:
        FOR EACH res-line WHERE res-line.resnr = resnr 
            AND (res-line.active-flag = 1 OR res-line.active-flag = 0) AND 
            res-line.resstatus NE 12 AND res-line.reslinnr = reslinnr NO-LOCK, 
            FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
            USE-INDEX gastnr_index NO-LOCK,
            FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY 
            res-line.ankunft:
            RUN assign-it.
        END.
    END.
END.
ELSE
DO:
    FOR EACH res-line WHERE res-line.gastnr = gastnr 
        AND (res-line.active-flag = 1 OR res-line.active-flag = 0) AND 
        res-line.resstatus NE 12 NO-LOCK, 
        FIRST guest WHERE guest.gastnr = res-line.gastnrmember 
        USE-INDEX gastnr_index NO-LOCK,
        FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK BY 
        res-line.ankunft:
        RUN assign-it.
    END.
END.

PROCEDURE assign-it:
    CREATE b3-list.
    ASSIGN
        b3-list.resnr     = res-line.resnr
        b3-list.ankunft   = res-line.ankunft
        b3-list.abreise   = res-line.abreise
        b3-list.name      = guest.name
        b3-list.vorname1  = guest.vorname1
        b3-list.zimmeranz = res-line.zimmeranz
        b3-list.kurzbez   = zimkateg.kurzbez
        b3-list.zinr      = res-line.zinr
        b3-list.resstatus = res-line.resstatus
        b3-list.erwachs   = res-line.erwachs
        b3-list.kind1     = res-line.kind1
        b3-list.kind2     = res-line.kind2 .
END.
