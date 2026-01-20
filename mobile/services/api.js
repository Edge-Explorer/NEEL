import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://neel-backend-v2.loca.lt'; // New stable tunnel address v2

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Automatically add JWT token to every request
apiClient.interceptors.request.use(async (config) => {
    const token = await AsyncStorage.getItem('userToken');
    console.log(`🔵 API Request: ${config.method.toUpperCase()} ${config.baseURL}${config.url}`);
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        console.log(`   ✅ Token present`);
    } else {
        console.log(`   ℹ️  No token (expected for login/signup)`);
    }
    return config;
}, (error) => {
    console.error('❌ Request interceptor error:', error);
    return Promise.reject(error);
});

// Handle 401 Unauthorized errors globally
apiClient.interceptors.response.use(
    (response) => {
        console.log(`✅ Response: ${response.status} ${response.config.url}`);
        return response;
    },
    async (error) => {
        if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
            console.error('⏱️  TIMEOUT: Backend took too long to respond');
            console.error('   Check: Is backend running? Is IP correct?');
        } else if (error.message?.includes('Network Error')) {
            console.error('🌐 NETWORK ERROR: Cannot reach backend');
            console.error('   Check: Are phone and PC on same WiFi?');
            console.error('   Check: Is Windows Firewall blocking port 8000?');
        } else if (error.response && error.response.status === 401) {
            console.log('🔒 Session expired or invalid token. Logging out...');
            await AsyncStorage.removeItem('userToken');
        } else if (error.response) {
            console.error(`❌ Server Error: ${error.response.status} - ${error.response.data?.detail || 'Unknown error'}`);
        } else {
            console.error('❌ Unknown Error:', error.message);
        }
        return Promise.reject(error);
    }
);

export default apiClient;
