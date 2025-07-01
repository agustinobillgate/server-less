DEF TEMP-TABLE ghistory   LIKE history
  FIELD hname   AS CHAR FORMAT "x(24)" COLUMN-LABEL "Hotel Name"
  FIELD gname   AS CHAR
  FIELD address AS CHAR
  FIELD s-recid AS INTEGER.

DEF TEMP-TABLE summ-list LIKE history. /*ger 66FA47*/

DEFINE BUFFER hist1 FOR history.

DEF INPUT  PARAMETER gastnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER fdate  AS DATE    NO-UNDO.
DEF INPUT  PARAMETER tdate  AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR ghistory.
DEF OUTPUT PARAMETER TABLE FOR summ-list. /*ger 66FA47*/

DEFINE VARIABLE htl-name AS CHARACTER.

/*FDL Jan 20, 2023 - Ticket 890590*/
FIND FIRST paramtext WHERE paramtext.txtnr EQ 200 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN htl-name = paramtext.ptexte.

RUN create-ghistory.

PROCEDURE create-ghistory:
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
  
    /* FDL Comment
    IF AVAILABLE queasy THEN ghistory.hname = queasy.char3.
    */
    ghistory.hname = htl-name.
    ASSIGN ghistory.s-recid = INTEGER(RECID(history)).
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
          summ-list.zikateg        = "T O T A L"
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
  END.
  /*end ger*/
END.
