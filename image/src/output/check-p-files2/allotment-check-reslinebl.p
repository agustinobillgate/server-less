
DEFINE INPUT  PARAMETER kontcode AS CHAR.
DEFINE INPUT  PARAMETER kontignr AS INT.
DEFINE OUTPUT PARAMETER it-exist AS LOGICAL INITIAL NO.
DEFINE OUTPUT PARAMETER res-line-resnr   AS INT.
DEFINE OUTPUT PARAMETER res-line-name    AS CHAR.
DEFINE OUTPUT PARAMETER res-line-ankunft AS DATE.
DEFINE OUTPUT PARAMETER res-line-abreise AS DATE.

FIND FIRST kontline WHERE kontline.kontignr = kontignr
    AND kontline.kontcode = kontcode.

RUN check-resline.

PROCEDURE check-resline:

DEFINE VARIABLE d AS DATE. 
DEFINE buffer kline FOR kontline. 
  FOR EACH res-line WHERE res-line.kontignr GT 0 
    AND res-line.active-flag LT 2 
    AND res-line.resstatus LT 11 NO-LOCK, 
    FIRST kline WHERE kline.kontignr = res-line.kontignr 
    AND kline.kontcode = kontline.kontcode AND kline.kontstat = 1 NO-LOCK: 
    IF res-line.abreise LE kontline.ankunft 
    OR res-line.ankunft GT kontline.abreise THEN . 
    ELSE 
    DO: 
        res-line-resnr = res-line.resnr.
        res-line-name = res-line.name.
        res-line-ankunft = res-line.ankunft.
        res-line-abreise = res-line.abreise.
        it-exist = YES.
        RETURN.
    END. 
  END. 
END. 
