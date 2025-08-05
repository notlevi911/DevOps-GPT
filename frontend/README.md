# DevOps GPT Frontend

A modern React TypeScript frontend for the DevOps GPT application - an AI-powered DevOps assistant.

## Features

- 💬 **Chat Interface**: Interactive chat with AI assistant
- 📁 **Repository Upload**: Connect GitHub repos or upload files
- 🎯 **Smart Tabs**: Suggestions, Monitoring, Testing, and Settings
- 📱 **Responsive Design**: Works on desktop and mobile
- 🎨 **Modern UI**: Glassmorphism design with smooth animations

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Lucide React** for beautiful icons
- **CSS3** with modern features (backdrop-filter, gradients)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── App.tsx          # Main application component
├── App.css          # Application styles
├── main.tsx         # Application entry point
└── index.css        # Global styles
```

## Features Overview

### Chat Interface
- Real-time messaging with AI assistant
- Typing indicators
- Message timestamps
- Responsive design

### Repository Integration
- GitHub repository URL input
- File upload support
- Drag and drop functionality

### Smart Tabs
- **Suggestions**: AI-powered recommendations for Docker, K8s, CI/CD
- **Monitoring**: Prometheus alerts and Grafana dashboards
- **Testing**: Automated test generation
- **Settings**: Configuration and preferences

## API Integration

The frontend is configured to proxy API requests to `http://localhost:8000` (your FastAPI backend). Update the proxy configuration in `vite.config.ts` if needed.

## Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`

### Deploy to Netlify
1. Build the project: `npm run build`
2. Deploy the `dist` folder to Netlify

## Customization

### Styling
- Modify `src/index.css` for global styles
- Update `src/App.css` for component-specific styles
- Use CSS custom properties for theming

### Adding New Features
- Create new components in `src/components/`
- Add new tabs in the `tabs` array in `App.tsx`
- Implement API calls using axios

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
