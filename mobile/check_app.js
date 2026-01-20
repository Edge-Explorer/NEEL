const fs = require('fs');
const path = require('path');

console.log('🔍 NEEL Mobile App Diagnostic Check\n');

// Check if required files exist
const requiredFiles = [
    'app/index.tsx',
    'app/login.tsx',
    'app/signup.tsx',
    'app/_layout.tsx',
    'app/(tabs)/_layout.tsx',
    'services/api.js',
    'constants/Theme.js',
];

console.log('📁 Checking required files:');
requiredFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    const exists = fs.existsSync(filePath);
    console.log(`  ${exists ? '✅' : '❌'} ${file}`);
});

// Check package.json dependencies
console.log('\n📦 Checking key dependencies:');
const packageJson = require('./package.json');
const keyDeps = [
    'expo-router',
    'expo-linear-gradient',
    'lucide-react-native',
    '@react-native-async-storage/async-storage',
    'axios',
];

keyDeps.forEach(dep => {
    const version = packageJson.dependencies[dep];
    console.log(`  ${version ? '✅' : '❌'} ${dep}: ${version || 'MISSING'}`);
});

console.log('\n✨ Diagnostic complete!');
