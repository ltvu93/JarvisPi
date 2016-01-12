#!/bin/bash
text2wfreq < jarvispi.txt | wfreq2vocab > jarvispi.vocab
text2idngram -vocab jarvispi.vocab -idngram jarvispi.idngram < jarvispi.txt
idngram2lm -vocab_type 0 -idngram jarvispi.idngram -vocab jarvispi.vocab -arpa jarvispi.arpa
sphinx_lm_convert -i jarvispi.arpa -o jarvispi.lm.DMP
