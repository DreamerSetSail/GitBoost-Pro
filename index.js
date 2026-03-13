#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the path to the Python script
const pythonScript = path.join(__dirname, 'gitboost_pro.py');

// Check if Python is installed
function checkPython() {
  try {
    execSync('python --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    try {
      execSync('python3 --version', { stdio: 'ignore' });
      return true;
    } catch (error) {
      return false;
    }
  }
}

// Run the Python script
function runGitBoost() {
  console.log('🚀 Starting GitBoost Pro...');
  console.log('=' .repeat(60));
  
  try {
    // Check if Python is available
    if (!checkPython()) {
      console.error('❌ Error: Python is not installed. Please install Python 3.6 or higher.');
      process.exit(1);
    }
    
    // Check if the Python script exists
    if (!fs.existsSync(pythonScript)) {
      console.error('❌ Error: gitboost_pro.py not found.');
      process.exit(1);
    }
    
    // Execute the Python script
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
    execSync(`${pythonCommand} "${pythonScript}"`, { stdio: 'inherit' });
  } catch (error) {
    console.error('❌ Error running GitBoost Pro:', error.message);
    process.exit(1);
  }
}

// Run GitBoost Pro
runGitBoost();