DEF TEMP-TABLE nation1
    FIELD kurzbez LIKE nation.kurzbez.
DEFINE TEMP-TABLE grprline-list 
  FIELD s-recid AS INTEGER 
  FIELD zinr AS CHAR. 

DEFINE TEMP-TABLE s-list 
  FIELD res-recid   AS INTEGER 
  FIELD resstatus   AS INTEGER 
  FIELD active-flag AS INTEGER
  FIELD flag        AS INTEGER INITIAL 0 /* used for res-line.gastnrmember */
  FIELD karteityp   AS INTEGER 
  FIELD zimmeranz   AS INTEGER
  FIELD erwachs     AS INTEGER FORMAT ">9" LABEL "Adult" 
  FIELD kind1       AS INTEGER LABEL "Ch1" FORMAT ">9"    FIELD kind2       AS INTEGER LABEL "Ch2" FORMAT ">9" 
  FIELD old-zinr    AS CHAR 
  FIELD name        AS CHAR FORMAT "x(36)" LABEL "Name, Firstname, Title" 
  FIELD nat         AS CHAR FORMAT "x(3)" LABEL "Nation" 
  FIELD land        AS CHAR FORMAT "x(3)" LABEL "Cntry" 
  FIELD zinr        LIKE zimmer.zinr LABEL "RmNo " 
  FIELD eta         AS CHAR FORMAT "99:99" LABEL "ETA" INITIAL "0000"
  FIELD etd         AS CHAR FORMAT "99:99" LABEL "ETD" INITIAL "0000"
  FIELD flight1     AS CHAR
  FIELD flight2     AS CHAR
  FIELD rmcat       AS CHAR FORMAT "x(6)" LABEL "RmCat" 
  FIELD ankunft     AS DATE LABEL "Arrival" 
  FIELD abreise     AS DATE LABEL "Departure" 
  FIELD zipreis     AS DECIMAL FORMAT ">,>>>,>>>,>>9.99" LABEL "Room Rate"
  FIELD bemerk      AS CHAR
  FIELD zikatnr     AS INTEGER
. 

DEF TEMP-TABLE zimkateg-list
    FIELD zikatnr LIKE zimkateg.zikatnr
    FIELD kurzbez LIKE zimkateg.kurzbez.

DEF TEMP-TABLE resline-list
    FIELD resnr       LIKE res-line.resnr
    FIELD reslinnr    LIKE res-line.reslinnr
    FIELD setup       LIKE res-line.setup
    FIELD zikatnr     LIKE res-line.zikatnr
    FIELD active-flag LIKE res-line.active-flag
    FIELD resstatus   LIKE res-line.resstatus
    FIELD zimmeranz   LIKE res-line.zimmeranz
    FIELD ankunft     LIKE res-line.ankunft
    FIELD abreise     LIKE res-line.abreise
    FIELD rec-id      AS INT.

DEF TEMP-TABLE zimmer-list
    FIELD zinr LIKE zimmer.zinr.

DEF TEMP-TABLE active-roomlist LIKE zimmer
    FIELD room-selected     AS LOGICAL INITIAL NO
    FIELD res-recid         AS INTEGER
    FIELD arrival-date      AS DATE
    FIELD departure-date    AS DATE
    .   

DEF TEMP-TABLE room-resline
    FIELD zinr      AS CHARACTER
    FIELD zikatnr   AS INTEGER
    FIELD setup     AS INTEGER    
    .

DEF TEMP-TABLE room-ooo LIKE outorder
    FIELD zikatnr   AS INTEGER
    FIELD setup     AS INTEGER    
    .

DEF INPUT  PARAMETER resnr AS INTEGER. 
DEF OUTPUT PARAMETER if-flag AS LOGICAL.
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER default-nat AS CHAR.
DEF OUTPUT PARAMETER htparam-feldtyp AS INT.
DEF OUTPUT PARAMETER htparam-flogical AS LOGICAL.
DEF OUTPUT PARAMETER master-exist AS LOGICAL.
DEF OUTPUT PARAMETER htparam-flogical2 AS LOGICAL.
DEF OUTPUT PARAMETER troom AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR grprline-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR zimkateg-list.
DEF OUTPUT PARAMETER TABLE FOR resline-list.
DEF OUTPUT PARAMETER TABLE FOR zimmer-list.
DEF OUTPUT PARAMETER TABLE FOR nation1.
DEF OUTPUT PARAMETER TABLE FOR active-roomlist.

DEFINE VARIABLE do-it AS LOGICAL.

FIND FIRST master WHERE master.resnr = resnr NO-LOCK NO-ERROR. 
IF AVAILABLE master THEN master-exist = YES. 
FIND FIRST htparam WHERE paramnr = 76 NO-LOCK. 
htparam-flogical2 = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 961 NO-LOCK.
ASSIGN
htparam-feldtyp  = htparam.feldtyp
htparam-flogical = htparam.flogical.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
FIND FIRST htparam WHERE htparam.paramnr = 307 NO-LOCK. 
if-flag = htparam.flogical. 

FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK. 
FIND FIRST guest WHERE guest.gastnr = reservation.gastnr NO-LOCK.
IF guest.karteityp GE 1 AND guest.land NE "" THEN
DO:
  FIND FIRST htparam WHERE htparam.paramnr = 153 NO-LOCK.
  IF htparam.fchar NE "" AND guest.land NE htparam.fchar THEN
    default-nat = guest.land.
END.

RUN create-list.

FOR EACH zimkateg NO-LOCK:
    CREATE zimkateg-list.
    ASSIGN
    zimkateg-list.zikatnr = zimkateg.zikatnr
    zimkateg-list.kurzbez = zimkateg.kurzbez.
END.

FOR EACH zimmer WHERE NOT zimmer.sleeping NO-LOCK:
    CREATE zimmer-list.
    ASSIGN zimmer-list.zinr = zimmer.zinr.
END.

FIND LAST zimmer NO-LOCK.
troom = zimmer.zinr.

FOR EACH nation NO-LOCK:
    CREATE nation1.
    ASSIGN nation1.kurzbez = nation.kurzbez.
END.

PROCEDURE create-list: 
  FOR EACH grprline-list: 
    delete grprline-list. 
  END. 
  FOR EACH res-line WHERE res-line.resnr = resnr 
    AND active-flag LT 2 AND resstatus NE 12 
    AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikat NO-LOCK. 
    FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK. 
    CREATE s-list.
    ASSIGN
      s-list.res-recid   = RECID(res-line)
      s-list.name        = guest.NAME + ", " + guest.vorname1 + ", "
                         + guest.anrede1
      s-list.NAME        = TRIM(s-list.NAME)
      s-list.flag        = res-line.gastnrmember
      s-list.nat         = guest.nation1 
      s-list.land        = guest.land
      s-list.zinr        = res-line.zinr 
      s-list.old-zinr    = res-line.zinr
      s-list.flight1     = SUBSTR(res-line.flight-nr,1,6)
      s-list.eta         = SUBSTR(res-line.flight-nr,7,4)
      s-list.flight2     = SUBSTR(res-line.flight-nr,12,6)
      s-list.etd         = SUBSTR(res-line.flight-nr,18,4)
      s-list.zimmeranz   = res-line.zimmeranz 
      s-list.resstatus   = res-line.resstatus 
      s-list.active-flag = res-line.active-flag
      s-list.karteityp   = guest.karteityp
      s-list.erwachs     = res-line.erwachs 
      s-list.rmcat       = zimkateg.kurzbez
      s-list.ankunft     = res-line.ankunft 
      s-list.abreise     = res-line.abreise 
      s-list.kind1       = res-line.kind1
      s-list.kind2       = res-line.kind2 
      s-list.zipreis     = res-line.zipreis
      s-list.bemerk      = res-line.bemerk
      s-list.zikatnr     = res-line.zikatnr
    . 

    CREATE resline-list.
    ASSIGN
    resline-list.resnr       = res-line.resnr
    resline-list.reslinnr    = res-line.reslinnr
    resline-list.setup       = res-line.setup
    resline-list.zikatnr     = res-line.zikatnr
    resline-list.active-flag = res-line.active-flag
    resline-list.resstatus   = res-line.resstatus
    resline-list.zimmeranz   = res-line.zimmeranz
    resline-list.ankunft     = res-line.ankunft
    resline-list.abreise     = res-line.abreise
    resline-list.rec-id      = RECID(res-line).

    IF s-list.nat = "" THEN s-list.nat = default-nat.

    CREATE grprline-list. 
    grprline-list.s-recid = s-list.res-recid.
    grprline-list.zinr = res-line.zinr.        
  END. 
END. 

/*FDL Nov 28, 2024: Ticket 9824CF*/
/*
FOR EACH zimmer WHERE zimmer.sleeping EQ YES
    AND zimmer.zistatus LE 3 NO-LOCK:

    do-it = YES.    
    FIND FIRST res-line WHERE res-line.zikatnr EQ zimmer.zikatnr
        AND res-line.setup EQ zimmer.setup AND res-line.zinr EQ zimmer.zinr
        AND res-line.zinr NE "" AND res-line.active-flag LE 1
        AND res-line.resstatus NE 8 AND res-line.resstatus NE 9
        AND res-line.resstatus NE 12 AND res-line.resstatus NE 99
        AND res-line.l-zuordnung[3] EQ 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE res-line THEN
    DO:
        FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr 
            AND outorder.betriebsnr NE res-line.resnr 
            AND ((res-line.ankunft GE outorder.gespstart AND res-line.ankunft LE outorder.gespende) 
            OR (res-line.abreise GT outorder.gespstart AND res-line.abreise LE outorder.gespende) 
            OR (outorder.gespstart GE res-line.ankunft AND outorder.gespstart LT res-line.abreise) 
            OR (outorder.gespende GE res-line.ankunft AND outorder.gespende LE res-line.abreise)) NO-LOCK NO-ERROR. 
        IF AVAILABLE outorder THEN do-it = NO.

        IF do-it THEN
        DO:
            CREATE active-roomlist.
            BUFFER-COPY zimmer TO active-roomlist.
        END.        
    END.     
END.
*/

FOR EACH zimmer WHERE zimmer.sleeping EQ YES
    AND zimmer.zistatus LE 3
    AND zimmer.zinr NE "" NO-LOCK,
    FIRST resline-list WHERE resline-list.zikatnr EQ zimmer.zikatnr NO-LOCK:

    FIND FIRST outorder WHERE outorder.zinr EQ zimmer.zinr
        AND NOT outorder.gespstart GT resline-list.abreise
        AND NOT outorder.gespende LT resline-list.ankunft
        AND outorder.betriebsnr LE 2 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE outorder THEN
    DO:
        IF zimmer.zistatus EQ 6 AND resline-list.ankunft LE ci-date THEN.
        ELSE
        DO:
            CREATE active-roomlist.
            BUFFER-COPY zimmer TO active-roomlist.
            active-roomlist.res-recid = INT(resline-list.rec-id).
        END.
    END.
END.
/*
FOR EACH res-line WHERE res-line.zinr NE ""
    AND res-line.resstatus NE 12
    AND res-line.active-flag LE 1
    AND res-line.l-zuordnung[3] EQ 0 NO-LOCK,
    FIRST resline-list WHERE resline-list.zikatnr EQ res-line.zikatnr NO-LOCK: 

    IF resline-list.rec-id EQ INT(RECID(res-line)) THEN.
    ELSE IF res-line.resstatus EQ 6 AND res-line.abreise LE resline-list.ankunft THEN.
    ELSE IF (res-line.abreise LE resline-list.ankunft) OR (res-line.ankunft GE resline-list.abreise) THEN.
    ELSE
    DO:
        FIND FIRST active-roomlist WHERE active-roomlist.zinr EQ res-line.zinr
            AND active-roomlist.zikatnr EQ res-line.zikatnr NO-LOCK NO-ERROR.
        IF AVAILABLE active-roomlist THEN DELETE active-roomlist.
    END.
END.

FOR EACH zimmer WHERE zimmer.sleeping EQ YES
    AND zimmer.zistatus LE 3 NO-LOCK,
    FIRST resline-list WHERE resline-list.zikatnr EQ zimmer.zikatnr NO-LOCK:
    CREATE active-roomlist.
    BUFFER-COPY zimmer TO active-roomlist.
    active-roomlist.res-recid = INT(resline-list.rec-id).
END.
*/
FOR EACH res-line WHERE res-line.zinr NE "" AND res-line.active-flag LE 1
    AND res-line.resstatus NE 8 AND res-line.resstatus NE 9
    AND res-line.resstatus NE 12 AND res-line.resstatus NE 99
    AND res-line.l-zuordnung[3] EQ 0 NO-LOCK:
    CREATE room-resline.
    ASSIGN
        room-resline.zinr       = res-line.zinr   
        room-resline.zikatnr    = res-line.zikatnr
        room-resline.setup      = res-line.setup  
        .
END.

FOR EACH active-roomlist:    
    FIND FIRST room-resline WHERE room-resline.zinr EQ active-roomlist.zinr
        AND room-resline.zikatnr EQ active-roomlist.zikatnr NO-LOCK NO-ERROR.
    IF AVAILABLE room-resline THEN DELETE active-roomlist.
END.
