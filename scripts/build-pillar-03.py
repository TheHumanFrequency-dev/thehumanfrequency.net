#!/usr/bin/env python3
"""build-pillar-03.py — Difficult Conversations surface (6 pages)."""
import json, subprocess
from pathlib import Path

ROOT = Path("/sessions/friendly-beautiful-ritchie/mnt/thehumanfrequency.net")
GENERATOR = ROOT / "scripts" / "generate-wiki-page.py"
CONTENT_DIR = ROOT / "scripts" / "wiki-content"
OUTPUT_DIR = ROOT / "human-os"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

DC_GUMROAD = "https://thehumanfrequency.gumroad.com"  # DC playbook on store
SHOW_LINK = "/thf-podcast"

EXIT_SHOW = {
    "tag": "Show · Coming soon", "tag_class": "community", "url": SHOW_LINK,
    "title": "The Live Show",
    "body": "A live call-in show on the topics this wiki covers — unscripted, judgment-free, ordinary people, extraordinary stories. Join the waitlist for the launch.",
    "cta": "Get on the list →",
}

def dc_book_exit(body):
    return {
        "tag": "Full guide · See store", "tag_class": "", "url": DC_GUMROAD,
        "title": "The Difficult Conversations Playbook",
        "body": body,
        "cta": "Read the playbook →",
    }

PAGES = [
    # ─── Page 18: SCARF Threat Audit ────────────────────────────────────
    {
        "slug": "scarf-threat-audit",
        "page_num": "18",
        "title": "SCARF Threat Audit OS",
        "title_pre_words": "SCARF",
        "title_grad_word": "THREAT AUDIT",
        "pillar": "UNDERSTANDING EACH OTHER",
        "thesis": "Five social domains your brain treats as survival-level threats: Status, Certainty, Autonomy, Relatedness, Fairness. The 5-minute audit before any difficult conversation that names which threats you're walking into — and which to defuse first.",
        "reading_time": "8 min read",
        "last_updated": "May 2026",
        "source_chapter": "Difficult Conversations, Ch. 3",
        "date_published": "2026-05-01",
        "meta_description": "The SCARF Model — Status, Certainty, Autonomy, Relatedness, Fairness. The 5-minute pre-conversation threat audit. Sourced from Difficult Conversations Ch. 3.",
        "og_description": "Five social domains your brain treats as threats. The 5-minute audit before any difficult conversation.",
        "twitter_description": "SCARF: Status, Certainty, Autonomy, Relatedness, Fairness. The 5-minute audit.",
        "schema_keywords": "SCARF model, David Rock, social threat, conflict preparation, neuroscience of leadership, difficult conversation",
        "pull_quote": {
            "text": "The brain processes social threats with the same neural circuitry as physical threats. SCARF — Status, Certainty, Autonomy, Relatedness, Fairness — names the five domains your nervous system is bracing for.",
            "cite": "— Difficult Conversations Playbook, Chapter 3 (after David Rock, 2008)",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're walking into a performance review, a salary conversation, a relationship talk, or any other interaction where your nervous system is firing before the meeting starts. Your usual move is to script the words you'll say. But the words aren't the problem. The problem is that your body is bracing for something specific — and you don't know what."},
            {"type": "p", "text": "The SCARF Threat Audit is a 5-minute pre-conversation tool that surfaces what your brain is actually bracing for. It doesn't change the conversation. It changes how you walk in. Knowing that you're primarily bracing for a Status threat (vs. a Fairness threat, vs. an Autonomy threat) tells you which threat to defuse first — both for yourself and for the person across from you."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Two things make SCARF more useful than generic conflict-preparation advice."},
            {"type": "p_bold_lead", "lead": "Different threats need different responses.", "rest": "A Status threat (\"this person is going to dismiss my expertise\") is defused by being asked your view, given recognition, or invited to demonstrate competence. A Certainty threat (\"I don't know what's about to happen\") is defused by clear agendas, transparent timelines, and explicit naming of next steps. A generic \"stay calm\" approach won't address either one. The SCARF model lets you target the specific threat with the specific antidote."},
            {"type": "p_bold_lead", "lead": "The same neural circuitry as physical threat.", "rest": "Eisenberger and Lieberman's foundational research showed that social pain and physical pain share the same neural substrate (anterior cingulate cortex, anterior insula). \"It hurts\" is not a metaphor when someone undermines your status or excludes you. SCARF gives names to the five social inputs that hit that circuitry hardest."},
            {"type": "stat_box", "label": "THE FIVE DOMAINS", "figure": "Status · Certainty · Autonomy · Relatedness · Fairness", "cite": "David Rock (2008), <em>NeuroLeadership Journal.</em> Cited and operationalized in Difficult Conversations Ch. 3 — each domain is a discrete threat detection system in the brain; each can be triggered or defused independently."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. Run it 5-15 minutes before any conversation where the stakes feel high."},
        ],
        "steps": [
            {"name": "Status — what's at stake for relative importance?", "body": "Status is your perceived rank or expertise relative to others. Threatened by criticism, unsolicited advice, public correction, or being ignored. Ask: Is this conversation likely to threaten my status? Whose status is the other person worried about? In a performance review, the employee's status is at stake. In a salary negotiation, both parties' status. Note the status dynamic explicitly before walking in.", "tip": "Defusing a status threat: lead with recognition (\"I want to start by acknowledging the work you did on X\"). Asking for someone's view explicitly bolsters status; correcting someone in front of others crashes it."},
            {"name": "Certainty — what's the unknown?", "body": "Certainty is your ability to predict what happens next. Threatened by ambiguity, sudden changes, and undefined timelines. Ask: What does the other person not know about how this conversation will go? What don't I know? Naming the agenda and the timeline up front (\"I want to talk about three things; this should take 20 minutes\") often does more to lower the threat response than any specific words inside the conversation.", "tip": "If you can't be certain about the outcome, be certain about the process. \"I don't know what we'll decide today, but I want us to leave knowing what we'll do by Friday\" defuses certainty without false promises."},
            {"name": "Autonomy — where's the control?", "body": "Autonomy is your sense of choice over events affecting you. Threatened by micromanagement, being told what to do without input, or having decisions made about you without consultation. Ask: Will this conversation reduce someone's sense of choice? Can I find one place to give the other person genuine agency, even if the broader decision isn't theirs to make?", "tip": "Even small autonomy preservation matters: \"Would you prefer to talk now or after lunch?\" \"Which of these two approaches would work better for you?\" The choice doesn't have to be over the substance to register."},
            {"name": "Relatedness — are we still on the same team?", "body": "Relatedness is your sense of belonging and safety with the other person. Threatened by exclusion, in-group/out-group framing, or perceived betrayal. Ask: Will the structure of this conversation feel adversarial? What signals can I send that we are still allies even if we disagree on this specific issue?", "tip": "Use \"we\" language and shared goals when you can. \"We need to figure out how to make this work\" lands very differently from \"You need to figure out how to fix this.\" Same content, opposite Relatedness signal."},
            {"name": "Fairness — is the process equitable?", "body": "Fairness is your sense of equitable treatment. Threatened by favoritism, opaque processes, or rules applied inconsistently. Ask: Will the other person feel they're being treated by the same standards as everyone else? Can I make the process visible? Naming the criteria you're using (\"the same metrics we apply to all reviews\") defuses fairness anxiety even when the outcome is unwelcome.", "tip": "Fairness is the threat most often missed by managers. \"Why is X getting Y and I'm not?\" is a Fairness signal, not a Status one — and the fix is process transparency, not a defense of your decision."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Run the audit on the index card 5-15 minutes before any conversation where the stakes feel high. The naming is the work.",
        "printable_card": {
            "title": "SCARF THREAT AUDIT · 5 MIN",
            "subtitle": "After Rock 2008 — DC Playbook Ch. 3",
            "items": [
                {"num": "01 · STATUS", "text": "Whose relative importance is at stake? Recognition defuses.", "help": "Public correction crashes it. Asking views bolsters it."},
                {"num": "02 · CERTAINTY", "text": "What's the unknown? Name the agenda and timeline up front.", "help": "Be certain about process if you can't be about outcome."},
                {"num": "03 · AUTONOMY", "text": "Where's the choice? Find one place to grant genuine agency.", "help": "\"Now or after lunch?\" works."},
                {"num": "04 · RELATEDNESS", "text": "Are we still on the same team? Use \"we\" language.", "help": "\"We need to figure this out,\" not \"you need to.\""},
                {"num": "05 · FAIRNESS", "text": "Is the process equitable? Make the criteria visible.", "help": "\"The same metrics we apply to all reviews.\""},
            ],
        },
        "exits": [
            dc_book_exit("Chapter 3 covers SCARF in clinical detail with the full neuroscience, the threat/reward matrix, and worked examples for performance reviews, project conflicts, and team retros. Plus Chapters 4-5 on conducting the conversation itself."),
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/polyvagal-repair", "title": "Polyvagal Repair OS", "body": "When the audit fails and the conversation triggers nervous-system shutdown, the next page covers what to do — three steps, in order.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-scarf-newsletter",
        "subscribe_source": "source-wiki-scarf",
        "sources_intro": "All claims on this page are sourced from <em>The Difficult Conversations Playbook</em>, Chapter 3. Primary sources cited:",
        "sources_list": [
            "Rock, D. (2008). SCARF: A brain-based model for collaborating with and influencing others. <em>NeuroLeadership Journal.</em>",
            "Eisenberger, N. I. & Lieberman, M. D. (2004). Why rejection hurts: a common neural alarm system for physical and social pain. <em>Trends in Cognitive Sciences.</em>",
            "Difficult Conversations Playbook Ch. 3 — SCARF operationalized for difficult workplace conversations.",
        ],
        "sources_outro": "",
    },

    # ─── Page 19: Polyvagal Repair ──────────────────────────────────────
    {
        "slug": "polyvagal-repair",
        "page_num": "19",
        "title": "Polyvagal Repair OS",
        "title_pre_words": "POLYVAGAL",
        "title_grad_word": "REPAIR OS",
        "pillar": "UNDERSTANDING EACH OTHER",
        "thesis": "When a conversation has triggered nervous-system shutdown — yours or theirs — words are not the lever. The body is. The three-step protocol that engages ventral vagal safety signals and reopens connection.",
        "reading_time": "8 min read",
        "last_updated": "May 2026",
        "source_chapter": "Difficult Conversations, Ch. 2",
        "date_published": "2026-05-01",
        "meta_description": "Polyvagal Theory applied to conflict repair. The three-step protocol — co-regulate the body, project safety, then re-engage. Sourced from Difficult Conversations Ch. 2 (after Porges).",
        "og_description": "When conversations shut down, words don't fix it. The body does. The polyvagal repair protocol.",
        "twitter_description": "When conversations shut down, words don't fix it. The body does.",
        "schema_keywords": "polyvagal theory, Stephen Porges, ventral vagal, conflict repair, neuroception, difficult conversation",
        "pull_quote": {
            "text": "Effective conflict resolution requires you to actively project cues of safety — maintaining an open posture, softening your eyes, speaking in a calm, melodic tone — to intentionally activate your counterpart's ventral vagal state. You are not just managing words; you are managing nervous systems.",
            "cite": "— Difficult Conversations Playbook, Chapter 2 (after Porges)",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "The conversation was going well until it wasn't. Something landed wrong. Now the other person has gone silent, eyes down, voice flat. Or they've gone the other direction — voice raised, body forward, the words coming faster than they can process. You feel your own chest tighten. You try to repeat your point more clearly. They go further into shutdown or escalation. Words have stopped working."},
            {"type": "p", "text": "What just happened is a polyvagal state shift. Stephen Porges's Polyvagal Theory describes three neural circuits that govern how the body responds to perceived safety or threat. When the conversation triggered enough threat, one of you (or both) dropped out of ventral vagal — the social engagement circuit where calm, rational conversation happens — and into either sympathetic (fight/flight) or dorsal vagal (shutdown). Below ventral vagal, words are not the lever. The body is."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three concepts make polyvagal repair work."},
            {"type": "p_bold_lead", "lead": "Three circuits, three states.", "rest": "Ventral vagal: connected, curious, open, capable of empathy and disagreement. Sympathetic: mobilized, raised voice, rapid argumentation, rigid body. Dorsal vagal: collapsed, withdrawn, silent, dissociated. Successful conversation happens in ventral vagal. The first job of repair is getting both nervous systems back there."},
            {"type": "p_bold_lead", "lead": "Neuroception is automatic.", "rest": "Porges's term for the subconscious threat-scanning that runs constantly underneath your awareness. You read someone's micro-expression, sigh, or vocal tone before you finish processing their words. Most conversations escalate not because of what was said but because of what neuroception detected. Repair requires sending different cues, not arguing better."},
            {"type": "p_bold_lead", "lead": "Co-regulation outperforms self-regulation.", "rest": "When one nervous system in a dyad is regulated, it pulls the other toward regulation. The DC Playbook is explicit: \"You are not just managing words; you are managing nervous systems.\" Your tone, posture, breath, and eye contact are sending signals into your counterpart's neuroception in real time. Lead with your body, then with your words."},
            {"type": "stat_box", "label": "THE THREE STATES", "figure": "Ventral · Sympathetic · Dorsal — words only work in ventral", "cite": "Porges, S. W. (2011), <em>The Polyvagal Theory.</em> Operationalized in Difficult Conversations Ch. 2 — words are processed differently in each autonomic state; conflict resolution requires the conversation to happen in ventral vagal."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. The first three are your own regulation; the last two are co-regulation back into shared ventral vagal."},
        ],
        "steps": [
            {"name": "Notice the shift — yours and theirs", "body": "The pause is the protocol. Before saying anything else, scan: where are you on the autonomic ladder? Where is the other person? Sympathetic shows in raised voice, fast speech, forward posture, narrowed eyes. Dorsal vagal shows in silence, downward gaze, monotone voice, withdrawn body. Ventral vagal shows in open eyes, melodic vocal range, present body. If either of you is out of ventral, do not press the substantive point.", "tip": "If you notice you've shifted into sympathetic before they have, that's information you can use. Slow your breath, drop your shoulders, soften your eyes — your body changing first often pulls theirs along."},
            {"name": "Regulate your own body first", "body": "Three slow exhales. Drop your shoulders explicitly. Soften your jaw and eyes. Open your hands if they were clenched or pointing. The body cues you send out are read by their neuroception in seconds. Trying to verbally calm someone whose nervous system is reading your tense body as threat is a contradiction the body wins.", "tip": "If you can, sit down. If you're already sitting, lean back slightly. Vertical drop in your physical position is a strong safety signal — it's the opposite of the predator stance."},
            {"name": "Project safety — tone, eyes, prosody", "body": "Speak slower than you want to. Drop your pitch. Use what Porges calls \"prosodic vocal range\" — the melodic, slightly singsong quality of safe human speech. Maintain soft eye contact (not staring; the difference matters). Acknowledge that something has shifted: \"I notice this got hard. I want to slow down for a second.\" The acknowledgment itself is a safety cue.", "tip": "Avoid the \"calm voice that sounds patronizing\" trap. The difference is genuineness — you are actually calming, not performing calm at them."},
            {"name": "Name the state, offer the pause", "body": "If they're still not back in ventral, name what's happening explicitly without diagnosing them: \"I think we're both pretty activated right now. Would it help to take five minutes and come back?\" The pause is a tool, not a defeat. Coming back five minutes later in ventral vagal accomplishes more than another 30 minutes of escalating attempts to push through.", "tip": "If they don't want a pause, don't force it. Stay with the conversation but at a much slower pace. Your continued ventral presence may pull them back without an explicit break."},
            {"name": "Reconnect before re-engaging the substance", "body": "Before returning to the disagreement, send one signal of relatedness: \"We're on the same side here.\" \"I want this to work for both of us.\" \"I'm not trying to win this; I'm trying to understand what's actually true.\" Even one sentence of explicit relatedness usually opens the door back to ventral. Then, and only then, return to the substance — slower, smaller bites.", "tip": "If after all five steps you're still not back in ventral as a pair, the conversation is over for today. Schedule the next attempt explicitly. \"Let's come back to this Thursday\" is a better outcome than continuing past the point where words work."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Stick it on the back of your office door, the bathroom mirror, the inside of your laptop case. Use it before re-entering the conversation, not in the middle of escalation.",
        "printable_card": {
            "title": "POLYVAGAL REPAIR · 5 STEPS",
            "subtitle": "Porges · DC Playbook Ch. 2",
            "items": [
                {"num": "01 · NOTICE THE SHIFT", "text": "Where are you on the ladder? Where are they?", "help": "Sympathetic = mobilized. Dorsal = shutdown. Don't press in either."},
                {"num": "02 · REGULATE YOUR BODY FIRST", "text": "Three slow exhales. Drop shoulders. Soften jaw + eyes. Open hands.", "help": "Body cues land in their neuroception in seconds."},
                {"num": "03 · PROJECT SAFETY — TONE + EYES", "text": "Slower speech. Lower pitch. Prosodic range. Soft eyes.", "help": "Genuine, not performed."},
                {"num": "04 · NAME + OFFER PAUSE", "text": "\"I think we're both pretty activated. Want to take five?\"", "help": "Pause is a tool, not a defeat."},
                {"num": "05 · RECONNECT FIRST", "text": "\"We're on the same side here.\" Then return to substance.", "help": "Relatedness signal opens the door back to ventral."},
            ],
        },
        "exits": [
            dc_book_exit("Chapter 2 covers Polyvagal Theory in clinical detail — the three neural circuits, neuroception, the autonomic ladder, and worked examples of state shifts in real workplace conflicts. Plus the Polyvagal Self-Map exercise."),
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/scarf-threat-audit", "title": "SCARF Threat Audit OS", "body": "Polyvagal repair handles state. SCARF handles the specific social threat that triggered the state in the first place. Use them together.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-polyvagal-newsletter",
        "subscribe_source": "source-wiki-polyvagal",
        "sources_intro": "All claims on this page are sourced from <em>The Difficult Conversations Playbook</em>, Chapter 2. Primary sources cited:",
        "sources_list": [
            "Porges, S. W. (2011). <em>The Polyvagal Theory: Neurophysiological Foundations of Emotions, Attachment, Communication, and Self-Regulation.</em>",
            "Dana, D. (2018). <em>The Polyvagal Theory in Therapy.</em> The autonomic ladder framework.",
            "Difficult Conversations Playbook Ch. 2 — Polyvagal Theory operationalized for conflict repair.",
        ],
        "sources_outro": "",
    },

    # ─── Page 20: Harvard 4-Step ────────────────────────────────────────
    {
        "slug": "harvard-method",
        "page_num": "20",
        "title": "Harvard Method 4-Step OS",
        "title_pre_words": "HARVARD METHOD",
        "title_grad_word": "4-STEP OS",
        "pillar": "UNDERSTANDING EACH OTHER",
        "thesis": "The framework that ended the Apple-Samsung patent war. Four pillars of principled negotiation: separate people from problems, focus on interests not positions, generate options for mutual gain, insist on objective criteria. Plus your BATNA — the strongest negotiation lever you have.",
        "reading_time": "8 min read",
        "last_updated": "May 2026",
        "source_chapter": "Difficult Conversations, Ch. 7",
        "date_published": "2026-05-01",
        "meta_description": "The Harvard Method 4-step principled negotiation framework. Plus BATNA — your walk-away power. Sourced from Difficult Conversations Ch. 7 (after Fisher & Ury).",
        "og_description": "Four pillars of principled negotiation. The framework that ended Apple-Samsung.",
        "twitter_description": "Four pillars of principled negotiation. Plus BATNA. The Harvard Method.",
        "schema_keywords": "Harvard negotiation, Fisher Ury, principled negotiation, BATNA, interests vs positions, Getting to Yes",
        "pull_quote": {
            "text": "Seemingly incompatible positions often mask highly compatible needs. A position is 'I won't pay more than $50,000.' An interest is 'I need to keep operational costs under a ceiling to avoid layoffs.' Find the interest, find the deal.",
            "cite": "— Difficult Conversations Playbook, Chapter 7 (after Fisher & Ury, 1981)",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're walking into a negotiation. Salary, contract, vendor terms, a co-founder split, a divorce. The instinct is to figure out your number and hold the line. The other side has done the same. Two opening positions, fifty miles apart. Hours of grinding back and forth. Either someone caves and resents it, or no deal happens and the relationship corrodes."},
            {"type": "p", "text": "Most negotiations get stuck because both sides are arguing positions. The Harvard Method, codified by Roger Fisher and William Ury in <em>Getting to Yes</em> and operationalized in Difficult Conversations Ch. 7, gives you four principles that move every conversation off positions and onto interests — where deals actually live."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things make principled negotiation outperform positional bargaining."},
            {"type": "p_bold_lead", "lead": "Positions hide interests.", "rest": "A position is the specific outcome you're demanding. An interest is the underlying need that produced the demand. \"I want $145K\" is a position. \"I want to feel that my contribution is valued, and I need to cover daycare and my mortgage\" is the interest. Two parties' positions can be incompatible while their interests overlap dramatically. Move the conversation to interests and the deal space expands."},
            {"type": "p_bold_lead", "lead": "BATNA is your real leverage.", "rest": "BATNA — Best Alternative to a Negotiated Agreement — is your fallback if this negotiation fails. A strong BATNA gives you confidence and options; a weak BATNA leaves you stuck accepting bad terms. Define your BATNA before any meaningful negotiation. The strength of your BATNA is the actual lever, not your tone or your tactics."},
            {"type": "p_bold_lead", "lead": "Objective criteria short-circuit ego.", "rest": "Anchoring agreements to external standards — market data, industry benchmarks, legal precedent, comparable transactions — converts \"my will vs. your will\" into \"what does the data say.\" When both parties anchor to the same criteria, the conversation becomes about interpretation, not power."},
            {"type": "stat_box", "label": "THE FRAMEWORK", "figure": "4 pillars + BATNA · used in Apple-Samsung settlement", "cite": "Fisher, R. & Ury, W. (1981), <em>Getting to Yes</em>; operationalized in DC Playbook Ch. 7. Used in the Apple-Samsung patent settlement that ended years of multi-jurisdiction litigation."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. The four Harvard pillars + the BATNA preparation that has to happen before you walk in."},
        ],
        "steps": [
            {"name": "Define your BATNA — before the meeting", "body": "Write down explicitly: what is my best alternative if this negotiation completely fails? Other job offers? Other vendors? Walking away entirely? The strength of your BATNA determines your true negotiation power. If your BATNA is weak, take time to strengthen it before negotiating — find another offer, build a parallel option, demonstrate you have alternatives. Walking in with a weak undefined BATNA is the most common failure mode in negotiation.", "tip": "Estimate the other side's BATNA too. Their fallback determines how flexible they really are, regardless of what they say in the room."},
            {"name": "Separate the people from the problem", "body": "View yourselves as collaborators attacking a mutual problem, not adversaries attacking each other. Address the factual summit of the dispute while remaining empathetic to the emotional dynamics beneath. Practically: name the relational frame at the top of the conversation. \"I want us both to leave this conversation feeling we worked it out together.\" Even one sentence resets the adversarial default.", "tip": "When the other side becomes hostile, don't match it. Hard on the problem, soft on the person — you can disagree forcefully on the substance while protecting the relationship."},
            {"name": "Focus on interests, not positions", "body": "Ask why behind every position. Why do you need $145K specifically? Why is the deadline non-negotiable? Why must the contract include this clause? Each \"why\" surfaces an interest. Name your own interests too — they're often less rigid than your position. Interests overlap. Positions don't.", "tip": "If the other side won't reveal their interests, propose them tentatively: \"It sounds like the deadline matters because the board meets that week — am I reading that right?\" Wrong guesses get corrected, which is also useful."},
            {"name": "Generate options for mutual gain", "body": "Before deciding, brainstorm. Suspend judgment. \"Enlarge the pie before dividing it.\" If salary is fixed, what about signing bonus, equity, PTO, professional development budget, flexible hours, defined performance review timeline? If price is fixed, what about payment terms, scope, exclusivity, warranty? Most negotiations leave value on the table because options are generated only after positions have hardened.", "tip": "The brainstorm has to happen before commitment. \"Let's spend ten minutes naming options before we evaluate any of them\" is an explicit rule that protects creativity from premature judgment."},
            {"name": "Insist on objective criteria", "body": "Anchor to market benchmarks, legal precedent, industry standards, comparable transactions. \"For directors with my track record in this region, comp typically ranges from $130K to $145K\" is more powerful than \"I want $140K.\" When both parties commit to objective criteria, the negotiation moves from will vs. will to interpretation of evidence. The party with the stronger evidence usually wins; both parties usually feel the process was fair.", "tip": "If the other side rejects your criteria, propose theirs. \"What benchmarks would you find credible?\" Forces them to either propose objective criteria or admit they have none."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Run it before any negotiation where the dollar amount or stakes feel high. The 5-minute prep matters more than the words you'll say in the room.",
        "printable_card": {
            "title": "HARVARD METHOD · 4 PILLARS + BATNA",
            "subtitle": "Fisher & Ury · DC Playbook Ch. 7",
            "items": [
                {"num": "01 · DEFINE BATNA — BEFORE", "text": "Best alternative if this fails. Strengthen it before you negotiate.", "help": "Estimate theirs too."},
                {"num": "02 · SEPARATE PEOPLE FROM PROBLEM", "text": "Collaborators attacking a mutual problem.", "help": "Hard on the problem, soft on the person."},
                {"num": "03 · INTERESTS, NOT POSITIONS", "text": "Ask \"why\" behind every demand. Yours and theirs.", "help": "Interests overlap. Positions don't."},
                {"num": "04 · GENERATE OPTIONS — BEFORE DECIDING", "text": "Brainstorm. Suspend judgment. Enlarge the pie.", "help": "10 minutes of generation before any evaluation."},
                {"num": "05 · INSIST ON OBJECTIVE CRITERIA", "text": "Market data, precedent, benchmarks. Mutual evidence.", "help": "If they reject yours, ask what they'd find credible."},
            ],
        },
        "exits": [
            dc_book_exit("Chapter 7 covers the full Harvard Method with the Apple-Samsung and Starbucks-Kraft case studies, the Principled Negotiation Preparation Workbook, and worked examples for salary, contract, and dispute negotiations. Chapter 12 is the salary-specific application."),
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/salary-negotiation", "title": "Salary Negotiation OS", "body": "The Harvard Method applied specifically to compensation conversations. With three negotiation scripts (Value Proposition, Pivot, Future Commitment).", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-harvard-newsletter",
        "subscribe_source": "source-wiki-harvard",
        "sources_intro": "All claims on this page are sourced from <em>The Difficult Conversations Playbook</em>, Chapter 7. Primary sources cited:",
        "sources_list": [
            "Fisher, R. & Ury, W. (1981/2011). <em>Getting to Yes: Negotiating Agreement Without Giving In.</em> The Harvard Negotiation Project's foundational text.",
            "Difficult Conversations Playbook Ch. 7 — Harvard Method operationalized; Apple-Samsung and Starbucks-Kraft case studies.",
            "Difficult Conversations Playbook Ch. 12 — Salary-specific application with three scripted frameworks.",
        ],
        "sources_outro": "",
    },

    # ─── Page 21: Gottman Repair Phrases ────────────────────────────────
    {
        "slug": "gottman-repair",
        "page_num": "21",
        "title": "Gottman Repair Phrases OS",
        "title_pre_words": "GOTTMAN",
        "title_grad_word": "REPAIR",
        "pillar": "UNDERSTANDING EACH OTHER",
        "thesis": "John Gottman's research predicts relationship dissolution with 93% accuracy — by counting repair attempts. The Four Horsemen, their antidotes, and three repair phrases you can use in any escalating conversation. Critical rule: the repair attempt must NEVER be followed by \"but.\"",
        "reading_time": "7 min read",
        "last_updated": "May 2026",
        "source_chapter": "Difficult Conversations, Ch. 10",
        "date_published": "2026-05-01",
        "meta_description": "The Four Horsemen of conversation breakdown — Criticism, Contempt, Defensiveness, Stonewalling — and their antidotes. Plus three repair phrases that prevent escalation. Sourced from DC Ch. 10 (Gottman).",
        "og_description": "Gottman predicts relationship dissolution with 93% accuracy. The Four Horsemen and their antidotes.",
        "twitter_description": "Four Horsemen, four antidotes, three repair phrases. Gottman.",
        "schema_keywords": "Gottman, four horsemen, repair attempts, criticism contempt defensiveness stonewalling, relationship repair",
        "pull_quote": {
            "text": "An effective repair attempt must NEVER be followed by the word 'but.' Saying 'I apologize for my tone, but you started it' instantly invalidates the accountability and re-triggers defensiveness. The repair must stand alone.",
            "cite": "— Difficult Conversations Playbook, Chapter 10 (after Gottman)",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "The conversation has tipped. Someone said something sharp. Someone else got defensive. Now the original substance is gone and you're arguing about how the other person is being unreasonable. By the time you both walk away, no one remembers what started it — but the resentment is real, and it's going to compound the next time the topic comes up."},
            {"type": "p", "text": "John Gottman spent decades watching couples have these conversations on video. His research identified four specific patterns — what he calls the Four Horsemen — that, when present in regular conversation, predict relationship dissolution with 93% accuracy. He also identified the antidote to each, and the structure of repair attempts that successful long-term partners use to interrupt the spiral."},
            {"type": "p", "text": "This page operationalizes that work for any difficult conversation — partner, family, friend, colleague. The Four Horsemen, their antidotes, and three repair phrases that work."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things drive the framework."},
            {"type": "p_bold_lead", "lead": "Patterns predict dissolution, not specific arguments.", "rest": "Gottman's research found that the content of fights matters far less than the patterns. Couples who fought constantly but maintained repair attempts and avoided contempt stayed together. Couples who rarely fought but slipped into the Four Horsemen patterns dissolved. The pattern is the variable; the topic is incidental."},
            {"type": "p_bold_lead", "lead": "Each horseman has a specific antidote.", "rest": "Criticism (attacking character) → \"I\" statements about specific behavior. Contempt (superiority, mockery) → genuine appreciation, building a culture of respect. Defensiveness (counter-attacking) → taking responsibility for even a small part. Stonewalling (emotional withdrawal) → physiological self-soothing and a tactical pause. Wrong horseman, wrong antidote — generic \"be nicer\" advice doesn't work."},
            {"type": "p_bold_lead", "lead": "Repair attempts are protective even when imperfect.", "rest": "What separates durable relationships from dissolving ones is not the absence of conflict but the presence of repair attempts — small gestures, statements, or even humor that prevent negativity from cascading. A clumsy repair is better than no repair. The critical rule is that the repair cannot be followed by \"but\" — that one word converts the apology into a re-attack."},
            {"type": "stat_box", "label": "THE PREDICTIVE POWER", "figure": "93% accuracy predicting dissolution · across 14-year studies", "cite": "Gottman, J. M. (1994). <em>Why Marriages Succeed or Fail.</em> The pattern of Four Horsemen presence + repair attempt frequency predicts relationship outcomes with high reliability across long-term studies."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. The first four are spotting and applying the antidotes; the fifth is the repair-attempt phrase library."},
        ],
        "steps": [
            {"name": "Spot Criticism — apply the \"I\" statement antidote", "body": "Criticism attacks character: \"You always interrupt me — you don't care what I think.\" The antidote: an \"I\" statement focused on specific behavior. \"When I get interrupted, I lose my train of thought and I feel small. I need a few minutes to finish my point.\" Same content, different shape — and the partner can respond to the behavioral request without defending their character.", "tip": "If you catch yourself starting a sentence with \"You always\" or \"You never,\" stop. Restart with \"When [specific event] happens, I feel [specific feeling] because [specific reason].\""},
            {"name": "Spot Contempt — build a culture of appreciation", "body": "Contempt is superiority. Sarcasm, mockery, eye-rolling, name-calling, name-flavored sighs. It is the single strongest predictor of dissolution in Gottman's research. The antidote is structural, not tactical: build a daily practice of appreciation. Name specific things you appreciate, in real time, frequently. Contempt withers in a relationship saturated with genuine respect.", "tip": "If contempt has become a default in a relationship, the repair work is bigger than this page. Couples therapy is appropriate. The page-level move is naming when you've slipped into contempt and apologizing specifically for it."},
            {"name": "Spot Defensiveness — take responsibility for any small part", "body": "Defensiveness is counter-attack. \"You're saying I'm late? You were late yesterday too.\" The antidote: take responsibility for any piece of what they said, even a small one, before responding to the rest. \"You're right — I was 20 minutes late tonight, and that wasn't fair to you. The part about yesterday is more complicated, and I'd like to come back to that, but tonight I should have texted you.\"", "tip": "The micro-accountability has to be genuine. Fake \"I'm sorry, but\" doesn't work — see step 5. Find the real thing you're responsible for and own it before introducing your counter-information."},
            {"name": "Spot Stonewalling — request a tactical pause, not silence", "body": "Stonewalling is emotional withdrawal — going silent, refusing to engage, the wall going up. It usually signals physiological flooding. The antidote is not pushing through; it's a tactical pause with a return commitment. \"I'm getting overwhelmed and I'm going to shut down if I keep going. Can we take 30 minutes and come back at 8 PM?\" The pause + the return commitment together prevents stonewalling from becoming abandonment.", "tip": "If you find yourself wanting to stonewall, name it: \"I notice I want to go silent right now. I think I need 20 minutes.\" Naming what's happening preserves the relationship even when the conversation is paused."},
            {"name": "Three repair phrases — the library", "body": "Build a personal library of repair attempts that fit your authentic voice. Three durable templates: <strong>\"I think I came across wrong — can I try again?\"</strong> (interrupts your own escalation). <strong>\"We're on the same team here. Let's slow down.\"</strong> (relatedness signal + pace request). <strong>\"I can hear that I hurt you. I'm sorry. Can you tell me more about what landed?\"</strong> (validation + curiosity, with no \"but\"). Repair attempts must NEVER be followed by \"but.\" \"I apologize for my tone, but you started it\" instantly invalidates everything and re-triggers defensiveness.", "tip": "Practice repair phrases out loud during calm moments, not first time during conflict. The phrases that don't fit your natural voice will collapse under pressure. Edit them until they sound like you."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Stick it on the back of your phone case or inside your wallet. The next time a conversation tips, glance at it before responding.",
        "printable_card": {
            "title": "GOTTMAN REPAIR · 4 ANTIDOTES + 3 PHRASES",
            "subtitle": "DC Playbook Ch. 10",
            "items": [
                {"num": "01 · CRITICISM → \"I\" STATEMENT", "text": "Specific behavior, not character. \"When X, I feel Y because Z.\"", "help": "Not \"you always.\""},
                {"num": "02 · CONTEMPT → APPRECIATION", "text": "Build daily appreciation practice.", "help": "Strongest dissolution predictor — fix is structural."},
                {"num": "03 · DEFENSIVENESS → OWN A SMALL PART", "text": "Take responsibility for any piece before responding to the rest.", "help": "Genuine, not \"I'm sorry but.\""},
                {"num": "04 · STONEWALLING → TACTICAL PAUSE", "text": "\"I'm getting overwhelmed. 30 minutes, back at 8.\"", "help": "Pause + return commitment, not silence."},
                {"num": "05 · THREE REPAIR PHRASES — NEVER + \"BUT\"", "text": "\"Came across wrong — can I try again?\" / \"Same team. Slow down.\" / \"I hear I hurt you. Tell me more.\"", "help": "\"But\" instantly cancels the repair."},
            ],
        },
        "exits": [
            dc_book_exit("Chapter 10 covers the Gottman Method in clinical detail — the Four Horsemen, the antidotes, the Sound Relationship House framework, and the post-conflict processing protocol with three steps for genuine repair after the argument ceases."),
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/polyvagal-repair", "title": "Polyvagal Repair OS", "body": "Gottman handles the conversational pattern. Polyvagal handles the nervous system underneath it. Both are needed when conversations have tipped.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-gottman-newsletter",
        "subscribe_source": "source-wiki-gottman",
        "sources_intro": "All claims on this page are sourced from <em>The Difficult Conversations Playbook</em>, Chapter 10. Primary sources cited:",
        "sources_list": [
            "Gottman, J. M. & Silver, N. (1999). <em>The Seven Principles for Making Marriage Work.</em>",
            "Gottman, J. M. (1994). <em>Why Marriages Succeed or Fail.</em> The Four Horsemen and the 93% prediction accuracy across 14-year longitudinal studies.",
            "Difficult Conversations Playbook Ch. 10 — Gottman Method operationalized; Critical Rule on \"but\".",
        ],
        "sources_outro": "",
    },

    # ─── Page 22: Termination Conversation ──────────────────────────────
    {
        "slug": "termination-conversation",
        "page_num": "22",
        "title": "Termination Conversation OS",
        "title_pre_words": "TERMINATION",
        "title_grad_word": "CONVERSATION",
        "pillar": "UNDERSTANDING EACH OTHER",
        "thesis": "The hardest conversation in business — letting someone go with dignity, clarity, and legal precision. The pre-flight checklist, the first 30 seconds, and the things you must never say. Sourced from Difficult Conversations Ch. 13.",
        "reading_time": "8 min read",
        "last_updated": "May 2026",
        "source_chapter": "Difficult Conversations, Ch. 13",
        "date_published": "2026-05-01",
        "meta_description": "The protocol for compassionate, legally compliant termination conversations. Pre-flight checklist + the first 30 seconds + what never to say. Sourced from Difficult Conversations Ch. 13.",
        "og_description": "Letting someone go with dignity, clarity, and legal precision. The protocol.",
        "twitter_description": "Letting someone go with dignity. The protocol — first 30 seconds matter most.",
        "schema_keywords": "termination, firing employee, layoff, HR compliance, severance, WARN Act, Title VII",
        "pull_quote": {
            "text": "Termination conversations must balance profound human empathy with rigorous HR compliance. Be direct and clear within the first 2 minutes. Burying the message in small talk or compliments creates more harm, not less.",
            "cite": "— Difficult Conversations Playbook, Chapter 13",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You're about to end someone's job. Maybe a layoff. Maybe a performance termination. Maybe both. You've been carrying the weight for a week. You don't want to do this conversation. The instinct is to soften it — open with chitchat, lead with compliments, get to the point only after warming them up. That instinct is wrong. Every minute you delay the message is a minute they're processing false information about why they were called into your office."},
            {"type": "p", "text": "Compassionate termination is direct. The directness is the compassion. The Difficult Conversations Playbook Chapter 13 outlines the protocol used by HR professionals at scale — pre-flight checklist, first 30 seconds, what to say and what to never say, and how to manage \"survivor syndrome\" in the team that remains."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things govern the protocol."},
            {"type": "p_bold_lead", "lead": "Documentation prevents legal exposure.", "rest": "Before any termination — especially performance-based — verify that a comprehensive documentation trail exists: PIPs, attendance records, disciplinary warnings, dated. Without it, the company is exposed to discrimination claims under Title VII, WARN Act violations, and OWBPA non-compliance. Documentation is the protective layer; if it doesn't exist yet, the termination is premature."},
            {"type": "p_bold_lead", "lead": "Directness is kindness.", "rest": "Burying the message in small talk creates false hope and prolongs the trauma. The standard is: be direct and clear within the first 2 minutes. The person knows something is up the moment you call them in. Stretching it for 10 minutes of preamble is not gentle — it's cruel."},
            {"type": "p_bold_lead", "lead": "Logistics + dignity in equal measure.", "rest": "After the message, the conversation pivots to logistics: severance, benefits, return of equipment, reference policy, transition support. Each of these is a place to preserve dignity — or to compound the injury. Have all the documents prepared in advance. Don't make promises about future rehire. Don't let the meeting happen on a Friday afternoon."},
            {"type": "stat_box", "label": "THE STANDARD", "figure": "Direct in 2 minutes · prepared documents · early in the workweek", "cite": "DC Playbook Ch. 13 — Title VII / WARN Act / OWBPA compliance baseline; Friday-afternoon terminations leave the person without HR support over the weekend and predict worse outcomes."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. The first three are pre-meeting; the last two are the meeting itself and what comes after."},
        ],
        "steps": [
            {"name": "Pre-flight checklist — before scheduling", "body": "Verify each item before you put the meeting on the calendar: documentation trail complete (PIPs, warnings, attendance — all dated). Legal/HR has reviewed. Severance prepared and approved. Private location secured (not a glass-walled conference room). Survivor communication plan drafted. Witnesses identified (HR partner is standard). If any item is missing, do not schedule — fix the gap first.", "tip": "If this is a performance termination and the documentation trail is thin, you don't have a termination — you have a PIP. Initiate the PIP with proper documentation; revisit the termination question in 30-60 days."},
            {"name": "Schedule it correctly — early week, private", "body": "Early in the workweek (Tuesday-Wednesday is ideal), not Friday afternoon. Private location. Block 30-45 minutes minimum (you may need less, but never run short). Have the HR partner present. Have water and tissues available. Make sure the person can leave the building without walking through the team — and if they need to retrieve personal items, plan that explicitly.", "tip": "If the termination is part of a layoff, schedule all the conversations on the same day, not staggered. The team finding out one person at a time over a week creates worse anxiety than a single hard day."},
            {"name": "First 30 seconds — direct, prepared, unambiguous", "body": "Open with the message. Three sentences, drafted in advance: <em>\"I have hard news. I'm letting you go effective today. I want to walk you through what happens next.\"</em> Or for layoff: <em>\"I have hard news. The company is making cuts and your role is being eliminated effective today. I want to walk you through what happens next.\"</em> Read it from notes if you need to. Do not soften the message. Do not couch it in praise. The directness is the dignity.", "tip": "After the message, stop talking. Let them respond. They may need 30 seconds to absorb. Don't fill the silence with explanations. Wait."},
            {"name": "Pivot to logistics — with humanity", "body": "Once they've absorbed the message, walk through the logistics calmly: severance amount and timing, benefits continuation (COBRA / equivalent), return of equipment, reference policy, outplacement support if offered. Have all documents ready. Sign nothing today. Hand them the packet to review with counsel of their choice. Make no promises about future rehire or specific reference language — those come from HR, in writing.", "tip": "If they ask \"why me?\" — and they often will — the answer is the same one in the documentation. Performance: \"the issues we discussed in the [date] PIP, [date] review, and [date] warning.\" Layoff: \"the role is being eliminated; this is not about your individual performance.\" Stick to the documented frame."},
            {"name": "After the meeting — survivor management + next steps", "body": "The team finding out tomorrow is the next conversation. \"Survivor syndrome\" — anxiety, lowered productivity, suspicion about future cuts — sets in if the announcement is opaque or delayed. Communicate transparently within 24 hours: who is gone, what role, what changes for remaining work. Do not share confidential personal details. Address the unstated question every survivor is asking: \"Am I next?\" — directly if you can. \"There are no further reductions planned\" if true; \"I'll communicate as soon as I have more information\" if uncertain.", "tip": "Survivors often want the departed person's contact info to send messages of support. Facilitate this — it's a dignity gesture that costs nothing and matters disproportionately to the person who just lost their job."},
        ],
        "after_steps_h2": "The printable: a wallet card",
        "after_steps_p": "Print this. Bring it to the pre-meeting prep. Do not bring it into the meeting itself.",
        "printable_card": {
            "title": "TERMINATION · 5-STEP PROTOCOL",
            "subtitle": "DC Playbook Ch. 13",
            "items": [
                {"num": "01 · PRE-FLIGHT CHECKLIST", "text": "Documentation, legal review, severance, private location, witnesses.", "help": "If anything is missing, don't schedule yet."},
                {"num": "02 · SCHEDULE EARLY WEEK", "text": "Tuesday-Wednesday. Private. 30-45 min block.", "help": "Not Friday afternoon. Not a glass-walled room."},
                {"num": "03 · FIRST 30 SECONDS — DIRECT", "text": "Three sentences, drafted in advance. Read if you must.", "help": "Don't soften. Don't preamble. The directness is the dignity."},
                {"num": "04 · PIVOT TO LOGISTICS — HUMANELY", "text": "Severance, benefits, equipment, reference policy. Documents ready.", "help": "Sign nothing today. No verbal promises about rehire/references."},
                {"num": "05 · MANAGE SURVIVORS WITHIN 24 HOURS", "text": "Transparent announcement. Address \"am I next?\" directly.", "help": "Survivor syndrome is the next risk. Manage it."},
            ],
        },
        "exits": [
            dc_book_exit("Chapter 13 covers compassionate termination in full clinical detail — the legal architecture (Title VII, WARN Act, OWBPA), the script library, survivor management protocols, and the post-termination 30-day checklist."),
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/scarf-threat-audit", "title": "SCARF Threat Audit OS", "body": "Run the SCARF audit before the termination meeting. Status, Certainty, Autonomy, Relatedness, Fairness — all five are firing for the person across from you.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-termination-newsletter",
        "subscribe_source": "source-wiki-termination",
        "sources_intro": "All claims on this page are sourced from <em>The Difficult Conversations Playbook</em>, Chapter 13. Primary sources cited:",
        "sources_list": [
            "Title VII of the Civil Rights Act (US federal law) — anti-discrimination baseline.",
            "Worker Adjustment and Retraining Notification (WARN) Act (US federal law) — large-scale layoff notification requirements.",
            "Older Workers Benefit Protection Act (OWBPA) — additional protections for terminations affecting workers 40+.",
            "Difficult Conversations Playbook Ch. 13 — full operational protocol with script library and survivor management.",
        ],
        "sources_outro": "",
    },

    # ─── Page 23: Salary Negotiation ────────────────────────────────────
    {
        "slug": "salary-negotiation",
        "page_num": "23",
        "title": "Salary Negotiation OS",
        "title_pre_words": "SALARY",
        "title_grad_word": "NEGOTIATION",
        "pillar": "UNDERSTANDING EACH OTHER",
        "thesis": "Three scripted frameworks: the Value Proposition that opens the negotiation, the Pivot when base salary is denied, and the Future Commitment that secures the next review. Plus the five non-salary elements you can negotiate when the base is fixed.",
        "reading_time": "7 min read",
        "last_updated": "May 2026",
        "source_chapter": "Difficult Conversations, Ch. 12",
        "date_published": "2026-05-01",
        "meta_description": "Three scripted salary negotiation frameworks: Value Proposition, Pivot, Future Commitment. Plus the five non-salary elements you can ask for. Sourced from Difficult Conversations Ch. 12.",
        "og_description": "Three scripted salary negotiation frameworks. Plus the non-salary asks.",
        "twitter_description": "Three scripts. Plus what to ask for when base is denied.",
        "schema_keywords": "salary negotiation, compensation, BATNA, value proposition, anchoring, principled negotiation",
        "pull_quote": {
            "text": "Salary negotiations represent a direct negotiation over Status and Fairness. Success demands pivoting from combative positional bargaining to the integrative, value-creation principles of the Harvard Method.",
            "cite": "— Difficult Conversations Playbook, Chapter 12",
        },
        "sections": [
            {"type": "h2", "title": "The problem", "no_rule": True},
            {"type": "p", "text": "You've been offered a number. Or you're going into a review and want a raise. Either way, the next 20 minutes will determine your compensation for the next 12. The instinct is to argue your case — list your accomplishments, ask for what you want, hope. The instinct underperforms. Most salary conversations are won or lost in the first three sentences."},
            {"type": "p", "text": "The Difficult Conversations Playbook Chapter 12 gives you three scripted frameworks: the Value Proposition (your opening), the Pivot (your fallback when base is denied), and the Future Commitment (the structure that protects you if today's answer is no). Plus the five non-salary elements you can ask for when the base is locked. The scripts work because they anchor on data, not on hope."},
            {"type": "h2", "title": "The mechanism"},
            {"type": "p", "text": "Three things make scripted compensation conversations outperform improvised ones."},
            {"type": "p_bold_lead", "lead": "Anchoring with market data shifts the frame.", "rest": "Saying \"based on market data, comp typically ranges from $130K to $145K\" anchors the conversation to an external benchmark. The negotiation moves from \"my will vs. your will\" to \"interpretation of evidence.\" The party with the stronger market data usually wins; both parties usually feel the process was fair (which matters for the post-negotiation relationship)."},
            {"type": "p_bold_lead", "lead": "Specific accomplishments beat general claims.", "rest": "\"I exceeded revenue targets by 20%\" beats \"I had a great year.\" \"I led the migration that cut infrastructure costs by $400K\" beats \"I'm a strong contributor.\" Specific numbers, dates, and outcomes are what convert your value proposition from a request into a calculation."},
            {"type": "p_bold_lead", "lead": "Non-salary asks expand the deal space.", "rest": "If base salary is fixed, the negotiation isn't over. Signing bonus, performance bonus tied to specific metrics, equity, additional PTO, professional development budget, flexible hours, defined review timeline — all of these are negotiable, often more easily than base. The Pivot script is what redirects the conversation onto these levers."},
            {"type": "stat_box", "label": "THE THREE SCRIPTS", "figure": "Value Proposition · Pivot · Future Commitment", "cite": "Difficult Conversations Playbook Ch. 12 — three scripted frameworks for the standard arc of a compensation negotiation; based on Harvard Method principles applied to salary specifically."},
            {"type": "h2", "title": "The protocol"},
            {"type": "p", "text": "Five steps. The first two are prep; the last three are the three scripts in their natural sequence."},
        ],
        "steps": [
            {"name": "Pre-meeting research — get the market data", "body": "Pull comparable compensation data from at least three sources before walking in. Levels.fyi, Glassdoor, Payscale, BLS, recent recruiter conversations. Find the range for your role + region + level + company tier. Not the average — the range. Memorize the bottom of the range, the median, and the top. \"Compensation typically ranges from $130K to $145K\" requires real data behind it.", "tip": "If you can't find market data because your role is unusual, find proxy data — adjacent roles, similar companies, recent hires at your seniority. Some data beats no data; aim for credible, not perfect."},
            {"name": "Pre-meeting accomplishments — three specifics", "body": "List your top three accomplishments from the past 12 months in measurable terms. Revenue, cost savings, team growth, projects shipped, problems solved. Each one needs a number, a timeframe, and a name (\"the Q3 product launch\"). Three specifics outperform a list of ten general claims because the negotiation is anchored to evidence, not enthusiasm.", "tip": "If your role doesn't produce easily measurable outcomes, use proxies: \"I onboarded 14 new hires across 3 functions, cutting average ramp time from 6 weeks to 4.\" Even back-office roles produce metrics if you look."},
            {"name": "Script 1: Value Proposition (opening)", "body": "<em>\"I appreciate the opportunity to discuss my compensation. Over the past twelve months, I have [accomplishment 1 with metric], [accomplishment 2], and [accomplishment 3]. Based on market data for [role] with this track record in [region/industry], compensation typically ranges from $X to $Y. I would like to discuss adjusting my base salary to align with this standard and my expanded contributions.\"</em> Read it. Practice it. Deliver it directly. Then stop talking and let them respond.", "tip": "The silence after the ask is uncomfortable. Don't fill it. Don't soften it (\"I know it's a lot to ask...\"). The first person to break the silence is the one who weakens their position."},
            {"name": "Script 2: Pivot (when base is denied)", "body": "<em>\"I completely understand that departmental budgets are currently fixed. Given my enthusiasm for this role, I would love to explore other elements of the compensation package. Would there be flexibility to discuss a performance-based signing bonus, an additional week of PTO, or a dedicated stipend for professional development certifications?\"</em> The Pivot redirects the conversation onto non-base elements. List 3-5 specifics — having concrete alternatives ready prevents the conversation from ending at \"no.\"", "tip": "Rank your non-salary asks by personal value beforehand. If the company will give you one item from a list of five, you want them to give you the most valuable one to you, not the cheapest one to them."},
            {"name": "Script 3: Future Commitment (regardless of today's outcome)", "body": "<em>\"Can we establish a specific set of performance metrics that, if achieved over the next six months, would trigger an automatic compensation review?\"</em> This script protects you from the most common failure mode: today's no becoming next year's no. By converting the no into a defined milestone, you turn a compensation conversation into a measurable goal with a known timeline. Even if today's negotiation produces nothing, the Future Commitment is what makes the next one different.", "tip": "Get the agreed-on metrics in writing — email follow-up at minimum. \"To confirm what we discussed, the metrics we'll review against in February are X, Y, and Z.\" Verbal commitments evaporate; written ones don't."},
        ],
        "after_steps_h2": "The printable: the three scripts",
        "after_steps_p": "Print this. Practice the three scripts out loud at least three times before the meeting. The naturalness comes from rehearsal, not improvisation.",
        "printable_card": {
            "title": "SALARY NEGOTIATION · 3 SCRIPTS",
            "subtitle": "DC Playbook Ch. 12",
            "items": [
                {"num": "01 · MARKET DATA — RANGE NOT AVERAGE", "text": "Bottom, median, top from 3+ sources.", "help": "Levels.fyi, Glassdoor, Payscale, BLS, recruiter convos."},
                {"num": "02 · THREE ACCOMPLISHMENTS — METRICS", "text": "Number + timeframe + project name. Three only.", "help": "Specifics > general claims."},
                {"num": "03 · VALUE PROPOSITION — OPEN", "text": "Three accomplishments + range + ask. Stop talking.", "help": "Don't fill the silence. Don't soften."},
                {"num": "04 · PIVOT — WHEN BASE IS DENIED", "text": "Signing bonus, PTO, dev stipend, flex hours, review timeline.", "help": "Rank by personal value beforehand."},
                {"num": "05 · FUTURE COMMITMENT — REGARDLESS", "text": "\"Specific metrics → automatic review in 6 months.\"", "help": "Get it in writing. Email follow-up."},
            ],
        },
        "exits": [
            dc_book_exit("Chapter 12 covers compensation negotiation in full — the three scripts in expanded form, the BATNA architecture for salary specifically, market data sourcing strategies, and the five non-salary elements with negotiation playbooks for each. Chapter 7 is the underlying Harvard Method."),
            {"tag": "Wiki · Free", "tag_class": "free", "url": "/human-os/harvard-method", "title": "Harvard Method 4-Step OS", "body": "Salary is one application; the Harvard Method is the underlying framework. Use both — pillars + scripts.", "cta": "Read the page →"},
            EXIT_SHOW,
        ],
        "subscribe_form_name": "wiki-salary-newsletter",
        "subscribe_source": "source-wiki-salary",
        "sources_intro": "All claims on this page are sourced from <em>The Difficult Conversations Playbook</em>, Chapter 12. Primary sources cited:",
        "sources_list": [
            "Fisher, R. & Ury, W. (1981). <em>Getting to Yes.</em> Underlying principled negotiation framework.",
            "Difficult Conversations Playbook Ch. 12 — three scripted frameworks (Value Proposition, Pivot, Future Commitment); five non-salary elements ranked.",
            "Babcock, L. & Laschever, S. (2003). <em>Women Don't Ask.</em> Foundational on the cumulative cost of not negotiating, particularly for women.",
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
    print(f"\nAll {len(PAGES)} Pillar 03 pages generated.")


if __name__ == "__main__":
    main()
