// test ตรวจหน้าจอรายการกิจกรรม (อ้างอิง FR-SRCH-01)
import { fireEvent, render, screen } from '@testing-library/react'
import App from '../App.jsx'

test('หน้าระบบจัดหากิจกรรมเปิดได้', () => {
  render(<App />)
  expect(screen.getByText('กิจกรรมที่กำลังเปิดรับ')).toBeTruthy()
})

test('AC-APP-ROLE-01 นักศึกษาเปิดตารางส่วนตัวและลงทะเบียนได้', () => {
  render(<App />)
  fireEvent.click(screen.getByRole('link', { name: 'ตารางของฉัน' }))
  expect(screen.getByRole('heading', { name: 'ตารางของฉัน' })).toBeTruthy()

  fireEvent.click(screen.getByRole('link', { name: 'ค้นหากิจกรรม' }))
  fireEvent.click(screen.getAllByRole('button', { name: /ดูรายละเอียด/ })[0])
  expect(screen.getByText('พื้นที่ Google Form จำลอง')).toBeTruthy()
  expect(screen.getByRole('button', { name: 'ส่ง Google Form' })).toBeTruthy()
})

test('AC-APP-ROLE-02 ผู้จัดกิจกรรมเข้าถึง NewActivity และ ViewInfo ได้', () => {
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: /นักศึกษา/ }))
  fireEvent.click(screen.getByRole('button', { name: /ผู้จัดกิจกรรม/ }))

  expect(screen.getByRole('link', { name: 'สร้างกิจกรรมใหม่' })).toBeTruthy()
  expect(screen.getByRole('link', { name: 'ข้อมูลผู้ลงทะเบียน' })).toBeTruthy()

  fireEvent.click(screen.getByRole('link', { name: 'สร้างกิจกรรมใหม่' }))
  expect(screen.getAllByRole('heading', { name: 'สร้างกิจกรรมใหม่' }).length).toBeGreaterThan(0)
  fireEvent.click(screen.getByRole('link', { name: 'ข้อมูลผู้ลงทะเบียน' }))
  expect(screen.getByRole('heading', { name: 'รายชื่อผู้ลงทะเบียน' })).toBeTruthy()
})

test('AC-APP-ROLE-03 Admin เข้าถึงหน้าจัดการกิจกรรมได้', () => {
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: /นักศึกษา/ }))
  fireEvent.click(screen.getByRole('button', { name: /Admin/ }))
  fireEvent.click(screen.getByRole('link', { name: 'จัดการกิจกรรมทั้งหมด' }))
  expect(screen.getByRole('heading', { name: 'กิจกรรมที่เผยแพร่แล้ว' })).toBeTruthy()
  expect(screen.getAllByRole('button', { name: 'ลบ' }).length).toBeGreaterThan(0)
})
