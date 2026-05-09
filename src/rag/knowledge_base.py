"""
Knowledge base: curated passages on effective studying.
Each entry has an id, the text content, and metadata tags.
"""

DOCUMENTS = [
    {
        "id": "spaced-repetition-1",
        "text": (
            "Spaced repetition is one of the most evidence-backed study techniques. "
            "Instead of reviewing material all at once (massed practice), you spread reviews "
            "over increasing time intervals — for example: review after 1 day, then 3 days, "
            "then 1 week, then 2 weeks. Each time you successfully recall something, the next "
            "review is scheduled further in the future. Tools like Anki implement this "
            "automatically using the SM-2 algorithm. Studies show spaced repetition can produce "
            "retention rates 2–3× higher than cramming for the same study time."
        ),
        "metadata": {"topic": "memory", "technique": "spaced repetition"},
    },
    {
        "id": "active-recall-1",
        "text": (
            "Active recall (also called retrieval practice) means testing yourself on material "
            "rather than passively re-reading it. After reading a section, close the book and "
            "try to write down or say everything you remember. This effortful retrieval "
            "strengthens the memory trace far more than re-reading. The 'testing effect' is "
            "one of the most replicated findings in cognitive psychology. Practical methods: "
            "flashcards, practice problems, the blank-page technique (dump everything you know "
            "onto a blank page), and past exam questions."
        ),
        "metadata": {"topic": "memory", "technique": "active recall"},
    },
    {
        "id": "feynman-technique-1",
        "text": (
            "The Feynman Technique is a four-step method for deep understanding: "
            "(1) Pick a concept and write its name at the top of a page. "
            "(2) Explain it in plain language as if teaching a 12-year-old — no jargon. "
            "(3) Identify gaps: wherever your explanation breaks down or you reach for technical "
            "terms you can't unpack, go back to the source material. "
            "(4) Simplify further and use analogies. "
            "The goal is to expose the difference between familiarity and genuine understanding. "
            "Named after physicist Richard Feynman, who was famous for being able to explain "
            "complex ideas simply."
        ),
        "metadata": {"topic": "understanding", "technique": "feynman"},
    },
    {
        "id": "pomodoro-1",
        "text": (
            "The Pomodoro Technique structures study into focused intervals: 25 minutes of "
            "deep work followed by a 5-minute break, repeated 4 times, then a longer 15–30 "
            "minute break. This combats two major problems: starting (the timer creates a "
            "low-stakes commitment) and sustaining focus (knowing a break is coming makes "
            "it easier to resist distractions). Adjust the intervals to fit your attention "
            "span — some people do better with 50/10. The key principle is time-boxing: "
            "working with full attention for a defined period rather than half-working indefinitely."
        ),
        "metadata": {"topic": "focus", "technique": "pomodoro"},
    },
    {
        "id": "interleaving-1",
        "text": (
            "Interleaving means mixing different topics or problem types within a single study "
            "session, rather than blocking (finishing all of topic A before starting topic B). "
            "Although interleaving feels harder and produces slower apparent progress during "
            "practice, it leads to significantly better long-term retention and the ability "
            "to transfer knowledge to new problems. For example, instead of doing 30 calculus "
            "problems then 30 statistics problems, mix them together. This forces your brain "
            "to identify which strategy applies to each problem — a skill exams actually test."
        ),
        "metadata": {"topic": "memory", "technique": "interleaving"},
    },
    {
        "id": "sleep-memory-1",
        "text": (
            "Sleep is not optional for learning — it is when memory consolidation primarily "
            "happens. During slow-wave sleep, the hippocampus replays the day's learning and "
            "transfers it to the cortex for long-term storage. REM sleep is critical for "
            "procedural and emotional memory. Pulling an all-nighter before an exam trades "
            "short-term cram gains for degraded recall and reasoning the next day. "
            "Aim for 7–9 hours. Studying material right before sleep (especially with a "
            "quick review session) can enhance consolidation."
        ),
        "metadata": {"topic": "biology", "technique": "sleep"},
    },
    {
        "id": "elaborative-interrogation-1",
        "text": (
            "Elaborative interrogation means asking 'why' and 'how' as you study, then "
            "generating explanations. Instead of reading 'the heart pumps blood', ask "
            "'why does blood need to be pumped — what happens if it isn't?' and construct "
            "an answer. This forces you to connect new information to things you already "
            "know, building a richer network of associations. Studies show it significantly "
            "outperforms simple re-reading. It works especially well for factual material "
            "in science and history."
        ),
        "metadata": {"topic": "understanding", "technique": "elaborative interrogation"},
    },
    {
        "id": "environment-focus-1",
        "text": (
            "Your study environment directly affects focus quality. Key factors: "
            "Remove your phone from the room (not just silence it — physical distance matters). "
            "Use background noise at 60–70 dB (ambient café sounds or brown noise) if silence "
            "is distracting. Study in the same place consistently — your brain associates "
            "the environment with focus mode. Avoid studying in bed, which your brain "
            "associates with sleep. Good lighting reduces eye strain. Some people benefit "
            "from study-specific playlists they always use — the familiar sound becomes a "
            "focus trigger."
        ),
        "metadata": {"topic": "focus", "technique": "environment"},
    },
    {
        "id": "goals-planning-1",
        "text": (
            "Effective study sessions start with a specific goal, not a time target. "
            "'Study for 2 hours' is less effective than 'understand how the Krebs cycle "
            "works and be able to draw it from memory'. Specific goals give you a way to "
            "know when you're done and keep you from passive re-reading. "
            "Use weekly planning: identify what needs to be mastered by week's end, then "
            "work backwards to assign topics to each day. Leave buffer days for review "
            "and unexpected difficulty. Track what you actually accomplished vs planned — "
            "the gap reveals overestimation patterns."
        ),
        "metadata": {"topic": "planning", "technique": "goal setting"},
    },
    {
        "id": "desirable-difficulty-1",
        "text": (
            "Desirable difficulties are study conditions that slow apparent learning during "
            "practice but enhance long-term retention. Examples: "
            "— Using handwriting instead of typing (slower, but encodes more deeply). "
            "— Reducing font readability slightly forces deeper processing. "
            "— Generating an answer before reading it (even if wrong, the attempt primes memory). "
            "— Varying your study location instead of always using the same spot. "
            "The core idea: if studying feels too easy, you probably aren't learning much. "
            "Some friction is a signal of effective encoding, not inefficiency."
        ),
        "metadata": {"topic": "memory", "technique": "desirable difficulty"},
    },
    {
        "id": "mind-mapping-1",
        "text": (
            "Mind mapping is a visual organisation technique where you place a central concept "
            "in the middle of a page and branch out to related ideas, sub-concepts, and "
            "connections. It works best for understanding relationships between ideas, "
            "not for memorising isolated facts. The act of building the map — deciding what "
            "connects to what — is more valuable than the finished diagram. After studying "
            "a chapter, try drawing a mind map from memory before checking your notes. "
            "This combines the benefits of retrieval practice with visual organisation."
        ),
        "metadata": {"topic": "understanding", "technique": "mind mapping"},
    },
    {
        "id": "motivation-habits-1",
        "text": (
            "Motivation is unreliable as a study driver — habits and systems are more durable. "
            "Implementation intentions ('I will study at 7pm at my desk after dinner') "
            "are far more effective than vague goals ('I should study more'). "
            "Reduce friction: have your materials ready before the scheduled time. "
            "Track your streak — even a simple calendar X-mark builds identity reinforcement. "
            "Use temptation bundling: pair studying with something you enjoy (a specific "
            "tea, a comfortable chair) so the study context itself becomes rewarding. "
            "Don't rely on feeling ready — start anyway, as motivation often follows action."
        ),
        "metadata": {"topic": "habits", "technique": "motivation systems"},
    },
]