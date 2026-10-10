// Supports FR-DEL-01, FR-DEL-02, IF-ADMIN-01, CON-DEL-01
export default function ActivityActionMenu({ activity, onSelect }) {
  if (activity?.status !== 'published') {
    return null
  }

  return (
    <div aria-label={`actions-${activity.id}`}>
      <button type="button" onClick={() => onSelect('delete')}>
        ลบ
      </button>
      <button type="button" onClick={() => onSelect('suspend')}>
        ระงับ
      </button>
    </div>
  )
}
