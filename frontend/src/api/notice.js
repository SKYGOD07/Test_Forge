import request from './index'

/**
 * Notice-to-Action API Client
 */

/**
 * Check Notice Service health and Gemma 4 model status
 */
export function getNoticeHealth() {
  return request({
    url: '/api/notice/health',
    method: 'get'
  })
}

/**
 * Fetch pre-packaged campus notice demo samples
 */
export function getNoticeSamples() {
  return request({
    url: '/api/notice/samples',
    method: 'get'
  })
}

/**
 * Analyze a campus notice with Gemma 4
 * @param {FormData|Object} data - FormData (for file uploads) or JSON payload
 */
export function analyzeNotice(data) {
  const isFormData = data instanceof FormData
  return request({
    url: '/api/notice/analyze',
    method: 'post',
    data,
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : { 'Content-Type': 'application/json' }
  })
}
