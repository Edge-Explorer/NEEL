import React, { useState, useEffect } from 'react';
import {
    StyleSheet,
    View,
    Text,
    TouchableOpacity,
    TextInput,
    ScrollView,
    ActivityIndicator,
    Alert,
    KeyboardAvoidingView,
    Platform
} from 'react-native';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../constants/Theme';
import {
    X,
    Check,
    Clock,
    Calendar as CalendarIcon,
    Tag,
    Zap,
    ChevronDown
} from 'lucide-react-native';
import apiClient from '../services/api';

export default function LogActivityScreen() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [activityTypes, setActivityTypes] = useState<any[]>([]);
    const [fetchingTypes, setFetchingTypes] = useState(true);

    // Form State
    const [selectedActivity, setSelectedActivity] = useState('');
    const [duration, setDuration] = useState('');
    const [notes, setNotes] = useState('');
    const [energyLevel, setEnergyLevel] = useState(3); // 1-5 scale

    useEffect(() => {
        const fetchTypes = async () => {
            try {
                const response = await apiClient.get('/api/activity-types/');
                setActivityTypes(response.data);
            } catch (error) {
                console.error('Failed to fetch activity types:', error);
            } finally {
                setFetchingTypes(false);
            }
        };
        fetchTypes();
    }, []);

    const handleLogActivity = async () => {
        if (!selectedActivity || !duration) {
            Alert.alert("Missing Info", "Please select an activity and specify duration.");
            return;
        }

        setLoading(true);
        try {
            const response = await apiClient.post('/api/activities/log', {
                activity_name: selectedActivity,
                duration_minutes: parseInt(duration),
                notes: notes,
                energy_level: energyLevel,
                date: new Date().toISOString().split('T')[0], // YYYY-MM-DD
                completed: true
            });

            if (response.status === 200 || response.status === 201) {
                Alert.alert("Success 🚀", "Activity logged! Your NEEL Calibration is updating.", [
                    { text: "Awesome", onPress: () => router.back() }
                ]);
            }
        } catch (error: any) {
            console.error('Logging failed:', error);
            Alert.alert("Error", error.response?.data?.detail || "Failed to log activity. Try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.container}
        >
            <LinearGradient colors={['#0F172A', '#050505']} style={styles.gradient}>

                {/* Header */}
                <View style={styles.header}>
                    <TouchableOpacity onPress={() => router.back()} style={styles.closeButton}>
                        <X color={COLORS.text} size={24} />
                    </TouchableOpacity>
                    <Text style={styles.headerTitle}>Log Activity</Text>
                    <View style={{ width: 40 }} />
                </View>

                <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>

                    {/* Activity Selection */}
                    <Text style={styles.label}>What did you do?</Text>
                    {fetchingTypes ? (
                        <ActivityIndicator color={COLORS.primary} style={{ marginVertical: 20 }} />
                    ) : (
                        <View style={styles.chipContainer}>
                            {activityTypes.map((type) => (
                                <TouchableOpacity
                                    key={type.activity_id}
                                    style={[
                                        styles.chip,
                                        selectedActivity === type.activity_name && styles.selectedChip
                                    ]}
                                    onPress={() => setSelectedActivity(type.activity_name)}
                                >
                                    <Text style={[
                                        styles.chipText,
                                        selectedActivity === type.activity_name && styles.selectedChipText
                                    ]}>
                                        {type.activity_name}
                                    </Text>
                                </TouchableOpacity>
                            ))}
                        </View>
                    )}

                    {/* Duration Input */}
                    <View style={styles.inputGroup}>
                        <View style={styles.labelRow}>
                            <Clock color={COLORS.secondary} size={18} />
                            <Text style={styles.inputLabel}>Duration (Minutes)</Text>
                        </View>
                        <TextInput
                            style={styles.input}
                            placeholder="e.g. 60"
                            placeholderTextColor="rgba(255,255,255,0.3)"
                            keyboardType="numeric"
                            value={duration}
                            onChangeText={setDuration}
                        />
                    </View>

                    {/* Energy Level Selector */}
                    <Text style={styles.label}>Energy Level during activity</Text>
                    <View style={styles.energyContainer}>
                        {[1, 2, 3, 4, 5].map((level) => (
                            <TouchableOpacity
                                key={level}
                                onPress={() => setEnergyLevel(level)}
                                style={[
                                    styles.energyBtn,
                                    energyLevel === level && { backgroundColor: COLORS.primary }
                                ]}
                            >
                                <Text style={styles.energyText}>{level === 1 ? '😴' : level === 5 ? '⚡' : level}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    {/* Notes Input */}
                    <View style={styles.inputGroup}>
                        <View style={styles.labelRow}>
                            <Tag color={COLORS.accent} size={18} />
                            <Text style={styles.inputLabel}>Notes (Details for AI)</Text>
                        </View>
                        <TextInput
                            style={[styles.input, styles.textArea]}
                            placeholder="What specifically did you achieve?"
                            placeholderTextColor="rgba(255,255,255,0.3)"
                            multiline
                            numberOfLines={4}
                            value={notes}
                            onChangeText={setNotes}
                        />
                    </View>

                    {/* Submit Button */}
                    <TouchableOpacity
                        style={[styles.submitButton, loading && { opacity: 0.7 }]}
                        onPress={handleLogActivity}
                        disabled={loading}
                    >
                        {loading ? (
                            <ActivityIndicator color="#fff" />
                        ) : (
                            <>
                                <Check color="#fff" size={24} style={{ marginRight: 10 }} />
                                <Text style={styles.submitButtonText}>Confirm Session</Text>
                            </>
                        )}
                    </TouchableOpacity>

                </ScrollView>
            </LinearGradient>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#050505',
    },
    gradient: {
        flex: 1,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: SPACING.lg,
        paddingTop: 60,
        marginBottom: 20,
    },
    closeButton: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: 'rgba(255,255,255,0.1)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: '800',
        color: COLORS.text,
    },
    scrollContent: {
        padding: SPACING.lg,
    },
    label: {
        fontSize: 16,
        fontWeight: '700',
        color: COLORS.text,
        marginBottom: 15,
    },
    chipContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 10,
        marginBottom: 30,
    },
    chip: {
        paddingHorizontal: 16,
        paddingVertical: 10,
        borderRadius: 25,
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    selectedChip: {
        backgroundColor: COLORS.primary,
        borderColor: COLORS.primary,
    },
    chipText: {
        color: COLORS.textSecondary,
        fontWeight: '600',
    },
    selectedChipText: {
        color: '#fff',
    },
    inputGroup: {
        marginBottom: 30,
    },
    labelRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
        gap: 8,
    },
    inputLabel: {
        fontSize: 14,
        color: COLORS.textSecondary,
        fontWeight: '600',
    },
    input: {
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderRadius: 16,
        padding: SPACING.md,
        color: COLORS.text,
        fontSize: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    textArea: {
        height: 120,
        textAlignVertical: 'top',
    },
    energyContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 30,
    },
    energyBtn: {
        width: 50,
        height: 50,
        borderRadius: 15,
        backgroundColor: 'rgba(255,255,255,0.05)',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    energyText: {
        color: '#fff',
        fontWeight: '800',
    },
    submitButton: {
        backgroundColor: COLORS.primary,
        height: 60,
        borderRadius: 20,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 50,
        shadowColor: COLORS.primary,
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.3,
        shadowRadius: 20,
        elevation: 10,
    },
    submitButtonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: '800',
    },
});
