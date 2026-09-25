from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TypologyNote:
    title: str
    tags: tuple[str, ...]
    content: str


class TypologyIndex:
    """Minimal in-memory retrieval index for fraud typology notes."""

    def __init__(self, notes: list[TypologyNote] | None = None) -> None:
        self.notes = notes or [
            TypologyNote(
                title="Account takeover",
                tags=("account takeover", "credential theft", "new device"),
                content=(
                    "A customer account shows rapid login changes, new device trust, "
                    "and follow-on transfers to external wallets."
                ),
            ),
            TypologyNote(
                title="Mule cash-out",
                tags=("mule", "cash-out", "rapid transfer"),
                content=(
                    "A newly created beneficiary receives repeated outflows in small "
                    "batches followed by immediate settlement."
                ),
            ),
            TypologyNote(
                title="Card testing",
                tags=("card testing", "small authorizations", "declines"),
                content=(
                    "Many low-value transactions from a single card or account with "
                    "repeated failed attempts before a larger charge."
                ),
            ),
            TypologyNote(
                title="Geography anomaly",
                tags=("new geography", "travel", "unusual region"),
                content=(
                    "A payment occurs from an unusual geography or from a different "
                    "country than the customer’s recent activity."
                ),
            ),
            TypologyNote(
                title="Velocity spike",
                tags=("velocity", "burst", "payment burst"),
                content=(
                    "A customer completes several high-value transactions within a "
                    "short period, inconsistent with their prior history."
                ),
            ),
        ]

    def search(self, query: str, limit: int = 3) -> list[dict[str, str | tuple[str, ...]]]:
        keywords = {term.lower() for term in query.replace("-", " ").split() if term}
        scored: list[tuple[float, TypologyNote]] = []

        for note in self.notes:
            tokens = {
                term.lower()
                for term in note.title.lower().split()
                + list(note.tags)
                + note.content.lower().split()
            }
            overlap = len(tokens & keywords)
            if overlap == 0 and not keywords:
                overlap = 1
            scored.append((float(overlap), note))

        ranked = sorted(scored, key=lambda item: item[0], reverse=True)
        return [
            {"title": note.title, "tags": note.tags, "content": note.content}
            for _, note in ranked[:limit]
        ]
