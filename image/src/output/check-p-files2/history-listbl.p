/*ragung */
/*ragung */
/*ragung */
/*ragung 2115C6*/
DEFINE TEMP-TABLE history-list
    FIELD gastinfo        LIKE history.gastinfo
    FIELD ankunft         LIKE history.ankunft 
    FIELD abreise         LIKE history.abreise 
    FIELD abreisezeit     LIKE history.abreisezeit 
    FIELD zikateg         LIKE history.zikateg 
    FIELD zinr            LIKE history.zinr 
    FIELD zipreis         LIKE history.zipreis 
    FIELD zimmeranz       LIKE history.zimmeranz 
    FIELD arrangement     LIKE history.arrangement 
    FIELD resnr           LIKE history.resnr 
    FIELD gesamtumsatz    LIKE history.gesamtumsatz 
    FIELD zahlungsart     LIKE history.zahlungsart 
    FIELD segmentcode     LIKE history.segmentcode 
    FIELD bemerk          LIKE history.bemerk
    FIELD betriebsnr      LIKE history.betriebsnr
    FIELD reslinnr        LIKE history.reslinnr
    FIELD gastnr          LIKE history.gastnr
    /*gerald request E3A60C*/
    FIELD address         LIKE guest.adresse1
    FIELD telefon         LIKE guest.telefon
    /*Riven request B61AFE*/
    FIELD vip             AS CHARACTER.

DEF TEMP-TABLE h-list LIKE history
    /*gerald request E3A60C*/
    FIELD address         LIKE guest.adresse1
    FIELD telefon         LIKE guest.telefon.

DEF TEMP-TABLE i-list 
  FIELD s-recid AS INTEGER
  FIELD ind     AS INTEGER INITIAL 0.

DEF INPUT PARAMETER from-name AS CHAR.
DEF INPUT PARAMETER zinr      AS CHAR.
DEF INPUT PARAMETER disptype  AS INT.
DEF INPUT PARAMETER sorttype  AS INT.
DEF INPUT PARAMETER all-flag  AS LOGICAL.
DEF INPUT PARAMETER f-date    AS DATE.
DEF INPUT PARAMETER t-date    AS DATE.
DEF OUTPUT PARAMETER TABLE FOR history-list.

DEFINE VARIABLE zeit AS INTEGER.
DEFINE VARIABLE counter AS INTEGER.

IF SUBSTR(from-name,1,1) = "*" THEN 
DO: 
    IF SUBSTR(from-name, LENGTH(from-name), 1) NE "*" THEN 
      from-name = from-name + "*". 
    IF disptype = 0 THEN RUN disp-it1. 
    ELSE IF disptype GT 0 AND NOT all-flag THEN RUN disp-it1A.
    ELSE IF disptype GT 0 AND all-flag THEN RUN disp-it1B.
END. 
ELSE 
DO: 
    IF disptype = 0 THEN RUN disp-it.     
    ELSE IF disptype GT 0 AND NOT all-flag THEN RUN disp-itA.
    ELSE IF disptype GT 0 AND all-flag THEN RUN disp-itB.  
END.


PROCEDURE disp-it: 
  DEFINE VARIABLE curr-date AS INTEGER NO-UNDO.

  IF sorttype = 0 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype NO-LOCK BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.gastnr GT 0 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:
            
            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
              AND guest.name GE from-name 
              AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
                  AND history.gastnr GT 0 
                  AND history.ankunft GE f-date 
                  AND history.ankunft LE t-date USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.     
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name 
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:
            
            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.gastnr EQ guest.gastnr 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date NO-LOCK BY history.gastinfo:
                
                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name 
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.
    ELSE DO:
        /*FOR EACH history WHERE
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK,
          FIRST guest WHERE guest.gastnr = history.gastnr
          AND guest.name GE from-name
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr
              AND guest.name GE from-name
              AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.        
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date
                AND history.zinr EQ zinr 
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END.
  ELSE IF sorttype = 1 THEN 
  DO:
    IF zinr = "" THEN DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name GE from-name 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.
             
            FIND NEXT history WHERE history.betriebsnr LE 1
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.   
    ELSE DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name GE from-name AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it. 

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END.
END. 
 
PROCEDURE disp-itA: 
  
  IF sorttype = 0 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name GE from-name AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it. 
            
            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
    ELSE DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name GE from-name AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it. 

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END. 
  ELSE IF sorttype = 1 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:
            
            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name GE from-name AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it. 

            FIND NEXT history WHERE history.betriebsnr LE 1 
                  AND history.abreise GE f-date 
                  AND history.abreise LE t-date 
                  AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
    ELSE DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name GE from-name AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.     

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name GE from-name
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name GE from-name
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END.
END. 

PROCEDURE disp-itB: 
DEF VAR curr-i AS INTEGER INITIAL 0.
DEF BUFFER hbuff FOR history.
  
  FOR EACH h-list:
    DELETE h-list.
  END.
  FOR EACH i-list:
    DELETE i-list.
  END.
  IF sorttype = 0 THEN DO:
       /*
      FOR EACH history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date AND history.ankunft LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY guest.NAME:
          curr-i = curr-i + 1.
          CREATE h-list.
          BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
          ASSIGN 
            h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
              + " - " + guest.wohnort
            h-list.betriebsnr = 1
          . 
          CREATE i-list.
          ASSIGN
            i-list.s-recid = RECID(h-list)
            i-list.ind = curr-i
          .
          FOR EACH hbuff WHERE hbuff.resnr = history.resnr
            AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr 
            AND NOT hbuff.zi-wechsel NO-LOCK BY hbuff.gastinfo:
            curr-i = curr-i + 1.
            CREATE h-list.
            BUFFER-COPY hbuff TO h-list.
            CREATE i-list.
            ASSIGN
              i-list.s-recid = RECID(h-list)
              i-list.ind = curr-i
            .
          END.
      END.*/

      /* FDL Comment => Still Slow Loading Time
      FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date AND history.ankunft LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE history:
            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
              AND guest.name GE from-name 
              AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                  curr-i = curr-i + 1.
                  CREATE h-list.
                  BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
                  ASSIGN 
                    h-list.gastinfo   = guest.NAME + ", " + guest.anredefirma 
                                        + " - " + guest.wohnort
                    h-list.betriebsnr = 1
                    h-list.address    = guest.adresse1
                    h-list.telefon    = guest.telefon. 

                  CREATE i-list.
                  ASSIGN
                    i-list.s-recid = RECID(h-list)
                    i-list.ind = curr-i
                  .
                  FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                    AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr 
                    AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.gastinfo:
                    curr-i = curr-i + 1.
                    CREATE h-list.
                    BUFFER-COPY hbuff TO h-list.
                    CREATE i-list.
                    ASSIGN
                      i-list.s-recid = RECID(h-list)
                      i-list.ind = curr-i
                    .
                  END.
            END.
            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date AND history.ankunft LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      END.
      */
      /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
      FIND FIRST guest WHERE guest.gastnr GT 0
          AND guest.name GE from-name
          AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE guest:
          /*Sergio 4 May 2023 =>03F3F2 Added by history.ankunft in line 562 & 582*/
          FOR EACH history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.gastnr EQ guest.gastnr NO-LOCK BY history.ankunft:

              curr-i = curr-i + 1.
              CREATE h-list.
              BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
              ASSIGN 
                  h-list.gastinfo   = guest.NAME + ", " + guest.anredefirma 
                                      + " - " + guest.wohnort
                  h-list.betriebsnr = 1
                  h-list.address    = guest.adresse1
                  h-list.telefon    = guest.telefon
              . 
              CREATE i-list.
              ASSIGN
                  i-list.s-recid = RECID(h-list)
                  i-list.ind = curr-i
              .

              FOR EACH hbuff WHERE hbuff.resnr EQ history.resnr
                  AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr 
                  AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.ankunft BY hbuff.gastinfo:
                  curr-i = curr-i + 1.
                  CREATE h-list.
                  BUFFER-COPY hbuff TO h-list.
                  CREATE i-list.
                  ASSIGN
                      i-list.s-recid = RECID(h-list)
                      i-list.ind = curr-i
                  .
              END. 
          END.

          FIND NEXT guest WHERE guest.gastnr GT 0
              AND guest.name GE from-name
              AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      END.
  END.  
  ELSE IF sorttype = 1 THEN DO:
      /*FOR EACH history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date AND history.abreise LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name GE from-name 
          AND guest.karteityp = disptype BY guest.NAME:
          curr-i = curr-i + 1.
          CREATE h-list.
          BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
          ASSIGN 
            h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
              + " - " + guest.wohnort
            h-list.betriebsnr = 1
          .
          CREATE i-list.
          ASSIGN
            i-list.s-recid = RECID(h-list)
            i-list.ind = curr-i
          .
          FOR EACH hbuff WHERE hbuff.resnr = history.resnr
            AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
            AND NOT hbuff.zi-wechsel NO-LOCK BY hbuff.gastinfo:
            curr-i = curr-i + 1.
            CREATE h-list.
            BUFFER-COPY hbuff TO h-list.
            CREATE i-list.
            ASSIGN
              i-list.s-recid = RECID(h-list)
              i-list.ind = curr-i
            .
          END.
      END.*/
      /* FDL Comment => Still Slow Loading Time
      FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date AND history.abreise LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE history:

          FIND FIRST guest WHERE guest.gastnr = history.gastnr 
              AND guest.name GE from-name 
              AND guest.karteityp = disptype NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN DO:
              curr-i = curr-i + 1.
              CREATE h-list.
              BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
              ASSIGN 
                h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
                  + " - " + guest.wohnort
                h-list.betriebsnr = 1
                h-list.address    = guest.adresse1
                h-list.telefon    = guest.telefon. 

              CREATE i-list.
              ASSIGN
                i-list.s-recid = RECID(h-list)
                i-list.ind = curr-i
              .
              FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
                AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.gastinfo:
                curr-i = curr-i + 1.
                CREATE h-list.
                BUFFER-COPY hbuff TO h-list.
                CREATE i-list.
                ASSIGN
                  i-list.s-recid = RECID(h-list)
                  i-list.ind = curr-i
                .
              END.
          END.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date AND history.abreise LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      END.
      */
      /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
      FIND FIRST guest WHERE guest.gastnr GT 0
          AND guest.name GE from-name
          AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE guest:
          /*Sergio 4 May 2023 =>03F3F2 Added by history.abreise in line 685 & 706*/
          FOR EACH history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.gastnr EQ guest.gastnr NO-LOCK BY history.abreise:

              curr-i = curr-i + 1.
              CREATE h-list.
              BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
              ASSIGN 
                  h-list.gastinfo     = guest.NAME + ", " + guest.anredefirma 
                                      + " - " + guest.wohnort
                  h-list.betriebsnr   = 1
                  h-list.address      = guest.adresse1
                  h-list.telefon      = guest.telefon
              . 

              CREATE i-list.
              ASSIGN
                  i-list.s-recid = RECID(h-list)
                  i-list.ind = curr-i
              .

              FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                  AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
                  AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.abreise BY hbuff.gastinfo:
                  curr-i = curr-i + 1.
                  CREATE h-list.
                  BUFFER-COPY hbuff TO h-list.
                  CREATE i-list.
                  ASSIGN
                      i-list.s-recid = RECID(h-list)
                      i-list.ind = curr-i
                  .
              END.
          END.

          FIND NEXT guest WHERE guest.gastnr GT 0
              AND guest.name GE from-name
              AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      END.
  END.   
  FOR EACH h-list,
    FIRST i-list WHERE i-list.s-recid = INTEGER(RECID(h-list)) BY i-list.ind:
    RUN assign-it2.
  END.
END. 

PROCEDURE disp-it1: 

  IF sorttype = 0 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/

        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date 
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
    ELSE DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date 
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END. 
  ELSE IF sorttype = 1 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date 
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:
                
                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.   
    ELSE DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END. 
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date 
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:
                
                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END.
END. 
 
PROCEDURE disp-it1A: 
  
  IF sorttype = 0 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date 
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.
    ELSE DO:
        /*
        FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date 
          AND history.ankunft LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.ankunft GE f-date 
                AND history.ankunft LE t-date 
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END. 
  ELSE IF sorttype = 1 THEN 
  DO: 
    IF zinr = "" THEN DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:
                
            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date 
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.
    ELSE DO:
        /*FOR EACH history WHERE 
          history.betriebsnr LE 1 AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY history.gastinfo:
          RUN assign-it.
        END.*/
        /* FDL Comment => Still Slow Loading Time
        FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date 
          AND history.abreise LE t-date 
          AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE history:

            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
                  AND guest.name MATCHES(from-name) 
                  AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN RUN assign-it.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.zinr = zinr AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
        END.
        */
        /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
        FIND FIRST guest WHERE guest.gastnr GT 0
            AND guest.name MATCHES(from-name)
            AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE guest:

            FOR EACH history WHERE history.betriebsnr LE 1 
                AND history.abreise GE f-date 
                AND history.abreise LE t-date 
                AND history.zinr EQ zinr
                AND history.gastnr EQ guest.gastnr NO-LOCK BY history.gastinfo:

                RUN assign-it.
            END.

            FIND NEXT guest WHERE guest.gastnr GT 0
                AND guest.name MATCHES(from-name)
                AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
        END.
    END.    
  END.
END. 

PROCEDURE disp-it1B: 
DEF VAR curr-i AS INTEGER INITIAL 0.
DEF BUFFER hbuff FOR history.
  
  FOR EACH h-list:
    DELETE h-list.
  END.
  IF sorttype = 0 THEN DO:
      /*
      FOR EACH history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date AND history.ankunft LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY guest.NAME: 
          curr-i = curr-i + 1.
          CREATE h-list.
          BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
          ASSIGN 
            h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
              + " - " + guest.wohnort
            h-list.betriebsnr = 1
          . 
          CREATE i-list.
          ASSIGN
            i-list.s-recid = RECID(h-list)
            i-list.ind = curr-i
          .
          FOR EACH hbuff WHERE hbuff.resnr = history.resnr
            AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
            AND NOT hbuff.zi-wechsel NO-LOCK BY hbuff.gastinfo:
            curr-i = curr-i + 1.
            CREATE h-list.
            BUFFER-COPY hbuff TO h-list.
            CREATE i-list.
            ASSIGN
              i-list.s-recid = RECID(h-list)
              i-list.ind = curr-i
            .
          END.
      END.*/
      /* FDL Comment => Still Slow Loading Time
      FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.ankunft GE f-date AND history.ankunft LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE history:
            FIND FIRST guest WHERE guest.gastnr = history.gastnr 
              AND guest.name MATCHES(from-name) 
              AND guest.karteityp = disptype NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN DO:
                  curr-i = curr-i + 1.
                  CREATE h-list.
                  BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
                  ASSIGN 
                    h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
                      + " - " + guest.wohnort
                    h-list.betriebsnr = 1
                    h-list.address    = guest.adresse1
                    h-list.telefon    = guest.telefon. 

                  CREATE i-list.
                  ASSIGN
                    i-list.s-recid = RECID(h-list)
                    i-list.ind = curr-i
                  .
                  FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                    AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
                    AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.gastinfo:
                    curr-i = curr-i + 1.
                    CREATE h-list.
                    BUFFER-COPY hbuff TO h-list.
                    CREATE i-list.
                    ASSIGN
                      i-list.s-recid = RECID(h-list)
                      i-list.ind = curr-i
                    .
                  END.
            END.

            FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date AND history.ankunft LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      END.
      */
      /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
      FIND FIRST guest WHERE guest.gastnr GT 0
          AND guest.name MATCHES(from-name)
          AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE guest:
          /*Sergio 4 May 2023 =>03F3F2 Added by history.ankunft in line 1227 & 1248*/
          FOR EACH history WHERE history.betriebsnr LE 1 
              AND history.ankunft GE f-date 
              AND history.ankunft LE t-date 
              AND history.gastnr EQ guest.gastnr NO-LOCK BY history.ankunft:

              curr-i = curr-i + 1.
              CREATE h-list.
              BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
              ASSIGN 
                  h-list.gastinfo   = guest.NAME + ", " + guest.anredefirma 
                                    + " - " + guest.wohnort
                  h-list.betriebsnr = 1
                  h-list.address    = guest.adresse1
                  h-list.telefon    = guest.telefon
                  . 

              CREATE i-list.
              ASSIGN
                  i-list.s-recid = RECID(h-list)
                  i-list.ind = curr-i
              .

              FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                  AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
                  AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.ankunft BY hbuff.gastinfo:
                  curr-i = curr-i + 1.
                  CREATE h-list.
                  BUFFER-COPY hbuff TO h-list.
                  CREATE i-list.
                  ASSIGN
                      i-list.s-recid = RECID(h-list)
                      i-list.ind = curr-i
                  .
              END.
          END.

          FIND NEXT guest WHERE guest.gastnr GT 0
              AND guest.name MATCHES(from-name)
              AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      END.
  END.  
  ELSE IF sorttype = 1 THEN DO:
      /*
        FOR EACH history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date AND history.abreise LE t-date 
          AND history.gastnr GT 0 NO-LOCK, 
          FIRST guest WHERE guest.gastnr = history.gastnr 
          AND guest.name MATCHES(from-name) 
          AND guest.karteityp = disptype BY guest.NAME: 
          curr-i = curr-i + 1.
          CREATE h-list.
          BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
          ASSIGN 
            h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
              + " - " + guest.wohnort
            h-list.betriebsnr = 1
          . 
          CREATE i-list.
          ASSIGN
            i-list.s-recid = RECID(h-list)
            i-list.ind = curr-i
          .
          FOR EACH hbuff WHERE hbuff.resnr = history.resnr
            AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
            AND NOT hbuff.zi-wechsel NO-LOCK BY hbuff.gastinfo:
            CREATE h-list.
            BUFFER-COPY hbuff TO h-list.
            curr-i = curr-i + 1.
            CREATE i-list.
            ASSIGN
              i-list.s-recid = RECID(h-list)
              i-list.ind = curr-i
            .
          END.
      END.*/
      /* FDL Comment => Still Slow Loading Time
      FIND FIRST history WHERE history.betriebsnr LE 1 
          AND history.abreise GE f-date AND history.abreise LE t-date 
          AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE history:
          FIND FIRST guest WHERE guest.gastnr = history.gastnr 
              AND guest.name MATCHES(from-name) 
              AND guest.karteityp = disptype NO-LOCK NO-ERROR.
          IF AVAILABLE guest THEN DO:
              curr-i = curr-i + 1.
              CREATE h-list.
              BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
              ASSIGN 
                h-list.gastinfo = guest.NAME + ", " + guest.anredefirma 
                  + " - " + guest.wohnort
                h-list.betriebsnr = 1
                h-list.address    = guest.adresse1
                h-list.telefon    = guest.telefon.

              CREATE i-list.
              ASSIGN
                i-list.s-recid = RECID(h-list)
                i-list.ind = curr-i
              .
              FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
                AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.gastinfo:
                CREATE h-list.
                BUFFER-COPY hbuff TO h-list.
                curr-i = curr-i + 1.
                CREATE i-list.
                ASSIGN
                  i-list.s-recid = RECID(h-list)
                  i-list.ind = curr-i
                .
              END.
          END.

          FIND NEXT history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date AND history.abreise LE t-date 
              AND history.gastnr GT 0 USE-INDEX betr-hist_ix NO-LOCK NO-ERROR.
      END.
      */
      /*FDL Jan 31, 2023 => Ticket 3C5B5A Performance Query for Slow Loading Time*/
      FIND FIRST guest WHERE guest.gastnr GT 0
          AND guest.name MATCHES(from-name)
          AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      DO WHILE AVAILABLE guest:
          /*Sergio 4 May 2023 =>03F3F2 Added by history.abreise in line 1351 & 1372*/
          FOR EACH history WHERE history.betriebsnr LE 1 
              AND history.abreise GE f-date 
              AND history.abreise LE t-date 
              AND history.gastnr GT guest.gastnr NO-LOCK BY history.abreise:

              curr-i = curr-i + 1.
              CREATE h-list.
              BUFFER-COPY history EXCEPT history.gastinfo TO h-list.
              ASSIGN 
                  h-list.gastinfo   = guest.NAME + ", " + guest.anredefirma 
                                    + " - " + guest.wohnort
                  h-list.betriebsnr = 1
                  h-list.address    = guest.adresse1
                  h-list.telefon    = guest.telefon
                  .

              CREATE i-list.
              ASSIGN
                  i-list.s-recid = RECID(h-list)
                  i-list.ind = curr-i
              .

              FOR EACH hbuff WHERE hbuff.resnr = history.resnr
                AND hbuff.reslinnr GT 0 AND hbuff.gastnr NE history.gastnr
                AND NOT hbuff.zi-wechsel USE-INDEX res_ix NO-LOCK BY hbuff.abreise BY hbuff.gastinfo:
                CREATE h-list.
                BUFFER-COPY hbuff TO h-list.
                curr-i = curr-i + 1.
                CREATE i-list.
                ASSIGN
                    i-list.s-recid = RECID(h-list)
                    i-list.ind = curr-i
                .
              END.
          END.

          FIND NEXT guest WHERE guest.gastnr GT 0
              AND guest.name MATCHES(from-name)
              AND guest.karteityp EQ disptype USE-INDEX typenam_ix NO-LOCK NO-ERROR.
      END.
  END.
   
  FOR EACH h-list,
    FIRST i-list WHERE i-list.s-recid = INTEGER(RECID(h-list)) BY i-list.ind:
    RUN assign-it2.
  END.
END. 


PROCEDURE assign-it:    
    CREATE history-list.
    ASSIGN
        history-list.gastinfo        = ENTRY(1, history.gastinfo, "-")
        history-list.ankunft         = history.ankunft 
        history-list.abreise         = history.abreise 
        history-list.abreisezeit     = history.abreisezeit 
        history-list.zikateg         = history.zikateg 
        history-list.zinr            = history.zinr 
        history-list.zipreis         = history.zipreis 
        history-list.zimmeranz       = history.zimmeranz 
        history-list.arrangement     = history.arrangement 
        history-list.resnr           = history.resnr 
        history-list.gesamtumsatz    = history.gesamtumsatz 
        history-list.zahlungsart     = history.zahlungsart 
        history-list.segmentcode     = history.segmentcode 
        history-list.bemerk          = history.bemerk
        history-list.betriebsnr      = history.betriebsnr
        history-list.reslinnr        = history.reslinnr
        history-list.gastnr          = history.gastnr
        history-list.address         = guest.adresse1
        history-list.telefon         = guest.telefon.

    /*B61AFE*/
    FIND FIRST segment WHERE segment.segmentcode EQ history.segmentcode
        AND segment.betriebsnr EQ 3 NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
        history-list.vip = "VIP".
    END.
    ELSE
    DO:
        history-list.vip = "non-VIP".
    END.
END.

PROCEDURE assign-it2:
    CREATE history-list.
    ASSIGN
        history-list.gastinfo        = h-list.gastinfo
        history-list.ankunft         = h-list.ankunft 
        history-list.abreise         = h-list.abreise 
        history-list.abreisezeit     = h-list.abreisezeit 
        history-list.zikateg         = h-list.zikateg 
        history-list.zinr            = h-list.zinr 
        history-list.zipreis         = h-list.zipreis 
        history-list.zimmeranz       = h-list.zimmeranz 
        history-list.arrangement     = h-list.arrangement 
        history-list.resnr           = h-list.resnr 
        history-list.gesamtumsatz    = h-list.gesamtumsatz 
        history-list.zahlungsart     = h-list.zahlungsart 
        history-list.segmentcode     = h-list.segmentcode 
        history-list.bemerk          = h-list.bemerk
        history-list.betriebsnr      = h-list.betriebsnr
        history-list.reslinnr        = h-list.reslinnr
        history-list.gastnr          = h-list.gastnr
        history-list.address         = h-list.address
        history-list.telefon         = h-list.telefon.

    /*B61AFE*/
    FIND FIRST segment WHERE segment.segmentcode EQ h-list.segmentcode
        AND segment.betriebsnr EQ 3 NO-LOCK NO-ERROR.
    IF AVAILABLE segment THEN
    DO:
        history-list.vip = "VIP".
    END.
    ELSE
    DO:
        history-list.vip = "non-VIP".
    END.
END.
