import React, { useEffect, useState, useCallback } from 'react';
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
  LogOut
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

  useEffect(() => {
    fetchDashboardData();
  }, []);

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
        <LinearGradient
          colors={['rgba(139, 92, 246, 0.15)', 'rgba(6, 182, 212, 0.05)']}
          style={styles.insightCard}
        >
          <View style={styles.insightHeader}>
            <Zap color={COLORS.primary} size={20} />
            <Text style={styles.insightTitle}>Primary Goal</Text>
          </View>
          <Text style={styles.insightValue}>Focus</Text>
          <Text style={styles.insightDesc}>
            {data?.profile?.primary_goal || 'Connect your brain to NEEL to set a target.'}
          </Text>
        </LinearGradient>

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
            <Text style={styles.statValue}>{data?.outcomes?.length || 0}</Text>
          </View>
          <View style={styles.statItem}>
            <View style={[styles.statIconContainer, { backgroundColor: 'rgba(244, 114, 182, 0.1)' }]}>
              <BarChart3 color={COLORS.accent} size={20} />
            </View>
            <Text style={styles.statLabel}>Sync</Text>
            <Text style={styles.statValue}>1.0.7</Text>
          </View>
        </View>

        {/* Intelligence Feed */}
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Intelligence Feed</Text>
          <TouchableOpacity>
            <Text style={styles.viewAll}>Expand All</Text>
          </TouchableOpacity>
        </View>

        {data?.activities?.map((item: any, index: any) => (
          <TouchableOpacity key={item.log_id || index} style={styles.feedCard}>
            <View style={styles.feedIcon}>
              <Activity color={COLORS.textSecondary} size={18} />
            </View>
            <View style={styles.feedContent}>
              <Text style={styles.feedTitle}>{item.activity_type?.name || 'Activity'}</Text>
              <Text style={styles.feedTime}>
                {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </Text>
            </View>
            <ChevronRight color={COLORS.textSecondary} size={20} />
          </TouchableOpacity>
        ))}

        {/* FAB for record activity could go here */}
        <View style={{ height: 100 }} />
      </LinearGradient>

      {/* Action Button */}
      <TouchableOpacity style={styles.fab}>
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
  }
});
