"""Calculate reading estimates from local chapter counts. No network access."""
import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
import math
from pathlib import Path

def rate(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("rate must be a positive finite number")
    return number

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--book", help="English book name or slug, e.g. John or 1-john")
    p.add_argument("--chapter", type=int, help="omit to sum the selected book")
    p.add_argument("--edition", choices=["kjv", "cuv"], default="kjv")
    p.add_argument("--wpm", type=rate, default=238, help="KJV words/minute")
    p.add_argument("--cpm", type=rate, default=390, help="CUV characters/minute")
    p.add_argument("--check", action="store_true", help="validate distributed counts and arithmetic")
    args = p.parse_args()
    with (Path(__file__).resolve().parent / "chapter-counts.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if args.check:
        keys = {(r["book_slug"], int(r["chapter"])) for r in rows}
        assert len(rows) == len(keys) == 1189
        assert len({r["book_slug"] for r in rows}) == 66
        assert sum(int(r["kjv_words"]) for r in rows) == 789634
        assert sum(int(r["cuv_chars"]) for r in rows) == 930059
        for r in rows:
            assert int(r["chapter"]) > 0 and int(r["kjv_words"]) > 0 and int(r["cuv_chars"]) > 0
            for count, speed, estimate in [("kjv_words",238,"kjv_minutes_at_238wpm"),("cuv_chars",390,"cuv_minutes_at_390cpm")]:
                expected = (Decimal(r[count]) / speed).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                assert Decimal(r[estimate]) == expected, (r["book"], r["chapter"], estimate)
        print("Checked 1,189 unique chapters, 66 books, both totals and all fixed-rate estimates.")
        return
    if not args.book:
        p.error("--book is required unless using --check")
    selected = [r for r in rows if args.book.casefold() in {r["book"].casefold(),r["book_slug"].casefold()}]
    if args.chapter is not None:
        selected = [r for r in selected if int(r["chapter"]) == args.chapter]
    if not selected:
        p.error("book or chapter not found in this 66-book corpus")
    key,unit,speed = ("kjv_words","words",args.wpm) if args.edition=="kjv" else ("cuv_chars","characters",args.cpm)
    count=sum(int(r[key]) for r in selected)
    label=selected[0]["book"] + (" "+str(args.chapter) if args.chapter is not None else " (whole book)")
    minutes = count/speed
    if not math.isfinite(minutes):
        p.error("rate is too small to produce a finite reading-time estimate")
    print(f"{label}: {count} {args.edition.upper()} {unit}; {minutes:.1f} estimated minutes at {speed:g} {unit}/minute.")

if __name__=="__main__":
    main()
