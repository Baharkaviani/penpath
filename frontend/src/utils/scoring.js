export function weeklyScore(core, side) {
  return Math.round(0.7 * core + 0.3 * side)
}

export function scoreClass(score) {
  if (score >= 80) return 'stat-card__value--success'
  if (score >= 70) return 'stat-card__value--warning'
  return 'stat-card__value--danger'
}

export function computeRatesFromTasks(coreTasks, sideTasks) {
  const countFilled = (tasks) =>
    (tasks || []).reduce((sum, t) => sum + (t.trackerFilled || 0), 0)
  const coreFilled = countFilled(coreTasks)
  const coreTotal = 7 * 14
  const sideFilled = countFilled(sideTasks)
  const sideTotal = 5 * 14
  const coreRate = coreTotal ? Math.round((coreFilled / coreTotal) * 100) : 0
  const sideRate = sideTotal ? Math.round((sideFilled / sideTotal) * 100) : 0
  return { coreRate, sideRate, score: weeklyScore(coreRate, sideRate), coreFilled, sideTotal: sideFilled, coreTotal, sideTotalRaw: sideTotal }
}
