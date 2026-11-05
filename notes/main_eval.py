"""A/B on trafilatura's eval corpus: extract() vs extract() + <main> fallback (exactly one <main>/[role=main];
if trafilatura kept < RATIO of main's distinct 3+ letter words, return main's cleaned text).
usage: main_eval.py TRAF_REPO [RATIO ...]"""
import re, sys
from pathlib import Path
repo = Path(sys.argv[1]); sys.path.insert(0, str(repo / "tests"))
from eval_common import RUNNERS, ConfusionMatrix, load_evaldata, read_corpus, run_and_count
from lxml import html as lh

DROP = "script style noscript template svg nav aside form button select footer header".split()

import os
SKIP_ARTICLES = os.environ.get("SKIP_ARTICLES") == "1"

def is_article(tree):
    og = tree.xpath("//meta[@property='og:type']/@content")
    return bool(og and og[0].strip().lower() == "article") or (os.environ.get("ART_TAG") == "1" and len(tree.xpath("//article")) == 1)

def main_text(htmlbinary):
    try:
        tree = lh.fromstring(htmlbinary)
    except Exception:
        return None
    if SKIP_ARTICLES and is_article(tree):
        return None
    mains = tree.xpath("//main") or tree.xpath("//*[@role='main']")
    if len(mains) != 1:
        return None
    m = mains[0]
    for el in m.xpath(".//" + " | .//".join(DROP)):
        el.drop_tree()
    lines = [re.sub(r"\s+", " ", t).strip() for t in m.itertext()]
    return "\n".join(l for l in lines if l)

words = lambda t: set(re.findall(r"\w{3,}", (t or "").lower()))

def make(base, ratio):
    def fn(b):
        out = base(b)
        mt = main_text(b)
        if mt and len(words(out)) < ratio * len(words(mt)) and len(mt.split()) > len((out or "").split()):
            fn.used += 1
            return mt
        return out
    fn.used = 0
    return fn

here = str(repo / "tests")
data = load_evaldata(here); docs = read_corpus(here, data)
ratios = [float(r) for r in sys.argv[2:]] or [0.6]
for mode in ("fast", "fallback"):
    base = RUNNERS[mode]
    cms = {"base": ConfusionMatrix(), **{r: ConfusionMatrix() for r in ratios}}
    fns = {r: make(base, r) for r in ratios}
    for url, (_, b) in docs.items():
        out, counts, _ = run_and_count(base, b, data[url]); cms["base"].add(counts)
        mt = main_text(b)
        for r in ratios:
            # reuse base output instead of re-extracting
            if mt and len(words(out)) < r * len(words(mt)) and len(mt.split()) > len((out or "").split()):
                fns[r].used += 1; res = mt
            else:
                res = out
            from eval_common import count_item
            cms[r].add(count_item(data[url], res))
    print(mode, "base", [round(x, 4) for x in cms["base"].scores()])
    for r in ratios:
        print(mode, f"ratio {r}", [round(x, 4) for x in cms[r].scores()], "fallback used on", fns[r].used, "of", len(docs))
