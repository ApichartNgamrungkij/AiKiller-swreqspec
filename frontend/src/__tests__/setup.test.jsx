// test ตรวจหน้าจอรายการกิจกรรม (อ้างอิง FR-SRCH-01)
import { render, screen } from '@testing-library/react'
import App from '../App.jsx'

test('หน้าระบบจัดหากิจกรรมเปิดได้', () => {
  render(<App />)
  expect(screen.getByText('กิจกรรมที่กำลังเปิดรับ')).toBeTruthy()
})
