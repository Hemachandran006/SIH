import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

class API {
  private axios = axios.create({ baseURL })
  constructor() {
    // Initialize Authorization header from localStorage on first load
    try {
      const saved = localStorage.getItem('token')
      if (saved) this.setToken(saved)
    } catch {
      // ignore if localStorage not available
    }

    this.axios.interceptors.response.use(
      (res) => res,
      (err) => {
        if (err.response?.status === 401) {
          // You can force logout or show a toast here if desired
        }
        return Promise.reject(err)
      }
    )
  }

  setToken(token: string | null) {
    if (token) this.axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    else delete this.axios.defaults.headers.common['Authorization']
  }

  // Auth
  async login(email: string, password: string) {
    const { data } = await this.axios.post('/auth/login', { email, password })
    return data as { access_token: string }
  }
  async signup(email: string, password: string, full_name?: string) {
    const { data } = await this.axios.post('/auth/signup', { email, password, full_name })
    return data as { access_token: string }
  }

  // Devices
  async scanDevice() {
    const { data } = await this.axios.post('/devices/scan')
    return data.device as { id: number; device_uid: string; name: string; type: string }
  }

  // Wipes
  async startWipe(device_uid: string, method: string, size_mb?: number) {
    const payload: any = { device_uid, method }
    if (size_mb) payload.size_mb = size_mb
    const { data } = await this.axios.post('/wipes/start', payload)
    return data as {
      id: number; device_uid: string; method: string; status: string; started_at: string; completed_at?: string
    }
  }
  async verifyWipe(wipe_id: number) {
    const { data } = await this.axios.post('/wipes/verify', { wipe_id })
    return data
  }
  async getWipes() {
    const { data } = await this.axios.get('/wipes')
    return data.items as Array<{
      id: number; device_uid: string; method: string; status: string; started_at: string; completed_at?: string; certificate_url?: string
    }>
  }

  // Certificates
  certificateUrl(wipe_id: number) {
    return `${baseURL}/certificates/${wipe_id}.pdf`
  }
  async downloadCertificate(wipe_id: number) {
    const res = await this.axios.get(`/certificates/${wipe_id}.pdf`, { responseType: 'blob' })
    const disposition = res.headers['content-disposition'] as string | undefined
    let filename = `wipechain-certificate-${wipe_id}.pdf`
    if (disposition) {
      const match = /filename\*?=(?:UTF-8'')?["']?([^"';\n]+)["']?/i.exec(disposition)
      if (match?.[1]) filename = decodeURIComponent(match[1])
    }
    return { blob: res.data as Blob, filename }
  }
}

export const api = new API()