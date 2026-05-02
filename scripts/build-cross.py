#!/usr/bin/env python3
"""build-cross.py — 5 cross-pillar pages: 3 Wired to Win + 1 FASD + 1 Executive Function."""
import json, subprocess
from pathlib import Path

ROOT = Path("/sessions/friendly-beautiful-ritchie/mnt/thehumanfrequency.net")
GENERATOR = ROOT / "scripts" / "generate-wiki-page.py"
CONTENT_DIR = ROOT / "scripts" / "wiki-content"
OUTPUT_DIR = ROOT / "human-os"

WtW_GUMROAD = "https://thehumanfrequency.gumroad.com/l/cepsrj"  # Wired to Win $34.99
ID_GUMROAD = "https://thehumanfrequency.gumroad.com/l/nzejsn"   # Invisible Disability PWYW $44.99
SB_GUMROAD = "https://thehumanfrequency.gumroad.com/l/xigwwn"
SHOW_LINK = "/thf-podcast"

EXIT_SHOW = {
    "tag": "Show · Coming soon", "tag_class": "community", "url": SHOW_LINK,
    "title": "The Live Show",
    "body": "A live call-in show on the topics this wiki covers — unscripted, judgment-free, ordinary people, extraordinary stories. Join the waitlist for the launch.",
    "cta": "Get on the list →",
}

PAGES = [
    # ─── Page 24: 5-Question Pre-Bet Audit ──────────────────────────────
    {
        "slug": "pre-bet-audit",
        "page_num": "24",
        "title": "5-Question Pre-Bet Audit",
        "title_pre_words": "5-QUESTION",
        "title_grad_word": "PRE-BET AUDIT",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "The decision discipline that separates winning poker players from losing ones — and applies equally to any high-stakes choice you make under pressure. Five questions to run before committing chips, capital, or commitment.",
        "reading_time": "7 min read",
        "last_updated": "May 2026",
        "source_chapter": "Wired to Win, Ch. 14",
        "date_published": "2026-05-01",
        "meta_description": "The 5-question pre-bet audit — the decision discipline that separates winning players from losing ones, applied to any high-stakes decision. Sourced from Wired to Win Ch. 14.",
        "og_description": "Five questions before any high-stakes decision. The discipline that separates winners from losers.",
        "twitter_description": "Five questions before betting chips, capital, or commitment.",
        "schema_keywords": "decision making, poker strategy, pre-decision audit, EV thinking, expected value, Wired to Win",
        "pull_quote": {
            "text": "The losing player and the winning player look identical in any single hand. The difference is invisible: the winner ran a five-question audit before pressing the chip forward; the loser pressed first and rationalized after.",
            "cite": "— Wired to Win, Chapter 14",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're about to make a decision under pressure. A bet at the poker table. A trade. A pricing call on a contract. A response in a difficult conversation. The system 1 (fast, intuitive) brain has already produced an answer. The system 2 (slow, deliberative) brain hasn't shown up yet. Most decisions made under pressure are made by system 1 alone — which means they're made on pattern-match, not on math."},
            {"type": "p", "text": "The 5-Question Pre-Bet Audit forces system 2 online for 30 seconds before commitment. It's the decision-quality equivalent of a pilot's pre-flight checklist: not because pilots are bad, but because the cost of a missed item is asymmetric. Wired to Win Chapter 14 frames it as the highest-leverage decision tool in the catalog. The page below extracts the framework so it works for any high-stakes choice, not just poker."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things make the 5 questions outperform improvisation."},
            {"type": "p_bold_lead", "lead": "System 2 needs an external prompt.", "rest": "Under pressure, the deliberative brain has to be summoned deliberately. It does not show up on its own. A written list of five questions — printed, memorized, tattooed on a wallet card — is the prompt that pulls system 2 online. The questions are not optional even when the answer feels obvious."},
            {"type": "p_bold_lead", "lead": "Each question targets a known cognitive failure mode.", "rest": "Q1 (what's my range vs. theirs) targets the failure to think probabilistically. Q2 (what's the EV) targets the failure to compute expected value. Q3 (am I tilted) targets the failure to notice your own emotional state. Q4 (what's my BATNA / fold equity) targets the failure to consider alternatives. Q5 (what's the worst case I can live with) targets the failure to size the bet to actual stakes. Each question is a checkpoint against a specific bias."},
            {"type": "p_bold_lead", "lead": "Process discipline beats intuition over time.", "rest": "Even great players make decisions that look identical to a losing player's in any single hand. The difference is process discipline — running the questions every hand, every time, regardless of how obvious the answer feels. Over thousands of decisions, the disciplined process compounds. Over single decisions, it looks like overhead. The compounding is the point."},
            {"type": "stat_box", "label": "THE COMPOUND", "figure": "Process discipline > raw skill over thousands of decisions", "cite": "Wired to Win Ch. 14 — the difference between winning and losing professional players is rarely individual hand quality; it's the consistency of the pre-decision audit applied across thousands of decisions."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps, one per question. Adapted from poker to any high-stakes decision. The shapes hold; only the inputs change."},
        ],
        "steps": [
            {"name": "Q1: What's the range — mine and the other side's?", "body": "In poker: what hands could my opponent realistically have, and what hands could I have given the action so far? In any decision: what are the realistic possibilities — for what I'm trying to achieve and for what the other side is doing? \"They have a strong hand\" is a guess. \"They could have any of these 12 hand combinations, and 8 of them beat mine\" is a range.", "tip": "Most decision-making improves dramatically just from substituting \"a range of possibilities\" for \"the most likely outcome.\" The probabilistic frame is the entire trick."},
            {"name": "Q2: What's the expected value (EV)?", "body": "What does this decision pay off, weighted by the probability it pays off? In poker: pot size × probability I win, minus call size × probability I lose. In business: upside × probability of upside, minus cost × probability of failure. EV thinking forces you to multiply, not just add. \"There's a chance this works\" doesn't pencil. \"There's a 30% chance this returns 4x and a 70% chance it returns 0\" pencils.", "tip": "If you can't put numbers on probability, use ranges (\"between 20% and 40%\") and compute EV at both ends. If both endpoints have positive EV, the decision holds; if only one does, you're in fragile territory."},
            {"name": "Q3: Am I tilted?", "body": "Tilt is any emotional state that's distorting my decision-making. In poker, tilt has seven types (covered on the Tilt Taxonomy page). In life, tilt looks like: I'm angry, I'm scared, I'm desperate to recover a loss, I'm proving something to someone, I just won and feel invincible. If I am tilted, my pre-bet answers in Q1 and Q2 are unreliable. The honest answer to Q3 may be: pause until tilted state passes. That's a complete decision.", "tip": "If you can't tell whether you're tilted, ask: would I make this decision the same way if I'd had the previous 30 minutes go differently? If the answer is no, you're tilted."},
            {"name": "Q4: What's my BATNA?", "body": "What is my best alternative to making this commitment right now? In poker: I can fold and play the next hand. In business: I can wait, negotiate further, walk away to another offer, or do nothing. Most pressured decisions feel binary (\"do this or lose everything\") and are actually multi-option. Naming the BATNA explicitly — even for 10 seconds — is what shifts the decision from \"do it\" to \"is this better than my alternative.\"", "tip": "If your BATNA is genuinely terrible, that's information about the broader situation, not an instruction to take the current bad option. Often the right response to a bad BATNA is to invest in strengthening alternatives, not to accept a bad current deal."},
            {"name": "Q5: What's the worst case I can live with?", "body": "If this decision goes badly, what's the loss? Can I survive it financially, professionally, relationally? Sizing the bet to your actual stakes is the difference between healthy risk-taking and ruin. \"This will work out\" is not a sizing rule. \"If this returns 0, I can absorb it\" is. The Tendler stop-loss principle applies here: pre-commit the worst case before pressure arrives.", "tip": "If you cannot articulate the worst case in concrete terms (specific dollar loss, specific reputation hit, specific time cost), you're not ready to commit. The unease is information."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Keep it visible during high-stakes decisions. The 30 seconds it takes to run is the highest-leverage time in the entire decision.",
        "printable_card": {
            "title": "5-QUESTION PRE-BET AUDIT",
            "subtitle": "Wired to Win Ch. 14",
            "items": [
                {"num": "01 · RANGE — MINE AND THEIRS", "text": "What are the realistic possibilities? Probabilistic, not single-answer.", "help": "\"A range of\" beats \"the likely.\""},
                {"num": "02 · EXPECTED VALUE", "text": "Upside × probability minus downside × probability.", "help": "Multiply, not add."},
                {"num": "03 · AM I TILTED?", "text": "Angry, scared, desperate, proving? If yes, pause.", "help": "Tilted answers to Q1+Q2 are unreliable."},
                {"num": "04 · BATNA", "text": "Best alternative if I don't commit right now?", "help": "Most pressured decisions feel binary, are multi-option."},
                {"num": "05 · WORST CASE I CAN LIVE WITH", "text": "Concrete dollar / time / reputation loss. Pre-committed.", "help": "If you can't articulate it concretely, you're not ready."},
            ],
        },
        "exits": [
            {"tag": "Full guide · $34.99", "tag_class": "", "url": WtW_GUMROAD, "title": "Wired to Win", "body": "Chapter 14 covers the 5-Question Pre-Bet Audit in poker context, with worked examples for cash games and tournaments. Plus the full tilt taxonomy and the mental hand history framework that catches what the audit missed.", "cta": "Read the book →"},
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/tilt-taxonomy", "title": "Tendler 7-Tilt OS", "body": "Q3 — \"am I tilted\" — has seven distinct answers. The next page covers each, with the specific cognitive injection that defuses each one.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-pre-bet-newsletter",
        "subscribe_source": "source-wiki-pre-bet",
        "sources_intro": "All claims on this page are sourced from <em>Wired to Win</em>, Chapter 14. Primary sources cited:",
        "sources_list": [
            "Tendler, J. (2011). <em>The Mental Game of Poker.</em> Foundational on tilt and structured pre-decision discipline.",
            "Kahneman, D. (2011). <em>Thinking, Fast and Slow.</em> System 1 vs. System 2 framework underlying the audit's necessity.",
            "Wired to Win Ch. 14 — operationalized for poker; this page extracts the framework for any high-stakes decision.",
        ],
        "sources_outro": "",
    },

    # ─── Page 25: Tendler 7-Tilt ────────────────────────────────────────
    {
        "slug": "tilt-taxonomy",
        "page_num": "25",
        "title": "Tendler 7-Tilt OS",
        "title_pre_words": "TENDLER",
        "title_grad_word": "7-TILT OS",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "Tilt isn't one thing. It's seven distinct types, each with a different trigger, a different root belief, and a different cognitive injection that defuses it. Treating all tilt the same is like treating all illnesses with the same medicine.",
        "reading_time": "9 min read",
        "last_updated": "May 2026",
        "source_chapter": "Wired to Win, Ch. 13",
        "date_published": "2026-05-01",
        "meta_description": "Jared Tendler's tilt taxonomy: seven types of emotional disruption, each with a specific cognitive injection that defuses it. Sourced from Wired to Win Ch. 13.",
        "og_description": "Tilt isn't one thing. It's seven distinct types, each with a different cure.",
        "twitter_description": "Seven types of tilt. Seven cognitive injections. Tendler's framework.",
        "schema_keywords": "tilt, emotional regulation, Jared Tendler, mental game, decision making under stress",
        "pull_quote": {
            "text": "Treating all tilt as a single phenomenon, as most players do, is like treating all illnesses with the same medicine. You have to diagnose before you can treat.",
            "cite": "— Wired to Win, Chapter 13 (after Tendler)",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "Something just went badly. A bad beat, a missed forecast, a project that imploded, a comment that landed wrong. The next 20 minutes of your decision-making are not the same as the previous 20. Your brain is now operating from a different state — heightened emotion, narrowed focus, distorted probability assessment. This is tilt."},
            {"type": "p", "text": "Most people treat tilt as a single condition: \"I'm tilted, I should calm down.\" Jared Tendler's framework — synthesized in Wired to Win Ch. 13 — argues that tilt is actually seven distinct conditions. Each has its own trigger, its own underlying belief, and its own cognitive correction. Generic \"calm down\" advice fails because the right correction depends on which type of tilt you're in."},
            {"type": "p", "text": "This page maps the seven tilts. The exact cognitive injection from Tendler's framework is included for each. The whole list fits on a card you can carry."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things make the taxonomy useful."},
            {"type": "p_bold_lead", "lead": "Each tilt has a flawed belief.", "rest": "Tendler's insight: tilt is downstream of an underlying belief that's wrong. Running-Bad tilt is downstream of \"results should match decision quality in the short run.\" Hate-Losing tilt is downstream of \"losing reflects negatively on me as a person.\" The cognitive injection works by surfacing and correcting the belief, not by suppressing the emotion."},
            {"type": "p_bold_lead", "lead": "Reading the injection out loud engages a different circuit.", "rest": "Tendler recommends building a \"tilt first-aid kit\" — written corrections in your own words, accessed during a break. The act of reading, not just thinking, engages different cognitive pathways than the emotional circuits firing. Reading breaks the loop in a way internal monologue can't."},
            {"type": "p_bold_lead", "lead": "Naming is half the work.", "rest": "Just identifying which type of tilt you're in often defuses 30-50% of it. The diagnostic act — \"this is Mistake Tilt, not Running-Bad Tilt\" — is itself an act of system 2 engagement, which lowers system 1's grip. Even if you don't apply the injection, naming the type helps."},
            {"type": "stat_box", "label": "THE SEVEN TYPES", "figure": "Running-Bad · Injustice · Hate-Losing · Entitlement · Revenge · Desperation · Mistake", "cite": "Tendler, J. (2011). <em>The Mental Game of Poker.</em> Synthesized in Wired to Win Ch. 13. Each type has a distinct trigger, root belief, and cognitive injection."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Step 1 is the diagnostic; steps 2-5 are the four most-encountered tilt types and their injections. The full seven are on the printable card."},
        ],
        "steps": [
            {"name": "Diagnose first — name the type", "body": "Before applying any injection, identify which tilt type is firing. The triggers help: did you just have a streak of bad outcomes (Running-Bad)? A specific unfair-feeling event (Injustice)? Any loss at all (Hate-Losing)? A loss to someone you perceive as inferior (Entitlement)? A specific opponent (Revenge)? A deep losing session you want to recover (Desperation)? A mistake you knew was wrong as you made it (Mistake)? Pick the one that fits.", "tip": "If two types feel applicable, the more specific one usually fires first. \"I lost to my rival\" looks like both Hate-Losing and Entitlement; if the trigger is the rival specifically, it's Entitlement; if it's the loss in general, it's Hate-Losing."},
            {"name": "Running-Bad → variance is math, not punishment", "body": "Trigger: a cluster of negative outcomes. Belief: \"results should match decision quality in the short run.\" Injection (read aloud): <em>\"Variance is a mathematical certainty, not a personal attack. A 5bb/100 winner will lose for 50,000 hands and it's a statistically unremarkable event. My strategy doesn't become wrong because the last 500 hands went against me. The sample is too small to draw any conclusion. Keep playing correctly. The math takes care of the rest.\"</em>", "tip": "Adapt the injection to your domain. For trading: \"a 60%-edge strategy will lose 40% of trades, including streaks. The streak is not evidence the strategy is wrong.\" For business: \"good decisions can produce bad outcomes in any single quarter.\""},
            {"name": "Injustice → opponent's mistake = your long-term profit", "body": "Trigger: a specific bad beat that feels fundamentally unfair. Belief: \"the game should reward good play and punish bad play in real time.\" Injection: <em>\"My opponent's mistake is my long-term profit source. If they always played correctly, I'd have no edge. The specific hand where their mistake got rewarded is the price of admission to a game where their mistakes fund my income across thousands of hands. I want them to make that call every time.\"</em>", "tip": "Injustice tilt is the most contagious — it spreads to bystanders watching your bad beat. Articulating the injection to yourself prevents the spread."},
            {"name": "Hate-Losing → losing is structural, not personal", "body": "Trigger: any loss, even a correct one. Belief: \"losing reflects on me as a player and as a person.\" Injection: <em>\"Losing is a structural feature of the game, not a failure. Even the best player in the world loses roughly 40% of their sessions. My job is to make correct decisions, not to win every hand. Decision quality is the only metric that matters, and it's completely disconnected from short-term monetary results.\"</em>", "tip": "Hate-Losing is the most common tilt in domains where competence is part of identity (engineering, surgery, anything credential-heavy). The injection is decoupling decision quality from outcome."},
            {"name": "Mistake → recover, don't compound", "body": "Trigger: making an error you knew was wrong as you made it. Belief: \"one mistake means I've lost control. If I can't play my A-game, I might as well give up on this session.\" Injection: <em>\"Everyone makes mistakes. The best players in the world make multiple mistakes per session. The difference is that they don't let one mistake become five. Acknowledge the error, note it for post-session review, and reset. The next hand is independent of the last one. My ability to recover from a mistake is a more important skill than never making one.\"</em>", "tip": "Mistake Tilt is the most dangerous because it cascades. Catching it early is the difference between a one-mistake session and a ten-mistake session. The Mental Hand History (next page) is the post-session debrief that prevents the same mistake next time."},
        ],
        "after_steps_h2": "The printable: the seven-tilt card",
        "after_steps_p": "Print this. The card lists all seven tilts with their triggers and injections. Build your own \"tilt first-aid kit\" — write the injections in your own words, with examples from your own history.",
        "printable_card": {
            "title": "TENDLER 7-TILT TAXONOMY",
            "subtitle": "Wired to Win Ch. 13",
            "items": [
                {"num": "01 · RUNNING-BAD", "text": "Cluster of negative outcomes. \"Results should match decisions short-term.\"", "help": "Variance is math, not punishment."},
                {"num": "02 · INJUSTICE", "text": "Specific unfair beat. \"The game should reward good play in real time.\"", "help": "Their mistake is your long-term profit."},
                {"num": "03 · HATE-LOSING + ENTITLEMENT", "text": "Any loss / loss to inferior. Structural feature, not personal failure.", "help": "Even pros lose 40% of sessions."},
                {"num": "04 · REVENGE + DESPERATION", "text": "Specific opponent / want to recover before quitting.", "help": "Each hand independent. Honor the stop-loss."},
                {"num": "05 · MISTAKE", "text": "Error you knew was wrong as you made it.", "help": "Recover, don't compound. One mistake ≠ five."},
            ],
        },
        "exits": [
            {"tag": "Full guide · $34.99", "tag_class": "", "url": WtW_GUMROAD, "title": "Wired to Win", "body": "Chapter 13 covers all seven tilts in clinical detail with poker-specific examples and the full tilt first-aid kit template. Chapter 14 is the pre-bet audit; Chapter 16 is the mental hand history that converts post-session reflection into compounding skill.", "cta": "Read the book →"},
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/mental-hand-history", "title": "Mental Hand History OS", "body": "After tilt, the post-session debrief. The 5-step Mental Hand History format that turns emotional leakage into structured learning.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-tilt-newsletter",
        "subscribe_source": "source-wiki-tilt",
        "sources_intro": "All claims on this page are sourced from <em>Wired to Win</em>, Chapter 13. Primary sources cited:",
        "sources_list": [
            "Tendler, J. (2011). <em>The Mental Game of Poker.</em>",
            "Tendler, J. (2013). <em>The Mental Game of Poker 2.</em>",
            "Wired to Win Ch. 13 — synthesized tilt taxonomy with poker-specific cognitive injections; framework adapted for general decision-making in this page.",
        ],
        "sources_outro": "",
    },

    # ─── Page 26: Mental Hand History ───────────────────────────────────
    {
        "slug": "mental-hand-history",
        "page_num": "26",
        "title": "Mental Hand History OS",
        "title_pre_words": "MENTAL HAND",
        "title_grad_word": "HISTORY",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "The 5-step structured-writing protocol that converts emotional leakage into compounding skill. Used by professional poker players to externalize tilt analysis. Applies to any domain where decisions under pressure matter.",
        "reading_time": "7 min read",
        "last_updated": "May 2026",
        "source_chapter": "Wired to Win, Ch. 13 + 16",
        "date_published": "2026-05-01",
        "meta_description": "The Mental Hand History — Tendler's 5-step structured writing format that turns emotional leakage into compounding skill. Sourced from Wired to Win Ch. 13 + 16.",
        "og_description": "Five-step structured writing. Externalize the tilt. Compound the learning.",
        "twitter_description": "Five steps. Structured writing. Externalize the tilt.",
        "schema_keywords": "mental hand history, Jared Tendler, structured reflection, decision review, post-session debrief",
        "pull_quote": {
            "text": "Writing forces the analytical brain to engage, which is exactly what both ADHD and autistic emotional processing benefit from. The MHH externalizes implicit emotional regulation into explicit systematic analysis.",
            "cite": "— Wired to Win, Chapter 13",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You had a bad session. Bad day at work. Bad meeting. Bad week. The tilt has receded; the lessons haven't landed. You know something went wrong but you can't articulate what — and tomorrow you'll probably make the same mistake."},
            {"type": "p", "text": "Tendler's solution from poker, refined in Wired to Win, is the Mental Hand History (MHH) — a 5-step structured-writing protocol that converts implicit emotional processing into explicit systematic analysis. It's not journaling. It's not venting. It's a deliberate format that catches what your unconscious processing would otherwise miss."},
            {"type": "p", "text": "The page below applies the MHH format to any domain where decisions under pressure matter. The structure holds. Only the inputs change."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things make MHH outperform unstructured reflection."},
            {"type": "p_bold_lead", "lead": "Writing engages a different circuit.", "rest": "Internal rumination tends to loop the same emotional content without resolution. Writing forces sequencing, naming, and explicit causation — all functions of the analytical brain. The act of producing words on paper engages the prefrontal cortex in a way that thinking about what happened doesn't."},
            {"type": "p_bold_lead", "lead": "Format catches what free-form misses.", "rest": "Five fixed steps prevent the brain from gravitating to its preferred narrative. Step 4 — naming the underlying flawed belief — is the one most people skip in free-form reflection. The format makes it mandatory."},
            {"type": "p_bold_lead", "lead": "Weekly review compounds.", "rest": "A single MHH entry is useful. A weekly review of recent entries reveals patterns you cannot see at the level of individual events. Three weeks of entries shows that your tilt episodes cluster around the same trigger type. Six months shows whether your corrections are actually working. The compounding is in the review, not the writing."},
            {"type": "stat_box", "label": "THE FORMAT", "figure": "5 steps · 10-15 minutes · weekly review", "cite": "Wired to Win Ch. 13 — Mental Hand History format from Tendler's <em>The Mental Game of Poker</em>; the weekly review described in Ch. 16 is what produces compounding pattern recognition."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. One per MHH entry. 10-15 minutes per entry. Done after the session/event ends and the body has settled — not during the heat."},
        ],
        "steps": [
            {"name": "Describe the triggering situation factually", "body": "What happened, in concrete terms. No emotional language yet. \"At 3:47 PM I lost a 12 bb pot to a flush draw that hit on the river.\" Or \"In the 2 PM meeting, my proposal was rejected after 90 seconds of discussion, and the CEO interrupted me when I tried to clarify.\" Just the facts. No interpretation. No \"and that wasn't fair\" yet.", "tip": "If you find yourself adding interpretation, edit it out. The discipline of writing the facts cleanly is itself an act of cognitive control."},
            {"name": "Identify the emotional response without judgment", "body": "What did you feel, in plain language. Not why. Not whether it was justified. Just the feeling. \"I felt anger that intensified into a sense of helplessness over the next 10 minutes.\" \"I felt humiliation followed by a strong urge to leave the meeting.\" The naming itself does work that pure rumination cannot.", "tip": "Use specific emotional vocabulary. \"I was upset\" is too vague. \"I felt resentful, then ashamed, then a flat tiredness\" surfaces information about the actual cascade."},
            {"name": "Name the tilt type — from the taxonomy", "body": "Match the response to one of the seven tilts from the previous page (Running-Bad, Injustice, Hate-Losing, Entitlement, Revenge, Desperation, Mistake). The diagnostic act is what activates the right correction. \"This is Injustice Tilt — the river card felt unfair.\" \"This is Hate-Losing — I was angry that the proposal lost, not specifically about who won.\" Pick one even if multiple feel applicable; the more specific one usually fires first.", "tip": "If none of the seven fits, you may be in sensory overload (especially relevant for ND profiles), grief, or fatigue — which require different interventions than tilt. Naming \"this isn't tilt, it's overload\" is itself useful."},
            {"name": "Trace it to the underlying flawed belief", "body": "Tendler's insight: every tilt sits on top of a wrong belief. Surface yours. \"My belief was: <em>my opponent's bad call shouldn't be rewarded</em> — which assumes the game owes me something.\" Or \"My belief was: <em>my proposal was so well-prepared it deserved to win on merit</em> — which assumes the meeting was a meritocracy and not a political environment.\" Be brutal about it.", "tip": "The honest answer to \"what did I believe?\" is often something you wouldn't want to say out loud. Write it anyway. The ugly version is the accurate one."},
            {"name": "Write the logical correction in your own words", "body": "Replace the flawed belief with one that's true. \"The game does not owe me variance-free results. My opponent's bad calls fund my edge over thousands of hands. The river hand is the cost of running a profitable strategy.\" \"Meetings are political environments. Merit is necessary but not sufficient. My job is to combine merit with influence and stakeholder management.\" Use specific examples from your own history when you can — concrete corrections compound faster than abstract ones.", "tip": "Save these. The collection of corrections becomes your tilt first-aid kit — exactly the thing Tendler recommends. Read them during the next tilt episode, not for the first time during it."},
        ],
        "after_steps_h2": "The printable: the MHH worksheet",
        "after_steps_p": "Print this. Use it the next time something goes badly. 10-15 minutes of structured writing produces more learning than 3 hours of unstructured rumination.",
        "printable_card": {
            "title": "MENTAL HAND HISTORY · 5 STEPS",
            "subtitle": "Tendler · Wired to Win Ch. 13",
            "items": [
                {"num": "01 · TRIGGERING SITUATION — FACTUALLY", "text": "What happened, no emotional language yet.", "help": "Edit out interpretation."},
                {"num": "02 · EMOTIONAL RESPONSE — NO JUDGMENT", "text": "What you felt, in specific vocabulary. Not why.", "help": "Specific words surface the cascade."},
                {"num": "03 · TILT TYPE — FROM TAXONOMY", "text": "Pick one of the seven. Most specific fits.", "help": "Activates the right correction."},
                {"num": "04 · UNDERLYING FLAWED BELIEF", "text": "What did I believe that produced this response?", "help": "Be brutal. Ugly version = accurate version."},
                {"num": "05 · LOGICAL CORRECTION — OWN WORDS", "text": "Replace the flawed belief with one that's true.", "help": "Save them. They become your first-aid kit."},
            ],
        },
        "exits": [
            {"tag": "Full guide · $34.99", "tag_class": "", "url": WtW_GUMROAD, "title": "Wired to Win", "body": "Chapter 13 contains the full MHH framework with worked examples for every tilt type. Chapter 16 covers the weekly review process that produces pattern recognition across entries — the compounding part.", "cta": "Read the book →"},
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/tilt-taxonomy", "title": "Tendler 7-Tilt OS", "body": "Step 3 of the MHH requires diagnosing which of the seven tilts is firing. The taxonomy page is the reference.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-mhh-newsletter",
        "subscribe_source": "source-wiki-mhh",
        "sources_intro": "All claims on this page are sourced from <em>Wired to Win</em>, Chapters 13 and 16. Primary sources cited:",
        "sources_list": [
            "Tendler, J. (2011). <em>The Mental Game of Poker.</em> Origin of the Mental Hand History format.",
            "Wired to Win Ch. 13 — MHH 5-step structure; Ch. 16 — weekly review for pattern recognition.",
            "Pennebaker, J. W. (1997). Writing about emotional experiences as a therapeutic process. <em>Psychological Science.</em> Foundational empirical support for structured-writing protocols.",
        ],
        "sources_outro": "",
    },

    # ─── Page 27: 8 Magic Keys (FASD) ───────────────────────────────────
    {
        "slug": "eight-magic-keys",
        "page_num": "27",
        "title": "The 8 Magic Keys (FASD)",
        "title_pre_words": "8 MAGIC",
        "title_grad_word": "KEYS",
        "pillar": "UNDERSTANDING YOUR KIDS",
        "thesis": "The foundational framework for FASD-informed parenting and care. Not suggestions — essential survival tools, developed through decades of clinical practice. The eight environmental modifications that compensate for the brain damage that has no medication.",
        "reading_time": "9 min read",
        "last_updated": "May 2026",
        "source_chapter": "The Invisible Disability, Ch. 4",
        "date_published": "2026-05-01",
        "meta_description": "The 8 Magic Keys — the foundational framework for FASD-informed environmental accommodation. Structure, Concrete Language, Consistency, Repetition, Routine, Simplify, Specific Directives, Supervision. Sourced from Invisible Disability Ch. 4.",
        "og_description": "The 8 Magic Keys for FASD. Environmental modifications that compensate for brain damage that has no medication.",
        "twitter_description": "Eight environmental modifications for FASD. Foundational framework.",
        "schema_keywords": "FASD, fetal alcohol spectrum disorder, 8 magic keys, environmental accommodation, neurodivergent parenting",
        "pull_quote": {
            "text": "These are not suggestions. They are essential survival tools. Adopted by FASD intervention programs across North America, Australia, and Europe. The brain damage will not heal; the environment can adapt around it.",
            "cite": "— The Invisible Disability, Chapter 4",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "FASD — Fetal Alcohol Spectrum Disorder — is the most prevalent and least diagnosed neurodevelopmental disability in the world. The brain damage is permanent. There is no medication that fixes it. Traditional discipline does not work because the brain that needs to learn from consequences is the brain that's damaged. Most of what well-meaning parents and teachers do to help actually makes things worse."},
            {"type": "p", "text": "What does work is environmental accommodation — adapting the world around the FASD brain to compensate for the missing internal capacities. The 8 Magic Keys, developed through decades of clinical practice and adopted by FASD programs across three continents, are the operational framework."},
            {"type": "p", "text": "This page summarizes all eight in their published form, sourced from <em>The Invisible Disability</em> Chapter 4. The book's full chapter includes scripts, age-banded applications, and the neuroscience behind why each Key works. The summary below is what every caregiver, teacher, and clinician working with FASD needs in their pocket."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things explain why the Magic Keys work where ordinary parenting strategies fail."},
            {"type": "p_bold_lead", "lead": "Brain damage requires environmental adaptation, not behavioral training.", "rest": "FASD damages specific brain structures: prefrontal cortex (executive function), hippocampus (memory consolidation), corpus callosum (interhemispheric processing), amygdala (threat regulation). These are not skills that can be trained. The Keys do not fix the brain; they reshape the environment so the brain that exists can function."},
            {"type": "p_bold_lead", "lead": "What looks like defiance is usually disability.", "rest": "Forgetting a rule that was learned yesterday looks like defiance to a neurotypical observer. For FASD, it's the hippocampus damage. The Keys reframe \"won't\" as \"can't\" — and the practical consequence is structural, not motivational. You don't punish; you accommodate."},
            {"type": "p_bold_lead", "lead": "Lifelong supervision is love, not control.", "rest": "FASD adaptive functioning typically operates at 50-70% of chronological age. A 16-year-old with FASD often functions at 9-11 in social judgment and risk assessment. Withdrawing supervision as a reward for good behavior — standard for neurotypical parenting — is dangerous for FASD. The 8th Key is supervision as a permanent accommodation, framed as care."},
            {"type": "stat_box", "label": "THE EVIDENCE", "figure": "Adopted across NA, Australia, Europe · decades of clinical practice", "cite": "Invisible Disability Ch. 4 — 8 Magic Keys developed through decades of clinical practice; widely adopted across FASD intervention programs in North America, Australia, and Europe."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "All eight Keys, condensed. The book's chapter has scripts, neuroscience, and applied examples for each — this page is the at-a-glance reference."},
        ],
        "steps": [
            {"name": "Keys 1-2: Structure + Concrete Language", "body": "<strong>Structure</strong> — Externalize the timeline the brain cannot generate internally. Photo-based visual schedules at eye level, Velcro \"done\" cards, visual timers, same schedule every day in the same location. Replaces the missing internal sequencing. <strong>Concrete Language</strong> — Frontal lobe damage impairs interpretation of abstract, figurative, or implied meaning. Say exactly what you mean. \"Put your shoes on, they are by the door\" instead of \"Get ready.\" Idioms, sarcasm, rhetorical questions cause confusion. One possible meaning per instruction.", "tip": "Pair every verbal instruction with a visual cue when possible. The visual works when the verbal evaporates."},
            {"name": "Keys 3-4: Consistency + Repetition", "body": "<strong>Consistency</strong> — The FASD brain cannot generalize. \"No running\" in the school hallway is a different rule from \"no running\" in the grocery store as far as the brain is concerned. All caregivers — parents, teachers, babysitters, grandparents — use identical language for the same rule. Written cheat sheet of exact phrasings distributed to every adult. <strong>Repetition</strong> — The hippocampus is damaged. Neurotypical learners need 3-7 exposures; FASD may need 50, 100, or more. Repeat the same rule on day 50 with the same neutral tone you used on day 1. No frustration. No \"I told you this already.\" Repetition is the treatment.", "tip": "When teaching a new rule to an FASD individual, pre-commit to 100 repetitions before evaluating whether they've learned it. The frustration that derails caregivers usually appears around repetition 15-20."},
            {"name": "Keys 5-6: Routine + Simplify", "body": "<strong>Routine</strong> — Without the ability to predict what comes next, every moment carries uncertainty. The amygdala fires. Predictable routines provide the safety the brain cannot generate internally. Same Monday as last Monday. Bath at the same time. Bedtime ritual identical every night. Visual change card 24 hours in advance for any unavoidable variation. <strong>Simplify</strong> — Sensory and cognitive load overwhelms the FASD brain. Minimal furniture. Muted colors. One toy bin out at a time. One instruction given, completed, acknowledged before the next. Two outfit choices laid out the night before, not a closet full of options.", "tip": "Surprise outings presented as treats almost always backfire. \"We're going somewhere fun!\" without specifying where, when, and what triggers exactly the unpredictability the routine was designed to prevent."},
            {"name": "Key 7: Specific Directives — micro-commands not goals", "body": "Prefrontal cortex damage means the brain cannot reverse-engineer a large objective into steps. \"Clean your room\" causes executive paralysis because the brain cannot determine where to start, what to do next, or what \"clean\" means in concrete terms. Issue one instruction at a time. Wait for completion. Confirm. Then the next. \"Pick up the clothes on the floor. Put them in the hamper.\" [Wait.] \"Now pick up the toys. Put them in the blue bin.\" [Wait.] Each step named, each step confirmed before the next.", "tip": "This is the same principle as the 5-Task Reframe page (which sources from Survival Blueprint), applied with even tighter granularity. For FASD, every step is its own atomic instruction."},
            {"name": "Key 8: Supervision — Think Younger paradigm", "body": "Adaptive functioning at 50-70% of chronological age. Ask yourself: \"Would I leave a 9-year-old alone in this situation?\" before making supervision decisions about a 16-year-old with FASD. Pre-arranged activities for unstructured time. An adult present during peer interactions. Explicit safety scripts practiced weekly. Supervision is not punishment. It is not lack of trust. It is an accommodation, framed as love. The script: \"I check on you because my job is to keep you safe. The same way I look both ways before you cross the street. This is not punishment. This is because I love you and your brain needs a teammate for some things.\"", "tip": "Withdrawing supervision as a reward for good behavior is a standard neurotypical parenting strategy and a dangerous FASD strategy. The Key is permanent supervision, calibrated to functional age, framed as care across the lifespan."},
        ],
        "after_steps_h2": "The printable: the 8-Key reference card",
        "after_steps_p": "Print this. Distribute to every caregiver. The Keys only work when applied consistently across everyone in the FASD individual's life.",
        "printable_card": {
            "title": "8 MAGIC KEYS · FASD-INFORMED CARE",
            "subtitle": "Invisible Disability Ch. 4",
            "items": [
                {"num": "01-02 · STRUCTURE + CONCRETE LANGUAGE", "text": "Visual schedules. Say exactly what you mean. One meaning per instruction.", "help": "External timeline. Literal interpretation only."},
                {"num": "03-04 · CONSISTENCY + REPETITION", "text": "Identical language across caregivers. 100+ repetitions, neutral tone.", "help": "FASD brain cannot generalize. Hippocampus is damaged."},
                {"num": "05-06 · ROUTINE + SIMPLIFY", "text": "Predictable schedule. Minimal sensory load. One thing at a time.", "help": "Predictability replaces missing internal capacity."},
                {"num": "07 · SPECIFIC DIRECTIVES", "text": "Micro-commands. One step. Wait. Confirm. Next.", "help": "No goals like \"clean your room.\""},
                {"num": "08 · SUPERVISION — THINK YOUNGER", "text": "Adaptive age 50-70% of chronological. Lifelong accommodation.", "help": "Framed as love, not control."},
            ],
        },
        "exits": [
            {"tag": "Full guide · $44.99+", "tag_class": "", "url": ID_GUMROAD, "title": "The Invisible Disability", "body": "Chapter 4 contains all eight Keys in expanded form with scripts, neuroscience, and age-banded applications (5-9, 10-14, 15-18+). Plus the FASD justice-system chapter, the school advocacy templates, and the caregiver burnout assessment.", "cta": "Read the guide →"},
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/five-task-reframe", "title": "The 5-Task Reframe", "body": "Key 7 (Specific Directives) is the FASD-specific version of the 5-Task Reframe. The general principle applies to ADHD and ND profiles broadly; the FASD application is even tighter.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-magic-keys-newsletter",
        "subscribe_source": "source-wiki-magic-keys",
        "sources_intro": "All claims on this page are sourced from <em>The Invisible Disability</em>, Chapter 4. Primary sources cited:",
        "sources_list": [
            "Evensen, D. & Lutke, J. — Original 8 Magic Keys framework, developed through decades of clinical practice with FASD populations.",
            "Cook, J. L. et al. — Canadian FASD diagnostic guidelines.",
            "SAMHSA Technical Assistance Publication (TIP) 58 — FASD Treatment.",
            "Invisible Disability Ch. 4 — Synthesized framework with scripts, neuroscience, and age-banded applications.",
        ],
        "sources_outro": "",
    },

    # ─── Page 28: Executive Function Scaffolding ────────────────────────
    {
        "slug": "executive-function-scaffolding",
        "page_num": "28",
        "title": "Executive Function Scaffolding OS",
        "title_pre_words": "EXECUTIVE FUNCTION",
        "title_grad_word": "SCAFFOLDING",
        "pillar": "UNDERSTANDING YOURSELF",
        "thesis": "Executive function isn't one skill — it's a cluster: task initiation, working memory, time management, planning, organization, emotional regulation, sustained attention. The scaffolding framework for compensating each one when the internal version is unreliable.",
        "reading_time": "8 min read",
        "last_updated": "May 2026",
        "source_chapter": "Survival Blueprint Ch. 2 + Invisible Disability Ch. 4",
        "date_published": "2026-05-01",
        "meta_description": "Executive function scaffolding — external systems that compensate for ADHD, autism, FASD, or ND profiles. Body doubling, externalized time, written checklists, environmental cues. Sourced from Survival Blueprint + Invisible Disability.",
        "og_description": "Executive function isn't one skill. The scaffolding framework for compensating each one externally.",
        "twitter_description": "Executive function isn't one skill. The scaffolding for compensating each one externally.",
        "schema_keywords": "executive function, ADHD, body doubling, time blindness, working memory, scaffolding, ND adult",
        "pull_quote": {
            "text": "Externalize what the brain cannot internalize. The scaffolding is not a training wheel — it is a permanent accommodation. The goal is not to eventually do without it; the goal is to function fully with it.",
            "cite": "— Survival Blueprint Ch. 2 + Invisible Disability Ch. 4",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You have ADHD, autism, FASD, or some 2e combination — or you don't have a diagnosis at all but the executive function piece of your brain runs unreliably. Tasks pile up. You forget things you genuinely intended to do. You can plan a project flawlessly in your head and not start it. Time evaporates without your noticing. The frustration is not that you're not trying. The frustration is that trying isn't the lever."},
            {"type": "p", "text": "Executive function is not one skill. It's a cluster: task initiation, sustained attention, working memory, time management, planning, organization, emotional regulation. The cluster shows up across diagnoses (ADHD, autism, FASD, depression, anxiety, brain injury, just being human) and the interventions are the same shape — externalizing what the brain can't internalize."},
            {"type": "p", "text": "This page is the cross-domain scaffolding framework. Pulled from the executive-function strategies in Survival Blueprint Ch. 2 and the 8 Magic Keys in Invisible Disability Ch. 4. Adapted for adult use without parental supervision in the picture."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things make scaffolding outperform willpower."},
            {"type": "p_bold_lead", "lead": "External structure replaces missing internal capacity.", "rest": "The brain that cannot generate an internal timeline can use an external timeline. The brain that cannot reliably remember can use external memory (lists, notes, alarms, recurring calendar events). The scaffolding works because it does the cognitive work the brain isn't doing — not because it makes the brain do that work."},
            {"type": "p_bold_lead", "lead": "Body-doubling outperforms self-direction.", "rest": "Working alongside another person — even silently, even virtually — provides external activation that the deficient task-initiation circuit can borrow. ADHD coaches and tools like FocusMate operationalize this. The mechanism is not accountability; it's the presence of another nervous system anchoring you in the present task."},
            {"type": "p_bold_lead", "lead": "Permanence is the design feature.", "rest": "The scaffolding is not a training wheel you eventually remove. It is permanent infrastructure. People who treat it as temporary keep \"trying to do without\" and keep failing. The Invisible Disability framing — \"this is not a training wheel — it is a permanent accommodation\" — applies broadly. Glasses do not make your eyes weaker. Scaffolding does not make your executive function weaker. It makes your function possible."},
            {"type": "stat_box", "label": "THE FRAMING", "figure": "Permanent accommodation · not training wheel", "cite": "Invisible Disability Ch. 4 + Survival Blueprint Ch. 2 — executive function scaffolding works only when treated as permanent infrastructure, not as a temporary support to outgrow."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Each one externalizes a different EF cluster. Build them as a layered system, not all at once."},
        ],
        "steps": [
            {"name": "Externalize time — visual, not numerical", "body": "Time blindness is the most common EF deficit and the least understood by neurotypical observers. Numerical time (\"it's 3:42\") doesn't register the same way visual time does. Use Time Timer-style devices or apps that show time as a shrinking visual wedge. Calendar blocks for every commitment, including blocks for transitions, breaks, and \"deep work.\" If it's not on the calendar in a visible block, it doesn't exist. Phone alarms 15 minutes before every transition.", "tip": "The single highest-leverage scaffolding for adults with EF challenges is moving from \"a task list of things to do today\" to \"a calendar with explicit time blocks for each task.\" The list is data; the calendar is structure."},
            {"name": "Externalize working memory — write everything", "body": "Working memory tops out fast for ND brains. Anything held in working memory tends to evaporate. Externalize it: write down ideas as they arrive, capture commitments the moment you make them, dump tomorrow's tasks before you go to sleep, leave physical notes for yourself in obvious places. \"I'll remember that\" is the most expensive sentence in your vocabulary.", "tip": "Use one capture system, not five. Phone notes app, paper notebook, whiteboard, voice memos — pick one and route everything through it. The cognitive load of choosing where to capture is itself working-memory tax."},
            {"name": "Body-double for task initiation", "body": "Find another person to work alongside. In person, on video, or via async tools like FocusMate. The mechanism: the presence of another nervous system anchors you to the task. Doesn't have to be related to your task; doesn't even have to be conversational. The activation is the active ingredient. For routine task initiation (e.g., chore start), even a video call to a friend who's also doing chores works.", "tip": "If body-doubling isn't socially available, the next-best is environmental: a designated work location, a specific chair, a specific browser profile. Environment functions as silent body-double over time."},
            {"name": "Pre-commit decisions — reduce in-the-moment cognitive load", "body": "Decision-making depletes EF capacity. Pre-commit anything you can: same outfit on workdays, same breakfast, same morning sequence, the meeting agenda before you walk in, the scope of work before you start, the time you'll stop. Implementation intentions (\"if X, then Y\") encode pre-commitment in a form the brain can execute without re-deciding. d = 0.65 effect size from the meta-analytic literature.", "tip": "Pre-commitment is the FASD Magic Key 6 (\"Simplify\") and the Self-Care non-negotiable #4 (implementation intentions) intersected. Same mechanism. Different domain."},
            {"name": "Build redundant safety nets — assume the system will fail", "body": "Even good scaffolding fails sometimes. Build redundancy: phone alarm + visual reminder + accountability text from a friend. Calendar block + physical note on the door + the activity scheduled with someone else who's expecting you. Single-point-of-failure scaffolding will fail; redundant scaffolding will catch the failures. The medication-decision framework's tracking sheet is one example; the IEP/504 paper trail is another. Assume any single piece of structure will collapse under load and design accordingly.", "tip": "Don't design scaffolding to work on your best days. Design it to work on your worst day. The day you forgot to charge your phone, the day the alarm didn't go off, the day you were too depleted to check the calendar. Redundancy is what makes the system survive bad days."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Use it as the diagnostic the next time something falls through. Which scaffolding wasn't in place — and which redundant layer should be added.",
        "printable_card": {
            "title": "EXECUTIVE FUNCTION SCAFFOLDING",
            "subtitle": "Survival Blueprint + Invisible Disability",
            "items": [
                {"num": "01 · EXTERNALIZE TIME — VISUAL", "text": "Time Timer. Calendar blocks. 15-min advance alarms.", "help": "Numerical time doesn't register; visual does."},
                {"num": "02 · EXTERNALIZE WORKING MEMORY", "text": "Write everything. One capture system, not five.", "help": "\"I'll remember\" is the most expensive sentence."},
                {"num": "03 · BODY-DOUBLE — TASK INITIATION", "text": "Work alongside someone. In person, video, FocusMate.", "help": "Presence anchors. Activation borrowed."},
                {"num": "04 · PRE-COMMIT DECISIONS", "text": "Same outfit, breakfast, sequence. Implementation intentions.", "help": "If [trigger], then [behavior]. d = 0.65."},
                {"num": "05 · REDUNDANT SAFETY NETS", "text": "Assume failure. Build for worst day, not best.", "help": "Single-point-of-failure scaffolding will fail."},
            ],
        },
        "exits": [
            {"tag": "Full guide · $17.99", "tag_class": "", "url": SB_GUMROAD, "title": "The Survival Blueprint", "body": "Survival Blueprint Ch. 2 covers the executive function toolkit for ages 5-12; Ch. 3 covers ages 13-15; Ch. 4 covers ages 15-18 and transition to supported adulthood. The same scaffolding principles, applied developmentally.", "cta": "Read the guide →"},
            {"tag": "Full guide · $44.99+", "tag_class": "free", "url": ID_GUMROAD, "title": "The Invisible Disability", "body": "Chapter 4 (8 Magic Keys) is the fullest published account of executive function scaffolding for the FASD population — applicable framework with the strongest evidence base across ND profiles.", "cta": "Read the guide →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-ef-scaffolding-newsletter",
        "subscribe_source": "source-wiki-ef-scaffolding",
        "sources_intro": "All claims on this page are sourced from <em>The Survival Blueprint</em> (Ch. 2) and <em>The Invisible Disability</em> (Ch. 4). Primary sources cited:",
        "sources_list": [
            "Barkley, R. A. (2012). <em>Executive Functions: What They Are, How They Work, and Why They Evolved.</em> Foundational on EF as a multi-component cluster, not a single skill.",
            "Gollwitzer, P. M. & Sheeran, P. (2006). Implementation intentions and goal achievement: a meta-analysis. d = 0.65 effect size.",
            "Survival Blueprint Ch. 2 — body doubling (FocusMate), executive function toolkit; Invisible Disability Ch. 4 — 8 Magic Keys as the lifelong accommodation framework.",
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
    print(f"\nAll {len(PAGES)} cross-pillar pages generated.")


if __name__ == "__main__":
    main()
