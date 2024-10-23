
DEFINE TEMP-TABLE tt-prices
    FIELD i-counter AS INTEGER
    FIELD prices    AS INTEGER
.
DEFINE TEMP-TABLE tt-zeiten
    FIELD i-counter AS INTEGER
    FIELD zeiten    AS INTEGER
.
DEF INPUT PARAMETER TABLE FOR tt-prices.
DEF INPUT PARAMETER TABLE FOR tt-zeiten.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER dept AS INT.
DEF INPUT PARAMETER tolerance AS INT.
DEF OUTPUT PARAMETER avail-paramtext AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER t-sprachcode AS INT.
DEF OUTPUT PARAMETER t-ptexte AS CHAR.
DEF OUTPUT PARAMETER t-notes AS CHAR.

DEF VARIABLE prices AS INTEGER FORMAT "9" EXTENT 24. 
DEF VARIABLE zeiten AS INTEGER FORMAT "9" EXTENT 24. 

DEF VARIABLE curr-i AS INTEGER NO-UNDO.

FIND FIRST tt-prices.
FIND FIRST tt-zeiten.

FOR EACH tt-prices:
    prices[tt-prices.i-counter] = tt-prices.prices.
END.
FOR EACH tt-zeiten:
    zeiten[tt-zeiten.i-counter] = tt-zeiten.zeiten.
END.

FIND FIRST paramtext WHERE paramtext.txtnr = (10000 + dept) 
  AND paramtext.number = dept 
  EXCLUSIVE-LOCK NO-ERROR. 
IF AVAILABLE paramtext THEN
DO:
    avail-paramtext = YES.
    t-sprachcode = paramtext.sprachcode.
    t-ptexte = paramtext.ptexte.
    t-notes = paramtext.notes.
END.
IF case-type = 1 THEN
DO:
    IF NOT AVAILABLE paramtext THEN
    DO:
      create paramtext. 
      paramtext.txtnr = 10000 + dept. 
      paramtext.number = dept. 
    END.
    RUN fill-paramtext.
END.

PROCEDURE fill-paramtext: 
DEFINE VARIABLE i AS INTEGER. 
  paramtext.ptexte = "". 
  paramtext.notes = "". 
  DO i = 1 TO 24: 
    paramtext.ptexte = paramtext.ptexte + STRING(prices[i], "9"). 
    paramtext.notes = paramtext.notes + STRING(zeiten[i], "9"). 
  END. 
  paramtext.sprachcode = tolerance. 
END. 

