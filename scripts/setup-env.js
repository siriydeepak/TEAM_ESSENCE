#!/usr/bin/env node

/**
 * Environment Setup Script
 * 
 * This script runs after npm install to set up the development environment
 * for the TEAM_ESSENCE monorepo. It ensures that environment files exist
 * and provides helpful setup instructions.
 */

const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up TEAM_ESSENCE monorepo environment...');

// Check if frontend and backend directories exist
const frontendDir = path.join(process.cwd(), 'frontend');
const backendDir = path.join(process.cwd(), 'backend');

if (!fs.existsSync(frontendDir)) {
  console.log('⚠️  Frontend directory not found. Run migration tasks to set up the monorepo structure.');
}

if (!fs.existsSync(backendDir)) {
  console.log('⚠️  Backend directory not found. Run migration tasks to set up the monorepo structure.');
}

// Check for environment files
const envExample = path.join(process.cwd(), '.env.example');
const envFile = path.join(process.cwd(), '.env');

if (fs.existsSync(envExample) && !fs.existsSync(envFile)) {
  console.log('📝 Creating .env file from .env.example...');
  fs.copyFileSync(envExample, envFile);
  console.log('✅ .env file created. Please update it with your configuration.');
}

console.log('✨ Environment setup complete!');
console.log('');
console.log('Next steps:');
console.log('1. Update .env file with your API keys and configuration');
console.log('2. Run "npm run dev" to start both frontend and backend development servers');
console.log('3. Visit http://localhost:3000 to access the application');
console.log('');