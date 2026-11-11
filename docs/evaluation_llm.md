\# Évaluation des explications du LLM local



Modèle : Qwen 3.5 9B via LM Studio, 7 alertes de catégories variées.

Notation : OK / Moyen / Faux pour chaque critère.



| # | Catégorie | Fidèle aux données | Précise l'origine de l'étiquette | MITRE cohérent | Action réaliste | Commentaire |

|---|---|---|---|---|---|---|

| 1 | Generic (DNS) | OK | Moyen | Moyen | Moyen | Brute force = correspondance approximative |

| 2 | Exploits (RDP) | OK | Moyen | OK | OK | Bonne recommandation sur l'accès RDP |

| 3 | DoS (RDP) | Faux | Faux | OK | Moyen | Conclut à un déni de service sans preuve |

| 4 | Fuzzers (RDP) | OK | Moyen | OK | OK | |

| 5 | Backdoor (RDP) | Faux | Faux | OK | OK | Écrit « identifiée par le modèle » |

| 6 | Reconnaissance (RDP) | OK | Moyen | OK | OK | Réponse prudente et nuancée |

| 7 | Reconnaissance (UNAS) | Faux | Moyen | OK | Moyen | Lit `INT` comme « interne » au lieu d'« interrompue » |



\## Observation principale

Les alertes 3, 4, 5 et 6 ont des caractéristiques quasi identiques (RDP, connexion

interrompue, 200 octets, aucune réponse), mais reçoivent quatre diagnostics

différents. L'explication suit donc l'étiquette du jeu de données plutôt que les

caractéristiques du flux.



\## Conclusion

\- \*\*Points forts\*\* : français correct, mention systématique du caractère indicatif

&#x20; de la correspondance MITRE, recommandations plausibles.

\- \*\*Défauts\*\* :

&#x20; 1. attribue parfois la catégorie au modèle alors qu'elle provient de l'étiquette ;

&#x20; 2. conclusions non prouvées par les données (déni de service sur un seul flux) ;

&#x20; 3. mauvaise lecture du champ `state` (INT).

\- \*\*Corrections appliquées au prompt\*\* : signification des états de connexion,

&#x20; interdiction d'attribuer la catégorie au modèle, obligation de signaler quand

&#x20; les données ne permettent pas de conclure.

\- \*\*Limite de fond\*\* : le modèle de détection est binaire (normal / attaque).

&#x20; Prédire le type d'attaque nécessite un modèle multi-classes, prévu comme

&#x20; prochaine étape.

