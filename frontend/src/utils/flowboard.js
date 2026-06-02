/** Empty task row matching API flowboard shape. */
export function emptyTask() {
  return { goal: '', why: '', time: '', notes: '', trackerFilled: 0 }
}

/** Ensure flowboard always has 7 core + 5 side rows and 4 reflection lines. */
export function normalizeWeek(week) {
  if (!week) return null

  const coreTasks = Array.from({ length: 7 }, (_, i) => ({
    ...emptyTask(),
    ...(week.coreTasks?.[i] || {}),
  }))
  const sideTasks = Array.from({ length: 5 }, (_, i) => ({
    ...emptyTask(),
    ...(week.sideTasks?.[i] || {}),
  }))
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
