DEFINE TEMP-TABLE webservice-info
    FIELD VHPWebBased1 AS CHAR
    FIELD VHPWebBased2 AS CHAR
    FIELD VHPWebBased3 AS CHAR
    FIELD VHPWebBased4 AS CHAR
    FIELD VHPWebBased5 AS CHAR
    FIELD VHPWebBased1-AppServiceName AS CHAR
    FIELD VHPWebBased2-AppServiceName AS CHAR
    FIELD VHPWebBased3-AppServiceName AS CHAR
    FIELD VHPWebBased4-AppServiceName AS CHAR
    FIELD VHPWebBased5-AppServiceName AS CHAR
    FIELD vhplibweb-version AS CHAR
    /*
    FIELD VHPMobile1 AS CHAR
    FIELD VHPMobile2 AS CHAR
    FIELD VHPMobile3 AS CHAR
    FIELD VHPMobile4 AS CHAR
    FIELD VHPMobile5 AS CHAR
    FIELD VHPMobileAppServiceName1 AS CHAR
    FIELD VHPMobileAppServiceName2 AS CHAR
    FIELD VHPMobileAppServiceName3 AS CHAR
    FIELD VHPMobileAppServiceName4 AS CHAR
    FIELD VHPMobileAppServiceName5 AS CHAR
    FIELD vhplibmobile-version AS CHAR*/
    .

DEFINE OUTPUT PARAMETER TABLE FOR webservice-info.

DEFINE VARIABLE vhplib-version AS CHAR.
DEFINE VARIABLE tomcat-path    AS CHAR.
DEFINE VARIABLE run-path    AS CHAR EXTENT 5.
DEFINE VARIABLE usr-path    AS CHAR EXTENT 5.
DEFINE VARIABLE web-version AS CHAR EXTENT 5.
DEFINE VARIABLE run-name    AS CHAR EXTENT 5.
DEFINE VARIABLE gethtml     AS LONGCHAR EXTENT 5.
DEFINE VARIABLE getruntime  AS LONGCHAR EXTENT 5.
DEFINE VARIABLE loop-i      AS INT.

/*HANYA UBAH VALUE INI SAJA*/

vhplib-version = "v8.7.17.16".

/*==========================*/

IF SEARCH ("/usr1/tomcat/apache-tomcat-9.0.39/webapps/VHPWebBased1/index.html")  NE ? THEN tomcat-path = "/usr1/tomcat/apache-tomcat-9.0.39".
IF SEARCH ("/usr1/tomcat/apache-tomcat-9.0.74/webapps/VHPWebBased1/index.html")  NE ? THEN tomcat-path = "/usr1/tomcat/apache-tomcat-9.0.74".
IF SEARCH ("/usr1/tomcat/apache-tomcat-8.5.100/webapps/VHPWebBased1/index.html") NE ? THEN tomcat-path = "/usr1/tomcat/apache-tomcat-8.5.100".

usr-path[1] = tomcat-path + "/webapps/VHPWebBased1/index.html".
usr-path[2] = tomcat-path + "/webapps/VHPWebBased2/index.html".
usr-path[3] = tomcat-path + "/webapps/VHPWebBased3/index.html".
usr-path[4] = tomcat-path + "/webapps/VHPWebBased4/index.html".
usr-path[5] = tomcat-path + "/webapps/VHPWebBased5/index.html".

run-path[1] = tomcat-path + "/webapps/VHPWebBased1/WEB-INF/adapters/runtime.props".
run-path[2] = tomcat-path + "/webapps/VHPWebBased2/WEB-INF/adapters/runtime.props".
run-path[3] = tomcat-path + "/webapps/VHPWebBased3/WEB-INF/adapters/runtime.props".
run-path[4] = tomcat-path + "/webapps/VHPWebBased4/WEB-INF/adapters/runtime.props".
run-path[5] = tomcat-path + "/webapps/VHPWebBased5/WEB-INF/adapters/runtime.props".

IF usr-path[1] NE "" THEN COPY-LOB FROM FILE usr-path[1] TO gethtml[1] NO-ERROR.
IF usr-path[2] NE "" THEN COPY-LOB FROM FILE usr-path[2] TO gethtml[2] NO-ERROR.
IF usr-path[3] NE "" THEN COPY-LOB FROM FILE usr-path[3] TO gethtml[3] NO-ERROR.
IF usr-path[4] NE "" THEN COPY-LOB FROM FILE usr-path[4] TO gethtml[4] NO-ERROR.
IF usr-path[5] NE "" THEN COPY-LOB FROM FILE usr-path[5] TO gethtml[5] NO-ERROR.

IF run-path[1] NE "" THEN COPY-LOB FROM FILE run-path[1] TO getruntime[1] NO-ERROR.
IF run-path[2] NE "" THEN COPY-LOB FROM FILE run-path[2] TO getruntime[2] NO-ERROR.
IF run-path[3] NE "" THEN COPY-LOB FROM FILE run-path[3] TO getruntime[3] NO-ERROR.
IF run-path[4] NE "" THEN COPY-LOB FROM FILE run-path[4] TO getruntime[4] NO-ERROR.
IF run-path[5] NE "" THEN COPY-LOB FROM FILE run-path[5] TO getruntime[5] NO-ERROR.

DO loop-i = 1 TO 5:
    web-version[loop-i] = STRING(SUBSTRING(gethtml[loop-i],1,1053)).
    web-version[loop-i] = STRING(SUBSTRING(web-version[loop-i],977,85)).
    web-version[loop-i] = REPLACE(web-version[loop-i],"<br>","").
    web-version[loop-i] = REPLACE(web-version[loop-i],"<","").
    web-version[loop-i] = REPLACE(web-version[loop-i],">","").
    web-version[loop-i] = REPLACE(web-version[loop-i],"\r","").
    web-version[loop-i] = REPLACE(web-version[loop-i],"\n","").
    web-version[loop-i] = TRIM(web-version[loop-i]).
END.

DO loop-i = 1 TO 5:
    run-name[loop-i] = STRING(SUBSTRING(getruntime[loop-i],1,904)).
    run-name[loop-i] = STRING(SUBSTRING(run-name[loop-i],843,62)).
    run-name[loop-i] = REPLACE(run-name[loop-i],"<","").
    run-name[loop-i] = REPLACE(run-name[loop-i],">","").
    run-name[loop-i] = REPLACE(run-name[loop-i],"/","").
    run-name[loop-i] = REPLACE(run-name[loop-i],"bpm:appServiceName","").
    run-name[loop-i] = REPLACE(run-name[loop-i],"\r","").
    run-name[loop-i] = REPLACE(run-name[loop-i],"\n","").
    run-name[loop-i] = TRIM(run-name[loop-i]).
END.



CREATE webservice-info.
ASSIGN 
    webservice-info.VHPWebBased1 = web-version[1] 
    webservice-info.VHPWebBased2 = web-version[2] 
    webservice-info.VHPWebBased3 = web-version[3] 
    webservice-info.VHPWebBased4 = web-version[4] 
    webservice-info.VHPWebBased5 = web-version[5]

    webservice-info.VHPWebBased1-AppServiceName = run-name[1]
    webservice-info.VHPWebBased2-AppServiceName = run-name[2]
    webservice-info.VHPWebBased3-AppServiceName = run-name[3]
    webservice-info.VHPWebBased4-AppServiceName = run-name[4]
    webservice-info.VHPWebBased5-AppServiceName = run-name[5]

    webservice-info.vhplibweb-version = vhplib-version
    .


/*WAJIB UPDATE SETIAP RELEASE GIT*/


