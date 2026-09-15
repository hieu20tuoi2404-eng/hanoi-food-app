import React from 'react'
import { useApp } from '../context/AppContext'
import { useNavigate } from 'react-router-dom'

export default function Settings() {
  const {
    mascot,
    mascots,
    clearMascot,
    openMascotPicker,
    animationsEnabled,
    toggleAnimations,
    mascotReady,
  } = useApp()
  const navigate = useNavigate()

  const handleOpenPicker = () => {
    openMascotPicker()
    navigate('/chon-con-giap')
  }

  return (
    <div className="settings-page">
      <h2 className="settings-title">Cài đặt</h2>

      <section className="settings-card">
        <h3>Linh vật đồng hành (12 con giáp)</h3>
        {mascot ? (
          <div className="settings-mascot-current" style={{ '--mascot-color': mascot.theme_color }}>
            <span className="settings-mascot-emoji">{mascot.emoji}</span>
            <div>
              <strong>{mascot.name} – {mascot.animal}</strong>
              <p>{mascot.greeting}</p>
              {mascot.verification_status === 'demo' && (
                <small>Hình minh hoạ do ứng dụng tự tạo (bản dùng thử).</small>
              )}
            </div>
          </div>
        ) : (
          <p className="settings-mascot-none">
            {mascotReady ? 'Bạn chưa chọn linh vật nào.' : 'Đang tải…'}
          </p>
        )}
        <div className="settings-actions">
          <button type="button" className="btn btn-primary" onClick={handleOpenPicker}>
            {mascot ? 'Đổi linh vật' : 'Chọn linh vật'}
          </button>
          {mascot && (
            <button
              type="button"
              className="btn btn-danger"
              onClick={async () => {
                if (window.confirm('Xoá linh vật đồng hành và dữ liệu liên quan?')) {
                  await clearMascot()
                }
              }}
            >
              Xoá linh vật &amp; dữ liệu
            </button>
          )}
        </div>
      </section>

      <section className="settings-card">
        <h3>Animation</h3>
        <p className="settings-hint">Tắt animation nếu bạn thích giao diện yên tĩnh hơn.</p>
        <label className="settings-toggle">
          <input
            type="checkbox"
            checked={animationsEnabled}
            onChange={toggleAnimations}
          />
          <span>Bật animation linh vật &amp; hiệu ứng</span>
        </label>
      </section>

      <section className="settings-card">
        <h3>Bộ sưu tập &amp; 12 con giáp</h3>
        <p className="settings-hint">
          Khám phá 30 món ăn Hà Nội, mở khoá 4 bậc thẻ hiếm và săn huy hiệu trong Bộ sưu tập.
        </p>
        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => navigate('/bo-suu-tap')}
        >
          Mở Bộ sưu tập
        </button>
      </section>

      <p className="settings-gennote">
        Mọi mô tả tính cách con giáp chỉ mang tính giải trí — không phải tư vấn khoa học.
      </p>
    </div>
  )
}