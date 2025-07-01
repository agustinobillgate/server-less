
DEFINE OUTPUT PARAMETER datetime-server AS CHARACTER INITIAL "".

DEFINE VARIABLE bill-date AS DATE.
DEFINE VARIABLE curr-zeit AS INTEGER.

curr-zeit = TIME.
datetime-server = STRING(TODAY) + " " + STRING(curr-zeit, "HH:MM:SS").

