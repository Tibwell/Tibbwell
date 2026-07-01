import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach JWT token if available
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("tibbwell_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// ─── Quiz API ──────────────────────────────────────────────

export interface QuizQuestion {
  id: number;
  question_text: string;
  category: string;
  options: Array<{
    text: string;
    temperament: "sanguinous" | "bilious" | "phlegmatic" | "melancholic";
    points: number;
  }>;
}

export interface QuizResult {
  dominant_temperament: string;
  sub_dominant_temperament: string;
  combination: string;
  description: string;
  dominant_quality: string;
  quality_explanation: string;
  foods_to_eat: string[];
  foods_to_avoid: string[];
  disease_risks: string[];
  seasonal_tip: string;
}

export const quizApi = {
  getQuestions: async (): Promise<QuizQuestion[]> => {
    const response = await api.get("/api/quiz/questions");
    return response.data;
  },

  submitAnswers: async (
    answers: Record<number, string>
  ): Promise<QuizResult> => {
    const response = await api.post("/api/quiz/submit", { answers });
    return response.data;
  },
};

// ─── Auth API ──────────────────────────────────────────────

export interface User {
  id: number;
  email: string;
  name: string;
  is_premium: boolean;
}

export const authApi = {
  register: async (data: {
    email: string;
    password: string;
    name: string;
  }): Promise<{ token: string; user: User }> => {
    const response = await api.post("/api/auth/register", data);
    if (response.data.token) {
      localStorage.setItem("tibbwell_token", response.data.token);
    }
    return response.data;
  },

  login: async (data: {
    email: string;
    password: string;
  }): Promise<{ token: string; user: User }> => {
    const response = await api.post("/api/auth/login", data);
    if (response.data.token) {
      localStorage.setItem("tibbwell_token", response.data.token);
    }
    return response.data;
  },

  getProfile: async (): Promise<User> => {
    const response = await api.get("/api/auth/profile");
    return response.data;
  },

  logout: () => {
    localStorage.removeItem("tibbwell_token");
  },
};

// ─── Premium API ──────────────────────────────────────────

export const premiumApi = {
  getDashboard: async (): Promise<any> => {
    const response = await api.get("/api/premium/dashboard");
    return response.data;
  },

  createSubscription: async (): Promise<{ url: string }> => {
    const response = await api.post("/api/payfast/subscribe");
    return response.data;
  },
};

// ─── Chatbot API ──────────────────────────────────────────

export const chatbotApi = {
  ask: async (message: string): Promise<{ reply: string }> => {
    const response = await api.post("/api/chatbot/ask", { message });
    return response.data;
  },
};

// ─── Admin API ────────────────────────────────────────────

export interface AdminStats {
  total_users: number;
  active_subscribers: number;
  monthly_revenue: number;
  quiz_completion_rate: number;
  most_common_temperament: string;
  temperament_distribution: Record<string, number>;
}

export interface AdminUser {
  id: number;
  name: string;
  email: string;
  created_at: string;
  is_premium: boolean;
  temperament?: string;
}

export interface AdminQuizStats {
  total_quiz_attempts: number;
  completion_rate: number;
  average_score: number;
  temperament_breakdown: Record<string, number>;
}

export const adminApi = {
  login: async (data: {
    username: string;
    password: string;
  }): Promise<{ token: string }> => {
    const response = await api.post("/api/admin/login", data);
    if (response.data.access_token) {
      localStorage.setItem("tibbwell_token", response.data.access_token);
    }
    return response.data;
  },

  getStats: async (): Promise<AdminStats> => {
    const response = await api.get("/api/admin/stats");
    return response.data;
  },

  getUsers: async (): Promise<AdminUser[]> => {
    const response = await api.get("/api/admin/users");
    return response.data;
  },

  getQuizStats: async (): Promise<AdminQuizStats> => {
    const response = await api.get("/api/admin/quiz-stats");
    return response.data;
  },

  togglePremium: async (
    userId: number,
    isPremium: boolean
  ): Promise<void> => {
    await api.put(`/api/admin/users/${userId}/premium`, {
      is_premium: isPremium,
    });
  },

  updateContent: async (
    temperamentCombinationId: number,
    content: any
  ): Promise<void> => {
    await api.put("/api/admin/content", {
      temperament_combination_id: temperamentCombinationId,
      content,
    });
  },

  logout: () => {
    localStorage.removeItem("tibbwell_token");
  },
};

// Attach admin token interceptor
const adminApiInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

adminApiInstance.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("tibbwell_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export { adminApiInstance };

export default api;
