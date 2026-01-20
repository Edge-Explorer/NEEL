import React, { useEffect, useState, useCallback } from 'react';
import { useFocusEffect } from 'expo-router';
import {
  StyleSheet,
  ScrollView,
  View,
  Text,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
  Dimensions,
  Alert
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../../constants/Theme';
import {
  BarChart3,
  Activity,
  Target,
  Zap,
  BrainCircuit,
  ChevronRight,
  Plus,
  LogOut,
  Flame,
  TrendingUp
} from 'lucide-react-native';
import apiClient from '../../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';

const { width } = Dimensions.get('window');

export default function DashboardScreen() {
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [expandedActivities, setExpandedActivities] = useState(false);

  const fetchDashboardData = async () => {
    try {
      const response = await apiClient.get('/api/dashboard/');
      setData(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      fetchDashboardData();
    }, [])
  );

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchDashboardData();
  }, []);

  const handleLogout = async () => {
    Alert.alert(
      "Log Out",
      "Are you sure you want to disconnect?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Log Out",
          style: 'destructive',
          onPress: async () => {
            await AsyncStorage.removeItem('userToken');
            router.replace('/login');
          }
        }
      ]
    );
  };

  if (loading && !refreshing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={COLORS.primary} />
      }
    >
      <LinearGradient colors={['#0F172A', '#050505']} style={styles.content}>

        {/* Header - NEEL Pulse */}
        <View style={styles.header}>
          <View>
            <Text style={styles.welcomeText}>NEEL Pulse</Text>
            <Text style={styles.statusText}>
              {data?.profile?.name ? `Active: ${data.profile.name}` : 'Initializing...'}
            </Text>
          </View>
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <TouchableOpacity style={styles.aiButton} onPress={handleLogout}>
              <LogOut color={COLORS.error} size={24} />
            </TouchableOpacity>
            <TouchableOpacity style={styles.aiButton}>
              <BrainCircuit color={COLORS.primary} size={28} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Global Insight Card */}
        <TouchableOpacity
          onPress={() => router.push('/set-goals')}
          activeOpacity={0.8}
        >
          <LinearGradient
            colors={['rgba(139, 92, 246, 0.15)', 'rgba(6, 182, 212, 0.05)']}
            style={styles.insightCard}
          >
            <View style={styles.insightHeader}>
              <Zap color={COLORS.primary} size={20} />
              <Text style={styles.insightTitle}>Primary Goal</Text>
            </View>
            <Text style={styles.insightValue}>
              {data?.profile?.primary_goal || 'Focus'}
            </Text>
            <Text style={styles.insightDesc}>
              {data?.profile?.primary_goal
                ? "Tap to recalibrate your strategy"
                : "Connect your brain to NEEL to set a target."}
            </Text>
          </LinearGradient>
        </TouchableOpacity>

        {/* Activity Breakdown (Visual Analytics) */}
        {data?.activity_distribution && Object.keys(data.activity_distribution).length > 0 && (
          <View style={styles.breakdownContainer}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Activity Breakdown</Text>
              <BarChart3 color={COLORS.secondary} size={18} />
            </View>
            <View style={styles.breakdownCard}>
              {Object.entries(data.activity_distribution).map(([cat, mins]: [any, any], idx) => {
                const totalMins: number = Object.values(data.activity_distribution).reduce((a: any, b: any) => a + b, 0) as number;
                const percentage = Math.round((mins / totalMins) * 100);
                const colors = [COLORS.primary, COLORS.secondary, COLORS.error, COLORS.accent, '#A855F7'];

                return (
                  <View key={cat} style={styles.breakdownRow}>
                    <View style={styles.breakdownLabelRow}>
                      <Text style={styles.breakdownLabel}>{cat}</Text>
                      <Text style={styles.breakdownValue}>{mins}m ({percentage}%)</Text>
                    </View>
                    <View style={styles.breakdownBarBg}>
                      <View
                        style={[
                          styles.breakdownBarFill,
                          { width: `${percentage}%`, backgroundColor: colors[idx % colors.length] }
                        ]}
                      />
                    </View>
                  </View>
                );
              })}
            </View>
          </View>
        )}

        {/* Quick Stats Grid */}
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <View style={[styles.statIconContainer, { backgroundColor: 'rgba(139, 92, 246, 0.1)' }]}>
              <Activity color={COLORS.primary} size={20} />
            </View>
            <Text style={styles.statLabel}>Logs</Text>
            <Text style={styles.statValue}>{data?.activities?.length || 0}</Text>
          </View>
          <View style={styles.statItem}>
            <View style={[styles.statIconContainer, { backgroundColor: 'rgba(6, 182, 212, 0.1)' }]}>
              <Target color={COLORS.secondary} size={20} />
            </View>
            <Text style={styles.statLabel}>Goals</Text>
            <Text style={styles.statValue}>{data?.goals_count || 0}</Text>
          </View>
          <View style={styles.statItem}>
            <View style={[styles.statIconContainer, { backgroundColor: 'rgba(34, 197, 94, 0.1)' }]}>
              <Zap color="#22c55e" size={20} />
            </View>
            <Text style={styles.statLabel}>Sync</Text>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}>
              <View style={{ width: 6, height: 6, borderRadius: 3, backgroundColor: '#22c55e' }} />
              <Text style={[styles.statValue, { color: '#22c55e' }]}>Active</Text>
            </View>
          </View>
        </View>

        {/* Training Progress / Streak Section */}
        <View style={styles.trainingSection}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>NEEL Training Progress</Text>
            <View style={styles.streakBadge}>
              <Flame color={COLORS.accent} size={16} fill={COLORS.accent} />
              <Text style={styles.streakText}>{data?.streak || 0} Day Streak</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.progressCard}>
            <View style={styles.progressHeader}>
              <Text style={styles.progressLabel}>Calibration Status</Text>
              <Text style={styles.progressValue}>{Math.round(data?.onboarding?.overall_progress || 0)}%</Text>
            </View>

            <View style={styles.progressBarContainer}>
              <View
                style={[
                  styles.progressBar,
                  { width: `${data?.onboarding?.overall_progress || 0}%` }
                ]}
              />
            </View>

            <View style={styles.progressFooter}>
              <View style={styles.progressInfo}>
                <Activity color={COLORS.primary} size={12} />
                <Text style={styles.progressInfoText}>
                  {data?.onboarding?.total_minutes || 0}/{data?.onboarding?.target_minutes || 120} mins
                </Text>
              </View>
              <View style={styles.progressInfo}>
                <TrendingUp color={COLORS.secondary} size={12} />
                <Text style={styles.progressInfoText}>
                  Day {data?.onboarding?.days_logged || 0} of 7
                </Text>
              </View>
            </View>

            <Text style={styles.onboardingMessage}>
              {data?.onboarding?.is_complete
                ? "🚀 NEEL is fully synchronized! Deep insights unlocked."
                : "Feed more activity logs to sharpen NEEL's strategy engine."}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Intelligence Feed */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Intelligence Feed</Text>
          <TouchableOpacity onPress={() => setExpandedActivities(!expandedActivities)}>
            <Text style={styles.viewAll}>{expandedActivities ? 'Show Less' : 'Expand All'}</Text>
          </TouchableOpacity>
        </View>

        {(expandedActivities ? data.activities || [] : (data.activities || []).slice(0, 3)).map((item: any) => (
          <TouchableOpacity
            key={item.log_id}
            style={styles.feedCard}
            onPress={() => router.push({
              pathname: '/edit-activity',
              params: { id: item.log_id, data: JSON.stringify(item) }
            })}
          >
            <View style={styles.feedIcon}>
              <Activity color={COLORS.textSecondary} size={18} />
            </View>
            <View style={styles.feedContent}>
              <Text style={styles.feedTitle}>{item.activity_name}</Text>
              <Text style={styles.feedTime}>
                {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
              </Text>
            </View>
            <ChevronRight color={COLORS.textSecondary} size={20} />
          </TouchableOpacity>
        ))}

        {/* FAB for record activity could go here */}
        <View style={{ height: 100 }} />
      </LinearGradient>

      {/* Action Button */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => router.push('/log-activity')}
      >
        <Plus color="#fff" size={32} />
      </TouchableOpacity>
    </ScrollView >
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050505',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#050505',
  },
  content: {
    flex: 1,
    padding: SPACING.lg,
    paddingTop: 60,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  welcomeText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  statusText: {
    fontSize: 24,
    color: COLORS.text,
    fontWeight: '800',
    marginTop: 4,
  },
  aiButton: {
    width: 50,
    height: 50,
    borderRadius: 15,
    backgroundColor: 'rgba(139, 92, 246, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(139, 92, 246, 0.2)',
  },
  insightCard: {
    borderRadius: 24,
    padding: SPACING.lg,
    marginBottom: SPACING.xl,
    borderWidth: 1,
    borderColor: 'rgba(139, 92, 246, 0.1)',
  },
  insightHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  insightTitle: {
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '700',
    marginLeft: SPACING.sm,
    textTransform: 'uppercase',
  },
  insightValue: {
    fontSize: 36,
    color: '#fff',
    fontWeight: '900',
    marginBottom: SPACING.xs,
  },
  insightDesc: {
    color: COLORS.textSecondary,
    fontSize: 14,
    lineHeight: 20,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.xxl,
  },
  statItem: {
    width: (width - SPACING.lg * 2 - SPACING.md * 2) / 3,
    backgroundColor: COLORS.surface,
    borderRadius: 20,
    padding: SPACING.md,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.05)',
  },
  statIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  statLabel: {
    color: COLORS.textSecondary,
    fontSize: 12,
    fontWeight: '600',
  },
  statValue: {
    color: COLORS.text,
    fontSize: 18,
    fontWeight: '800',
    marginTop: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  sectionTitle: {
    fontSize: 18,
    color: COLORS.text,
    fontWeight: '700',
  },
  viewAll: {
    color: COLORS.primary,
    fontSize: 14,
    fontWeight: '600',
  },
  feedCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.05)',
  },
  feedIcon: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  feedContent: {
    flex: 1,
  },
  feedTitle: {
    color: COLORS.text,
    fontSize: 16,
    fontWeight: '600',
  },
  feedTime: {
    color: COLORS.textSecondary,
    fontSize: 12,
    marginTop: 2,
  },
  fab: {
    position: 'absolute',
    bottom: 30,
    right: 30,
    width: 65,
    height: 65,
    borderRadius: 33,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.5,
    shadowRadius: 15,
    elevation: 8,
  },
  trainingSection: {
    marginBottom: SPACING.xl,
  },
  streakBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(244, 114, 182, 0.15)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(244, 114, 182, 0.3)',
  },
  streakText: {
    color: COLORS.accent,
    fontSize: 12,
    fontWeight: '700',
    marginLeft: 6,
  },
  progressCard: {
    backgroundColor: COLORS.surface,
    padding: SPACING.md,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.05)',
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  progressLabel: {
    color: COLORS.text,
    fontSize: 14,
    fontWeight: '600',
  },
  progressValue: {
    color: COLORS.secondary,
    fontSize: 14,
    fontWeight: '800',
  },
  progressBarContainer: {
    height: 10,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 5,
    marginBottom: 12,
    overflow: 'hidden',
  },
  progressBar: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 5,
  },
  progressFooter: {
    flexDirection: 'row',
    gap: 15,
    marginBottom: 12,
  },
  progressInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
  },
  progressInfoText: {
    color: COLORS.textSecondary,
    fontSize: 11,
    fontWeight: '600',
  },
  onboardingMessage: {
    color: COLORS.textSecondary,
    fontSize: 12,
    fontStyle: 'italic',
    lineHeight: 18,
  },
  breakdownContainer: {
    marginBottom: SPACING.xl,
  },
  breakdownCard: {
    backgroundColor: COLORS.surface,
    padding: SPACING.lg,
    borderRadius: 24,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.05)',
  },
  breakdownRow: {
    marginBottom: 16,
  },
  breakdownLabelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  breakdownLabel: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '700',
  },
  breakdownValue: {
    color: COLORS.textSecondary,
    fontSize: 12,
    fontWeight: '600',
  },
  breakdownBarBg: {
    height: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: 4,
    overflow: 'hidden',
  },
  breakdownBarFill: {
    height: '100%',
    borderRadius: 4,
  },
});
