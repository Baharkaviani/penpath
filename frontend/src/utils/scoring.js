export function weeklyScore(core, side) {
  return Math.round(0.7 * core + 0.3 * side)
}

export function scoreClass(score) {
  if (score >= 80) return 'stat-card__value--success'
  if (score >= 70) return 'stat-card__value--warning'
  return 'stat-card__value--danger'
}

import { TRACKER_CIRCLES } from './flowboard'

const CORE_ROWS = 7
const SIDE_ROWS = 5

export function computeRatesFromTasks(coreTasks, sideTasks) {
  const countFilled = (tasks) =>
    (tasks || []).reduce((sum, t) => sum + (t.trackerFilled || 0), 0)
  const coreFilled = countFilled(coreTasks)
  const coreTotal = CORE_ROWS * TRACKER_CIRCLES
  const sideFilled = countFilled(sideTasks)
  const sideTotal = SIDE_ROWS * TRACKER_CIRCLES
  const coreRate = coreTotal ? Math.round((coreFilled / coreTotal) * 100) : 0
  const sideRate = sideTotal ? Math.round((sideFilled / sideTotal) * 100) : 0
  return { coreRate, sideRate, score: weeklyScore(coreRate, sideRate), coreFilled, sideTotal: sideFilled, coreTotal, sideTotalRaw: sideTotal }
}
