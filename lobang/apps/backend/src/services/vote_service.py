"""
Purpose: Create, delete, summarize, and aggregate user votes on deals.
"""

from typing import Any, Optional

from src.database.connection import get_conn


def _ensure_deal_exists(cur, deal_id: int) -> None:
    cur.execute("SELECT 1 FROM public.deals WHERE id = %s;", (deal_id,))
    if cur.fetchone() is None:
        raise ValueError(f"Deal {deal_id} does not exist")


def get_vote_summary(deal_id: int, user_id: Optional[str] = None) -> dict[str, Any]:
    """
    Return aggregate vote counts and, when available, the current user's vote.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            _ensure_deal_exists(cur, deal_id)
            return _get_vote_summary_with_cursor(cur, deal_id, user_id)
    finally:
        conn.close()


def _get_vote_summary_with_cursor(cur, deal_id: int, user_id: Optional[str]) -> dict[str, Any]:
    cur.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN vote = 1 THEN 1 ELSE 0 END), 0) AS upvote_count,
            COALESCE(SUM(CASE WHEN vote = -1 THEN 1 ELSE 0 END), 0) AS downvote_count
        FROM public.deal_votes
        WHERE deal_id = %s;
        """,
        (deal_id,),
    )
    counts = cur.fetchone()
    upvote_count = counts[0]
    downvote_count = counts[1]

    user_vote = None
    if user_id is not None:
        cur.execute(
            """
            SELECT vote
            FROM public.deal_votes
            WHERE deal_id = %s AND user_id = %s;
            """,
            (deal_id, user_id),
        )
        row = cur.fetchone()
        user_vote = row[0] if row else None

    return {
        "deal_id": deal_id,
        "upvote_count": upvote_count,
        "downvote_count": downvote_count,
        "community_score": upvote_count - downvote_count,
        "user_vote": user_vote,
    }


def set_vote(user_id: str, deal_id: int, vote: int) -> dict[str, Any]:
    """
    Insert or update the user's vote, then return the refreshed summary.
    """
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                _ensure_deal_exists(cur, deal_id)
                cur.execute(
                    """
                    INSERT INTO public.deal_votes (user_id, deal_id, vote)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, deal_id) DO UPDATE SET
                        vote = EXCLUDED.vote,
                        updated_at = NOW();
                    """,
                    (user_id, deal_id, vote),
                )
                return _get_vote_summary_with_cursor(cur, deal_id, user_id)
    finally:
        conn.close()


def remove_vote(user_id: str, deal_id: int) -> dict[str, Any]:
    """
    Delete the user's vote, then return the refreshed summary.
    """
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                _ensure_deal_exists(cur, deal_id)
                cur.execute(
                    """
                    DELETE FROM public.deal_votes
                    WHERE user_id = %s AND deal_id = %s;
                    """,
                    (user_id, deal_id),
                )
                return _get_vote_summary_with_cursor(cur, deal_id, user_id)
    finally:
        conn.close()


def get_vote_maps(
    deal_ids: list[int],
    user_id: Optional[str] = None,
) -> tuple[dict[int, dict[str, int]], dict[int, int]]:
    """
    Return aggregate vote counts for many deals plus the current user's votes.
    """
    if not deal_ids:
        return {}, {}

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    deal_id,
                    COALESCE(SUM(CASE WHEN vote = 1 THEN 1 ELSE 0 END), 0) AS upvote_count,
                    COALESCE(SUM(CASE WHEN vote = -1 THEN 1 ELSE 0 END), 0) AS downvote_count
                FROM public.deal_votes
                WHERE deal_id = ANY(%s)
                GROUP BY deal_id;
                """,
                (deal_ids,),
            )
            counts = {
                row[0]: {
                    "upvote_count": row[1],
                    "downvote_count": row[2],
                    "community_score": row[1] - row[2],
                }
                for row in cur.fetchall()
            }

            user_votes: dict[int, int] = {}
            if user_id is not None:
                cur.execute(
                    """
                    SELECT deal_id, vote
                    FROM public.deal_votes
                    WHERE deal_id = ANY(%s) AND user_id = %s;
                    """,
                    (deal_ids, user_id),
                )
                user_votes = {row[0]: row[1] for row in cur.fetchall()}

            return counts, user_votes
    finally:
        conn.close()
