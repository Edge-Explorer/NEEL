import { useEffect } from 'react';
import { useRouter } from 'expo-router';
import { View, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import apiClient from '../services/api';

export default function Index() {
    const router = useRouter();

    useEffect(() => {
        checkAuth();
    }, []);



    const checkAuth = async () => {
        try {
            const token = await AsyncStorage.getItem('userToken');
            if (token) {
                // Verify token with backend
                try {
                    await apiClient.get('/api/auth/me');
                    router.replace('/(tabs)');
                } catch (e) {
                    console.log('Token invalid, redirecting to login');
                    await AsyncStorage.removeItem('userToken');
                    router.replace('/login');
                }
            } else {
                router.replace('/login');
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            router.replace('/login');
        }
    };

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#050505' }}>
            <ActivityIndicator size="large" color="#8B5CF6" />
        </View>
    );
}
