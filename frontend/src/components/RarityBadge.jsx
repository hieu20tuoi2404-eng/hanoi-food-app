import React from 'react'

export const RARITY_STYLES = {
  'cuc-pham': { cls: 'rarity-cuc-pham', icon: '💎' },
  'dac-biet': { cls: 'rarity-dac-biet', icon: '🌟' },
  'hiem': { cls: 'rarity-hiem', icon: '✨' },
  'quoc-dan': { cls: 'rarity-quoc-dan', icon: '🍜' },
  'toi-mat': { cls: 'rarity-toi-mat', icon: '🎭' },
}

export default function RarityBadge({ rarity }) {
  if (!rarity || !rarity.key) return null
  const style = RARITY_STYLES[rarity.key] || RARITY_STYLES['toi-mat']
  return (
    <span className={`rarity-badge ${style.cls}`}>
      <span className="rarity-icon">{style.icon}</span>
      {rarity.label}
    </span>
  )
}