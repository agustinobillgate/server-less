DEFINE TEMP-TABLE glores-control-list
    FIELD datum     AS DATE                   LABEL "Date"
    FIELD gastnr    AS INTEGER
    FIELD firma     AS CHAR FORMAT "x(32)"    LABEL "Company Name"
    FIELD kontcode  AS CHAR FORMAT "x(12)"    LABEL "Code"
    FIELD zikatnr   AS INTEGER
    FIELD kurzbez   AS CHAR FORMAT "x(6)"     LABEL "RmType"
    FIELD erwachs   AS INTEGER FORMAT ">9"    LABEL "A"
    FIELD kind1     AS INTEGER FORMAT ">9"    LABEL "Ch"
    FIELD gloAnz    AS INTEGER FORMAT ">>>9"  LABEL "Qty"
    FIELD gresAnz   AS INTEGER FORMAT ">>>>9" LABEL "GRsv"
    FIELD resAnz    AS INTEGER FORMAT ">>>>9" LABEL "Rsv"
    FIELD resnrStr  AS CHAR FORMAT "x(80)"    LABEL "ResNo not from Global Reservation"
    INDEX idx1 datum gastnr kontcode
    INDEX idx2 datum gastnr zikatnr erwachs
    INDEX idx3 datum gastnr zikatnr
.
    
DEFINE INPUT PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER del-flag     AS LOGICAL.
DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETER to-date      AS DATE.
DEFINE INPUT PARAMETER from-name    AS CHARACTER.
DEFINE INPUT PARAMETER to-name      AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR glores-control-list.

DEFINE VARIABLE datum           AS DATE. 
DEFINE VARIABLE usr-init        AS CHAR. 
DEFINE VARIABLE i               AS INTEGER. 
DEFINE VARIABLE count           AS INTEGER. 
DEFINE VARIABLE currResnr       AS INTEGER INITIAL 0.
DEFINE VARIABLE anz1            AS INTEGER EXTENT 31. 
DEFINE VARIABLE anz2            AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz0          AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz1          AS INTEGER EXTENT 31. 
DEFINE VARIABLE t-anz2          AS INTEGER EXTENT 31. 
DEFINE VARIABLE avail-allotm    AS INTEGER EXTENT 31. 
DEFINE VARIABLE overbook        AS INTEGER EXTENT 31. 
DEFINE VARIABLE wday            AS CHAR FORMAT "x(2)" EXTENT 8 
    INITIAL ["SU", "MO", "TU", "WE", "TH", "FR", "SA", "SU"]. 
  
DEFINE WORKFILE k-list 
    FIELD gastnr AS INTEGER 
    FIELD bediener-nr AS INTEGER 
    FIELD kontcode AS CHAR 
    FIELD ankunft AS DATE 
    FIELD zikatnr AS INTEGER 
    FIELD argt AS CHAR 
    FIELD zimmeranz AS INTEGER EXTENT 31 
    FIELD erwachs AS INTEGER 
    FIELD kind1 AS INTEGER 
    FIELD ruecktage AS INTEGER 
    FIELD overbooking AS INTEGER 
    FIELD abreise AS DATE 
    FIELD useridanlage AS CHAR 
    FIELD resdate AS DATE 
    FIELD bemerk AS CHAR. 

DEFINE BUFFER usr FOR bediener. 


{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "pickup-list". 
/*****************************************************************************/
FOR EACH k-list: 
    DELETE k-list. 
END. 

FOR EACH glores-control-list:
    DELETE glores-control-list.
END.

RUN create-alist. 

FOR EACH k-list,  
    FIRST guest WHERE guest.gastnr = k-list.gastnr NO-LOCK 
    BY guest.name BY k-list.ankunft: 

    FOR EACH res-line WHERE res-line.gastnr =  k-list.gastnr 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT from-date) 
        AND res-line.resstatus LE 6 AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.kontignr = 0 NO-LOCK BY res-line.resnr: 
        DO datum = from-date TO to-date:
            IF res-line.ankunft LE datum AND res-line.abreise GT datum THEN
            DO:
                FIND FIRST glores-control-list WHERE glores-control-list.datum = datum
                    AND glores-control-list.gastnr = res-line.gastnr
                    AND glores-control-list.zikatnr = res-line.zikatnr
                    AND glores-control-list.erwachs GE res-line.erwachs 
                    USE-INDEX idx2 NO-ERROR.
                IF NOT AVAILABLE glores-control-list THEN
                    FIND FIRST glores-control-list WHERE glores-control-list.datum = datum
                    AND glores-control-list.gastnr = res-line.gastnr
                    AND glores-control-list.zikatnr = res-line.zikatnr
                    USE-INDEX idx3 NO-ERROR.
                IF AVAILABLE glores-control-list THEN 
                    ASSIGN glores-control-list.resAnz   = glores-control-list.resAnz + res-line.zimmeranz.
                
                IF currResNr NE res-line.resnr THEN 
                DO:    
                    currResNr = res-line.resnr.
                    ASSIGN glores-control-list.resnrStr = glores-control-list.resnrStr 
                        + TRIM(STRING(res-line.resnr,">>>>>>>9")) + "; ".
                END.
            END.
        END.
    END.

    FOR EACH res-line WHERE res-line.gastnr =  k-list.gastnr 
        AND res-line.active-flag LE 1 
        AND NOT (res-line.ankunft GT to-date) 
        AND NOT (res-line.abreise LT from-date) 
        AND res-line.resstatus LE 6 AND res-line.resstatus NE 3 
        AND res-line.resstatus NE 4 
        AND res-line.kontignr LT 0 NO-LOCK, 
        FIRST kontline WHERE kontline.kontignr = - res-line.kontignr 
        AND kontline.kontcode = k-list.kontcode 
        AND kontline.betriebsnr = 1 
        AND kontline.kontstat = 1 NO-LOCK BY res-line.ankunft 
        BY res-line.abreise BY res-line.resnr: 
        FIND FIRST reservation WHERE reservation.resnr = res-line.resnr NO-LOCK. 
        DO datum = from-date TO to-date:
            IF res-line.ankunft LE datum AND res-line.abreise GT datum THEN
            DO:
                FIND FIRST glores-control-list WHERE glores-control-list.datum = datum
                    AND glores-control-list.gastnr = res-line.gastnr
                    AND glores-control-list.kontcode = k-list.kontcode 
                    USE-INDEX idx1 NO-ERROR.
                IF AVAILABLE glores-control-list THEN 
                    ASSIGN glores-control-list.gresAnz = glores-control-list.gresAnz + res-line.zimmeranz.
            END.
        END.
    END.
END.

PROCEDURE create-alist: 
    DEFINE VARIABLE curr-code AS CHAR INITIAL "". 
    DEFINE VARIABLE d AS DATE. 
    DEFINE VARIABLE d1 AS DATE. 
    DEFINE VARIABLE d2 AS DATE. 
    DEFINE VARIABLE i AS INTEGER.

    FOR EACH kontline WHERE kontline.betriebsnr = 1
        AND NOT (kontline.ankunft GT to-date)
        AND NOT (kontline.abreise LT from-date) 
        AND kontline.kontstat = 1 NO-LOCK, 
        FIRST guest WHERE guest.gastnr = kontline.gastnr 
        AND guest.name GE from-name AND guest.name LE to-name NO-LOCK 
        BY guest.name BY kontline.kontcode BY kontline.ankunft: 

        IF curr-code NE kontline.kontcode THEN 
        DO: 
            FIND FIRST usr WHERE usr.nr = kontline.bediener-nr NO-LOCK NO-ERROR. 
            curr-code = kontline.kontcode. 
            CREATE k-list. 
            ASSIGN 
                k-list.gastnr = guest.gastnr 
                k-list.kontcode = curr-code 
                k-list.ankunft = kontline.ankunft 
                k-list.zikatnr = kontline.zikatnr 
                k-list.argt = kontline.arrangement 
                k-list.erwachs = kontline.erwachs 
                k-list.kind1 = kontline.kind1 
                k-list.ruecktage = kontline.ruecktage 
                k-list.overbooking = kontline.overbooking 
                k-list.abreise = kontline.abreise 
                k-list.useridanlage = kontline.useridanlage 
                k-list.resdat = kontline.resdat 
                k-list.bemerk = kontline.bemerk. 
            IF AVAILABLE usr THEN k-list.bediener-nr = usr.nr. 
        END. 
        ELSE k-list.abreise = kontline.abreise. 

        IF from-date GT kontline.ankunft THEN d1 = from-date. 
        ELSE d1 = kontline.ankunft. 
             
        IF to-date LT kontline.abreise THEN d2 = to-date. 
        ELSE d2 = kontline.abreise. 

        i = d1 - from-date. 
        DO d = d1 TO d2: 
            CREATE glores-control-list.
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = k-list.zikatnr 
                NO-LOCK NO-ERROR.
            ASSIGN
                glores-control-list.datum  = d
                glores-control-list.gastnr = kontline.gastnr
                glores-control-list.firma  = guest.NAME
                glores-control-list.kontcode = kontline.kontcode
                glores-control-list.zikatnr  = kontline.zikatnr
                glores-control-list.gloAnz   = kontline.zimmeranz
                glores-control-list.erwachs  = kontline.erwachs
                glores-control-list.kind1    = kontline.kind1
              .

            IF AVAILABLE zimkateg THEN  
                ASSIGN glores-control-list.kurzbez  = zimkateg.kurzbez.
            i = i + 1. 
            IF d GE kontline.ankunft AND d LE kontline.abreise THEN 
                k-list.zimmeranz[i] = kontline.zimmeranz. 
        END. 
    END. 
END. 
