DEFINE INPUT PARAMETER resnr     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER reslinnr  AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER curr-code AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER argt      AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER datum     AS DATE    NO-UNDO.

DEFINE OUTPUT PARAMETER rmrate   AS DECIMAL NO-UNDO.


DEFINE VARIABLE ebdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE kbdisc-flag     AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE rate-found      AS LOGICAL INITIAL NO   NO-UNDO.
DEFINE VARIABLE early-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE kback-flag      AS LOGICAL              NO-UNDO.
DEFINE VARIABLE rm-rate         AS DECIMAL              NO-UNDO. 

FIND FIRST res-line WHERE res-line.resnr = resnr AND res-line.reslinnr = reslinnr
    NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN DO:
    FIND FIRST arrangement WHERE arrangement.arrangement = argt NO-LOCK NO-ERROR.
    IF AVAILABLE arrangement THEN DO:
        ASSIGN 
            ebdisc-flag = res-line.zimmer-wunsch MATCHES ("*ebdisc*")
            kbdisc-flag = res-line.zimmer-wunsch MATCHES ("*kbdisc*").

        RUN ratecode-rate.p(ebdisc-flag, kbdisc-flag, res-line.resnr, 
                          res-line.reslinnr, curr-code, ?, datum, res-line.ankunft,
                          res-line.abreise, res-line.reserve-int, arrangement.argtnr,
                          res-line.zikatnr, res-line.erwachs, res-line.kind1, res-line.kind2,
                          res-line.reserve-dec, res-line.betriebsnr, OUTPUT rate-found,
                          OUTPUT rm-rate, OUTPUT early-flag, OUTPUT kback-flag).
        IF rate-found = YES THEN ASSIGN rmrate = rm-rate.
    END.
END.
