import type { Analysis, AuthResponse, Recycler, User } from '../types'
const baseUrl = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000/api'
const tokenKey = 'ewaste-session-token'
export const getToken = () => localStorage.getItem(tokenKey)
export const saveToken = (token: string) => localStorage.setItem(tokenKey, token)
export const clearToken = () => localStorage.removeItem(tokenKey)
async function request<T>(path: string, init?: RequestInit): Promise<T> { const response = await fetch(`${baseUrl}${path}`, init); if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? 'The service could not complete this request.'); return response.status === 204 ? undefined as T : response.json() as Promise<T> }
export const api = {
  register: (full_name: string, email: string, password: string) => request<AuthResponse>('/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ full_name, email, password }) }),
  login: (email: string, password: string) => request<AuthResponse>('/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) }),
  me: () => request<User>('/auth/me', { headers: { Authorization: `Bearer ${getToken()}` } }),
  logout: () => request<void>('/auth/logout', { method: 'POST', headers: { Authorization: `Bearer ${getToken()}` } }),
  analyze: (image: File, location?: GeolocationCoordinates) => { const body = new FormData(); body.append('image', image); if (location) { body.append('latitude', String(location.latitude)); body.append('longitude', String(location.longitude)); } return request<Analysis>('/analyze', { method: 'POST', body }) },
  nearby: (latitude: number, longitude: number, radius = 25, wasteType?: string) => request<Recycler[]>(`/recyclers/nearby?latitude=${latitude}&longitude=${longitude}&radius_km=${radius}${wasteType ? `&waste_type=${encodeURIComponent(wasteType)}` : ''}`),
}
