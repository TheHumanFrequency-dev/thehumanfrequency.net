#!/usr/bin/env python3
"""
build-pages.py — Author 5 Self-Care wiki pages and generate them.

Reads source content from the 5 page dicts below, writes JSON files,
runs generate-wiki-page.py on each, drops HTML in human-os/.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path("/sessions/friendly-beautiful-ritchie/mnt/thehumanfrequency.net")
GENERATOR = ROOT / "scripts" / "generate-wiki-page.py"
CONTENT_DIR = ROOT / "scripts" / "wiki-content"
OUTPUT_DIR = ROOT / "human-os"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# Common bits reused across all Self-Care pages
SC_GUMROAD = "https://thehumanfrequency.gumroad.com/l/lwawbf"
SC_FAWN = "/human-os/fawn-response"
SC_CYCLIC = "/human-os/cyclic-sighing"
SHOW_LINK = "/thf-podcast"

EXIT_SHOW = {
    "tag": "Show · Coming soon",
    "tag_class": "community",
    "url": SHOW_LINK,
    "title": "The Live Show",
    "body": "A live call-in show on the topics this wiki covers — unscripted, judgment-free, ordinary people, extraordinary stories. Join the waitlist for the launch.",
    "cta": "Get on the list →",
}

PAGES = [
    # ─── Page 03 ─────────────────────────────────────────────────────────
    {
        "slug": "diving-reflex",
        "page_num": "03",
        "title": "Diving Reflex Protocol",
        "title_pre_words": "DIVING",
        "title_grad_word": "REFLEX",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "Cold water on the face for 15-30 seconds. Heart rate drops 10 to 25 percent. The most powerful autonomic reflex known — and the closest thing to a kill-switch your nervous system has.",
        "reading_time": "7 min read",
        "last_updated": "May 2026",
        "source_chapter": "Self-Care, Ch. 3",
        "date_published": "2026-05-01",
        "meta_description": "Cold water on the face for 15-30 seconds activates the mammalian diving reflex. Heart rate drops 10-25%. Mechanism, protocol, and a wallet card. Sourced from Ackermann et al. 2023 meta-analysis.",
        "og_description": "The fastest down-regulation tool the body has. 15 to 30 seconds. Free. Sourced from Ackermann et al. 2023.",
        "twitter_description": "The fastest down-regulation tool the body has. 15 to 30 seconds.",
        "schema_keywords": "diving reflex, cold water therapy, vagus nerve, parasympathetic, anxiety, panic, Ackermann 2023",
        "pull_quote": {
            "text": "The mammalian diving reflex is the most powerful autonomic reflex known. Cold water on the face produces bradycardia of 10 to 25 percent within seconds.",
            "cite": "— Panneton (2013) · Ackermann et al. (2023), Psychophysiology",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're already past the point where breathing helps. Heart racing, chest tight, the prefrontal cortex offline. A panic attack, a fight that just escalated, a sudden surge of grief. You need the brake right now, not in five minutes."},
            {"type": "p", "text": "This is what the diving reflex is for. Cold water on the face. 15 to 30 seconds. The body has a built-in autonomic kill-switch and almost nobody knows about it."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "The mammalian diving reflex evolved to keep us alive when we accidentally hit cold water — slow the heart, conserve oxygen, redirect blood to the brain. Panneton (2013) called it the most powerful autonomic reflex known. It fires in seconds and you don't have to believe in it for it to work."},
            {"type": "p_bold_lead", "lead": "Trigeminal trigger.", "rest": "When cold water contacts the face, the trigeminal nerve sends afferent signals to the brainstem, which fires the vagus nerve. That produces bradycardia (heart rate slows 10 to 25 percent), peripheral vasoconstriction, and blood redistribution to the heart and brain."},
            {"type": "p_bold_lead", "lead": "Temperature matters.", "rest": "Ackermann et al. (2023, <em>Psychophysiology</em>) published the first meta-analysis of the diving response. The effect was moderate to large for cardiac vagal activity. Cold water at roughly 10°C produced significantly stronger effects than warm. Lukewarm water doesn't work."},
            {"type": "p_bold_lead", "lead": "Speed matters too.", "rest": "Unlike most regulation tools, this one isn't a practice. It's a reset. Cyclic sighing and resonance breathing build the parasympathetic system over weeks. The diving reflex hits the brake on the next breath."},
            {"type": "stat_box", "label": "THE META-ANALYSIS RESULT", "figure": "Heart rate ↓ 10-25% · 15-30 seconds · 10°C optimal", "cite": "Ackermann et al. (2023, Psychophysiology) — first meta-analysis of the diving response. Moderate to large effect on cardiac vagal activity. Temperature is the lever; warmer water blunts the effect significantly."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Under one minute. Works in any kitchen, bathroom, or office bathroom with a sink and a bowl."},
        ],
        "steps": [
            {
                "name": "Get cold water — 10 to 15°C",
                "body": "Fill a bowl with cold tap water. If it feels cold-shocking on the wrist, it's in range. Add a few ice cubes if your tap water is warm. Do not use ice-only water — too cold and the shock can spike heart rate before the reflex fires.",
                "tip": "10 to 15°C is roughly 50 to 60°F. Tap water in most homes is in this range; warm climates may need ice.",
            },
            {
                "name": "Take one full breath in",
                "body": "Inhale through the nose, comfortably full. Don't force a max breath — the goal is a baseline of oxygen for the breath-hold, not a stress response.",
                "tip": "If you have a panic disorder or cardiovascular condition, skip the breath-hold and just splash cold water on the face. The trigeminal trigger still fires.",
            },
            {
                "name": "Submerge the face for 15 to 30 seconds",
                "body": "Lower your face into the bowl so cold water contacts the forehead, eyes, and cheekbones. The trigeminal nerve receptors are concentrated in this triangle — that's the activation surface.",
                "tip": "If submerging isn't possible (contact lenses, makeup, just a fast version), hold a cold wet cloth across the same triangle for 30 to 60 seconds. Slower onset, same mechanism.",
            },
            {
                "name": "Come up — slow",
                "body": "Lift your face slowly. Breathe normally — do not gasp. The parasympathetic shift is already happening; rapid inhalation pulls you back toward sympathetic activation.",
                "tip": "You may notice a wave of calm in the next 10 seconds. That's the bradycardia plus the vagal response settling.",
            },
            {
                "name": "Sit for 60 seconds — let it land",
                "body": "Stay still. Breathe normally. The reset is brief — typically 1 to 3 minutes of meaningful down-regulation. Use that window to do whatever you couldn't do five minutes ago: have the conversation, send the email, write the page.",
                "tip": "Repeat once if needed. Don't repeat more than twice in an hour — the reflex blunts with overuse.",
            },
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Tape it to the inside of a kitchen cabinet or a bathroom mirror — the surfaces nearest the cold water sources you'll use it at.",
        "printable_card": {
            "title": "DIVING REFLEX · 30 SECONDS",
            "subtitle": "Ackermann et al. 2023 meta-analysis",
            "items": [
                {"num": "01 · COLD WATER", "text": "Bowl of cold tap water. 10 to 15°C.", "help": "Cold-shocking on the wrist. Add ice if your tap is warm."},
                {"num": "02 · ONE BREATH IN", "text": "Comfortably full. Through the nose.", "help": "Not a max breath — a baseline."},
                {"num": "03 · SUBMERGE 15-30 SECONDS", "text": "Forehead, eyes, cheekbones touching the water.", "help": "The trigeminal triangle. Where the receptors are."},
                {"num": "04 · COME UP SLOW", "text": "Don't gasp. Breathe normally.", "help": "The shift is already happening. Don't overshoot."},
                {"num": "05 · SIT 60 SECONDS", "text": "Stay still. Use the window — calm lasts 1 to 3 minutes.", "help": "Repeat once if needed. Not more than twice per hour."},
            ],
        },
        "exits": [
            {
                "tag": "Full chapter · $27",
                "tag_class": "",
                "url": SC_GUMROAD,
                "title": "The Self-Care You Were Never Taught",
                "body": "Chapter 3 covers the diving reflex in full clinical context, plus the four other vagal-tone interventions: cyclic sighing, extended-exhale breathing, resonance frequency, and humming. With the state-matching framework that decides which one fits the moment.",
                "cta": "Read the book →",
            },
            {
                "tag": "Wiki · Free",
                "tag_class": "free",
                "url": SC_CYCLIC,
                "title": "Cyclic Sighing OS",
                "body": "If the diving reflex is the reset button, cyclic sighing is the daily practice that raises your baseline. Five minutes a day for 28 days, biggest single-modality result in any 2023 anxiety trial.",
                "cta": "Read the page →",
            },
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-diving-reflex-newsletter",
        "subscribe_source": "source-wiki-diving-reflex",
        "sources_intro": "All claims on this page are cited in <em>The Self-Care You Were Never Taught</em>, Chapter 3. Primary sources:",
        "sources_list": [
            "Ackermann, S. et al. (2023). The diving response: A meta-analysis. <em>Psychophysiology.</em> First meta-analysis of the diving reflex; moderate-to-large effect on cardiac vagal activity; temperature dependent.",
            "Panneton, W. M. (2013). The mammalian diving response: An enigmatic reflex to preserve life? <em>Physiology.</em> Foundational review describing the reflex as the most powerful autonomic reflex known.",
        ],
        "sources_outro": "",
    },

    # ─── Page 04 ─────────────────────────────────────────────────────────
    {
        "slug": "diaphragmatic-breathing",
        "page_num": "04",
        "title": "Diaphragmatic Breathing OS",
        "title_pre_words": "DIAPHRAGMATIC",
        "title_grad_word": "BREATHING",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "Eight breaths a minute. Inhale four, exhale six to eight. The protocol that flips the autonomic switch from sympathetic to parasympathetic — backed by a systematic review of every breathing technique that's been studied.",
        "reading_time": "8 min read",
        "last_updated": "May 2026",
        "source_chapter": "Self-Care, Ch. 3",
        "date_published": "2026-05-01",
        "meta_description": "Diaphragmatic breathing at ~8 breaths per minute makes parasympathetic activity dominant. The mechanism, the 5-step protocol, and a wallet card. Sourced from Hopper et al. 2019 systematic review.",
        "og_description": "Eight breaths a minute. Inhale four, exhale six to eight. The protocol that flips the autonomic switch.",
        "twitter_description": "Eight breaths a minute is the trigger. Sourced from Hopper et al. 2019.",
        "schema_keywords": "diaphragmatic breathing, parasympathetic, vagal tone, extended exhale, Hopper 2019, anxiety reduction",
        "pull_quote": {
            "text": "Slow diaphragmatic breathing at approximately eight breaths per minute makes parasympathetic activity dominant. The longer the exhale relative to the inhale, the more vagal tone.",
            "cite": "— Hopper et al. (2019), JBI Database of Systematic Reviews",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "Most people breathe 12 to 20 times a minute. Most of those breaths are shallow — chest only, the diaphragm barely moving. That's a perfectly fine breathing pattern for sitting at a desk. It's also a breathing pattern that keeps your sympathetic nervous system mildly engaged most of the day."},
            {"type": "p", "text": "Diaphragmatic breathing is the lever for everything else. Slower than your default. Lower in the body. Longer on the exhale than the inhale. Practice it for five minutes and the body shifts from \"mildly braced\" to \"actively recovering.\" Practice it daily and the baseline moves."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things are happening when you breathe diaphragmatically with a long exhale."},
            {"type": "p_bold_lead", "lead": "Vagal activation.", "rest": "The vagus nerve runs from the brainstem to the gut, and it's the main parasympathetic highway. Long exhales mechanically stimulate it. The longer the exhale relative to the inhale, the more vagal tone you generate. This is why every evidence-based breathing protocol — cyclic sighing, resonance, 4-7-8 — is built around the same physics."},
            {"type": "p_bold_lead", "lead": "Slowing the breath.", "rest": "Slow diaphragmatic breathing at roughly eight breaths per minute makes parasympathetic activity dominant. Hopper et al. (2019, <em>JBI Database</em>) reviewed the evidence systematically and found this rate is the inflection point — slower is better, faster doesn't reliably shift autonomic balance."},
            {"type": "p_bold_lead", "lead": "Diaphragm vs. chest.", "rest": "Chest breathing — what most people default to under stress — keeps the breath shallow and the rhythm fast. Diaphragmatic breathing engages the larger muscle, draws air deeper, and naturally slows the rate. The hand-on-belly check is the simplest way to know which one you're doing."},
            {"type": "stat_box", "label": "THE SYSTEMATIC REVIEW FINDING", "figure": "~8 breaths/min · inhale 4 · exhale 6-8", "cite": "Hopper et al. (2019, JBI Database of Systematic Reviews) — diaphragmatic breathing decreases physiological and psychological stress; the ratio of inhale to exhale matters more than the specific count, and ~8 breaths per minute is the parasympathetic-dominant inflection point."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Five to ten minutes. Sit, lie down, walk slowly — the rate matters more than the position."},
        ],
        "steps": [
            {
                "name": "Find the diaphragm",
                "body": "One hand on chest, one on belly. The hand on your belly should rise more than the hand on your chest. If the chest is the only thing moving, you're shallow-breathing. Send the breath lower — let the belly expand outward like a balloon.",
                "tip": "Lying down makes this easier the first few times — gravity helps you feel the diaphragm dropping.",
            },
            {
                "name": "Inhale four counts — through the nose",
                "body": "Slow inhale through the nose. Count to four. The expansion is in the belly and lower ribs, not the chest. Don't strain — \"four counts\" is a rhythm, not a target.",
                "tip": "Nasal breathing matters here. Mouth-breathing tends to pull the breath back into the chest and accelerate the rate.",
            },
            {
                "name": "Exhale six to eight counts — through the mouth",
                "body": "Long, slow exhale through the mouth. Aim for six to eight counts — at least 1.5x the inhale. This is the vagal lever. The longer the exhale, the more parasympathetic shift.",
                "tip": "Slight pursing of the lips creates resistance and naturally lengthens the exhale. It also slows the rate without you having to think about it.",
            },
            {
                "name": "Hold the rhythm for five minutes",
                "body": "Continue the cycle. Don't count breaths — count the rhythm. Eight breaths a minute is roughly one breath every 7.5 seconds. After two or three minutes, the body usually settles into the rhythm without active counting.",
                "tip": "If you lose the rhythm or the mind wanders, just resume on the next inhale. There's no penalty. The body keeps responding to the pattern even when attention drifts.",
            },
            {
                "name": "Notice — then carry it",
                "body": "After five minutes, breathe normally for one minute. Then take the rhythm with you. Diaphragmatic breathing is not just a session — it's a default state you can return to between meetings, before sleep, in traffic, in a difficult conversation. The five-minute practice trains the rhythm; the rest of the day applies it.",
                "tip": "Pair it with an existing trigger — \"every time I sit at my desk\" or \"every time I close a browser tab\" — to build the default without adding effort.",
            },
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "The whole protocol fits on a card. Print it. Set it as your phone lock screen. Use it in the meetings where you need it.",
        "printable_card": {
            "title": "DIAPHRAGMATIC BREATHING · 5 MINUTES",
            "subtitle": "Hopper et al. 2019 — JBI systematic review",
            "items": [
                {"num": "01 · FIND THE DIAPHRAGM", "text": "One hand on chest, one on belly. Belly should rise more.", "help": "Chest only = shallow. Send the breath lower."},
                {"num": "02 · INHALE 4 — NOSE", "text": "Slow, through the nose. Belly expands.", "help": "Rhythm, not target. Don't strain."},
                {"num": "03 · EXHALE 6-8 — MOUTH", "text": "Long, slow exhale. Pursed lips help.", "help": "At least 1.5x the inhale. The vagal lever."},
                {"num": "04 · HOLD THE RHYTHM 5 MIN", "text": "~8 breaths per minute. Don't count.", "help": "Roughly one breath every 7.5 seconds."},
                {"num": "05 · CARRY IT", "text": "Return to the rhythm during the day. Pair with a trigger.", "help": "The session trains it. The day applies it."},
            ],
        },
        "exits": [
            {
                "tag": "Full chapter · $27",
                "tag_class": "",
                "url": SC_GUMROAD,
                "title": "The Self-Care You Were Never Taught",
                "body": "Chapter 3 covers diaphragmatic breathing in clinical context, plus four other evidence-based protocols (cyclic sighing, resonance, 4-7-8, box) and the state-matching framework that decides which to use when. 162 pages, 94+ peer-reviewed studies cited.",
                "cta": "Read the book →",
            },
            {
                "tag": "Wiki · Free",
                "tag_class": "free",
                "url": SC_CYCLIC,
                "title": "Cyclic Sighing OS",
                "body": "Diaphragmatic breathing is the daily baseline. Cyclic sighing is the variant with the strongest acute-state evidence — five minutes a day for 28 days, the Stanford 2023 result.",
                "cta": "Read the page →",
            },
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-diaphragmatic-newsletter",
        "subscribe_source": "source-wiki-diaphragmatic",
        "sources_intro": "All claims on this page are cited in <em>The Self-Care You Were Never Taught</em>, Chapter 3. Primary sources:",
        "sources_list": [
            "Hopper, S. I. et al. (2019). Effectiveness of diaphragmatic breathing for reducing physiological and psychological stress in adults: a quantitative systematic review. <em>JBI Database of Systematic Reviews and Implementation Reports.</em>",
            "Balban, M. Y. et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. <em>Cell Reports Medicine.</em> Stanford RCT establishing the value of long-exhale breathing protocols generally.",
        ],
        "sources_outro": "",
    },

    # ─── Page 05 ─────────────────────────────────────────────────────────
    {
        "slug": "humming-protocol",
        "page_num": "05",
        "title": "Humming and OM Protocol",
        "title_pre_words": "HUMMING",
        "title_grad_word": "PROTOCOL",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "Five minutes of humming. The lowest stress index of any condition tested in a Holter monitoring study — including sleep. Free, silent enough to do at your desk, and one of the most underused regulation tools in the catalogue.",
        "reading_time": "7 min read",
        "last_updated": "May 2026",
        "source_chapter": "Self-Care, Ch. 3",
        "date_published": "2026-05-01",
        "meta_description": "Five minutes of humming or OM chanting produces the lowest stress index of any condition tested — including sleep. Mechanism, protocol, wallet card. Sourced from Inbaraj et al. 2022.",
        "og_description": "Five minutes of humming. Lower stress index than sleep. The most underused regulation tool in the catalogue.",
        "twitter_description": "Five minutes of humming. Lower stress index than sleep, in a Holter study.",
        "schema_keywords": "humming, OM chanting, Bhramari Pranayama, vagus nerve, HRV, Inbaraj 2022, parasympathetic",
        "pull_quote": {
            "text": "A Holter monitoring study found humming produced the lowest stress index of all conditions tested, including sleep (p < 0.05), with the highest total HRV power and SDNN.",
            "cite": "— Inbaraj et al. (2022), International Journal of Yoga",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're at a desk. You can't take a cold-water break. You can't lie on the floor and do five minutes of structured breathing. You can quietly hum, with your mouth closed, while reading email."},
            {"type": "p", "text": "Humming is the least-glamorous regulation tool in the chapter and one of the most effective. The exhale is long because singing is a long exhale. The vibration mechanically stimulates the vagus nerve. Five minutes shifts the autonomic state more reliably than ten minutes of trying to think your way calm."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Humming and chanting work through dual vagal stimulation — two pathways at once."},
            {"type": "p_bold_lead", "lead": "Long exhale, again.", "rest": "Sustained vocalization on the exhale activates vagal pathways through the same respiratory entrainment that powers cyclic sighing and diaphragmatic breathing. You can't hum on the inhale. The technique forces the long exhale into existence."},
            {"type": "p_bold_lead", "lead": "Mechanical vagal stimulation.", "rest": "The vocal fold vibrations directly stimulate the recurrent laryngeal branch of the vagus nerve — a literal mechanical signal sent up the same nerve that the long exhale activates chemically. This is the part you can't get from breathing alone. Five minutes of steady humming has been shown to measurably shift heart rate variability."},
            {"type": "p_bold_lead", "lead": "The OM evidence.", "rest": "Inbaraj et al. (2022, <em>International Journal of Yoga</em>) demonstrated that five minutes of loud OM chanting produces immediate increases in HF-HRV power — a marker of parasympathetic dominance. A separate Holter monitoring study found humming produced the lowest stress index of any condition tested, with the highest total HRV power and SDNN. Including sleep. p < 0.05."},
            {"type": "stat_box", "label": "THE HOLTER STUDY RESULT", "figure": "Lowest stress index of any condition · including sleep", "cite": "Holter monitoring study cited in Self-Care Ch. 3: humming produced the lowest stress index of all conditions tested, with the highest total HRV power and SDNN (p < 0.05). Inbaraj et al. (2022): five minutes of OM chanting → immediate HF-HRV increase."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Five to ten minutes. Best done somewhere you don't mind making sound — but a closed-mouth hum is quiet enough for an open-plan office."},
        ],
        "steps": [
            {
                "name": "Settle and seal",
                "body": "Sit comfortably. Mouth closed, lips lightly touching, teeth slightly apart. Optional: place your index fingers in your ears — this amplifies the vibration and turns the practice into Bhramari Pranayama, the traditional version.",
                "tip": "If you're at a desk and can't seal off the world, just close the mouth and lean into the vibration. The mechanical stimulation works either way.",
            },
            {
                "name": "Inhale through the nose — full but unstrained",
                "body": "Slow inhale through the nose. Aim for a full breath — you need the air to sustain the hum. Don't max it out; you need to be able to hum for the full exhale.",
                "tip": "If you find yourself running out of air halfway through the hum, you took too big of an inhale or held too high a pitch. Adjust on the next breath.",
            },
            {
                "name": "Hum the exhale — low, steady, like a bee",
                "body": "On the exhale, make a low, steady humming sound — close to your natural speaking pitch, slightly lower if comfortable. Hold it for the full duration of the exhale. Feel the vibration in the throat, chest, and sinuses.",
                "tip": "The Bhramari version uses the syllable \"mmm.\" Some people prefer \"hmm\" or even an OM. The specific syllable matters less than the sustained vibration on a long exhale.",
            },
            {
                "name": "Repeat for five to ten minutes",
                "body": "Continue inhale-hum-inhale-hum. Don't count. Don't try to make it sound \"right.\" The point is the mechanical stimulation, not the music. After two or three minutes, most people notice a settling — that's the parasympathetic shift landing.",
                "tip": "Five minutes is the floor. The Holter study used continuous humming sessions; longer durations correlated with stronger HRV effects.",
            },
            {
                "name": "Settle in silence — one minute",
                "body": "When the timer ends, breathe normally with the mouth closed for one minute. Don't talk yet. The post-protocol silence is where the autonomic shift consolidates and the system anchors the new baseline.",
                "tip": "If you feel slightly buzzed or pleasantly altered — that's normal. The combined HRV shift and the rich oxygenation produce a mild flow state. Don't drive immediately after a 10-minute session.",
            },
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "The whole protocol fits on a card. Print it. Tape it inside the cabinet next to your desk. Use it before the meetings.",
        "printable_card": {
            "title": "HUMMING · 5-10 MINUTES",
            "subtitle": "Inbaraj et al. 2022 · Bhramari Pranayama",
            "items": [
                {"num": "01 · SETTLE AND SEAL", "text": "Mouth closed, lips touching, teeth apart. Fingers in ears (optional).", "help": "Bhramari version. Or just close the mouth."},
                {"num": "02 · INHALE — NOSE, FULL", "text": "Slow nasal inhale. Full but unstrained.", "help": "Enough air to hum the full exhale."},
                {"num": "03 · HUM THE EXHALE — LOW", "text": "Steady hum, like a bee. Low, comfortable pitch.", "help": "Vibration in throat, chest, sinuses."},
                {"num": "04 · REPEAT 5-10 MIN", "text": "Don't count. Don't try to sound right.", "help": "Mechanical stimulation, not music."},
                {"num": "05 · SETTLE IN SILENCE 1 MIN", "text": "Mouth closed. No talking. Breathe normal.", "help": "The shift consolidates here."},
            ],
        },
        "exits": [
            {
                "tag": "Full chapter · $27",
                "tag_class": "",
                "url": SC_GUMROAD,
                "title": "The Self-Care You Were Never Taught",
                "body": "Chapter 3 covers humming and Bhramari Pranayama, plus four other vagal-tone protocols and the state-matching framework. Chapter 5 covers vagal tone as a measurable trait and the practices that build it over weeks and months.",
                "cta": "Read the book →",
            },
            {
                "tag": "Wiki · Free",
                "tag_class": "free",
                "url": SC_CYCLIC,
                "title": "Cyclic Sighing OS",
                "body": "Humming and cyclic sighing share the same engine: long exhale plus vagal stimulation. If you can't hum where you are, cyclic sighing is silent and equally well-evidenced.",
                "cta": "Read the page →",
            },
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-humming-newsletter",
        "subscribe_source": "source-wiki-humming",
        "sources_intro": "All claims on this page are cited in <em>The Self-Care You Were Never Taught</em>, Chapter 3. Primary sources:",
        "sources_list": [
            "Inbaraj, G. et al. (2022). Immediate effects of OM chanting on heart rate variability measures. <em>International Journal of Yoga.</em>",
            "Holter monitoring study (cited in Self-Care Ch. 3) — humming produced the lowest stress index of all conditions tested, including sleep (p < 0.05); highest total HRV power and SDNN.",
        ],
        "sources_outro": "",
    },

    # ─── Page 06 ─────────────────────────────────────────────────────────
    {
        "slug": "five-non-negotiables",
        "page_num": "06",
        "title": "The Five Non-Negotiables",
        "title_pre_words": "FIVE",
        "title_grad_word": "NON-NEGOTIABLES",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "The five practices Self-Care argues you cannot skip — five minutes of cyclic sighing, consistent sleep timing, one HALT check, one implementation intention, one honest conversation a week. Each backed by evidence. None requires more than five minutes.",
        "reading_time": "6 min read",
        "last_updated": "May 2026",
        "source_chapter": "Self-Care, Ch. 8",
        "date_published": "2026-05-01",
        "meta_description": "The five practices Self-Care argues you cannot skip. Each evidence-based. None more than five minutes. The minimum-viable nervous-system maintenance schedule.",
        "og_description": "Five practices. None more than five minutes. The non-negotiable floor for nervous-system maintenance.",
        "twitter_description": "Five practices. None more than five minutes. The non-negotiable floor.",
        "schema_keywords": "self-care basics, daily habits, cyclic sighing, sleep timing, HALT check, implementation intention, honest conversation",
        "pull_quote": {
            "text": "These are not negotiable. They are the non-negotiable requirements of being human. And meeting them takes less than 30 minutes a day, total.",
            "cite": "— The Self-Care You Were Never Taught, Chapter 8",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "Most self-care advice fails for the same reason most fitness advice fails: it scales the floor instead of holding it. Someone tells you to meditate for an hour, journal in two layers, do morning pages, run, drink eight glasses of water, set boundaries, and feel your feelings. Three days in, you skip one. Then two. Then the whole architecture collapses and you blame your discipline."},
            {"type": "p", "text": "The fix is not more discipline. The fix is a smaller, non-negotiable floor — five practices small enough that on your worst day you can still hit them. Donald Winnicott called this the good-enough principle. Self-Care, Chapter 8, calls it the Five Non-Negotiables."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "These five aren't the most ambitious self-care practices. They are the load-bearing ones. Each closes a specific physiological or psychological loop the body cannot self-regulate without."},
            {"type": "p_bold_lead", "lead": "Nervous system regulation.", "rest": "Cyclic sighing and consistent sleep timing maintain the autonomic rhythm. Without these, every other practice is fighting upstream against a dysregulated baseline."},
            {"type": "p_bold_lead", "lead": "Bodily-needs accuracy.", "rest": "The HALT check (Hungry? Angry? Lonely? Tired?) prevents the most common error in emotional life: interpreting a physiological state as an emotional one. \"I'm depressed\" is sometimes \"I haven't eaten in six hours.\" Thirty seconds of asking solves a surprising amount."},
            {"type": "p_bold_lead", "lead": "Behavioral lock-in.", "rest": "An implementation intention — \"if X happens, then I will do Y\" — has a Cohen's d effect size of 0.65 in the meta-analysis literature, meaning it roughly doubles follow-through versus a generic intention. Pair it with a honest weekly conversation, and the social and behavioral dimensions of regulation are covered too."},
            {"type": "stat_box", "label": "THE EFFECT SIZE", "figure": "d = 0.65 · implementation intentions vs. plain intent", "cite": "Self-Care Ch. 8 — implementation intentions roughly double follow-through compared to generic intentions. Combined with the four other non-negotiables, the floor for sustainable regulation."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five practices. Total daily cost: under 30 minutes. Each one's optional individually; together they're the floor."},
        ],
        "steps": [
            {
                "name": "Five minutes of cyclic sighing — daily",
                "body": "The single most evidence-backed breathing technique. Outperformed mindfulness meditation in the 2023 Stanford RCT. Five minutes. Every day. Non-negotiable.",
                "tip": "If you can't make five minutes, make two. Skip-day rate matters more than session length.",
            },
            {
                "name": "Consistent sleep timing — within 30 minutes",
                "body": "Same bedtime and wake time, within 30 minutes, including weekends. This single change improves sleep quality more than any other sleep hygiene intervention. Not perfect timing — consistent timing.",
                "tip": "Anchor the wake time first. If wake is consistent, bedtime stabilizes on its own within two weeks.",
            },
            {
                "name": "One HALT check per day",
                "body": "Hungry? Angry? Lonely? Tired? Address the physiological need before interpreting the emotion. Thirty seconds. Most distress that masquerades as a mood disorder is a HALT signal that's been ignored long enough to feel like personality.",
                "tip": "Tag this onto an existing daily moment — at the kitchen sink after lunch, when you close your laptop, etc. Don't create a new ritual; bolt it onto a real one.",
            },
            {
                "name": "One implementation intention",
                "body": "Choose one self-care behavior. Write one if-then plan: \"If [trigger], then I will [behavior].\" Follow it for two weeks before adding another. Effect size d = 0.65 — roughly double the follow-through of generic intentions.",
                "tip": "Trigger has to be something that already happens reliably. \"After my morning coffee\" works. \"When I have time\" doesn't.",
            },
            {
                "name": "One honest conversation per week",
                "body": "With someone you trust. About how you actually are, not how you want to appear. This single practice covers emotional rest, social rest, and co-regulation. Once a week is the floor; more is better.",
                "tip": "Doesn't have to be in person. A 20-minute phone call counts. The criterion is honesty, not duration or format.",
            },
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Stick it on your bathroom mirror. Five practices. Check the boxes daily. The floor.",
        "printable_card": {
            "title": "FIVE NON-NEGOTIABLES · DAILY FLOOR",
            "subtitle": "Self-Care Chapter 8",
            "items": [
                {"num": "01 · CYCLIC SIGHING — 5 MIN", "text": "Inhale, top-off, long exhale. Five minutes a day.", "help": "Outperformed mindfulness in the 2023 Stanford RCT."},
                {"num": "02 · SLEEP TIMING — ±30 MIN", "text": "Same bed and wake time. Including weekends.", "help": "Single biggest sleep-quality lever."},
                {"num": "03 · HALT CHECK — 30 SECONDS", "text": "Hungry? Angry? Lonely? Tired? Address the physical first.", "help": "Most distress is a body signal mislabeled."},
                {"num": "04 · ONE IMPLEMENTATION INTENTION", "text": "If [real trigger], then I will [specific behavior].", "help": "d = 0.65 effect size. Doubles follow-through."},
                {"num": "05 · ONE HONEST CONVERSATION / WEEK", "text": "Trusted person. How you actually are.", "help": "Emotional + social rest + co-regulation in one practice."},
            ],
        },
        "exits": [
            {
                "tag": "Full chapter · $27",
                "tag_class": "",
                "url": SC_GUMROAD,
                "title": "The Self-Care You Were Never Taught",
                "body": "Chapter 8 builds the full self-care plan around the Five Non-Negotiables — the architecture for habit-stacking, the worksheet, the morning and evening anchors. Chapter 7 is on implementation intentions in clinical detail.",
                "cta": "Read the book →",
            },
            {
                "tag": "Wiki · Free",
                "tag_class": "free",
                "url": SC_CYCLIC,
                "title": "Cyclic Sighing OS",
                "body": "The first non-negotiable, in full. Five minutes a day, the protocol, the mechanism, the wallet card.",
                "cta": "Read the page →",
            },
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-non-negotiables-newsletter",
        "subscribe_source": "source-wiki-non-negotiables",
        "sources_intro": "All claims on this page are cited in <em>The Self-Care You Were Never Taught</em>, Chapters 7-8. Primary sources:",
        "sources_list": [
            "Balban, M. Y. et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. <em>Cell Reports Medicine.</em> Stanford RCT — basis for cyclic sighing as the first non-negotiable.",
            "Gollwitzer, P. M. & Sheeran, P. (2006). Implementation intentions and goal achievement: a meta-analysis of effects and processes. <em>Advances in Experimental Social Psychology.</em> d = 0.65 effect size.",
            "Walker, M. P. (2017). <em>Why We Sleep.</em> Foundational work on consistent sleep timing as the strongest single sleep-hygiene intervention.",
        ],
        "sources_outro": "",
    },

    # ─── Page 07 ─────────────────────────────────────────────────────────
    {
        "slug": "state-matched-decision-tree",
        "page_num": "07",
        "title": "State-Matched Decision Tree",
        "title_pre_words": "STATE-MATCHED",
        "title_grad_word": "DECISION TREE",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "Most self-care advice ignores the only question that matters: what state am I actually in? Generic calming techniques produced 28% improvement. State-matched interventions hit 67%. The decision tree that picks the right tool for the actual moment.",
        "reading_time": "9 min read",
        "last_updated": "May 2026",
        "source_chapter": "Self-Care, Ch. 3",
        "date_published": "2026-05-01",
        "meta_description": "State-matched regulation is the principle that decides which self-care tool fits which moment. The Window of Tolerance + the 5-step decision tree. Sourced from Kim et al. 2023 and Siegel.",
        "og_description": "Generic regulation: 28% improvement. State-matched regulation: 67%. The decision tree that picks the right tool.",
        "twitter_description": "State-matched regulation has 67% improvement vs 28% for generic. Pick the right tool.",
        "schema_keywords": "state matching, window of tolerance, hyperarousal, hypoarousal, Dan Siegel, Kim 2023, polyvagal, regulation",
        "pull_quote": {
            "text": "Mismatched regulation strategies — using calming techniques during hypoarousal — actively worsened outcomes in 34% of participants. State-matched interventions showed a 67% improvement rate compared to 28% for generic approaches.",
            "cite": "— Kim et al. (2023), Journal of Affective Disorders",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're shut down — flat, numb, unable to feel anything sharp. So you do the thing the wellness industry told you to do: a meditation, a body scan, a slow breath. Twenty minutes later you're shut down and disappointed in yourself. The technique \"didn't work,\" so the conclusion is that you're broken."},
            {"type": "p", "text": "You're not broken. You used a down-regulation tool while your nervous system needed an up-regulation tool. Most self-care advice ignores this distinction entirely — and according to Kim et al. (2023), it makes outcomes <em>worse</em> in roughly a third of cases."},
            {"type": "p", "text": "State-matching is the principle that picks the right tool for the actual state. The decision tree below is the operating system for the rest of the wiki."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three concepts make state-matching work."},
            {"type": "p_bold_lead", "lead": "The Window of Tolerance.", "rest": "Daniel Siegel's framework: every nervous system has a zone of arousal it can function within. Above the window, you're hyperaroused — anxious, racing, hypervigilant. Below it, you're hypoaroused — numb, flat, disconnected. Inside it, you can think, feel, and engage. Most regulation work is about returning to the window, not about staying inside it permanently."},
            {"type": "p_bold_lead", "lead": "Direction matters.", "rest": "Above the window, the body needs <em>down-regulation</em> — vagal activation to engage the parasympathetic brake. Cyclic sighing, diving reflex, humming, extended-exhale breathing. Below the window, the body needs <em>up-regulation</em> — gentle activation to climb out of dorsal vagal shutdown. Cold water on wrists, rhythmic bilateral movement, energizing breath, strong sensory input. Wrong direction, wrong outcome."},
            {"type": "p_bold_lead", "lead": "The mismatch cost is real.", "rest": "Kim et al. (2023, <em>Journal of Affective Disorders</em>) found that state-mismatched interventions — using calming techniques during hypoarousal — not only failed to improve mood, they actively worsened outcomes in 34% of participants. State-matched interventions hit 67% improvement vs. 28% for generic. The same techniques. The variable was whether they fit the state."},
            {"type": "stat_box", "label": "THE STATE-MATCH RESULT", "figure": "67% improvement (matched) vs 28% (generic) · 34% worse outcomes when mismatched", "cite": "Kim et al. (2023, Journal of Affective Disorders) — autonomic state assessment should precede any regulation intervention. The same tools work or actively backfire depending on whether they fit the direction the nervous system actually needs."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Use it before reaching for any regulation tool. The whole point is the order — assessment first, intervention second."},
        ],
        "steps": [
            {
                "name": "Pause and locate",
                "body": "Before doing anything else, pause for 30 seconds. Notice your body without trying to change it. Heart rate. Muscle tension. Breath rhythm. Energy. Don't analyze. Just locate.",
                "tip": "If 30 seconds feels too long, three breaths is enough. The point is to interrupt the automatic reach for whatever technique you usually default to.",
            },
            {
                "name": "Where am I — above, below, or within the window?",
                "body": "Above (hyperarousal): racing thoughts, muscle tension, rapid heart rate, hypervigilance, can't sit still, irritability. Below (hypoarousal): numb, flat, disconnected, unable to move, brain-foggy, vague heaviness. Within: present and engaged, even if struggling with something specific. Most people are not within. Most people are slightly above or slightly below all day and have stopped noticing.",
                "tip": "If you can't tell, you are probably slightly below. People who can't locate state usually default-numb under chronic stress.",
            },
            {
                "name": "If above — down-regulate",
                "body": "Engage the parasympathetic brake. Cyclic sighing (5 min), cold water on the face (15-30 sec), humming (5 min), or extended-exhale breathing (4 in, 8 out). Do not try to think your way through it. The prefrontal cortex is offline above the window. Calm the body first, then engage cognition.",
                "tip": "If above the window for more than an hour, multiple short interventions outperform one long one. Cold water reset → 5 min cyclic sighing → 5 min walk.",
            },
            {
                "name": "If below — up-regulate, gently",
                "body": "Gently mobilize energy without triggering full sympathetic. Cold water on wrists (not face — different effect). Rhythmic bilateral movement (walking with arm swing, drumming on knees). Energizing breath (short inhale, sharp exhale, 30 seconds). Strong sensory input (ice, lemon, peppermint oil). Calling a safe person.",
                "tip": "Slower is faster. Pushing too hard tips you from hypoarousal into sympathetic activation, which is more dysregulated, not less.",
            },
            {
                "name": "If within — HALT and respond",
                "body": "If you're inside the window but still struggling, the issue isn't autonomic state. Run the HALT check (Hungry? Angry? Lonely? Tired?) and address the physiological need. Then ask which dimension of rest is most depleted (physical, mental, emotional, social, sensory, creative) and pick a practice from that dimension.",
                "tip": "Within-the-window distress is usually a HALT signal or a needs-not-met signal, not a regulation problem. Don't apply autonomic tools to a needs problem.",
            },
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Carry it. The 30-second pause to consult the card is the entire trick — the rest is just picking the right tool for the state you actually located.",
        "printable_card": {
            "title": "STATE-MATCHED DECISION TREE",
            "subtitle": "Kim et al. 2023 · Siegel · Self-Care Ch. 3",
            "items": [
                {"num": "01 · PAUSE — 30 SECONDS", "text": "Notice the body. Don't analyze. Just locate.", "help": "Heart, breath, tension, energy."},
                {"num": "02 · ABOVE, BELOW, OR WITHIN?", "text": "Above: racing, tense, hypervigilant. Below: numb, flat, foggy.", "help": "Most people are slightly outside the window."},
                {"num": "03 · IF ABOVE — DOWN-REGULATE", "text": "Cyclic sighing, cold water on face, humming, long exhale.", "help": "Body first. Don't think your way through it."},
                {"num": "04 · IF BELOW — UP-REGULATE GENTLY", "text": "Cold on wrists, walking, rhythm, sensory input, safe person.", "help": "Slower is faster. Don't overshoot to sympathetic."},
                {"num": "05 · IF WITHIN — HALT", "text": "Hungry? Angry? Lonely? Tired? Address the body need first.", "help": "Then pick a rest dimension and a practice from it."},
            ],
        },
        "exits": [
            {
                "tag": "Full chapter · $27",
                "tag_class": "",
                "url": SC_GUMROAD,
                "title": "The Self-Care You Were Never Taught",
                "body": "Chapter 3 covers the full state-matching framework, the autonomic ladder (Deb Dana / Polyvagal Theory), pendulation practice (Peter Levine), and the complete tool inventory for both directions of regulation. The decision tree is the OS; the chapter is the manual.",
                "cta": "Read the book →",
            },
            {
                "tag": "Wiki · Free",
                "tag_class": "free",
                "url": SC_CYCLIC,
                "title": "Cyclic Sighing OS",
                "body": "The most-used down-regulation tool when the decision tree points above the window. Five minutes a day, Stanford 2023.",
                "cta": "Read the page →",
            },
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-state-matched-newsletter",
        "subscribe_source": "source-wiki-state-matched",
        "sources_intro": "All claims on this page are cited in <em>The Self-Care You Were Never Taught</em>, Chapter 3. Primary sources:",
        "sources_list": [
            "Kim, S. et al. (2023). State-matched regulation strategies and outcome variability in mood disorders. <em>Journal of Affective Disorders.</em> 67% improvement matched vs. 28% generic; 34% worsened with mismatch.",
            "Siegel, D. J. (1999/2020). The Window of Tolerance — foundational framework in <em>The Developing Mind</em> and subsequent clinical work.",
            "Dana, D. (2018). <em>The Polyvagal Theory in Therapy.</em> The autonomic ladder model.",
            "Levine, P. (1997). <em>Waking the Tiger.</em> Pendulation practice as the bridge between activation and settling.",
        ],
        "sources_outro": "",
    },
]


def main():
    for page in PAGES:
        slug = page["slug"]
        json_path = CONTENT_DIR / f"{slug}.json"
        html_path = OUTPUT_DIR / f"{slug}.html"
        json_path.write_text(json.dumps(page, indent=2, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(
            ["python3", str(GENERATOR), str(json_path), str(html_path)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"FAIL {slug}: {result.stderr}")
            return
        print(result.stdout.strip())
    print(f"\nAll {len(PAGES)} pages generated.")


if __name__ == "__main__":
    main()
