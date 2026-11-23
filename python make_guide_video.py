import cv2
import numpy as np

# Video parametrləri: 45 saniyə, 15 FPS -> 675 kadr, 1280x720 HD
FPS = 15
DURATION_SEC = 45
TOTAL_FRAMES = FPS * DURATION_SEC
WIDTH, HEIGHT = 1280, 720
OUTPUT_FILE = "chemartix_guide.mp4"

# OpenCV BGR rəngləri: Fosfor yaşılı və göy aksent
NEON_GREEN = (20, 255, 57)
NEON_CYAN = (255, 212, 0)
WHITE = (240, 250, 242)
MUTED = (155, 178, 160)
CARD_BG = (15, 24, 18)
BG_DARK = (5, 8, 6)

SCENES = [
    (
        0, 15,
        "00:00 - 00:15  |  SAYT NE ISE YARAYIR?",
        "C.h.e.MartixAZE: NASA Peyk ve Aqrokimya SI",
        [
            "1. Torpagin pH, Azot (N), Rutubet ve NASA NDVI gostericilerini analiz edir.",
            "2. Oten 10 ilin mehsuldarliq dinamikasini ve kecen ille ferqi gosterir.",
            "3. Fermer ucun risk siqnali, gosterisli qrafikler ve qazanc plani qurur."
        ]
    ),
    (
        15, 30,
        "00:15 - 00:30  |  HARA NE DAXIL EDILMELIDIR?",
        "Sol Panel ve Bitki Secimi Qutusu",
        [
            "1. Sol panelden Rayon secin ve ya Manual rejimde pH, Azot, Rutubet yazin.",
            "2. Sol paneldeki goy duymelerle ve ya axtarisla lazimi bolmeye kecin.",
            "3. Ekranin merkezindeki Bitki Seciminden Pomidor, Pambiq, Turp ve s. secin."
        ]
    ),
    (
        30, 45,
        "00:30 - 00:45  |  QAZANC PLANI VE NINO AI",
        "Gelir-Xerc Hesablamasi ve Sag Kunc Komekcisi",
        [
            "1. Hekar sayini daxil edib texmini xerc, gelir, xalis qazanc ve SI % baxin.",
            "2. Qazanci artirmaq ucun addim-addim aqrotexniki tovsiyeleri izleyin.",
            "3. Sag kuncdeki Nino AI suallarina toxunub her addimda cavab alin."
        ]
    ),
]

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

font = cv2.FONT_HERSHEY_DUPLEX

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    frame = np.full((HEIGHT, WIDTH, 3), BG_DARK, dtype=np.uint8)

    # Kiber-aqro incə tor (grid) fonu
    for x in range(0, WIDTH, 64):
        cv2.line(frame, (x, 0), (x, HEIGHT), (12, 22, 16), 1)
    for y in range(0, HEIGHT, 64):
        cv2.line(frame, (0, y), (WIDTH, y), (12, 22, 16), 1)

    # Aktiv səhnəni tap
    active_scene = SCENES[-1]
    for s in SCENES:
        if s[0] <= t < s[1]:
            active_scene = s
            break

    start_t, end_t, badge_txt, title_txt, bullets = active_scene

    # Əsas kart çərçivəsi
    cv2.rectangle(frame, (70, 65), (WIDTH - 70, HEIGHT - 95), CARD_BG, -1)
    cv2.rectangle(frame, (70, 65), (WIDTH - 70, HEIGHT - 95), NEON_GREEN, 2)
    cv2.line(frame, (70, 65), (70, HEIGHT - 95), NEON_CYAN, 6)

    # Üst etiket və başlıq
    cv2.putText(frame, badge_txt, (110, 125), font, 0.78, NEON_CYAN, 2)
    cv2.putText(frame, title_txt, (110, 185), font, 1.05, NEON_GREEN, 2)
    cv2.line(frame, (110, 210), (WIDTH - 110, 210), (45, 90, 55), 1)

    # Mətn bəndləri (animasiyalı görünmə)
    elapsed_in_scene = t - start_t
    y_pos = 285
    for idx, b_text in enumerate(bullets):
        if elapsed_in_scene >= idx * 0.6:
            cv2.putText(frame, b_text, (115, y_pos), font, 0.72, WHITE, 1)
        y_pos += 85

    # Aşağıda 45 saniyəlik zaman xətti (progress bar)
    progress = min(1.0, t / DURATION_SEC)
    bar_x1, bar_x2, bar_y = 70, WIDTH - 70, HEIGHT - 50
    cv2.rectangle(frame, (bar_x1, bar_y - 8), (bar_x2, bar_y + 8), (25, 40, 30), -1)
    fill_x = int(bar_x1 + (bar_x2 - bar_x1) * progress)
    cv2.rectangle(frame, (bar_x1, bar_y - 8), (fill_x, bar_y + 8), NEON_GREEN, -1)

    time_label = f"{int(t):02d}s / {DURATION_SEC}s"
    cv2.putText(frame, time_label, (WIDTH - 210, HEIGHT - 20), font, 0.65, NEON_GREEN, 1)
    cv2.putText(frame, "C.h.e.MartixAZE  |  Cicək Məmmədzadə", (70, HEIGHT - 20), font, 0.65, MUTED, 1)

    writer.write(frame)

writer.release()
print(f"Hazirdir: {OUTPUT_FILE} ({DURATION_SEC} saniye)")
