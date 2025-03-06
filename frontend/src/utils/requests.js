import { getCSRFToken } from '@/services/auth.js'

export const GameId = {
  MEMORY: 1,
  CLICKSPEED: 2,
  REFLEX: 3
};


export async function saveScore(userId, gameId, score) {
  try {
    const response = await fetch("http://localhost:8000/api/save_score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({
        user: userId,
        game: gameId,
        points: score,
      }),
    });

    if (!response.ok) {
      throw new Error("Error while saving score");
    }

    const data = await response.json();
    console.log("Score successfully saved :", data);
  } catch (error) {
    console.error("Error while sending request :", error);
  }
}
