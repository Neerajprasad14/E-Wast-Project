export type Recycler = { id: string; name: string; city: string; state: string; distance_km?: number; score?: number; verified: boolean; pickup_available: boolean; accepted_waste_types: string[]; authorization_status: string; ranking_reason?: string }
export type Analysis = { classification: { object: string; category: string; confidence: number }; condition: { condition: string; repairability: string; observations: string[] }; environmental_impact: { risk_level: string; environmental_impacts: string[] }; recommendation: { action: string; reason: string; steps: string[]; safety_instructions: string[] }; nearby_recyclers: Recycler[]; warnings: string[] }
export type User = { id: number; full_name: string; email: string }
export type AuthResponse = { token: string; user: User }
