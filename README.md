# humanizer-fr

Catalogue des marqueurs d'écriture IA **en français** + script d'audit mesurable + skill Claude pour la correction et la prévention à la génération.

Les ressources existantes sur les "signes d'écriture IA" sont presque toutes centrées sur l'anglais. Ce dépôt les adapte au français, y ajoute les patterns propres au contenu SEO, et fournit un outil de mesure chiffrée plutôt qu'un jugement à l'œil.

## Contenu

| Fichier | Rôle |
|---|---|
| [PATTERNS.md](PATTERNS.md) | Le catalogue complet : ~50 marqueurs organisés par couche (lexique, structure, rythme, typographie, fond, SEO), chacun avec exemple français et correction |
| [audit.py](audit.py) | Script de mesure : burstiness, uniformité du rythme, vocabulaire IA, typographie (cadratins, apostrophes, guillemets), participiales plaquées. Sortie chiffrée, utilisable sur n'importe quel texte |
| [skill/SKILL.md](skill/SKILL.md) | Skill Claude : édition humanisante en français, avec règles de prévention à la génération (pas seulement de correction après coup) |

## Utilisation rapide

```bash
python3 audit.py mon-texte.md
```

Le script ne rend pas de verdict "IA ou pas" : il chiffre chaque famille de marqueurs pour permettre de comparer deux versions d'un texte ou de suivre une progression.

## Position méthodologique (à lire avant usage)

1. **Aucun détecteur n'est une preuve.** GPTZero fonctionne depuis fin 2023 par classification deep learning phrase par phrase, plus par simple perplexité/burstiness. Les faux positifs sur écriture humaine contrainte (contenu SEO calibré, rédacteurs non natifs) sont documentés jusqu'à 61 % (Liang et al., arXiv:2304.02819). La Bible et la Constitution américaine sont régulièrement flaguées "IA".
2. **Les outils anti-détection sont une impasse.** Les détecteurs commerciaux embarquent des couches dédiées à la détection des paraphraseurs/humanizers automatiques (Quillbot flagué à ~91 % par GPTZero). La substitution de synonymes et les astuces de caractères ne fonctionnent pas durablement.
3. **Le seul levier stable est la qualité éditoriale réelle** : variance du rythme des phrases, spécificité concrète (chiffres précis, termes métier, cas situés), structures asymétriques, suppression du remplissage. Ce dépôt vise à améliorer les textes, pas à tromper des détecteurs : un texte creux dont on gomme les tics reste un texte creux.
4. **Raisonner en grappes, jamais sur un marqueur isolé.** Un "cependant" ou un adjectif soutenu isolé ne prouve rien. Le signal, c'est l'accumulation : cadratins + règle de trois + vocabulaire IA + conclusion générique dans le même texte.

## Sources principales

- [Wikipedia — Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup)
- [GPTZero — How AI detectors work](https://gptzero.me/news/how-ai-detectors-work/) · [Perplexity & burstiness](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)
- [Liang et al. 2023 — GPT detectors are biased against non-native English writers](https://arxiv.org/pdf/2304.02819)
- [Sadasivan et al. — Can AI-Generated Text be Reliably Detected?](https://arxiv.org/abs/2303.11156)
- [RAID benchmark (arXiv:2405.07940)](https://arxiv.org/abs/2405.07940) · [MULTITuDE, benchmark multilingue (arXiv:2310.13606)](https://arxiv.org/abs/2310.13606)
- Sources francophones : [Daria décrypte l'IA](https://dariadecrypteia.substack.com/p/les-tics-de-langage-de-chatgpt), [Projet Voltaire](https://www.projet-voltaire.fr/ressources/detecter-texte-chatgpt-ia-generative/), [kluster.fr](https://kluster.fr/eviter-patterns-ia-redaction), [redacteur.com](https://www.redacteur.com/blog/eviter-tics-de-langage-chatgpt/)

La liste complète des sources est dans [PATTERNS.md](PATTERNS.md).

## Licence

MIT — voir [LICENSE](LICENSE).
