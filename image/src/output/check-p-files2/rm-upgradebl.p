DEFINE TEMP-TABLE str-list LIKE res-line
  FIELD gname    LIKE res-line.NAME
  FIELD company  AS CHARACTER FORMAT "x(24)" LABEL "Reserved Name"
  FIELD rmType   LIKE zimkateg.kurzbez COLUMN-LABEL "From" INITIAL ""
  FIELD currency LIKE waehrung.wabkurz COLUMN-LABEL "Curr"
  FIELD cat      LIKE zimkateg.kurzbez COLUMN-LABEL "Cat"
  FIELD id       AS CHARACTER FORMAT "x(4)" COLUMN-LABEL "ID".

DEFINE INPUT PARAMETER datum        AS DATE     NO-UNDO.
DEFINE INPUT PARAMETER to-date      AS DATE     NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR str-list.

DEFINE VARIABLE new-contrate        AS LOGICAL INITIAL NO.
DEFINE VARIABLE curr-date           AS DATE     NO-UNDO. 

DEFINE VARIABLE ci-date             AS DATE                      NO-UNDO.
DEFINE VARIABLE from-date           AS DATE                      NO-UNDO. 
DEFINE VARIABLE ct                  AS CHARACTER                 NO-UNDO.
DEFINE VARIABLE curr-i              AS INTEGER                   NO-UNDO.
DEFINE VARIABLE origZikatnr         AS INTEGER                   NO-UNDO.
DEFINE VARIABLE origrmType          AS CHARACTER FORMAT "x(6)"   NO-UNDO.
DEFINE BUFFER gbuff FOR guest.

FOR EACH str-list:
    DELETE str-list.
END.

FIND FIRST htparam WHERE htparam.paramnr = 550 NO-LOCK.
IF htparam.feldtyp = 4 THEN new-contrate = htparam.flogical.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ASSIGN
  ci-date   = htparam.fdate 
  curr-date = ci-date
  /*datum     = ci-date 
  to-date   = ci-date*/
.
  /*from-date = datum.
  IF datum LT ci-date THEN from-date = ci-date.*/
  IF datum LE to-date THEN RUN upgrade1.
  ELSE IF datum GE to-date THEN RUN upgrade2.  

PROCEDURE upgrade1:
    FOR EACH genstat WHERE genstat.datum LT ci-date
        AND genstat.datum GE datum AND genstat.datum LE to-date
        AND genstat.zinr NE "" 
        AND genstat.res-char[2] MATCHES ("*RmUpgrade*") NO-LOCK:

        origZikatnr = 0.
        DO curr-i = 1 TO NUM-ENTRIES(res-char[2], ";") - 1:
           ct = ENTRY(curr-i, res-char[2], ";").
           IF SUBSTR(ct, 1, 9) = "RmUpgrade" THEN 
           DO:
               origZikatnr = INTEGER(SUBSTR(ct,10)).
               FIND FIRST zimkateg WHERE zimkateg.zikatnr = origZikatnr NO-LOCK NO-ERROR.              
               IF AVAILABLE zimkateg THEN origRmType = zimkateg.kurzbez.
           END.
       END.

       FIND FIRST str-list WHERE str-list.resnr = genstat.resnr
            AND str-list.reslinnr = genstat.res-int[1]
            AND str-list.zikatnr = genstat.zikatnr
            AND str-list.rmType = origRmType NO-LOCK NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK. 
            FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnr NO-LOCK.
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK.
          
            FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
                AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
            IF origRmType NE zimkateg.kurzbez THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.resnr        = genstat.resnr
                    str-list.reslinnr     = genstat.res-int[1]
                    str-list.zinr         = genstat.zinr
                    str-list.zikatnr      = genstat.zikatnr
                    str-list.rmType       = origRmType
                    str-list.arrangement  = genstat.argt
                    str-list.gname        = guest.NAME + ", " + guest.vorname1
                    str-list.company      = gbuff.NAME + ", " + gbuff.anredefirma
                    str-list.ankunft      = genstat.res-date[1]
                    str-list.abreise      = genstat.res-date[2]
                    str-list.zipreis      = genstat.zipreis
                    str-list.cat          = zimkateg.kurzbez
                    str-list.changed      = res-line.changed
                    .

                FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsn NO-LOCK.
                IF AVAILABLE waehrung THEN
                DO:
                    ASSIGN str-list.currency = waehrung.wabkurz.
                END.

                FIND FIRST reservation WHERE reservation.gastnr = genstat.gastnr NO-LOCK NO-ERROR.
                IF AVAILABLE reservation THEN
                DO:
                    ASSIGN
                        str-list.id          = reservation.useridanlage
                        str-list.changed-id  = reservation.useridmutat
                        .
                END.
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE upgrade2:
    FOR EACH res-line WHERE NOT res-line.ankunft GT to-date
        AND NOT res-line.abreise LE from-date 
        AND res-line.active-flag LE 1 AND res-line.resstatus NE 12
        AND res-line.l-zuordnung[1] GE 0 NO-LOCK: 

        ASSIGN 
            origZikatnr = res-line.l-zuordnung[1].

        FIND FIRST zimkateg WHERE zimkateg.zikatnr = origZikatnr NO-LOCK NO-ERROR. /*origRmType*/
        IF AVAILABLE zimkateg THEN ASSIGN origRmType = zimkateg.kurzbez.

        FIND FIRST str-list WHERE str-list.resnr = res-line.resnr
            AND str-list.reslinnr = res-line.reslinnr
            AND str-list.zikatnr = res-line.zikatnr
            AND str-list.rmType = origRmType
            /*AND str-list.zipreis = genstat.zipreis*/ NO-ERROR.
        IF NOT AVAILABLE str-list THEN
        DO:
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.
            FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK.
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr  NO-LOCK NO-ERROR.
            FIND FIRST reservation WHERE reservation.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
            IF origRmType NE zimkateg.kurzbez THEN 
            DO:
                CREATE str-list.
                ASSIGN
                    str-list.resnr       = res-line.resnr
                    str-list.reslinnr    = res-line.reslinnr
                    str-list.zinr        = res-line.zinr
                    str-list.zikatnr     = res-line.zikatnr
                    str-list.rmType      = origRmType
                    str-list.arrangement = res-line.arrangement
                    str-list.gname       = guest.NAME + ", " + guest.vorname1
                    str-list.company     = gbuff.NAME + ", " + gbuff.anredefirma
                    str-list.ankunft     = res-line.ankunft
                    str-list.abreise     = res-line.abreise
                    str-list.zipreis     = res-line.zipreis
                    str-list.cat         = zimkateg.kurzbez
                    str-list.changed     = res-line.changed
                    .
                IF AVAILABLE reservation THEN
                DO:
                    ASSIGN
                        str-list.id          = reservation.useridanlage
                        str-list.changed-id  = reservation.useridmutat
                        .
                END.                
        
                FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
                IF AVAILABLE waehrung THEN ASSIGN str-list.currency = waehrung.wabkurz.
            END.
        END.
    END.
END PROCEDURE.

  /*IF datum LT ci-date THEN
  FOR EACH genstat WHERE genstat.datum LT ci-date
    AND genstat.datum GE datum AND genstat.datum LE to-date
    AND genstat.zinr NE "" 
    AND genstat.res-char[2] MATCHES ("*RmUpgrade*") NO-LOCK:
    origZikatnr = 0.
    DO curr-i = 1 TO NUM-ENTRIES(res-char[2], ";") - 1:
      ct = ENTRY(curr-i, res-char[2], ";").
      IF SUBSTR(ct, 1, 9) = "RmUpgrade" THEN 
      DO:
          origZikatnr = INTEGER(SUBSTR(ct,10)).
          FIND FIRST zimkateg WHERE zimkateg.zikatnr = origZikatnr
          AND zimkateg.kurzbez = origRmType NO-LOCK.
      END.
    END.
    FIND FIRST str-list WHERE str-list.resnr = genstat.resnr
        AND str-list.reslinnr = genstat.res-int[1]
        AND str-list.zikatnr = genstat.zikatnr
        AND str-list.rmType = origRmType NO-LOCK NO-ERROR.
    IF NOT AVAILABLE str-list THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = genstat.gastnrmember NO-LOCK. 
      FIND FIRST gbuff WHERE gbuff.gastnr = genstat.gastnr NO-LOCK.
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = genstat.zikatnr NO-LOCK.
      
      FIND FIRST res-line WHERE res-line.resnr = genstat.resnr
      AND res-line.reslinnr = genstat.res-int[1] NO-LOCK NO-ERROR.
      IF origRmType NE zimkateg.kurzbez THEN 
      DO:
          CREATE str-list.
          ASSIGN
              str-list.resnr        = genstat.resnr
              str-list.reslinnr     = genstat.res-int[1]
              str-list.zinr         = genstat.zinr
              str-list.zikatnr      = genstat.zikatnr
              str-list.rmType       = origRmType
              str-list.arrangement  = genstat.argt
              str-list.gname        = guest.NAME + ", " + guest.vorname1
              str-list.company      = gbuff.NAME + ", " + gbuff.anredefirma
              str-list.ankunft      = genstat.res-date[1]
              str-list.abreise      = genstat.res-date[2]
              str-list.zipreis      = genstat.zipreis
              str-list.cat          = zimkateg.kurzbez
              str-list.changed      = res-line.changed.
          FIND FIRST waehrung WHERE waehrung.waehrungsnr = genstat.wahrungsn NO-LOCK.
          IF AVAILABLE waehrung THEN
          DO:
              ASSIGN str-list.currency = waehrung.wabkurz.
          END.
          IF AVAILABLE reservation THEN
          DO:
              ASSIGN
                  str-list.id          = reservation.useridanlage.
                  str-list.changed-id  = reservation.useridmutat.
          END.
    END.
  END.
 END.
  /*here*/
  IF from-date LE to-date THEN
  FOR EACH res-line WHERE NOT res-line.ankunft GT to-date
    AND NOT res-line.abreise LE from-date 
    AND res-line.active-flag LE 1 AND res-line.resstatus NE 12
    AND res-line.l-zuordnung[1] GE 0 NO-LOCK: 
    ASSIGN origZikatnr = res-line.l-zuordnung[1].
    FIND FIRST zimkateg WHERE zimkateg.zikatnr = origZikatnr NO-LOCK NO-ERROR. /*origRmType*/
    IF AVAILABLE zimkateg THEN
    ASSIGN  origRmType = zimkateg.kurzbez.
    FIND FIRST str-list WHERE str-list.resnr = res-line.resnr
      AND str-list.reslinnr = res-line.reslinnr
      AND str-list.zikatnr = res-line.zikatnr
      AND str-list.rmType = origRmType
      AND str-list.zipreis = genstat.zipreis NO-ERROR.
    IF NOT AVAILABLE str-list THEN
    DO:
      FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK.
      FIND FIRST gbuff WHERE gbuff.gastnr = res-line.gastnr NO-LOCK.
      FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr  NO-LOCK NO-ERROR.
      FIND FIRST reservation WHERE reservation.gastnr = res-line.gastnr NO-LOCK NO-ERROR.
      IF origRmType NE zimkateg.kurzbez THEN DO:
      CREATE str-list.
      ASSIGN
         str-list.resnr       = res-line.resnr
         str-list.reslinnr    = res-line.reslinnr
         str-list.zinr        = res-line.zinr
         str-list.zikatnr     = res-line.zikatnr
         str-list.rmType      = origRmType
         str-list.arrangement = res-line.arrangement
         str-list.gname       = guest.NAME + ", " + guest.vorname1
         str-list.company     = gbuff.NAME + ", " + gbuff.anredefirma
         str-list.ankunft     = res-line.ankunft
         str-list.abreise     = res-line.abreise
         str-list.zipreis     = res-line.zipreis
         str-list.cat         = zimkateg.kurzbez
         str-list.changed     = res-line.changed
         .
         IF AVAILABLE reservation THEN
         str-list.id          = reservation.useridanlage.
         str-list.changed-id  = reservation.useridmutat.
        
     /*FIND FIRST waehrung WHERE waehrung.waehrungsnr = res-line.betriebsnr NO-LOCK NO-ERROR.
     IF AVAILABLE waehrung THEN ASSIGN str-list.currency = waehrung.wabkurz.*/
   END.
 END.
     END.*/
