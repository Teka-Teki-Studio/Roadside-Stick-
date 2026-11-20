"""Generate all Sprint 4 procedural chiptune SFX (22050 Hz, 16-bit PCM mono WAV)."""
import os, wave, struct, math, random

os.makedirs("assets/audio", exist_ok=True)
SR = 22050  # sample rate

def save_wav(path, samples):
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        for s in samples:
            v = max(-32767, min(32767, int(s)))
            w.writeframes(struct.pack("<h", v))

def square(t, freq):
    return 1.0 if (t * freq) % 1.0 < 0.5 else -1.0

def triangle(t, freq):
    p = (t * freq) % 1.0
    return (4.0 * abs(p - 0.5) - 1.0)

def noise():
    return random.uniform(-1.0, 1.0)

def env_adsr(i, total, a_frac=0.05, d_frac=0.1, s_level=0.6, r_frac=0.2):
    t = i / total
    a_end = a_frac
    d_end = a_frac + d_frac
    r_start = 1.0 - r_frac
    if t < a_end:
        return t / a_end
    elif t < d_end:
        return 1.0 - (1.0 - s_level) * ((t - a_end) / (d_end - a_end))
    elif t < r_start:
        return s_level
    else:
        return s_level * (1.0 - (t - r_start) / r_frac)

# 1. sfx_pickup.wav — bright ascending arpeggio (C5-E5-G5-C6)
def gen_pickup():
    freqs = [523.25, 659.25, 783.99, 1046.50]
    note_len = int(SR * 0.06)
    samples = []
    for freq in freqs:
        for i in range(note_len):
            t = i / SR
            e = env_adsr(i, note_len, 0.02, 0.15, 0.5, 0.3)
            s = square(t, freq) * 0.35 + triangle(t, freq * 2) * 0.15
            samples.append(s * e * 20000)
    save_wav("assets/audio/sfx_pickup.wav", samples)

# 2. sfx_drop.wav — descending boop
def gen_drop():
    n = int(SR * 0.15)
    samples = []
    for i in range(n):
        t = i / SR
        freq = 600 - 350 * (i / n)
        e = env_adsr(i, n, 0.02, 0.1, 0.4, 0.4)
        s = square(t, freq) * 0.4
        samples.append(s * e * 18000)
    save_wav("assets/audio/sfx_drop.wav", samples)

# 3. sfx_step.wav — very short percussive noise tap
def gen_step():
    n = int(SR * 0.04)
    samples = []
    for i in range(n):
        e = max(0, 1.0 - (i / n) * 3.0)
        s = noise() * 0.3 + square(i / SR, 150 + random.uniform(-20, 20)) * 0.15
        samples.append(s * e * 12000)
    save_wav("assets/audio/sfx_step.wav", samples)

# 4. sfx_extraction.wav — happy victory jingle (C5-E5-G5 arpeggio + sustained C6)
def gen_extraction():
    freqs = [523.25, 659.25, 783.99]
    note_len = int(SR * 0.1)
    final_len = int(SR * 0.25)
    samples = []
    for freq in freqs:
        for i in range(note_len):
            t = i / SR
            e = env_adsr(i, note_len, 0.03, 0.1, 0.6, 0.2)
            s = triangle(t, freq) * 0.4 + square(t, freq) * 0.2
            samples.append(s * e * 22000)
    for i in range(final_len):
        t = i / SR
        e = env_adsr(i, final_len, 0.05, 0.1, 0.5, 0.5)
        s = triangle(t, 1046.50) * 0.4 + square(t, 1046.50) * 0.15 + triangle(t, 523.25) * 0.1
        samples.append(s * e * 22000)
    save_wav("assets/audio/sfx_extraction.wav", samples)

# 5. sfx_hit.wav — harsh impact noise burst + low thud
def gen_hit():
    n = int(SR * 0.18)
    samples = []
    for i in range(n):
        t = i / SR
        e = max(0, 1.0 - (i / n) * 2.5)
        s = noise() * 0.5 * e + square(t, 80 - 30 * (i/n)) * 0.3 * max(0, 1.0 - i/n)
        samples.append(s * 24000)
    save_wav("assets/audio/sfx_hit.wav", samples)

# 6. sfx_alert.wav — two-tone warning siren beep
def gen_alert():
    n = int(SR * 0.4)
    samples = []
    for i in range(n):
        t = i / SR
        cycle = int(t * 6) % 2
        freq = 880 if cycle == 0 else 660
        e = env_adsr(i, n, 0.01, 0.05, 0.7, 0.1)
        s = square(t, freq) * 0.35
        samples.append(s * e * 18000)
    save_wav("assets/audio/sfx_alert.wav", samples)

# 7. sfx_menu_select.wav — cute UI blip
def gen_menu_select():
    n = int(SR * 0.08)
    samples = []
    for i in range(n):
        t = i / SR
        freq = 800 + 400 * (i / n)
        e = env_adsr(i, n, 0.05, 0.1, 0.5, 0.4)
        s = triangle(t, freq) * 0.5
        samples.append(s * e * 16000)
    save_wav("assets/audio/sfx_menu_select.wav", samples)

# 8. sfx_pause.wav — low toggle beep
def gen_pause():
    n = int(SR * 0.1)
    samples = []
    for i in range(n):
        t = i / SR
        e = env_adsr(i, n, 0.03, 0.15, 0.4, 0.4)
        s = square(t, 440) * 0.3 + triangle(t, 220) * 0.2
        samples.append(s * e * 15000)
    save_wav("assets/audio/sfx_pause.wav", samples)

# 9. sfx_steal.wav — alarming descending wail
def gen_steal():
    n = int(SR * 0.25)
    samples = []
    for i in range(n):
        t = i / SR
        freq = 1200 - 800 * (i / n)
        e = env_adsr(i, n, 0.02, 0.1, 0.5, 0.3)
        s = square(t, freq) * 0.35 + noise() * 0.1 * max(0, 1 - i/n)
        samples.append(s * e * 20000)
    save_wav("assets/audio/sfx_steal.wav", samples)

# 10. sfx_recapture.wav — triumphant burst
def gen_recapture():
    freqs = [392.00, 523.25, 659.25, 783.99]
    note_len = int(SR * 0.07)
    samples = []
    for freq in freqs:
        for i in range(note_len):
            t = i / SR
            e = env_adsr(i, note_len, 0.03, 0.1, 0.6, 0.2)
            s = square(t, freq) * 0.3 + triangle(t, freq) * 0.25
            samples.append(s * e * 20000)
    save_wav("assets/audio/sfx_recapture.wav", samples)

gen_pickup()
gen_drop()
gen_step()
gen_extraction()
gen_hit()
gen_alert()
gen_menu_select()
gen_pause()
gen_steal()
gen_recapture()

print(f"All 10 chiptune SFX generated in assets/audio/")
