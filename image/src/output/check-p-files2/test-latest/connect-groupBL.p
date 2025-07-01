DEFINE TEMP-TABLE guest-list
    FIELD gastnr            LIKE guest.gastnr
    FIELD NAME              LIKE guest.NAME
    FIELD anredefirma       LIKE guest.anredefirma
    FIELD wohnort           LIKE guest.wohnort
    FIELD karteityp         LIKE guest.karteityp.

DEFINE TEMP-TABLE res-list LIKE res-line
    FIELD kurzbez           LIKE zimkateg.kurzbez
    FIELD groupname         LIKE reservation.groupname
    FIELD join-flag         AS LOGICAL LABEL "JoinGroup" 
    FIELD mbill-flag        AS LOGICAL LABEL "Assign Mbill" 
    FIELD prev-join         AS LOGICAL
    FIELD prev-mbill        AS LOGICAL.

DEFINE TEMP-TABLE mainres-list
    FIELD gastnr    LIKE guest.gastnr
    FIELD resnr     LIKE reservation.resnr
    FIELD actflag   LIKE reservation.activeflag
    FIELD zimanz    LIKE res-line.zimmeranz
    FIELD ankunft   LIKE res-line.ankunft
    FIELD abreise   LIKE res-line.abreise
    FIELD segm      LIKE reservation.segmentcode
    FIELD deposit   AS DECIMAL FORMAT "->>>,>>>,>>>,>>9.99"
    FIELD until     AS DATE
    FIELD paid      AS DECIMAL
    FIELD id1       AS CHAR    FORMAT "x(3)"
    FIELD id2       AS CHAR    FORMAT "x(3)"
    FIELD id2-date  AS DATE
    FIELD groupname LIKE reservation.groupname
    FIELD grpflag   LIKE reservation.grpflag
    FIELD bemerk    LIKE reservation.bemerk
    FIELD arrival   AS LOGICAL
    FIELD resident  AS LOGICAL
    FIELD arr-today AS LOGICAL.


DEFINE INPUT  PARAMETER case-type      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER resNo          AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER reslinNo       AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER gastno         AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER grpname        AS CHARACTER NO-UNDO.
DEFINE INPUT  PARAMETER gname          AS CHARACTER NO-UNDO.
DEFINE INPUT  PARAMETER sorttype       AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR res-list. 
DEFINE OUTPUT PARAMETER TABLE FOR mainres-list. 
DEFINE OUTPUT PARAMETER TABLE FOR guest-list.


DEFINE VARIABLE ci-date AS DATE         NO-UNDO.
DEFINE VARIABLE co-date AS DATE         NO-UNDO.
DEFINE BUFFER mainbuff FOR reservation.
DEFINE BUFFER gast FOR guest.
DEFINE BUFFER mainres FOR reservation.

/****************** MAIN LOGIC ******************/
FIND FIRST res-line WHERE res-line.resnr = resNo
      AND res-line.reslinnr = reslinNo NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN ASSIGN co-date = res-line.abreise.

IF case-type EQ 1 THEN
DO:
  FOR EACH res-line WHERE res-line.resnr = resNo
      AND res-line.active-flag LE 1
      AND res-line.resstatus NE 12 
      AND res-line.l-zuordnung[3] = 0
      USE-INDEX res-resnr_ix,
      FIRST zimkateg NO-LOCK WHERE zimkateg.zikatnr = res-line.zikatnr
      USE-INDEX zikatnr_ix,
      FIRST mainbuff NO-LOCK WHERE mainbuff.resnr = res-line.resnr
      USE-INDEX resnr_index:
    CREATE res-list.
    BUFFER-COPY res-line TO res-list.
    IF res-list.l-zuordnung[2] = 0 AND res-list.l-zuordnung[5] = 0 THEN
    DO:
      ASSIGN
        res-list.join-flag  = YES
        res-list.mbill-flag = YES
        res-list.prev-join  = NO
        res-list.prev-mbill = res-list.mbill-flag
    .
    END.
    ELSE
    ASSIGN
        res-list.join-flag  = res-list.l-zuordnung[5] NE 0
        res-list.mbill-flag = res-list.l-zuordnung[2] EQ 0
        res-list.prev-join  = res-list.join-flag
        res-list.prev-mbill = res-list.mbill-flag
    .
    
    IF res-line.l-zuordnung[5] NE 0 THEN
    DO:
      FOR EACH mainres WHERE 
          mainres.resnr = res-line.l-zuordnung[5] USE-INDEX resnr_index,
          FIRST guest WHERE guest.gastnr = mainres.gastnr NO-LOCK USE-INDEX gastnr_index:
          FIND FIRST guest-list WHERE guest-list.gastnr = guest.gastnr
              NO-LOCK NO-ERROR.
          IF NOT AVAILABLE guest-list THEN
          DO:
              ASSIGN gastno = guest.gastnr.
              CREATE guest-list.
              ASSIGN guest-list.gastnr      = guest.gastnr
                     guest-list.name        = guest.name
                     guest-list.anredefirma = guest.anredefirma
                     guest-list.wohnort     = guest.wohnort
                     guest-list.karteityp   = guest.karteityp.
          END.

          RUN create-res.
      END.
    END.
  END.
END.
ELSE IF case-type EQ 2 THEN
DO: 
    FOR EACH reservation WHERE reservation.activeflag = 0 
      AND reservation.groupname = grpname 
      NO-LOCK USE-INDEX rnr_ix,
        FIRST gast WHERE gast.gastnr = reservation.gastnr 
        NO-LOCK USE-INDEX gastnr_index BY gast.NAME.
        IF AVAILABLE gast THEN 
        DO:    
          CREATE guest-list.
          ASSIGN guest-list.gastnr    = gast.gastnr
                 guest-list.name        = gast.name
                 guest-list.anredefirma = gast.anredefirma
                 guest-list.wohnort   = gast.wohnort
                 guest-list.karteityp = gast.karteityp.
        END.
    END.
END.
ELSE IF case-type EQ 22 THEN
DO: 
    FOR EACH reservation WHERE reservation.activeflag = 0 
          AND reservation.groupname NE "" NO-LOCK USE-INDEX rnr_ix,
          FIRST gast WHERE gast.gastnr = reservation.gastnr 
            AND gast.NAME GE gname AND gast.gastnr GT 0 
            AND gast.karteityp = sorttype 
            NO-LOCK USE-INDEX typ-wohn-name_ix BY gast.NAME.
        IF AVAILABLE gast THEN 
        DO:    
          CREATE guest-list.
          ASSIGN guest-list.gastnr    = gast.gastnr
                 guest-list.name        = gast.name
                 guest-list.anredefirma = gast.anredefirma
                 guest-list.wohnort   = gast.wohnort
                 guest-list.karteityp = gast.karteityp.
        END.
    END.
END.
ELSE IF case-type EQ 23 THEN
DO: 
    FOR EACH reservation WHERE reservation.activeflag = 0 
        NO-LOCK USE-INDEX rnr_ix ,
          FIRST gast WHERE gast.gastnr = reservation.gastnr 
            AND gast.NAME GE gname AND gast.gastnr GT 0 
            AND gast.karteityp = sorttype 
            NO-LOCK USE-INDEX typ-wohn-name_ix BY reservation.gastnr BY gast.NAME.
        IF AVAILABLE gast THEN 
        DO:    
            FIND FIRST guest-list WHERE guest-list.gastnr = gast.gastnr NO-ERROR.
            IF NOT AVAILABLE guest-list THEN
            DO:
                CREATE guest-list.
                ASSIGN guest-list.gastnr      = gast.gastnr
                       guest-list.name        = gast.name
                       guest-list.anredefirma = gast.anredefirma
                       guest-list.wohnort     = gast.wohnort
                       guest-list.karteityp   = gast.karteityp.
            END.
        END.
    END.
END.
ELSE IF case-type EQ 3 THEN
DO: 
    RUN create-res.
END.

/****************** PROCEDURE ******************/
PROCEDURE create-res:  
  RUN fill-mainres.
END. 


PROCEDURE fill-mainres: 
  DEFINE VARIABLE do-it AS LOGICAL          NO-UNDO.
  DEFINE BUFFER   rline FOR res-line.

  FIND FIRST guest WHERE guest.gastnr = gastno NO-LOCK USE-INDEX gastnr_index.
  FOR EACH reservation WHERE reservation.gastnr = gastno 
    AND reservation.resnr NE resNo AND reservation.activeflag = 0 
    AND reservation.groupname NE "" NO-LOCK USE-INDEX gastnr_index:

      FIND FIRST res-line WHERE res-line.resnr = reservation.resnr
          AND res-line.active-flag = 1 NO-LOCK USE-INDEX res-resnr_ix NO-ERROR.
      do-it = AVAILABLE res-line .

      IF NOT do-it THEN
      DO: 
        FIND FIRST res-line WHERE res-line.resnr = reservation.resnr
            AND res-line.active-flag = 0
            AND (res-line.resstatus LE 2 OR res-line.resstatus = 5)
            AND res-line.ankunft LE co-date 
            NO-LOCK USE-INDEX res-ank_ix NO-ERROR.
        do-it = AVAILABLE res-line.

      END.

      IF do-it THEN
      DO: 
        FIND FIRST mainres-list WHERE mainres-list.resnr = reservation.resnr
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE mainres-list THEN
        DO:
            CREATE mainres-list. 
            ASSIGN
              mainres-list.resnr        = reservation.resnr
              mainres-list.deposit      = reservation.depositgef 
              mainres-list.until        = reservation.limitdate 
              mainres-list.paid         = depositbez + depositbez2 
              mainres-list.segm         = reservation.segmentcode 
              mainres-list.groupname    = reservation.groupname
              mainres-list.bemerk       = reservation.bemerk
              mainres-list.id1          = reservation.useridanlage 
              mainres-list.id2          = reservation.useridmutat 
              mainres-list.id2-date     = reservation.mutdat
              mainres-list.grpflag      = reservation.grpflag
            .
            RUN update-mainres. 
        END.
      END. 
  END.
 
END. 

PROCEDURE update-mainres: 
  mainres-list.ankunft   = 01/01/2099. 
  mainres-list.abreise   = 01/01/1998. 
  mainres-list.zimanz    = 0. 
  mainres-list.arrival   = NO. 
  mainres-list.arr-today = NO. 
  mainres-list.resident  = NO. 
  FOR EACH res-line WHERE res-line.resnr = mainres-list.resnr 
    AND resstatus NE 9 AND resstatus NE 10 AND resstatus NE 12 
      NO-LOCK USE-INDEX relinr_index: 
    IF res-line.resstatus LE 6 THEN
      mainres-list.zimanz   = mainres-list.zimanz + res-line.zimmeranz. 
    IF mainres-list.ankunft > res-line.ankunft THEN 
       mainres-list.ankunft = res-line.ankunft. 
    IF mainres-list.abreise < res-line.abreise THEN 
       mainres-list.abreise = res-line.abreise. 
    IF (resstatus LE 5 OR resstatus = 11) THEN 
       mainres-list.arrival = YES. 
    IF mainres-list.arrival = YES AND res-line.ankunft = ci-date THEN 
       mainres-list.arr-today = YES. 
    IF res-line.resstatus = 6 OR res-line.resstatus = 13 THEN 
       mainres-list.resident = YES. 
  END. 
  FOR EACH mainres-list WHERE mainres-list.zimanz = 0:
      DELETE mainres-list.
  END.
END.
