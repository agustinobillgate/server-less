DEF INPUT  PARAMETER gastno      AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER zahlungsart AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER outstand    AS DECIMAL NO-UNDO INIT 0.

FOR EACH debitor WHERE debitor.artnr = zahlungsart 
    AND debitor.gastnr = gastno AND debitor.opart LE 1 NO-LOCK: 
    outstand = outstand + debitor.saldo. 
END.
