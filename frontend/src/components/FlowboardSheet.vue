<script setup>
import { computed, ref, watch } from 'vue'
import { normalizeWeek } from '../utils/flowboard'
import { computeRatesFromTasks, scoreClass } from '../utils/scoring'

const FLAME_ITEMS = [
  { dim: 'focus', letter: 'F', label: 'Focus', q: 'How present and focused were you?' },
  { dim: 'leverage', letter: 'L', label: 'Leverage', q: 'Highest-impact work?' },
  { dim: 'alignment', letter: 'A', label: 'Alignment', q: 'Aligned with who you want to become?' },
  { dim: 'momentum', letter: 'M', label: 'Momentum', q: 'Staying ahead and moving forward?' },
  { dim: 'energy', letter: 'E', label: 'Energy', q: 'Energized and sustainable?' },
  { dim: 'fulfillment', letter: '+', label: 'Fulfillment', q: 'Fulfilled and satisfied?' },
]

const props = defineProps({
  week: { type: Object, required: true },
  readOnly: { type: Boolean, default: false },
})

const emit = defineEmits(['update'])

const local = ref(normalizeWeek(props.week))

watch(
  () => props.week,
  (w) => {
    local.value = normalizeWeek(w)
  },
  { deep: true }
)

const rates = computed(() => {
  if (props.readOnly) {
    return {
      coreRate: local.value.core ?? 0,
      sideRate: local.value.side ?? 0,
      score: local.value.score ?? 0,
    }
  }
  const r = computeRatesFromTasks(local.value.coreTasks, local.value.sideTasks)
  return {
    coreRate: r.coreRate,
    sideRate: r.sideRate,
    score: r.score,
  }
})

function emitUpdate() {
  if (!props.readOnly) emit('update', normalizeWeek(local.value))
}

function toggleTracker(taskList, rowIndex, circleIndex) {
  if (props.readOnly) return
  const filled = local.value[taskList][rowIndex].trackerFilled || 0
  const next = circleIndex + 1
  if (filled === next) {
    local.value[taskList][rowIndex].trackerFilled = circleIndex
  } else {
    local.value[taskList][rowIndex].trackerFilled = next
  }
  emitUpdate()
}

function setRating(dim, val) {
  if (props.readOnly) return
  if (!local.value.flameRatings) local.value.flameRatings = {}
  local.value.flameRatings[dim] = val
  emitUpdate()
}

function onFieldChange() {
  emitUpdate()
}
</script>

<template>
  <div class="flowboard-sheet" :class="{ 'flowboard-sheet--readonly': readOnly }">
    <header class="flowboard-header">
      <div class="flowboard-header__field">
        <label for="focus-week">Focus of the Week</label>
        <input id="focus-week" v-model="local.focus" type="text" :readonly="readOnly" @input="onFieldChange" />
      </div>
      <div class="flowboard-title">
        <h2>Weekly Flowboard</h2>
        <div class="date-line" />
        <input
          id="flowboard-date"
          type="text"
          :value="local.label"
          readonly
          aria-label="Date range"
          style="border: none; text-align: center; width: 100%; max-width: 10rem; margin: 0.5rem auto 0; display: block; font-size: 0.75rem; color: var(--ink-muted); background: transparent"
        />
      </div>
      <div class="flowboard-header__field" style="text-align: right">
        <label for="prize-week" style="text-align: right">Prize of the Week</label>
        <input id="prize-week" v-model="local.prize" type="text" :readonly="readOnly" @input="onFieldChange" />
      </div>
    </header>

    <div class="flowboard-table-wrap">
      <div class="flowboard-table-label">CORE TASKS</div>
      <table class="flowboard-table" aria-label="Core tasks">
        <thead>
          <tr>
            <th class="col-goal">Main Goal</th>
            <th class="col-why">Why?</th>
            <th class="col-time">Est. Time</th>
            <th class="col-tracker">Tracker [Free Yourself]</th>
            <th class="col-notes">Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(task, i) in local.coreTasks" :key="'c' + i">
            <td><input v-model="task.goal" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
            <td><input v-model="task.why" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
            <td><input v-model="task.time" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
            <td>
              <div class="tracker-row">
                <button
                  v-for="n in 14"
                  :key="n"
                  type="button"
                  class="tracker-circle"
                  :class="{ 'is-filled': (task.trackerFilled || 0) >= n }"
                  :disabled="readOnly"
                  :aria-label="`Tracker ${n}`"
                  @click="toggleTracker('coreTasks', i, n - 1)"
                />
              </div>
            </td>
            <td><input v-model="task.notes" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flowboard-table-wrap">
      <div class="flowboard-table-label">SIDE QUESTS</div>
      <table class="flowboard-table" aria-label="Side quests">
        <thead>
          <tr>
            <th class="col-goal">Side Activity</th>
            <th class="col-why">Why?</th>
            <th class="col-time">Est. Time</th>
            <th class="col-tracker">Tracker</th>
            <th class="col-notes">Notes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(task, i) in local.sideTasks" :key="'s' + i">
            <td><input v-model="task.goal" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
            <td><input v-model="task.why" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
            <td><input v-model="task.time" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
            <td>
              <div class="tracker-row">
                <button
                  v-for="n in 14"
                  :key="n"
                  type="button"
                  class="tracker-circle"
                  :class="{ 'is-filled': (task.trackerFilled || 0) >= n }"
                  :disabled="readOnly"
                  @click="toggleTracker('sideTasks', i, n - 1)"
                />
              </div>
            </td>
            <td><input v-model="task.notes" type="text" :readonly="readOnly" @input="onFieldChange" /></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flowboard-rates">
      <div class="rate-block">
        <strong>Core Rate:</strong>
        <span class="rate-value">{{ rates.coreRate }}%</span>
      </div>
      <div class="rate-block">
        <strong>Side Rate:</strong>
        <span class="rate-value">{{ rates.sideRate }}%</span>
      </div>
      <div class="rate-block">
        <strong>Weekly Score</strong> = 0.7 × Core + 0.3 × Side:
        <span class="rate-value" :class="scoreClass(rates.score)">{{ rates.score }}%</span>
      </div>
    </div>

    <div class="flowboard-bottom">
      <div class="flame-review">
        <div class="flowboard-section-label">FLAME + Fulfillment</div>
        <div v-for="item in FLAME_ITEMS" :key="item.dim" class="flame-item">
          <div class="flame-item__text">
            <strong>{{ item.letter }} — {{ item.label }}</strong>
            <span>{{ item.q }}</span>
          </div>
          <div class="rating-scale">
            <button
              v-for="n in 5"
              :key="n"
              type="button"
              class="rating-btn"
              :class="{ 'is-selected': (local.flameRatings?.[item.dim] || 0) === n }"
              :disabled="readOnly"
              @click="setRating(item.dim, n)"
            >
              {{ n }}
            </button>
          </div>
        </div>
      </div>
      <div class="flowboard-divider" />
      <div class="reflection-lines">
        <div class="flowboard-section-label">Reflection</div>
        <textarea
          v-for="(line, i) in local.reflection"
          :key="'r' + i"
          v-model="local.reflection[i]"
          :readonly="readOnly"
          rows="2"
          @input="onFieldChange"
        />
      </div>
    </div>
  </div>
</template>
