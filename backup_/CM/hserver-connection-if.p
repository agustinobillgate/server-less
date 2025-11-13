
DEF VAR lvCAREA AS CHAR INITIAL "hServer-connect".   
  
DEFINE SHARED VARIABLE ASremoteFlag AS LOGICAL          NO-UNDO.   
DEFINE SHARED VARIABLE  hServer     AS HANDLE           NO-UNDO.  
DEFINE SHARED VARIABLE  vAppParam   AS CHAR             NO-UNDO.  
DEFINE OUTPUT PARAMETER lReturn     AS LOGICAL INIT YES NO-UNDO.
DEFINE OUTPUT PARAMETER errorMsg    AS CHARACTER        NO-UNDO.

DEFINE VARIABLE vAppParamSSL        AS CHAR             NO-UNDO.

IF NOT ASremoteFLag THEN /* this is the local mode */
DO:
    errorMsg = "ERROR|ASremoteFlag=NO, Running Locally".
    RETURN.
END.
  
IF NOT hServer:CONNECTED() THEN  
DO:  
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait").   
    PROCESS EVENTS.   
    ASSIGN vAppParamSSL = vAppParam + " -ssl -nohostverify -sslprotocols TLSv1 -sslciphers RC4-SHA -ct 1".
    lReturn = hServer:DISCONNECT() NO-ERROR.  
    lReturn = NO.
    lReturn = hServer:CONNECT(vAppParamSSL, ? , ? , ?) NO-ERROR.   /* TLS 1.0 */
    IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
        errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
      
    IF NOT lReturn THEN
    DO:
        ASSIGN vAppParamSSL = vAppParam + " -ssl -nohostverify -ct 1".
        lReturn = hServer:DISCONNECT() NO-ERROR.  
        lReturn = NO.
        lReturn = hServer:CONNECT(vAppParamSSL, ? , ? , ?) NO-ERROR.   /* TLS 1.2*/
        IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
            errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
    END.
    /*ASSIGN vAppParamSSL = vAppParam + " -ssl -nohostverify".
    lReturn = hServer:DISCONNECT() NO-ERROR.  
    lReturn = NO.
    lReturn = hServer:CONNECT(vAppParamSSL, ? , ? , ?) NO-ERROR.  */

    
    IF NOT lReturn THEN DO:
     ASSIGN vAppParamSSL = vAppParam + " -ct 1".
     lReturn = hServer:DISCONNECT() NO-ERROR.  
     lReturn = NO.
     lReturn = hServer:CONNECT(vAppParam, ? , ? , ?) NO-ERROR. /*normal*/
     END.
    IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
        errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").
    IF NOT lReturn THEN  
        errorMsg = errorMsg + " ERROR|Can not connect to the AppServer.".
END.

/* clear error message if connected */
IF lReturn THEN
    errorMsg = "".
