
DEFINE TEMP-TABLE allot-list
    FIELD datum     AS DATE                 COLUMN-LABEL "Date"
    FIELD w-day     AS CHAR    FORMAT "x(3)" COLUMN-LABEL "WD"
    FIELD tot-rm    AS INTEGER FORMAT ">>>" COLUMN-LABEL "TotRm"
    FIELD ooo       AS INTEGER FORMAT ">>>" COLUMN-LABEL "OOO"
    FIELD occ       AS INTEGER FORMAT ">>>" COLUMN-LABEL "Occ"
    FIELD avl-rm    AS INTEGER FORMAT ">>>" COLUMN-LABEL "Saleable"
    FIELD stat1     AS INTEGER FORMAT ">>>" COLUMN-LABEL "Guaranted"
    FIELD stat2     AS INTEGER FORMAT ">>>" COLUMN-LABEL "6 PM"
    FIELD stat5     AS INTEGER FORMAT ">>>" COLUMN-LABEL "VerbalConf"
    FIELD glres     AS INTEGER FORMAT ">>>" COLUMN-LABEL "Gl-Res"
    FIELD avail1    AS INTEGER FORMAT ">>>" COLUMN-LABEL "Avail"
    FIELD ovb1      AS INTEGER FORMAT ">>>" COLUMN-LABEL "OVB"
    FIELD allot1    AS INTEGER FORMAT ">>>" COLUMN-LABEL "Gl-Allot"
    FIELD gl-allot  AS INTEGER FORMAT ">>9" COLUMN-LABEL "Chg To"
    FIELD gl-used   AS INTEGER FORMAT ">>9" COLUMN-LABEL "Used"
    FIELD gl-remain AS INTEGER FORMAT ">>9" COLUMN-LABEL "Remain"
    FIELD allot2    AS INTEGER FORMAT ">>>" COLUMN-LABEL "OthAllot"
    FIELD blank-str AS CHAR    FORMAT "x(1)" COLUMN-LABEL "" 
    FIELD avail2    AS INTEGER FORMAT ">>>" COLUMN-LABEL "AVAIL"
    FIELD ovb2      AS INTEGER FORMAT ">>>" COLUMN-LABEL "OVB"
    FIELD s-avail2  AS INTEGER
    FIELD expired   AS LOGICAL INIT NO
.

DEF INPUT PARAMETER user-init AS CHAR NO-UNDO.
DEF INPUT PARAMETER currcode  AS CHAR NO-UNDO.
DEF INPUT PARAMETER TABLE     FOR allot-list.

RUN update-allotment.

PROCEDURE update-allotment:
DEF BUFFER kline  FOR kontline.
DEF BUFFER kbuff  FOR kontline.

  FOR EACH allot-list WHERE allot-list.expired = NO 
      AND allot-list.allot1 NE allot-list.gl-allot BY allot-list.datum:
      FIND FIRST kontline WHERE kontline.kontcode = currcode
          AND kontline.ankunft LE allot-list.datum
          AND kontline.abreise GE allot-list.datum NO-ERROR.
      IF AVAILABLE kontline AND kontline.zimmeranz NE allot-list.gl-allot THEN
      DO:
        IF kontline.ankunft = kontline.abreise THEN
        DO:
            ASSIGN kontline.zimmeranz = allot-list.gl-allot.
            FIND CURRENT kontline NO-LOCK.
        END.
        ELSE
        DO:
            FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK. 
            counters.counter = counters.counter + 1. 
            FIND CURRENT counter NO-LOCK. 
            CREATE kline.
            BUFFER-COPY kontline EXCEPT kontignr TO kline.
            ASSIGN
              kline.abreise  = allot-list.datum - 1
              kline.kontignr = counters.counter
            .
            FIND CURRENT kline NO-LOCK.
            
            FIND FIRST counters WHERE counters.counter-no = 10 EXCLUSIVE-LOCK. 
            counters.counter = counters.counter + 1. 
            FIND CURRENT counter NO-LOCK. 
            CREATE kline.
            BUFFER-COPY kontline EXCEPT kontignr TO kline.
            ASSIGN
              kline.ankunft  = allot-list.datum + 1
              kline.kontignr = counters.counter
            .
            FIND CURRENT kline NO-LOCK.
            
            ASSIGN 
                kontline.ankunft      = allot-list.datum
                kontline.abreise      = allot-list.datum
                kontline.zimmeranz    = allot-list.gl-allot
                kontline.useridanlage = user-init
            .
            FIND CURRENT kontline NO-LOCK.
        END.
      END.
  END.
/* merge kontline with the same QTY */
  FOR EACH kontline WHERE kontline.kontcode = currcode NO-LOCK BY kontline.ankunft:
      FIND FIRST kline WHERE kline.kontcode = currcode
          AND kline.ankunft = kontline.abreise + 1
          AND kline.zimmeranz = kontline.zimmeranz NO-LOCK NO-ERROR.
      IF AVAILABLE kline THEN
      DO:
        FIND FIRST kbuff WHERE RECID(kbuff) = RECID(kontline).
        ASSIGN kbuff.abreise = kline.abreise.
        FIND CURRENT kbuff NO-LOCK.
        FIND CURRENT kline EXCLUSIVE-LOCK.
        DELETE kline.
        RELEASE kline.
      END.
  END.
END.

