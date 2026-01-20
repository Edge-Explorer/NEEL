
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
import { useLocalSearchParams, useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../constants/Theme';
import { X, Check, Clock, Tag, Zap, Trash2 } from 'lucide-react-native';
import apiClient from '../services/api';

export default function EditActivityScreen() {
    const params = useLocalSearchParams();
    const router = useRouter();

    const [loading, setLoading] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [activityName, setActivityName] = useState('');
    const [duration, setDuration] = useState('');
    const [notes, setNotes] = useState('');
    const [energyLevel, setEnergyLevel] = useState(3);
    const [canEdit, setCanEdit] = useState(true);

    useEffect(() => {
        if (params.data) {
            try {
                const data = JSON.parse(params.data as string);
                setActivityName(data.activity_name);
                setDuration(data.duration?.toString() || '');
                setNotes(data.notes || '');
                setEnergyLevel(data.energy_level || 3);
                setCanEdit(data.can_edit !== false);
            } catch (e) {
                console.error("Failed to parse activity data", e);
            }
        }
    }, [params.data]);

    const handleUpdate = async () => {
        if (!activityName || !duration) {
            Alert.alert("Missing Info", "Please provide activity name and duration.");
            return;
        }

        setSubmitting(true);
        try {
            await apiClient.put(`/api/activities/log/${params.id}`, {
                activity_name: activityName,
                duration_minutes: parseInt(duration),
                notes: notes,
                energy_level: energyLevel
            });
            Alert.alert("Success", "Session updated successfully!");
            router.back();
        } catch (error: any) {
            const msg = error.response?.data?.detail || "Could not update session.";
            Alert.alert("Error", msg);
        } finally {
            setSubmitting(false);
        }
    };

    const handleDelete = async () => {
        Alert.alert(
            "Delete Session",
            "Are you sure you want to delete this activity log?",
            [
                { text: "Cancel", style: "cancel" },
                {
                    text: "Delete",
                    style: "destructive",
                    onPress: async () => {
                        setSubmitting(true);
                        try {
                            await apiClient.delete(`/api/activities/log/${params.id}`);
                            router.back();
                        } catch (error: any) {
                            Alert.alert("Error", "Could not delete session.");
                        } finally {
                            setSubmitting(false);
                        }
                    }
                }
            ]
        );
    };

    if (!canEdit) {
        return (
            <View style={[styles.container, { justifyContent: 'center', alignItems: 'center', padding: 20 }]}>
                <X color={COLORS.error} size={48} />
                <Text style={[styles.title, { marginTop: 20, textAlign: 'center' }]}>Edit Window Expired</Text>
                <Text style={{ color: COLORS.textSecondary, textAlign: 'center', marginTop: 10 }}>
                    Activities can only be edited within 24 hours of creation for data integrity.
                </Text>
                <TouchableOpacity style={[styles.confirmButton, { marginTop: 30, width: '100%' }]} onPress={() => router.back()}>
                    <Text style={styles.confirmButtonText}>Go Back</Text>
                </TouchableOpacity>
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
                    <Text style={styles.headerTitle}>Edit Session</Text>
                    <TouchableOpacity onPress={handleDelete} style={styles.deleteButtonHeader}>
                        <Trash2 color={COLORS.error} size={20} />
                    </TouchableOpacity>
                </View>

                <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Tag color={COLORS.secondary} size={18} />
                            <Text style={styles.sectionTitle}>What did you do?</Text>
                        </View>
                        <TextInput
                            style={styles.input}
                            value={activityName}
                            onChangeText={setActivityName}
                            placeholder="Activity name (e.g. Coding)"
                            placeholderTextColor={COLORS.textSecondary}
                        />
                    </View>

                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Clock color={COLORS.secondary} size={18} />
                            <Text style={styles.sectionTitle}>Duration (Minutes)</Text>
                        </View>
                        <TextInput
                            style={styles.input}
                            value={duration}
                            onChangeText={setDuration}
                            keyboardType="numeric"
                            placeholder="e.g. 45"
                            placeholderTextColor={COLORS.textSecondary}
                        />
                    </View>

                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Zap color={COLORS.secondary} size={18} />
                            <Text style={styles.sectionTitle}>Energy Level (1-5)</Text>
                        </View>
                        <View style={styles.energyContainer}>
                            {[1, 2, 3, 4, 5].map((level) => (
                                <TouchableOpacity
                                    key={level}
                                    style={[styles.energyBtn, energyLevel === level && styles.energyBtnSelected]}
                                    onPress={() => setEnergyLevel(level)}
                                >
                                    <Text style={[styles.energyText, energyLevel === level && styles.energyTextSelected]}>
                                        {level}
                                    </Text>
                                </TouchableOpacity>
                            ))}
                        </View>
                    </View>

                    <View style={styles.section}>
                        <View style={styles.sectionHeader}>
                            <Tag color={COLORS.secondary} size={18} />
                            <Text style={styles.sectionTitle}>Notes (Details for AI)</Text>
                        </View>
                        <TextInput
                            style={[styles.input, styles.textArea]}
                            value={notes}
                            onChangeText={setNotes}
                            placeholder="Describe what you achieved..."
                            placeholderTextColor={COLORS.textSecondary}
                            multiline
                            numberOfLines={4}
                        />
                    </View>

                    <View style={{ height: 40 }} />
                </ScrollView>

                <View style={styles.footer}>
                    <TouchableOpacity
                        style={styles.confirmButton}
                        onPress={handleUpdate}
                        disabled={submitting}
                    >
                        {submitting ? (
                            <ActivityIndicator color="#fff" />
                        ) : (
                            <>
                                <Check color="#fff" size={20} style={{ marginRight: 8 }} />
                                <Text style={styles.confirmButtonText}>Save Changes</Text>
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
        backgroundColor: '#050505',
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
    deleteButtonHeader: {
        width: 40,
        height: 40,
        borderRadius: 20,
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
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
        borderRadius: 12,
        paddingHorizontal: 16,
        paddingVertical: 14,
        color: '#fff',
        fontSize: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    textArea: {
        height: 120,
        textAlignVertical: 'top',
    },
    energyContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    energyBtn: {
        width: 50,
        height: 50,
        borderRadius: 25,
        backgroundColor: COLORS.surface,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    energyBtnSelected: {
        backgroundColor: COLORS.secondary,
        borderColor: COLORS.secondary,
    },
    energyText: {
        color: COLORS.textSecondary,
        fontSize: 18,
        fontWeight: '700',
    },
    energyTextSelected: {
        color: '#fff',
    },
    footer: {
        padding: SPACING.lg,
        backgroundColor: 'transparent',
    },
    confirmButton: {
        backgroundColor: COLORS.primary,
        height: 56,
        borderRadius: 16,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: COLORS.primary,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 5,
    },
    confirmButtonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: '700',
    },
    title: {
        fontSize: 24,
        fontWeight: '800',
        color: '#fff',
    }
});
