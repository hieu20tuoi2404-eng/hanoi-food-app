import React from 'react'

export default function AchievementBadge({ achievement, unlocked = true }) {
  return (
    <span className={`achievement-badge ${unlocked ? 'unlocked' : 'locked'}`} title={`${achievement.name}: ${achievement.desc}`}>
      <span className="achievement-icon">{achievement.icon}</span>
      <span className="achievement-name">{achievement.name}</span>
      <span className="achievement-xp">+{achievement.xp} XP</span>
    </span>
  )
}