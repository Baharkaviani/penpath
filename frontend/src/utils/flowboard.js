/** Circles per task row — matches printable flowboard (design/flowboard.tex). */
export const TRACKER_CIRCLES = 14

/** Empty task row matching API flowboard shape. */
export function emptyTask() {
  return { goal: '', estimation: '', why: '', trackerFilled: 0 }
}

/** Map API / legacy payloads onto the current flowboard row shape. */
function normalizeTaskRow(task) {
  const row = {
    ...emptyTask(),
    ...task,
    estimation: task?.estimation ?? task?.time ?? task?.est_time ?? '',
    why: task?.why ?? '',
  }
  const notes = (task?.notes || '').trim()
  if (notes) {
    const why = row.why.trim()
    row.why = why ? `${why} — ${notes}` : notes
  }
  delete row.time
  delete row.est_time
  delete row.notes
  return row
}

/** Ensure flowboard always has 7 core + 5 side rows and 4 reflection lines. */
export function normalizeWeek(week) {
  if (!week) return null

  const coreTasks = Array.from({ length: 7 }, (_, i) =>
    normalizeTaskRow(week.coreTasks?.[i] || {})
  )
  const sideTasks = Array.from({ length: 5 }, (_, i) =>
    normalizeTaskRow(week.sideTasks?.[i] || {})
  )
  const reflection = [...(week.reflection || [])]
  while (reflection.length < 4) reflection.push('')

  return {
    ...week,
    coreTasks,
    sideTasks,
    reflection: reflection.slice(0, 4),
    flameRatings: { ...(week.flameRatings || {}) },
  }
}