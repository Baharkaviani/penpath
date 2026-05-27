# Penpath

> Plan on paper. Track digitally.

Penpath is a hybrid productivity system that lets you write your weekly tasks by hand on a printable flowboard, then scan the paper to automatically sync everything into a digital planner — complete with progress tracking and statistics.

---

## The Problem

Most planners force you to choose: the focus of pen and paper, or the power of digital tracking. Penpath eliminates that tradeoff.

---

## How It Works

1. **Print** your weekly flowboard — a clean, paper-optimized layout designed for handwriting.
2. **Plan** your week on paper, the way humans think best.
3. **Scan** the completed sheet with the Penpath app.
4. **Track** your progress, completion rates, and productivity trends digitally — no manual re-entry.

---

## Features

- Printable weekly flowboard (PDF)
- Mobile app to scan and digitize handwritten tasks
- OCR-powered task extraction with completion state detection
- Digital planner synced from your paper
- Progress dashboard and weekly statistics

---

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Print      │ → │  Scan       │ → │  Data       │ → │  Analytics  │
│  Layer      │    │  Layer      │    │  Layer      │    │  Layer      │
│  (PDF)      │    │  (OCR/ML)   │    │  (Storage)  │    │  (Dashboard)│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Status

🚧 Early development

---

## License

MIT
