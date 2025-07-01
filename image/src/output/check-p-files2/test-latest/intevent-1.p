/*---------------------------------------------------------------------------
  intevent.p          Larry Barnhill jr. 1.1
  Created:            09/08/95
  Last updated:
    07/11/95 LBJR for new intevent-1.i
    18/12/97 LBJR Added Voicemailbox-event (htparm 1039)
    06/12/99 LBJR htlogic used
  NOTES:
  SYNTAX:
          DEF VAR ev-type     AS INTEGER.
          DEF VAR zinr        AS CHAR.
          DEF VAR parms       AS CHAR.
  PRE-CONDITIONS:
  POST-CONDITIONS:
          For each interface interested in 'ev-type' a record is added in
          file 'interfaces'.
          Interested Interfaces have to set their appropiate htparam values
          397  POS                           Key = 1
          398  Telephone                     Key = 2
          399  Video /* select TV */         Key = 3
          437  Energy-Management             Key = 4
          438  Key-Cards                     Key = 5
          1070 Voice-Box System              Key = 6
          249  Greeting Emails               key = 7
          TBD  Priscilla                     Key = 10
          TBD  Loyalty                       Key = 11
          TBD  NewGCF                        Key = 36   /* tambahan CRG 23Nov18 */
          TBD  Guest_Concierge               Key = 37   /* Adding BLY 140125 */

  NOTE!!!!: intevent-1.i 5 .... used for CRM, defined in res-checkout.p
  
  EVENT-TYPES:
    As in input parameter ev-type:
          1  Checkin
          2  Checkout
          3  Roomchange
          4  Messagelamp on
          5  Messagelamp off
          6  Wakeup
          7  Do not Disturb On
          8  Do not Disturb Off
          9  Modify
          10 Walk-in
          11 Insert
          12 New
          13 Split
          14 Cancel
          15 Delete
  EXAMPLE:
   RUN intevent.p( 1, "666", "My Checkin!").
   RUN intevent1.p ( 2, 1,  "666", "My Checkin for telephone!").
 
 -------------------------------------------------------------------------- */
DEF INPUT PARAMETER ev-type          AS INTEGER.
DEF INPUT PARAMETER zinr             AS CHAR.
DEF INPUT PARAMETER parms            AS CHAR.
DEF INPUT PARAMETER resNo            AS INTEGER.
DEF INPUT PARAMETER reslinNo         AS INTEGER.

/*
DEF VARIABLE ev-type          AS INTEGER INIT 1.
DEF VARIABLE zinr             AS CHAR INIT "206".
DEF VARIABLE parms            AS CHAR INIT "My Checkin!".
DEF VARIABLE resNo            AS INTEGER INIT 125175.
DEF VARIABLE reslinNo         AS INTEGER INIT 2.
*/
/* ------------------------------------------------------------------------ */
DEF VAR             doEvent          AS LOGICAL                 NO-UNDO.
DEF VAR             do-it            AS LOGICAL                 NO-UNDO.
DEF VAR             parms-mapping    AS CHAR                    NO-UNDO.
DEF VAR             chdoEvent        AS CHAR                    NO-UNDO.
DEF VAR             chardoEvent      AS CHAR                    NO-UNDO.
DEF VAR             parms-flag       AS CHAR                    NO-UNDO.

DEF BUFFER          res-line1        FOR res-line.

/* manual checkin/checkout comes from LineSwitching update-rmext.p */
/* Activate! and Deactivate! comes from telop.p */
IF NUM-ENTRIES(parms) GT 1 THEN
DO:
    IF ENTRY(1,parms,";") = "Activate!"             THEN parms-mapping = "My Checkin!".
    ELSE IF ENTRY(1,parms,";") = "Manual Checkin!"  THEN parms-mapping = "My Checkin!".
    ELSE IF ENTRY(1,parms,";") = "Deactivate!"      THEN parms-mapping = "My Checkout!".
    ELSE IF ENTRY(1,parms,";") = "Manual Checkout!" THEN parms-mapping = "My Checkout!".
    ELSE parms-mapping = ENTRY(1,parms,";").
    parms-flag = ENTRY(2,parms,";").
END.
ELSE
DO:
    IF parms = "Activate!"             THEN parms-mapping = "My Checkin!".
    ELSE IF parms = "Manual Checkin!"  THEN parms-mapping = "My Checkin!".
    ELSE IF parms = "Deactivate!"      THEN parms-mapping = "My Checkout!".
    ELSE IF parms = "Manual Checkout!" THEN parms-mapping = "My Checkout!".
    ELSE parms-mapping = parms.
    parms-flag = "".    
END.

IF parms NE "Priscilla" AND parms NE "Loyalty" AND parms NE "newgcf" AND parms NE "closemonth" THEN
DO:
  FIND FIRST res-line WHERE res-line.resnr = resNo
     AND res-line.reslinnr = reslinNo NO-LOCK NO-ERROR.
  IF AVAILABLE res-line THEN
    FIND FIRST res-line1 WHERE res-line1.active-flag = 1 
      AND (res-line1.resstatus = 6 OR res-line1.resstatus = 13)
      AND res-line1.zinr = res-line.zinr 
      AND res-line1.l-zuordnung[3] = 0
      AND RECID(res-line1) NE RECID(res-line) NO-LOCK NO-ERROR.        


    /* Nettify Wiffi for send data room sharer */
    RUN htpchar.p(341, OUTPUT chardoEvent).
    IF chardoEvent MATCHES "*nettify*" THEN
    DO:
        IF AVAILABLE res-line1 THEN
            FIND FIRST res-line1 WHERE res-line1.active-flag = 1 
                AND res-line1.resstatus = 11            /* CREATE TRIGGER FOR ROOMSHARER */
                AND res-line1.zinr = res-line.zinr 
                AND res-line1.l-zuordnung[3] = 0
                AND RECID(res-line1) NE RECID(res-line) 
                AND res-line1.reslinnr NE res-line.reslinnr NO-LOCK NO-ERROR.
    END.

    IF parms = "My Checkin!" OR parms = "My Checkout!" THEN
      do-it = NOT AVAILABLE res-line1.
    ELSE do-it = YES.

    IF do-it THEN
    DO:
        {intevent-1.i 39 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /*Digital First - Trigger Checkin*/      

        IF parms-flag EQ "PABX" THEN
        DO:
            RUN htplogic.p(398, OUTPUT doEvent).
            IF doEvent THEN DO:
                {intevent-1.i 2 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 2 = Telephone */
            END.
        END.
        IF parms-flag MATCHES "*WIFI*" THEN
        DO:
            RUN htpchar.p(341, OUTPUT chardoEvent).
            IF chardoEvent NE "" THEN DO:
                {intevent-1.i 9 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 9 = WiFi */
            END.                                           
        END.
        IF parms-flag EQ "" THEN
        DO:
            RUN htplogic.p(398, OUTPUT doEvent).
            IF doEvent THEN DO:
                {intevent-1.i 2 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 2 = Telephone */
            END.
            RUN htpchar.p(341, OUTPUT chardoEvent).
            IF chardoEvent NE "" THEN DO:
                {intevent-1.i 9 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 9 = WiFi */
            END.                 
        END.
        RUN htplogic.p(358, OUTPUT doEvent).
        IF doEvent AND ev-type GE 1 AND ev-type LE 3 THEN DO:
            {intevent-1.i 4 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 4 = Internet Billing */
        END.
    
        FIND FIRST htparam WHERE htparam.paramnr = 1070 NO-LOCK.
        IF htparam.flogical AND htparam.feldtyp = 4 AND ev-type GE 1 AND ev-type LE 3 THEN DO:
            {intevent-1.i 6 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 6 = Voice-Box System */
        END.
    END.
    
    FIND FIRST htparam WHERE htparam.paramnr = 249 NO-LOCK.
    IF htparam.flogical AND htparam.paramgr = 6 
        AND ev-type GE 1 AND ev-type LE 3 THEN
    DO:
        /* (request) kirim ci-greetingemail H-ankunft dan co-greetingemail H+abreise, CHIRAG 23Jan2019 */
        DEFINE VARIABLE progname AS CHAR NO-UNDO INITIAL "nt-custom-emailtrigger.r".
        FIND FIRST nightaudit WHERE nightaudit.programm = progname NO-LOCK NO-ERROR.    /* utk check apakah C/O akan dikirim seperti biasa? (YES=biasa NO=customtrigger) */
        IF AVAILABLE nightaudit THEN                                                    /* ketemu=property memang memakai fitur ini */
        DO:
            IF nightaudit.selektion THEN .                                              /* tidak perlu di definisikan karena sudah di handle dalam nt-custom-emailtrigger.p */
            ELSE                                                                        /* NO=create seperti biasa */
                {intevent-1.i 7 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 7 = Greeting Email */
        END.
        ELSE IF NOT AVAILABLE nightaudit THEN                                           /* create table interface seperti biasa karena property tidak memakai fitur ini */
            {intevent-1.i 7 ev-type zinr parms-mapping zinr 0 resNo reslinNo} /* 7 = Greeting Email */
    END.
    
    RUN htplogic.p(359, OUTPUT doEvent).         /* chg fr 399 to 359=Licence */
    IF doEvent THEN DO:
        {intevent-1.i 3 ev-type zinr parms zinr 0 resNo reslinNo} /* 3 = SelectTV */
        {intevent-1.i 33 ev-type zinr parms zinr 0 resNo reslinNo} /* 3 = SelectTV */
    END.
END.

/* tambahan untuk GuestProfile Chrondigital (Damien Lee) CRG 23Nov18 */
IF parms = "newgcf" THEN
    {intevent-1.i 36 ev-type zinr parms zinr 0 resNo reslinNo}

/* Request Tauzia, GL close month trigger CRG 11Sept20 */
IF parms = "closemonth" THEN
    {intevent-1.i 37 ev-type zinr parms zinr 0 resNo reslinNo}


IF parms = "Loyalty" THEN
DO:   
    /* NEW */
    IF ev-type = 1 /*checkin*/ THEN   
    DO:
        DO TRANSACTION.
          CREATE INTERFACE.
          ASSIGN
            INTERFACE.KEY         = 11
            INTERFACE.zinr        = zinr
            INTERFACE.nebenstelle = ""
            INTERFACE.intfield    = 0
            INTERFACE.decfield    = ev-type
            INTERFACE.int-time    = TIME
            INTERFACE.intdate     = TODAY
            INTERFACE.parameters  = "newbill"
            INTERFACE.resnr       = resNo
            INTERFACE.reslinnr    = reslinNo
          .
          FIND CURRENT INTERFACE NO-LOCK.
          RELEASE INTERFACE.
        END. /* ... DO TRANSACTION */    
    END.
    /**/

    /* OLD 
    IF ev-type = 1 /*checkin*/ THEN
        {intevent-1.i 11 ev-type zinr 'newbill' '' 0 resNo reslinNo}
    */
END.

/*
FIND FIRST htparam WHERE htparam.paramnr = ... NO-LOCK.
IF htparam.flogical THEN DO:*/
    IF parms = "Priscilla" THEN /* 10 = Priscilla Apps */
        DO:        
        IF ev-type = 1 /*checkin*/ THEN
            {intevent-1.i 10 ev-type zinr 'checkin' '' 0 resNo reslinNo}
        ELSE IF ev-type = 2 /*checkout*/ THEN
            {intevent-1.i 10 ev-type zinr 'checkout' '' 0 resNo reslinNo}
        ELSE IF ev-type = 9 /*modify*/ THEN
            {intevent-1.i 10 ev-type zinr 'modify' '' 0 resNo reslinNo}
        ELSE IF ev-type = 10 /*qci*/ THEN
            {intevent-1.i 10 ev-type zinr 'qci' '' 0 resNo reslinNo}
        ELSE IF ev-type = 11 /*insert*/ THEN
            {intevent-1.i 10 ev-type zinr 'insert' '' 0 resNo reslinNo}
        ELSE IF ev-type = 12 /*new*/ THEN
            {intevent-1.i 10 ev-type zinr 'new' '' 0 resNo reslinNo}
        ELSE IF ev-type = 13 /*split*/ THEN
            {intevent-1.i 10 ev-type zinr 'split' '' 0 resNo reslinNo}
        ELSE IF ev-type = 14 /*cancel*/ THEN
            {intevent-1.i 10 ev-type zinr 'cancel' '' 0 resNo reslinNo}
        ELSE IF ev-type = 15 /*delete*/ THEN       
            {intevent-1.i 10 ev-type zinr 'delete' '' 0 resNo reslinNo} 
        
    END.
/*END.*/
/* NOTE!!!!: intevent-1.i 5 .... used for CRM, defined in res-checkout.p */

IF parms = "bridge" THEN /* 11 = Bridge Interface for OHM */
DO:    
         IF ev-type = 1 /*checkin*/  THEN {intevent-1.i 11 ev-type zinr 'generalledger' '' 0 resNo reslinNo}
    ELSE IF ev-type = 2 /*checkout*/ THEN {intevent-1.i 11 ev-type zinr 'checkout' '' 0 resNo reslinNo}
    ELSE IF ev-type = 9 /*modify*/   THEN {intevent-1.i 11 ev-type zinr 'modify' '' 0 resNo reslinNo}
    ELSE IF ev-type = 10 /*qci*/ THEN
        {intevent-1.i 11 ev-type zinr 'qci' '' 0 resNo reslinNo}
    ELSE IF ev-type = 11 /*insert*/ THEN
        {intevent-1.i 11 ev-type zinr 'insert' '' 0 resNo reslinNo}
    ELSE IF ev-type = 12 /*new*/ THEN
        {intevent-1.i 11 ev-type zinr 'new' '' 0 resNo reslinNo}
    ELSE IF ev-type = 13 /*split*/ THEN
        {intevent-1.i 11 ev-type zinr 'split' '' 0 resNo reslinNo}
    ELSE IF ev-type = 14 /*cancel*/ THEN
        {intevent-1.i 11 ev-type zinr 'cancel' '' 0 resNo reslinNo}
    ELSE IF ev-type = 15 /*delete*/ THEN       
        {intevent-1.i 11 ev-type zinr 'delete' '' 0 resNo reslinNo}  
END.

/* BLY Adding Key For FCS1 IF -    96468D */
RUN htplogic.p(298, OUTPUT doEvent).
IF doEvent THEN
DO:
    IF ev-type = 9 /*modify*/ THEN
            {intevent-1.i 38 ev-type zinr 'modify' '' 0 resNo reslinNo}
        ELSE IF ev-type = 10 /*qci*/ THEN
            {intevent-1.i 38 ev-type zinr 'qci' '' 0 resNo reslinNo}
        ELSE IF ev-type = 11 /*insert*/ THEN
            {intevent-1.i 38 ev-type zinr 'insert' '' 0 resNo reslinNo}
        ELSE IF ev-type = 12 /*new*/ THEN
            {intevent-1.i 38 ev-type zinr 'new' '' 0 resNo reslinNo}
        ELSE IF ev-type = 13 /*split*/ THEN
            {intevent-1.i 38 ev-type zinr 'split' '' 0 resNo reslinNo}
        ELSE IF ev-type = 14 /*cancel*/ THEN
            {intevent-1.i 38 ev-type zinr 'cancel' '' 0 resNo reslinNo}
        ELSE IF ev-type = 15 /*delete*/ THEN       
            {intevent-1.i 38 ev-type zinr 'delete' '' 0 resNo reslinNo}
    ELSE {intevent-1.i 38 ev-type zinr parms zinr 0 resNo reslinNo}
END.
/* End BLY */
