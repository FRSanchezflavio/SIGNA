import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import * as url from 'url';
import * as fs from 'fs';
import { spawn, ChildProcess } from 'child_process';

let mainWindow: BrowserWindow | null = null;
let pythonProcess: ChildProcess | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    minWidth: 1366,
    minHeight: 768,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false,
    },
    icon: path.join(__dirname, '../../public/icon.png'),
    title: 'SIGNA - Sistema de Inteligencia y Gestión de Análisis',
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, '../renderer/index.html'),
        protocol: 'file:',
        slashes: true,
      })
    );
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startPythonBackend() {
  const pythonScript = path.join(__dirname, '../../backend/app.py');

  let pythonExecutable = 'python';
  const venvPath = path.join(__dirname, '../../backend/venv');
  const venvPython =
    process.platform === 'win32'
      ? path.join(venvPath, 'Scripts/python.exe')
      : path.join(venvPath, 'bin/python');

  if (fs.existsSync(venvPython)) {
    pythonExecutable = venvPython;
    console.log(`Using Python from venv: ${pythonExecutable}`);
  } else {
    console.log('Using global Python');
  }

  pythonProcess = spawn(pythonExecutable, [pythonScript]);

  pythonProcess.stdout?.on('data', data => {
    console.log(`Python Backend: ${data}`);
  });

  pythonProcess.stderr?.on('data', data => {
    console.error(`Python Backend Error: ${data}`);
  });

  pythonProcess.on('close', code => {
    console.log(`Python Backend exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  createWindow();
  startPythonBackend();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }

  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// IPC Handlers
ipcMain.handle('get-app-path', () => {
  return app.getPath('userData');
});

ipcMain.handle('get-version', () => {
  return app.getVersion();
});
