"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { adminApi, AdminStats, AdminUser } from "@/lib/api";
import { MOCK_TEMPERAMENT_COMBINATIONS } from "@/lib/dashboard";

export default function AdminDashboardPage() {
  const router = useRouter();
  const [isAuthed, setIsAuthed] = useState(false);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [activeTab, setActiveTab] = useState<"overview" | "users" | "content">("overview");
  const [selectedCombo, setSelectedCombo] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token =
      localStorage.getItem("tibbwell_token");
    if (!token) {
      router.push("/admin/login");
      return;
    }
    setIsAuthed(true);

    const loadData = async () => {
      try {
        const [statsData, usersData] = await Promise.all([
          adminApi.getStats(),
          adminApi.getUsers(),
        ]);
        setStats(statsData);
        setUsers(usersData);
      } catch (err: any) {
        setError(err.message || "Failed to load admin data.");
        setStats(null);
        setUsers([]);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [router]);

  const handleLogout = () => {
    adminApi.logout();
    router.push("/admin/login");
  };

  const handleTogglePremium = async (userId: number, current: boolean) => {
    try {
      await adminApi.togglePremium(userId, !current);
      setUsers((prev) =>
        prev.map((u) => (u.id === userId ? { ...u, is_premium: !current } : u))
      );
    } catch {
      setError("Failed to update premium status.");
    }
  };

  if (!isAuthed) return null;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-wellness-light border-t-wellness-green rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 text-sm">Loading admin dashboard...</p>
        </div>
      </div>
    );
  }

  const combo = MOCK_TEMPERAMENT_COMBINATIONS[selectedCombo];

  if (error && !stats) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="w-16 h-16 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">Unable to Load Dashboard</h2>
          <p className="text-gray-500 text-sm mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-wellness-green text-white px-6 py-3 rounded-xl font-semibold hover:bg-wellness-dark transition-all"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Admin Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-wellness-green rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">TW</span>
                </div>
                <span className="text-lg font-bold text-wellness-dark">TibbWell</span>
              </Link>
              <span className="text-gray-300 mx-2">|</span>
              <span className="text-sm font-medium text-gray-500">Admin</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="inline-flex items-center gap-1.5 bg-amber-100 text-amber-700 text-xs font-semibold px-3 py-1.5 rounded-full">
                <span className="w-1.5 h-1.5 bg-amber-500 rounded-full" />
                Admin
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-gray-500 hover:text-red-500 transition-colors flex items-center gap-1.5"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex gap-6 -mb-px">
            {[
              { key: "overview" as const, label: "Overview", icon: "📊" },
              { key: "users" as const, label: "Users", icon: "👥" },
              { key: "content" as const, label: "Health Content", icon: "📝" },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`py-4 px-1 border-b-2 text-sm font-medium transition-colors ${
                  activeTab === tab.key
                    ? "border-wellness-green text-wellness-green"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                <span className="mr-1.5">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "overview" && stats && (
          <OverviewTab stats={stats} />
        )}

        {activeTab === "users" && (
          <UsersTab users={users} onTogglePremium={handleTogglePremium} />
        )}

        {activeTab === "content" && (
          <ContentTab
            combinations={MOCK_TEMPERAMENT_COMBINATIONS}
            selectedCombo={selectedCombo}
            onSelectCombo={setSelectedCombo}
          />
        )}
      </div>
    </div>
  );
}

// ─── Overview Tab ──────────────────────────────────────────

function OverviewTab({ stats }: { stats: AdminStats }) {
  const statCards = [
    {
      label: "Total Users",
      value: stats.total_users.toLocaleString(),
      icon: "👥",
      change: "+12% this month",
      color: "bg-blue-50 text-blue-600",
    },
    {
      label: "Active Subscribers",
      value: stats.active_subscribers.toLocaleString(),
      icon: "⭐",
      change: `${((stats.active_subscribers / stats.total_users) * 100).toFixed(1)}% conversion`,
      color: "bg-green-50 text-green-600",
    },
    {
      label: "Monthly Revenue",
      value: `R${stats.monthly_revenue.toLocaleString()}`,
      icon: "💰",
      change: `${stats.active_subscribers} × R99/month`,
      color: "bg-amber-50 text-amber-600",
    },
    {
      label: "Quiz Completion Rate",
      value: `${stats.quiz_completion_rate}%`,
      icon: "📋",
      change: `${((stats.total_users * stats.quiz_completion_rate) / 100).toFixed(0)} completed`,
      color: "bg-purple-50 text-purple-600",
    },
  ];

  const maxValue = Math.max(...Object.values(stats.temperament_distribution));

  return (
    <div className="space-y-8">
      {/* Stats Cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => (
          <div
            key={card.label}
            className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-2xl">{card.icon}</span>
              <span className="text-xs text-gray-400">{card.change}</span>
            </div>
            <p className="text-2xl font-bold text-gray-800">{card.value}</p>
            <p className="text-sm text-gray-500 mt-1">{card.label}</p>
          </div>
        ))}
      </div>

      {/* Most Common Temperament Highlight */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-gray-800 mb-1">Most Common Temperament</h2>
        <p className="text-3xl font-bold text-wellness-green mb-4">{stats.most_common_temperament}</p>

        {/* Temperament Distribution Chart */}
        <h3 className="text-sm font-semibold text-gray-700 mb-4">Temperament Distribution</h3>
        <div className="space-y-2.5">
          {Object.entries(stats.temperament_distribution).map(([name, count]) => (
            <div key={name} className="flex items-center gap-3">
              <span className="text-xs text-gray-600 w-40 text-right flex-shrink-0">{name}</span>
              <div className="flex-1 bg-gray-100 rounded-full h-5 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-wellness-green to-wellness-accent rounded-full transition-all duration-500"
                  style={{ width: `${(count / maxValue) * 100}%` }}
                />
              </div>
              <span className="text-xs font-medium text-gray-500 w-12">{count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Users Tab ─────────────────────────────────────────────

function UsersTab({
  users,
  onTogglePremium,
}: {
  users: AdminUser[];
  onTogglePremium: (id: number, current: boolean) => void;
}) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      <div className="px-6 py-5 border-b border-gray-100">
        <h2 className="text-lg font-bold text-gray-800">User Management</h2>
        <p className="text-sm text-gray-500 mt-0.5">
          {users.length} recent registrations
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left">
              <th className="px-6 py-3 font-medium text-gray-600">Name</th>
              <th className="px-6 py-3 font-medium text-gray-600">Email</th>
              <th className="px-6 py-3 font-medium text-gray-600">Registered</th>
              <th className="px-6 py-3 font-medium text-gray-600">Temperament</th>
              <th className="px-6 py-3 font-medium text-gray-600">Status</th>
              <th className="px-6 py-3 font-medium text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-medium text-gray-800">{user.name}</td>
                <td className="px-6 py-4 text-gray-500">{user.email}</td>
                <td className="px-6 py-4 text-gray-500">{user.created_at}</td>
                <td className="px-6 py-4">
                  {user.temperament ? (
                    <span className="text-xs bg-wellness-light text-wellness-green px-2 py-1 rounded-full font-medium">
                      {user.temperament}
                    </span>
                  ) : (
                    <span className="text-xs text-gray-400">—</span>
                  )}
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full ${
                      user.is_premium
                        ? "bg-green-100 text-green-700"
                        : "bg-gray-100 text-gray-500"
                    }`}
                  >
                    <span
                      className={`w-1.5 h-1.5 rounded-full ${
                        user.is_premium ? "bg-green-500" : "bg-gray-400"
                      }`}
                    />
                    {user.is_premium ? "Premium" : "Free"}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <button
                    onClick={() => onTogglePremium(user.id, user.is_premium)}
                    className={`text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors ${
                      user.is_premium
                        ? "border-red-200 text-red-600 hover:bg-red-50"
                        : "border-wellness-green text-wellness-green hover:bg-wellness-light"
                    }`}
                  >
                    {user.is_premium ? "Remove Premium" : "Make Premium"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─── Content Tab ───────────────────────────────────────────

function ContentTab({
  combinations,
  selectedCombo,
  onSelectCombo,
}: {
  combinations: typeof MOCK_TEMPERAMENT_COMBINATIONS;
  selectedCombo: number;
  onSelectCombo: (id: number) => void;
}) {
  const combo = combinations[selectedCombo];

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      {/* Sidebar: Temperament list */}
      <div className="lg:col-span-1">
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div className="px-5 py-4 border-b border-gray-100">
            <h2 className="font-bold text-gray-800">Temperament Combinations</h2>
          </div>
          <div className="divide-y divide-gray-100 max-h-[500px] overflow-y-auto">
            {combinations.map((c, i) => (
              <button
                key={c.id}
                onClick={() => onSelectCombo(i)}
                className={`w-full text-left px-5 py-3.5 transition-colors ${
                  selectedCombo === i
                    ? "bg-wellness-light border-l-4 border-wellness-green"
                    : "hover:bg-gray-50 border-l-4 border-transparent"
                }`}
              >
                <p className="text-sm font-medium text-gray-800">{c.combination_name}</p>
                <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">{c.description}</p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Editor */}
      <div className="lg:col-span-2">
        {combo && (
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
            <div className="px-6 py-5 border-b border-gray-100">
              <h2 className="text-lg font-bold text-gray-800">{combo.combination_name}</h2>
              <p className="text-sm text-gray-500 mt-0.5">{combo.description}</p>
            </div>

            <div className="p-6 space-y-6">
              {/* Foods to Eat */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Foods to Eat</label>
                <div className="flex flex-wrap gap-2">
                  {combo.foods_to_eat.map((food, i) => (
                    <span
                      key={i}
                      className="text-xs bg-green-50 text-green-700 border border-green-200 px-3 py-1.5 rounded-full"
                    >
                      {food}
                    </span>
                  ))}
                </div>
              </div>

              {/* Foods to Avoid */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Foods to Avoid</label>
                <div className="flex flex-wrap gap-2">
                  {combo.foods_to_avoid.map((food, i) => (
                    <span
                      key={i}
                      className="text-xs bg-red-50 text-red-700 border border-red-200 px-3 py-1.5 rounded-full"
                    >
                      {food}
                    </span>
                  ))}
                </div>
              </div>

              {/* Disease Risks */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Disease Risks</label>
                <ul className="space-y-1">
                  {combo.disease_risks.map((risk, i) => (
                    <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                      <span className="w-1.5 h-1.5 bg-yellow-500 rounded-full mt-1.5 flex-shrink-0" />
                      {risk}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Seasonal Tips */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Seasonal Tips</label>
                <p className="text-sm text-gray-600 bg-amber-50 rounded-xl p-4">{combo.seasonal_tips}</p>
              </div>

              {/* Edit placeholder */}
              <div className="bg-gray-50 rounded-xl p-4 text-center">
                <p className="text-sm text-gray-500">
                  ✏️ Content editing via API will be available when connected to the backend.
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  PUT /api/admin/content — Update health content per temperament type
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}