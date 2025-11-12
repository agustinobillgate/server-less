/****************************************************************************
****************************************************************************
**
**   Date: 2016/10/18
**   Descript: VHP interface program with SiteMinder v2
**
*****************************************************************************
****************************************************************************/
DEFINE NEW SHARED VAR ASremoteFlag  AS LOGICAL INITIAL NO  NO-UNDO. 
DEFINE NEW SHARED VAR hServer       AS HANDLE              NO-UNDO.
DEFINE NEW SHARED VAR hdeskServer   AS HANDLE              NO-UNDO.
DEFINE NEW SHARED VAR vAppParam     AS CHAR                NO-UNDO.
DEFINE VAR vHost         AS CHAR                NO-UNDO.
DEFINE VAR vService      AS CHAR                NO-UNDO.
DEFINE VAR hdeskHost     AS CHAR                NO-UNDO.
DEFINE VAR hdeskService  AS CHAR                NO-UNDO.
DEFINE VAR lReturn       AS LOGICAL             NO-UNDO.
DEFINE VAR hReturn       AS LOGICAL             NO-UNDO.

DEFINE NEW SHARED VARIABLE curr-map AS CHAR     NO-UNDO INITIAL "".
DEFINE NEW SHARED VARIABLE cou-map  AS CHAR     NO-UNDO INITIAL "".


DEFINE VARIABLE vhWebSocket AS HANDLE NO-UNDO.
DEFINE VARIABLE vcXMLText   AS LONGCHAR     NO-UNDO.
DEFINE VARIABLE vcRequest   AS CHARACTER    NO-UNDO.

DEFINE VARIABLE vcWSAgent  AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE vcWSAgent2 AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE vcWSAgent3 AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE vcWSAgent4 AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE vcWSAgent5 AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE vcWebHost  AS CHARACTER INITIAL "" NO-UNDO.
DEFINE VARIABLE vcWebPort  AS CHARACTER INITIAL "" NO-UNDO.

DEFINE VARIABLE vcWebResp           AS LONGCHAR.
DEFINE VARIABLE errorMsg            AS CHARACTER.
DEFINE VARIABLE abi-host            AS CHARACTER. /* untuk ABI (Artotel Booking Indonesia) */
DEFINE VARIABLE abi-port            AS CHARACTER.
DEFINE VARIABLE abi-readmanual-flag AS CHARACTER INIT "".
DEFINE VARIABLE huruf               AS CHARACTER INIT "".
DEFINE VARIABLE debugging-flag      AS CHARACTER INIT "".
DEFINE VARIABLE roomtypeoutput      AS CHARACTER INIT "".
DEFINE VARIABLE backuproomtype      AS CHARACTER INIT "".

DEFINE VARIABLE hXML                AS HANDLE NO-UNDO.
DEFINE VARIABLE hRoot               AS HANDLE NO-UNDO.
DEFINE VARIABLE hWebService         AS HANDLE NO-UNDO.

DEFINE STREAM sBatch.
DEFINE STREAM s1.
DEFINE STREAM s2.
DEFINE STREAM s3.
DEFINE STREAM s4.
DEFINE STREAM lfile.

DEFINE VARIABLE bookengID           AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE response            AS LONGCHAR NO-UNDO.
DEFINE VARIABLE json-str            AS LONGCHAR NO-UNDO.
DEFINE VARIABLE json-file           AS CHAR     NO-UNDO.
DEFINE VARIABLE rDir                AS CHAR     NO-UNDO.
DEFINE VARIABLE allotfile           AS CHAR     NO-UNDO.
DEFINE VARIABLE ratefile            AS CHAR     NO-UNDO.
DEFINE VARIABLE allotflag           AS LOGICAL  NO-UNDO.
DEFINE VARIABLE rateflag            AS LOGICAL  NO-UNDO.
DEFINE VARIABLE comboflag           AS LOGICAL  NO-UNDO.
DEFINE VARIABLE readaricomboflag    AS LOGICAL  NO-UNDO.
DEFINE VARIABLE central-path        AS CHARACTER NO-UNDO. /* BLY 04/06/2025 */

DEFINE VARIABLE bookeng-grp         AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE cPushRate           AS LOGICAL  INITIAL NO.
DEFINE VARIABLE cPullBook           AS LOGICAL  INITIAL NO.
DEFINE VARIABLE cUpdAvail           AS LOGICAL  INITIAL NO.
DEFINE VARIABLE cPushBook           AS LOGICAL  INITIAL NO.
DEFINE VARIABLE delayfrompf         AS INTEGER  INITIAL 60.
DEFINE VARIABLE delay               AS INTEGER  INITIAL 300.
DEFINE VARIABLE period              AS INTEGER  INITIAL 90.
DEFINE VARIABLE dyna-code           AS CHAR     INITIAL "".
DEFINE VARIABLE LiveFlag            AS LOGICAL  INITIAL "YES".
DEFINE VARIABLE prog-avail-update   AS CHAR     INITIAL "".
DEFINE VARIABLE maxAdult            AS INTEGER  INITIAL 1.
DEFINE VARIABLE maxChild            AS INTEGER  INITIAL 0.
DEFINE VARIABLE num-guest           AS INTEGER  NO-UNDO INIT 0.

DEFINE VARIABLE calc-tax-amount      AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE calc-tax-amount-serv AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE avail-after          AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE roomstay-flag        AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE roomstay-comment	 AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE service-flag         AS LOGICAL  NO-UNDO INIT NO.

DEFINE VARIABLE i                   AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE path                AS CHAR     NO-UNDO INITIAL ".\SM\".
DEFINE VARIABLE workPath            AS CHAR     NO-UNDO INITIAL "".
DEFINE VARIABLE logPath             AS CHAR     NO-UNDO INITIAL "".
DEFINE VARIABLE error-str           AS CHAR     NO-UNDO INITIAL "".
DEFINE VARIABLE logpath-flag        AS LOGICAL  NO-UNDO INITIAL NO.
DEFINE VARIABLE done                AS LOGICAL  NO-UNDO INITIAL NO.   
DEFINE VARIABLE frDate              AS DATE     NO-UNDO INITIAL ?.
DEFINE VARIABLE toDate              AS DATE     NO-UNDO INITIAL ?.
DEFINE VARIABLE SM-gastno           AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE qty-booking         AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE pauseinterval       AS INTEGER  NO-UNDO INITIAL 0.
DEFINE VARIABLE restartinterval     AS INTEGER  NO-UNDO INITIAL 3600.

DEFINE VARIABLE htl-code            AS CHARACTER NO-UNDO.
DEFINE VARIABLE cUsername           AS CHARACTER NO-UNDO.
DEFINE VARIABLE cPassword           AS CHARACTER NO-UNDO.
DEFINE VARIABLE hotelfile           AS LOGICAL INIT NO NO-UNDO.
DEFINE VARIABLE hotellist           AS CHARACTER NO-UNDO.
DEFINE VARIABLE filepath            AS CHARACTER NO-UNDO.
DEFINE VARIABLE restartscheduler    AS CHARACTER NO-UNDO.
DEFINE VARIABLE schedulerpath       AS CHARACTER NO-UNDO. /*#F37323*/

DEFINE VARIABLE diff-push-rate      AS LOGICAL INIT YES NO-UNDO.
DEFINE VARIABLE push-all            AS LOGICAL INIT NO NO-UNDO.

DEFINE VARIABLE incl-tentative      AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE pushPax             AS LOGICAL  NO-UNDO INIT NO. 
DEFINE VARIABLE upperCaseName       AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE pushAll             AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE re-calculate        AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE restriction-flag    AS LOGICAL  NO-UNDO INIT YES.
DEFINE VARIABLE allotment           AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE bedSetup            AS LOGICAL  NO-UNDO INIT NO.
DEFINE VARIABLE pax                 AS INT      NO-UNDO INIT 2.
DEFINE VARIABLE delayRate           AS INT      NO-UNDO INIT 0.
DEFINE VARIABLE delayPull           AS INT      NO-UNDO INIT 0.
DEFINE VARIABLE delayAvail          AS INT      NO-UNDO INIT 0.
DEFINE VARIABLE grp                 AS INT      NO-UNDO INIT 0.

DEFINE VARIABLE multiplier          AS INTEGER      NO-UNDO.
DEFINE VARIABLE multiamount         AS CHARACTER    NO-UNDO.
DEFINE VARIABLE multiamount-nett    AS CHARACTER    NO-UNDO.
DEFINE VARIABLE multiamount-tax     AS CHARACTER    NO-UNDO.
DEFINE VARIABLE errfile             AS CHARACTER    NO-UNDO.
DEFINE VARIABLE loopm               AS INTEGER      NO-UNDO.
DEFINE VARIABLE rcode-rmtype AS CHARACTER NO-UNDO.
DEFINE VARIABLE taxflag     AS LOGICAL INIT YES.
DEFINE VARIABLE dirname     AS CHAR.
DEFINE VARIABLE del-folder  AS INT.

/*Jason 21 July 2016 Siteminder v2*/
DEFINE VARIABLE uuid         AS RAW       NO-UNDO.
DEFINE VARIABLE echotoken    AS CHARACTER NO-UNDO INITIAL "".
DEFINE VARIABLE timestamp    AS CHARACTER NO-UNDO.
DEFINE VARIABLE str-date     AS CHARACTER NO-UNDO.
DEFINE VARIABLE serviceRPH   AS CHARACTER NO-UNDO INIT "".
DEFINE VARIABLE m            AS INTEGER   NO-UNDO.
DEFINE VARIABLE yy           AS INTEGER   NO-UNDO.
DEFINE VARIABLE dd           AS INTEGER   NO-UNDO.
DEFINE VARIABLE resnr            AS INTEGER     NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-aftertax     AS DECIMAL     NO-UNDO INITIAL 0.
DEFINE VARIABLE tot-beforetax    AS DECIMAL     NO-UNDO INITIAL 0.
DEFINE VARIABLE counter2         AS INTEGER     NO-UNDO INITIAL 0.
DEFINE VARIABLE depositpercent   AS DECIMAL     NO-UNDO INITIAL 0.
DEFINE VARIABLE primary-ota      AS LOGICAL     NO-UNDO INIT NO.    
DEFINE VARIABLE deposit-flag     AS LOGICAL     NO-UNDO INIT NO.    
DEFINE VARIABLE remark-flag      AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE rmrate-flag      AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE guest-flag       AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE taxes-flag       AS LOGICAL     NO-UNDO INIT NO.
DEFINE VARIABLE cc-email         AS CHARACTER.
DEFINE VARIABLE emailadr         AS CHARACTER NO-UNDO.
DEFINE VARIABLE email-username   AS CHARACTER NO-UNDO.
DEFINE VARIABLE email-password   AS CHARACTER NO-UNDO.
DEFINE VARIABLE email-server     AS CHARACTER NO-UNDO.
DEFINE VARIABLE email-port       AS INTEGER NO-UNDO.
DEFINE VARIABLE drive            AS CHARACTER NO-UNDO.
DEFINE VARIABLE drive-raw        AS CHARACTER NO-UNDO.
DEFINE VARIABLE versionInfo      AS CHAR FORMAT "X(80)" NO-UNDO.

/*Update Notice Night Audit 07-08-2023*/
DEFINE VARIABLE p-253           AS LOGICAL      NO-UNDO INIT NO. 
DEFINE VARIABLE txtfilefound    AS LOGICAL      NO-UNDO INITIAL NO.
DEFINE VARIABLE todays-date     AS CHAR         NO-UNDO INITIAL "".
DEFINE VARIABLE timestr         AS CHARACTER    NO-UNDO.
DEFINE VARIABLE txt-fpath       AS CHARACTER    NO-UNDO.
DEFINE VARIABLE cFileName       AS CHAR         NO-UNDO INITIAL "".
DEFINE VARIABLE ftime           AS INTEGER      NO-UNDO INITIAL 0.
DEFINE VARIABLE longbody        AS LONGCHAR     NO-UNDO INITIAL "".
DEFINE VARIABLE checktime       AS INTEGER      NO-UNDO INITIAL 0.
DEFINE VARIABLE currtime        AS INTEGER      NO-UNDO INITIAL 0.
DEFINE VARIABLE sendemailflag   AS LOGICAL      NO-UNDO INITIAL NO.

DEFINE STREAM dirlist.

/*************** DEFINE TEMP - TABLES ***************/
DEFINE TEMP-TABLE header-list
  FIELD vKey AS CHAR
  FIELD vValue AS CHAR.

/*DEF TEMP-TABLE rlist
    FIELD rcode AS CHAR.*/

DEF TEMP-TABLE t-pull-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0
.    

DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0
.

DEF TEMP-TABLE temp-list
    FIELD rcode  AS CHAR
    FIELD rmtype AS CHAR
    FIELD zikatnr AS INT
.

DEF TEMP-TABLE t-list
    FIELD autostart     AS LOGICAL
    FIELD period        AS INT
    FIELD delay         AS INT
    FIELD hotelcode     AS CHAR
    FIELD username      AS CHAR
    FIELD password      AS CHAR
    FIELD liveflag      AS LOGICAL
    FIELD defcurr       AS CHAR
    FIELD pushrateflag  AS LOGICAL
    FIELD pullbookflag  AS LOGICAL
    FIELD pushavailflag AS LOGICAL
    FIELD workpath      AS CHAR
    FIELD progavail     AS CHAR
.

DEF TEMP-TABLE r-list
    FIELD rcode AS CHAR.
DEF TEMP-TABLE rm-list
    FIELD rmtype AS CHAR.
DEF TEMP-TABLE logs-list
    FIELD rmtype AS CHAR
	FIELD logs AS CHAR.

DEFINE TEMP-TABLE push-allot-list
    FIELD startperiode AS DATE
    FIELD endperiode   AS DATE
    FIELD zikatnr      AS INT
    FIELD counter      AS INT
    FIELD rcode        AS CHAR
    FIELD bezeich      AS CHAR
    FIELD qty          AS INT
    FIELD flag         AS LOGICAL INIT YES
    FIELD str-date1    AS CHAR
    FIELD str-date2    AS CHAR
    FIELD minLOS       AS INT
    FIELD maxLOS       AS INT
    FIELD statnr       AS INT
    FIELD ota          AS CHAR
    FIELD bsetup       AS CHAR
    FIELD rmtype       AS CHAR
	INDEX mergeallot rcode ASC zikatnr ASC ota ASC startperiode ASC
.

DEFINE TEMP-TABLE push-rate-list
    FIELD startperiode AS DATE
    FIELD endperiode   AS DATE
    FIELD zikatnr      AS INT
    FIELD counter      AS INT
    FIELD rcode        AS CHAR
    FIELD bezeich      AS CHAR
    FIELD pax          AS INT
    FIELD child        AS INT
    FIELD rmrate       AS DECIMAL FORMAT ">>>,>>>,>>9.99"
    FIELD flag         AS LOGICAL INIT YES
    FIELD currency     AS CHAR
    FIELD scode        AS CHAR
	FIELD str-date1    AS CHAR
    FIELD str-date2    AS CHAR
	INDEX mergerate rcode ASC zikatnr ASC startperiode ASC
.
/*
DEFINE TEMP-TABLE push-rate-list LIKE rate-list
    FIELD str-date1    AS CHAR
    FIELD str-date2    AS CHAR.
*/
DEFINE TEMP-TABLE brate LIKE push-rate-list
    FIELD rmrate-str        AS CHAR
    FIELD pax-str           AS CHAR
    FIELD rmrate-child-str  AS CHAR
    FIELD child-str         AS CHAR.

DEFINE TEMP-TABLE room-list
    FIELD reslinnr  AS INTEGER
    FIELD res-id    AS CHARACTER
    FIELD ci-date   AS CHARACTER
    FIELD co-date   AS CHARACTER
    FIELD amount    AS CHARACTER
    FIELD room-type AS CHARACTER
    FIELD rate-code AS CHARACTER
    FIELD number    AS INTEGER
    FIELD adult     AS INTEGER
    FIELD child1    AS INTEGER
    FIELD child2    AS INTEGER
    FIELD service   AS CHARACTER
    FIELD gastnr    AS CHARACTER
    FIELD comment   AS CHARACTER
    FIELD argtnr    AS CHARACTER
    FIELD ankunft   AS DATE
    FIELD abreise   AS DATE
    FIELD zikatnr   AS INTEGER
    FIELD resstatus AS CHARACTER.

DEFINE TEMP-TABLE room-list1 
    FIELD reslinnr  LIKE room-list.reslinnr
    FIELD res-id    LIKE room-list.res-id
    FIELD ci-date   LIKE room-list.ci-date
    FIELD co-date   LIKE room-list.co-date
    FIELD amount    LIKE room-list.amount
    FIELD room-type LIKE room-list.room-type
    FIELD rate-code LIKE room-list.rate-code
    FIELD number    LIKE room-list.number
    FIELD adult     LIKE room-list.adult
    FIELD child1    LIKE room-list.child1
    FIELD child2    LIKE room-list.child2
    FIELD service   LIKE room-list.service
    FIELD gastnr    LIKE room-list.gastnr
    FIELD comment   LIKE room-list.comment
    FIELD argtnr    LIKE room-list.argtnr
    FIELD ankunft   LIKE room-list.ankunft
    FIELD abreise   LIKE room-list.abreise
    FIELD zikatnr   LIKE room-list.zikatnr.

DEFINE TEMP-TABLE service-list
    FIELD ci-date           AS CHARACTER
    FIELD co-date           AS CHARACTER
    FIELD res-id            AS CHARACTER
    FIELD amountaftertax    AS DECIMAL
    FIELD amountbeforetax   AS DECIMAL
    FIELD tamountaftertax   AS DECIMAL
    FIELD tamountbeforetax  AS DECIMAL
    FIELD bezeich           AS CHARACTER
    FIELD rph               AS CHARACTER
    FIELD id                AS CHARACTER
    FIELD curr              AS CHARACTER
    FIELD qty               AS INTEGER.
    

DEFINE TEMP-TABLE res-info
    FIELD res-time      AS CHARACTER
    FIELD res-id        AS CHARACTER
    FIELD ota-code      AS CHARACTER
    FIELD commission    AS CHARACTER
    FIELD curr          AS CHARACTER
    FIELD adult         AS CHARACTER
    FIELD child1        AS CHARACTER
    FIELD child2        AS CHARACTER
    FIELD remark        AS CHARACTER
    FIELD eta           AS CHARACTER
    FIELD given-name    AS CHARACTER
    FIELD sure-name     AS CHARACTER
    FIELD phone         AS CHARACTER
    FIELD email         AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD city          AS CHARACTER
    FIELD zip           AS CHARACTER
    FIELD state         AS CHARACTER
    FIELD country       AS CHARACTER
    FIELD uniq-id       AS CHARACTER
    FIELD res-status    AS CHARACTER /*Jason 29/07/16*/
    FIELD deposit       AS DECIMAL
    FIELD membership    AS CHARACTER /* membershipProgramName-membershipID */
    FIELD card-info     AS CHARACTER
    FIELD gastnrmember  AS INTEGER
    .

DEFINE TEMP-TABLE guest-list
    FIELD res-id        AS CHARACTER
    FIELD given-name    AS CHARACTER
    FIELD sure-name     AS CHARACTER
    FIELD phone         AS CHARACTER
    FIELD email         AS CHARACTER
    FIELD address1      AS CHARACTER
    FIELD address2      AS CHARACTER
    FIELD city          AS CHARACTER
    FIELD zip           AS CHARACTER
    FIELD state         AS CHARACTER
    FIELD country       AS CHARACTER
    FIELD gastnr        AS CHARACTER
    FIELD gastnrmember  AS INTEGER.

DEFINE TEMP-TABLE logs-allot LIKE push-allot-list.
DEFINE TEMP-TABLE service-list1 LIKE service-list.
DEFINE TEMP-TABLE guest-list1 LIKE guest-list.
DEFINE TEMP-TABLE buffroom LIKE room-list.

DEFINE TEMP-TABLE detRes
    FIELD reslinnr          AS INTEGER
    FIELD amount            AS CHARACTER
    FIELD amountbeforetax   AS CHARACTER
    FIELD base-flag         AS LOGICAL
    FIELD adult             AS INT
    FIELD child1            AS INT
    FIELD child2            AS INT
    FIELD room-type         AS CHARACTER
    FIELD rate-code         AS CHARACTER
    FIELD argtnr            AS CHARACTER
    FIELD ci-date           AS DATE
    FIELD co-date           AS DATE
    FIELD night             AS INT
    FIELD firstname         AS CHARACTER
    FIELD lastname          AS CHARACTER
    FIELD SELECTED          AS LOGICAL
    FIELD uniq-id           AS CHARACTER
    FIELD zikatnr           AS INTEGER
    FIELD gastnrmember      AS INTEGER.

DEFINE TEMP-TABLE t-fixleist
    FIELD uniq-id         AS CHARACTER
    FIELD bezeich         AS CHARACTER    
    FIELD serviceRPH      AS INTEGER
    FIELD qty             AS INTEGER
    FIELD amountaftertax  AS DECIMAL
    FIELD amountbeforetax AS DECIMAL
    FIELD start-date      AS DATE 
    FIELD end-date        AS DATE.

DEFINE TEMP-TABLE map-list
    FIELD rmtypeVHP     AS CHARACTER
    FIELD rmtypeSM      AS CHARACTER
    FIELD ratecdVHP     AS CHARACTER
    FIELD ratecdSM      AS CHARACTER
    FIELD argtnr        AS CHARACTER
    FIELD adult         AS INTEGER  INIT 1
    FIELD child         AS INTEGER  INIT 0.

DEFINE TEMP-TABLE map-list-push LIKE map-list.
DEFINE TEMP-TABLE map-list-pull LIKE map-list.

DEFINE TEMP-TABLE temp-res      LIKE res-info.
DEFINE TEMP-TABLE temp-detres   LIKE detRes.

DEFINE BUFFER b-map         FOR map-list.
DEFINE BUFFER b-map-pull    FOR map-list-pull.
DEFINE BUFFER b-map-push    FOR map-list-push.

DEFINE TEMP-TABLE error-tax
    FIELD uniq-id       AS CHARACTER.

DEFINE TEMP-TABLE brs-data
    FIELD hotelid       AS CHARACTER
    FIELD res-status    AS CHARACTER
    FIELD res-id        AS CHARACTER
    FIELD ota-code      AS CHARACTER
    FIELD roomrate      AS DECIMAL
    FIELD createdate    AS DATE
    FIELD cidate        AS DATE
    FIELD codate        AS DATE
    FIELD firstname     AS CHAR
    FIELD lastname      AS CHAR.

DEFINE TEMP-TABLE hotel 
    FIELD number        AS INTEGER
    FIELD Name          AS CHARACTER
    FIELD License       AS INTEGER
    FIELD htlcode       AS CHARACTER
    FIELD IP            AS CHARACTER
    FIELD Port          AS CHARACTER
    FIELD BECode        AS INTEGER
    FIELD grp           AS INTEGER 
    FIELD exdata        AS INTEGER
    FIELD rms           AS INTEGER  /* dipakai sebagai informasi voidarticlenumber untuk ABI */
    FIELD BECodeRMS     AS INTEGER
    FIELD pushall       AS LOGICAL INIT NO
    FIELD errorcounter  AS INTEGER INIT 0
    FIELD rsvcounter    AS INTEGER INIT 0
    FIELD availcounter  AS INTEGER INIT 0
    FIELD ratecounter   AS INTEGER INIT 0
    FIELD pushbookcounter AS INTEGER INIT 0
    FIELD notifcounter  AS INTEGER INIT 0
    FIELD defemail      AS CHARACTER
    FIELD abi           AS LOGICAL
    FIELD activeflag    AS LOGICAL
    .
DEFINE TEMP-TABLE hotel-list NO-UNDO
    FIELD nr               AS INT
    FIELD benum            AS INT 
    FIELD hotelname        AS CHAR
    FIELD license          AS INT
    FIELD hotelcode        AS CHAR
    FIELD ip               AS CHAR  
    FIELD port             AS CHAR  
    FIELD becode           AS INT 
    FIELD grp              AS INT 
    FIELD exdata           AS INT 
    FIELD rms              AS INT 
    FIELD becoderms        AS INT 
    FIELD pushall          AS LOGICAL  
    FIELD errorcounter     AS INT 
    FIELD rsvcounter       AS INT 
    FIELD availcounter     AS INT 
    FIELD ratecounter      AS INT 
    FIELD pushbookcounter  AS INT 
    FIELD notifcounter     AS INT 
    FIELD defemail         AS CHAR  
    FIELD abi              AS LOGICAL  
    FIELD rsv-char         AS CHAR EXTENT 10
    FIELD rsv-int          AS INT EXTENT 10
    FIELD rsv-dec          AS DECIMAL EXTENT 10
    FIELD rsv-date         AS DATE EXTENT 10
    FIELD recnr            AS INT FORMAT ">>>>" LABEL "No"
    FIELD xmlnr            AS INT FORMAT ">>>>" LABEL "XMLNo"
    FIELD hotel-name       AS CHARACTER FORMAT "x(40)" LABEL "Hotel Name"
    FIELD hotel-ip         AS CHARACTER FORMAT "x(25)" LABEL "IP"
    FIELD hotel-port       AS CHARACTER FORMAT "x(6)"  LABEL "Port"
    FIELD be-group         AS INT
    FIELD active-flag      AS LOGICAL
    .
DEFINE TEMP-TABLE raw-file
    FIELD filenm AS CHAR FORMAT "x(22)"
    FIELD filepath AS CHAR
    FIELD filedate AS DATE
    FIELD filetime AS INT.
	
DEFINE TEMP-TABLE preference-list
  FIELD email           AS CHAR FORMAT "x(50)" 
  FIELD pass            AS CHAR FORMAT "x(50)" 
  FIELD email-server    AS CHAR FORMAT "x(50)" 
  FIELD email-port      AS INT  FORMAT ">,>>9" 
  FIELD hdesk-host      AS CHAR FORMAT "x(50)"
  FIELD hdesk-port      AS INT  FORMAT ">,>>9" 
  FIELD BECode          AS INT  FORMAT ">,>>9"
  FIELD Ctr-logs-path   AS CHAR FORMAT "x(50)" /* BLY 04/06/2025 */
  .

DEFINE TEMP-TABLE notif-list
    FIELD cmid AS CHAR
    FIELD otaid AS CHAR.

DEFINE NEW SHARED VARIABLE debug-on     AS LOGICAL  INITIAL NO.
DEFINE NEW SHARED VARIABLE minSize      AS LOGICAL  INITIAL NO.
DEFINE NEW SHARED VARIABLE autostart    AS LOGICAL  INITIAL NO.
DEFINE NEW SHARED VARIABLE alertbox     AS LOGICAL  INITIAL NO.
DEFINE NEW SHARED VARIABLE chDelimeter  AS CHAR     INITIAL "," NO-UNDO.
DEFINE NEW SHARED VARIABLE chDelimeter1 AS CHAR     INITIAL ":" NO-UNDO.
DEFINE NEW SHARED VARIABLE chDelimeter2 AS CHAR     INITIAL ";" NO-UNDO.
DEFINE NEW SHARED VARIABLE chDelimeter3 AS CHAR     INITIAL "[newline]" NO-UNDO.
DEFINE NEW SHARED VARIABLE user-init    AS CHAR.
DEFINE NEW SHARED VARIABLE product-name AS CHAR.                   
DEFINE NEW SHARED VARIABLE htl-no       AS CHAR     INITIAL "".
DEFINE VARIABLE tot-rec                 AS INTEGER  INITIAL 0   NO-UNDO.
DEFINE VARIABLE message1                AS CHAR FORMAT "x(256)"  EXTENT 12
    VIEW-AS FILL-IN SIZE 86 BY .88 BGCOLOR 15 NO-UNDO FONT 1.
DEFINE VARIABLE fr-title                AS CHAR     NO-UNDO.
DEFINE STREAM lStream.


/***************************DEFINE BUTTONS******************************/
DEFINE BUTTON btn-start  LABEL "START" SIZE 15 BY 1.15 FONT 1.
DEFINE BUTTON btn-exit   LABEL "EXIT"  SIZE 15 BY 1.15 FONT 1.

/************************SET VARIABLES*******************************/
chDelimeter = CHR(2).
chDelimeter1 = CHR(4).
chDelimeter2 = CHR(3).

/*************** DEFINE FRAME ***************/
DEFINE FRAME frame1
    message1[1]    AT ROW 2.31 COL 3 COLON-ALIGNED NO-LABEL
    message1[2]    AT ROW 3.38 COL 3 COLON-ALIGNED NO-LABEL
    message1[3]    AT ROW 4.46 COL 3 COLON-ALIGNED NO-LABEL
    message1[4]    AT ROW 5.54 COL 3 COLON-ALIGNED NO-LABEL
    message1[5]    AT ROW 6.62 COL 3 COLON-ALIGNED NO-LABEL
    message1[6]    AT ROW 7.69 COL 3 COLON-ALIGNED NO-LABEL
    message1[7]    AT ROW 8.77 COL 3 COLON-ALIGNED NO-LABEL
    message1[8]    AT ROW 9.85 COL 3 COLON-ALIGNED NO-LABEL
    message1[9]    AT ROW 10.92 COL 3 COLON-ALIGNED NO-LABEL
    message1[10]   AT ROW 12    COL 3 COLON-ALIGNED NO-LABEL
    message1[11]   AT ROW 13.08 COL 3 COLON-ALIGNED NO-LABEL
    message1[12]   AT ROW 14.15 COL 3 COLON-ALIGNED NO-LABEL

    btn-start      AT ROW 16.5 COL 28 
    btn-exit       AT ROW 16.5 COL 48 
    SPACE(41.71) SKIP(0.64)

    WITH SIDE-LABELS CENTERED WIDTH 95 OVERLAY THREE-D
    VIEW-AS DIALOG-BOX KEEP-TAB-ORDER TITLE fr-title
    BGCOL 61 DEFAULT-BUTTON btn-exit.
                               
/*************** DEFINE TRIGGERS ***************/
ON 'choose':U OF btn-start
DO:
    DEF VAR sm-con       AS LOGICAL INIT NO.
    DEF VAR push-created AS LOGICAL INIT NO.
    DEF VAR parameters   AS CHAR.
    DEF VAR flag-connect AS INT NO-UNDO.
    DEF VAR inet-connect AS CHAR.
    DEF VAR repeat-flag  AS LOGICAL INIT ? NO-UNDO.
    DEF VAR counter      AS INT INIT 0.
    DEF VAR counter-rate AS INT INIT 0.
    DEF VAR lReturn      AS LOGICAL.
    DEF VAR done-avail   AS LOGICAL INIT NO.
    DEF VAR done-rate    AS LOGICAL INIT NO.
    DEF VAR do-it        AS LOGICAL INIT NO.
    DEF VAR inp-str      AS CHAR.
    DEF VAR version-msg  AS CHAR.
    DEF VAR starttime    AS INT INIT 0.
    DEF VAR time1        AS INT INIT 0.
    DEF VAR diff         AS INT INIT 0.
    DEF VAR deleted-row  AS INT INIT 0.
    DEF VAR ci-date      AS DATE.
    PROCESS EVENTS.
    
    version-msg = "v2.7.6 05/11/2025 (" + STRING(grp) + ") ".
/*2.7.4 me-remove logs-alot ganti logs-list*/
/*2.7.5 reposition logs-list, etc for optimation push rate and push avail procedure*/
/*2.7.6 fix xml empty push-allot-list & rates */
    IF MinSize THEN
    DO:
        HIDE FRAME frame1 NO-PAUSE.
        ASSIGN CURRENT-WINDOW:WINDOW-STATE = 2
               CURRENT-WINDOW:SENSITIVE    = FALSE.
    END.
    ELSE
    DO:
        btn-exit:TOOLTIP = "Press CTRL-ALT-DEL to stop".
        FRAME frame1:TITLE = "VHP-CM Interface " + version-msg + "(Status Running)".
        HIDE btn-start.
    END.
    
    versionInfo = "@(#) if-cmUI.p CRG " + version-msg.
    RUN logmess(versionInfo).

    PROCESS EVENTS.
    
    /*Task*/
    starttime = TIME.
    flag-connect = 0.
    

    REPEAT:
        time1 = TIME.
        FOR EACH hotel WHERE hotel.becode NE 0 AND hotel.grp = grp NO-LOCK BY hotel.number:
            CREATE SERVER hServer.
            ASSIGN
                lReturn = NO
                repeat-flag = NO.

            IF hotelfile THEN /*centralized*/
            DO:
                workpath = drive + logpath + hotel.htlcode + "\".
                IF SEARCH(workpath) EQ ? THEN
                    OS-COMMAND SILENT VALUE("mkdir " + workpath).
                /*RUN logmess("Connect to " + hotel.NAME + " " + hotel.htlcode + "(" + STRING(hotel.number) + ") from Group-" + STRING(hotel.grp) + "(" + hotel.IP + ":" + hotel.Port + ")" ). /*20/03/2025*/ /*NC - 08/04/25 onpremise also needs this logs*/ */
            END.
            /*ELSE on premise
            DO:*/ /*NC - 08/04/25 */
                RUN logmess("Connect to " + STRING(hotel.number) + ". " + hotel.NAME + "(" + hotel.htlcode + ")" + " becode(" + STRING(hotel.BECode) + ") from Group-" + STRING(hotel.grp) + "(" + hotel.IP + ":" + hotel.Port + ")" ). 
            /*END.*/
            
            RUN connect-hserver(hotel.ip, hotel.port, OUTPUT lReturn).
            IF lReturn THEN
            DO:
                /* RUN logmess("Connected to " + hotel.NAME). */
                IF debugging-flag = "YES" THEN
                DO:
                    RUN logmess("Debugging Mode ON for " + hotel.NAME).
                END.

				EMPTY TEMP-TABLE t-pull-list.
				EMPTY TEMP-TABLE t-push-list.
				EMPTY TEMP-TABLE t-list.
                EMPTY TEMP-TABLE brs-data.

                RUN if-siteminder-chk-repeatflagbl.p ON hServer(OUTPUT repeat-flag).
                IF repeat-flag THEN
                    RUN logmess("Re-Setup your Configuration.." + "-" + hotel.NAME).
               /* RUN logmess("Prepare Configuration..."). */ /**/
                /*should use BL version which frDate = TODAY.*/
				RUN prepare-if-siteminderbl.p
					ON hServer(hotel.becode, OUTPUT frDate, OUTPUT toDate, OUTPUT htl-no,
							OUTPUT TABLE t-pull-list, OUTPUT TABLE t-push-list,
					        OUTPUT TABLE t-list).
                RUN read-temp-table(OUTPUT do-it).
                IF do-it THEN
                DO:
                    IF hotelfile THEN
                    DO:
                        IF hotel.pushall THEN
						DO:
                            pushAll = YES. 
							RUN logmess("Push All from hdesk config" + "-" + hotel.NAME).
						END.
                    
                        ASSIGN
                            sm-con = NO
                            workpath = drive + logpath + hotel.htlcode + "\".
                    END.
    
                    inp-str = STRING(pushAll) + "=" + STRING(re-calculate) + "=" + STRING(allotment) + "=" + STRING(bedSetup).
    
                    /*IF NOT sm-con THEN
                        RUN connect-sm(OUTPUT sm-con).
                               
                    IF NOT sm-con THEN RUN logmess("Failed connecting to Channel Manager").
                    ELSE IF sm-con THEN*/
                    DO:
                        EMPTY TEMP-TABLE temp-list.
                        FOR EACH t-push-list WHERE t-push-list.rcodeBE NE "" AND t-push-list.rmtypeBE NE "" NO-LOCK:
                            CREATE temp-list.
                            ASSIGN
                                temp-list.rcode = t-push-list.rcodeVHP
                                temp-list.rmtype = t-push-list.rmtypeVHP
                            .
                        END.

                        IF comboflag = YES OR readaricomboflag = YES THEN
                        DO:
                            IF SEARCH("C:\e1-vhp\radiantone\") EQ ? THEN
                                OS-COMMAND SILENT VALUE("mkdir C:\e1-vhp\radiantone\").
                        END.

                        IF readaricomboflag = YES THEN
                        DO:
                            allotfile = "".
                            ratefile = "".
                            allotflag = YES.
                            rateflag = YES.
                            EMPTY TEMP-TABLE raw-file.
                            rDir = "C:\e1-vhp\radiantone\".
                            INPUT FROM OS-DIR (rDir) ECHO.
                            REPEAT: 
                                CREATE raw-file.
                                IMPORT raw-file.filenm.
                                FILE-INFO:FILE-NAME = rDir + raw-file.filenm.
                                IF FILE-INFO:FILE-NAME BEGINS rdir + REPLACE(hotel.ip,".","") + hotel.port THEN
                                    ASSIGN
                                        raw-file.filepath = FILE-INFO:FULL-PATHNAME
                                        raw-file.filedate = FILE-INFO:FILE-MOD-DATE
                                        raw-file.filetime = FILE-INFO:FILE-MOD-TIME.          
                            END.
                            FOR EACH raw-file WHERE raw-file.filenm MATCHES "*allotlist*" BY raw-file.filedate BY raw-file.filetime:
                                allotfile = raw-file.filepath.
                                LEAVE.
                            END.
                            FOR EACH raw-file WHERE raw-file.filenm MATCHES "*ratelist*" BY raw-file.filedate BY raw-file.filetime:
                                ratefile = raw-file.filepath.
                                LEAVE.
                            END.
                            FOR EACH raw-file WHERE raw-file.filenm MATCHES "*allotflag*" BY raw-file.filedate BY raw-file.filetime:
                                allotflag = NO.
                                LEAVE.
                            END.
                            FOR EACH raw-file WHERE raw-file.filenm MATCHES "*rateflag*" BY raw-file.filedate BY raw-file.filetime:
                                rateflag = NO.
                                LEAVE.
                            END.
                        END.
    
                        /*FILE-INFO:FILE-NAME = 'C:\chksvc'.
                        IF FILE-INFO:FULL-PATHNAME <> ? THEN  NC - not use anymore*/
    					
                        /* read from RAW folder if reading manual xml for ABI (CRG 28/03/2022) */
                        IF abi-readmanual-flag = "YES" THEN
                        DO:
                            RUN logmess("Reading Reservation Manually from RAW folder for ABI database.").
                            RUN pull-rsv2.
                        END.
                        ELSE
                        DO:
                            /*PULL METHOD*/
                            IF cPullBook THEN
                            DO:
                                echotoken = "".
                                ASSIGN
                                    uuid = GENERATE-UUID
                                    echotoken = GUID(uuid).
                                RUN logmess("Retrieve reservation.. [Token : " + echotoken + "]").
                                RUN pull-rsv.
                            END.
        					ELSE IF NOT cPullBook AND cPushBook THEN /*PUSH METHOD*/
        					DO:
                                RUN logmess("Checking reservation..").
                                RUN pull-rsv2.
                            END.
        
                            done-avail = NO.
                            /*Update Notice Night Audit 16-08-2023*/
                            RUN htplogic.p ON hServer(253, OUTPUT p-253).   /* check night audit still running or not */
                            IF p-253 THEN
                            DO:
                                RUN logmess("Night Audit is running, ARI Updates are being processed...").
                                IF emailadr NE "" THEN
                                    RUN send-email("NightAudit", "", htl-code, ""). /*22/01/2025*/ /* NC- 14/04/2025 change to 4 input parameters*/
                                ELSE
                                    RUN logmess("Email not sent due to email address not defined (" + STRING(hotel.license) + ")").
                            END.
            
                            /*IF NOT p-253 THEN
                            DO:*/
                            IF cUpdAvail THEN
                            DO:
                                EMPTY TEMP-TABLE push-allot-list.
                                RUN logmess("Calculating availability..").
    
                                IF readaricomboflag = NO OR allotflag = NO THEN
                                DO:
                                    IF NOT incl-tentative THEN
                                        RUN if-vhp-bookeng-push-availbl.p ON hServer
                                        (cPushRate,inp-str,frdate,todate,hotel.becode,TABLE temp-list,OUTPUT done-avail,
                                         OUTPUT TABLE push-allot-list).
                                    ELSE
                                        RUN if-vhp-bookeng-push-availxbl.p ON hServer
                                        (cPushRate,inp-str,frdate,todate,hotel.becode,TABLE temp-list,OUTPUT done-avail,
                                         OUTPUT TABLE push-allot-list).
                                END.
                                ELSE
                                DO:
                                    done-avail = YES.
                                    IF allotfile NE "" THEN
                                        TEMP-TABLE push-allot-list:READ-JSON("file", allotfile, "empty").
                                END.
        
                                FOR EACH push-allot-list WHERE push-allot-list.startperiode LT frdate OR push-allot-list.endperiode GT todate:
                                    DELETE push-allot-list.
                                END.
    
                                FOR EACH push-allot-list WHERE push-allot-list.qty LT 0:
                                    ASSIGN push-allot-list.qty = 0.
                                END.
                                
                                FIND FIRST push-allot-list NO-LOCK NO-ERROR.
                                IF NOT AVAILABLE push-allot-list THEN 
                                DO:
                                    RUN logmess("No updated availability.").
                                    IF readaricomboflag = YES AND allotfile NE "" THEN 
                                        DOS SILENT VALUE("DEL " + allotfile).
									IF hotel.availcounter NE 0 THEN RUN update-xml("avail", "reset").
                                END.
                                ELSE 
                                DO:
                                    /* output json temp-table request ayung ubud - IF Radiant1 (CRG 24/07/2023) */
                                    IF comboflag = YES THEN
                                    DO:
                                        TEMP-TABLE push-allot-list:WRITE-JSON("longchar",json-str,TRUE).
                                        json-file = "C:\e1-vhp\radiantone\" + REPLACE(hotel.ip,".","") + hotel.port + "_allotlist_" + REPLACE(STRING(TODAY),"/","") + "_" + STRING(TIME) + "_" + STRING(hotel.license) + ".json".
                                        COPY-LOB json-str TO FILE json-file.
                                        json-file = "C:\e1-vhp\radiantone\" + REPLACE(hotel.ip,".","") + hotel.port + "_allotflag.json".
                                        IF SEARCH(json-file) NE ? THEN
                                            DOS SILENT VALUE("DEL " + json-file).
                                    END.

                                    FIND FIRST temp-list NO-LOCK NO-ERROR.
                                    IF AVAILABLE temp-list THEN
                                    DO:
                                        deleted-row = 0.
                                        FOR EACH push-allot-list:
                                            FIND FIRST temp-list WHERE temp-list.rcode = push-allot-list.rcode AND temp-list.rmtype = push-allot-list.bezeich NO-LOCK NO-ERROR.
                                            IF NOT AVAILABLE temp-list THEN
                                            DO:
                                                /*NC -07/12/21*/
                                                /*timestr = STRING(TIME,"HH:MM:SS").
                                                RUN logmess(timestr + " Deleted availability not mapped.. details : date=" + STRING(push-allot-list.startperiode) + " RC=" + push-allot-list.rcode + " RT="+ push-allot-list.bezeich + " qty=" + STRING(push-allot-list.qty)).*/
                                                DELETE push-allot-list.
                                                deleted-row = deleted-row + 1.
                                            END.
                                        END.
                                        IF deleted-row GT 0 THEN
                                            RUN logmess("Deleted Availability Not Mapped = " + STRING(deleted-row) + " Rows").
                                    END.
    
                                    RUN logmess("Updating availability..").
                                    RUN push-allotment.
                                END.
                            END.
                            ELSE
                            DO:
                                IF comboflag = YES THEN
                                DO:
                                    json-str = "-".
                                    json-file = "C:\e1-vhp\radiantone\" + REPLACE(hotel.ip,".","") + hotel.port + "_allotflag.json".
                                    COPY-LOB json-str TO FILE json-file.
                                END.
                            END.
            
                            IF cPushRate THEN
                            DO:
                                EMPTY TEMP-TABLE push-rate-list.
                                EMPTY TEMP-TABLE brate.
                                counter-rate = 1.
                                
                                RUN logmess("Calculating room rates..").
                                IF NOT cUpdAvail THEN 
                                DO:
                                    IF readaricomboflag = NO OR allotflag = NO THEN
                                    DO:
                                        IF NOT incl-tentative THEN
                                            RUN if-vhp-bookeng-push-availbl.p ON hServer
                                            (cPushRate,inp-str,frdate,todate,hotel.becode,TABLE temp-list,OUTPUT done-avail,
                                             OUTPUT TABLE push-allot-list).
                                        ELSE
                                            RUN if-vhp-bookeng-push-availxbl.p ON hServer
                                            (cPushRate,inp-str,frdate,todate,hotel.becode,TABLE temp-list,OUTPUT done-avail,
                                             OUTPUT TABLE push-allot-list).
                                    END.
                                    ELSE done-avail = YES.
                                END.
    
                                IF done-avail THEN
                                DO:
                                    IF readaricomboflag = NO OR rateflag = NO THEN
                                    DO:
                                        IF NOT incl-tentative THEN
                                            RUN if-vhp-bookeng-push-ratebl.p ON hServer
                                                (inp-str,counter-rate,pushpax,frdate,todate,maxAdult, maxChild,hotel.becode,
                                                TABLE temp-list,OUTPUT done-rate,OUTPUT TABLE push-rate-list).
                                        ELSE
                                            RUN if-vhp-bookeng-push-ratexbl.p ON hServer
                                                (inp-str,counter-rate,pushpax,frdate,todate,maxAdult, maxChild,hotel.becode,
                                                TABLE temp-list,OUTPUT done-rate,OUTPUT TABLE push-rate-list).
                                    END.
                                    ELSE
                                    DO:
                                        IF ratefile NE "" THEN
                                            TEMP-TABLE push-rate-list:READ-JSON("file", ratefile, "empty").
                                    END.
                                END.
        
                                FOR EACH push-rate-list WHERE push-rate-list.startperiode LT frdate OR push-rate-list.endperiode GT todate:
                                    DELETE push-rate-list.
                                END.
                                
                                FIND FIRST push-rate-list NO-LOCK NO-ERROR.
                                IF NOT AVAILABLE push-rate-list THEN 
                                DO:
                                    RUN logmess("No updated rates.").
                                    IF readaricomboflag = YES AND ratefile NE "" THEN
                                        DOS SILENT VALUE("DEL " + ratefile).
									IF hotel.ratecounter NE 0 THEN RUN update-xml("rate", "reset"). /*NC - reset hotel.ratecounter*/
                                END.
                                ELSE 
                                DO:
                                    /* output json temp-table request ayung ubud - IF Radiant1 (CRG 24/07/2023) */
                                    IF comboflag = YES THEN
                                    DO:
                                        TEMP-TABLE push-rate-list:WRITE-JSON("longchar",json-str,TRUE).
                                        json-file = "C:\e1-vhp\radiantone\" + REPLACE(hotel.ip,".","") + hotel.port + "_ratelist_" + REPLACE(STRING(TODAY),"/","") + "_" + STRING(TIME) + "_" + STRING(hotel.license) + ".json".
                                        COPY-LOB json-str TO FILE json-file.
                                        json-file = "C:\e1-vhp\radiantone\" + REPLACE(hotel.ip,".","") + hotel.port + "_rateflag.json".
                                        IF SEARCH(json-file) NE ? THEN
                                            DOS SILENT VALUE("DEL " + json-file).
                                    END.

                                    FIND FIRST temp-list NO-LOCK NO-ERROR.
                                    IF AVAILABLE temp-list THEN
                                    DO:
                                        deleted-row = 0.
                                        FOR EACH push-rate-list:
                                            FIND FIRST temp-list WHERE temp-list.rcode = push-rate-list.rcode AND temp-list.rmtype = push-rate-list.bezeich NO-LOCK NO-ERROR.
                                            IF NOT AVAILABLE temp-list THEN
                                            DO:
                                                /*timestr = STRING(TIME,"HH:MM:SS").
                                                RUN logmess(timestr + " Deleted rates not mapped details : date=" + STRING(push-rate-list.startperiode) + " AM=" + STRING(push-rate-list.rmRate) + " RC=" + push-rate-list.rcode + " RT=" + push-rate-list.bezeich).*/
                                                DELETE push-rate-list.
                                                deleted-row = deleted-row + 1.
                                            END.
                                        END.
                                        IF deleted-row GT 0 THEN
                                            RUN logmess("Deleted Rates Not Mapped = " + STRING(deleted-row) + " Rows").
                                    END.
    
                                    RUN logmess("Updating room rates..").
                                    RUN push-rate.
                                END.
                            END.
                            ELSE
                            DO:
                                IF comboflag = YES THEN
                                DO:
                                    json-str = "-".
                                    json-file = "C:\e1-vhp\radiantone\" + REPLACE(hotel.ip,".","") + hotel.port + "_rateflag.json".
                                    COPY-LOB json-str TO FILE json-file.
                                END.
                            END.
                            /*END. /*End of p-253 = yes*/*/
                            /*ELSE /* p-253 if yes validation */
                            DO:
                                IF cUpdAvail OR cPushRate THEN /* to make sure inv-updates are selected */
                                DO:
                                    txtfilefound = NO.
                                    todays-date = REPLACE(STRING(TODAY), "/", "").
                                    timestr = STRING(TIME,"HH:MM:SS").

                                    txt-fpath = workpath + "debug" + STRING(MONTH(TODAY)) + "\" + "NTFLAG_" + todays-date + "_" + 
                                                STRING(TIME) + "_" + STRING(hotel.license) + "_" + "START" + ".txt".

                                    INPUT STREAM dirlist FROM OS-DIR(workpath + "debug" + STRING(MONTH(TODAY)) + "\").
                                    REPEAT:
                                        IMPORT STREAM dirlist cFileName.

                                        IF INDEX(cFILENAME,".txt") NE 0 AND cFileName MATCHES "*NTFLAG*" AND ENTRY(2, cFileName, "_") = todays-date 
                                            AND ENTRY(4, cFileName, "_") = STRING(hotel.license) THEN
                                        DO:
                                            ASSIGN
                                                ftime = INT(ENTRY(3, cFileName, "_"))
                                                txtfilefound = YES.
                                            LEAVE.
                                        END.
                                
                                        IF txtfilefound = YES THEN
                                            LEAVE.
                                    END.
                                    INPUT CLOSE.

                                    IF txtfilefound = NO THEN
                                    DO:
                                        longbody = "".
                                        COPY-LOB longbody TO FILE txt-fpath.
                                    END.

                                    checktime = TIME.
                                    IF checktime LT ftime THEN
                                        currtime = 86400 - ftime + checktime.
                                    ELSE
                                    DO:
                                        IF txtfilefound = YES THEN
                                            currtime = checktime - ftime.
                                        ELSE
                                            currtime = 0.
                                    END.

                                    IF currtime GT 3600 THEN
                                        sendemailflag = YES.
                                    ELSE sendemailflag = NO.

                                    RUN logmess(timestr + " Night Audit is running, ARI Update Skipped (" + STRING(currtime) + " seconds)").
                                    IF sendemailflag = YES THEN
                                    DO:
                                        IF emailadr NE "" THEN
                                            RUN send-email("NightAudit", "", htl-code, ""). /*22/01/2025*/
                                        ELSE
                                            RUN logmess(timestr + " Email not sent due to email address not defined (" + STRING(hotel.license) + ")").
                                    END.
                                END.
                            END. /* end of p-253 = NO */*/
                        END.

                        IF hotelfile AND hotel.pushall = YES THEN
                            RUN update-xml("pushall", "").
                    END.
                END.
            END. /* end if lreturn */
            ELSE RUN logmess("Can not connect to " + hotel.NAME).

            hServer:DISCONNECT() NO-ERROR.

            /* connect ke database ABI untuk input AR & AP (Artotel Booking Indonesia) hanya untuk hotel yang under Artotel Group dan e1-booking  CRG 18/03/2022 */
            IF hotel.abi = YES THEN
            DO:
                lReturn = NO.
                RUN connect-hserver-artotel(OUTPUT lReturn).
                IF lReturn THEN
                DO:
                    DEFINE VARIABLE syserror-flag AS LOGICAL.
                    DEFINE VARIABLE errmsg AS CHARACTER.
                    DEFINE VARIABLE inptype AS CHARACTER.
                    DEFINE VARIABLE success-flag AS LOGICAL.
                    DEFINE VARIABLE refno AS CHAR.
                
                    FOR EACH brs-data:
                        DO TRANSACTION:
                            syserror-flag = NO.
                            success-flag = NO.
                            errmsg = "".
                            refno = brs-data.hotelid + ";" + brs-data.ota-code.

                            IF brs-data.res-status = "Reserved" THEN inptype = "New".
                            ELSE IF brs-data.res-status = "Modify" THEN inptype = "Modify".
                            ELSE IF brs-data.res-status = "Cancel" THEN inptype = "Cancel".
                
                            RUN if-d-edge-brs-create-entrybl.p ON hServer (inptype, brs-data.createdate, refno, "", 
                                   brs-data.roomrate, 0, "", brs-data.res-id, hotel.rms, 
                                   brs-data.cidate, brs-data.codate, brs-data.firstname, brs-data.lastname,
                                   OUTPUT success-flag, OUTPUT errmsg).
                    
                            CATCH plsErr AS Progress.Lang.SysError.
                                DO i = 1 TO plsErr:NumMessages:
                                    RUN logmess (plsErr:GetMessage(i)).
                                    syserror-flag = YES.
                                END.
                            END CATCH.
                        END.
                
                        IF errmsg NE "" THEN
                            RUN logmess(errmsg).
                
                        IF syserror-flag = NO AND success-flag = YES THEN
                        DO:
                            IF inptype = "New" THEN
                                RUN logmess(brs-data.res-id + " entry in ABI Created for " + STRING(TODAY)).
                            IF inptype = "Modify" THEN
                                RUN logmess(brs-data.res-id + " entry in ABI Modified for " + STRING(TODAY)).
                            ELSE IF inptype = "Cancel" THEN
                                RUN logmess(brs-data.res-id + " entry in ABI Cancelled for " + STRING(TODAY)).
                        END.
                    END.

                END.
            END.

            hServer:DISCONNECT() NO-ERROR.
            DELETE OBJECT hServer NO-ERROR.
			IF DAY(frdate) = 1 AND hotelfile THEN
			DO:                    
				IF MONTH(frdate) - 2 = -1 THEN
					del-folder = 11.
				ELSE IF MONTH(frdate) - 2 = 0 THEN
					del-folder = 12.
				ELSE del-folder = MONTH(frdate) - 2.
				dirname = drive + logpath + hotel.htlcode + "\debug" + STRING(del-folder) + "\".
			END.
            ELSE IF DAY(frdate) = 1 AND NOT hotelfile THEN
            DO:                    
                IF MONTH(frdate) - 6 LE 0 THEN
                    del-folder = MONTH(frdate) - 6 + 12.
                ELSE del-folder = MONTH(frdate) - 6.
				dirname = drive + logpath + "debug" + STRING(del-folder) + "\".
            END.
			
			DOS SILENT VALUE ("DEL " + dirname + "*.xml").
			/*DOS SILENT VALUE ("DEL " + dirname + "*.log"). do not delete the logfile*/
			DOS SILENT VALUE ("DEL " + dirname + "*.txt").

            PAUSE pauseinterval.
        END. /*end for each hotel*/
        
        ASSIGN
            diff = TIME - time1
            counter = counter + 1.

        IF TIME - starttime GE restartinterval OR TIME - starttime LT 0 THEN
        DO:
			RUN logmess("Performing Scheduled Restart..."). /* NC - 08/04/25*/
            IF SEARCH(drive + logpath + "vhplib\" + restartscheduler) NE ? THEN
            DO:
				schedulerpath = drive + logpath + "vhplib\" + restartscheduler. /*NC - 10/07/25*/
				RUN logmess("Run scheduller file on " + schedulerpath ).
                /*OS-COMMAND SILENT VALUE(drive + logpath + "vhplib\" + restartscheduler).*/ /*NC - 10/07/25*/
				OS-COMMAND SILENT VALUE(schedulerpath) NO-WAIT. /*#F37323*/
            END.
            ELSE IF SEARCH(drive + logpath + restartscheduler) NE ? THEN
			DO:
				schedulerpath = drive + logpath + restartscheduler. /*NC - 10/07/25*/
				RUN logmess("Run scheduller file on " + schedulerpath ).
				/*OS-COMMAND SILENT VALUE(drive + logpath + restartscheduler).*/ /*NC - 10/07/25*/
				OS-COMMAND SILENT VALUE(schedulerpath) NO-WAIT. /*#F37323*/
			END.
			ELSE DO:
				RUN logmess("Batch file not found!").
				RUN logmess("Restart Required").
			END.
        END.

        IF diff LE delayfrompf AND diff GT 0 THEN delay = delayfrompf - diff.
            ELSE delay = 0.

        PAUSE delay.
    END.
END.

ON 'choose':U OF btn-exit
DO:
    DEF VAR answer AS LOGICAL   NO-UNDO INITIAL NO.
    
    HIDE MESSAGE NO-PAUSE.
    MESSAGE "Do you really want to STOP the interface?"
        VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE answer.
    IF NOT answer THEN RETURN NO-APPLY.
    ELSE HIDE FRAME frame1.                  
END.

/*************** MAIN LOGIC ***************/
FILE-INFO:FILE-NAME = ".".

drive = "C:".
delayfrompf = 60.
pauseinterval = 0.
restartinterval = 3600.
logpath = "\vhp-cm\CM\".
restartscheduler = "RESTART-CM-BYPROG.bat".

RUN readSession.
IF drive-raw = "" THEN drive-raw = drive. /*NC - 28/01/21 put after readSession since as default raw folder will followed assigned drive in cfg*/
ASSIGN    
    fr-title    = "VHP - ChannelManager Interface " + STRING(grp) +
                  "(Status Not Running)"
    hotellist   = drive + logpath + "vhplib\hotel-list.xml". /*NC- change to helpdesk hotel-list*/
	
RUN create-hotel-list.

/* IF SEARCH(hotelfile) EQ ? THEN
    hotelfile   = drive + logpath + "hotel-list.xml". */

/*IF DAY(frdate) = 1 AND hotelfile THEN
DO:                    
    IF MONTH(frdate) - 2 = -1 THEN
        del-folder = 11.
    ELSE IF MONTH(frdate) - 2 = 0 THEN
        del-folder = 12.
    ELSE del-folder = MONTH(frdate) - 2.

    dirname = drive + logpath + hotel.htlcode + "\debug" + STRING(del-folder) + "\".
    DOS SILENT VALUE ("DEL " + dirname + "*.xml").
    DOS SILENT VALUE ("DEL " + dirname + "*.log").
    DOS SILENT VALUE ("DEL " + dirname + "*.txt").                    
END.
ELSE IF DAY(frdate) = 1 AND SEARCH(hotelfile) = ? THEN
DO:                    
    IF MONTH(frdate) - 6 LE 0 THEN
        del-folder = MONTH(frdate) - 6 + 12.
    ELSE del-folder = MONTH(frdate) - 6.

    dirname = drive + logpath + "debug" + STRING(del-folder) + "\".
    DOS SILENT VALUE ("DEL " + dirname + "*.xml").
    DOS SILENT VALUE ("DEL " + dirname + "*.log").
    DOS SILENT VALUE ("DEL " + dirname + "*.txt").                   
END.*/
/*IF DAY(frdate) = 1 THEN  /*03/09/25 NC - back to comment since del folder needs do by each hotel*/
DO:                    
    IF MONTH(frdate) - 6 LE 0 THEN
        del-folder = MONTH(frdate) - 6 + 12.
    ELSE del-folder = MONTH(frdate) - 6.

    IF hotelfile THEN dirname = drive + logpath + hotel.htlcode + "\debug" + STRING(del-folder) + "\".
    ELSE dirname = drive + logpath + "debug" + STRING(del-folder) + "\".

    DOS SILENT VALUE ("DEL " + dirname + "*.xml").
    /*DOS SILENT VALUE ("DEL " + dirname + "*.log"). do not delete the logfile*/
    DOS SILENT VALUE ("DEL " + dirname + "*.txt").

END.
*/

PROCESS EVENTS.
REPEAT:
    VIEW FRAME frame1.
    ENABLE message1[1] message1[2] message1[3] message1[4] message1[5]
        message1[6] message1[7] message1[8] message1[9] message1[10] 
        message1[11] message1[12] btn-start btn-exit WITH FRAME frame1.
    
    autostart = YES.
    IF autostart THEN APPLY "choose" TO btn-start.
    ELSE RUN assign-frame.        
    WAIT-FOR CHOOSE OF btn-exit.
    PAUSE(3) NO-MESSAGE.
END.

/*************** PROCEDURE ***************/
PROCEDURE read-temp-table:
DEF OUTPUT PARAMETER do-it AS LOGICAL INIT YES.
DEF VARIABLE err-config AS CHARACTER INIT "".
    
    do-it = YES.
    FIND FIRST t-list NO-LOCK NO-ERROR.
    IF AVAILABLE t-list THEN
    DO:
        ASSIGN
            AutoStart   = t-list.autostart
            delay       = t-list.delay
            period      = t-list.period
            liveflag    = t-list.liveflag
            htl-code    = TRIM(t-list.hotelcode) /*19/05/25 - Vhpcloud usually have space*/
            cUsername   = TRIM(t-list.username) /*19/05/25 - Vhpcloud usually have space*/
            cPassword   = TRIM(t-list.password) /*19/05/25 - Vhpcloud usually have space*/
            cPushRate   = t-list.pushrateflag
            cPullBook   = t-list.pullbookflag
            cUpdAvail   = t-list.pushavailflag
            /* workpath    = t-list.workpath */ /*NC 07/03/2025 - workpath assign on beginning not on this procedure*/ 
    		.
    
        IF NUM-ENTRIES(t-list.progavail,"=") GT 1  THEN
        DO:
            ASSIGN
                prog-avail-update = ENTRY(1,t-list.progavail,"=")
                dyna-code = ENTRY(2,t-list.progavail,"=").
            IF NUM-ENTRIES(t-list.progavail,"=") GE 3  THEN
                pushpax = LOGICAL(ENTRY(3,t-list.progavail,"=")).
            ELSE pushpax = NO.
            IF NUM-ENTRIES(t-list.progavail,"=") GE 4  THEN
                upperCaseName = LOGICAL(ENTRY(4,t-list.progavail,"=")).
            ELSE upperCaseName = NO.
            IF NUM-ENTRIES(t-list.progavail,"=") GE 5 THEN
                ASSIGN
                    delayRate  = INT(ENTRY(5,t-list.progavail,"="))
                    delayPull  = INT(ENTRY(6,t-list.progavail,"="))
                    delayAvail = INT(ENTRY(7,t-list.progavail,"=")).
    
            IF NUM-ENTRIES(t-list.progavail,"=") GE 8 THEN
                ASSIGN
                    pushAll      = LOGICAL(ENTRY(8,t-list.progavail,"="))
                    re-calculate = LOGICAL(ENTRY(9,t-list.progavail,"=")).
    
            IF NUM-ENTRIES(t-list.progavail,"=") GE 10 THEN
                ASSIGN
                    restriction-flag = LOGICAL(ENTRY(10,t-list.progavail,"="))
                    allotment   = LOGICAL(ENTRY(11,t-list.progavail,"="))
                    pax         = INT(ENTRY(12,t-list.progavail,"="))
                    bedsetup    = LOGICAL(ENTRY(13,t-list.progavail,"=")).
    		IF NUM-ENTRIES(t-list.progavail,"=") GE 14 THEN
    			ASSIGN
    				cPushBook = LOGICAL(ENTRY(14,t-list.progavail,"=")).
            IF NUM-ENTRIES(t-list.progavail,"=") GE 16 THEN
                ASSIGN
                    vcWSAgent     = ENTRY(16,t-list.progavail,"=")
                    vcWSAgent2    = ENTRY(17,t-list.progavail,"=")
                    vcWSAgent3    = ENTRY(18,t-list.progavail,"=")
                    vcWSAgent4    = ENTRY(19,t-list.progavail,"=")                
                    vcWebHost     = ENTRY(20,t-list.progavail,"=")
                    vcWebPort     = ENTRY(21,t-list.progavail,"=")                
                .
    
            IF NUM-ENTRIES(t-list.progavail,"=") GE 22 THEN
                ASSIGN           
                    emailadr = ENTRY(22,t-list.progavail,"="). /*delimeter wajib menggunakan comma*/                                   
    
            IF NUM-ENTRIES(t-list.progavail,"=") GE 23 THEN
                    vcWSAgent5    = ENTRY(23,t-list.progavail,"=").

            incl-tentative = NO.    /* FOR PUSH AVAILABILITY */
            IF NUM-ENTRIES(t-list.progavail,"=") GE 24 THEN
                incl-tentative    = LOGICAL(ENTRY(24,t-list.progavail,"=")).

            IF NUM-ENTRIES(t-list.progavail,"=") GE 26 THEN
                comboflag         = LOGICAL(ENTRY(26,t-list.progavail,"=")).

            IF NUM-ENTRIES(t-list.progavail,"=") GE 27 THEN
                readaricomboflag  = LOGICAL(ENTRY(27,t-list.progavail,"=")).
        END.
        ELSE
            ASSIGN
                prog-avail-update = t-list.progavail
                dyna-code         = ""
                pushpax           = NO
                upperCaseName     = NO
                delayRate         = 3600
                delayPull         = 60
                delayAvail        = 60
                pushAll           = NO
                re-calculate      = NO
                restriction-flag  = NO
                comboflag         = NO
                readaricomboflag  = NO.

        /* IF SEARCH(hotelfile) NE ? AND logpath-flag THEN
                workpath = drive + logpath.
        
        IF SUBSTR(workpath,LENGTH(workpath),1) NE CHR(92) THEN
                workpath = workpath + CHR(92). */ /*NC - Move to Main logic*/
       /* IF SUBSTR(logpath,LENGTH(logpath),1) NE CHR(92) THEN
            logpath = logpath + CHR(92). */ /*NC - double since already handle by readsession*/

        IF emailadr = "" THEN
            emailadr = hotel.defemail.
    
        IF SEARCH(workpath) EQ ? THEN
            OS-COMMAND SILENT VALUE("mkdir " + workpath).
    END.
    ELSE 
        do-it = NO.

    /*IF htl-code EQ "" OR cUsername EQ "" OR cPassword EQ "" OR 
        vcwsagent EQ "" OR vcwsagent2 EQ "" OR vcwsagent3 EQ "" OR vcwsagent4 EQ "" THEN 
            do-it = NO.*/

    IF htl-code EQ "" OR cUsername EQ "" OR cPassword EQ "" THEN
        ASSIGN
            do-it = NO
            err-config = "Credentials ".

    IF cPullBook THEN
    DO:
        IF vcwsagent EQ "" OR vcwsagent4 EQ "" THEN
            ASSIGN
                do-it = NO
                err-config = "PullBook ".
    END.
    IF cUpdAvail THEN
    DO:
        IF vcwsagent2 EQ "" THEN
            ASSIGN
                do-it = NO
                err-config = "PushAvail ".
    END.
    IF cPushRate THEN
    DO:
        IF vcwsagent3 EQ "" THEN
            ASSIGN
                do-it = NO
                err-config = "PushRate ".
    END.
    /*IF cPushBook THEN. /*no need to define*/ */

    IF NOT do-it THEN
    DO:
        RUN logmess(err-config + "configuration not complete").
        RETURN.
    END.
	EMPTY TEMP-TABLE r-list.
	EMPTY TEMP-TABLE rm-list.
    EMPTY TEMP-TABLE map-list-pull.
    EMPTY TEMP-TABLE map-list-push.
    
    FOR EACH t-pull-list WHERE t-pull-list.rcodeBE NE "" 
        AND t-pull-list.rmtypeBE NE "" NO-LOCK:
        CREATE map-list-pull.
        ASSIGN
            map-list-pull.ratecdVHP  = t-pull-list.rcodeVHP
            map-list-pull.ratecdSM   = t-pull-list.rcodeBE
            map-list-pull.rmtypeVHP  = t-pull-list.rmtypeVHP
            map-list-pull.rmtypeSM   = t-pull-list.rmtypeBE
            map-list-pull.argtnr     = t-pull-list.argtVHP
            
            map-list-pull.ratecdVHP  = TRIM(map-list-pull.ratecdVHP)
            map-list-pull.ratecdSM   = TRIM(map-list-pull.ratecdSM)
            map-list-pull.rmtypeVHP  = TRIM(map-list-pull.rmtypeVHP)
            map-list-pull.rmtypeSM   = TRIM(map-list-pull.rmtypeSM)
            map-list-pull.argtnr     = TRIM(map-list-pull.argtnr)
            
            map-list-pull.ratecdVHP  = REPLACE(map-list-pull.ratecdVHP, CHR(10), "")
            map-list-pull.ratecdSM   = REPLACE(map-list-pull.ratecdSM, CHR(10), "")
            map-list-pull.rmtypeVHP  = REPLACE(map-list-pull.rmtypeVHP, CHR(10), "")
            map-list-pull.rmtypeSM   = REPLACE(map-list-pull.rmtypeSM, CHR(10), "")
            map-list-pull.argtnr     = REPLACE(map-list-pull.argtnr, CHR(10), "")
            
            map-list-pull.ratecdVHP  = REPLACE(map-list-pull.ratecdVHP, CHR(13), "")
            map-list-pull.ratecdSM   = REPLACE(map-list-pull.ratecdSM, CHR(13), "")
            map-list-pull.rmtypeVHP  = REPLACE(map-list-pull.rmtypeVHP, CHR(13), "")
            map-list-pull.rmtypeSM   = REPLACE(map-list-pull.rmtypeSM, CHR(13), "")
            map-list-pull.argtnr     = REPLACE(map-list-pull.argtnr, CHR(13), "")
            
            map-list-pull.ratecdVHP  = REPLACE(map-list-pull.ratecdVHP, CHR(160), "")
            map-list-pull.ratecdSM   = REPLACE(map-list-pull.ratecdSM, CHR(160), "")
            map-list-pull.rmtypeVHP  = REPLACE(map-list-pull.rmtypeVHP, CHR(160), "")
            map-list-pull.rmtypeSM   = REPLACE(map-list-pull.rmtypeSM, CHR(160), "")
            map-list-pull.argtnr     = REPLACE(map-list-pull.argtnr, CHR(160), "")
            
            map-list-pull.ratecdVHP  = REPLACE(map-list-pull.ratecdVHP, "~n", "")
            map-list-pull.ratecdSM   = REPLACE(map-list-pull.ratecdSM, "~n", "")
            map-list-pull.rmtypeVHP  = REPLACE(map-list-pull.rmtypeVHP, "~n", "")
            map-list-pull.rmtypeSM   = REPLACE(map-list-pull.rmtypeSM, "~n", "")
            map-list-pull.argtnr     = REPLACE(map-list-pull.argtnr, "~n", "")
            
            .
    END.

    FOR EACH t-push-list
        WHERE t-push-list.rcodeBE NE "" 
        AND t-push-list.rmtypeBE NE "" NO-LOCK:
        CREATE map-list-push.
        ASSIGN
            map-list-push.ratecdVHP  = t-push-list.rcodeVHP
            map-list-push.ratecdSM   = t-push-list.rcodeBE
            map-list-push.rmtypeVHP  = t-push-list.rmtypeVHP
            map-list-push.rmtypeSM   = t-push-list.rmtypeBE
            map-list-push.argtnr     = t-push-list.argtVHP
            
            map-list-push.ratecdVHP  = TRIM(map-list-push.ratecdVHP)
            map-list-push.ratecdSM   = TRIM(map-list-push.ratecdSM)
            map-list-push.rmtypeVHP  = TRIM(map-list-push.rmtypeVHP)
            map-list-push.rmtypeSM   = TRIM(map-list-push.rmtypeSM)
            map-list-push.argtnr     = TRIM(map-list-push.argtnr)
            
            map-list-push.ratecdVHP  = REPLACE(map-list-push.ratecdVHP, CHR(10), "")
            map-list-push.ratecdSM   = REPLACE(map-list-push.ratecdSM, CHR(10), "")
            map-list-push.rmtypeVHP  = REPLACE(map-list-push.rmtypeVHP, CHR(10), "")
            map-list-push.rmtypeSM   = REPLACE(map-list-push.rmtypeSM, CHR(10), "")
            map-list-push.argtnr     = REPLACE(map-list-push.argtnr, CHR(10), "")
            
            map-list-push.ratecdVHP  = REPLACE(map-list-push.ratecdVHP, CHR(13), "")
            map-list-push.ratecdSM   = REPLACE(map-list-push.ratecdSM, CHR(13), "")
            map-list-push.rmtypeVHP  = REPLACE(map-list-push.rmtypeVHP, CHR(13), "")
            map-list-push.rmtypeSM   = REPLACE(map-list-push.rmtypeSM, CHR(13), "")
            map-list-push.argtnr     = REPLACE(map-list-push.argtnr, CHR(13), "")
            
            map-list-push.ratecdVHP  = REPLACE(map-list-push.ratecdVHP, CHR(160), "")
            map-list-push.ratecdSM   = REPLACE(map-list-push.ratecdSM, CHR(160), "")
            map-list-push.rmtypeVHP  = REPLACE(map-list-push.rmtypeVHP, CHR(160), "")
            map-list-push.rmtypeSM   = REPLACE(map-list-push.rmtypeSM, CHR(160), "")
            map-list-push.argtnr     = REPLACE(map-list-push.argtnr, CHR(160), "")
            
            map-list-push.ratecdVHP  = REPLACE(map-list-push.ratecdVHP, "~n", "")
            map-list-push.ratecdSM   = REPLACE(map-list-push.ratecdSM, "~n", "")
            map-list-push.rmtypeVHP  = REPLACE(map-list-push.rmtypeVHP, "~n", "")
            map-list-push.rmtypeSM   = REPLACE(map-list-push.rmtypeSM, "~n", "")
            map-list-push.argtnr     = REPLACE(map-list-push.argtnr, "~n", "")
            .
			FIND FIRST r-list WHERE r-list.rcode = map-list-push.ratecdVHP NO-LOCK NO-ERROR.
			IF NOT AVAILABLE r-list THEN
            DO:
				CREATE r-list.
				ASSIGN
					r-list.rcode = map-list-push.ratecdVHP
				.
			END.
			FIND FIRST rm-list WHERE rm-list.rmtype = map-list-push.rmtypeVHP NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rm-list THEN
            DO:
				CREATE rm-list.
				ASSIGN 
					rm-list.rmtype = map-list-push.rmtypeVHP 
				.
			END.
    END.
END.

PROCEDURE logmess:
    DEFINE INPUT PARAMETER LogMessage AS CHAR FORMAT "x(200)"      NO-UNDO.
    DEFINE VARIABLE logfile AS CHAR NO-UNDO.
    DEFINE VARIABLE ct                      AS CHAR FORMAT "x(200)"     NO-UNDO.
    DEFINE VARIABLE ch                      AS CHAR                     NO-UNDO.
    DEFINE VARIABLE i                       AS INTEGER                  NO-UNDO.

    IF SEARCH(workPath + "debug" + STRING(MONTH(TODAY))) EQ ? THEN
        OS-COMMAND SILENT VALUE("mkdir " + workPath + "debug" + STRING(MONTH(TODAY))).
        
    ct = LogMessage.
    /*
    ct = "".
    DO i = 1 TO LENGTH(LogMessage):
        ch = SUBSTR(LogMessage, i, 1).
        IF      ch = CHR(1)  THEN ct = ct + "<SOH>".
        ELSE IF ch = CHR(2)  THEN ct = ct + "<STX>".
        ELSE IF ch = CHR(3)  THEN ct = ct + "<ETX>".
        ELSE IF ch = CHR(4)  THEN ct = ct + "<EOT>".
        ELSE IF ch = CHR(5)  THEN ct = ct + "<ENQ>".
        ELSE IF ch = CHR(6)  THEN ct = ct + "<ACK>".
        ELSE IF ch = CHR(7)  THEN ct = ct + "<BEL>".
        ELSE IF ch = CHR(8)  THEN ct = ct + "<BS>".
        ELSE IF ch = CHR(9)  THEN ct = ct + "<HT>".
        ELSE IF ch = CHR(10) THEN ct = ct + "<LF>".
        ELSE IF ch = CHR(11) THEN ct = ct + "<VT>".
        ELSE IF ch = CHR(12) THEN ct = ct + "<FF>".
        ELSE IF ch = CHR(13) THEN ct = ct + "<LRC>".
        ELSE IF ch = CHR(21) THEN ct = ct + "<NAK>".
        ELSE IF ch = CHR(32) THEN ct = ct + ch.
        ELSE IF (ASC(ch) LE 31) OR (ASC(ch) GE 127) THEN
          ct = ct + "CHR(" + STRING(ASC(ch)) + ")".
        ELSE ct = ct + ch.
    END.
    */
    timestr = STRING(TIME,"HH:MM:SS").
    logfile = workpath + "debug" + STRING(MONTH(TODAY)) + "\"+ STRING(MONTH(TODAY), "99")+ STRING(YEAR(TODAY),"9999") + ".LOG".
    
    OUTPUT STREAM lStream TO Value(logfile) APPEND UNBUFFERED.
        PUT STREAM lStream UNFORMATTED 
        "[" STRING(TODAY,"99.99.99") " " timestr "] " 
        ct SKIP.         
    OUTPUT STREAM lStream CLOSE.
	IF central-path NE "" THEN /* NC - 25/09/25 */
		RUN logmess-central(ct).

    IF NOT MinSize THEN RUN disp-mess(timestr + " " + ct).
END PROCEDURE.

PROCEDURE logmess-nodisplay:
	DEFINE INPUT PARAMETER rmtypeVHP AS CHARACTER NO-UNDO.
    DEFINE VARIABLE logfile AS CHAR NO-UNDO.
    /*
    DEFINE INPUT PARAMETER LogMessage2 AS CHAR FORMAT "x(200)"      NO-UNDO.
   
    DEFINE VARIABLE ct                      AS CHAR FORMAT "x(200)"     NO-UNDO.
    DEFINE VARIABLE ch                      AS CHAR                     NO-UNDO.
    DEFINE VARIABLE i                       AS INTEGER                  NO-UNDO.

    
    ct = "".
    DO i = 1 TO LENGTH(LogMessage):
        ch = SUBSTR(LogMessage, i, 1).
        IF      ch = CHR(1)  THEN ct = ct + "<SOH>".
        ELSE IF ch = CHR(2)  THEN ct = ct + "<STX>".
        ELSE IF ch = CHR(3)  THEN ct = ct + "<ETX>".
        ELSE IF ch = CHR(4)  THEN ct = ct + "<EOT>".
        ELSE IF ch = CHR(5)  THEN ct = ct + "<ENQ>".
        ELSE IF ch = CHR(6)  THEN ct = ct + "<ACK>".
        ELSE IF ch = CHR(7)  THEN ct = ct + "<BEL>".
        ELSE IF ch = CHR(8)  THEN ct = ct + "<BS>".
        ELSE IF ch = CHR(9)  THEN ct = ct + "<HT>".
        ELSE IF ch = CHR(10) THEN ct = ct + "<LF>".
        ELSE IF ch = CHR(11) THEN ct = ct + "<VT>".
        ELSE IF ch = CHR(12) THEN ct = ct + "<FF>".
        ELSE IF ch = CHR(13) THEN ct = ct + "<LRC>".
        ELSE IF ch = CHR(21) THEN ct = ct + "<NAK>".
        ELSE IF ch = CHR(32) THEN ct = ct + ch.
        ELSE IF (ASC(ch) LE 31) OR (ASC(ch) GE 127) THEN
          ct = ct + "CHR(" + STRING(ASC(ch)) + ")".
        ELSE ct = ct + ch.
    END.
    */
    logfile = workpath + "debug" + STRING(MONTH(TODAY)) + "\"+ STRING(MONTH(TODAY), "99")+ STRING(YEAR(TODAY),"9999") + ".LOG".
    
    OUTPUT STREAM lStream TO Value(logfile) APPEND UNBUFFERED.
    FOR EACH logs-list WHERE logs-list.rmtype EQ rmtypeVHP :
        PUT STREAM lStream UNFORMATTED 
        "[" STRING(TODAY,"99.99.99") " " STRING(TIME,"HH:MM:SS") "] " 
        logs-list.logs SKIP.  
    END.
    OUTPUT STREAM lStream CLOSE.
   /* EMPTY TEMP-TABLE logs-list.

    RUN logmess-central(LogMessage2).*/ /*NC - 27/03/25 Optimize process*/

    /*IF NOT MinSize THEN RUN disp-mess(ct).*/
END PROCEDURE.

PROCEDURE logmess-central:
    DEFINE INPUT PARAMETER LogMessage3 AS CHAR FORMAT "x(200)"      NO-UNDO.
    DEFINE VARIABLE logfile AS CHAR NO-UNDO.
    DEFINE VARIABLE modifiedPath        AS CHARACTER    NO-UNDO.

    /* BLY Changing Log central in 1 place 30/05/2025 */
    IF SEARCH(central-path) EQ ? THEN
    OS-COMMAND SILENT VALUE("mkdir " + central-path).

    modifiedPath = IF SUBSTR(logpath, LENGTH(logpath), 1) = "\" THEN SUBSTR(logpath, 1, LENGTH(logpath) - 1) ELSE logpath.
    modifiedPath = REPLACE(modifiedPath, "-", "").
    
    logfile = central-path + modifiedPath + "-group" + STRING(grp) + "-" + STRING(MONTH(TODAY), "99") + STRING(YEAR(TODAY),"9999") + ".LOG". /* nc - 24/12/24*/ 
    /* END BLY */
    
    OUTPUT STREAM lStream TO Value(logfile) APPEND UNBUFFERED.
        PUT STREAM lStream UNFORMATTED 
        "[" STRING(TODAY,"99.99.99") " " STRING(TIME,"HH:MM:SS") "] " 
        LogMessage3 SKIP.         
    OUTPUT STREAM lStream CLOSE.

END PROCEDURE.

PROCEDURE push-rate:
DEFINE VARIABLE dd          AS INTEGER  NO-UNDO.
DEFINE VARIABLE mm          AS INTEGER  NO-UNDO.
DEFINE VARIABLE yy          AS INTEGER  NO-UNDO.
DEFINE VARIABLE rm-rate     AS DECIMAL        NO-UNDO.
DEFINE VARIABLE rmType      AS CHAR           NO-UNDO.
DEFINE VARIABLE rCode       AS CHAR           NO-UNDO.

DEFINE VARIABLE attempt   AS INTEGER  NO-UNDO.
DEFINE VARIABLE curr-stat    AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE curr-rate    AS DECIMAL.
DEFINE VARIABLE curr-recid   AS INT.
DEFINE VARIABLE curr-rcode   AS CHAR.
DEFINE VARIABLE curr-bezeich AS CHAR.
DEFINE VARIABLE curr-pax     AS INT.
DEFINE VARIABLE curr-child   AS INT.
DEFINE VARIABLE msg-str      AS CHAR.
DEFINE VARIABLE counter      AS INT INIT 0.
DEFINE VARIABLE duplicate    AS LOGICAL.

DEFINE BUFFER buffrate  FOR push-rate-list. 
DEFINE BUFFER brate1    FOR brate.
EMPTY TEMP-TABLE logs-list.
    ASSIGN
        curr-rate    = 0
        curr-recid   = 0
        curr-bezeich = ""
        curr-rcode   = ""
        curr-pax     = 0
        curr-child   = 0
    .
	RUN update-xml("rate", ""). /*NC #E98552*/ /*for count hotel.ratecounter*/
    IF pushPax THEN
    DO:
        FOR EACH push-rate-list WHERE push-rate-list.flag /* BY push-rate-list.rcode BY push-rate-list.zikatnr 
            BY push-rate-list.startperiode BY push-rate-list.pax BY push-rate-list.child */:
            
            FIND FIRST brate WHERE brate.startperiode = push-rate-list.startperiode AND brate.zikatnr = push-rate-list.zikatnr 
                AND brate.rcode = push-rate-list.rcode NO-LOCK NO-ERROR.
            IF NOT AVAILABLE brate THEN
            DO:
                CREATE brate1.
                ASSIGN
                    brate1.startperiode  = push-rate-list.startperiode
                    brate1.endperiode    = push-rate-list.endperiode
                    brate1.zikatnr       = push-rate-list.zikatnr 
                    brate1.rcode         = push-rate-list.rcode 
                    brate1.currency      = push-rate-list.currency
                    brate1.bezeich       = push-rate-list.bezeich
                .
                IF push-rate-list.pax NE 0 THEN
                    ASSIGN
                        brate1.rmrate-str    = STRING(push-rate-list.rmrate) + ";"
                        brate1.pax-str       = STRING(push-rate-list.pax) + ";".
                
                IF push-rate-list.child NE 0 THEN
                    ASSIGN
                        brate1.rmrate-child-str = STRING(push-rate-list.rmrate) + ";"
                        brate1.child-str     = STRING(push-rate-list.child) + ";".
            END.
            ELSE IF AVAILABLE brate THEN
            DO:
                IF push-rate-list.pax NE 0 THEN
                    ASSIGN
                        brate.rmrate-str    = brate.rmrate-str + STRING(push-rate-list.rmrate) + ";"
                        brate.pax-str       = brate.pax-str + STRING(push-rate-list.pax) + ";".
                
                IF push-rate-list.child NE 0 THEN
                    ASSIGN
                        brate.rmrate-child-str = brate.rmrate-child-str + STRING(push-rate-list.rmrate) + ";"
                        brate.child-str     = brate.child-str + STRING(push-rate-list.child) + ";".
            END.
        END.
    
        FOR EACH brate /* BY brate.rcode BY brate.zikatnr BY brate.startperiode */:
            counter = counter + 1.
            IF counter GT 1 THEN
            DO: 
                FIND FIRST brate1 WHERE brate1.endperiode = brate.startperiode - 1 AND brate1.rcode = brate.rcode
                    AND brate1.zikatnr = brate.zikatnr NO-ERROR.
                IF AVAILABLE brate1 AND NUM-ENTRIES(brate1.pax-str,";") =  NUM-ENTRIES(brate.pax-str,";") THEN
                DO:
                    duplicate = YES.
                    DO i = 1 TO NUM-ENTRIES(brate1.pax-str,";") - 1:
                        IF INT(ENTRY(i,brate1.pax-str,";")) NE INT(ENTRY(i,brate.pax-str,";")) OR
                           DEC(ENTRY(i,brate1.rmrate-str,";")) NE DEC(ENTRY(i,brate.rmrate-str,";")) THEN
                        DO:
                            duplicate = NO.
                            LEAVE.
                        END.
                    END.

                    DO i = 1 TO NUM-ENTRIES(brate1.child-str,";") - 1:
                        IF INT(ENTRY(i,brate1.child-str,";")) NE INT(ENTRY(i,brate.child-str,";")) OR
                           DEC(ENTRY(i,brate1.rmrate-child-str,";")) NE DEC(ENTRY(i,brate.rmrate-child-str,";")) THEN
                        DO:
                            duplicate = NO.
                            LEAVE.
                        END.
                    END.
                    
                    IF duplicate THEN
                    DO:
                        ASSIGN brate1.endperiode = brate.startperiode.
                        DELETE brate.
                    END.
                END.                 
            END.
        END.
        FOR EACH brate:
			 /*FIND FIRST map-list-push WHERE map-list-push.rmtypeVHP = brate.bezeich AND 
                map-list-push.ratecdVHP = brate.rcode NO-LOCK NO-ERROR.
            IF AVAILABLE map-list-push THEN
                ASSIGN
                    curr-bezeich = map-list-push.rmtypeSM
                    curr-rcode  = map-list-push.ratecdSM.
            ASSIGN
                brate.str-date1 = 
                    STRING(YEAR(brate.startperiode),"9999") + "-" + 
                    STRING(MONTH(brate.startperiode),"99") + "-" +
                    STRING(DAY(brate.startperiode),"99")
                brate.str-date2 = 
                    STRING(YEAR(brate.endperiode),"9999") + "-" + 
                    STRING(MONTH(brate.endperiode),"99") + "-" +
                    STRING(DAY(brate.endperiode),"99").

            msg-str = "DT" + STRING(brate.str-date1) + ";" + STRING(brate.str-date2) + "<ETX>" +
                        "CUR" + brate.currency + "<ETX>" +
                        "AM" + STRING(brate.rmRate-str) + "<ETX>" +
                        "PAX" + STRING(brate.pax-str) + "<ETX>" +
                        "AMc" + STRING(brate.rmRate-child-str) + "<ETX>" +
                        "PAXc" + STRING(brate.child-str) + "<ETX>" +
                        "RC" + curr-rcode + "<ETX>" +
                        "RT" + curr-bezeich.*/
            CREATE logs-list.
            ASSIGN 
				logs-list.rmtype = brate.bezeich
				logs-list.logs = "RATES|" + brate.bezeich + " " 
						 + "RateCode: " + brate.rcode + " "
                         + "Start Date: " + brate.str-date1 + " " 
                         + "End Date: " + brate.str-date2 + " " 
						 + "Pax: " + STRING(brate.pax-str) + " "
                         + "Amount: " + STRING(brate.rmRate-str)
				. /*NC - concept changed - revertback 27/10/25*/
        END.
    END. 
    IF NOT pushpax THEN
    DO:
        FOR EACH push-rate-list WHERE push-rate-list.flag /* BY push-rate-list.rcode 
            BY push-rate-list.zikatnr BY push-rate-list.startperiode BY push-rate-list.pax */ :
           /* MESSAGE push-rate-list.rcode push-rate-list.zikatnr push-rate-list.startperiode. */
			CREATE logs-list.
            ASSIGN 
				logs-list.rmtype = push-rate-list.bezeich
				logs-list.logs = "RATES|" + push-rate-list.bezeich + " " 
						 + "RateCode: " + push-rate-list.rcode + " "
                         + "Start Date: " + push-rate-list.str-date1 + " " 
                         + "End Date: " + push-rate-list.str-date2 + " " 
                         + "Amount: " + STRING(push-rate-list.rmRate). /* NC - use original date for debug purpose*/
            IF curr-rate NE push-rate-list.rmrate THEN
                ASSIGN
                    curr-rcode   = push-rate-list.rcode
                    curr-bezeich = push-rate-list.bezeich
                    curr-recid   = push-rate-list.counter
                    curr-rate    = push-rate-list.rmrate
                    curr-pax     = push-rate-list.pax
                .
            ELSE IF curr-rate = push-rate-list.rmrate AND (curr-rcode NE push-rate-list.rcode OR curr-bezeich NE push-rate-list.bezeich OR
                                                           curr-pax NE push-rate-list.pax) THEN
                ASSIGN 
                    curr-rcode = push-rate-list.rcode
                    curr-bezeich = push-rate-list.bezeich
                    curr-recid  = push-rate-list.counter
                    curr-rate  = push-rate-list.rmrate
                    curr-pax     = push-rate-list.pax.
    
            ELSE IF curr-rate = push-rate-list.rmrate AND curr-rcode = push-rate-list.rcode AND curr-bezeich = push-rate-list.bezeich 
                AND curr-pax = push-rate-list.pax THEN
            DO:
                FIND FIRST buffrate WHERE buffrate.counter = curr-recid /*EXCLUSIVE-LOCK*/ NO-ERROR.
                IF AVAILABLE buffrate AND (buffrate.endperiode = push-rate-list.startperiode - 1 OR 
                                           buffrate.endperiode GE push-rate-list.startperiode)
                    AND buffrate.rcode = push-rate-list.rcode
                    AND buffrate.bezeich = push-rate-list.bezeich THEN
                DO:
                    
                    IF buffrate.endperiode GT push-rate-list.endperiode THEN.
                    ELSE buffrate.endperiode = push-rate-list.endperiode.
                    /*DELETE push-rate-list.
                    RELEASE push-rate-list.*/
                    ASSIGN push-rate-list.flag = NO.
                END.
            END.    
        END.

        /*FOR EACH push-rate-list WHERE push-rate-list.flag :
			FIND FIRST map-list-push WHERE map-list-push.rmtypeVHP = push-rate-list.bezeich AND 
                map-list-push.ratecdVHP = push-rate-list.rcode NO-LOCK NO-ERROR.
            IF AVAILABLE map-list-push THEN
                ASSIGN
                    curr-bezeich = map-list-push.rmtypeSM
                    curr-rcode  = map-list-push.ratecdSM.
            ASSIGN
                push-rate-list.str-date1 = 
                    STRING(YEAR(push-rate-list.startperiode),"9999") + "-" + 
                    STRING(MONTH(push-rate-list.startperiode),"99") + "-" +
                    STRING(DAY(push-rate-list.startperiode),"99")
                push-rate-list.str-date2 = 
                    STRING(YEAR(push-rate-list.endperiode),"9999") + "-" + 
                    STRING(MONTH(push-rate-list.endperiode),"99") + "-" +
                    STRING(DAY(push-rate-list.endperiode),"99").

             msg-str = "DT" + STRING(push-rate-list.str-date1) + ";" + STRING(push-rate-list.str-date2) + "<ETX>" + 
                        "CUR" + push-rate-list.currency + "<ETX>" + 
                        "AM" + STRING(push-rate-list.rmRate) + "<ETX>" + 
                        "RC" + curr-rcode + "<ETX>" + 
                        "RT" + curr-bezeich.
            
        END.*/
    END.

    FIND FIRST push-rate-list NO-LOCK NO-ERROR.
    IF AVAILABLE push-rate-list THEN 
    DO:
                
        /* FOR EACH push-rate-list WHERE push-rate-list.flag:
            FIND FIRST r-list WHERE r-list.rcode = push-rate-list.rcode NO-LOCK NO-ERROR.
            IF NOT AVAILABLE r-list THEN
            DO:
                CREATE r-list.
                r-list.rcode = push-rate-list.rcode.
            END.
            FIND FIRST rm-list WHERE rm-list.rmtype = push-rate-list.bezeich NO-LOCK NO-ERROR.
            IF NOT AVAILABLE rm-list THEN
            DO:
                CREATE rm-list.
                ASSIGN rm-list.rmtype = push-rate-list.bezeich.
            END.
        END. */ /*NC - Moved to read-temp-table procedure*/
		
		FOR EACH rm-list:
			FIND FIRST push-rate-list WHERE push-rate-list.bezeich = rm-list.rmtyp NO-LOCK NO-ERROR.
			IF AVAILABLE push-rate-list THEN
			DO:
				IF pushpax THEN DO:
					RUN logmess-nodisplay(rm-list.rmtyp).
					RUN call-HotelRateAmountNotifRQ-pax(rm-list.rmtyp, OUTPUT curr-stat).
					/*DO attempt = 1 TO 3:
					
					RUN call-HotelRateAmountNotifRQ-pax(rm-list.rmtyp, OUTPUT curr-stat).
					IF curr-stat THEN LEAVE.
					
					END.*/ /*NC - #E98552*/
				END.
				ELSE DO:
					RUN logmess-nodisplay(rm-list.rmtyp).
					RUN call-HotelRateAmountNotifRQ(rm-list.rmtyp, OUTPUT curr-stat).
				/* DO attempt = 1 TO 3:
						RUN call-HotelRateAmountNotifRQ(rm-list.rmtyp, OUTPUT curr-stat).
						IF curr-stat THEN LEAVE.
					END. */ /*NC - #E98552*/
				END.
				
			END.
		END.
		 
		IF NOT curr-stat AND hotel.ratecounter GE 5 THEN
		DO:
			RUN logmess("STOP push rates for ALL roomtype since 5 times loop and still got error...").
			IF pushall THEN RUN update-bookengine-configbl.p ON hServer (8,hotel.beCode,NO,"").
			IF readaricomboflag = NO OR rateflag = NO THEN 
				RUN if-bookeng-update-aribl.p ON hServer ("","rateAll").
			ELSE
				DOS SILENT VALUE("DEL " + ratefile).
			IF NOT cUpdAvail THEN
			DO:
				IF readaricomboflag = NO OR allotflag = NO THEN 
					RUN if-bookeng-update-aribl.p ON hServer ("","availAll").
				ELSE
					DOS SILENT VALUE("DEL " + allotfile).
			END.
		END.
    END.
END.

PROCEDURE call-HotelRateAmountNotifRQ:
    DEFINE INPUT PARAMETER in-rmtype AS CHAR.
	DEFINE OUTPUT PARAMETER state-attempt AS LOGICAL INIT NO.
    DEFINE VARIABLE OTA_HotelRateAmountNotifRS  AS LONGCHAR NO-UNDO INIT "".

    DEF VAR room-type   AS CHARACTER.
    DEF VAR rate-code   AS CHARACTER.
    DEF VAR currency    AS CHARACTER.
    DEF VAR start-date  AS CHARACTER.
    DEF VAR end-date    AS CHARACTER.
    DEF VAR room-rate   AS CHARACTER.
    DEF VAR rcode       AS CHARACTER.

    DEFINE VARIABLE filenm AS CHAR.

    DEFINE VARIABLE error-pushrate-file AS CHARACTER.

    ASSIGN
        uuid = GENERATE-UUID
        echotoken = GUID(uuid)
        timestamp = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" +
                    STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "+00:00"
        .

    
    vcXMLText = 

    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '~n' +
      '<soap:Header>' + '~n' +
        '<wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' + '~n' +
          '<wsse:UsernameToken>' + '~n' +
            '<wsse:Username>' + cUsername + '</wsse:Username>' + '~n' +
            '<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">' + cPassword + '</wsse:Password>' + '~n' +
          '</wsse:UsernameToken>' + '~n' +
        '</wsse:Security>' + '~n' +
      '</soap:Header>' + '~n' +
    
    '<soap:Body>' + '~n' +
    '<OTA_HotelRateAmountNotifRQ EchoToken="' + echotoken + '" TimeStamp="' + timestamp + '" Version="1.0" xmlns="http://www.opentravel.org/OTA/2003/05">' + '~n' +
        '<RateAmountMessages HotelCode="' + htl-code + '">'.

        FOR EACH push-rate-list WHERE push-rate-list.bezeich = in-rmtype AND push-rate-list.flag NO-LOCK /*BY push-rate-list.rcode BY push-rate-list.zikatnr BY push-rate-list.startperiode*/ /*14/05/25*/ :
		
			ASSIGN
                push-rate-list.str-date1 = 
                    STRING(YEAR(push-rate-list.startperiode),"9999") + "-" + 
                    STRING(MONTH(push-rate-list.startperiode),"99") + "-" +
                    STRING(DAY(push-rate-list.startperiode),"99")
                push-rate-list.str-date2 = 
                    STRING(YEAR(push-rate-list.endperiode),"9999") + "-" + 
                    STRING(MONTH(push-rate-list.endperiode),"99") + "-" +
                    STRING(DAY(push-rate-list.endperiode),"99").
				
            FIND FIRST map-list-push WHERE map-list-push.rmtypeVHP = push-rate-list.bezeich AND 
                map-list-push.ratecdVHP = push-rate-list.rcode NO-LOCK NO-ERROR.
            IF AVAILABLE map-list-push THEN
                ASSIGN
                    room-type = map-list-push.rmtypeSM
                    rate-code  = map-list-push.ratecdSM
                    .
            ELSE
                ASSIGN
                    room-type = push-rate-list.bezeich
                    rate-code  = push-rate-list.rcode
                    .
            DO:
                vcXMLText = vcXMLText + 

            	'<RateAmountMessage>' + '~n' +
            		'<StatusApplicationControl InvTypeCode="' + room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-rate-list.str-date1 + 
                        '" End="' + push-rate-list.str-date2 + '"/>' + '~n' +
            		'<Rates>' + '~n' +
            			'<Rate CurrencyCode="' + push-rate-list.currency + '" >' + '~n' +
            				'<BaseByGuestAmts>' + '~n' +
            					'<BaseByGuestAmt AmountAfterTax="' + STRING(push-rate-list.rmrate) + '"/>' + '~n' +
            				'</BaseByGuestAmts>' + '~n' +
            			'</Rate>' + '~n' +
            		'</Rates>' + '~n' +
            	'</RateAmountMessage>'.
            END.
        END.

        vcXMLText = vcXMLText +

        '</RateAmountMessages>' + '~n' +
    '</OTA_HotelRateAmountNotifRQ>' + '~n' +
    '</soap:Body>' + '~n' +
    '</soap:Envelope>'.
/*
    vcRequest =
        'POST ' + vcWSAgent3 + ' HTTP/1.1' + '~r~n' +
        'Host: ' + vcWebHost + '~r~n' +
        'Content-Type: text/xml;charset=UTF-8' + '~r~n' +
        'Content-Length: ' + STRING(LENGTH(vcXMLText)) + '~r~n' +
        '~r~n'.
*/    
    /* IF roomtypeoutput = "" THEN
        roomtypeoutput = backuproomtype. */ /*NC - no use anymore use in-rmtype instead*/

    /*M 240611 -> Debugging to check request to push rates */
    filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\rate_" + in-rmtype + "_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".
    
   /* OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(vcXMLText) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(vcXMLText, i, 1)) FORMAT "x(1)".
        END.        
    OUTPUT STREAM s2 CLOSE.*/

    COPY-LOB vcXMLText TO FILE filenm.
    IF debugging-flag = "YES" THEN
    DO:
        RUN logmess("Rate File Has Been Generated").
        IF readaricomboflag = NO OR rateflag = NO THEN
            FOR EACH r-list:
                ASSIGN rcode-rmtype = r-list.rcode + ";" + rm-list.rmtyp.
                RUN if-bookeng-update-aribl.p ON hServer (rcode-rmtype,"ratebyrmtype").
            END.
        ELSE
            DOS SILENT VALUE("DEL " + ratefile).
        IF NOT cUpdAvail THEN
        DO:
            IF readaricomboflag = NO OR allotflag = NO THEN
                RUN if-bookeng-update-aribl.p ON hServer ("","avail").
            ELSE
                DOS SILENT VALUE("DEL " + allotfile).
        END.
        IF re-calculate THEN
            RUN update-bookengine-configbl.p ON hServer (9,hotel.beCode,NO,"").
        IF pushall = YES THEN
            RUN update-bookengine-configbl.p ON hServer (8,hotel.beCode,NO,"").
        /* IF hotel.ratecounter NE 0 THEN RUN update-xml("rate", "reset"). */ /*move up*/
    END.
    ELSE
    DO:
        IF SEARCH(filenm) = ? THEN 
        DO:
            RUN logmess ("debug: not available file xml rate").
            RUN mt-program.
        END.
    
        EMPTY TEMP-TABLE header-list.
    
        CREATE header-list.
        ASSIGN
            vKey="Content-Type"
            vValue="text/xml;charset=UTF-8".
       RUN logmess("Uploading rates for room type " + in-rmtype + " to Channel Manager..."). 
       RUN http-request-tlsui.p("post",vcWSAgent3,vcxmltext,TABLE header-list,
                                 OUTPUT OTA_HotelRateAmountNotifRS, OUTPUT errorMsg).
      /*   MESSAGE STRING(OTA_HotelRateAmountNotifRS) VIEW-AS ALERT-BOX.*/

        IF errorMsg NE "" THEN
            RUN logmess(errorMsg + " | " + vcWSagent3).
    
        IF OTA_HotelRateAmountNotifRS MATCHES "*Success*" THEN
        DO: 
    		state-attempt = YES.
            RUN logmess("Success Updating Rates " + in-rmtype).
    		IF readaricomboflag = NO OR rateflag = NO THEN
                FOR EACH r-list:
                    ASSIGN rcode-rmtype = r-list.rcode + ";" + rm-list.rmtyp.
                    RUN if-bookeng-update-aribl.p ON hServer (rcode-rmtype,"ratebyrmtype").
                END.
            ELSE
                DOS SILENT VALUE("DEL " + ratefile).
            IF NOT cUpdAvail THEN
            DO:
                IF readaricomboflag = NO OR allotflag = NO THEN
                    RUN if-bookeng-update-aribl.p ON hServer ("","avail").
                ELSE
                    DOS SILENT VALUE("DEL " + allotfile).
            END.
            IF re-calculate THEN
                RUN update-bookengine-configbl.p ON hServer (9,hotel.beCode,NO,"").
            IF pushall = YES THEN
                RUN update-bookengine-configbl.p ON hServer (8,hotel.beCode,NO,"").
            /* IF hotel.ratecounter NE 0 THEN RUN update-xml("rate", "reset"). */ /*Move up*/
        END.
        ELSE
        DO:
    		state-attempt = NO.
            RUN logmess("Failed Updating Rates " + in-rmtype).
            IF OTA_HotelRateAmountNotifRS = "" THEN
                RUN logmess ("Check Push Rate Code Mapping Setup").
            ELSE IF NOT OTA_HotelRateAmountNotifRS MATCHES "*Success*" THEN
            DO:
				RUN logmess ("OTA_HotelRateAmountNotifRS== " + OTA_HotelRateAmountNotifRS ).
                error-pushrate-file = 
                    workPath + "debug" + STRING(MONTH(TODAY)) + "\Error_rate_" + in-rmtype + "_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".
                /*
                OUTPUT STREAM s2 TO VALUE(error-pushrate-file).
                DO i = 1 TO LENGTH(OTA_HotelRateAmountNotifRS) :
                    PUT STREAM s2 UNFORMATTED STRING(SUBSTR(OTA_HotelRateAmountNotifRS, i, 1)) FORMAT "x(1)".
                END.        
                OUTPUT STREAM s2 CLOSE.*/

                COPY-LOB OTA_HotelRateAmountNotifRS TO FILE error-pushrate-file.
                RUN send-email("Rate", error-pushrate-file, htl-code, "").
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE call-HotelRateAmountNotifRQ-pax:
    DEFINE INPUT  PARAMETER in-rmtype AS CHAR.
	DEFINE OUTPUT PARAMETER state-attempt AS LOGICAL INIT NO.
    DEFINE VARIABLE OTA_HotelRateAmountNotifRS  AS LONGCHAR NO-UNDO INIT "".

    DEF VAR room-type   AS CHARACTER.
    DEF VAR rate-code   AS CHARACTER.
    DEF VAR currency    AS CHARACTER.
    DEF VAR start-date  AS CHARACTER.
    DEF VAR end-date    AS CHARACTER.
    DEF VAR room-rate   AS CHARACTER.
    DEF VAR rcode       AS CHARACTER.

    DEFINE VARIABLE filenm AS CHAR.
    DEFINE VARIABLE rcode-rmtype AS CHAR.

    DEFINE VARIABLE error-pushrate-file AS CHARACTER.
    
    ASSIGN
        uuid = GENERATE-UUID
        echotoken = GUID(uuid)
        timestamp = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" +
                    STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "+00:00"
        .

    
    vcXMLText = 

    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '~n' +
      '<soap:Header>' + '~n' +
        '<wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' + '~n' +
          '<wsse:UsernameToken>' + '~n' +
            '<wsse:Username>' + cUsername + '</wsse:Username>' + '~n' +
            '<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">' + cPassword + '</wsse:Password>' + '~n' +
          '</wsse:UsernameToken>' + '~n' +
        '</wsse:Security>' + '~n' +
      '</soap:Header>' + '~n' +
    
    '<soap:Body>' + '~n' +
    '<OTA_HotelRateAmountNotifRQ EchoToken="' + echotoken + '" TimeStamp="' + timestamp + '" Version="1.0" xmlns="http://www.opentravel.org/OTA/2003/05">' + '~n' +
        '<RateAmountMessages HotelCode="' + htl-code + '">'.



    FOR EACH brate WHERE brate.bezeich = in-rmtype /*BY brate.rcode BY brate.zikatnr BY brate.startperiode*/ :
		ASSIGN
                brate.str-date1 = 
                    STRING(YEAR(brate.startperiode),"9999") + "-" + 
                    STRING(MONTH(brate.startperiode),"99") + "-" +
                    STRING(DAY(brate.startperiode),"99")
                brate.str-date2 = 
                    STRING(YEAR(brate.endperiode),"9999") + "-" + 
                    STRING(MONTH(brate.endperiode),"99") + "-" +
                    STRING(DAY(brate.endperiode),"99").
        FIND FIRST map-list-push WHERE map-list-push.rmtypeVHP = brate.bezeich AND 
            map-list-push.ratecdVHP = brate.rcode NO-LOCK NO-ERROR.
        IF AVAILABLE map-list-push THEN
            ASSIGN
                room-type = map-list-push.rmtypeSM
                rate-code  = map-list-push.ratecdSM
                .
        ELSE
            ASSIGN
                room-type = brate.bezeich
                rate-code  = brate.rcode
                .

        
        vcXMLText = vcXMLText +
            '<RateAmountMessage>' + '~n' +
                '<StatusApplicationControl Start=' + '"' + brate.str-date1 + '"' + ' End=' + '"' + brate.str-date2 + '"' + 
                    ' RatePlanCode=' + '"' + rate-code + '"' + ' InvTypeCode=' + '"' + room-type + '"' + '/>' + '~n' +
                '<Rates>' + '~n' +
                    '<Rate CurrencyCode=' + '"' + brate.currency + '"' + '>' + '~n' +
                    '<BaseByGuestAmts>' + '~n'.
        IF brate.pax-str NE "" THEN
            DO i = 1 TO NUM-ENTRIES(brate.pax-str,";") - 1:
                vcXMLText = vcXMLText + '<BaseByGuestAmt AmountAfterTax=' + '"' + ENTRY(i,brate.rmrate-str,";") + '" NumberOfGuests="' + 
                                ENTRY(i,brate.pax-str,";") + '" AgeQualifyingCode="10"/>' + '~n'.
            END.
        IF brate.child-str NE "" THEN
            DO i = 1 TO NUM-ENTRIES(brate.child-str,";") - 1:
                vcXMLText = vcXMLText + '<BaseByGuestAmt AmountAfterTax=' + '"' + ENTRY(i,brate.rmrate-child-str,";") + '" NumberOfGuests="' + 
                                ENTRY(i,brate.child-str,";") + '" AgeQualifyingCode="8"/>' + '~n'.
            END.

        vcXMLText = vcXMLText + '</BaseByGuestAmts>' + '~n' +
                '</Rate>' + '~n' +
            '</Rates>' + '~n' +
        '</RateAmountMessage>' + '~n'.
    END.

    vcXMLText = vcXMLText +
        '</RateAmountMessages>' + '~n' +
        '</OTA_HotelRateAmountNotifRQ>' + '~n' +
        '</soap:Body>' + '~n' +
        '</soap:Envelope>'.
/*
    vcRequest =
        'POST ' + vcWSAgent3 + ' HTTP/1.1' + '~r~n' +
        'Host: ' + vcWebHost + '~r~n' +
        'Content-Type: text/xml;charset=UTF-8' + '~r~n' +
        'Content-Length: ' + STRING(LENGTH(vcXMLText)) + '~r~n' +
        '~r~n'.
*/    
    /* IF roomtypeoutput = "" THEN
        roomtypeoutput = backuproomtype. */

    /*M 240611 -> Debugging to check request to push rates */
    filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\rate_pax_" + in-rmtype + "_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".
    /*
    OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(vcXMLText) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(vcXMLText, i, 1)) FORMAT "x(1)".
        END.        
    OUTPUT STREAM s2 CLOSE.
    */
    
    COPY-LOB vcXMLText TO FILE filenm.
    
    IF debugging-flag = "YES" THEN
    DO:
        RUN logmess("RatePerPax File Has Been Generated").
        IF readaricomboflag = NO OR rateflag = NO THEN
            FOR EACH r-list:
                ASSIGN rcode-rmtype = r-list.rcode + ";" + rm-list.rmtyp.
                RUN if-bookeng-update-aribl.p ON hServer (rcode-rmtype,"ratebyrmtype").
            END.
        ELSE
            DOS SILENT VALUE("DEL " + ratefile).
        IF NOT cUpdAvail THEN
        DO:
            IF readaricomboflag = NO OR allotflag = NO THEN
                RUN if-bookeng-update-aribl.p ON hServer ("","avail").
            ELSE
                DOS SILENT VALUE("DEL " + allotfile).
        END.
        IF re-calculate THEN
            RUN update-bookengine-configbl.p ON hServer (9,hotel.beCode,NO,"").
        IF pushall = YES THEN
            RUN update-bookengine-configbl.p ON hServer (8,hotel.beCode,NO,"").
       /*  IF hotel.ratecounter NE 0 THEN RUN update-xml("rate", "reset"). */ /*move up*/
    END.
    ELSE
    DO:
        IF SEARCH(filenm) = ? THEN 
        DO:
            RUN logmess ("debug: not available file xml rate").
            RUN mt-program.
        END.
    
        EMPTY TEMP-TABLE header-list.
    
        CREATE header-list.
        ASSIGN
            vKey="Content-Type"
            vValue="text/xml;charset=UTF-8".
        RUN logmess("Uploading rates by pax for room type " + in-rmtype + " to Channel Manager..."). 
        RUN http-request-tlsui.p("post",vcWSAgent3,vcxmltext,TABLE header-list,
                                 OUTPUT OTA_HotelRateAmountNotifRS, OUTPUT errorMsg).
       /* MESSAGE STRING(OTA_HotelRateAmountNotifRS) VIEW-AS ALERT-BOX.*/
    
        IF errorMsg NE "" THEN
            RUN logmess(errorMsg + " | " + vcWSagent3).
    
        IF OTA_HotelRateAmountNotifRS MATCHES "*Success*" THEN
        DO:
    		state-attempt = YES.
            RUN logmess("Success Updating Rates " + in-rmtype).
    		IF readaricomboflag = NO OR rateflag = NO THEN
                FOR EACH r-list:
                    ASSIGN rcode-rmtype = r-list.rcode + ";" + rm-list.rmtyp.
                    RUN if-bookeng-update-aribl.p ON hServer (rcode-rmtype,"ratebyrmtype").
                END.
            ELSE
                DOS SILENT VALUE("DEL " + ratefile).
            IF NOT cUpdAvail THEN
            DO:
                IF readaricomboflag = NO OR allotflag = NO THEN
                    RUN if-bookeng-update-aribl.p ON hServer ("","avail").
                ELSE
                    DOS SILENT VALUE("DEL " + allotfile).
            END.
            IF re-calculate THEN
                RUN update-bookengine-configbl.p ON hServer (9,hotel.beCode,NO,"").
            IF pushall = YES THEN
                RUN update-bookengine-configbl.p ON hServer (8,hotel.beCode,NO,"").
            /* IF hotel.ratecounter NE 0 THEN RUN update-xml("rate", "reset"). */ /* move up*/
        END.
        ELSE
        DO:
    		state-attempt = NO.
            RUN logmess("Failed Updating Rates " + in-rmtype).
            IF OTA_HotelRateAmountNotifRS = "" THEN
                RUN logmess ("Check Push Rate Code Mapping Setup").
            ELSE IF NOT OTA_HotelRateAmountNotifRS MATCHES "*Success*" THEN
            DO:
				RUN logmess ("OTA_HotelRateAmountNotifRS==" + OTA_HotelRateAmountNotifRS).
                error-pushrate-file = 
                    workPath + "debug" + STRING(MONTH(TODAY)) + "\Error_rate_pax_" + in-rmtype + "_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".
                /*
                OUTPUT STREAM s2 TO VALUE(error-pushrate-file).
                DO i = 1 TO LENGTH(OTA_HotelRateAmountNotifRS) :
                    PUT STREAM s2 UNFORMATTED STRING(SUBSTR(OTA_HotelRateAmountNotifRS, i, 1)) FORMAT "x(1)".
                END.        
                OUTPUT STREAM s2 CLOSE.
                */
                
                COPY-LOB OTA_HotelRateAmountNotifRS TO FILE error-pushrate-file.
                RUN send-email("Rate", error-pushrate-file, htl-code, "").
            END.
        END.
    END.
END PROCEDURE.

PROCEDURE pull-rsv2:
    DEFINE VARIABLE pull-file       AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE notif-file      AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE notif-resp      AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE pull-txt        AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE notif-txt       AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE ckey            AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE keychar         AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE contchar        AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE dd              AS INTEGER  NO-UNDO INITIAL ?.
    DEFINE VARIABLE mm              AS INTEGER  NO-UNDO INITIAL ?.
    DEFINE VARIABLE yy              AS INTEGER  NO-UNDO INITIAL ?.
    DEFINE VARIABLE qty-booking     AS INTEGER  NO-UNDO INITIAL 0.
    DEFINE VARIABLE qty             AS INT      NO-UNDO INITIAL 0.
    DEFINE VARIABLE created         AS LOGICAL  NO-UNDO INITIAL NO.
    DEFINE VARIABLE ct              AS CHAR     NO-UNDO.
    DEFINE VARIABLE t-guest-nat     AS CHAR.
    DEFINE VARIABLE t-curr-name     AS CHAR.
    DEFINE VARIABLE n-char          AS CHAR.
    DEFINE VARIABLE loopi           AS INT.
    DEFINE VARIABLE list-room       AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE beCode          AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE rtype           AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE rcode           AS CHAR INIT "" NO-UNDO.

    DEFINE VARIABLE rate-code-str   AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE room-type-str   AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE co-date-str     AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE ci-date-str     AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE amount          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE adult           AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE child1          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE child2          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE remark          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE curr-i          AS INTEGER   INIT 0  NO-UNDO.

    DEFINE VARIABLE cDir            AS CHARACTER NO-UNDO.
    DEFINE VARIABLE movedir         AS CHARACTER NO-UNDO.
    DEFINE VARIABLE do-it           AS LOGICAL  NO-UNDO INITIAL NO.    
    DEFINE VARIABLE date1           AS DATE.
    DEFINE VARIABLE date2           AS DATE.

    CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait"). 
    PROCESS EVENTS. 

    IF abi-readmanual-flag = "YES" THEN
    DO:
        cDir = drive + logpath + htl-code + "\RAW\".
        IF SEARCH(cDir) EQ ? THEN OS-COMMAND SILENT VALUE("mkdir " + cDir).
        INPUT FROM OS-DIR (cDir) ECHO.
        REPEAT: 
            CREATE raw-file.
            IMPORT raw-file.filenm.
            FILE-INFO:FILE-NAME = cDir + raw-file.filenm.
            IF FILE-INFO:FILE-NAME BEGINS cdir + "pull1_" THEN
                ASSIGN
                    raw-file.filepath = FILE-INFO:FULL-PATHNAME
                    raw-file.filedate = FILE-INFO:FILE-MOD-DATE
                    raw-file.filetime = FILE-INFO:FILE-MOD-TIME.          
        END.
        FIND FIRST raw-file WHERE raw-file.filenm MATCHES "*pull1_*" NO-LOCK NO-ERROR.
        IF NOT AVAILABLE raw-file THEN
        DO:
            RUN logmess("No Booking..").
            LEAVE.
        END.
    END.
    ELSE
    DO:
        cDir = drive-raw + logpath + htl-code + "\RAW\".
        IF SEARCH(cDir) EQ ? THEN OS-COMMAND SILENT VALUE("mkdir " + cDir).
        INPUT FROM OS-DIR (cDir) ECHO.
        REPEAT: 
            CREATE raw-file.
            IMPORT raw-file.filenm.
            FILE-INFO:FILE-NAME = cDir + raw-file.filenm.
            IF FILE-INFO:FILE-NAME BEGINS cdir + "rsv_" THEN
                ASSIGN
                    raw-file.filepath = FILE-INFO:FULL-PATHNAME
                    raw-file.filedate = FILE-INFO:FILE-MOD-DATE
                    raw-file.filetime = FILE-INFO:FILE-MOD-TIME.          
        END.
        FIND FIRST raw-file WHERE raw-file.filenm MATCHES "*rsv_*" NO-LOCK NO-ERROR.
        IF NOT AVAILABLE raw-file THEN
        DO:
            RUN logmess("No Booking..").
            LEAVE.
        END.
    END.

    FOR EACH raw-file /* WHERE raw-file.filenm MATCHES "*rsv_*" */ BY raw-file.filedate BY raw-file.filetime:
        FOR EACH res-info :
            DELETE res-info.
        END.

        EMPTY TEMP-TABLE res-info.
		EMPTY TEMP-TABLE service-list.
		EMPTY TEMP-TABLE guest-list.
		EMPTY TEMP-TABLE room-list.
		EMPTY TEMP-TABLE buffroom.

        CREATE X-DOCUMENT hXML.
        CREATE X-NODEREF hRoot.        
        /*hXML:LOAD('LONGCHAR', response, FALSE).*/
        hXML:LOAD('file', raw-file.filepath, FALSE).
        hXML:GET-DOCUMENT-ELEMENT(hRoot).
        RUN getChildren(hRoot, 1).
        DELETE OBJECT hXML.
        DELETE OBJECT hRoot.

        FOR EACH room-list:
            DO curr-i = 1 TO room-list.number:
                CREATE buffroom.
                BUFFER-COPY room-list TO buffroom.
            END.        
        END.

        qty-booking = 0.
        qty = 0.
        CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow"). 
        
        FIND FIRST res-info NO-LOCK NO-ERROR.
        IF AVAILABLE res-info THEN do-it = YES.
        
        IF NOT do-it THEN                 
            RUN logmess("Res-Info Not Created").                
        
        IF do-it THEN
        DO:
            FOR EACH res-info NO-LOCK:

                ASSIGN 
                    created = YES 
                    qty-booking = qty-booking + 1 
                    rate-code-str = ""
                    room-type-str = ""
                    ci-date-str   = ""
                    co-date-str   = ""
                    amount        = ""
                    child1        = ""
                    child2        = ""
                    remark        = ""
                .

                FOR EACH buffroom:
                    IF buffroom.rate-code NE "" THEN 
                    DO:
                        FIND FIRST map-list-pull WHERE map-list-pull.ratecdSM = buffroom.rate-code 
                            AND map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
                        IF AVAILABLE map-list-pull THEN buffroom.argtnr = map-list-pull.argtnr.
                    END.
                    ELSE
                    DO:
                        buffroom.rate-code = dyna-code.
                        FIND FIRST map-list-pull WHERE map-list-pull.ratecdVHP = dyna-code
                            AND map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
                        IF AVAILABLE map-list-pull THEN buffroom.argtnr = map-list-pull.argtnr.
                    END.
                    
					/*NC - 20/11/24*/
					FIND FIRST map-list-pull WHERE map-list-pull.ratecdSM = buffroom.rate-code 
					AND map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
					IF AVAILABLE map-list-pull THEN 
					DO:	
						 ASSIGN 
							buffroom.rate-code = TRIM(map-list-pull.ratecdVHP)
							buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(10), "")
							buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(13), "")
							buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(160), "")
							buffroom.rate-code = REPLACE(buffroom.rate-code, "~n", "")
							buffroom.room-type = TRIM(map-list-pull.rmtypeVHP)
							buffroom.room-type = REPLACE(buffroom.room-type, CHR(10), "")
							buffroom.room-type = REPLACE(buffroom.room-type, CHR(13), "")
							buffroom.room-type = REPLACE(buffroom.room-type, CHR(160), "")
							buffroom.room-type = REPLACE(buffroom.room-type, "~n", "")
							.
					END.
					ELSE DO:
						FIND FIRST map-list-pull WHERE map-list-pull.ratecdSM = buffroom.rate-code NO-LOCK NO-ERROR.
						IF AVAILABLE map-list-pull THEN 
							ASSIGN 
							buffroom.rate-code = TRIM(map-list-pull.ratecdVHP)
							buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(10), "")
							buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(13), "")
							buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(160), "")
							buffroom.rate-code = REPLACE(buffroom.rate-code, "~n", "")
							.
						
						FIND FIRST map-list-pull WHERE map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
						IF AVAILABLE map-list-pull THEN 
							ASSIGN 
								buffroom.room-type = TRIM(map-list-pull.rmtypeVHP)
								buffroom.room-type = REPLACE(buffroom.room-type, CHR(10), "")
								buffroom.room-type = REPLACE(buffroom.room-type, CHR(13), "")
								buffroom.room-type = REPLACE(buffroom.room-type, CHR(160), "")
								buffroom.room-type = REPLACE(buffroom.room-type, "~n", "")
								.
					END.
            
                    IF buffroom.ci-date NE "" THEN
                        buffroom.ankunft = DATE(INT(ENTRY(2,buffroom.ci-date,"-")),INT(ENTRY(3,buffroom.ci-date,"-")),INT(ENTRY(1,buffroom.ci-date,"-"))).
                    IF buffroom.co-date NE "" THEN
                        buffroom.abreise = DATE(INT(ENTRY(2,buffroom.co-date,"-")),INT(ENTRY(3,buffroom.co-date,"-")),INT(ENTRY(1,buffroom.co-date,"-"))).
            
                END.           
                                
                RUN logmess ("Storing " + STRING(qty-booking) + " reservation(s) into VHP.").
        
                /*RUN if-siteminder-read-mappingbl.p ON hServer(1, res-info.curr, OUTPUT n-char).
                IF n-char NE "" THEN res-info.curr = n-char.
        
                RUN if-siteminder-read-mappingbl.p ON hServer(2, res-info.country, OUTPUT t-guest-nat).
                IF t-guest-nat NE "" THEN res-info.country = t-guest-nat.*/
        
                IF upperCaseName THEN
                    ASSIGN
                        res-info.given-name = CAPS(res-info.given-name)
                        res-info.sure-name = CAPS(res-info.sure-name)
                    .
        
                EMPTY TEMP-TABLE guest-list1.
                EMPTY TEMP-TABLE service-list1.
                EMPTY TEMP-TABLE room-list1.
                EMPTY TEMP-TABLE temp-res.
               
                FOR EACH buffroom WHERE buffroom.res-id = res-info.res-id AND buffroom.resstatus = res-info.res-status:
                    ASSIGN
                        rate-code-str = rate-code-str + buffroom.rate-code + ";"
                        room-type-str = room-type-str + buffroom.room-type + ";"
                        ci-date-str   = ci-date-str   + buffroom.ci-date   + ";"
                        co-date-str   = co-date-str   + buffroom.co-date   + ";"
                        amount        = amount        + buffroom.amount    + ";"
                        adult         = adult         + STRING(buffroom.adult)     + ";"
                        child1        = child1        + STRING(buffroom.child1)    + ";"
                        child2        = child2        + STRING(buffroom.child2)    + ";"
                        remark        = remark        + buffroom.comment   + ";"
                    .
                    CREATE room-list1.
                    BUFFER-COPY buffroom TO room-list1.
					IF NUM-ENTRIES(buffroom.service,"-") NE 0 THEN /*NC - 12/09/19 service room level*/
					DO:
						DO i = 1 TO NUM-ENTRIES(buffroom.service,"-") - 1:
							FIND FIRST service-list WHERE service-list.res-id = res-info.res-id
								AND service-list.rph = ENTRY(i,buffroom.service,"-") NO-LOCK NO-ERROR.
							IF AVAILABLE service-list THEN
							DO:
								CREATE service-list1.
								BUFFER-COPY service-list TO service-list1.
							END.                                          
						END.
                    END.
					ELSE /*NC - 12/09/19 service reservation level*/
					DO:
						FOR EACH service-list WHERE service-list.res-id = res-info.res-id NO-LOCK:
							CREATE service-list1.
							BUFFER-COPY service-list TO service-list1.
						END.
					END.
                    FIND FIRST guest-list WHERE guest-list.res-id = res-info.res-id
                        AND guest-list.gastnr = buffroom.gastnr NO-LOCK NO-ERROR.
                    IF AVAILABLE guest-list THEN
                    DO:

                        IF upperCaseName THEN
                        ASSIGN
                            guest-list.given-name = CAPS(guest-list.given-name)
                            guest-list.sure-name = CAPS(guest-list.sure-name)
                        .
                        CREATE guest-list1.
                        BUFFER-COPY guest-list TO guest-list1.						
                    END.  
                END.
        
                IF res-info.sure-name = "" AND res-info.given-name = "" THEN
                DO:
                    FIND FIRST guest-list1 WHERE guest-list1.sure-name NE "" AND guest-list1.given-name NE "" AND guest-list1.email NE "" NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE guest-list1 THEN
                        FIND FIRST guest-list1 WHERE guest-list1.sure-name NE "" AND guest-list1.given-name NE "" NO-LOCK NO-ERROR.
                    
                    IF AVAILABLE guest-list1 THEN
                        ASSIGN
                            res-info.sure-name  = guest-list1.sure-name
                            res-info.given-name = guest-list1.given-name
                            res-info.email      = guest-list.email
                            res-info.address1   = guest-list.address1
                            /* res-info.address2   = guest-list.address2 */ 
							/*NC - 07/01/21 - used for store Promotion Code*/
                            res-info.city       = guest-list.city
                            res-info.country    = guest-list.country
                            res-info.zip        = guest-list.zip
                            res-info.phone      = guest-list.phone
                            res-info.country    = guest-list.country.
                END.
                CREATE temp-res.
                BUFFER-COPY res-info TO temp-res.
                IF res-info.res-status = "Reserved" THEN
                DO:        
                                    
                    /* only store booking if it is not reading manual for ABI */
                    IF abi-readmanual-flag NE "YES" THEN
                    DO:
						
                        RUN if-vhp-bookeng-store-resbl.p 
                            ON hServer(INPUT TABLE temp-res, INPUT TABLE room-list1, INPUT TABLE service-list1,
                                   INPUT TABLE guest-list1,"new", dyna-code, hotel.beCode,resnr, chDelimeter,
                                   chDelimeter1, chDelimeter2, chDelimeter3,t-guest-nat, t-curr-name,
                                   OUTPUT error-str, OUTPUT done).

                    END.
                    ELSE done = YES.
        
                    RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).
        
                    IF NOT done THEN
                    DO:
                        DEFINE VARIABLE i AS INT NO-UNDO. 
                        
                        OUTPUT STREAM s2 TO VALUE (workpath + "debug" + STRING(MONTH(TODAY)) + "\" +  res-info.res-id + ".txt").
                        PUT STREAM s2 "res-time: " TRIM(res-info.res-time).
                        
                        PUT STREAM s2 SKIP "rate-code: " TRIM(rate-code-str).
                        
						PUT STREAM s2 SKIP "room-type: " TRIM(room-type-str).
						
                        PUT STREAM s2 SKIP "ci-date: " TRIM(ci-date-str).
						
						PUT STREAM s2 SKIP "co-date: " TRIM(co-date-str).
						
                        PUT STREAM s2 SKIP "amount: " TRIM(amount).
                        
                        PUT STREAM s2 SKIP "curr: " TRIM(res-info.curr).
                        
                        PUT STREAM s2 SKIP "adult: " TRIM(adult).
                        
                        PUT STREAM s2 SKIP "child1: " TRIM(child1).
                        
                        PUT STREAM s2 SKIP "child2: " TRIM(child2).
                        
                        PUT STREAM s2 SKIP "remark: " TRIM(remark).
                        
                        PUT STREAM s2 SKIP "given-name: " TRIM(res-info.given-name).
                        
                        PUT STREAM s2 SKIP "sure-name: " TRIM(res-info.sure-name).
                        
                        PUT STREAM s2 SKIP "phone: " TRIM(res-info.phone).
                       
                        PUT STREAM s2 SKIP "email: " TRIM(res-info.email).
                        
                        PUT STREAM s2 SKIP "address1: " TRIM(res-info.address1).
                        
                        PUT STREAM s2 SKIP "promo-code: " TRIM(res-info.address2).
                        
                        PUT STREAM s2 SKIP "city: " TRIM(res-info.city).
                        
                        PUT STREAM s2 SKIP "zip: " TRIM(res-info.zip).
                        
                        PUT STREAM s2 SKIP "state: " TRIM(res-info.state).
                        
                        PUT STREAM s2 SKIP "country: " TRIM(res-info.country).
                        
                        PUT STREAM s2 SKIP "filename: " errfile.
                       
                        PUT STREAM s2 SKIP.
                        OUTPUT STREAM s2 CLOSE.
                        RUN send-email("Rsv", raw-file.filepath, htl-code, "").
                        movedir = drive + logpath + htl-code + "\debug" + STRING(MONTH(TODAY)) + "\Error_" + ENTRY(1, raw-file.filenm, ".") /* + "_" + res-info.res-id*/ + ".xml".
                    END.
                    ELSE
                    DO: 
                        IF NOT error-str MATCHES "*already exist*" THEN
                            RUN logmess(STRING(qty-booking) + " reservation(s) created.").
                                                        
                        movedir = drive + logpath + htl-code + "\debug" + STRING(MONTH(TODAY)) + "\" + ENTRY(1, raw-file.filenm, ".") /* + "_" + res-info.res-id */ + ".xml".
                        IF hotel.rsvcounter NE 0 THEN RUN update-xml("rsv", "reset").
                    END.

                    /* only send notif if it is not reading manual for ABI */
                    IF abi-readmanual-flag NE "YES" THEN
                    DO:
                        RUN logmess("NOTIF the reservation...").
                        RUN call-NotifReportRQ(res-info.res-id, res-info.res-time,res-info.res-status). 
                    END.
                    OS-COPY VALUE(raw-file.filepath) VALUE(movedir).                    
                    IF SEARCH(movedir) NE ? THEN
                        DOS SILENT DEL VALUE(raw-file.filepath).
                END.
                ELSE IF res-info.res-status = "Modify" THEN
                DO: 
                    /* only store booking if it is not reading manual for ABI */
                    IF abi-readmanual-flag NE "YES" THEN
                    DO:
                        RUN if-vhp-bookeng-modifybl.p ON hServer(INPUT TABLE temp-res, TABLE room-list1, TABLE service-list1,
                            TABLE guest-list1,hotel.becode, t-guest-nat, t-curr-name, dyna-code, chDelimeter, 
                            chDelimeter1, chDelimeter2, chDelimeter3, OUTPUT error-str, OUTPUT done). 
                    END.
                    ELSE done = YES.
					IF error-str NE "" THEN RUN logmess(error-str).
                    RUN logmess(res-info.res-id + " Modified = " + STRING(done)). 

                    /* request dari client penambahan fitur jika modify reservation not found maka di create reservasi baru -   30/11/2022 */
                    IF error-str MATCHES "*Reservation " + res-info.res-id + " not found*" THEN
                    DO:
                        RUN logmess("Modify Booking Failed: Data Not Found... Storing As New Booking").
        
                        RUN if-vhp-bookeng-store-resbl.p 
                        ON hServer(INPUT TABLE temp-res, INPUT TABLE room-list1, INPUT TABLE service-list1,
                                   INPUT TABLE guest-list1,"new", dyna-code, hotel.beCode,resnr, chDelimeter,
                                   chDelimeter1, chDelimeter2, chDelimeter3,t-guest-nat, t-curr-name,
                                   OUTPUT error-str, OUTPUT done).
        
                        RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).
                    END.

                    IF done = NO THEN
                    DO:                        
                        RUN send-email("Rsv", raw-file.filepath, htl-code, "").
                        movedir = drive + logpath + htl-code + "\debug" + STRING(MONTH(TODAY)) + "\Error_" + ENTRY(1, raw-file.filenm, ".") /* + "_" + res-info.res-id */ + ".xml".
                    END.  
                    ELSE
                    DO:                                                                                                                               
                        movedir = drive + logpath + htl-code + "\debug" + STRING(MONTH(TODAY)) + "\" + ENTRY(1, raw-file.filenm, ".") /* + "_" + res-info.res-id */ + ".xml".
                        IF hotel.rsvcounter NE 0 THEN RUN update-xml("rsv", "reset").
                    END.   

                    /* only send notif if it is not reading manual for ABI */
                    IF abi-readmanual-flag NE "YES" THEN
                    DO:
                        RUN logmess("NOTIF Modified reservation...").
                        RUN call-NotifReportRQ(res-info.res-id, res-info.res-time,res-info.res-status). 
                    END.
                    OS-COPY VALUE(raw-file.filepath) VALUE(movedir).                    
                    IF SEARCH(movedir) NE ? THEN
                        DOS SILENT DEL VALUE(raw-file.filepath).
                END.
                ELSE IF res-info.res-status = "Cancel" THEN
                DO:
                    /* only store booking if it is not reading manual for ABI */
                    IF abi-readmanual-flag NE "YES" THEN
                    DO:
                        RUN if-vhp-bookeng-cancelbl.p ON hServer(hotel.becode, res-info.res-id, res-info.ota-code, 
                            OUTPUT done, OUTPUT error-str).
                    END.
                    ELSE done = YES.
                    IF error-str NE "" THEN RUN logmess(error-str).
                    RUN logmess(res-info.res-id + " Cancelled = " + STRING(done)).

                    IF done = NO THEN
                    DO:                        
                        RUN send-email("Rsv", raw-file.filepath, htl-code, "").
                        movedir = drive + logpath + htl-code + "\debug" + STRING(MONTH(TODAY)) + "\Error_" + ENTRY(1, raw-file.filenm, ".") /* + "_" + res-info.res-id */ + ".xml".
                    END.                            
                    ELSE                    
                    DO: 
                        movedir = drive + logpath + htl-code + "\debug" + STRING(MONTH(TODAY)) + "\" + ENTRY(1, raw-file.filenm, ".") /* + "_" + res-info.res-id */ +  ".xml".
                        IF hotel.rsvcounter NE 0 THEN RUN update-xml("rsv", "reset").
                    END.
                      
                    /* only send notif if it is not reading manual for ABI */
                    IF abi-readmanual-flag NE "YES" THEN
                    DO:
                        RUN logmess("NOTIF Cancelled reservation...").
                        RUN call-NotifReportRQ(res-info.res-id, res-info.res-time,res-info.res-status). 
                    END.

                    OS-COPY VALUE(raw-file.filepath) VALUE(movedir).                    
                    IF SEARCH(movedir) NE ? THEN
                        DOS SILENT DEL VALUE(raw-file.filepath).
                END.
        
                RUN logmess2("PULL|" + "TM"   + chDelimeter1 + res-info.res-time       + chDelimeter2 
                                     + "RI"   + chDelimeter1 + res-info.res-id         + chDelimeter2 
                                     + "OC"   + chDelimeter1 + res-info.ota-code       + chDelimeter2 
                                     + "RC"   + chDelimeter1 + rate-code-str           + chDelimeter2 
                                     + "RT"   + chDelimeter1 + room-type-str           + chDelimeter2 
                                     + "CI"   + chDelimeter1 + ci-date-str             + chDelimeter2 
                                     + "CO"   + chDelimeter1 + co-date-str             + chDelimeter2 
                                     + "AM"   + chDelimeter1 + amount                  + chDelimeter2 
                                     + "CU"   + chDelimeter1 + res-info.curr           + chDelimeter2 
                                     + "AD"   + chDelimeter1 + adult                   + chDelimeter2 
                                     + "CH1"  + chDelimeter1 + child1                  + chDelimeter2 
                                     + "CH2"  + chDelimeter1 + child2                  + chDelimeter2 
                                     + "RM"   + chDelimeter1 + remark                  + chDelimeter2 
                                     + "GN"   + chDelimeter1 + res-info.given-name     + chDelimeter2 
                                     + "SN"   + chDelimeter1 + res-info.sure-name      + chDelimeter2 
                                     + "PH"   + chDelimeter1 + res-info.phone          + chDelimeter2 
                                     + "EM"   + chDelimeter1 + res-info.email          + chDelimeter2 
                                     + "ADR1" + chDelimeter1 + res-info.address1       + chDelimeter2 
                                     + "PRM"  + chDelimeter1 + res-info.address2       + chDelimeter2 
                                     + "CIT"  + chDelimeter1 + res-info.city           + chDelimeter2 
                                     + "ZIP"  + chDelimeter1 + res-info.zip            + chDelimeter2 
                                     + "ST"   + chDelimeter1 + res-info.state          + chDelimeter2 
                                     + "COU"  + chDelimeter1 + res-info.country        + chDelimeter2 
                             ).                            

                /* for Artotel Corporate database ABI */
                CREATE brs-data.
                ASSIGN
                    brs-data.hotelid = hotel.htlcode
                    brs-data.ota-code = res-info.ota-code
                    brs-data.res-status = res-info.res-status
                    brs-data.res-id = res-info.res-id
                    brs-data.createdate = raw-file.filedate
                    brs-data.cidate = 01/01/3000
                    brs-data.codate = 01/01/1970
                    brs-data.firstname = res-info.given-name
                    brs-data.lastname = res-info.sure-name.
        
                FOR EACH buffroom WHERE buffroom.res-id = res-info.res-id AND buffroom.resstatus = res-info.res-status NO-LOCK:
                    DO i = 1 TO NUM-ENTRIES(buffroom.amount, "-") - 1:
                        brs-data.roomrate = brs-data.roomrate + DECIMAL(ENTRY(i,buffroom.amount,"-")).

                        RUN find-start-date(buffroom.ankunft, brs-data.cidate, OUTPUT date1).
                        brs-data.cidate = date1.
                        RUN find-end-date(buffroom.abreise, brs-data.codate, OUTPUT date2).
                        brs-data.codate = date2.
                    END.
                END.

            END.
        END.
    END.
    
    EMPTY TEMP-TABLE res-info.
    EMPTY TEMP-TABLE buffroom.
    EMPTY TEMP-TABLE service-list.
    EMPTY TEMP-TABLE guest-list.
    EMPTY TEMP-TABLE raw-file.
END PROCEDURE.

PROCEDURE pull-rsv:
    DEFINE VARIABLE pull-file       AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE notif-file      AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE notif-resp      AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE pull-txt        AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE notif-txt       AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE ckey            AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE keychar         AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE contchar        AS CHAR     NO-UNDO INITIAL "".
    DEFINE VARIABLE dd              AS INTEGER  NO-UNDO INITIAL ?.
    DEFINE VARIABLE mm              AS INTEGER  NO-UNDO INITIAL ?.
    DEFINE VARIABLE yy              AS INTEGER  NO-UNDO INITIAL ?.
    DEFINE VARIABLE qty-booking     AS INTEGER  NO-UNDO INITIAL 0.
    DEFINE VARIABLE qty             AS INT      NO-UNDO INITIAL 0.
    DEFINE VARIABLE created         AS LOGICAL  NO-UNDO INITIAL NO.
    DEFINE VARIABLE ct              AS CHAR     NO-UNDO.
    DEFINE VARIABLE t-guest-nat     AS CHAR.
    DEFINE VARIABLE t-curr-name     AS CHAR.
    DEFINE VARIABLE n-char          AS CHAR.
    DEFINE VARIABLE loopi           AS INT.
    DEFINE VARIABLE list-room       AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE beCode          AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE rtype           AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE rcode           AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE msg-str         AS CHAR INIT "" NO-UNDO.
    DEFINE VARIABLE ori-resid       AS CHAR INIT "" NO-UNDO.

    DEFINE VARIABLE rate-code-str   AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE room-type-str   AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE co-date-str     AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE ci-date-str     AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE amount          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE adult           AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE child1          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE child2          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE remark          AS CHARACTER INIT "" NO-UNDO.
    DEFINE VARIABLE date1           AS DATE.
    DEFINE VARIABLE date2           AS DATE.

    CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait"). 
    PROCESS EVENTS. 
    RUN mt-pull.
    qty-booking = 0.
    qty = 0.
    CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").

    FOR EACH buffroom:
        IF buffroom.rate-code NE "" THEN 
        DO:
            FIND FIRST map-list-pull WHERE map-list-pull.ratecdSM = buffroom.rate-code 
                AND map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
            IF AVAILABLE map-list-pull THEN buffroom.argtnr = map-list-pull.argtnr.
        END.
        ELSE
        DO:
            buffroom.rate-code = dyna-code.
            FIND FIRST map-list-pull WHERE map-list-pull.ratecdVHP = dyna-code
                AND map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
            IF AVAILABLE map-list-pull THEN buffroom.argtnr = map-list-pull.argtnr.
        END.
        

        FIND FIRST map-list-pull WHERE map-list-pull.ratecdSM = buffroom.rate-code NO-LOCK NO-ERROR.
        IF AVAILABLE map-list-pull THEN 
                ASSIGN 
                buffroom.rate-code = TRIM(map-list-pull.ratecdVHP)
                buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(10), "")
                buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(13), "")
                buffroom.rate-code = REPLACE(buffroom.rate-code, CHR(160), "")
                buffroom.rate-code = REPLACE(buffroom.rate-code, "~n", "")
                .
        
        FIND FIRST map-list-pull WHERE map-list-pull.rmtypeSM = buffroom.room-type NO-LOCK NO-ERROR.
        IF AVAILABLE map-list-pull THEN 
             ASSIGN 
                buffroom.room-type = TRIM(map-list-pull.rmtypeVHP)
                buffroom.room-type = REPLACE(buffroom.room-type, CHR(10), "")
                buffroom.room-type = REPLACE(buffroom.room-type, CHR(13), "")
                buffroom.room-type = REPLACE(buffroom.room-type, CHR(160), "")
                buffroom.room-type = REPLACE(buffroom.room-type, "~n", "")
                .

        IF buffroom.ci-date NE "" THEN
            buffroom.ankunft = DATE(INT(ENTRY(2,buffroom.ci-date,"-")),INT(ENTRY(3,buffroom.ci-date,"-")),INT(ENTRY(1,buffroom.ci-date,"-"))).
        IF buffroom.co-date NE "" THEN
            buffroom.abreise = DATE(INT(ENTRY(2,buffroom.co-date,"-")),INT(ENTRY(3,buffroom.co-date,"-")),INT(ENTRY(1,buffroom.co-date,"-"))).

    END.

    FIND FIRST res-info NO-LOCK NO-ERROR.
    IF NOT AVAILABLE res-info THEN
    DO:
        RUN logmess("No Booking..").
        LEAVE.
    END.

    FOR EACH res-info NO-LOCK:
        ASSIGN 
            created = YES 
            qty-booking = qty-booking + 1 
            rate-code-str = ""
            room-type-str = ""
            ci-date-str   = ""
            co-date-str   = ""
            amount        = ""
            child1        = ""
            child2        = ""
            remark        = ""
        .
        RUN logmess ("Storing " + STRING(qty-booking) + " reservation(s) into VHP.").

        /*RUN if-siteminder-read-mappingbl.p ON hServer(1, res-info.curr, OUTPUT n-char).
        IF n-char NE "" THEN res-info.curr = n-char.

        RUN if-siteminder-read-mappingbl.p ON hServer(2, res-info.country, OUTPUT t-guest-nat).
        IF t-guest-nat NE "" THEN res-info.country = t-guest-nat.*/

        IF upperCaseName THEN
            ASSIGN
                res-info.given-name = CAPS(res-info.given-name)
                res-info.sure-name = CAPS(res-info.sure-name)
            .

        EMPTY TEMP-TABLE guest-list1.
        EMPTY TEMP-TABLE service-list1.
        EMPTY TEMP-TABLE room-list1.
        EMPTY TEMP-TABLE temp-res.

        FOR EACH buffroom WHERE buffroom.res-id = res-info.res-id AND buffroom.resstatus = res-info.res-status:
            ASSIGN
                rate-code-str = rate-code-str + buffroom.rate-code + ";"
                room-type-str = room-type-str + buffroom.room-type + ";"
                ci-date-str   = ci-date-str   + buffroom.ci-date   + ";"
                co-date-str   = co-date-str   + buffroom.co-date   + ";"
                amount        = amount        + buffroom.amount    + ";"
                adult         = adult         + STRING(buffroom.adult)     + ";"
                child1        = child1        + STRING(buffroom.child1)    + ";"
                child2        = child2        + STRING(buffroom.child2)    + ";"
                remark        = remark        + buffroom.comment   + ";"
            .
            CREATE room-list1.
			BUFFER-COPY buffroom TO room-list1.
			IF NUM-ENTRIES(buffroom.service,"-") NE 0 THEN /*NC - 12/09/19 service room level*/
			DO:
				DO i = 1 TO NUM-ENTRIES(buffroom.service,"-") - 1:
					FIND FIRST service-list WHERE service-list.res-id = res-info.res-id
						AND service-list.rph = ENTRY(i,buffroom.service,"-") NO-LOCK NO-ERROR.
					IF AVAILABLE service-list THEN
					DO:
						CREATE service-list1.
						BUFFER-COPY service-list TO service-list1.
					END.                                          
				END.
			END.
			ELSE /*NC - 12/09/19 service reservation level*/
			DO:
				FOR EACH service-list WHERE service-list.res-id = res-info.res-id AND service-list.amountaftertax GT 0 NO-LOCK:
					IF AVAILABLE service-list THEN
					DO:
						CREATE service-list1.
						BUFFER-COPY service-list TO service-list1.
					END.
				END.
			END.
            
            FIND FIRST guest-list WHERE guest-list.res-id = res-info.res-id
                AND guest-list.gastnr = buffroom.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest-list THEN
            DO:
                IF upperCaseName THEN
                ASSIGN
                    guest-list.given-name = CAPS(guest-list.given-name)
                    guest-list.sure-name = CAPS(guest-list.sure-name)
                .
                CREATE guest-list1.
                BUFFER-COPY guest-list TO guest-list1.
            END.  
        END.

        IF res-info.sure-name = "" AND res-info.given-name = "" THEN
        DO:                                                                                                                    
            FIND FIRST guest-list1 WHERE guest-list1.sure-name NE "" AND guest-list1.given-name NE "" AND guest-list1.email NE "" NO-LOCK NO-ERROR.
            IF NOT AVAILABLE guest-list1 THEN
                FIND FIRST guest-list1 WHERE guest-list1.sure-name NE "" AND guest-list1.given-name NE "" NO-LOCK NO-ERROR.
            
            IF AVAILABLE guest-list1 THEN
                ASSIGN
                    res-info.sure-name  = guest-list1.sure-name
                    res-info.given-name = guest-list1.given-name
                    res-info.email      = guest-list.email
                    res-info.address1   = guest-list.address1
                    /* res-info.address2   = guest-list.address2 */ 
					/*NC - 07/01/21 - used for store Promotion Code*/
                    res-info.city       = guest-list.city
                    res-info.country    = guest-list.country
                    res-info.zip        = guest-list.zip
                    res-info.phone      = guest-list.phone
                    res-info.country    = guest-list.country.
        END.
        CREATE temp-res.
        BUFFER-COPY res-info TO temp-res.
        IF res-info.res-status = "Reserved" THEN
        DO:
            RUN if-vhp-bookeng-store-resbl.p 
                ON hServer(INPUT TABLE temp-res, INPUT TABLE room-list1, INPUT TABLE service-list1,
                           INPUT TABLE guest-list1,"new", dyna-code, hotel.beCode,resnr, chDelimeter,
                           chDelimeter1, chDelimeter2, chDelimeter3,t-guest-nat, t-curr-name,
                           OUTPUT error-str, OUTPUT done).

            RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).

            IF NOT done THEN
            DO:
                DEFINE VARIABLE i AS INT NO-UNDO. 
                OUTPUT STREAM s2 TO VALUE (workpath + "debug" + STRING(MONTH(TODAY)) + "\" +  res-info.res-id + ".txt").
                
                PUT STREAM s2 "res-time: " TRIM(res-info.res-time).
                        
                PUT STREAM s2 SKIP "rate-code: " TRIM(rate-code-str).
                
                PUT STREAM s2 SKIP "room-type: " TRIM(room-type-str).
                
                PUT STREAM s2 SKIP "ci-date: " TRIM(ci-date-str).
                
                PUT STREAM s2 SKIP "co-date: " TRIM(co-date-str).
                
                PUT STREAM s2 SKIP "amount: " TRIM(amount).
                
                PUT STREAM s2 SKIP "curr: " TRIM(res-info.curr).
                
                PUT STREAM s2 SKIP "adult: " TRIM(adult).
                
                PUT STREAM s2 SKIP "child1: " TRIM(child1).
                
                PUT STREAM s2 SKIP "child2: " TRIM(child2).
                
                PUT STREAM s2 SKIP "remark: " TRIM(remark).
                
                PUT STREAM s2 SKIP "given-name: " TRIM(res-info.given-name).
                
                PUT STREAM s2 SKIP "sure-name: " TRIM(res-info.sure-name).
                
                PUT STREAM s2 SKIP "phone: " TRIM(res-info.phone).
               
                PUT STREAM s2 SKIP "email: " TRIM(res-info.email).
                
                PUT STREAM s2 SKIP "address1: " TRIM(res-info.address1).
                
                PUT STREAM s2 SKIP "promo-code: " TRIM(res-info.address2).
                
                PUT STREAM s2 SKIP "city: " TRIM(res-info.city).
                
                PUT STREAM s2 SKIP "zip: " TRIM(res-info.zip).
                
                PUT STREAM s2 SKIP "state: " TRIM(res-info.state).
                
                PUT STREAM s2 SKIP "country: " TRIM(res-info.country).
                
                PUT STREAM s2 SKIP "filename: " errfile.
               
                PUT STREAM s2 SKIP.
                OUTPUT STREAM s2 CLOSE.

            END.
            ELSE
            DO: 
                IF NOT error-str MATCHES "*already exist*" THEN
                    RUN logmess(STRING(qty-booking) + " reservation(s) created.").
            END.

			RUN logmess("NOTIF the reservation...").
            RUN call-NotifReportRQ(res-info.res-id, res-info.res-time,res-info.res-status).
        END.
        ELSE IF res-info.res-status = "Modify" THEN
        DO:            
            RUN if-vhp-bookeng-modifybl.p ON hServer(INPUT TABLE temp-res, TABLE room-list1, TABLE service-list1,
                TABLE guest-list1,hotel.becode, t-guest-nat, t-curr-name, dyna-code, chDelimeter, 
                chDelimeter1, chDelimeter2, chDelimeter3, OUTPUT error-str, OUTPUT done). 

            ori-resid = res-info.res-id.
            IF done = YES OR error-str MATCHES "*Reservation " + res-info.res-id + " not found*" THEN
            DO:
                IF done = NO THEN
                DO:
                    RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).

                    FIND FIRST notif-list WHERE notif-list.otaid = res-info.res-id NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE notif-list THEN
                    DO:
                        FIND FIRST notif-list WHERE notif-list.cmid = res-info.res-id NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE notif-list THEN
                            temp-res.res-id = notif-list.cmid.
                        ELSE
                            temp-res.res-id = notif-list.cmid.
                    END.
                    ELSE
                    DO:
                        temp-res.res-id = notif-list.cmid.
                    END.

                    RUN logmess("Retry Storing " + res-info.res-status + " Data " + res-info.res-id + " with ID " + temp-res.res-id).
                    res-info.res-id = temp-res.res-id.

                    RUN if-vhp-bookeng-modifybl.p ON hServer(INPUT TABLE temp-res, TABLE room-list1, TABLE service-list1,
                        TABLE guest-list1,hotel.becode, t-guest-nat, t-curr-name, dyna-code, chDelimeter, 
                        chDelimeter1, chDelimeter2, chDelimeter3, OUTPUT error-str, OUTPUT done). 

                    IF done = YES OR error-str MATCHES "*Reservation " + res-info.res-id + " not found*" THEN
                    DO:
                        IF done = NO THEN
                            RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).
                        ELSE
                            RUN logmess(res-info.res-id + " Modified = " + STRING(done)).
                    END.
                    ELSE IF done = NO THEN
                        RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).
                END.
                ELSE 
                    RUN logmess(res-info.res-id + " Modified = " + STRING(done)).
            END.
            ELSE IF done = NO THEN
                RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).

            /* request dari client penambahan fitur jika modify reservation not found maka di create reservasi baru - CRG 30/11/2022 */
            IF error-str MATCHES "*Reservation " + res-info.res-id + " not found*" THEN
            DO:
                res-info.res-id = ori-resid.
                temp-res.res-id = ori-resid.
                /* res-status tetap modify karena notify modify booking bukan new booking */
                RUN logmess("Modify Booking Failed: Data Not Found... Storing As New Booking").

                RUN if-vhp-bookeng-store-resbl.p 
                ON hServer(INPUT TABLE temp-res, INPUT TABLE room-list1, INPUT TABLE service-list1,
                           INPUT TABLE guest-list1,"new", dyna-code, hotel.beCode,resnr, chDelimeter,
                           chDelimeter1, chDelimeter2, chDelimeter3,t-guest-nat, t-curr-name,
                           OUTPUT error-str, OUTPUT done).

                RUN logmess(error-str + " DONE = " + STRING(done) + " " + res-info.res-id).
            END.

            RUN logmess("NOTIF Modified reservation...").
            RUN call-NotifReportRQ(res-info.res-id, res-info.res-time,res-info.res-status).
        END.
        ELSE IF res-info.res-status = "Cancel" THEN
        DO:
            RUN if-vhp-bookeng-cancelbl.p ON hServer(hotel.becode, res-info.res-id, res-info.ota-code, 
                OUTPUT done, OUTPUT error-str).
            
            IF done = YES OR error-str MATCHES "*Reservation " + res-info.res-id + " not found*" THEN
            DO: 
                IF done = NO THEN
                DO:
                    RUN logmess(error-str + " DONE = " + STRING(done)).

                    FIND FIRST notif-list WHERE notif-list.otaid = res-info.res-id NO-LOCK NO-ERROR.
                    IF NOT AVAILABLE notif-list THEN
                    DO:
                        FIND FIRST notif-list WHERE notif-list.cmid = res-info.res-id NO-LOCK NO-ERROR.
                        IF NOT AVAILABLE notif-list THEN
                            temp-res.res-id = notif-list.cmid.
                        ELSE
                            temp-res.res-id = notif-list.cmid.
                    END.
                    ELSE
                    DO:
                        temp-res.res-id = notif-list.cmid.
                    END.

                    RUN logmess("Retry Storing " + res-info.res-status + " Data " + res-info.res-id + " with ID " + temp-res.res-id).
                    res-info.res-id = temp-res.res-id.

                    RUN if-vhp-bookeng-cancelbl.p ON hServer(hotel.becode, res-info.res-id, res-info.ota-code, 
                        OUTPUT done, OUTPUT error-str).

                    IF done = YES OR error-str MATCHES "*Reservation " + res-info.res-id + " not found*" THEN
                    DO: 
                        IF done = NO THEN
                            RUN logmess(error-str + " DONE = " + STRING(done)).
                        ELSE
                            RUN logmess(res-info.res-id + " Cancelled = " + STRING(done)).
                    END.
                    ELSE IF done = NO THEN
                        RUN logmess(error-str + " DONE = " + STRING(done)).
                END.
                ELSE
                    RUN logmess(res-info.res-id + " Cancelled = " + STRING(done)).
            END.
            ELSE IF done = NO THEN
                RUN logmess(error-str + " DONE = " + STRING(done)).

            RUN logmess("NOTIF Cancelled reservation...").
            RUN call-NotifReportRQ(res-info.res-id, res-info.res-time,res-info.res-status).
        END.

        IF done = NO THEN
            RUN send-email("Rsv", errfile, htl-code, "").
        ELSE 
        DO:
            IF hotel.rsvcounter NE 0 THEN RUN update-xml("rsv", "reset").
        END.

        RUN logmess2("PULL|" + "TM"   + chDelimeter1 + res-info.res-time       + chDelimeter2 
                             + "RI"   + chDelimeter1 + res-info.res-id         + chDelimeter2 
                             + "OC"   + chDelimeter1 + res-info.ota-code       + chDelimeter2 
                             + "RC"   + chDelimeter1 + rate-code-str           + chDelimeter2 
                             + "RT"   + chDelimeter1 + room-type-str           + chDelimeter2 
                             + "CI"   + chDelimeter1 + ci-date-str             + chDelimeter2 
                             + "CO"   + chDelimeter1 + co-date-str             + chDelimeter2 
                             + "AM"   + chDelimeter1 + amount                  + chDelimeter2 
                             + "CU"   + chDelimeter1 + res-info.curr           + chDelimeter2 
                             + "AD"   + chDelimeter1 + adult                   + chDelimeter2 
                             + "CH1"  + chDelimeter1 + child1                  + chDelimeter2 
                             + "CH2"  + chDelimeter1 + child2                  + chDelimeter2 
                             + "RM"   + chDelimeter1 + remark                  + chDelimeter2 
                             + "GN"   + chDelimeter1 + res-info.given-name     + chDelimeter2 
                             + "SN"   + chDelimeter1 + res-info.sure-name      + chDelimeter2 
                             + "PH"   + chDelimeter1 + res-info.phone          + chDelimeter2 
                             + "EM"   + chDelimeter1 + res-info.email          + chDelimeter2 
                             + "ADR1" + chDelimeter1 + res-info.address1       + chDelimeter2 
                             + "PRM"  + chDelimeter1 + res-info.address2       + chDelimeter2 
                             + "CIT"  + chDelimeter1 + res-info.city           + chDelimeter2 
                             + "ZIP"  + chDelimeter1 + res-info.zip            + chDelimeter2 
                             + "ST"   + chDelimeter1 + res-info.state          + chDelimeter2 
                             + "COU"  + chDelimeter1 + res-info.country        + chDelimeter2 
                     ).

    END.
    
    FOR EACH res-info:
        CREATE brs-data.
        ASSIGN
            brs-data.hotelid = hotel.htlcode
            brs-data.ota-code = res-info.ota-code
            brs-data.res-status = res-info.res-status
            brs-data.res-id = res-info.res-id
            brs-data.createdate = ?
            brs-data.cidate = 01/01/3000
            brs-data.codate = 01/01/1970
            brs-data.firstname = res-info.given-name
            brs-data.lastname = res-info.sure-name.

        FOR EACH buffroom WHERE buffroom.res-id = res-info.res-id AND buffroom.resstatus = res-info.res-status NO-LOCK:
            DO i = 1 TO NUM-ENTRIES(buffroom.amount, "-") - 1:
                brs-data.roomrate = brs-data.roomrate + DECIMAL(ENTRY(i,buffroom.amount,"-")).

                RUN find-start-date(buffroom.ankunft, brs-data.cidate, OUTPUT date1).
                brs-data.cidate = date1.
                RUN find-end-date(buffroom.abreise, brs-data.codate, OUTPUT date2).
                brs-data.codate = date2.
            END.
        END.
    END.

    EMPTY TEMP-TABLE res-info.
    EMPTY TEMP-TABLE buffroom.
    EMPTY TEMP-TABLE service-list.
    EMPTY TEMP-TABLE guest-list.
END PROCEDURE.

PROCEDURE send-email:
    DEFINE INPUT PARAMETER case-type AS CHAR. /* "rsv" , "avail" , "rate" , "error" */
    DEFINE INPUT PARAMETER email-attachment AS CHAR.
    DEFINE INPUT PARAMETER hotelcode AS CHAR.
    DEFINE INPUT PARAMETER customreply AS CHAR.
    DEFINE VARIABLE sgbody          AS CHAR                                 NO-UNDO.
    DEFINE VARIABLE total-receiver  AS INTEGER                              NO-UNDO.
    DEFINE VARIABLE count-receiver  AS INTEGER                              NO-UNDO.
    DEFINE VARIABLE sender          AS CHAR FORMAT "x(45)"                  NO-UNDO.
    DEFINE VARIABLE receiver        AS CHAR     NO-UNDO INIT " ".

    DEFINE VARIABLE chWord      AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE chtext      AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE olMail      AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE ch-smtp     AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE ch-ssl      AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE ch-msg      AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE att         AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE filenm1     AS CHAR.
    DEFINE VARIABLE filenm2     AS CHAR.
    DEFINE VARIABLE file-other  AS CHAR.
    DEFINE VARIABLE ch-imap     AS COM-HANDLE   NO-UNDO.
    DEFINE VARIABLE loopi       AS INTEGER      NO-UNDO.

    DEFINE VARIABLE serveraddress   AS CHARACTER.
    DEFINE VARIABLE portaddress     AS CHARACTER.
    DEFINE VARIABLE username        AS CHARACTER.
    DEFINE VARIABLE password        AS CHARACTER.
    DEFINE VARIABLE filepath        AS CHARACTER.
    DEFINE VARIABLE filepath1       AS CHARACTER.
    DEFINE VARIABLE subject         AS CHARACTER. 
    DEFINE VARIABLE send-email      AS LOGICAL INIT YES.
    DEFINE VARIABLE varcounter      AS LOGICAL INIT YES.
    DEFINE VARIABLE mess-str        AS CHARACTER.
    DEFINE VARIABLE fletter         AS CHARACTER.
    
    DEFINE VARIABLE success-flag    AS LOGICAL      NO-UNDO INIT NO.
    DEFINE VARIABLE enableSSL       AS LOGICAL      NO-UNDO INIT YES.
    DEFINE VARIABLE curr-sender     AS CHARACTER    NO-UNDO.    
    DEFINE VARIABLE curr-guest      AS CHARACTER NO-UNDO.
    DEFINE VARIABLE msg-str         AS CHARACTER NO-UNDO.

    /* BLY 04/06/2025 
    FIND FIRST preference-list NO-LOCK NO-ERROR.
	IF AVAILABLE preference-list THEN
		ASSIGN 
			email-username = preference-list.email
			email-password = preference-list.pass
			email-server = preference-list.email-server
			email-port = preference-list.email-port
		.
	ELSE RUN readSession2.
    */
	
    IF hotelcode = "" THEN hotelcode = hotel.htlcode.

    IF email-username EQ "" OR email-password EQ "" OR email-server EQ "" OR email-port EQ 0 OR emailadr EQ "" THEN
    DO:
        send-email = NO.
        mess-str = CHR(40) + case-type + CHR(41) + " Email Credentials Not Defined".
    END.
/* NC - No used anymore since email will be loop together with push avail / rates
    IF send-email  THEN
    DO:
        IF case-type = "Rsv" THEN
        DO:
            IF hotel.rsvcounter GT 3 THEN ASSIGN send-email = NO.
        END.
        IF case-type = "Avail" THEN
        DO:
            IF hotel.availcounter GT 3 THEN ASSIGN send-email = NO.
        END.
        IF case-type = "Rate" THEN
        DO:
            IF hotel.ratecounter GT 3 THEN ASSIGN send-email = NO.
        END.
        IF case-type = "Error" THEN
        DO:
            IF hotel.errorcounter GT 3 THEN ASSIGN send-email = NO.
        END.

        IF send-email = NO THEN mess-str = "".
    END.
*/
    IF send-email EQ NO THEN
    DO:
        IF mess-str NE "" THEN
            RUN logmess(mess-str).
        RETURN.
    END.
    ELSE
    DO:
        IF enableSSl THEN                                                                                       
            CREATE "MailBee.ssl" ch-ssl.                                                                        
                                                                                                                 
        CREATE "MailBee.message" ch-msg.                                                                                
        CREATE "MailBee.attachment" att.                                                                      
        CREATE "MailBee.SMTP" ch-smtp.                                                                          
        CREATE "MailBee.Imap4" ch-imap.
    
        ASSIGN
            ch-smtp:liCenseKey = "MBC500-E1E13887DE-357907CCE837FA2FA77F244275613246"
            ch-imap:licenseKey = "MBC500-E1E13887DE-357907CCE837FA2FA77F244275613246".
    
        IF enableSSl THEN
        DO:
            ASSIGN
                ch-ssl:liCenseKey = "MBC500-E1E13887DE-357907CCE837FA2FA77F244275613246".
    
            IF NOT ch-ssl:licensed THEN
            DO:
                RUN logmess("ERR;" + "SSL License key is invalid or expired").
                RETURN.
            END.
        END.          

        IF NOT emailadr MATCHES "*@*" AND NOT emailadr MATCHES "*.*" THEN
            RUN logmess("Incorrect Email Format").
        ELSE
        DO:
            IF enableSSl THEN 
                ASSIGN ch-smtp:ssl = ch-ssl.
            
            ASSIGN
                ch-smtp:serverName = email-server
                ch-smtp:portNumber = email-port
                ch-smtp:AuthMethod = 2
                ch-smtp:fromAddr   = email-username
                ch-smtp:UserName   = email-username
                ch-smtp:password   = email-password
                ch-smtp:ToAddr     = emailadr.                
            
            IF case-type = "NightAudit" THEN
                ASSIGN
                    ch-smtp:Subject    = "VHP<>Channel Manager Night Audit Running Notification - " + hotelcode
                    ch-smtp:BodyText   = "Dear Partner, " + CHR(13) + CHR(13) + 
                                        "Night Audit is currently running, inventory updates are being sent anyways for property " + hotel.htlcode + " to Channel Manager." + CHR(13) +
                                        "Please check the Night Audit Flag in general parameter 253. " + CHR(13) + CHR(13) +
                                        "Thank you for your attention and cooperation.".
            ELSE IF case-type = "Rsv" THEN
                ASSIGN
                    ch-smtp:BodyText   = "Dear Partner, the booking with ID of " + res-info.res-id
                                        + " for property " + hotel.htlcode + " was not able to be stored into VHP due to " + error-str + CHR(10) + drive + logpath
                    ch-smtp:Subject    = "VHP<>Channel Manager Failed Booking Notification " + CHR(40) + res-info.res-status + " Reservation" + CHR(41) + " - " + hotel.htlcode.
            ELSE IF case-type = "Avail" THEN
                ASSIGN
                    ch-smtp:BodyText   = "Dear Partner, there is an error while updating availability to channel manager for property " + hotel.htlcode + 
                                        ". For further information please take a look in the attachment file." + CHR(10) + drive + logpath
                    ch-smtp:Subject    = "VHP<>Channel Manager Failed Availability Notification - " + hotel.htlcode.
            ELSE IF case-type = "Rate" THEN
                ASSIGN
                    ch-smtp:BodyText   = "Dear Partner, there is an error while updating rates to channel manager for property " + hotel.htlcode + 
                                        ". For further information please take a look in the attachment file." + CHR(10) + drive + logpath
                    ch-smtp:Subject    = "VHP<>Channel Manager Failed Rates Notification - " + hotel.htlcode.
            ELSE IF case-type = "Error" THEN
                ASSIGN
                    ch-smtp:BodyText   = customreply + CHR(10) + drive + logpath
                    ch-smtp:Subject    = "VHP<>Channel Manager Error Encountered - " + hotel.htlcode.
                
            IF email-attachment NE "" THEN ch-smtp:AddAttachment (email-attachment, , ,).
            IF cc-email NE "" THEN ASSIGN ch-smtp:CcAddr = cc-email.
    
            ch-imap:CONNECT(serveraddress , 993, username, password). 

            IF ch-smtp:SEND THEN
            DO:
                ch-imap:AppendMessage("Sent",ch-smtp:MESSAGE:RawBody,,32,0).
                success-flag = YES.
                RUN logmess("Email (" + case-type + ") Sent To " + emailadr).
            END.
            ELSE
            DO:
                IF ch-smtp:errcode MATCHES "*123*" THEN
                DO:
                    ASSIGN
                      success-flag = NO
                      msg-str      = msg-str + "Wrong email address definition for guest: " + 
                                     STRING(TRIM(receiver)) + ", " +
                                     "|System Message: " + ch-smtp:errdesc.
                    RUN logmess(msg-str).
                END.
                ELSE
                DO:
                    ASSIGN 
                      success-flag = NO.
                      msg-str      = msg-str + "Email NOT Sent:"
                                     + "|System Message: " + ch-smtp:errdesc + "|" + ch-smtp:errcode.
                    RUN logmess(msg-str).
                END.
            END.
        END.
        ch-smtp:DISCONNECT.
        ch-imap:DISCONNECT.
        RELEASE OBJECT ch-smtp.
    END.
END PROCEDURE.

PROCEDURE call-NotifReportRQ:
    DEFINE INPUT PARAMETER res-id       AS CHARACTER.
    DEFINE INPUT PARAMETER res-time     AS CHARACTER.
    DEFINE INPUT PARAMETER res-status   AS CHARACTER.
    DEFINE VARIABLE OTA_NotifReportRS   AS LONGCHAR NO-UNDO INIT "".
    DEFINE VARIABLE filenm              AS CHARACTER NO-UNDO INIT "".
    DEFINE VARIABLE rsv-id              AS CHARACTER NO-UNDO INIT "".
    
    ASSIGN
        uuid = GENERATE-UUID
        echotoken = GUID(uuid)
        timestamp = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" +
                    STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "+00:00"
		vcXMLText = ""
    .

    FIND FIRST notif-list WHERE notif-list.otaid = res-id NO-LOCK NO-ERROR.
    IF NOT AVAILABLE notif-list THEN
    DO:
        FIND FIRST notif-list WHERE notif-list.cmid = res-id NO-LOCK NO-ERROR.
        IF NOT AVAILABLE notif-list THEN
            rsv-id = res-id.
        ELSE
            rsv-id = notif-list.cmid.
    END.
    ELSE
    DO:
        rsv-id = notif-list.cmid.
    END.
	
    /* error staah masuk notif "errors" karena masih membaca chksvc, seharusnya kirim notif success - CRG 25/11/2022 */
    /*FILE-INFO:FILE-NAME = 'C:\chksvc'.*/
    IF done OR
    (/*FILE-INFO:FULL-PATHNAME = ? AND*/ error-str MATCHES "*Reservation " + res-info.res-id + " not found*") THEN
    DO:
        vcXMLText =
    
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '~n' +
          '<soap:Header>' + '~n' +
            '<wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' + '~n' +
              '<wsse:UsernameToken>' + '~n' +
                '<wsse:Username>' + cUsername + '</wsse:Username>' + '~n' +
                '<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">' + cPassword + '</wsse:Password>' + '~n' +
              '</wsse:UsernameToken>' + '~n' +
            '</wsse:Security>' + '~n' +
          '</soap:Header>' + '~n' +
          '<soap:Body>' + '~n' +
           '<OTA_NotifReportRQ xmlns="http://www.opentravel.org/OTA/2003/05" Version="1.0" TimeStamp="' + timestamp + '" EchoToken="' + echotoken + '">' + '~n' +
              '<Success/>' + '~n' +
              '<NotifDetails>' + '~n' +
                '<HotelNotifReport>' + '~n' +
                  '<HotelReservations>' + '~n' +
                    '<HotelReservation CreateDateTime="' + res-time + '" ResStatus="' + res-status + '">' + '~n' +
                      '<ResGlobalInfo>' + '~n' +
                        '<HotelReservationIDs>' + '~n' +
                          '<HotelReservationID ResID_Value="' + rsv-id + '"/>' + '~n' +
                        '</HotelReservationIDs>' + '~n' +
                      '</ResGlobalInfo>' + '~n' +
                    '</HotelReservation>' + '~n' +
                  '</HotelReservations>' + '~n' +
                '</HotelNotifReport>' + '~n' +
              '</NotifDetails>' + '~n' +
            '</OTA_NotifReportRQ>' + '~n' +
          '</soap:Body>' + '~n' +
        '</soap:Envelope>'.
    END.
    ELSE IF (FILE-INFO:FULL-PATHNAME NE ? OR FILE-INFO:FULL-PATHNAME EQ ?) AND NOT done THEN
    DO:
        vcXMLText =

        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '~n' +
          '<soap:Header>' + '~n' +
            '<wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' + '~n' +
              '<wsse:UsernameToken>' + '~n' +
                '<wsse:Username>' + cUsername + '</wsse:Username>' + '~n' +
                '<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">' + cPassword + '</wsse:Password>' + '~n' +
              '</wsse:UsernameToken>' + '~n' +
            '</wsse:Security>' + '~n' +
          '</soap:Header>' + '~n' +
          '<soap:Body>' + '~n' +
           '<OTA_NotifReportRQ xmlns="http://www.opentravel.org/OTA/2003/05" Version="1.0" TimeStamp="' + timestamp + '" EchoToken="' + echotoken + '">' + '~n' +
              '<Errors/>' + '~n' +
              '<NotifDetails>' + '~n' +
                '<HotelNotifReport>' + '~n' +
                  '<HotelReservations>' + '~n' +
                    '<HotelReservation CreateDateTime="' + res-time + '" ResStatus="' + res-status + '">' + '~n' +
                      '<ResGlobalInfo>' + '~n' +
                        '<HotelReservationIDs>' + '~n' +
                          '<HotelReservationID ResID_Value="' + rsv-id + '"/>' + '~n' +
                        '</HotelReservationIDs>' + '~n' +
                      '</ResGlobalInfo>' + '~n' +
                    '</HotelReservation>' + '~n' +
                  '</HotelReservations>' + '~n' +
                '</HotelNotifReport>' + '~n' +
              '</NotifDetails>' + '~n' +
            '</OTA_NotifReportRQ>' + '~n' +
          '</soap:Body>' + '~n' +
        '</soap:Envelope>'.
    END.
/*
    vcRequest =
        'POST ' + vcWSAgent4 + ' HTTP/1.1' + '~r~n' +
        'Host: ' + vcWebHost + '~r~n' +
        'Content-Type: text/xml;charset=UTF-8' + '~r~n' +
        'Content-Length: ' + STRING(LENGTH(vcXMLText)) + '~r~n' +
        '~r~n'.
*/    
    filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\notifRQ.xml".
	IF SEARCH(filenm) NE ? THEN
      DOS SILENT VALUE ("DEL " + filenm).
      /*
    OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(vcXMLText) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(vcXMLText, i, 1)) FORMAT "x(1)".
        END.        
    OUTPUT STREAM s2 CLOSE.*/
    COPY-LOB vcXMLText TO FILE filenm.

    IF debugging-flag = "YES" THEN
    DO:
        RUN logmess("Notif File Has Been Generated").
    END.
    ELSE
    DO:
        EMPTY TEMP-TABLE header-list.
        CREATE header-list.
        ASSIGN
            vKey="Content-Type"
            vValue="text/xml;charset=UTF-8".
    
        RUN http-request-tlsui.p("post",vcWSAgent4,vcxmltext,TABLE header-list,
                                 OUTPUT OTA_NotifReportRS, OUTPUT errorMsg).
        /* MESSAGE STRING(OTA_NotifReportRS) VIEW-AS ALERT-BOX.*/
        IF errorMsg NE "" THEN
            RUN logmess(errorMsg + " | " + vcWSagent4).
    	 
        IF OTA_NotifReportRS MATCHES "*Success*" THEN
            RUN logmess("NOTIF Success").
        ELSE
		DO:
            RUN logmess("NOTIF Failed").
			RUN logmess("OTA_NotifReportRS== " + OTA_NotifReportRS).
		END.
    
        filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\notifRS.xml".
    	IF SEARCH(filenm) NE ? THEN
          DOS SILENT VALUE ("DEL " + filenm).
         /*
        OUTPUT STREAM s2 TO VALUE(filenm).
            DO i = 1 TO LENGTH(OTA_NotifReportRS) :
                PUT STREAM s2 UNFORMATTED STRING(SUBSTR(OTA_NotifReportRS, i, 1)) FORMAT "x(1)".
            END.        
        OUTPUT STREAM s2 CLOSE.*/
        COPY-LOB OTA_NotifReportRS TO FILE filenm.
    END.
END PROCEDURE.

PROCEDURE push-allotment:
DEFINE VARIABLE dd           AS INTEGER  NO-UNDO.
DEFINE VARIABLE mm           AS INTEGER  NO-UNDO.
DEFINE VARIABLE yy           AS INTEGER  NO-UNDO.
DEFINE VARIABLE rm-avail     AS DECIMAL        NO-UNDO.
DEFINE VARIABLE rmType       AS CHAR           NO-UNDO.
DEFINE VARIABLE rCode        AS CHAR           NO-UNDO.
DEFINE VARIABLE attempt   AS INTEGER  NO-UNDO.
DEFINE VARIABLE curr-stat    AS LOGICAL INIT NO  NO-UNDO.
DEFINE VARIABLE curr-qty     AS DECIMAL.
DEFINE VARIABLE curr-recid   AS INT.
DEFINE VARIABLE curr-rcode   AS CHAR.
DEFINE VARIABLE curr-bezeich AS CHAR.
DEFINE VARIABLE curr-statnr  AS INT.
DEFINE VARIABLE curr-ota     AS CHAR.
DEFINE VARIABLE curr-bsetup  AS CHAR.
DEFINE VARIABLE msg-str      AS CHAR.
DEFINE VARIABLE deleted      AS LOGICAL.

DEFINE BUFFER buffallot FOR push-allot-list.
EMPTY TEMP-TABLE logs-list.
    ASSIGN
        curr-qty     = 0
        curr-recid   = 0
        curr-statnr  = 0
        curr-bezeich = ""
        curr-rcode   = ""
        curr-ota     = ""
        curr-bsetup  = ""
    .
	RUN update-xml("avail", ""). /*NC #E98552*/ /*for count hotel.availcounter*/
    
    FOR EACH push-allot-list WHERE push-allot-list.flag /* BY push-allot-list.rcode 
        BY push-allot-list.zikatnr BY push-allot-list.bsetup BY push-allot-list.ota 
        BY push-allot-list.statnr BY push-allot-list.startperiode */:
		CREATE logs-list.
		ASSIGN 
			logs-list.rmtype = push-allot-list.bezeich
			logs-list.logs = "AVAILABILITY|" + push-allot-list.bezeich + " " 
		 + "Start Date: " + push-allot-list.str-date1 + " " 
		 + "End Date: " + push-allot-list.str-date2 + " " 
		 + "RateCode: " + push-allot-list.rcode + " " 
		 + "Qty: " + STRING(push-allot-list.qty) + " "
		 + "Status: " + STRING(push-allot-list.statnr). /* NC - use original date for debug purpose*/
        IF curr-qty NE push-allot-list.qty THEN
            ASSIGN
                curr-rcode   = push-allot-list.rcode
                curr-bezeich = push-allot-list.bezeich
                curr-bsetup  = push-allot-list.bsetup
                curr-recid   = push-allot-list.counter
                curr-qty     = push-allot-list.qty
                curr-statnr  = push-allot-list.statnr
                curr-ota     = push-allot-list.ota
            .
        ELSE IF curr-qty = push-allot-list.qty AND (curr-rcode NE push-allot-list.rcode OR curr-bezeich NE push-allot-list.bezeich
                                                    OR curr-bsetup NE push-allot-list.bsetup
                                                    OR curr-statnr NE push-allot-list.statnr
                                                    OR curr-ota NE push-allot-list.ota) THEN
            ASSIGN 
                curr-rcode = push-allot-list.rcode
                curr-bezeich = push-allot-list.bezeich
                curr-bsetup  = push-allot-list.bsetup
                curr-recid  = push-allot-list.counter
                curr-qty  = push-allot-list.qty
                curr-statnr  = push-allot-list.statnr
                curr-ota     = push-allot-list.ota
            .
        ELSE IF curr-qty = push-allot-list.qty AND curr-rcode = push-allot-list.rcode AND curr-bezeich = push-allot-list.bezeich
            AND curr-bsetup = push-allot-list.bsetup AND curr-statnr = push-allot-list.statnr AND curr-ota = push-allot-list.ota THEN
        DO:
            FIND FIRST buffallot WHERE buffallot.counter = curr-recid /*EXCLUSIVE-LOCK*/ NO-ERROR.
            IF AVAILABLE buffallot AND (buffallot.endperiode = push-allot-list.startperiode - 1 OR 
                                       buffallot.endperiode GE push-allot-list.startperiode)
                AND buffallot.rcode     = push-allot-list.rcode
                AND buffallot.bezeich   = push-allot-list.bezeich 
                AND buffallot.bsetup    = push-allot-list.bsetup
                AND buffallot.statnr    = push-allot-list.statnr 
                AND buffallot.ota       = push-allot-list.ota THEN
            DO:
                
                IF buffallot.endperiode GT push-allot-list.endperiode THEN.
                ELSE buffallot.endperiode = push-allot-list.endperiode.
               /* DELETE push-allot-list.
                RELEASE push-allot-list.*/ /*NC - 27/03/25*/
                ASSIGN push-allot-list.flag = NO. /*NC - 27/03/25 optimize proces*/
            END.
            /*
            FIND CURRENT buffallot NO-LOCK.
            RELEASE buffallot.*/ /* NC - temp-table no need use this */
        END.    
    END.
    

    /* RUN logmess-nodisplay.*/ /*NC - moved*/
    
    FOR EACH rm-list:
        FIND FIRST push-allot-list WHERE push-allot-list.bezeich = rm-list.rmtyp NO-LOCK NO-ERROR.
        IF AVAILABLE push-allot-list THEN DO:
		
			/*FOR EACH logs-allot WHERE logs-allot.bezeich = rm-list.rmtyp :
				CREATE logs-list.
				ASSIGN logs-list.logs = "AVAILABILITY|" + logs-allot.bezeich + " " 
				 + "Start Date: " + logs-allot.str-date1 + " " 
				 + "End Date: " + logs-allot.str-date2 + " " 
				 + "Qty: " + STRING(logs-allot.qty) + " "
				 + "Status: " + STRING(logs-allot.statnr).
			END.*/
			RUN logmess-nodisplay(rm-list.rmtyp). /*moved here for optimalization + input rmtype*/ /*27/10/25*/
			RUN call-HotelAvailNotifRQ(rm-list.rmtyp, OUTPUT curr-stat).
			/* DO attempt = 1 TO 3:
				RUN call-HotelAvailNotifRQ(rm-list.rmtyp, OUTPUT curr-stat).
				IF curr-stat THEN LEAVE.
			END. */ /*NC - #E98552*/
		END.
    END.
	 
	IF NOT curr-stat AND hotel.availcounter GE 5 THEN
	DO:
		RUN logmess("STOP push avail for ALL roomtype since 5 times loop and still got error.").
		IF NOT cPushRate AND pushall THEN RUN update-bookengine-configbl.p ON hServer (8,hotel.becode,NO,"").
		IF readaricomboflag = NO OR allotflag = NO THEN DO:
			
			RUN if-bookeng-update-aribl.p ON hServer ("","avail").
		END.
		ELSE
			DOS SILENT VALUE("DEL " + allotfile).
	END.
END.

PROCEDURE call-HotelAvailNotifRQ:
    DEFINE INPUT PARAMETER in-rmtype AS CHAR.
	DEFINE OUTPUT PARAMETER state-attempt AS LOGICAL INIT NO.
    DEF VAR rate-code   	AS CHARACTER.
    DEF VAR room-type       AS CHARACTER.
    DEF VAR start-date      AS CHARACTER INIT "" NO-UNDO.
    DEF VAR start-date1     AS CHARACTER INIT "" NO-UNDO.
    DEF VAR end-date        AS CHARACTER INIT "" NO-UNDO.
    DEF VAR allotment       AS INT INIT "" NO-UNDO.

    DEF VAR start-flag      AS LOGICAL INIT YES NO-UNDO.
    DEF VAR end-flag        AS LOGICAL INIT NO  NO-UNDO.
    DEF VAR tot-record      AS INT INIT 0  NO-UNDO.
    DEF VAR temp-tot-record AS INT INIT 0  NO-UNDO.

    DEF VAR restriction AS CHAR INIT "".
    DEF VAR stat        AS CHAR INIT "".

    DEF VAR error-pushavail-file AS CHAR INIT "".
    
    DEFINE VARIABLE filenm AS CHAR.
    
    DEFINE VARIABLE OTA_HotelAvailNotifRS     AS LONGCHAR INIT "".    

    ASSIGN
        uuid      = GENERATE-UUID
        echotoken = GUID(uuid)
        timestamp = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" +
                    STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "+00:00"
        .

    
    vcXMLText =
    
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '~n' +
      '<soap:Header>' + '~n' +
        '<wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' + '~n' +
          '<wsse:UsernameToken>' + '~n' +
            '<wsse:Username>' + cUsername + '</wsse:Username>' + '~n' +
            '<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">' + cPassword + '</wsse:Password>' + '~n' +
          '</wsse:UsernameToken>' + '~n' +
        '</wsse:Security>' + '~n' +
      '</soap:Header>' + '~n' +
      
      '<soap:Body>' + '~n' +

      '<OTA_HotelAvailNotifRQ EchoToken="' + echotoken + '" TimeStamp="' + timestamp + '" Version="1.0" xmlns="http://www.opentravel.org/OTA/2003/05">' + '~n' +
        '<AvailStatusMessages HotelCode="' + htl-code + '">'.

        FOR EACH push-allot-list WHERE push-allot-list.bezeich = in-rmtype AND push-allot-list.flag : /*14/05/25*/ /*BY push-allot-list.bezeich BY push-allot-list.bsetup 
            BY push-allot-list.rcode BY push-allot-list.startperiode :*/ /*24/03/2025*/
    
            ASSIGN
                restriction = ""
                stat        = ""
				push-allot-list.str-date1 = 
                    STRING(YEAR(push-allot-list.startperiode),"9999") + "-" + 
                    STRING(MONTH(push-allot-list.startperiode),"99") + "-" +
                    STRING(DAY(push-allot-list.startperiode),"99")
                push-allot-list.str-date2 = 
                    STRING(YEAR(push-allot-list.endperiode),"9999") + "-" + 
                    STRING(MONTH(push-allot-list.endperiode),"99") + "-" +
                    STRING(DAY(push-allot-list.endperiode),"99")
            .            

            FIND FIRST map-list-push WHERE map-list-push.rmtypeVHP = push-allot-list.bezeich AND 
                map-list-push.ratecdVHP = push-allot-list.rcode NO-LOCK NO-ERROR.
            IF AVAILABLE map-list-push THEN
				ASSIGN
				room-type = map-list-push.rmtypeSM
				rate-code  = map-list-push.ratecdSM
				.
			ELSE 
				ASSIGN
                    room-type = push-allot-list.bezeich
                    rate-code  = push-allot-list.rcode.
    
            IF push-allot-list.statnr = 0 THEN
                stat = "Open".
            ELSE IF push-allot-list.statnr = 1 THEN
                stat = "Close".
            ELSE IF push-allot-list.statnr = 2 THEN
                ASSIGN
                    stat = "Close"
                    restriction = "Arrival".
            ELSE IF push-allot-list.statnr = 3 THEN
                ASSIGN
                    stat = "Close"
                    restriction = "Departure".
            ELSE IF push-allot-list.statnr = 4 THEN
                stat = "Close".
            ELSE IF push-allot-list.statnr = 5 THEN
                ASSIGN
                    stat = "Open"
                    restriction = "Arrival".
            ELSE IF push-allot-list.statnr = 6 THEN
                ASSIGN
                    stat = "Open"
                    restriction = "Departure".
    
            IF push-allot-list.statnr NE 4 THEN
            DO:                
                /* Status = close NC- 02/12/22; changed from 0 to push-allot-list.qty 06/12/23
                IF push-allot-list.statnr NE 1 /*AND push-allot-list.ota = ""*/ THEN
                DO:                
        		    vcXMLText = vcXMLText +
                    '<AvailStatusMessage BookingLimit="' + STRING(push-allot-list.qty) + '">'.
                END.
                ELSE
                DO:
                    vcXMLText = vcXMLText +
                    '<AvailStatusMessage BookingLimit="0">'. /* Status = close NC- 02/12/22 */
                END.
        		*/
				vcXMLText = vcXMLText +
                    '<AvailStatusMessage BookingLimit="' + STRING(push-allot-list.qty) + '">'.
        		
                IF NOT bedsetup THEN
                    vcXMLText = vcXMLText +
                        '<StatusApplicationControl End="' + push-allot-list.str-date2 + '" InvTypeCode="' + 
                        room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-allot-list.str-date1 + '">'.
                ELSE
                    vcXMLText = vcXMLText +
                        '<StatusApplicationControl End="' + push-allot-list.str-date2 + '" InvTypeCode="' + 
                        room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-allot-list.str-date1 + 
                        '" BedSetupCode="' + push-allot-list.bsetup + '">'.

                IF push-allot-list.ota NE "" THEN
                DO:
                    vcXMLText = vcXMLText + 

                        '<DestinationSystemCodes>' + '~n' +
                            '<DestinationSystemCode>' + push-allot-list.ota + '</DestinationSystemCode>' + '~n' +
                        '</DestinationSystemCodes>'.
                END.
                
                vcXMLText = vcXMLText + 
                '</StatusApplicationControl>'.

                IF restriction-flag THEN
                DO:
                    IF restriction NE "" THEN
                        vcXMLText = vcXMLText + '<RestrictionStatus Status="' + stat + '" Restriction="' + restriction + '"/>'.
                    ELSE
                        vcXMLText = vcXMLText + '<RestrictionStatus Status="' + stat + '"/>'.
                END.
                
                vcXMLText = vcXMLText + 
                '</AvailStatusMessage>'.
            END.
            ELSE IF push-allot-list.statnr = 4 THEN /*ctad*/
            DO:
				vcXMLText = vcXMLText +
                    '<AvailStatusMessage BookingLimit="' + STRING(push-allot-list.qty) + '">'.
                /*cta*/                
                IF NOT bedsetup THEN
                    vcXMLText = vcXMLText +
                        '<StatusApplicationControl End="' + push-allot-list.str-date2 + '" InvTypeCode="' + 
                        room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-allot-list.str-date1 + '">'.
                ELSE
                    vcXMLText = vcXMLText +
                        '<StatusApplicationControl End="' + push-allot-list.str-date2 + '" InvTypeCode="' + 
                        room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-allot-list.str-date1 + 
                        '" BedSetupCode="' + push-allot-list.bsetup + '">'.

                IF push-allot-list.ota NE "" THEN
                DO:
                    vcXMLText = vcXMLText + 

                    '<DestinationSystemCodes>' + '~n' +
                        '<DestinationSystemCode>' + push-allot-list.ota + '</DestinationSystemCode>' + '~n' +
                    '</DestinationSystemCodes>'.
                END.

                vcXMLText = vcXMLText + '</StatusApplicationControl>' + '~n'.

                IF restriction-flag THEN
                    vcXMLText = vcXMLText + '<RestrictionStatus Status="' + stat + '" Restriction="Arrival" />' + '~n'.
                
                vcXMLText = vcXMLText + '</AvailStatusMessage>'.

                /*ctd*/
				vcXMLText = vcXMLText +
                    '<AvailStatusMessage BookingLimit="' + STRING(push-allot-list.qty) + '">'.
                IF NOT bedsetup THEN
                    vcXMLText = vcXMLText +
                        '<StatusApplicationControl End="' + push-allot-list.str-date2 + '" InvTypeCode="' + 
                        room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-allot-list.str-date1 + '">'.
                ELSE
                    vcXMLText = vcXMLText +
                        '<StatusApplicationControl End="' + push-allot-list.str-date2 + '" InvTypeCode="' + 
                        room-type + '" RatePlanCode="' + rate-code + '" Start="' + push-allot-list.str-date1 + 
                        '" BedSetupCode="' + push-allot-list.bsetup + '">'.

                IF push-allot-list.ota NE "" THEN
                DO:
                    vcXMLText = vcXMLText + 

                    '<DestinationSystemCodes>' + '~n' +
                        '<DestinationSystemCode>' + push-allot-list.ota + '</DestinationSystemCode>' + '~n' +
                    '</DestinationSystemCodes>'.
                END.

                vcXMLText = vcXMLText + '</StatusApplicationControl>' + '~n'.

                IF restriction-flag THEN
                    vcXMLText = vcXMLText + '<RestrictionStatus Status="' + stat + '" Restriction="Departure"/>' + '~n'.

                vcXMLText = vcXMLText + '</AvailStatusMessage>'.
            END.
        END.
            
        vcXMLText = vcXMLText +

    	'</AvailStatusMessages>' + '~n' +
      '</OTA_HotelAvailNotifRQ>' + '~n' +
    '</soap:Body>' + '~n' +
    '</soap:Envelope>'.
/*
    vcRequest =
        'POST ' + vcWSAgent2 + ' HTTP/1.1' + '~r~n' +
        'Host: ' + vcWebHost + '~r~n' +
        'Content-Type: text/xml;charset=UTF-8' + '~r~n' +
        'Content-Length: ' + STRING(LENGTH(vcXMLText)) + '~r~n' +
        '~r~n'.
*/

    /* IF roomtypeoutput = "" THEN
        roomtypeoutput = backuproomtype. */ /*NC - not used anymore*/
    
    filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\avail_" + in-rmtype + "_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".
    
    /*OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(vcXMLText) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(vcXMLText, i, 1)) FORMAT "x(1)".
        END.        
    OUTPUT STREAM s2 CLOSE.
    */
    
    COPY-LOB vcXMLText TO FILE filenm.
    IF debugging-flag = "YES" THEN
    DO:
        RUN logmess("Availability File Has Been Generated").
        IF readaricomboflag = NO OR allotflag = NO THEN
            RUN if-bookeng-update-aribl.p ON hServer ("","avail").
        ELSE
            DOS SILENT VALUE("DEL " + allotfile).
        IF NOT cPushRate AND pushall = YES THEN RUN update-bookengine-configbl.p ON hServer (8,hotel.becode,NO,"").
        /* IF hotel.availcounter NE 0 THEN RUN update-xml("avail", "reset"). */ /*move up*/
    END.
    ELSE
    DO:
        IF SEARCH(filenm) = ? THEN 
        DO:
            RUN logmess ("debug: no available xml avail").
            RUN mt-program.
        END.
    
        EMPTY TEMP-TABLE header-list.
    
        CREATE header-list.
        ASSIGN
            vKey="Content-Type"
            vValue="text/xml;charset=UTF-8".
        RUN logmess("Uploading availability " + in-rmtype + " to Channel Manager...").
        RUN http-request-tlsui.p("post",vcWSAgent2,vcxmltext,TABLE header-list,
                                 OUTPUT OTA_HotelAvailNotifRS, OUTPUT errorMsg).
       /* MESSAGE STRING(OTA_HotelAvailNotifRS) VIEW-AS ALERT-BOX.*/

        IF errorMsg NE "" THEN
            RUN logmess(errorMsg + " | " + vcWSagent2).
    
        IF OTA_HotelAvailNotifRS MATCHES "*Success*" THEN
        DO:
    		state-attempt = YES.
            RUN logmess("Success Updating Availability " + in-rmtype).
            IF readaricomboflag = NO OR allotflag = NO THEN
                RUN if-bookeng-update-aribl.p ON hServer ("","avail").
            ELSE
                DOS SILENT VALUE("DEL " + allotfile).
            IF NOT cPushRate AND pushall = YES THEN RUN update-bookengine-configbl.p ON hServer (8,hotel.becode,NO,"").
            /* IF hotel.availcounter NE 0 THEN RUN update-xml("avail", "reset"). */ /*move up*/
        END.
        ELSE 
        DO:
    		state-attempt = NO.
            RUN logmess("Failed Updating Availability " + in-rmtype).
            IF OTA_HotelAvailNotifRS = "" THEN
                RUN logmess ("Check Push Rate Code Mapping Setup").
            ELSE IF NOT OTA_HotelAvailNotifRS MATCHES "*Success*" THEN
            DO:
				RUN logmess ("OTA_HotelAvailNotifRS==" + OTA_HotelAvailNotifRS).
                error-pushavail-file = 
                    workPath + "debug" + STRING(MONTH(TODAY)) + "\Error_avail_" + in-rmtype + "_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".            
                /*
                OUTPUT STREAM s2 TO VALUE(error-pushavail-file).
                DO i = 1 TO LENGTH(OTA_HotelAvailNotifRS) :
                    PUT STREAM s2 UNFORMATTED STRING(SUBSTR(OTA_HotelAvailNotifRS, i, 1)) FORMAT "x(1)".
                END.        
                OUTPUT STREAM s2 CLOSE.*/
                
                COPY-LOB OTA_HotelAvailNotifRS TO FILE error-pushavail-file.
                RUN send-email("Avail", error-pushavail-file, htl-code, "").
            END.
        END.
    END.
END PROCEDURE.

/*PROCEDURE connect-sm :
    DEFINE OUTPUT PARAMETER sm-con AS LOGICAL INIT NO.
    DEFINE VARIABLE con-param   AS CHAR NO-UNDO.
    DEFINE VARIABLE response         AS CHARACT NO-UNDO INITIAL "".
    DEFINE VARIABLE err     AS CHARACT NO-UNDO INITIAL "".
	
	/*NC -22/04/21 - BNL report 408 using web socket*/
	EMPTY TEMP-TABLE header-list.
	ASSIGN
		response = ""
		err = ""
	.
	IF vcWebHost EQ "bookandlink.com" THEN
	DO:
		vcWebHost = "https://bookandlink.com/status.php".
		RUN http-request-tlsui.p("get",vcWebHost,"",TABLE header-list,
								 OUTPUT response, OUTPUT err).
		IF err NE '' THEN
			RUN logmess(err).
		ELSE
			sm-con = YES.
	END.
	ELSE
	DO:
		CREATE SOCKET vhWebSocket.
		vhWebSocket:CONNECT('-H ' + vcWebHost + ' -S ' + vcWebPort) NO-ERROR.
		IF err NE '' THEN
			RUN logmess("ERROR|" + err).
		ELSE
			sm-con = vhWebSocket:CONNECTED().
	END.

    IF NOT sm-con THEN
        RUN send-email("error", "", htl-code, "Ping Connection Error:" + CHR(10) + hotel.NAME + CHR(10) + vcWebHost + CHR(10) + vcWebPort).
    ELSE 
    DO:
        IF hotel.errorcounter NE 0 THEN RUN update-xml("error", "reset").
    END.
END.*/

PROCEDURE mt-pull:
    DEFINE VARIABLE updated     AS LOGICAL  NO-UNDO INIT NO.
    
    DEFINE VARIABLE curr-i      AS INT.
    DEFINE VARIABLE remark-str  AS CHAR.
    DEFINE VARIABLE temp-value  AS DECIMAL.    
    
    IF debugging-flag NE "YES" THEN
    DO:
        RUN call-ReadRQ(OUTPUT response).
        IF response NE "" THEN
            RUN check-pull(OUTPUT updated).
    END.
    ELSE IF debugging-flag = "YES" THEN
    DO:
        updated = YES.
        COPY-LOB FROM FILE "C:\e1-vhp\temp-pull.xml" TO response.
    END.
    
    EMPTY TEMP-TABLE res-info.
    EMPTY TEMP-TABLE service-list.
    EMPTY TEMP-TABLE guest-list.
    EMPTY TEMP-TABLE room-list.
	EMPTY TEMP-TABLE buffroom.

/*    updated = YES.*/

    IF updated THEN
    DO:            
        CREATE X-DOCUMENT hXML.
        CREATE X-NODEREF hRoot.        
		hXML:LOAD('LONGCHAR', response, FALSE).
/*      hXML:LOAD('file', "C:\vhp-cm\vhplib\debug9\pull1_12091961230.xml", FALSE).*/
        hXML:GET-DOCUMENT-ELEMENT(hRoot).
        RUN getChildren(hRoot, 1).
        DELETE OBJECT hXML.
        DELETE OBJECT hRoot.
    END.

    FOR EACH room-list:
        DO curr-i = 1 TO room-list.number:
            CREATE buffroom.
            BUFFER-COPY room-list TO buffroom.
        END.        
    END.
	FOR EACH service-list WHERE service-list.amountaftertax LE 0 :
		DELETE service-list. /*NC - 20/11/2024 */
	END.
    /*EMPTY TEMP-TABLE temp-info.

    FOR EACH res-info:
        IF res-info.taxes NE "" THEN
        DO:
            IF res-info.amount EQ "" AND res-info.amountbeforetax NE "" THEN
            DO curr-j = 1 TO NUM-ENTRIES(res-info.amountbeforetax, "-") - 1:
                temp-value = DEC(ENTRY(curr-j, res-info.amountbeforetax, "-")) + DEC(ENTRY(curr-j,res-info.taxes,"-")).
                res-info.amount = res-info.amount + STRING(temp-value) + "-".
            END.
            ELSE IF res-info.amountbeforetax EQ "" AND res-info.amount NE "" THEN
            DO curr-j = 1 TO NUM-ENTRIES(res-info.amount, "-") - 1:
                temp-value = DEC(ENTRY(curr-j, res-info.amount, "-")) - DEC(ENTRY(curr-j,res-info.taxes,"-")).
                res-info.amountbeforetax = res-info.amountbeforetax + STRING(temp-value) + "-".
            END.
        END.

        remark-str = "".
        REPLACE(res-info.remark, '"', "'").
        REPLACE(res-info.given-name, '"', "'").
        REPLACE(res-info.sure-name, '"', "'").
        REPLACE(res-info.email, '"', "'").
        REPLACE(res-info.address1, '"', "'").
        REPLACE(res-info.address2, '"', "'").
        REPLACE(res-info.city, '"', "'").
        REPLACE(res-info.zip, '"', "'").
        REPLACE(res-info.state, '"', "'").
        REPLACE(res-info.country, '"', "'").

        CREATE temp-info.
        BUFFER-COPY res-info TO temp-info.

        ASSIGN 
            temp-info.ci-date-str = 
                          STRING(MONTH(res-info.ci-date), "99")  + '/'  +
                          STRING(DAY(res-info.ci-date), "99")    + '/'  +
                          STRING(YEAR(res-info.ci-date), "9999")
            temp-info.co-date-str = 
                          STRING(MONTH(res-info.co-date), "99")  + '/'  +
                          STRING(DAY(res-info.co-date), "99")    + '/'  +
                          STRING(YEAR(res-info.co-date), "9999")
            temp-info.no-room-str = STRING(res-info.no-room)
            temp-info.night-str = STRING(res-info.night).
        DO curr-i = 1 TO LENGTH(temp-info.remark):
           IF ASC(SUBSTR(temp-info.remark,curr-i,1)) GT 127 
               OR ASC(SUBSTR(temp-info.remark,curr-i,1)) LT 32 THEN 
               remark-str = remark-str + "-".
           ELSE remark-str = remark-str + SUBSTR(temp-info.remark,curr-i,1).
        END.
        temp-info.remark = remark-str.
    END.*/
END.

PROCEDURE update-xml:
    DEFINE INPUT PARAMETER casetyp AS CHAR.
    DEFINE INPUT PARAMETER casestat AS CHAR.

    DEF VAR i AS INTEGER.
    DEF VAR update-flag AS LOGICAL INIT NO.
    DEF VAR htl-list AS CHAR.
	
    IF SEARCH(hotellist) NE ? THEN DO:
        vcXMLText = "".
        COPY-LOB FROM FILE hotellist TO vcxmltext.

        DO i = 1 TO LENGTH(vcxmltext):
            IF SUBSTR(vcxmltext,i,9) = "<htlcode>" THEN
            DO:
                IF SUBSTR(vcxmltext,i + 9,LENGTH(hotel.htlcode)) = hotel.htlcode THEN
                 update-flag = YES.
            END.
            IF SUBSTR(vcxmltext,i,9) = "<pushall>" AND update-flag = YES AND casetyp = "pushall" THEN
            DO:
                SUBSTRING(vcxmltext, i + 9, 3) = REPLACE(SUBSTRING(vcxmltext, i + 9, 3), "true", "false").
                hotel.pushall = NO.
            END.
            IF SUBSTR(vcxmltext,i,12) = "<rsvcounter>" AND update-flag = YES AND casetyp = "rsv" THEN
            DO:
                IF casestat = "reset" THEN 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 12, 1) = REPLACE(SUBSTRING(vcxmltext, i + 12, 1), STRING(hotel.rsvcounter), "0")
                        hotel.rsvcounter = 0.
                ELSE 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 12, 1) = REPLACE(SUBSTRING(vcxmltext, i + 12, 1), STRING(hotel.rsvcounter), STRING(hotel.rsvcounter + 1))
                        hotel.rsvcounter = hotel.rsvcounter + 1.
            END.
            IF SUBSTR(vcxmltext,i,14) = "<availcounter>" AND update-flag = YES AND casetyp = "avail" THEN
            DO:
                IF casestat = "reset" THEN 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 14, 1) = REPLACE(SUBSTRING(vcxmltext, i + 14, 1), STRING(hotel.availcounter), "0")
                        hotel.availcounter = 0.
                ELSE 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 14, 1) = REPLACE(SUBSTRING(vcxmltext, i + 14, 1), STRING(hotel.availcounter), STRING(hotel.availcounter + 1))
                        hotel.availcounter = hotel.availcounter + 1.
            END.
            IF SUBSTR(vcxmltext,i,13) = "<ratecounter>" AND update-flag = YES AND casetyp = "rate" THEN
            DO:
                IF casestat = "reset" THEN 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 13, 1) = REPLACE(SUBSTRING(vcxmltext, i + 13, 1), STRING(hotel.ratecounter), "0")
                        hotel.ratecounter = 0.
                ELSE 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 13, 1) = REPLACE(SUBSTRING(vcxmltext, i + 13, 1), STRING(hotel.ratecounter), STRING(hotel.ratecounter + 1))
                        hotel.ratecounter = hotel.ratecounter + 1.
            END.
            IF SUBSTR(vcxmltext,i,17) = "<pushbookcounter>" AND update-flag = YES AND casetyp = "pushbook" THEN
            DO:
                IF casestat = "reset" THEN
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 17, 1) = REPLACE(SUBSTRING(vcxmltext, i + 17, 1), STRING(hotel.pushbookcounter), "0")
                        hotel.pushbookcounter = 0.
                ELSE
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 17, 1) = REPLACE(SUBSTRING(vcxmltext, i + 17, 1), STRING(hotel.pushbookcounter), STRING(hotel.pushbookcounter + 1))
                        hotel.pushbookcounter = hotel.pushbookcounter + 1.
            END.
            IF SUBSTR(vcxmltext,i,14) = "<errorcounter>" AND update-flag = YES AND casetyp = "error" THEN
            DO:
                IF casestat = "reset" THEN 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 14, 1) = REPLACE(SUBSTRING(vcxmltext, i + 14, 1), STRING(hotel.errorcounter), "0")
                        hotel.errorcounter = 0.
                ELSE 
                    ASSIGN
                        SUBSTRING(vcxmltext, i + 14, 1) = REPLACE(SUBSTRING(vcxmltext, i + 14, 1), STRING(hotel.errorcounter), STRING(hotel.errorcounter + 1))
                        hotel.errorcounter = hotel.errorcounter + 1.
            END.
        END.

		COPY-LOB FROM vcxmltext TO FILE hotellist.
	END.
	ELSE IF hotelfile THEN DO: /*E98552*/
		CASE casetyp:
			WHEN "pushall" THEN
			DO:
				ASSIGN hotel.pushall = NO.
			END. 
			WHEN "rsv" THEN
			DO:
				IF casestat = "reset" THEN 
					ASSIGN
						hotel.rsvcounter = 0.
				ELSE 
					ASSIGN
						hotel.rsvcounter = hotel.rsvcounter + 1.
			END.
			WHEN "avail" THEN
			DO:
				IF casestat = "reset" THEN 
					ASSIGN
						hotel.availcounter = 0.
				ELSE 
					ASSIGN
						hotel.availcounter = hotel.availcounter + 1.
			END.
			WHEN "rate" THEN
			DO:
				IF casestat = "reset" THEN 
					ASSIGN
						hotel.ratecounter = 0.
				ELSE 
					ASSIGN
						hotel.ratecounter = hotel.ratecounter + 1.
			END.
			WHEN "error" THEN
			DO:
				IF casestat = "reset" THEN 
					ASSIGN
						hotel.errorcounter = 0.
				ELSE 
					ASSIGN
						hotel.errorcounter = hotel.errorcounter + 1.
			END.
		END.
	END.
END PROCEDURE.

PROCEDURE call-readRQ:
    DEFINE OUTPUT PARAMETER OTA_ResRetrieveRS   AS LONGCHAR NO-UNDO INIT "".
    DEFINE VARIABLE OTA_ReadRQ                  AS LONGCHAR NO-UNDO INIT "".

    DEFINE VARIABLE filenm      AS CHARACTER.           
    DEFINE VARIABLE vcXMLText   AS LONGCHAR     NO-UNDO.
    DEFINE VARIABLE vcRequest   AS CHARACTER    NO-UNDO.    

    DEFINE VARIABLE flag        AS LOGICAL  INIT NO.

    ASSIGN        
        timestamp = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" +
                    STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "+00:00".
		vcXMLText = ""
	.

    vcXMLText =

    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' + '~n' +
      '<soap:Header>' + '~n' +
        '<wsse:Security soap:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' + '~n' +
          '<wsse:UsernameToken>' + '~n' +
            '<wsse:Username>' + cUsername + '</wsse:Username>' + '~n' +
            '<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">' + cPassword + '</wsse:Password>' + '~n' +
          '</wsse:UsernameToken>' + '~n' +
        '</wsse:Security>' + '~n' +
      '</soap:Header>' + '~n' +
      '<soap:Body>' + '~n' +
       '<OTA_ReadRQ xmlns="http://www.opentravel.org/OTA/2003/05" Version="1.0" EchoToken="' + echotoken + '" TimeStamp="' + timestamp + '">' + '~n' +
          '<POS>' + '~n' +
            '<Source>' + '~n' +
              '<RequestorID Type="22" ID="VHP"/>' + '~n' +
            '</Source>' + '~n' +
          '</POS>' + '~n' +
          '<ReadRequests>' + '~n' +
            '<HotelReadRequest HotelCode="' + htl-code + '">' + '~n' +
              '<SelectionCriteria SelectionType="Undelivered"/>' + '~n' +
            '</HotelReadRequest>' + '~n' +
          '</ReadRequests>' + '~n' +
        '</OTA_ReadRQ>' + '~n' +
      '</soap:Body>' + '~n' +
    '</soap:Envelope>'.
    
/*    
    vcRequest =
        'POST ' + vcWSAgent + ' HTTP/1.1' + '~r~n' +
        'Host: ' + vcWebHost + '~r~n' +
        'Content-Type: text/xml;charset=UTF-8' + '~r~n' +
        'Content-Length: ' + STRING(LENGTH(vcXMLText)) + '~r~n' +
        '~r~n'.
*/
    filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\pullReq.xml".
    
    IF SEARCH(filenm) NE ? THEN
        DOS SILENT DEL VALUE(filenm).
    /*
    OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(vcXMLText) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(vcXMLText, i, 1)) FORMAT "x(1)".
        END.        
    OUTPUT STREAM s2 CLOSE.*/
    
    COPY-LOB vcXMLText TO FILE filenm.
    IF vcXMLText = "" OR vcXMLText = ? OR LENGTH(vcXMLText) = 0 THEN
    DO:
        flag = YES.
        RUN logmess ("debugPull:empty xml OTA_ReadRQ").
        RUN mt-program.                                
    END.

    EMPTY TEMP-TABLE header-list.

    CREATE header-list.
    ASSIGN
        vKey="Content-Type"
        vValue="text/xml;charset=UTF-8".
    
    RUN http-request-tlsui.p("post",vcWSAgent,vcxmltext,TABLE header-list,
                             OUTPUT OTA_ResRetrieveRS, OUTPUT errorMsg).
   /* MESSAGE STRING(OTA_ResRetrieveRS) VIEW-AS ALERT-BOX.*/

    IF errorMsg NE "" THEN
        RUN logmess(errorMsg + " | " + vcWSagent).


    /*OTA_ResRetrieveRS = CODEPAGE-CONVERT(STRING(OTA_ResRetrieveRS), SESSION:CHARSET, "UTF-8"). /* menyebabkan error di CM-Staah field GivenName */ */
    IF OTA_ResRetrieveRS MATCHES "*Connection failure*" THEN
    DO:
        RUN logmess ("debugPull:connection failure== " + OTA_ResRetrieveRS ).
        RUN mt-program.
    END.
    ELSE IF OTA_ResRetrieveRS = ? THEN
    DO:
        RUN logmess ("debugPull:OTA_ResRetrieveRS = ?").
        RUN mt-program.
    END.
    ELSE IF OTA_ResRetrieveRS = ""  OR LENGTH(OTA_ResRetrieveRS) = 0 THEN
    DO:
        RUN logmess ("debugPull:empty response").
        IF flag THEN RUN mt-program.
    END.
END PROCEDURE.

PROCEDURE check-pull:
    DEFINE OUTPUT PARAMETER updated AS LOGICAL  NO-UNDO INIT NO.
    DEFINE VARIABLE temp    AS CHAR     NO-UNDO.
    DEFINE VARIABLE filenm  AS CHAR     NO-UNDO.
    DEFINE VARIABLE flag-i  AS LOGICAL INIT NO.
    DEFINE VARIABLE start-i AS INT.
    DEFINE VARIABLE end-i   AS INT.
    DEFINE VARIABLE str     AS LONGCHAR.
    DEFINE VARIABLE unused  AS CHAR.

    filenm = workPath + "debug" + STRING(MONTH(TODAY)) + "\pull1_" + STRING(TODAY, "999999") + STRING(TIME) + ".xml".
    errfile = filenm.
    /*OUTPUT STREAM s2 TO VALUE(filenm).*/ /*no used*/
    DO i = 1 TO LENGTH(response) :
        temp = STRING(SUBSTR(response, i, 17)). 
        IF temp EQ "ReservationsList>" THEN /*NC - #FF4259*/
        DO:                    
            ASSIGN updated = YES.        
            LEAVE.
        END.
    END.        
    /*OUTPUT STREAM s2 CLOSE.*/
    
    IF updated THEN
    DO:
        RUN character-conversionbl.p ("", response, OUTPUT unused, OUTPUT response).   /* added by CRG 7 Jan 2022 */
        DO i = 1 TO LENGTH(response):
            IF SUBSTR(response,i,1) EQ "<" AND NOT flag-i THEN 
                ASSIGN
                    start-i = i
                    flag-i = YES.
            ELSE IF SUBSTR(response,i,LENGTH("</soap:Envelope>")) EQ "</soap:Envelope>" THEN
                end-i = i.
        END.
        str = SUBSTR(response,start-i, end-i - start-i + LENGTH("</soap:Envelope>")).

        response = str.
        /*
        OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(response) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(response, i, 1)) FORMAT "x(1)".
        END.        
        OUTPUT STREAM s2 CLOSE.*/
        
        COPY-LOB response TO FILE filenm.
        IF SEARCH(filenm) = ? THEN 
        DO:
            RUN logmess ("debug: no available xml pull").
            RUN mt-program.
        END.
            
    END.

    /*M 100512 -> if error, stores the xml */
    IF NOT updated THEN DOS SILENT DEL VALUE(filenm).
END.

PROCEDURE GetChildren:
    DEFINE INPUT PARAMETER hParent AS HANDLE.
    DEFINE INPUT PARAMETER level AS INTEGER.

    DEFINE VARIABLE hNoderef    AS HANDLE       NO-UNDO.
    DEFINE VARIABLE good        AS LOGICAL      NO-UNDO.
    DEFINE VARIABLE entries     AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE aname       AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE avalue      AS CHARACTER    NO-UNDO.
    DEFINE VARIABLE i           AS INTEGER      NO-UNDO.
    DEFINE VARIABLE j           AS INTEGER      NO-UNDO.
    DEFINE VARIABLE rm-qty      AS INTEGER      NO-UNDO.
    DEFINE VARIABLE age-code    AS INTEGER      NO-UNDO.
    DEFINE VARIABLE str-rate-perday  AS CHAR.
    DEFINE VARIABLE rate-perday      AS DECIMAL     NO-UNDO INIT 0.
    DEFINE VARIABLE tot-tax          AS DECIMAL     NO-UNDO INIT 0.
    DEFINE VARIABLE tot-tax-serv     AS DECIMAL     NO-UNDO INIT 0.
    DEFINE VARIABLE tot-am-after-tax AS DECIMAL     NO-UNDO INIT 0.
    DEFINE VARIABLE tot-be-after-tax AS DECIMAL     NO-UNDO INIT 0.
    DEFINE VARIABLE proc             AS DECIMAL     NO-UNDO INIT 0.

    DEFINE VARIABLE hValue AS HANDLE.
    CREATE X-NODEREF hValue.

    DEFINE VARIABLE res-id  AS CHARACTER    NO-UNDO.
    
    CREATE X-NODEREF hNoderef.
    REPEAT i = 1 TO hParent:NUM-CHILDREN: /*M get number of nodes */
        good = hParent:GET-CHILD(hNoderef,i).
        IF NOT good THEN LEAVE.
        ELSE 
        DO:
            IF hNoderef:SUBTYPE <> "ELEMENT" THEN NEXT.
            IF hNoderef:NAME = "HotelReservation" THEN
            DO:
                CREATE res-info.
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "CreateDateTime" THEN
                    DO:
                        avalue = hNoderef:GET-ATTRIBUTE(aname).                        
                        ASSIGN res-info.res-time  = avalue.
                    END.
                    ELSE IF aname MATCHES "LastModifyDateTime" THEN
                    DO:
                        avalue = hNoderef:GET-ATTRIBUTE(aname).                        
                        ASSIGN res-info.res-time  = avalue.
                    END.
                    ELSE IF aname MATCHES "ResStatus" THEN
                    DO:
                        avalue = hNoderef:GET-ATTRIBUTE(aname).
                        res-info.res-status = avalue.
                    END.
                END.
            END.
            IF hNoderef:NAME = "CompanyName" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "Code" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.ota-code = avalue.
                END.
            END.
            IF hNoderef:NAME = "RoomStay" THEN
            DO:
                service-flag = NO.
                roomstay-flag = YES.
				roomstay-comment = YES.
                CREATE room-list.
                room-list.resstatus = res-info.res-status.
				/* 07/01/2021 NC - added PromotionCode */
				IF hNoderef:ATTRIBUTE-NAMES NE "" OR hNoderef:ATTRIBUTE-NAMES NE ? THEN
				DO:
					entries = hNoderef:ATTRIBUTE-NAMES.

					REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
						aname = ENTRY (j, entries, ",").
						IF aname MATCHES "PromotionCode" THEN
							ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
								res-info.address2 = avalue.
					END.
				END.
            END.
            IF hNoderef:NAME = "RoomRate" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "RatePlanCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                            room-list.rate-code = avalue.
                    ELSE IF aname MATCHES "RoomTypeCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                            room-list.room-type = avalue.
                    ELSE IF aname MATCHES "NumberOfUnits" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                            room-list.number = INT(avalue).
                END.
            END.
            IF hNoderef:NAME = "Rate" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "UnitMultiplier" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               multiplier = INT(avalue).
                END.
            END.
            IF hNoderef:NAME = "Base" AND NOT service-flag AND roomstay-flag THEN
            DO:
                ASSIGN 
                    avail-after     = NO
                    calc-tax-amount = NO
                    multiamount     = ""
                    entries         = hNoderef:ATTRIBUTE-NAMES
                .

                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "AmountAfterTax" THEN
                    DO:
                        ASSIGN
                            avail-after = YES
                            avalue      = hNoderef:GET-ATTRIBUTE(aname)
                            multiamount = avalue.
                    END.
                    IF aname MATCHES "CurrencyCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.curr = avalue.
                END.
                
                IF NOT avail-after THEN
                DO:
                    ASSIGN calc-tax-amount = YES.
                    REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                        aname = ENTRY (j, entries, ",").
                        IF aname MATCHES "AmountBeforeTax" THEN
                            ASSIGN avalue      = hNoderef:GET-ATTRIBUTE(aname)
                                   multiamount = avalue
                            .
                        IF aname MATCHES "CurrencyCode" THEN
                            ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                                   res-info.curr = avalue.
                    END.
                    avail-after = NO.
                END.

                IF room-list.number GT 1 THEN
                    multiamount = STRING(DECIMAL(multiamount) / INT(room-list.number)).

                DO loopm = 1 TO multiplier:
                    room-list.amount = room-list.amount + multiamount + "-".
                END.
                multiamount = "".
            END.
            IF hNoderef:NAME = "ServiceRPH" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "RPH" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               room-list.service = room-list.service + avalue + "-".
                END.
            END.

            IF hNoderef:NAME = "GuestCount" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "AgeQualifyingCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               age-code = INTEGER(avalue).
                    IF age-code = 10 AND aname MATCHES "Count" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               room-list.adult = INT(avalue).
                    ELSE IF age-code = 8 AND aname MATCHES "Count" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               room-list.child1 = INT(avalue).
                    ELSE IF age-code = 7 AND aname MATCHES "Count" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               room-list.child2 = INT(avalue).
                END.
            END.

            IF hNoderef:NAME = "TimeSpan" THEN
            DO:
                DEFINE VARIABLE dd AS INTEGER NO-UNDO  INITIAL ?.
                DEFINE VARIABLE mm AS INTEGER NO-UNDO  INITIAL ?.
                DEFINE VARIABLE yy AS INTEGER NO-UNDO  INITIAL ?.
                
                IF roomstay-flag THEN
                DO:
                    entries = hNoderef:ATTRIBUTE-NAMES.
                    REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                        aname = ENTRY (j, entries, ",").
                        IF aname MATCHES "Start" THEN
                        DO:
                            ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname).
                            room-list.ci-date = avalue.
                        END.
                        ELSE IF aname MATCHES "End" THEN
                        DO:
                            ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname).
                            room-list.co-date = avalue.
                        END.                           
                    END.
                    IF roomstay-flag THEN roomstay-flag = NO.
                END. 
                IF service-flag THEN
                DO:
                    entries = hNoderef:ATTRIBUTE-NAMES.
                    REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                        aname = ENTRY (j, entries, ",").
                        IF aname MATCHES "Start" THEN
                        DO:
                            ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname).
                            service-list.ci-date = avalue.
                        END.
                        ELSE IF aname MATCHES "End" THEN
                        DO:
                            ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname).
                            service-list.co-date = avalue.
                        END.                           
                    END.
                END.
            END.
            IF hNoderef:NAME = "Total" AND calc-tax-amount AND rmrate-flag THEN 
            DO: 
                str-rate-perday = "".
                rate-perday = 0.
                tot-am-after-tax = 0.
                tot-be-after-tax = 0.
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "AmountAfterTax" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               tot-am-after-tax = DECIMAL(avalue).
                    IF aname MATCHES "AmountBeforeTax" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               tot-be-after-tax = DECIMAL(avalue).
                END.
                tot-tax = tot-am-after-tax - tot-be-after-tax.
                REPEAT j = 1 TO NUM-ENTRIES(room-list.amount, "-") :
                    rate-perday = DECIMAL(ENTRY (j, room-list.amount, "-")).
                    IF rate-perday NE 0 THEN
                    DO:
                        proc = tot-tax / tot-be-after-tax.
                        rate-perday = rate-perday + (rate-perday * proc).
                        str-rate-perday = str-rate-perday + STRING(rate-perday) + "-".
                    END.
                END.
                room-list.amount = str-rate-perday.
                calc-tax-amount = NO.
            END.
            IF hNoderef:NAME = "resGuestRPH" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "RPH" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               room-list.gastnr = avalue.
                END.
            END.
			IF hNoderef:NAME = "Comment" AND roomstay-comment AND hNoderef:NUM-CHILDREN GT 0 THEN
			/*make different flag between Reservation Comment tag*/
			DO:
				hNoderef:GET-CHILD(hValue, 1).
				IF hValue:NODE-VALUE NE ? OR hValue:NODE-VALUE NE "" OR hValue:NODE-VALUE NE " " THEN
					room-list.comment = hValue:NODE-VALUE.
			END.
            IF hNoderef:NAME = "Service" THEN
            DO:
                service-flag = YES.
                CREATE service-list.
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "ServiceInventoryCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               service-list.bezeich = avalue.
                    IF aname MATCHES "serviceRPH" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               service-list.rph = avalue.
                    IF aname MATCHES "Quantity" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               service-list.qty = INT(avalue).
                    IF aname MATCHES "ID" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               service-list.id = avalue.
                END.
            END.
            IF hNoderef:NAME = "Base" AND service-flag THEN
            DO:
                ASSIGN 
                    entries = hNoderef:ATTRIBUTE-NAMES
                    calc-tax-amount-serv = NO.

                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "AmountAfterTax" THEN
                    DO:
                        ASSIGN
                            avalue = hNoderef:GET-ATTRIBUTE(aname)
                            service-list.amountaftertax = DECIMAL(avalue).
                    END.
                    IF aname MATCHES "AmountBeforeTax" THEN
                    DO:
                        ASSIGN
                            avalue = hNoderef:GET-ATTRIBUTE(aname)
                            service-list.amountbeforetax = DECIMAL(avalue).
                    END.

                    IF service-list.amountaftertax = 0 THEN 
                        calc-tax-amount-serv = YES.

                    IF aname MATCHES "CurrencyCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               service-list.curr = avalue.
                END.
            END.

            IF hNoderef:NAME = "Total" AND service-flag THEN
            DO:
                ASSIGN entries = hNoderef:ATTRIBUTE-NAMES.

                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "AmountAfterTax" THEN
                    DO:
                        ASSIGN
                            avalue = hNoderef:GET-ATTRIBUTE(aname)
                            service-list.tamountaftertax = DECIMAL(avalue).
                    END.
                    IF aname MATCHES "AmountBeforeTax" THEN
                    DO:
                        ASSIGN
                            avalue = hNoderef:GET-ATTRIBUTE(aname)
                            service-list.tamountbeforetax = DECIMAL(avalue).
                    END.
                END.

                IF calc-tax-amount-serv AND service-list.amountaftertax = 0 THEN
                DO:
                    tot-tax-serv = service-list.tamountaftertax - service-list.tamountbeforetax.
                    IF tot-tax-serv NE 0 THEN
                    DO:
                        proc = tot-tax-serv / service-list.tamountaftertax.
                        service-list.amountaftertax = service-list.amountbeforetax + (service-list.amountbeforetax * proc).
                    END.
                END.    
                IF service-flag THEN
                    service-flag = NO.
            END.

            IF hNoderef:NAME = "ResGuest" THEN
            DO:
                CREATE guest-list.
                ASSIGN entries = hNoderef:ATTRIBUTE-NAMES.
                
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "ResGuestRPH" THEN
                    DO:
                        ASSIGN
                            avalue = hNoderef:GET-ATTRIBUTE(aname)
                            guest-list.gastnr = avalue.
							guest-flag = YES.
                    END.
                END.
            END.

            IF hNoderef:NAME = "Surname" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.sure-name =  hValue:NODE-VALUE.
                ELSE res-info.sure-name = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "GivenName" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.given-name =  hValue:NODE-VALUE.
                ELSE res-info.given-name = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "Email" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.Email =  hValue:NODE-VALUE.
                ELSE res-info.Email = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "Telephone" THEN
            DO:
                ASSIGN entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "PhoneNumber" THEN
                    DO:
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname).
                        IF guest-flag THEN
                            guest-list.phone = avalue.
                        ELSE res-info.phone = avalue.
                    END.
                END.
            END.

            IF hNoderef:NAME = "AddressLine" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.address1 =  hValue:NODE-VALUE.
                ELSE res-info.address1 = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "City" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.city =  hValue:NODE-VALUE.
                ELSE res-info.city = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "Country" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.Country =  hValue:NODE-VALUE.
                ELSE res-info.Country = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "StateProv" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                IF guest-flag THEN
                    guest-list.state =  hValue:NODE-VALUE.
                ELSE res-info.state = hValue:NODE-VALUE.
            END.

            IF hNoderef:NAME = "ResGlobalInfo" THEN
            DO:
                IF guest-flag THEN guest-flag = NO.
				IF roomstay-comment THEN roomstay-comment = NO.
            END.
/*
            IF hNoderef:NAME = "PaymentCard" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "CardNumber" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.card-info = res-info.card-info + "number:" + avalue + ";".
                    ELSE IF aname MATCHES "expireDate" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.card-info = res-info.card-info + "exp:" + avalue + ";".
                    ELSE IF aname MATCHES "CardCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.card-info = res-info.card-info + "code:" + avalue + ";".
                END.
            END.  
*/			
            IF hNoderef:NAME = "DepositPayments" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "Amount" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.deposit = DECIMAL(avalue).
                END.
            END.

            IF hNoderef:NAME = "Membership" THEN
            DO:                
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "ProgramCode" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.membership = res-info.membership + 
                                                    "MembershipProgram:" + avalue + "-".
                    IF aname MATCHES "AccountID" THEN
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.membership = res-info.membership +
                                                    "MembershipID:" + avalue + "-".
                END.
            END.
			/*For KIOSK self Checkin - NC 26/03/20*/
			IF hNoderef:NAME = "Total" AND NOT service-flag AND NOT rmrate-flag THEN
			DO:
				entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "Paid" THEN
                    DO:
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.commission = avalue.
                    END.                              
                END.
			END.

            IF hNoderef:NAME = "HotelReservationID" THEN
            DO:
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "ResID_Value" THEN
                    DO:
                        ASSIGN avalue = hNoderef:GET-ATTRIBUTE(aname)
                               res-info.res-id = avalue.

                        FOR EACH room-list WHERE room-list.res-id = "":
                            room-list.res-id = avalue.
                        END.  
                        FOR EACH service-list WHERE service-list.res-id = "":
                            service-list.res-id = avalue.
                        END.
                        FOR EACH guest-list WHERE guest-list.res-id = "":
                            guest-list.res-id = avalue.
                        END.

                        CREATE notif-list.
                        ASSIGN
                            notif-list.cmid = res-info.res-id
                            notif-list.otaid = "NULL".
                    END.
                END.
            END. 
            IF hNoderef:NAME = "OTAReservation" THEN
            DO:
                FIND FIRST notif-list WHERE notif-list.cmid = res-info.res-id NO-LOCK NO-ERROR.
                entries = hNoderef:ATTRIBUTE-NAMES.
                REPEAT j = 1 TO NUM-ENTRIES(entries, ",") :
                    aname = ENTRY (j, entries, ",").
                    IF aname MATCHES "ID" THEN
                    DO:
                        avalue = hNoderef:GET-ATTRIBUTE(aname).
                        FOR EACH room-list WHERE room-list.res-id = res-info.res-id:
                            room-list.res-id = avalue.
                        END.  
                        FOR EACH service-list WHERE service-list.res-id = res-info.res-id:
                            service-list.res-id = avalue.
                        END.
                        FOR EACH guest-list WHERE guest-list.res-id = res-info.res-id:
                            guest-list.res-id = avalue.
                        END.
                        res-info.res-id = avalue.

                        notif-list.otaid = res-info.res-id.
                    END.
                END.
            END.

            IF hNoderef:NAME = "Text" AND hNoderef:NUM-CHILDREN GT 0 THEN
            DO: 
                hNoderef:GET-CHILD(hValue, 1).
                res-info.remark = hValue:NODE-VALUE.
            END.
            
            RUN getchildren(hNoderef, (level + 1)).
        END.
    END.
    DELETE OBJECT hNoderef.
    DELETE OBJECT hValue.
END PROCEDURE.

PROCEDURE logmess2:
    DEFINE INPUT PARAMETER LogMessage AS CHAR FORMAT "x(200)"      NO-UNDO.
    DEFINE VARIABLE logfile AS CHAR NO-UNDO.
    
    logfile = workpath + "debug" + STRING(MONTH(TODAY)) + "\2-" + STRING(MONTH(TODAY), "99")+ STRING(YEAR(TODAY),"9999") + ".LOG".
	IF SEARCH(logfile) NE ? THEN
      DOS SILENT VALUE ("DEL " + logfile).
    OUTPUT STREAM lfile TO VALUE(logfile) APPEND UNBUFFERED.
    PUT STREAM lfile UNFORMATTED 
        "[" STRING(TODAY,"99.99.99") " " STRING(TIME,"HH:MM:SS") "] " 
        LogMessage SKIP.
    OUTPUT STREAM lfile CLOSE.
END PROCEDURE.


PROCEDURE readSession: 
DEFINE VARIABLE lvCTmp AS CHARACTER             NO-UNDO. 
DEFINE VARIABLE lvCLeft AS CHARACTER            NO-UNDO. 
DEFINE VARIABLE lvCVal AS CHARACTER             NO-UNDO. 
DEFINE VARIABLE lvICnt AS INTEGER               NO-UNDO. 
DEFINE VARIABLE lvI AS INTEGER                  NO-UNDO. 
DEFINE VARIABLE lvITmp AS INTEGER               NO-UNDO. 
 
    lvICnt = NUM-ENTRIES(SESSION:PARAMETER, ";"). 
    DO lvI = 1 TO lvICnt: 
        ASSIGN 
            lvCTmp  = "" 
            lvCLeft = "" 
        . 
 
        lvCtmp = TRIM(ENTRY(lvI, SESSION:PARAMETER, ";")). 
        lvCLeft = TRIM(ENTRY(1, lvCTmp, "=")) NO-ERROR. 
 
        CASE lvCLeft: 
            WHEN "RemoteLocal" THEN DO:
              IF TRIM(ENTRY(2, lvCTmp, "=")) = "REMOTE" THEN ASremoteFlag = YES.
            END.
            WHEN "AppSHost" THEN vHost = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "AppSPort" THEN vService = TRIM(ENTRY(2, lvCTmp, "=")).
			WHEN "HdeskHost" THEN hdeskHost = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "HdeskPort" THEN hdeskService = TRIM(ENTRY(2, lvCTmp, "=")).
			WHEN "BEGroup" THEN bookeng-grp = INT(TRIM(ENTRY(2, lvCTmp, "="))).
            WHEN "alert-box" THEN DO: 
                lvITmp = INTEGER(ENTRY(2, lvCTmp, "=")) NO-ERROR. 
                IF lvITmp = 1 THEN SESSION:SYSTEM-ALERT-BOXES = TRUE. 
            END.
            WHEN "BECode" THEN bookengID = INT(TRIM(ENTRY(2, lvCTmp, "="))).
            WHEN "Drive" THEN drive = TRIM(ENTRY(2, lvCTmp, "=")).
			WHEN "RawDrive" THEN drive-raw = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "Delay" THEN delayfrompf = INT(TRIM(ENTRY(2, lvCTmp, "="))).
            WHEN "Restart" THEN restartscheduler = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "Interval" THEN restartinterval = INT(TRIM(ENTRY(2, lvCTmp, "="))).
            WHEN "Pause" THEN pauseinterval = INT(TRIM(ENTRY(2, lvCTmp, "="))).
            WHEN "logpath" THEN ASSIGN 
                logpath = TRIM(ENTRY(2, lvCTmp, "="))
                logpath-flag = YES.
            WHEN "ABIhost" THEN abi-host = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "ABIport" THEN abi-port = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "readmanual" THEN abi-readmanual-flag = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "Debug" THEN debugging-flag = TRIM(ENTRY(2, lvCTmp, "=")).
        END CASE. 
 
    END.

    IF logpath NE "" THEN
        IF SUBSTR(logpath,LENGTH(logpath),1) NE CHR(92) THEN
            logpath = logpath + CHR(92).

END PROCEDURE. 

PROCEDURE readSession2: /*khusus untuk baca username & password untuk send-email*/ 
    DEFINE VARIABLE lvCTmp AS CHARACTER             NO-UNDO. 
    DEFINE VARIABLE lvCLeft AS CHARACTER            NO-UNDO. 
    DEFINE VARIABLE lvCVal AS CHARACTER             NO-UNDO. 
    DEFINE VARIABLE lvICnt AS INTEGER               NO-UNDO. 
    DEFINE VARIABLE lvI AS INTEGER                  NO-UNDO. 
    DEFINE VARIABLE lvITmp AS INTEGER               NO-UNDO. 
 
    lvICnt = NUM-ENTRIES(SESSION:PARAMETER, ";"). 
    DO lvI = 1 TO lvICnt: 
        ASSIGN 
            lvCTmp  = "" 
            lvCLeft = "" 
        . 
 
        lvCtmp = TRIM(ENTRY(lvI, SESSION:PARAMETER, ";")). 
        lvCLeft = TRIM(ENTRY(1, lvCTmp, "=")) NO-ERROR. 
 
        CASE lvCLeft: 
            WHEN "RemoteLocal" THEN DO:
              IF TRIM(ENTRY(2, lvCTmp, "=")) = "REMOTE" THEN ASremoteFlag = YES.
            END.
            WHEN "EmailUsername" THEN email-username = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "EmailPassword" THEN email-password = TRIM(ENTRY(2, lvCTmp, "=")).
            WHEN "EmailServer"   THEN email-server = TRIM(ENTRY(2, lvCTmp, "=")).                             
            WHEN "EmailPort"     THEN email-port = INT(TRIM(ENTRY(2, lvCTmp, "="))).            
        END CASE. 
 
    END. 

    /*DEFINE VARIABLE p-1379 AS CHAR.
    RUN htpchar.p ON hServer(1379, OUTPUT p-1379).

    IF p-1379 NE "" THEN
        ASSIGN
            email-server    = ENTRY(1, p-1379, ";")
            email-port      = ENTRY(2, p-1379, ";")
            email-username  = ENTRY(3, p-1379, ";")
            email-password  = ENTRY(4, p-1379, ";") NO-ERROR.*/

END PROCEDURE. 

PROCEDURE create-hotel-list:
    DEFINE VARIABLE lOK      AS LOGICAL NO-UNDO.
    DEFINE VARIABLE timestr             AS CHARACTER    NO-UNDO.
    FOR EACH hotel-list:
        DELETE hotel-list.
    END.
	FOR EACH hotel:
		DELETE hotel.
	END.
	IF hdeskHost NE "" AND hdeskService NE "" THEN DO:
		CREATE SERVER hdeskServer.
		RUN connect-hdeskServer (hdeskHost,hdeskService, OUTPUT hReturn).
		IF hReturn THEN DO:
			RUN helpdesk-load-hotel-setup_2bl.p ON hdeskServer (bookeng-grp, OUTPUT TABLE hotel-list, OUTPUT TABLE preference-list). /* BLY 04/06/2025 */

            /* BLY 04/06/2025 */
            FIND FIRST preference-list NO-LOCK NO-ERROR.
            IF AVAILABLE preference-list THEN
                ASSIGN 
                    email-username = preference-list.email
                    email-password = preference-list.pass
                    email-server = preference-list.email-server
                    email-port = preference-list.email-port
                    central-path = preference-list.Ctr-logs-path
                .
            ELSE RUN readSession2.
            /* END BLY */

			FOR EACH hotel-list WHERE hotel-list.active-flag EQ YES NO-LOCK:
				CREATE hotel.
				ASSIGN 
					hotel.number         = hotel-list.nr        
					hotel.Name           = TRIM(hotel-list.hotelname)          
					hotel.License        = hotel-list.License       
					hotel.htlcode        = TRIM(hotel-list.hotelcode)       
					hotel.IP             = TRIM(hotel-list.IP)            
					hotel.Port           = hotel-list.Port          
					hotel.BECode         = hotel-list.BECode        
					hotel.grp            = hotel-list.grp           
					hotel.exdata         = hotel-list.exdata        
					hotel.rms            = hotel-list.rms           
					hotel.BECodeRMS      = hotel-list.BECodeRMS     
					hotel.pushall        = hotel-list.pushall       
					hotel.errorcounter   = hotel-list.errorcounter  
					hotel.rsvcounter     = hotel-list.rsvcounter    
					hotel.availcounter   = hotel-list.availcounter  
					hotel.ratecounter    = hotel-list.ratecounter   
					hotel.pushbookcounte = hotel-list.pushbookcounte
					hotel.notifcounter   = hotel-list.notifcounter  
					hotel.defemail       = TRIM(hotel-list.defemail)      
					hotel.abi            = hotel-list.abi
					hotel.activeflag     = hotel-list.active-flag
					. 				
			END.
			hotelfile = YES.
		END.
		ELSE
		DO:
			timestr = STRING(TIME,"HH:MM:SS").
			RUN logmess(timestr + " Can not connect to Helpdesk Server...").
		END.
		hReturn = NO.
		hdeskServer:DISCONNECT() NO-ERROR.
		DELETE OBJECT hdeskServer NO-ERROR.
	END.
	ELSE IF SEARCH(hotellist) NE ? THEN DO: /*nc-24/12/2024*/
		lOk = TEMP-TABLE hotel:READ-XML("file",                /* SourceType             */
                                hotellist,    /* File                   */
                                "empty",              /* ReadMode               */
                                ?,                     /* SchemaLocation         */
                                ?,                     /* OverrideDefaultMapping */
                                ?,                     /* FieldTypeMapping       */
                                ?).                    /* VerifySchemaMode       */
		hotelfile = YES.	
	END.
	ELSE DO:
		filepath = drive + logpath.
		workpath = drive + logpath + "log\".
		grp = 1.
    
		CREATE hotel.
		ASSIGN
			hotel.number = 1
			hotel.ip = vHost
			hotel.port = vService
			hotel.becode = bookengID
			hotel.grp = 1
		.
		IF SEARCH(filepath) EQ ? THEN
			OS-COMMAND SILENT VALUE("mkdir " + filepath).
		IF SEARCH(workpath) EQ ? THEN
			OS-COMMAND SILENT VALUE("mkdir " + workpath).
	END.
    IF hotelfile THEN DO:
        workpath = drive + logpath.
    
        IF SUBSTR(workpath,LENGTH(workpath),1) NE CHR(92) THEN
        workpath = workpath + CHR(92).
    END.
	FIND FIRST hotel NO-LOCK NO-ERROR.
	IF AVAILABLE hotel THEN
	DO:
		filepath    = FILE-INFO:FULL-PATHNAME.
		DO i = 1 TO LENGTH(filepath):
			huruf = SUBSTR(filepath,i,1).
			IF huruf = "0" OR huruf = "1" OR huruf = "2" OR huruf = "3" OR huruf = "4" OR huruf = "5" OR huruf = "6" OR huruf = "7" OR huruf = "8" OR huruf = "9" THEN
			DO:
				grp = INT(SUBSTR(filepath,i)).
				LEAVE.
			END.
		END.
	END.
END.

PROCEDURE connect-hServer:
	DEFINE INPUT PARAMETER ip AS CHARACTER INIT NO.
	DEFINE INPUT PARAMETER port AS CHARACTER INIT NO.
    DEFINE OUTPUT PARAMETER lReturn AS LOGICAL INIT NO.
    IF ip NE "" AND port NE "" THEN
    DO:
        CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait").
        PROCESS EVENTS.
        vAppParam = " -H " + ip + " -S " + port + " -DirectConnect -sessionModel Session-free".
       /* lReturn = hServer:CONNECT(vAppParam, ? , ? , ?) NO-ERROR.
        IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
        RUN logmess("ERROR|" + ERROR-STATUS:GET-MESSAGE(1)).*/
         errorMsg = "".
        RUN hserver-connection-if.p(OUTPUT lReturn, OUTPUT errorMsg). 
        IF errorMsg NE "" THEN
            RUN logmess(errorMsg).
        CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").
    END.
    ELSE 
    DO:
        hServer = SESSION:HANDLE.
        lReturn = YES.
        RUN logmess("Running Locally, Hotel IP and Port Not Found...").
    END.

    IF errorMsg NE "" OR lReturn = NO THEN
    DO:
        RUN send-email("error", "", htl-code, "Dear Partner, there is an error while accessing the database of " + hotel.NAME + "." + CHR(10) + errormsg).
    END.
    ELSE
    DO:
        IF hotel.errorcounter NE 0 THEN RUN update-xml("error", "reset").
    END.
END.

PROCEDURE connect-hserver-artotel:
    DEFINE OUTPUT PARAMETER lReturn AS LOGICAL INIT NO.

    CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait").
    PROCESS EVENTS.
    vAppParam = " -H " + abi-host + " -S " + abi-port + " -DirectConnect -sessionModel Session-free".
    errorMsg = "".
    RUN hserver-connection-if.p(OUTPUT lReturn, OUTPUT errorMsg).
    IF errorMsg NE "" THEN
        RUN logmess(errorMsg).

    CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").

END PROCEDURE.

PROCEDURE connect-hdeskServer:
	DEFINE INPUT PARAMETER ip AS CHARACTER INIT NO.
	DEFINE INPUT PARAMETER port AS CHARACTER INIT NO.
    DEFINE OUTPUT PARAMETER hReturn AS LOGICAL INIT NO.
    
    DEFINE VARIABLE timestr  AS CHARACTER NO-UNDO.
    IF ip NE "" AND port NE "" THEN
    DO:
      CURRENT-WINDOW:LOAD-MOUSE-POINTER("wait").
      PROCESS EVENTS.
      vAppParam = " -H " + ip + " -S " + port + " -DirectConnect -sessionModel Session-free".
      errorMsg = "".
		 hReturn = hdeskServer:CONNECT(vAppParam, ? , ? , ?) NO-ERROR. /*normal*/
		IF ERROR-STATUS:GET-MESSAGE(1) NE '' THEN
			errorMsg = "ERROR|" + ERROR-STATUS:GET-MESSAGE(1).
		CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").
		IF NOT hReturn THEN  
			errorMsg = errorMsg + " ERROR|Can not connect to the AppServer.".
		IF errorMsg NE "" THEN
			  RUN logmess(errorMsg).
		  CURRENT-WINDOW:LOAD-MOUSE-POINTER("arrow").
    END.
    ELSE 
    DO:
        hReturn = NO.
        timestr = STRING(TIME,"HH:MM:SS").
        RUN logmess(timestr + " Hdesk Server did not connect, Hdesk Server IP and Port Not Found...").
    END.              
END.

PROCEDURE find-start-date:
    DEFINE INPUT PARAMETER inp-date AS DATE.
    DEFINE INPUT PARAMETER compare-date AS DATE.
    DEFINE OUTPUT PARAMETER out-date AS DATE.

    IF inp-date LE compare-date THEN
        out-date = inp-date.
    ELSE out-date = compare-date.
END PROCEDURE.
PROCEDURE find-end-date:
    DEFINE INPUT PARAMETER inp-date AS DATE.
    DEFINE INPUT PARAMETER compare-date AS DATE.
    DEFINE OUTPUT PARAMETER out-date AS DATE.

    IF inp-date GE compare-date THEN
        out-date = inp-date.
    ELSE out-date = compare-date.
END PROCEDURE.

PROCEDURE mt-program:
    DEFINE VARIABLE filemt  AS CHAR INIT "".
    DEFINE VARIABLE filecmt AS CHAR INIT "".
    DEFINE VARIABLE filenm  AS CHAR INIT "".
    DEFINE VARIABLE str-param AS CHAR INIT "".
    DEFINE VARIABLE param1 AS CHAR INIT "".
    
    ASSIGN                                       
        filemt = filepath + "\MP-SM" + STRING(grp) + ".exe"
        filecmt = filepath + "\config.ini".

    IF SEARCH(filemt) NE ? AND SEARCH(filecmt) NE ? THEN
    DO:
        INPUT STREAM s1 FROM VALUE (filecmt).
        REPEAT:
            IMPORT STREAM s1 UNFORMATTED str-param NO-ERROR.
            IF (NOT str-param MATCHES "*#*" OR NOT str-param MATCHES "#*") AND NUM-ENTRIES(str-param, "=") = 2 THEN
            DO: 
                param1 = ENTRY(1, str-param, "=").
                IF param1 MATCHES ("*FILENAME*") THEN
                    filenm = TRIM(ENTRY(2, str-param, "=")).
                IF filenm NE "" THEN LEAVE.
            END.
        END.
        INPUT STREAM s1 CLOSE. 
        
        ASSIGN
            filenm = filepath + "\" + filenm
            str-param = "LANGSUNG".
        
        OUTPUT STREAM s2 TO VALUE(filenm).
        DO i = 1 TO LENGTH(str-param) :
            PUT STREAM s2 UNFORMATTED STRING(SUBSTR(str-param, i, 1)) FORMAT "x(1)".
        END.        
        OUTPUT STREAM s2 CLOSE.
        QUIT.
    END.
END.

PROCEDURE create-file-monitoring:
    
    DEFINE VARIABLE curr-date       AS CHAR.
    DEFINE VARIABLE curr-date-rep   AS CHAR.
    DEFINE VARIABLE curr-time       AS CHAR.
    DEFINE VARIABLE curr-time-rep   AS CHAR.

    DEFINE VARIABLE filemt  AS CHAR INIT "".
    DEFINE VARIABLE filecmt AS CHAR INIT "".
    DEFINE VARIABLE filenm  AS CHAR INIT "".
    DEFINE VARIABLE str-param AS CHAR INIT "".
    DEFINE VARIABLE param1 AS CHAR INIT "".

     ASSIGN                                       
        filemt = filepath + "\MP-SM" + STRING(grp) + ".exe"
        filecmt = filepath + "\config.ini"
        curr-date = STRING(TODAY, "99/99/9999")
        curr-date-rep = REPLACE(curr-date, "/", "")
        curr-time = STRING(TIME, "HH:MM:SS")
        curr-time-rep = REPLACE(curr-time, ":", "").

    IF SEARCH(filemt) NE ? AND SEARCH(filecmt) NE ? THEN
    DO:
        INPUT STREAM s1 FROM VALUE (filecmt).
        REPEAT:
            IMPORT STREAM s1 UNFORMATTED str-param NO-ERROR.
            IF (NOT str-param MATCHES "*#*" OR NOT str-param MATCHES "#*") 
                AND NUM-ENTRIES(str-param, "=") = 2 THEN
            DO: 
                param1 = ENTRY(1, str-param, "=").
                IF param1 MATCHES ("*FILENAME*") THEN
                    filenm = TRIM(ENTRY(2, str-param, "=")).
                IF filenm NE "" THEN LEAVE.
            END.
        END.
        INPUT STREAM s1 CLOSE.

        

        IF filenm NE "" THEN
        DO:
            filenm = filepath + filenm.
            IF SEARCH(filenm) NE ? THEN
                DOS SILENT DEL VALUE(filenm).
            OUTPUT STREAM s1 TO VALUE(filenm).
            PUT STREAM s1
                curr-date-rep " " curr-time-rep.
            OUTPUT STREAM s1 CLOSE.
        END.
    END.
    
END.

PROCEDURE disp-mess:
    DEFINE INPUT PARAMETER mess1 AS CHAR.
    
    IF mess1 = "" THEN RETURN.
    
    tot-rec = tot-rec + 1.

    IF tot-rec = 1 THEN message1[1] = mess1.
    ELSE IF tot-rec = 2 THEN message1[2] = mess1.
    ELSE IF tot-rec = 3 THEN message1[3] = mess1.
    ELSE IF tot-rec = 4 THEN message1[4] = mess1.
    ELSE IF tot-rec = 5 THEN message1[5] = mess1.
    ELSE IF tot-rec = 6 THEN message1[6] = mess1.
    ELSE IF tot-rec = 7 THEN message1[7] = mess1.
    ELSE IF tot-rec = 8 THEN message1[8] = mess1.
    ELSE IF tot-rec = 9 THEN message1[9] = mess1.
    ELSE IF tot-rec = 10 THEN message1[10] = mess1.
    ELSE IF tot-rec = 11 THEN message1[11] = mess1.
    ELSE IF tot-rec = 12 THEN message1[12] = mess1.
    ELSE
    DO:
        message1[1]  = message1[2].
        message1[2]  = message1[3].
        message1[3]  = message1[4].
        message1[4]  = message1[5].
        message1[5]  = message1[6].
        message1[6]  = message1[7].
        message1[7]  = message1[8].
        message1[8]  = message1[9].
        message1[9]  = message1[10].
        message1[10] = message1[11].
        message1[11] = message1[12].
        message1[12] = mess1.
    END.
    DISP message1 WITH FRAME frame1.
END.

PROCEDURE assign-frame:
    ASSIGN message1[1]:READ-ONLY IN FRAME frame1 = YES
           message1[2]:READ-ONLY IN FRAME frame1 = YES
           message1[3]:READ-ONLY IN FRAME frame1 = YES
           message1[4]:READ-ONLY IN FRAME frame1 = YES
           message1[5]:READ-ONLY IN FRAME frame1 = YES
           message1[6]:READ-ONLY IN FRAME frame1 = YES
           message1[7]:READ-ONLY IN FRAME frame1 = YES
           message1[8]:READ-ONLY IN FRAME frame1 = YES
           message1[9]:READ-ONLY IN FRAME frame1 = YES
           message1[10]:READ-ONLY IN FRAME frame1 = YES
           message1[11]:READ-ONLY IN FRAME frame1 = YES
           message1[12]:READ-ONLY IN FRAME frame1 = YES
         .
END.
