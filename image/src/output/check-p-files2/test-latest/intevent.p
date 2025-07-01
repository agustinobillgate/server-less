/*---------------------------------------------------------------------------
  intevent.p          Larry Barnhill jr. 1.1
  Created:            09/08/95
  Last updated:
    07/11/95 LBJR for new intevent.i
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
  EXAMPLE:
   RUN intevent.p( 1, "666", "My Checkin!").
   RUN intevent1.p ( 2, 1,  "666", "My Checkin for telephone!").
 -------------------------------------------------------------------------- */
DEF INPUT PARAMETER ev-type          AS INTEGER.
DEF INPUT PARAMETER zinr             AS CHAR.
DEF INPUT PARAMETER parms            AS CHAR.
/* ------------------------------------------------------------------------ */
DEF VAR             doEvent          AS LOGICAL                 NO-UNDO.
DEF VAR             parms-mapping    AS CHAR                    NO-UNDO.

IF parms = "Activate!" THEN parms-mapping = "My Checkin!".
ELSE IF parms = "Manual Checkin!" THEN parms-mapping = "My Checkin!".
ELSE IF parms = "Deactivate!" THEN parms-mapping = "My Checkout!".
ELSE IF parms = "Manual Checkout!" THEN parms-mapping = "My Checkout!".
ELSE parms-mapping = parms.

RUN htplogic.p(398, OUTPUT doEvent).
IF doEvent THEN DO:
    {intevent.i 2 ev-type zinr parms-mapping zinr 0} /* 2 = Telephone */
END.

RUN htplogic.p(359, OUTPUT doEvent).         /* chg fr 399 to 359=Licence */
IF doEvent THEN DO:
    {intevent.i 3 ev-type zinr parms zinr 0} /* 3 = SelectTV */
END.

RUN htplogic.p(358, OUTPUT doEvent).
IF doEvent AND ev-type GE 1 AND ev-type LE 3 THEN DO:
    {intevent.i 4 ev-type zinr parms-mapping zinr 0} /* 4 = Internet Billing */
END.

/* NOTE!!!!: intevent.i 5 .... used for CRM, defined in res-checkout.p */


/* currently not used
RUN htplogic.p(397, OUTPUT doEvent).
IF doEvent THEN DO:
    {intevent.i 1 ev-type zinr parms zinr 0}  /* 1 = POS */
END.
*/

/*
RUN htplogic.p(437, OUTPUT doEvent). /* do not use 437 !! */
IF doEvent THEN DO:
    {intevent.i 4 ev-type zinr parms zinr 0} /* 4 = EMS */
END.
*/

/*  changed to queasy where key = 30
RUN htplogic.p(438, OUTPUT doEvent). /* used for internet booking */
IF doEvent THEN DO:
    {intevent.i 5 ev-type zinr parms zinr 0} /* 5 = KeyCards */
END.
*/

/* currently not used
RUN htplogic.p(1070, OUTPUT doEvent).
IF doEvent THEN DO:
    {intevent.i 6 ev-type zinr parms zinr 0} /* 6 = VoiceBox */
END.
*/
/* ------------------------------------------------------------------------ */
