DEFINE TEMP-TABLE allotment-list LIKE kontline
    FIELD kurzbez  AS CHAR
    FIELD userinit AS CHAR
.

DEFINE TEMP-TABLE check-resline-list
    FIELD resnr         LIKE res-line.resnr
    FIELD name          LIKE res-line.name
    FIELD abreise       LIKE res-line.abreise
    FIELD ankunft       LIKE res-line.ankunft.

DEFINE TEMP-TABLE allot-list 
  FIELD datum AS DATE 
  FIELD anz AS INTEGER. 

DEFINE TEMP-TABLE s-list 
  FIELD datum AS DATE LABEL "Date" 
  FIELD tag   AS CHAR FORMAT "x(3)"     LABEL "Day" 
  FIELD qty   AS INTEGER FORMAT "->>>9" LABEL "RmQty" 
  FIELD occ   AS INTEGER FORMAT "->>>9" LABEL "Occu" 
  FIELD vac   AS INTEGER FORMAT "->>>9" LABEL "avail" 
  FIELD ovb   AS INTEGER FORMAT "->>>9" LABEL "Overb". 


DEFINE INPUT PARAMETER case-type  AS INTEGER.
DEFINE INPUT PARAMETER gastnr     AS INTEGER.
DEFINE INPUT PARAMETER kon-gastnr AS INTEGER.
DEFINE INPUT PARAMETER kontcode   AS CHAR.
DEFINE INPUT PARAMETER ankunft    AS DATE.
DEFINE INPUT PARAMETER abreise    AS DATE.
DEFINE INPUT PARAMETER zimmeranz  AS INTEGER.

DEFINE OUTPUT PARAMETER TABLE FOR allotment-list.
DEFINE OUTPUT PARAMETER TABLE FOR check-resline-list.
DEFINE OUTPUT PARAMETER TABLE FOR allot-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE d1 AS DATE.
DEFINE VARIABLE d2 AS DATE.
DEFINE VARIABLE datum AS DATE.
DEFINE VARIABLE d AS DATE.


/********** MAIN LOGIC **********/
IF case-type EQ 1 THEN RUN assign-it.
ELSE IF case-type EQ 2 THEN RUN check-resline.
ELSE IF case-type EQ 3 THEN RUN check-allotment.
ELSE IF case-type EQ 4 THEN RUN create-slist.



/********** PROCEDURE **********/
PROCEDURE assign-it:
    FOR EACH kontline WHERE kontline.gastnr = gastnr 
        AND kontline.kontignr GT 0 
        AND kontline.betriebsnr = 0 
        AND kontline.kontstat = 1 NO-LOCK, 
        FIRST bediener WHERE bediener.nr = kontline.bediener-nr NO-LOCK 
        BY kontline.kontcode BY kontline.ankunft:
    
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr 
            NO-LOCK NO-ERROR. 
        CREATE allotment-list.
        BUFFER-COPY kontline TO allotment-list.
        ASSIGN allotment-list.userinit = bediener.userinit.
        IF AVAILABLE zimkateg THEN
          ASSIGN allotment-list.kurzbez  = zimkateg.kurzbez.
    END.
END.

PROCEDURE check-resline:

    FOR EACH res-line WHERE res-line.kontignr NE 0
      AND res-line.gastnr = kon-gastnr AND res-line.active-flag LT 2
      AND res-line.resstatus LT 11 NO-LOCK,
      FIRST kontline WHERE kontline.kontignr = res-line.kontignr
      AND kontline.kontcode = kontcode AND kontline.kontstat = 1 NO-LOCK:

        IF res-line.abreise LE kontline.ankunft 
          OR res-line.ankunft GT kontline.abreise THEN . 
        ELSE 
        DO:
            CREATE check-resline-list.
            ASSIGN
                check-resline-list.resnr         = res-line.resnr
                check-resline-list.name          = res-line.name
                check-resline-list.abreise       = res-line.abreise
                check-resline-list.ankunft       = res-line.ankunft.
        END.
    END.

END.

PROCEDURE check-allotment:
    FOR EACH res-line WHERE res-line.kontignr NE 0 
        AND res-line.gastnr = gastnr 
        AND res-line.active-flag LT 2 AND res-line.resstatus LT 11 
        AND NOT (res-line.ankunft GT abreise) 
        AND NOT (res-line.abreise LT ankunft) NO-LOCK, 
        FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
        AND kontline.kontcode = kontcode AND kontline.kontstat = 1 NO-LOCK:
        
        IF res-line.ankunft GE ankunft THEN d1 = res-line.ankunft. 
        ELSE d1 = ankunft. 
        IF res-line.abreise LE abreise THEN d2 = res-line.abreise - 1. 
        ELSE d2 = abreise. 
        DO datum = d1 TO d2: 
          FIND FIRST allot-list WHERE allot-list.datum = datum NO-ERROR. 
          IF NOT AVAILABLE allot-list THEN 
          DO: 
            create allot-list. 
            allot-list.datum = datum. 
            allot-list.anz = zimmeranz. 
          END. 
          allot-list.anz = allot-list.anz - res-line.zimmeranz. 
        END.
    END.
END.

PROCEDURE create-slist:
  DEFINE VARIABLE weekdays AS CHAR EXTENT 8  FORMAT "x(3)"
      INITIAL ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].
  
  DO d = ankunft TO abreise: 
    create s-list. 
    ASSIGN 
      s-list.datum = d 
      s-list.qty = zimmeranz 
      s-list.vac = zimmeranz. 
      s-list.tag = weekdays[weekday(s-list.datum)]. 
  END. 

  FOR EACH res-line WHERE res-line.kontignr NE 0 
    AND res-line.gastnr = gastnr AND res-line.active-flag LT 2 
    AND res-line.resstatus LT 11 NO-LOCK, 
    FIRST kontline WHERE kontline.kontignr = res-line.kontignr 
    AND kontline.kontcode = kontcode 
    AND kontline.kontstat = 1 NO-LOCK: 
    IF res-line.abreise LE ankunft 
    OR res-line.ankunft GT abreise THEN . 
    ELSE 
    DO d = res-line.ankunft TO (res-line.abreise - 1): 
      FIND FIRST s-list WHERE s-list.datum = d NO-ERROR. 
      IF AVAILABLE s-list THEN 
      DO:
        s-list.vac = s-list.vac - res-line.zimmeranz. 
        s-list.occ = s-list.occ + res-line.zimmeranz. 
      END.
    END.
  END. 
END.
