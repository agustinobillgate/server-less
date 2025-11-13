USING System.*. 
USING System.Net.*.

DEFINE TEMP-TABLE header-list
  FIELD vKey AS CHAR
  FIELD vValue AS CHAR.

/**/
DEFINE INPUT PARAMETER get-post AS CHAR. /* GET or POST */
DEFINE INPUT PARAMETER web-url AS CHAR.
DEFINE INPUT PARAMETER body AS LONGCHAR.
DEFINE INPUT PARAMETER TABLE FOR header-list. 
DEFINE OUTPUT PARAMETER webResponse AS LONGCHAR NO-UNDO. 
DEFINE OUTPUT PARAMETER errorMsg    AS CHARACTER NO-UNDO.
/**/
/*
DEF VAR errorMsg AS CHAR INIT "".
DEF VAR get-post AS CHAR INIT "post".

DEF VAR web-url AS CHAR INIT "http://103.58.162.85/api/event/checkout".
/*
DEF VAR web-url AS CHAR INIT "http://www.google.com".
*/
DEF VAR body AS LONGCHAR.
DEF VAR webresponse AS LONGCHAR.

body = CHR(123) + '~n' +
            '"room" : "102"' + '~n' +
       CHR(125).
*/
DEFINE VARIABLE HttpClient AS CLASS System.Net.WebClient. 
FIX-CODEPAGE (webResponse) = "UTF-8". 

HttpClient = NEW System.Net.WebClient(). 

ServicePointManager:SecurityProtocol = CAST(Progress.Util.EnumHelper:Or(SecurityProtocolType:Tls12,SecurityProtocolType:Tls11),SecurityProtocolType).
HttpClient:Proxy:Credentials = System.Net.CredentialCache:DefaultNetworkCredentials. 

/* Set Headers */
FOR EACH header-list:
  HttpClient:Headers:ADD(vKey,vValue).
END.
/*
MESSAGE STRING(body)
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
/*GET*/
IF get-post EQ "get" THEN
DO:
    webResponse = HttpClient:DownloadString(web-url) NO-ERROR.
    IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
        errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
END.
ELSE IF get-post EQ "post" THEN
DO:
    webResponse = HttpClient:UploadString(web-url,body) NO-ERROR.
    IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
        errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
END.
ELSE
DO:
    webResponse = HttpClient:UploadString(web-url,get-post,body) NO-ERROR.
    IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
        errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
END.
/*
MESSAGE String(webresponse)
    VIEW-AS ALERT-BOX INFO BUTTONS OK.

MESSAGE STRING(errorMsg)
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
*/
HttpClient:Dispose(). 
DELETE OBJECT HttpClient. 
