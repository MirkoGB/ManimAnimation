# ManimAnimation

Animazioni matematiche con [Manim Community](https://www.manim.community/).

## Requisiti (già installati su questo PC)

- Python 3.14 con ambiente virtuale in `.venv`
- Manim 0.22.1 (vedi `requirements.txt`)
- MiKTeX per le formule LaTeX (`MathTex`, `Tex`), con installazione automatica dei pacchetti mancanti

## Installazione su un nuovo PC

```powershell
winget install --id MiKTeX.MiKTeX -e --scope user
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Rendering

```powershell
.\.venv\Scripts\Activate.ps1
manim -pql main.py ApprossimazioneRadice   # anteprima veloce (480p) e apre il video
manim -pqh main.py ApprossimazioneRadice   # alta qualità (1080p)
```

I video vengono salvati in `media/videos/`.
