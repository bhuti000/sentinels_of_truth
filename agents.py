from tools import search_web
import sqlite3

DB_NAME = "facts.db"


def is_claim_verified(claim: str, evidence: str) -> bool:
    """
    Simple heuristic to detect whether a claim appears to be supported.
    """

    evidence_lower = evidence.lower()
    claim_lower = claim.lower()
    if "search failed" in evidence_lower:
        return False

    positive_keywords = [
        "won",
        "defeated",
        "confirmed",
        "official",
        "announced",
        "according to",
        "champion",
        "victory"
    ]

    negative_keywords = [
        "false",
        "fake",
        "hoax",
        "not true",
        "incorrect",
        "rumor",
        "unverified",
        "myth"
    ]

    # If negative keywords found, treat as fake
    for keyword in negative_keywords:
        if keyword in evidence_lower:
            return False

    for keyword in positive_keywords:
        if keyword in evidence_lower:
            return True

    return False


def agent_alpha(state):
    """
    Agent Alpha: Investigator
    Searches the web and determines whether the claim is verified or fake.
    """
    claim = state["claim"]

    print(f"[Agent Alpha] Investigating claim: {claim}")

    evidence = search_web(claim)

    if is_claim_verified(claim, evidence):
        verification_status = "VERIFIED"
    else:
        verification_status = "FAKE"

    state["evidence"] = evidence
    state["verification_status"] = verification_status

    return state


def agent_beta(state):
    """
    Agent Beta: Archivist
    Checks database and decides:
    - INSERT
    - DISCARD
    - FLAG_REVIEW
    """
    claim = state["claim"]
    status = state["verification_status"]
    evidence = state["evidence"]

    print("[Agent Beta] Checking database for claim...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status FROM facts WHERE claim = ?",
        (claim,)
    )
    existing = cursor.fetchone()

    if existing:
        existing_status = existing[0]
        if existing_status != status:
            decision = "FLAG_REVIEW"
        else:
            decision = "DISCARD"

    else:
        if status == "VERIFIED":
            cursor.execute(
                "INSERT INTO facts (claim, status, evidence) VALUES (?, ?, ?)",
                (claim, status, evidence)
            )
            conn.commit()
            decision = "INSERT"
        else:
            decision = "FLAG_REVIEW"

    conn.close()

    state["decision"] = decision

    return state