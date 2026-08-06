#!/usr/bin/env python3
"""Audit des marqueurs d'écriture IA pour texte FRANÇAIS (voir PATTERNS.md).

Usage : python3 audit.py texte.md [texte2.md ...]

Ne rend PAS de verdict "IA ou humain" : chiffre chaque famille de marqueurs pour comparer
deux versions d'un texte ou suivre une progression. Raisonner en grappes, jamais sur un
marqueur isolé (les faux positifs des détecteurs sur écriture humaine contrainte sont
documentés jusqu'à 61 % — Liang et al., arXiv:2304.02819).
"""
import re
import statistics
import sys

# L1/L3 — lexique IA français (grappes d'adjectifs hyperboliques + formules creuses)
AI_VOCAB = [
    "crucial", "cruciale", "cruciaux", "essentiel", "essentielle", "essentiels",
    "incontournable", "primordial", "primordiale", "fondamental", "fondamentale",
    "indispensable", "optimal", "optimale", "véritable", "précieux", "précieuse",
    "significatif", "significative", "captivant", "fascinant", "révolutionnaire",
    "il convient de", "il est important de", "il est essentiel de", "il est impératif de",
    "dans cette optique", "dans ce cadre", "dans ce contexte", "jouer un rôle clé",
    "force est de constater", "en d'autres termes", "il ne faut pas négliger",
    "n'hésitez pas", "n'attendez plus", "que vous soyez",
    "tranquillité d'esprit", "en toute sérénité",
]

# L2 — ouvertures bateau
OPENERS = re.compile(
    r"(?:dans un monde où|à l'ère (?:du|de la|des)|de nos jours|dans le paysage actuel"
    r"|face aux enjeux|dans le monde (?:actuel|trépidant))", re.I)

# L4 — connecteurs formulaïques en TÊTE de paragraphe (là où ils pèsent)
CONNECTORS_AT_START = re.compile(
    r"(?m)^(?:En effet|Par ailleurs|En outre|De plus|Ainsi|De ce fait|Par conséquent"
    r"|En somme|En résumé|En conclusion|En définitive)\b")

# S3 — participes présents plaqués en fin de proposition
PARTICIPIAL = re.compile(
    r",\s+(?:garantissant|assurant|permettant|offrant|soulignant|renforçant|facilitant"
    r"|favorisant|apportant|illustrant|témoignant|contribuant)\b")

# S2 — parallélismes négatifs
NEG_PARALLEL = re.compile(
    r"(?:ne s'agit pas (?:seulement|uniquement)|pas seulement[^.]{0,60},\s*(?:mais|c'est)"
    r"|non seulement[^.]{0,60}mais (?:aussi|également))", re.I)

# S4 — évitement du verbe être
COPULA_AVOIDANCE = re.compile(
    r"\b(?:constitue(?:nt)?|représente(?:nt)?|s'impose(?:nt)? comme|se positionne(?:nt)? comme)\b")

SUPERSCRIPTS = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def prose_sentences(text: str) -> list[str]:
    """Phrases de prose (hors titres, tableaux, listes) — le rythme se mesure sur la prose."""
    lines = [l for l in text.split("\n")
             if l.strip() and not re.match(r"^\s*(?:#|\||>|-|\*|\d+[.)])", l)]
    prose = " ".join(lines)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.strip()) > 10]


def audit(label: str, text: str) -> dict:
    sents = prose_sentences(text)
    lens = [len(s.split()) for s in sents]
    mean = statistics.mean(lens) if lens else 0.0
    stdev = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    burstiness = stdev / mean if mean else 0.0

    max_run = run = 0
    for i in range(1, len(lens)):
        run = run + 1 if abs(lens[i] - lens[i - 1]) <= 3 else 0
        max_run = max(max_run, run)

    short_sentences = sum(1 for n in lens if n <= 8)
    low = text.lower()
    vocab_hits = {w: low.count(w) for w in AI_VOCAB if w in low}

    apos_typo = text.count("’")
    apos_droite = text.count("'")
    total_apos = apos_typo + apos_droite
    apos_uniformity = max(apos_typo, apos_droite) / total_apos if total_apos else 0.0

    paragraphs = [p for p in text.split("\n\n") if len(p.split()) > 20 and not p.strip().startswith(("#", "|"))]
    para_lens = [len(p.split()) for p in paragraphs]
    para_burst = (statistics.pstdev(para_lens) / statistics.mean(para_lens)) if len(para_lens) > 1 else 0.0

    report = {
        "phrases": len(sents),
        "longueur moyenne (mots)": round(mean, 1),
        "burstiness phrases (σ/μ — bas = uniforme = signal IA)": round(burstiness, 2),
        "phrases courtes (≤8 mots)": short_sentences,
        "plus longue série de phrases quasi identiques (±3 mots)": max_run + 1 if lens else 0,
        "burstiness paragraphes (σ/μ)": round(para_burst, 2),
        "R3 parenthèses / points-virgules / questions dans la prose": (
            f"{text.count('(')} / {text.count(';')} / "
            f"{sum(1 for s in sents if s.endswith('?'))}"
        ),
        "L1/L3 vocabulaire IA (occurrences)": sum(vocab_hits.values()),
        "L2 ouvertures bateau": len(OPENERS.findall(text)),
        "L4 connecteurs formulaïques en tête de paragraphe": len(CONNECTORS_AT_START.findall(text)),
        "S2 parallélismes négatifs": len(NEG_PARALLEL.findall(text)),
        "S3 participiales plaquées": len(PARTICIPIAL.findall(text)),
        "S4 évitement du verbe être": len(COPULA_AVOIDANCE.findall(text)),
        "T1 tirets cadratins / demi-cadratins": f"{text.count('—')} / {text.count('–')}",
        "T2 apostrophes typo (’) / droites (') — uniformité": f"{apos_typo} / {apos_droite} — {apos_uniformity:.0%}",
        "T3 guillemets anglais courbes (“”)": text.count("“") + text.count("”"),
        "T4 segments en gras": text.count("**") // 2,
    }

    print(f"=== {label} ===")
    for key, value in report.items():
        print(f"  {key}: {value}")
    if vocab_hits:
        top = sorted(vocab_hits.items(), key=lambda kv: -kv[1])[:8]
        print(f"  détail vocabulaire: {top}")
    print()
    return report


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as handle:
            audit(path, handle.read())


if __name__ == "__main__":
    main()
