
DEFINE TEMP-TABLE hkdiscrepancy-list
    FIELD zinr          LIKE zimmer.zinr
    FIELD features      LIKE zimmer.features
    FIELD etage         LIKE zimmer.etage
    FIELD bezeich       LIKE zimmer.bezeich
    FIELD house-status  LIKE zimmer.house-status
    FIELD zistatus      LIKE zimmer.zistatus
    FIELD userinit      LIKE bediener.userinit
    FIELD nr            LIKE bediener.nr
    FIELD fo-adult      AS INTEGER
    FIELD fo-child      AS INTEGER
    .

DEFINE TEMP-TABLE rmplan
    FIELD nr    AS INTEGER
    FIELD str   AS CHAR.

    
DEFINE INPUT PARAMETER pvILanguage      AS INTEGER.
DEFINE INPUT PARAMETER case-type        AS CHARACTER.
DEFINE INPUT PARAMETER zinNo            AS CHARACTER.
DEFINE INPUT PARAMETER housestat        AS INTEGER.
DEFINE INPUT PARAMETER feat             AS CHARACTER.
DEFINE INPUT PARAMETER fo-stat1         AS CHARACTER.
DEFINE INPUT PARAMETER hk-stat1         AS CHARACTER.
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER hk-str           AS CHARACTER.
/*
DEFINE INPUT PARAMETER fo-pax           AS INTEGER.
DEFINE INPUT PARAMETER fo-ch1           AS INTEGER.
*/
DEFINE INPUT PARAMETER hk-pax           AS INTEGER.
DEFINE INPUT PARAMETER hk-ch1           AS INTEGER.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER.
DEFINE OUTPUT PARAMETER fo-stat         AS CHARACTER.
DEFINE OUTPUT PARAMETER hk-stat         AS CHARACTER.
DEFINE OUTPUT PARAMETER fo-pax           AS INTEGER.
DEFINE OUTPUT PARAMETER fo-ch1           AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR hkdiscrepancy-list.
DEFINE OUTPUT PARAMETER TABLE FOR rmplan.    
        
DEF BUFFER room FOR zimmer.
DEF BUFFER usr  FOR bediener.

{ Supertransbl.i }.
DEF VAR lvCAREA AS CHAR INITIAL "hk-discrepancy". 
    
/*****************************************************************************/

IF zinNo NE "" THEN
DO:
  FOR EACH res-line WHERE res-line.active-flag EQ 1 AND
    res-line.zinr EQ zinNo AND
    res-line.resstatus EQ 6 OR res-line.resstatus EQ 13:
    fo-pax = fo-pax + res-line.erwachs + res-line.gratis.
    fo-ch1 = fo-ch1 + res-line.kind1.
  END.
END.

IF case-type EQ "deactivate-disc" THEN
DO:
    FIND FIRST zimmer WHERE zimmer.zinr = zinNo EXCLUSIVE-LOCK.
    ASSIGN  zimmer.house-stat   = housestat
            zimmer.features     = feat.
    FIND CURRENT zimmer NO-LOCK.
END.
ELSE IF case-type EQ "cr-rmplan" THEN
DO:
    DEF VAR i AS INTEGER INITIAL 0 NO-UNDO.

    FIND FIRST room WHERE room.house-status GT 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE room:
        FIND FIRST usr WHERE usr.userinit = SUBSTR(room.features, 25, 2) NO-LOCK NO-ERROR.
        i = i + 1.
        IF (i MODULO 2) NE 0 THEN
        DO:
            CREATE rmplan.
            rmplan.nr = i.
            rmplan.str = rmplan.str 
                        + STRING(room.zinr, "x(6)")
                        + STRING(SUBSTR(room.features, 1, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 64, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 66, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 13, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 68, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 70, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 32, 32), "x(32)").
        END.
        ELSE
        DO:
            rmplan.str = rmplan.str 
                        + STRING(room.zinr, "x(6)")
                        + STRING(SUBSTR(room.features, 1, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 64, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 66, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 13, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 68, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 70, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 32, 32), "x(32)").
        END.
        FIND NEXT room WHERE room.house-status GT 0 NO-LOCK NO-ERROR.
    END.
    /*
    FOR EACH room WHERE room.house-status GT 0 NO-LOCK:
        FIND FIRST usr WHERE usr.userinit = SUBSTR(room.features, 25, 2) NO-LOCK NO-ERROR.
        i = i + 1.
        IF (i MODULO 2) NE 0 THEN
        DO:
            CREATE rmplan.
            rmplan.nr = i.
            rmplan.str = rmplan.str 
                        + STRING(room.zinr, "x(6)")
                        + STRING(SUBSTR(room.features, 1, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 64, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 66, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 13, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 68, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 70, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 32, 32), "x(32)").
        END.
        ELSE
        DO:
            rmplan.str = rmplan.str 
                        + STRING(room.zinr, "x(6)")
                        + STRING(SUBSTR(room.features, 1, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 64, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 66, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 13, 12), "x(12)")
                        + STRING(SUBSTR(room.features, 68, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 70, 2), "x(2)")
                        + STRING(SUBSTR(room.features, 32, 32), "x(32)").
        END.
    END.
    */
END.
ELSE IF case-type = "of-zinr" THEN
DO:
    FIND FIRST zimmer WHERE zimmer.zinr = zinNo NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE zimmer THEN 
        msg-str = translateExtended ("Room not found",lvCAREA,""). 
    ELSE IF AVAILABLE zimmer AND zimmer.house-status NE 0 THEN 
        msg-str = translateExtended ("Discrepancy already defined for this room.",lvCAREA,""). 
    ELSE 
    DO: 
        IF zimmer.zistatus LE 2 THEN 
        DO: 
            fo-stat = translateExtended ("Vacant",lvCAREA,""). 
            hk-stat = translateExtended ("Occupied",lvCAREA,""). 
        END. 
        ELSE IF zimmer.zistatus LE 5 OR zimmer.zistatus = 8 THEN 
        DO: 
            fo-stat = translateExtended ("Occupied",lvCAREA,""). 
            hk-stat = "".
        END. 
        ELSE IF zimmer.zistatus EQ 6 THEN 
        DO: 
            fo-stat = translateExtended ("Occupied",lvCAREA,""). 
            hk-stat = translateExtended ("out-of-order",lvCAREA,""). 
        END.                                 
    END. 
END.
ELSE IF case-type = "of-exit" THEN
DO: 
    FIND FIRST zimmer WHERE zimmer.zinr = zinNo SHARE-LOCK NO-ERROR. 
    IF AVAILABLE zimmer THEN
    DO:
        ASSIGN  zimmer.house-status = 1 
                zimmer.features = "                                                                 ". 
                OVERLAY(zimmer.features, 1) = STRING(fo-stat1). 
                OVERLAY(zimmer.features, 13) = STRING(hk-stat1). 
                OVERLAY(zimmer.features, 25) = STRING(user-init). 
                OVERLAY(zimmer.features, 27) = STRING(TIME, "HH:MM"). 
                OVERLAY(zimmer.features, 32) = STRING(hk-str). 
                OVERLAY(zimmer.features, 64) = STRING(fo-pax). 
                OVERLAY(zimmer.features, 66) = STRING(fo-ch1). 
                OVERLAY(zimmer.features, 68) = STRING(hk-pax). 
                OVERLAY(zimmer.features, 70) = STRING(hk-ch1). 
    END.

END.
ELSE IF case-type EQ "" OR case-type EQ ? THEN
DO:
  RUN disp-it.
END.

/*********************** DEFINE PROCEDURES ***********************************/
PROCEDURE disp-it :
    FIND FIRST zimmer WHERE zimmer.house-status NE 0 NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE zimmer:
        FIND FIRST bediener WHERE bediener.userinit = SUBSTR(zimmer.features,25,2) NO-LOCK NO-ERROR.
        CREATE hkdiscrepancy-list.
        ASSIGN  hkdiscrepancy-list.zinr          = zimmer.zinr
                hkdiscrepancy-list.features      = zimmer.features
                hkdiscrepancy-list.etage         = zimmer.etage
                hkdiscrepancy-list.bezeich       = zimmer.bezeich
                hkdiscrepancy-list.house-status  = zimmer.house-status
                hkdiscrepancy-list.zistatus      = zimmer.zistatus
                hkdiscrepancy-list.userinit      = bediener.userinit
                hkdiscrepancy-list.nr            = bediener.nr
                .                 

        FIND NEXT zimmer WHERE zimmer.house-status NE 0 NO-LOCK NO-ERROR.
    END.
    /* 
    FOR EACH zimmer WHERE zimmer.house-status NE 0 NO-LOCK, 
        FIRST bediener WHERE bediener.userinit = SUBSTR(zimmer.features,25,2) 
        NO-LOCK BY zimmer.zinr:
        CREATE hkdiscrepancy-list.
        ASSIGN  hkdiscrepancy-list.zinr          = zimmer.zinr
                hkdiscrepancy-list.features      = zimmer.features
                hkdiscrepancy-list.etage         = zimmer.etage
                hkdiscrepancy-list.bezeich       = zimmer.bezeich
                hkdiscrepancy-list.house-status  = zimmer.house-status
                hkdiscrepancy-list.zistatus      = zimmer.zistatus
                hkdiscrepancy-list.userinit      = bediener.userinit
                hkdiscrepancy-list.nr            = bediener.nr
                .                 
    END.
    */
END.
