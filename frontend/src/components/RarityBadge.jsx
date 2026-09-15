import React from 'react'

export const RARITY_STYLES = {
  legendary: { cls: 'rarity-legendary', icon: '🌟' },
  epic: { cls: 'rarity-epic', icon: '💎' },
  rare: { cls: 'rarity-rare', icon: '✨' },
  common: { cls: 'rarity-common', icon: '🍜' },
}

export default function RarityBadge({ rarity }) {
  if (!rarity || !rarity.key) return null
  const style = RARITY_STYLES[rarity.key] || RARITY_STYLES['common']
  return (
    <span className={`rarity-badge ${style.cls}`}>
      <span className="rarity-icon">{style.icon}</span>
      {rarity.label}
    </span>
  )
}