DEFINE INPUT PARAMETER userinit            AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER custID              AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER username            AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER password            AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER url-push            AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER url-notif           AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER storage             AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER push-dml            AS LOGICAL NO-UNDO.
DEFINE INPUT PARAMETER art-deposit         AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER api-key             AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER supplier            AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER coa-apdeposit       AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER coa-apclearence     AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER artikel-apclearence AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER usr-id              AS INTEGER NO-UNDO.


DEFINE VARIABLE ct AS CHAR NO-UNDO.


ct = "$CustID$" + custID + ";" +
     "$username$" + username + ";" +
     "$password$" + password + ";" +
     "$urlpush$" + url-push + ";" +
     "$urlnotif$" + url-notif + ";" +
     "$storage$" + STRING(storage) + ";" +
     "$pushdml$" + STRING(push-dml) + ";" +
     "$artdeposit$" + STRING(art-deposit) + ";" +
     "$apikey$" + api-key + ";" +
     "$supplier$" + supplier + ";" +
     "$apdeposit$" + coa-apdeposit + ";" +
     "$apclearence$" + coa-apclearence + ";" +
     "$artikelap$" + STRING(artikel-apclearence) + ";" +
     "$userID$" + STRING(usr-id)
  .

FIND FIRST queasy WHERE queasy.KEY = 253 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    ASSIGN queasy.char1 = ct
           queasy.date1 = TODAY
           queasy.char2 = userinit
    .
    FIND CURRENT queasy NO-LOCK.
    RELEASE queasy.
END.
ELSE DO:
    CREATE queasy.
    ASSIGN 
        queasy.KEY      = 253 
        queasy.char1    = ct
        queasy.date1    = TODAY
        queasy.char2    = userinit
     .
END.
      
