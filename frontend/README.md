# AI-Powered Multimodal Dementia Detection System - Frontend

Next.js frontend for the dementia detection system.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Run development server:
```bash
npm run dev
```

4. Open browser:
```
http://localhost:3000
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js 14 App Router
│   ├── components/       # React components
│   │   ├── auth/        # Authentication components
│   │   ├── voice/       # Voice recording & analysis
│   │   ├── memory/      # Memory game components
│   │   ├── mri/         # MRI upload & results
│   │   ├── reports/     # Report viewers
│   │   └── dashboard/   # Dashboard components
│   ├── lib/             # Utility functions
│   └── styles/          # Global styles
├── public/              # Static assets
└── package.json         # Dependencies
```

## Tech Stack

- **Framework**: Next.js 14 (React 18)
- **Styling**: Tailwind CSS + Material-UI
- **State Management**: React Context + TanStack Query
- **Forms**: React Hook Form + Zod
- **Audio**: Web Audio API + Howler.js
