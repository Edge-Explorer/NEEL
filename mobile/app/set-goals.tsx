
import React, { useState, useEffect } from 'react';
import {
    StyleSheet,
    View,
    Text,
    TouchableOpacity,
    TextInput,
    ScrollView,
    Alert,
    ActivityIndicator,
    KeyboardAvoidingView,
    Platform
} from 'react-native';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../constants/Theme';
import { X, Check, Target, Layers } from 'lucide-react-native';
import apiClient from '../services/api';

export default function SetGoalsScreen() {
    const router = useRouter();
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [primaryGoal, setPrimaryGoal] = useState('');
    const [focusAreas, setFocusAreas] = useState('');

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await apiClient.get('/api/dashboard/');
            setPrimaryGoal(response.data.profile.primary_goal || '');
            if (response.data.profile.focus_areas) {
                setFocusAreas(Array.isArray(response.data.profile.focus_areas)
                    ? response.data.profile.focus_areas.join(', ')
                    : response.data.profile.focus_areas);
            }
        } catch (error) {
            console.error("Failed to fetch profile", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!primaryGoal.trim()) {
            Alert.alert("Error", "Please set a primary goal.");
            return;
        }

        setSubmitting(true);
        try {
            // Reusing the onboarding/profile logic if it exists, or just a direct update
            await apiClient.post('/api/profiles/update', {
                primary_goal: primaryGoal,
                focus_areas: focusAreas.split(',').map(s => s.trim()).filter(s => s !== '')
            });
            Alert.alert("Success", "Your goals have been updated!");
            router.back();
        } catch (error: any) {
            Alert.alert("Error", "Could not update goals.");
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color={COLORS.primary} />
            </View>
        );
    }

    return (
        <LinearGradient colors={['#0F172A', '#050505']} style={styles.container}>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={{ flex: 1 }}
            >
                <View style={styles.header}>
                    <TouchableOpacity onPress={() => router.back()} style={styles.closeButton}>
                        <X color="#fff" size={24} />
                    </TouchableOpacity>
                    <Text style={styles.headerTitle}>Strategy Calibration</Text>
                    <View style={{ width: 40 }} />
                </View>

                <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
                    <View style={styles.infoCard}>
                        <Target color={COLORS.primary} size={32} />
                        <Text style={styles.infoTitle}>What is your North Star?</Text>
                        <Text style={styles.infoDesc}>
                            Establishing a clear primary goal helps NEEL calibrate its advice to your specific trajectory.
                        </Text>
                    </View>

                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Target color={COLORS.secondary} size={18} />
                            <Text style={styles.sectionTitle}>Primary Goal (The "Why")</Text>
                        </View>
                        <TextInput
                            style={styles.input}
                            value={primaryGoal}
                            onChangeText={setPrimaryGoal}
                            placeholder="e.g. Become a Lead ML Engineer"
                            placeholderTextColor={COLORS.textSecondary}
                        />
                    </View>

                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Layers color={COLORS.secondary} size={18} />
                            <Text style={styles.sectionTitle}>Focus Areas (Comma separated)</Text>
                        </View>
                        <TextInput
                            style={[styles.input, styles.textArea]}
                            value={focusAreas}
                            onChangeText={setFocusAreas}
                            placeholder="e.g. Deep Work, Learning, Exercise"
                            placeholderTextColor={COLORS.textSecondary}
                            multiline
                            numberOfLines={3}
                        />
                    </View>
                </ScrollView>

                <View style={styles.footer}>
                    <TouchableOpacity
                        style={styles.confirmButton}
                        onPress={handleSave}
                        disabled={submitting}
                    >
                        {submitting ? (
                            <ActivityIndicator color="#fff" />
                        ) : (
                            <>
                                <Check color="#fff" size={20} style={{ marginRight: 8 }} />
                                <Text style={styles.confirmButtonText}>Calibrate Target</Text>
                            </>
                        )}
                    </TouchableOpacity>
                </View>
            </KeyboardAvoidingView>
        </LinearGradient>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    loadingContainer: {
        flex: 1,
        backgroundColor: '#050505',
        justifyContent: 'center',
        alignItems: 'center',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: SPACING.lg,
        paddingTop: 60,
        paddingBottom: SPACING.md,
    },
    closeButton: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: 'rgba(255,255,255,0.05)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    headerTitle: {
        color: '#fff',
        fontSize: 18,
        fontWeight: '700',
    },
    content: {
        flex: 1,
        padding: SPACING.lg,
    },
    infoCard: {
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        borderRadius: 24,
        padding: 24,
        alignItems: 'center',
        marginBottom: 32,
        borderWidth: 1,
        borderColor: 'rgba(139, 92, 246, 0.2)',
    },
    infoTitle: {
        color: '#fff',
        fontSize: 20,
        fontWeight: '800',
        marginTop: 16,
        marginBottom: 8,
    },
    infoDesc: {
        color: COLORS.textSecondary,
        fontSize: 14,
        textAlign: 'center',
        lineHeight: 20,
    },
    section: {
        marginBottom: 24,
    },
    sectionHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 12,
    },
    sectionTitle: {
        color: COLORS.textSecondary,
        fontSize: 14,
        fontWeight: '600',
        marginLeft: 8,
    },
    input: {
        backgroundColor: COLORS.surface,
        borderRadius: 16,
        paddingHorizontal: 16,
        paddingVertical: 14,
        color: '#fff',
        fontSize: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    textArea: {
        height: 100,
        textAlignVertical: 'top',
    },
    footer: {
        padding: SPACING.lg,
    },
    confirmButton: {
        backgroundColor: COLORS.primary,
        height: 56,
        borderRadius: 16,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
    },
    confirmButtonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: '700',
    }
});
