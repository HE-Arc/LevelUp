import { getCSRFToken } from '@/services/auth.js'
import { API_BASE_URL } from '@/config.js'

export const GameName = {
  MEMORY: "Memory",
  CLICKSPEED: "ClickSpeed",
  REFLEX: "Reflex",
  SNAKE: "Snake",
  RUNNER: "Runner",
  TYPING: "Typing",
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
    //console.log('Score successfully saved :', data)
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
    //console.log('Raw response:', text)

    const data = JSON.parse(text)
    //console.log('Leaderboard retrieved:', data)
    return data
  } catch (error) {
    console.error('Error while fetching leaderboard:', error)
    return []
  }
}

export async function getRecords(gameName) {
  try {
    const response = await fetch(`${API_BASE_URL}/records?game_name=${gameName}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    const text = await response.text()

    return JSON.parse(text)

  } catch (error) {
    console.error('Error while fetching records:', error)
    return []
  }
}
