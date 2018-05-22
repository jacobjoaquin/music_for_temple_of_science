
<CsoundSynthesizer>
<CsInstruments>
sr = 44100
kr = 44100
ksmps = 1
nchnls = 2
0dbfs = 0.5

gifadein = 1
gifadeout = 1
gifadepercent = 0.05

; Diskin Mono
instr 1
  idur = p3
  iamp = p4
  ipch = p5
  SFilename = p6
  istart_time = p7
  imix = p8

  cigoto (idur > gifadein + gifadeout), fade
  igoto fadepercent

fade:
  ifadein = gifadein
  ifadeout = gifadeout
  goto cont

fadepercent:
  ifadein = idur * gifadepercent
  ifadeout = idur * gifadepercent
  goto cont

cont:
  ;aline linseg 0, ifadein, 1, idur - ifadeout, 1, ifadeout, 0
  aline linseg 0, ifadein, 1, idur - (ifadeout + ifadein), 0

  a0 diskin SFilename, ipch, istart_time, 1, 0, 32
  a0 *= iamp
  a0 = a0 * aline
  outs a0 * imix, a0 * imix

  chnmix a0 * (1 - imix), "leftmono"
  chnmix a0 * (1 - imix), "rightmono"
endin

; Diskin Stereo player
instr 2
  idur = p3
  iamp = p4
  ipch = p5
  SFilename = p6
  istart_time = p7
  imix = p8

  cigoto (idur > gifadein + gifadeout), fade
  igoto fadepercent

fade:
  ifadein = gifadein
  ifadeout = gifadeout
  goto cont

fadepercent:
  ifadein = idur * gifadepercent
  ifadeout = idur * gifadepercent
  goto cont

cont:
  ;aline linseg 0, ifadein, 1, idur - ifadeout, 1, ifadeout, 0
  aline linseg 0, ifadein, 1, idur - (ifadeout + ifadein), 0

  a0, a1 diskin SFilename, ipch, istart_time, 1, 0, 32
  a0 *= iamp
  a1 *= iamp
  a0 = a0 * aline
  a1 = a1 * aline
  outs a0 * imix, a1 * imix

  chnmix a0 * (1 - imix), "left"
  chnmix a1 * (1 - imix), "right"
endin

instr 100
  iamp = p4 * 0.5
  idelay_left = p5
  idelay_right = p6
  iroom_size = p7
  iHFDamp = p8

  itime = 1
  ifb = 0.25

  aleft chnget "left"
  aright chnget "right"

  aleft delay aleft, idelay_left
  aright delay aright, idelay_right

  adelayl delayr itime * 0.95
  delayw aleft + adelayl * ifb
  adelayr delayr itime
  delayw aright + adelayr * ifb * 0.95

  al, ar freeverb adelayl, adelayr, iroom_size, iHFDamp
  outs (al + adelayr) * iamp * 0.5, (ar + adelayl) * iamp * 0.5

;  outs adelayl * iamp, adelayr * iamp
  chnclear "left"
  chnclear "right"
endin

instr 101
  iamp = p4 * 0.5
  idelay_left = p5
  idelay_right = p6
  iroom_size = p7
  iHFDamp = p8

  itime = 0.617
  ifb = 0.25

  aleft chnget "leftmono"
  aright chnget "rightmono"

  aleft delay aleft, idelay_left
  aright delay aright, idelay_right

  adelayl delayr itime * 0.95
  delayw aleft + adelayl * ifb
  adelayr delayr itime
  delayw aright + adelayr * ifb * 0.95

  al, ar freeverb adelayl, adelayr, iroom_size, iHFDamp
  outs (al + adelayr) * iamp * 0.5, (ar + adelayl) * iamp * 0.5

;  outs adelayl * iamp, adelayr * iamp
  chnclear "leftmono"
  chnclear "rightmono"
endin


</CsInstruments>
<CsScore bin="python">
execfile('tos_score.py')
</CsScore>
</CsoundSynthesizer>
