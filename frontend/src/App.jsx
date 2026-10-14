import { useMemo, useState } from 'react'

const activities = [
  { id: 1, title: 'ปลูกป่าชายเลน รักษ์ทะเลบ้านเรา', type: 'บำเพ็ญประโยชน์', date: 'เสาร์ 26 ตุลาคม 2569', time: '08:00–15:00 น.', location: 'ศูนย์อนุรักษ์ป่าชายเลน จังหวัดชลบุรี', hours: 6, enrolled: 42, capacity: 60, organizer: 'ชมรมอาสาพัฒนา มหาวิทยาลัย', description: 'ร่วมปลูกต้นโกงกางและเรียนรู้การดูแลระบบนิเวศชายฝั่งกับชุมชนท้องถิ่น', color: 'ocean' },
  { id: 2, title: 'ติวหนังสือให้น้องบนดอย', type: 'คุณธรรมจริยธรรม', date: 'อาทิตย์ 3 พฤศจิกายน 2569', time: '09:00–16:00 น.', location: 'โรงเรียนบ้านแม่กลางหลวง จังหวัดเชียงใหม่', hours: 6, enrolled: 18, capacity: 25, organizer: 'โครงการพี่สอนน้อง', description: 'แบ่งปันความรู้และสร้างแรงบันดาลใจในการเรียนให้กับน้อง ๆ ในชุมชน', color: 'sun' },
  { id: 3, title: 'เวิร์กช็อปศิลปะจากวัสดุเหลือใช้', type: 'ศิลปวัฒนธรรม', date: 'เสาร์ 9 พฤศจิกายน 2569', time: '13:00–17:00 น.', location: 'หอศิลป์ชุมชน มหาวิทยาลัย', hours: 4, enrolled: 30, capacity: 30, organizer: 'ชมรมศิลปะสร้างสรรค์', description: 'ชวนเด็ก ๆ ในชุมชนสร้างงานศิลป์จากวัสดุเหลือใช้ เพื่อเรียนรู้เรื่องความยั่งยืน', color: 'coral' },
]

const categories = ['ทั้งหมด', 'วิชาการ', 'กีฬา', 'ศิลปวัฒนธรรม', 'คุณธรรมจริยธรรม', 'บำเพ็ญประโยชน์']

function App() {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('ทั้งหมด')
  const [selected, setSelected] = useState(null)
  const filteredActivities = useMemo(() => activities.filter((activity) => {
    const text = `${activity.title} ${activity.location} ${activity.type}`.toLowerCase()
    return (category === 'ทั้งหมด' || activity.type === category) && text.includes(query.toLowerCase())
  }), [category, query])

  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#top"><span className="brand-mark">✦</span><span><strong>อาสาดี</strong><small>Volunteer Hub</small></span></a><nav className="nav-links"><a className="active" href="#activities">ค้นหากิจกรรม</a><a href="#schedule">ตารางของฉัน</a><a href="#about">เกี่ยวกับระบบ</a></nav><button className="profile-button" type="button">เข้าสู่ระบบ <span>→</span></button></header>
    <main id="top">
      <section className="hero"><div className="hero-copy"><p className="eyebrow">FIND YOUR GOOD DEED</p><h1>ค้นหากิจกรรมดี ๆ<br /><em>ที่ใช่สำหรับคุณ</em></h1><p className="hero-text">รวมกิจกรรมจิตอาสาจากมหาวิทยาลัยไว้ในที่เดียว<br />เลือกสิ่งที่สนใจ และออกไปสร้างความเปลี่ยนแปลงด้วยกัน</p><a className="hero-link" href="#activities">ดูรายการกิจกรรม <span>↓</span></a></div><div className="hero-art" aria-hidden="true"><div className="sun-disc" /><div className="hill hill-back" /><div className="hill hill-front" /><div className="flower flower-one">✿</div><div className="flower flower-two">✿</div><div className="hero-stat"><strong>120+</strong><span>กิจกรรมรอคุณอยู่</span></div></div></section>
      <section className="content-section" id="activities"><div className="section-heading"><div><p className="eyebrow">EXPLORE ACTIVITIES</p><h2>กิจกรรมที่กำลังเปิดรับ</h2></div><span className="result-count">พบ {filteredActivities.length} กิจกรรม</span></div><div className="search-row"><label className="search-box"><span>⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="ค้นหาชื่อกิจกรรม สถานที่ หรือประเภท..." /></label><label className="select-box"><span>ประเภทกิจกรรม</span><select value={category} onChange={(event) => setCategory(event.target.value)}>{categories.map((item) => <option key={item}>{item}</option>)}</select></label></div><div className="category-pills">{categories.map((item) => <button className={category === item ? 'pill selected' : 'pill'} key={item} onClick={() => setCategory(item)} type="button">{item}</button>)}</div>{filteredActivities.length === 0 ? <div className="empty-state">ไม่พบกิจกรรมที่ตรงกับเงื่อนไข</div> : <div className="activity-grid">{filteredActivities.map((activity) => <ActivityCard activity={activity} onSelect={setSelected} key={activity.id} />)}</div>}</section>
    </main>
    {selected && <ActivityModal activity={selected} onClose={() => setSelected(null)} />}<footer><span>อาสาดี · Volunteer Hub</span><span>ทุกชั่วโมงของคุณ มีความหมาย</span></footer>
  </div>
}

function ActivityCard({ activity, onSelect }) {
  const isFull = activity.enrolled >= activity.capacity
  return <article className="activity-card"><div className={`card-illustration ${activity.color}`}><span className="card-spark">✦</span><span className="card-leaf">◒</span><span className="card-number">0{activity.id}</span></div><div className="card-body"><div className="card-meta"><span className="type-tag">{activity.type}</span><span className={isFull ? 'status full' : 'status'}>{isFull ? 'เต็มแล้ว' : 'ยังรับสมัคร'}</span></div><h3>{activity.title}</h3><p className="organizer">โดย {activity.organizer}</p><div className="details"><span>◷ {activity.date}</span><span>⌖ {activity.location}</span><span>✦ {activity.hours} ชั่วโมงจิตอาสา</span></div><div className="card-bottom"><span className="capacity">{activity.enrolled}/{activity.capacity} คน</span><button onClick={() => onSelect(activity)} type="button">ดูรายละเอียด <span>↗</span></button></div></div></article>
}

function ActivityModal({ activity, onClose }) {
  return <div className="modal-backdrop" role="presentation" onClick={onClose}><div className="modal" role="dialog" aria-modal="true" aria-labelledby="activity-title" onClick={(event) => event.stopPropagation()}><button className="close-button" onClick={onClose} type="button" aria-label="ปิด">×</button><span className="type-tag">{activity.type}</span><h2 id="activity-title">{activity.title}</h2><p>{activity.description}</p><div className="modal-details"><span>◷ {activity.date} · {activity.time}</span><span>⌖ {activity.location}</span><span>✦ ได้รับ {activity.hours} ชั่วโมงจิตอาสา</span></div><div className="modal-notice">การลงทะเบียนจะดำเนินการต่อผ่าน Google Form ของกิจกรรม</div><a className="form-button" href="https://forms.google.com" target="_blank" rel="noreferrer">ไปยัง Google Form <span>↗</span></a></div></div>
}

export default App
