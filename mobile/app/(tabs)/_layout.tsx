import React from 'react';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { Link, Tabs } from 'expo-router';
import { Pressable } from 'react-native';

import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { useClientOnlyValue } from '@/components/useClientOnlyValue';

import { LayoutDashboard, Brain, User as UserIcon } from 'lucide-react-native';
import { COLORS } from '../../constants/Theme';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textSecondary,
        tabBarStyle: {
          backgroundColor: '#050505',
          borderTopColor: 'rgba(255, 255, 255, 0.05)',
          height: 65,
          paddingBottom: 10,
        },
        headerShown: false,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'NEEL',
          tabBarIcon: ({ color }) => <LayoutDashboard color={color} size={24} />,
        }}
      />
      <Tabs.Screen
        name="two"
        options={{
          title: 'Intelligence',
          tabBarIcon: ({ color }) => <Brain color={color} size={24} />,
        }}
      />
    </Tabs>
  );
}
