DEF TEMP-TABLE ghistory   LIKE history
  FIELD hname   AS CHAR FORMAT "x(24)" COLUMN-LABEL "Hotel Name"
  FIELD gname   AS CHAR
  FIELD address AS CHAR
  FIELD s-recid AS INTEGER
  FIELD vcrnr   AS CHAR /*Add field vcrnr by damen 14/02/2023 DF25EB*/
  FIELD mblnr   AS CHARACTER /*Add field mblnr by damen 14/04/2023 69C171*/
  FIELD email   AS CHARACTER /*Add field email by damen 14/04/2023 69C171*/
  .

DEF TEMP-TABLE summ-list LIKE history. /*ger 66FA47*/

DEFINE BUFFER hist1 FOR history.

DEF INPUT  PARAMETER gastnr AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER fdate  AS DATE    NO-UNDO.
DEF INPUT  PARAMETER tdate  AS DATE    NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR ghistory.
DEF OUTPUT PARAMETER TABLE FOR summ-list. /*ger 66FA47*/

DEFINE VARIABLE htl-name AS CHARACTER.
DEFINE VARIABLE str      AS CHARACTER.
DEFINE VARIABLE i        AS INTEGER.

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

    find first guest where guest.gastnr EQ history.gastnr no-lock no-error.
    if available guest then
    do:
      ghistory.mblnr = guest.mobil-telefon.
      ghistory.email = guest.email-adr.
    end.

    /* FDL Comment
    IF AVAILABLE queasy THEN ghistory.hname = queasy.char3.
    */
    FIND FIRST queasy WHERE queasy.KEY EQ 203
        AND queasy.number1 EQ guest.gastnr
        AND queasy.number2 EQ history.resnr
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN ghistory.hname = queasy.char1.
    END.
    ELSE
    DO:
        ASSIGN ghistory.hname = htl-name.
    END.

    
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
          summ-list.zimmeranz      = ghistory.zimmeranz /* malik 5C68F1*/
          summ-list.zipreis        = ghistory.zipreis
          summ-list.gesamtumsatz   = ghistory.gesamtumsatz
          summ-list.argtumsatz     = ghistory.argtumsatz
          summ-list.f-b-umsatz     = ghistory.f-b-umsatz
          summ-list.sonst-umsatz   = ghistory.sonst-umsatz.
      END.
      ELSE
      DO:
        ASSIGN
          summ-list.zimmeranz      = summ-list.zimmeranz + ghistory.zimmeranz /* malik 5C68F1*/
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
