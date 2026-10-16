<template>
  <div class="home-container">
    <!-- Top Navigation Bar -->
    <nav class="navbar">
      <div class="nav-left">
        <div class="nav-brand" @click="currentTab = 'notice'">
          <img src="/logo.svg" alt="CampusPulse AI Logo" class="nav-logo-icon" />
          <span class="brand-text">CAMPUSPULSE AI</span>
        </div>
        <span class="nav-tagline">{{ $t('nav.tagline') }}</span>
      </div>

      <div class="nav-center-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'notice' }" 
          @click="currentTab = 'notice'"
        >
          <span class="tab-icon">⚡</span>
          <span>Notice-to-Action</span>
          <span class="gemma-pill">Gemma 4</span>
        </button>

        <button 
          class="tab-btn" 
          :class="{ active: currentTab === 'sandbox' }" 
          @click="currentTab = 'sandbox'"
        >
          <span class="tab-icon">🧪</span>
          <span>Campus Reaction Sandbox</span>
        </button>
      </div>

      <div class="nav-links">
        <LanguageSwitcher />
        <a 
          href="https://www.mlh.com/events/hacktoberfest-hack-day-gwalior-x-itm-university" 
          target="_blank" 
          class="event-link"
          title="MLH Hacktoberfest Hack Day Gwalior x ITM University"
        >
          {{ $t('nav.eventLink') }} <span class="arrow">↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- TAB 1: Notice-to-Action (Primary Feature) -->
      <section v-if="currentTab === 'notice'" class="feature-section">
        <!-- Hero Header -->
        <div class="hero-strip">
          <div class="hero-strip-left">
            <div class="tag-row">
              <span class="hackathon-tag">MLH HACKTOBERFEST HACK DAY GWALIOR</span>
              <span class="gemma-prize-tag">Best Use of Gemma 4</span>
            </div>
            <h1 class="main-hero-title">
              Turn Campus Notices<br>
              <span class="gradient-text">Into Clear Actions</span>
            </h1>
            <p class="hero-strip-desc">
              Transform confusing event posters, exam deadlines, circulars, and university policy memos into verified, prioritized action checklists with Gemma 4 multimodal intelligence.
            </p>
          </div>
        </div>

        <!-- The Notice-to-Action Interactive Workspace -->
        <NoticeToAction />
      </section>

      <!-- TAB 2: Campus Reaction Sandbox (Inherited Multi-Agent Simulation Engine) -->
      <section v-show="currentTab === 'sandbox'" class="sandbox-section">
        <!-- Sandbox Hero -->
        <div class="sandbox-hero">
          <div class="sandbox-hero-left">
            <div class="tag-row">
              <span class="sandbox-tag">CAMPUS REACTION SIMULATION</span>
              <span class="version-text">Multi-Agent Sandbox</span>
            </div>
            
            <h2 class="sandbox-title">
              Simulate Student Responses<br>
              <span class="gradient-text">Before Policy Rollouts</span>
            </h2>
            
            <p class="sandbox-desc">
              Rehearse how student bodies, faculty departments, and clubs react to notices. Upload official announcements and seed materials to simulate discussions and forecast campus impact.
            </p>
          </div>
        </div>

        <!-- Dashboard Section: Status & Simulation Console -->
        <div class="dashboard-section">
          <!-- Left Panel: Pipeline Info -->
          <div class="left-panel">
            <div class="panel-header">
              <span class="status-dot">■</span> {{ $t('home.systemStatus') }}
            </div>
            
            <h2 class="section-title">{{ $t('home.systemReady') }}</h2>
            <p class="section-desc">
              {{ $t('home.systemReadyDesc') }}
            </p>
            
            <!-- Metrics Row -->
            <div class="metrics-row">
              <div class="metric-card">
                <div class="metric-value">{{ $t('home.metricLowCost') }}</div>
                <div class="metric-label">{{ $t('home.metricLowCostDesc') }}</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">{{ $t('home.metricHighAvail') }}</div>
                <div class="metric-label">{{ $t('home.metricHighAvailDesc') }}</div>
              </div>
            </div>

            <!-- Workflow Sequence -->
            <div class="steps-container">
              <div class="steps-header">
                <span class="diamond-icon">◇</span> {{ $t('home.workflowSequence') }}
              </div>
              <div class="workflow-list">
                <div class="workflow-item">
                  <span class="step-num">01</span>
                  <div class="step-info">
                    <div class="step-title">{{ $t('home.step01Title') }}</div>
                    <div class="step-desc">{{ $t('home.step01Desc') }}</div>
                  </div>
                </div>
                <div class="workflow-item">
                  <span class="step-num">02</span>
                  <div class="step-info">
                    <div class="step-title">{{ $t('home.step02Title') }}</div>
                    <div class="step-desc">{{ $t('home.step02Desc') }}</div>
                  </div>
                </div>
                <div class="workflow-item">
                  <span class="step-num">03</span>
                  <div class="step-info">
                    <div class="step-title">{{ $t('home.step03Title') }}</div>
                    <div class="step-desc">{{ $t('home.step03Desc') }}</div>
                  </div>
                </div>
                <div class="workflow-item">
                  <span class="step-num">04</span>
                  <div class="step-info">
                    <div class="step-title">{{ $t('home.step04Title') }}</div>
                    <div class="step-desc">{{ $t('home.step04Desc') }}</div>
                  </div>
                </div>
                <div class="workflow-item">
                  <span class="step-num">05</span>
                  <div class="step-info">
                    <div class="step-title">{{ $t('home.step05Title') }}</div>
                    <div class="step-desc">{{ $t('home.step05Desc') }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Panel: Interactive Console -->
          <div class="right-panel">
            <div class="console-box">
              <!-- Upload Section -->
              <div class="console-section">
                <div class="console-header">
                  <span class="console-label">{{ $t('home.realitySeed') }}</span>
                  <span class="console-meta">{{ $t('home.supportedFormats') }}</span>
                </div>
                
                <div 
                  class="upload-zone"
                  :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                  @dragover.prevent="handleDragOver"
                  @dragleave.prevent="handleDragLeave"
                  @drop.prevent="handleDrop"
                  @click="triggerFileInput"
                >
                  <input
                    ref="fileInput"
                    type="file"
                    multiple
                    accept=".pdf,.md,.txt,.png,.jpg,.jpeg,.webp,image/*"
                    @change="handleFileSelect"
                    style="display: none"
                    :disabled="loading"
                  />
                  
                  <div v-if="files.length === 0" class="upload-placeholder">
                    <div class="upload-icon">↑</div>
                    <div class="upload-title">{{ $t('home.dragToUpload') }}</div>
                    <div class="upload-hint">{{ $t('home.orBrowse') }}</div>
                  </div>
                  
                  <div v-else class="file-list">
                    <div v-for="(file, index) in files" :key="index" class="file-item">
                      <span class="file-icon">{{ isImageFile(file) ? '🖼️' : '📄' }}</span>
                      <span class="file-name">{{ file.name }}</span>
                      <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Console Divider -->
              <div class="console-divider">
                <span>{{ $t('home.inputParams') }}</span>
              </div>

              <!-- Input Area -->
              <div class="console-section">
                <div class="console-header">
                  <span class="console-label">{{ $t('home.simulationPrompt') }}</span>
                </div>
                <div class="input-wrapper">
                  <textarea
                    v-model="formData.simulationRequirement"
                    :placeholder="$t('home.promptPlaceholder')"
                    class="console-textarea"
                    rows="4"
                    :disabled="loading"
                  ></textarea>
                </div>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="error-message">
                {{ error }}
              </div>

              <!-- Action Bar -->
              <div class="console-action">
                <div class="action-info">
                  <span class="pulse-dot"></span>
                  <span class="engine-text">{{ $t('home.engineBadge') }}</span>
                </div>
                <button
                  class="start-btn"
                  :class="{ 'is-loading': loading }"
                  :disabled="!canSubmit || loading"
                  @click="startSimulation"
                >
                  <span v-if="!loading">{{ $t('home.startEngine') }}</span>
                  <span v-else>{{ $t('home.initializing') }}</span>
                  <span class="btn-arrow">→</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- History Projects Database -->
        <HistoryDatabase />
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NoticeToAction from '../components/NoticeToAction.vue'
import HistoryDatabase from '../components/HistoryDatabase.vue'
import LanguageSwitcher from '../components/LanguageSwitcher.vue'

const router = useRouter()

// Active Navigation Tab: 'notice' (Flagship) or 'sandbox'
const currentTab = ref('notice')

// Form data for simulation sandbox
const formData = ref({
  simulationRequirement: ''
})

const files = ref([])
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)
const fileInput = ref(null)

const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

const handleDragOver = () => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = () => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

const isImageFile = (file) => {
  if (file?.type && file.type.startsWith('image/')) return true
  const ext = (file?.name || '').split('.').pop().toLowerCase()
  return ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'].includes(ext)
}

const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt', 'png', 'jpg', 'jpeg', 'webp'].includes(ext) || (file.type && file.type.startsWith('image/'))
  })
  files.value.push(...validFiles)
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const startSimulation = async () => {
  if (!canSubmit.value || loading.value) return
  loading.value = true
  error.value = ''

  try {
    const { setPendingUpload } = await import('../store/pendingUpload')
    setPendingUpload(files.value, formData.value.simulationRequirement)
    router.push({ name: 'Process', params: { projectId: 'new' } })
  } catch (err) {
    console.error('Failed to start simulation:', err)
    error.value = err.message || 'Failed to initialize simulation.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-bg: #FAFAFA;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: #ffffff;
  font-family: 'Inter', -apple-system, sans-serif;
  color: #0f172a;
}

/* Navbar */
.navbar {
  height: 64px;
  background: #0f172a;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  border-bottom: 1px solid #1e293b;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.nav-logo-icon {
  width: 28px;
  height: 28px;
}

.brand-text {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  letter-spacing: 0.05em;
  font-size: 1.15rem;
  color: #ffffff;
}

.nav-tagline {
  font-size: 0.78rem;
  color: #94a3b8;
  border-left: 1px solid #334155;
  padding-left: 14px;
  font-style: italic;
}

@media (max-width: 900px) {
  .nav-tagline { display: none; }
}

.nav-center-tabs {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #1e293b;
  padding: 4px;
  border-radius: 8px;
}

.tab-btn {
  background: transparent;
  color: #94a3b8;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #ffffff;
}

.tab-btn.active {
  background: #0284c7;
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.4);
}

.tab-icon {
  font-size: 0.9rem;
}

.gemma-pill {
  font-size: 0.65rem;
  font-family: 'JetBrains Mono', monospace;
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  padding: 1px 6px;
  border-radius: 10px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 14px;
}

.event-link {
  color: #38bdf8;
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border: 1px solid rgba(56, 189, 248, 0.3);
  border-radius: 6px;
  transition: all 0.2s;
}

.event-link:hover {
  background: rgba(56, 189, 248, 0.1);
  border-color: #38bdf8;
}

/* Main Content */
.main-content {
  max-width: 1300px;
  margin: 0 auto;
  padding: 40px 24px;
}

/* Hero Strip */
.hero-strip {
  margin-bottom: 28px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.hackathon-tag {
  background: #0f172a;
  color: #f59e0b;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.gemma-prize-tag {
  background: #e0f2fe;
  color: #0369a1;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}

.main-hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.8rem;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: #0f172a;
  margin: 0 0 10px 0;
}

.gradient-text {
  background: linear-gradient(90deg, #0284c7 0%, #2563eb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-strip-desc {
  font-size: 1rem;
  color: #64748b;
  max-width: 720px;
  line-height: 1.5;
  margin: 0;
}

/* Sandbox Section */
.sandbox-hero {
  margin-bottom: 30px;
}

.sandbox-tag {
  background: #f1f5f9;
  color: #475569;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}

.version-text {
  color: #94a3b8;
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
}

.sandbox-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: #0f172a;
  margin: 8px 0;
}

.sandbox-desc {
  font-size: 0.95rem;
  color: #64748b;
  max-width: 700px;
  line-height: 1.5;
}

/* Dashboard Section (Sandbox) */
.dashboard-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 40px;
}

@media (max-width: 900px) {
  .dashboard-section {
    grid-template-columns: 1fr;
  }
}

.left-panel {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
}

.panel-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  color: #10b981;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 6px 0;
}

.section-desc {
  font-size: 0.88rem;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 20px;
}

.metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.metric-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.15rem;
  font-weight: 700;
  color: #0284c7;
}

.metric-label {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 2px;
}

.steps-container {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
}

.steps-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.diamond-icon {
  color: #0284c7;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: #0284c7;
  background: #e0f2fe;
  padding: 2px 6px;
  border-radius: 4px;
}

.step-info {
  display: flex;
  flex-direction: column;
}

.step-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #0f172a;
}

.step-desc {
  font-size: 0.75rem;
  color: #64748b;
}

/* Right Panel Console */
.right-panel {
  display: flex;
  flex-direction: column;
}

.console-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
}

.console-section {
  margin-bottom: 16px;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.console-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
}

.console-meta {
  font-size: 0.75rem;
  color: #94a3b8;
}

.upload-zone {
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  background: #f8fafc;
  transition: all 0.2s;
}

.upload-zone:hover, .upload-zone.drag-over {
  border-color: #0284c7;
  background: #f0f9ff;
}

.upload-icon {
  font-size: 1.5rem;
  color: #0284c7;
  margin-bottom: 4px;
}

.upload-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1e293b;
}

.upload-hint {
  font-size: 0.78rem;
  color: #64748b;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  font-size: 0.82rem;
}

.file-name {
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-btn {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 1rem;
}

.console-divider {
  border-top: 1px solid #e2e8f0;
  margin: 16px 0;
  text-align: center;
  position: relative;
}

.console-divider span {
  position: relative;
  top: -10px;
  background: #ffffff;
  padding: 0 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #94a3b8;
}

.console-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  color: #0f172a;
  box-sizing: border-box;
  resize: vertical;
}

.console-textarea:focus {
  outline: none;
  border-color: #0284c7;
}

.console-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
}

.action-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
}

.engine-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #64748b;
}

.start-btn {
  background: #0284c7;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.start-btn:hover:not(:disabled) {
  background: #0369a1;
}

.start-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  font-size: 0.8rem;
  margin-top: 8px;
}
</style>
