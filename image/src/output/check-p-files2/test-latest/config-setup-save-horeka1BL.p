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

DEFINE OUTPUT PARAMETER msg-str            AS CHAR    NO-UNDO.

DEFINE VARIABLE ct AS CHAR NO-UNDO.

FIND FIRST l-artikel WHERE l-artikel.bestellt
    AND NOT l-artikel.bezeich MATCHES "(Don't use)*"
    AND NOT l-artikel.bezeich MATCHES "(Dont use)*"
    AND NOT l-artikel.bezeich MATCHES "(Don't used)*"
    AND NOT l-artikel.bezeich MATCHES "(Dont used)*"
    AND NOT l-artikel.bezeich MATCHES "(Don't Use )*"
    AND NOT l-artikel.bezeich MATCHES "*(Don't Use)"
    AND l-artikel.traubensort = " " OR l-artikel.masseinheit = " " NO-LOCK NO-ERROR.
IF AVAILABLE l-artikel THEN DO:
    msg-str = "There are delivery units/mess units still empty. Please check again.".
    RETURN.
END.


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
      
