import React, { useEffect, useState } from 'react'
import { useApp } from '../context/AppContext'
import AchievementBadge from './AchievementBadge'

export default function ExplorationProfile() {
  const { api } = useApp()
  const [data, setData] = useState(null)
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const d = await api('/api/exploration')
      setData(d)
    } catch (e) {
      // keep old data
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    // refresh when user comes back / after interactions
    window.addEventListener('focus', load)
    return () => window.removeEventListener('focus', load)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  if (!data) {
    return (
      <div className="explore-card compact">
        <div className="explore-row">
          <span className="explore-level-icon">🌱</span>
          <div>
            <div className="explore-level-name">Đang tải hồ sơ khám phá...</div>
          </div>
        </div>
      </div>
    )
  }

  const { level, xp, next_level, viewed_count, reviewed_count, districts_explored, achievements, unlocked_count, total_achievements } = data
  const progress = next_level ? Math.min(100, Math.round((xp / next_level.min_xp) * 100)) : 100

  return (
    <div className={`explore-card ${open ? 'open' : 'compact'}`}>
      <button className="explore-toggle" type="button" onClick={() => setOpen((o) => !o)}>
        <div className="explore-row">
          <span className="explore-level-icon">{level.icon}</span>
          <div>
            <div className="explore-level-name">{level.name}</div>
            <div className="explore-level-desc">{level.desc}</div>
          </div>
          <div className="explore-xp">
            <b>{xp}</b> XP
            <span className="explore-xp-total">/ {next_level ? next_level.min_xp : xp}</span>
          </div>
          <div className="explore-chevron">{open ? '▲' : '▼'}</div>
        </div>
      </button>

      {open && (
        <div className="explore-detail">
          <div className="explore-progress">
            <div className="explore-progress-track">
              <div className="explore-progress-fill" style={{ width: `${progress}%` }} />
            </div>
            <div className="explore-progress-label">
              {next_level
                ? `Còn ${next_level.min_xp - xp} XP nữa để mở ${next_level.name} ${next_level.icon}`
                : 'Đã đạt cấp độ cao nhất!'}
            </div>
          </div>

          <div className="explore-stats">
            <div className="explore-stat"><b>{viewed_count}</b> món đã xem</div>
            <div className="explore-stat"><b>{reviewed_count}</b> đánh giá</div>
            <div className="explore-stat"><b>{districts_explored}</b> quận đã ghé</div>
            <div className="explore-stat"><b>{unlocked_count}/{total_achievements}</b> huy hiệu</div>
          </div>

          <div className="achievements">
            <h4 className="achievements-title">Huy hiệu đã đạt</h4>
            {achievements.length === 0 && <div className="empty small">Chưa có huy hiệu — xem vài món ăn để bắt đầu!</div>}
            <div className="achievement-list">
              {achievements.map((a) => (
                <AchievementBadge key={a.key} achievement={a} unlocked />
              ))}
            </div>
            <h4 className="achievements-title">Còn thiếu</h4>
            <div className="achievement-list locked">
              {Array.from({ length: total_achievements - unlocked_count }).map((_, i) => (
                <span key={`lock-${i}`} className="achievement-badge locked" title="Chưa mở khóa">
                  🔒
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}