import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TextInput,
    TouchableOpacity,
    KeyboardAvoidingView,
    Platform,
    Dimensions,
    ActivityIndicator,
    Alert
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SPACING } from '../constants/Theme';
import { User, Lock, ArrowRight, Zap, Eye, EyeOff } from 'lucide-react-native';
import apiClient from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';

const { width } = Dimensions.get('window');

export default function LoginScreen() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async (isRetry = false) => {
        if (!email || !password) {
            setError('Please fill in all fields');
            return;
        }

        setLoading(true);

        // Show friendly message if this is the first attempt
        if (!isRetry) {
            setError('');
        }

        try {
            const response = await apiClient.post('/api/auth/login', {
                email,
                password,
            }, {
                timeout: 70000, // 70 second timeout for sleeping backend
            });

            const { access_token } = response.data;
            await AsyncStorage.setItem('userToken', access_token);

            router.replace('/(tabs)');
        } catch (err: any) {
            console.error('Login Error:', err.response?.data || err.message);

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
                    handleLogin(true);
                }, 60000);
                return;
            }

            const errorMsg = err.response?.data?.detail || 'Login failed. Check your credentials.';
            setError(errorMsg);
            Alert.alert('Login Failed', errorMsg);
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
                        <Zap color={COLORS.primary} size={48} strokeWidth={2.5} />
                    </View>
                    <Text style={styles.title}>Welcome to NEEL</Text>
                    <Text style={styles.subtitle}>Your AI Productivity Evolution</Text>
                </View>

                <View style={styles.form}>
                    {error ? <Text style={styles.errorText}>{error}</Text> : null}

                    <View style={styles.inputWrapper}>
                        <User color={COLORS.textSecondary} size={20} style={styles.inputIcon} />
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
                            placeholder="Password"
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
                        style={styles.loginButton}
                        onPress={() => handleLogin(false)}
                        disabled={loading}
                    >
                        <LinearGradient
                            colors={['#8B5CF6', '#7C3AED']}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={styles.gradientButton}
                        >
                            {loading ? (
                                <ActivityIndicator color="#fff" />
                            ) : (
                                <>
                                    <Text style={styles.buttonText}>Authenticate</Text>
                                    <ArrowRight color="#fff" size={20} />
                                </>
                            )}
                        </LinearGradient>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.registerLink} onPress={() => router.push('/signup')}>
                        <Text style={styles.registerText}>
                            New to NEEL? <Text style={styles.registerHighlight}>Create Account</Text>
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
        width: 80,
        height: 80,
        borderRadius: 24,
        backgroundColor: 'rgba(139, 92, 246, 0.1)',
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: SPACING.md,
        borderWidth: 1,
        borderColor: 'rgba(139, 92, 246, 0.2)',
    },
    title: {
        fontSize: 28,
        fontWeight: '800',
        color: COLORS.text,
        letterSpacing: 0.5,
    },
    subtitle: {
        fontSize: 16,
        color: COLORS.textSecondary,
        marginTop: SPACING.xs,
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
    loginButton: {
        marginTop: SPACING.lg,
        height: 60,
        borderRadius: 16,
        overflow: 'hidden',
        elevation: 8,
        shadowColor: COLORS.primary,
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
    registerLink: {
        marginTop: SPACING.xl,
        alignItems: 'center',
    },
    registerText: {
        color: COLORS.textSecondary,
        fontSize: 14,
    },
    registerHighlight: {
        color: COLORS.primary,
        fontWeight: '700',
    },
});
