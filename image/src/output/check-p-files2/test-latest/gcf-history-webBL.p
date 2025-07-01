DEF TEMP-TABLE ghistory   
  FIELD gastnr          LIKE history.gastnr      
  FIELD ankunft         LIKE history.ankunft     
  FIELD abreise         LIKE history.abreise     
  FIELD zimmeranz       LIKE history.zimmeranz   
  FIELD zikateg         LIKE history.zikateg     
  FIELD zinr            LIKE history.zinr        
  FIELD erwachs         LIKE history.erwachs     
  FIELD kind            LIKE history.kind        
  FIELD gratis          LIKE history.gratis      
  FIELD zipreis         LIKE history.zipreis     
  FIELD arrangement     LIKE history.arrangement 
  FIELD gesamtumsatz    LIKE history.gesamtumsatz
  FIELD bemerk          LIKE history.bemerk      
  FIELD logisumsatz     LIKE history.logisumsatz 
  FIELD argtumsatz      LIKE history.argtumsatz  
  FIELD f-b-umsatz      LIKE history.f-b-umsatz  
  FIELD sonst-umsatz    LIKE history.sonst-umsatz
  FIELD gastinfo        LIKE history.gastinfo    
  FIELD zahlungsart     LIKE history.zahlungsart 
  FIELD com-logis       LIKE history.com-logis   
  FIELD com-argt        LIKE history.com-argt    
  FIELD com-f-b         LIKE history.com-f-b     
  FIELD com-sonst       LIKE history.com-sonst   
  FIELD guestnrcom      LIKE history.guestnrcom  
  FIELD abreisezeit     LIKE history.abreisezeit 
  FIELD segmentcode     LIKE history.segmentcode 
  FIELD zi-wechsel      LIKE history.zi-wechsel  
  FIELD resnr           LIKE history.resnr       
  FIELD ums-kurz        LIKE history.ums-kurz    
  FIELD ums-lang        LIKE history.ums-lang    
  FIELD reslinnr        LIKE history.reslinnr    
  FIELD hname           AS CHAR FORMAT "x(24)" COLUMN-LABEL "Hotel Name"
  FIELD gname           AS CHAR
  FIELD address         AS CHAR
  FIELD s-recid         AS INTEGER
  FIELD vcrnr           AS CHAR /*Add field vcrnr by damen 14/02/2023 DF25EB*/
  FIELD mblnr           AS CHARACTER /*Add field mblnr by damen 14/04/2023 69C171*/
  FIELD email           AS CHARACTER /*Add field email by damen 14/04/2023 69C171*/
  .

DEF TEMP-TABLE summ-list LIKE history. /*ger 66FA47*/

DEFINE BUFFER hist1 FOR history.

DEF INPUT  PARAMETER gastnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER fdate  AS DATE    NO-UNDO.
DEF INPUT  PARAMETER tdate  AS DATE    NO-UNDO.
DEF INPUT  PARAMETER vKey   AS INTEGER NO-UNDO. /*FDL Sept 06, 2023 => Ticket 74873E*/
DEF OUTPUT PARAMETER TABLE FOR ghistory.
DEF OUTPUT PARAMETER TABLE FOR summ-list. /*ger 66FA47*/

DEFINE VARIABLE htl-name AS CHARACTER.
DEFINE VARIABLE str      AS CHARACTER.
DEFINE VARIABLE i        AS INTEGER.

DEFINE BUFFER b-history FOR history.

/*FDL Jan 20, 2023 - Ticket 890590*/
FIND FIRST paramtext WHERE paramtext.txtnr EQ 200 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN htl-name = paramtext.ptexte.

RUN create-ghistory.

PROCEDURE create-ghistory:
  IF vKey EQ 1 THEN /*Departure*/
  DO:
    FOR EACH history WHERE history.gastnr = gastnr AND history.abreise GE fdate 
      AND history.abreise LE tdate NO-LOCK BY history.abreise DESCENDING:
      /* FDL Comment
      FIND FIRST queasy WHERE queasy.KEY = 136 AND queasy.number1
        = history.guestnrcom NO-LOCK NO-ERROR.
      */
      CREATE ghistory.
      BUFFER-COPY history EXCEPT gastinfo TO ghistory.
    
      FIND FIRST hist1 WHERE hist1.resnr = history.resnr
          AND hist1.ankunft = history.ankunft 
          AND hist1.abreise = history.abreise 
          AND hist1.segmentcode = history.segmentcode 
          AND hist1.arrangement = history.arrangement NO-LOCK NO-ERROR.  
      IF AVAILABLE hist1 THEN DO:
          ghistory.gastinfo  = hist1.gastinfo.
          ghistory.gname = ENTRY(1, ghistory.gastinfo, "-" ).
          IF NUM-ENTRIES(ghistory.gastinfo, "-") = 2 THEN
              ghistory.address   = ENTRY(2, ghistory.gastinfo, "-").
      END.
    
      /* add by damen 13/02/2023 DF25EB request Sunardi */
      FIND FIRST res-line WHERE res-line.zimmer-wunsch MATCHES "*voucher*"
          AND res-line.resnr EQ history.resnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,7) = "voucher" THEN 
              DO:
                  ghistory.vcrnr = SUBSTR(str,8).
              END.            
          END.
      END.
    
      FIND FIRST guest WHERE guest.gastnr EQ history.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
      DO:
        ghistory.mblnr = guest.mobil-telefon.
        ghistory.email = guest.email-adr.
        ghistory.bemerk = ghistory.bemerk + "G: " + guest.bemerk + CHR(10). /* Naufal Afthar - 96640A -> add guest remark*/

        /* Oscar (24/03/2025) - 088D6D - Add reservation member remark on guest history as Company or Travel Agent */
        IF guest.karteityp NE 0 THEN
        DO:
          ghistory.bemerk = ghistory.bemerk + "RL: " + CHR(10).

          FOR EACH b-history WHERE b-history.resnr EQ history.resnr
            AND b-history.reslinnr NE 999 NO-LOCK
            BY b-history.reslinnr:
              
            FIND FIRST res-line WHERE res-line.resnr EQ b-history.resnr
                AND res-line.reslinnr EQ b-history.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
              IF TRIM(res-line.bemerk) NE "" THEN
              DO:
                  ghistory.bemerk = ghistory.bemerk + "[" + STRING(b-history.reslinnr) + "] " + res-line.bemerk + CHR(10).
              END.
            END.
          END.
        END.
      END.
    
      /* FDL Comment
      IF AVAILABLE queasy THEN ghistory.hname = queasy.char3.
      */
      ghistory.hname = htl-name.
      ASSIGN ghistory.s-recid = INTEGER(RECID(history)).
    END.
  END.
  ELSE IF vKey EQ 2 THEN /*Arrival*/
  DO:
    FOR EACH history WHERE history.gastnr = gastnr AND history.ankunft GE fdate 
      AND history.ankunft LE tdate NO-LOCK BY history.ankunft DESCENDING:
      /* FDL Comment
      FIND FIRST queasy WHERE queasy.KEY = 136 AND queasy.number1
        = history.guestnrcom NO-LOCK NO-ERROR.
      */
      CREATE ghistory.
      BUFFER-COPY history EXCEPT gastinfo TO ghistory.
    
      FIND FIRST hist1 WHERE hist1.resnr = history.resnr
          AND hist1.ankunft = history.ankunft 
          AND hist1.abreise = history.abreise 
          AND hist1.segmentcode = history.segmentcode 
          AND hist1.arrangement = history.arrangement NO-LOCK NO-ERROR.  
      IF AVAILABLE hist1 THEN DO:
          ghistory.gastinfo  = hist1.gastinfo.
          ghistory.gname = ENTRY(1, ghistory.gastinfo, "-" ).
          IF NUM-ENTRIES(ghistory.gastinfo, "-") = 2 THEN
              ghistory.address   = ENTRY(2, ghistory.gastinfo, "-").
      END.
    
      /* add by damen 13/02/2023 DF25EB request Sunardi */
      FIND FIRST res-line WHERE res-line.zimmer-wunsch MATCHES "*voucher*"
          AND res-line.resnr EQ history.resnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,7) = "voucher" THEN 
              DO:
                  ghistory.vcrnr = SUBSTR(str,8).
              END.            
          END.
      END.
    
      FIND FIRST guest WHERE guest.gastnr EQ history.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
      DO:
        ghistory.mblnr = guest.mobil-telefon.
        ghistory.email = guest.email-adr.
        ghistory.bemerk = ghistory.bemerk + "G: " + guest.bemerk + CHR(10). /* Naufal Afthar - 96640A -> add guest remark*/

        /* Oscar (24/03/2025) - 088D6D - Add reservation member remark on guest history as Company or Travel Agent */
        IF guest.karteityp NE 0 THEN
        DO:
          ghistory.bemerk = ghistory.bemerk + "RL: " + CHR(10).

          FOR EACH b-history WHERE b-history.resnr EQ history.resnr
            AND b-history.reslinnr NE 999 NO-LOCK
            BY b-history.reslinnr:
              
            FIND FIRST res-line WHERE res-line.resnr EQ b-history.resnr
                AND res-line.reslinnr EQ b-history.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
              IF TRIM(res-line.bemerk) NE "" THEN
              DO:
                  ghistory.bemerk = ghistory.bemerk + "[" + STRING(b-history.reslinnr) + "] " + res-line.bemerk + CHR(10).
              END.
            END.
          END.
        END.
      END.
    
      /* FDL Comment
      IF AVAILABLE queasy THEN ghistory.hname = queasy.char3.
      */
      ghistory.hname = htl-name.
      ASSIGN ghistory.s-recid = INTEGER(RECID(history)).
    END.
  END.
  
  /*ger 66FA47*/
  FOR EACH ghistory:
      FIND FIRST summ-list WHERE summ-list.gastnr = ghistory.gastnr
            AND summ-list.arrangement = ghistory.arrangement NO-LOCK NO-ERROR.
      IF NOT AVAILABLE summ-list THEN
      DO:
        CREATE summ-list.
        ASSIGN
          summ-list.gastnr         = ghistory.gastnr
          summ-list.zikateg        = "T O T A L - " + ghistory.arrangement
          summ-list.arrangement    = ghistory.arrangement
          summ-list.zimmeranz      = 1
          summ-list.zipreis        = ghistory.zipreis
          summ-list.gesamtumsatz   = ghistory.gesamtumsatz
          summ-list.argtumsatz     = ghistory.argtumsatz
          summ-list.f-b-umsatz     = ghistory.f-b-umsatz
          summ-list.sonst-umsatz   = ghistory.sonst-umsatz.
      END.
      ELSE
      DO:
        ASSIGN
          summ-list.zimmeranz      = summ-list.zimmeranz + 1
          summ-list.zipreis        = summ-list.zipreis      + ghistory.zipreis
          summ-list.gesamtumsatz   = summ-list.gesamtumsatz + ghistory.gesamtumsatz
          summ-list.argtumsatz     = summ-list.argtumsatz   + ghistory.argtumsatz
          summ-list.f-b-umsatz     = summ-list.f-b-umsatz   + ghistory.f-b-umsatz
          summ-list.sonst-umsatz   = summ-list.sonst-umsatz + ghistory.sonst-umsatz.
      END.
      /* ADD by damen 14/04/2023 69C171 */
      FIND FIRST guest WHERE guest.NAME EQ ENTRY(1,ghistory.gname,",") NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN 
      do:
        ghistory.mblnr = guest.mobil-telefon.
        ghistory.email = guest.email-adr.
      end.
  END.
  /*end ger*/
END.
DEF TEMP-TABLE ghistory   
  FIELD gastnr          LIKE history.gastnr      
  FIELD ankunft         LIKE history.ankunft     
  FIELD abreise         LIKE history.abreise     
  FIELD zimmeranz       LIKE history.zimmeranz   
  FIELD zikateg         LIKE history.zikateg     
  FIELD zinr            LIKE history.zinr        
  FIELD erwachs         LIKE history.erwachs     
  FIELD kind            LIKE history.kind        
  FIELD gratis          LIKE history.gratis      
  FIELD zipreis         LIKE history.zipreis     
  FIELD arrangement     LIKE history.arrangement 
  FIELD gesamtumsatz    LIKE history.gesamtumsatz
  FIELD bemerk          LIKE history.bemerk      
  FIELD logisumsatz     LIKE history.logisumsatz 
  FIELD argtumsatz      LIKE history.argtumsatz  
  FIELD f-b-umsatz      LIKE history.f-b-umsatz  
  FIELD sonst-umsatz    LIKE history.sonst-umsatz
  FIELD gastinfo        LIKE history.gastinfo    
  FIELD zahlungsart     LIKE history.zahlungsart 
  FIELD com-logis       LIKE history.com-logis   
  FIELD com-argt        LIKE history.com-argt    
  FIELD com-f-b         LIKE history.com-f-b     
  FIELD com-sonst       LIKE history.com-sonst   
  FIELD guestnrcom      LIKE history.guestnrcom  
  FIELD abreisezeit     LIKE history.abreisezeit 
  FIELD segmentcode     LIKE history.segmentcode 
  FIELD zi-wechsel      LIKE history.zi-wechsel  
  FIELD resnr           LIKE history.resnr       
  FIELD ums-kurz        LIKE history.ums-kurz    
  FIELD ums-lang        LIKE history.ums-lang    
  FIELD reslinnr        LIKE history.reslinnr    
  FIELD hname           AS CHAR FORMAT "x(24)" COLUMN-LABEL "Hotel Name"
  FIELD gname           AS CHAR
  FIELD address         AS CHAR
  FIELD s-recid         AS INTEGER
  FIELD vcrnr           AS CHAR /*Add field vcrnr by damen 14/02/2023 DF25EB*/
  FIELD mblnr           AS CHARACTER /*Add field mblnr by damen 14/04/2023 69C171*/
  FIELD email           AS CHARACTER /*Add field email by damen 14/04/2023 69C171*/
  .

DEF TEMP-TABLE summ-list LIKE history. /*ger 66FA47*/

DEFINE BUFFER hist1 FOR history.

DEF INPUT  PARAMETER gastnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER fdate  AS DATE    NO-UNDO.
DEF INPUT  PARAMETER tdate  AS DATE    NO-UNDO.
DEF INPUT  PARAMETER vKey   AS INTEGER NO-UNDO. /*FDL Sept 06, 2023 => Ticket 74873E*/
DEF OUTPUT PARAMETER TABLE FOR ghistory.
DEF OUTPUT PARAMETER TABLE FOR summ-list. /*ger 66FA47*/

DEFINE VARIABLE htl-name AS CHARACTER.
DEFINE VARIABLE str      AS CHARACTER.
DEFINE VARIABLE i        AS INTEGER.

DEFINE BUFFER b-history FOR history.

/*FDL Jan 20, 2023 - Ticket 890590*/
FIND FIRST paramtext WHERE paramtext.txtnr EQ 200 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN htl-name = paramtext.ptexte.

RUN create-ghistory.

PROCEDURE create-ghistory:
  IF vKey EQ 1 THEN /*Departure*/
  DO:
    FOR EACH history WHERE history.gastnr = gastnr AND history.abreise GE fdate 
      AND history.abreise LE tdate NO-LOCK BY history.abreise DESCENDING:
      /* FDL Comment
      FIND FIRST queasy WHERE queasy.KEY = 136 AND queasy.number1
        = history.guestnrcom NO-LOCK NO-ERROR.
      */
      CREATE ghistory.
      BUFFER-COPY history EXCEPT gastinfo TO ghistory.
    
      FIND FIRST hist1 WHERE hist1.resnr = history.resnr
          AND hist1.ankunft = history.ankunft 
          AND hist1.abreise = history.abreise 
          AND hist1.segmentcode = history.segmentcode 
          AND hist1.arrangement = history.arrangement NO-LOCK NO-ERROR.  
      IF AVAILABLE hist1 THEN DO:
          ghistory.gastinfo  = hist1.gastinfo.
          ghistory.gname = ENTRY(1, ghistory.gastinfo, "-" ).
          IF NUM-ENTRIES(ghistory.gastinfo, "-") = 2 THEN
              ghistory.address   = ENTRY(2, ghistory.gastinfo, "-").
      END.
    
      /* add by damen 13/02/2023 DF25EB request Sunardi */
      FIND FIRST res-line WHERE res-line.zimmer-wunsch MATCHES "*voucher*"
          AND res-line.resnr EQ history.resnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,7) = "voucher" THEN 
              DO:
                  ghistory.vcrnr = SUBSTR(str,8).
              END.            
          END.
      END.
    
      FIND FIRST guest WHERE guest.gastnr EQ history.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
      DO:
        ghistory.mblnr = guest.mobil-telefon.
        ghistory.email = guest.email-adr.
        ghistory.bemerk = ghistory.bemerk + "G: " + guest.bemerk + CHR(10). /* Naufal Afthar - 96640A -> add guest remark*/

        /* Oscar (24/03/2025) - 088D6D - Add reservation member remark on guest history as Company or Travel Agent */
        IF guest.karteityp NE 0 THEN
        DO:
          ghistory.bemerk = ghistory.bemerk + "RL: " + CHR(10).

          FOR EACH b-history WHERE b-history.resnr EQ history.resnr
            AND b-history.reslinnr NE 999 NO-LOCK
            BY b-history.reslinnr:
              
            FIND FIRST res-line WHERE res-line.resnr EQ b-history.resnr
                AND res-line.reslinnr EQ b-history.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
              IF TRIM(res-line.bemerk) NE "" THEN
              DO:
                  ghistory.bemerk = ghistory.bemerk + "[" + STRING(b-history.reslinnr) + "] " + res-line.bemerk + CHR(10).
              END.
            END.
          END.
        END.
      END.
    
      /* FDL Comment
      IF AVAILABLE queasy THEN ghistory.hname = queasy.char3.
      */
      ghistory.hname = htl-name.
      ASSIGN ghistory.s-recid = INTEGER(RECID(history)).
    END.
  END.
  ELSE IF vKey EQ 2 THEN /*Arrival*/
  DO:
    FOR EACH history WHERE history.gastnr = gastnr AND history.ankunft GE fdate 
      AND history.ankunft LE tdate NO-LOCK BY history.ankunft DESCENDING:
      /* FDL Comment
      FIND FIRST queasy WHERE queasy.KEY = 136 AND queasy.number1
        = history.guestnrcom NO-LOCK NO-ERROR.
      */
      CREATE ghistory.
      BUFFER-COPY history EXCEPT gastinfo TO ghistory.
    
      FIND FIRST hist1 WHERE hist1.resnr = history.resnr
          AND hist1.ankunft = history.ankunft 
          AND hist1.abreise = history.abreise 
          AND hist1.segmentcode = history.segmentcode 
          AND hist1.arrangement = history.arrangement NO-LOCK NO-ERROR.  
      IF AVAILABLE hist1 THEN DO:
          ghistory.gastinfo  = hist1.gastinfo.
          ghistory.gname = ENTRY(1, ghistory.gastinfo, "-" ).
          IF NUM-ENTRIES(ghistory.gastinfo, "-") = 2 THEN
              ghistory.address   = ENTRY(2, ghistory.gastinfo, "-").
      END.
    
      /* add by damen 13/02/2023 DF25EB request Sunardi */
      FIND FIRST res-line WHERE res-line.zimmer-wunsch MATCHES "*voucher*"
          AND res-line.resnr EQ history.resnr NO-LOCK NO-ERROR.
      IF AVAILABLE res-line THEN
      DO:
          DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
              str = ENTRY(i, res-line.zimmer-wunsch, ";").
              IF SUBSTR(str,1,7) = "voucher" THEN 
              DO:
                  ghistory.vcrnr = SUBSTR(str,8).
              END.            
          END.
      END.
    
      FIND FIRST guest WHERE guest.gastnr EQ history.gastnr NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN
      DO:
        ghistory.mblnr = guest.mobil-telefon.
        ghistory.email = guest.email-adr.
        ghistory.bemerk = ghistory.bemerk + "G: " + guest.bemerk + CHR(10). /* Naufal Afthar - 96640A -> add guest remark*/

        /* Oscar (24/03/2025) - 088D6D - Add reservation member remark on guest history as Company or Travel Agent */
        IF guest.karteityp NE 0 THEN
        DO:
          ghistory.bemerk = ghistory.bemerk + "RL: " + CHR(10).

          FOR EACH b-history WHERE b-history.resnr EQ history.resnr
            AND b-history.reslinnr NE 999 NO-LOCK
            BY b-history.reslinnr:
              
            FIND FIRST res-line WHERE res-line.resnr EQ b-history.resnr
                AND res-line.reslinnr EQ b-history.reslinnr NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
              IF TRIM(res-line.bemerk) NE "" THEN
              DO:
                  ghistory.bemerk = ghistory.bemerk + "[" + STRING(b-history.reslinnr) + "] " + res-line.bemerk + CHR(10).
              END.
            END.
          END.
        END.
      END.
    
      /* FDL Comment
      IF AVAILABLE queasy THEN ghistory.hname = queasy.char3.
      */
      ghistory.hname = htl-name.
      ASSIGN ghistory.s-recid = INTEGER(RECID(history)).
    END.
  END.
  
  /*ger 66FA47*/
  FOR EACH ghistory:
      FIND FIRST summ-list WHERE summ-list.gastnr = ghistory.gastnr
            AND summ-list.arrangement = ghistory.arrangement NO-LOCK NO-ERROR.
      IF NOT AVAILABLE summ-list THEN
      DO:
        CREATE summ-list.
        ASSIGN
          summ-list.gastnr         = ghistory.gastnr
          summ-list.zikateg        = "T O T A L - " + ghistory.arrangement
          summ-list.arrangement    = ghistory.arrangement
          summ-list.zimmeranz      = 1
          summ-list.zipreis        = ghistory.zipreis
          summ-list.gesamtumsatz   = ghistory.gesamtumsatz
          summ-list.argtumsatz     = ghistory.argtumsatz
          summ-list.f-b-umsatz     = ghistory.f-b-umsatz
          summ-list.sonst-umsatz   = ghistory.sonst-umsatz.
      END.
      ELSE
      DO:
        ASSIGN
          summ-list.zimmeranz      = summ-list.zimmeranz + 1
          summ-list.zipreis        = summ-list.zipreis      + ghistory.zipreis
          summ-list.gesamtumsatz   = summ-list.gesamtumsatz + ghistory.gesamtumsatz
          summ-list.argtumsatz     = summ-list.argtumsatz   + ghistory.argtumsatz
          summ-list.f-b-umsatz     = summ-list.f-b-umsatz   + ghistory.f-b-umsatz
          summ-list.sonst-umsatz   = summ-list.sonst-umsatz + ghistory.sonst-umsatz.
      END.
      /* ADD by damen 14/04/2023 69C171 */
      FIND FIRST guest WHERE guest.NAME EQ ENTRY(1,ghistory.gname,",") NO-LOCK NO-ERROR.
      IF AVAILABLE guest THEN 
      do:
        ghistory.mblnr = guest.mobil-telefon.
        ghistory.email = guest.email-adr.
      end.
  END.
  /*end ger*/
END.
