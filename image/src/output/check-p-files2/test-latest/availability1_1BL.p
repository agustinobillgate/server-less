/*FT 130614 -> OCC in %*/
/**********TEMP-TABLE*******/
DEFINE TEMP-TABLE rmcat-list 
  FIELD zikatnr  AS INTEGER FORMAT ">9" COLUMN-LABEL "No " 
  FIELD kurzbez  AS CHAR FORMAT "x(6)" COLUMN-LABEL "RmCat " 
  FIELD kurzbez1 AS CHAR FORMAT "x(6)" COLUMN-LABEL "RmCat  " 
  FIELD bezeich     AS CHAR FORMAT "x(30)" COLUMN-LABEL "Description" 
  FIELD setup       AS CHAR FORMAT "x(20)" COLUMN-LABEL "Bed Setup" 
  FIELD haupt       AS LOGICAL INITIAL NO 
  FIELD anzahl      AS INTEGER 
  FIELD nr          AS INTEGER INITIAL 0 
  FIELD glores      AS LOGICAL INITIAL NO. 

DEFINE TEMP-TABLE room-list 
  FIELD flag        AS CHAR 
  FIELD setup       AS INTEGER INITIAL 0
  FIELD haupt       AS LOGICAL 
  FIELD zikatnr     AS INTEGER 
  FIELD bezeich     AS CHAR FORMAT "x(20)" 
  FIELD room        AS DECIMAL EXTENT 21 FORMAT "->>>9" 
  FIELD coom        AS CHAR EXTENT 21 FORMAT "x(5)" 
  FIELD glores      AS LOGICAL. 

DEFINE TEMP-TABLE sum-list 
  FIELD bezeich     AS CHAR FORMAT "x(15)" 
  FIELD summe       AS CHAR EXTENT 21 FORMAT "x(5)". 

/* START for extra article in general param setting No 2999 */
DEFINE TEMP-TABLE tmp-resline LIKE res-line.
DEFINE TEMP-TABLE tmp-extra 
    FIELD art       AS INTEGER
    FIELD typ-pos   AS CHAR
    FIELD pos-from  AS CHAR
    FIELD cdate     AS DATE
    FIELD room      AS CHAR
    FIELD qty       AS INTEGER.

DEFINE TEMP-TABLE temp-art 
    FIELD art-nr    AS INTEGER
    FIELD art-nm    AS CHAR FORMAT "x(50)".
/* END for extra article in general param setting No 2999 */

/*FD Jan 24, 20222 => Req Prime Plaza*/
DEFINE TEMP-TABLE zikat-list 
    FIELD selected AS LOGICAL INITIAL NO 
    FIELD zikatnr  AS INTEGER 
    FIELD kurzbez  AS CHAR 
    FIELD bezeich  AS CHAR FORMAT "x(32)"
.

DEFINE INPUT  PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER printer-nr       AS INTEGER.
DEFINE INPUT  PARAMETER call-from        AS INTEGER.
DEFINE INPUT  PARAMETER txt-file         AS CHAR.
DEFINE INPUT  PARAMETER curr-date        AS DATE.
DEFINE INPUT  PARAMETER incl-tentative   AS LOGICAL.
DEFINE INPUT  PARAMETER TABLE            FOR zikat-list.    /*FD Jan 24, 20222 => Req Prime Plaza*/
DEFINE OUTPUT PARAMETER msg-str          AS CHAR INITIAL ""  NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE            FOR room-list.
DEFINE OUTPUT PARAMETER TABLE            FOR sum-list.

/****VARIABLE******/
DEFINE VARIABLE LnLDelimeter            AS CHAR.
DEFINE VARIABLE ttl-room                AS INTEGER EXTENT 21 NO-UNDO.
DEFINE VARIABLE occ-room                AS INTEGER EXTENT 21 NO-UNDO.
DEFINE VARIABLE ooo-room                AS INTEGER EXTENT 21 NO-UNDO.

DEFINE VARIABLE anz-setup               AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-room                AS INTEGER.
DEFINE VARIABLE isetup-array            AS INTEGER EXTENT 99.
DEFINE VARIABLE csetup-array            AS CHAR FORMAT "x(1)" EXTENT 99. 
DEFINE VARIABLE ci-date                 AS DATE NO-UNDO.
DEFINE VARIABLE datum                   AS DATE NO-UNDO.
DEFINE VARIABLE week-list               AS CHAR EXTENT 14 FORMAT "x(5)" 
  INITIAL [" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun "]. 
DEFINE VARIABLE i                       AS INTEGER NO-UNDO.
DEFINE VARIABLE j                       AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-day                AS INTEGER. 

DEF BUFFER zkbuff FOR zimkateg.


DEF VAR lvCAREA AS CHAR INITIAL "availability1". 

/***********MAIN Logic***********/

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate .

DO i = 1 TO 21:
  ASSIGN
    ttl-room[i] = 0
    occ-room[i] = 0
    ooo-room[i] = 0
  .
END.

RUN get-bedsetup. 
RUN create-rmcat-list. 
RUN count-rmcateg.
/* Oscar - 789CA8 - create backdate procedure */

IF curr-date LT ci-date THEN RUN backdate-create-browse.
ELSE RUN create-browse.

RUN calc-extra(curr-date).

/*******************PROCEDURE**********/

/* Oscar - 789CA8 - create backdate procedure */
PROCEDURE backdate-create-browse:
  DEFINE VARIABLE datum-browse   AS DATE. /* Malik Serverless : datum -> datum-browse-browse */
  DEFINE VARIABLE fdate          AS DATE. 
  DEFINE VARIABLE tdate          AS DATE. 
  DEFINE VARIABLE do-it          AS LOGICAL. 
  DEFINE VARIABLE m              AS INTEGER. /* Malik Serverless: i -> m */
  DEFINE VARIABLE anz            AS INTEGER. 
  DEFINE VARIABLE s              AS DECIMAL. 
  DEFINE VARIABLE tmp-list       AS INTEGER EXTENT 21.

  DEF BUFFER rlist            FOR room-list. 

  FOR EACH room-list: 
    DELETE room-list. 
  END. 

  FOR EACH sum-list: 
    DELETE sum-list. 
  END. 

  FIND FIRST rmcat-list NO-ERROR.
  IF AVAILABLE rmcat-list THEN DO:
      FOR EACH rmcat-list,
        FIRST zkbuff WHERE zkbuff.zikatnr = rmcat-list.zikatnr
        BY zkbuff.typ BY zkbuff.zikatnr BY rmcat-list.nr: 
    
        CREATE room-list. 
        m = 1. 
        DO WHILE m LE 21: 
          room-list.room[m] = rmcat-list.anzahl. 
          m = m + 1. 
        END. 
    
        ASSIGN 
          room-list.zikatnr = rmcat-list.zikatnr 
          room-list.setup   = rmcat-list.nr 
          room-list.haupt   = rmcat-list.haupt 
          room-list.glores  = rmcat-list.glores. 
    
        IF rmcat-list.anzahl GT 0 THEN /*Dody 25/07/2016*/
              room-list.bezeich = STRING(rmcat-list.kurzbez1, "x(10)") + STRING(rmcat-list.anzahl, ">>>9"). 
        ELSE room-list.bezeich = STRING(rmcat-list.kurzbez1, "x(10)") /* + "GBAL" */. /*gerald 02F59E 05/22 remove gbal*/
      END. 
  END.

  

  datum-browse = curr-date.
  DO m = 1 TO 21:
    IF datum-browse LT ci-date THEN
    DO:
      IF anz-setup GT 0 THEN
      DO:
        FOR EACH genstat WHERE genstat.datum EQ datum-browse
            AND genstat.segmentcode NE 0
            AND genstat.nationnr NE 0
            AND genstat.zinr NE ""
            AND genstat.res-logic[2] EQ YES 
            AND genstat.resstatus NE 13
            NO-LOCK USE-INDEX gastnrmember_ix, 
            FIRST zimkateg WHERE zimkateg.zikatnr EQ genstat.zikatnr NO-LOCK,
            FIRST zimmer WHERE zimmer.zinr EQ genstat.zinr:  

            IF genstat.resstatus EQ 3 AND NOT incl-tentative THEN
              do-it = NO.
            ELSE IF genstat.resstatus EQ 3 AND incl-tentative THEN
              do-it = YES.
            ELSE
              do-it = NO.

            IF do-it THEN 
            DO:
              FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr 
                AND room-list.setup = zimmer.setup. 

              room-list.room[m] = room-list.room[m] - 1. 
              occ-room[m]       = occ-room[m] + 1.

              FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr 
                AND room-list.glores = YES NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE room-list THEN 
                FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr. 

              room-list.room[m] = room-list.room[m] + 1. 
            END.
        END.
      END.
    END.
    ELSE
    DO:
      IF anz-setup GT 0 THEN
      DO:
        FOR EACH res-line WHERE res-line.active-flag LE 1 
          AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
          AND res-line.resstatus NE 4 
          AND ((res-line.ankunft LE datum-browse AND res-line.abreise GT datum-browse)
          OR (res-line.ankunft EQ datum-browse AND res-line.abreise EQ datum-browse))
          AND res-line.kontignr LT 0 
          AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
            
          do-it = YES. 
          IF res-line.zinr NE "" THEN 
          DO: 
            FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
            do-it = zimmer.sleeping. 
          END.

          IF res-line.kontignr LT 0 THEN do-it = NO.
          IF res-line.resstatus = 3 AND NOT incl-tentative THEN
            do-it = NO.
            
          IF do-it THEN 
          DO: 
            FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
              AND room-list.setup = res-line.setup AND NOT room-list.glores 
              NO-ERROR. 
            IF NOT AVAILABLE room-list THEN 
              FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
                AND room-list.haupt = YES AND NOT room-list.glores NO-ERROR. 
            IF NOT AVAILABLE room-list THEN 
              FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
                AND room-list.setup = res-line.setup NO-ERROR. 
            IF NOT AVAILABLE room-list THEN 
              FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
                NO-ERROR. 

            IF NOT AVAILABLE room-list THEN 
            DO: 
              msg-str = ("room-list record missing ResNo:") 
                + " " + STRING(res-line.resnr) 
                +  ("Bed Setup:") + " " + STRING(res-line.setup). 
            END. 
            ELSE 
            DO:
              ASSIGN
                room-list.room[m] = room-list.room[m] - res-line.zimmeranz
                occ-room[m]       = occ-room[m] + res-line.zimmeranz
              .
            END.
          END. 
        END. 
      END.
    END.

    datum-browse = datum-browse + 1.
  END.

  datum-browse = curr-date.
  DO m = 1 TO 21:
    IF datum-browse LT ci-date THEN
    DO:
      FOR EACH zinrstat WHERE zinrstat.datum EQ datum-browse
        AND zinrstat.zinr EQ "ooo" NO-LOCK,
        FIRST zimmer WHERE zimmer.zinr EQ zinrstat.zinr :

        FIND FIRST room-list WHERE room-list.zikatnr EQ zimmer.zikatnr 
          AND room-list.setup EQ zimmer.setup 
          AND room-list.glores EQ NO NO-ERROR. 
        IF NOT AVAILABLE room-list THEN 
          FIND FIRST room-list WHERE room-list.zikatnr EQ zimmer.zikatnr 
          AND room-list.setup EQ zimmer.setup NO-ERROR. 
        IF NOT AVAILABLE room-list THEN 
          FIND FIRST room-list WHERE room-list.zikatnr EQ zimmer.zikatnr NO-ERROR. 
        IF NOT AVAILABLE room-list THEN 
        DO: 
          msg-str = ("room-list record missing for OOO RoomNo:") + " " + zimmer.zinr 
            + ("Bed Setup:") + " " + STRING(zimmer.setup). 
        END. 
        ELSE 
        DO:
          DO m = 1 TO 21:
            ASSIGN 
              room-list.room[m] = room-list.room[m] - 1
              ooo-room[m]       = ooo-room[m] + 1
            .
          END.
        END.
      END.
    END.

    datum-browse = datum-browse + 1. 
  END.

  datum-browse = curr-date.
  DO m = 1 TO 21:
    FOR EACH kontline WHERE kontline.kontignr GT 0 AND kontline.betriebsnr = 1 
      AND kontline.ankunft LE datum-browse AND kontline.abreise GE datum-browse 
      AND kontline.kontstat = 1 NO-LOCK: 

      IF anz-setup GT 0 THEN FIND FIRST room-list WHERE room-list.zikatnr = kontline.zikatnr 
        AND room-list.glores = YES. 
      ELSE FIND FIRST room-list WHERE room-list.zikatnr = kontline.zikatnr. 

      room-list.room[m] = room-list.room[m] - kontline.zimmeranz. 
      occ-room[m]       = occ-room[m] + kontline.zimmeranz.
    END. 

    IF datum-browse LT ci-date THEN
    DO:
      FOR EACH genstat WHERE genstat.datum EQ datum-browse
          AND genstat.segmentcode NE 0
          AND genstat.nationnr NE 0
          AND genstat.zinr NE ""
          AND genstat.res-logic[2] EQ YES 
          AND genstat.resstatus NE 13
          NO-LOCK USE-INDEX gastnrmember_ix, 
          FIRST zimkateg WHERE zimkateg.zikatnr EQ genstat.zikatnr NO-LOCK,
          FIRST zimmer WHERE zimmer.zinr EQ genstat.zinr:  

          IF genstat.resstatus NE 11 AND genstat.resstatus NE 13 THEN
          DO:
            FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr
              AND room-list.setup = zimmer.setup AND NOT room-list.glores 
              NO-ERROR. 
            IF NOT AVAILABLE room-list THEN 
              FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr
                AND room-list.haupt = YES AND NOT room-list.glores NO-ERROR. 
            IF NOT AVAILABLE room-list THEN 
              FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr 
                AND room-list.setup = zimmer.setup NO-ERROR. 
            IF NOT AVAILABLE room-list THEN 
              FIND FIRST room-list WHERE room-list.zikatnr = genstat.zikatnr 
                NO-ERROR. 

            IF NOT AVAILABLE room-list THEN 
            DO: 
              msg-str = ("room-list record missing ResNo:") 
                + " " + STRING(genstat.resnr) 
                +  ("Bed Setup:") + " " + STRING(zimmer.setup). 
            END. 
            ELSE 
            DO:
              ASSIGN
                room-list.room[m] = room-list.room[m] - 1
                occ-room[m]       = occ-room[m] + 1
              .  
            END.
          END.
      END.
    END.
    ELSE
    DO:
      FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
        AND res-line.resstatus NE 4 
        AND ((res-line.ankunft LE datum-browse AND res-line.abreise GT datum-browse)
        OR (res-line.ankunft EQ datum-browse AND res-line.abreise EQ datum-browse))
        AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
          
        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
          do-it = zimmer.sleeping. 
        END.

        IF res-line.kontignr LT 0 THEN do-it = NO.
        IF res-line.resstatus = 3 AND NOT incl-tentative THEN
          do-it = NO.
          
        IF do-it THEN 
        DO: 
          FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
            AND room-list.setup = res-line.setup AND NOT room-list.glores 
            NO-ERROR. 
          IF NOT AVAILABLE room-list THEN 
            FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
              AND room-list.haupt = YES AND NOT room-list.glores NO-ERROR. 
          IF NOT AVAILABLE room-list THEN 
            FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
              AND room-list.setup = res-line.setup NO-ERROR. 
          IF NOT AVAILABLE room-list THEN 
            FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
              NO-ERROR. 

          IF NOT AVAILABLE room-list THEN 
          DO: 
            msg-str = ("room-list record missing ResNo:") 
              + " " + STRING(res-line.resnr) 
              +  ("Bed Setup:") + " " + STRING(res-line.setup). 
          END. 
          ELSE 
          DO:
            ASSIGN
              room-list.room[m] = room-list.room[m] - res-line.zimmeranz
              occ-room[m]       = occ-room[m] + res-line.zimmeranz
            .
          END.
        END. 
      END. 
    END.

    datum-browse = datum-browse + 1.
  END.

  datum-browse = curr-date.

  CREATE sum-list.
  sum-list.bezeich =  ("TOTAL ROOM"). 
  DO m = 1 TO 21:
    sum-list.summe[m] = STRING(ttl-room[m], "->>>9"). 
  END.

  CREATE sum-list.
  sum-list.bezeich = ("TOTAL OCC"). 
  DO m = 1 TO 21:
    sum-list.summe[m] = STRING(occ-room[m], "->>>9"). 
  END.

  CREATE sum-list.
  sum-list.bezeich = ("TOTAL OOO"). 
  DO m = 1 TO 21:
    sum-list.summe[m] = STRING(ooo-room[m], "->>>9"). 
  END.

  CREATE sum-list. 
  sum-list.bezeich = ("AVAILABLE"). 
  DO m = 1 TO 21: 
    s = 0. 
    FOR EACH room-list: 
      s = s + room-list.room[m]. 
    END. 
    sum-list.summe[m] = STRING(s, "->>>9"). 
    tmp-list[m] = s.
  END. 

  CREATE sum-list. 
  sum-list.bezeich = ("AVAIL in %"). 
  DO m = 1 TO 21: 
    IF tot-room GT 0 THEN s = INTEGER(tmp-list[m]) / tot-room * 100. 

    IF s LT 0 THEN sum-list.summe[m] = STRING(s, "->>9.9"). 
    ELSE sum-list.summe[m] = STRING(s, ">>9.9"). 
  END. 

  CREATE sum-list. /*FT 130614*/
  sum-list.bezeich = ("OCC in %"). 
  DO m = 1 TO 21:  
    IF ttl-room[m] GT 0 THEN s = occ-room[m] / ttl-room[m] * 100.

    IF s LT 0 THEN sum-list.summe[m] = STRING(s, "->>9.99"). 
    ELSE sum-list.summe[m] = STRING(s, ">>9.99").
  END. 
 
  CREATE sum-list. 
  sum-list.bezeich = ("OVERBOOK"). 
  DO m = 1 TO 21: 
    anz = 0. 
    IF tmp-list[m] LT 0 THEN anz = tmp-list[m]. 
    IF anz LT 0 THEN sum-list.summe[m] = STRING(- anz, "->>>9"). 
    ELSE sum-list.summe[m] = STRING(0, "->>>9"). 
  END. 

  FOR EACH room-list: 
    DO m = 1 TO 21: 
      room-list.coom[m] = STRING(room-list.room[m], " ->>9"). 
    END. 
  END.
END.

PROCEDURE create-tmpExtra:
  DEFINE INPUT PARAMETER art-nr   AS INTEGER.
  DEFINE INPUT PARAMETER typ-pos  AS CHAR.
  DEFINE INPUT PARAMETER pos-from AS CHAR.
  DEFINE INPUT PARAMETER cdate    AS DATE.
  DEFINE INPUT PARAMETER room     AS  CHAR.
  DEFINE INPUT PARAMETER qty      AS INTEGER.

  CREATE tmp-extra. 
  ASSIGN tmp-extra.art        = art-nr
        tmp-extra.typ-pos    = typ-pos
        tmp-extra.pos-from   = pos-from
        tmp-extra.cdate      = cdate
        tmp-extra.room       = room
        tmp-extra.qty        = qty.
END.

/*MT
PROCEDURE calc-extra:
DEFINE INPUT PARAMETER fdate AS DATE.

DEF VAR tdate       AS DATE.
DEF VAR art-nr      AS INTEGER.
DEF VAR int-art     AS CHAR.
DEF VAR bdate       AS DATE.
DEF VAR edate       AS DATE.
DEF VAR eposdate    AS DATE.
DEF VAR ndate       AS DATE.
DEF VAR art-qty     AS INTEGER.
DEF VAR art-rem     AS INTEGER.
DEF VAR tot-used    AS INTEGER.

    tdate = fdate + 21.

    FOR EACH tmp-resline :
        DELETE tmp-resline.
    END.
    FOR EACH tmp-extra :
        DELETE tmp-extra.
    END.
    FOR EACH temp-art :
        DELETE temp-art.
    END.

    FOR EACH res-line WHERE res-line.ankunft >= fdate AND res-line.ankunft <= tdate OR 
        res-line.abreise > fdate + 1 AND res-line.abreise < tdate  NO-LOCK BY res-line.resnr :
        FIND FIRST tmp-resline WHERE tmp-resline.resnr = res-line.resnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE tmp-resline THEN
        DO:
            CREATE tmp-resline.
            BUFFER-COPY res-line TO tmp-resline.
        END.
    END.

    FIND FIRST htparam WHERE htparam.paramgr = 5 AND htparam.paramnr = 2999 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(htparam.fchar , ";" ) :
            int-art  = ENTRY(i,htparam.fchar,";").

            IF int-art NE "" THEN
            DO:
                FIND FIRST artikel WHERE artikel.artnr = int(int-art) AND artikel.departement = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    CREATE temp-art.
                    ASSIGN temp-art.art-nr = int(int-art)
                           temp-art.art-nm = artikel.bezeich.

                    art-nr = int(int-art).
    
                    FOR EACH tmp-resline BY tmp-resline.resnr :
                        FOR EACH fixleist WHERE fixleist.resnr = tmp-resline.resnr AND fixleist.artnr = art-nr 
                            AND fixleist.departement = 0 NO-LOCK :
    
                            IF tmp-resline.ankunft = tmp-resline.abreise THEN
                            DO:
                                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 6 THEN
                                    RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).   
                                ELSE IF fixleist.sequenz = 4 THEN
                                    IF DAY(tmp-resline.ankunft) = 1 THEN 
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                                ELSE IF fixleist.sequenz = 5 THEN
                                    IF DAY(tmp-resline.ankunft + 1) = 1 THEN 
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                            END.
                            ELSE
                            DO:
                                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 4 OR fixleist.sequenz = 5 THEN
                                DO:
                                    IF tmp-resline.ankunft < fdate THEN
                                        bdate = fdate.
                                    ELSE
                                        bdate = tmp-resline.ankunft.
                                    IF tmp-resline.abreise > tdate THEN /* IF tmp-resline.abreise > tdate THEN */
                                        edate = tdate + 1.
                                    ELSE IF tmp-resline.abreise <= tdate THEN
                                        edate = tmp-resline.abreise.
                                END.

                                IF fixleist.sequenz = 1 THEN
                                DO:
                                    DO WHILE bdate LT edate :
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                                        bdate = bdate + 1.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 2 THEN
                                DO:
                                    RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).
                                END.
                                ELSE IF fixleist.sequenz = 4 THEN
                                DO:
                                    DO WHILE bdate LT edate :
                                        IF DAY(bdate) = 1 THEN 
                                             RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                                        bdate = bdate + 1.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 5 THEN
                                DO:
                                    DO WHILE bdate LT edate :
                                        IF DAY(bdate + 1) = 1 THEN 
                                            RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number). 
                                        bdate = bdate + 1.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 6 THEN
                                DO:
                                    eposdate = (fixleist.lfakt + fixleist.dekade).

                                    IF fixleist.lfakt < fdate THEN
                                        bdate = fdate.
                                    ELSE
                                        bdate = fixleist.lfakt.

                                    IF eposdate > tdate THEN
                                        edate = tdate + 1.
                                    ELSE IF eposdate <= tdate THEN
                                    DO:
                                        IF eposdate > tmp-resline.abreise THEN
                                            edate = tmp-resline.abreise .
                                        ELSE IF eposdate <= tmp-resline.abreise  THEN
                                            edate = eposdate.
                                    END.  

                                    DO WHILE bdate LT edate :
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).
                                        bdate = bdate + 1.
                                    END.

                                END.
                            END.
                        END.

                        FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" AND reslin-queasy.resnr = tmp-resline.resnr 
                            AND reslin-queasy.number1 = 0 AND reslin-queasy.number3 = art-nr NO-LOCK :

                            IF reslin-queasy.date1 < fdate THEN
                                bdate = fdate.
                            ELSE
                                bdate = reslin-queasy.date1.
    
                            IF reslin-queasy.date2 > tdate THEN
                                edate = tdate + 1.
                            ELSE IF reslin-queasy.date2 <= tdate THEN
                                edate = reslin-queasy.date2.
    
                            DO WHILE bdate LT edate :
                                RUN create-tmpExtra (art-nr, "argt line", "0", bdate, tmp-resline.zinr, 1).        
                                bdate = bdate + 1.
                            END.
                        END.
                    END.
                END.
            END.
        END.
    END.

    ndate =fdate.
    create sum-list. 
    ASSIGN sum-list.bezeich = "" . 

    tot-used = 0.
    
    FOR EACH temp-art :
        FIND FIRST artikel WHERE artikel.artnr = temp-art.art-nr AND artikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
        DO:
            art-qty = artikel.anzahl.
            create sum-list. 
            sum-list.bezeich = temp-art.art-nm. 
            DO i = 1 TO 21: 
                FOR EACH tmp-extra WHERE tmp-extra.art = temp-art.art-nr AND tmp-extra.cdate = ndate AND tmp-extra.qty NE 0 :
                    tot-used = tot-used + tmp-extra.qty.
                END.
                art-rem = art-qty - tot-used.
                sum-list.summe[i] =  STRING(art-rem, "->>>9"). 
                ndate = fdate + i.
                tot-used = 0.
            END. 
        END.
    END.
END.*/

PROCEDURE calc-extra:
    DEFINE INPUT PARAMETER tmp-fdate AS DATE.

    DEF VAR tdate       AS DATE.
    DEF VAR art-nr      AS INTEGER.
    DEF VAR int-art     AS CHAR.
    DEF VAR bdate       AS DATE.
    DEF VAR edate       AS DATE.
    DEF VAR eposdate    AS DATE.
    DEF VAR ndate       AS DATE.
    DEF VAR art-qty     AS INTEGER.
    DEF VAR art-rem     AS INTEGER.
    DEF VAR tot-used    AS INTEGER.
    DEF VAR argtnr      AS INTEGER.

    /*tdate = fdate + 21.*/
    tdate = tmp-fdate + 20.

    FOR EACH tmp-resline :
        DELETE tmp-resline.
    END.
    FOR EACH tmp-extra :
        DELETE tmp-extra.
    END.
    FOR EACH temp-art :
        DELETE temp-art.
    END.

    FOR EACH res-line WHERE NOT (res-line.abreise LT tmp-fdate) AND NOT (res-line.ankunft GT tdate) 
        AND res-line.resstatus NE 9 AND res-line.resstatus NE 10 
        AND res-line.resstatus NE 99
        AND res-line.l-zuordnung[3] = 0 NO-LOCK BY res-line.resnr :
        CREATE tmp-resline.
        BUFFER-COPY res-line TO tmp-resline.
    END.  
    
    /*MESSAGE fdate tdate VIEW-AS ALERT-BOX INFO.
    FOR EACH tmp-resline BY tmp-resline.zinr :
      DISP tmp-resline.resnr tmp-resline.ankunft tmp-resline.abreise tmp-resline.resstatus 
           tmp-resline.zinr.
    END.*/


    FIND FIRST htparam WHERE htparam.paramgr = 5 AND htparam.paramnr = 2999 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        DO i = 1 TO NUM-ENTRIES(htparam.fchar , ";" ) :
            int-art  = ENTRY(i,htparam.fchar,";").

            IF int-art NE "" THEN
            DO:
                FIND FIRST artikel WHERE artikel.artnr = int(int-art) AND artikel.departement = 0 NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN
                DO:
                    CREATE temp-art.
                    ASSIGN temp-art.art-nr = int(int-art)
                           temp-art.art-nm = artikel.bezeich.

                    art-nr = int(int-art).
    
                    FOR EACH tmp-resline BY tmp-resline.resnr :
                        FOR EACH fixleist WHERE fixleist.resnr = tmp-resline.resnr 
                            AND fixleist.reslinnr = tmp-resline.reslinnr
                            AND fixleist.artnr = art-nr 
                            AND fixleist.departement = 0 NO-LOCK :
                            
                            IF tmp-resline.ankunft = tmp-resline.abreise THEN
                            DO:
                                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 6 THEN
                                    RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).   
                                ELSE IF fixleist.sequenz = 4 THEN
                                    IF DAY(tmp-resline.ankunft) = 1 THEN 
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                                ELSE IF fixleist.sequenz = 5 THEN
                                    IF DAY(tmp-resline.ankunft + 1) = 1 THEN 
                                        RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number). 
                            END.
                            ELSE
                            DO:
                                IF fixleist.sequenz = 1 OR fixleist.sequenz = 2 OR fixleist.sequenz = 4 OR fixleist.sequenz = 5 THEN
                                DO:
                                    IF tmp-resline.ankunft < tmp-fdate THEN
                                        bdate = tmp-fdate.
                                    ELSE
                                        bdate = tmp-resline.ankunft.

                                    IF tmp-resline.abreise > tdate THEN /* IF tmp-resline.abreise > tdate THEN */
                                        edate = tdate + 1.
                                    ELSE IF tmp-resline.abreise <= tdate THEN
                                        edate = tmp-resline.abreise.
                                END.

                                IF fixleist.sequenz = 1 THEN
                                DO:
                                    IF bdate NE ? AND edate NE ? THEN DO:
                                         DO WHILE bdate LT edate :
                                            RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                                            bdate = bdate + 1.
                                        END.
                                    END.
                                   
                                END.
                                ELSE IF fixleist.sequenz = 2 THEN
                                DO:
                                    RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), tmp-resline.ankunft, tmp-resline.zinr, fixleist.number).
                                END.
                                ELSE IF fixleist.sequenz = 4 THEN
                                DO:
                                    IF bdate NE ? AND edate NE ? THEN DO:
                                        DO WHILE bdate LT edate :
                                            IF DAY(bdate) = 1 THEN 
                                                 RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).    
                                            bdate = bdate + 1.
                                        END.
                                    END.                                    
                                END.
                                ELSE IF fixleist.sequenz = 5 THEN
                                DO:
                                    IF bdate NE ? AND edate NE ? THEN DO:
                                        DO WHILE bdate LT edate :
                                            IF DAY(bdate + 1) = 1 THEN 
                                                RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number). 
                                            bdate = bdate + 1.
                                        END.
                                    END.
                                END.
                                ELSE IF fixleist.sequenz = 6 THEN
                                DO:
                                    eposdate = (fixleist.lfakt + fixleist.dekade).

                                    IF fixleist.lfakt < tmp-fdate THEN
                                        bdate = tmp-fdate.
                                    ELSE
                                        bdate = fixleist.lfakt.

                                    IF eposdate > tdate THEN
                                        edate = tdate + 1.
                                    ELSE IF eposdate <= tdate THEN
                                    DO:
                                        IF eposdate > tmp-resline.abreise THEN
                                            edate = tmp-resline.abreise .
                                        ELSE IF eposdate <= tmp-resline.abreise  THEN
                                            edate = eposdate.
                                    END.  

                                    IF bdate NE ? AND edate NE ? THEN DO:
                                        DO WHILE bdate LT edate :
                                            RUN create-tmpExtra (art-nr, "Fix-cost line", STRING(fixleist.sequenz), bdate, tmp-resline.zinr, fixleist.number).
                                            bdate = bdate + 1.
                                        END.
                                    END.
                                    
                                END.
                            END.
                        END.

                        FIND FIRST arrangement WHERE arrangement.arrangement = tmp-resline.arrangement NO-LOCK NO-ERROR.
                        IF AVAILABLE arrangement THEN ASSIGN argtnr = arrangement.argtnr.

                        FOR EACH reslin-queasy WHERE reslin-queasy.key = "fargt-line" AND reslin-queasy.resnr = tmp-resline.resnr 
                            AND reslin-queasy.reslinnr = tmp-resline.reslinnr
                            AND reslin-queasy.number1 = 0 AND reslin-queasy.number3 = art-nr
                            AND reslin-queasy.number2 = argtnr NO-LOCK :

                            IF reslin-queasy.date1 < tmp-fdate THEN
                                bdate = tmp-fdate.
                            ELSE
                                bdate = reslin-queasy.date1.
    
                            IF reslin-queasy.date2 > tdate THEN
                                edate = tdate + 1.
                            ELSE IF reslin-queasy.date2 <= tdate THEN
                                edate = reslin-queasy.date2.
        
                            IF bdate NE ? AND tdate NE ? THEN DO:
                                DO WHILE bdate LT edate :
                                    RUN create-tmpExtra (art-nr, "argt line", "0", bdate, tmp-resline.zinr, 1).        
                                    bdate = bdate + 1.
                                END.
                            END.                            
                        END.
                    END.
                END.
            END.
        END.
    END.

    ndate = tmp-fdate.

    CREATE sum-list. 
    ASSIGN sum-list.bezeich = "" . 

    tot-used = 0.
    
    /*
    FOR EACH tmp-extra WHERE tmp-extra.art = 117 BY tmp-extra.cdate:
        DISP tmp-extra.
    END.*/

    FOR EACH temp-art :
        FIND FIRST artikel WHERE artikel.artnr = temp-art.art-nr AND artikel.departement = 0 NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN
        DO:
            art-qty = artikel.anzahl.
            CREATE sum-list. 
            sum-list.bezeich = temp-art.art-nm. 
            ndate = tmp-fdate.
            DO i = 1 TO 21: 
                FOR EACH tmp-extra WHERE tmp-extra.art = temp-art.art-nr AND tmp-extra.cdate = ndate AND tmp-extra.qty NE 0 :
                    tot-used = tot-used + tmp-extra.qty.
                END.
                art-rem = art-qty - tot-used.
                sum-list.summe[i] =  STRING(art-rem, "->>>9"). 
                /*IF temp-art.art-nr = 117  THEN DO:
                    DISP i temp-art.art-nm art-rem art-qty tot-used ndate.
                    PAUSE.
                END.*/
                ndate = tmp-fdate + i.
                tot-used = 0.
            END. 
        END.
    END.
END.


PROCEDURE get-bedsetup: 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK BY paramtext.txtnr: 
    IF paramtext.notes NE "" THEN 
    DO: 
      FIND FIRST zimmer WHERE zimmer.setup = (paramtext.txtnr - 9200)
          NO-LOCK NO-ERROR.
      IF AVAILABLE zimmer THEN
      DO:
        anz-setup = anz-setup + 1. 
        csetup-array[anz-setup] = SUBSTR(paramtext.notes,1,1). /* Malik Serverless : notes -> paramtext.notes */
        isetup-array[anz-setup] = paramtext.txtnr - 9200. 
      END.
    END.
  END. 
END. 


PROCEDURE count-rmcateg: 
  DEFINE VARIABLE zikatnr AS INTEGER INITIAL 0. 
  tot-room = 0. 
  /*
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK,
    FIRST zikat-list WHERE zikat-list.zikatnr EQ zimmer.zikatnr
    AND zikat-list.SELECTED EQ YES NO-LOCK,     /*FD Jan 24, 20222 => Req Prime Plaza*/
    FIRST zkbuff WHERE zkbuff.zikatnr = zikat-list.zikatnr
    BY zkbuff.typ BY zkbuff.zikatnr: 

    FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimmer.zikatnr 
      AND rmcat-list.nr = zimmer.setup NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE rmcat-list THEN 
    DO: 
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
      CREATE rmcat-list. 
      rmcat-list.nr       = zimmer.setup. 
      rmcat-list.zikatnr  = zimkateg.zikatnr. 
      rmcat-list.kurzbez  = zimkateg.kurzbez. 
      rmcat-list.kurzbez1 = zimkateg.kurzbez. 
      rmcat-list.bezeich  = zimkateg.bezeich. 
    END. 

    tot-room = tot-room + 1. 
    rmcat-list.anzahl = rmcat-list.anzahl + 1. 
  END. */

  /*ITA 04/06/25 - update for serverless*/
  FOR EACH zimmer WHERE zimmer.sleeping = YES NO-LOCK:
      FIND FIRST zikat-list WHERE zikat-list.zikatnr EQ zimmer.zikatnr
            AND zikat-list.SELECTED EQ YES NO-LOCK NO-ERROR.
      IF AVAILABLE zikat-list THEN DO:
          FIND FIRST zkbuff WHERE zkbuff.zikatnr = zikat-list.zikatnr NO-LOCK NO-ERROR.
          IF AVAILABLE zkbuff THEN DO:

              FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimmer.zikatnr 
                  AND rmcat-list.nr = zimmer.setup NO-ERROR. 
              IF NOT AVAILABLE rmcat-list THEN 
              DO: 
                  FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
                  IF AVAILABLE zimkateg THEN DO:
                      CREATE rmcat-list. 
                      rmcat-list.nr       = zimmer.setup. 
                      rmcat-list.zikatnr  = zimkateg.zikatnr. 
                      rmcat-list.kurzbez  = zimkateg.kurzbez. 
                      rmcat-list.kurzbez1 = zimkateg.kurzbez. 
                      rmcat-list.bezeich  = zimkateg.bezeich. 

                  END.
              END. 
              ASSIGN
                  tot-room          = tot-room + 1
                  rmcat-list.anzahl = rmcat-list.anzahl + 1. 
          END.
      END.
  END.

  DO i = 1 TO 21:
    ASSIGN ttl-room[i] = tot-room.
  END.
END. 
 
PROCEDURE create-browse: 
  DEFINE VARIABLE datum-browse       AS DATE. /* Malik Serverless : datum -> datum-browse-browse */
  DEFINE VARIABLE fdate       AS DATE. 
  DEFINE VARIABLE tdate       AS DATE. 
  DEFINE VARIABLE do-it       AS LOGICAL. 
  DEFINE VARIABLE m           AS INTEGER. /* Malik Serverless: i -> m */
  DEFINE VARIABLE anz         AS INTEGER. 
  DEFINE VARIABLE s           AS DECIMAL. 
  DEFINE VARIABLE tmp-list    AS INTEGER EXTENT 21.

  DEF BUFFER rlist            FOR room-list. 

  FOR EACH room-list: 
    DELETE room-list. 
  END. 
  FOR EACH sum-list: 
    DELETE sum-list. 
  END. 
 
  fdate = curr-date. 
  tdate = curr-date + 20. 

  FIND FIRST rmcat-list NO-ERROR.
  IF AVAILABLE rmcat-list THEN DO:
      /*FOR EACH rmcat-list,
          FIRST zkbuff WHERE zkbuff.zikatnr = rmcat-list.zikatnr
          BY zkbuff.typ BY zkbuff.zikatnr BY rmcat-list.nr: 
        create room-list. 
        m = 1. 
        DO WHILE m LE 21: 
          room-list.room[m] = rmcat-list.anzahl. 
          m = m + 1. 
        END. 
        ASSIGN 
          room-list.zikatnr = rmcat-list.zikatnr 
          room-list.setup   = rmcat-list.nr 
          room-list.haupt   = rmcat-list.haupt 
          room-list.glores  = rmcat-list.glores. 
     
        IF rmcat-list.anzahl GT 0 THEN /*Dody 25/07/2016*/
             room-list.bezeich = STRING(rmcat-list.kurzbez1, "x(10)") + STRING(rmcat-list.anzahl, ">>>9"). 
        ELSE room-list.bezeich = STRING(rmcat-list.kurzbez1, "x(10)") /* + "GBAL" */. /*gerald 02F59E 05/22 remove gbal*/
      END.*/

      FOR EACH rmcat-list NO-LOCK:
          FIND FIRST zkbuff WHERE zkbuff.zikatnr = rmcat-list.zikatnr NO-LOCK NO-ERROR.
          IF AVAILABLE zkbuff THEN DO:
                CREATE room-list. 
                m = 1. 
                DO WHILE m LE 21: 
                  room-list.room[m] = rmcat-list.anzahl. 
                  m = m + 1. 
                END. 
                ASSIGN 
                  room-list.zikatnr = rmcat-list.zikatnr 
                  room-list.setup   = rmcat-list.nr 
                  room-list.haupt   = rmcat-list.haupt 
                  room-list.glores  = rmcat-list.glores. 
             
                IF rmcat-list.anzahl GT 0 THEN /*Dody 25/07/2016*/
                     room-list.bezeich = STRING(rmcat-list.kurzbez1, "x(10)") + STRING(rmcat-list.anzahl, ">>>9"). 
                ELSE room-list.bezeich = STRING(rmcat-list.kurzbez1, "x(10)") /* + "GBAL" */. /*gerald 02F59E 05/22 remove gbal*/
          END.
      END.
  END.
  

  datum-browse = curr-date.
  m = 1.
  DO WHILE m LE 21: 
    FOR EACH kontline WHERE kontline.kontignr GT 0 AND kontline.betriebsnr = 1 
      AND kontline.ankunft LE datum-browse AND kontline.abreise GE datum-browse 
      AND kontline.kontstat = 1 NO-LOCK: 

      IF anz-setup GT 0 THEN FIND FIRST room-list WHERE room-list.zikatnr = kontline.zikatnr 
        AND room-list.glores = YES. 
      ELSE FIND FIRST room-list WHERE room-list.zikatnr = kontline.zikatnr. 

      room-list.room[m] = room-list.room[m] - kontline.zimmeranz. 
      occ-room[m]       = occ-room[m] + kontline.zimmeranz.
    END. 
 
    IF anz-setup GT 0 THEN
    DO:
      FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
        AND res-line.resstatus NE 4 
        AND ((res-line.ankunft LE datum-browse AND res-line.abreise GT datum-browse)
        OR (res-line.ankunft EQ datum-browse AND res-line.abreise EQ datum-browse))
        AND res-line.kontignr LT 0 
        AND res-line.l-zuordnung[3] = 0 NO-LOCK:         

        do-it = YES. 
        IF res-line.zinr NE "" THEN 
        DO: 
          FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
          do-it = zimmer.sleeping. 
        END. 

        IF res-line.resstatus = 3 AND NOT incl-tentative THEN
            do-it = NO.

        IF do-it THEN 
        DO:           
          FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
            AND room-list.setup = res-line.setup. 

          room-list.room[m] = room-list.room[m] - res-line.zimmeranz. 
          occ-room[m]       = occ-room[m] + res-line.zimmeranz.

          FIND FIRST rlist WHERE rlist.zikatnr = res-line.zikatnr 
            AND rlist.glores = YES NO-ERROR. 
          IF NOT AVAILABLE rlist THEN 
            FIND FIRST rlist WHERE rlist.zikatnr = res-line.zikatnr. 

          rlist.room[m] = rlist.room[m] + res-line.zimmeranz. 
        END. 
      END. 
    END.

    m = m + 1. 
    datum-browse = datum-browse + 1. 
  END. 
 
  FOR EACH outorder WHERE outorder.betriebsnr LE 1 NO-LOCK, 
    FIRST zimmer WHERE zimmer.zinr = outorder.zinr 
    AND zimmer.sleeping NO-LOCK:

    FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK. 
    datum-browse = curr-date.

    FIND FIRST room-list WHERE room-list.zikatnr = zimmer.zikatnr 
      AND room-list.setup = zimmer.setup 
      AND room-list.glores = NO NO-ERROR. 
    IF NOT AVAILABLE room-list THEN 
      FIND FIRST room-list WHERE room-list.zikatnr = zimmer.zikatnr AND room-list.setup = zimmer.setup NO-ERROR. 

    IF NOT AVAILABLE room-list THEN 
      FIND FIRST room-list WHERE room-list.zikatnr = zimmer.zikatnr NO-ERROR. 

    IF NOT AVAILABLE room-list THEN 
    DO: 
      msg-str = ("room-list record missing for OOO RoomNo:") + " " + zimmer.zinr 
        + ("Bed Setup:") + " " + STRING(zimmer.setup). 
    END. 
    ELSE 
    DO m = 1 TO 21: 
      IF outorder.gespstart LE datum-browse AND outorder.gespende GE datum-browse THEN 
      ASSIGN 
        room-list.room[m] = room-list.room[m] - 1
        ooo-room[m]       = ooo-room[m] + 1
        .
      datum-browse = datum-browse + 1. 
    END. 
  END. 

  DEFINE BUFFER gmember FOR guest.
  datum-browse = curr-date. 

  DO m = 1 TO 21: 
    FOR EACH res-line WHERE res-line.active-flag LE 1 
      AND res-line.resstatus LE 6 /*AND res-line.resstatus NE 3 */
      AND res-line.resstatus NE 4 
      AND ((res-line.ankunft LE datum-browse AND res-line.abreise GT datum-browse)
      OR (res-line.ankunft EQ datum-browse AND res-line.abreise EQ datum-browse))
      AND res-line.l-zuordnung[3] = 0 NO-LOCK: 
        
      do-it = YES. 
      IF res-line.zinr NE "" THEN 
      DO: 
        FIND FIRST zimmer WHERE zimmer.zinr = res-line.zinr NO-LOCK. 
        do-it = zimmer.sleeping. 
      END.

      IF res-line.kontignr LT 0 THEN do-it = NO.
      IF res-line.resstatus = 3 AND NOT incl-tentative THEN
        do-it = NO.
        
      IF do-it THEN 
      DO: 
        FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
          AND room-list.setup = res-line.setup AND NOT room-list.glores 
          NO-ERROR. 
        IF NOT AVAILABLE room-list THEN 
          FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
            AND room-list.haupt = YES AND NOT room-list.glores NO-ERROR. 
        IF NOT AVAILABLE room-list THEN 
          FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
            AND room-list.setup = res-line.setup NO-ERROR. 
        IF NOT AVAILABLE room-list THEN 
          FIND FIRST room-list WHERE room-list.zikatnr = res-line.zikatnr 
            NO-ERROR. 

        IF NOT AVAILABLE room-list THEN 
        DO: 
          msg-str = ("room-list record missing ResNo:") 
            + " " + STRING(res-line.resnr) 
            +  ("Bed Setup:") + " " + STRING(res-line.setup). 
        END. 
        ELSE 
        DO:
          ASSIGN
            room-list.room[m] = room-list.room[m] - res-line.zimmeranz
            occ-room[m]       = occ-room[m] + res-line.zimmeranz
          .
        END.
      END. 
    END. 

    datum-browse = datum-browse + 1. 
    /*do m = 1 ...*/
  END.

  CREATE sum-list.
  sum-list.bezeich =  ("TOTAL ROOM"). 
  DO m = 1 TO 21:
    sum-list.summe[m] = STRING(ttl-room[m], "->>>9"). 
  END.

  CREATE sum-list.
  sum-list.bezeich = ("TOTAL OCC"). 
  DO m = 1 TO 21:
    sum-list.summe[m] = STRING(occ-room[m], "->>>9"). 
  END.

  CREATE sum-list.
  sum-list.bezeich = ("TOTAL OOO"). 
  DO m = 1 TO 21:
    sum-list.summe[m] = STRING(ooo-room[m], "->>>9"). 
  END.

  CREATE sum-list. 
  sum-list.bezeich = ("AVAILABLE"). 
  DO m = 1 TO 21: 
    s = 0. 
    FOR EACH room-list: 
      s = s + room-list.room[m]. 
    END. 
    sum-list.summe[m] = STRING(s, "->>>9"). 
    tmp-list[m] = s.
  END. 

  CREATE sum-list. 
  sum-list.bezeich = ("AVAIL in %"). 
  DO m = 1 TO 21: 
    IF tot-room GT 0 THEN s = INTEGER(tmp-list[m]) / tot-room * 100. 

    IF s LT 0 THEN sum-list.summe[m] = STRING(s, "->>9.9"). 
    ELSE sum-list.summe[m] = STRING(s, ">>9.9"). 
  END. 

  CREATE sum-list. /*FT 130614*/
  sum-list.bezeich = ("OCC in %"). 
  DO m = 1 TO 21:  
    IF ttl-room[m] GT 0 THEN s = occ-room[m] / ttl-room[m] * 100.

    IF s LT 0 THEN sum-list.summe[m] = STRING(s, "->>9.99"). 
    ELSE sum-list.summe[m] = STRING(s, ">>9.99").
  END. 
 
  CREATE sum-list. 
  sum-list.bezeich = ("OVERBOOK"). 
  DO m = 1 TO 21: 
    anz = 0. 
    IF tmp-list[m] LT 0 THEN anz = tmp-list[m]. 
    IF anz LT 0 THEN sum-list.summe[m] = STRING(- anz, "->>>9"). 
    ELSE sum-list.summe[m] = STRING(0, "->>>9"). 
  END. 

  FOR EACH room-list: 
    DO m = 1 TO 21: 
      room-list.coom[m] = STRING(room-list.room[m], " ->>9"). 
    END. 
  END. 
END. 
 
PROCEDURE create-rmcat-list: 
  DEFINE VARIABLE n AS INTEGER. /* Malik serverless: i -> n */
  DEFINE VARIABLE curr-zikat AS INTEGER INITIAL 0. 
  DEFINE VARIABLE haupt AS LOGICAL. 
  DEFINE VARIABLE datum-rmcat AS DATE NO-UNDO. /* Malik Serverless : datum -> datum-rmcat-rmcat */
 
  IF anz-setup GT 0 THEN 
  DO: 
    FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit = YES NO-LOCK,
        FIRST zikat-list WHERE zikat-list.zikatnr EQ zimkateg.zikatnr
        AND zikat-list.SELECTED EQ YES NO-LOCK:     /*FD Jan 24, 20222 => Req Prime Plaza*/ 
      haupt = YES. 
      DO n = 1 TO anz-setup: 
        /*FIND FIRST paramtext WHERE paramtext.txtnr = (n + 9200) NO-LOCK NO-ERROR. */
          FIND FIRST paramtext WHERE paramtext.txtnr = (isetup-array[n] + 9200) NO-LOCK NO-ERROR. 
        FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
          AND zimmer.setup = isetup-array[n] NO-LOCK NO-ERROR. 
        IF AVAILABLE zimmer THEN 
        DO: 
          CREATE rmcat-list. 
          rmcat-list.zikatnr  = zimkateg.zikatnr. 
          rmcat-list.kurzbez  = zimkateg.kurzbez. 
          rmcat-list.kurzbez1 = zimkateg.kurzbez + SUBSTR(paramtext.notes,1,1). 
          rmcat-list.bezeich  = zimkateg.bezeich. 
          rmcat-list.setup    = paramtext.ptexte. 
          /*rmcat-list.nr       = n. */
          rmcat-list.nr       = isetup-array[n]. 
          rmcat-list.haupt    = haupt. 
          IF haupt = YES THEN haupt = NO. 
        END. 
      END. 
    END. 
  END. 
  ELSE 
  DO: 
    FOR EACH zimkateg NO-LOCK, 
        FIRST zikat-list WHERE zikat-list.zikatnr EQ zimkateg.zikatnr
        AND zikat-list.SELECTED EQ YES NO-LOCK:     /*FD Jan 24, 20222 => Req Prime Plaza*/
      CREATE rmcat-list. 
      rmcat-list.zikatnr  = zimkateg.zikatnr. 
      rmcat-list.kurzbez  = zimkateg.kurzbez. 
      rmcat-list.kurzbez1 = zimkateg.kurzbez. 
      rmcat-list.bezeich  = zimkateg.bezeich. 
      rmcat-list.haupt    = YES. 
    END. 
  END. 

  datum-rmcat = curr-date. 
  IF anz-setup GT 0 THEN n = 1.
  ELSE n = 99.
  DO WHILE n LE 21: 
    FOR EACH kontline WHERE kontline.betriebsnr = 1 
      AND kontline.ankunft LE datum-rmcat AND kontline.abreise GE datum-rmcat 
      AND kontline.kontstat = 1 NO-LOCK BY kontline.zikatnr: 
      IF curr-zikat NE kontline.zikatnr THEN 
      DO: 
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = kontline.zikatnr NO-LOCK. 
        FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = kontline.zikatnr 
          AND rmcat-list.haupt = YES AND rmcat-list.glores = YES NO-ERROR. 
        IF NOT AVAILABLE rmcat-list THEN 
        DO: 
          CREATE rmcat-list. 
          ASSIGN 
            rmcat-list.zikatnr  = kontline.zikatnr 
            rmcat-list.kurzbez  = zimkateg.kurzbez 
            rmcat-list.kurzbez1 = zimkateg.kurzbez 
            rmcat-list.bezeich  = zimkateg.bezeich 
            rmcat-list.haupt    = YES 
            rmcat-list.glores   = YES 
            curr-zikat = zimkateg.zikatnr. 
        END. 
      END. 
    END. 
    datum-rmcat = datum-rmcat + 1. 
    n = n + 1. 
  END. 
END. 

