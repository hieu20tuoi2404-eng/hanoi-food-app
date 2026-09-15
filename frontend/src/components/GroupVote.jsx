import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

const BAD_WORDS = ['mẹ', 'bố', 'con cặc', 'địt', 'lồn', 'chó má', 'cút']

function sanitizeName(name) {
  return name.replace(/[<>{}]/g, '').trim()
}

function isClean(name) {
  const low = name.toLowerCase()
  return !BAD_WORDS.some((w) => low.includes(w))
}

export default function GroupVote() {
  const { api } = useApp()
  const [hostName, setHostName] = useState('')
  const [voterName, setVoterName] = useState('')
  const [roomCode, setRoomCode] = useState('')
  const [room, setRoom] = useState(null)
  const [choice, setChoice] = useState(null)
  const [view, setView] = useState('create') // create | join | room
  const [error, setError] = useState('')
  const [info, setInfo] = useState('')
  const [loading, setLoading] = useState(false)

  const createRoom = async (e) => {
    e.preventDefault()
    setError(''); setInfo('')
    const name = sanitizeName(hostName)
    if (!name || name.length > 40) { setError('Tên chủ phòng không hợp lệ (≤40 ký tự)'); return }
    if (!isClean(name)) { setError('Tên có nội dung không phù hợp'); return }
    setLoading(true)
    try {
      const r = await api('/api/group-rooms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ host_name: name, config: {} }),
      })
      setRoom(r)
      setRoomCode(r.room_code)
      setView('room')
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }

  const joinRoom = async (e) => {
    e.preventDefault()
    setError(''); setInfo('')
    const code = roomCode.trim().toUpperCase()
    if (code.length !== 6) { setError('Mã phòng 6 ký tự'); return }
    if (view !== 'room') {
      // first fetch to open the room view
    }
    setLoading(true)
    try {
      const r = await api(`/api/group-rooms/${code}`)
      setRoom(r)
      setView('room')
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }

  const castVote = async (dishId) => {
    setError(''); setInfo('')
    const name = sanitizeName(voterName)
    if (!name || name.length > 40) { setError('Tên hợp lệ cần 1-40 ký tự'); return }
    if (!isClean(name)) { setError('Tên có nội dung không phù hợp'); return }
    setLoading(true)
    try {
      await api(`/api/group-rooms/${room.room_code}/votes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voter_name: name, dish_id: dishId }),
      })
      setChoice(dishId)
      setInfo('Đã bỏ phiếu!')
      const r = await api(`/api/group-rooms/${room.room_code}`)
      setRoom(r)
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }

  const finish = async (e) => {
    e.preventDefault()
    setError(''); setInfo('')
    const name = sanitizeName(hostName)
    if (!name || name.length > 40) { setError('Tên chủ phòng không hợp lệ'); return }
    if (!isClean(name)) { setError('Tên có nội dung không phù hợp'); return }
    setLoading(true)
    try {
      await api(`/api/group-rooms/${room.room_code}/finish`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      })
      const r = await api(`/api/group-rooms/${room.room_code}`)
      setRoom(r)
      setInfo('Đã chốt kết quả!')
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }

  const tally = room?.vote_tally
  const votesCount = (dishId) => (room?.vote_tally?.tally || []).find((t) => t.dish.id === dishId)?.votes || 0
  const totalVotes = tally?.total_votes || 0

  return (
    <div className="widget group-widget">
      <h3 className="widget-title">👥 "Ăn gì đây mọi người?"</h3>
      <p className="widget-sub">Tạo phòng, mời mọi người, vote món — không cần tài khoản!</p>

      {!room && view === 'create' && (
        <form className="group-form" onSubmit={createRoom}>
          <input type="text" placeholder="Tên của bạn (chủ phòng)" value={hostName}
                 onChange={(e) => setHostName(e.target.value)} maxLength={40} />
          <button type="submit" className="lootbox-open fate-btn" disabled={loading}>
            {loading ? 'Đang tạo...' : 'Tạo phòng 🏠'}
          </button>
          <button type="button" className="fate-btn-soft" onClick={() => setView('join')}>Tôi có mã phòng rồi — vào phòng</button>
        </form>
      )}

      {!room && view === 'join' && (
        <form className="group-form" onSubmit={joinRoom}>
          <input type="text" placeholder="Mã phòng (VD: ABC123)" value={roomCode}
                 onChange={(e) => setRoomCode(e.target.value)} maxLength={6} />
          <button type="submit" className="lootbox-open fate-btn" disabled={loading}>
            {loading ? 'Đang vào...' : 'Vào phòng 🚪'}
          </button>
          <button type="button" className="fate-btn-soft" onClick={() => setView('create')}>Quay lại tạo phòng</button>
        </form>
      )}

      {error && <div className="lootbox-error">{error}</div>}
      {info && <div className="group-info">{info}</div>}

      {room && (
        <div className="group-room">
          <div className="group-room-head">
            <span>Phòng <b className="group-code">{room.room_code}</b></span>
            <span className="group-status">{room.status === 'open' ? 'Đang bỏ phiếu' : 'Đã chốt'}</span>
            <button type="button" className="fate-btn-soft" onClick={() => { setRoom(null); setChoice(null); setView('create') }}>
              Rời phòng
            </button>
          </div>

          {!choice && room.status === 'open' && (
            <div className="group-vote-note">
              Nhập tên rồi chọn món cho phiếu của bạn (1 người 1 phiếu):
              <input type="text" placeholder="Tên của bạn" value={voterName}
                     onChange={(e) => setVoterName(e.target.value)} maxLength={40} />
            </div>
          )}

          <div className="group-dishes">
            {room.dishes.map((d) => {
              const v = votesCount(d.id)
              const isTop = tally?.winner?.id === d.id && v > 0
              return (
                <button key={d.id} type="button"
                  className={`group-dish ${choice === d.id ? 'chosen' : ''} ${isTop ? 'top' : ''}`}
                  onClick={() => room.status === 'open' && castVote(d.id)}
                  disabled={room.status !== 'open' || !!choice}
                >
                  <img src={d.image_url} alt={d.name} onError={(e) => { e.target.src = '/images/fallback.svg' }}
                       className="group-dish-img" />
                  <span className="group-dish-name">{d.name}</span>
                  <span className="group-dish-votes">{v} phiếu</span>
                  {isTop && <span className="group-top-badge">👑 Leading</span>}
                </button>
              )
            })}
          </div>

          {totalVotes > 0 && (
            <div className="group-tally">
              <b>{totalVotes}</b> phiếu đã bỏ
            </div>
          )}

          {room.status === 'open' && (
            <button type="button" className="lootbox-open fate-btn" onClick={finish} disabled={loading}>
              {loading ? 'Đang chốt...' : 'Chốt kết quả 🏁'}
            </button>
          )}

          {room.status === 'finished' && tally?.winner && (
            <div className="group-winner">
              🎉 Quyết định hôm nay là <b>{tally.winner.name}</b>!
              <Link to={`/dish/${tally.winner.slug}`} className="lootbox-result-link"> Xem chi tiết &#8594;</Link>
            </div>
          )}
          {room.status === 'finished' && tally?.tied?.length > 1 && (
            <div className="group-winner">Hoà phiếu giữa: {tally.tied.map((t) => t.name).join(', ')} — chốt ngẫu nhiên nếu cần!</div>
          )}
        </div>
      )}
    </div>
  )
}