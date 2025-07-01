
DEFINE TEMP-TABLE hk-histlist
    FIELD gastinfo    LIKE history.gastinfo
    FIELD zinr        LIKE history.zinr
    FIELD zikateg     LIKE history.zikateg
    FIELD ankunft     LIKE history.ankunft
    FIELD abreise     LIKE history.abreise
    FIELD abreisezeit LIKE history.abreisezeit
    FIELD arrangement LIKE history.arrangement
    FIELD zi-wechsel  LIKE history.zi-wechsel.


DEFINE INPUT PARAMETER sorttype     AS INTEGER      NO-UNDO.
DEFINE INPUT PARAMETER zinr         AS CHARACTER    NO-UNDO.
DEFINE INPUT PARAMETER f-date       AS DATE         NO-UNDO.
DEFINE INPUT PARAMETER t-date       AS DATE         NO-UNDO.
DEFINE INPUT PARAMETER from-name    AS CHARACTER    NO-UNDO.
DEFINE INPUT PARAMETER disptype     AS INTEGER      NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR hk-histlist.

IF sorttype = 0 THEN 
DO: 
    IF zinr NE "" THEN
    DO:
        FOR EACH history WHERE 
            history.betriebsnr = 0 AND history.ankunft GE f-date 
            AND history.ankunft LE t-date 
            AND history.zinr = zinr
            AND history.gastnr GT 0 NO-LOCK, 
            FIRST guest WHERE guest.gastnr = history.gastnr 
            AND guest.name GE from-name 
            AND guest.karteityp = disptype BY history.gastinfo:
            CREATE hk-histlist.
            ASSIGN
                hk-histlist.gastinfo    = history.gastinfo
                hk-histlist.zinr        = history.zinr
                hk-histlist.zikateg     = history.zikateg
                hk-histlist.ankunft     = history.ankunft
                hk-histlist.abreise     = history.abreise
                hk-histlist.abreisezeit = history.abreisezeit
                hk-histlist.arrangement = history.arrangement
                hk-histlist.zi-wechsel  = history.zi-wechsel.
        END.
    END.
    ELSE
    DO:
        FOR EACH history WHERE 
            history.betriebsnr = 0 AND history.ankunft GE f-date 
            AND history.ankunft LE t-date 
            /*AND history.zinr = zinr*/ AND history.gastnr GT 0 NO-LOCK, 
            FIRST guest WHERE guest.gastnr = history.gastnr 
            AND guest.name GE from-name 
            AND guest.karteityp = disptype BY history.gastinfo:
            CREATE hk-histlist.
            ASSIGN
                hk-histlist.gastinfo    = history.gastinfo
                hk-histlist.zinr        = history.zinr
                hk-histlist.zikateg     = history.zikateg
                hk-histlist.ankunft     = history.ankunft
                hk-histlist.abreise     = history.abreise
                hk-histlist.abreisezeit = history.abreisezeit
                hk-histlist.arrangement = history.arrangement
                hk-histlist.zi-wechsel  = history.zi-wechsel.
        END.
    END.
END.

ELSE IF sorttype = 1 THEN 
DO: 
    IF zinr = "" THEN
    DO:
        FOR EACH history WHERE 
            history.betriebsnr = 0 AND history.abreise GE f-date 
            AND history.abreise LE t-date 
            AND history.gastnr GT 0 NO-LOCK, 
            FIRST guest WHERE guest.gastnr = history.gastnr 
            AND guest.name GE from-name 
            AND guest.karteityp = disptype BY history.gastinfo:
            CREATE hk-histlist.
            ASSIGN
                hk-histlist.gastinfo    = history.gastinfo
                hk-histlist.zinr        = history.zinr
                hk-histlist.zikateg     = history.zikateg
                hk-histlist.ankunft     = history.ankunft
                hk-histlist.abreise     = history.abreise
                hk-histlist.abreisezeit = history.abreisezeit
                hk-histlist.arrangement = history.arrangement
                hk-histlist.zi-wechsel  = history.zi-wechsel.
        END.
    END.
    ELSE
    DO:
        FOR EACH history WHERE 
            history.betriebsnr = 0 AND history.abreise GE f-date 
            AND history.abreise LE t-date 
            AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
            FIRST guest WHERE guest.gastnr = history.gastnr 
            AND guest.name GE from-name 
            AND guest.karteityp = disptype BY history.gastinfo:
            CREATE hk-histlist.
            ASSIGN
                hk-histlist.gastinfo    = history.gastinfo
                hk-histlist.zinr        = history.zinr
                hk-histlist.zikateg     = history.zikateg
                hk-histlist.ankunft     = history.ankunft
                hk-histlist.abreise     = history.abreise
                hk-histlist.abreisezeit = history.abreisezeit
                hk-histlist.arrangement = history.arrangement
                hk-histlist.zi-wechsel  = history.zi-wechsel.
        END.
    END.
END.


