#!/usr/bin/env python3
"""
DEV UTILITY — regenerates the sounds/ WAV files from scratch.
Not needed at runtime. Run this if you want to tweak the tones.

Requires Python 3. No additional packages needed.

Usage:
  python generate-sounds.py          # regenerates all sounds/*.wav
"""

import os, math, struct

SR = 44100
OUT_DIR = os.path.join(os.path.dirname(__file__), "sounds")


def chord(freqs, ms, vol=0.62, dk=3.8, vib=0.0, vr=5.2):
    n = int(SR * ms / 1000); atk = max(1, int(n * 0.025)); dur = ms / 1000; buf = []
    for i in range(n):
        t = i / SR
        env = (i / atk if i < atk else 1.0) * math.exp(-dk * t / dur)
        mix = sum(math.sin(2*math.pi*(hz + vib*math.sin(2*math.pi*vr*t))*t) for hz in freqs) / len(freqs)
        buf.append(vol * env * mix)
    return buf


def render(score):
    buf = []
    for ev in score:
        buf += chord(ev['f'], ev['ms'], dk=ev.get('dk', 3.8), vib=ev.get('vib', 0.0), vr=ev.get('vr', 5.2))
        buf += [0.0] * int(SR * ev.get('gap', 60) / 1000)
    pcm = struct.pack(f'<{len(buf)}h', *[max(-32767, min(32767, int(s * 32767))) for s in buf])
    hdr = struct.pack('<4sI4s4sIHHIIHH4sI', b'RIFF', 36+len(pcm), b'WAVE', b'fmt ', 16, 1, 1, SR, SR*2, 2, 16, b'data', len(pcm))
    return hdr + pcm


SCORES = {
    'calm':     [{'f': [294, 392, 440], 'ms': 600, 'dk': 2.5, 'vib': 1.8, 'vr': 4.5}],
    'curious':  [{'f': [294, 392], 'ms': 240, 'dk': 4.0, 'gap': 55},
                 {'f': [370, 494], 'ms': 240, 'dk': 4.0, 'gap': 55},
                 {'f': [440, 622], 'ms': 420, 'dk': 2.8, 'vib': 2.5, 'vr': 5.0}],
    'happy':    [{'f': [523, 659],  'ms': 170, 'dk': 4.5, 'gap': 40},
                 {'f': [659, 784],  'ms': 170, 'dk': 4.5, 'gap': 40},
                 {'f': [784, 1047], 'ms': 170, 'dk': 4.5, 'gap': 40},
                 {'f': [659, 784],  'ms': 130, 'dk': 5.0, 'gap': 35},
                 {'f': [784, 1047], 'ms': 420, 'dk': 2.5, 'vib': 3.0, 'vr': 5.5}],
    'excited':  [{'f': [659, 784],        'ms': 105, 'dk': 6.0, 'gap': 28},
                 {'f': [740, 880],        'ms': 105, 'dk': 6.0, 'gap': 28},
                 {'f': [831, 988],        'ms': 105, 'dk': 6.0, 'gap': 28},
                 {'f': [988, 1175],       'ms': 105, 'dk': 6.0, 'gap': 28},
                 {'f': [880, 1047, 1319], 'ms': 380, 'dk': 2.2, 'vib': 4.0, 'vr': 6.0},
                 {'f': [784, 1047],       'ms': 220, 'dk': 3.5}],
    'greeting': [{'f': [220, 330], 'ms': 300, 'dk': 3.5, 'gap': 70},
                 {'f': [277, 415], 'ms': 300, 'dk': 3.5, 'gap': 70},
                 {'f': [330, 494], 'ms': 300, 'dk': 3.5, 'gap': 70},
                 {'f': [415, 622], 'ms': 300, 'dk': 3.5, 'gap': 70},
                 {'f': [494, 740], 'ms': 560, 'dk': 2.0, 'vib': 2.0, 'vr': 4.8}],
    'sad':      [{'f': [370, 494], 'ms': 460, 'dk': 2.5, 'gap': 80},
                 {'f': [330, 440], 'ms': 460, 'dk': 2.5, 'gap': 80},
                 {'f': [294, 370], 'ms': 460, 'dk': 2.5, 'gap': 80},
                 {'f': [247, 311], 'ms': 680, 'dk': 2.0}],
}


os.makedirs(OUT_DIR, exist_ok=True)
for mood, score in SCORES.items():
    path = os.path.join(OUT_DIR, f"{mood}.wav")
    with open(path, 'wb') as f:
        f.write(render(score))
    print(f"Generated {path}")

