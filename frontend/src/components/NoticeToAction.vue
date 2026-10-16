<template>
  <div class="notice-to-action">
    <!-- Component Header -->
    <div class="nta-header">
      <div class="nta-title-group">
        <div class="nta-badge-row">
          <span class="engine-badge">
            <span class="pulse-dot"></span> GEMMA 4
          </span>
          <span class="model-tag">{{ activeModel }}</span>
          <span class="mode-indicator" :class="isDemo ? 'demo' : 'live'">
            {{ isDemo ? 'DEMO MODE' : 'LIVE GEMINI API' }}
          </span>
        </div>
        <h2 class="nta-title">Notice-to-Action</h2>
        <p class="nta-subtitle">
          Turn campus event posters, university circulars, and policy announcements into clear, prioritized action checklists.
        </p>
      </div>

      <div class="nta-controls">
        <label class="demo-toggle-label" title="Toggle between real Gemma 4 API calls and pre-verified sample responses">
          <input type="checkbox" v-model="isDemo" class="demo-checkbox" />
          <span class="toggle-text">Demo Mode</span>
        </label>
      </div>
    </div>

    <!-- Quick Samples Selector -->
    <div class="samples-bar">
      <span class="samples-label">Quick Demo Presets:</span>
      <button 
        v-for="sample in sampleList" 
        :key="sample.id"
        class="sample-pill-btn"
        :class="{ active: selectedSampleId === sample.id }"
        @click="loadSample(sample)"
      >
        <span class="pill-dot">▪</span>
        <span class="pill-title">{{ sample.title }}</span>
        <span class="pill-badge">{{ sample.badge }}</span>
      </button>
    </div>

    <!-- Input Form (Hidden or Collapsible once results are present, but accessible via reset) -->
    <div v-if="!analysisResult || showInputCard" class="input-card">
      <div class="input-grid">
        <!-- Left: Image Upload Dropzone -->
        <div 
          class="dropzone"
          :class="{ 'has-file': Boolean(imagePreview), 'dragover': isDragging }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <input 
            type="file" 
            ref="fileInputRef" 
            accept="image/png,image/jpeg,image/jpg,image/webp" 
            class="hidden-input" 
            @change="handleFileSelect"
          />

          <div v-if="!imagePreview" class="dropzone-empty">
            <div class="upload-icon">📷</div>
            <div class="dropzone-text">
              <strong>Drag & drop campus poster image</strong>
              <span>or click to browse from device</span>
            </div>
            <div class="dropzone-hint">Supports PNG, JPG, JPEG, WebP (up to 15MB)</div>
          </div>

          <div v-else class="dropzone-preview" @click.stop>
            <img :src="imagePreview" alt="Notice Preview" class="preview-img" />
            <div class="preview-overlay">
              <span class="file-name">{{ selectedFile ? selectedFile.name : 'Sample Notice Poster' }}</span>
              <button class="remove-btn" @click.stop="clearImage" title="Remove image">✕</button>
            </div>
          </div>
        </div>

        <!-- Right: Text Announcement Input -->
        <div class="text-input-panel">
          <div class="panel-label-row">
            <span class="panel-label">Notice Text / Announcement Body</span>
            <span v-if="noticeText" class="char-count">{{ noticeText.length }} chars</span>
          </div>
          <textarea
            v-model="noticeText"
            placeholder="Paste university notice text, event circular, registration rules, or deadline announcement here..."
            class="notice-textarea"
            rows="7"
          ></textarea>
          <div class="input-footer-note">
            💡 Provide a poster image, announcement text, or both. Gemma 4 will cross-analyze both modalities.
          </div>
        </div>
      </div>

      <!-- Action Button Row -->
      <div class="submit-row">
        <button 
          class="analyze-btn" 
          :disabled="isLoading || (!selectedFile && !noticeText.trim())"
          @click="runAnalysis"
        >
          <span v-if="isLoading" class="spinner"></span>
          <span v-else class="btn-icon">⚡</span>
          <span>{{ isLoading ? 'Analyzing Notice with Gemma 4...' : 'Analyze with Gemma 4' }}</span>
        </button>

        <button 
          v-if="selectedFile || noticeText" 
          class="clear-all-btn" 
          :disabled="isLoading" 
          @click="resetAllInputs"
        >
          Clear Inputs
        </button>
      </div>

      <!-- Error State -->
      <div v-if="errorMessage" class="error-banner">
        <span class="error-icon">⚠️</span>
        <div class="error-content">
          <strong>Analysis Error</strong>
          <p>{{ errorMessage }}</p>
          <p v-if="errorHint" class="error-hint">{{ errorHint }}</p>
        </div>
        <button class="error-close-btn" @click="errorMessage = ''">✕</button>
      </div>
    </div>

    <!-- Loading State Skeleton -->
    <div v-if="isLoading" class="loading-state-card">
      <div class="loading-pulse-spinner"></div>
      <h3 class="loading-title">Gemma 4 is processing your campus notice...</h3>
      <p class="loading-step">{{ loadingStepText }}</p>
      <div class="loading-model-info">
        Model: <code>{{ activeModel }}</code> • Endpoint: <code>Google Gen AI / Gemini API</code>
      </div>
    </div>

    <!-- Results Display -->
    <div v-if="analysisResult && !isLoading" class="results-container">
      <!-- Result Action Bar -->
      <div class="result-action-bar">
        <div class="result-meta-badge">
          <span class="meta-tag model">Gemma 4</span>
          <span class="meta-tag mode" :class="analysisResultMeta.mode">
            {{ analysisResultMeta.mode === 'live_gemini_api' ? 'Verified Live Response' : 'Pre-verified Demo Output' }}
          </span>
          <span v-if="analysisResult.category" class="meta-tag category">
            {{ analysisResult.category.toUpperCase() }}
          </span>
        </div>

        <div class="result-btns">
          <button class="action-btn copy-btn" @click="copyActionChecklist">
            <span v-if="copiedChecklist">✓ Copied!</span>
            <span v-else>📋 Copy Checklist</span>
          </button>
          <button class="action-btn secondary-btn" @click="copyFullSummary">
            <span v-if="copiedSummary">✓ Copied!</span>
            <span v-else>📄 Copy Summary</span>
          </button>
          <button class="action-btn reset-btn" @click="resetForNewAnalysis">
            🔄 Analyze Another
          </button>
        </div>
      </div>

      <!-- Main Title & Summary -->
      <div class="result-header-card">
        <h1 class="extracted-title">{{ analysisResult.title || 'Campus Announcement' }}</h1>
        <div v-if="analysisResult.organizer" class="extracted-organizer">
          <span class="info-label">Organized by:</span>
          <span class="info-value">{{ analysisResult.organizer }}</span>
        </div>
        <p class="extracted-summary">{{ analysisResult.summary }}</p>
      </div>

      <!-- Key Dates & Critical Deadlines Grid -->
      <div class="dates-banner-grid">
        <div class="date-card deadline-card" :class="{ 'has-deadline': Boolean(analysisResult.registration_deadline) }">
          <div class="date-card-header">
            <span class="date-icon">⏳</span>
            <span class="date-title">REGISTRATION DEADLINE</span>
          </div>
          <div class="date-val">
            {{ analysisResult.registration_deadline || 'No deadline specified in notice' }}
          </div>
          <div class="date-subtext">Critical cutoff — verify before applying</div>
        </div>

        <div class="date-card event-card">
          <div class="date-card-header">
            <span class="date-icon">📅</span>
            <span class="date-title">EVENT DATE / TIMELINE</span>
          </div>
          <div class="date-val">
            {{ analysisResult.event_date || 'Date not explicitly specified' }}
          </div>
          <div class="date-subtext">Scheduled event date or period</div>
        </div>

        <div class="date-card venue-card">
          <div class="date-card-header">
            <span class="date-icon">📍</span>
            <span class="date-title">VENUE / LOCATION</span>
          </div>
          <div class="date-val">
            {{ analysisResult.venue || 'Venue details not specified' }}
          </div>
          <div class="date-subtext">Physical room or digital link</div>
        </div>
      </div>

      <!-- Main 2-Column Intelligence Grid -->
      <div class="intel-grid">
        <!-- Left Column: Action Items Checklist & Requirements -->
        <div class="intel-col left-col">
          <!-- Action Checklist -->
          <div class="intel-card checklist-card">
            <div class="intel-card-header">
              <span class="card-icon">✅</span>
              <h3 class="card-title">Prioritized Action Checklist</h3>
              <span class="items-count">{{ analysisResult.action_items ? analysisResult.action_items.length : 0 }} tasks</span>
            </div>

            <div v-if="analysisResult.action_items && analysisResult.action_items.length" class="checklist-items">
              <div 
                v-for="(item, idx) in analysisResult.action_items" 
                :key="idx" 
                class="checklist-row"
                :class="{ 'done': checkedItems[idx] }"
              >
                <label class="custom-checkbox-label">
                  <input type="checkbox" v-model="checkedItems[idx]" class="custom-checkbox" />
                  <span class="checkbox-indicator"></span>
                </label>
                <div class="item-content">
                  <span class="item-task" :class="{ 'strikethrough': checkedItems[idx] }">{{ item.task }}</span>
                  <div class="item-meta">
                    <span v-if="item.priority" class="priority-pill" :class="item.priority.toLowerCase()">
                      {{ item.priority.toUpperCase() }}
                    </span>
                    <span v-if="item.deadline" class="item-deadline">
                      Deadline: {{ item.deadline }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state-notice">
              No specific action checklist items found in notice.
            </div>
          </div>

          <!-- Eligibility & Prerequisites -->
          <div class="intel-card">
            <div class="intel-card-header">
              <span class="card-icon">🎓</span>
              <h3 class="card-title">Eligibility & Who Can Apply</h3>
            </div>
            <ul v-if="analysisResult.eligibility && analysisResult.eligibility.length" class="bullet-list">
              <li v-for="(rule, idx) in analysisResult.eligibility" :key="idx">
                {{ rule }}
              </li>
            </ul>
            <p v-else class="empty-state-notice">No specific eligibility constraints mentioned.</p>
          </div>

          <!-- Requirements & Preparation -->
          <div class="intel-card">
            <div class="intel-card-header">
              <span class="card-icon">📦</span>
              <h3 class="card-title">Required Documents & Materials</h3>
            </div>
            <ul v-if="analysisResult.requirements && analysisResult.requirements.length" class="bullet-list">
              <li v-for="(req, idx) in analysisResult.requirements" :key="idx">
                {{ req }}
              </li>
            </ul>
            <p v-else class="empty-state-notice">No mandatory documents explicitly listed.</p>
          </div>
        </div>

        <!-- Right Column: Uncertainties, Contact, and Source Evidence -->
        <div class="intel-col right-col">
          <!-- Critical Uncertainties & Warnings (Key Hackathon Requirement) -->
          <div class="intel-card warnings-card">
            <div class="intel-card-header warning-header">
              <span class="card-icon">⚠️</span>
              <h3 class="card-title">Uncertainties & Ambiguities to Verify</h3>
            </div>
            <div class="warning-explanation">
              Gemma 4 identified the following missing or unstated details in the notice:
            </div>
            <ul v-if="analysisResult.uncertainties && analysisResult.uncertainties.length" class="uncertainty-list">
              <li v-for="(item, idx) in analysisResult.uncertainties" :key="idx">
                {{ item }}
              </li>
            </ul>
            <div v-else class="clean-pass-notice">
              ✓ All standard details appear explicitly specified in the supplied material.
            </div>
            <div class="official-safety-note">
              <strong>Administrative Safety Rule:</strong> Always confirm critical fee amounts, bank accounts, and gate deadlines against official university notices.
            </div>
          </div>

          <!-- Important Milestones Schedule -->
          <div v-if="analysisResult.important_dates && analysisResult.important_dates.length" class="intel-card">
            <div class="intel-card-header">
              <span class="card-icon">⏱️</span>
              <h3 class="card-title">Key Milestones Schedule</h3>
            </div>
            <div class="milestones-timeline">
              <div v-for="(d, idx) in analysisResult.important_dates" :key="idx" class="timeline-row">
                <span class="timeline-dot"></span>
                <div class="timeline-info">
                  <strong class="timeline-label">{{ d.label }}</strong>
                  <span class="timeline-date">{{ d.date }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="intel-card">
            <div class="intel-card-header">
              <span class="card-icon">📞</span>
              <h3 class="card-title">Organizer Contacts</h3>
            </div>
            <div v-if="analysisResult.contact_information && analysisResult.contact_information.length" class="contact-rows">
              <div v-for="(c, idx) in analysisResult.contact_information" :key="idx" class="contact-pill">
                <span class="contact-dept">{{ c.name_or_dept }}:</span>
                <span class="contact-val">{{ c.contact }}</span>
              </div>
            </div>
            <p v-else class="empty-state-notice">No contact numbers or emails provided.</p>
          </div>

          <!-- Verbatim Source Evidence (Fact Transparency) -->
          <div class="intel-card evidence-card">
            <div class="intel-card-header">
              <span class="card-icon">🔍</span>
              <h3 class="card-title">Direct Source Quotes (Evidence)</h3>
            </div>
            <div class="evidence-quotes">
              <blockquote v-for="(ev, idx) in analysisResult.source_evidence" :key="idx" class="source-quote">
                "{{ ev }}"
              </blockquote>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { analyzeNotice, getNoticeSamples, getNoticeHealth } from '@/api/notice.js'

// State
const activeModel = ref('gemma-4-26b-a4b-it')
const isDemo = ref(false)
const selectedFile = ref(null)
const imagePreview = ref(null)
const noticeText = ref('')
const isDragging = ref(false)
const fileInputRef = ref(null)

const sampleList = ref([])
const selectedSampleId = ref('')

const isLoading = ref(false)
const loadingStepText = ref('Connecting to Gemma 4...')
const errorMessage = ref('')
const errorHint = ref('')

const analysisResult = ref(null)
const analysisResultMeta = ref({})
const checkedItems = ref({})
const copiedChecklist = ref(false)
const copiedSummary = ref(false)
const showInputCard = ref(true)

// Fetch Health and Samples on load
onMounted(async () => {
  try {
    const health = await getNoticeHealth()
    if (health?.gemma?.model) {
      activeModel.value = health.gemma.model
    }
    // If backend is not configured with GEMINI_API_KEY, auto-enable demo mode toggle default
    if (health?.gemma?.configured === false) {
      isDemo.value = true
    }
  } catch (err) {
    console.warn('Notice health check unavailable:', err)
  }

  try {
    const sampleRes = await getNoticeSamples()
    if (sampleRes?.samples) {
      sampleList.value = sampleRes.samples
    }
  } catch (err) {
    console.warn('Notice samples check unavailable:', err)
  }
})

// Trigger hidden file picker
const triggerFileInput = () => {
  if (fileInputRef.value) {
    fileInputRef.value.click()
  }
}

// Handle file select
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    setFile(file)
  }
}

// Handle Drag & Drop
const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer?.files[0]
  if (file) {
    setFile(file)
  }
}

// Set file and preview
const setFile = (file) => {
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Please select a valid image file (PNG, JPG, JPEG, WebP).'
    return
  }
  if (file.size > 15 * 1024 * 1024) {
    errorMessage.value = 'File is too large. Maximum size is 15MB.'
    return
  }
  errorMessage.value = ''
  selectedFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

// Clear selected image
const clearImage = () => {
  selectedFile.value = null
  imagePreview.value = null
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}

// Reset all inputs
const resetAllInputs = () => {
  clearImage()
  noticeText.value = ''
  selectedSampleId.value = ''
  errorMessage.value = ''
}

// Load pre-configured sample
const loadSample = (sample) => {
  selectedSampleId.value = sample.id
  noticeText.value = sample.sample_text || ''
  clearImage()
  // Run directly or fill input
  runAnalysisWithSample(sample.id)
}

// Run Analysis
const runAnalysis = async () => {
  if (!selectedFile.value && !noticeText.value.trim() && !selectedSampleId.value) {
    errorMessage.value = 'Please upload a notice poster or paste announcement text.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  errorHint.value = ''
  loadingStepText.value = 'Preparing notice content and validating media...'

  setTimeout(() => {
    if (isLoading.value) loadingStepText.value = `Invoking ${activeModel.value} via Gemini API...`
  }, 1200)

  setTimeout(() => {
    if (isLoading.value) loadingStepText.value = 'Extracting deadlines, requirements, and prioritized actions...'
  }, 3200)

  try {
    let payload
    if (selectedFile.value) {
      payload = new FormData()
      payload.append('image', selectedFile.value)
      if (noticeText.value) payload.append('text', noticeText.value)
      payload.append('demo', String(isDemo.value))
      if (selectedSampleId.value) payload.append('sample_id', selectedSampleId.value)
    } else {
      payload = {
        text: noticeText.value,
        demo: isDemo.value,
        sample_id: selectedSampleId.value || undefined
      }
    }

    const res = await analyzeNotice(payload)
    if (res?.success && res.data) {
      analysisResult.value = res.data
      analysisResultMeta.value = res.meta || {}
      checkedItems.value = {}
      showInputCard.value = false
    } else {
      throw new Error(res?.error || 'Failed to analyze notice.')
    }
  } catch (err) {
    console.error('Notice analysis error:', err)
    errorMessage.value = err.message || 'An error occurred during notice analysis.'
    if (err.message && err.message.includes('GEMINI_API_KEY')) {
      errorHint.value = 'You can switch to Demo Mode using the toggle above to test the full structured experience.'
    }
  } finally {
    isLoading.value = false
  }
}

// Run direct with sample id
const runAnalysisWithSample = async (sampleId) => {
  isLoading.value = true
  errorMessage.value = ''
  loadingStepText.value = `Loading verified analysis for preset: ${sampleId}...`

  try {
    const res = await analyzeNotice({
      demo: true,
      sample_id: sampleId
    })
    if (res?.success && res.data) {
      analysisResult.value = res.data
      analysisResultMeta.value = res.meta || {}
      checkedItems.value = {}
      showInputCard.value = false
    }
  } catch (err) {
    errorMessage.value = err.message || 'Failed to load sample.'
  } finally {
    isLoading.value = false
  }
}

// Reset view for another notice
const resetForNewAnalysis = () => {
  showInputCard.value = true
  analysisResult.value = null
  checkedItems.value = {}
}

// Copy Action Checklist to clipboard
const copyActionChecklist = async () => {
  if (!analysisResult.value?.action_items) return
  const title = analysisResult.value.title || 'Campus Notice Action Plan'
  const lines = [
    `ACTION CHECKLIST: ${title}`,
    `Deadline: ${analysisResult.value.registration_deadline || 'N/A'}`,
    `Venue: ${analysisResult.value.venue || 'N/A'}`,
    '',
    'TASKS:'
  ]

  analysisResult.value.action_items.forEach((item, i) => {
    const status = checkedItems.value[i] ? '[x]' : '[ ]'
    const prio = item.priority ? `(${item.priority.toUpperCase()})` : ''
    const dl = item.deadline ? `[Due: ${item.deadline}]` : ''
    lines.push(`${status} ${i + 1}. ${item.task} ${prio} ${dl}`)
  })

  lines.push('')
  lines.push('Generated via CampusPulse AI (Powered by Gemma 4)')

  try {
    await navigator.clipboard.writeText(lines.join('\n'))
    copiedChecklist.value = true
    setTimeout(() => { copiedChecklist.value = false }, 2500)
  } catch (e) {
    console.error('Clipboard copy error:', e)
  }
}

// Copy Full Executive Summary
const copyFullSummary = async () => {
  if (!analysisResult.value) return
  const r = analysisResult.value
  const text = `
CAMPUSPULSE AI — NOTICE INTELLIGENCE SUMMARY
Title: ${r.title || 'Campus Announcement'}
Category: ${r.category || 'General'}
Organizer: ${r.organizer || 'Unspecified'}
Event Date: ${r.event_date || 'N/A'}
Registration Deadline: ${r.registration_deadline || 'N/A'}
Venue: ${r.venue || 'N/A'}

OVERVIEW:
${r.summary}

ELIGIBILITY:
${(r.eligibility || []).map(e => `• ${e}`).join('\n')}

REQUIREMENTS:
${(r.requirements || []).map(req => `• ${req}`).join('\n')}

UNCERTAINTIES & VERIFICATION:
${(r.uncertainties || []).map(u => `! ${u}`).join('\n')}
`.trim()

  try {
    await navigator.clipboard.writeText(text)
    copiedSummary.value = true
    setTimeout(() => { copiedSummary.value = false }, 2500)
  } catch (e) {
    console.error('Clipboard copy error:', e)
  }
}
</script>

<style scoped>
.notice-to-action {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Inter', -apple-system, sans-serif;
  color: #0f172a;
}

/* Header */
.nta-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.nta-badge-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.engine-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #0f172a;
  color: #38bdf8;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #38bdf8;
  box-shadow: 0 0 8px #38bdf8;
}

.model-tag {
  background: #f1f5f9;
  color: #475569;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 3px 8px;
  border-radius: 4px;
  border: 1px solid #cbd5e1;
}

.mode-indicator {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  text-transform: uppercase;
}

.mode-indicator.live {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #86efac;
}

.mode-indicator.demo {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.nta-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.85rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 6px 0;
}

.nta-subtitle {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
  max-width: 680px;
  line-height: 1.5;
}

.demo-toggle-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #334155;
  transition: all 0.2s;
}

.demo-toggle-label:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.demo-checkbox {
  cursor: pointer;
  accent-color: #0284c7;
}

/* Samples Bar */
.samples-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  background: #f8fafc;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px dashed #cbd5e1;
}

.samples-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #475569;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
}

.sample-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  color: #1e293b;
  cursor: pointer;
  transition: all 0.15s;
}

.sample-pill-btn:hover {
  border-color: #0284c7;
  background: #f0f9ff;
  color: #0369a1;
}

.sample-pill-btn.active {
  background: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
}

.pill-dot {
  font-size: 0.7rem;
  color: #0284c7;
}

.sample-pill-btn.active .pill-dot {
  color: #ffffff;
}

.pill-badge {
  font-size: 0.68rem;
  background: #f1f5f9;
  color: #475569;
  padding: 1px 6px;
  border-radius: 10px;
}

.sample-pill-btn.active .pill-badge {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* Input Card */
.input-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
  margin-bottom: 24px;
}

.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

@media (max-width: 860px) {
  .input-grid {
    grid-template-columns: 1fr;
  }
}

/* Dropzone */
.dropzone {
  border: 2px dashed #cbd5e1;
  border-radius: 10px;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.2s ease;
}

.dropzone:hover, .dropzone.dragover {
  border-color: #0284c7;
  background: #f0f9ff;
}

.hidden-input {
  display: none;
}

.dropzone-empty {
  text-align: center;
  padding: 20px;
}

.upload-icon {
  font-size: 2.5rem;
  margin-bottom: 8px;
}

.dropzone-text strong {
  display: block;
  font-size: 0.95rem;
  color: #1e293b;
  margin-bottom: 4px;
}

.dropzone-text span {
  font-size: 0.82rem;
  color: #64748b;
}

.dropzone-hint {
  margin-top: 10px;
  font-size: 0.75rem;
  color: #94a3b8;
  font-family: 'JetBrains Mono', monospace;
}

.dropzone-preview {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f172a;
}

.preview-img {
  max-width: 100%;
  max-height: 220px;
  object-fit: contain;
}

.preview-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(15, 23, 42, 0.85);
  padding: 6px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.file-name {
  color: #f8fafc;
  font-size: 0.78rem;
  font-family: 'JetBrains Mono', monospace;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-btn {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  font-size: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Text Input Panel */
.text-input-panel {
  display: flex;
  flex-direction: column;
}

.panel-label-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.panel-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

.char-count {
  font-size: 0.75rem;
  color: #94a3b8;
  font-family: 'JetBrains Mono', monospace;
}

.notice-textarea {
  width: 100%;
  flex: 1;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  color: #0f172a;
  background: #ffffff;
  resize: vertical;
  line-height: 1.5;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.notice-textarea:focus {
  outline: none;
  border-color: #0284c7;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.1);
}

.input-footer-note {
  margin-top: 8px;
  font-size: 0.76rem;
  color: #64748b;
}

/* Submit Row */
.submit-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.analyze-btn {
  background: #0284c7;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 0.95rem;
  font-weight: 600;
  font-family: 'Space Grotesk', sans-serif;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.analyze-btn:hover:not(:disabled) {
  background: #0369a1;
  box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
}

.analyze-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.clear-all-btn {
  background: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 18px;
  font-size: 0.88rem;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-all-btn:hover:not(:disabled) {
  background: #f1f5f9;
  color: #0f172a;
}

/* Error Banner */
.error-banner {
  margin-top: 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.error-icon {
  font-size: 1.2rem;
}

.error-content {
  flex: 1;
  font-size: 0.88rem;
  color: #991b1b;
}

.error-content strong {
  display: block;
  margin-bottom: 2px;
}

.error-hint {
  margin-top: 4px;
  font-size: 0.8rem;
  color: #b91c1c;
}

.error-close-btn {
  background: none;
  border: none;
  color: #991b1b;
  cursor: pointer;
  font-size: 1rem;
}

/* Loading Card */
.loading-state-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  margin-bottom: 24px;
}

.loading-pulse-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  border: 4px solid #e2e8f0;
  border-top-color: #0284c7;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-title {
  font-size: 1.25rem;
  color: #0f172a;
  margin: 0 0 8px 0;
  font-family: 'Space Grotesk', sans-serif;
}

.loading-step {
  font-size: 0.95rem;
  color: #0284c7;
  font-weight: 500;
  margin: 0 0 16px 0;
}

.loading-model-info {
  font-size: 0.75rem;
  color: #94a3b8;
  font-family: 'JetBrains Mono', monospace;
}

.loading-model-info code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
}

/* Results Display */
.results-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Result Action Bar */
.result-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  background: #f8fafc;
  padding: 12px 18px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.result-meta-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.meta-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 4px;
}

.meta-tag.model {
  background: #0f172a;
  color: #38bdf8;
}

.meta-tag.mode.live_gemini_api {
  background: #dcfce7;
  color: #166534;
}

.meta-tag.mode.demo_simulation {
  background: #fef3c7;
  color: #92400e;
}

.meta-tag.category {
  background: #e0f2fe;
  color: #0369a1;
}

.result-btns {
  display: flex;
  gap: 8px;
}

.action-btn {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  transition: all 0.15s;
}

.copy-btn {
  background: #0284c7;
  color: white;
}

.copy-btn:hover {
  background: #0369a1;
}

.secondary-btn {
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #cbd5e1;
}

.secondary-btn:hover {
  background: #e2e8f0;
}

.reset-btn {
  background: transparent;
  color: #64748b;
  border: 1px solid #cbd5e1;
}

.reset-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

/* Extracted Title Card */
.result-header-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
}

.extracted-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  line-height: 1.25;
}

.extracted-organizer {
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.info-label {
  color: #64748b;
  margin-right: 6px;
}

.info-value {
  color: #0f172a;
  font-weight: 600;
}

.extracted-summary {
  font-size: 1rem;
  color: #334155;
  line-height: 1.6;
  margin: 0;
}

/* Dates Grid */
.dates-banner-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 860px) {
  .dates-banner-grid {
    grid-template-columns: 1fr;
  }
}

.date-card {
  border-radius: 10px;
  padding: 16px;
  border: 1px solid #e2e8f0;
}

.date-card.deadline-card {
  background: #fff1f2;
  border-color: #fecdd3;
}

.date-card.event-card {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.date-card.venue-card {
  background: #f8fafc;
  border-color: #e2e8f0;
}

.date-card-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.date-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.deadline-card .date-title { color: #e11d48; }
.event-card .date-title { color: #16a34a; }
.venue-card .date-title { color: #475569; }

.date-val {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
  line-height: 1.3;
}

.deadline-card .date-val { color: #9f1239; }

.date-subtext {
  font-size: 0.75rem;
  color: #64748b;
}

/* Main Intel 2-Col Grid */
.intel-grid {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 20px;
}

@media (max-width: 960px) {
  .intel-grid {
    grid-template-columns: 1fr;
  }
}

.intel-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.intel-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
}

.intel-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  flex: 1;
}

.items-count {
  font-size: 0.75rem;
  background: #f1f5f9;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
  padding: 2px 8px;
  border-radius: 12px;
}

/* Checklist Items */
.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checklist-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.15s;
}

.checklist-row:hover {
  background: #f1f5f9;
}

.checklist-row.done {
  background: #f8fafc;
  opacity: 0.6;
}

.custom-checkbox-label {
  cursor: pointer;
  margin-top: 2px;
}

.custom-checkbox {
  cursor: pointer;
  width: 18px;
  height: 18px;
  accent-color: #0284c7;
}

.item-content {
  flex: 1;
}

.item-task {
  font-size: 0.95rem;
  font-weight: 500;
  color: #0f172a;
  line-height: 1.4;
  display: block;
}

.item-task.strikethrough {
  text-decoration: line-through;
  color: #94a3b8;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.priority-pill {
  font-size: 0.68rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
}

.priority-pill.high {
  background: #fee2e2;
  color: #b91c1c;
}

.priority-pill.medium {
  background: #fef3c7;
  color: #b45309;
}

.priority-pill.low {
  background: #e0f2fe;
  color: #0369a1;
}

.item-deadline {
  font-size: 0.75rem;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
}

/* Bullet List */
.bullet-list {
  margin: 0;
  padding-left: 20px;
  color: #334155;
  font-size: 0.92rem;
  line-height: 1.6;
}

.bullet-list li {
  margin-bottom: 6px;
}

/* Warnings & Uncertainties Card */
.warnings-card {
  background: #fffbeb;
  border-color: #fde68a;
}

.warning-header .card-title {
  color: #92400e;
}

.warning-explanation {
  font-size: 0.85rem;
  color: #78350f;
  margin-bottom: 12px;
}

.uncertainty-list {
  margin: 0 0 16px 0;
  padding-left: 18px;
  color: #92400e;
  font-size: 0.88rem;
  line-height: 1.5;
}

.uncertainty-list li {
  margin-bottom: 6px;
}

.clean-pass-notice {
  font-size: 0.85rem;
  color: #166534;
  background: #dcfce7;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 12px;
}

.official-safety-note {
  font-size: 0.78rem;
  color: #b45309;
  background: rgba(254, 243, 199, 0.7);
  border-left: 3px solid #f59e0b;
  padding: 8px 10px;
  border-radius: 0 4px 4px 0;
}

/* Milestones Timeline */
.milestones-timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.timeline-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.timeline-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #0284c7;
  margin-top: 6px;
}

.timeline-info {
  display: flex;
  flex-direction: column;
}

.timeline-label {
  font-size: 0.88rem;
  color: #0f172a;
}

.timeline-date {
  font-size: 0.78rem;
  color: #64748b;
  font-family: 'JetBrains Mono', monospace;
}

/* Contact Details */
.contact-rows {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.contact-pill {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
}

.contact-dept {
  font-weight: 600;
  color: #334155;
  margin-right: 6px;
}

.contact-val {
  color: #0284c7;
  font-family: 'JetBrains Mono', monospace;
}

/* Evidence Card */
.evidence-card {
  background: #f8fafc;
}

.evidence-quotes {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.source-quote {
  margin: 0;
  font-size: 0.82rem;
  color: #475569;
  background: #ffffff;
  border-left: 3px solid #94a3b8;
  padding: 6px 10px;
  border-radius: 0 4px 4px 0;
  font-style: italic;
  line-height: 1.4;
}

.empty-state-notice {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 0;
  font-style: italic;
}
</style>
