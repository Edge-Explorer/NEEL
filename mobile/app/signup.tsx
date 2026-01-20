import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TextInput,
    TouchableOpacity,
    KeyboardAvoidingView,
    Platform,
    ActivityIndicator,
    Alert
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../constants/Theme';
import { User, Mail, Lock, ArrowRight, Sparkles, Eye, EyeOff } from 'lucide-react-native';
import apiClient from '../services/api';
import { useRouter } from 'expo-router';

export default function SignupScreen() {
    const router = useRouter();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSignup = async (isRetry = false) => {
        if (!name || !email || !password) {
            setError('Please fill in all fields');
            return;
        }

        setLoading(true);

        // Show friendly message if this is the first attempt
        if (!isRetry) {
            setError('');
        }

        try {
            await apiClient.post('/api/auth/register', {
                name,
                email,
                password,
            }, {
                timeout: 70000, // 70 second timeout for sleeping backend
            });

            router.replace('/login');
        } catch (err: any) {
            console.error('Signup Error:', err.response?.data || err.message);

            // Check if it's a timeout or network error (backend sleeping)
            const isNetworkError = err.code === 'ECONNABORTED' || err.message?.includes('timeout') ||
                err.message?.includes('Network Error') || !err.response;

            if (isNetworkError && !isRetry) {
                // Backend is likely sleeping on Render's free tier
                setError('⏳ Waking up the server, please wait...');
                setLoading(false);

                // Show alert and auto-retry after 60 seconds
                Alert.alert(
                    'Server Initializing',
                    'The backend is waking up from sleep mode. This takes about 60 seconds on the free tier. Retrying automatically...',
                    [{ text: 'OK' }]
                );

                // Auto-retry after 60 seconds
                setTimeout(() => {
                    handleSignup(true);
                }, 60000);
                return;
            }

            const errorMsg = err.response?.data?.detail || 'Registration failed.';
            setError(errorMsg);
            Alert.alert('Registration Failed', errorMsg);
            setLoading(false);
        }
    };

    return (
        <LinearGradient colors={['#0F172A', '#050505']} style={styles.container}>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                style={styles.content}
            >
                <View style={styles.header}>
                    <View style={styles.logoContainer}>
                        <Sparkles color={COLORS.secondary} size={40} strokeWidth={2.5} />
                    </View>
                    <Text style={styles.title}>Create NEEL ID</Text>
                    <Text style={styles.subtitle}>Begin your evolved productivity journey</Text>
                </View>

                <View style={styles.form}>
                    {error ? <Text style={styles.errorText}>{error}</Text> : null}

                    <View style={styles.inputWrapper}>
                        <User color={COLORS.textSecondary} size={20} style={styles.inputIcon} />
                        <TextInput
                            style={styles.input}
                            placeholder="Full Name"
                            placeholderTextColor={COLORS.textSecondary}
                            value={name}
                            onChangeText={setName}
                        />
                    </View>

                    <View style={styles.inputWrapper}>
                        <Mail color={COLORS.textSecondary} size={20} style={styles.inputIcon} />
                        <TextInput
                            style={styles.input}
                            placeholder="Email Address"
                            placeholderTextColor={COLORS.textSecondary}
                            value={email}
                            onChangeText={setEmail}
                            keyboardType="email-address"
                            autoCapitalize="none"
                        />
                    </View>

                    <View style={styles.inputWrapper}>
                        <Lock color={COLORS.textSecondary} size={20} style={styles.inputIcon} />
                        <TextInput
                            style={styles.input}
                            placeholder="Secret Password"
                            placeholderTextColor={COLORS.textSecondary}
                            value={password}
                            onChangeText={setPassword}
                            secureTextEntry={!showPassword}
                        />
                        <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                            {showPassword ?
                                <EyeOff color={COLORS.textSecondary} size={20} /> :
                                <Eye color={COLORS.textSecondary} size={20} />
                            }
                        </TouchableOpacity>
                    </View>

                    <TouchableOpacity
                        style={styles.signupButton}
                        onPress={() => handleSignup(false)}
                        disabled={loading}
                    >
                        <LinearGradient
                            colors={['#06B6D4', '#0891B2']}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={styles.gradientButton}
                        >
                            {loading ? (
                                <ActivityIndicator color="#fff" />
                            ) : (
                                <>
                                    <Text style={styles.buttonText}>Initialze NEEL</Text>
                                    <ArrowRight color="#fff" size={20} />
                                </>
                            )}
                        </LinearGradient>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.loginLink} onPress={() => router.back()}>
                        <Text style={styles.loginText}>
                            Already registered? <Text style={styles.loginHighlight}>Access NEEL</Text>
                        </Text>
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
    content: {
        flex: 1,
        justifyContent: 'center',
        padding: SPACING.xl,
    },
    header: {
        alignItems: 'center',
        marginBottom: SPACING.xxl,
    },
    logoContainer: {
        width: 70,
        height: 70,
        borderRadius: 20,
        backgroundColor: 'rgba(6, 182, 212, 0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: SPACING.md,
        borderWidth: 1,
        borderColor: 'rgba(6, 182, 212, 0.2)',
    },
    title: {
        fontSize: 28,
        fontWeight: '800',
        color: COLORS.text,
        letterSpacing: 0.5,
    },
    subtitle: {
        fontSize: 14,
        color: COLORS.textSecondary,
        marginTop: SPACING.xs,
        textAlign: 'center',
    },
    form: {
        width: '100%',
    },
    inputWrapper: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: COLORS.surface,
        borderRadius: 16,
        paddingHorizontal: SPACING.md,
        marginBottom: SPACING.md,
        borderWidth: 1,
        borderColor: 'rgba(255, 255, 255, 0.1)',
        height: 60,
    },
    inputIcon: {
        marginRight: SPACING.md,
    },
    input: {
        flex: 1,
        color: COLORS.text,
        fontSize: 16,
    },
    signupButton: {
        marginTop: SPACING.lg,
        height: 60,
        borderRadius: 16,
        overflow: 'hidden',
        elevation: 8,
        shadowColor: COLORS.secondary,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 12,
    },
    gradientButton: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
    },
    buttonText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: '700',
        marginRight: SPACING.sm,
    },
    errorText: {
        color: COLORS.error,
        textAlign: 'center',
        marginBottom: SPACING.md,
        fontWeight: '600',
    },
    loginLink: {
        marginTop: SPACING.xl,
        alignItems: 'center',
    },
    loginText: {
        color: COLORS.textSecondary,
        fontSize: 14,
    },
    loginHighlight: {
        color: COLORS.secondary,
        fontWeight: '700',
    },
});
