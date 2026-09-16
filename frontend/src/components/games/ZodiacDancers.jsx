const ZODIAC = [
  { id: 'chuot', name: 'Tý',   animal: 'Chuột', emoji: '🐭', start: 23, end: 1 },
  { id: 'trau',  name: 'Sửu',  animal: 'Trâu',  emoji: '🐮', start: 1,  end: 3 },
  { id: 'ho',    name: 'Dần',  animal: 'Hổ',    emoji: '🐯', start: 3,  end: 5 },
  { id: 'tho',   name: 'Mão',  animal: 'Thỏ',   emoji: '🐰', start: 5,  end: 7 },
  { id: 'rong',  name: 'Thìn', animal: 'Rồng',  emoji: '🐲', start: 7,  end: 9 },
  { id: 'ran',   name: 'Tỵ',   animal: 'Rắn',   emoji: '🐍', start: 9,  end: 11 },
  { id: 'ngua',  name: 'Ngọ',  animal: 'Ngựa',  emoji: '🐴', start: 11, end: 13 },
  { id: 'de',    name: 'Mùi',  animal: 'Dê',    emoji: '🐐', start: 13, end: 15 },
  { id: 'khi',   name: 'Thân', animal: 'Khỉ',   emoji: '🐵', start: 15, end: 17 },
  { id: 'ga',    name: 'Dậu',  animal: 'Gà',    emoji: '🐓', start: 17, end: 19 },
  { id: 'cho',   name: 'Tuất', animal: 'Chó',   emoji: '🐶', start: 19, end: 21 },
  { id: 'heo',   name: 'Hợi',  animal: 'Lợn',   emoji: '🐷', start: 21, end: 23 },
]

const MEAL_ZODIAC = {
  breakfast: 'tho',
  lunch: 'ngua',
  dinner: 'cho',
  snack: 'khi',
  drinking: 'heo',
}

export function zodiacNow(now = new Date()) {
  const h = now.getHours()
  return ZODIAC.find((z) => {
    if (z.start < z.end) return h >= z.start && h < z.end
    return h >= z.start || h < z.end
  }) || ZODIAC[0]
}

export function zodiacForMeal(meal) {
  return ZODIAC.find((z) => z.id === MEAL_ZODIAC[meal]) || zodiacNow()
}

export default function ZodiacDancers({ highlight, active }) {
  return (
    <div className="zodiac-stage" role="img" aria-label="12 con giáp nhảy">
      {ZODIAC.map((z, i) => {
        const isHighlight = z.id === highlight
        const isWinner = z.id === active
        return (
          <span
            key={z.id}
            className={`zodiac-dancer ${isHighlight ? 'zodiac-dancer-highlight' : ''} ${isWinner ? 'zodiac-dancer-winner' : ''}`}
            style={{ '--z-i': i, '--z-delay': `${-(i * 0.14)}s` }}
            title={`${z.name} — ${z.animal}`}
          >
            {z.emoji}
          </span>
        )
      })}
    </div>
  )
}