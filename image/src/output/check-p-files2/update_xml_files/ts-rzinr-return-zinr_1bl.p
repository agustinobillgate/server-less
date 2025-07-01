DEFINE TEMP-TABLE q1-list
    FIELD resnr       LIKE vhp.res-line.resnr
    FIELD zinr        LIKE vhp.res-line.zinr
    FIELD code        LIKE vhp.res-line.code
    FIELD resstatus   LIKE vhp.res-line.resstatus
    FIELD erwachs     LIKE vhp.res-line.erwachs
    FIELD kind1       LIKE vhp.res-line.kind1
    FIELD gratis      LIKE vhp.res-line.gratis
    FIELD bemerk      LIKE vhp.res-line.bemerk
    FIELD billnr      LIKE bill.billnr
    FIELD g-name      LIKE guest.name
    FIELD vorname1    LIKE vhp.guest.vorname1
    FIELD anrede1     LIKE vhp.guest.anrede1
    FIELD anredefirma LIKE vhp.guest.anredefirma
    FIELD bill-name   LIKE bill.NAME
    FIELD ankunft     LIKE vhp.res-line.ankunft
    FIELD abreise     LIKE vhp.res-line.abreise
    FIELD nation1     LIKE vhp.guest.nation1
    FIELD parent-nr   LIKE bill.parent-nr
    FIELD reslinnr    LIKE res-line.reslinnr
    FIELD resname     LIKE res-line.NAME
    FIELD name-bg-col AS INT INIT 15
    FIELD name-fg-col AS INT 
    FIELD bill-bg-col AS INT INIT 15
    FIELD bill-fg-col AS INT 
    .

DEF INPUT  PARAMETER pvILanguage  AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER case-type    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER room         AS CHAR.
DEF INPUT  PARAMETER dept         AS INT.
DEF INPUT  PARAMETER dept-mbar    AS INT.
DEF INPUT  PARAMETER dept-ldry    AS INT.

DEF OUTPUT PARAMETER zinr         AS CHAR.
DEF OUTPUT PARAMETER lastzinr     AS CHAR.
DEF OUTPUT PARAMETER comments     AS CHAR.
DEF OUTPUT PARAMETER resline      AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-rzinr".

DEFINE BUFFER rline FOR vhp.res-line.
DEFINE BUFFER bbuff FOR vhp.bill.

IF case-type = 1 THEN DO:
    FIND FIRST rline WHERE active-flag = 1 
      AND rline.pin-code = room 
      AND rline.resstatus NE 12 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE rline THEN 
    DO: 
      FIND FIRST vhp.queasy WHERE vhp.queasy.key = 16 
        AND vhp.queasy.char1 = room NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.queasy THEN 
      FIND FIRST rline WHERE rline.active-flag = 1 
        AND rline.resnr = vhp.queasy.number1 
        AND rline.reslinnr = vhp.queasy.number2 NO-LOCK NO-ERROR. 
    END.
    
    IF AVAILABLE rline THEN 
    DO:
      resline = YES.
      ASSIGN
        zinr = rline.zinr 
        lastzinr = zinr
        comments = translateExtended ("A/Ch/CO:",lvCAREA,"") + " "
                 + STRING(rline.erwachs) + "/"
                 + STRING(rline.kind1) + "/"
                 + STRING(rline.gratis) + CHR(10)
                 + rline.bemerk.
    
      FOR EACH vhp.res-line WHERE 
          vhp.res-line.zinr EQ zinr AND vhp.res-line.active-flag = 1 
          AND vhp.res-line.resnr = rline.resnr NO-LOCK, 
          FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.res-line.gastnrmember NO-LOCK,
          FIRST bbuff WHERE bbuff.resnr = vhp.res-line.resnr 
          AND bbuff.parent-nr = vhp.rline.reslinnr NO-LOCK BY vhp.res-line.reslinnr:
    
          CREATE q1-list.
          ASSIGN
            q1-list.resnr       = vhp.res-line.resnr
            q1-list.zinr        = vhp.res-line.zinr
            q1-list.code        = vhp.res-line.code
            q1-list.resstatus   = vhp.res-line.resstatus
            q1-list.erwachs     = vhp.res-line.erwachs
            q1-list.kind1       = vhp.res-line.kind1
            q1-list.gratis      = vhp.res-line.gratis
            q1-list.bemerk      = vhp.res-line.bemerk
            q1-list.billnr      = bbuff.billnr
            q1-list.g-name      = guest.name
            q1-list.vorname1    = vhp.guest.vorname1
            q1-list.anrede1     = vhp.guest.anrede1
            q1-list.anredefirma = vhp.guest.anredefirma
            q1-list.bill-name   = bbuff.NAME
            q1-list.ankunft     = vhp.res-line.ankunft
            q1-list.abreise     = vhp.res-line.abreise
            q1-list.nation1     = vhp.guest.nation1
            q1-list.parent-nr   = bbuff.parent-nr
            q1-list.reslinnr    = res-line.reslinnr
            q1-list.resname     = res-line.NAME
            .
          IF (dept NE dept-mbar AND dept NE dept-ldry) THEN
          IF res-line.code NE "" THEN
          DO:
              FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 AND vhp.queasy.number1 = 
                INTEGER(res-line.code) NO-LOCK NO-ERROR. 
              IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN 
                ASSIGN q1-list.name-bg-col = 12
                       q1-list.name-fg-col = 15.
          END.
          IF res-line.resstatus = 12 THEN
          ASSIGN q1-list.bill-bg-col = 2
                 q1-list.bill-fg-col = 15.
    
      END.
      /*MTDISP zinr comments WITH FRAME frame1. 
      OPEN QUERY q1 FOR EACH vhp.res-line WHERE 
        vhp.res-line.zinr EQ zinr AND vhp.res-line.active-flag = 1 
        AND vhp.res-line.resnr = rline.resnr NO-LOCK, 
        FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.res-line.gastnrmember 
        NO-LOCK,
        FIRST bbuff WHERE bbuff.resnr = vhp.res-line.resnr AND bbuff.parent-nr
        = vhp.rline.reslinnr NO-LOCK BY vhp.res-line.reslinnr. 
      PAUSE 0. 
      GET FIRST q1 NO-LOCK.
      DO WHILE AVAILABLE res-line:
        numRec = numRec + 1.
        GET NEXT q1 NO-LOCK.
      END.
      GET FIRST q1 NO-LOCK.
      IF numRec = 1 THEN APPLY "choose" TO btn-exit. 
      ELSE APPLY "entry" TO btn-exit.*/
    END. 
END.
ELSE IF case-type = 2 THEN DO:
    ASSIGN 
        zinr     = room
        lastzinr = zinr.
    FOR EACH vhp.res-line WHERE 
          vhp.res-line.zinr EQ room AND vhp.res-line.active-flag = 1 NO-LOCK, 
          FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.res-line.gastnrmember NO-LOCK,
          FIRST bbuff WHERE bbuff.resnr = vhp.res-line.resnr 
          AND bbuff.parent-nr = vhp.res-line.reslinnr NO-LOCK BY vhp.res-line.reslinnr:
           
          resline = YES.
    
          CREATE q1-list.
          ASSIGN
            q1-list.resnr       = vhp.res-line.resnr
            q1-list.zinr        = vhp.res-line.zinr
            q1-list.code        = vhp.res-line.code
            q1-list.resstatus   = vhp.res-line.resstatus
            q1-list.erwachs     = vhp.res-line.erwachs
            q1-list.kind1       = vhp.res-line.kind1
            q1-list.gratis      = vhp.res-line.gratis
            q1-list.bemerk      = vhp.res-line.bemerk
            q1-list.billnr      = bbuff.billnr
            q1-list.g-name      = guest.name
            q1-list.vorname1    = vhp.guest.vorname1
            q1-list.anrede1     = vhp.guest.anrede1
            q1-list.anredefirma = vhp.guest.anredefirma
            q1-list.bill-name   = bbuff.NAME
            q1-list.ankunft     = vhp.res-line.ankunft
            q1-list.abreise     = vhp.res-line.abreise
            q1-list.nation1     = vhp.guest.nation1
            q1-list.parent-nr   = bbuff.parent-nr
            q1-list.reslinnr    = res-line.reslinnr
            q1-list.resname     = res-line.NAME
            .
          IF (dept NE dept-mbar AND dept NE dept-ldry) THEN
          IF res-line.code NE "" THEN
          DO:
              FIND FIRST vhp.queasy WHERE vhp.queasy.key = 9 AND vhp.queasy.number1 = 
                INTEGER(res-line.code) NO-LOCK NO-ERROR. 
              IF AVAILABLE vhp.queasy AND vhp.queasy.logi1 THEN 
                ASSIGN q1-list.name-bg-col = 12
                       q1-list.name-fg-col = 15.
          END.
          IF res-line.resstatus = 12 THEN
          ASSIGN q1-list.bill-bg-col = 2
                 q1-list.bill-fg-col = 15.

          comments = translateExtended ("A/Ch/CO:",lvCAREA,"") + " "
                 + STRING(res-line.erwachs) + "/"
                 + STRING(res-line.kind1) + "/"
                 + STRING(res-line.gratis) + CHR(10)
                 + res-line.bemerk.
    
      END.
END.
