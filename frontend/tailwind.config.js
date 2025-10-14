/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./shared/src/**/*.{vue,js,ts,jsx,tsx}",
        "./driver-pwa/src/**/*.{vue,js,ts,jsx,tsx}",
        "./operations-pwa/src/**/*.{vue,js,ts,jsx,tsx}",
        "./safety-pwa/src/**/*.{vue,js,ts,jsx,tsx}",
        "./fleet-pwa/src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#e6ffe8',    // Lightest neon green tint
                    100: '#ccffce',   // Light neon green
                    200: '#99ff9d',   // Soft neon green
                    300: '#66ff6b',   // Medium neon green
                    400: '#4dff3a',   // Bright neon green
                    500: '#39ff14',   // TEMS Neon Green (Main)
                    600: '#2ecc10',   // Darker neon green
                    700: '#24990c',   // Deep neon green
                    800: '#196607',   // Very deep green
                    900: '#0f3304',   // Darkest green
                },
                charcoal: {
                    50: '#e8eaeb',    // Lightest charcoal
                    100: '#d1d5d7',   // Light charcoal
                    200: '#a3abb0',   // Soft charcoal
                    300: '#758188',   // Medium charcoal
                    400: '#475761',   // Dark charcoal
                    500: '#36454f',   // TEMS Charcoal Gray (Main)
                    600: '#2b373f',   // Deeper charcoal
                    700: '#20292f',   // Very deep charcoal
                    800: '#161c20',   // Darkest charcoal
                    900: '#0b0e10',   // Almost black
                },
                background: '#e0e2db',  // TEMS Light Gray Background
                success: '#39ff14',     // Neon green for success
                warning: '#ffcc00',     // Bright yellow for warnings
                danger: '#ff3366',      // Bright red for errors
                info: '#00ccff',        // Bright cyan for info
            },
            boxShadow: {
                'soft': '0 2px 15px -3px rgba(54, 69, 79, 0.12), 0 10px 20px -2px rgba(54, 69, 79, 0.08)',
                'card': '0 1px 3px 0 rgba(54, 69, 79, 0.15), 0 1px 2px 0 rgba(54, 69, 79, 0.10)',
                'lg': '0 10px 15px -3px rgba(54, 69, 79, 0.1), 0 4px 6px -2px rgba(54, 69, 79, 0.05)',
                'neon': '0 0 10px rgba(57, 255, 20, 0.5), 0 0 20px rgba(57, 255, 20, 0.3)',
                'neon-lg': '0 0 20px rgba(57, 255, 20, 0.6), 0 0 40px rgba(57, 255, 20, 0.4)',
            },
            backgroundImage: {
                'gradient-primary': 'linear-gradient(135deg, #39ff14 0%, #2ecc10 100%)',
                'gradient-charcoal': 'linear-gradient(135deg, #36454f 0%, #2b373f 100%)',
                'gradient-hero': 'linear-gradient(135deg, #36454f 0%, #2b373f 50%, #20292f 100%)',
            },
            fontFamily: {
                sans: [
                    'system-ui',
                    '-apple-system',
                    'BlinkMacSystemFont',
                    '"Segoe UI"',
                    'Roboto',
                    '"Helvetica Neue"',
                    'Arial',
                    'sans-serif',
                ],
            },
            spacing: {
                '18': '4.5rem',
                '88': '22rem',
                '128': '32rem',
            },
        },
    },
    plugins: [],
}
