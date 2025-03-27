import { getCSRFToken } from '@/services/auth.js'
import { API_BASE_URL } from '@/config.js'

export const GameName = {
  MEMORY: "Memory",
  CLICKSPEED: "ClickSpeed",
  REFLEX: "Reflex",
  SNAKE: "Snake",
}

export async function saveScore(gameName, score, userId) {
  try {
    const response = await fetch(API_BASE_URL + '/save_score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({
        user: userId,
        game: gameName,
        points: score,
      }),
    })

    if (!response.ok) {
      throw new Error('Error while saving score')
    }

    const data = await response.json()

  } catch (error) {
    console.error('Error while sending request :', error)
  }
}

export async function getLeaderboard(gameName) {
  try {
    const response = await fetch(`${API_BASE_URL}/leaderboard?game_name=${gameName}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    const text = await response.text()

    const data = JSON.parse(text)

    return data
  } catch (error) {
    console.error('Error while fetching leaderboard:', error)
    return []
  }
}
