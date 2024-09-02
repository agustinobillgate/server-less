@openapi.openedge.export FILE(type="REST", executionMode="external", useReturnValue="false", writeDataSetBeforeImage="false").

DEFINE INPUT PARAMETER input-username AS CHARACTER.
DEFINE INPUT PARAMETER input-userkey AS CHARACTER.
DEFINE OUTPUT PARAMETER output-ok-flag AS LOGICAL INITIAL NO.
DEFINE TEMP-TABLE cost-list
  FIELD num AS INTEGER FORMAT "9999"
  FIELD name AS CHAR FORMAT "x(24)".
.

DEF OUTPUT PARAMETER double-currency    AS LOGICAL. 
DEF OUTPUT PARAMETER price-decimal      AS INTEGER. 
DEF OUTPUT PARAMETER cost1              AS INTEGER. 
DEF OUTPUT PARAMETER cost2              AS INTEGER. 
DEF OUTPUT PARAMETER TABLE FOR cost-list.
