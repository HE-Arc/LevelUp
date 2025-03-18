import { getCSRFToken } from '@/services/auth.js'
import { API_BASE_URL } from '@/config.js'

export const GameId = {
  MEMORY: 1,
  CLICKSPEED: 2,
  REFLEX: 3,
}

export async function saveScore(gameId, score, userId) {
  try {
    const response = await fetch(API_BASE_URL + '/save_score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({
        user: userId, //authStore.user.id,
        game: gameId,
        points: score,
      }),
    })

    if (!response.ok) {
      throw new Error('Error while saving score')
    }

    const data = await response.json()
    console.log('Score successfully saved :', data)
  } catch (error) {
    console.error('Error while sending request :', error)
  }
}

export async function getLeaderboard(gameId) {
  try {
    const response = await fetch(`${API_BASE_URL}/leaderboard?game_id=${gameId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    const text = await response.text() // Lire la réponse brute
    console.log('Raw response:', text) // Vérifier si c'est du JSON valide

    const data = JSON.parse(text) // Parser le JSON
    console.log('Leaderboard retrieved:', data)
    return data
  } catch (error) {
    console.error('Error while fetching leaderboard:', error)
    return []
  }
}
