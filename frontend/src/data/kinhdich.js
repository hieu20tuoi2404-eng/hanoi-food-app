// Bát quái — 8 quái cơ bản, lines từ dưới lên (bottom → top)
export const TRIGRAMS = {
  Khôn: [0, 0, 0],   // ☷ Đất
  Cấn: [0, 0, 1],    // ☶ Núi
  Khảm: [0, 1, 0],   // ☵ Nước
  Tốn: [0, 1, 1],    // ☴ Gió
  Chấn: [1, 0, 0],   // ☳ Sấm
  Ly: [1, 0, 1],     // ☲ Lửa
  Doai: [1, 1, 0],   // ☱ Hồ
  Can: [1, 1, 1],    // ☰ Trời
}

// Giá trị 3-bit cho mỗi quái (bottom → top, LSB = bottom)
const TRI_ID = {
  Khôn: 0b000,
  Cấn: 0b001,
  Khảm: 0b010,
  Tốn: 0b011,
  Chấn: 0b100,
  Ly: 0b101,
  Doai: 0b110,
  Can: 0b111,
}

const TRI_NAME = { 0: 'Khôn', 1: 'Cấn', 2: 'Khảm', 3: 'Tốn', 4: 'Chấn', 5: 'Ly', 6: 'Doai', 7: 'Can' }
const TRI_EMOJI = { Khôn:'☷', Cấn:'☶', Khảm:'☵', Tốn:'☴', Chấn:'☳', Ly:'☲', Doai:'☱', Can:'☰' }

// 64 quẻ — theo thứ tự Lễ Ký / Văn Vương
// lower là quái dưới (hào 1-3), upper là quái trên (hào 4-6)
// y = lời quẻ, food = gợi ý món Hà Nội
const HEXAGRAMS = [
  { n:1,  ten:'Quẻ Càn — Thuần Trời',    han:'乾', lower:'Can',  upper:'Can',  y:'Cát, Đại hanh. Sức mạnh trời đất hội tụ, mọi sự hanh thông.', food:'Bún chả — nướng khói càn lộc, dễ ăn.' },
  { n:2,  ten:'Quẻ Khôn — Thuần Đất',     han:'坤', lower:'Khôn', upper:'Khôn', y:'Thuận theo Đức lớn. Mang thai đất trời, lợi cho hóa vật.', food:'Xôi xéo — màu vàng đất, ấm áp, nuôi dưỡng.' },
  { n:3,  ten:'Truân — Sơ Nan',           han:'屯', lower:'Can',  upper:'Khảm', y:'Vạn sự khởi đầu nan. Dòng nước hiểm trở cần kiên trì.', food:'Phở gà — rau thơm giải ngán, giữ sức đi đường dài.' },
  { n:4,  ten:'Mông — Ủ Dột',             han:'蒙', lower:'Khảm', upper:'Cấn', y:'Dạy dỗ trẻ thơ. Chưa biết gì, cần thầy hướng dẫn.', food:'Cháo gà — dễ tiêu, phù hợp người mới bắt đầu.' },
  { n:5,  ten:'Nhu — Chờ Đợi',            han:'需', lower:'Can',  upper:'Khảm', y:'Chờ đợi giác ngộ. Nuôi dưỡng bản thân, chờ thời cơ.', food:'Bánh cuốn — khéo tay tráng từng lớp, chờ chín đều.' },
  { n:6,  ten:'Tụng — Tranh Tụng',        han:'讼', lower:'Khảm', upper:'Can',  y:'Tranh cãi bất lợi. Nhún nhường mà giữ mình.', food:'Bún đậu mắm tôm — vị mạnh, cần đàm phán bằng dạ dày.' },
  { n:7,  ten:'Sư — Quân Đoàn',            han:'师', lower:'Khảm', upper:'Khôn', y:'Quân đội chính nghĩa, chỉ huy tài tình, chiến thắng vẻ vang.', food:'Bún bò Huế — cay nồng dẫn đầu, đầy năng lượng.' },
  { n:8,  ten:'Tỷ — Kết Nghĩa',           han:'比', lower:'Khôn', upper:'Khảm', y:'Gắn bó, hợp tác. Chọn bạn hiền mà cùng tiến.', food:'Lẩu dê — quây quần chia sẻ, quan hệ keo sơn.' },
  { n:9,  ten:'Tiểu Súc — Nuôi Nhỏ',      han:'小畜', lower:'Can',  upper:'Tốn', y:'Tích tiểu thành đại. Dưỡng dục từ từ, đợi ngày thành tựu.', food:'Cốm Làng Vòng — nhón từng hạt, thu nhỏ tinh túy Hà Nội.' },
  { n:10, ten:'Lý — Đi Bộ',               han:'履', lower:'Doai', upper:'Can',  y:'Đi đúng đường, giữ lễ phép, ứng xử ôn hòa.', food:'Bánh giò — vuông vức, đàng hoàng, giữ đúng chuẩn.' },
  { n:11, ten:'Thái — Thái Hòa',           han:'泰', lower:'Can',  upper:'Khôn', y:'Địa Thiên giao cảm, muôn vật thông thái, thái bình thịnh.', food:'Cơm lam — vị ngọt tự nhiên, thanh bình, dễ chịu.' },
  { n:12, ten:'Bĩ — Bế Tắc',              han:'否', lower:'Khôn', upper:'Can',  y:'Nghịch cảnh, đóng cửa. Chờ vận chuyển biến.', food:'Mì vằn thắn — vùng vẫy trong sợi nước, rồi cũng thông.' },
  { n:13, ten:'Đồng Nhân — Hòa Hợp',      han:'同人', lower:'Can',  upper:'Ly',  y:'Kết bạn đồng âm. Hợp lực với người cùng chí hướng.', food:'Nem rán — vỏ giòn, nhân đồng lòng, dễ chia.' },
  { n:14, ten:'Đại Hữu — Giàu Lớn',       han:'大有', lower:'Ly',  upper:'Can',  y:'Tài sản dồi dào, ánh sáng soi rọi, may mắn lớn.', food:'Chả cá Lã Vọng — vàng óng, đắt giá, thịnh vượng.' },
  { n:15, ten:'Khiêm — Khiêm Nhường',      han:'谦', lower:'Cấn', upper:'Khôn', y:'Khiêm tốn được quý trọng. Giữ mình khi thành công.', food:'Bánh khúc — bé nhỏ, khiêm nhường nhưng tinh túy.' },
  { n:16, ten:'Dự — Dự Đoán',             han:'豫', lower:'Khôn', upper:'Chấn', y:'Vui vẻ hân hoan, sẵn sàng hành động.', food:'Kem Tràng Tiền — vui tươi, tuổi thơ, hân hoan.' },
  { n:17, ten:'Tùy — Tùy Duyên',           han:'随', lower:'Chấn', upper:'Doai', y:'Tùy theo thời thế, linh hoạt ứng biến, không cố chấp.', food:'Bún riêu cua — thay đổi vị theo mùa, tùy duyên.' },
  { n:18, ten:'Cổ — Sửa Đổi',             han:'蛊', lower:'Tốn',  upper:'Cấn', y:'Sửa chữa sai lầm. Bỏ cái cũ, đón nhận cái mới.', food:'Bánh mì patê — mix cũ mới, biến tấu truyền thống.' },
  { n:19, ten:'Lâm — Tiến Lên',            han:'临', lower:'Doai', upper:'Khôn', y:'Tiến lên gặp thuận lợi. Bốn tháng hanh thông.', food:'Cơm tấm — sườn nướng tiến lên, đậm đà.' },
  { n:20, ten:'Quán — Quan sát',           han:'观', lower:'Khôn', upper:'Tốn', y:'Nhìn lại bản thân, soi xét tự đáy lòng.', food:'Bánh mì xíu mại — quán nhỏ nhưng tinh tế, quan sát kỹ.' },
  { n:21, ten:'Phệ Hạp — Gặm Nhấm',       han:'噬嗑', lower:'Chấn', upper:'Ly',  y:'Xử lý rào cản, gỡ bỏ vật cản để thông suốt.', food:'Phá lấu — cắn xuyên qua, gỡ bỏ.' },
  { n:22, ten:'Bí — Trang Trọng',          han:'贲', lower:'Ly',  upper:'Cấn', y:'Trang trí đẹp đẽ. Vẻ ngoài tinh tế phản ánh nội tâm.', food:'Bánhrella — trang trí đẹp, bắt mắt, thịnh soạn.' },
  { n:23, ten:'Bác — Bóc Lột',            han:'剥', lower:'Khôn', upper:'Cấn', y:'Suy yếu dần, cần bảo toàn lực, chờ thời.', food:'Bánh tráng trộn — lớp lớp bóc, vị chua ngọt.' },
  { n:24, ten:'Phục — Quay Về',           han:'复', lower:'Chấn', upper:'Khôn', y:'Sự sống quay về. Nhất dương động, niềm hy vọng.', food:'Cháo lòng — ấm bụng, phục hồi sinh lực.' },
  { n:25, ten:'Vô Vọng — Không Ngờ',      han:'无妄', lower:'Chấn', upper:'Can',  y:'Tránh vọng động, thuận theo tự nhiên, không cưỡng cầu.', food:'Bánh tôm — ngon bất ngờ, không hề giả tạo.' },
  { n:26, ten:'Đại Súc — Nuôi Lớn',       han:'大畜', lower:'Can',  upper:'Cấn', y:'Tích trữ nhiều, tài đức được giữ gìn.', food:'Thịt bò nhúng dấm — tích trữ dinh dưỡng, giữ trọn vị.' },
  { n:27, ten:'Di — Nuôi Dưỡng',           han:'颐', lower:'Cấn', upper:'Chấn', y:'Chăm sóc khẩu phần, dưỡng sinh đúng cách.', food:'Cháo sườn — dễ tiêu, nuôi dưỡng từ từ.' },
  { n:28, ten:'Đại Quá — Quá Lớn',        han:'大过', lower:'Doai', upper:'Tốn', y:'Gánh nặng quá sức. Cần cẩn trọng trước khi gãy.', food:'Bánh xèo — to, giòn, nặng tay, cẩn thận khi cắn.' },
  { n:29, ten:'Khảm — Thuần Thủy',        han:'坎', lower:'Khảm', upper:'Khảm', y:'Nước chồng nước, nguy hiểm trùng điệp. Bình tĩnh vượt qua.', food:'Bún cá — bơi trong nước, vượt thác.' },
  { n:30, ten:'Ly — Thuần Hỏa',           han:'离', lower:'Ly',  upper:'Ly',  y:'Lửa sáng rực rỡ. Trí tuệ soi đường, kiên trì vững bước.', food:'Bún chả — nướng lửa hồng, tỏa sáng.' },
  { n:31, ten:'Hàm — Cảm Ứng',            han:'咸', lower:'Cấn', upper:'Doai', y:'Cảm ứng âm dương, rung động tự nhiên.', food:'Kem Tràng Tiền — cảm ứng vị ngọt dịu.' },
  { n:32, ten:'Hằng — Bền Lâu',           han:'恒', lower:'Tốn',  upper:'Chấn', y:'Lâu bền không đổi. Giữ vững nguyên tắc, không dao động.', food:'Phở bò — bền vững hàng trăm năm, không đổi.' },
  { n:33, ten:'Độn — Trốn Rời',           han:'遁', lower:'Cấn', upper:'Can',  y:'Rút lui đúng lúc, giữ mình khi thời không thuận.', food:'Bún mọc — trốn trong nước, im lặng mà ngon.' },
  { n:34, ten:'Đại Tráng — Mạnh Mẽ',      han:'大壮', lower:'Can',  upper:'Chấn', y:'Sức mạnh dâng cao. Dùng sức đúng lúc, kiềm chế đúng mức.', food:'Nem rán — mạnh mẽ, đầy năng lượng.' },
  { n:35, ten:'Tấn — Tiến Lên',           han:'晋', lower:'Khôn', upper:'Ly',  y:'Mặt trời mọc trên đất. Rực rỡ tiến lên, được tán dương.', food:'Xôi gấc — màu đỏ rực rỡ, tiến lên thịnh vượng.' },
  { n:36, ten:'Minh Di — Tối Tăm',        han:'明夷', lower:'Ly',  upper:'Khôn', y:'Ánh sáng bị che khuất. Giữ mình trong bóng tối, chờ ngày.', food:'Mì vằn thắn — mờ trong nước, nhưng vẫn ngon.' },
  { n:37, ten:'Gia Nhân — Gia Đình',      han:'家人', lower:'Ly',  upper:'Tốn', y:'Gia hòa vạn sự hưng. Gia đình thuận hòa, sự nghiệp tấn tới.', food:'Cơm nhà — ấm áp, sum vầy, gia đình.' },
  { n:38, ten:'Khuê — Đối Lập',           han:'睽', lower:'Doai', upper:'Ly',  y:'Mặt trời mặt trăng đối lập. Khác biệt nhưng bổ sung.', food:'Bún đậu — mắm tôm đối lập đậu hũ, hài hòa.' },
  { n:39, ten:'Kiển — Ngại Ngần',          han:'蹇', lower:'Cấn', upper:'Khảm', y:'Đường núi hiểm trở, nước chảy ngược. Khó khăn chồng chất.', food:'Bánh canh — đậm đặc, vượt qua thử thách.' },
  { n:40, ten:'Giải — Giải Thoát',        han:'解', lower:'Khảm', upper:'Chấn', y:'Sấm sét giải tỏa cơn mưa. Khó khăn qua đi, dễ chịu.', food:'Bún riêu — giải cơn khát, thanh mát.' },
  { n:41, ten:'Tổn — Giảm Thiểu',         han:'损', lower:'Doai', upper:'Cấn', y:'Giảm bớt lợi ích, tăng đức. Cho đi để nhận lại.', food:'Bánh cuốn — mỏng nhẹ, giữ tinh túy, bớt phô trương.' },
  { n:42, ten:'Ích — Tăng Thêm',          han:'益', lower:'Chấn', upper:'Tốn', y:'Tăng trưởng thuận lợi, lợi cho đường lớn.', food:'Cơm chiên — nhiều nguyên liệu, tăng thêm dinh dưỡng.' },
  { n:43, ten:'Quải — Quyết Đoán',        han:'夬', lower:'Can',  upper:'Doai', y:'Quyết liệt hành động, tuyên bố công khai.', food:'Bún chả — quyết liệt nướng chín, mạnh mẽ.' },
  { n:44, ten:'Cấu — Gặp Gỡ',            han:'姤', lower:'Tốn',  upper:'Can',  y:'Gặp gỡ bất ngờ, cẩn trọng kẻo mê hoặc.', food:'Phở cuốn — gặp gỡ vị tươi trong lớp bánh mỏng.' },
  { n:45, ten:'Tụy — Tụ Hợp',            han:'萃', lower:'Khôn', upper:'Doai', y:'Mọi người tụ họp, cùng chung mục tiêu.', food:'Lẩu — tụ họp quây quần, chung nồi.' },
  { n:46, ten:'Thăng — Lên Cao',          han:'升', lower:'Tốn',  upper:'Khôn', y:'Cây lớn dần từ đất. Tăng trưởng tự nhiên, kiên nhẫn.', food:'Bánh bèo — từ từ nổi lên, nhẹ nhàng.' },
  { n:47, ten:'Khốn — Khốn Khó',          han:'困', lower:'Khảm', upper:'Doai', y:'Nước dưới hồ cạn. Khốn khó nhưng không từ bỏ.', food:'Bánh đúc — đơn giản, vượt qua nghèo khó.' },
  { n:48, ten:'Tỉnh — Giếng Nước',        han:'井', lower:'Tốn',  upper:'Khảm', y:'Giếng nước nuôi người. Chăm chỉ đào sâu, không ngừng nghỉ.', food:'Canh măng — nuôi dưỡng, tự nhiên, tinh khiết.' },
  { n:49, ten:'Cách — Cách Mạng',         han:'革', lower:'Ly',  upper:'Doai', y:'Đổi mới toàn diện. Loại bỏ cái cũ, đón cái mới.', food:'Bánh mì mới — cách tân từ bánh mì truyền thống.' },
  { n:50, ten:'Đỉnh — Lò Đúc',            han:'鼎', lower:'Tốn',  upper:'Ly',  y:'Cái đỉnh thiêng. Nấu nướng tinh tế, văn hóa cao quý.', food:'Bún ốc — đỉnh cao ẩm thực Hà Nội, tinh túy.' },
  { n:51, ten:'Chấn — Thuần Lôi',         han:'震', lower:'Chấn', upper:'Chấn', y:'Sấm sét đôi, rung chuyển. Tỉnh thức, tự vấn.', food:'Bún cav — sấm dậy, vị cay tỉnh thức.' },
  { n:52, ten:'Cấn — Thuần Sơn',          han:'艮', lower:'Cấn', upper:'Cấn', y:'Núi đôi, tĩnh lặng. Dừng lại chiêm nghiệm.', food:'Bánh khúc — tĩnh lặng, nhấm nháp từng miếng.' },
  { n:53, ten:'Tiệm — Từ Từ',             han:'渐', lower:'Cấn', upper:'Tốn', y:'Từ từ tiến lên, từng bước chắc chắn.', food:'Bánh cuốn — từng lớp mỏng, kiên nhẫn tráng.' },
  { n:54, ten:'Quy Muội — Gả Em',         han:'归妹', lower:'Doai', upper:'Chấn', y:'Em gái xuất giá. Quyết định vội vàng, cần cân nhắc.', food:'Bánh trôi — đỏ thắm, háo hức nhưng cần kỹ.' },
  { n:55, ten:'Phong — Dồi Dào',          han:'丰', lower:'Ly',  upper:'Chấn', y:'Thời đại thịnh vượng. Đầy đủ, rực rỡ.', food:'Chả cá — dồi dào hương vị, thịnh soạn.' },
  { n:56, ten:'Lữ — Lữ Hành',            han:'旅', lower:'Cấn', upper:'Ly',  y:'Lữ hành trên núi. Mang ít hành lý, giữ mình.', food:'Bánh mì dọc đường — nhẹ, mang theo dễ dàng.' },
  { n:57, ten:'Tốn — Thuần Phong',        han:'巽', lower:'Tốn',  upper:'Tốn', y:'Gió đôi, thấm nhuần. Tinh tế, kiên nhẫn, không vội.', food:'Nem chua rán — tinh tế giòn tan, mềm.' },
  { n:58, ten:'Doai — Thuần Trạch',       han:'兑', lower:'Doai', upper:'Doai', y:'Hồ đôi, vui vẻ. Hài lòng, giao tiếp tốt.', food:'Bánh kem — vui vẻ, ngọt ngào.' },
  { n:59, ten:'Hoán — Tan Rã',            han:'涣', lower:'Khảm', upper:'Tốn', y:'Gió thổi tan sương mù. Giải tỏa, làm mới.', food:'Bún chả — thơm nức, tan tỏa vị ngon.' },
  { n:60, ten:'Tiết — Tiết Chế',          han:'节', lower:'Doai', upper:'Khảm', y:'Nước trong đê. Tiết chế, điều độ, biết dừng.', food:'Cơm nắm — gói gọn, tiết chế tinh túy.' },
  { n:61, ten:'Trung Phu — Lòng Tin',     han:'中孚', lower:'Doai', upper:'Tốn', y:'Cá bơi lên. Lòng tin chân thật, cảm hóa.', food:'Chả nem — giòn rụm, tin tưởng nguyên liệu tươi.' },
  { n:62, ten:'Tiểu Quá — Vượt Nhỏ',      han:'小过', lower:'Cấn', upper:'Chấn', y:'Chim bay qua núi. Nhỏ nhặt nhưng cẩn trọng.', food:'Bánh tráng — mỏng nhẹ, vượt qua từng sợi.' },
  { n:63, ten:'Ký Tế — Xong Xong',        han:'既济', lower:'Khảm', upper:'Ly',  y:'Nước trên lửa, việc đã thành. Thưởng thức thành quả.', food:'Bún chả — xong xuôi, thưởng thức thành quả.' },
  { n:64, ten:'Vị Tế — Chưa Xong',        han:'未济', lower:'Ly',  upper:'Khảm', y:'Lửa dưới nước, chưa xong. Kiên nhẫn, còn cơ hội.', food:'Phở — luôn còn hơn một bát nữa.' },
]

// Lookup map: key = `${lowerTriId}-${upperTriId}`
const HEX_MAP = {}
HEXAGRAMS.forEach(h => {
  const key = `${TRI_ID[h.lower]}-${TRI_ID[h.upper]}`
  HEX_MAP[key] = h
})

// Determine trigram from 3 lines (bottom → top), each line 0 or 1
function triFromLines(lines) {
  const key = lines[0] * 4 + lines[1] * 2 + lines[2]
  return TRI_NAME[key]
}

// From 6 lines → hexagram object
export function resolveHexagram(lines) {
  const lower = [lines[0], lines[1], lines[2]]
  const upper = [lines[3], lines[4], lines[5]]
  const lowerId = lower[0] * 4 + lower[1] * 2 + lower[2]
  const upperId = upper[0] * 4 + upper[1] * 2 + upper[2]
  const key = `${lowerId}-${upperId}`
  return HEX_MAP[key] || null
}

// Toss 3 coins → sum (6,7,8,9) + array of coin results [0,0,0]=tails
// coin: 0=sấp(2), 1=ngửa(3)
export function tossCoins() {
  const coins = [0,0,0].map(() => Math.random() < 0.5 ? 0 : 1)
  const sum = coins.reduce((a, b) => a + b + 2, 0) // 0→2, 1→3
  const isYang = sum % 2 === 1
  const isMoving = sum === 6 || sum === 9
  return {
    coins,       // [0,0,0] or [1,0,1] etc.
    sum,         // 6 | 7 | 8 | 9
    yang: isYang,
    moving: isMoving,
    label: sum === 6 ? 'Lão Âm' : sum === 7 ? 'Thiếu Dương' : sum === 8 ? 'Thiếu Âm' : 'Lão Dương',
  }
}

// Tổng hợp: gieo 6 lần → array 6 object tossCoins → lines (0/1) → hexagram
export function castHexagram() {
  const tosses = []
  const lines = []
  for (let i = 0; i < 6; i++) {
    const t = tossCoins()
    tosses.push(t)
    lines.push(t.yang ? 1 : 0)
  }
  const hex = resolveHexagram(lines)
  return { tosses, lines, hex }
}

export { TRI_EMOJI, TRI_NAME }
